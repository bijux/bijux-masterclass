---
module_id: DARCH-022
program: Data Architecture Engineering
level: 1
module_number: 22
title: Domain Boundaries
status: complete
last_verified: 2026-09-03
---

# Domain Boundaries

## One-Page Review

### Governing question

Where should data-domain boundaries be drawn, joined, split, protected, and evolved so that meanings and invariants remain coherent, teams can change and operate safely, and cross-domain dependence is explicit rather than hidden in shared storage or organization charts?

### Essential definitions

- A **domain boundary** is an explicit semantic, authority, change, and operational perimeter within which a model and its governing decisions remain coherent.
- A **bounded context** is the boundary inside which one domain model and ubiquitous language apply consistently.
- A **fracture plane** is evidence of a natural separation, such as distinct language, change cadence, authority, risk, scaling, team, or business outcome.
- A **cohesion force** is a reason concepts belong together, such as one invariant, lifecycle, authority, decision, or tightly coupled change.
- A **coupling force** is a dependency across boundaries, including semantic, temporal, transactional, availability, schema, organizational, security, or operational coupling.
- A **context relationship** states how two bounded contexts collaborate, depend, translate, conform, share, publish, or remain separate.
- A **cross-boundary invariant** is a rule involving facts owned by more than one domain; it requires an explicit consistency, authority, and failure model.
- A **trust boundary** is a perimeter across which identity, authentication, authorization, validation, classification, or threat assumptions change.
- **Boundary fitness** is the observed ability of a boundary and owning team to deliver safe change, coherent decisions, reliable products, and manageable interactions.
- A **boundary transition** is a versioned split, merge, transfer, extraction, or retirement that migrates ownership, contracts, histories, consumers, and obligations.

### Central model, mechanism, or theorem

Represent a candidate boundary as:

`B = (language, concepts, invariants, decisions, authority, change, products, team, dependencies, protection, operations, lifecycle)`

Evaluate it with an evidence vector:

`E(B) = (semantic_cohesion, change_locality, authority_clarity, team_fit, dependency_cost, failure_isolation, protection_fit, consumer_value)`

No scalar formula chooses the boundary. A defensible boundary localizes most semantic and operational change while preserving the smallest necessary cross-boundary contracts. Any proposed split must explain how shared invariants work after separation; any proposed merge must explain why increased cognitive load and blast radius are justified.

### Critical invariants

- A boundary is named by durable domain responsibility, never by a temporary project, team number, vendor, database, or delivery sequence.
- In-scope and out-of-scope concepts, decisions, data products, events, authorities, and protections are explicit.
- One model and vocabulary are internally coherent; terms that differ legitimately across contexts are translated at the boundary.
- Business invariants have one decision authority and a declared consistency model, even when evidence arrives from many domains.
- Data ownership, write authority, source assertions, derived products, replicas, and caches remain distinguishable.
- Cross-boundary contracts name exact semantics, versions, time, identity, quality, security, privacy, service behavior, and failure handling.
- Shared databases, schemas, libraries, transactions, files, dashboards, and teams do not silently bypass boundary contracts.
- Boundary placement considers cognitive load, flow of change, availability, latency, scale, protection, residency, and recovery—not only conceptual elegance.
- Split, merge, and transfer preserve provenance, historical interpretation, consumer migration, incident ownership, and lawful retention or deletion.
- Fitness is measured continuously through change and operations; a published diagram does not freeze the organization or domain model.

### Common failures

Common failures are naming a domain after an application or table; drawing one box per department; splitting every noun into a service; keeping every shared invariant in a distributed transaction; declaring a monolith boundary-free; forcing one enterprise vocabulary; sharing a database as an undocumented integration API; using events without authority or version semantics; selecting boundaries only for independent deployment; assigning several accountable owners; placing all regulated data in one giant domain; creating cross-domain aggregates that rewrite source truth; ignoring batch, analytics, archive, and recovery consumers; moving code without ownership; and treating the first context map as permanent architecture.

### Compact example

An order application owns cart, pricing, inventory reservation, payment, shipment, and customer tables in one database transaction. Language and change analysis identifies Ordering, Pricing, Inventory, Payments, Fulfillment, and Party contexts. The boundary transition keeps Order acceptance as Ordering's decision; uses quoted-price, reservation, authorization, and shipment contracts; adopts compensating workflows where business policy permits; leaves atomic stock decrement inside Inventory; preserves old-table history and identifiers; and measures coordination, latency, failure, reconciliation, and consumer outcomes before physical extraction.

### Connections

[DARCH-014](014-entities-relationships-and-business-keys.md) supplies identity, [DARCH-018](018-temporal-and-historical-modeling.md) temporal scope, [DARCH-020](020-reconciling-conflicting-models-across-systems.md) mapping, and [DARCH-021](021-business-capabilities-and-data-domains.md) capability/domain discovery. This module defines boundary evidence before [DARCH-023](../ROADMAP.md) assigns accountability and [DARCH-026](../ROADMAP.md) specifies product service expectations.

## Governing Question

A domain boundary determines where one language is authoritative, which changes can be made locally, which facts can be written, and which failures propagate. It is simultaneously a semantic, organizational, contractual, protection, and operational decision. Treating it as only a service or database boundary leaves the hardest questions unanswered.

Good boundaries are discovered through tension. Concepts need to remain together because of invariants and coordinated decisions; they need to separate because meanings, authorities, change cadences, risks, or team capacities differ. Architecture makes those forces visible and chooses a boundary whose tradeoffs are explicit and measurable.

## Why This Matters

Poor boundaries tax every change. A shared model requires unrelated consumers to coordinate. A distributed invariant causes inconsistent decisions. A platform team becomes the owner of domain ambiguity. Data copies lose provenance, and incidents cross unclear support lines.

Eric Evans's [DDD Reference](https://www.domainlanguage.com/ddd/reference/) defines bounded context and context-map relationships such as shared kernel, customer/supplier, conformist, anticorruption layer, open host service, published language, and separate ways. These patterns treat boundaries as agreements among models and teams, not merely namespace conventions.

Melvin Conway's original [“How Do Committees Invent?”](https://melconway.com/Home/pdf/committees.pdf) argues that system design reflects the communication structures of design organizations. Team and communication design therefore affect whether intended boundaries remain real. An architecture diagram cannot overcome a reward structure that requires constant unowned coordination.

[Team Topologies key concepts](https://teamtopologies.com/key-concepts) connect stream-aligned, platform, enabling, and complicated-subsystem teams with cognitive load and explicit interaction modes. A boundary that no stable team can understand, build, run, and support is not operationally viable.

[ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) distinguishes architecture from its description and structures descriptions around stakeholders, concerns, viewpoints, and model kinds. Boundary evidence should therefore present several concern-specific views rather than treating one box-and-arrow drawing as the architecture itself.

## Prerequisites and Retrieval

You should understand capabilities, domains, bounded contexts, entities, invariants, transactions, distributed systems, data products, model reconciliation, versioning, security, privacy, team design, and migration.

Retrieve bounded context, ubiquitous language, context map, fracture plane, seam, cohesion, coupling, invariant, consistency, autonomy, authority, upstream, downstream, shared kernel, customer/supplier, conformist, anticorruption layer, open host service, published language, separate ways, cognitive load, stream-aligned, platform, trust boundary, blast radius, data gravity, strangler, coexistence, split, merge, transfer, and retirement.

As a retrieval test, inspect a proposal to create a Customer domain service from a `customers` table. Ask which Customer concept applies; which assertions and decisions belong inside; which invariants require other tables; who owns identity, contact, account, consent, and credit; which consumers bypass the service; what consistency and failure behavior are acceptable; which protections change; and which team can operate it. Without those answers, the proposal is a table extraction, not a domain boundary.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish semantic, authority, organizational, deployment, storage, transactional, trust, and product boundaries;
2. discover fracture planes through language, invariants, decisions, change, risk, scale, and team evidence;
3. identify forces that require concepts to remain together and forces that justify separation;
4. model context relationships and select shared-kernel, translation, published-language, conformist, or separate-way strategies;
5. assign consistency and authority for invariants that span domains without hiding distributed failure;
6. expose cross-boundary data through versioned product, event, API, batch, query, and metadata contracts;
7. evaluate cognitive load, communication paths, flow, operability, protection, and recovery alongside conceptual coherence;
8. find and govern boundary bypasses through shared storage, code, pipelines, dashboards, files, and emergency procedures;
9. migrate boundaries incrementally with coexistence, reconciliation, rollback, provenance, and consumer coordination;
10. use quantitative and qualitative fitness evidence to revisit boundaries without organizational churn for its own sake.

## Core Exposition

**Name the entity of interest.** State whether the boundary concerns a business domain, bounded context, team responsibility, service, data product, database, trust zone, or deployment. These views can align, but assuming alignment creates category mistakes.

A bounded context is a model boundary. A service is an interface and deployment unit. A data domain is an accountability and semantic boundary. A trust boundary marks changed security assumptions. Use distinct identifiers and record their relationships.

**Begin from decisions and invariants.** Ask which decisions must be internally coherent and which rules must hold atomically or eventually. Concepts participating in one high-consequence invariant often need close ownership, even if technical distribution remains possible.

For an inventory reservation, identify available stock, allocation policy, expiration, oversell tolerance, authority, and correction. “Orders and Inventory share data” is too weak. The boundary decision depends on who can promise stock and what happens during partitions.

**Listen for linguistic seams.** Terms that change definition across workflows indicate possible contexts. `Account` can mean ledger account, user login, subscription relationship, or customer organization. One term with multiple meanings should not force one global entity.

Conversely, different labels may name one shared concept. Validate with definitions, rules, examples, counterexamples, and expert decisions. A glossary can document relationships; it cannot abolish contextual language.

**Trace change locality.** Inspect commits, schema evolution, incidents, tickets, releases, meetings, and consumer migrations. Concepts that change together repeatedly may belong together. Changes that require broad coordination expose boundary leakage or a genuinely shared invariant.

Do not optimize for zero cross-boundary change. Business capabilities interact. Seek explicit, stable dependence and localizable consequences. A boundary is successful when most changes within it do not surprise unrelated domains.

**Map authority at assertion level.** A domain may own Order acceptance but not quoted Price, Payment authorization, or Party identity. It records references and snapshots needed for its decisions while preserving upstream authority and provenance.

Specify subject, predicate, context, jurisdiction, valid time, recorded time, use, correction, and dispute authority. “Customer domain owns customer data” is too broad to resolve conflicts or incidents.

**Separate write authority from custody.** A warehouse may store copies from every domain but own few source assertions. A domain can own semantics while a managed platform stores the bytes. A consumer-aligned product owns its derivation, not the underlying facts.

Document system of entry, authoritative reference, operational executor, custodian, processor, steward, product owner, and consumer. Physical control can create operational duties without transferring semantic authority.

**Inventory coupling dimensions.** Structural coupling shares schema or code. Semantic coupling shares definitions. Temporal coupling requires actions at the same time. Transactional coupling requires atomic commit. Availability coupling makes one service depend on another being live. Organizational coupling requires teams to coordinate. Protection coupling shares trust or compliance obligations.

Different remedies address different dimensions. An asynchronous event reduces temporal availability coupling but can preserve semantic and schema coupling. A shared library reduces duplication but couples releases. Measure rather than assuming a technology decouples everything.

**Challenge cross-boundary transactions.** Some invariants are truly indivisible; many encode a workflow that can tolerate reservation, authorization, compensation, reconciliation, or delayed confirmation. Write the business consequence of inconsistency before choosing consensus or eventual behavior.

If a strong invariant spans candidate domains and cannot tolerate partial state, consider keeping the decision within one authority boundary. Distributed transactions add coordination and failure modes; sagas add intermediate states and compensation. Neither is automatically superior.

**Keep aggregates bounded.** An aggregate protects invariants under one consistency boundary. Do not create an enterprise-sized aggregate to avoid reasoning about workflow. Do not split an aggregate only to achieve one service per noun.

References across boundaries should use stable identities and explicit snapshots or versions when historical decisions need reproduction. Avoid navigable object graphs that silently load and mutate another domain's state.

**Choose context relationships deliberately.** A shared kernel is a small mutually owned model requiring close coordination. Customer/supplier establishes downstream needs and upstream commitments. Conformist accepts an upstream model. An anticorruption layer translates and protects local semantics. An open host service plus published language supports many consumers. Separate ways avoids integration whose value is lower than its cost.

Record relationship direction, negotiation power, contract, cadence, support, translation, escalation, and exit. The pattern name alone does not create the behavior.

**Use published contracts, not shared internals.** Cross boundaries through APIs, events, files, query products, views, or controlled replication whose semantics and lifecycle are explicit. The format matters less than whether ownership, version, time, identity, quality, protection, and failure behavior are defined.

A database table shared by several teams is an undocumented interface unless governed as a product. Direct access can be appropriate for performance or transition, but grant read/write scopes explicitly and prohibit consumers from inferring private columns as stable contracts.

**Treat events as assertions.** A domain event communicates something the owning context asserts occurred. It needs identity, meaning, occurrence and recording times, schema version, authority, ordering scope, correction, privacy, retention, and delivery semantics.

Publishing every database change does not produce a domain contract. Change data capture is a transport and evidence source. Translate it into stable domain assertions or expose it as a source-aligned product with limitations.

**Design analytical boundaries too.** Operational boundaries are not automatically appropriate for every analytical product. Cross-domain aggregates can form consumer-aligned or aggregate domains when they own a coherent derived concept, consumer outcome, and lifecycle.

They must retain lineage and source authority. A Revenue product may own the definition and calculation of recognized revenue while Billing and Payments retain invoice and settlement assertions. The aggregate boundary does not authorize upstream correction.

**Do not equate data location with domain.** Data may be physically centralized for cost, compliance, or platform operations while remaining semantically federated. Data may be distributed across regions while one domain owns the contract. Separate location, custody, processing, semantic authority, and access.

The OMG [Business Architecture Core Metamodel](https://www.omg.org/spec/BACM/1.0/) relates capabilities, outcomes, business objects, information items, performers, and resources without collapsing ability into implementation. Those relationships can help test whether a proposed boundary follows durable responsibility or current technology.

**Expose catalog boundaries.** A catalog should show domain, owner, product, dataset, distribution, service, version, contract, access, quality, and lineage. W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) distinguishes datasets, distributions, data services, series, and catalog records and supports decentralized catalog publication.

A namespace or catalog folder can reflect a domain but does not prove it. Validate that records have accountable teams and coherent semantics. Detect assets listed under one domain that are written or interpreted by another without an agreement.

**Consider organizational communication.** System boundaries drift toward actual communication paths. If Pricing and Ordering teams need daily informal negotiation over undocumented fields, the interface is not stable. If one central data team decides every domain mapping, decentralized ownership is nominal.

Design teams and interaction modes alongside model contracts. Stream-aligned teams need end-to-end responsibility within manageable cognitive load. Platform and enabling teams reduce non-differentiating or learning burdens without owning domain decisions by default.

**Measure cognitive load.** Inventory domain concepts, technologies, operational responsibilities, consumer support, policies, and dependencies a team must understand. Use interviews, on-call signals, lead time, escaped defects, and unanswered questions. Headcount alone is not capacity.

Split when unrelated languages and responsibilities exceed sustainable comprehension. Merge when microscopic boundaries create more coordination than domain complexity. A specialist subsystem or platform service may remove technical load without changing semantic ownership.

**Design trust boundaries.** Crossing a domain can also cross principals, networks, jurisdictions, classifications, or purposes. Authenticate workloads and people, authorize the exact product and operation, validate inputs, minimize output, and propagate policy metadata.

Do not trust a request merely because it originates from another internal domain. Threats include confused deputies, excessive service identities, stale entitlements, poisoned events, schema attacks, data exfiltration, and compromised pipelines. Log decisions without leaking protected content.

**Align protection with semantics.** A Party domain may contain identity and contact data with different purposes and retention. A Fraud domain may infer sensitive risk signals. Boundaries can reduce exposure but can also produce duplicate sensitive stores.

Apply classification, purpose, consent, residency, minimization, encryption, retention, deletion, legal hold, access review, and incident response to products and derivations. ISO/IEC [38505-1:2026](https://www.iso.org/standard/87195.html) keeps governing-body responsibility for effective, efficient, acceptable use and protection of data in view.

**Model failure propagation.** Ask what happens if each domain, contract, registry, identity provider, network link, or platform capability is slow, unavailable, corrupted, or inconsistent. Define timeouts, retries, idempotency, backpressure, stale reads, queues, fallback, fail-open/closed behavior, reconciliation, and recovery.

Avoid boundaries that require every domain to be available for ordinary work. Conversely, do not cache high-consequence data indefinitely without staleness policy. Failure isolation is a business decision as much as a deployment feature.

**Model scaling and data gravity.** Different workloads may justify separate operational boundaries: high-volume telemetry, large media, graph traversal, transactional ledgers, and regulated archives. Technical fracture planes matter when they affect cost, latency, risk, or team load.

Do not create a domain solely because a database technology differs. A specialized storage service can remain inside a semantic domain or behind a complicated-subsystem team. Name the lasting responsibility, not the current engine.

**Detect boundary bypasses.** Search for direct table writes, shared credentials, copied schemas, common libraries containing domain rules, unversioned files, spreadsheet exports, manual reconciliation, reverse ETL, BI calculations, feature pipelines, backup restores, and emergency admin paths.

Classify each as authorized contract, transitional exception, operational mechanism, or violation. Add owner, risk, controls, expiry, and removal plan. A clean service diagram with uncontrolled analytical access is not a complete boundary.

**Use several architecture views.** Stakeholders need different evidence: concept and context maps for meaning; capability and value views for purpose; authority and stewardship views for decisions; product and lineage views for data flow; team views for communication; deployment and failure views for operations; trust and privacy views for protection.

ISO/IEC/IEEE 42010's concern and viewpoint approach supports this plural description. Reconcile view inconsistencies. A concept assigned to one domain in a semantic view but written by another in an operational view is a question, not a documentation nuisance.

**Evaluate candidate splits.** Before splitting, write target responsibilities, contracts, identifiers, invariants, consistency, ownership, team capacity, protection, data migration, consumer impact, failure modes, and costs. Simulate common changes and incidents.

Prefer seams that reduce coordination and make authority clearer. Reject a split that merely moves calls across a network while teams, schemas, transactions, and releases remain coupled. Logical boundaries can precede physical extraction.

**Evaluate candidate merges.** Merge when models and invariants are artificially separated, coordination is constant, separate products confuse consumers, or no teams can independently operate the pieces. Check that the merged scope remains cognitively and operationally manageable.

Preserve historical identities and provenance. A merge is not permission to deduplicate entities or overwrite semantics automatically. Publish a new contract and migration, then retire predecessors deliberately.

**Use incremental extraction.** Establish a target contract and owner, route new behavior through it, mirror or capture changes, backfill history with provenance, compare outputs, migrate consumers, then transfer write authority. Keep checkpoints and rollback.

Avoid long dual-write periods without reconciliation. Define which source wins per assertion and time. Test retries, partial failure, late events, concurrent writes, schema versions, access, deletion, and disaster recovery.

**Version boundary transitions.** A split or merge changes domain maps, products, schemas, identifiers, authorities, policies, teams, on-call, catalogs, lineage, and support. Treat it as a governed release, not a folder move.

Historical data should resolve the domain and contract that applied when created or decided upon. A successor can accept obligations, but past provenance should not be rewritten as though it always owned the data.

**Measure boundary fitness.** Track change lead time within and across boundaries, coordinated releases, contract breaks, consumer migration time, mapping defects, data-quality objectives, incidents and blast radius, unresolved ownership, on-call load, platform tickets, policy exceptions, and recovery results.

Interpret metrics together. Few cross-team changes may mean good locality or organizational avoidance. High event volume may indicate healthy integration or chatty coupling. Pair quantitative signals with incident and change narratives.

**Run boundary reviews as experiments.** Select representative changes: add a price rule, correct an identity, introduce a region, replay history, delete protected data, survive an outage, change a code, or retire a product. Trace affected models, teams, products, and controls.

If ordinary changes cross many boundaries, refine the design or strengthen contracts. If a domain accumulates unrelated responsibilities, split or add platform/subsystem support. Record the hypothesis, evidence, decision, and revisit trigger.

**Avoid permanent transitional boundaries.** A migration context, compatibility layer, or legacy bubble can be useful, but give it an owner, purpose, contract, support window, removal criteria, and archive plan. Names such as `temp-domain` hide neglect and violate durable design.

If a legacy context must remain indefinitely, name its enduring responsibility honestly and fund it. A boundary's age does not make its semantics clear or its risk acceptable.

**Govern disagreement.** Domain experts, security, platform, operations, and consumers may weight concerns differently. Document alternatives, consequences, evidence, unknowns, and decision authority. Use reversible trials where possible.

No method derives the one true boundary. A high-quality decision is explicit, testable, adaptable, and accountable. The goal is a system of boundaries that supports sustained flow and trustworthy meaning, not a final taxonomy.

## Definitions and Notation

Let `B` be a candidate boundary containing assertion and decision set `X`. Let `Δ(x)` be observed changes affecting element `x`. Change locality can be explored through co-change relationships among elements, but repository co-change is only evidence: generated files, broad commits, and organization habits can distort it.

Define boundary evidence as:

`E(B) = (S, L, A, T, C, F, P, V)`

where `S` is semantic cohesion, `L` change locality, `A` authority clarity, `T` team fit, `C` dependency cost, `F` failure isolation, `P` protection fit, and `V` consumer or business value. Each coordinate contains observations, confidence, and counterevidence.

For a cross-boundary invariant `I`, record:

`I = (facts, owners, decision_authority, consistency, deadline, failure_policy, compensation, reconciliation, evidence)`

This forces eventual consistency to state “eventual by when and with what consequence?” and strong consistency to name coordination and availability costs.

Represent a context edge as `R(U,D,type,contract,versions,interaction,authority,exit)`, from upstream context `U` to downstream `D`. Direction and power matter. A shared-kernel edge differs from a customer/supplier or conformist relationship even if the same data crosses it.

A boundary transition is `M = (from, to, contracts, data, authority, consumers, teams, protections, checkpoints, rollback, retirement)`. Completion requires every coordinate to be resolved or an explicit accepted limitation.

## Mechanisms, Invariants, or Proof Structure

Use ten gates for each boundary decision.

**1. Concern gate.** Identify stakeholders, outcomes, decisions, regulatory and operational concerns, and the exact entity of interest for each architecture view.

**2. Semantic gate.** Define language, concepts, examples, counterexamples, identity, grain, time, invariants, and in/out scope.

**3. Authority gate.** Assign assertion, decision, write, correction, dispute, product, incident, and lifecycle authority at useful scope.

**4. Coupling gate.** Inventory semantic, structural, transactional, temporal, availability, organizational, protection, and operational coupling plus bypasses.

**5. Relationship gate.** Choose context-map relationship, contract, versions, translations, interaction mode, negotiation, escalation, and exit.

**6. Team gate.** Verify stable end-to-end ownership, cognitive load, skills, communication paths, platform support, on-call, and consumer service.

**7. Protection gate.** Validate trust, identity, access, purpose, consent, minimization, residency, retention, deletion, audit, incident, and recovery boundaries.

**8. Failure gate.** Exercise partitions, latency, unavailability, stale data, partial writes, retries, duplicates, corruption, backpressure, reconciliation, and disaster recovery.

**9. Transition gate.** Plan contracts, coexistence, migration, provenance, consumer cohorts, checkpoints, rollback, authority transfer, and retirement.

**10. Fitness gate.** Measure change locality, coordination, contract stability, quality, incidents, team load, consumer outcomes, cost, risk, and revisit triggers.

The executable example checks four narrow boundary-proposal failures: absent semantic scope, an invariant split without a consistency policy, ambiguous ownership, and missing failure isolation.

<!-- bijux-verify: {"id":"domain-boundary-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"boundaries=4\nvalid=0\nfindings=analytics:ambiguous-owner,customer:missing-semantic-scope,orders:cross-boundary-invariant,payments:missing-failure-isolation\nready=false\n","stderr":""}} -->
```python
boundaries = (
    {"id": "customer", "semantic_scope": "", "split_invariant": False, "consistency_policy": "", "owners": 1, "failure_isolation": True},
    {"id": "orders", "semantic_scope": "order acceptance", "split_invariant": True, "consistency_policy": "", "owners": 1, "failure_isolation": True},
    {"id": "analytics", "semantic_scope": "customer value", "split_invariant": False, "consistency_policy": "", "owners": 2, "failure_isolation": True},
    {"id": "payments", "semantic_scope": "payment authorization", "split_invariant": False, "consistency_policy": "", "owners": 1, "failure_isolation": False},
)

findings = []
valid = 0
for boundary in boundaries:
    local = []
    if not boundary["semantic_scope"]:
        local.append("missing-semantic-scope")
    if boundary["split_invariant"] and not boundary["consistency_policy"]:
        local.append("cross-boundary-invariant")
    if boundary["owners"] != 1:
        local.append("ambiguous-owner")
    if not boundary["failure_isolation"]:
        local.append("missing-failure-isolation")
    if local:
        findings.extend(f"{boundary['id']}:{finding}" for finding in local)
    else:
        valid += 1

print(f"boundaries={len(boundaries)}")
print(f"valid={valid}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(valid == len(boundaries)).lower()}")
```

The checker validates four declared proposal predicates only. It does not prove semantic cohesion, correct invariants, domain authority, complete coupling discovery, team fitness, security, privacy, availability, migration safety, consumer value, or business outcomes. Those require multiple architecture views, domain expertise, operational traces, representative change scenarios, failure experiments, protection review, and accountable decision-making.

## Alternatives and Trade-Offs

**Semantic alignment versus independent deployment.** Aligning contexts, services, teams, and stores simplifies ownership but may be expensive. Logical boundaries can precede physical separation; deployment independence without semantic ownership is hollow.

**Shared kernel versus duplicated translation.** A shared kernel preserves common invariants but couples governance and release. Translation preserves autonomy but costs work and can lose meaning. Keep shared surfaces minimal and explicit.

**Strong consistency versus workflow consistency.** Atomic decisions simplify invariants but increase coordination and availability coupling. Reservations and compensation improve autonomy but expose intermediate states. Choose from business consequences and deadlines.

**Synchronous versus asynchronous contracts.** Synchronous calls offer immediate results and simple request context but couple latency and availability. Events decouple time but require ordering, idempotency, correction, backlog, and eventual-state semantics.

**Central versus distributed storage.** Central storage can simplify operations and control; distributed stores can isolate failure and authority. Neither determines semantic ownership. Govern access and contracts in both.

**Large versus small contexts.** Large contexts retain invariants but raise cognitive load and blast radius. Small contexts localize expertise but multiply interfaces. Test representative changes and incidents before choosing.

**Boundary security versus broad internal trust.** Explicit trust boundaries reduce lateral movement and confused authority but add identity, policy, and observability cost. Automate controls and design usable paved paths.

**Immediate extraction versus evolutionary transition.** Immediate extraction can unlock urgent isolation but concentrates migration risk. Incremental strangling supports evidence and rollback but creates coexistence complexity. Bound the transition and reconcile continuously.

## Failure Modes and Misconceptions

1. **A table defines a domain.** It reveals storage, not necessarily language, authority, or invariants.
2. **A service defines a bounded context.** Service boundaries can split or mix models badly.
3. **One noun deserves one service.** Behavior, invariants, authority, and team fit matter more than nouns.
4. **A monolith has no boundaries.** Modules, models, teams, schemas, and responsibilities still form boundaries, often implicit.
5. **Shared vocabulary means shared model.** Contextual definitions and rules may still differ.
6. **Events remove coupling.** They change temporal and availability coupling while preserving semantic obligations.
7. **A shared database is harmless internally.** Direct reads and writes become hidden contracts and authority bypasses.
8. **Every cross-domain invariant should use a distributed transaction.** Business workflow and failure policy may permit other consistency models.
9. **Every cross-domain invariant should be eventual.** Some consequences require one authority and atomic decision.
10. **Independent deployment proves autonomy.** Teams can remain coupled by schemas, approvals, knowledge, data, and incidents.
11. **Platform teams should own cross-domain meaning.** Platforms enable domains but do not resolve semantics by default.
12. **Regulated data belongs in one giant domain.** Protection can cross semantic domains through federated controls.
13. **Aggregate products own their sources.** They own derivations and consumer commitments, not upstream facts.
14. **The org chart is the target architecture.** Communication matters, but reporting lines are neither necessary nor durable semantics.
15. **A context map is final.** Boundaries evolve with language, business, teams, risk, and evidence.
16. **Moving code transfers ownership.** Contracts, authority, data, consumers, on-call, and lifecycle must also move.
17. **Fewer dependencies always mean better design.** Some dependencies express real business value and invariants; the goal is explicit, manageable coupling.

## Worked Examples

### Example 1

One `customer` table mixes person identity, account contract, contact permission, and credit assessment. Boundary analysis separates Party, Accounts, Communications, and Credit contexts while preserving versioned references and purpose-specific authority.

### Example 2

Ordering and Inventory share an atomic transaction. Business review finds only reservation creation must be serialized within Inventory; Order acceptance can await a reservation outcome. A workflow contract localizes stock invariants without pretending failures disappear.

### Example 3

Two teams share a tax-calculation library containing policy rules. Releases require synchronized deployment. A Tax context exposes a versioned decision service and evidence, while clients preserve quoted results needed for historical reproduction.

### Example 4

A telemetry domain is proposed solely because it uses a time-series database. Its concepts actually belong to Device Operations, while the storage and query engine are platform capabilities. The design keeps semantic ownership with devices and offers specialized infrastructure as a service.

### Example 5

A central warehouse writes corrected account status back into an operational system. The boundary review reveals an authority inversion. The warehouse retains a derived quality finding; the Accounts domain adjudicates and emits the authoritative correction.

### Example 6

A shared Party kernel grows to include preferences, segmentation, balances, and risk. Coordination becomes constant. Teams shrink the kernel to identity primitives and translate contextual attributes through explicit contracts.

### Example 7

A new regional privacy rule requires residency and shorter retention. Rather than duplicate the whole business domain, the architecture adds protected regional distributions and processing boundaries while preserving one semantic contract and scoped policy authority.

### Example 8

A recommendation product depends synchronously on Catalog, Availability, Pricing, Identity, and Features. One outage removes all recommendations. Cached, versioned input products and explicit staleness rules isolate failure while high-risk price display remains live-validated.

### Example 9

A Claims domain overwhelms one team with intake, adjudication, payments, fraud, documents, and reporting. Language, incidents, and change data reveal Claim Handling, Claim Payments, and Claim Intelligence seams with governed events and identity links.

### Example 10

A merger combines two Billing contexts. Teams first publish a shared invoice language and mappings, migrate consumers, reconcile balances, and transfer incident ownership. Historical invoices retain their source model and authority after the operational merge.

## Cross-Program Connections

- **Software architecture:** modules, services, aggregates, contracts, events, workflows, deployment, and evolutionary extraction implement boundaries.
- **Distributed systems:** consensus, partitions, consistency, queues, retries, idempotency, compensation, and reconciliation constrain cross-boundary invariants.
- **Data engineering:** CDC, batch products, streams, lineage, quality, backfill, aggregates, and replay reveal operational and analytical bypasses.
- **Platform engineering:** self-service compute, storage, contracts, policy, identity, observability, and recovery reduce extraneous domain-team load.
- **Security and privacy:** trust zones, principals, purpose, consent, classification, residency, minimization, retention, deletion, and incident response shape seams.
- **Product and organization design:** value streams, consumers, stable teams, cognitive load, interaction modes, funding, and support make boundaries operable.
- **Database engineering:** schemas, transactions, constraints, replication, ownership, views, migrations, and backups expose physical coupling.
- **Systems engineering:** stakeholders, concerns, viewpoints, interfaces, configuration, hazards, verification, change control, and lifecycle structure evidence.

## References

1. Evans, E., *Domain-Driven Design Reference*, 2015. <https://www.domainlanguage.com/ddd/reference/>
2. Conway, M. E., “How Do Committees Invent?”, *Datamation*, 1968. <https://melconway.com/Home/pdf/committees.pdf>
3. Skelton, M., and Pais, M., *Team Topologies Key Concepts*, current web edition. <https://teamtopologies.com/key-concepts>
4. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>
5. Object Management Group, *Business Architecture Core Metamodel*, Version 1.0, 2024. <https://www.omg.org/spec/BACM/1.0/>
6. Dehghani, Z., “Data Mesh Principles and Logical Architecture,” 2020. <https://martinfowler.com/articles/data-mesh-principles.html>
7. W3C, *Data Catalog Vocabulary (DCAT)—Version 3*, W3C Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>
8. ISO/IEC, *38505-1:2026 Information technology—Governance of data—Part 1*, 2026. <https://www.iso.org/standard/87195.html>

## Exercises

### Exercise 1

Evaluate whether Ordering and Inventory should share one boundary. Cover language, identities, invariants, consistency, availability, change, teams, protection, products, and failure scenarios.

### Exercise 2

Create a context map for Party, Accounts, Communications, Credit, and Analytics. Select relationship patterns, authority, contracts, versions, translations, and exit strategies.

### Exercise 3

Audit boundary bypasses in a shared enterprise warehouse. Include direct reads/writes, schemas, credentials, BI, files, reverse ETL, notebooks, feature pipelines, backup, and emergency paths.

### Exercise 4

Plan the split of a large Claims domain into three viable contexts. Include team cognitive load, source and aggregate products, identifiers, events, migration, protection, rollback, and measurements.

### Exercise 5

Design a boundary fitness review using stakeholder concerns and representative changes. Define evidence, counterevidence, thresholds, decision authority, and revisit triggers.

## Answers to the Exercises

### Answer 1

Ordering owns cart intent, offer snapshot, acceptance, order lifecycle, and customer-facing commitment. Inventory owns stock position, reservation, allocation, expiration, and oversell policy. Shared nouns do not require one language. The critical question is whether Order acceptance requires a confirmed reservation and by what deadline, not whether both use `product_id`.

If oversell is unacceptable, Inventory serializes reservation decisions and Ordering accepts only after success. During unavailability it can fail closed, queue, or offer a pending state under explicit policy. Idempotent reservation commands, versioned outcomes, expiry, cancellation, reconciliation, and recovery define the contract. Keep one boundary only if the invariant, change, team knowledge, and operations are inseparable; otherwise explicit workflow usually improves authority and failure isolation. Test partitions, retries, late release, concurrent orders, stale availability, and restoration.

### Answer 2

Party publishes stable identity primitives through an open host service and published language. Accounts consumes party references but owns account contracts and status; use customer/supplier commitments. Communications uses an anticorruption layer because consent and channel preferences have purpose-specific semantics. Credit consumes verified identity and account evidence but owns assessments and should not expose internal risk rules as shared Party attributes. Analytics consumes versioned products from all four and owns derived measures only.

Every edge names direction, model versions, identity, time, quality, protection, service behavior, change notice, and escalation. Shared kernels remain limited to truly joint identifiers. Authority matrices prevent Analytics from correcting sources. Exit strategies cover replacement of published languages, retirement of feeds, mapping preservation, consumer migration, and historical resolution.

### Answer 3

Inventory database grants and query logs for direct table access, write-capable service identities, shared schemas, stored procedures, views, materializations, common libraries, copied definitions, and undocumented joins. Trace BI tools, extracts, spreadsheets, partner files, notebooks, ML features, reverse ETL, CDC, caches, manual uploads, backup restores, support queries, and break-glass accounts.

Classify each path as a governed product, internal implementation, bounded transition, or violation. Record owner, consumer, purpose, fields, authority assumptions, versions, freshness, protection, failures, and last use. Remove unauthorized writes first. Wrap legitimate reads in contracts or governed distributions, isolate credentials, add lineage and policy, migrate consumers, and test archive and emergency procedures. Do not switch off unknown paths without consequence analysis and rollback.

### Answer 4

Use language, incidents, changes, and decisions to separate Claim Handling, Claim Payments, and Claim Intelligence. Handling owns claim identity, intake, evidence, adjudication, and status. Payments owns disbursement instructions, settlement, recovery, and ledger reconciliation. Intelligence owns derived fraud and performance models, not claim truth. Stable claim and party references plus versioned adjudication, payment-request, settlement, and finding events connect them.

Assign stream-aligned teams with platform and specialist support. Protect documents, payment data, and inferred risk separately. Establish source-aligned products and consumer aggregates with lineage. Extract one seam through a new contract, shadow and reconcile, backfill with provenance, migrate consumers, transfer write and on-call authority, then retire old paths. Test partial writes, duplicate payment, late evidence, correction, deletion, outage, replay, and rollback. Measure lead time, coordinated changes, mismatch, incidents, team load, consumer outcomes, and policy exceptions.

### Answer 5

Define stakeholder concerns for domain experts, consumers, product owners, operations, security/privacy, platform, finance, legal, and governing bodies. Maintain semantic, capability, authority, product-lineage, team, deployment-failure, and trust views. Exercise representative changes such as a new jurisdiction, corrected identity, code revision, volume surge, dependency outage, protected deletion, historical replay, and domain retirement.

For each scenario record teams touched, lead time, contract changes, semantic loss, decisions, failure propagation, recovery, protection, and consumer effect. Counterevidence includes broad commits, generated co-change, hidden consumers, and temporary staff shortages. Define unacceptable conditions such as unowned high-consequence decisions or unrecoverable writes, while treating other thresholds as context-specific. A named architecture authority decides with domain and risk owners. Revisit after major incidents, sustained coordination growth, model divergence, team overload, regulation, acquisition, or product change.
