---
module_id: DBE-008
program: Database Engineering
level: 1
module_number: 8
title: OLTP, OLAP, and Mixed Workloads
status: complete
last_verified: 2026-08-30
---

# OLTP, OLAP, and Mixed Workloads

## One-Page Review

### Governing question

How do transaction processing, analytical processing, and mixed workloads differ, and how should their latency, throughput, freshness, isolation, and resource demands shape a database architecture?

### Essential definitions

**Online transaction processing (OLTP)** serves many short operations that read or change a small working set while preserving business invariants. **Online analytical processing (OLAP)** scans, joins, groups, and orders substantial data to answer exploratory or decision-support questions. A **mixed** or **hybrid transactional/analytical processing (HTAP)** workload needs both behaviors over related, often fresh data. **Freshness lag** is the distance between an authoritative committed change and its visibility to a reader. **Interference** is degradation one workload causes another through shared CPU, memory, storage, locks, cache, admission slots, or maintenance work.

### Central model, mechanism, or theorem

Workload class is a distribution, not a schema or product label. Describe operations by rows examined and changed, request rate, concurrency, result size, tail-latency objective, transaction duration, access locality, freshness, and consistency. A point lookup can be analytical in purpose; a large batch correction can be transactional in semantics. Mixed architecture then becomes an isolation choice: share an engine and govern resources, use a transactionally maintained analytical structure, or copy changes to a separate serving system and accept an explicit freshness and reconciliation contract.

### Critical invariants

- Business writes remain atomic and preserve constraints regardless of reporting load.
- OLTP tail latency and error rate are measured separately from average throughput.
- Analytical scans have explicit memory, CPU, I/O, concurrency, and cancellation limits.
- Freshness is defined from a named commit point to a named readable state.
- A replica, change stream, cache, or materialized view has an owner and reconciliation path.
- Benchmarks preserve data shape, skew, query mix, concurrency, think time, and durability.
- Resource isolation is verified during peak overlap, maintenance, failure, and recovery.
- Derived results identify source snapshot/version and do not silently combine incompatible times.

### Common failures

Common errors are classifying by table size alone, optimizing means while p99 transactions fail, running unbounded dashboards on the writer, assuming a read replica has zero lag, calling a nightly warehouse “real time,” measuring isolated queries instead of concurrency, disabling durability for a published throughput number, treating TPC workloads as application blueprints, adding indexes for every report without pricing write amplification, refreshing a materialized view without an atomic visibility contract, and duplicating data without reconciliation or deletion handling.

### Compact example

A checkout changes a few rows under a 50 ms p99 objective: OLTP. A quarterly margin report scans millions of facts and may run for seconds: OLAP. An operations dashboard reads aggregates within 45 seconds of checkout while checkouts continue: mixed. If a shared system has 100 capacity units and reserves 70 for transactions, analytical admission must remain at or below 30 in the model; that arithmetic is a policy illustration, not a universal sizing formula.

### Connections

[DBE-007](007-client-server-and-embedded-architectures.md) locates the engine boundary. [DBE-009](../ROADMAP.md) follows a read through that engine. Data Engineering owns dependable change movement, Data Architecture owns system-wide data responsibility, and Large-Scale Data Systems Engineering expands analytical execution and serving.

## Governing Question

“Transactional” and “analytical” are workload descriptions, not moral rankings or mutually exclusive database types. A system may execute both, and one business feature may contain both. The engineering question is whether the actual distributions can share representation and resources while meeting correctness, latency, freshness, recovery, and cost objectives.

Classification must therefore start with traces and service objectives. What is read or written? How many rows and bytes are examined, changed, and returned? At what request rate and concurrency? Which operations conflict? How long does a transaction retain locks or versions? How fresh must an answer be, and from which committed event? What happens when a report is canceled, a replica lags, or a transfer is replayed?

## Why This Matters

OLTP usually occupies the direct path of a user or machine action. Its failures can duplicate a payment, oversell inventory, lose an order, or expose an intermediate state. High throughput matters, but bounded tail latency, admission, durability, integrity, and predictable recovery often matter more. Averages hide queues: one long scan can evict hot pages or consume I/O so that thousands of otherwise small transactions miss their objective.

OLAP turns accumulated data into explanation and decision support. It must efficiently process wide ranges, joins, aggregates, sorts, windows, and repeated slices. Correctness includes semantic definitions and snapshot context: two dashboards can both execute valid SQL yet disagree because they use different event-time rules, late-data policies, dimensions, currencies, or refresh versions.

Mixed workloads create a coupled system. Keeping one copy can reduce freshness lag and duplication, but transactions and scans compete. Separating systems can specialize storage and compute, but introduces transfer delay, duplicated governance, transformation errors, replay, and reconciliation. There is no free “best of both”; the boundary moves costs and failure modes.

## Prerequisites and Retrieval

Retrieve transactions, isolation, constraints, indexes, rows and columns, joins, aggregation, percentiles, queues, cache locality, working sets, replication, change data capture, snapshots, materialized views, partitioning, compression, admission control, service-level objectives, recovery point objective, and recovery time objective.

Distinguish event time, source commit time, capture time, apply time, refresh completion, and query snapshot time. Also distinguish rows returned from rows examined. A report returning one number may scan billions of values; a transaction returning a full document may examine one keyed record.

## Learning Objectives

After this module, you should be able to:

1. characterize OLTP, OLAP, and mixed workloads from traces rather than labels;
2. distinguish transactional semantics from a workload's physical size;
3. define throughput, latency percentiles, concurrency, freshness, and staleness precisely;
4. identify CPU, memory, storage, cache, lock, version, and admission interference;
5. compare row-oriented, column-oriented, and mixed physical representations;
6. compare shared-engine, maintained-summary, replica, and separate analytical architectures;
7. define correctness and reconciliation across copied or derived data;
8. design representative workload and overlap experiments;
9. interpret benchmark results without overgeneralizing them; and
10. justify workload placement with measured objectives and explicit failure behavior.

## Core Exposition

An OLTP operation usually touches a small, selective working set: create an order, reserve inventory, update a device lease, or read an account. “Online” signals that the operation is in an interactive or operational path, not that it uses the public internet. The transaction may span several statements because the business invariant spans several relations. Short duration, selective access paths, bounded results, and predictable contention support high concurrency.

OLTP design favors constraints near authoritative writes, selective indexes, compact transactions, explicit idempotency, bounded retries, and admission before overload. Normalized schemas can avoid contradictory updates, but normalization alone does not make a workload OLTP. A transactional import may modify millions of rows, while a read-only fraud decision may need low-latency access to historical features.

An OLAP query typically examines much more data than it returns. It groups sales by region and month, joins facts to dimensions, computes percentiles, or explores an unknown predicate. Scan bandwidth, compression, vectorized execution, parallelism, join algorithms, cardinality estimates, spill behavior, and result governance dominate. Analytical systems often favor columnar access because a query can read selected columns and process value batches, but layouts and engines vary.

OLAP is not synonymous with “no correctness requirements.” Reports may inform regulated filings, capacity decisions, or automated action. Define duplicate handling, slowly changing dimensions, late arrivals, deletes, time zones, currency, null semantics, and reproducible snapshot/version. A fast aggregate over semantically inconsistent inputs is wrong.

Workload classification needs a vector rather than one threshold. Useful dimensions include operations per second; concurrent sessions; rows/bytes examined, changed, and returned; selectivity; read/write ratio; transaction duration; lock or version lifetime; temporal and key locality; query-shape stability; freshness; consistency; latency distribution; scheduled versus bursty arrival; and resource demand. Record distributions by operation class, not only totals.

Throughput and latency interact through queues. As utilization approaches a bottleneck, small bursts or service-time variance can produce disproportionate tail latency. Reporting only transactions per second hides whether requests were rejected, queued, or completed outside their objective. Reporting only one query runtime hides its interference with commits. Measure achieved throughput together with p50, p95, p99, maximum, errors, cancellations, queue time, and resource saturation.

Concurrency is part of the workload definition. Ten reports run serially are unlike ten concurrent reports even if total work is equal. User think time, connection reuse, transaction pacing, and skew determine contention. A hot account or newest partition behaves differently from uniform random keys. Preserve correlations: an order write may be followed immediately by an order-status read.

Physical representation expresses trade-offs. Row-oriented layouts place values of a record together, useful when an operation needs most columns of a few rows. Column-oriented layouts group values by attribute, supporting compression and scans over a subset of columns. Indexes accelerate selective reads but add write, log, storage, cache, and maintenance cost. Partitioning can prune scans and manage lifecycle, yet poor partition keys create hotspots or excessive metadata.

A shared general-purpose engine is the simplest mixed topology. Transactions and analytics see one authority under engine isolation rules; there is no cross-system change pipeline. It can succeed when analytical work is bounded, concurrency modest, and the engine provides appropriate plans and governance. It can fail when scans consume caches, memory, I/O, worker slots, temporary space, locks, or old versions required by long snapshots.

Resource governance makes shared execution deliberate. Separate workload identities; cap analytical concurrency and memory; apply statement, lock, and queue timeouts; prioritize operational admission; cancel runaway work; schedule heavy maintenance; and observe per-class wait and resource metrics. A 70/30 capacity partition is not inherently correct. Reserve enough tested headroom for peak transactions, failover, vacuum/compaction, checkpointing, backup, and uncertainty.

Maintained summaries—materialized views, aggregate tables, covering projections, or columnar secondary structures—trade write/refresh work and storage for cheaper reads. They may be updated transactionally, asynchronously, incrementally, or by full refresh. State which base changes are included, when a new version becomes visible, whether refresh blocks readers/writers, and how corruption or missed changes are rebuilt. “Materialized” does not imply current.

A read replica separates some compute while retaining a database-native copy. It may protect the writer from CPU and query workers, but replication traffic, storage, WAL retention, hot-standby conflicts, and shared infrastructure can remain coupled. Define freshness from writer commit to replica visibility. Decide whether applications may read their own writes, how they behave during lag, and whether failover changes analytical load placement.

A separate analytical store allows specialized columnar representation, independent scaling, longer retention, transformed schemas, and failure isolation. It also creates a distributed data product. Change capture must preserve identity, ordering scope, transaction boundaries where required, schema changes, deletes, retries, and checkpoints. The target needs idempotent application or deduplication, observable lag, backfill, reconciliation, and cutover rules.

Freshness is an end-to-end budget. Let a source change commit at `t_c` and become eligible for a named analytical snapshot at `t_v`; observed lag is `L=t_v-t_c`. Capture, transport, queue, apply, refresh, cache, and query scheduling all contribute. A dashboard “updated every minute” may be older if a job overruns, fails silently, reads a stale replica, or serves a cached result. Publish as-of time and degraded-state behavior.

Snapshot consistency matters across tables and partitions. Copying each table at a different point may create an impossible combination: an order without its customer or a payment without the matching status. Use a supported consistent snapshot, transaction-aware log position, or domain-specific watermark. If exact cross-entity consistency is unnecessary, state the bounded inconsistency accepted.

HTAP systems try to serve both modes over one logical, often current dataset through multiple representations, snapshots, execution paths, or resource pools. The HyPer research line demonstrated snapshot-based analytical processing alongside transactions; commercial and open systems implement different mechanisms. “HTAP” does not specify isolation, freshness, or absence of interference. Those remain measured product/version/configuration properties.

Benchmarks are controlled contracts, not anecdotes. TPC-C models a particular transaction-processing environment; TPC-H models decision support; current specifications define scale, query/transaction mix, metrics, disclosure, and validity. A compliant published result cannot be compared casually with an altered local script. Conversely, exact benchmark compliance is unnecessary for internal diagnosis, but every deviation and durability setting must be disclosed.

Construct a workload corpus from traces plus deliberately adversarial cases. Preserve data volume, distributions, skew, correlations, parameter frequencies, concurrency, think time, results, and write churn. Warm and cold cache answer different questions. Run transaction-only and analytics-only baselines, then overlap them to obtain interference: compare latency, throughput, resource use, and freshness against isolation objectives.

Failure testing belongs in the workload test. Stop capture, delay apply, exhaust analytical memory, fill temporary storage, cancel queries, restart replicas, fail over writers, corrupt a derived partition, and replay a range. Verify that OLTP correctness survives, staleness becomes visible, backpressure is bounded, and reconciliation repairs rather than duplicates data.

Architecture selection should end with evidence and an exit condition. Keep one system if it satisfies objectives under overlap and its operations are simpler. Add summaries when query shapes are stable and refresh semantics are acceptable. Use replicas when database-native change propagation and staleness fit. Split stores when specialization or isolation outweighs pipeline complexity. Revisit as distributions, objectives, and engine capabilities change.

## Definitions and Notation

For workload class `k`, define:

- arrival rate `lambda_k` in requests per second and achieved throughput `X_k`;
- concurrency `N_k`, including queued and executing work;
- latency random variable `T_k`, reported with named percentiles;
- examined bytes `B_e`, changed bytes `B_w`, and returned bytes `B_r`;
- freshness lag `L=t_visible-t_commit` for named source and consumer states;
- resource demand vector `D_k=(cpu, memory, io, workers, locks, versions, temp)`;
- interference ratio `I_k=p99_k(mixed)/p99_k(isolated)` when denominators and load are comparable.

An interference ratio greater than one reports degradation, not its cause. Capacity units in the executable model are an illustrative admission budget, not interchangeable CPU, memory, or I/O units. A workload is “mixed” here when operational transactions and freshness-sensitive analysis overlap over related data; this is not proof that one engine should execute both.

## Mechanisms, Invariants, or Proof Structure

A workload review should:

1. inventory operation classes and business correctness boundaries;
2. capture per-class distributions, correlations, skew, and objectives;
3. trace rows and bytes examined, changed, logged, transferred, and returned;
4. establish isolated OLTP and OLAP baselines;
5. overlap representative peaks and measure interference;
6. specify commit-to-visible freshness and snapshot consistency;
7. assign admission, cancellation, retry, and degradation policy;
8. test change movement, replay, backfill, deletion, and reconciliation;
9. inject resource, process, storage, and network failures; and
10. document benchmark fidelity, configuration, versions, and limitations.

The finite model below classifies three deliberately distinct fixtures using declared requirements, then calculates a simple shared-capacity admission ceiling and freshness lag. It validates arithmetic and transparent rules; it does not select a production database or predict performance.

<!-- bijux-verify: {"id":"finite-workload-classification","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"checkout_class=oltp\nmargin_class=olap\ndashboard_class=mixed\ncheckout_rows_examined=3\nmargin_rows_examined=25000000\ncapacity_units=100\ntransaction_reserve=70\nanalytical_ceiling=30\nfreshness_lag_s=45\n","stderr":""}} -->
```python
workloads = {
    "checkout": {
        "changes_authoritative_state": True,
        "rows_examined": 3,
        "scan_and_aggregate": False,
        "fresh_analysis_during_writes": False,
    },
    "margin": {
        "changes_authoritative_state": False,
        "rows_examined": 25_000_000,
        "scan_and_aggregate": True,
        "fresh_analysis_during_writes": False,
    },
    "dashboard": {
        "changes_authoritative_state": False,
        "rows_examined": 2_000_000,
        "scan_and_aggregate": True,
        "fresh_analysis_during_writes": True,
    },
}


def classify(workload):
    if workload["fresh_analysis_during_writes"]:
        return "mixed"
    if workload["changes_authoritative_state"] and not workload["scan_and_aggregate"]:
        return "oltp"
    if workload["scan_and_aggregate"]:
        return "olap"
    raise ValueError("fixture lacks a declared workload purpose")


capacity = 100
transaction_reserve = 70
analytical_ceiling = capacity - transaction_reserve
commit_second = 1_000
visible_second = 1_045

print(f"checkout_class={classify(workloads['checkout'])}")
print(f"margin_class={classify(workloads['margin'])}")
print(f"dashboard_class={classify(workloads['dashboard'])}")
print(f"checkout_rows_examined={workloads['checkout']['rows_examined']}")
print(f"margin_rows_examined={workloads['margin']['rows_examined']}")
print(f"capacity_units={capacity}")
print(f"transaction_reserve={transaction_reserve}")
print(f"analytical_ceiling={analytical_ceiling}")
print(f"freshness_lag_s={visible_second - commit_second}")
```

The classifier is intentionally not a general algorithm. Real operations can combine large transactions, point analytical decisions, streaming updates, and several freshness classes. The capacity subtraction assumes one additive policy dimension; real resources require separate limits and measured headroom. The timestamps assume synchronized observation of named states.

## Alternatives and Trade-Offs

**One row-oriented engine** minimizes copies and offers direct freshness, but analytical scans may be inefficient or disruptive. **One columnar or mixed-format engine** can accelerate analysis and perhaps transactions, but update paths, point access, compaction, and concurrency must be verified. **Maintained summaries** make stable queries cheap but add write or refresh cost and semantic versioning. **Read replicas** isolate some execution and preserve native schema but introduce lag and may remain operationally coupled. **A separate warehouse/lakehouse** specializes analytics and scales independently but owns a pipeline, duplicate state, governance, and reconciliation.

Scheduled analytics can avoid peak interference but increases answer age. Admission and cancellation protect transactions but may make analytical completion unpredictable. Strong snapshot consistency improves reproducibility but can retain old versions or delay visibility. Incremental refresh reduces repeated work but makes late changes, retractions, and repair more complex. Full rebuild is simpler to reason about but may exceed time and cost budgets.

## Failure Modes and Misconceptions

“OLTP means normalized rows” and “OLAP means star schemas” confuse common designs with definitions. The same normalized tables can be scanned analytically, and an operational service can maintain denormalized state. Classify observed operations and guarantees.

“Read-only cannot hurt writes” ignores shared CPU, cache, I/O, worker slots, temporary storage, old versions, catalog locks, and maintenance. Prove isolation under overlap. “Replica reads are current” ignores capture and apply lag. “One database guarantees one snapshot” ignores separate sessions, caches, asynchronous summaries, and long-running queries.

“Real time” has no engineering content without a bound and percentile. Define source commit, target visibility, cache behavior, and failure state. “Exactly once” is not a substitute for idempotency and reconciliation; duplicated, lost, reordered, or poison changes must have detectable handling.

“A benchmark proves our application” ignores different schemas, distributions, mixes, concurrency, hardware, durability, and objectives. “Faster query” may consume resources that violate transaction p99. “More indexes solve mixed load” ignores write amplification. “Split systems isolate failures” is incomplete if they share storage, network, credentials, orchestration, or operator actions.

## Worked Examples

### Example 1

A checkout reads one cart, decrements inventory, writes an order, and emits an outbox record atomically. It is OLTP even if later fulfillment is asynchronous because the direct business invariant is a short authoritative transaction.

### Example 2

A quarterly report scans 25 million order lines, joins dimensions, and returns twelve monthly margins. The one-row result does not make it a point query; rows examined, grouping, and seconds-level objective identify OLAP behavior.

### Example 3

A fraud decision reads one account plus a precomputed historical feature vector under 20 ms. Its access is selective but analytical in purpose. It demonstrates why purpose and physical signature are separate dimensions.

### Example 4

A dashboard must show accepted orders within 45 seconds. Commit-to-capture is 5 seconds, queue is 12, apply is 20, and refresh/cache is 8; the budget is exactly 45 seconds. Any retry must remain visible rather than quietly exceeding the promise.

### Example 5

Transactions meet p99=40 ms alone and p99=92 ms during four concurrent scans, so `I=92/40=2.3`. The ratio proves degradation under that load, not whether CPU, I/O, cache, locks, or versions caused it; wait and resource evidence must follow.

### Example 6

A materialized daily summary refreshes at 02:00. A 02:30 reader sees a stable version but not necessarily current transactions. The interface publishes data-through time and refresh status, and retains the previous complete version if refresh fails.

### Example 7

A replica is normally 2 seconds behind but reaches 20 minutes during network loss. Routing an order-confirmation read there violates read-your-write. The application reads the writer for that path and rejects or labels stale analytics when lag exceeds policy.

### Example 8

A change pipeline replays offsets after a crash. Target upserts keyed by source identity/version make repeats harmless, tombstones propagate deletes, and a periodic source-versus-target aggregate plus sampled record comparison detects gaps.

### Example 9

An index cuts a report from 8 seconds to 1 second but adds 15% write latency and doubles maintenance I/O. The local query win is rejected because checkout p99 and recovery objectives are governing constraints; a summary or analytical copy is tested instead.

### Example 10

An internal benchmark uses a TPC-H-shaped dataset but changes queries and omits power/throughput rules. It is reported as an application experiment, not a TPC-H result. Dataset generator, scale, changes, concurrency, cache state, durability, versions, and raw distributions are retained.

## Cross-Program Connections

- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns capture, transport, replay, backfill, and pipeline observability between transactional and analytical states.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) assigns authority, semantic models, ownership, lineage, and governance across copies.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) develops distributed scan, shuffle, storage, and serving mechanisms.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) explains scheduling, caches, virtual memory, I/O, and resource interference.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) supplies replication, ordering, failure, and consistency models for fresh copies.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) turns workload identities, quotas, telemetry, deployment, and incident policy into an operable service.

## References

1. [Microsoft Azure Architecture Center, Online Transaction Processing](https://learn.microsoft.com/en-us/azure/architecture/data-guide/relational-data/online-transaction-processing)
2. [Microsoft Azure Architecture Center, Online Analytical Processing](https://learn.microsoft.com/en-us/azure/architecture/data-guide/relational-data/online-analytical-processing)
3. [DuckDB, Why DuckDB](https://duckdb.org/why_duckdb)
4. [Transaction Processing Performance Council, Current Benchmark Specifications](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp)
5. [PostgreSQL 18 Documentation, Materialized Views](https://www.postgresql.org/docs/18/rules-materializedviews.html)
6. [PostgreSQL 18 Documentation, ANALYZE](https://www.postgresql.org/docs/18/sql-analyze.html)
7. [Microsoft Learn, In-Memory Technologies in Azure SQL Database](https://learn.microsoft.com/en-us/azure/azure-sql/database/in-memory-oltp-overview?view=azuresql)
8. [Kemper and Neumann, HyPer: A Hybrid OLTP and OLAP Main Memory Database System](https://arxiv.org/abs/1103.5160)

## Exercises

### Exercise 1

Characterize checkout, inventory search, order history, fraud scoring, and monthly finance reporting using at least eight workload dimensions. Explain why a single OLTP/OLAP label is insufficient for two of them.

### Exercise 2

A transaction service has p99 latency of 35 ms alone and 84 ms during reports. Design measurements that distinguish CPU, memory/cache, storage, lock/version, worker, and temporary-space interference.

### Exercise 3

Design a commit-to-dashboard freshness contract of 60 seconds. Allocate the budget across capture, transport, apply, refresh, cache, and query, and specify degraded and recovery behavior.

### Exercise 4

Compare a materialized view, a read replica, and a separate analytical store for a report that scans two years of orders while writes continue. Include semantics, isolation, cost, failure, and reconciliation.

### Exercise 5

Design a reproducible mixed-workload evaluation and state what must be disclosed before its result can support an architecture decision.

## Answers to the Exercises

### Answer 1

For each operation record request rate, concurrency, rows/bytes examined, rows/bytes changed, result size, transaction duration, conflict/skew, latency percentiles, freshness, and consistency. Checkout is selective authoritative OLTP; monthly finance is scan-heavy OLAP. Inventory search may scan an index and require near-current stock; fraud scoring may point-read precomputed history inside an operational deadline. Those combine analytical purpose with operational latency, so retain the vector rather than forcing a label. Order history varies with account size and pagination and can change class at the tail.

### Answer 2

Run transaction-only and report-only baselines, then controlled overlaps at increasing analytical concurrency with identical data, parameters, arrival process, and cache conditions. Record per-class queue and execution percentiles, achieved throughput, errors, CPU run queues, memory and eviction, buffer hit/miss, read/write latency and bandwidth, lock waits, snapshot/version retention, worker admission, spills, and temporary-space use. Cap one suspected resource at a time, inspect plans, and repeat. The interference ratio is `84/35=2.4`; it establishes degradation but not causality.

### Answer 3

One allocation is capture 5 s, transport/queue 10 s, apply 15 s, summary refresh 15 s, cache 5 s, and query/admission 10 s, totaling 60 s. Measure from authoritative commit to eligibility in the exact dashboard snapshot, publish source watermark and as-of time, alert before exhaustion, and reject or visibly mark stale results after 60 s. Pause unsafe consumption on schema incompatibility, preserve checkpoints, replay idempotently, reconcile source/target counts and samples, and declare recovery complete only after the watermark catches up and checks pass.

### Answer 4

A materialized view stays near the authority and can give an atomic complete version, but refresh consumes source resources and freshness follows its refresh mechanism. A read replica moves query compute and uses native change propagation, but has lag, may retain coupling, and can conflict with recovery or long snapshots. A separate analytical store offers specialized representation and independent scaling, but requires capture, schema evolution, delete handling, idempotent apply, consistent watermarks, backfill, and reconciliation. Test all three during writes, lag, refresh failure, replica restart, pipeline replay, and source recovery; choose against named p99, freshness, cost, and recovery objectives.

### Answer 5

Replay a versioned corpus with production-like volume, distributions, skew, correlations, parameters, write churn, connection behavior, think time, and peak overlap. Establish cold/warm OLTP-only and OLAP-only baselines, then vary mixed concurrency; inject cancellation, memory pressure, lag, restart, and replay. Record throughput, latency distributions, errors, freshness, plans, waits, CPU, memory, I/O, cache, locks, versions, spills, maintenance, and cost. Disclose schema/data generator, scale, query and transaction definitions, load driver, hardware, topology, engine/configuration, durability, cache state, run duration, repetitions, raw results, failures, and every deviation from any named benchmark. Compare objectives, not one headline score.
