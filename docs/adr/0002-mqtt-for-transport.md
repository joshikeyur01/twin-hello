# 2. MQTT for the L2 transport layer

Date: 2026-06-22
Status: Accepted

## Context

The bridge needs to move `/joint_states` from ROS 2 DDS into a form that
non-ROS consumers (Telegraf, dashboards, future services) can consume without
inheriting ROS-specific type systems or QoS profiles.

Candidates: raw DDS bridge, gRPC streaming, MQTT, Kafka.

## Decision

Use MQTT (Mosquitto broker).

## Consequences

Positive:
- One line of client code to publish or subscribe in any language.
- Telegraf has first-class MQTT input; no glue code needed.
- Broad Industry 4.0 tooling ecosystem, aligned with thesis themes.
- Low overhead at the 50 Hz × ~20 topics scale of this repo.

Negative:
- No native schema. We mitigate by validating with Pydantic on the bridge
  side and by keeping payloads to single-field JSON.
- No native auth or encryption in the default config. Acceptable on
  localhost; `twin-services` will add mTLS.
- QoS 0 means we tolerate drops. Acceptable for telemetry; will be revisited
  when a command path exists.

## Alternatives considered

- **DDS bridge:** rejected because it forces every consumer to speak ROS 2.
- **gRPC:** rejected because Telegraf/Grafana integration is worse and the
  request/response model is a poor fit for one-way fan-out telemetry.
- **Kafka:** rejected as overkill for one robot; will be revisited in
  `twin-fleet` if MQTT breaks under load.
