# StatefulSet semantics

A StatefulSet supplies stable orchestration identity, not database correctness.

| Feature | What it provides | What the application must still provide |
|---|---|---|
| ordinal Pod names | repeatable member identities | membership and stale-member handling |
| governing Service | stable discovery names | protocol identity and authorization |
| volume claim templates | per-ordinal claim creation | data correctness and restore lineage |
| ordered management | sequencing of some Pod transitions | quorum-safe bootstrap and upgrade |
| update strategy/partition | controlled template rollout | mixed-version and data-format compatibility |
| claim retention policy | claim lifecycle during scale/delete | safe reuse, retirement, and deletion authority |

## Lifecycle questions

- Is stable ordinal identity genuinely required?
- What distinguishes a new process incarnation using the same ordinal?
- How is writer generation fenced?
- What does readiness mean for leader, follower, recovery, and lag?
- Can a retained claim be safely reused after scale-down?
- What happens when the highest ordinal cannot become Ready?
- Which changes make rollback impossible?

Use a Deployment when the workload needs durable external state but not stable member identity. Use an operator only when its lifecycle contract is understood and tested.
