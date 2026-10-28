---
module_id: DARCH-050
program: Data Architecture Engineering
level: 1
module_number: 50
title: Mapping Data Workloads to Platforms and Serving Systems
status: complete
last_verified: 2026-09-03
---

# Mapping Data Workloads to Platforms and Serving Systems

## One-Page Review

### Governing question

How should architects map each data workload to authoritative, processing, serving, search, cache, history, and archive roles that satisfy correctness, performance, resilience, protection, operability, cost, and lifecycle requirements without mistaking a product feature matrix or fashionable database category for architectural fit?

### Essential definitions

- A **data workload** is a bounded set of reads, writes, transformations, decisions, actors, data, service qualities, failure consequences, and lifecycle obligations.
- An **access pattern** describes operations such as point lookup, range scan, transaction, append, search, traversal, aggregation, similarity lookup, stream consumption, or object delivery at declared scale.
- A **data-store model** organizes and operates data through relational, key-value, document, column-family, graph, time-series, search-index, log, object, analytical, vector, or another set of semantics.
- A **platform capability** is a reusable managed function for storage, compute, query, policy, metadata, delivery, observability, recovery, or lifecycle.
- A **serving system** exposes data or derived results to a named consumer under an interface, freshness, consistency, latency, availability, and protection contract.
- A **system of record** is the accountable authority for a declared fact and mutation, not merely the store holding the most convenient copy.
- A **projection** is derived state optimized for a consumer or access pattern and linked to authority, positions, correction, reconciliation, and rebuild behavior.
- A **cache** is replaceable state used to reduce latency or source load under invalidation, staleness, miss, and failure rules.
- A **hard gate** is a non-negotiable correctness, protection, jurisdiction, recovery, or compatibility requirement that excludes a candidate.
- A **fitness score** is a weighted comparison among candidates that already pass hard gates; it is decision support, not a proof of suitability.
- **polyglot persistence** uses multiple store models for distinct roles whose authority, propagation, failure, and lifecycle relationships are explicit.
- A **technology decision record** binds the workload contract, candidates, evidence, choice, assumptions, exceptions, owners, review triggers, and exit plan.

### Central model, mechanism, or theorem

Represent a workload-to-platform decision as:

`M = (outcome, authority, data, operations, correctness, scale, service, topology, protection, operations, economics, evidence, lifecycle)`

First characterize the workload independently of products. Exclude any candidate that fails hard requirements. Compare surviving store models and platform capabilities using representative evidence, uncertainty, and lifecycle cost. Assign each selected system one or more explicit roles—authority, log, work queue, projection, cache, search, analytical history, feature serving, or archive—and define propagation and reconciliation between them. The best component in isolation can still create an unfit system when ownership, failure coupling, data movement, or exit is ignored.

### Critical invariants

- Every choice traces to named decisions, users, operations, data, deadlines, consequences, and fallback.
- Fact authority and mutation ownership remain explicit when copies, indexes, caches, and analytical projections multiply.
- Correctness, consistency, isolation, ordering, durability, jurisdiction, protection, and recovery hard gates precede weighted scoring.
- Latency, throughput, concurrency, scale, skew, and growth use percentiles and representative distributions, not only averages or vendor maxima.
- Data movement defines identity, positions, delivery, schema, corrections, deletions, replay, reconciliation, and source impact.
- A cache, search index, lake, warehouse, feature store, or vector index does not silently become the authoritative write path.
- Capacity tests cover normal load, peaks, replay, failover, maintenance, recovery, noisy neighbors, and degraded modes.
- Protection follows data into replicas, logs, indexes, caches, snapshots, backups, exports, telemetry, and provider control planes.
- Operational ownership, skills, observability, support, change, migration, cost, and exit are evaluated with functional fit.
- Retirement removes writers, readers, copies, replication, credentials, backups, alerts, contracts, and retained obligations under verified closure.

### Common failures

Common failures are choosing a database before defining the workload; treating all reads or writes as alike; using average latency; copying vendor benchmark numbers; using a search index as a source of record; using a cache as durable state; assuming SQL syntax implies relational transactions; expecting a log to answer arbitrary current-state queries; forcing transactional and analytical workloads into one resource pool; adopting multiple stores without reconciliation; duplicating the same authority in two regions or products; ignoring hot keys and tenant skew; promising strong consistency without naming operations and scope; confusing replication with backup; setting RPO and RTO without exercises; benchmarking empty datasets; omitting data movement and egress cost; choosing managed services without an exit path; relying on undocumented provider limits; and retiring a store while backfills, backups, credentials, or consumers remain.

### Compact example

An order-commit workload needs authoritative writes, multi-record transactions, uniqueness, read-your-writes, and an audit trail. A relational system passes those hard gates and becomes the system of record. Full-text order discovery needs relevance ranking and flexible search, so a search index becomes a derived projection. Even if the search candidate scores well on latency and query fit, it fails the authority gates. Events propagate by stable order ID and source version; consumers tolerate declared lag; reconciliation compares keys and versions; loss of the index degrades search but does not lose orders.

### Connections

[DARCH-026](026-data-products-and-service-expectations.md), [DARCH-040](040-choosing-an-integration-style-from-semantics-and-latency.md), [DARCH-041](041-enterprise-data-warehouse-architecture.md), [DARCH-042](042-data-lake-architecture.md), [DARCH-043](043-lakehouse-architecture.md), [DARCH-046](046-operational-data-stores.md), [DARCH-047](047-streaming-analytics-architecture.md), [DARCH-048](048-feature-and-training-data-architecture.md), and [DARCH-049](049-self-service-analytics-boundaries.md) establish candidate roles and contracts. Data Engineering owns implementation mechanics. This module closes Level I and prepares [DARCH-051](../ROADMAP.md) on master data and golden records.

## Governing Question

Technology selection is often framed as comparing products. That begins too late. A feature matrix cannot tell whether a workload needs transactional authority, approximate search, immutable history, current state, replay, graph traversal, low-latency lookup, or economical scans.

The governing question is which composition of store models and platform capabilities makes each workload fit under real data, load, failure, protection, team, and lifecycle conditions—and which evidence would falsify that choice before or after adoption.

## Why This Matters

Microsoft's [Prepare to Choose a Data Store](https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-stores-getting-started) describes functional, nonfunctional, cost, management, security, governance, and team considerations. Its [data-store model guide](https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/understand-data-store-models) maps access patterns to models, and its [analytical serving guidance](https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/analytical-data-stores) compares serving-layer criteria. These provider guides support evaluation but do not replace workload-specific proof.

AWS [Data Management guidance](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/data-management.html) recommends purpose-built stores based on data and access characteristics. Google Cloud's [Plan Resource Allocation](https://docs.cloud.google.com/architecture/framework/performance-optimization/plan-resource-allocation) emphasizes granular performance and growth requirements. Provider guidance is evidence about mechanisms and selection questions, not a neutral guarantee of fit or future price.

PostgreSQL's [MVCC introduction](https://www.postgresql.org/docs/current/mvcc-intro.html) describes transactional concurrency semantics. Apache Kafka's [Design documentation](https://kafka.apache.org/40/design/design/) describes log, compaction, and delivery mechanisms. Google's [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) explains overload, degradation, and retry amplification. NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy systems across their lifecycle. Architecture must qualify product mechanisms inside a complete system.

## Prerequisites and Retrieval

You should understand data models, transactions, consistency, isolation, replication, partitioning, logs, caches, indexes, object storage, analytical systems, APIs, data products, quality, security, privacy, service levels, recovery, and cost.

Retrieve outcome, authority, fact, mutation, access pattern, workload, store model, platform capability, serving system, projection, cache, source position, consistency, isolation, latency percentile, throughput, concurrency, skew, working set, retention, RPO, RTO, residency, reconciliation, total cost, hard gate, fitness score, decision record, and exit.

As a retrieval test, inspect “we need a fast customer database.” Ask which customer facts, authority, reads and writes, keys, transactions, queries, sizes, growth, concurrency, latency percentiles, consistency, regions, availability, recovery, protection, integrations, costs, owners, and retirement obligations apply. “Fast” and “database” do not form a workload contract.

## Learning Objectives

After completing this module, you should be able to:

1. characterize data workloads independently of products and vendor categories;
2. distinguish authority, log, queue, projection, cache, search, analytical history, feature serving, and archive roles;
3. translate operations, data shape, scale, correctness, and service qualities into hard gates and evaluation criteria;
4. map relational, key-value, document, column-family, graph, time-series, search, log, object, analytical, vector, and cache models to suitable patterns;
5. design propagation, positions, corrections, deletes, reconciliation, replay, and degraded behavior across multiple systems;
6. evaluate capacity, skew, failover, recovery, maintenance, protection, jurisdiction, operability, and cost with representative evidence;
7. avoid false authority, accidental dual writes, fragile polyglot persistence, and benchmark theater;
8. record assumptions, uncertainty, trade-offs, exceptions, owners, review triggers, migration, and exit;
9. monitor continued fitness through workload, product, provider, team, risk, and economic changes; and
10. retire platforms and serving systems with dependency and retained-data closure.

## Core Exposition

**Start with the outcome.** Name the decision, transaction, observation, actor, frequency, useful deadline, correctness consequence, availability consequence, and fallback.

“Store customer data” can mean authorize a payment, render a profile, find similar records, audit history, train a model, or aggregate revenue. Each produces different requirements.

**Define the fact authority.** For every mutable fact, assign the accountable system and operation that can create, correct, supersede, or delete it.

Authority is a governance and behavior contract. It is not automatically the oldest, largest, fastest, or most centralized store.

**Decompose mixed workloads.** Separate commands, point reads, relational queries, search, scans, aggregates, streams, traversals, similarity lookup, files, reporting, training, and archive.

One user journey may require several roles. Do not force incompatible operations into one store before considering governed projections.

**Describe operation semantics.** Record key shape, predicates, joins, ranges, ordering, aggregation, mutation type, transaction boundary, contention, idempotency, batch size, and result size.

“Read-heavy” hides whether reads are point lookups, prefix searches, graph paths, or petabyte scans.

**Model data shape.** Specify structure, relationships, cardinality, sparsity, size, object granularity, schema evolution, compression, and validation.

Store models make different operations natural or expensive. A flexible schema does not remove semantic contracts.

**Quantify scale as a distribution.** Measure present and forecast records, bytes, reads and writes per second, concurrency, partitions, tenants, regions, working set, and growth.

Include peaks, seasonality, launches, replays, failover, maintenance, and batch overlap. Averages hide the conditions that break systems.

**Identify skew and hot keys.** A few tenants, entities, time buckets, partitions, or terms may dominate traffic and state.

Uniform synthetic keys create comforting benchmarks. Test real or representative frequency distributions and adversarial concentration.

**Set latency at observable boundaries.** Define source mutation to durable acknowledgement, visible read, index availability, analytical release, API response, and decision use.

Use percentiles, time windows, payload sizes, concurrency, and error treatment. Median latency does not protect tail-sensitive decisions.

**Set throughput with correctness.** A system that reports high writes while dropping durability, weakening validation, or deferring unusable work has not met the workload.

Measure useful completed operations under the required guarantees, including retries and downstream effects.

**Specify consistency per operation.** Name read-your-writes, monotonic reads, bounded staleness, causal order, snapshot, serializable, or another observable requirement and its scope.

“Strong” is incomplete without object, region, failure, client session, and time boundaries.

**Specify isolation and invariants.** Define uniqueness, referential rules, balance, inventory, authorization, and multi-record constraints that concurrent mutations must preserve.

Application-side checks over stale reads can violate invariants. Test actual contention and failure paths.

**Define ordering scope.** Logs and partitions may order within a key or partition, not globally. Databases may serialize transactions without preserving external event time.

Use source versions, epochs, and stable identities where consumers require gap or stale-update detection.

**Separate availability from correctness.** A reachable replica returning stale or partial data may be unavailable for the decision. A temporarily rejected write can preserve system safety.

Define acceptable degraded modes, partial results, stale bounds, fail-open or fail-closed behavior, and user communication.

**Define durability and loss tolerance.** State which acknowledged facts may be lost, under which failure domains, and how the system detects and repairs loss.

Replication improves availability or durability under some failures. It does not replace independent backups, immutable history, or recovery evidence.

**Set recovery objectives from outcomes.** RPO bounds acceptable data loss; RTO bounds restoration time. Add consistency, dependency order, backlog, reconciliation, and decision recovery.

Exercise restore at realistic size and topology. A backup completion metric does not prove recoverability.

**Map temporal needs.** Distinguish current state, immutable events, effective history, transaction history, snapshots, revisions, retention, legal holds, and deletion.

An online current-state store cannot answer past knowledge unless history exists elsewhere with valid semantics.

**Map geographical needs.** Identify users, writers, sources, residency, sovereignty, latency, failure domains, transfer limits, and conflict policy.

Multi-region replication creates consistency, cost, recovery, and jurisdiction trade-offs. It is not a checkbox for global readiness.

**Make protection a hard gate.** Require identity integration, authorization granularity, encryption, key ownership, network boundaries, audit, tenant isolation, deletion, retention, and provider assurance appropriate to the data.

A technically fast store is ineligible if it cannot satisfy jurisdiction or protection obligations.

**Evaluate relational stores.** They fit structured relationships, constraints, rich queries, and transactions when scale and topology remain suitable.

Do not assume every SQL interface supplies equivalent constraints, isolation, transactions, extensions, or operational maturity.

**Evaluate key-value stores.** They fit simple key-based operations, bounded values, predictable partitioning, and low latency.

Secondary queries, cross-key transactions, large values, and hot keys can undermine the fit or require projections.

**Evaluate document stores.** They fit aggregate-oriented records and evolving nested shapes when most operations align to document boundaries.

Cross-document invariants, joins, duplication, update contention, and unbounded documents need explicit treatment.

**Evaluate column-family stores.** They fit high-scale sparse data and query-driven denormalization with known partition and clustering keys.

Ad hoc access, hot partitions, tombstones, and operational complexity can be costly.

**Evaluate graph stores.** They fit repeated multi-hop relationship traversal, path, neighborhood, and pattern questions.

Graph labeling does not justify a graph database when bounded relational joins or precomputed paths suffice.

**Evaluate time-series stores.** They fit time-keyed observations, retention tiers, downsampling, and time-window aggregation.

High-cardinality labels, corrections, irregular relationships, and authoritative transactional mutations may need other roles.

**Evaluate search indexes.** They fit full-text retrieval, relevance, facets, flexible filtering, and approximate discovery.

Indexes are derived and can lag, omit, duplicate, or reorder facts. Preserve authority and reconciliation elsewhere.

**Evaluate logs.** Durable ordered logs fit event distribution, replay, decoupling, and change histories within declared partitions and retention.

A log is not automatically a work queue, current-state query system, transaction authority, archive, or complete event history.

**Evaluate object stores.** They fit large immutable objects, raw and curated files, snapshots, backups, media, and economical tiered retention.

Listing, small updates, transaction semantics, metadata queries, and low-latency random mutation differ by system and layer.

**Evaluate analytical stores.** Warehouses, lakehouses, cubes, and analytical engines fit scans, joins, aggregations, historical releases, and concurrent analysis under different contracts.

Do not direct heavy analytical work at transactional authority merely because it supports SQL.

**Evaluate caches.** Caches reduce latency or source load when misses, staleness, invalidation, eviction, stampede, warm-up, and bypass are safe.

If losing the cache loses the only copy, it is not a cache. If the source cannot carry misses, the cache is a capacity dependency requiring stronger engineering.

**Evaluate vector indexes.** They fit similarity retrieval over versioned embeddings under model, distance, filtering, recall, freshness, and evaluation contracts.

Approximate similarity is not fact authority. Preserve source objects, embedding lineage, protection, and deletion propagation.

**Assign roles before products.** Record which component owns authoritative writes, change history, integration, current projection, search, cache, analytics, feature lookup, and archive.

One component may serve several compatible roles, but each role needs explicit guarantees and owners.

**Apply hard gates first.** Exclude candidates that cannot meet correctness, jurisdiction, protection, recovery, essential interfaces, or organizational constraints.

Weighted scores must not compensate for a failed non-negotiable requirement. A fast unsafe candidate remains ineligible.

**Weight remaining criteria transparently.** Score functional fit, latency, scale, availability, operability, ecosystem, cost, portability, and team readiness with evidence ranges.

Document weights, uncertainty, sensitivity, and dissent. Small score differences rarely justify false precision.

**Compare configurations, not product names.** Consistency, durability, limits, topology, indexing, backup, and cost depend on configured modes and service tiers.

Evaluate the exact region, version, size, replication, client, and operational model intended.

**Prototype the risky questions.** Test unknown query plans, transaction contention, partition skew, failover, restore, schema change, deletion, indexing lag, and integration behavior.

A broad proof of concept that demonstrates only happy-path inserts and reads resolves little risk.

**Benchmark representative workloads.** Use realistic data volume, shape, skew, compression, indexes, concurrency, payload, network, security, background work, and steady-state duration.

Measure latency distributions, useful throughput, errors, saturation, recovery, cost, and correctness. Preserve configurations and raw results.

**Test until failure and beyond.** Find saturation, queue growth, timeout, retry, eviction, compaction, rebalance, and recovery behavior.

Safe systems reject or degrade predictably instead of collapsing useful throughput as load rises.

**Design propagation contracts.** For every derived store define source identity, snapshots or positions, delivery, order, schema, corrections, deletes, checkpoints, freshness, backfill, and ownership.

Dual writes from an application to unrelated stores create ambiguous outcomes unless coordinated or reconciled.

**Prefer one authoritative mutation.** Commit the fact once at its authority, then project through a durable outbox, change stream, log, or governed pipeline.

When distributed coordination is unavoidable, specify failure semantics, idempotency, outcome discovery, compensation, and repair.

**Reconcile by identity and version.** Compare source and target keys, versions, counts, values or digests, deletes, gaps, and positions at compatible boundaries.

Matching row counts can hide wrong identities and values. Reconciliation is a product operation with safe repair.

**Prevent feedback authority.** Derived analytics, search, cache, or model output must not silently flow back as authoritative fact.

Commands informed by derivations pass through accountable domain validation and create new facts with provenance.

**Isolate workload classes.** Separate transactional, analytical, search, streaming, backfill, maintenance, recovery, and exploratory demand using pools, priorities, quotas, and source budgets.

Shared physical infrastructure still needs logical and capacity isolation.

**Model dependency failure.** Determine which decisions stop, degrade, use stale data, queue, or fall back when each store, network, region, identity service, key service, or pipeline fails.

Avoid cyclic fallbacks and retry amplification. Validate the system composition, not only component availability.

**Observe consumer outcomes.** Track authority commits, propagation positions, lag, query latency, errors, saturation, cache hit reasons, stale reads, reconciliation, recovery, and decision impact.

Provider uptime and CPU metrics alone cannot prove data fitness.

**Assess operability.** Evaluate provisioning, patching, upgrades, schema change, indexing, partitioning, backups, restore, failover, observability, incidents, support, and automation.

Managed services transfer some tasks, not accountability. Clarify shared responsibility and evidence access.

**Assess team and ecosystem fit.** Consider client libraries, query languages, delivery workflows, local testing, debuggability, hiring, on-call load, documentation, and support.

Novel technology can be justified, but its learning and failure costs belong in the decision.

**Calculate total lifecycle cost.** Include compute, storage, replicas, backups, network, egress, licenses, support, engineering, on-call, data movement, idle headroom, migration, and exit.

Unit price multiplied by average volume misses peaks, minimum commitments, amplification, and labor.

**Design portability and exit.** Preserve canonical data, schemas, change histories, identifiers, export paths, compatible interfaces where useful, and migration capacity.

Portability is not avoiding every provider feature. It is knowing the benefit, dependency, replacement cost, and recovery path.

**Record the decision.** Capture workload contract, candidate configurations, gates, evidence, benchmark, risks, assumptions, choice, rejected alternatives, topology, owners, exceptions, review triggers, and retirement.

The record should let a future reviewer understand why the system fit then and what change would invalidate it.

**Review continued fitness.** Trigger review on workload growth, new operations, changed correctness, incidents, provider limits, price, region, regulation, skills, end of support, or acquisition.

Do not wait for failure or renewal negotiations to discover architectural drift.

**Migrate with explicit authority.** Declare old and new roles, source of truth during each interval, capture boundary, backfill, dual-read or shadow comparison, cutover, rollback, freeze, and reconciliation.

Avoid open-ended dual writes and ambiguous ownership. Every transitional state gets an owner and exit condition.

**Retire completely.** Inventory writers, readers, pipelines, snapshots, backups, exports, credentials, DNS, firewall rules, alerts, contracts, licenses, and retained data.

Stop writes, migrate consumers, verify reconciliation, preserve required evidence, delete prohibited copies, revoke access, end costs, and record closure.

## Definitions and Notation

Represent workload $w$ as $w=(O,D,A,C,S,P,E,L)$, where $O$ is outcomes and operations, $D$ data shape and scale, $A$ authority, $C$ correctness and consistency, $S$ service qualities, $P$ protection, $E$ economics and operability, and $L$ lifecycle.

For candidate configuration $x$, let hard requirements be $H={h_1,\ldots,h_n\}$. Eligibility is

$$
Eligible(x,w)=\bigwedge_{h\in H} h(x,w).
$$

Only eligible candidates receive weighted comparison $Score(x)=\sum_i \alpha_i s_i(x)$, where weights, score evidence, uncertainty, and sensitivity are recorded. A higher score cannot override a failed hard gate.

For a composition of authority $a$ and projections $p_1,\ldots,p_k$, each edge records source and target identity, position, delivery, transformation, freshness, correction, deletion, replay, reconciliation, failure, and owner.

Define `FitMapping(M,w,t)` as a review predicate requiring justified outcome, explicit authority, operation and data fit, passed hard gates, representative service evidence, safe composition, effective protection, operability, economic viability, ownership, migration, and lifecycle closure at time $t$.

## Mechanisms, Invariants, or Proof Structure

Use ten architecture gates.

**1. Outcome gate.** Define actors, decisions, transactions, observations, deadlines, consequences, fallback, and value.

**2. Authority gate.** Assign fact and mutation ownership, identities, invariants, corrections, deletes, and histories.

**3. Workload gate.** Quantify operations, access patterns, data shape, scale, skew, growth, concurrency, and temporal needs.

**4. Correctness gate.** Require consistency, isolation, ordering, durability, jurisdiction, and protection before scoring.

**5. Service gate.** Define latency distributions, useful throughput, availability, degradation, RPO, RTO, and capacity evidence.

**6. Composition gate.** Assign system roles and specify propagation, versions, lag, replay, reconciliation, and failure coupling.

**7. Operations gate.** Prove observability, change, backup, restore, failover, incident response, support, and team readiness.

**8. Economics gate.** Compare full lifecycle cost, utilization, headroom, data movement, labor, commitments, and uncertainty.

**9. Evidence gate.** Preserve prototypes, representative benchmarks, failure tests, assumptions, scores, dissent, and decision records.

**10. Lifecycle gate.** Define review triggers, compatibility, migration, authority transfer, rollback, exit, and verified retirement.

Passing a gate supports one scoped workload and configuration. It does not endorse a product for every workload or future condition.

### Executable evidence

The executable example applies hard gates before comparing weighted fit.

<!-- bijux-verify: {"id":"workload-platform-hard-gates","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"workload=order-commit\nrelational_hard_gates=pass\nrelational_weighted_score=64\nsearch_hard_gates=fail\nsearch_weighted_score=55\nauthority=relational-system-of-record\nsearch_role=derived-query-projection\ndecision=compose-with-reconciliation\n","stderr":""}} -->
```python
weights = {
    "consistency": 5,
    "latency": 4,
    "query_fit": 3,
    "operations": 2,
    "cost": 1,
}
candidates = {
    "relational": {
        "gates": [True, True, True],
        "scores": [5, 4, 4, 4, 3],
    },
    "search": {
        "gates": [False, False, True],
        "scores": [2, 5, 5, 3, 4],
    },
}

def weighted_score(scores):
    return sum(weight * score for weight, score in zip(weights.values(), scores))

relational = candidates["relational"]
search = candidates["search"]
print("workload=order-commit")
print(f"relational_hard_gates={'pass' if all(relational['gates']) else 'fail'}")
print(f"relational_weighted_score={weighted_score(relational['scores'])}")
print(f"search_hard_gates={'pass' if all(search['gates']) else 'fail'}")
print(f"search_weighted_score={weighted_score(search['scores'])}")
print("authority=relational-system-of-record")
print("search_role=derived-query-projection")
print("decision=compose-with-reconciliation")
```

The result proves only Boolean gates and integer-weight arithmetic for two in-memory candidates. It does not prove product semantics, transaction safety, search quality, benchmark validity, propagation, reconciliation, capacity, recovery, protection, cost, operational readiness, or architectural fitness.

## Alternatives and Trade-Offs

**One general-purpose store.** Fewer systems reduce movement and operations. It fits when one model meets all hard requirements with acceptable efficiency and isolation.

**Purpose-built composition.** Specialized roles improve access fit but add propagation, consistency, protection, skills, cost, and retirement burden.

**Managed service.** Providers operate infrastructure and some controls. This reduces toil while adding service limits, shared responsibility, pricing, and dependency.

**Self-managed system.** Teams gain configuration and deployment control. They also own patching, capacity, recovery, security, and expertise.

**Synchronous projection.** Consumers see derived state within the command path, but latency, availability, and distributed-outcome ambiguity increase.

**Asynchronous projection.** Authority commits independently and projections can scale, but consumers need lag, revision, and degraded behavior.

**Strong consistency.** It simplifies some invariants and reads while potentially increasing coordination latency and reducing availability under partition.

**Bounded or eventual consistency.** It can improve locality and availability when consumers tolerate and observe staleness; it shifts reasoning to versions and reconciliation.

**Precompute versus query on demand.** Precomputation lowers read cost but adds storage and freshness. On-demand queries preserve flexibility but consume runtime capacity.

**Open portability versus provider differentiation.** Portable formats and interfaces ease exit. Provider-specific features can deliver real value when dependency is conscious and reversible enough.

Choose the smallest composition that passes hard gates and demonstrates fit under representative load, failure, protection, operations, cost, and lifecycle evidence.

## Failure Modes and Misconceptions

1. **A product category determines fit.** Configurations and workloads vary inside every category.
2. **SQL means relational guarantees.** Syntax does not prove constraints, isolation, or transactions.
3. **NoSQL means unlimited scale.** Keys, partitions, skew, limits, and operations still bound systems.
4. **A search index can own facts.** Indexing can lag, omit, duplicate, and reorder source changes.
5. **A cache is durable storage.** Replaceability, miss behavior, and source capacity define a cache.
6. **A log is a database for every query.** Logs optimize ordered retention and consumption, not arbitrary serving.
7. **Replication is backup.** Replicas can copy corruption, deletion, and operator error.
8. **Average latency describes service.** Tails, errors, concurrency, payload, and saturation matter.
9. **High benchmark throughput proves fit.** Wrong data, guarantees, topology, or load shape invalidates comparison.
10. **Weighted scores can trade away correctness.** Hard gates cannot be compensated by convenience.
11. **Multiple stores are automatically resilient.** Dependencies and retries can increase correlated failure.
12. **Eventual consistency needs no bound.** Consumers require observable versions, lag, and correction behavior.
13. **Managed means no operations.** Accountability, configuration, integration, recovery, and incidents remain.
14. **Cheapest unit price means lowest cost.** Amplification, headroom, egress, labor, migration, and support matter.
15. **Dual writes make migration safer.** They can create conflicting authority and unknown outcomes.
16. **A successful restore proves recovery.** Backlog, reconciliation, consumers, and decision readiness remain.
17. **Stopping traffic retires a store.** Data, backups, pipelines, credentials, contracts, and costs can persist.

## Worked Examples

### Example 1

Order commits need multi-row invariants and read-your-writes; full-text discovery needs relevance and facets. A relational authority feeds a search projection with version reconciliation. **Conclusion:** one domain can justify distinct authoritative and query roles.

### Example 2

Session lookup uses one key, small values, short TTL, and reconstructible state. A key-value store fits; the durable account system remains authority. **Conclusion:** bounded key access and replaceability define the role.

### Example 3

A product catalog stores nested aggregates but pricing validity spans products and regions. A document model fits catalog reads, while price authority and cross-product rules require a separate governed boundary. **Conclusion:** model fit is operation-specific.

### Example 4

Fraud relationship investigation repeatedly traverses several hops among accounts, devices, and merchants. Representative graph queries outperform complex dynamic joins, but source identities and corrections remain external authorities. **Conclusion:** traversal evidence, not connected-looking data, justifies graph serving.

### Example 5

Telemetry arrives append-only at high volume, is queried by time range, downsampled, and expired by tier. A time-series role fits; configuration history is versioned separately. **Conclusion:** time-keyed operations and retention shape the selection.

### Example 6

A data lake retains raw objects economically, while a warehouse publishes governed finance releases with concurrency and semantic controls. **Conclusion:** storage and analytical serving are distinct roles even when data is shared.

### Example 7

A cache shows 99.9% hit rate but the authority cannot survive the remaining synchronized misses after restart. Load testing exposes collapse during warm-up. **Conclusion:** capacity caches need failure engineering.

### Example 8

A vector index returns similar support cases, but recall changes with embedding version and deletion lags. Source cases, embedding lineage, evaluation, filtering, and reconciliation remain explicit. **Conclusion:** approximate retrieval is a derived model-dependent product.

### Example 9

A candidate wins a weighted score but cannot keep protected records in the required jurisdiction. It is excluded before ranking. **Conclusion:** scoring never overrides a hard gate.

### Example 10

A managed database price appears low until replicas, cross-region transfer, backups, peak headroom, support, migration, and on-call integration are included. **Conclusion:** compare lifecycle systems, not list prices.

## Cross-Program Connections

- **Data engineering:** schemas, partitions, file formats, pipelines, change capture, materialization, tests, reconciliation, and backfills implement the mapping.
- **Platform engineering:** paved provisioning, policy, observability, backup, recovery, tenancy, quotas, and lifecycle make selected capabilities operable.
- **API and service engineering:** consumer interfaces translate store semantics into stable contracts, freshness, errors, pagination, idempotency, and limits.
- **Distributed systems:** consistency, isolation, ordering, replication, partitioning, coordination, failure, and recovery constrain every composition.
- **Security and privacy:** jurisdiction, identity, authorization, encryption, key control, audit, minimization, retention, and deletion can exclude candidates.
- **Reliability engineering:** latency distributions, capacity, overload, degradation, RPO, RTO, reconciliation, and incident response determine service fit.
- **Software delivery:** infrastructure, schemas, clients, policies, migrations, compatibility, rollback, and decommissioning require controlled releases.
- **Economics:** total cost, utilization, commitments, egress, labor, opportunity cost, migration, and exit influence sustainable selection.
- **Systems engineering:** stakeholder outcomes, hard constraints, trade studies, evidence, uncertainty, lifecycle assurance, and verification structure the decision.

## References

1. Microsoft, *Prepare to Choose a Data Store in Azure*. <https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-stores-getting-started>
2. Microsoft, *Understand Data Models*. <https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/understand-data-store-models>
3. Microsoft, *Choose an Analytical Data Store in Azure*. <https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/analytical-data-stores>
4. AWS, *Well-Architected Framework: Data Management*. <https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/data-management.html>
5. Google Cloud, *Plan Resource Allocation*. <https://docs.cloud.google.com/architecture/framework/performance-optimization/plan-resource-allocation>
6. PostgreSQL Global Development Group, *Multiversion Concurrency Control: Introduction*. <https://www.postgresql.org/docs/current/mvcc-intro.html>
7. Apache Kafka, *Design*. <https://kafka.apache.org/40/design/design/>
8. Google, *Site Reliability Engineering: Addressing Cascading Failures*. <https://sre.google/sre-book/addressing-cascading-failures/>
9. NIST, *SP 800-160 Volume 1 Revision 1: Engineering Trustworthy Secure Systems*. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>

## Exercises

### Exercise 1

Map an order-management workload that needs transactional commits, customer search, operational dashboards, long-term audit, and recovery. Define roles, hard gates, propagation, and degradation.

### Exercise 2

A team proposes one globally distributed document store for account balances, full-text search, event replay, analytics, and archive. Evaluate the workload decomposition and candidate without assuming it must be rejected or accepted.

### Exercise 3

Design a representative evaluation for a high-volume tenant-keyed serving workload with severe skew, regional failover, protected data, and a two-hour recovery objective.

### Exercise 4

A search projection is missing 0.2% of orders after a source schema change, and clients have begun correcting orders through the search API. Describe containment, repair, and architectural correction.

### Exercise 5

Compare one general-purpose store, a managed purpose-built composition, and a self-managed composition for a small team whose workload may grow tenfold. Include cost, skill, evidence, migration, and exit.

## Answers to the Exercises

### Answer 1

Make the relational order service authoritative for order identity, line items, price, inventory reservation references, status transitions, uniqueness, and multi-record commit. Emit versioned changes through a durable outbox or log. Build a search projection for customer, text, and facet discovery; an operational analytical projection for bounded dashboards; immutable or versioned audit history under retention policy; and independent backups or snapshots for disaster recovery.

Hard gates include transaction invariants, acknowledged-write durability, jurisdiction, protected access, deletion and retention, order identity, and recovery. Each projection records source positions, order versions, schema, corrections, deletes, freshness, replay, and reconciliation. If search fails, preserve order commit and offer bounded lookup or explicit search unavailability. If dashboards lag, mark their cutoff. Exercise restore of authority first, then replay projections without overloading it; reconcile keys and versions before declaring decision readiness.

### Answer 2

Decompose operations before choosing. Balance mutation needs invariants, concurrency, durability, read semantics, and conflict policy. Search needs indexing, ranking, and lag tolerance. Replay needs ordered retained facts, source identity, and consumer positions. Analytics needs scans, aggregations, history, and workload isolation. Archive needs economical durable retention, integrity, holds, and retrieval objectives. Then evaluate the exact document-store configuration against each hard gate and representative load.

The product might legitimately own account aggregates if its transactions and global behavior preserve the scoped invariants. Search indexes within it may be a derived capability, while an external immutable log or object archive may remain necessary. Analytics may use isolated replicas or another projection if it cannot harm commits. Accept one platform only when roles, isolation, failure, recovery, protection, cost, and exit all fit; split roles when evidence shows divergent access or lifecycle needs. Product unity does not imply one authority or resource pool.

### Answer 3

Build data at forecast scale with real value sizes, tenant counts, key frequencies, hot tenants, growth, deletes, and protected classifications. Test point reads and mutations at normal, seasonal, impulse, and replay loads with production clients, encryption, authorization, network paths, indexes, replicas, and background maintenance. Measure useful throughput, latency percentiles by tenant, errors, saturation, cost, replication lag, fairness, and invariant correctness.

Fail a region and dependencies under load; observe routing, consistency, duplicate or lost effects, queue growth, retry amplification, and degraded behavior. Test backup and restore at full size, rebuild indexes, replay retained changes, drain backlog, reconcile keys and versions, and demonstrate consumer readiness inside two hours with the declared RPO. Verify residency, key access, audit, deletion, incident evidence, and tenant isolation. Preserve configurations and raw results, quantify uncertainty, and repeat at review triggers.

### Answer 4

Stop corrections through the search API, preserve evidence, mark search results incomplete, identify the schema and position boundary, notify consumers, and protect authoritative order mutation. Inventory missing, malformed, duplicated, and stale order IDs; determine whether clients acted on wrong search results or sent unauthorized corrections; route valid commands through the order authority and compensate unsafe outcomes under domain policy.

Repair the schema contract and projector in an isolated target. Replay from a trusted source position or snapshot with load limits, compare keys, versions, values or digests, deletes, and coverage, then cut over after accountable approval. Remove mutation capability from search, enforce API boundaries, add source-version responses, schema compatibility gates, gap detection, keyed reconciliation, and incident alerts. Test that losing or corrupting search degrades discovery without changing authoritative orders.

### Answer 5

One general-purpose store minimizes systems, data movement, and on-call surfaces; choose it if exact configuration passes hard gates and tenfold capacity with acceptable isolation and cost. A managed purpose-built composition can improve search, analytics, or cache fit while transferring infrastructure work, but adds service limits, propagation, provider dependency, egress, and reconciliation. Self-managed specialization offers control and portability options but demands deep skills, patching, capacity, backup, recovery, and continuous operations.

Model current and tenfold distributions, peaks, failure headroom, replicas, backups, transfer, support, labor, incidents, migration, and exit. Prototype only risky operations and benchmark representative configurations. Prefer the smallest passing composition the team can operate. Preserve canonical exports, identities, positions, schemas, decision records, and migration capacity; define review triggers for growth and skills; avoid adopting specialized systems only for hypothetical scale, but do not ignore hard constraints that already require them.
