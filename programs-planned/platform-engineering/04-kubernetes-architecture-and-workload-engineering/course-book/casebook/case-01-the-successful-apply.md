# Case 1 — The successful apply that produced no service

A release pipeline reports success after applying the Atlas API Deployment. Ten minutes later, the user journey fails and no Pod exists.

The first response is to separate stages. The API server returned an admitted Deployment with UID, generation, and resource version. That proves persistence. It does not prove controller action.

The evidence packet shows:

```text
Deployment generation:        7
observedGeneration:            6
ReplicaSets owned by UID:      0
Deployment-controller events:  none
controller-manager health:     unavailable
```

The earliest missing transition is Deployment-controller reconciliation. Reapplying the manifest changes resource version and may generate audit noise, but it does not create the missing control loop. Deleting and recreating the Deployment destroys evidence and still depends on the same unavailable controller.

The safe repair restores the controller manager, then verifies that observed generation advances, a ReplicaSet appears with the correct owner reference, Pods are created, and later transitions proceed. The incident record distinguishes control-plane recovery from workload success.

A second version of the case has a ReplicaSet but no Pods. That moves ownership to the ReplicaSet controller or selector/adoption relationship. A third has Pods Pending, moving the diagnosis to scheduling. The same external symptom requires a different repair at each transition.

**Lesson:** a successful API write is the beginning of convergence evidence, not the end.
