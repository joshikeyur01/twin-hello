# Roadmap

Four phases, one week total. If a phase slips more than two days, cut scope
inside the phase — do not push the next phase.

## Phase 0 · Scaffold (day 1)

- [x] Repo skeleton, licence, `.gitignore`, pre-commit.
- [x] `pyproject.toml` with `uv`, ruff, mypy, pytest.
- [x] CI: lint + type-check + tests on push.
- [x] Empty `docker-compose.yml` that starts Mosquitto, InfluxDB, Grafana,
      Telegraf and passes a `just healthz` smoke check.

**DoD:** `just up && just healthz` returns green on a fresh clone.

## Phase 1 · Sim (days 2–3)

- [ ] Gazebo Harmonic world with a UR5 loaded from open-source URDF.
- [ ] Sine-trajectory publisher on `/joint_states` — no bridge yet.
- [ ] `just sim` reproducibly launches the world.

**DoD:** `ros2 topic echo /joint_states` shows joint values changing.

## Phase 2 · Bridge (days 4–5)

- [ ] `rclpy` node subscribes to `/joint_states`, validates against Pydantic
      model, publishes to MQTT one topic per joint per field.
- [ ] Structured logging (`structlog`), `/healthz` served on :8080.
- [ ] Integration test with in-process MQTT broker.

**DoD:** `mosquitto_sub -t 'twin/ur5/#' -v` prints values matching Gazebo.

## Phase 3 · Observation (days 6–7)

- [ ] Telegraf pipeline MQTT → InfluxDB.
- [ ] Grafana dashboard provisioned from JSON in `deploy/grafana/dashboards/`.
- [ ] README GIF recorded and committed.
- [ ] `WHAT_I_LEARNED.md` filled in.

**DoD:** Fresh clone → `just up && just sim && just bridge && just demo`
produces the README GIF within 5 minutes.

## Explicit non-goals for this repo

- Command path (Gazebo ← MQTT). Belongs in `twin-services`.
- Multi-robot. Belongs in `twin-fleet`.
- Semantic model. Belongs in `twin-aas`.
- Any anomaly detection. Belongs in `twin-anomaly`.
