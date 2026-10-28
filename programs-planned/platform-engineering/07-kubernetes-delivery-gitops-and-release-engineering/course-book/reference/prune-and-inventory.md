# Reference — Inventory and prune

Inventory records which resources one delivery application owns. Prune considers resources in prior inventory but absent from desired state. It must exclude uncertain source observations, external/shared ownership, and protected resources.

Deletion requires lifecycle authority, not merely absence from a render. Data resources, CRDs, namespaces, and shared controllers need explicit retirement policy.

## Extended reader notes

Inventory answers which desired-set owner is responsible for a live resource. Prune removes inventory members absent from the new desired set. The operation is safe only when inventory ownership and lifecycle authority align.

Classify resources before enabling prune: ordinary application resources; shared resources; generated children owned by another controller; protected data and recovery objects; cluster-scoped platform resources; and orphaned objects under adoption review. A resource can be technically in inventory while its lifecycle belongs to another team.

Atlas blocks ordinary prune for PVs, PVCs, snapshot contents, group snapshot contents, and annotated protected objects. Retirement requires a separate record proving consumers are gone, retention is satisfied, recovery evidence exists, and a data owner approved deletion. Source fetch failure never produces an empty prune set.
