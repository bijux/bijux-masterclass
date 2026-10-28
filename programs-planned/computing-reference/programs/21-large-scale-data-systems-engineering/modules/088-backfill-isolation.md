---
module_id: LSDS-088
program: Large-Scale Data Systems Engineering
level: 2
module_number: 88
title: Backfill Isolation
status: complete
last_verified: 2026-09-04
---

# Backfill Isolation

## One-Page Review

### Governing question

How can a platform recompute historical intervals at high volume without corrupting live state, repeating external effects, starving production, mixing code/input versions, or publishing unverified results—and then cut over safely?

### Essential definitions

- A **backfill** is a bounded historical recomputation under an explicit interval and version contract.
- The **live plane** serves current production traffic/state; the **backfill plane** performs historical work.
- A **run manifest** pins interval, input snapshot, code/config/schema, partition plan, output namespace, and policy.
- A **shadow output** is backfill materialization invisible to normal production readers.
- **resource isolation** reserves live capacity and caps/prioritizes backfill CPU, memory, I/O, network, and destination load.
- **effect isolation** disables or redirects notifications, charges, mutable commands, and other live side effects.
- A **comparison gate** evaluates completeness, identity, schema, quality, reconciliation, and performance before publication.
- **publication** atomically promotes validated partitions/snapshot references to a reader-visible version.
- A **cutover fence** prevents stale live/backfill writers from changing the promoted ownership boundary.
- A **rollback point** preserves the prior visible snapshot and compatible execution evidence.
- A **contamination path** is any shared namespace, state, cache, quota, sink, credential, or control channel through which backfill can affect live service.

### Central model, mechanism, or theorem

Represent backfill run $B$ as

$$B=(I,X,V,E,S,O,Q,G,P),$$

where $I$ is the exact logical interval/partition set, $X$ input snapshot/offsets, $V$ code/config/schema/model versions, $E$ execution identity, $S$ isolated state/checkpoints, $O$ shadow output, $Q$ resource/destination quotas, $G$ validation gates, and $P$ publication/rollback policy.

Safety requires deterministic reads from $X$, disjoint mutable namespaces for $E,S,O$, denied or sandboxed external effects, enforced quota/priority $Q$ that preserves live SLO reserves, and publication only when every required partition passes $G$ under one manifest digest. A conditional metadata swap publishes the complete candidate or selected validated partitions with explicit version lineage; it never lets task completion mutate the live pointer directly.

### Critical invariants

- Interval semantics use logical data time/partition identity, not the wall clock when the run executes.
- Input snapshots, code, config, schema, model, and reference data are pinned and recorded.
- Backfill run, state, checkpoint, cache, temporary, output, transaction, and metric identities cannot collide with live identities.
- Production side effects are denied, sandboxed, or protected by stable effect keys and explicit policy.
- Live capacity has enforceable reserves; backfill has bounded concurrency, rate, priority, and pause/cancel controls.
- Backfill writes only shadow/versioned output until comparison and approval succeed.
- Each output partition maps to exactly one declared input interval/version and has completeness/content evidence.
- Publication uses one authorized, audited, conditional decision and fences stale writers.
- Partial failure can resume idempotently without reusing incompatible artifacts.
- Rollback preserves the previous visible snapshot and all dependencies through the observation window.

### Common failures

Common failures include reusing live consumer groups or checkpoints; reading “latest” mutable source/reference data; executing historical intervals with current wall-clock defaults; writing directly into production tables/topics; resending notifications; sharing state-store paths, caches, staging prefixes, transaction IDs, or metrics labels; giving backfill unbounded parallelism; assuming scheduler priority limits database/object-store pressure; publishing partitions as individual tasks finish; comparing only row counts; mixing retry output from changed code; deleting the previous snapshot immediately; and calling a dry run safe when it still performs remote effects.

### Compact example

A 100-CPU cluster reserves 60 CPU for live service and caps backfill at 25, leaving 15 CPU unallocated headroom. Run `bf-orders-2026q1` reads seven pinned daily snapshots, uses isolated consumer/state/output namespaces, and cannot access notification credentials. Six candidate partitions pass row-key/content/schema reconciliation; one differs and is quarantined. A conditional table-snapshot publication can promote the six approved replacements only if partial publication is an explicit policy with dependency closure; otherwise the entire run remains shadowed.

### Connections

[LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md) supplies replay-safe effects, [LSDS-057](057-memory-cpu-and-i-o-isolation.md) supplies resource isolation, [LSDS-080](080-operating-table-metadata-under-millions-of-files.md) supplies metadata operations, [LSDS-085](085-checkpoint-based-recovery.md) supplies recovery roots, [LSDS-086](086-exactly-once-state-updates.md) supplies state identity, and [LSDS-087](087-transactional-sinks.md) supplies atomic publication.

## Governing Question

Backfills compress months or years of work into hours. Their demand can exceed normal production volume, and their older intervals often execute with newer software. Running them “through the same pipeline” may appear consistent but can reuse live offsets, mutate current keyed state, repeat irreversible actions, overwhelm shared dependencies, and interleave versions in one destination.

Isolation is broader than compute placement. A separate cluster that shares the live sink credentials can still send duplicate emails. A separate output prefix that reads mutable reference data can still produce irreproducible history. A low-priority queue that saturates the database can still violate live SLOs. Every contamination path must be named and controlled.

The governing question spans planning, identity, data snapshots, state and effects, resource governance, observability, validation, publication, rollback, and cleanup. A safe backfill remains reversible and invisible until its evidence supports a deliberate visibility change.

## Why This Matters

Backfills repair bugs, apply schema/rule changes, populate new fields, rebuild after corruption, onboard sources, and satisfy audits. Refusing all historical recomputation sacrifices correctness; executing it casually risks a second incident.

Production protection is a multi-resource problem. CPU quotas do not bound object-store requests, shuffle bandwidth, metadata commits, warehouse slots, database connections, API rate, or cache eviction. Backfill can also amplify input by repartitioning or retry storms. Isolation needs budgets at each scarce shared dependency and feedback from live SLOs.

Publication determines blast radius. Direct overwrite exposes partial days and makes rollback hard. Shadow outputs allow row/key/aggregate/digest comparison, sampled semantic checks, consumer rehearsal, and approval. Atomic snapshot/manifest swaps give clear lineage; partition-by-partition promotion may reduce blast radius only when cross-partition invariants permit it.

## Prerequisites and Retrieval

Review effect-safe replay in [LSDS-050](050-reprocessing-a-stream-without-double-applying-effects.md), resource isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), large table metadata in [LSDS-080](080-operating-table-metadata-under-millions-of-files.md), checkpoint recovery in [LSDS-085](085-checkpoint-based-recovery.md), state updates in [LSDS-086](086-exactly-once-state-updates.md), and transactional sinks in [LSDS-087](087-transactional-sinks.md).

You should understand logical data intervals, immutable snapshots, partitioning, idempotency, checkpoints, consumer groups, transactions, manifests/catalogs, conditional commits, quotas, priority, rate limits, workload identity, data quality, canaries, lineage, and rollback.

For diagnosis retain run/manifest digest, requested/effective interval, source snapshot/offset generation, code/image/config/schema/model/reference versions, execution/state/checkpoint/output namespaces, task attempt/partition, resource class/requests/limits/priority, dependency quotas/rates, effect policy/denials, candidate/production snapshot IDs, validation results, approvals, publication CAS, rollback reference, and cleanup disposition.

## Learning Objectives

After this module, you should be able to:

1. inventory compute, data, state, effect, destination, identity, and control-plane contamination paths;
2. define a reproducible backfill manifest with pinned intervals and versions;
3. isolate consumer progress, state, checkpoints, caches, staging, transactions, and metrics;
4. deny or safely redirect historical external effects;
5. protect live SLOs with reserves, quotas, priorities, pacing, and circuit breakers;
6. produce resumable shadow output with stable partition identity;
7. validate completeness, uniqueness, content, schema, lineage, and downstream behavior;
8. choose atomic whole-snapshot or dependency-safe partial publication;
9. fence cutover, observe canaries, and roll back without recomputation; and
10. verify isolation with contention, failure, retry, and accidental-effect tests.

## Core Exposition

### Define intent and interval semantics

State why history is being recomputed and whether it repairs existing truth, creates a new version, or fills missing intervals. Define half-open logical interval $[t_0,t_1)$, time zone, calendar, partition keys, event-time versus ingestion-time rule, lateness horizon, and inclusions/exclusions.

A scheduler's execution date is not automatically the data interval. Dry-run expansion should enumerate exact partitions and existing run/output states before creating work. Reprocessing policy distinguishes missing, failed, and already completed intervals.

### Pin an immutable run manifest

Create one immutable manifest before execution. Pin source snapshot IDs or offsets/generations, code/image digest, feature/config flags, schema/serializer, model and reference-data versions, partitioner, transformation graph, output contract, effect policy, validation gates, resources, and publication policy.

Retries use the same manifest digest. A change creates a new run identity and candidate lineage; it must not silently reuse earlier partial results. Secrets remain referenced by scoped identity/version rather than copied into the manifest.

### Separate execution and ownership identities

Use durable backfill run ID in job names, consumer groups, coordinator epochs, transaction prefixes, leases, state keys, and audit. Attempt identity is subordinate to logical partition identity. A live worker and backfill worker must never both believe they own the same mutable keyspace.

Admission rejects namespace overlap with live or another incompatible backfill. Workload identity grants read access to pinned inputs and write access only to the run's shadow namespace. It denies live effects and publication authority to task workers.

### Isolate state and checkpoints

Do not restore a historical run into the live state directory or advance live offsets. Use separate checkpoint roots, consumer groups, changelogs, timer namespaces, state stores, and coordinator history. Backfill can bootstrap from a compatible copied snapshot only under explicit read/claim ownership.

Record state schema and source frontier per partition. Retain recovery artifacts until validation/publication completes. Concurrent backfills need distinct roots even if they share immutable base files through governed references.

### Isolate outputs and effects

Write tables/files to a branch, candidate snapshot, staging catalog, or versioned namespace. Write topics to a shadow topic or transaction namespace. Redirect emails/webhooks to a capture sink, disable them through enforceable policy, or produce outbox intents that require separate authorization.

Do not rely on code paths “usually not calling” an effect. Remove credentials/network access, use destination policy, and test denial. If replayed effects are intended, assign stable logical keys, reconcile existing outcomes, and approve the exact effect class separately.

### Protect live compute and memory

Reserve minimum live capacity; cap backfill maximums independently. Use separate clusters/node pools when failure or noisy-neighbor risk justifies it. Priority controls queue order, while quotas/limits bound consumption. Preemption can reclaim resources but may amplify retry and sunk work.

Limit active runs, partition concurrency, task parallelism, speculative execution, memory, local disk, shuffle, and checkpoint concurrency. Start small, measure amplification, and ramp with a live-SLO guard.

### Protect shared dependencies

Inventory source read throughput, object-store requests, network, catalog commits, warehouse slots, database connections/locks, API rate, message partitions, cache, DNS, and control-plane operations. Apply per-run rate/concurrency budgets at the dependency, not only the scheduler.

Use dedicated connection pools/queues and request tags. Circuit breakers pause admission when live latency/error/budget signals cross thresholds. A paused backfill must checkpoint safely and not hold scarce transactions indefinitely.

### Plan order and chunking

Chunk by independently valid partition or dependency closure. Small chunks limit retry and validation scope; too many create scheduler/catalog/file overhead. Newest-first can repair recent user-visible history sooner, while oldest-first may be necessary for cumulative state.

Encode dependencies rather than assuming dates are independent. Stateful recurrence, slowly changing dimensions, session windows, and cross-partition deduplication may require ordered execution or a larger atomic publication set.

### Make execution resumable

Each partition attempt writes privately and produces a committable/report with manifest digest, input/output identity, counts, checksums, quality metrics, lineage, and status. Retry selects or replaces one winner; it never appends blindly to prior attempt output.

Coordinator persists partition states: planned, running, prepared, validated, rejected, published, rolled back, or abandoned. Resume reconciles storage/catalog reality rather than trusting task status alone.

### Validate candidate data

Validate interval/partition coverage, schema, null/domain constraints, primary-key uniqueness, referential integrity, row/key sets, digests, aggregates, distributions, business invariants, late/deletion handling, and lineage. Compare against expected/source truth and current production with differences classified by the intended change.

Counts can match while keys differ. Sampling can find semantic defects but cannot prove completeness. Define blocking versus advisory gates and preserve evidence at partition and whole-run levels.

### Rehearse downstream consumption

Run representative queries, joins, dashboards, exports, access controls, and retention/deletion workflows against the shadow version. Validate performance, file layout, metadata volume, schema compatibility, and consumer assumptions.

Shadow reads must not populate shared caches under colliding keys or emit live alerts. Consumer rehearsal uses isolated credentials/routes and records the candidate snapshot explicitly.

### Publish conditionally

Publication authority verifies the immutable manifest, required partitions/gates/approvals, current live base version, and no conflicting writer. It then conditionally swaps a catalog/manifest pointer or commits a declared partition replacement set.

If the live base changed since comparison, rebase/revalidate or reject; do not overwrite. Whole-snapshot publication is simplest for cross-partition invariants. Partial publication requires closure, ordering, and a mixed-version reader contract.

### Fence, observe, and roll back

Fence old live/backfill writers at cutover. Preserve previous snapshot/tag, code/config, source retention, and dependencies. Canary readers or tenant/partition slices when the storage/catalog supports an explicit route.

Monitor correctness, freshness, latency, errors, and downstream reconciliation through an observation window. Rollback is a conditional pointer/version change, not ad hoc overwriting; new writes since publication require a documented merge/forward-fix policy.

### Clean up safely

After approval and rollback window, remove abandoned staging and expired branches by lineage/reachability. Preserve audit, validation, publication, and deletion evidence. Ensure no checkpoint, active query, rollback tag, legal hold, or shared file still references data.

Revoke run credentials and quotas, close consumer groups/connections, and classify every partition/output as published, retained for rollback/audit, or safely deleted. Never let anonymous orphan files become accidental inputs.

## Definitions and Notation

Let:

- $B=(I,X,V,E,S,O,Q,G,P)$ be a backfill run contract;
- $I$ be required logical partitions and $I_v\subseteq I$ validated partitions;
- $X$ be pinned source/reference snapshots and $V$ semantic versions;
- $E,S,O$ be execution, state/checkpoint, and output namespaces;
- $Q=(q_c,q_m,q_i,q_n,q_d)$ be CPU, memory, I/O, network, and dependency budgets;
- $C$ be total cluster CPU, $L$ reserved live CPU, and $b$ granted backfill CPU;
- $R_p$ and $C_p$ be reference and candidate key/content sets for partition $p$;
- $D_p$ be classified expected differences and $U_p$ unexplained differences;
- $v_0,v_1$ be pre-publication and candidate snapshot versions.

Admission requires $b\le C-L$ plus independent dependency budgets; unused CPU is not permission to exceed database or object-store limits. Validation requires coverage and $U_p=\varnothing$ under named comparison, not merely $|R_p|=|C_p|$. Publication is conditional on expected base $v_0$ and gate policy.

## Mechanisms, Invariants, or Proof Structure

### Non-contamination proof

Assume disjoint mutable namespaces for execution/state/output, denied live-effect authority, and publication restricted to a separate gate. Task retries can change only run-owned state and shadow output. Therefore no task attempt directly mutates the protected live data/effect plane.

### Resource protection proof

Enforced live reserve $L$ and backfill cap $b\le C-L$ prevent backfill CPU allocation from consuming the reserve. Equivalent per-dependency quotas bound other resources. This is a capacity claim, not proof live SLOs hold; feedback guards still pause on measured degradation.

### Publication atomicity proof

Candidate output is immutable and invisible through the live pointer. Authorized publisher verifies complete gate evidence against base $v_0$, then conditionally swaps to $v_1$. Failure before swap preserves $v_0$; success exposes the declared candidate set. A conflicting base change rejects the swap.

### Reproducibility proof

Each attempt uses identical manifest digest, pinned $X,V$, interval semantics, and deterministic/captured nondeterminism. Its partition identity and output digest can therefore be compared across retry. Changed inputs or semantics create a new run rather than contaminating equivalence.

### Adversarial verification

Test empty/huge intervals, overlap/gaps, DST/time zones, late/deleted data, duplicate runs, retry with changed code, namespace collision, denied effects, credential leak, quota saturation, live degradation, task/coordinator crash, partial output, corrupt candidate, base-version race, cutover split brain, rollback, and cleanup with active references.

## Alternatives and Trade-Offs

| Design | Strength | Cost or limitation |
|---|---|---|
| Same pipeline/shared resources | Minimal infrastructure | Highest contamination and noisy-neighbor risk |
| Shared cluster with quotas/priority | Efficient capacity use | Shared control/data-plane dependencies remain |
| Dedicated cluster/project | Stronger compute/identity isolation | Cost, provisioning, drift, shared sinks may remain |
| In-place idempotent overwrite | Simple for independent replaceable partitions | Partial visibility and rollback complexity |
| Shadow table/branch plus swap | Validation, atomic visibility, rollback | Extra storage/catalog and cutover workflow |
| Full-run atomic publication | Strong cross-partition consistency | Delays all value and increases retained candidate size |
| Partition canary/promotion | Smaller blast radius, progressive value | Mixed-version contract and dependency closure needed |

Choose isolation strength from effect severity, data coupling, live SLOs, dependency controls, publication atomicity, and rollback needs. Separate compute alone is never the whole design.

## Failure Modes and Misconceptions

1. **Execution date equals data interval.** DST, schedules, and lateness invalidate it.
2. **Read latest.** Retry sees different source/reference truth.
3. **Shared consumer/checkpoint.** Backfill advances or corrupts live recovery state.
4. **Shared output prefix.** Attempts and live writers collide.
5. **Feature flag isolation.** Credentials still allow accidental effects.
6. **CPU-only quota.** Storage, network, database, and catalog still saturate.
7. **Low priority equals limit.** Running work can consume unbounded resources.
8. **Task success equals valid partition.** Content/schema/lineage may be wrong.
9. **Equal counts equal data.** Missing and duplicate keys can cancel.
10. **Immediate partition publish.** Consumers observe partial/mixed history.
11. **Blind snapshot swap.** Concurrent live changes are overwritten.
12. **Retry after code change.** One candidate mixes semantic versions.
13. **Delete old version.** Rollback becomes impossible during observation.
14. **Cleanup by age.** Active branches/checkpoints lose referenced files.
15. **Separate metrics absent.** Backfill hides live degradation and its own failures.

## Worked Examples

### Example 1

A daily interval is `[2026-03-08T00:00, 2026-03-09T00:00)` in a named time zone; treating it as 24 UTC hours would be wrong across a daylight-saving transition.

### Example 2

Retry under a new exchange-rate snapshot gets a new run manifest ID rather than reusing candidate partitions from the old snapshot.

### Example 3

A backfill consumer group and checkpoint root include `bf-orders-2026q1`; the live group and state paths are read-only/inaccessible.

### Example 4

Notification credentials are absent, and egress policy permits only a capture endpoint. A coding mistake is denied rather than sending historical emails.

### Example 5

Cluster CPU is 100, live reserve is 60, and backfill cap is 25, leaving 15 CPU headroom. Database connections have a separate cap.

### Example 6

Newest-first order is useful for independent daily reports; an opening-balance recurrence requires oldest-first dependency execution.

### Example 7

Candidate/reference both contain 1,000 rows but candidate duplicates one key and misses another. Key-set and digest comparison rejects it.

### Example 8

Six of seven partitions pass. Whole-run publication retains all seven in shadow; partial promotion is allowed only if downstream invariants accept the mixed version.

### Example 9

Live snapshot changes from 90 to 91 during validation. Compare-and-swap expecting 90 rejects publication and forces rebase/revalidation.

### Example 10

The executable fixture applies CPU isolation and per-partition comparison gates.

<!-- bijux-verify: {"id":"backfill-isolation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"live_reserved_cpu=60\nbackfill_cpu=25\nheadroom_cpu=15\nvalidated=2\nquarantined=1\npublishable=false\n","stderr":""}} -->
```python
cluster_cpu = 100
live_reserved_cpu = 60
backfill_requested_cpu = 40
backfill_cap_cpu = 25
backfill_cpu = min(backfill_requested_cpu, backfill_cap_cpu, cluster_cpu - live_reserved_cpu)

partitions = [
    ("2026-01-01", {"a": "10", "b": "20"}, {"a": "10", "b": "20"}),
    ("2026-01-02", {"c": "30"}, {"c": "30"}),
    ("2026-01-03", {"d": "40"}, {"d": "41"}),
]
validated = []
quarantined = []
for name, reference, candidate in partitions:
    (validated if reference == candidate else quarantined).append(name)

print(f"live_reserved_cpu={live_reserved_cpu}")
print(f"backfill_cpu={backfill_cpu}")
print(f"headroom_cpu={cluster_cpu - live_reserved_cpu - backfill_cpu}")
print(f"validated={len(validated)}")
print(f"quarantined={len(quarantined)}")
print(f"publishable={str(not quarantined).lower()}")
```

## Cross-Program Connections

- **Distributed systems:** namespaces, fencing, conditional publication, and recovery prevent split ownership.
- **Scheduling:** queues, quotas, priority, preemption, pacing, and admission protect live capacity.
- **Storage:** snapshots, branches, manifests, immutable files, lineage, and reachability enable shadow output.
- **Streaming:** consumer groups, offsets, state, watermarks, and replay define historical execution.
- **Security:** workload identities, denied credentials, egress policy, and publication authorization isolate effects.
- **Data quality:** coverage, identity/content comparison, invariants, and classified differences gate truth.
- **Platform engineering:** separate telemetry, dependency budgets, circuit breakers, canaries, and rollback operationalize safety.
- **Governance:** approvals, audit, retention, legal hold, and deletion evidence govern historical changes.

## References

1. Apache Airflow, [Backfill](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/backfill.html). Current. Documents interval runs, reprocessing behavior, concurrency, ordering, and dry runs.
2. Apache Airflow, [DAG Runs](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html). Current. Defines logical data intervals and historical execution.
3. Apache Iceberg, [Branching and Tagging](https://iceberg.apache.org/docs/nightly/branching/). Nightly documentation. Describes independent snapshot lineages, audit branches, validation, fast-forward, and retention.
4. Apache Iceberg, [Reliability](https://iceberg.apache.org/docs/latest/reliability/). Current. Describes atomic metadata commits, optimistic concurrency, and retry.
5. Google Cloud Dataflow, [Plan Your Dataflow Pipeline](https://cloud.google.com/dataflow/docs/guides/plan-pipelines). Current. Describes isolating batch and streaming pipelines for different SLOs.
6. Google Cloud Dataflow, [Design Dataflow Pipeline Workflows](https://cloud.google.com/dataflow/docs/guides/pipeline-workflows). Current. Covers job lifecycle, updates, snapshots, and isolation principles.
7. Apache Spark, [Job Scheduling](https://spark.apache.org/docs/latest/job-scheduling.html). Current. Documents scheduling pools, fair sharing, and concurrent jobs.
8. Apache Spark, [Configuration](https://spark.apache.org/docs/latest/configuration). Current. Documents scheduler mode and runtime resource controls.
9. Apache Flink, [Configuration](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/config/). Current. Documents task isolation, slots, memory, parallelism, and resource caps.
10. Apache Flink, [Jobs and Scheduling](https://nightlies.apache.org/flink/flink-docs-stable/docs/internals/job_scheduling/). Current. Describes task slots and slot-sharing behavior.
11. Kubernetes, [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/). Current. Defines namespace aggregate resource limits and their boundaries.
12. Kubernetes, [Pod Priority and Preemption](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/). Current. Defines priority, preemption, non-preempting priority, and quota interaction.

## Exercises

### Exercise 1

Write a run manifest for rebuilding 90 daily partitions after a calculation bug, including every version and namespace needed for reproducibility.

### Exercise 2

Design resource protection when live and backfill share compute, object storage, a catalog, and a database.

### Exercise 3

Design effect isolation for a pipeline that normally writes a table, sends emails, and calls a provisioning API.

### Exercise 4

Define validation and publication for a candidate where 89 of 90 partitions pass and downstream queries span the full quarter.

### Exercise 5

Design a fault-injection and rollback exercise covering retries, coordinator loss, quota pressure, concurrent live change, and cleanup.

## Answers to the Exercises

### Answer 1

Record half-open intervals/time zone/calendar/late-data policy; immutable source and reference snapshots; code/image/config/feature/model/schema/serializer/partitioner digests; graph and dependency order; run/execution/consumer/state/checkpoint/cache/staging/output/transaction/metric namespaces; effect policy; resource/dependency budgets; validation thresholds; expected live base; publication unit/approvers; rollback tag/window; and retention/cleanup rules. Retries preserve the digest; any semantic change creates a new run.

### Answer 2

Reserve live CPU/memory and cap lower-priority backfill concurrency/parallelism with pause/cancel controls. Separately rate-limit object reads/writes/requests, catalog commits, database connections/queries/locks, and network/shuffle; use distinct pools/identities/tags. Monitor live SLOs plus dependency saturation and stop backfill admission automatically before reserves fail. Test because scheduler quotas do not prove database or storage isolation.

### Answer 3

Grant read-only pinned inputs and write-only shadow-table access. Remove live email/provisioning credentials and block their network endpoints; route optional rehearsal to capture/sandbox destinations. Produce stable outbox intents only if later separately reviewed effects are required. Tasks cannot publish; a distinct authorized gate promotes table metadata. Audit denial tests and reconcile that live email/API effect counts remain zero.

### Answer 4

Keep all output shadowed because quarter-spanning queries make one missing partition violate closure, unless the business explicitly supports a mixed-version partition route. Quarantine the failed day with key/content/schema/lineage evidence, rerun it under the identical manifest, then validate per-day and quarter-wide aggregates/invariants. Conditional publish the whole candidate only if the live base still matches; retain the old quarter snapshot for rollback.

### Answer 5

Crash tasks before/after writes and validation, lose coordinator state/replies, retry with identical and changed manifest, saturate each quota/dependency, attempt forbidden effects, and degrade live load to trigger pause. Change the live base during validation and prove CAS rejects cutover. Publish a validated candidate, route canary readers, inject a post-cutover semantic alert, roll back conditionally, then race cleanup with active checkpoint/query/rollback references and prove referenced data survives.
