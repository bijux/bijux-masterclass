# Controller status and condition design

Status should let users and automation answer: what generation was observed, what is progressing, what is blocked, and what action is required?

## Conditions as observations

A condition type should remain stable across versions. Status is one of `True`, `False`, or `Unknown`. Reason is machine-readable; message is human-readable. Observed generation prevents a condition about old desired state from being mistaken for evidence about new desired state.

Transition time changes when condition status changes, not whenever the controller checks. Repeated timestamp writes create watch traffic, resource-version churn, reconciliation loops, and noisy audit history.

## Summary versus detailed evidence

Status should summarize, not mirror every child object. Atlas records child names and conditions, while detailed replica and Pod evidence remains on native child objects. Mirroring all fields creates synchronization problems and API bloat.

## Failure taxonomy

Useful reasons distinguish:

- `InvalidSpec` — desired state cannot be interpreted;
- `DependencyNotFound` — a referenced object is absent;
- `Progressing` — children are converging normally;
- `Unschedulable` — placement is blocked;
- `CleanupDenied` — finalizer cleanup lacks authority;
- `ChildrenAvailable` — required child availability is satisfied.

Reasons should guide the next owner. “Error” is not enough.

## Status update discipline

Calculate desired status from current observation, compare semantically, and write only when changed. Use the status subresource where available. Do not let status writes increment desired generation.
