"""Bridge entrypoint.

Subscribes to /joint_states via rclpy, validates each message with Pydantic,
and republishes one MQTT message per joint per field. Also serves /healthz.

Kept deliberately small (~150 lines) so the whole pipeline is legible in
one sitting.
"""

from __future__ import annotations

import asyncio
import json
import signal
import threading
from contextlib import suppress
from typing import Any

import aiomqtt
import structlog
import uvicorn
from fastapi import FastAPI

from bridge.config import BridgeConfig
from bridge.models import JointSample, JointStateMessage

log = structlog.get_logger()


def build_health_app() -> FastAPI:
    app = FastAPI(title="twin-hello bridge")

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    return app


async def publish_sample(client: aiomqtt.Client, sample: JointSample, asset: str) -> None:
    """Publish one joint sample as three MQTT messages (position, velocity, effort)."""
    prefix = sample.topic_prefix(asset)
    payloads: dict[str, float] = {
        f"{prefix}/position": sample.position,
        f"{prefix}/velocity": sample.velocity,
        f"{prefix}/effort": sample.effort,
    }
    for topic, value in payloads.items():
        await client.publish(
            topic,
            payload=json.dumps({"value": value, "stamp_ns": sample.stamp_ns}),
            qos=0,
        )


async def mqtt_worker(config: BridgeConfig, queue: asyncio.Queue[JointStateMessage]) -> None:
    """Consume validated messages and publish them. Reconnect on failure."""
    while True:
        try:
            async with aiomqtt.Client(config.mqtt_host, port=config.mqtt_port) as client:
                log.info("mqtt.connected", host=config.mqtt_host, port=config.mqtt_port)
                while True:
                    msg = await queue.get()
                    for sample in msg.per_joint():
                        await publish_sample(client, sample, config.asset_name)
        except aiomqtt.MqttError as exc:
            log.warning("mqtt.reconnect", error=str(exc))
            await asyncio.sleep(2.0)


def start_ros_subscriber(queue: asyncio.Queue[JointStateMessage], config: BridgeConfig) -> Any:
    """Start rclpy on a background thread and forward /joint_states to the queue.

    Imported lazily so that unit tests can run without a ROS 2 environment.
    """
    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import JointState

    loop = asyncio.get_event_loop()

    class BridgeNode(Node):  # type: ignore[misc]
        def __init__(self) -> None:
            super().__init__("twin_hello_bridge")
            self.create_subscription(JointState, config.ros_topic, self._on_msg, 10)

        def _on_msg(self, msg: JointState) -> None:
            try:
                validated = JointStateMessage(
                    stamp_ns=msg.header.stamp.sec * 1_000_000_000 + msg.header.stamp.nanosec,
                    names=list(msg.name),
                    positions=list(msg.position),
                    velocities=list(msg.velocity),
                    efforts=list(msg.effort),
                )
            except Exception as exc:  # noqa: BLE001 — bridge must not die on bad msgs
                log.warning("bridge.validation_failed", error=str(exc))
                return
            asyncio.run_coroutine_threadsafe(queue.put(validated), loop)

    def _spin() -> None:
        rclpy.init()
        node = BridgeNode()
        try:
            rclpy.spin(node)
        finally:
            node.destroy_node()
            rclpy.shutdown()

    thread = threading.Thread(target=_spin, name="rclpy-spin", daemon=True)
    thread.start()
    return thread


async def main_async() -> None:
    config = BridgeConfig.from_env()
    queue: asyncio.Queue[JointStateMessage] = asyncio.Queue(maxsize=1000)

    start_ros_subscriber(queue, config)

    health_task = asyncio.create_task(
        uvicorn.Server(
            uvicorn.Config(build_health_app(), host="0.0.0.0", port=config.health_port, log_level="warning")
        ).serve()
    )
    mqtt_task = asyncio.create_task(mqtt_worker(config, queue))

    stop = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set)

    await stop.wait()
    log.info("bridge.shutdown")
    for task in (health_task, mqtt_task):
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task


def main() -> None:
    structlog.configure(processors=[structlog.processors.JSONRenderer()])
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
