# ROS Mapping

## Cell to ROS mapping

| BHA-S Cell | ROS Node(s) | Command | Query | Event Topic | Metric/Diagnostics | Lifecycle Required? |
|---|---|---|---|---|---|---|
| perception | camera_driver_node, object_detection_node | | | /perception/events | /diagnostics | depends |

## Mapping rules

- Command maps to ROS Service or Action.
- Long-running Command maps to ROS Action.
- Query maps to ROS Service or local state read.
- Event maps to ROS Topic.
- Metrics map to diagnostics, telemetry, or OpenTelemetry bridge.
- Safety-critical and hardware-resource nodes should use LifecycleNode or equivalent lifecycle wrapper.
- BHA-S safe states are project-level safety modes; do not confuse them with standard ROS lifecycle states.
