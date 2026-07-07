"""Unit tests for the bridge Pydantic contracts.

These do not require ROS 2 or an MQTT broker.
"""

from __future__ import annotations

import pytest

from bridge.models import JointStateMessage


def _sample_msg(**overrides: object) -> JointStateMessage:
    defaults = dict(
        stamp_ns=1_700_000_000_000_000_000,
        names=["shoulder_pan", "shoulder_lift"],
        positions=[0.1, 0.2],
        velocities=[0.0, 0.0],
        efforts=[0.5, 0.5],
    )
    defaults.update(overrides)
    return JointStateMessage(**defaults)  # type: ignore[arg-type]


def test_per_joint_fans_out_correctly() -> None:
    msg = _sample_msg()
    samples = msg.per_joint()
    assert [s.name for s in samples] == ["shoulder_pan", "shoulder_lift"]
    assert samples[0].position == pytest.approx(0.1)
    assert samples[1].effort == pytest.approx(0.5)


def test_topic_prefix_uses_asset_name() -> None:
    sample = _sample_msg().per_joint()[0]
    assert sample.topic_prefix("ur5") == "twin/ur5/joint/shoulder_pan"
    assert sample.topic_prefix("cubesat_arm") == "twin/cubesat_arm/joint/shoulder_pan"


def test_mismatched_field_lengths_raise() -> None:
    msg = _sample_msg(velocities=[0.0])  # one short
    with pytest.raises(ValueError, match="field lengths"):
        msg.per_joint()


def test_negative_stamp_rejected() -> None:
    with pytest.raises(ValueError):
        _sample_msg(stamp_ns=-1)
