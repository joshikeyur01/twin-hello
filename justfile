# twin-hello task runner. `just` for a listing.

set shell := ["bash", "-euo", "pipefail", "-c"]

# ─── setup ─────────────────────────────────────────────────────────────────

# Install dev dependencies with uv.
install:
    uv sync --all-groups

# ─── quality gates ─────────────────────────────────────────────────────────

lint:
    uv run ruff check .
    uv run ruff format --check .

format:
    uv run ruff format .
    uv run ruff check --fix .

typecheck:
    uv run mypy src tests

test:
    uv run pytest

check: lint typecheck test

# ─── infra ─────────────────────────────────────────────────────────────────

# Start Mosquitto, Telegraf, InfluxDB, Grafana.
up:
    docker compose up -d
    @echo "Grafana:  http://localhost:3000 (admin/admin)"
    @echo "InfluxDB: http://localhost:8086"

down:
    docker compose down

# Smoke check: are all infra endpoints responding?
healthz:
    @curl -sf http://localhost:3000/api/health >/dev/null && echo "grafana ✓" || echo "grafana ✗"
    @curl -sf http://localhost:8086/health   >/dev/null && echo "influx  ✓" || echo "influx  ✗"
    @docker exec twin-mosquitto mosquitto_sub -t '$$SYS/broker/uptime' -C 1 >/dev/null 2>&1 \
       && echo "mqtt    ✓" || echo "mqtt    ✗"

# ─── sim + bridge ──────────────────────────────────────────────────────────

# Launch Gazebo with the UR5 world. Requires ROS 2 Jazzy sourced.
sim:
    ros2 launch sim/launch/ur5_demo.launch.py

# Run the bridge locally (requires ROS 2 sourced and `just up`).
bridge:
    MQTT_HOST=localhost uv run python -m bridge.main

# Move the arm through a sine trajectory for the demo GIF.
demo:
    uv run python sim/scripts/sine_trajectory.py

# Record a 15s screencast for the README. Requires peek.
record:
    peek --start-timer 3 --duration 15 --output-format gif \
         --output docs/demo/twin-hello.gif
