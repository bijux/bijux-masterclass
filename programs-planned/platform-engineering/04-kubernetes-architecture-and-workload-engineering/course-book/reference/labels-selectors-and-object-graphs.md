# Labels, selectors, and object graphs

Labels serve selection and organization. They become dangerous when used casually because selectors often define controller ownership, traffic populations, policy targets, or disruption populations.

## Separate identity dimensions

Atlas uses recommended label dimensions deliberately:

- `app.kubernetes.io/name` — component identity;
- `app.kubernetes.io/part-of` — platform grouping;
- `app.kubernetes.io/version` — release observation, not controller selector;
- `app.kubernetes.io/managed-by` — managing actor.

A Deployment selector uses stable component labels. If the version label were in the selector, every release would attempt to change an effectively immutable ownership boundary.

## Selector overlap

Two controllers whose selectors overlap may both count or adopt the same Pods. Owner references reduce some adoption ambiguity, but overlapping selectors remain a design defect. Services, PDBs, NetworkPolicies, and monitoring rules can also select populations unintentionally.

Review selectors as set expressions. For every object, ask:

- What population does this selector define?
- Can another object select the same population?
- Is overlap intentional and safe?
- Which labels may change without changing ownership?
- Does the template satisfy the selector exactly?

## Object graph and field graph

Owner references form a lifecycle graph: AtlasWorkload → Deployment → ReplicaSet → Pod. Managed fields form a separate graph of field-level authority. A GitOps manager may own the AtlasWorkload spec, while the controller owns generated Deployment fields and status. Do not infer field authority from lifecycle ownership alone.

## Garbage collection

Foreground and background deletion affect when dependents disappear relative to owners. Orphan deletion deliberately preserves dependents. Finalizers can block owner deletion. A release should not rely on default propagation without recording the intended cleanup behavior.
