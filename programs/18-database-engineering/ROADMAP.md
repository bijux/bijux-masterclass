# 18. Database Engineering

**Program code:** `DBE`

**Purpose:** Develop end-to-end command of database storage, indexing, query processing, transactions, recovery, replication, distribution, specialization, and production operation.

**Level-II professional outcome:** Ready to design schemas and workloads, diagnose database behavior, tune and operate production databases, and contribute to database engines or data infrastructure.

**Prerequisites:** data structures and algorithms; systems programming basics; operating-system and storage basics; SQL familiarity.

**Primary ownership:** relational and physical models; storage engines; indexes; transactions and concurrency control; query execution and optimization; logging and recovery; replication and HA; distributed databases; specialized database engines; database operations.

**Explicit exclusions:** pipeline construction (Program 19); enterprise data architecture (Program 20); distributed algorithms beyond database context (Program 27).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Database Models and Architecture

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Database Systems, Workloads, and Guarantees** | `001-database-systems-workloads-and-guarantees.md` |
| 002 | **Relational Model and Relational Algebra** | `002-relational-model-and-relational-algebra.md` |
| 003 | **Schemas, Keys, and Constraints** | `003-schemas-keys-and-constraints.md` |
| 004 | **Normalization and Functional Dependencies** | `004-normalization-and-functional-dependencies.md` |
| 005 | **Denormalization and Read Models** | `005-denormalization-and-read-models.md` |
| 006 | **Database Catalogs and Metadata** | `006-database-catalogs-and-metadata.md` |
| 007 | **Client-Server and Embedded Architectures** | `007-client-server-and-embedded-architectures.md` |
| 008 | **OLTP, OLAP, and Mixed Workloads** | `008-oltp-olap-and-mixed-workloads.md` |
| 009 | **Life of a Read Query** | `009-life-of-a-read-query.md` |
| 010 | **Life of a Transactional Write** | `010-life-of-a-transactional-write.md` |

### Block 02 — SQL and Relational Querying

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Selection, Projection, and Ordering** | `011-selection-projection-and-ordering.md` |
| 012 | **Joins and Join Semantics** | `012-joins-and-join-semantics.md` |
| 013 | **Aggregation and Grouping** | `013-aggregation-and-grouping.md` |
| 014 | **Subqueries and Common Table Expressions** | `014-subqueries-and-common-table-expressions.md` |
| 015 | **Window Functions** | `015-window-functions.md` |
| 016 | **Set Operations** | `016-set-operations.md` |
| 017 | **Recursive Queries** | `017-recursive-queries.md` |
| 018 | **Null and Three-Valued Logic** | `018-null-and-three-valued-logic.md` |
| 019 | **Data Modification and Upsert** | `019-data-modification-and-upsert.md` |
| 020 | **Writing Correct SQL Under Duplicate and Null Semantics** | `020-writing-correct-sql-under-duplicate-and-null-semantics.md` |

### Block 03 — Storage Engines and Buffer Management

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Pages, Blocks, and Database Files** | `021-pages-blocks-and-database-files.md` |
| 022 | **Record and Tuple Layout** | `022-record-and-tuple-layout.md` |
| 023 | **Slotted Pages** | `023-slotted-pages.md` |
| 024 | **Heap Files** | `024-heap-files.md` |
| 025 | **Database Page Free-Space Management** | `025-database-page-free-space-management.md` |
| 026 | **Buffer Pools** | `026-buffer-pools.md` |
| 027 | **Buffer-Pool Page Replacement** | `027-buffer-pool-page-replacement.md` |
| 028 | **Dirty Pages and Writeback** | `028-dirty-pages-and-writeback.md` |
| 029 | **Checksums and Page Corruption** | `029-checksums-and-page-corruption.md` |
| 030 | **Tracing a Record from Logical Row to Persistent Bytes** | `030-tracing-a-record-from-logical-row-to-persistent-bytes.md` |

### Block 04 — Indexes and Access Paths

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **B+ Tree Structure** | `031-b-tree-structure.md` |
| 032 | **B+ Tree Search and Range Scan** | `032-b-tree-search-and-range-scan.md` |
| 033 | **B+ Tree Insertion, Splitting, and Deletion** | `033-b-tree-insertion-splitting-and-deletion.md` |
| 034 | **Hash Indexes** | `034-hash-indexes.md` |
| 035 | **Composite and Covering Indexes** | `035-composite-and-covering-indexes.md` |
| 036 | **Partial and Expression Indexes** | `036-partial-and-expression-indexes.md` |
| 037 | **Bitmap and BRIN-Style Indexes** | `037-bitmap-and-brin-style-indexes.md` |
| 038 | **Full-Text and Inverted Indexes** | `038-full-text-and-inverted-indexes.md` |
| 039 | **Index Maintenance and Write Amplification** | `039-index-maintenance-and-write-amplification.md` |
| 040 | **Choosing Indexes from Workload Evidence** | `040-choosing-indexes-from-workload-evidence.md` |

### Block 05 — Transactions and Concurrency Control

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **ACID and Transaction Boundaries** | `041-acid-and-transaction-boundaries.md` |
| 042 | **Read and Write Anomalies** | `042-read-and-write-anomalies.md` |
| 043 | **Lock Modes and Granularity** | `043-lock-modes-and-granularity.md` |
| 044 | **Two-Phase Locking** | `044-two-phase-locking.md` |
| 045 | **Deadlock Detection and Resolution** | `045-deadlock-detection-and-resolution.md` |
| 046 | **Multi-Version Concurrency Control** | `046-multi-version-concurrency-control.md` |
| 047 | **Snapshot Visibility** | `047-snapshot-visibility.md` |
| 048 | **Isolation Levels** | `048-isolation-levels.md` |
| 049 | **Serializable Snapshot Isolation** | `049-serializable-snapshot-isolation.md` |
| 050 | **Reproducing and Eliminating Transaction Anomalies** | `050-reproducing-and-eliminating-transaction-anomalies.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Query Execution Engines

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Logical and Physical Plans** | `051-logical-and-physical-plans.md` |
| 052 | **Sequential and Index Scans** | `052-sequential-and-index-scans.md` |
| 053 | **Nested-Loop Joins** | `053-nested-loop-joins.md` |
| 054 | **Hash Joins** | `054-hash-joins.md` |
| 055 | **Single-Node Sort-Merge Joins** | `055-single-node-sort-merge-joins.md` |
| 056 | **Hash and Sort Aggregation** | `056-hash-and-sort-aggregation.md` |
| 057 | **External Sorting and Spilling** | `057-external-sorting-and-spilling.md` |
| 058 | **Iterator and Volcano Execution** | `058-iterator-and-volcano-execution.md` |
| 059 | **Vectorized and Pipeline Execution** | `059-vectorized-and-pipeline-execution.md` |
| 060 | **Profiling a Query Operator Pipeline** | `060-profiling-a-query-operator-pipeline.md` |

### Block 07 — Query Optimization

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Relational Rewrite Rules** | `061-relational-rewrite-rules.md` |
| 062 | **Predicate Pushdown and Projection Pruning** | `062-predicate-pushdown-and-projection-pruning.md` |
| 063 | **Statistics and Histograms** | `063-statistics-and-histograms.md` |
| 064 | **Cardinality Estimation** | `064-cardinality-estimation.md` |
| 065 | **Cost Models** | `065-cost-models.md` |
| 066 | **Join Ordering** | `066-join-ordering.md` |
| 067 | **Access-Path Selection** | `067-access-path-selection.md` |
| 068 | **Plan Caching and Parameter Sensitivity** | `068-plan-caching-and-parameter-sensitivity.md` |
| 069 | **Adaptive Query Processing** | `069-adaptive-query-processing.md` |
| 070 | **Diagnosing an Incorrect or Unstable Query Plan** | `070-diagnosing-an-incorrect-or-unstable-query-plan.md` |

### Block 08 — Logging, Recovery, and Durability

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Failure Models** | `071-failure-models.md` |
| 072 | **Write-Ahead Logging** | `072-write-ahead-logging.md` |
| 073 | **Log Sequence Numbers** | `073-log-sequence-numbers.md` |
| 074 | **Undo and Redo Logging** | `074-undo-and-redo-logging.md` |
| 075 | **Checkpoints** | `075-checkpoints.md` |
| 076 | **ARIES Analysis, Redo, and Undo** | `076-aries-analysis-redo-and-undo.md` |
| 077 | **Group Commit** | `077-group-commit.md` |
| 078 | **Crash Recovery** | `078-crash-recovery.md` |
| 079 | **Physical and Logical Backup** | `079-physical-and-logical-backup.md` |
| 080 | **Point-in-Time Recovery and Restore Verification** | `080-point-in-time-recovery-and-restore-verification.md` |

### Block 09 — Replication and Distributed Databases

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Physical Replication** | `081-physical-replication.md` |
| 082 | **Logical Replication** | `082-logical-replication.md` |
| 083 | **Synchronous and Asynchronous Replication** | `083-synchronous-and-asynchronous-replication.md` |
| 084 | **Replication Lag and Stale Reads** | `084-replication-lag-and-stale-reads.md` |
| 085 | **Leader Election and Failover** | `085-leader-election-and-failover.md` |
| 086 | **Sharding and Data Placement** | `086-sharding-and-data-placement.md` |
| 087 | **Distributed Transactions and Two-Phase Commit** | `087-distributed-transactions-and-two-phase-commit.md` |
| 088 | **Consensus-Backed Replication** | `088-consensus-backed-replication.md` |
| 089 | **Distributed SQL and Global Transactions** | `089-distributed-sql-and-global-transactions.md` |
| 090 | **Evaluating Consistency, Latency, and Availability Trade-Offs** | `090-evaluating-consistency-latency-and-availability-trade-offs.md` |

### Block 10 — Specialized Engines and Production Operations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Columnar Analytical Databases** | `091-columnar-analytical-databases.md` |
| 092 | **LSM-Based Key-Value Stores** | `092-lsm-based-key-value-stores.md` |
| 093 | **Document Databases** | `093-document-databases.md` |
| 094 | **Wide-Column Databases** | `094-wide-column-databases.md` |
| 095 | **Time-Series Databases** | `095-time-series-databases.md` |
| 096 | **Graph Databases** | `096-graph-databases.md` |
| 097 | **Vector Search Engines** | `097-vector-search-engines.md` |
| 098 | **Database Observability and Capacity** | `098-database-observability-and-capacity.md` |
| 099 | **Online Schema and Version Upgrades** | `099-online-schema-and-version-upgrades.md` |
| 100 | **Conducting a Production Database Reliability and Performance Review** | `100-conducting-a-production-database-reliability-and-performance-review.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
