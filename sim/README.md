# sim

Gazebo Harmonic assets and launch files for `twin-hello`.

## Contents

- `urdf/` — UR5 description from the official [Universal_Robots_ROS2_Description](https://github.com/UniversalRobots/Universal_Robots_ROS2_Description) package. Vendored (not submodule) so this repo runs offline.
- `worlds/ur5_demo.sdf` — one UR5 arm on a plinth, in an empty world with a directional light.
- `launch/ur5_demo.launch.py` — brings up Gazebo Harmonic + robot_state_publisher + ros_gz_bridge.
- `scripts/sine_trajectory.py` — drives the arm through a sine trajectory for the demo GIF.

## First-time setup

```bash
# UR5 description
git clone --depth 1 https://github.com/UniversalRobots/Universal_Robots_ROS2_Description urdf/tmp
cp -r urdf/tmp/{meshes,urdf} urdf/
rm -rf urdf/tmp
```

The launch file and world SDF are intentionally scaffolded but not
committed as final files — write them yourself as part of Phase 1 in the
[roadmap](../docs/context/ROADMAP.md). Doing this by hand is where you
actually learn Gazebo.
