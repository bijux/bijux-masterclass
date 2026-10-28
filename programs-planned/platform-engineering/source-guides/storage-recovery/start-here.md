# Start here — Platform Engineering

Platform engineering is the design and operation of trusted capabilities that let other teams deliver and run software without rediscovering every systems problem. This program teaches those capabilities from the bottom up. An abstraction is introduced only after the learner can explain the state it owns, the control loop that changes that state, the failure modes it creates, and the evidence needed to trust it.

The first six stages are:

```text
Atlas Host Runtime 1.0
→ Atlas Cloud Foundation 1.0
→ Atlas Workload Release 1.0
→ Atlas Kubernetes Workload 1.0
→ Atlas Connectivity Plane 1.0
→ Atlas Data Plane 1.0
```

Course 6 begins after Kubernetes can run and connect the Atlas API and worker workloads. It does not assume that a bound PVC means data is durable, that a snapshot is a backup, that a StatefulSet is a database operator, or that a mounted filesystem makes concurrent writers safe. The course makes data authority explicit: which system owns bytes, which controller owns provisioning, which process may write, which evidence establishes consistency, and which restore exercise proves recoverability.

Begin Course 6 at `06-kubernetes-storage-stateful-workloads-and-data-resilience-engineering/course-book/start-here.md`.
