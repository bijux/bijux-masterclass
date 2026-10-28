---
module_id: DARCH-005
program: Data Architecture Engineering
level: 1
module_number: 5
title: Operational, Analytical, and Shared Data
status: complete
last_verified: 2026-09-03
---

# Operational, Analytical, and Shared Data

## One-Page Review

### Governing question

How should an architecture distinguish data used to execute current operations, data reorganized to analyze observations across time and domains, and data deliberately shared across boundaries while preserving authority, fitness, and lifecycle obligations?

### Essential definitions

- **Operational data** supports bounded state transitions and immediate decisions in a running business or technical process.
- **Analytical data** is selected and organized to describe, compare, explain, predict, or evaluate phenomena for declared populations, definitions, and time horizons.
- **Shared data** is data intentionally offered across an ownership, product, organizational, jurisdictional, or trust boundary under a governed contract.
- A **workload** is a set of reads, writes, transformations, latency, consistency, history, scale, and failure expectations—not merely a query language.
- A **projection** is a consumer-oriented representation derived from authoritative sources at identifiable source positions.
- A **semantic contract** defines population, grain, keys, measures, dimensions, units, time, missingness, corrections, and compatibility.
- A **serving contract** defines interface, format, freshness, availability, access, cost, limits, support, and lifecycle behavior.

### Central model, mechanism, or theorem

Classify responsibilities rather than platforms:

`Fitness(product, use) = semantic_fit and temporal_fit and operational_fit and policy_fit`

Operational and analytical are workload roles. Shared is a boundary relationship. The same governed product may support more than one role, but each use needs explicit authority, representation, snapshot or source position, quality, service, policy, and correction terms. A copy is not shared responsibly merely because another team can read it.

### Critical invariants

- Operational commands return to the authoritative transition boundary; analytical copies do not become accidental writers.
- Analytical outputs identify source versions, population, grain, definitions, event and processing times, and `as_of` or revision state.
- Cross-boundary products name producer, consumers, purpose, authority, contract, policy, support, and exit.
- Shared representations hide private implementation choices and expose compatible, versioned semantics.
- Corrections, deletions, restrictions, and policy changes propagate according to declared rules.
- Freshness, consistency, completeness, and availability are measured at the consumer decision boundary.
- Physical co-location or separation follows workload evidence and risk, not the labels alone.

### Common failures

Common failures include defining operational as “database” and analytical as “warehouse,” running unbounded scans on command stores, feeding operations from stale extracts, sharing private tables, equating replication with a product contract, mixing incompatible grains, omitting event time, overwriting history, granting broad access for convenience, and creating an enterprise canonical dataset whose coordination cost exceeds its demonstrated reuse.

### Compact example

An order service records accepted order transitions. A positioned event stream builds a daily order-line analytical product with event time, correction, and reconciliation rules. Finance consumes a governed monthly projection, while support consumes a fresh order-status view. Both are shared, but their grains, freshness, policy, and service contracts differ. Neither may bypass the order command boundary.

### Connections

[DARCH-004](004-systems-of-record-engagement-and-insight.md) assigns record, engagement, and insight roles. [DARCH-006](../ROADMAP.md) develops principles and decision rules. [Database Engineering](../../18-database-engineering/ROADMAP.md) supplies transaction and analytical storage mechanisms; [Data Engineering](../../19-data-engineering/ROADMAP.md) supplies pipelines, quality, lineage, serving, and lifecycle mechanisms.

## Governing Question

Data architectures commonly draw operational systems on the left, an integration layer in the middle, and analytical systems on the right. The picture can clarify broad movement, but it becomes a false law when it equates roles with products. Operational and analytical requirements overlap; sharing cuts across both; and every derived representation carries authority, temporal, policy, and lifecycle consequences.

An operational service may answer analytical-looking aggregates needed to execute a workflow. An analytical platform may publish an authoritative governed metric. A stream may feed both fraud decisions and historical analysis. A shared product may remain in a producer's store and be accessed by service rather than copied. The architecture must reason from consumers and decisions to contracts and mechanisms.

The governing question is therefore about fitness. What state transition or analysis is being performed? Which facts and histories are required? At what time, grain, consistency, and scale? Across which boundary? Which authority, policy, cost, correction, and failure obligations follow? Only after these are known should the architecture select stores, replication, federation, or interfaces.

## Why This Matters

Operational systems protect current decisions. Poorly isolated analytical work can exhaust their resources, hold locks, expose private schemas, or read inconsistent snapshots. Conversely, extracts built to protect operations can become stale, unreconciled, and semantically detached while consumers treat them as truth.

Analytical work joins domains and spans history. It needs stable populations, temporal semantics, reproducible snapshots, comparable definitions, and often large scans. Without those properties, a fast query can still produce an invalid conclusion. Changing source systems, late events, corrections, and policy restrictions make analytical truth explicitly versioned.

Sharing multiplies both value and obligation. A producer no longer controls when a field is interpreted, cached, combined, exported, or used to make a decision. Consumers create dependencies; classifications propagate; support and compatibility costs persist; deletion becomes distributed. An undocumented grant or copied table transfers risk without establishing a product relationship.

Good separation improves autonomy and safety. Operational models can evolve behind contracts, analytical products can optimize for evidence and history, and shared interfaces can expose only the stable semantic intersection. Good integration also avoids needless copies where governed query, secure view, or in-place computation meets the use.

## Prerequisites and Retrieval

You should understand transactions, schemas, indexes, APIs, events, batch and stream processing, basic dimensional modeling, access control, and data-product ownership. Recall the distinction between an authoritative fact and a projection, and between a conceptual dataset and its physical distributions.

Retrieve grain, business key, event time, valid time, transaction time, snapshot, watermark, idempotency, consistency, lineage, classification, retention, and service-level objective. This chapter uses these concepts to compare roles rather than prescribe one platform pattern.

## Learning Objectives

After completing this module, you should be able to:

- distinguish operational, analytical, and shared responsibilities without reducing them to technologies;
- characterize a workload by decision, reads, writes, history, latency, consistency, concurrency, and failure;
- define analytical population, grain, temporal basis, measures, dimensions, and revision policy;
- define semantic and serving contracts for cross-boundary data products;
- choose among direct access, API, events, replication, governed views, files, and federated query;
- preserve source authority while serving consumer-specific projections;
- identify workload interference, stale-decision, fan-out, policy, and lifecycle risks;
- design correction, deletion, restriction, reconciliation, and recovery behavior;
- evaluate standardization against domain fit and coordination cost;
- verify consumer fitness with evidence at the point of use.

## Core Exposition

Start with the **use**, not the store. A use record names the actor or system, decision or output, fact population, acceptable latency, history, consistency, error consequence, policy, volume, concurrency, and recovery behavior. The same physical dataset can be fit for one use and unsafe for another.

**Operational data** participates in current execution. It may represent an order being accepted, inventory being reserved, a case being assigned, a device command being acknowledged, or access being authorized. Operational workloads often combine selective reads and state transitions under concurrency, bounded latency, invariant enforcement, and immediate failure handling.

Operational does not mean small, relational, normalized, or synchronous. A high-volume event service is operational if it participates in current work. A document or key-value store may enforce a domain transition. A periodic optimization may be operational when its output commits tomorrow's schedule. The defining concern is the live decision and its authority.

Operational models commonly organize data around transaction and domain boundaries. They may avoid redundant state that could diverge, or deliberately maintain synchronized projections for latency. Their schemas often change with application behavior. Exposing private operational tables makes consumers depend on implementation, transaction timing, and codes never designed as public semantics.

**Analytical data** supports inquiry across observations. It may describe what happened, diagnose relationships, compare segments, forecast outcomes, evaluate an intervention, or produce a governed report. Analytical workloads frequently scan many records, join domains, aggregate at multiple grains, and require stable history and reproducibility.

Analytical does not mean read-only in implementation. Pipelines write tables, users curate annotations, experiments record results, and products revise published measures. The distinction is that these writes construct evidence or derived products rather than accept the source domain's operational transition.

Michael Stonebraker and Uğur Çetintemel's [“One Size Fits All”](https://cs.brown.edu/~ugur/fits_all.pdf) argument explains why specialized data-management engines arise for differing workloads. It is a research position, not proof that every organization needs separate platforms. Workload shape, scale, skills, operations, and lifecycle cost determine whether specialization pays.

Every analytical product needs a population and **grain**. “Daily sales” could mean one row per order day, shipment day, store-local day, customer, order, line, or product-location. Measures must state aggregation and additivity. Dimensions need version and slowly changing behavior. Mixing order-level revenue with line-level promotions can multiply values while producing syntactically valid queries.

Time is part of meaning. Record event time, source-recording time, ingestion time, processing time, valid time, and revision or publication time where relevant. A daily product should define timezone, day boundary, late-event cutoff, backfill, and restatement. An `as_of` label without a source position can hide partial ingestion.

Historical truth may be mutable. Corrections arrive, identities merge, exchange rates restate, policies change, and late facts cross reporting windows. Choose append, bitemporal history, snapshot, correction event, overwrite-plus-audit, or versioned release according to consumer needs. Publish how prior results change.

Analytical consistency is not automatically weaker. A financial close may require a clean, frozen, reconciled cut stricter than a support screen. A monitoring view may prefer recent partial information with uncertainty. Define consistency at the decision boundary rather than ranking operational and analytical categories.

**Shared data** crosses an accountable boundary. The boundary may separate teams, domains, products, legal entities, jurisdictions, trust zones, platforms, or external parties. Sharing can occur by copy, event, API, query, clean room, view, model execution, or governed in-place computation. Physical movement is not required.

Conversely, copying does not establish sharing responsibly. A replica without a named producer, consumer, purpose, contract, policy, support path, and lifecycle is merely duplicated state. It may already be business-critical, but its obligations are hidden.

A shared data product has a stable identity separate from its table or endpoint. W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) distinguishes conceptual datasets, distributions, and data services. One product can have a batch file, API, and queryable representation with different freshness and access properties.

The **semantic contract** defines what consumers may mean by the product. Include population, grain, keys, entity resolution, measures, dimensions, units, code sets, nulls, duplicates, event and valid time, source authority, transformations, exclusions, quality thresholds, corrections, and compatibility rules.

The **serving contract** defines how and under what operational conditions data is consumed. Include interface and version, format and schema, authentication and authorization, freshness, availability, latency, throughput, quotas, delivery, ordering, retention, support, cost attribution, observability, incident communication, deprecation, and exit.

The **policy contract** maps classification, permitted purposes, recipients, residency, minimization, retention, preservation, deletion, audit, and exception authority. Policy cannot be inferred from an interface. A public endpoint can serve restricted data incorrectly; a private table can still be shared lawfully under control.

Consumer registration should be proportional to consequence. At minimum identify consuming product and owner, purpose, decision, representation, criticality, policy basis, expected volume, SLO dependence, and migration contact. Anonymous discovery can remain available where safe, but consequential production use must be visible enough to support change and incident response.

Choose the sharing mechanism by constraints. An **API** supports selective, current, policy-mediated access but couples availability and latency. **Events** decouple producers and convey accepted change, but require ordering, replay, schema, duplicate, and retention design. **Batch files** create simple durable exchanges but add snapshot, transfer, duplication, and correction obligations.

A **governed view** can reduce copying and centralize current rules but couples query workload and availability. **Replication** isolates reads and preserves local availability but introduces lag and lifecycle. **Federated query** keeps data in place but distributes performance, policy, metadata, and failure dependencies. **Secure computation or clean-room patterns** may constrain disclosure but do not remove semantic, legal, or inference risk.

Direct access to operational tables is tempting because it avoids a pipeline. It also exports private schema, bypasses service authorization, exposes transient states, and lets scans interfere with commands. Where it is justified, publish stable read interfaces, resource isolation, snapshot semantics, access controls, and a migration contract.

Change-data capture can build analytical projections without modifying the source application. It observes physical or logical changes, which may not equal stable business events. Transaction-log ordering, snapshot bootstrap, schema changes, deletes, before-images, transaction boundaries, and resynchronization become part of correctness.

Domain events communicate accepted meaning more directly, but they require intentional product design and evolution. Not every consumer need belongs in the operational event. Producers should expose stable facts; consumers construct their projections. A universal event containing every downstream field recreates shared-table coupling.

Reconciliation proves that a derived representation agrees with declared source invariants at a boundary. Compare counts, control totals, keys, state transitions, event positions, and sampled records. Equality of row counts does not establish semantic equivalence. Reconciliation must include late and corrected data.

Freshness has components: source delay, extraction delay, queue delay, processing delay, publication delay, cache delay, and consumer observation delay. Measure the end-to-end condition. A pipeline completing on schedule does not prove that the source was current or the consumer read the latest release.

Quality is use-relative. Referential integrity important to billing may be irrelevant to an aggregate that excludes the relation; approximate sketches may be fit for exploration but not payment. Define validity, completeness, uniqueness, consistency, timeliness, and accuracy expectations against the consumer decision and consequence.

Shared products need change discipline. Classify changes as compatible, conditionally compatible, or breaking for each consumer use. Additive schema change can still break positional files, wildcard queries, privacy minimization, or exhaustive enumeration. Semantic changes can break every consumer without changing schema.

Version at the contract boundary. Preserve definition, schema, transformations, source versions, policy, and release identity. During migration, run old and new representations long enough to compare consequential consumers. Retirement depends on evidence of migration or authorized acceptance, not elapsed notice alone.

Corrections require consumer-visible identity. State whether a release is replaced, superseded, or amended; how consumers locate affected keys and windows; whether downstream products must recompute; and how audit history remains accessible. For events, use explicit correction or compensating semantics instead of mutation consumers cannot observe.

Deletion and restriction propagate across shares. Maintain the mapping needed to identify copies and derivatives, while minimizing unnecessary personal detail. Backups, aggregates, model artifacts, legal holds, external recipients, and immutable logs need policy-specific treatment. “Delete at source” is not a distributed deletion protocol.

Operational and analytical isolation can be physical, logical, or scheduled. Separate compute pools, replicas, workload management, resource groups, priorities, quotas, and snapshot exports are options. Isolation reduces interference but increases duplication, lag, cost, and operational surfaces. Verify with load and failure evidence.

Security architecture follows purpose and boundary. Apply least privilege, service identities, field or row controls where appropriate, protected transport and storage, output controls, audit, anomaly detection, and revocation. Analytical aggregation can reduce some exposure while linkage and broad history increase others.

Economics span producer and consumers. Include extraction, transfer, storage copies, compute, egress, catalog, controls, support, incidents, backfills, migration, and exit. A central share may reduce duplicate engineering but create concentrated cost and priority contention. Unit costs should connect to products and decisions without encouraging unsafe omission of controls.

Standardization should target demonstrated intersections. Shared identifiers, time conventions, classifications, contract metadata, and a small semantic core can enable composition. Forcing every domain into one canonical physical schema can freeze local evolution and create lowest-common-denominator meaning. Document translation where legitimate differences remain.

Observability joins the roles. Track source position, pipeline run, data-quality outcomes, release identity, consumer reads, SLOs, incidents, and corrections. Operational telemetry must not leak sensitive values. Analytical lineage must not be mistaken for causal proof.

Recovery must cover more than bytes. Restore source snapshots, logs or events, schemas, contracts, definitions, policies, keys, lineage, checkpoints, orchestration, access, and consumer releases to a consistent boundary. Then replay idempotently and reconcile before reopening consequential decisions.

Governance is a product relationship, not a committee afterthought. Producers own declared semantics and service; consumers own appropriate use and local controls; policy authorities set constraints; platforms provide mechanisms; a forum resolves cross-boundary conflict. “Everyone owns shared data” usually means no one can decide.

## Definitions and Notation

Let a use be `u = (actor, decision, population, grain, history, latency, consistency, scale, consequence, policy)`. Let a product representation be `p = (authority, sources, transform, schema, position, as_of, quality, service, policy, owner)`.

Define four necessary fitness predicates:

- `S(p,u)`: semantic fit—population, grain, keys, definitions, units, and correction match;
- `T(p,u)`: temporal fit—event time, history, source position, freshness, and revision match;
- `O(p,u)`: operational fit—availability, latency, throughput, recovery, and support match;
- `P(p,u)`: policy fit—purpose, recipient, minimization, location, retention, and control match.

Then:

`Fitness(p,u) = S(p,u) and T(p,u) and O(p,u) and P(p,u)`

The conjunction matters. Excellent freshness does not compensate for an unlawful purpose; correct semantics do not compensate for missing availability in a safety-critical decision. Some constraints are noncompensable.

Let `pos(p)` identify source offsets or snapshot versions included in `p`. Let `release(p)` identify its published version. Two products with the same schema and row count are not equivalent unless their population, meaning, positions, policy, and correction state agree for the use.

## Mechanisms, Invariants, or Proof Structure

Review an operational, analytical, or shared design through eight gates.

**1. Use gate.** Name the consumer decision, actor, population, consequence, history, latency, consistency, and policy. Reject platform-first requirements.

**2. Authority gate.** Identify source authorities and permitted transitions. Ensure analytical or shared copies cannot bypass authoritative commands.

**3. Semantic gate.** Define population, grain, keys, measures, dimensions, units, missingness, time, exclusions, quality, and correction.

**4. Representation gate.** Select API, event, file, view, replication, federation, or computation. Record source positions, transforms, release, and reproducibility.

**5. Service gate.** Define freshness, availability, latency, throughput, delivery, quotas, observability, incident, recovery, support, and cost.

**6. Policy gate.** Verify purpose, recipients, minimization, access, residency, retention, preservation, deletion, audit, and exceptions across every distribution.

**7. Evolution gate.** Version contracts, discover consumers, test compatibility, dual run where needed, propagate corrections, and require evidence for retirement.

**8. Assurance gate.** Test load isolation, stale and partial data, duplicate delivery, late facts, source resnapshot, backfill, revocation, recovery, reconciliation, and consumer behavior.

The following executable linter checks three product descriptions. It rejects an analytical copy allowed to accept operational writes, a shared snapshot with no consumer contract, and an analytical cube with no `as_of` identity.

<!-- bijux-verify: {"id":"data-role-contract-review","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"products=3\nvalid=0\nfindings=customer_snapshot:shared-without-contract,order_commands:analytical-copy-as-writer,sales_cube:missing-as-of\nready=false\n","stderr":""}} -->
```python
products = {
    "order_commands": {
        "analytical": True,
        "accepts_operational_writes": True,
        "shared": False,
        "consumer_contract": True,
        "as_of": "events:920",
    },
    "customer_snapshot": {
        "analytical": False,
        "accepts_operational_writes": False,
        "shared": True,
        "consumer_contract": False,
        "as_of": "snapshot:2026-09-01",
    },
    "sales_cube": {
        "analytical": True,
        "accepts_operational_writes": False,
        "shared": False,
        "consumer_contract": True,
        "as_of": "",
    },
}

findings = []
valid = 0
for name, product in products.items():
    local = []
    if product["analytical"] and product["accepts_operational_writes"]:
        local.append("analytical-copy-as-writer")
    if product["shared"] and not product["consumer_contract"]:
        local.append("shared-without-contract")
    if product["analytical"] and not product["as_of"]:
        local.append("missing-as-of")
    if local:
        findings.extend(f"{name}:{finding}" for finding in local)
    else:
        valid += 1

print(f"products={len(products)}")
print(f"valid={valid}")
print(f"findings={','.join(sorted(findings))}")
print(f"ready={str(not findings).lower()}")
```

This output verifies only the three declared conditions over the fixture. It does not prove the products' semantics, source positions, policies, isolation, contracts, or consumer fitness. Production evidence must include real contracts, source and runtime observations, tests, policy authority, and accountable review.

## Alternatives and Trade-Offs

**One store versus workload isolation.** One store reduces movement and can provide current consistency. Isolation protects commands and enables specialized layout but adds lag, copies, cost, and reconciliation.

**Normalized operational model versus denormalized serving model.** Normalization can protect update integrity. Denormalization reduces joins for consumers but duplicates facts and needs refresh and correction rules.

**Batch versus streaming.** Batch creates explicit snapshots and can simplify reconciliation. Streaming lowers potential latency but adds event-time, watermark, ordering, replay, and continuous-operation complexity.

**Copy versus query in place.** Copying isolates load and supports local history, while multiplying data and lifecycle duties. In-place query reduces copies but couples availability, performance, policy, and metadata.

**API versus event.** APIs offer current selective responses and centralized policy. Events support decoupled change propagation and replay. Many products need both, with reconciliation between snapshot and stream.

**Central warehouse versus federated products.** Centralization simplifies cross-domain joins and controls but can bottleneck semantics and ownership. Federation preserves domain context but needs interoperable contracts, identity, and governance.

**Canonical model versus translation.** A canonical intersection reduces repeated mapping. A universal model can erase valid differences and slow change. Standardize where reuse exceeds coordination cost.

**Freshness versus clean consistency.** Rapid partial results help some operations; frozen reconciled cuts serve others. Publish distinct products instead of hiding incompatible promises behind one name.

## Failure Modes and Misconceptions

1. **Operational means OLTP database.** It means participation in current execution; many technologies can implement it.
2. **Analytical means warehouse.** Analysis can occur elsewhere, and a warehouse can serve authoritative derived facts.
3. **Shared is a storage tier.** Sharing is a governed relationship across a boundary.
4. **Read access is a contract.** Permissions alone omit semantics, purpose, service, support, change, and lifecycle.
5. **A replica is current.** Its source position and lag determine temporal fit.
6. **Schema compatibility preserves meaning.** Population, definition, time, and policy can change without schema change.
7. **More freshness is always better.** Fast partial data can be worse than a clean reconciled cut.
8. **Row counts prove reconciliation.** Duplicates, omissions, wrong keys, and changed meanings can preserve counts.
9. **CDC emits business events.** Physical changes require interpretation before they become stable domain facts.
10. **Federation eliminates integration.** It moves integration into query planning, semantics, identity, policy, and operations.
11. **Deletion at the source deletes shared data.** Copies, caches, backups, exports, and derivatives need governed treatment.
12. **A common platform creates common semantics.** Meaning and authority require explicit cross-domain decisions.

## Worked Examples

### Example 1

**Question:** Is a five-minute inventory aggregate operational or analytical?

**Reasoning:** If it determines current replenishment, it participates in operations; it is also a derived analytical projection. Roles can overlap.

**Conclusion:** Classify the use, not the query shape.

### Example 2

**Question:** May analysts query the order database directly?

**Reasoning:** Only with stable semantics, authorization, snapshot behavior, workload isolation, and lifecycle agreement. A projection is often safer, but not free.

**Conclusion:** Directness trades movement for coupling.

### Example 3

**Question:** Two daily sales tables have identical columns. Are they interchangeable?

**Reasoning:** Compare population, grain, day boundary, source position, returns, currency, late facts, corrections, and policy.

**Conclusion:** Schema equality is not semantic equivalence.

### Example 4

**Question:** A dashboard refreshes every minute. Is it fresh?

**Reasoning:** Not necessarily. The source may be hours behind. Measure end-to-end event-to-consumer delay and expose `as_of`.

**Conclusion:** Schedule success is not data freshness.

### Example 5

**Question:** A partner can download a file from object storage. Is it a shared product?

**Reasoning:** Only if identity, semantics, purpose, recipient, service, policy, corrections, support, and exit are governed.

**Conclusion:** Accessibility alone is unmanaged distribution.

### Example 6

**Question:** Can a fraud projection decline a payment while the payment service is unavailable?

**Reasoning:** Only if policy delegates that decision under defined staleness and failure conditions. Otherwise it may queue or refuse safely.

**Conclusion:** Analytical availability does not confer operational authority.

### Example 7

**Question:** Is streaming always more current than batch?

**Reasoning:** A stalled consumer or incomplete watermark can lag behind a completed reconciled batch. Compare actual source positions and decision needs.

**Conclusion:** Architecture labels do not establish observed freshness.

### Example 8

**Question:** An additive column breaks no parser. Is the change compatible?

**Reasoning:** It may expand sensitive data, alter wildcard results, violate minimization, or break exhaustive semantics.

**Conclusion:** Compatibility is consumer- and policy-relative.

### Example 9

**Question:** How should a corrected transaction affect last month's report?

**Reasoning:** Follow the product's close and restatement policy: amend, supersede, or preserve the prior release while publishing reconciliation.

**Conclusion:** Historical truth needs explicit revision semantics.

### Example 10

**Question:** When should two workloads share physical infrastructure?

**Reasoning:** When measured concurrency, isolation, failure, security, recovery, skills, and lifecycle cost satisfy both uses with margin.

**Conclusion:** Co-location is an evidence-based deployment choice.

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) develops transactions, indexing, isolation, replication, temporal data, analytical execution, and recovery. These mechanisms implement workload guarantees but do not assign semantic or policy authority.

[Data Engineering](../../19-data-engineering/ROADMAP.md) develops ingestion, CDC, batch, streaming, contracts, quality, lineage, backfill, orchestration, serving, SLOs, economics, and lifecycle. [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) addresses distributed analytical and streaming behavior at scale.

[API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) develops shared service and event contracts, versioning, compatibility, authentication, idempotency, and deprecation. [Security Engineering](../../25-security-engineering/ROADMAP.md) governs trust boundaries, access, minimization, audit, threat, and response.

## References

- Michael Stonebraker and Uğur Çetintemel, [*“One Size Fits All”: An Idea Whose Time Has Come and Gone*](https://cs.brown.edu/~ugur/fits_all.pdf), ICDE, 2005. Primary research argument for workload-specialized data engines.
- Microsoft, [*CQRS Pattern*](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs), Azure Architecture Center, checked 2026-09-03. Official discussion of command and read models, separate stores, synchronization, materialized views, and trade-offs.
- Microsoft, [*Materialized View Pattern*](https://learn.microsoft.com/en-us/azure/architecture/patterns/materialized-view), Azure Architecture Center, checked 2026-09-03. Official guidance on precomputed consumer representations and consistency.
- W3C, [*Data Catalog Vocabulary (DCAT) — Version 3*](https://www.w3.org/TR/vocab-dcat-3/), W3C Recommendation, 2024. Normative vocabulary for datasets, distributions, services, series, and catalog records.
- W3C, [*PROV-Overview*](https://www.w3.org/TR/prov-overview/), W3C Working Group Note, 2013. Official overview of interoperable provenance for entities, activities, agents, derivation, and responsibility.
- NIST, [*Big Data Interoperability Framework: Volume 6, Reference Architecture, Version 3*](https://doi.org/10.6028/NIST.SP.1500-6r2), NIST SP 1500-6r2, 2019. Vendor-neutral provider, consumer, application, framework, orchestrator, management, and security/privacy roles.
- Apache Iceberg, [*Table Specification*](https://iceberg.apache.org/spec/), checked 2026-09-03. Official specification for table snapshots, sequence numbers, schema and partition evolution, and metadata needed for versioned analytical state.
- Martin Fowler, [*Event Sourcing*](https://martinfowler.com/eaaDev/EventSourcing.html), 2005. Primary pattern account of event histories, replay, temporal query, correction, and integration.

## Exercises

### Exercise 1

Characterize the operational and analytical uses of inventory availability for checkout, replenishment, and quarterly planning. State which properties differ.

### Exercise 2

Write semantic, serving, and policy contracts for a daily order-line product shared with Finance.

### Exercise 3

Compare API, event, batch file, replicated table, and federated query for sharing current account status with support.

### Exercise 4

Design correction and restatement behavior for a monthly revenue product when late refunds and currency-rate corrections arrive.

### Exercise 5

Design an assurance plan for moving analytical queries off an operational database onto a CDC-fed projection.

## Answers to the Exercises

### Answer 1

Checkout needs item-location sellable quantity at request time, low latency, bounded staleness, and safe refusal or reservation behavior under uncertainty. Replenishment may combine recent inventory, commitments, lead times, forecasts, and policy in a scheduled operational decision; it needs an auditable input cut and correction before execution. Quarterly planning needs longer history, comparable definitions, scenario versions, and reconciled aggregates rather than transaction-current state. All three may derive from common authorities, but their population, grain, freshness, history, consistency, uncertainty, availability, and decision consequence differ. Publish separate positioned projections or service operations when one promise cannot safely cover them.

### Answer 2

The semantic contract defines one row per accepted order line and finance day, order and line keys, seller and jurisdiction population, event and close timezone, currency and conversion source, gross, discount, tax, refund, cancellation, null and duplicate rules, source authorities, exclusions, late events, and restatement. The serving contract defines a versioned file or table release, schema, snapshot/source positions, completion marker, publication deadline, availability, checksum, access, support, reconciliation totals, correction notification, deprecation, and exit. The policy contract defines Finance's purpose, allowed identities and regions, minimization, classification, retention, preservation, deletion/restriction, audit, onward sharing, and exception authority. Consumers register their reports and decision consequences.

### Answer 3

An API provides selective current status and centralized policy but couples support to account-service availability and latency. Events enable a local support view and history but require ordering, replay, correction, and lag handling. A batch file is simple and reconcilable but likely too stale for consequential current action. A replica isolates reads but exports schema and needs lag, access, and lifecycle control. Federated query avoids a managed copy but couples performance and failure across systems. A common design uses a positioned support projection for display and the authoritative API for state-changing commands, with explicit stale-state labeling and incident fallback.

### Answer 4

Freeze each monthly release with definition, input positions, currency table version, close cutoff, and control totals. Late refunds and corrected rates enter a subsequent computation. Policy decides whether the original remains immutable with an amending release or is superseded by a restated version. Publish affected periods, keys or aggregates, reason, materiality, old and new totals, approval, and consumer action. Preserve audit history and prevent silent overwrite in downstream reports. Recompute derivatives whose contract requires restatement; notify and track consequential consumers. Accounting authority, not the pipeline alone, approves close and restatement semantics.

### Answer 5

Baseline operational query latency, lock/resource contention, analytical result semantics, volumes, consumers, access, and incidents. Bootstrap a clean snapshot at a recorded log position, then apply CDC with transaction ordering, idempotency, schema, delete, and resnapshot rules. Define projection grain, source position, freshness, reconciliation, corrections, access, SLOs, recovery, and ownership. Dual run representative and peak workloads; compare keys, counts, control totals, sampled records, late changes, and consumer outputs. Inject connector outage, duplicates, schema changes, backfill, source restore, and projection rebuild. Migrate named consumers, monitor old queries, and retire direct access only after accountable acceptance and rollback evidence.
