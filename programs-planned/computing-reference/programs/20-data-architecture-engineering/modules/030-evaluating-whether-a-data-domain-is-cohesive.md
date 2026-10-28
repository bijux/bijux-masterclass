---
module_id: DARCH-030
program: Data Architecture Engineering
level: 1
module_number: 30
title: Evaluating Whether a Data Domain Is Cohesive
status: complete
last_verified: 2026-09-03
---

# Evaluating Whether a Data Domain Is Cohesive

## One-Page Review

### Governing question

How can architects determine whether a proposed data domain forms a durable, operable boundary around related business meaning and decisions—or whether it should be split, merged, reframed, or connected differently—without treating organization charts, systems, nouns, or coupling scores as proof?

### Essential definitions

- A **data domain** is a bounded area of organizational meaning and decision authority that governs related assertions, rules, products, obligations, and outcomes.
- **Cohesion** is the degree to which a boundary contains elements that belong together because they share purpose, language, invariants, authority, change, expertise, and lifecycle.
- **Coupling** is the degree to which one domain depends on another's meaning, decisions, services, timing, controls, or change.
- A **domain invariant** is a rule that must remain true across relevant state transitions within a declared domain scope.
- **Semantic cohesion** is consistency and close relationship among concepts, definitions, identities, rules, and authoritative assertions.
- **decision cohesion** exists when related decisions can be assigned to a credible accountable role with appropriate mandate, evidence, and escalation.
- **change cohesion** is the tendency of concepts, rules, products, and processes to evolve together for common reasons and at compatible rates.
- **operational cohesion** is the ability of a team or role system to own, support, protect, correct, and retire the domain's products effectively.
- A **boundary smell** is evidence suggesting a domain is arbitrary, too broad, too narrow, duplicated, unstable, or organized around implementation rather than enduring meaning.
- A **boundary decision record** preserves candidate boundaries, evidence, options, decision, dissent, consequences, review triggers, and migration.

### Central model, mechanism, or theorem

Represent a candidate domain as:

`D = (purpose, outcomes, capabilities, language, concepts, invariants, authority, assertions, products, changes, teams, dependencies, obligations, lifecycle)`

Evaluate evidence across semantic, behavioral, decision, change, operational, dependency, protection, and lifecycle cohesion. No scalar score proves a correct boundary. A viable domain has a comprehensible purpose, internally related language and invariants, credible authority and capability, manageable cognitive and operational scope, explicit external contracts, and stable reasons to change. Split when internal conflicts dominate; merge when boundaries create artificial coordination; reframe when the candidate is merely a system, department, project, or vague noun.

### Critical invariants

- Domain boundaries are justified by enduring meaning and decision responsibility rather than current reporting lines, vendors, platforms, or delivery sequences.
- Concepts inside a domain participate in related capabilities, invariants, state transitions, policies, or outcomes that practitioners can explain coherently.
- Predicate-level authority is explicit; one domain does not claim every assertion about a broad entity such as Customer, Product, or Employee.
- Internal contradictions, translation, and coordination are lower or more manageable than they would be under credible alternative boundaries.
- External dependencies use explicit contracts and mappings; cohesion does not mean isolation or ownership of every dependency.
- Team cognitive load, competence, capacity, service operation, protection, and lifecycle duties fit the boundary or have a funded operating model.
- Shared data, reference data, analytics, platform, and governance concerns are not labeled domains solely because they serve many teams.
- Boundary evidence includes actual decisions, language, change, incidents, products, dependencies, and outcomes rather than workshops alone.
- Split, merge, transfer, and reframe decisions preserve product contracts, identities, history, authority, access, corrections, and consumer migration.
- Boundaries are reviewed when strategy, capabilities, regulation, products, organization, technology, dependencies, or repeated conflicts materially change.

### Common failures

Common failures are making each database a domain; copying the organization chart; treating every business noun as a boundary; defining “Shared Data” or “Analytics” as owner of everything reused; grouping unrelated work under Customer 360; requiring a single enterprise meaning where contexts differ; splitting until every table has a team; merging domains to avoid contracts; optimizing a numerical cohesion score; ignoring human cognitive load; assigning boundaries without decision authority; confusing platform capability with business semantics; letting temporary programs become permanent domains; moving data without transferring accountability; and never reviewing a boundary after repeated incidents or changes.

### Compact example

A proposed Customer domain contains party identity, sales prospects, support cases, billing accounts, consent, loyalty points, and churn predictions. Workshops show no single invariant or authority, and the concepts change for different reasons. The organization reframes Party Identity, Sales Engagement, Customer Support, Billing, Privacy Preference, Loyalty, and Retention Analytics as distinct domains or products connected by contracts and shared identifiers. It retains a customer-oriented discovery view without inventing one universal source of truth. Boundary records document authority, mappings, dependencies, migrations, and review triggers.

### Connections

[DARCH-021](021-business-capabilities-and-data-domains.md) identifies candidates, [DARCH-022](022-domain-boundaries.md) defines boundaries, [DARCH-023](023-data-ownership-and-accountability.md) assigns decisions, and [DARCH-025](025-source-aligned-aggregate-and-consumer-aligned-data.md) through [DARCH-029](029-domain-metadata-and-discoverability.md) make products, contracts, dependencies, and discovery operational. This module evaluates whether the resulting domain remains coherent before the program enters integration architecture.

## Governing Question

Domain design is a hypothesis about organizational meaning and change. The label may sound plausible while concealing several unrelated capabilities, incompatible definitions, separate authorities, and overloaded teams. Conversely, a boundary can be split so finely that ordinary business decisions require constant distributed coordination.

The task is not to maximize independence. It is to place strongly related meaning and decisions together while making necessary external relationships explicit. Evaluation therefore combines qualitative reasoning, operational evidence, graph measures, and experiments; no workshop artifact or formula decides alone.

## Why This Matters

Poor boundaries create durable cost. Overbroad domains accumulate political ownership, contradictory terms, slow change, excessive cognitive load, and products nobody can support. Overnarrow domains multiply interfaces, duplicated policy, distributed transactions, mappings, and escalation.

Data architecture makes these problems visible because assertions persist and travel across systems. A mistaken service boundary can sometimes be hidden behind an API; conflicting domain meaning emerges in reports, models, retention, rights, corrections, and historical reconciliation.

Eric Evans's [Domain-Driven Design Reference](https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf) summarizes bounded contexts, ubiquitous language, context mapping, modules, aggregates, and related strategic patterns. Martin Fowler's [Bounded Context](https://martinfowler.com/bliki/BoundedContext.html) explains the need to divide large models and keep meanings explicit at boundaries.

Zhamak Dehghani's [Data Mesh Principles and Logical Architecture](https://martinfowler.com/articles/data-mesh-principles.html) connects domain-oriented ownership with data as a product, self-service platforms, and federated governance. Domain ownership is an operating responsibility, not simply a data-placement choice.

[ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html) defines architecture-description concepts involving stakeholders, concerns, viewpoints, views, model kinds, and correspondences. Cohesion needs several views because semantic, organizational, information, operational, protection, and lifecycle structures differ.

NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) emphasizes trustworthy secure-system engineering across life cycles. Domain boundaries affect protection, assurance, interfaces, change, and responsibility, so they require lifecycle reasoning.

[Team Topologies key concepts](https://teamtopologies.com/key-concepts) describe team types, interaction modes, cognitive load, and Conway's law-related organizational design. Melvin Conway's original paper, [How Do Committees Invent?](https://www.melconway.com/Home/Committees_Paper.html), analyzes how communication structures relate to system design. Team boundaries and domain boundaries influence each other, but neither should be copied mechanically from the other.

W3C [DCAT 3](https://www.w3.org/TR/vocab-dcat-3/) supports descriptions and relationships among catalogs, resources, datasets, services, and distributions. Product and dependency metadata provide evidence for cohesion review without deciding the organizational boundary.

## Prerequisites and Retrieval

You should understand capabilities, bounded contexts, domain language, entities, invariants, source authority, data products, ownership, stewardship, contracts, dependencies, metadata, organizational design, risk, and lifecycle.

Retrieve domain, subdomain, bounded context, capability, value stream, ubiquitous language, concept, invariant, authority, cohesion, coupling, connascence, cognitive load, change cadence, context map, upstream, downstream, product, aggregate, platform, shared service, boundary smell, split, merge, and reframe.

As a retrieval test, inspect “Customer is one enterprise domain.” Ask which customer contexts; what outcomes, capabilities, invariants, states, and decisions belong together; who has authority; which assertions are sources; which concepts conflict; why changes co-occur; which products and consumers exist; what the team can operate; and what remains external. If answers span unrelated purposes and authorities, the noun is not enough.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish domain cohesion from organizational proximity, data similarity, shared infrastructure, reuse, and low technical coupling;
2. evaluate purpose, capability, language, concept, invariant, decision, change, operational, protection, and lifecycle evidence;
3. identify overbroad, overnarrow, implementation-led, politically assigned, duplicated, and transitional boundaries;
4. analyze internal and external dependencies, translation, cycles, shared services, coordination, incidents, and change propagation;
5. assess team cognitive load, competence, capacity, product ownership, stewardship, support, and assurance fit;
6. compare split, merge, reframe, shared-kernel, platform, reference-data, aggregate-product, and mapping options;
7. use interviews, event and concept modeling, repository analysis, lineage, telemetry, work history, incidents, and experiments as evidence;
8. record boundary decisions with assumptions, dissent, migration, measures, and review triggers;
9. migrate authority, products, identifiers, contracts, data, controls, consumers, and history safely after a boundary change;
10. review domain cohesion continuously without optimizing a single score or freezing the organization.

## Core Exposition

**Treat a domain as a hypothesis.** A candidate says that a set of meanings, decisions, and outcomes belongs under one bounded authority and operating model. State the hypothesis explicitly before collecting evidence.

“Customer domain” is weak. “Party Identity governs verified identity assertions and merge/split decisions used across products” is testable. It names purpose, authority, and a boundary that can be compared with alternatives.

**Begin with outcomes and capabilities.** Identify enduring outcomes and the capabilities that produce them. Capabilities describe what the organization can do, independent of current team or system implementation.

Elements are more cohesive when they contribute to closely related outcomes and policies. A department can contain several capabilities; one capability can span teams. Avoid treating the capability map as an automatic domain map.

**Map value and decisions.** Trace decisions that create, approve, reject, price, fulfill, settle, correct, retain, or retire value. Identify which facts and rules each decision needs.

Decision clusters can reveal boundaries better than nouns. Order acceptance, fulfillment, payment settlement, and revenue recognition all concern an order journey but use different authority and invariants.

**Model language in context.** Interview practitioners and examine policies, forms, code, reports, events, schemas, incidents, and support. Record terms, definitions, examples, exclusions, synonyms, and conflicts.

A cohesive domain supports a usable ubiquitous language within its boundary. This does not mean every participant uses identical vocabulary, but translations should be manageable and disputes resolvable under one context.

**Look for semantic fractures.** The same word with incompatible identity, lifecycle, grain, or authority can indicate several contexts. `Account` in authentication and banking is an obvious split; `Customer` across prospecting, contracting, billing, service, and privacy can be subtler.

Do not split merely because labels differ. Different labels may denote one concept, while one label may hide many. Use definitions, behavior, evidence, and authority.

**Identify invariants.** An invariant constrains state transitions: an accepted order has at least one line; a settled payment balances; a consent record has purpose and effective interval. Related invariants often belong near the decisions that enforce them.

If one candidate contains unrelated invariant sets with independent transitions and authorities, it may be too broad. If an invariant requires synchronous decisions across proposed domains on every ordinary operation, the split may be too narrow.

**Trace state and lifecycle.** Model commands, events, states, transitions, corrections, and terminal conditions. Elements whose lifecycles change together may be cohesive. Elements joined only for reporting may be aggregate-product concerns instead.

Do not confuse chronological sequence with ownership. Fulfillment follows ordering, yet its resource allocation and evidence can form a separate domain connected through an accepted-order contract.

**Locate source authority.** For each assertion, name the role and process authorized to adopt, correct, or retire it. Authority may vary by predicate, jurisdiction, and time.

A candidate that requires several independent authorities is not necessarily invalid, but a single “domain owner” may be misleading. Split decisions, define a federation, or create explicit product ownership rather than hiding conflict.

**Evaluate decision cohesion.** Ask whether one credible accountable role can govern the domain's key outcomes and resolve routine conflicts. Check mandate, competence, resources, evidence, risk limits, and escalation.

One executive can sponsor many domains without operating them as one. Conversely, separate teams can participate in a cohesive domain under clear decision rights and shared products.

**Examine change reasons.** Analyze historical changes to policy, terminology, schemas, events, products, processes, and code. Ask which elements changed together and why.

Change cohesion is stronger when elements respond to common business policy, regulation, market behavior, or lifecycle. Co-change from a monolithic repository or coordinated release train can be an implementation artifact, not semantic evidence.

**Examine change cadence.** Fast-changing experimentation and slow regulated records can coexist, but a single boundary may impose unsuitable process on one side. Distinct change rates can support a split or separate product layers.

Cadence alone is insufficient. Regulatory changes can cross domains, and tightly cohesive concepts can change at different frequencies. Combine cadence with language, invariants, and authority.

**Use repository evidence carefully.** Version-control co-change, module dependencies, schema evolution, ownership files, tests, incidents, and deployment history can reveal coupling. Normalize for generated files, bulk formatting, monorepos, and shared libraries.

Correlation does not prove a domain. A central platform dependency can make unrelated modules change together. Interview maintainers and inspect reasons behind representative commits.

**Inspect product portfolios.** A cohesive domain should be able to explain its source-aligned products, consumers, contracts, quality, service, protection, and lifecycle. Products can expose whether the boundary creates a coherent external promise.

If every product combines unrelated concepts for different consumers, the domain may be a reporting bucket. If several domains publish competing source products for the same assertion, authority needs resolution.

**Inspect internal product relationships.** A domain may own several products at different grains or service tiers while sharing core meaning and authority. Internal products should not require the same heavy translation as cross-domain exchange.

Too many internal contracts can indicate over-segmentation within the domain. Too few explicit external contracts can indicate the boundary has swallowed independent contexts.

**Analyze dependencies.** Build a typed graph of semantic, operational, control, organizational, and provider dependencies. Compare internal relationships with external edges, but do not optimize a ratio mechanically.

High external dependency is normal for integration or consumer products. A domain can remain cohesive while relying on many sources. The question is whether it owns a clear purpose and derivation rather than whether it is isolated.

**Assess translation cost.** At a healthy boundary, explicit mappings translate concepts, identifiers, events, and policies. Measure frequency, complexity, ambiguity, defects, and ownership of translation.

Heavy translation inside a proposed domain suggests incompatible contexts were merged. Repeated identical translation across a proposed split suggests the boundary may be artificial or a shared mapping product is missing.

**Look for circular authority.** If Domain A defines a fact from B and B defines the same fact from A, neither source is clear. Feedback loops can be legitimate when derived decisions influence later observations, but must remain labeled.

Break cycles by assigning predicate authority, separating observation from inference, introducing time, or treating feedback as a proposal. Asynchrony does not remove semantic cycles.

**Assess cognitive load.** Inventory concepts, rules, workflows, products, interfaces, consumers, technologies, controls, incidents, and support. Ask whether the team can understand and safely change the domain.

Do not use team size alone. Experienced teams and platforms alter capacity. Observe onboarding time, review bottlenecks, misunderstood changes, queue age, and dependency coordination.

**Assess competence and capacity.** A domain needs semantic expertise, product ownership, stewardship, engineering, operations, security, privacy, records, quality, and consumer engagement appropriate to consequence. Some expertise can be shared through enabling teams or services.

If no role can own outcomes or no team can support products, the boundary is not operationally viable. The response may be funding or organizational design rather than semantic splitting.

**Assess operational cohesion.** Examine on-call, support, incident command, correction, replay, recovery, consumer communication, change, and retirement. Related products should have understandable responsibility and escalation.

One incident crossing every part of a broad domain may reveal hidden contexts. Conversely, constant multi-team coordination for each routine incident may reveal over-fragmentation.

**Assess protection cohesion.** Data sensitivity, purpose, legal role, retention, jurisdiction, licensing, safety, and assurance can influence boundaries. Separating highly restricted processing can reduce exposure and clarify controls.

Do not create a “Sensitive Data” domain that steals business meaning from sources. Preserve domain authority while using protected products, enclaves, control services, or scoped subdomains.

**Assess temporal cohesion.** Concepts may require different event, effective, record, correction, and publication times. A cohesive domain can govern these distinctions if they serve related invariants.

Conflicting retention and history rules can indicate separate contexts or policy overlays. Evaluate actual obligations rather than assuming all data about one entity shares a lifecycle.

**Distinguish core, supporting, and generic concerns.** A strategically differentiating core domain may justify dedicated expertise and careful modeling. Supporting domains enable the business but may be simpler. Generic capabilities may use shared platforms or purchased services.

These categories affect investment, not truth. A generic platform can still be critical, and a core domain still depends on contracts. Reevaluate as strategy changes.

**Distinguish business domain and platform.** Identity, catalog, orchestration, storage, and observability platforms serve domains through technical capabilities. They should not automatically own business definitions merely because all data passes through them.

A platform can be treated as a product with users, contracts, service, and lifecycle. Its cohesion derives from enabling capability and operational responsibility, distinct from source authority.

**Distinguish reference-data domains.** Shared codes, units, calendars, legal entities, and classifications can have genuine enterprise authority and lifecycle. A reference-data domain is justified when it owns those decisions, not merely because values are reused.

Local variants can remain mapped. Do not force a central team to own every code embedded in domain policy.

**Distinguish aggregate products from domains.** Customer 360, enterprise revenue, risk view, and executive metrics may combine domains for reusable decisions. Their cohesion can come from a product purpose and derivation rather than source authority.

Create an aggregate-product owner and contract instead of declaring ownership of all inputs. This preserves source corrections and semantic context.

**Distinguish analytical contexts.** Analytics and machine-learning teams create metrics, features, labels, models, and reports for decisions. “Analytics” is rarely a source domain for every input.

Some analytical areas form domains around enduring decisions and specialized language, such as pricing or fraud. Evaluate purpose, authority, feedback, and product lifecycle rather than technology.

**Identify overbroad-domain smells.** Smells include vague purpose, many unrelated capabilities, competing definitions, multiple unresolvable authorities, excessive cognitive load, slow decisions, independent change clusters, internal translation, omnibus products, and recurring ownership disputes.

One smell prompts investigation. Several corroborated smells support split or reframe. Large domains can be viable when subdomains and authority are explicit.

**Identify overnarrow-domain smells.** Smells include one table or noun per domain, constant synchronous coordination, distributed invariants, repeated mappings, duplicate stewards, tiny unsupported products, shared release decisions, and inability to produce value independently.

The remedy may be merge, module consolidation, shared kernel, or stronger product composition. Avoid merging merely to remove every interface; healthy boundaries require contracts.

**Identify implementation-led smells.** Domains named after databases, vendors, cloud accounts, ETL layers, microservices, or projects often reflect current mechanism. Ask whether meaning and authority survive replacement.

Some technical capabilities are legitimate platform domains. Name them by enduring responsibility—such as Identity Resolution or Data Delivery—not incidental product brand.

**Identify political smells.** A powerful department may claim broad data ownership, or boundaries may be drawn to avoid conflict. Look for unsupported authority, duplicate sources, hidden consumers, unfunded stewardship, and exceptions.

Architecture cannot settle organizational mandate alone. Surface evidence and decision needs to leadership. Record dissent and unresolved risk rather than presenting consensus fiction.

**Compare candidate boundaries.** Develop at least two credible options. For each, map purpose, language, invariants, authority, products, teams, dependencies, translation, risk, service, cost, migration, and future change.

Avoid straw alternatives. A split has coordination cost; a merge has cognitive and governance cost. Make trade-offs visible to accountable decision makers.

**Use qualitative matrices carefully.** Rate evidence as strong, mixed, weak, or unknown across cohesion dimensions. Attach observations and sources to each rating.

Do not sum ordinal ratings into false precision. Weighting hides judgment. A critical authority conflict can dominate several favorable similarities.

**Use quantitative indicators as prompts.** Candidate measures include internal versus external co-change, dependency density, translation defects, number of authorities, incident coordination, onboarding time, product support load, and consumer migration frequency.

Normalize populations and periods. Metrics can be gamed and reflect current organization. Use them to find questions and compare trends, not prove boundaries.

**Run modeling workshops.** Event storming, domain storytelling, capability mapping, Wardley mapping, concept modeling, and context mapping can reveal language, decisions, dependencies, and evolution.

Workshops produce hypotheses. Validate them against code, data, policies, incidents, products, users, and operating history. Include diverse practitioners and affected control roles.

**Run boundary experiments.** Pilot a product contract, separate a change queue, assign a focused owner, create an anti-corruption mapping, or operate independent release and support for a bounded period.

Define success and rollback before the experiment. Observe decision speed, defects, coordination, cognitive load, service, consumer outcomes, and protection. Do not let a pilot name become permanent without review.

**Record the decision.** A boundary decision record includes context, candidate, evidence, alternatives, decision, authority, assumptions, consequences, dissent, migration, metrics, and review triggers.

Link concepts, products, contracts, roles, systems, and dependencies. Version the record. Future teams should understand why the boundary exists without relying on memory.

**Plan a split.** Allocate concepts, assertions, authority, products, contracts, data, code, controls, incidents, staff, budgets, and lifecycle. Define shared identifiers, mappings, transition products, and temporary dependencies.

Avoid copying data and declaring completion. Consumers need versioned contracts and migration. Historical corrections, retention, legal holds, and evidence need explicit owners.

**Plan a merge.** Reconcile language, identity, invariants, authorities, products, service, controls, and lifecycle. Preserve legitimate contexts and avoid choosing one model by organizational power.

Retire duplicate products only after consumer validation. Merging teams without resolving semantics concentrates confusion.

**Plan a reframe.** A candidate may be a value-stream view, product collection, platform, shared service, aggregate product, taxonomy, or governance forum rather than a source domain. Keep the useful view and assign the correct kind of ownership.

Reframing can resolve debates that assume every important concept needs one domain. Different architecture views can coexist with explicit correspondences.

**Migrate authority.** State which role can decide during transition, when authority transfers, who accepts open risks, and how conflicts escalate. Avoid overlapping final authority.

Update stewardship, access approvals, quality exceptions, incident paths, retention, contracts, and catalog records. Revoke obsolete permissions after verified transfer.

**Migrate data and history.** Preserve business keys, provenance, lineage, temporal semantics, corrections, and versions. A physical move is not necessary for every boundary change, and a physical move alone proves nothing.

Validate current and historical products. Reconcile totals and representative assertions. Keep evidence of values and boundaries used for past decisions where required.

**Migrate consumers.** Inventory direct and transitive consumers, unknown-use signals, reports, models, exports, and manual processes. Publish mappings, versions, notices, fixtures, support, and deadlines.

Measure migrated behavior and decision outcomes. Bound extensions and exceptions. Do not abandon consumers because a new org chart became effective.

**Review cohesion continuously.** Triggers include strategy shift, new regulation, mergers, recurring disputes, overloaded teams, duplicated products, change bottlenecks, incidents, provider change, new platform capability, or sustained translation cost.

Periodic review can be lightweight when evidence remains stable. High-consequence or rapidly changing domains need deeper assurance. Preserve time-series evidence rather than rewriting history.

**Treat uncertainty honestly.** Some boundaries are ambiguous because the business itself is evolving. Use provisional decisions with explicit assumptions, guardrails, owners, and review dates.

Unknown evidence is not negative evidence. Invest in discovery, instrumentation, and experiments. Avoid premature precision and permanent transitional labels.

The final test is whether practitioners can explain why the elements belong together, make and operate related decisions within the boundary, and interact with other domains through manageable contracts. If the explanation depends on a database, manager, or slogan, the boundary needs more work.

## Definitions and Notation

Let candidate domain `D = (P,C,L,I,A,S,R,T,E,O,H)`, where `P` is purpose and outcomes, `C` capabilities, `L` language and concepts, `I` invariants, `A` authority and assertions, `S` products and services, `R` roles and resources, `T` change and lifecycle, `E` external dependencies, `O` obligations and protection, and `H` historical evidence.

Let evidence item `x = (dimension,observation,source,method,scope,time,confidence,limitation)`. An assessment is a set of evidence items and reasoned judgments, not one unqualified score.

For candidate partition `Π = {D1,...,Dn}`, define translation edges among domains and internal relationships within domains. Indicators such as internal-edge fraction can describe structure under a chosen graph, but results depend on node, edge, weight, time, and evidence definitions.

Let `Viable(D,t)` require coherent purpose, usable language, governable invariants, credible authority, operable products, capable roles, manageable dependencies, protection, and lifecycle at time `t`. These are review predicates, not mechanically decidable facts.

A boundary decision record is `B = (context,candidates,evidence,criteria,decision,authority,assumptions,consequences,dissent,migration,measures,review_triggers)`.

## Mechanisms, Invariants, or Proof Structure

Use ten gates to evaluate each material domain candidate.

**1. Purpose gate.** State enduring outcomes, capabilities, value, users, scope, exclusions, and strategic role.

**2. Language gate.** Test concepts, definitions, identities, synonyms, conflicts, mappings, examples, and practitioner comprehension.

**3. Invariant gate.** Identify state, transitions, rules, consistency boundaries, temporal behavior, corrections, and lifecycle.

**4. Authority gate.** Assign predicate-level decisions, accountable roles, stewardship, legal and risk limits, evidence, and escalation.

**5. Product gate.** Evaluate source and derived products, consumers, contracts, quality, service, protection, support, and retirement.

**6. Change gate.** Analyze reasons, cadence, co-change, releases, incidents, correction, regulation, and likely future evolution.

**7. Team gate.** Verify cognitive load, competence, capacity, interactions, platform support, operations, and succession.

**8. Dependency gate.** Analyze internal and external semantic, service, control, provider, translation, cycle, concentration, and recovery relationships.

**9. Evidence gate.** Reconcile interviews, models, policies, code, data, lineage, telemetry, tickets, incidents, metrics, experiments, and limitations.

**10. Lifecycle gate.** Compare alternatives, decide, record, migrate authority and consumers, measure outcomes, review triggers, split, merge, reframe, or retire.

The executable example checks four narrow candidate-domain failures: missing coherent outcomes, conflicting authority, missing stable language, and missing operating ownership.

<!-- bijux-verify: {"id":"domain-cohesion-integrity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"candidates=4\nviable=0\nfindings=analytics:missing-stable-language,customer-360:missing-coherent-outcomes,shared-data:conflicting-authority,warehouse:missing-operating-owner\nready=false\n","stderr":""}} -->
```python
candidates = (
    {"id": "customer-360", "outcomes": False, "authority": True, "language": True, "operating_owner": True},
    {"id": "shared-data", "outcomes": True, "authority": False, "language": True, "operating_owner": True},
    {"id": "analytics", "outcomes": True, "authority": True, "language": False, "operating_owner": True},
    {"id": "warehouse", "outcomes": True, "authority": True, "language": True, "operating_owner": False},
)

findings = []
viable = 0
for candidate in candidates:
    local = []
    if not candidate["outcomes"]:
        local.append("missing-coherent-outcomes")
    if not candidate["authority"]:
        local.append("conflicting-authority")
    if not candidate["language"]:
        local.append("missing-stable-language")
    if not candidate["operating_owner"]:
        local.append("missing-operating-owner")
    if local:
        findings.extend(f"{candidate['id']}:{finding}" for finding in local)
    else:
        viable += 1

print(f"candidates={len(candidates)}")
print(f"viable={viable}")
print("findings=" + ",".join(sorted(findings)))
print(f"ready={str(viable == len(candidates)).lower()}")
```

The checker validates four declared predicates only. It does not prove the candidates are real domains, boundaries are correct, language is coherent, authority is lawful, teams have capacity, dependencies are manageable, products are fit, migrations are safe, or production outcomes will improve. Those require practitioner evidence, models, authority records, product and dependency analysis, operational history, experiments, protection review, and accountable decisions.

## Alternatives and Trade-Offs

**Broad versus narrow domains.** Broad domains reduce external coordination and can preserve end-to-end outcomes but increase cognitive load and internal conflict. Narrow domains focus language and ownership while multiplying interfaces and distributed invariants.

**Business capability versus value-stream boundary.** Capabilities emphasize durable ability; value streams emphasize flow across outcomes. Domains can align with either when authority and language support it. Use multiple views.

**Central authority versus federated domains.** Centralization improves uniformity and enterprise decisions but can become remote and slow. Federation improves context and autonomy but needs shared policies, platforms, contracts, and escalation.

**Shared kernel versus explicit translation.** A shared model reduces duplication for genuinely stable common concepts but couples change. Translation preserves autonomy at ongoing mapping cost. Keep shared kernels small and jointly governed.

**Source domain versus aggregate product.** Source domains own authoritative assertions; aggregate products own reconciliation for a purpose. Making an aggregate a source domain can erase input authority, while refusing aggregates duplicates integration.

**Semantic split versus operational consolidation.** Separate contexts can share infrastructure and teams when contracts remain explicit. Cohesive semantics need not imply separate deployment, and shared deployment need not imply one domain.

**Quantitative score versus evidence narrative.** Scores aid comparison and trend but conceal weighting and uncertainty. Narratives preserve reasoning but are harder to scan. Use structured evidence matrices without automatic totals.

**Immediate restructuring versus bounded experiment.** Immediate change addresses clear harm but increases migration risk. Experiments gather evidence and build capability but can become permanent ambiguity. Define authority, duration, success, and rollback.

## Failure Modes and Misconceptions

1. **Every database is a domain.** Storage boundaries reflect implementation, not necessarily meaning or authority.
2. **The organization chart defines domains.** Reporting structures change and can contain several contexts.
3. **Every major noun is one domain.** Broad nouns often contain incompatible identities, lifecycles, and decisions.
4. **Cohesion means no external dependencies.** Healthy domains rely on explicit contracts.
5. **Low technical coupling proves cohesion.** Language and authority can still conflict.
6. **High data similarity means one domain.** Similar schemas can represent different contexts and obligations.
7. **One source of truth means one owner for every predicate.** Authority varies by assertion, purpose, time, and jurisdiction.
8. **Customer 360 should own all customer facts.** It is usually an aggregate product with governed derivations.
9. **Shared data is automatically a domain.** Reuse does not establish coherent decisions or authority.
10. **Analytics is never a domain.** An enduring analytical decision area can have language, authority, products, and lifecycle.
11. **Smaller domains always increase autonomy.** Distributed invariants and constant coordination can reduce it.
12. **Merging removes integration cost.** It can move translation and conflict inside an overloaded boundary.
13. **A cohesion score decides the boundary.** Measures depend on modeling choices and cannot replace judgment.
14. **Workshop agreement proves the model.** Operational, historical, consumer, and protection evidence must corroborate it.
15. **Moving data completes a domain change.** Authority, products, contracts, controls, consumers, and history also move.
16. **Reorganization automatically changes boundaries.** Semantic and operational reality may not follow the chart.
17. **Once chosen, a domain is permanent.** Strategy, regulation, products, incidents, and capabilities can change evidence.

## Worked Examples

### Example 1

A warehouse schema becomes the “Finance domain.” Review separates Accounts Payable, Treasury, Ledger, and Reporting contexts while retaining shared infrastructure and governed financial reference products.

### Example 2

Customer 360 mixes prospects, parties, contracts, billing, service, consent, loyalty, and predictions. It is reframed as a product collection and discovery view over explicit source domains and aggregates.

### Example 3

Order and Fulfillment change together in one monolith. Event and authority analysis shows distinct invariants and decisions. Separate domains retain an accepted-order contract and share a team temporarily.

### Example 4

Two tiny domains must coordinate every change to enforce one balance invariant. The organization merges their semantic modules while keeping separate deployment components for scale.

### Example 5

A global Product domain conflicts with regulated regional classifications. The core identity remains shared, while scoped regulatory subdomains own local assertions and mapped products.

### Example 6

A Data Platform group claims business definitions because it hosts every table. The boundary is reframed around delivery capability; domain owners retain semantics and use platform contracts.

### Example 7

Fraud Analytics develops stable concepts, features, labels, decisions, appeals, and feedback. It qualifies as a domain despite consuming many source products, with careful separation of inference and observed facts.

### Example 8

Commit co-change suggests one domain, but analysis finds mass generated-schema updates. After normalization, semantic changes cluster separately, preventing an implementation artifact from driving a merge.

### Example 9

An owner dispute persists across Claims Intake and Adjudication. A pilot gives each focused decisions and products; reduced queue delay and clearer corrections support a split with a shared claim identifier.

### Example 10

A merger introduces overlapping Supplier domains. The migration preserves source histories and legal entities, maps identities, reconciles products, transfers authority, and delays consolidation until consumer evidence supports it.

## Cross-Program Connections

- **Domain-driven design:** bounded contexts, ubiquitous language, context maps, aggregates, invariants, and strategic design provide core reasoning patterns.
- **Enterprise architecture:** capabilities, value streams, stakeholders, viewpoints, organization, strategy, and transition planning frame candidate boundaries.
- **Data engineering:** schemas, events, lineage, transformations, quality, changes, incidents, and products provide operational evidence.
- **Platform engineering:** self-service capabilities, shared services, team cognitive load, ownership, and golden paths influence viable operation.
- **Software architecture:** modularity, cohesion, coupling, connascence, dependency direction, interfaces, repositories, and deployments offer partial indicators.
- **Security and privacy:** trust boundaries, purpose, classification, legal roles, controls, incidents, retention, and assurance can reshape domain scope.
- **Organizational design:** communication structures, authority, incentives, cognitive load, team interactions, succession, and funding affect implementation.
- **Systems engineering:** stakeholder concerns, requirements allocation, interfaces, verification, configuration, trade studies, migration, and lifecycle support durable decisions.

## References

1. Evans, E., *Domain-Driven Design Reference: Definitions and Pattern Summaries*, 2015. <https://www.domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf>
2. Fowler, M., *Bounded Context*, 2014. <https://martinfowler.com/bliki/BoundedContext.html>
3. Dehghani, Z., *Data Mesh Principles and Logical Architecture*, 2020. <https://martinfowler.com/articles/data-mesh-principles.html>
4. ISO/IEC/IEEE, *42010:2022 Software, systems and enterprise—Architecture description*, 2022. <https://www.iso.org/standard/74393.html>
5. NIST, *Systems Security Engineering: Considerations for a Multidisciplinary Approach in the Engineering of Trustworthy Secure Systems*, SP 800-160 Volume 1 Revision 1, 2022. <https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final>
6. Skelton, M., and Pais, M., *Team Topologies: Key Concepts*, continuously maintained. <https://teamtopologies.com/key-concepts>
7. Conway, M. E., *How Do Committees Invent?*, Datamation 14(4), 1968. <https://www.melconway.com/Home/Committees_Paper.html>
8. W3C, *Data Catalog Vocabulary (DCAT)—Version 3*, W3C Recommendation, 2024. <https://www.w3.org/TR/vocab-dcat-3/>

## Exercises

### Exercise 1

Evaluate a proposed Customer domain containing prospect, party identity, contracts, billing, support, consent, loyalty, and churn prediction. Produce evidence, candidate boundaries, and a decision.

### Exercise 2

Compare one broad Order-to-Cash domain with Order, Fulfillment, Billing, Payment, and Revenue domains. Analyze invariants, authority, change, teams, products, dependencies, and failure.

### Exercise 3

Design a cohesion evidence program using interviews, language, capabilities, events, repositories, lineage, contracts, tickets, incidents, metrics, and experiments. Address bias and limitations.

### Exercise 4

Plan a split of an overbroad domain while preserving authority, products, identifiers, history, controls, consumers, and operations. Include transitional risks and verification.

### Exercise 5

Create a recurring domain-cohesion review covering triggers, evidence, alternatives, decision records, measures, governance, migration, and closure.

## Answers to the Exercises

### Answer 1

The broad noun is insufficient. Model distinct outcomes, language, identities, invariants, authority, change reasons, products, and consumers. Party Identity can govern verified identity and merge/split assertions. Sales Engagement governs prospects and opportunities. Contracting governs agreements; Billing governs accounts and invoices; Support governs cases; Privacy Preference governs purpose-specific consent evidence; Loyalty governs points; Retention Analytics owns churn features and scores. Jurisdiction or organizational evidence may justify different names or combinations.

Keep shared person and organization identifiers with versioned mappings. Customer Profile and 360 views become aggregate or consumer-aligned products, not universal source domains. Compare alternatives including a smaller number of subdomains. Assess team capacity and protection. Record predicate authority, context mappings, product contracts, dependencies, consumer migrations, and historical correction. Preserve a customer-oriented catalog journey. Review after operating evidence rather than treating the workshop decomposition as final proof.

### Answer 2

The broad boundary reduces external interfaces and can coordinate the end-to-end cash outcome. It risks incompatible language, several authorities, different invariants, cadences, controls, and cognitive overload. Separate domains clarify accepted order, physical fulfillment, invoice, funds transfer, accounting recognition, and their corrections. They add contracts and cross-domain incident work.

Map which invariants are truly atomic. If payment authorization must occur during order acceptance, define a synchronous decision contract without merging all payment lifecycle. Use events for later fulfillment and accounting where timing permits. Assign predicate-level authority, product owners, quality and service, and one cross-domain incident coordinator. Compare historical co-change after removing monolith artifacts, operational incidents, translation defects, team load, regulation, and consumers. A plausible result is distinct domains with an Order-to-Cash value-stream view and aggregate metrics, not either one universal domain or isolated teams.

### Answer 3

Gather practitioner interviews and domain stories; capability, value, concept, event, state, invariant, authority, product, dependency, protection, and lifecycle models; policies and legal-role evidence; version-control and schema changes; lineage and runtime use; contract and catalog records; work queues, decision delays, defects, incidents, corrections, onboarding, and support. Normalize generated changes, reorganizations, monorepos, seasonality, and missing telemetry.

Triangulate each finding with source, method, scope, time, confidence, and limitation. Include producers, consumers, operations, security, privacy, records, finance, and affected regions. Workshops generate hypotheses; operational samples challenge them. Quantitative indicators prompt investigation but are not summed as proof. Run bounded ownership, contract, mapping, or release experiments with baseline, success, rollback, and duration. Record contradictory evidence and dissent. Protect sensitive organizational and incident data and use independent facilitation for politically contested boundaries.

### Answer 4

Define target domains by purpose, language, invariants, authority, products, teams, and obligations. Inventory concepts, assertions, keys, schemas, history, products, consumers, contracts, quality, service, access, retention, incidents, exceptions, providers, staff, budgets, and evidence. Establish one transition authority per decision and dated successor acceptance. Create stable shared identifiers, explicit context mappings, and temporary compatibility products without creating ambiguous duplicate sources.

Migrate product contracts and consumers through versions, fixtures, parallel validation, notices, support, and deadlines. Preserve provenance, effective and record time, corrections, legal holds, and historical decisions. Reassign stewardship, access approvals, incident paths, quality exceptions, and on-call. Reconcile current and historical data. Measure decision speed, defects, coordination, load, service, consumer outcomes, and protection. Bound exceptions and revoke obsolete access. Close the old boundary only after products, consumers, work, controls, evidence, and archival obligations transfer.

### Answer 5

Trigger review after strategy, regulation, acquisition, recurring authority disputes, duplicated sources, overloaded teams, incidents, translation growth, product proliferation, provider change, or major platform capability. Periodically sample stable domains. Use a common evidence template across purpose, language, invariants, authority, products, change, team, dependencies, protection, operations, and lifecycle, with confidence and limitations.

Require credible split, merge, reframe, and retain alternatives for material cases. The accountable architecture and business authorities decide with affected domain, consumer, platform, security, privacy, legal, records, risk, and workforce input as applicable. Version boundary decision records with assumptions, dissent, consequences, migration, measures, and future triggers. Track outcomes without optimizing one score. Migration has named authority, contracts, tests, consumers, controls, support, and rollback. Closure verifies transfers, access revocation, historical evidence, retired products, and successor obligations; review the resulting boundary against observed operation.
