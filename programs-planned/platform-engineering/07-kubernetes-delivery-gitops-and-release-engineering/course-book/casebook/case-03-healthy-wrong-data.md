# Case 3 — Healthy workloads, incompatible data

A canary passed readiness and HTTP error-rate checks. It began writing a new data representation that the stable revision could not read. When latency later regressed, traffic rollback restored the stable Pods and service failed broadly.

The release crossed the rollback frontier before analysis completed. Kubernetes health was accurate but too narrow.

The repair introduces stable/candidate read-write compatibility matrices, writer-authority phases, and a rule that progressive exposure cannot proceed beyond the compatibility window without a forward-repair plan.

## Extended reader notes

### Timeline

A candidate Deployment became Ready and Argo CD reported Healthy. The new writer stored a representation not understood by stable. A domain assertion failed after 20% exposure. Automatic traffic abort returned users to stable, which then failed reading the new rows.

### Root cause

Progressive delivery evaluated Kubernetes and HTTP signals but did not consume the data compatibility matrix. The release had crossed its rollback frontier before traffic exposure.

### Durable correction

Stable and candidate must dual-read before candidate writer cutover. Backfill is resumable and verified. Old-writer removal is a separate approved phase. Rollout analysis includes domain correctness, and abort logic checks the current data phase before selecting a prior binary.
