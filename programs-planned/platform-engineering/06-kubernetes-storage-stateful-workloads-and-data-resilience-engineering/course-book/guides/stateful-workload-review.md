# Stateful workload review

Use this review before approving a StatefulSet or operator-managed data service.

## Why stable identity?

State the exact requirement for ordinal DNS, stable PVC identity, ordered lifecycle, or per-member configuration. Reject StatefulSet use when the workload merely needs durable external state.

## Data authority

Name the authoritative writer, election mechanism, fencing method, membership generation, data generation, and client consistency model. Explain how a stale process is rejected after Node partition or force detach.

## Placement

Map replica anti-affinity, topology spread, PV affinity, storage replication domains, attach limits, and maintenance capacity. Three Pods in three zones do not imply three independent data copies.

## Lifecycle

Define bootstrap, readiness, liveness, shutdown, failover, scale-down, update order, and claim retention. Explain how long recovery may take without liveness killing it.

## Upgrade and rollback

List mixed-version compatibility, schema phases, operator version, storage format, and rollback boundary. Stateful rollback is a data protocol, not merely changing an image tag.

## Recovery

Name backup, snapshot, restore, quorum repair, and disaster procedures. Require a recent empty-destination restore report.
