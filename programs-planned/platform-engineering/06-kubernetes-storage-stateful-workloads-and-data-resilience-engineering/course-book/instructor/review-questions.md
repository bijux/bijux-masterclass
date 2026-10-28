# Architecture review questions

Use these questions during checkpoints and the final defense.

## Authority

- Which copy is authoritative now?
- Which principal may write, delete, restore, or change retention?
- How is a stale writer rejected after partition or failover?

## Lifecycle

- Which object expresses intent, which controller reconciles it, and which backend record proves the effect?
- What happens after an ambiguous timeout and retry?
- Which identities survive process, Pod, Node, cluster, and account replacement?

## Consistency and recovery

- What consistency class does the recovery point claim?
- Which application generation or log position does it represent?
- Has it been restored into an empty destination?
- Which key, catalogue, and software versions are required?

## Capacity and operations

- What is the first bottleneck under growth or failure recovery?
- Is replacement placement possible after one Node or zone loss?
- Which alerts lead to a runbook before data safety is threatened?

## Evidence

- What was executed locally, natively, against the backend, or under operated conditions?
- What remains `not-executed`?
- Is any conclusion stronger than its evidence?
