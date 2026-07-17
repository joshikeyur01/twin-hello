# twin-hello

> The minimum viable digital twin: one simulated robot arm, one transport
> layer, one dashboard. First rung of the [`twin-*`](https://github.com/joshikeyur01?tab=repositories&q=twin-)
> portfolio.

![demo](docs/demo/twin-hello.gif)

## What this is

A UR5 robot arm simulated in Gazebo Harmonic, streaming joint telemetry over
MQTT into InfluxDB, visualised in Grafana. End-to-end in under 200 lines of
application code.

Deliberately does **not** include: microservices, information models,
prediction, or fleet management — those live in follow-on repos
(`twin-services`, `twin-aas`, `twin-anomaly`, `twin-fleet`, `twin-cubesat`).

## Architecture (5-layer stack)

| Layer | Component |
|-------|-----------|
| L5 Application | Grafana |
| L4 Services | *(none — this is the baseline)* |
| L3 Information model | *(none — raw topics)* |
| L2 Transport | ROS 2 DDS → MQTT bridge |
| L1 Physical / simulated | UR5 in Gazebo Harmonic |

See [`docs/context/ARCHITECTURE.md`](docs/context/ARCHITECTURE.md).

## Quick start

Prerequisites: Docker, Docker Compose, [`just`](https://github.com/casey/just),
and (for local ROS work) ROS 2 Jazzy + Gazebo Harmonic.

```bash
just up          # start Mosquitto, Telegraf, InfluxDB, Grafana
just sim         # launch Gazebo with the UR5 world
just bridge      # run the rclpy → MQTT bridge
just demo        # move the arm through a sine trajectory
```

Then open <http://localhost:3000> (Grafana, `admin`/`admin`) to see joint
positions update live.

## Repo layout

```
src/bridge/           # rclpy node that mirrors /joint_states → MQTT
sim/                  # Gazebo world + URDF
deploy/               # Mosquitto, Telegraf, Grafana provisioning
docs/context/         # vision, architecture, style, roadmap
docs/adr/             # architecture decision records
tests/                # pytest suite
```

## What I learned

*(fill in as you go — recruiters read this section first)*

## Licence

Apache-2.0 — see [`LICENSE`](LICENSE).
