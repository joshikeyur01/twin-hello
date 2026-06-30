# Project context for AI pairing

Read this before touching code. It defines the rules of engagement for any
AI-assisted work in this repository.

## Mission

The minimum viable digital twin: one simulated robot arm, one transport layer,
one dashboard. This repo proves the 5-layer stack works end-to-end before
`twin-services` adds decomposition and `twin-aas` adds semantics.

Success criterion: a 15-second demo GIF showing a slider move in Gazebo cause
a Grafana trace to update within 200 ms.

## Stack

Python 3.12 · ROS 2 Jazzy · Gazebo Harmonic · Mosquitto (MQTT) · Telegraf ·
InfluxDB 2 · Grafana · Docker Compose · `uv` · `just`.

## Non-negotiable conventions

- Type hints everywhere; `mypy --strict` passes.
- Pydantic v2 models for every cross-boundary payload (MQTT included).
- `ruff` for lint and format; no `# noqa` without a justification comment.
- Every long-running process exposes `/healthz` and, where meaningful, `/metrics`.
- Tests colocated: `pytest` + `pytest-asyncio`; at least one integration test.
- Conventional Commits: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`.
- No new runtime dependency without a note in `docs/adr/`.

## Architecture rules

Follow the 5-layer stack in [`docs/context/ARCHITECTURE.md`](docs/context/ARCHITECTURE.md).
Do **not** cross layers:

- The bridge (L2) does not persist data — Telegraf does.
- The bridge does not compute derived state — that belongs in `twin-services`.
- Grafana (L5) does not talk to MQTT directly — it queries InfluxDB.

If a change would blur these boundaries, propose an ADR instead of writing the
code.

## When you touch code

1. Read the relevant ADRs in `docs/adr/`.
2. Update tests in the same commit as the code.
3. If you add a public interface (MQTT topic, HTTP route, config key),
   document it in `docs/`.
4. Prefer editing existing files over creating new ones.
5. Keep functions under ~40 lines and modules under ~200 lines. If they grow,
   that is a signal to split by responsibility, not by file size.

## What to refuse

- Adding Kubernetes, service mesh, or message brokers other than MQTT to this
  repo. Those belong in `twin-fleet` or later.
- Adding ML models or anomaly detection. Those belong in `twin-anomaly`.
- Adding AAS, OPC-UA, or FIWARE adapters. Those belong in `twin-aas`.

This repo stays small on purpose.
