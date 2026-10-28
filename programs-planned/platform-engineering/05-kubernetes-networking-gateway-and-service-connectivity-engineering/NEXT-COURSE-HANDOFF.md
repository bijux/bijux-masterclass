# Course 6 handoff

Course 5 publishes an exact network and topology contract for **Kubernetes Storage, Stateful Workloads, and Data Resilience Engineering** at:

```text
capstone/handoff/
```

The handoff records the connectivity facts Course 6 must preserve:

- storage-facing DNS names, ports, protocols, and address families;
- namespaces, labels, and NetworkPolicy dependencies;
- zone and node-topology assumptions;
- source-identity and TLS expectations;
- egress and private-connectivity requirements;
- failure semantics that affect quorum, replication, backup, and restore traffic;
- known unresolved evidence and the complete version ledger.

Course 5 does **not** claim persistent-volume durability, CSI correctness, StatefulSet recovery, database fencing, snapshot validity, backup integrity, restore success, RPO, or RTO. Those properties belong to Course 6 and require storage-specific evidence. The handoff states network dependencies without fabricating data-resilience guarantees.
