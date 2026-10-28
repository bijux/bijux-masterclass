# Start here — Platform Engineering

Platform engineering is the design and operation of trusted capabilities that let teams deliver and run software without rediscovering every systems problem. This program develops those capabilities from the substrate upward. An abstraction appears only after the learner can explain the state it owns, the controller or process that changes that state, the failure modes it introduces, and the evidence required to trust it.

The released progression is:

```text
Atlas Host Runtime 1.0
→ Atlas Cloud Foundation 1.0
→ Atlas Workload Release 1.0
→ Atlas Kubernetes Runtime 1.0
→ Atlas Connectivity Plane 1.0
→ Atlas Data Plane 1.0
→ Atlas Delivery Plane 1.0
```

Course 7 begins after Kubernetes can run, connect, persist, and recover Atlas workloads. It adds reviewed desired state, deterministic rendering, GitOps reconciliation, artifact promotion, secret delivery, progressive exposure, fleet rollout, and release operations. It does not permit GitOps to redefine data authority or represent synchronization as proof of correctness.

Begin Course 7 at `07-kubernetes-delivery-gitops-and-release-engineering/course-book/start-here.md`. Learners joining the program at this stage should first verify the Course 6 handoff and be able to explain protected data resources, migration phases, restore gates, and rollback boundaries.
