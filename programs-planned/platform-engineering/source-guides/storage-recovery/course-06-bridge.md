# Course 6 bridge — from connectivity to durable state

| Course 5 guarantee | Course 6 obligation |
|---|---|
| Service and DNS identity are explicit | stateful endpoints preserve names without confusing reachability with data correctness |
| default-deny policy is the baseline | CSI, database, snapshot, backup, object-store, KMS, and restore flows are enumerated before enforcement |
| topology preferences are not availability guarantees | storage binding and data placement are evaluated against zones, capacity, attach limits, and failure domains |
| readiness controls endpoint eligibility | a stateful workload cannot become ready until recovery, fencing, and replay have completed |
| egress policy validates the connected peer | snapshot and backup targets are governed as external data authorities, not merely DNS names |
| public TLS authority is preserved | artifact restoration and download never expose backend storage credentials or internal authorities |

The bridge prevents a common platform error: treating `Bound`, `Mounted`, or `Ready` as evidence that data is current, exclusive, restorable, and safe from a second writer.
