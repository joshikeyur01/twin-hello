# Vision

## Why this repo exists

The digital-twin literature is full of grand architecture diagrams and short
on running code. Before I can meaningfully write about service-oriented
twins, standards, and in-orbit servicing, I need to feel the shape of the
basic loop in my hands: physical asset → transport → observation.

This repo is that loop, made small on purpose.

## What "done" looks like

- `just up && just sim && just bridge && just demo` works on a fresh clone
  in under five minutes.
- Grafana shows six live joint traces with less than 200 ms end-to-end latency
  at 50 Hz.
- The README's demo GIF is under 15 seconds and shows the full pipeline.
- The bridge has a passing `pytest` suite including one integration test that
  publishes a synthetic `JointState` and asserts the MQTT message shape.
- One ADR written explaining why MQTT was chosen over gRPC or raw DDS for
  this layer.

## What "done" does not look like

- A microservice architecture. That's `twin-services`.
- Semantic modelling. That's `twin-aas`.
- Anomaly detection. That's `twin-anomaly`.
- Multiple robots. That's `twin-fleet`.
- Anything orbital. That's `twin-cubesat`.

Feature creep here is failure, not success.

## Audience

Three people, in order:

1. **Me, six months from now**, needing to remember why I made these choices
   when I fork this scaffold for the next project.
2. **A thesis examiner** who wants to see that the architecture I write about
   is grounded in something that runs.
3. **A recruiter or PI** who scans the README, watches the GIF, and decides
   in ninety seconds whether to keep reading.

If a change doesn't help at least one of those three, it doesn't ship.
