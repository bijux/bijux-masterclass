# 21. Large-Scale Data Systems Engineering

**Program code:** `LSDS`

**Purpose:** Develop deep command of distributed storage and computation mechanisms that make large-scale batch, streaming, and analytical systems correct, efficient, and operable.

**Level-II professional outcome:** Ready to build, tune, and diagnose cluster-scale data systems and to contribute to distributed processing, storage, query, or lakehouse infrastructure.

**Prerequisites:** Data Engineering Levels I-II or equivalent; Distributed Systems Level I or equivalent; algorithms, databases, and systems basics.

**Primary ownership:** distributed data storage; cluster dataflow engines; shuffle and distributed joins; stream processors; large-scale query engines; lakehouse internals; resource scheduling; fault tolerance; skew and performance; cluster cost and capacity.

**Explicit exclusions:** ordinary pipeline construction (Program 19); organization-wide data architecture (Program 20); general consensus and distributed theory (Program 27); database internals outside analytical scale (Program 18).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Scale, Partitioning, and Distributed Dataflow

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Workloads That Require Multiple Machines** | `001-workloads-that-require-multiple-machines.md` |
| 002 | **Horizontal Partitioning** | `002-horizontal-partitioning.md` |
| 003 | **Range, Hash, and Consistent Partitioning** | `003-range-hash-and-consistent-partitioning.md` |
| 004 | **Data Locality** | `004-data-locality.md` |
| 005 | **Distributed Task Graphs** | `005-distributed-task-graphs.md` |
| 006 | **Stages, Tasks, and Dependencies** | `006-stages-tasks-and-dependencies.md` |
| 007 | **Narrow and Wide Transformations** | `007-narrow-and-wide-transformations.md` |
| 008 | **Serialization Across Workers** | `008-serialization-across-workers.md` |
| 009 | **Cluster Failure Assumptions** | `009-cluster-failure-assumptions.md` |
| 010 | **Reasoning About Work, Movement, and State at Scale** | `010-reasoning-about-work-movement-and-state-at-scale.md` |

### Block 02 — Distributed Filesystems and Object Storage

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Distributed Block Storage** | `011-distributed-block-storage.md` |
| 012 | **Metadata Servers and Namespace** | `012-metadata-servers-and-namespace.md` |
| 013 | **Replication and Erasure Coding** | `013-replication-and-erasure-coding.md` |
| 014 | **Read and Write Pipelines** | `014-read-and-write-pipelines.md` |
| 015 | **Failure Detection and Re-Replication** | `015-failure-detection-and-re-replication.md` |
| 016 | **Object Storage Semantics** | `016-object-storage-semantics.md` |
| 017 | **Multipart Upload and Commit** | `017-multipart-upload-and-commit.md` |
| 018 | **Consistency of Listings and Metadata** | `018-consistency-of-listings-and-metadata.md` |
| 019 | **Small-File Pathologies** | `019-small-file-pathologies.md` |
| 020 | **Selecting Storage Layouts for Large Analytical Workloads** | `020-selecting-storage-layouts-for-large-analytical-workloads.md` |

### Block 03 — Batch Dataflow Engines

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **MapReduce Execution Model** | `021-mapreduce-execution-model.md` |
| 022 | **Map-Side and Reduce-Side Processing** | `022-map-side-and-reduce-side-processing.md` |
| 023 | **Partitioners and Combiners** | `023-partitioners-and-combiners.md` |
| 024 | **Directed Acyclic Graph Execution** | `024-directed-acyclic-graph-execution.md` |
| 025 | **Lazy Evaluation and Plan Construction** | `025-lazy-evaluation-and-plan-construction.md` |
| 026 | **Stage Scheduling** | `026-stage-scheduling.md` |
| 027 | **Task Retry and Speculation** | `027-task-retry-and-speculation.md` |
| 028 | **Intermediate Data Materialization** | `028-intermediate-data-materialization.md` |
| 029 | **Checkpointing Long Computations** | `029-checkpointing-long-computations.md` |
| 030 | **Tracing a Batch Job Through a Cluster Engine** | `030-tracing-a-batch-job-through-a-cluster-engine.md` |

### Block 04 — Shuffle, Join, and Aggregation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Shuffle Architecture** | `031-shuffle-architecture.md` |
| 032 | **Map-Side Buffering and Spill** | `032-map-side-buffering-and-spill.md` |
| 033 | **Sort-Based Shuffle** | `033-sort-based-shuffle.md` |
| 034 | **Hash-Based Shuffle** | `034-hash-based-shuffle.md` |
| 035 | **Broadcast Joins** | `035-broadcast-joins.md` |
| 036 | **Repartition Joins** | `036-repartition-joins.md` |
| 037 | **Distributed Sort-Merge Joins** | `037-distributed-sort-merge-joins.md` |
| 038 | **Distributed Aggregation** | `038-distributed-aggregation.md` |
| 039 | **Skewed Keys and Heavy Hitters** | `039-skewed-keys-and-heavy-hitters.md` |
| 040 | **Reducing Network and Disk Cost in a Wide Transformation** | `040-reducing-network-and-disk-cost-in-a-wide-transformation.md` |

### Block 05 — Distributed Stream Processing

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Logs as Distributed Input** | `041-logs-as-distributed-input.md` |
| 042 | **Partitioned Consumption** | `042-partitioned-consumption.md` |
| 043 | **Stateful Operators** | `043-stateful-operators.md` |
| 044 | **Event-Time Processing** | `044-event-time-processing.md` |
| 045 | **Watermarks** | `045-watermarks.md` |
| 046 | **Window Assignment and Triggers** | `046-window-assignment-and-triggers.md` |
| 047 | **Checkpoint Barriers** | `047-checkpoint-barriers.md` |
| 048 | **State Snapshots and Recovery** | `048-state-snapshots-and-recovery.md` |
| 049 | **Backpressure Across Operators** | `049-backpressure-across-operators.md` |
| 050 | **Reprocessing a Stream Without Double-Applying Effects** | `050-reprocessing-a-stream-without-double-applying-effects.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Cluster Scheduling and Resource Management

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Cluster Resource Models** | `051-cluster-resource-models.md` |
| 052 | **Static and Dynamic Allocation** | `052-static-and-dynamic-allocation.md` |
| 053 | **Fair and Capacity Scheduling** | `053-fair-and-capacity-scheduling.md` |
| 054 | **Data-Local Task Placement** | `054-data-local-task-placement.md` |
| 055 | **Work Stealing and Speculation** | `055-work-stealing-and-speculation.md` |
| 056 | **Preemption** | `056-preemption.md` |
| 057 | **Memory, CPU, and I/O Isolation** | `057-memory-cpu-and-i-o-isolation.md` |
| 058 | **Multi-Tenant Queueing** | `058-multi-tenant-queueing.md` |
| 059 | **Autoscaling Data Clusters** | `059-autoscaling-data-clusters.md` |
| 060 | **Diagnosing Scheduler Delay and Resource Fragmentation** | `060-diagnosing-scheduler-delay-and-resource-fragmentation.md` |

### Block 07 — Large-Scale SQL and Query Engines

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Distributed Logical and Physical Plans** | `061-distributed-logical-and-physical-plans.md` |
| 062 | **Coordinator and Worker Architecture** | `062-coordinator-and-worker-architecture.md` |
| 063 | **Exchange Operators** | `063-exchange-operators.md` |
| 064 | **Distributed Hash and Merge Joins** | `064-distributed-hash-and-merge-joins.md` |
| 065 | **Partial and Final Aggregation** | `065-partial-and-final-aggregation.md` |
| 066 | **Vectorized Execution at Cluster Scale** | `066-vectorized-execution-at-cluster-scale.md` |
| 067 | **Runtime Filtering and Dynamic Pruning** | `067-runtime-filtering-and-dynamic-pruning.md` |
| 068 | **Adaptive Query Execution** | `068-adaptive-query-execution.md` |
| 069 | **Federated Query** | `069-federated-query.md` |
| 070 | **Diagnosing a Distributed Query from Plan to Network** | `070-diagnosing-a-distributed-query-from-plan-to-network.md` |

### Block 08 — Lakehouse Table and Metadata Systems

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Table Snapshots and Atomic Commit** | `071-table-snapshots-and-atomic-commit.md` |
| 072 | **Manifest and Metadata Trees** | `072-manifest-and-metadata-trees.md` |
| 073 | **Optimistic Concurrency** | `073-optimistic-concurrency.md` |
| 074 | **Schema Evolution at Scale** | `074-schema-evolution-at-scale.md` |
| 075 | **Metadata Mechanics of Partition Evolution** | `075-metadata-mechanics-of-partition-evolution.md` |
| 076 | **Compaction Planning** | `076-compaction-planning.md` |
| 077 | **File Clustering and Ordering** | `077-file-clustering-and-ordering.md` |
| 078 | **Deletion Vectors and Row-Level Changes** | `078-deletion-vectors-and-row-level-changes.md` |
| 079 | **Catalog and Transaction Coordination** | `079-catalog-and-transaction-coordination.md` |
| 080 | **Operating Table Metadata Under Millions of Files** | `080-operating-table-metadata-under-millions-of-files.md` |

### Block 09 — Fault Tolerance, Consistency, and Reprocessing

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Task-Level Failure Recovery** | `081-task-level-failure-recovery.md` |
| 082 | **Worker and Executor Loss** | `082-worker-and-executor-loss.md` |
| 083 | **Coordinator Failure** | `083-coordinator-failure.md` |
| 084 | **Lineage-Based Recompute** | `084-lineage-based-recompute.md` |
| 085 | **Checkpoint-Based Recovery** | `085-checkpoint-based-recovery.md` |
| 086 | **Exactly-Once State Updates** | `086-exactly-once-state-updates.md` |
| 087 | **Transactional Sinks** | `087-transactional-sinks.md` |
| 088 | **Backfill Isolation** | `088-backfill-isolation.md` |
| 089 | **Schema and Code Changes During Reprocessing** | `089-schema-and-code-changes-during-reprocessing.md` |
| 090 | **Designing Recovery for Multi-Hour and Multi-Day Jobs** | `090-designing-recovery-for-multi-hour-and-multi-day-jobs.md` |

### Block 10 — Performance, Capacity, and Cost at Scale

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Partition Count and Task Granularity** | `091-partition-count-and-task-granularity.md` |
| 092 | **Memory Pressure, Spill, and Garbage Collection** | `092-memory-pressure-spill-and-garbage-collection.md` |
| 093 | **Serialization and Compression Trade-Offs** | `093-serialization-and-compression-trade-offs.md` |
| 094 | **Network Saturation** | `094-network-saturation.md` |
| 095 | **Storage Throughput and Request Limits** | `095-storage-throughput-and-request-limits.md` |
| 096 | **Skew Detection and Mitigation** | `096-skew-detection-and-mitigation.md` |
| 097 | **Cluster Benchmarking** | `097-cluster-benchmarking.md` |
| 098 | **Capacity Planning for Batch and Streaming** | `098-capacity-planning-for-batch-and-streaming.md` |
| 099 | **Cost Attribution and Workload Governance** | `099-cost-attribution-and-workload-governance.md` |
| 100 | **Conducting an End-to-End Large-Scale Data Performance Review** | `100-conducting-an-end-to-end-large-scale-data-performance-review.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
