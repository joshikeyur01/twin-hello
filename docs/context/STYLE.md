# Style

Inherits from the `twin-*` portfolio-wide conventions in
[`twin-arch`](https://github.com/joshikeyur01/twin-arch/blob/main/docs/style.md).
Only deltas and specifics are documented here.

## Python

- Target 3.12. Prefer `match` over long `if/elif` chains for message dispatch.
- `uv` for dependency management. Runtime deps in `pyproject.toml`; dev deps
  in the `[dependency-groups.dev]` table.
- Pydantic v2 for all message contracts. Never pass raw dicts across module
  boundaries.
- Async where I/O-bound (MQTT client), sync where CPU-bound. No mixing inside
  one module.

## ROS 2

- `rclpy` only. No C++ in this repo.
- QoS profiles set explicitly at subscription creation; do not rely on defaults.
- Use `rclpy.executors.SingleThreadedExecutor` unless profiled otherwise.

## MQTT

- Topic scheme: `twin/<asset>/<subsystem>/<component>/<metric>`.
- Payloads are JSON, one field per message. Yes, this is verbose. It makes
  Telegraf and Grafana trivial. When it stops being trivial, revisit.
- QoS 0 for telemetry. QoS 1 will be considered only when we have commands.

## Tests

- `pytest` with `pytest-asyncio` in auto mode.
- One integration test that spins up an in-process MQTT broker and asserts
  end-to-end message shape. Slow tests marked `@pytest.mark.slow` and skipped
  by default in CI's fast lane.

## Commits and branches

- Conventional Commits. Scope is the top-level directory: `feat(bridge): ...`.
- Trunk-based. Feature branches merged via squash, PR title = commit message.
- Tag releases `v0.x.y`. Generate `CHANGELOG.md` with `git-cliff` on tag.
