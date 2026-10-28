# Evidence model

Storage claims are unusually easy to overstate. Course 6 uses seven evidence classes.

| Class | Establishes | Does not establish |
|---|---|---|
| document | intended ownership and procedure | executable correctness |
| semantic | invariant logic in deterministic models | driver or backend behavior |
| filesystem | local atomicity, checksum, and restore mechanisms | CSI or distributed storage guarantees |
| API/static | manifest shape and cross-object references | controller admission or execution |
| cluster | Kubernetes and CSI control-loop behavior | cloud durability or regional recovery |
| storage-system | backend attach, snapshot, expansion, and performance behavior | long-term operational readiness |
| operated | repeated restoration, capacity, incidents, and maintenance over time | universal behavior outside the observed environment |

The phrase “backup succeeded” is forbidden without a named manifest, source boundary, target boundary, restore destination, verification oracle, and measured recovery point. The phrase “highly available” is forbidden without failure-domain, quorum, fencing, recovery-time, and client-observation evidence.
