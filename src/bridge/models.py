"""Pydantic contracts for the bridge.

Every payload that crosses a module boundary is one of these models. Raw
dicts stop at the ROS 2 subscription callback.
"""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class JointStateMessage(BaseModel):
    """Validated snapshot of a `sensor_msgs/JointState` at one instant."""

    stamp_ns: int = Field(..., ge=0, description="ROS clock time in nanoseconds.")
    names: list[str] = Field(..., min_length=1)
    positions: list[float]
    velocities: list[float]
    efforts: list[float]

    @field_validator("velocities", "efforts")
    @classmethod
    def _same_length_as_names(cls, v: list[float], info: object) -> list[float]:
        # Pydantic doesn't expose sibling fields cleanly in v2 field validators,
        # so lengths are checked again in the model validator below.
        return v

    def per_joint(self) -> list[JointSample]:
        """Fan out into one sample per joint for MQTT publishing."""
        n = len(self.names)
        if not (len(self.positions) == len(self.velocities) == len(self.efforts) == n):
            raise ValueError("JointState field lengths must all match names length.")
        return [
            JointSample(
                name=self.names[i],
                stamp_ns=self.stamp_ns,
                position=self.positions[i],
                velocity=self.velocities[i],
                effort=self.efforts[i],
            )
            for i in range(n)
        ]


class JointSample(BaseModel):
    """One joint at one instant. This is what actually gets published to MQTT."""

    name: str
    stamp_ns: int
    position: float
    velocity: float
    effort: float

    def topic_prefix(self, asset: str = "ur5") -> str:
        return f"twin/{asset}/joint/{self.name}"
