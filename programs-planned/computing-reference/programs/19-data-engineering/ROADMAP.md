# 19. Data Engineering

**Program code:** `DE`

**Purpose:** Develop command of reliable data ingestion, modeling, transformation, orchestration, quality, lineage, and delivery across batch and streaming workflows.

**Level-II professional outcome:** Ready to build, test, operate, and evolve production data pipelines and analytical data products using SQL, Python, databases, object storage, and modern orchestration systems.

**Prerequisites:** SQL and Python; database fundamentals; basic statistics; software engineering and version control.

**Primary ownership:** data representation and schemas; ingestion and CDC; data modeling for analytics; batch transformations; stream processing at pipeline level; orchestration; data quality; metadata and lineage; analytical serving; data pipeline operations.

**Explicit exclusions:** enterprise-wide data architecture and governance operating models (Program 20); cluster-engine internals and extreme scale (Program 21); database engine internals (Program 18).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Data Representation and Pipeline Foundations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Data Producers, Consumers, and Lifecycle** | `001-data-producers-consumers-and-lifecycle.md` |
| 002 | **Rows, Columns, Records, and Events** | `002-rows-columns-records-and-events.md` |
| 003 | **CSV, JSON, and Line-Oriented Formats** | `003-csv-json-and-line-oriented-formats.md` |
| 004 | **Avro, Protocol Buffers, and Schema-Aware Serialization** | `004-avro-protocol-buffers-and-schema-aware-serialization.md` |
| 005 | **Arrow and In-Memory Columnar Representation** | `005-arrow-and-in-memory-columnar-representation.md` |
| 006 | **Parquet and Columnar Files** | `006-parquet-and-columnar-files.md` |
| 007 | **Compression and Encoding Choices** | `007-compression-and-encoding-choices.md` |
| 008 | **Schemas, Nullability, and Type Fidelity** | `008-schemas-nullability-and-type-fidelity.md` |
| 009 | **Time, Time Zones, and Event Timestamps** | `009-time-time-zones-and-event-timestamps.md` |
| 010 | **Designing a Reproducible Data Boundary** | `010-designing-a-reproducible-data-boundary.md` |

### Block 02 — Analytical Data Modeling

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Grain and the Meaning of a Row** | `011-grain-and-the-meaning-of-a-row.md` |
| 012 | **Facts, Dimensions, and Measures** | `012-facts-dimensions-and-measures.md` |
| 013 | **Star and Snowflake Schemas** | `013-star-and-snowflake-schemas.md` |
| 014 | **Slowly Changing Dimensions** | `014-slowly-changing-dimensions.md` |
| 015 | **Snapshot and Accumulating Fact Tables** | `015-snapshot-and-accumulating-fact-tables.md` |
| 016 | **Event and Activity Models** | `016-event-and-activity-models.md` |
| 017 | **Wide Tables and Denormalized Models** | `017-wide-tables-and-denormalized-models.md` |
| 018 | **Data Vault Foundations** | `018-data-vault-foundations.md` |
| 019 | **Metric Definitions and Semantic Consistency** | `019-metric-definitions-and-semantic-consistency.md` |
| 020 | **Validating an Analytical Model Against Business Questions** | `020-validating-an-analytical-model-against-business-questions.md` |

### Block 03 — Data Ingestion and Integration

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Full and Incremental Extraction** | `021-full-and-incremental-extraction.md` |
| 022 | **Watermarks and High-Water Marks** | `022-watermarks-and-high-water-marks.md` |
| 023 | **File Arrival and Manifest Processing** | `023-file-arrival-and-manifest-processing.md` |
| 024 | **API-Based Ingestion** | `024-api-based-ingestion.md` |
| 025 | **Database Snapshot Extraction** | `025-database-snapshot-extraction.md` |
| 026 | **Database Change Data Capture** | `026-database-change-data-capture.md` |
| 027 | **Idempotent Loads** | `027-idempotent-loads.md` |
| 028 | **Deduplication and Record Identity** | `028-deduplication-and-record-identity.md` |
| 029 | **Quarantine and Dead-Letter Data** | `029-quarantine-and-dead-letter-data.md` |
| 030 | **Designing Replayable Raw Ingestion** | `030-designing-replayable-raw-ingestion.md` |

### Block 04 — Batch Transformation Engineering

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Extract-Transform-Load and Extract-Load-Transform** | `031-extract-transform-load-and-extract-load-transform.md` |
| 032 | **SQL Transformation Pipelines** | `032-sql-transformation-pipelines.md` |
| 033 | **Dataframe Transformation Pipelines** | `033-dataframe-transformation-pipelines.md` |
| 034 | **Partitioned Processing** | `034-partitioned-processing.md` |
| 035 | **Incremental Models** | `035-incremental-models.md` |
| 036 | **Merge and Upsert Semantics** | `036-merge-and-upsert-semantics.md` |
| 037 | **Backfills** | `037-backfills.md` |
| 038 | **Late Corrections and Restatement** | `038-late-corrections-and-restatement.md` |
| 039 | **Deterministic Transformations** | `039-deterministic-transformations.md` |
| 040 | **Testing a Multi-Stage Batch Pipeline** | `040-testing-a-multi-stage-batch-pipeline.md` |

### Block 05 — Orchestration and Data Workflow Operations

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Directed Acyclic Graphs and Dependencies** | `041-directed-acyclic-graphs-and-dependencies.md` |
| 042 | **Tasks, Jobs, Assets, and Datasets** | `042-tasks-jobs-assets-and-datasets.md` |
| 043 | **Scheduling and Event-Triggered Execution** | `043-scheduling-and-event-triggered-execution.md` |
| 044 | **Retries, Timeouts, and Idempotency** | `044-retries-timeouts-and-idempotency.md` |
| 045 | **Partitioned Assets** | `045-partitioned-assets.md` |
| 046 | **Backfill Planning** | `046-backfill-planning.md` |
| 047 | **Parameterization and Environment Separation** | `047-parameterization-and-environment-separation.md` |
| 048 | **Data-Aware CI/CD** | `048-data-aware-ci-cd.md` |
| 049 | **Run Metadata and Operational State** | `049-run-metadata-and-operational-state.md` |
| 050 | **Designing an Operable Data Workflow** | `050-designing-an-operable-data-workflow.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Streaming Data Pipelines

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Streams, Logs, and Unbounded Data** | `051-streams-logs-and-unbounded-data.md` |
| 052 | **Topics, Partitions, and Offsets** | `052-topics-partitions-and-offsets.md` |
| 053 | **Producer Keys and Ordering** | `053-producer-keys-and-ordering.md` |
| 054 | **Consumer Groups** | `054-consumer-groups.md` |
| 055 | **Delivery Semantics in Streaming Pipelines** | `055-delivery-semantics-in-streaming-pipelines.md` |
| 056 | **Exactly-Once Effects** | `056-exactly-once-effects.md` |
| 057 | **Event Time and Processing Time** | `057-event-time-and-processing-time.md` |
| 058 | **Windows and Watermarks** | `058-windows-and-watermarks.md` |
| 059 | **Stateful Stream Transformations** | `059-stateful-stream-transformations.md` |
| 060 | **Handling Late, Duplicate, and Out-of-Order Events** | `060-handling-late-duplicate-and-out-of-order-events.md` |

### Block 07 — Lakehouse and Analytical Storage Practice

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Object Storage as a Data Substrate** | `061-object-storage-as-a-data-substrate.md` |
| 062 | **Raw, Standardized, and Curated Zones** | `062-raw-standardized-and-curated-zones.md` |
| 063 | **Table Metadata and Snapshots** | `063-table-metadata-and-snapshots.md` |
| 064 | **Schema Evolution** | `064-schema-evolution.md` |
| 065 | **Partition Evolution in Data Pipelines** | `065-partition-evolution-in-data-pipelines.md` |
| 066 | **Time Travel and Reproducible Reads** | `066-time-travel-and-reproducible-reads.md` |
| 067 | **Compaction and Small-File Management** | `067-compaction-and-small-file-management.md` |
| 068 | **Clustering and Data Skipping** | `068-clustering-and-data-skipping.md` |
| 069 | **Catalog Integration** | `069-catalog-integration.md` |
| 070 | **Operating a Transactional Table Format** | `070-operating-a-transactional-table-format.md` |

### Block 08 — Data Quality, Contracts, and Observability

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Completeness, Validity, Accuracy, and Consistency** | `071-completeness-validity-accuracy-and-consistency.md` |
| 072 | **Schema and Constraint Tests** | `072-schema-and-constraint-tests.md` |
| 073 | **Reconciliation Tests** | `073-reconciliation-tests.md` |
| 074 | **Freshness and Timeliness** | `074-freshness-and-timeliness.md` |
| 075 | **Volume and Distribution Monitoring** | `075-volume-and-distribution-monitoring.md` |
| 076 | **Data Contracts** | `076-data-contracts.md` |
| 077 | **Producer and Consumer Responsibilities** | `077-producer-and-consumer-responsibilities.md` |
| 078 | **Data Incident Detection and Triage** | `078-data-incident-detection-and-triage.md` |
| 079 | **Root-Cause Analysis with Lineage** | `079-root-cause-analysis-with-lineage.md` |
| 080 | **Building Quality Gates for a Data Product** | `080-building-quality-gates-for-a-data-product.md` |

### Block 09 — Metadata, Lineage, Governance, and Security

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Technical, Operational, and Business Metadata** | `081-technical-operational-and-business-metadata.md` |
| 082 | **Dataset and Column Lineage** | `082-dataset-and-column-lineage.md` |
| 083 | **Data Catalogs** | `083-data-catalogs.md` |
| 084 | **Ownership and Stewardship** | `084-ownership-and-stewardship.md` |
| 085 | **Classification and Sensitive Data** | `085-classification-and-sensitive-data.md` |
| 086 | **Access Control for Analytical Data** | `086-access-control-for-analytical-data.md` |
| 087 | **Masking, Tokenization, and De-Identification** | `087-masking-tokenization-and-de-identification.md` |
| 088 | **Retention and Deletion** | `088-retention-and-deletion.md` |
| 089 | **Auditability and Provenance** | `089-auditability-and-provenance.md` |
| 090 | **Making Data Discoverable Without Losing Control** | `090-making-data-discoverable-without-losing-control.md` |

### Block 10 — Serving, Reliability, and Data Product Engineering

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Warehouses, Query Engines, and Serving Stores** | `091-warehouses-query-engines-and-serving-stores.md` |
| 092 | **Materialized Views and Derived Tables** | `092-materialized-views-and-derived-tables.md` |
| 093 | **Reverse ETL and Operational Activation** | `093-reverse-etl-and-operational-activation.md` |
| 094 | **Data APIs** | `094-data-apis.md` |
| 095 | **Feature and Training Dataset Pipelines** | `095-feature-and-training-dataset-pipelines.md` |
| 096 | **Freshness and Completeness SLOs** | `096-freshness-and-completeness-slos.md` |
| 097 | **Pipeline Capacity and Cost** | `097-pipeline-capacity-and-cost.md` |
| 098 | **Disaster Recovery for Data Products** | `098-disaster-recovery-for-data-products.md` |
| 099 | **Versioning and Deprecating Datasets** | `099-versioning-and-deprecating-datasets.md` |
| 100 | **Reviewing a Production Data Product End to End** | `100-reviewing-a-production-data-product-end-to-end.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
