# Lab — field conflict and finalizer deadlock

## Goal

Repair two object-lifecycle failures without overwriting another manager or abandoning cleanup silently.

## Safety boundary

Use the semantic API store. The optional kind extension must use a disposable custom resource in `atlas-system`.

## Baseline

Create AtlasWorkload with `atlas-author` owning replicas and configuration, and `atlas-controller` owning generated status and selector fields.

## Hypothesis

A conflicting apply to an author-owned field is rejected, while a deletion with an uncleared finalizer remains visible with a deletion timestamp. Both failures can be repaired through explicit ownership rather than forceful deletion.

## Controlled action

1. Apply a conflicting replica value as `atlas-controller`.
2. Record the conflict and managed-field sets.
3. Delete the object after adding the controller finalizer.
4. Make cleanup return an authorization error.
5. Restore permission, complete idempotent cleanup, and remove only the controller finalizer.

## Oracle

The conflicting field is not overwritten. The deleting object remains until cleanup succeeds. After repair, no external reservation remains and the object is removed exactly once.

## Evidence

Preserve managed fields, resource versions, generation, deletion timestamp, finalizers, cleanup identity, condition history, and external-resource state.

## Interpretation

Explain why force-conflicts and manual finalizer removal would each hide an ownership failure.

## Cleanup

Remove generated semantic state and any disposable CRD/namespace resources.

## Completion gate

Advance only after you can prove which actor owned every changed field and why deletion was safe to complete.
