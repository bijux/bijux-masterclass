---
module_id: DE-031
program: Data Engineering
level: 1
module_number: 31
title: Extract-Transform-Load and Extract-Load-Transform
status: complete
last_verified: 2026-09-02
---

# Extract-Transform-Load and Extract-Load-Transform

## One-Page Review

### Governing question

Where should each data transformation execute relative to the first durable load into the named analytical target so source fidelity, security, correctness, replay, atomic publication, performance, cost, and operational ownership remain explicit?

### Essential definitions

- **Extract** acquires a declared source scope at a source cut/range and preserves identity, schema, ordering, and lineage needed to interpret it.
- **Transform** changes representation or meaning through parsing, typing, validation, filtering, normalization, joining, aggregation, modeling, or policy enforcement.
- **Load** durably writes a named target boundary under explicit append, replace, merge, snapshot, transaction, and publication semantics.
- **ETL (extract–transform–load)** applies the governed transformation before loading the named analytical target.
- **ELT (extract–load–transform)** first loads a source-faithful representation into the named analytical target/platform, then transforms it there.
- A **landing/raw boundary** preserves replayable source evidence; it may exist before an ETL engine or inside an ELT platform, so its existence alone does not settle the acronym.
- **pushdown** moves suitable computation into a source or target engine rather than executing it in a separate transformation runtime.
- **staging** is an unpublished intermediate area used for validation, deduplication, merge, or atomic replacement; it is not trusted output.
- A **transformation contract** fixes input/output grain, schemas, keys, null/time/numeric semantics, code/configuration, reference data, determinism, quality rules, and lineage.
- **semantic equivalence** means two execution placements produce the same declared output and side effects under the same source cut and contract; similar SQL or row counts are insufficient.
- A **trusted publication** makes a complete validated output generation visible atomically or through a defined transactional metadata transition.

### Central model, mechanism, or theorem

For source population $I_c$ at cut $c$, extraction $E$, pre-target transformation $T_s$, curated load $L_c$, faithful target load $L_r$, and target transformation $T_t$:

$$
Y_{ETL}=L_c(T_s(E(I_c))),\qquad Y_{ELT}=T_t(L_r(E(I_c))).
$$

The placements are semantically equivalent only if, for every permitted $I_c$, their type coercion, filtering, validation, ordering, joins, side effects, failure boundaries, and publication produce the same declared result:

$$
L_c\circ T_s\circ E\equiv T_t\circ L_r\circ E.
$$

That equivalence is not automatic. A lossy target load before transformation can change rounding, nulls, strings, timestamps, or duplicates. A pre-load filter can discard data needed for replay. Architecture should therefore place each transformation according to its contract and preserve an authoritative replay boundary, not choose an acronym as ideology.

### Critical invariants

- The named source, source cut/range, target, and meanings of extract/transform/load are unambiguous.
- Highest-required source fidelity and lineage become durable before any lossy transformation or source acknowledgement.
- Input/output grain, keys, schemas, types, null/default, time zone, precision/rounding, deletes, and late-data policy are explicit.
- Stage order never changes semantics unintentionally; coercion/filter/join/aggregation placement is tested for equivalence or documented difference.
- Every load declares append, replace, merge/upsert, snapshot, and transaction/visibility behavior; command success is not publication proof.
- Staging generations are isolated and complete before conditional/atomic publication; readers never infer completeness from partial tables or file listings.
- Incremental boundaries, idempotency keys, occurrence versions, tombstones, and checkpoints make retry/replay safe.
- Code, configuration, schemas, references, runtime, and target semantics are versioned sufficiently for reproduction or explicit recomputation.
- Security and privacy controls apply where raw/sensitive data crosses networks, runtimes, and target access domains.
- Performance/cost decisions include source impact, transfer, transformation, target contention, storage, operational toil, and recovery—not only nominal compute speed.
- Lineage and quality evidence cover every intermediate and final boundary regardless of where transformation runs.

### Common failures

Calling any object-storage landing ETL or ELT without naming the target; assuming ELT means “no ETL”; transforming before retaining replayable raw; loading raw into a broadly accessible warehouse; filtering columns before future requirements or audit are understood; letting target column types coerce before business rounding; using `COPY` or a load job as an upsert; appending reruns; truncating trusted tables before validation; mixing DDL and DML without product-specific transaction analysis; using current lookup tables; moving all computation to the source and harming production; moving all computation to the warehouse and creating contention; comparing only row counts; or selecting architecture from tool fashion rather than source, target, risk, and operating evidence.

### Compact example

Three source records carry decimal strings: two `keep` and one `drop`. ETL parses and rounds the original values before curated load; ELT with a lossless raw load yields the same two rows and 3,006 cents. An ELT raw table that first coerces `10.005` to a two-decimal half-even type stores `10.00`, so later half-up business transformation totals 3,005 cents. Loading before transforming changed meaning. A replay of the lossless contract remains stable.

### Connections

[DE-008](008-schemas-nullability-and-type-fidelity.md) and [DE-009](009-time-time-zones-and-event-timestamps.md) define representation semantics; [DE-020](020-validating-an-analytical-model-against-business-questions.md) defines output fitness; [DE-021](021-full-and-incremental-extraction.md) through [DE-030](030-designing-replayable-raw-ingestion.md) provide source cuts, manifests, replay, identity, and quarantine. The next modules develop SQL, dataframe, partitioned, incremental, merge, backfill, correction, deterministic, and tested batch transformations.

## Governing Question

Given one source population and one target product, which operations must occur before the first target load, which should run inside the target engine, which evidence must survive both, and how will the team prove the placement preserves intended semantics under failure and replay?

ETL and ELT are often presented as competing eras. The more useful question is where a particular transformation belongs. Decompression and framing may have to occur in a connector. Sensitive-field minimization may be required before a shared platform. Large joins may be best inside a warehouse. A custom model may need a dataframe engine. A final view or materialization may execute in a serving database.

The word “load” is relative. If a connector writes source bytes to object storage and later transforms them before loading a warehouse, that path is ETL relative to the warehouse but ELT relative to the object store. Without naming the target boundary, architecture diagrams can disagree while describing the same pipeline.

Placement can change results. A target loader might coerce decimal scale, normalize time zones, collapse invalid strings to null, apply defaults, or reject duplicates before target SQL runs. A pre-load transformation might omit unknown fields, join mutable reference data, or aggregate away occurrence identity. The algebra does not commute merely because column names match.

The governing question therefore joins semantics and operations: source fidelity, transformation expressiveness, security, engine capability, publication, retry, lineage, quality, source/target impact, cost, and team ownership all matter.

## Why This Matters

Transformation placement establishes the recovery boundary. If raw source evidence is loaded durably before business transformation, many defects can be recomputed without rereading the source. If an ETL engine transforms directly from a finite source and retains only curated output, a parser or rule bug may be irreversible. ETL can avoid that by landing immutable raw outside the analytical target first.

Placement establishes the security boundary. Pre-load minimization/tokenization can prevent sensitive fields from entering a multi-tenant or broadly queried warehouse. Conversely, transforming in an isolated external engine can create unmanaged copies, credentials, and egress. “ELT is flexible” is not permission to centralize prohibited raw data.

Placement affects semantics. Parsing before versus after target type conversion, joining before versus after snapshotting reference data, and filtering before versus after deduplication can create different rows. Engines also differ in collations, decimal arithmetic, timestamp handling, null ordering, transaction behavior, and nondeterministic ties.

Placement affects performance and cost. Pushdown can reduce network transfer and exploit engine indexes/parallelism, but can burden an operational source or consume scarce warehouse slots during peak analytics. External compute can isolate workloads and use specialized libraries, but adds serialization, movement, and platform operations.

Placement affects ownership. Warehouse SQL is often visible to analysts and governed through centralized permissions/lineage. External code may offer better testing and expressiveness while fragmenting observability. A durable design assigns each stage, contract, deployment, incident, and cost to an owner.

Most production systems are hybrid: extract to immutable raw, normalize/enforce critical contracts in a processing layer, bulk load standardized tables, and perform business modeling in a warehouse. Hybrid is not indecision when each boundary has a reason and verification.

## Prerequisites and Retrieval

Retrieve source and target owners; business questions and output grain; source systems/epochs, cuts, snapshots, logs, files, APIs, queues, and retention; extraction scope, filters, keys, deletes, ordering, transactions, schemas, encodings, time zones, precision, volume/change rate; network/egress and source-load budgets; raw landing and replay horizon; target engine/version, regions, storage/compute architecture, load interfaces, table formats, transaction/DDL semantics, constraints, indexes, partitioning/clustering, concurrency and workload management; transformation operations; required libraries/languages/models; reference/lookup data and valid-time snapshots; security classification, residency, minimization, masking/tokenization, encryption, credentials and tenant isolation; staging/publish/rollback; full/incremental/CDC semantics; idempotency, deduplication and quarantine; code/config/runtime/schema versions; orchestrator; quality controls; lineage; tests; SLOs; observability; cost models; team skills/on-call; disaster recovery; and audit/regulatory requirements.

Distinguish source-side filter from governed transformation; lossless projection from lossy minimization; landing store from analytical target; staging from trusted output; raw object from typed raw table; load append from merge or replacement; physical movement from logical publication; SQL pushdown from ELT as a whole; same expression from same engine semantics; target transaction from orchestrator task; statement success from complete dataset; table name from immutable generation; current lookup from versioned reference input; event occurrence from entity state; extraction time from source cut; incremental watermark from output checkpoint; data-quality warning from publication gate; replay from duplicate append; runtime cost from total system cost; and architectural label from verified behavior.

Create a placement matrix for every operation:

| Operation | Candidate location | Evidence needed |
|---|---|---|
| Source filtering | source query/connector | source impact, stable predicate, completeness, audit, pushdown semantics |
| Decode/type | connector, external engine, target | writer schema, invalid handling, precision/time/collation equivalence |
| Security minimization | before shared landing or governed target | legal/policy boundary, irreversibility, recovery and key controls |
| Dedup/version merge | processing layer or target | identity, concurrency, ordering, tombstones, idempotence |
| Large join/aggregation | target or distributed engine | snapshots, skew, shuffle, numeric/order semantics, cost/contention |
| Business modeling | warehouse SQL/semantic layer | grain, metrics, tests, accessibility, lineage, publication |
| Specialized algorithm | dataframe/ML/runtime | reproducibility, serialization, dependencies, observability |
| Final serving projection | target/serving store | latency, constraints, atomic switch, consumer contract |

Do not decide from a generic checklist alone. Prototype representative data, reproduce edge semantics, measure resource use, and test failure/recovery in the candidate engines.

## Learning Objectives

After completing this module, you should be able to:

1. define ETL and ELT relative to a named analytical target and identify hybrid designs;
2. model extraction, transformation, load, staging, and publication as separate contracts;
3. explain and test why moving transformation across a load can change semantics;
4. preserve replayable raw evidence in both ETL- and ELT-oriented architectures;
5. choose transformation placement from security, source impact, engine ability, latency, cost, ownership, and recovery constraints;
6. specify append, replace, merge, snapshot, transaction, and visibility semantics for every load;
7. implement full/incremental/delete/late-data flows with stable identity and checkpoints;
8. version code, schemas, references, runtime, and target behavior for deterministic replay or explicit recomputation;
9. validate quality, lineage, performance, and cost across all stage boundaries; and
10. design and review an atomic, observable, recoverable hybrid batch pipeline.

## Core Exposition

### Name the target before choosing the acronym

ETL means transformation occurs before load into a particular target; ELT means a source-faithful representation loads into that target before transformation there. A pipeline can be ELT relative to a lakehouse raw table and ETL relative to a downstream serving database.

Draw all durable boundaries: source, connector buffer, immutable landing, typed raw, standardized, curated, semantic, and serving. Mark which are authoritative, replayable, staging, or trusted. Then describe operation placement directly. The acronym becomes shorthand, not architecture.

Use “source-faithful” instead of “unchanged” when the extractor already performs logical decoding, SDK parsing, decompression, redaction, or projection. Record those acquisition transformations as [DE-030](030-designing-replayable-raw-ingestion.md) requires.

### Model the two compositions

Let $E$ capture source population $I_c$ at cut $c$. In an ETL path, external/pre-target $T_s$ produces target-ready data and $L_c$ loads it. In ELT, $L_r$ loads a faithful raw/staging representation and target-native $T_t$ produces trusted output:

$$
Y_{ETL}=L_c(T_s(E(I_c))),\qquad Y_{ELT}=T_t(L_r(E(I_c))).
$$

The functions include failure and side-effect semantics, not only row values. Equivalence requires same grain, types, nulls, ordering, filters, reference cuts, duplicates, errors, outputs, and publication. In general,

$$
L_c\circ T_s\not\equiv T_t\circ L_r.
$$

Test whether a target-native $T_t$ is constructed to compensate for any representation differences introduced by $L_r$. If $L_r$ loses required information, no downstream transform can reconstruct it.

### Separate acquisition from business transformation

Some operations are required simply to establish a readable boundary: authenticate, frame messages, validate transfer checksum, decompress safely, locate records, and associate writer schema. Others express business meaning: choose grain, calculate revenue, resolve customer identity, assign fiscal period, or enforce product policy.

Keep acquisition transformations narrow, versioned, and fidelity-preserving. Do not hide business filtering in a connector where lineage/testing/replay are weak. Conversely, do not postpone basic payload safety until arbitrary warehouse users query hostile bytes.

Represent both stages in lineage so a reader knows whether a value came directly from source, acquisition normalization, or business transformation.

### Preserve a replayable boundary in either architecture

ELT naturally can retain source-faithful data in the target platform, but only if raw tables/objects are immutable/versioned, complete, access-controlled, schema-resolvable, and retained. A mutable table loaded with `TRUNCATE` is not replayable merely because it is named `raw`.

ETL can be equally replayable by landing immutable source artifacts before transformation, even though the analytical warehouse sees only target-ready data. The landing platform is a separate target for recovery, not necessarily the target named by ETL.

If security policy forbids raw in the warehouse, pre-target tokenization/minimization may be mandatory. Preserve only legally permitted replay evidence, keys/mappings under stronger control, and explicit limitations.

### Define extraction once

Both ETL and ELT begin with source semantics: consistent full snapshot, bounded incremental watermark, file manifest, API cursor/cut, CDC log positions, or broker offsets. Record source identity/epoch, scope, filters, schema, ordering, transactions, deletes, and checkpoint.

Do not let ETL and ELT prototypes read different source cuts and compare output. Extract once into an immutable manifest when evaluating placement. Otherwise source changes confound engine differences.

Minimize source impact. Predicate/column pushdown can reduce transfer, but prove filters are stable and do not discard evidence needed for reconciliation or future transformation. Use replicas/export facilities only under documented consistency.

### Define the load verb precisely

“Load” may mean append rows, insert-if-absent events, overwrite a partition, replace a complete snapshot, merge versioned current state, create a new immutable table, or publish a view/pointer. These operations are not interchangeable.

For each target specify target object/generation, input manifest, uniqueness/version key, schema coercion, null/default behavior, delete/tombstone handling, transaction boundary, isolation, error mode, row/byte limits, retry identity, visibility, validation, and rollback.

PostgreSQL documents that `COPY FROM` inserts file fields into a table and appends to existing contents. It is a bulk transfer primitive, not an automatic deduplication, merge, or atomic dataset publication protocol. Stage and validate, then use appropriate target transactions/conditional publication.

### Stage before trusted publication

Write to attempt/generation-specific staging tables or immutable objects. Validate exact input membership, schema, counts, keys, duplicates, nulls, relationships, controls, and quarantines. Transform/merge from staging into a new target generation or one transactionally protected target change.

Trusted readers must not observe partial chunks. Publish through table swap/rename, view or catalog pointer, transactional merge plus receipt, or table-format snapshot under verified target semantics. A successful loader command may still precede final controls.

Do not use staging names based only on wall-clock or worker ID as logical identity. Bind them to immutable input manifest and transformation/run attempt; garbage collection must avoid active or published generations.

### Account for target transaction semantics

Products differ in DDL, DML, autocommit, temporary tables, transactional table formats, and client behavior. Retrieve exact engine/version rules before composing load and publish statements.

Snowflake documents that DDL statements execute as separate transactions and implicitly commit an active transaction. That matters for patterns that expect `CREATE OR REPLACE`, `ALTER`, and DML to roll back together. Similar-looking scripts can have different atomicity across engines.

Use transaction receipts and post-timeout lookup for ambiguous commits. Orchestrator success flags are not a substitute for target commit evidence.

### Use target-native load interfaces deliberately

Warehouse load jobs often ingest object files more efficiently than row-by-row inserts. BigQuery documents batch and streaming ingestion paths, supported sources/formats, and load-job configuration. Treat each as an interface with schema, write disposition, job identity, quotas, error, and visibility semantics.

Record source object versions/digests and target job ID. On timeout, query job/target state rather than issue a new append blindly. Use staging or idempotent generation names so job retry cannot duplicate logical units.

Separate physical ingestion completion from semantic transformation/publication. A raw table can finish loading while curated quality gates remain pending.

### Use external transformation engines where they fit

External/distributed runtimes support custom code, complex parsers, reusable libraries, graph/ML algorithms, streaming/batch unification, and resource isolation from the warehouse. They can scale shuffles and state under independent compute.

Apache Beam's programming guide models pipelines as transforms over `PCollection`s with I/O, windowing, state, and runner execution. That abstraction provides portability and composability, but actual I/O guarantees, coder/schema behavior, ordering, side inputs, runner semantics, and sink idempotence still require verification.

External processing adds serialization boundaries, temporary storage, credentials, network movement, dependency/runtime management, and separate observability. Preserve manifests and schema/type fidelity across them.

### Use target transformation where it fits

ELT target SQL can exploit co-location, column pruning, predicate pushdown, joins, aggregation, workload management, snapshots, access controls, catalog metadata, and analyst familiarity. It avoids moving large raw tables out for routine relational modeling.

dbt's explanation of ELT reflects loading data to a warehouse before transformation and using warehouse compute. That workflow can improve modular SQL and lineage, but correctness still depends on raw fidelity, target semantics, deterministic models, tests, publication, and cost controls.

Not every transformation belongs in SQL. Complex stateful algorithms, unsafe parsing, unsupported libraries, or operations that would monopolize target resources may fit another engine. Hybrid boundaries should exchange immutable versioned datasets.

### Push down only safe operations

Source-side pushdown can reduce transfer and target cost. It can also load the production database, change semantics through source collation/time zone/types, and discard data before replay. Limit concurrency, use stable predicates/indexes, record query/plan and source cut, and compare controls.

Target pushdown keeps computation near data but competes with interactive/serving workloads. Use workload pools/warehouses, budgets, query tags, limits, and schedules. Materialize repeated expensive subexpressions only with versioned dependencies and lifecycle ownership.

Pushdown decisions are per operation. A pipeline may parse proprietary binary externally, load standardized columns, then join and aggregate in the warehouse.

### Preserve type semantics across the load boundary

Define parse/coercion order for decimal precision/scale/rounding, integer overflow, floating NaN/infinity/signed zero, timestamps/time zones/DST, dates, intervals, strings/Unicode/collation, binary values, booleans, nested types, null/empty/missing, defaults, enums, arrays/maps, and invalid values.

If $L_r$ coerces before $T_t$, result can differ from $T_s$ before $L_c$. For value 10.005, a raw target column rounded half-even to two decimals stores 10.00; a business transform requiring half-up cents would have produced 10.01 from the original. Loading into an insufficient type destroyed the distinction.

Use sufficiently faithful raw target types or preserve original bytes/string alongside parsed fields. Fail/quarantine invalid values explicitly; never let engine-specific coercion silently convert them to null or truncate.

### Preserve null, default, and missing distinctions

Source missing field, explicit null, empty string, defaulted target column, invalid parse, redaction, and not-applicable may carry different meaning. Load interfaces can collapse them depending on format and column list.

PostgreSQL `COPY`, file formats, and warehouse loaders expose configurable null and default behaviors. Test round trips and edge cases. Record presence indicators or raw payload where schema requires distinctions.

Applying target defaults during raw load can make a value look source-provided. Prefer lineage fields or defer defaults to a named transformation whose rule/version is visible.

### Snapshot reference data

Joins and lookups are transformation inputs. If ETL calls an operational service and ELT joins a current warehouse dimension, they can differ even at the same fact cut. Choose a compatible reference snapshot/valid-time rule and include it in the transformation contract.

Avoid row-by-row remote lookups that are slow, failure-prone, and time-skewed. Extract/materialize the reference once at a declared cut, then join deterministically. Record missing/multi-match policy and relationship controls.

Replaying with today's dimension is recomputation unless the business contract intentionally uses “knowledge now.” Keep original reference snapshot for reproduction.

### Make security placement explicit

Classify every source field before moving it. Determine whether raw may enter the analytical target, who can query it, which regions/accounts may process it, and whether minimization/tokenization/masking/encryption must occur first.

Pre-load privacy transformation reduces target exposure but can be irreversible and concentrate mapping keys in an external service. ELT centralizes raw with warehouse controls but expands the high-fidelity dataset's access and breach radius. Evaluate both end to end.

Use least-privilege service identities by stage, private networking, secret management, encryption/key ownership, row/column policies, audit, egress controls, temporary-file cleanup, and safe quarantine. Avoid copying sensitive values into logs/lineage.

### Handle full replacement atomically

For full snapshots, do not truncate trusted target before extraction/transformation succeeds. Build a new generation, validate source cut, schema, counts, keys, relationships and controls, then conditionally switch trusted pointer/view/table metadata.

Keep previous generation for rollback within policy. A rerun of the same manifest should produce/reuse one generation by idempotency key. If transformation code changes, publish a distinct version even when target name stays stable.

ETL and ELT both can implement this pattern: only the compute location differs.

### Handle incremental state and deletes

Incremental ETL may filter/transform deltas before target merge; incremental ELT may load raw deltas then merge in target SQL. Both require source occurrence identity, comparable version/watermark, late-data policy, tombstones, snapshot handoff, deduplication, checkpoint, and replay.

Do not infer delete from absence in a delta. Preserve source delete operation and version. Conditional merge prevents older replay from resurrecting a tombstoned entity.

Checkpoint advances only after authoritative raw and required target effects/receipts are durable. If raw is authoritative, slow transformations can replay independently without holding source retention.

### Define quality gates at each boundary

At extract: source scope/cut, manifest/range, schema, count/bytes, checksums, control totals. At raw load: exact membership, object/job receipts, types/encoding, duplicates/conflicts, quarantine. At transform: grain, keys, domains, joins, calculations, invariants, reference coverage. At publish: output manifest, relationships, freshness, lineage, security, consumer contract.

A pre-load ETL validator can reject invalid rows before target exposure; an ELT design can load them into restricted raw and exclude them from standardized output. Either path must reconcile every input disposition.

Avoid using one passing row count as equivalence evidence. Compare key sets, row digests at stable grain, types, nulls, totals, distributions, and domain invariants at compatible cuts.

### Design failure and retry boundaries

Identify atomic unit for each stage: object, partition, source transaction, batch, model, or complete generation. Persist attempt and logical unit separately. Use stable idempotency keys and immutable staging so retries neither append duplicates nor overwrite good output.

On failure, determine whether source acquisition, raw load, transformation, target load, quality gate, or publication committed. Query receipts/manifests rather than infer from process exit. Quarantine deterministic input failures and circuit-break systemic failures as [DE-029](029-quarantine-and-dead-letter-data.md) specifies.

Rollback means leave trusted pointer unchanged or execute a validated target transaction/compensation. Deleting visible partial rows after consumers read them is not atomic rollback.

### Version transformation artifacts and environments

Record code commit/artifact digest, SQL/model version, configuration, schemas, runtime/container, packages, UDFs, target engine/release/settings, reference snapshots, feature flags, locale/time zone, random seed, and orchestrator parameters as needed.

Warehouse views and stored procedures can change under stable names. Snapshot definitions or deploy immutable versioned models and record compiled SQL/query text. External containers can also float base images or package downloads; preserve artifact provenance.

Define whether replay must reproduce original output or intentionally use corrected/latest rules. Never reuse the same output generation identity for different contracts.

### Plan schema evolution across placements

A producer can add, remove, rename, reorder, or change the type/meaning of a field. The extraction boundary must preserve writer schema and unknown data permitted by format; the raw load must not silently narrow it; the transformation must select an explicit reader/output schema; and publication must enforce the consumer contract.

In ETL, a pre-target parser can block a new source field before the warehouse ever sees it. That may protect a strict target but can lose history if raw bytes/schema were not retained. In ELT, permissive raw landing can preserve the field, but a target loader may infer unstable types across batches or coerce incompatible rows. Disable uncontrolled inference at governed boundaries, version schemas, and test compatibility deliberately.

Coordinate dual-read/dual-write or additive transitions where necessary. Backfill new columns from the same immutable source/reference cuts, distinguish default from historically unknown, and do not claim old rows had a producer value simply because the target now supplies one. For destructive changes, publish a new output contract/generation and maintain deprecation windows for consumers.

Record schema fingerprints at source, raw, standardized, and curated stages. Reconcile column identity, not only names: a rename differs from drop-plus-add when lineage/history matters. Test old writer/new reader, new writer/old reader, null/default, enum/domain expansion, nested evolution, precision narrowing, and rollback in every execution engine used.

### Separate the control plane from data execution

The control plane selects immutable input manifest, transformation contract, target generation, dependencies, attempt, and expected predecessor. The data plane reads those exact inputs and writes attempt-scoped outputs. Workers should not independently discover “latest” source files, schemas, reference tables, or target pointers.

Represent run state explicitly: planned, acquiring, landed, transforming, validating, ready-to-publish, published, failed, superseded. Transitions use durable receipts or conditional updates. A worker heartbeat or process exit does not advance semantic state; published is reached only after target evidence and quality gates.

Pass manifest and artifact identities between ETL and ELT stages rather than enormous mutable parameter lists or directory names. This makes retries, audits, and backfills reconstructable and lets the orchestrator query ambiguous outcomes. Attempt IDs remain separate from logical generation/idempotency IDs.

Isolate live, backfill, canary, and disaster-recovery runs by output namespace and workload policy while allowing them to reuse immutable inputs. Require conditional publication against an expected predecessor so a slow older backfill cannot overwrite a newer trusted generation. Garbage collection reads control-plane references and retention state before deleting staging.

### Capture lineage across engine boundaries

Lineage should connect source dataset/version and raw manifest to transform job/run, code/config/schema/reference versions, intermediate datasets, target output generation, quality decisions, and consuming products.

OpenLineage's object model defines datasets, jobs, runs, and runtime/design metadata events. Such a model can standardize cross-tool observation, but emitted lineage must still identify immutable dataset versions and be reconciled with actual manifests/target commits.

Do not consider lineage complete because a SQL parser inferred table names. Dynamic SQL, external code, temporary files, API lookups, UDFs, row/column logic, and failed/unpublished attempts require explicit evidence.

### Evaluate latency and throughput

For non-overlapped batch stages, approximate elapsed time as

$$
T_{batch}=T_E+T_{transfer}+T_T+T_L+T_{validate}+T_{publish}+T_{queue}.
$$

With safely pipelined steady-state stages, throughput is bounded by the bottleneck:

$$
r_{pipeline}\le\min(r_E,r_T,r_L).
$$

These simple models omit startup, skew, retries, spill, contention, autoscaling, rate limits, and transaction barriers. Measure percentiles and resource profiles on representative volumes.

ETL can overlap extract/transform/load but may complicate atomic generation completeness. ELT can load quickly and transform asynchronously, but consumer freshness is not raw-load freshness. Define SLO at the trusted output boundary.

### Evaluate total cost and contention

Model at least

$$
C_{total}=C_{source}+C_{network}+C_{compute}+C_{storage}+C_{target\ contention}+C_{operations}+C_{recovery}.
$$

Include source query/I/O/cache impact, egress, external and warehouse compute, intermediate/raw copies, concurrency queues, licensing, engineering/on-call, failed runs, replay/backfill, and retention. One cheap successful run can hide expensive incidents.

Use workload tags and per-stage metrics. Compare representative transformations and recovery exercises, not vendor list price alone. Account for data growth, skew, compression, and peak concurrency.

### Choose a hybrid intentionally

A common durable shape is:

1. extract once at a source cut into immutable replayable raw;
2. perform mandatory safe decode, contract validation, and privacy controls in an isolated standardization layer;
3. bulk load standardized data with manifests into the analytical platform;
4. execute relational business models near warehouse data;
5. export only governed serving outputs; and
6. publish each boundary atomically with lineage/quality evidence.

This is not universally optimal. A small regulated source may transform fully before any shared storage. A warehouse-native connector may load raw directly. A graph/ML workload may remain external. The point is explicit placement and proof.

### Test semantic equivalence and failure

Use one immutable source manifest and golden edge cases. Run candidate ETL and ELT paths, normalize only declared physical differences, and compare exact keys, values/types, ordering when meaningful, nulls, deletes, quarantines, totals, distributions, and lineage.

Test precision/scale edges, overflow, NaN, invalid encoding, Unicode/collation, DST gaps/folds, missing/default/null, duplicate keys, same-version conflicts, late changes, deletes, reference multi/no-match, nondeterministic peers, and schema evolution.

Inject crash/timeouts before/after raw load, transform partitions, target load, transaction commit, quality gate, and publication. Retry, overlap, backfill, change code/reference, exhaust target/source resources, deny permissions, and restore from disaster. Verify one complete trusted generation or unchanged prior state.

## Definitions and Notation

Let:

- $I_c$ be the exact in-scope source population at cut/range $c$;
- $E$ be source extraction preserving declared identity and fidelity;
- $T_s$ be transformation outside/before the named analytical target;
- $L_r$ be faithful raw/staging load into that target/platform;
- $T_t$ be target-native transformation;
- $L_c$ be load of target-ready curated data;
- $Y_{ETL}$ and $Y_{ELT}$ be published outputs;
- $M_I$ be immutable input manifest;
- $V_T$ be transformation contract/artifact version;
- $M_Y$ be output manifest/generation;
- $P$ be trusted target pointer;
- $r_E,r_T,r_L$ be sustainable stage throughputs; and
- $C_{total}$ be total lifecycle cost under a declared horizon/workload.

The two placements are

$$
Y_{ETL}=L_c(T_s(E(I_c))),\qquad Y_{ELT}=T_t(L_r(E(I_c))).
$$

Semantic equivalence on permitted source populations $mathcal{I}$ requires

$$
\forall I_c\in\mathcal{I}:L_c(T_s(E(I_c)))\equiv T_t(L_r(E(I_c))),
$$

where $\equiv$ includes the declared row/value/type/order and side-effect/publication contract. A single sample equality does not prove this universal condition.

If a load transformation $L_r$ is lossy with respect to required information, there can be $x\ne y$ such that $L_r(x)=L_r(y)$. No later deterministic $T_t$ can distinguish $x$ from $y$, so it cannot generally reproduce a pre-load $T_s$ that assigns different outputs to them.

For serial stages, batch time is approximately additive; for safe overlapped stages, throughput is bottlenecked as above. These are capacity approximations, not correctness results.

## Mechanisms, Invariants, or Proof Structure

**Conditional placement-equivalence theorem.** Suppose ETL and ELT consume the same complete immutable $I_c$; $L_r$ preserves every distinction required by $T_s$; $T_t$ implements the same transformation contract as $T_s$ under equivalent type, null, time, numeric, ordering, reference, and error semantics; $L_c$ and target publication yield equivalent output state/side effects; and both paths are deterministic/idempotent. Then $Y_{ETL}\equiv Y_{ELT}$ under the declared output relation.

**Proof sketch.** Same $I_c$ and equivalent extraction give the same logical input. Lossless-enough $L_r$ retains all distinctions consumed by $T_s$. Equivalent $T_t$ maps that representation to the same logical transformed relation as $T_s$. Equivalent curated load/publication yields the same visible generation and effects. Determinism/idempotence remove execution-order/retry multiplicity. Any lossy coercion, different reference cut, engine semantic mismatch, error-policy difference, or publication side effect breaks a premise.

**Named-target invariant.** ETL/ELT terminology always names the target relative to which load occurs; operation placement remains explicit across every durable boundary.

**Source-cut invariant.** Comparisons and production paths consume the same declared source cut/range, schema/scope, identity, deletes, and transaction/order evidence.

**Raw-fidelity invariant.** Highest-required source evidence becomes durable before lossy transformation/acknowledgement, whether outside or inside the analytical target.

**Type-order invariant.** Parse, coerce, default, normalize, round, filter, deduplicate, join, and aggregate order is part of $V_T$; moves across $L_r$ require equivalence evidence.

**Load-semantic invariant.** Every load declares append/insert/replace/merge/snapshot behavior, key/version/delete logic, transaction, retry identity, and visibility.

**Publication invariant.** Trusted $P$ changes only to a complete validated immutable $M_Y$ under conditional/transactional target semantics; staging remains untrusted.

**Incremental invariant.** Source progress never exceeds authoritative raw and required durable effects; replay preserves occurrence/effect identity and older versions cannot regress state.

**Dependency invariant.** Code, configuration, schemas, runtime/libraries, target settings, reference snapshot, time/randomness, and quality policy required by $V_T$ are versioned/resolvable.

**Security invariant.** Each transfer/storage/compute location is authorized for the data classification, tenant, residency, keys, credentials, and retention involved.

**Quality-lineage invariant.** Input, intermediate, quarantine, and output identities reconcile; every trusted result traces to source manifest and transformation contract across engine boundaries.

**Cost/evidence boundary.** Benchmarks and cost estimates establish behavior only for measured volume, skew, concurrency, engine configuration, price period, failure load, and recovery horizon; they do not prove semantic equivalence.

<!-- bijux-verify: {"id":"etl-elt-placement","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"source_records=3\netl_rows=2\nelt_rows=2\nequivalent_lossless=True\netl_total_cents=3006\nlossy_elt_total_cents=3005\nnoncommutative_lossy=True\nfiltered_records=1\nreplay_stable=True\n","stderr":""}} -->
```python
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP

source = (
    ("a", "10.005", "keep"),
    ("b", "20.05", "keep"),
    ("c", "7.00", "drop"),
)

def transform(records):
    result = []
    for key, raw_amount, disposition in records:
        if disposition != "keep":
            continue
        amount = Decimal(raw_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        result.append((key, int(amount * 100)))
    return tuple(sorted(result))

def lossless_raw_load(records):
    return tuple(records)

def lossy_raw_load(records):
    loaded = []
    for key, raw_amount, disposition in records:
        coerced = Decimal(raw_amount).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        loaded.append((key, str(coerced), disposition))
    return tuple(loaded)

etl = transform(source)
elt = transform(lossless_raw_load(source))
lossy_elt = transform(lossy_raw_load(source))
replay = transform(lossless_raw_load(source))
print(f"source_records={len(source)}")
print(f"etl_rows={len(etl)}")
print(f"elt_rows={len(elt)}")
print(f"equivalent_lossless={etl == elt}")
print(f"etl_total_cents={sum(amount for _, amount in etl)}")
print(f"lossy_elt_total_cents={sum(amount for _, amount in lossy_elt)}")
print(f"noncommutative_lossy={etl != lossy_elt}")
print(f"filtered_records={len(source) - len(etl)}")
print(f"replay_stable={etl == replay}")
```

The executable fixture models one immutable input, business half-up rounding before curated load, lossless raw load before the same transformation, and a deliberately lossy half-even target coercion before transformation. It demonstrates one counterexample to moving a transform across a load. It does not prove general ETL/ELT equivalence, database type behavior, distributed execution, security, transactions, cost, or target publication.

## Alternatives and Trade-Offs

**ETL before the analytical target.** Supports pre-load minimization, specialized runtimes, source-to-target shaping, and controlled target schemas. It risks lossy early transformation, separate infrastructure, movement, and weaker analyst accessibility if raw/replay is omitted.

**ELT inside the analytical target.** Retains flexible source-faithful data near scalable SQL and centralized governance. It expands raw storage/access/cost, depends on target semantics, and can contend with analytical workloads.

**Hybrid raw–standardized–curated.** Separates recovery, contract enforcement, and business modeling across suitable engines. It adds boundaries, copies, manifests, lineage, and operational coordination; those costs buy explicit trust stages.

**Source pushdown versus full extract.** Pushdown reduces transfer and can use source indexes. Full capture maximizes replay/future use but raises source/network/storage/security cost. Stable incremental predicates and raw retention can balance them.

**Warehouse SQL versus dataframe/distributed code.** SQL offers declarative optimization, accessibility, and target locality. Code offers libraries, custom algorithms, stronger modular typing/testing in some teams. Cross-engine equivalence and serialization must be governed.

**Target load job versus row streaming.** Batch load is efficient and manifest-friendly but adds latency. Streaming reduces latency but multiplies small commits/state/retry complexity. Trusted output SLO, not ingestion fashion, decides.

**Mutable table versus immutable generation.** Mutation/merge reduces storage and can serve low-latency current state. Generations simplify validation, rollback, reproducibility, and atomic switch. Hybrid tables can use transactional snapshots plus versioned changes.

**Transform-on-write versus transform-on-read.** Write-time materialization gives stable performance/contracts but incurs recompute/storage. Read-time views stay flexible but repeat cost and can change when definitions/dependencies change. Version definitions and materialize high-value boundaries.

**One monolithic job versus modular stages.** One transaction/process can reduce intermediate complexity but enlarges retry and review scope. Modular datasets improve test/reuse/lineage while requiring atomic dependency publication and avoiding partial chains.

**Strict schema before load versus permissive raw types.** Strict typing catches defects early and protects consumers. Permissive raw preserves unexpected values for later handling. Use restricted faithful raw plus strict standardized/curated boundaries rather than silently coercive permissiveness.

**Separate compute versus warehouse contention.** External compute isolates interactive workloads but adds platform/network operations. Warehouse compute uses managed scaling/locality but needs workload governance and cost controls.

**Reproduce original versus apply latest rules.** Original bundles support audit/debug. Latest/corrected rules support restatement. Preserve input/output generations and name the intent; do not conflate them.

## Failure Modes and Misconceptions

**“Modern means ELT; ETL is obsolete.”** Both are placements with valid security, source, engine, skill, and recovery constraints. Most systems combine them.

**“A lake/object landing makes the whole pipeline ELT.”** Only relative to the named target. Transformation can still precede warehouse load.

**“ELT means raw is replayable.”** Mutable/partial/unversioned raw without manifests, schemas, identities, retention, and tests is not.

**“ETL means raw cannot be retained.”** ETL can land immutable source evidence outside the analytical target before transformation.

**“Moving SQL between engines preserves results.”** Types, collations, null ordering, decimals, timestamps, functions, transactions, and optimizers differ. Test semantic equivalence.

**“Loading first is lossless.”** Target column types, parsers, defaults, constraints, invalid handling, and dedup can discard distinctions before target transforms.

**“Transforming first is safer.”** It can erase unknown fields, original encoding, identity, or audit evidence. Preserve authorized raw before lossy work.

**“`COPY` is an upsert.”** PostgreSQL `COPY FROM` appends rows; merge/dedup/publication require separate logic.

**“Bulk-load success means table complete.”** Expected membership, controls, quarantines, model outputs, and trusted publication still need validation.

**“Truncate and reload is atomic enough.”** Readers can see empty/partial state after failure. Build a new generation and switch conditionally.

**“One transaction script rolls back everywhere.”** DDL/DML/autocommit semantics differ; Snowflake DDL implicitly commits active transactions. Retrieve target rules.

**“Current lookup data is fine on replay.”** It changes results unless current-knowledge recomputation is intended. Pin reference snapshots.

**“Push every filter to source.”** It can harm operations and destroy replay/completeness evidence. Push only stable safe predicates with controls.

**“Push all transforms to warehouse.”** Specialized algorithms, unsafe parsing, security minimization, or workload isolation may belong elsewhere.

**“Same row count proves ETL/ELT equivalence.”** One missing and one extra row, type drift, value changes, delete errors, and duplicate substitutions can preserve counts.

**“Latest row resolves incremental state.”** Ingestion timestamps and nondeterministic peers can regress state. Use source identity/version/tombstones.

**“Retries can append again.”** A retry must reuse logical input/effect identity and target receipt/generation.

**“Lineage is just table names.”** Versions, fields, code/config/schema/reference, runs, failures, and publication connect actual data.

**“Raw-load freshness equals product freshness.”** Consumers need transformed, validated, published output; measure SLO there.

**“Cheapest query is cheapest architecture.”** Include source impact, network, storage, contention, operations, failures, and recovery.

## Worked Examples

### Example 1

A regulated source contains national IDs prohibited in the shared warehouse. Extraction lands encrypted raw in a restricted account, tokenizes identifiers under a controlled service, validates mapping receipts, and loads standardized tokens to the warehouse for SQL modeling. Relative to the warehouse this is ETL; relative to restricted raw it includes ELT. The placement follows policy, not fashion.

### Example 2

A SaaS API emits nested JSON with frequent optional fields. A connector preserves response bytes and source cursor in object raw, then loads source-faithful nested rows into a warehouse. Analysts build versioned target SQL models. This is ELT relative to the warehouse, with raw object evidence guarding against warehouse loader/schema-loss defects.

### Example 3

ETL parses `10.005` and applies business half-up rounding to 10.01. An ELT prototype first loads into a `NUMERIC(...,2)` column under half-even conversion, storing 10.00. The same downstream expression cannot recover the lost half-cent. The team changes raw column fidelity or performs governed parsing before load.

### Example 4

A PostgreSQL staging load uses `COPY FROM` for speed. A retry after lost acknowledgement would append duplicates if issued blindly. The pipeline loads into a generation-specific staging table keyed by input manifest, queries target receipt on ambiguity, validates exact keys/counts, then transactionally merges or publishes. `COPY` is only physical transfer.

### Example 5

A Snowflake script creates a replacement table, loads rows, validates, and swaps names inside what the author assumes is one rollback unit. Documentation shows DDL commits separately. The team redesigns publication around verified Snowflake semantics, immutable table identity, validation state, and a recoverable conditional pointer/swap rather than cross-engine transaction assumptions.

### Example 6

A 20-terabyte fact join is executed in the warehouse where both facts and versioned dimensions live. Column pruning, clustering, and elastic workload-isolated compute avoid exporting data. A specialized probabilistic identity model remains external and writes a versioned mapping dataset back. The pipeline is intentionally hybrid.

### Example 7

An incremental order feed loads raw CDC events, including tombstones and source versions, then target SQL selects one winner per entity with explicit equal-version conflict. Checkpoint advances after raw receipt; curated publication advances after merge receipt. A delayed older update becomes stale and cannot resurrect a deleted order.

### Example 8

Two implementations consume the same immutable manifest. ETL uses Python decimal and ELT uses target SQL. Row counts match, but key/digest comparison finds differences at negative half values because rounding modes differ. The contract names half-away/half-up behavior and both implementations adopt explicit compatible functions before migration.

### Example 9

A current currency table caused a historical replay to change totals. The transformation contract now includes a content-addressed rate snapshot and valid-time join rule. Original reproduction pins the old snapshot; a corrected recomputation uses a new snapshot, publishes a distinct output generation, and records expected deltas/downstream restatement.

### Example 10

A benchmark says warehouse ELT is 30% cheaper for one normal run. A recovery test shows warehouse contention delays backfills and current raw retention costs dominate; an external engine adds egress but isolates recovery. The team compares annual source, transfer, compute, storage, contention, operations, and replay scenarios before selecting a hybrid and documenting assumptions.

## Cross-Program Connections

**Database Engineering.** Bulk load, staging, constraints, transactions, DDL/autocommit, isolation, indexes, merge, snapshots, and query optimization determine target semantics.

**Distributed Systems.** Delivery, idempotence, checkpoints, atomic publication, partitioning, retry, ordering, and failure ambiguity span every ETL/ELT boundary.

**Programming Languages.** Type systems, decimal/floating arithmetic, serialization, deterministic iteration, dependency locking, and runtime semantics affect cross-engine equivalence.

**Security Engineering.** Classification, minimization, tokenization, tenant isolation, credentials, egress, access audit, retention, and key ownership can mandate transformation placement.

**Platform Engineering.** Compute runtimes, warehouses, object stores, networks, catalogs, CI/CD, workload isolation, observability, cost controls, and DR make hybrid pipelines operable.

**Software Engineering Patterns.** Pure transformations, ports/adapters, unit of work, immutable artifacts, configuration, modular tests, and versioned interfaces improve pipeline maintainability.

**Data Architecture and Governance.** Raw/standardized/curated ownership, contracts, lineage, quality, semantics, access, and lifecycle determine trusted boundaries.

**Systems Engineering.** Placement trades source risk, data loss, privacy, semantic drift, contention, cost, and recovery across one socio-technical system.

## References

1. Amazon Web Services, [ETL vs. ELT—Difference Between Data-Processing Approaches](https://aws.amazon.com/compare/the-difference-between-etl-and-elt/). Provides a vendor comparison of transform-before-load and load-before-transform workflows, benefits, limitations, and hybrid considerations.
2. Google Cloud, [What Is ETL?](https://cloud.google.com/learn/what-is-etl). Describes extract, transform, and load stages, ETL/ELT distinctions, pipeline concerns, and cloud data-processing context.
3. dbt Labs, [Understanding ELT: Extract, Load, Transform](https://docs.getdbt.com/terms/elt). Explains warehouse-first loading and downstream transformation using target compute in an ELT workflow.
4. Apache Beam, [Beam Programming Guide](https://beam.apache.org/documentation/programming-guide/). Documents pipeline, `PCollection`, transform, I/O, schema, windowing, state, and runner concepts for portable processing.
5. PostgreSQL Global Development Group, [PostgreSQL: COPY](https://www.postgresql.org/docs/current/sql-copy.html). Documents copying between tables and files/program streams, append behavior, column/default/null/error options, progress, privileges, and transaction-related details.
6. Google Cloud, [Introduction to Loading Data into BigQuery](https://cloud.google.com/bigquery/docs/loading-data). Documents batch/streaming ingestion choices, supported sources/formats, load jobs, schema/write configuration, and related constraints.
7. Snowflake, [Transactions](https://docs.snowflake.com/en/sql-reference/transactions). Documents explicit/implicit transactions, autocommit, DML/query behavior, and separate/implicitly committing DDL semantics.
8. OpenLineage, [Core Specification: Object Model](https://openlineage.io/docs/spec/object-model/). Defines dataset, job, run, runtime/design event, and facet concepts for observing data lineage across platforms.

## Exercises

### Exercise 1

A team says, “We use ELT because files first land in object storage,” but files are transformed by Spark before entering its warehouse; the warehouse then runs more SQL transformations. Name targets and classify each segment. Propose an unambiguous architecture description, raw/replay boundary, and trusted publication points.

### Exercise 2

Source values are `10.005`, `-10.005`, and `20.05`. The business contract rounds halves away from zero to two decimals before aggregation. The ELT raw table coerces to scale 2 using half-even before SQL. Compute business-correct and pre-coerced totals, explain why placement is non-equivalent, and state a faithful target schema/processing remedy.

### Exercise 3

A full refresh currently truncates a production table, bulk loads 100 files, transforms in place, and marks the orchestrator task successful. Design an atomic ETL or ELT replacement using immutable input/output manifests, staging, quality controls, transaction/pointer behavior, retries, rollback, and consumer visibility.

### Exercise 4

Two candidate designs process 5 TB/day. Design A transforms at source and transfers 0.5 TB but adds 35% source CPU and cannot retain omitted fields. Design B loads 5 TB raw into the warehouse, uses 20% of warehouse daily compute, and exposes sensitive fields unless new controls are built. Build a decision analysis covering evidence and experiments rather than choose from these numbers alone.

### Exercise 5

Design a hybrid incremental pipeline from CDC through raw, standardization, warehouse modeling, and serving export. Specify source/checkpoint, identity/version/delete handling, schemas/types, quarantine, atomic boundaries, reference snapshots, deterministic artifacts, lineage, quality gates, retries, cost/performance metrics, and disaster/backfill replay.

## Answers to the Exercises

### Answer 1

Relative to object storage, extraction followed by raw object load and later Spark transformation is ELT if the objects are the named target and source-faithful. Relative to the warehouse, Spark transforms before warehouse load, so that segment is ETL; warehouse SQL after standardized load is ELT within the warehouse. Describe operations directly: “capture immutable source files into object raw; transform manifest `m` with versioned Spark contract into standardized files; bulk load generation-specific warehouse staging; run versioned SQL models; publish curated snapshot.” Raw replay boundary is the immutable source-file manifest with versions/digests/schemas and capture receipts. Standardized Spark output and curated warehouse output each need complete manifests, tests, lineage, and atomic/conditional trusted pointers; staging/listing is never publication.

### Answer 2

Half-away-from-zero/half-up at two decimals gives 10.01, -10.01, and 20.05, totaling 20.05. Half-even pre-coercion gives 10.00, -10.00, and 20.05, also totaling 20.05 for this symmetric set, so the aggregate happens to match while two row values are wrong. This is a valuable counterexample to total-only validation: placement is non-equivalent at row semantics even when the sum matches. Store the original decimal string or a decimal with at least scale 3 in raw, then apply explicit business rounding inside a supported target function; or perform the governed rounding before load while retaining replayable original raw. Validate exact keys/values and edge cases, not only totals.

### Answer 3

Freeze one input source cut and manifest listing all 100 immutable object versions/digests, schemas, counts, and controls. Load into a new attempt/generation-specific staging table or raw snapshot using stable job/idempotency identity; on timeout query receipts instead of append. Validate exact file membership, decode/quarantine, row/key counts, schema/types/nulls, duplicates, relationships, and source controls. Transform into a new output generation with pinned code/config/reference/runtime/target semantics and record output manifest/lineage. Only after every gate passes, conditionally switch a view/catalog/table-format snapshot or use verified target transaction/swap semantics so consumers move from prior complete generation to new complete generation. Leave the old trusted generation untouched on failure and retain it for rollback. The orchestrator marks success only after target publication receipt. Retry reuses input/output logical IDs; cleanup removes only unreferenced inactive staging after policy.

### Answer 4

First test both on the same immutable source cut with representative skew, schema evolution, deletes, failures, and backfill. For A, measure production latency/locks/cache/replica impact under 35% CPU, stability of source pushdown semantics, omitted-field future/replay/audit cost, security of external compute, network savings, and whether immutable pre-filter raw is required. For B, measure egress, 5-TB load latency/storage/retention, target transformation cost/queue/contention and 20% under concurrency, raw access breach radius, residency, row/column controls, minimization/tokenization alternatives, deletion, and recovery. Compare type/time/null semantics and output equivalence. Add engineering/on-call, lineage/testing, target/source SLOs, scaling/pricing, failed runs, disaster/backfill, and policy approval. Consider hybrid source-safe incremental extraction to restricted raw, pre-warehouse minimization, then warehouse ELT. The given percentages lack denominators, peaks, cost, risk, and semantic evidence, so they cannot decide alone.

### Answer 5

Capture committed CDC from a named source/topology epoch at transaction/log positions into immutable raw envelopes before checkpoint, retaining writer schema, transaction ordinals, before/after/tombstone, occurrence identity, payload digest, and manifests. Standardization parses/types under pinned precision/time/null rules, validates schema and identities, preserves rejects in governed quarantine, and publishes complete transaction/range generations. Warehouse load uses immutable files or source-faithful tables, stable batch/event receipts, one winner per entity by comparable source version, equal-version conflict, and tombstones to prevent resurrection. Join only versioned reference snapshots. Version code/SQL/config/runtime/libraries/schema/target settings and produce lineage from source positions/raw manifest through standard and curated manifests to serving export. Gate exact input/disposition sets, counts/keys/digests, transaction continuity, domains, relationships, totals, freshness, security, and consumer contracts. Stage every output and publish atomically/conditionally; retries preserve logical IDs and query ambiguous commits. Measure source/raw/curated lag, throughput, skew, spill, source/warehouse contention, storage/egress/compute, quarantine, cost, and SLOs. For backfill/disaster, restore raw/manifests/schemas/keys/artifacts/references/receipts, replay isolated generations idempotently, reconcile, then supersede curated and serving pointers with rollback retained.
