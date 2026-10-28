---
module_id: DARCH-013
program: Data Architecture Engineering
level: 1
module_number: 13
title: Physical Models and Their Separation
status: complete
last_verified: 2026-09-03
---

# Physical Models and Their Separation

## One-Page Review

### Governing question

How can a team design concrete storage, encoding, access, placement, replication, and lifecycle mechanisms from measured workloads while preserving the logical model's meaning and making every physical dependency, trade-off, and migration reversible or explicitly governed?

### Essential definitions

- A **physical data model** specifies how a logical model is realized in particular technologies, versions, configurations, locations, and operational environments.
- **Physical data independence** is the degree to which storage and access changes can occur without changing logical meaning or consumer contracts.
- A **physical mapping** links logical structures and constraints to tables, columns, files, topics, nodes, indexes, partitions, encodings, services, or other mechanisms with transformation and evidence.
- An **access path** is a structure or mechanism used to locate data efficiently, such as an index, clustering order, partition directory, materialized projection, or graph adjacency.
- **Partitioning** divides a logical collection into physical subsets according to a governed rule; **sharding** distributes subsets across independently managed placement or failure boundaries.
- **Replication** maintains copies for availability, locality, scale, recovery, or distribution, introducing consistency, lag, conflict, cost, and common-cause concerns.
- A **materialized projection** stores derived data for bounded uses and therefore needs source, derivation, refresh, reconciliation, and lifecycle rules.
- A **physical design hypothesis** predicts that a mechanism will meet specified workload and quality scenarios under declared conditions and evidence thresholds.

### Central model, mechanism, or theorem

Represent a physical realization as:

`P = (logical_baseline, structures, access_paths, placement, encoding, controls, operations, evidence, evolution)`

A physical design is acceptable only when every applicable logical commitment is preserved or an authorized exception is recorded, workload and quality scenarios are met with representative evidence and margin, enforcement responsibilities close, dependencies and failure modes are explicit, and migration plus rollback preserve identity and correctness. Faster benchmark results cannot compensate for lost semantics, unlawful processing, unrecoverable state, or an unapproved constraint violation.

### Critical invariants

- Every physical element maps to a logical structure, constraint, operational obligation, or justified technical responsibility.
- Every logical key, relationship, type, temporal rule, and invariant maps to enforcement, detection, reconciliation, or an explicit accepted gap.
- Workload claims define operations, data distributions, volume/rate, concurrency, locality, freshness, consistency, failure modes, horizon, and growth.
- Performance evidence binds exact technology, version, configuration, dataset, workload, environment, statistic, and date.
- Partition, shard, cluster, cache, replica, and materialized-view boundaries do not silently change semantic grain or authority.
- Copies retain source, derivation, freshness, consistency, conflict, recovery, deletion, and reconciliation semantics.
- Encryption, keys, access, retention, deletion, audit, residency, backup, recovery, and disposal apply to all physical representations and metadata.
- Capacity and performance include tails, skew, amplification, background work, failure/recovery, and safety margin—not only average nominal load.
- Every migration controls source and target versions, dual operation, validation, cutover, rollback, reconciliation, and retirement evidence.
- Physical changes trigger logical and consumer review only when their observable meaning or contract changes; optimization alone does not redefine the domain.

### Common failures

Common failures are copying DDL into a logical model; selecting a database from fashion; sizing from row count alone; adding every possible index; partitioning by a mutable or high-cardinality field; equating logical partitioning with failure isolation; assuming replicas are independent; using eventual consistency without consequence analysis; materializing derived facts without reconciliation; compressing encrypted or high-entropy values and expecting the same result; benchmarking uniform synthetic data; ignoring write, compaction, vacuum, repair, backup, restore, and migration amplification; enforcing a global key only within shards; deleting an authoritative row while copies persist; treating schema compatibility as semantic preservation; and cutting over without rollback evidence.

### Compact example

A retailer's logical Inventory Position has one authoritative assertion per item-location and time, with corrections and a global uniqueness rule. A team hashes by item for scale, creates regional replicas, and adds a materialized availability cache. Review finds uniqueness is enforced only per shard, one region receives most traffic, corrections lag behind cached decisions, replicas share a control plane and key service, and backups omit the event log needed for reconstruction. The physical model adds a globally coordinated identity rule, skew-aware placement, versioned cache derivation, dependency evidence, a consistent recovery set, reconciliation, and tested cutover/rollback. The logical meaning remains unchanged while the realization becomes defensible.

### Connections

[DARCH-011](011-conceptual-data-models.md) establishes domain meaning and [DARCH-012](012-logical-data-models.md) establishes technology-independent structures and constraints. This module maps those commitments to concrete realizations. [DARCH-014](../ROADMAP.md) deepens keys and relationships, while later modules cover schemas, storage patterns, distribution, performance, reliability, security, migration, and lifecycle governance.

## Governing Question

A physical model answers where and how information exists and behaves: database product and version, schemas and objects, file/table/message formats, columns and fields, codecs, pages and row groups, keys and indexes, partitioning and clustering, regions and tiers, replicas and caches, transaction boundaries, enforcement mechanisms, backups, retention jobs, observability, and migrations.

These decisions determine cost and operability, but they must not silently redefine meaning. A hash shard key cannot become business identity. A nullable column cannot change a prohibited absence into an optional fact. A cache cannot become authoritative because it responds faster. A physical join limit cannot erase a conceptual relationship.

Separation is therefore an active engineering practice, not three folders named conceptual, logical, and physical. Teams must trace commitments downward, evidence upward, and changes in both directions. The mapping shows whether an optimization is meaning-preserving or a contract change requiring new authority.

## Why This Matters

Physical choices are expensive to reverse once data volume, consumers, retention, and operations accumulate. A poor partition key creates hot spots and painful redistribution. A broad index portfolio amplifies writes and maintenance. A format choice can constrain schema evolution. A replica topology can concentrate supposedly independent failure. An undocumented derived store can outlive its source and become de facto truth.

Codd's [relational-model paper](https://doi.org/10.1145/362384.362685) emphasized independence between users and internal representation. Modern systems add distributed services, files, logs, object storage, graph stores, caches, and table formats, but the architectural aim remains valuable: optimize implementation without forcing every consumer to understand physical access paths.

PostgreSQL's current [partitioning documentation](https://www.postgresql.org/docs/current/ddl-partitioning.html) explicitly describes splitting one logical table into smaller physical pieces and connects benefits to query and maintenance patterns while warning that design depends on workload. Apache Parquet's [concepts](https://parquet.apache.org/docs/concepts/) distinguish files, row groups, column chunks, and pages with different physical roles. These sources illustrate concrete mechanisms; neither supplies universal thresholds or proves a design fit outside its exact system and workload.

Strong separation also improves governance. Security and privacy controls can be checked across every copy. Logical changes can identify affected realizations. Infrastructure changes can be reviewed for semantic impact. Migration evidence can show that identities, counts, invariants, histories, and decisions survived—not merely that bytes moved.

## Prerequisites and Retrieval

You should understand conceptual and logical models, keys, dependencies, constraints, events and state, schemas and compatibility, basic storage and database operations, distributed systems, reliability, security, privacy, observability, capacity, performance testing, and migration.

Retrieve logical and physical independence, mapping, table, file, topic, node, column, field, page, row group, index, partition, shard, cluster key, replica, cache, materialized view, codec, compaction, amplification, selectivity, skew, locality, consistency, durability, recovery point, recovery time, cutover, rollback, and reconciliation.

As a retrieval test, inspect `CREATE INDEX customer_email_idx ON customer(email)`. Ask which query and scenario require it, expected selectivity and distribution, read benefit, write/storage/maintenance cost, collation and equality semantics, exposure of sensitive values, build and rollback procedure, evidence environment, monitoring trigger, and retirement rule. An index name and passing DDL answer almost none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish conceptual, logical, physical, deployment, and runtime-observation models;
2. create bidirectional mappings from logical structures and constraints to physical mechanisms;
3. define representative workload, data-distribution, quality, failure, growth, and lifecycle scenarios;
4. select storage layout, types, encodings, indexes, clustering, partitioning, and sharding from evidence;
5. analyze copies, caches, materialized projections, replication, consistency, and reconciliation;
6. allocate security, privacy, retention, deletion, backup, recovery, and audit obligations to every representation;
7. build capacity and performance models including tails, skew, amplification, background work, failure, and margin;
8. conduct reproducible benchmarks and distinguish model, prototype, staging, and production evidence;
9. plan online change, backfill, coexistence, cutover, rollback, validation, and retirement;
10. govern physical decisions, drift, exceptions, monitoring, and re-optimization without corrupting logical meaning.

## Core Exposition

**Fix the logical baseline before optimizing.** Record exact logical model and schema versions, conceptual mappings, keys, grain, relationships, constraints, temporal semantics, provenance, access, retention, compatibility, and open assumptions. If these are unstable, physical experiments may still inform feasibility, but label them exploratory rather than baseline realizations.

**Define the physical decision context.** State affected products and consumers, current topology, target environment, decision authority, technology constraints, migration window, budget, skill and support model, supplier commitments, portability needs, risks, and evidence threshold. Separate externally imposed constraints from prior design choices and preferences.

**Build workload scenarios, not one TPS number.** Describe operation mix, request and batch shapes, read/write ratios, object sizes, predicates, joins or traversals, sort/aggregation, concurrency, arrival distribution, burst duration, locality, hot keys, tenant skew, event ordering, freshness, consistency, retention, and growth. Include correction, reprocessing, backfill, export, deletion, compaction, failover, restore, and degraded conditions.

Percentiles need population and window. Throughput needs accepted/completed/error definitions. Latency needs start and end events. Capacity needs logical bytes, encoded bytes, copies, indexes, metadata, temporary work, logs, backups, headroom, and retention. “One billion rows” says little without width, distribution, access, churn, and lifecycle.

**Create a physical inventory and mapping.** For each database, schema, table, column, file, topic, index, partition, shard, node/edge label, cache, materialized view, backup, archive, and metadata store, record stable identity, product/version, environment, region, owner, logical source, purpose, format, lifecycle, controls, dependencies, evidence, and status.

For each logical structure and constraint, map representation, transformation, type conversion, key, enforcement or detection, consistency boundary, loss, exception, source/target versions, and tests. For each physical element, map upward to logical need or justify technical responsibility such as deduplication state, transaction log, tombstone, checksum, index, or checkpoint.

**Select physical types carefully.** Product types embody ranges, precision, collation, time, null, encoding, and interoperability behavior. Confirm integer range, decimal precision and rounding, floating-point consequences, character normalization, collation, byte ordering, time-zone handling, timestamp resolution, interval semantics, identifier encoding, and maximum lengths.

Avoid narrowing merely to save bytes without growth and migration analysis. Avoid unbounded types merely for flexibility when they undermine validation, indexability, interoperability, or cost. Preserve logical value semantics in constraints, metadata, and tests; a vendor type rarely encodes unit, authority, purpose, or valid time.

**Choose row, column, document, graph, or log layout from operations.** Row-oriented layouts favor access to many fields of selected records and frequent point updates. Columnar layouts favor scans and aggregation over selected attributes and compress repeated patterns. Documents can colocate aggregates. Graph layouts store adjacency for relationship traversal. Logs optimize append and ordered consumption. Real systems combine these.

Layout does not define authority. A columnar copy remains derived if its source is authoritative; a log is not automatically truth if events are unvalidated or retractable; a graph projection does not own identity because it connects records. Record source, derivation, freshness, reconciliation, and recovery.

**Design encodings and compression.** Choose codecs using actual distributions, CPU, latency, memory, network, storage, splittability, random access, compatibility, and recovery. Dictionary, run-length, delta, bit packing, general compression, and domain-specific encodings behave differently with sorted, sparse, high-cardinality, encrypted, or already-compressed values.

Parquet organizes column chunks within row groups and pages as encoding/compression units. Row-group size, page size, statistics, dictionary choices, and sorting affect scan pruning, parallelism, memory, compression, and update/rewrite cost. These are physical hypotheses to benchmark with representative readers and distributions.

**Add indexes for evidenced access paths.** An index trades read/navigation benefit for storage, write amplification, cache pressure, build time, vacuum/compaction, backup, recovery, and operational complexity. Record query shape, operator semantics, predicate, selectivity distribution, covering fields, expected benefit, write cost, size, build method, monitoring, and retirement.

An index can also expose sensitive values or access patterns. Apply authorization, encryption, audit, retention, and deletion to index structures and search services. Dropping base data while derived indexes or embeddings remain is incomplete deletion.

Compare B-tree, hash, inverted, spatial, full-text, bitmap-like, block-range, vector, and product-specific indexes only within supported semantics. PostgreSQL's [BRIN documentation](https://www.postgresql.org/docs/current/brin.html), for example, ties block-range summaries to correlation with physical location. The mechanism is useful evidence about PostgreSQL, not a universal index rule.

**Partition for a declared purpose.** Common goals are pruning, lifecycle deletion, parallelism, locality, tenant isolation, write distribution, operational containment, or tiering. Choose a key and bounds from workload, distribution, change, retention, uniqueness, and growth. State null and late-arrival routing, overflow, split/merge, metadata scale, and rebalancing.

Range partitioning supports time and ordered locality but risks hot current ranges. Hash spreads keys but weakens range locality and can make resize expensive. List partitioning expresses governed categories but can explode with tenants or evolving values. Composite designs add power and management cost.

Physical partition boundaries are not automatically authorization or failure boundaries. A tenant partition in one database may share process, keys, backups, administrators, and capacity. Claim isolation only for properties actually evidenced.

**Treat sharding as distributed ownership of physical work.** Define routing, shard-key semantics, placement, balance, resharding, cross-shard queries and transactions, global keys, sequence generation, consistency, failure, recovery, observability, and operational authority. A globally unique logical rule enforced only within each shard remains unenforced globally.

Model skew and adversarial keys. Uniform random fixtures hide celebrity accounts, large tenants, current-time hot spots, regional concentration, sequential identifiers, and correlated bursts. Test rebalancing while reads/writes continue and record the consistency boundary.

**Cluster and sort with lifecycle in mind.** Physical order can improve locality, compression, merge behavior, and range pruning. Updates may destroy correlation or cause rewrites. Record sort keys, ordering semantics, maintenance process, degradation measure, reclustering cost, and effect on late/corrected data.

**Replicate for specific outcomes.** Identify whether copies serve read scale, geographic latency, availability, disaster recovery, analytics, migration, or audit. Define leader/authority, replication unit, sync/async behavior, ordering, lag distribution, conflict, read consistency, failover, fencing, reintegration, deletion, schema changes, and common causes.

Logical duplication does not prove independence. Replicas may share region, network, control plane, software defect, credentials, key service, operator, or corrupt source. Map dependency and fault domains. Test loss, partition, stale read, failover, failback, and repair under realistic load.

**Govern caches and materialized projections.** Record logical source, key, derivation/version, refresh or invalidation, maximum staleness, consistency, negative caching, authorization, tenancy, encryption, capacity, eviction, failure, fallback, reconciliation, deletion, and recovery. A cache miss, stale hit, and source error must have distinct behavior.

Materialized views, search indexes, aggregates, feature stores, and embeddings are copies with semantic and lifecycle obligations. Rebuildability is a claim requiring retained sources, code/rule versions, capacity, time, and tested procedures. Some derived artifacts become operationally critical even when logically reproducible.

**Allocate constraints explicitly.** Simple type, nullability, uniqueness, check, and referential constraints may be enforced by one database. Cross-store, temporal, aggregate, authorization, and workflow rules may require service transactions, coordinators, reservations, idempotency, reconciliation, monitoring, and manual decisions.

For every logical constraint record enforcement point, atomicity/consistency scope, timing, error behavior, retry/idempotency, bypass paths, bulk-load and maintenance behavior, evidence, monitoring, remediation, and exception authority. “Application enforced” is not enough.

**Account for amplification.** One logical write can produce transaction log, indexes, replicas, change events, materialized views, compaction, backups, audit, and cache invalidations. Let physical write amplification be total durable bytes or operations caused per logical write under stated conditions. Include reprocessing and repair.

Read amplification counts extra pages, objects, partitions, services, or bytes touched. Space amplification includes copies, indexes, metadata, slack, version history, tombstones, and temporary work. Operational amplification includes coordinated deploys, on-call load, and manual reconciliation. Optimize the whole path rather than one engine metric.

**Build capacity and performance models.** Estimate arrival and service distributions, concurrency, data growth, retention, encoded size, indexes, replicas, background work, network, memory working set, CPU, I/O, quotas, and failure reserve. Keep mean, percentile, worst-case bound, and confidence separate.

Use conservation checks: stored bytes should reconcile with event rate, average encoded size, retention, copies, and overhead; peak work should reconcile with concurrency and service demand. These estimates reveal order-of-magnitude errors but do not replace measurement.

**Benchmark reproducibly.** Record hypothesis, exact product/version, hardware/virtual resources, topology, configuration, dataset generator and seed, size/distribution/skew, warm/cold state, workload script, concurrency, duration, fault conditions, background tasks, metrics, statistical method, raw results, and environment interference.

Run representative mixes and isolate variables. Include warm-up, steady state, saturation, recovery, and long enough duration to observe compaction, cache churn, checkpointing, garbage collection, or vacuum. Report errors and dropped work; throughput from rejected requests is not capacity.

Production observation has different biases: traffic shaping, survivorship, caching, retries, sampling, and unknown confounders. Label model, microbenchmark, prototype, staging, shadow, canary, and production evidence. None transfers automatically across configuration or scale.

**Design security and privacy into every structure.** Map data classification, purpose, tenant, jurisdiction, access path, service identity, administrator, key, encryption context, tokenization, masking, audit, retention, deletion, legal hold, backup, and incident response. Metadata, statistics, logs, indexes, and filenames can reveal sensitive information.

Physical minimization includes columns, copies, regions, retention, precision, indexes, caches, logs, samples, test data, and observability payloads. A projection should contain only what its decision use needs. Verify deletion propagation and cryptographic/key lifecycle rather than assuming base-row deletion is sufficient.

**Design recovery as a consistent set.** Identify products and decisions to restore, maximum disruption, recovery point/time, dependency sequence, keys, schemas, logs, metadata, checkpoints, indexes, caches, derived views, external interfaces, capacity, and reopening authority. Backups are inputs; only restoration, replay, reconciliation, and consumer validation demonstrate recovery.

Test corrupted source, partial region, lost credentials, incompatible schema, lagged replica, and unavailable staff or supplier. Rebuilding a multi-terabyte index or materialized view may dominate recovery even if base restore is fast.

**Plan change and migration as part of the model.** Specify source and target physical mappings, schema/format versions, compatibility, transform, identity preservation, backfill, change capture, ordering, dual read/write authority, validation, cutover, freeze if any, rollback, reconciliation, monitoring, and retirement.

Dual writes can diverge; dual reads can hide inconsistent semantics. Define one authority at each moment and evidence transitions. Use counts, hashes, key coverage, invariant checks, sampled semantic comparisons, history/replay checks, and consumer outcomes. Aggregate count equality alone cannot prove record correspondence.

Apache Iceberg's [specification](https://iceberg.apache.org/spec/) describes metadata, snapshots, schema and partition evolution, and file tracking for that table format. SQLite's [database file format](https://www.sqlite.org/fileformat.html) exposes concrete pages and B-trees for a different design. Such detail demonstrates why “table” does not determine physical layout and why product/version/configuration belong in the physical model.

**Control drift and retirement.** Compare declared physical model with infrastructure, catalogs, schemas, statistics, query plans, deployments, and runtime observations. Classify drift as approved change awaiting documentation, discovered current state, emergency deviation, unmanaged change, or generated-view lag. Do not overwrite the baseline without a decision.

Retire unused indexes, partitions, replicas, caches, topics, exports, backups, keys, service accounts, and documentation through dependency and evidence checks. Preserve required history and legal holds, revoke access, verify consumer exit, delete all copies, and update mappings. Storage cost is only one reason to remove obsolete physical complexity.

## Definitions and Notation

Let a physical model be:

`P = (B, O, Y, A, G, D, C, Q, E)`

where `B` is the logical baseline, `O` physical objects, `Y` types/encodings/layout, `A` access paths, `G` partition/placement/replication topology, `D` derivations and copies, `C` controls and constraint enforcement, `Q` workload/quality/capacity scenarios, and `E` evidence, evolution, and operations.

For logical element `l` and physical object `p`, a mapping `map(l,p,k,v,t)` identifies mapping kind `k`, versions `v`, and applicability time `t`. Mapping closure requires every applicable logical commitment to map to representation or enforcement, and every physical object to map upward or carry justified technical purpose.

A rough storage model is:

`S_total = S_base + S_indexes + S_replicas + S_derived + S_logs + S_backups + S_metadata + S_working + margin`

Every term must declare horizon, compression/encoding, retention, copy count, failure state, and confidence. The arithmetic cannot prove that copies are independent, restorable, lawful, or semantically correct.

For benchmark result `r`, evidence identity is `e = (hypothesis, workload, data, product, version, configuration, topology, environment, method, time)`. A change in any material component limits transfer of `r`.

## Mechanisms, Invariants, or Proof Structure

Use ten gates to design and assure a physical model.

**1. Baseline gate.** Bind conceptual/logical versions, keys, grain, constraints, time, provenance, access, retention, compatibility, and assumptions.

**2. Scenario gate.** Define operations, distributions, skew, volume/rate, concurrency, locality, consistency, freshness, failures, growth, and lifecycle work.

**3. Mapping gate.** Trace every logical commitment to representation/enforcement and every physical object to logical or technical justification.

**4. Layout and access gate.** Select types, encoding, row/column/document/graph/log layout, indexes, clustering, and derived projections from evidence.

**5. Distribution gate.** Design partitions, shards, placement, replication, routing, global constraints, fault domains, balance, and reconfiguration.

**6. Control gate.** Allocate integrity, security, privacy, retention, deletion, audit, consistency, backup, and recovery across every copy and bypass.

**7. Capacity and evidence gate.** Model tails and amplification, benchmark representative conditions, retain raw evidence, and preserve margin and uncertainty.

**8. Migration gate.** Govern source/target versions, backfill, change capture, coexistence, authority, validation, cutover, rollback, and reconciliation.

**9. Operations gate.** Define observability, maintenance, compaction, repair, failover, recovery, on-call ownership, cost, and supplier dependencies.

**10. Lifecycle gate.** Monitor drift and triggers, re-evaluate hypotheses, propagate contract changes, retire obsolete structures, and preserve evidence.

The executable example checks four physical-design failures: a stale logical mapping, a global constraint enforced only locally, an access path without workload evidence, and a migration with no rollback.

<!-- bijux-verify: {"id":"physical-model-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"items=4\nvalid=0\nfindings=customer-store:stale-logical-mapping,events-shard:constraint-not-enforced,orders-index:missing-workload-evidence,profile-migration:missing-rollback\nready=false\n","stderr":""}} -->
```python
items = (
    {"id": "customer-store", "logical_version": 7, "mapped_version": 6, "global_rule": False, "global_enforced": True, "evidence": "trace", "migration": False, "rollback": True},
    {"id": "events-shard", "logical_version": 4, "mapped_version": 4, "global_rule": True, "global_enforced": False, "evidence": "load-test", "migration": False, "rollback": True},
    {"id": "orders-index", "logical_version": 5, "mapped_version": 5, "global_rule": False, "global_enforced": True, "evidence": "", "migration": False, "rollback": True},
    {"id": "profile-migration", "logical_version": 3, "mapped_version": 3, "global_rule": False, "global_enforced": True, "evidence": "rehearsal", "migration": True, "rollback": False},
)

findings = []
valid = 0
for item in items:
    local = []
    if item["logical_version"] != item["mapped_version"]:
        local.append("stale-logical-mapping")
    if item["global_rule"] and not item["global_enforced"]:
        local.append("constraint-not-enforced")
    if not item["evidence"]:
        local.append("missing-workload-evidence")
    if item["migration"] and not item["rollback"]:
        local.append("missing-rollback")
    if local:
        findings.extend(f"{item['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"items={len(items)}")
print(f"valid={valid}")
print(f"findings={','.join(sorted(findings))}")
print(f"ready={str(not findings).lower()}")
```

The checker validates four registry predicates. It does not prove semantic preservation, global uniqueness, workload representativeness, performance, isolation, recovery, security, privacy, migration safety, or production fitness. Those require exact configurations, representative tests, fault exercises, source review, and accountable decisions.

## Alternatives and Trade-Offs

**General-purpose store versus specialized projections.** One store reduces movement and governance surfaces but may serve some workloads poorly. Specialized stores improve bounded access but create copies, mappings, skills, cost, and reconciliation. Add a projection only with a decision use and lifecycle owner.

**Row versus column layout.** Row layout favors point access and updates; column layout favors scans, compression, and aggregation. Mixed workloads may need separate authority and analytical projections rather than one compromised layout.

**More indexes versus fewer indexes.** Indexes can reduce read cost while increasing writes, space, maintenance, recovery, and exposure. Keep evidence-driven access paths and retire those whose total benefit no longer exceeds cost.

**Range versus hash partitioning.** Range supports ordered pruning and lifecycle operations but can hot-spot. Hash spreads load but weakens locality and complicates resize. Distribution and future change decide.

**Synchronous versus asynchronous replication.** Synchronous coordination can strengthen durability/consistency at latency and availability cost. Asynchronous replication improves decoupling but exposes lag and loss windows. Select by consequence, topology, and recovery evidence.

**Precomputed versus on-demand derivation.** Materialization improves predictable reads but creates freshness and reconciliation obligations. On-demand computation preserves immediacy to source but consumes latency and capacity. Hybrid designs need clear authority.

**Online migration versus controlled outage.** Online coexistence reduces downtime but adds dual-path complexity and divergence risk. A bounded outage can simplify correctness but may violate service needs. Choose from consequence and rehearsed evidence.

## Failure Modes and Misconceptions

1. **Physical design is DDL.** It also covers formats, access, topology, copies, controls, operations, evidence, and evolution.
2. **Vendor-neutral means logical.** A diagram can embed physical partition, index, encoding, or deployment assumptions without naming a vendor.
3. **Benchmark winner is architecture winner.** Results are conditional and do not aggregate semantics, risk, operations, migration, or cost automatically.
4. **More partitions improve scale.** Poor keys and excess metadata can worsen planning, balance, and operations.
5. **Replica means independent.** Shared causes and correlated administration can defeat redundancy.
6. **Cache is disposable.** Rebuild time, source retention, keys, capacity, and operational dependency may make it critical.
7. **Global rule plus local index is enough.** Enforcement scope must match rule scope.
8. **Encrypted means protected everywhere.** Keys, metadata, indexes, logs, administrators, and use paths remain part of protection.
9. **Backup means recovery.** Restore, replay, reconciliation, capacity, dependency order, and consumer validation must be exercised.
10. **Dual write means safe migration.** Partial failure, ordering, retries, and authority can diverge targets.
11. **Equal counts prove correctness.** Identity, fields, histories, constraints, and consumer outcomes can still differ.
12. **Optimization never changes behavior.** Ordering, consistency, freshness, precision, errors, and failure modes can leak into contracts.

## Worked Examples

### Example 1

A B-tree index speeds a selective account lookup but doubles write latency during peak ingestion and contains sensitive email. The team uses a protected normalized lookup key, measures write amplification, builds concurrently under a rollback plan, monitors selectivity, and schedules retirement if use falls.

### Example 2

Monthly partitions support seven-year retention deletion. Late corrections can target closed months, and a global invoice key cannot be enforced by per-partition uniqueness alone. The design adds explicit late routing, global identity coordination, correction tests, and detach/archive evidence.

### Example 3

Hash sharding by tenant balances ten large tenants. Growth adds 100,000 tiny tenants and metadata/connection overhead dominates. The physical hypothesis includes future distribution and compares virtual buckets, pooled placement, split/merge, and rebalancing rather than one shard per tenant.

### Example 4

A Parquet benchmark uses uniform integers and reports excellent compression. Production has encrypted identifiers, high-cardinality strings, skewed nested arrays, and small files. Representative fixtures reverse the expected storage and scan result, so row-group, dictionary, sorting, and compaction choices change.

### Example 5

Two regional replicas meet nominal read latency. Both depend on one key service and deployment pipeline. A key-policy error makes both unreadable. The recovery set adds independently recoverable key material, guarded rollout, break-glass authority, and tested restoration before claiming regional resilience.

### Example 6

A materialized customer summary refreshes hourly while fraud decisions require corrections within five minutes. The view is retained for reporting but removed from the fraud path; a correction-aware projection with freshness fencing and fallback serves that decision.

### Example 7

A delete job removes base rows but search indexes, CDC topics, cache entries, training extracts, backups, and query logs persist. The physical inventory and lineage define propagation, retention, legal-hold precedence, verification, and residual limitations across every representation.

### Example 8

A global unique username constraint is implemented by unique indexes on 32 shards. Concurrent requests on different shards create duplicates. The team changes routing to a deterministic ownership shard or uses a reservation authority, with idempotency, failure, reconciliation, and migration tests.

### Example 9

An online migration dual-writes old and new stores. Retry ordering produces newer state in the old store and older state in the new. Versioned events, one authoritative sequence, idempotent application, comparison, repair, cutover criteria, and rehearsed rollback replace timestamp-based last-write wins.

### Example 10

A logical monetary amount maps from decimal to binary floating point for a high-speed cache. Totals differ by rounding and consumers treat the cache as authoritative. The mapping is rejected; exact scaled representation and currency/rounding rules are preserved, then performance is remeasured.

## Cross-Program Connections

- **Database engineering:** files, pages, indexes, query plans, transactions, partitioning, replication, backup, and tuning realize logical models.
- **Data engineering:** object storage, Parquet, table formats, streaming logs, orchestration, compaction, lineage, and backfills are physical architecture surfaces.
- **Distributed systems:** partition, replication, ordering, consensus, failure detectors, clocks, and recovery determine consistency and availability claims.
- **API and service engineering:** databases and caches sit behind contracts whose latency, error, consistency, and compatibility behavior can expose physical decisions.
- **Platform engineering:** managed stores, tenancy, quotas, regions, encryption, observability, paved roads, and lifecycle automation govern realizations at scale.
- **Security and privacy:** placement, copies, keys, indexes, logs, backups, deletion, administrators, and suppliers define actual exposure.
- **Performance engineering:** workload design, measurement, queueing, tails, skew, capacity, amplification, and controlled experiments justify optimization.
- **Systems engineering:** allocation, physical architecture, interfaces, configuration, integration, verification, risk, and lifecycle governance provide the wider assurance frame.

## References

1. Codd, E. F., “A Relational Model of Data for Large Shared Data Banks,” *Communications of the ACM*, 13(6), 1970. <https://doi.org/10.1145/362384.362685>
2. ISO/IEC, *9075-1:2023 Information technology—Database languages SQL—Part 1: Framework*, 2023. <https://www.iso.org/standard/76583.html>
3. PostgreSQL Global Development Group, *PostgreSQL 18 Documentation: Table Partitioning*, current web edition. <https://www.postgresql.org/docs/current/ddl-partitioning.html>
4. PostgreSQL Global Development Group, *PostgreSQL 18 Documentation: BRIN Indexes*, current web edition. <https://www.postgresql.org/docs/current/brin.html>
5. Apache Software Foundation, *Apache Parquet Concepts and File Format*, current web edition. <https://parquet.apache.org/docs/concepts/>
6. Apache Software Foundation, *Apache Iceberg Specification*, current web edition. <https://iceberg.apache.org/spec/>
7. SQLite, *Database File Format*, current web edition. <https://www.sqlite.org/fileformat.html>
8. National Institute of Standards and Technology, *SP 800-34 Rev. 1: Contingency Planning Guide for Federal Information Systems*, 2010. <https://csrc.nist.gov/pubs/sp/800/34/r1/final>

## Exercises

### Exercise 1

Create a physical decision record for an order lookup index. Include logical mapping, query/workload, distribution, selectivity, operator semantics, product/version/configuration, expected benefit, write/space/recovery cost, sensitive exposure, build, rollback, monitoring, and retirement.

### Exercise 2

Estimate storage for 50 million events per day, 600 encoded bytes each, 30-day hot retention, two hot replicas, 25% index overhead, seven days of temporary compaction headroom equal to one base copy, and 20% safety margin. State counting assumptions and limitations.

### Exercise 3

Design a shard strategy for a marketplace with a few huge sellers, millions of small sellers, cross-seller buyer views, globally unique order identifiers, regional residency, seasonal bursts, and seller migration. Include alternatives, constraints, skew tests, routing, rebalancing, and global-rule enforcement.

### Exercise 4

Review a derived search index claimed to be disposable. Specify source/derivation versions, rebuild inputs, throughput and duration, keys, permissions, freshness, deletion, failure behavior, fallback, recovery priority, reconciliation, and evidence needed to support or reject the claim.

### Exercise 5

Plan an online migration from a relational authority store to a distributed document store. Cover semantic mapping, constraints, schema versions, backfill, change capture, ordering, dual operation, identity, validation, cutover, rollback, recovery, security/privacy, consumer evidence, and retirement.

## Answers to the Exercises

### Answer 1

Record the logical Order key and searchable fields, exact lookup and authorization query, result ordering, latency/SLO population, concurrency, read/write mix, tenant and key distribution, selectivity percentiles, growth, and failure modes. Bind evidence to database/version, collation/operator class, table/index definition, hardware, data fixture/seed, cache state, configuration, background work, duration, and raw results.

Estimate read benefit plus index bytes, write amplification, build and maintenance I/O, cache pressure, backup/restore, replica lag, and sensitive key exposure. Define protected access and audit, concurrent or staged build, cancellation and drop rollback, plan verification, correctness tests, production canary, monitoring for usage/selectivity/latency/write cost/bloat, and retirement when benefit falls below governed cost. Approval is conditional on representative evidence and logical equality semantics.

### Answer 2

One day of base encoded data is `50,000,000 * 600 = 30,000,000,000` bytes, or 30 GB decimal. Thirty days is 900 GB per copy. Two hot replicas total 1,800 GB. Index overhead is assumed to apply to both replicas: `0.25 * 1,800 = 450` GB. Seven days of one base-copy compaction headroom is `7 * 30 = 210` GB. Before margin the estimate is `1,800 + 450 + 210 = 2,460` GB. With 20% margin: `2,460 * 1.2 = 2,952` GB, about 2.952 TB decimal.

This assumes “two replicas” means two total copies, constant post-encoding size/rate, index overhead relative to replicated base, and compaction headroom not replicated. It excludes metadata, transaction logs, manifests, backups, deletes/tombstones, late data, growth, temporary indexes, network, compression drift, and failure/rebuild overlap. Binary units, peaks, retention boundaries, and observed distributions must be modeled before procurement.

### Answer 3

Compare seller-key, buyer-key, order-hash, region-first composite, and directory/virtual-bucket designs. Residency is a placement constraint; global order identity, buyer aggregation, seller operations, migrations, and seasonal hot sellers are distinct concerns. One shard per seller fails metadata balance; naive seller hashing leaves huge sellers hot; buyer sharding makes seller fulfillment expensive.

A candidate uses region-constrained virtual buckets, deterministic order-ID ownership, a routing directory, and split placement for large sellers, with derived buyer projections. Define globally unique ID issuance or reservation, cross-shard query semantics, transaction boundaries, consistency, authorization, reconciliation, and failure behavior. Test empirical seller-size and traffic distributions, top sellers, coordinated promotions, buyer fan-out, directory loss, region outage, split/merge, live migration, late events, and rollback. The selected design remains conditional on residency authority and workload evidence.

### Answer 4

Identify the search index, consumers and critical decisions; authoritative source and retained history; extraction, transformation, analyzer/tokenizer, embedding if any, schema, code, configuration, and model versions; checkpoints and ordering; keys; access and tenant filters; maximum staleness; update/delete propagation; and reconciliation rules. Calculate source scan, transform, index throughput, data volume, parallelism, quotas, cost, and rebuild duration under failure load.

Test whether required source versions, encryption keys, permissions, staff, capacity, and supplier are available during recovery. Define behavior while absent, fallback correctness/capacity, partial-build exposure, validation, cutover, and recovery priority. Exercise deletion and rebuild from a controlled snapshot plus changes, compare key/field/invariant coverage and consumer tasks, and measure time. Reject “disposable” if source or derivation is missing, rebuild exceeds consequence tolerance, or operations cannot safely function without it.

### Answer 5

Bind logical baseline and map relations, keys, relationships, null/missing, decimals, order, events, history, constraints, provenance, access, retention, and deletion to document structures. Identify constraints the target cannot enforce transactionally and design reservation, service enforcement, reconciliation, or an authorized bounded gap. Version writer/reader schemas and migrations; preserve identifiers and source assertions.

Take a controlled source snapshot, backfill idempotently, capture ordered changes from a known position, and reconcile before coexistence. Define one authority for each operation and moment; avoid independent dual writes or use a durable intent/outbox with retry and deduplication. Validate counts by partition plus keys, hashes, fields, relationships, histories, constraints, sampled semantics, deletion/retention, latency/errors, recovery, and consumer tasks. Canary reads/writes, monitor divergence, and rehearse rollback that preserves writes made after cutover. Verify encryption, keys, residency, least privilege, audit, backups, restores, and incident paths. Retire the old store only after rollback horizon, consumers, archives, legal holds, evidence, access, contracts, and responsibility transfer satisfy approved exit criteria.
