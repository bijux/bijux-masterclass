# Case 2 — The controller fight

Git declares three Atlas API replicas. An `AtlasWorkload` controller interprets `spec.size=small` as two replicas. During an incident, an operator scales the generated Deployment to five. The value oscillates between two, three, and five, while every actor reports drift.

The object is not unstable because Kubernetes lacks consistency. It is unstable because the authority model is contradictory.

Managed fields reveal:

```text
atlas-gitops      owns spec.replicas
atlas-controller  force-applied spec.replicas
kubectl-scale     updated spec.replicas
```

Three valid mechanisms are being used to express mutually incompatible ownership.

The repair begins above the generated Deployment. The team decides that the AtlasWorkload is the desired-state API. Git owns `AtlasWorkload.spec.apiReplicas`; the controller owns generated Deployment replicas; operators do not edit generated children. Emergency scale changes the custom resource through a recorded path. An autoscaler, if introduced later, requires an explicit ownership transfer and changes the higher-level API to express bounds rather than an exact value.

The controller is changed to apply only fields it owns and to reject or report conflicts instead of forcing them. The operator's temporary field ownership is removed deliberately. A steady-state test runs five reconciliations and expects zero writes.

**Lesson:** last-write-wins is not an ownership model. Reconciliation frequency cannot repair ambiguous authority.
