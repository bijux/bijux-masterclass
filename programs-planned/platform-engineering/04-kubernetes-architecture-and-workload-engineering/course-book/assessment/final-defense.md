# Final defense

The final defense is a 60-minute evidence review, not a slide presentation.

The learner must demonstrate:

1. exact Course 3 image identities preserved in Kubernetes objects;
2. one admitted object and its field-ownership history;
3. a controller stopped and restarted without duplicate children;
4. a rollout calculation and stalled-rollout diagnosis;
5. a scheduler infeasibility proof with per-Node reasons;
6. a probe failure whose repair matches the probe question;
7. a voluntary-disruption calculation;
8. a controller-fit decision rejecting an unnecessary StatefulSet or custom controller;
9. idempotent AtlasWorkload reconciliation and deletion cleanup;
10. an exact Course 5 handoff with honest unexecuted boundaries.

## Non-compensable failures

The learner cannot pass while any of these remain:

- mutable image tags in release manifests;
- root or privilege escalation contrary to the inherited workload contract;
- ambiguous field or child ownership;
- liveness tied to a remote dependency without justified restart semantics;
- durable-path claims backed only by `emptyDir`;
- status churn on steady-state reconciliation;
- finalizer removal without cleanup evidence;
- networking, storage, or production-cluster claims beyond executed evidence.
