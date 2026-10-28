---
module_id: DARCH-064
program: Data Architecture Engineering
level: 2
module_number: 64
title: Lineage Architecture
status: complete
last_verified: 2026-09-03
---

# Lineage Architecture

## One-Page Review

### Governing question

How should an enterprise identify, capture, qualify, combine, query, protect, validate, operate, and retire lineage assertions so that people and machines can reason about origin, transformation, impact, responsibility, and evidence without mistaking an incomplete graph for causality or truth?

### Essential definitions

- **Data lineage** is a governed set of assertions about how identified data entities, activities, and agents relate across declared scopes, times, versions, and evidence sources.
- **Provenance** is information about entities, activities, and agents involved in producing, influencing, or delivering something; lineage is an application-oriented view of that broader provenance.
- A **lineage entity** is an identified data-bearing or data-describing thing with sufficiently fixed aspects for a lineage question, such as a dataset version, field, partition, report, feature set, model artifact, file, message collection, or policy result.
- A **lineage activity** is an identified occurrence or planned transformation that uses, generates, copies, filters, joins, aggregates, validates, publishes, or otherwise affects entities.
- A **lineage assertion** is an attributable statement relating entities, activities, agents, or other assertions, with type, scope, evidence, time, confidence, and lifecycle.
- **Design lineage** describes intended dependencies derived from code, plans, schemas, or declared configuration.
- **Observed lineage** describes a particular execution or event as captured at runtime.
- **Reconstructed lineage** is inferred after the fact from logs, queries, diffs, statistics, or other evidence and must retain that inferential status.
- **Dataset-level lineage** relates collections; **field-level lineage** relates fields; record- and value-level lineage relate progressively finer instances.
- **Direct dependence** means an output value or entity is computed from an input; **control dependence** means an input affects whether, when, or how output is produced without necessarily contributing a value.
- **Lineage coverage** is the explicitly measured portion of a declared estate, transformation class, time interval, or critical path for which required assertions exist.
- **Lineage closure** is the verified end of active capture, publication, query, propagation, retention, and recovery obligations while preserving evidence required for historical interpretation.

### Central model, mechanism, or theorem

Represent a lineage system as:

`L = (E, A, G, X, I, T, V, P, Q, O, C)`

where `E` is versioned entity identity, `A` activities and agents, `G` typed graph assertions, `X` evidence and extraction, `I` integration and normalization, `T` temporal semantics, `V` validation and assurance, `P` protection and policy, `Q` query and decision profiles, `O` operations and recovery, and `C` change and closure. A lineage answer is fit only relative to a named question, scope, time, granularity, evidence threshold, access policy, and completeness claim. Reachability in an asserted graph proves only that an accepted path of assertions exists; it does not by itself prove actual execution, value contribution, legal responsibility, semantic equivalence, classification inheritance, or causal necessity.

### Critical invariants

- Entity identity distinguishes logical asset, physical representation, version, partition, field, record, and value when the question requires those boundaries.
- Job definition, job version, run, task attempt, query, and transformation step are not collapsed into one activity identifier.
- Every accepted edge has a relation type, source, target, producer, evidence class, observed or asserted time, version context, and lifecycle state.
- Design, observed, manually declared, imported, and reconstructed assertions remain distinguishable after normalization.
- Used and generated entities do not automatically establish derivation; the asserted influence and transformation semantics must be justified.
- Direct value dependence, control dependence, filtering, joining, aggregation, copying, masking, and unknown transformation remain distinct.
- Dataset-level evidence does not imply field-, record-, or value-level coverage.
- A graph query states its direction, depth or stopping rule, time slice, version policy, edge policy, confidence threshold, and hidden-node behavior.
- Absence of an edge is not evidence of independence unless coverage and negative-evidence conditions are established.
- Lineage-driven propagation of classifications, policies, or obligations is an explicit governed rule, not an automatic consequence of graph reachability.
- Corrections preserve superseded assertions and their decision history while preventing known-invalid edges from remaining silently active.
- Retirement closes producers, subscriptions, indexes, caches, APIs, credentials, recovery, and consumer dependencies without destroying required historical provenance.

### Common failures

Common failures include drawing arrows between mutable names; treating a job definition as a successful run; deriving lineage from orchestration order alone; inferring field dependencies from dataset inputs; omitting filters and control dependencies; recording only successful paths; losing partition and version context; joining graphs by normalized labels; presenting design lineage as observation; treating query logs as complete; flattening copies, revisions, transformations, and semantic mappings into one edge; propagating sensitive classifications across every reachable node; hiding inaccessible nodes without disclosing path redaction; measuring node count instead of decision coverage; allowing stale lineage to authorize changes; and deleting history during platform migration.

### Compact example

Five versioned assets and four activities are connected by four qualified assertions. Three assertions are observed and one is declared. A small executable check confirms every endpoint exists, every interval is coherent, one source root reaches the report, the source can affect four downstream assets, and the accepted graph is acyclic. It proves consistency of invented records only; it does not prove capture completeness, execution authenticity, transformation correctness, field semantics, causal necessity, or safe impact analysis.

### Connections

[DARCH-017](017-event-schemas-and-information-models.md), [DARCH-018](018-temporal-and-historical-modeling.md), [DARCH-027](027-producer-and-consumer-contracts.md), [DARCH-036](036-change-data-capture-architecture.md), [DARCH-048](048-feature-and-training-data-architecture.md), [DARCH-061](061-metadata-architecture.md), [DARCH-062](062-metadata-harvesting-and-synchronization.md), and [DARCH-063](063-business-glossaries-and-term-governance.md) establish event, time, contract, capture, metadata, and meaning foundations. [DARCH-065](../ROADMAP.md) next develops ontologies and knowledge graphs.

## Governing Question

A lineage diagram often looks authoritative because arrows are visually decisive. Yet an arrow can mean “configured before,” “read during one run,” “possibly contributed a value,” “was copied from,” “was declared by an owner,” “was inferred from SQL,” “shares a business concept,” or merely “appeared in the same workflow.” Those meanings support different decisions.

The governing question is how to construct lineage as a qualified evidence system rather than a decorative graph: precise enough for change safety, incident analysis, governance, audit, privacy, model traceability, and reproducibility; honest about missing instrumentation and inference; protected against disclosure and tampering; and operable across changing platforms and organizational boundaries.

## Why This Matters

W3C's [PROV Data Model](https://www.w3.org/TR/prov-dm/) defines domain-independent entities, activities, agents, generation, usage, derivation, attribution, association, delegation, bundles, specialization, alternates, and collections. It also warns that using an entity in an activity that generates another entity is necessary but not sufficient to establish derivation: influence must be determined. Enterprise lineage should preserve that distinction.

[PROV-O](https://www.w3.org/TR/prov-o/) provides an OWL 2 ontology for representing and interchanging provenance on the Web. It demonstrates how qualified relations and provenance bundles can carry additional detail, but an enterprise still needs domain profiles, identity rules, evidence classes, authorization, operations, and decision-specific validation.

W3C [PROV-CONSTRAINTS](https://www.w3.org/TR/prov-constraints/) defines inference, normalization, uniqueness, event-ordering, impossibility, and type constraints for provenance instances. Structural validity helps reject incoherent histories. It does not establish that instrumentation observed every relevant activity or that a producer's claims are trustworthy.

W3C [PROV-AQ](https://www.w3.org/TR/prov-aq/) describes mechanisms for discovering, accessing, and querying provenance, including provenance links, services, and pingback. Lineage architecture therefore includes access and discovery contracts, not just graph storage.

The current [OpenLineage object model](https://openlineage.io/docs/spec/object-model/) distinguishes jobs from runs and represents input and output datasets with extensible facets. It supports runtime and design events, reflecting the architectural need to separate a reusable transformation definition from a particular execution and its actual inputs and outputs.

OpenLineage's [run cycle](https://openlineage.io/docs/spec/run-cycle/) describes lifecycle updates such as `START`, `RUNNING`, and terminal outcomes and notes that events for a run can be cumulative or partial. A collector must assemble, validate, and reconcile run evidence instead of assuming one event is a complete execution record.

The OpenLineage [Lineage Dataset Facet](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/) represents dataset-, job-, and field-level inputs for structural relationships, including relationships with no natural event job. It distinguishes entity-level inputs from field-level inputs and can describe transformation types. A standard representation improves exchange but does not prove the producer captured dynamic behavior correctly.

[Apache Atlas](https://atlas.apache.org/) models metadata types and entity instances in a graph, exposes lineage through APIs and a UI, and can propagate classifications via lineage. It illustrates useful catalog capabilities while also exposing a key governance question: which relation types, boundaries, exceptions, and evidence authorize propagation?

[OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/) represent a request path as spans with identifiers, parents, links, times, attributes, events, status, and kind. Operational traces can correlate runtime activity with data lineage, but span parentage concerns execution flow and must not automatically be recast as data derivation.

[SLSA provenance](https://slsa.dev/spec/v1.2/provenance) defines provenance as verifiable information about where, when, and how software artifacts were produced. Data lineage has broader semantics, but the emphasis on artifact binding, producer trust, and verifiability is a useful corrective to unauthenticated lineage claims.

## Prerequisites and Retrieval

You should understand metadata architecture, data models, identifiers, datasets, schemas, fields, partitions, transformations, SQL, batch and stream processing, workflow orchestration, events, change data capture, graphs, temporal modeling, distributed systems, observability, provenance, data governance, privacy, security, reliability, versioning, migration, and audit evidence.

Retrieve lineage, provenance, entity, activity, agent, assertion, generation, usage, derivation, influence, attribution, association, specialization, alternate, bundle, job, job version, run, task attempt, input, output, source, sink, dependency, data flow, control flow, trace, span, design lineage, observed lineage, reconstructed lineage, dataset lineage, field lineage, record lineage, value lineage, direct dependence, control dependence, impact analysis, root cause, reachability, path, cycle, strongly connected component, temporal graph, coverage, confidence, attestation, redaction, reconciliation, correction, and closure.

As a retrieval test, inspect “table B comes from table A.” Ask which versions and partitions, through which activity and run, whether the edge is declared or observed, what “comes from” means, whether every field or only some rows depend on A, whether A controls filtering without contributing values, what code and parameters ran, who asserted the relationship, when it was valid, which evidence supports it, what was omitted, and which decision may rely on the claim. The sentence is a clue, not a lineage contract.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish lineage, provenance, dependency, data flow, control flow, operational trace, audit log, and semantic relationship;
2. model versioned entities, activities, agents, assertions, evidence, time, and responsibility without collapsing their identities;
3. choose dataset, field, record, or value granularity according to decision consequence and capture feasibility;
4. separate design, declared, observed, imported, and reconstructed lineage and assign appropriate assurance;
5. capture batch, streaming, API, file, manual, analytical, feature, model, and cross-organization transformations;
6. normalize and reconcile heterogeneous lineage without inventing equivalence or hiding conflict;
7. specify temporal, traversal, uncertainty, redaction, and version semantics for lineage queries;
8. validate coverage, correctness, freshness, integrity, protection, recovery, and consumer fitness;
9. design propagation, impact, incident, privacy, audit, and reproducibility uses with bounded claims; and
10. migrate and retire lineage capabilities while preserving required historical evidence.

## Core Exposition

**Begin with decisions.** List the decisions lineage must support: whether a breaking schema change can ship, which reports a defect may affect, where a restricted value traveled, which inputs trained a model, why a metric changed, whether an output is reproducible, and which owner must respond.

Each decision needs different entities, granularity, latency, history, evidence, and access. A graph adequate for catalog browsing may be unsafe for deletion proof or financial control.

**Define an assurance profile.** For each decision, name scope, authoritative sources, required edge types, granularity, maximum age, history, confidence, completeness target, query behavior, protection, validation, failure response, and accountable approver.

Avoid one universal “lineage completeness” percentage. Coverage of scheduled warehouse tables says little about spreadsheets, application-side transformations, streaming state, model features, or manual exports.

**Separate related disciplines.** Dependency says one thing relies on another. Data flow describes movement. Control flow describes execution order or choice. Operational tracing follows requests and work. Audit logs record events. Provenance describes production, influence, delivery, and responsibility. Lineage selects and profiles assertions from these domains for data decisions.

Do not convert every adjacency into derivation. An orchestrator predecessor might be a readiness check; a trace parent might merely call an authorization service; a joined table might control filtering while none of its values appear in output.

**Identify entities at the right stability.** A mutable table name is often a logical asset, while a snapshot identifier, file digest, table version, schema version, or partition interval identifies a more fixed entity.

Model logical identity and physical representations explicitly. Replicas, views, aliases, clones, shortcuts, cached results, and renamed assets can share relationships without becoming the same entity.

**Version what affects interpretation.** Record schema, data snapshot, code revision, query, configuration, parameters, environment, policy, glossary concept, and reference data versions when they can change the lineage answer.

Versioning every row may be infeasible. Define identity and retention by question: dataset versions for reproducibility, partition intervals for incidents, schema versions for compatibility, or bitemporal assertions for corrections.

**Separate activity definition from occurrence.** A job definition describes reusable intent. A version binds code and configuration. A run records an occurrence. A task attempt records retry behavior. A query or procedure invocation may be a nested activity.

A successful definition does not prove every run used the same inputs. Dynamic partition discovery, parameters, late binding, conditional branches, retries, and backfills require run-specific evidence.

**Represent agents and responsibility.** Record the service, user, team, organization, platform, owner, operator, and delegated actor relevant to assertion production or transformation execution.

Execution identity is not semantic accountability. A platform service account can run a job while a domain owns its outcome and another team owns the lineage connector.

**Make assertions first-class.** Give each assertion an identifier or stable key, relation type, endpoints, activity where applicable, producer, method, evidence reference, confidence, scope, granularity, valid time, observation time, ingestion time, status, version, and supersession.

First-class assertions can disagree. Preserve source-specific claims and reconcile them through policy instead of overwriting one edge with whichever collector arrived last.

**Distinguish assertion classes.** Design lineage comes from parsed code, query plans, transformation manifests, schemas, or declared workflow. Observed lineage comes from a run, query, transaction, or emitted event. Manual lineage comes from an accountable declaration. Imported lineage preserves an external source's claim. Reconstructed lineage is an inference from incomplete evidence.

Use these classes together. Design evidence covers paths before execution; runtime evidence captures dynamic inputs; manual evidence covers human and external work; reconstruction repairs gaps. Their assurance and update rules differ.

**Model usage and generation before derivation.** An activity can use inputs and generate outputs. Derivation additionally claims that an input influenced an output.

Some used entities affect only validation, authorization, routing, or branch selection. Preserve those roles as control or contextual dependence instead of claiming direct value derivation.

**Type transformations.** Useful types include identity copy, projection, expression, cast, lookup, join, union, filter, aggregate, window, sampling, masking, tokenization, encryption, decryption, imputation, enrichment, model inference, human classification, and unknown.

Type alone is insufficient. Record expression or code reference, parameters, information loss, determinism assumptions, state, lookup versions, and exceptions when needed.

**Represent field-level dependence carefully.** Direct field lineage links output fields to input fields. Dataset-wide influences such as filters, joins, ordering, limits, grouping, and window partitions may affect membership or values without mapping neatly to one output field.

Nested fields, arrays, wildcard expansion, ambiguous unqualified columns, user-defined functions, generated SQL, reflection, stored procedures, macros, and dynamic schemas limit static extraction. Preserve unknown and partial outcomes rather than inventing precision.

**Choose granularity from consequence.** Dataset lineage is relatively economical and supports broad discovery and impact. Field lineage supports schema change and sensitive-data analysis. Record lineage supports localized correction. Value lineage supports exact derivation but can be prohibitively large and sensitive.

Granularity can vary by path. Capture fine lineage only for critical fields or transformation classes, and state where queries fall back to coarser edges.

**Model subsets.** A run may read or write a partition, file range, topic offsets, time window, predicate-selected rows, or incremental watermark rather than an entire logical dataset.

Record subset descriptors in a stable queryable form. Treat predicates as potentially sensitive because they can reveal populations, incidents, or business rules.

**Handle batch execution.** Instrument orchestration for run identity and activity state; engines for actual inputs, outputs, queries, plans, and partitions; and storage for committed versions.

Do not mark output generated merely because a task returned success. Confirm the commit or publication boundary, distinguish partial output and retries, and relate superseded attempts.

**Handle streams and state.** Streaming lineage includes source topics and partitions, offset or sequence ranges, event-time windows, state stores, checkpoints, reference inputs, late-data policy, side outputs, and sink commits.

A continuously running job is not one timeless edge. Record definition versions and bounded observations or epochs so past outputs remain interpretable.

**Handle APIs and services.** Service lineage can relate request or message classes, endpoints, database queries, caches, external responses, and emitted events. Correlate trace or message context when policy permits.

Avoid persisting personal identifiers or payloads merely to join lineage. Use scoped opaque correlation and retention; sampled traces cannot prove complete lineage.

**Handle files and object stores.** Use canonical object identity, version ID or digest, path history, manifest membership, partition semantics, compression and serialization, writer activity, and atomic-publication boundary.

Paths can be reused. Overwrites, multipart uploads, rename emulation, lifecycle transitions, and compaction require versions rather than one permanent path node.

**Handle manual and desktop work.** Spreadsheets, notebooks, uploaded files, copied values, email attachments, and human decisions often sit on critical paths.

Provide accountable declaration, controlled import, checksum, template, review, and replacement mechanisms. Acknowledge what cannot be automatically observed; shadow work does not disappear because the catalog ignores it.

**Handle analytical metrics.** Link reports and metrics to semantic definitions, model or query versions, source fields, filters, reference data, time rules, and publication activities.

An edge to a table does not explain why a number exists. Bind technical lineage to the governed business concept and calculation specification without treating semantic mapping as data derivation.

**Handle features and models.** Record training, evaluation, validation, and serving datasets; feature definitions and materializations; sampling and labeling; code, parameters, environment, model artifacts, approvals, and deployment.

Separate data lineage from model behavior evidence. Knowing inputs does not prove fairness, validity, safety, or reproducibility if randomness, environment, external services, or missing versions remain.

**Capture near the evidence source.** Compilers and parsers observe design; query engines observe resolved plans; runtimes observe actual inputs; transaction logs observe mutations; orchestrators observe scheduling; storage observes committed objects; users can declare external or manual steps.

Prefer source-supported instrumentation with versioned contracts. Central scraping alone often loses dynamic semantics, while embedded capture can add latency or fail with the workload.

**Use events without trusting delivery as truth.** A lineage event identifies producer, event, activity, run, inputs, outputs, facets, schema, time, and sequence or source position where available.

Specify duplicates, out-of-order arrival, partial updates, terminal states, late facets, retries, deletion, correction, replay, and checkpoints. A collector acknowledgment does not prove a complete graph.

**Preserve raw evidence selectively.** Retain signed events, query identifiers, plans, manifests, logs, code digests, snapshots, attestations, and manual approvals according to risk and retention.

Raw SQL and plans may expose secrets, predicates, tenant names, or personal data. Store references or redacted forms when full evidence is disproportionate, and state the resulting assurance limit.

**Normalize through explicit mappings.** Map external asset, field, activity, agent, relation, time, and evidence models into a canonical profile while retaining source identifiers and source-native payload references.

Do not merge nodes from display names. Use resolvers grounded in namespace, system, tenant, environment, physical identity, version, and governed aliases; quarantine ambiguity.

**Reconcile sources.** A parser may declare three inputs, runtime instrumentation observe two, and storage reveal a fourth output. Preserve each claim, then apply policy to produce a decision view.

Classify agreement, refinement, expected omission, conflict, stale evidence, and unexplained gap. Reconciliation is evidence, not silent deduplication.

**Store a temporal attributed graph.** Graph databases are natural for traversal, but relational, document, search, and columnar stores can also support lineage. Choose by write rate, temporal history, query pattern, scale, consistency, access control, and recovery.

Maintain immutable or append-oriented assertion history plus materialized current views where practical. Rebuilding a current graph from evidence is safer than losing corrections in destructive updates.

**Define temporal semantics.** At minimum distinguish entity valid time, activity execution time, source assertion time, collector observation time, ingestion time, effective time, and correction time.

“As of” can mean what actually executed, what the source asserted then, or what the organization currently believes about that past execution. Bitemporal or multi-temporal queries must name which interpretation they provide.

**Define traversal semantics.** A query specifies start identities and versions, upstream or downstream direction, edge types, minimum assurance, time slice, environment, depth, stop classes, cycle behavior, redaction, and result limit.

Unlimited transitive traversal can explode or cross irrelevant control edges. Use typed path policies and return why each edge qualified.

**Treat cycles as meaningful.** Feedback, iterative models, recursive queries, streaming loops, shared state, and reprocessing can create legitimate cycles. Identity mistakes and stale aliases can create false ones.

Compute strongly connected components or bound traversal by version, run, epoch, time, and depth. A static asset graph may cycle even when each execution history is temporally ordered.

**Answer impact under uncertainty.** Downstream reachability produces candidates, not guaranteed impact. Filter by active versions, transformation type, field use, control dependence, environment, observed recency, consumer state, and confidence.

Return confirmed, possible, excluded, hidden, and unknown paths separately. Change approval must not interpret “no path found” as “safe” when coverage is incomplete.

**Answer origin and root cause carefully.** Upstream traversal can locate sources and transformations, but root cause additionally requires defect timing, behavior, version, execution, and counterfactual evidence.

Lineage narrows investigation. It does not prove the first upstream node caused an incident.

**Govern policy propagation.** Classification or obligation propagation requires a rule stating starting classifications, allowed edge types, direction, transformation exceptions, declassification authority, confidence, time, and conflict behavior.

Masking can reduce exposure without necessarily removing all sensitivity; aggregation can still leak; a control dependency can be privacy-relevant. Let accountable policy determine consequences rather than generic transitivity.

**Protect the graph.** Lineage can reveal restricted datasets, secret projects, security controls, personal relationships, commercial dependencies, code, vulnerabilities, and high-value targets.

Apply least privilege to nodes, edges, properties, evidence, traversal, export, and administration. Protect producer credentials and event integrity. Log queries and changes proportionately without turning exploration into employee surveillance.

**Design redaction semantics.** When a user cannot see an intermediate node, choose whether to hide the whole path, show an opaque boundary, return a summary edge, or disclose that results are incomplete.

Never splice visible endpoints into an apparent direct derivation without labeling redaction. Prevent count, timing, search, and traversal side channels where consequence warrants.

**Validate structure and meaning.** Structural checks cover endpoint existence, type compatibility, identifier format, time order, cardinality, status, source, signatures, duplicate keys, and forbidden self-relations.

Semantic validation uses known queries, code comparison, plan comparison, representative runs, field tests, owner review, and incident replay. Graph conformance cannot prove a captured edge reflects execution.

**Measure coverage explicitly.** Establish an inventory oracle by platform, domain, environment, job class, asset criticality, field classification, and time. Measure instrumented, emitting, accepted, current, and query-visible stages separately.

Coverage denominators change. Preserve snapshot, exclusions, unknowns, and confidence so apparent improvement does not result from shrinking the estate.

**Test negative and adversarial cases.** Exercise renamed assets, reused paths, dynamic SQL, wildcard fields, failed and retried runs, partial writes, late events, source restore, connector outage, unauthorized producer, forged edge, sensitive hidden node, cycle, backfill, stream restart, and correction.

Test whether decision consumers respond safely when lineage is unavailable, incomplete, conflicting, stale, or redacted.

**Operate lineage as a product.** Define availability, ingest lag, processing lag, freshness, accepted-event rate, quarantine, reconciliation gap, query latency, traversal limit, retention, recovery point, recovery time, support, and change objectives.

Prioritize critical decision paths. A massive graph that cannot answer a deployment or incident question reliably is not mature.

**Reconcile independently.** Compare observed runs with orchestrator history, query logs, storage commits, manifests, and asset inventories. Sample lineage against code and known transformations.

Ordinary capture and independent reconciliation should not share every failure mode. Otherwise both can omit the same path and agree falsely.

**Correct without rewriting history.** Mark an assertion disputed, superseded, or retracted; record reason, authority, time, affected decisions, replacement, and repair status.

Recompute materialized paths and propagated policy. Notify consumers that relied on the invalid edge, and preserve the prior view when required to explain earlier decisions.

**Recover from evidence.** Back up canonical identity, mappings, schemas, policies, assertions, evidence references, checkpoints, and consumer configuration. Test replay and index rebuild into isolation.

Recovery must prevent obsolete assertions, retired identifiers, and removed classifications from reappearing. Reconcile the rebuilt graph before promotion.

**Manage economics.** Costs include instrumentation, event volume, parsing, graph storage, history, indexes, traversal, fine granularity, evidence retention, access control, reconciliation, stewardship, and incident support.

Allocate fine-grained capture where it changes high-consequence decisions. Sampling can reduce cost for operational diagnosis but cannot support claims of complete data movement.

**Migrate deliberately.** Inventory producers, identifiers, mappings, assertion types, history, APIs, consumers, policies, access, dashboards, exports, and recovery. Define equivalence and loss between old and new models.

Dual-capture representative paths, compare graph answers rather than counts, migrate consumers by decision class, preserve redirects and historical evidence, then close old writes.

**Retire only after closure.** Stop capture only when authoritative scope is transferred or no longer required, consumers have migrated, retained evidence remains accessible, obligations are met, credentials and subscriptions are removed, caches and replicas expire, and recovery no longer resurrects active service.

Deleting a lineage UI is not retirement. Historical data, reports, incidents, models, and decisions may still need the old graph.

## Definitions and Notation

Let:

- `E` be lineage entities identified at declared logical, physical, version, subset, field, record, or value granularity;
- `A` be activities, including definitions, versions, runs, attempts, queries, transformations, publications, and manual actions;
- `N` be agents, including people, services, teams, platforms, and organizations;
- `R` be lineage assertions with typed endpoints, producer, method, evidence, time, confidence, and state;
- `K = {design, observed, declared, imported, reconstructed}` be assertion evidence classes;
- `Y` be relation types such as used, generated, derived, copied, filtered, joined, aggregated, controlled, attributed, associated, specialized, and alternate;
- `Z` be time dimensions, including execution, valid, assertion, observation, ingestion, effective, and correction time;
- `H` be evidence artifacts such as code digests, queries, plans, events, logs, manifests, storage versions, signatures, and approvals;
- `S` be assurance profiles for decision classes;
- `U` be consumers of lineage answers; and
- `D` be decision records that relied on lineage.

A qualified lineage assertion can be represented as:

`r = (id, relation, source, target, activity, producer, class, evidence, granularity, scope, valid_interval, observed_at, confidence, status, version)`.

`source`, `target`, or `activity` may be absent only when the relation profile permits it. An unqualified pair `(source, target)` is a projection for display, not the canonical assertion.

For activity `a`, let `Use(a, e, role)` mean `a` used entity `e` in a declared role, and `Gen(a, o, role)` mean `a` generated entity `o`. A derivation assertion is:

`Derive(o, e, a) => Use(a, e, input) and Gen(a, o, output) and Influence(e, o, a)`.

The reverse implication does not generally hold. Use plus generation does not prove influence.

Let `Active(r, t)` mean assertion `r` is accepted for valid time `t` and has not been retracted or superseded for the selected belief view. Let `Permitted(r, p)` mean policy profile `p` admits its relation, evidence class, confidence, scope, and redaction state.

The active decision graph is:

`G(t, p) = (E(t), {r in R | Active(r, t) and Permitted(r, p)})`.

Reachability is relative to that graph:

`Reach(x, y, t, p) = true` when a policy-admitted path from `x` to `y` exists in `G(t, p)`.

It proves accepted asserted reachability, not causal necessity or capture completeness.

For declared inventory `I_s` and accepted current assertions or assets `C_s` under scope `s`, coverage can be reported as:

`Coverage(s) = |C_s| / |I_s|`, when `I_s` is nonempty and the stage represented by `C_s` is named.

Report separate capture, acceptance, freshness, granularity, and query-visibility coverage rather than combining them into one score.

Let `Agree(r1, r2)` classify source assertions as exact agreement, compatible refinement, expected omission, temporal difference, semantic conflict, or unresolved. It is not Boolean when different sources observe different granularity.

A bounded impact candidate set for entity `e` is:

`Impact(e, t, p, d) = {x | Reach(e, x, t, p) within stopping rule d}`.

Consumers must combine it with coverage, current deployment, transformation behavior, and decision context.

A lineage capability is fit for assurance profile `s` only if:

`FitLineage(s) = Identity and Semantics and Evidence and Temporal and Coverage and Query and Protection and Integrity and Operations and Recovery and Closure`.

Each term is evaluated against explicit thresholds and accountable evidence. One passing graph query cannot compensate for missing authority, access control, or recovery.

## Mechanisms, Invariants, or Proof Structure

Use the following gates to design and review a lineage architecture.

**Outcome gate.** Name the decision, harm, accountable owner, subjects, required answer, latency, history, granularity, and failure behavior.

**Boundary gate.** Declare domains, systems, tenants, environments, asset classes, transformation classes, time intervals, inclusions, exclusions, and external boundaries.

**Identity gate.** Define logical and physical asset identity, versions, subsets, fields, aliases, copies, renames, clones, merges, splits, non-reuse, resolution, and retirement.

**Activity gate.** Separate definition, version, run, attempt, query, subactivity, schedule, commit, publication, failure, retry, cancellation, and backfill.

**Assertion gate.** Require typed endpoints, producer, class, method, evidence, granularity, time, confidence, status, version, and correction path.

**Semantic gate.** Distinguish use, generation, derivation, copy, revision, specialization, direct value dependence, control dependence, filter, join, aggregation, lookup, semantic mapping, and operational adjacency.

**Capture gate.** Select parsers, compilers, query plans, runtime hooks, events, logs, orchestration, storage commits, tracing, attestations, and manual declarations by source guarantee.

**Temporal gate.** Define execution, entity-valid, assertion-valid, observation, ingestion, effective, correction, and belief times plus ordering and interval rules.

**Normalization gate.** Map source identities and relation types explicitly, preserve raw identifiers and evidence, quarantine ambiguity, and version resolver behavior.

**Reconciliation gate.** Compare design, observed, imported, manual, inventory, and storage evidence; classify agreement, refinement, omission, conflict, age, and unknown.

**Validation gate.** Check structure, types, intervals, lifecycle, signatures, authenticity, code and plan correspondence, representative runs, known answers, coverage, and consumer fitness.

**Query gate.** Specify start version, direction, relation policy, time, environment, assurance, granularity, depth, cycles, stopping, redaction, ranking, pagination, and explanation.

**Propagation gate.** Define which policies or classifications traverse which edges, with direction, transformation exceptions, confidence, declassification, effective time, review, and correction.

**Protection gate.** Classify nodes, edges, code, queries, evidence, identities, graph shape, search and traversal telemetry; enforce least privilege, integrity, retention, and safe redaction.

**Operations gate.** Measure inventory, producer health, event acceptance, lag, quarantine, reconciliation, freshness, query service, cost, support, recovery, and decision outcomes.

**Correction gate.** Retract or supersede invalid assertions, retain explanation, recompute views and propagation, notify affected consumers, and repair decisions.

**Recovery gate.** Restore identity, mappings, assertions, evidence, policy, checkpoints, access, indexes, and consumer views; reconcile before activation.

**Closure gate.** End capture, subscriptions, credentials, APIs, indexes, caches, exports, support, and recovery only after consumers and obligations close while required history remains interpretable.

### Executable evidence: temporal lineage reachability integrity

This Python example validates a tiny accepted graph for endpoint existence, temporal intervals, assertion class counts, upstream roots, downstream impact candidates, and cycles.

<!-- bijux-verify: {"id":"temporal-lineage-reachability-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"assets=5\nactivities=4\nlineage_assertions=4\nobserved_assertions=3\ndeclared_assertions=1\norphan_assertions=0\ninvalid_intervals=0\nupstream_roots=1\ndownstream_impacts=4\ncycles=0\n","stderr":""}} -->
```python
from collections import defaultdict

assets = {
    "warehouse.orders@7",
    "warehouse.orders_clean@12",
    "warehouse.revenue_daily@5",
    "analytics.board_revenue@3",
    "features.customer_value@2",
}

activities = {
    "run:clean-orders:104",
    "run:aggregate-revenue:105",
    "design:publish-board-revenue:9",
    "run:build-customer-value:106",
}

assertions = [
    {
        "source": "warehouse.orders@7",
        "target": "warehouse.orders_clean@12",
        "activity": "run:clean-orders:104",
        "evidence": "observed",
        "valid_from": "2026-08-01",
        "valid_to": None,
    },
    {
        "source": "warehouse.orders_clean@12",
        "target": "warehouse.revenue_daily@5",
        "activity": "run:aggregate-revenue:105",
        "evidence": "observed",
        "valid_from": "2026-08-01",
        "valid_to": None,
    },
    {
        "source": "warehouse.revenue_daily@5",
        "target": "analytics.board_revenue@3",
        "activity": "design:publish-board-revenue:9",
        "evidence": "declared",
        "valid_from": "2026-08-15",
        "valid_to": None,
    },
    {
        "source": "warehouse.orders_clean@12",
        "target": "features.customer_value@2",
        "activity": "run:build-customer-value:106",
        "evidence": "observed",
        "valid_from": "2026-08-20",
        "valid_to": None,
    },
]

as_of = "2026-09-03"
active = [
    item
    for item in assertions
    if item["valid_from"] <= as_of
    and (item["valid_to"] is None or as_of < item["valid_to"])
]

orphan_assertions = sum(
    item["source"] not in assets
    or item["target"] not in assets
    or item["activity"] not in activities
    for item in active
)
invalid_intervals = sum(
    item["valid_to"] is not None and item["valid_from"] >= item["valid_to"]
    for item in assertions
)

forward = defaultdict(set)
reverse = defaultdict(set)
for item in active:
    forward[item["source"]].add(item["target"])
    reverse[item["target"]].add(item["source"])


def reachable(start, graph):
    seen = set()
    stack = list(graph[start])
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            stack.extend(graph[node] - seen)
    return seen


upstream = reachable("analytics.board_revenue@3", reverse)
upstream_roots = {node for node in upstream if not reverse[node]}
downstream = reachable("warehouse.orders@7", forward)
cycles = sum(node in reachable(node, forward) for node in assets)

print(f"assets={len(assets)}")
print(f"activities={len(activities)}")
print(f"lineage_assertions={len(active)}")
print(f"observed_assertions={sum(item['evidence'] == 'observed' for item in active)}")
print(f"declared_assertions={sum(item['evidence'] == 'declared' for item in active)}")
print(f"orphan_assertions={orphan_assertions}")
print(f"invalid_intervals={invalid_intervals}")
print(f"upstream_roots={len(upstream_roots)}")
print(f"downstream_impacts={len(downstream)}")
print(f"cycles={cycles}")
```

The expected output reports `assets=5`, `activities=4`, `lineage_assertions=4`, `observed_assertions=3`, `declared_assertions=1`, `orphan_assertions=0`, `invalid_intervals=0`, `upstream_roots=1`, `downstream_impacts=4`, and `cycles=0` on separate lines.

The evidence is deliberately narrow. Set membership does not prove globally persistent identity. A string labeled `observed` is not authenticated runtime evidence. The interval comparison assumes normalized ISO dates and one belief view. The traversal ignores edge types, fields, subsets, redaction, confidence, conflict, environments, and stopping rules. Reachable nodes are impact candidates, not proven consequences. Production assurance requires producer authentication, source-specific capture guarantees, independent inventory and reconciliation, temporal and semantic validation, access-control tests, adversarial events, representative decision queries, recovery exercises, and accountable acceptance.

## Alternatives and Trade-Offs

**Central lineage service.** A shared service can unify identity, traversal, policy, and operations. It concentrates credentials, sensitive graph knowledge, failure, cost, and governance and may impose one model on incompatible domains.

**Federated lineage products.** Domains retain context, authority, and source proximity. Cross-domain resolution, query semantics, access, evidence, and reliability can fragment without shared protocols and profiles.

**Graph store.** A graph store supports variable-depth traversal and relationship-rich models. High-ingest temporal history, fine-grained authorization, analytics, and deterministic rebuild may require additional stores and indexes.

**Relational store.** Tables provide transactions, constraints, temporal patterns, and familiar operations. Recursive traversal and heterogeneous relationship evolution can be harder to optimize and explain.

**Event-sourced assertions.** Append-only facts preserve source history and rebuildability. Materialization, correction, ordering, retention, and replay require disciplined operations.

**Mutable current graph.** A current graph is simple to query and cheaper to retain. Destructive updates lose belief history and make correction, audit, and migration harder; pair it with durable evidence.

**Static parsing.** Parsing SQL and code can provide lineage before execution and without runtime overhead. Dynamic queries, UDFs, reflection, branches, external calls, and engine rewrites create uncertainty.

**Runtime instrumentation.** Runtime evidence captures actual runs, dynamic inputs, and outcomes. It can add latency, fail with workloads, be sampled, miss manual paths, and become coupled to engine versions.

**Query-log reconstruction.** Existing logs reduce integration effort and can cover uninstrumented queries. Retention, redaction, failed queries, generated SQL, engine optimization, sampling, and external work limit proof.

**Manual declaration.** Accountable declarations cover spreadsheets, third parties, and conceptual paths. They become stale and subjective without ownership, evidence, review, expiration, and reconciliation.

**Dataset-level capture.** This is economical and useful for discovery and broad impact. It overstates field and subset dependence when consumers assume finer precision.

**Field-level capture.** This improves schema and classification decisions. Expressions, control dependencies, nested structures, wildcard expansion, and scale increase complexity.

**Record- or value-level capture.** Fine granularity supports targeted correction and exact explanation. Volume, sensitivity, retention, query cost, and instrumentation can be prohibitive.

**Precomputed transitive closure.** Materialized paths accelerate common impact and origin queries. Every correction can cause large recomputation, and path policy, time, redaction, and version changes multiply views.

**Traversal at query time.** Query-time traversal preserves flexible policies and current access. Latency, resource exhaustion, cycles, and denial-of-service risk require bounds and caching.

**Automatic classification propagation.** Automation improves consistency and reaction speed. Generic transitivity creates false positives or unsafe declassification unless transformation and policy semantics are explicit.

**Full raw evidence retention.** Rich evidence improves investigation and reprocessing. Queries, plans, payload identifiers, and predicates can expose secrets and personal data and incur substantial cost.

**Redacted summary lineage.** Summaries support broad discovery across boundaries. They reduce reproducibility and can accidentally imply a direct edge; disclose redaction and assurance limits.

**Open interchange model.** Shared standards reduce integration lock-in. Local concepts, identities, assurance, temporal semantics, and policy still need governed extensions and profiles.

**Vendor-native model.** Native capture can exploit engine details and ship faster. Cross-platform traversal and migration require explicit mappings and preservation of source semantics.

## Failure Modes and Misconceptions

1. **“An arrow means derivation.”** It may represent schedule order, use, copy, control, declaration, inference, or redaction.
2. **“Use plus generation proves influence.”** An activity can read an entity that does not affect a particular output.
3. **“The workflow graph is data lineage.”** Orchestration dependencies do not identify actual data inputs, fields, subsets, or committed outputs.
4. **“The job is the run.”** Definitions, versions, runs, attempts, queries, and publications have different identities.
5. **“A successful task generated correct output.”** Success may precede commit, hide partial output, or say nothing about correctness.
6. **“Static parsing is ground truth.”** Dynamic SQL, branches, UDFs, runtime discovery, and engine behavior can differ.
7. **“Runtime capture is complete.”** Instrumentation can fail, sample, omit external work, or lose events.
8. **“Query logs show everything.”** Retention, privileges, engine paths, external processing, and log loss create gaps.
9. **“Dataset input implies every output field depends on every input field.”** Granularity and control semantics do not permit that inference.
10. **“Field lineage covers row membership.”** Filters, joins, limits, and window choices can alter records without direct value mapping.
11. **“A path name is an asset identity.”** Paths can be reused, renamed, aliased, cloned, or overwritten.
12. **“Current lineage explains historical output.”** Code, schema, data, policy, and assertions change over time.
13. **“Acyclic graphs are always correct.”** Feedback and iterative systems can cycle; time and version can order occurrences.
14. **“Cycles are always legitimate.”** Identity collapse and stale aliases also create cycles.
15. **“No edge means no dependency.”** It may mean missing capture, rejected events, redaction, stale evidence, or coarse granularity.
16. **“Reachability proves impact.”** It identifies candidates under an edge policy, not deployed use or causal effect.
17. **“The furthest upstream node is the root cause.”** Cause requires defect and execution evidence, not topological position.
18. **“Lineage proves reproducibility.”** Missing data versions, randomness, environments, external services, and parameters can prevent replay.
19. **“Provenance makes data trustworthy.”** It supplies evidence for assessment; a trustworthy record can describe a bad process.
20. **“Classification should traverse every arrow.”** Relation type, transformation, policy, time, and exceptions matter.
21. **“Masking ends sensitivity.”** Reidentification, joins, aggregates, control dependence, and policy can preserve risk.
22. **“Hiding a node permits joining its neighbors.”** An unlabeled shortcut misrepresents derivation and may leak graph shape.
23. **“More nodes mean better coverage.”** Duplicate, stale, low-value, or unqueryable metadata can inflate counts.
24. **“One coverage percentage is enough.”** Inventory, capture, acceptance, freshness, granularity, and query visibility differ.
25. **“A valid graph is an accurate graph.”** Structural conformance does not establish observation, authenticity, or meaning.
26. **“Signing an assertion makes it true.”** A signature establishes origin and integrity under a trust model, not correctness.
27. **“The catalog is the lineage authority.”** It aggregates claims whose authority remains with sources and accountable actors.
28. **“Deleting old edges cleans the graph.”** It can destroy the explanation of historical data and prior decisions.

## Worked Examples

### Example 1

A warehouse deployment changes `orders.customer_id`. Dataset-level traversal finds twelve downstream assets, but only five have current field lineage. The release report labels two as confirmed field impacts, three as possible dataset impacts, seven as paths through stale or coarse assertions, and four estate segments as unknown. The owner does not interpret the absence of additional paths as safety.

### Example 2

A scheduled transformation reads a holiday calendar and sales facts, then emits daily revenue. Sales fields directly contribute values; the calendar controls grouping and inclusion. The graph records direct expression dependence separately from lookup and control dependence, allowing financial explanation without claiming every calendar value appears in the output.

### Example 3

A streaming job version consumes three topic partitions, a customer-state store, and reference-data version 18. A checkpoint epoch identifies the offset ranges and sink commit. When late events trigger reprocessing, a new bounded activity derives a replacement output version rather than editing the old run's lineage.

### Example 4

An orchestrator declares two upstream tasks, but runtime evidence shows one branch did not execute. Design assertions remain available for pre-deployment impact; observed assertions describe the run. The decision view does not overwrite design with observation or claim the unexecuted branch contributed data.

### Example 5

A notebook exports a CSV, an analyst edits two classifications in a spreadsheet, and a controlled upload produces a regulatory report. Automatic capture covers notebook execution and file digests. A reviewed manual activity records the human transformation, approval, versions, and limitations, closing a critical gap without pretending cell-level observation.

### Example 6

A service trace shows an API calling authorization, pricing, and database services. Only the database result and pricing response influence the emitted order event; authorization controls whether emission occurs. Trace identifiers correlate the occurrence, while separate qualified lineage assertions describe data and control dependencies.

### Example 7

A sensitive field is tokenized, aggregated, and joined with a small population. Propagation policy does not blindly remove classification after tokenization or blindly copy the most restrictive label forever. It evaluates transformation, joinability, group size, purpose, policy version, and review evidence and records the resulting decision separately from lineage.

### Example 8

A user can see a dashboard and a public aggregate but not the restricted intermediate dataset. The query response shows an opaque protected transformation boundary and marks the path incomplete. It does not draw a direct arrow from the visible source to the dashboard or reveal hidden node counts through pagination.

### Example 9

Two collectors disagree: static SQL parsing reports three source tables while runtime plan capture reports two plus a materialized cache. Reconciliation classifies two exact agreements, one design-only conditional source, and one observed physical refinement. Both source assertions remain attributable; the consumer view depends on its question and time.

### Example 10

During lineage-platform migration, teams crosswalk qualified asset identifiers and assertion types, dual-capture critical paths, compare answers for incident and deployment questions, replay history into isolation, and reconcile classifications. The old service becomes read-only only after consumers activate the new API; its historical evidence remains resolvable after active capture retires.

## Cross-Program Connections

- **Data engineering:** compilers, runtimes, orchestration, schemas, partitions, offsets, checkpoints, queries, storage commits, and reconciliation produce much technical lineage evidence.
- **API and service engineering:** resource identity, representations, pagination, temporal query parameters, events, idempotency, authorization, rate limits, errors, versioning, and deprecation shape lineage interfaces.
- **Platform engineering:** paved instrumentation, identity resolution, metadata events, graph services, policy, secrets, observability, tenancy, reliability, recovery, and cost make lineage operable at scale.
- **Database engineering:** catalogs, query plans, transaction logs, temporal tables, snapshots, views, stored procedures, isolation, and physical storage determine what can be observed.
- **Distributed systems:** partial failure, retries, order, duplicates, clocks, partitions, convergence, and replay limit claims about complete and current lineage.
- **Software architecture:** call graphs, build graphs, module dependencies, configuration, and deployment topology resemble lineage but require typed semantic translation.
- **Machine learning engineering:** feature derivation, training sets, labels, model artifacts, evaluation, serving, and monitoring require lineage plus behavior and governance evidence.
- **Security engineering:** authenticated producers, signed attestations, least privilege, integrity, tamper evidence, graph inference, redaction, incident response, and supply-chain provenance constrain trust.
- **Privacy engineering:** purpose, minimization, sensitive predicates, linkability, propagation, deletion, retention, access, and cross-border flows shape capture and query.
- **Reliability engineering:** service objectives, missing signals, backpressure, quarantine, reconciliation, replay, restoration, degraded modes, and exercises make lineage dependable.
- **Knowledge representation:** typed graphs, ontologies, identity, inference, constraints, provenance, and query semantics support interoperability while creating reasoning risks.
- **Organizational design:** data owners, producers, platform operators, stewards, risk owners, consumers, auditors, and external parties hold different authority and obligations.

## References

1. W3C, [“PROV-DM: The PROV Data Model”](https://www.w3.org/TR/prov-dm/), 2013. Retrieved 2026-09-03.
2. W3C, [“PROV-O: The PROV Ontology”](https://www.w3.org/TR/prov-o/), 2013. Retrieved 2026-09-03.
3. W3C, [“Constraints of the PROV Data Model”](https://www.w3.org/TR/prov-constraints/), 2013. Retrieved 2026-09-03.
4. W3C, [“PROV-AQ: Provenance Access and Query”](https://www.w3.org/TR/prov-aq/), 2013. Retrieved 2026-09-03.
5. OpenLineage, [“Object Model”](https://openlineage.io/docs/spec/object-model/), current specification documentation. Retrieved 2026-09-03.
6. OpenLineage, [“The Run Cycle”](https://openlineage.io/docs/spec/run-cycle/), current specification documentation. Retrieved 2026-09-03.
7. OpenLineage, [“Lineage Dataset Facet”](https://openlineage.io/docs/spec/facets/dataset-facets/lineage/), current specification documentation. Retrieved 2026-09-03.
8. Apache Software Foundation, [“Apache Atlas”](https://atlas.apache.org/), current project and feature documentation. Retrieved 2026-09-03.
9. OpenTelemetry, [“Traces”](https://opentelemetry.io/docs/concepts/signals/traces/), current documentation. Retrieved 2026-09-03.
10. SLSA, [“Provenance,” Specification 1.2](https://slsa.dev/spec/v1.2/provenance), current approved specification. Retrieved 2026-09-03.

## Exercises

### Exercise 1

Design lineage for a batch pipeline that reads orders, customers, exchange rates, and a holiday calendar; writes partitioned revenue facts; publishes a dashboard; retries failed tasks; and supports backfills. Specify identities, activities, assertions, granularity, times, evidence, validation, impact queries, and correction.

### Exercise 2

A privacy team asks where a sensitive customer field has traveled. Available evidence includes current schemas, sampled service traces, warehouse query logs, declared spreadsheet exports, and dataset-level orchestration. Design an answer that distinguishes confirmed, possible, unknown, hidden, and historical paths without overstating completeness.

### Exercise 3

Static parsing, runtime events, and storage commits disagree about a critical model-training dataset. Design reconciliation, assurance, escalation, consumer communication, and repair while preserving source-specific evidence.

### Exercise 4

A lineage platform contains 80 million nodes, claims 97 percent coverage, and returns most two-hop queries in 300 milliseconds. Design a scorecard that tests decision fitness, inventory, capture, acceptance, freshness, granularity, correctness, protection, redaction, operations, recovery, cost, and outcomes.

### Exercise 5

Migrate from a vendor-native mutable lineage graph to a federated event-sourced architecture serving deployment, incident, privacy, audit, and model-governance consumers. Design crosswalks, dual capture, history transfer, query comparison, policy propagation, rollback, activation, and retirement.

## Answers to the Exercises

### Answer 1

Identify logical and physical dataset versions, fields, partitions, dashboard version, code and schema revisions, exchange-rate and calendar versions, job definition and version, each run, task attempt, query, commit, and publication. Record use, generation, direct expression, join, filter, lookup, control, aggregation, and publication assertions with producer, observed or design class, evidence, valid and execution times, subset, status, and correction path. A retry is a new attempt under the run; a backfill is a bounded new activity whose outputs supersede or coexist with prior versions under explicit policy.

Capture design evidence from reviewed transformation code, run evidence from the engine and orchestrator, and committed versions from storage. Reconcile expected inputs with each execution and confirm publication. Field lineage covers revenue expressions while dataset-wide control assertions cover calendar and predicates. Validate endpoint identity, intervals, failed attempts, partition ranges, code-plan correspondence, late events, duplicate events, and known example rows. Impact queries name time, version, edge policy, field fallback, confidence, and coverage. Corrections retract or supersede assertions, recompute views, identify decisions that used them, and preserve the earlier belief view.

### Answer 2

Start with a declared inventory of systems, environments, periods, field identities, replicas, files, services, reports, models, exports, and external boundaries. Current schema annotations establish locations, not movement. Query logs can confirm represented warehouse executions under their retention and logging scope. Sampled traces confirm selected request occurrences but cannot prove every path. Reviewed spreadsheet declarations provide attributable manual claims. Orchestration supplies coarse candidates, not field propagation.

Return confirmed observed paths with activity and evidence; possible paths where dataset or design lineage is coarser; unknown areas with missing instrumentation or expired history; historical paths by version and time; and protected boundaries using opaque markers or authorized summaries. State inventories, dates, sampling, retention, rejected events, redaction behavior, and confidence. Apply policy propagation separately, considering masking, aggregation, joins, purpose, and control dependence. Escalate unowned critical gaps, preserve evidence proportionately, and do not claim erasure, legal compliance, or absence from “no edge found.”

### Answer 3

Preserve all three assertions with native identifiers, producers, versions, methods, timestamps, evidence references, and assurance. Resolve asset, activity, run, and subset identities before comparing. Classify exact agreements, physical refinements, conditional design paths, expected lifecycle differences, stale observations, missing events, uncommitted outputs, and genuine conflicts. A runtime input without a storage commit may belong to a failed attempt; a committed object without runtime evidence may indicate connector loss or an external writer.

Quarantine unsafe composite answers and notify model, data, platform, privacy, and risk owners. Use engine plans, signed or authenticated run events, orchestrator state, storage versions, code digests, training manifests, and independent inventory to investigate. Apply decision-specific policy: block reproducibility or deployment claims when required versions are unresolved while allowing a clearly labeled discovery view. Repair producer capture and identity mappings, supersede invalid assertions, rebuild materialized paths and propagated decisions, retest known training cases, record consumer activation, and preserve the conflict and resolution history.

### Answer 4

Node count measures scale, not usefulness; 97 percent is uninterpretable without inventory and stage; two-hop latency omits path policy and correctness. Define critical decisions and representative upstream, downstream, field, temporal, redacted, cyclic, and cross-domain queries. Segment inventory by platform, domain, environment, asset criticality, transformation class, field sensitivity, and time. Separately measure inventory quality, producer instrumentation, event emission, acceptance, quarantine, currentness, granularity, query visibility, and authenticated evidence.

Sample graph answers against code, plans, runs, commits, manifests, owners, and known incidents. Measure false and missing edges, unresolved identity, design-observed conflict, interval validity, stale paths, hidden-boundary correctness, access denials, side-channel tests, integrity, change propagation, correction lead time, affected-consumer repair, availability, ingest and processing lag, traversal latency by profile, resource limits, recovery point and time, replay reconciliation, storage and compute cost, connector and steward effort, incident time, prevented unsafe changes, and user decision success. Publish denominators, exclusions, confidence, trends, and corrective owners rather than one maturity score.

### Answer 5

Inventory every producer, connector, source type, identifier namespace, asset and activity type, assertion class, temporal field, correction state, evidence reference, history interval, access rule, propagation policy, API, export, query, cache, consumer, service objective, backup, and obligation. Define source-to-target crosswalks with explicit exact, refined, lossy, unsupported, and ambiguous mappings. Preserve vendor-native identifiers and payload references; do not merge nodes from display names. Establish append-oriented assertions and reproducible current views.

Dual-capture representative critical paths and compare answers for deployment impact, incident origin, sensitive-field travel, audit history, and model reproducibility under identical time, version, edge, assurance, and access profiles. Test conflicts, retries, late events, cycles, hidden nodes, corrections, replay, and rollback. Recompute classification propagation under the new policy rather than copying current labels blindly. Migrate consumers by risk, record activation, keep the old graph read-only, and reconcile results. Retire old writes only after producers and consumers close, then remove credentials, subscriptions, exports, caches, and recovery that could reactivate service while retaining resolvable historical evidence for required periods.
