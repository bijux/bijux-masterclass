---
module_id: DARCH-028
program: Data Architecture Engineering
level: 1
module_number: 28
title: Cross-Domain Dependencies
status: complete
last_verified: 2026-09-03
---

# Cross-Domain Dependencies

## One-Page Review

### Governing question

How can an organization make cross-domain data dependencies visible, bounded, testable, resilient, and jointly governed so domains preserve autonomy without hiding semantic coupling, propagating failures, circular authority, or enterprise-wide concentration risk?

### Essential definitions

- A **cross-domain dependency** exists when one domain's decisions, products, controls, or obligations rely on assertions or service behavior governed by another domain.
- A **dependency edge** is the governed relationship from a consuming product or domain to a providing product or domain for a declared purpose.
- **Semantic dependency** is reliance on another domain's meaning, identity, classification, rule, or authoritative assertion.
- **Operational dependency** is reliance on another product's availability, freshness, latency, recovery, support, or change behavior.
- **Control dependency** is reliance on another role or service to enforce access, privacy, security, records, quality, or evidence obligations.
- **Criticality** is the consequence-sensitive importance of a dependency to decisions, services, safety, law, finance, operations, or recovery.
- **Blast radius** is the set of products, domains, consumers, or decisions that can be affected by a dependency failure or change.
- A **strongly connected component** is a maximal set of graph nodes in which each node is reachable from every other; nontrivial components expose cycles.
- **Bulkhead** is a boundary that limits resource exhaustion, corrupt data, policy failure, or operational disruption from crossing dependency paths.
- **Dependency evidence** links declared edges to contracts, lineage, runtime observations, tests, incidents, changes, owners, and lifecycle state.

### Central model, mechanism, or theorem

Represent the dependency graph as `G = (V,E)`, where products or domains are vertices and each directed edge is:

`e = (consumer, provider, purpose, assertions, interface, contract, service, criticality, failure_modes, controls, evidence, ownership, lifecycle)`

For failed or changed node `v`, its potential blast radius is the set of reachable dependents under the selected edge semantics. Cycles are not automatically wrong, but they require explicit authority, convergence, initialization, recovery, and change rules. A credible architecture combines design-time declarations, runtime lineage, operational telemetry, contract tests, incident evidence, and accountable review; no single graph source proves the whole dependency system.

### Critical invariants

- Every material edge names a provider, consumer, purpose, assertions, interface, contract, criticality, owners, and effective interval.
- Semantic authority flows from explicit domain decisions; downstream popularity, storage, or repeated derivation does not reverse it silently.
- Operational promises account for dependency topology, correlated failures, shared platforms, caching, degraded modes, and human controls.
- Critical paths have detection, containment, fallback, recovery, correction, communication, and escalation proportionate to consequence.
- Cycles identify feedback separately from source authority and define convergence, delay, termination, replay, and failure behavior.
- Cross-domain changes analyze direct and transitive consumer impact, including unknown use, policy constraints, and historical obligations.
- Shared reference, identity, platform, catalog, and policy services are treated as concentration risks with capacity and continuity plans.
- Consumers validate fitness at their boundary; providers preserve contract evidence and do not inherit every downstream decision.
- Dependency telemetry and lineage are protected, current, versioned, and reconciled with declared contracts and observed use.
- Retirement removes or transfers edges, copies, access, exceptions, alerts, support, and historical correction obligations deliberately.

### Common failures

Common failures are drawing only system-to-system arrows; equating technical lineage with semantic authority; registering direct dependencies but ignoring transitive impact; assuming domain autonomy means no shared commitments; allowing downstream products to redefine source facts; hiding cycles through batch delay; multiplying availability percentages without topology; treating a shared identity service as risk-free infrastructure; using cached data without age or limitation; letting platform failures appear as unrelated domain incidents; coupling every domain through a central canonical model; changing a reference code without affected-use analysis; leaving anonymous consumers outside notification; and deleting a retired producer while historical reports remain dependent.

### Compact example

Revenue depends on Commerce orders, Fulfillment events, Finance exchange rates, and Party legal-entity reference data. Fraud consumes Revenue output and feeds risk decisions back into Commerce. The organization records predicate-level authority and product versions on each edge, separates fraud feedback from order truth, identifies a cycle, and defines delayed bounded feedback. It maps shared platform and identity dependencies, sets critical service and correction paths, tests late and corrupt inputs, provides last-known-good rates with visible age, and routes cross-domain incidents through one coordinator while each owner retains scoped decisions.

### Connections

[DARCH-022](022-domain-boundaries.md) scopes domains, [DARCH-025](025-source-aligned-aggregate-and-consumer-aligned-data.md) defines product alignments, [DARCH-026](026-data-products-and-service-expectations.md) defines service behavior, and [DARCH-027](027-producer-and-consumer-contracts.md) governs each exchange. This module analyzes their graph before [DARCH-029](../ROADMAP.md) develops discoverability and [DARCH-030](../ROADMAP.md) evaluates domain cohesion.

## Governing Question

Domains are not isolated islands. Customer identity influences orders, claims, payments, support, fraud, and reporting. Reference codes, platforms, policy engines, and catalogs cross many boundaries. A local change can therefore become an enterprise incident even when each individual interface appears well designed.

The architectural challenge is to preserve meaningful autonomy while governing the edges that create shared consequences. That requires more than a lineage screenshot. Architects must identify semantic reliance, operational coupling, control delegation, concentration, cycles, transitive impact, and lifecycle obligations with evidence and ownership.

## Why This Matters

Hidden dependencies make change unsafe. A producer removes an apparently unused field, a reference hierarchy is reorganized, or an identity rule changes. Direct consumers may be known, while downstream reports, models, exports, and controls fail days later.

Unbounded dependencies also create systemic risk. A catalog, identity resolver, or shared canonical aggregate becomes critical to every domain without appropriate capacity, recovery, or change governance. Local SLOs remain green until the shared component fails and the real blast radius appears.

[ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) defines architecture descriptions around stakeholders, concerns, viewpoints, views, model kinds, and correspondences. Cross-domain dependency analysis needs several views because semantic, runtime, organizational, protection, and lifecycle relationships are not interchangeable.

NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) frames trustworthy secure-system engineering across system life cycles. It supports treating dependency, assurance, protection, and lifecycle decisions as engineering concerns rather than after-the-fact diagrams.

W3C [PROV-O](https://www.w3.org/TR/prov-o/) provides concepts for entities, activities, agents, and derivation. W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) supports relationships among datasets, services, distributions, and catalogs. These enable interoperable descriptions, but local governance determines authority, completeness, criticality, and operating commitments.

The [OpenAPI Specification 3.1.1](https://spec.openapis.org/oas/v3.1.1.html) and [AsyncAPI Specification 3.0.0](https://www.asyncapi.com/docs/reference/specification/v3.0.0) support machine-readable synchronous and message-driven interfaces. They describe important technical edges without proving end-to-end semantic or operational fitness.

Google's SRE chapter [Addressing Cascading Failures](https://sre.google/sre-book/addressing-cascading-failures/) examines overload and failure propagation in distributed systems. Zhamak Dehghani's [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html) articulates domain ownership, data as a product, self-service infrastructure, and federated governance. Together they illuminate the tension between local autonomy and systemic dependency.

## Prerequisites and Retrieval

You should understand domains, bounded contexts, data products, contracts, service objectives, schemas, lineage, provenance, distributed systems, graphs, risk, privacy, security, incident response, recovery, and lifecycle.

Retrieve dependency, provider, consumer, semantic authority, interface, contract, upstream, downstream, direct, transitive, runtime lineage, design lineage, critical path, blast radius, concentration, shared service, cycle, feedback, strongly connected component, fallback, degradation, bulkhead, circuit breaker, replay, correction, migration, and retirement.

As a retrieval test, inspect “Revenue depends on Customer.” Ask which Customer assertions; from which product and version; for what calculation and period; under which authority; through which interface; with which service and protection needs; what happens if input is late, missing, conflicting, or corrected; who owns the edge; and which downstream decisions inherit impact. A domain name and arrow are not enough.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish semantic, operational, control, organizational, platform, provider, and lifecycle dependencies;
2. model products and domains as a directed multigraph with typed, versioned, owned dependency edges;
3. reconcile declared contracts, design lineage, runtime lineage, telemetry, access, tests, and incident evidence;
4. analyze direct and transitive dependencies, critical paths, blast radii, concentration, cut points, and cycles;
5. preserve predicate-level authority and separate source truth from feedback, reconciliation, aggregation, and inference;
6. design service budgets, degradation, caching, bulkheads, retries, replay, correction, and recovery across boundaries;
7. govern cross-domain change, compatibility, notice, migration, exceptions, disputes, and unknown consumers;
8. apply privacy, security, purpose, retention, licensing, jurisdiction, and evidence constraints across graphs;
9. measure dependency health through coverage, conformance, incidents, propagation, recovery, capacity, and stale edges;
10. manage dependency ownership through reorganization, provider change, consolidation, deprecation, retirement, and archive.

## Core Exposition

**Start with a directed multigraph.** Use nodes for governed products or domains and directed edges from consumer to provider, because a consumer relies on a provider. A pair can have multiple edges for different assertions, interfaces, purposes, or versions.

Direction conventions vary, so state yours. A graph that reverses arrows accidentally reverses blast-radius reasoning. Preserve edge type and effective time rather than flattening every relationship into “depends on.”

**Type each dependency.** Semantic dependencies rely on another domain's definitions or assertions. Operational dependencies rely on delivery, freshness, availability, or support. Control dependencies rely on identity, policy, encryption, deletion, monitoring, or review. Organizational dependencies rely on another team's decision or manual action.

Provider and platform dependencies can combine several types. Classify them separately so a technical fallback does not appear to replace semantic authority or legal review.

**Model products before systems.** A system can publish several products with different owners, contracts, and consumers. A product can span several systems. System-level arrows are useful for deployment and recovery but too coarse for semantic decisions.

Link product nodes to systems, teams, contracts, controls, and interfaces through separate views. This preserves correspondence without claiming the views are identical.

**Define the edge contract.** For each edge record consumer, provider, product and version, purpose, assertions, interface, semantic contract, service need, criticality, protection, failure modes, fallback, evidence, owners, escalation, and lifecycle.

This record complements the producer-consumer contract. The graph adds topology and transitive consequence; the bilateral contract adds reciprocal obligations. Both should share stable identifiers.

**Preserve predicate-level authority.** A Party domain may govern legal identity, while Commerce governs shipping contact and Risk governs risk classification. A downstream Customer aggregate must not imply one source owns every predicate.

Record authority on assertions or meaningful groups. When downstream rules choose among conflicts, that choice is a new governed derivation. Popularity or central storage does not transform it into source truth.

**Separate source, adoption, and feedback.** A consumer may enrich or correct local use and report evidence upstream. The provider decides whether to adopt the change under its authority. Feeding a downstream derived value back into the source without labeling can create circular truth.

Define feedback messages, evidence, review, acceptance, rejection, and effective time. Keep source assertions and proposed corrections distinguishable until adoption.

**Inventory declared dependencies.** Contracts, catalogs, architecture models, schemas, repositories, orchestration definitions, dashboards, and ownership records reveal intended edges. Each source has limitations and can become stale.

Normalize identities and versions. “Customer table,” `cust_360`, and a catalog product may describe different objects or aliases. Do not merge them solely by name.

**Observe runtime dependencies.** Query logs, lineage collectors, message subscriptions, API telemetry, access records, network flows, and execution traces show observed use. Runtime observation can find unknown consumers and obsolete declarations.

Observation is incomplete. Sampling, encryption, dynamic queries, manual exports, spreadsheets, provider systems, and disabled telemetry create blind spots. Record coverage, confidence, retention, and access.

**Reconcile declared and observed graphs.** A declared but unobserved edge may be seasonal, recovery-only, misconfigured, or obsolete. An observed but undeclared edge may be exploratory, unauthorized, or missing governance.

Route discrepancies to owners. Do not delete declared edges from absence of recent traffic alone, and do not legitimize observed use merely by cataloging it.

**Add human and policy edges.** A pipeline may wait for a steward approval, legal interpretation, manual file, provider contact, or records hold. These dependencies often dominate recovery but do not appear in technical lineage.

Record decision deadlines, deputies, capacity, escalation, and evidence. Automating a workflow can reduce delay, but it cannot manufacture authority or judgment.

**Classify criticality.** Consider decision consequence, affected people, safety, legal and regulatory duties, financial exposure, operational disruption, customer harm, recovery difficulty, alternatives, volume, duration, and reversibility.

Criticality belongs to the edge and use, not only the provider. The same Address product may be low consequence for marketing segmentation and high consequence for emergency service dispatch.

**Find transitive dependencies.** Direct catalogs answer “what do I call?” Transitive analysis answers “what can affect me?” Traverse product, platform, identity, control, and provider edges under declared types and time.

Bound traversal by purpose. Including every possible relationship creates unusable blast radii; excluding shared services understates risk. Preserve the query criteria with results.

**Calculate blast radius.** Starting from a changed or failed node, traverse reverse consumer edges to identify reachable dependents. Add consumer registrations, decisions, populations, jurisdictions, and criticality to rank consequence.

Reachability is potential impact, not proof of actual harm. Version, feature use, cache state, fallback, timing, and product logic determine realized impact. Confirm with evidence.

**Identify concentration.** High fan-out providers, shared identity services, reference data, catalogs, policy engines, exchange rates, and common aggregates can be systemic nodes. High fan-in products can concentrate many failure modes.

Dependency count alone is insufficient. Weight by critical consumers, alternatives, correlation, recovery, and change frequency. A low-degree bridge between critical subgraphs can matter more than a popular optional feed.

**Identify cut points and cut sets.** A cut point is a node whose loss disconnects important paths in the simplified graph. Real architectures can require multiple simultaneous losses, represented by cut sets or fault trees.

Use graph findings to ask engineering questions, not declare risk automatically. Validate topology, redundancy independence, human operations, shared providers, and common configuration.

**Detect cycles.** Use strongly connected components to locate mutually reachable nodes. Self-dependencies and components with multiple nodes warrant review. Cycles may arise through feedback, mastered identity, shared aggregates, model scores, or policy decisions.

Do not hide cycles with asynchronous queues. Delay changes timing, not semantic dependence. Document which information is authoritative, which is feedback, and how initialization, convergence, correction, replay, and failure work.

**Break unsafe semantic cycles.** Choose one authority for each assertion, make feedback proposals rather than truth, introduce effective intervals, or separate observed facts from derived decisions. Preserve provenance across adoption.

When a cycle is intentional, define convergence criteria and maximum iterations. Ensure repeated processing is idempotent or otherwise controlled. Detect oscillation and stale feedback.

**Budget end-to-end service.** Consumer expectations depend on sources, transformations, platforms, controls, and support. Allocate latency and freshness budgets across the critical path. Model availability using actual topology and correlation.

Do not multiply component percentages blindly. Active redundancy, shared failure domains, caches, conditional paths, and correlated providers alter results. Measure at the consumer boundary and retain diagnostics per edge.

**Design cached behavior.** Caches and materialization decouple read availability and performance from upstream service. They add freshness, invalidation, correction, storage, and protection obligations.

Declare last-known-good age, missing scope, update status, expiry, and permitted decisions. Some consumers can use stale reference codes temporarily; others must stop when rates or risk lists are outdated.

**Design bulkheads.** Separate compute, queues, credentials, storage, quotas, and release paths where shared exhaustion or corruption could spread. Domain autonomy needs practical failure boundaries.

Bulkheads cost capacity and coordination. Apply them to high-consequence or high-correlation paths and test whether they actually isolate provider, tenant, region, or data-quality failure.

**Control retries.** Retries can convert a local failure into shared overload. Define timeouts, backoff, jitter, budgets, concurrency, idempotency, and circuit-breaking per interface.

Data replay has similar risks. A mass backfill can saturate sources, platforms, quality services, and consumers. Schedule, throttle, partition, observe, and communicate it.

**Design graceful degradation.** Provide partial products, delayed partitions, prior versions, cached values, or manual alternatives only when consumers can interpret them safely. Label state and limitations in-band where possible.

High-consequence decisions may fail closed. Define who authorizes override, what evidence is captured, and how later reconciliation occurs. A fallback that silently changes meaning is a new incident.

**Propagate quality signals.** Providers publish relevant quality and limitation evidence. Consumers validate at their boundary and add use-specific measures. Aggregates expose input coverage and reconciliation, not only output checks.

Avoid a single inherited quality score. Transformations can repair, mask, amplify, or create defects. Trace findings to affected assertions and product versions.

**Propagate corrections.** A provider identifies changed keys, periods, assertions, and versions. Consumers decide replay, restatement, disclosure, or preservation under their contracts and obligations.

Keep correction status on edges. A source fix does not prove every downstream cache, aggregate, report, model, export, and decision is repaired. End-to-end closure needs consumer evidence.

**Coordinate incidents.** Cross-domain events need one coordinating incident role with a shared timeline and consequence view. Each domain owner retains authority for its product, risk, and corrections.

Messages state affected edges, versions, periods, populations, current guidance, fallback, next update, and evidence limitations. Protect sensitive incident and dependency information.

**Govern cross-domain change.** Change analysis begins at the product contract and expands through direct registrations, runtime observations, transitive graph queries, shared controls, and historical uses. Classify semantic, interface, quality, service, policy, and lifecycle effects.

Notify direct owners with actionable detail and let them propagate under explicit obligations. For critical changes, coordinate end-to-end tests and migrations rather than assuming notice cascades successfully.

**Handle unknown consumers.** Monitor access and runtime use, publish deprecations broadly, offer registration value, and search repositories and reports. Unknown use is evidence of uncertainty, not a reason for permanent immobility.

Use consequence-based extension, adapters, or controlled termination. Record decisions and residual risk. Unauthorized use may require containment rather than support.

**Govern shared semantics.** Cross-domain concepts need stable identifiers, scoped definitions, mappings, owners, stewards, versioning, and conflict paths. Interoperability does not require one universal model.

Use anti-corruption mappings where domains legitimately differ. Make loss, uncertainty, and context explicit. Central canonical models can become semantic bottlenecks and concentration points if every domain must change together.

**Govern reference dependencies.** Codes, currencies, countries, legal entities, calendars, units, and hierarchies affect many products. Reference-data changes need effective time, mappings, consumer impact, distribution, compatibility, and historical preservation.

Do not overwrite prior code meaning. Consumers need transition rules for facts arriving late or recomputed under older versions.

**Govern identity dependencies.** Shared identity resolution can simplify joins and rights handling while creating high blast radius. Record source evidence, match rules, confidence, merges, splits, effective time, correction, and appeals.

Consumers should not treat a probabilistic link as an observed source fact. Protect linkability and access. Test erroneous merge and split propagation.

**Map platform dependencies.** Products rely on storage, compute, orchestration, identity, secrets, catalogs, policy, observability, CI/CD, networking, and support. A self-service platform is still an upstream provider.

Separate platform service failure from domain data failure for diagnosis, but coordinate consumer impact. Publish responsibilities, objectives, quotas, recovery, change, and escalation.

**Map control dependencies.** Access may require identity, entitlement, purpose approval, policy evaluation, and audit. Deletion may require domain selection, records authority, platform execution, backup expiry, and verification.

Control chains need end-to-end evidence. A successful policy-engine call does not prove a request had lawful purpose or every copy was deleted.

**Map third parties.** External data and services add contract, licensing, provenance, jurisdiction, security, privacy, correction, availability, audit, subcontractor, and exit dependencies.

A provider SLA or certification does not remove internal accountability. Model alternatives, export, transition, retained copies, and historical reproducibility before critical adoption.

**Use architecture views.** Maintain semantic authority, product dependency, runtime lineage, service critical path, organizational responsibility, protection flow, deployment, and lifecycle views. Connect them through stable product, contract, role, and version identifiers.

No single view is complete. State viewpoint, stakeholders, questions, scope, date, evidence, and limitations. Contradictions among views are findings to resolve.

**Keep graphs current.** Update design declarations through delivery workflows, ingest runtime evidence, expire old observations, and review high-risk edges. Assign ownership for graph quality.

Track last verified time, confidence, source, and version. Stale dependency data can be more dangerous than acknowledged uncertainty because it directs change and incident response incorrectly.

**Test dependencies.** Contract tests validate interface and selected semantics. Integration tests validate composition. Failure-injection and recovery exercises validate timeouts, caches, bulkheads, replay, communication, and closure.

Include missing, late, duplicate, corrupt, semantically changed, denied, and restored inputs. Protect production and test data. Label which environments and cases evidence covers.

**Measure dependency health.** Track critical-edge coverage, unowned edges, stale contracts, unknown consumers, compatibility tests, service attainment, repeated failures, incident propagation, correction closure, cycles, concentration, recovery exercises, and retirement gaps.

Avoid rewarding graph size or lineage percentage alone. Sample whether edges express correct semantics and whether teams can act on them. High discovered dependency count can reflect improved visibility.

**Review architecture trade-offs.** Direct dependencies preserve domain meaning but can increase consumer fan-out. Aggregation can simplify consumers but concentrates rules and failure. Events decouple timing but add ordering and replay complexity. Shared services reduce duplication but increase systemic importance.

Choose deliberately from value, semantic authority, consequence, change rate, service, protection, cost, and operating capability. Architecture style does not eliminate dependency; it changes its form.

**Manage reorganization.** Transfer products, contracts, edges, incidents, exceptions, controls, consumers, evidence, and support to successor roles. Verify capacity and acceptance.

Organizational charts and runtime graphs change at different speeds. Maintain interim authority and escalation so dependencies do not become orphaned during transition.

**Retire edges and nodes.** Retirement checks direct and transitive consumers, runtime use, caches, copies, reports, models, exports, retention, holds, incidents, corrections, credentials, alerts, and historical support.

Provide migration and final versions. Remove obsolete routing after evidence of closure. Preserve contract and provenance history needed to explain past decisions.

**Treat dependency governance as continuous.** Every new product, interface, consumer, provider, control, or change alters the graph. Integrate declaration, testing, observation, incident learning, and lifecycle into normal delivery.

The final test is whether the organization can predict and bound the consequences of a provider change or failure, identify who must act, preserve semantic authority, recover and correct downstream state, and prove closure. If not, the graph is decoration.

## Definitions and Notation

Let `G = (V,E)` be a directed multigraph with edge direction `consumer → provider`. Each edge is `e = (c,p,u,a,i,k,s,r,f,b,z,o,t)`, representing consumer, provider, purpose, assertions, interface, contract, service, criticality, failure modes, fallback, evidence, ownership, and effective time.

For node `v`, direct providers are `Out(v)` under this direction, and direct consumers are `In(v)`. Potential blast radius for provider `v` is the reverse-reachable set `BR(v) = {u ∈ V | u reaches v}` excluding or including `v` by declared convention.

A strongly connected component `C ⊆ V` is maximal such that every pair of nodes in `C` is mutually reachable. Components with more than one node, or self-loops, identify cycles requiring review; they do not prove a defect.

Let `Declared(e,t)` and `Observed(e,t)` represent design and runtime evidence. Four useful states are corroborated, declared-only, observed-only, and absent. Observation coverage and retention bound conclusions.

Let `Critical(e,U,t)` evaluate edge consequence for use `U` at time `t`. Criticality is contextual; provider popularity alone is not a sufficient measure.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for every material cross-domain dependency.

**1. Identity gate.** Name provider, consumer, products, versions, owners, stewards, contacts, purpose, and effective interval.

**2. Semantic gate.** Define assertions, predicate authority, keys, grain, time, mappings, derivations, feedback, uncertainty, and limitations.

**3. Contract gate.** Link interfaces, schemas, quality, service, protection, change, correction, support, evidence, and lifecycle obligations.

**4. Discovery gate.** Reconcile architecture declarations, catalogs, repositories, lineage, telemetry, access, tests, incidents, and unknown use.

**5. Topology gate.** Analyze direct and transitive edges, critical paths, blast radius, fan-in, fan-out, cut points, concentration, cycles, and correlation.

**6. Resilience gate.** Design timeouts, retries, idempotency, caches, bulkheads, degradation, replay, recovery, reconciliation, and capacity.

**7. Protection gate.** Apply purpose, access, privacy, security, records, licensing, jurisdiction, provider, evidence, incident, and deletion controls.

**8. Change gate.** Govern compatibility, impact, notice, testing, migration, exceptions, emergency action, corrections, and version transitions.

**9. Operation gate.** Monitor edges, route alerts, coordinate incidents, communicate, correct downstream state, audit, exercise, and learn.

**10. Lifecycle gate.** Review freshness, transfer ownership, manage providers, deprecate, retire, revoke, archive, and verify closure.

The executable example computes the reverse-reachable potential blast radius of a failed provider in a small declared dependency graph.

<!-- bijux-verify: {"id":"cross-domain-blast-radius","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"nodes=6\nedges=6\nprovider=party\nblast_radius=fraud,fulfillment,orders,revenue\naffected=4\n","stderr":""}} -->
```python
edges = (
    ("orders", "party"),
    ("fulfillment", "orders"),
    ("revenue", "orders"),
    ("revenue", "rates"),
    ("fraud", "revenue"),
    ("fraud", "party"),
)

nodes = sorted({node for edge in edges for node in edge})
provider = "party"
affected = set()
frontier = [provider]
while frontier:
    current = frontier.pop()
    for consumer, dependency in edges:
        if dependency == current and consumer not in affected:
            affected.add(consumer)
            frontier.append(consumer)

affected.discard(provider)
print(f"nodes={len(nodes)}")
print(f"edges={len(edges)}")
print(f"provider={provider}")
print("blast_radius=" + ",".join(sorted(affected)))
print(f"affected={len(affected)}")
```

The checker establishes reverse reachability only for the six declared edges. It does not prove the graph is complete, edges are active, every reachable consumer is materially affected, cycles are absent, runtime behavior matches design, fallbacks work, controls are effective, or production risk is acceptable. Those require reconciled declarations and observations, version and feature analysis, contract tests, telemetry, exercises, incident evidence, protection review, and accountable decisions.

## Alternatives and Trade-Offs

**Direct consumption versus shared aggregate.** Direct products preserve source context and distribute failure paths; shared aggregates simplify consumers but concentrate semantics and service. Select by reuse, authority, consequence, and operating capacity.

**Synchronous versus asynchronous dependency.** Synchronous calls simplify current response semantics but couple availability and latency. Asynchronous exchange decouples time while adding lag, ordering, replay, duplication, and convergence concerns.

**Central canonical model versus domain mappings.** A canonical model simplifies common exchange but can become a change bottleneck. Mappings preserve bounded contexts but require explicit loss and version management.

**Live query versus materialized copy.** Live access reduces staleness and copies but couples runtime and load. Materialization improves isolation and history while adding correction, storage, protection, and lifecycle duties.

**Shared platform versus domain infrastructure.** Shared platforms reduce duplicated capability and improve policy consistency but increase concentration. Domain infrastructure isolates some failures at greater cost and fragmentation risk.

**Automatic discovery versus declared registration.** Runtime discovery finds unknown use but has blind spots and weak intent. Declarations carry purpose and accountability but become stale. Reconcile both.

**Fail-open versus fail-closed.** Continuing with stale or partial data preserves availability but can harm decisions. Stopping protects correctness but disrupts service. Define consequence-specific degraded modes and authority.

**Detailed graph versus minimized disclosure.** Rich dependency evidence improves change and incident response but can expose sensitive relationships and vulnerabilities. Provide controlled views, redaction, retention, and need-to-know access.

## Failure Modes and Misconceptions

1. **A lineage graph is the dependency architecture.** It may omit semantics, people, controls, contracts, criticality, and lifecycle.
2. **System arrows identify product responsibility.** Systems and products have different ownership and boundaries.
3. **Domain autonomy means no dependencies.** Autonomy requires explicit, governed interfaces and obligations.
4. **Downstream popularity establishes truth.** Source authority does not reverse through adoption count.
5. **Asynchrony removes coupling.** It changes temporal coupling and adds replay, lag, and convergence behavior.
6. **A cycle hidden by a queue is gone.** Semantic feedback remains even when delayed.
7. **All cycles are defects.** Feedback can be legitimate when authority and convergence are explicit.
8. **Component availabilities can simply be multiplied.** Correlation, topology, caching, routing, and optional paths matter.
9. **Caching is a free fallback.** It creates freshness, invalidation, correction, storage, and protection obligations.
10. **Retries always improve resilience.** They can amplify overload and duplicate effects.
11. **Provider failures are outside product accountability.** Consumers still need continuity, communication, correction, and evidence.
12. **A shared service is low risk because it is standard.** Broad adoption increases concentration and blast radius.
13. **Observed traffic legitimizes a consumer.** Purpose, access, contract, and ownership still require review.
14. **No observed traffic proves an edge is obsolete.** Seasonal, recovery, manual, or hidden use may remain.
15. **A source correction closes downstream impact.** Every derived state and decision needs analysis.
16. **Reorganization transfers dependencies automatically.** Successor authority, capacity, knowledge, and acceptance are required.
17. **Deleting a node removes its obligations.** Copies, history, retention, incidents, corrections, and reports can survive.

## Worked Examples

### Example 1

Revenue joins Orders and Rates. Its graph records distinct semantic and service edges, rate-version and calendar rules, reconciliation, stale-rate fallback, and downstream report impact rather than one generic upstream arrow.

### Example 2

Fraud scores feed Commerce decisions, which later influence fraud features. The cycle separates observed order facts from model feedback, delays adoption, versions features, and defines convergence and replay.

### Example 3

A Party identity merge propagates to Claims, Billing, Support, and models. Blast-radius analysis finds registered and observed consumers, while correction preserves original-decision evidence and validates splits downstream.

### Example 4

A shared policy engine fails. Domain products remain technically available but access cannot be evaluated safely. Critical products fail closed; approved low-risk paths use cached policy with visible expiry and later audit.

### Example 5

A backfill retries aggressively after source throttling and saturates the platform. Retry budgets, jitter, quotas, bulkheads, staged replay, and consumer windows bound the next operation.

### Example 6

A country code hierarchy changes without schema drift. Reference-data dependency records expose affected aggregations, local mappings, effective time, migration, historical preservation, and cross-domain notice.

### Example 7

Runtime lineage finds an unknown marketing consumer of protected Claims data. Observation triggers purpose and access review rather than automatic support; containment, registration, or termination follows accountable decision.

### Example 8

A product serves cached inventory during an upstream outage. The interface marks age and missing warehouses. Planning continues, while fulfillment allocation stops because its consequence-specific policy forbids stale availability.

### Example 9

A cloud region and nominal backup share one identity dependency. Architecture views reveal correlated failure, prompting independent recovery credentials, exercised procedures, and a revised critical path.

### Example 10

A legacy Customer aggregate retires. The team migrates direct and transitive consumers, removes schedules and credentials, transfers archive and correction support, and preserves lineage and contract history for old decisions.

## Cross-Program Connections

- **Systems engineering:** architecture views, interfaces, requirements allocation, dependency analysis, fault propagation, verification, configuration, and lifecycle shape the discipline.
- **Distributed systems:** partial failure, timeouts, retries, queues, idempotency, consensus, caching, overload, and recovery determine runtime edges.
- **Data engineering:** orchestration, lineage, tests, replay, backfill, quality, schemas, and observability provide evidence and mechanisms.
- **Platform engineering:** shared identity, catalogs, policy, compute, storage, delivery, telemetry, and support create both leverage and concentration.
- **API and service engineering:** interface contracts, versioning, discovery, compatibility, reliability, rate limits, and deprecation govern technical edges.
- **Security and privacy:** data flows, trust boundaries, access, purpose, providers, incidents, retention, and evidence constrain dependency graphs.
- **Graph theory:** reachability, strongly connected components, centrality, cuts, paths, and condensation graphs support structural analysis.
- **Organizational design:** ownership, team boundaries, cognitive load, coordination, escalation, federation, and succession determine whether edges are operable.

## References

1. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>
2. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>
3. W3C, *PROV-O: The PROV Ontology*, W3C Recommendation, 2013. <https://www.w3.org/TR/prov-o/>
4. W3C, *Data Catalog Vocabulary (DCAT)—Version 3*, W3C Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>
5. OpenAPI Initiative, *OpenAPI Specification 3.1.1*, 2024. <https://spec.openapis.org/oas/v3.1.1.html>
6. AsyncAPI Initiative, *AsyncAPI Specification 3.0.0*, 2023. <https://www.asyncapi.com/docs/reference/specification/v3.0.0>
7. Beyer, B., Jones, C., Petoff, J., and Murphy, N. R., eds., *Site Reliability Engineering: Addressing Cascading Failures*, Google, 2016. <https://sre.google/sre-book/addressing-cascading-failures/>
8. Dehghani, Z., *Data Mesh Principles and Logical Architecture*, 2020. <https://martinfowler.com/articles/data-mesh-principles.html>

## Exercises

### Exercise 1

Build a typed dependency graph for Orders, Party, Fulfillment, Revenue, Fraud, Rates, identity, policy, and platform products. Define each edge and analyze direct, transitive, critical, and control dependencies.

### Exercise 2

Analyze a cycle in which a fraud score changes Commerce treatment and the resulting behavior retrains the score. Define authority, feedback, delay, convergence, bias, replay, correction, and governance.

### Exercise 3

Design a resilience strategy for a shared identity product used by ten critical domains. Include concentration, service, cache, bulkhead, degradation, correction, recovery, protection, capacity, and exercises.

### Exercise 4

Plan impact analysis and migration for a cross-domain reference-code change with unknown consumers, historical reports, external exports, and three jurisdictions.

### Exercise 5

Create a dependency-assurance program combining declared architecture, contracts, runtime lineage, access evidence, tests, telemetry, incidents, audits, metrics, transfer, and retirement.

## Answers to the Exercises

### Answer 1

Create product nodes rather than one node per system. Direct consumer-to-provider edges include Orders→Party for legal identity, Fulfillment→Orders for accepted order and address claims, Revenue→Orders and Revenue→Rates for recognition, Fraud→Orders and Fraud→Party for features, and each product→identity, policy, and platform for controls and operation. Each edge records purpose, assertions, version, interface, contract, service need, criticality, failure modes, fallback, protection, evidence, owners, escalation, and effective time.

Traverse outward for providers and reverse edges for blast radius. Mark identity, policy, and platform as shared concentration nodes; Revenue as high fan-in; Orders and Party as high-consequence semantic providers. Separate runtime, semantic, control, and organizational views. Reconcile declared contracts with observed lineage and access. Test late Rates, Party correction, identity outage, policy denial, and platform saturation. Rank potential impact by decisions and critical populations, not edge count alone.

### Answer 2

Commerce remains authoritative for orders, offers, and observed customer responses. Fraud owns its score and risk recommendation, not the underlying identity or transaction facts. A score can influence a treatment decision through a versioned interface, while resulting observations return as labeled outcomes. Do not write scores into source attributes that later masquerade as independent facts.

Record model, feature, policy, and source versions plus event and decision time. Use delayed outcome windows, bounded iterations, stable initialization, idempotent processing, and explicit termination. Monitor oscillation, distribution shift, selective-label and intervention bias, subgroup effects where appropriate, and feedback amplification. Corrections identify affected features, scores, treatments, and outcomes; replay distinguishes counterfactual recomputation from decisions actually made. Model and business owners, privacy, security, risk, and domain authorities review material changes and appeals.

### Answer 3

Inventory each domain use at predicate and decision level, then assign criticality. Define identity contract, matching confidence, merge and split, version, correction, service, protection, support, and escalation. Analyze common infrastructure, regions, credentials, source feeds, human review, and provider correlations. Provide last-known-good identity only for decisions whose policy tolerates visible age; require stop or manual authority elsewhere.

Use partitioned capacity, tenant and workload quotas, isolated replay, independent recovery credentials, staged releases, and regional or product bulkheads where justified. Prevent retry storms and mass correction overload. Protect linkability and evidence through least privilege and controlled views. Exercise erroneous merge, split, source outage, region loss, policy outage, corrupt backup, telemetry loss, steward absence, and mass replay. Validate downstream correction and consumer decisions, not only identity service restoration. Fund the node according to enterprise concentration.

### Answer 4

Define old and new code sets, meanings, mappings, hierarchy, authority, effective dates, jurisdictions, late-fact behavior, and historical policy. Identify direct contracts, declared registrations, runtime queries, lineage, reports, repositories, access, exports, and seasonal uses. Traverse transitive dependencies and classify affected aggregations, policies, models, interfaces, and external agreements. Unknown use remains explicit uncertainty.

Publish versioned reference products and mapping evidence. Provide parallel support, fixtures, compatibility results, notice, migration dates, and owner contacts. Preserve old codes for historical facts; do not overwrite semantics. Each jurisdiction reviews local legal, records, reporting, and language implications. Track critical acknowledgements and observed migration. Bound extensions with risk, owner, expiry, and controls. Validate downstream totals and reports, communicate external changes, archive contract history, revoke obsolete access, and close only after direct and transitive evidence is reconciled.

### Answer 5

Require stable identifiers for products, contracts, interfaces, roles, versions, and edges. Delivery workflows publish declared dependency records and contract tests. Catalogs expose authorized semantic, service, protection, and lifecycle views. Runtime lineage, query and API telemetry, subscriptions, access records, orchestration, and incidents supply observed evidence with coverage and retention labels. Reconcile declared-only and observed-only edges through owner queues.

Analyze critical paths, reverse-reachable blast radii, fan-in, fan-out, concentration, cut points, strongly connected components, shared controls, providers, and human dependencies. Sample semantic authority and version accuracy, exercise late, missing, corrupt, denied, overloaded, recovered, and corrected inputs, and validate consumers. Metrics cover critical-edge coverage, stale evidence, unknown use, tests, incidents, propagation, correction closure, cycles, recovery, and retirement gaps. Review high-risk edges periodically, transfer assignments explicitly, and remove nodes only after consumers, copies, access, alerts, retention, historical evidence, and successor duties close.
