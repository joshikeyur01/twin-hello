# Bootstrap prompts

Paste the block for the project you want into a fresh AI coding
session, at the root of an empty directory. Each prompt inherits the
conventions from this `twin-hello` scaffold.

---

## Shared preamble (paste before any project-specific prompt)

> You are helping me scaffold the next project in my `twin-*` digital-twin
> portfolio. The conventions to inherit from my `twin-hello` reference repo:
>
> - **Stack:** Python 3.12, Pydantic v2, FastAPI, `uv`, `just`, Docker Compose,
>   Apache-2.0.
> - **Quality gates:** `ruff` (lint + format), `mypy --strict`, `pytest` +
>   `pytest-asyncio`, GitHub Actions CI, pre-commit.
> - **Repo skeleton:** `README.md`, `AGENTS.md`, `CHANGELOG.md`,
>   `docs/context/{VISION,ARCHITECTURE,STYLE,ROADMAP}.md`, `docs/adr/`,
>   `src/`, `tests/`, `deploy/`, `justfile`, `docker-compose.yml`,
>   `pyproject.toml`, `.github/workflows/ci.yml`, `.pre-commit-config.yaml`,
>   `.gitignore`, `LICENSE`.
> - **Architecture rule:** every project's `ARCHITECTURE.md` uses the same
>   five layers: L1 physical, L2 transport, L3 information model, L4 services,
>   L5 application.
> - **Docs come first.** Write `VISION.md`, `ARCHITECTURE.md`, and `ROADMAP.md`
>   before any source file. Then scaffold code that matches them.
> - **ADRs for design decisions.** Any new dependency or cross-layer choice
>   gets an ADR in `docs/adr/`.
> - **AGENTS.md** tells future AI sessions the rules of engagement (mission,
>   stack, non-negotiable conventions, what to refuse).
>
> Produce files in dependency order (docs → config → code → tests → CI). After
> each file, wait for me to say `next` before generating the following one, so
> I can review as we go.

---

## Project 2 · `twin-services`

> Bootstrap `twin-services`. This forks the `twin-hello` structure and
> decomposes the twin into four containerised microservices:
>
> - `telemetry-svc` — ingests MQTT, writes to InfluxDB.
> - `state-svc` — computes derived state (end-effector pose, velocity RMS),
>   exposes gRPC.
> - `command-svc` — accepts REST commands, publishes MQTT setpoints.
> - `viz-svc` — serves a React + react-three-fiber viewer of the live twin.
>
> Shared Pydantic + protobuf contracts live in a top-level `contracts/`
> package that all services depend on. Each service has its own Dockerfile,
> `/healthz`, and `/metrics`. Include ADRs for:
> (a) gRPC vs REST between services, (b) schema-evolution strategy,
> (c) health-check design.
>
> Success criterion: killing any single service degrades gracefully and
> Grafana shows it.

---

## Project 3 · `twin-aas`

> Bootstrap `twin-aas`. Same UR5 twin exposed through three parallel
> information-model adapters so we can compare them empirically:
>
> - `adapters/aas-basyx/` — Eclipse BaSyx AAS server with submodels
>   `Nameplate`, `TechnicalData`, `OperationalData`, `Capability`, live-populated
>   from MQTT.
> - `adapters/opcua/` — an OPC-UA server via `asyncua` exposing an equivalent
>   address space.
> - `adapters/mqtt-raw/` — the `twin-hello` baseline for reference.
>
> A `comparison/` package queries "current end-effector pose" through each
> adapter and records latency, verbosity, and client LOC. Deliverable:
> `docs/COMPARISON.md` with a filled matrix backed by working benchmarks.

---

## Project 4 · `twin-anomaly`

> Bootstrap `twin-anomaly`. Extend the `twin-services` stack with three new
> components:
>
> - `fault-injector/` — a ROS 2 node that on command applies parameterised
>   faults to the simulated arm (joint-friction spike, encoder noise, stuck
>   joint, comms drop-out).
> - `data-pipeline/` — batches InfluxDB telemetry into labelled parquet
>   windows.
> - `services/anomaly-svc/` — FastAPI service that loads a trained model
>   (start with Isolation Forest, then LSTM autoencoder) and exposes
>   `POST /score`.
>
> Reproducible training notebooks in `notebooks/`, model artefacts versioned
> with git-lfs in `models/`, Grafana panel that overlays anomaly alerts on
> joint traces. ADRs for feature-engineering choices and model-vs-rule
> trade-offs.

---

## Project 5 · `twin-fleet`

> Bootstrap `twin-fleet`. Generalise the `twin-services` stack from one robot
> to N. Use ROS 2 namespacing (`/robot_1/joint_states` etc.). Add:
>
> - `services/fleet-svc/` — registry of active twins, `GET /fleet`,
>   coordinated commands (e.g. "all robots home").
> - Per-robot Grafana row templates so the dashboard scales automatically.
> - `loadtest/` — script that ramps 1→20 robots and records p50/p95/p99
>   latency, MQTT broker CPU, InfluxDB write throughput.
>
> Deliverable: an ADR documenting the observed scaling breakpoint and the fix.

---

## Project 6 · `twin-cubesat`

> Bootstrap `twin-cubesat`. Translate the terrestrial stack into the space
> domain to expose what standards miss.
>
> - Gazebo world: 3U target CubeSat + servicer spacecraft with a 6-DOF
>   manipulator.
> - Repair task as a state machine: `APPROACH → GRAPPLE → DIAGNOSE →
>   REPLACE_PANEL → RELEASE → DEPART`.
> - `orbital/` — Poliastro-based propagation service updating servicer state
>   at 1 Hz.
> - `ccsds-comms/` — frames all twin telemetry as CCSDS Space Packets with
>   configurable delay, jitter, and blackout windows.
> - `services/mission-svc/` — orchestrates the state machine.
> - `web/mission-viz/` — dual-view UI showing orbital track + manipulator
>   scene.
>
> Reuse `twin-services` services where possible. Deliverable:
> `docs/DELTA.md` — what had to change vs the terrestrial baseline and why.
> This is the direct code companion to the thesis's M4 milestone.

---

## Project 7 · `twin-arch` (portfolio meta-repo)

> Bootstrap `twin-arch`. A MkDocs Material site hosted via GitHub Pages
> that ties every `twin-*` repo together. Sections:
>
> - The 5-layer stack, explained.
> - All ADRs from all six repos, consolidated by topic.
> - A matrix mapping thesis service-taxonomy categories to the repo that
>   demonstrates each.
> - Cross-links to each repo's live demo GIF.
>
> No source code, just docs. This is the artefact that survives the thesis.
