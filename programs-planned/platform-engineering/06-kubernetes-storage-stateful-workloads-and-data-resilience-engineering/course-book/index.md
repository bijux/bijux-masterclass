# Kubernetes Storage, Stateful Workloads, and Data Resilience Engineering

Kubernetes can create claims, schedule Pods near volumes, invoke CSI drivers, and coordinate workload identities. It cannot decide what your data means, whether two writers are safe, whether a snapshot captured a valid application state, whether a backup can be restored, or whether a recovered service has met its recovery objective.

This course teaches those missing responsibilities as one connected discipline. You will move from volume lifetime and binding through CSI operations, topology, StatefulSets, fencing, database placement, snapshots, backup, restoration, performance, and migration. Every mechanism is tied to Atlas Data Plane 1.0, and every claim is limited to the evidence that actually supports it.

Begin with [Start here](start-here.md).
