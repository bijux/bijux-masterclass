# Snapshot consistency review

Start with the recovery invariant.

1. List every volume and external state required to recover.
2. Choose crash-, filesystem-, application-, or distributed-consistency class.
3. Define prepare, quiesce/checkpoint, capture, verify, and resume phases.
4. Bound the write pause and define cleanup after timeout.
5. Record source PVC UIDs, PV/backend handles, application generation, schema, and key context.
6. For several volumes, verify group-snapshot support and exact membership.
7. Choose deletion policy, retention, and recovery owner.
8. Restore into new claims and run domain validation.

## Questions for reviewers

- At what instant were the bytes captured?
- Which writes were acknowledged before that instant?
- Can a snapshot report Ready while the application checkpoint failed?
- What happens when one member in a group fails?
- Are logs, object metadata, and external dependencies included?
- Which controller and backend versions produced the copy?

A `readyToUse` status closes only the storage-controller portion of the proof.
