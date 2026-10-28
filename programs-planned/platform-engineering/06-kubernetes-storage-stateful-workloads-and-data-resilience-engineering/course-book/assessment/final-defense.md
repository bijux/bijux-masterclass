# Final defense

The final defense is a 45–60 minute evidence-based review of Atlas Data Plane 1.0 from a clean workspace.

## Demonstration sequence

1. Verify the exact Course 5 handoff.
2. Explain the data catalogue, authority, acknowledgement, and deletion model.
3. Bind a claim through topology-aware provisioning and show rejected alternatives.
4. Trace create, attach, stage, publish, unpublish, detach, and delete semantics.
5. Demonstrate stale-writer rejection after a simulated takeover.
6. Produce a consistency-labelled snapshot or snapshot-group record.
7. Restore a backup into an empty destination and verify generation and artifact digests.
8. Diagnose one unknown planted defect using the earliest missing transition.
9. Defend capacity, RPO, RTO, and migration decisions.
10. Classify the release and verify the exact Course 7 handoff.

## Questioning standard

The learner must distinguish API intent, controller observation, backend effect, and application truth. Answers should name the owner, durable identity, failure mode, evidence, and rollback limit for each critical transition.

## Non-compensable failures

The defense fails when predecessor integrity is broken, a stale writer can mutate state, restore evidence is absent, destructive authority is unbounded, or local semantic evidence is misrepresented as native or production proof.
