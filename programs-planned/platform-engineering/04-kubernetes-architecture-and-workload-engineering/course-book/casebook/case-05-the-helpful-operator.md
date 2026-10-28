# Case 5 — The helpful operator

Deletion of an AtlasWorkload remains pending because the controller cannot remove an external release reservation. The object shows a deletion timestamp, the course finalizer, and `Ready=False, reason=CleanupDenied`.

An operator removes the finalizer manually. The API object disappears and garbage collection removes children, so the cluster looks clean. The external reservation remains. The next release cannot acquire the same identity.

The operator repaired API deletion but did not complete the controller's obligation.

A correct break-glass procedure would:

1. capture the deleting object, finalizer, reservation identity, and cleanup error;
2. decide whether API availability justifies abandoning automatic cleanup;
3. create an explicit orphan-remediation record owned by a person/team;
4. remove the finalizer only with that accepted residual risk;
5. reconcile or remove the external reservation later using the same stable identity;
6. verify no duplicate cleanup effect.

In the lab, authority is restored instead. The controller retries idempotently, removes the reservation, deletes owned children, removes only its finalizer, and lets deletion complete. A second reconcile produces no cleanup effect.

**Lesson:** manual finalizer removal is a transfer of cleanup responsibility, not evidence that cleanup happened.
