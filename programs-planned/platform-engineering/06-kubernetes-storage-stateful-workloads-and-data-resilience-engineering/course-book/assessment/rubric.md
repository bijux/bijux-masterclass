# Final assessment rubric

| Area | Points | Required evidence |
|---|---:|---|
| data authority and lifecycle | 15 | catalogue, acknowledgement and deletion boundaries |
| PV/PVC/StorageClass and topology | 15 | compatible binding and replacement placement |
| CSI lifecycle and diagnosis | 15 | idempotent transitions and phase-specific evidence |
| StatefulSet, quorum, and fencing | 15 | stable identity plus stale-generation rejection |
| snapshots and consistency | 10 | labelled recovery point and restored validation |
| backup, restore, RPO, and RTO | 15 | empty-destination drill and measured phases |
| performance, capacity, and quotas | 5 | workload-shaped evidence and headroom |
| migration, release, and Course 7 handoff | 10 | cutover/rollback ledger and exact handoff |

A score of 85/100 is required. The following are non-compensable regardless of total score:

- predecessor contract or manifest mismatch;
- missing authoritative writer or deletion owner;
- no enforced fencing for single-writer data;
- no executed restore at the claimed evidence class;
- destructive migration without a rollback boundary;
- evidence claims stronger than the environment actually executed.

Reviewers score demonstrated reasoning and artifacts, not memorized terminology.
