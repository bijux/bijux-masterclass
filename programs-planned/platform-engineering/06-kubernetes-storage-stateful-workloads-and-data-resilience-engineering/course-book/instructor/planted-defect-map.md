# Planted defect map

| Defect | Hidden error | Expected rejecting proof |
|---|---|---|
| DATA-01 | authoritative state stored in Pod-scoped storage | lifetime and data-catalogue review |
| DATA-02 | immediate binding creates topology conflict | binding/topology proof |
| DATA-03 | CSI replay creates a second backend volume | idempotency test |
| DATA-04 | stale writer accepted after takeover | fencing proof |
| DATA-05 | retained ordinal reuses stale data | lineage and membership review |
| DATA-06 | snapshot labelled application-consistent without checkpoint | consistency and restore proof |
| DATA-07 | backup manifest references missing object/key | integrity and empty-restore test |
| DATA-08 | capacity report ignores recovery headroom | capacity review |
| DATA-09 | migration enables target writes before source fencing | migration ledger proof |
| DATA-10 | local semantic evidence claimed as production durability | evidence-classification gate |

Use defects only after the relevant concept has been taught. Ask learners to identify the earliest violated invariant and the smallest proof that would have prevented release.
