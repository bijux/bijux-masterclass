# Orientation Checkpoint — Safe IaC Laboratory

## Required evidence

Retain:

- exact Course 1 predecessor verification;
- local tool and version inventory;
- selected evidence level for each module;
- repository credential/private-material scan;
- sandbox account ID and region when the AWS lane is used;
- named operator identity and session type;
- budget, stop condition, teardown owner, and deadline;
- clean dependency-light proof result;
- clean repository status after proof.

## Decision defense

Be prepared to explain:

1. why a provider profile name does not prove account identity;
2. why a correct configuration can still be dangerous in the wrong account or region;
3. why short-lived credentials reduce persistence but do not reduce the authority of the current session;
4. which evidence classes you can honestly execute in your environment;
5. how a failed cleanup becomes an owned incident.

## Progression gate

Proceed only when the predecessor is exact, no secret is present in source or evidence, and every optional cloud action would target an explicitly owned sandbox. OpenTofu or AWS unavailability does not block the reader-first and dependency-light course; it does block native/provider claims and must remain visible.
