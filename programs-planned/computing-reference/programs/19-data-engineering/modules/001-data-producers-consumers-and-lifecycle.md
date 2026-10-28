---
module_id: DE-001
program: Data Engineering
level: 1
module_number: 1
title: Data Producers, Consumers, and Lifecycle
status: complete
last_verified: 2026-08-29
---

# Data Producers, Consumers, and Lifecycle

## One-Page Review

### Governing question

How should data engineers preserve the meaning, accountability, and fitness of data as producers create it, pipelines transform it, consumers use it, and policy eventually archives or disposes of it?

### Essential definitions

- A **data producer** is an accountable system or process that creates or publishes data at a named boundary.
- A **data consumer** is an accountable use that reads data and relies on specified semantics or service properties.
- A **dataset version** is an identified, bounded data object whose contents and interpretation can be distinguished from other versions.
- A **data product** is a governed delivery boundary combining data, metadata, service expectations, ownership, and support—not merely stored bytes.
- A **lifecycle** is the set of allowed activities from planning and acquisition through processing, publication, use, evolution, preservation, and disposition.
- **Lineage** records relationships among inputs, transformations, runs, and outputs; **provenance** supports an account of how a particular data entity came to exist.
- A **system of record** is the authoritative source for a stated fact and time boundary; a **derived dataset** is computed from one or more sources.

### Central model, mechanism, or theorem

Treat every governed dataset version as a contract:

`identity + meaning + producer + transformation + consumers + policy + evidence`.

For each derivation `D_out = T(D_1, ..., D_n; C)`, record immutable input-version identities, transformation and configuration identity `T,C`, run identity, output identity, accountable owner, quality evidence, access classification, retention/disposition policy, and known consumers. Lifecycle stages are not a universal linear pipeline; they are control points over an evolving provenance graph.

### Critical invariants

- Every published version has a stable identity, owner, purpose, schema/meaning, and source boundary.
- A derived output points to the exact input versions and transformation run that produced it.
- Consumers do not silently turn undocumented fields or timing accidents into contracts.
- Corrections create traceable replacements or restatements; they do not erase history invisibly.
- Retention and disposition propagate across replicas, caches, exports, and derived products according to applicable policy.
- Observability distinguishes source absence, ingestion delay, transformation failure, quarantine, and consumer lag.

### Common failures

Frequent failures are treating the producer's database as the consumer contract, copying without ownership, confusing arrival time with event time, mutating published data in place, recording table-level lineage without version/run identity, retaining data “just in case,” deleting only the primary copy, discovering consumers during deprecation, and treating a successful pipeline run as evidence of semantic correctness.

### Compact example

A commerce service emits order facts. Finance consumes settled amounts; fulfillment consumes shippable items. A field rename can compile in the producer yet break both meanings. A durable boundary names the event or snapshot version, semantics, owner, compatibility window, quality checks, known consumers, and correction process. Storage location alone supplies none of those guarantees.

### Connections

[DE-002](../ROADMAP.md) distinguishes rows, columns, records, and events. Source authority connects to [Database Engineering](../../18-database-engineering/ROADMAP.md); enterprise ownership and policy belong to [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md); large-scale execution belongs to [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md); service contracts connect to [API & Service Engineering](../../28-api-and-service-engineering/ROADMAP.md).

## Governing Question

Data engineering begins before a pipeline reads its first byte and continues after a table stops receiving queries. Someone decides what a fact means, a system emits an observation, a pipeline selects and transforms it, a consumer makes a decision, and an owner eventually migrates, preserves, or disposes of the result. Each step can change meaning or create a new obligation. The governing question is therefore not “How do we move data?” but “How do we preserve an accountable chain from production to use and disposition?”

The [NIST Research Data Framework 2.0](https://doi.org/10.6028/NIST.SP.1500-18r2) organizes research-data concerns through six lifecycle stages: envision, plan, generate/acquire, process/analyze, share/use/reuse, and preserve/discard. Commercial pipelines use different vocabulary, but the structure exposes an important principle: acquisition, transformation, reuse, and disposition require decisions, roles, and evidence. The lifecycle is a reasoning framework, not a claim that every datum moves once through a single sequence.

## Why This Matters

Data outlives the code that produced it. A service release can be rolled back, but a corrupted historical table may have fed financial reports, experiments, models, alerts, and exported files. A producer can correct its current database while downstream copies continue to encode the old error. Conversely, a consumer can assign a new interpretation to an unchanged field and create a semantic defect without changing any producer bytes.

Data pipelines amplify both value and error. One source may feed dozens of direct consumers and hundreds of transitive ones. A transformation can standardize names and validate constraints, but it can also discard provenance, collapse distinctions, amplify bias, or create false precision. The engineering task is to make those changes observable and reviewable.

Lifecycle thinking also controls cost and risk. Unbounded retention consumes storage, increases breach impact, complicates correction and deletion, and leaves stale products discoverable. Premature deletion destroys auditability or reproducibility. A defensible policy states purpose, authority, retention trigger, period, preservation requirements, deletion scope, exceptions, and evidence. Technology executes that policy; it does not choose it.

## Prerequisites and Retrieval

You should understand files, databases, APIs, basic Python, schemas, and the distinction between mutable operational state and an immutable historical observation. Recall that an identifier names an object only within a namespace, a timestamp requires a clock and event definition, and a checksum establishes byte equality under an algorithm but not semantic correctness. You should also distinguish logical data meaning from its physical storage location.

## Learning Objectives

After completing this module, you should be able to:

- identify producers, consumers, owners, and intermediaries at a data boundary;
- distinguish source facts, observations, commands, events, snapshots, and derived data;
- model a dataset lifecycle as controlled activities over versioned entities;
- state the minimum contract for a published dataset or stream;
- distinguish lineage, provenance, metadata, and audit evidence;
- explain why bounded and unbounded sources need different completeness reasoning;
- inventory direct and transitive consumers before evolution or retirement;
- design correction, replay, preservation, and disposition paths;
- diagnose semantic, temporal, quality, privacy, and ownership failures;
- scope human review for high-consequence data uses.

## Core Exposition

A producer is defined at a boundary, not by a team label. A point-of-sale terminal produces observations of scans. A commerce service produces accepted-order events. A connector produces extracted records from a database log. A transformation job produces a curated table. The same component can consume one dataset and produce another. Producer identity must therefore include the system, operation, version, and accountable owner.

A consumer is similarly an identifiable use, not merely a query process. A dashboard, billing reconciliation, fraud feature, regulatory export, scientific analysis, and ad hoc notebook may consume the same table for different purposes. They can tolerate different freshness, completeness, history, and correction behavior. “Analytics uses this table” is not a consumer inventory; it is an unbounded risk statement.

Data does not carry meaning by itself. A numeric field named `amount` could mean requested, authorized, captured, refunded, gross, net, or converted value. A timestamp could denote physical occurrence, producer recording, ingestion, processing, or publication. A row could represent an event, current entity state, interval, aggregate, or correction. A useful boundary declares grain, units, domain, nullability, identifiers, time semantics, valid ranges, and update/correction behavior. Later modules develop representations and schemas; this module establishes why those choices belong to a producer-consumer contract.

The source of truth is scoped. An order service may be authoritative for accepted order intent, a payment processor for settlement, and a warehouse system for physical shipment. No single system is universally authoritative for “the order.” Authority can also vary by time: an event records what was asserted at occurrence, while a corrected master record supplies the current interpretation. Data engineers must not merge those temporal claims accidentally.

A data lifecycle is better represented as a graph of entities and activities than a single chain. A raw source version may feed standardized and quarantine outputs. A curated version may feed a report and a model. A correction may invalidate one version, produce a replacement, and trigger bounded recomputation. An archive may preserve one representation while operational replicas are disposed. Each node has identity and state; each edge has a named derivation or use.

The W3C [PROV Data Model](https://www.w3.org/TR/prov-dm/) distinguishes **entities**, **activities**, and **agents**. An entity is a thing with fixed aspects for the provenance account; an activity uses or generates entities over time; an agent bears responsibility. These concepts fit pipelines well: versioned datasets are entities, transformation runs are activities, and services or accountable people/organizations are agents. W3C PROV is a conceptual interoperability model, not an automatic proof that recorded lineage is complete or true.

Version identity is essential. A path such as `warehouse/orders` names a logical product, not necessarily the bytes read on Tuesday. Reproducibility requires a snapshot, partition set, transaction boundary, manifest, commit identifier, or other immutable reference. A mutable “latest” pointer may aid discovery, but evidence should bind the resolved version. Content digests help detect identical bytes; they do not describe schema meaning, source authority, or completeness.

The transformation identity must be equally precise. Record code/artifact version, configuration, relevant reference data, execution parameters, runtime where material, and run identity. `curated_orders = transform(raw_orders)` hides timezone databases, currency tables, schema rules, and deployment configuration. If those inputs can change the output, they belong in the effective derivation record.

Current [OpenLineage 1.52.0 job-facet documentation](https://openlineage.io/docs/spec/facets/job-facets/) models a job as an abstract process with input and output datasets and captures execution through runs. Facets extend job, run, and dataset metadata. This is a useful operational vocabulary. Emitting a lineage event, however, proves only that an emitter submitted a statement. Trust requires identity, completeness controls, reconciliation, access protection, and validation against actual execution.

Dataset lifecycle contracts should include at least:

- stable logical name and immutable version identity;
- accountable producer, product owner, and support route;
- purpose, grain, semantics, schema, time model, and element domain;
- acquisition mode and source authority;
- transformation and provenance identity;
- quality dimensions, acceptance thresholds, and evidence;
- availability, freshness, completeness, and correction expectations;
- classification, access conditions, approved purposes, and export constraints;
- direct consumer registry and deprecation communication path;
- retention trigger, retention/disposition rule, preservation exception, and deletion evidence.

Not every field must live in one document. Schemas, catalogs, manifests, run events, policies, and service objectives may divide the record. They must resolve to one coherent contract rather than contradicting copies.

Boundedness changes completeness. Apache Beam's current programming guide distinguishes bounded collections, such as a fixed file or snapshot, from unbounded collections produced continuously. A bounded dataset can have an enumerated end; an unbounded source is never globally complete. Consumers instead reason about windows, watermarks, checkpoints, or as-of positions. “Processed all records” is meaningful only with a named bound.

Lifecycle stages overlap. Planning defines purpose and future disposition before acquisition. Acquisition captures raw observations and collection context. Validation accepts, rejects, or quarantines according to declared checks. Transformation creates new entities rather than magically cleaning the original. Publication makes a version discoverable under a service contract. Consumption creates uses, dependencies, decisions, and sometimes feedback. Evolution introduces compatible or breaking changes. Preservation retains designated evidence; disposition makes data unavailable within a defined scope and records the outcome.

Publication is not copying to a shared location. It is an explicit state transition: identity is frozen or versioned, checks have an outcome, access is configured, metadata is discoverable, owner/support is live, and consumers know what may be relied upon. A failed or unavailable quality check cannot silently become a pass. Quarantined data remains evidence with restricted use; it is not a second unlabeled truth source.

Consumption creates obligations in both directions. Producers must communicate semantics, changes, incidents, and correction policy. Consumers must declare purpose, criticality, required fields, service expectations, derived outputs, and responsible owner. Consumers must not rely on undocumented behavior and then demand indefinite preservation. Producers must not dismiss actual critical uses merely because they were not registered. Discovery combines declarations, access/query telemetry, lineage, code search, and owner confirmation; no one signal proves completeness.

Corrections must preserve historical intelligibility. Depending on the contract, a source can append a compensating event, issue a new version, restate affected partitions, or update current state while retaining an audit trail. The correction record should say what changed, why, who authorized it, which versions are superseded, and which consumers need recomputation. In-place overwrite without version evidence can make prior results impossible to explain.

Retention is not only a storage time-to-live. It must cover raw and curated stores, replicas, caches, extracts, indexes, backups, dead-letter data, training sets, and downstream products. Some stores may age out asynchronously or require cryptographic erasure, media rotation, or documented exception handling. “Delete row 42” is an implementation action; “honor the applicable disposition decision across known data holdings with evidence” is the lifecycle outcome.

Documentation supports handoff. Gebru and colleagues' [*Datasheets for Datasets*](https://doi.org/10.1145/3458723) proposes structured documentation of motivation, composition, collection, recommended uses, and other lifecycle questions to improve communication between creators and consumers. The [FAIR principles](https://doi.org/10.1038/sdata.2016.18) emphasize findability, accessibility, interoperability, and reuse. FAIR does not mean unrestricted public access: sensitive data can have discoverable metadata and controlled access.

## Definitions and Notation

Let a dataset version be `D = (id, V, M, O, P)`, where `id` is stable identity, `V` is the data value or bounded reference, `M` is semantic and technical metadata, `O` is accountable ownership, and `P` is policy. Let a transformation run be `R = (rid, T, C, I, t)`, containing run identity, transformation identity, configuration, exact input versions, and execution time context.

A derivation assertion is `R : (D_1, ..., D_n) -> D_out`. It is reproducible only to the extent that `T`, `C`, input identities, environment assumptions, and non-data dependencies are captured and available. It is correct only if the transformation semantics and resulting data satisfy their contract; recorded lineage alone cannot establish that.

Let `Consumers(D)` be the known accountable uses of version or product `D`. Let `Desc(D)` be known transitive descendants in the lineage graph. A disposition plan for `D` must consider at least `{D} union Replicas(D) union Exports(D) union Desc(D)` under applicable policy. This set may be incomplete; discovery and reconciliation evidence must state coverage and uncertainty.

Use these distinctions:

- **metadata:** data describing a dataset, run, policy, or other object;
- **lineage:** graph relationships among data and processing steps;
- **provenance:** an account supporting how a particular entity came to exist;
- **audit log:** recorded actions or decisions, not automatically a complete provenance graph;
- **quality evidence:** observations about declared dimensions, not a universal “good data” score;
- **lifecycle state:** a controlled status of a particular version, not the physical location of every copy.

## Mechanisms, Invariants, or Proof Structure

A lifecycle review can be organized as preservation obligations across transitions. Creation establishes identity, owner, purpose, and initial history. Validation records check outcomes and quarantines failures. Publication requires a valid state and complete minimum contract. Consumer registration records accountable dependency. Deprecation requires inventory, replacement or cessation guidance, and dates. Retirement ends supported consumption. Disposition applies policy to the known copy/derivation scope and retains evidence of the action where required.

The executable model below enforces one intentionally simplified linear state path for a single immutable dataset version. It uses functional updates so the original record remains unchanged and requires publication before consumer registration. Real data lifecycles branch, correct, preserve, and replay; the model is a finite demonstration of guarded transitions, not a universal lifecycle engine.

<!-- bijux-verify: {"id":"dataset-lifecycle-guards","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"lifecycle=created>validated>published>deprecated>retired>disposed\nconsumers=finance,fulfillment\nsource_unchanged=created\ninvalid=disposed cannot transition to published\n","stderr":""}} -->
```python
ALLOWED = {
    "created": ("validated",),
    "validated": ("published",),
    "published": ("deprecated",),
    "deprecated": ("retired",),
    "retired": ("disposed",),
    "disposed": (),
}


def advance(asset, target):
    if target not in ALLOWED[asset["state"]]:
        raise ValueError(f"{asset['state']} cannot transition to {target}")
    successor = asset.copy()
    successor["state"] = target
    successor["history"] = asset["history"] + (target,)
    assert successor["owner"]
    assert successor["version_id"]
    assert successor["history"][-1] == successor["state"]
    return successor


def register_consumer(asset, consumer):
    if asset["state"] != "published":
        raise ValueError("consumers register only against a published version")
    successor = asset.copy()
    successor["consumers"] = asset["consumers"] + (consumer,)
    return successor


source = {
    "version_id": "orders/2026-08-29/v3",
    "owner": "commerce-data",
    "state": "created",
    "history": ("created",),
    "consumers": (),
}
asset = advance(source, "validated")
asset = advance(asset, "published")
asset = register_consumer(asset, "finance")
asset = register_consumer(asset, "fulfillment")
asset = advance(asset, "deprecated")
asset = advance(asset, "retired")
asset = advance(asset, "disposed")

print(f"lifecycle={'>'.join(asset['history'])}")
print(f"consumers={','.join(sorted(asset['consumers']))}")
print(f"source_unchanged={source['state']}")
try:
    advance(asset, "published")
except ValueError as error:
    print(f"invalid={error}")
```

The assertions check only local structural invariants. They do not verify that finance and fulfillment are the only consumers, that disposition reached every copy, or that the orders are accurate. Those claims require independent discovery, reconciliation, and domain evidence.

## Alternatives and Trade-Offs

**Central ingestion versus producer-published products.** A central team can standardize controls and reduce duplicated tooling. It may become a semantic bottleneck and own data it cannot interpret. Producer-owned publication keeps meaning close to the source but requires shared interoperability, governance, and operational standards. Responsibility should follow authority, not organizational fashion.

**Snapshot versus event interfaces.** Snapshots simplify current-state queries and bounded reconciliation. Events preserve change history and support incremental consumers, but ordering, duplication, correction, and retention become explicit. Many systems need both, with a documented relationship rather than competing truths.

**Mutable tables versus immutable versions.** Mutable tables support efficient current views. Immutable versions improve reproducibility and auditability but cost storage and require compaction or retention. A common design uses immutable source/history plus governed current projections. “Immutable” must name the boundary; administrators and retention systems may still alter physical storage.

**Push versus pull acquisition.** Push can reduce latency and decouple polling, but creates delivery and backpressure concerns. Pull supports consumer control and bounded snapshots but may increase source load and miss transient state unless change history exists. Either choice needs source positions and replay/reconciliation behavior.

**Central catalog versus local metadata.** A catalog improves discovery and cross-domain lineage. Source-controlled local contracts keep metadata near implementation. Synchronization is the hard part: stale catalog entries are worse than explicit unknowns. Prefer authoritative ownership per field and verifiable publication rather than manual duplication.

**Fine- versus coarse-grained lineage.** Table-level lineage is cheap and useful for blast-radius estimation. Column- or record-level provenance supports precise debugging and disposition but can be expensive, sensitive, or technically incomplete. Choose granularity from decisions it must support and state gaps.

## Failure Modes and Misconceptions

1. **The producer owns the meaning forever.** Downstream transformations create new semantics and require accountable owners.
2. **A schema is the whole contract.** Types omit grain, units, time, quality, correction, service, and policy.
3. **Successful ingestion means complete data.** A source can be partial, late, duplicated, or semantically wrong while transport succeeds.
4. **Lineage proves correctness.** It records asserted relationships; it does not validate inputs, transformation logic, or completeness.
5. **The catalog lists every consumer.** Undeclared notebooks, exports, copied tables, and model features may exist.
6. **Raw means untouched truth.** Acquisition selects fields, times, encodings, permissions, and failure behavior; raw data is still produced.
7. **One lifecycle fits every dataset.** Operational state, telemetry, research observations, financial records, and training data have different purposes and obligations.
8. **Retention means keeping everything.** Purposeless retention increases cost and risk; preservation must be intentional.
9. **Deletion of the primary table completes disposition.** Replicas, caches, extracts, backups, indexes, and derived products remain in scope as policy requires.
10. **No current queries means no consumers.** Seasonal, incident, audit, legal, and disaster-recovery uses may be dormant.

## Worked Examples

### Example 1

**Question:** Who produces a curated customer table built nightly from CRM and billing snapshots?

**Reasoning:** CRM and billing produce source versions. The extraction connectors produce acquired copies. The nightly transformation produces the curated version. The curated product owner is accountable for its declared combined semantics, while source owners retain authority for their facts.

**Conclusion:** Producer identity is specific to each data boundary and derivation.

### Example 2

**Question:** Is a daily file bounded?

**Reasoning:** Only with a closure rule. A named file may be finite, yet late replacements or append behavior can keep its logical contents unsettled. A manifest, source checkpoint, completion marker, or immutable object version supplies the bound.

**Conclusion:** Boundedness is a source contract, not an inference from a filename.

### Example 3

**Question:** A pipeline reports 100% successful records. Is the dataset complete?

**Reasoning:** The percentage uses received records as denominator. If the producer emitted only 80 of 100 expected entities, processing can be perfect while source completeness is 80%. Reconciliation needs an independent expected count or source position.

**Conclusion:** Processing success and source completeness are distinct measures.

### Example 4

**Question:** A producer renames `created_at` to `event_time` without changing values. Is this compatible?

**Reasoning:** Syntax breaks consumers unless an alias or version transition exists. Semantics may also differ: creation time and event occurrence are not interchangeable. Compatibility requires both readable shape and preserved meaning.

**Conclusion:** Schema compatibility cannot rescue a semantic rename.

### Example 5

**Question:** Why is a mutable `latest` table insufficient for reproducing last month's report?

**Reasoning:** Source corrections, late arrivals, reference tables, code, and configuration may all have changed. Reproduction requires exact input snapshots or positions and transformation identity, not the current logical name.

**Conclusion:** Logical discovery names and immutable evidence identities serve different purposes.

### Example 6

**Question:** A lineage system shows `raw.orders -> curated.orders -> revenue`. What is missing?

**Reasoning:** The graph lacks dataset versions, run IDs, transformation artifact/configuration, partitions, time bounds, owners, check outcomes, and whether the emitter observed every execution path. It is useful topology but weak provenance.

**Conclusion:** Lineage granularity must match the decision it supports.

### Example 7

**Question:** How should an erroneous exchange rate be corrected?

**Reasoning:** Identify affected source and derived versions, publish the corrected reference version, run a bounded restatement with a new run ID, compare results, mark superseded outputs, notify consumers, and preserve the reason and authorization. Silent overwrite loses explainability.

**Conclusion:** Correction is a traceable lifecycle operation, not merely a new value.

### Example 8

**Question:** Can a dataset be FAIR while access is restricted?

**Reasoning:** Yes. Metadata and identifiers can make it findable; access rules can be explicit and machine-readable; interoperable metadata and reusable documentation can exist while sensitive bytes require authorization. FAIR is not a synonym for public.

**Conclusion:** Discoverability and controlled access are compatible.

### Example 9

**Question:** A clinical feature table feeds a dosage-support model. May its owner dispose of raw observations after generating features?

**Reasoning:** Not from pipeline convenience alone. Clinical meaning, safety investigation, consent/purpose, correction, reproducibility, applicable retention, model governance, and downstream copies must be assessed. Named clinical, privacy/legal, safety, records, model, security, and data-engineering reviewers must authorize the scoped plan; no such external review is claimed here.

**Conclusion:** High-consequence disposition requires domain and governance authority beyond technical lineage.

### Example 10

**Question:** No catalog query has touched a table for six months. Can it be retired?

**Reasoning:** Query telemetry is one signal. Check scheduled code, seasonal reporting, exports, lineage, access grants, incident runbooks, model features, owner attestations, and required preservation. Publish deprecation, observe the window, then retire with rollback and evidence.

**Conclusion:** Consumer discovery is an evidence synthesis, not a zero-query test.

## Cross-Program Connections

Database engineering establishes transactional source and persistence guarantees, but a database table is not automatically a published analytical contract. Data architecture assigns enterprise-wide domains, policy, and governance; this program implements reliable pipeline boundaries within that environment. Large-scale data systems determine how transformations execute across machines, while data engineering owns the dataset semantics, validation, lineage, and delivery outcome.

API engineering and event systems share producer-consumer evolution problems. Software-delivery provenance identifies build inputs and artifacts; data provenance identifies data entities and transformations. Machine-learning systems intensify the consequences of hidden data consumers and feedback. Sculley and colleagues' [*Hidden Technical Debt in Machine Learning Systems*](https://proceedings.neurips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) identifies undeclared consumers, data dependencies, and feedback loops as system-level risks.

Privacy and security cross every stage. Collection limitation, classification, access, minimization, retention, and disposition are policies whose authority comes from applicable organizational, contractual, ethical, and legal context. A pipeline must carry and enforce those decisions without inventing them.

## References

- Robert Hanisch et al., [*NIST Research Data Framework (RDaF), Version 2.0*](https://doi.org/10.6028/NIST.SP.1500-18r2), NIST SP 1500-18r2, 2024. Official lifecycle-oriented research-data framework.
- W3C, [*PROV-DM: The PROV Data Model*](https://www.w3.org/TR/prov-dm/), Recommendation, 30 April 2013. Official conceptual model for entities, activities, agents, derivation, and responsibility.
- Peter Buneman, Sanjeev Khanna, and Wang-Chiew Tan, [*Why and Where: A Characterization of Data Provenance*](https://doi.org/10.1007/3-540-44503-X_20), ICDT 2001. Primary paper distinguishing forms of database provenance.
- OpenLineage, [*Facets and Extensibility*](https://openlineage.io/docs/spec/facets/) and [*Job Facets*](https://openlineage.io/docs/spec/facets/job-facets/), specification 1.52.0, checked 2026-08-29. Current official run, job, dataset, and extensible metadata model.
- Apache Beam, [*Programming Guide*](https://beam.apache.org/documentation/programming-guide/), checked 2026-08-29. Current official model for bounded and unbounded pipeline collections.
- Mark D. Wilkinson et al., [*The FAIR Guiding Principles for Scientific Data Management and Stewardship*](https://doi.org/10.1038/sdata.2016.18), Scientific Data 3, 2016. Primary statement of findable, accessible, interoperable, and reusable principles.
- Timnit Gebru et al., [*Datasheets for Datasets*](https://doi.org/10.1145/3458723), Communications of the ACM 64(12), 2021. Primary proposal for lifecycle-aware dataset documentation.
- D. Sculley et al., [*Hidden Technical Debt in Machine Learning Systems*](https://proceedings.neurips.cc/paper_files/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html), NeurIPS 2015. Primary discussion of undeclared consumers, data dependencies, and feedback loops.
- Martin Kleppmann and Chris Riccomini, [*Designing Data-Intensive Applications*, second edition](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/), O'Reilly Media, 2026. Durable system-of-record, derived-data, encoding, and dataflow foundations.

## Exercises

### Exercise 1

For a warehouse table of daily product inventory, identify a producer, two possible consumers, one version identity, and four essential contract elements beyond the schema.

### Exercise 2

A pipeline reads source snapshot `S7` using transform artifact `T3` and currency table `C9`, producing `D12`. Write the derivation assertion and list the evidence needed to reproduce it. Explain why the output path alone is insufficient.

### Exercise 3

A customer table's row count drops 35%, yet every received row passes validation and the job exits successfully. Diagnose at least four possible causes and propose evidence that distinguishes them.

### Exercise 4

Compare event and snapshot interfaces for order data. Design a combined lifecycle contract that supports current-state analytics, historical correction, replay, and bounded retirement.

### Exercise 5

A wildfire-response agency wants to retire a location dataset used by dispatch, evacuation modeling, public alerts, and research partners. Define the technical evidence and named human-review roles required before retirement and disposition. Account for intermittent and exported consumers.

## Answers to the Exercises

### Answer 1

The inventory service or its governed export is the source producer; a replenishment planner and an availability dashboard are two consumers. A version identity could be an immutable manifest for business date 2026-08-29 with source transaction/checkpoint bounds. Beyond schema, the contract needs grain (one row per product-location-date), meaning and units of quantities, source authority and closure time, accountable owner/support, freshness/completeness expectations, correction behavior, classification/access, and retention. Any four of those with precise values satisfy the request; merely naming a storage table does not.

### Answer 2

Write `R42 : (S7, C9) --T3,P--> D12`, where `R42` is the run identity and `P` contains material parameters and environment assumptions. Retain immutable identities or manifests for `S7` and `C9`, the exact `T3` artifact/source revision, configuration and parameters, relevant runtime/tool versions, start/end or logical time boundary, output identity/digest, schema versions, and check outcomes. The path may later point to different bytes, and it says nothing about code, reference data, configuration, or run context.

### Answer 3

Possible causes include genuine source activity decline, source extraction stopping early, a changed filter, schema parsing that rejects records before the measured validation stage, source partition omission, time-zone boundary shift, deduplication collapse, or an upstream deletion/correction. Compare independent source counts/checkpoints, expected partition manifests, extraction logs, quarantine/pre-validation counts, code/configuration diffs, event-time distributions, key cardinality, and source owner confirmation. Do not lower the alert or republish merely because all received rows are valid.

### Answer 4

Use immutable events as the historical change interface with stable event identity, aggregate identity, event time, ordering scope, schema version, correction/compensation semantics, retention, and replay position. Publish versioned snapshots with an as-of boundary, source event-position range, manifest, completeness evidence, and current-state schema. Record that snapshot `Qn` derives from a closed position set of the event source. Consumers needing current state use snapshots; incremental consumers use events; reconciliation compares a replayed projection with a snapshot. Retirement must preserve schema/upcaster and event history through the supported replay window, deprecate both interfaces with registered consumers, and state which artifacts are retained afterward.

### Answer 5

Inventory direct and transitive uses through catalog declarations, query/access telemetry, code and schedule search, export registers, lineage, contracts, emergency runbooks, and owner attestations. Identify every immutable version, replica, device/offline cache, partner export, derived model, backup, and preservation obligation. Test the replacement or cessation path under degraded connectivity and peak incident conditions; reconcile coverage, publish deprecation, run drills, preserve required provenance, and define rollback plus disposition evidence. Named reviewers should include dispatch operations, wildfire/evacuation domain experts, public-safety and human-factors authorities, geospatial/data engineering, partner representatives, privacy/legal and records-management authorities, security, incident command, accessibility/community communication, and an independent safety/assurance reviewer required by the agency. The exact legal and command authority is jurisdiction-specific. No external review has been performed by this chapter, so its answer is a review plan rather than retirement authorization.
