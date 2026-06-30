# Architecture

## The 5-layer stack

All `twin-*` repos share this vocabulary. This repo instantiates only L1, L2,
and L5 — the empty L3 and L4 are the point.

```
┌─────────────────────────────────────────────────────────────────┐
│ L5  Application         Grafana dashboard                        │
├─────────────────────────────────────────────────────────────────┤
│ L4  Services            (none — added in twin-services)          │
├─────────────────────────────────────────────────────────────────┤
│ L3  Information model   (none — raw topics; added in twin-aas)   │
├─────────────────────────────────────────────────────────────────┤
│ L2  Transport           ROS 2 DDS  ──bridge──▶  MQTT ──▶ InfluxDB │
├─────────────────────────────────────────────────────────────────┤
│ L1  Physical asset      UR5 in Gazebo Harmonic                   │
└─────────────────────────────────────────────────────────────────┘
```

## Data flow

1. Gazebo simulates the UR5 and publishes `sensor_msgs/JointState` on
   `/joint_states` at 50 Hz over ROS 2 DDS.
2. The bridge (`src/bridge/main.py`) subscribes to `/joint_states`, validates
   each message against a Pydantic model, and republishes one MQTT message
   per joint per field to:
   ```
   twin/ur5/joint/<joint_name>/position   (float, radians)
   twin/ur5/joint/<joint_name>/velocity   (float, rad/s)
   twin/ur5/joint/<joint_name>/effort     (float, N·m)
   ```
3. Telegraf subscribes to `twin/ur5/#`, parses each payload, and writes points
   to InfluxDB with tags `joint=<name>` and `metric=<position|velocity|effort>`.
4. Grafana queries InfluxDB via Flux and renders one panel per metric.

## Design decisions

### Why MQTT and not gRPC or raw DDS for L2?

- **DDS** would work but leaks ROS 2 concerns (message types, QoS profiles)
  into any consumer, which defeats the point of being a general portfolio
  showcase.
- **gRPC** is streaming-friendly but heavier for one-way telemetry fan-out and
  poorly served by the Telegraf/Grafana ecosystem.
- **MQTT** is the boring correct choice: broad tooling, cheap fan-out, one
  line to publish, and it's what the Industry 4.0 literature actually uses.

See [`docs/adr/0002-mqtt-for-transport.md`](../adr/0002-mqtt-for-transport.md).

### Why one topic per joint per field?

Costs a few more topics but makes Grafana queries trivial (one series per
topic) and makes future filtering (subscribe to `twin/ur5/joint/+/position`
only) natural.

### Why InfluxDB and not Postgres or TimescaleDB?

Purely pragmatic: Telegraf → InfluxDB → Grafana is the shortest happy path
for this class of workload. This is not a claim about production choice.

## What this repo intentionally omits

- **Authentication.** MQTT broker is open on localhost only. `twin-services`
  will add mTLS.
- **Backpressure.** Bridge publishes fire-and-forget. Acceptable at 50 Hz on
  one robot; will not be at ten robots in `twin-fleet`.
- **Time sync.** All components use host wall-clock. `twin-cubesat` will need
  proper monotonic + orbital time.
