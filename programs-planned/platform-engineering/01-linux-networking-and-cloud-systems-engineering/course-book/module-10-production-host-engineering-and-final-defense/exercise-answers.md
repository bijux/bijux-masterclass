# Worked Answers — Module 10: Production Host Engineering and Final Defense

These answers demonstrate reasoning. Equivalent answers are valid when they preserve the same mechanism and evidence boundary.

## Exercise 1 — Release unit

They determine identity, listeners, resources, trust, and failure behavior. A code release under different unit or edge policy is a different operational system. Version and review them together or record compatible configuration ranges. Otherwise rollback and reproduction are ambiguous.

## Exercise 2 — Readiness fault

Readiness for mutating traffic should fail because the service cannot preserve accepted work. Liveness can remain true because the process runs. The proxy should stop new routed work while operators diagnose. The check must be bounded and should not modify business state.

## Exercise 3 — Rollback boundary

Moving durable state to a new layout and deleting the old path can make old code unable to read current data. Changing TLS key formats, permissions, or configuration syntax can also break rollback. Use expand/migrate/contract sequencing and retain compatible configuration until rollback is no longer required.

## Exercise 4 — Patch strategy

It may be required for urgent remediation or a stateful host with bounded maintenance, provided the change is recorded, tested, and reconciled into a new image. Image replacement offers repeatability but may take longer. The decision depends on risk, state placement, downtime, and recovery evidence.

## Exercise 5 — Log truth

Logs can be dropped, duplicated, reordered, buffered, rotated, or lost with the host. They describe observations. Durable spool/result files own Course 1 job state. Use logs to correlate transitions and diagnose discrepancies, then reconcile against authoritative state.

## Exercise 6 — Restore time

No. One controlled observation under a specific dataset and environment is evidence, not a guaranteed objective. Record size, environment, procedure, variability, and dependencies. A defensible RTO requires repeated or bounded evidence and capacity assumptions.

## Exercise 7 — Game-day abort

Loss of management access, cleanup failure, unexpected scope beyond the lab namespace/VM, evidence that valued data is affected, uncontrolled resource growth, or uncertainty about the active firewall/mount state. Abort and restore from console or snapshot. Safety overrides experiment completion.

## Exercise 8 — Runbook quality

It lacks trigger, claim-state check, authority, grace period, evidence preservation, abort conditions, and verification. Restart can duplicate work or hide OOM/storage failure. A runbook must first classify the failure and state, then choose restart, lease recovery, repair, or escalation.

## Exercise 9 — Manifest meaning

It proves that current payload bytes match the manifest and detects accidental change relative to it. It does not establish author identity, trusted build environment, dependency integrity, vulnerability status, or external timestamp. Stronger provenance and signing are later responsibilities.

## Exercise 10 — Cloud evidence

It exercises processes, files, sockets, and TLS on one host. It has no provider zones, managed load balancer, persistent disk replication, IAM, quota, or regional control plane. It can validate the requirements model only. A real cloud failure exercise is required for the stronger claim.

## Exercise 11 — Final causal path

DNS/resolver maps the name; client routing reaches the edge; TLS authenticates the endpoint; firewall permits the flow; edge terminates TLS and forwards to loopback API; API validates and atomically queues; worker claims and computes; atomic store publishes result; API reads status; logs record observations. Each owner has a separate failure and evidence boundary.

## Exercise 12 — Course 2 readiness

The handoff must identify compute, identity, network, DNS/TLS, storage, metadata, availability, operations, quantities, and acceptance scenarios; files must be manifested; assumptions and unexecuted claims must be explicit. Course 2 then maps them to resources and state rather than inventing architecture from tool defaults.
