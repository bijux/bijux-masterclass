---
module_id: DARCH-092
program: Data Architecture Engineering
level: 2
module_number: 92
title: Target-State Architecture
status: complete
last_verified: 2026-09-03
---

# Target-State Architecture

## One-Page Review

### Governing question

How can an organization define a coherent, testable, feasible, and evolvable target data architecture that directs present decisions toward stakeholder outcomes without pretending the future is certain, encoding a vendor shopping list, or leaving transition and retirement to later?

### Essential definitions

- A **target-state architecture** is a versioned, time-bounded hypothesis about the required future structure, flow, ownership, policy, behavior, operation, evolution, and lifecycle of data capabilities for stated outcomes and constraints.
- A **target horizon** is the date or decision window for which assumptions, demand, obligations, capabilities, and architecture claims are intended to hold.
- A **target profile** states desired outcomes and conditions for a bounded scope; it need not prescribe every implementation detail.
- A **concept of operations** explains how people, organizations, services, data products, platforms, controls, and external parties will use and operate the target system across normal, changed, degraded, recovered, and retired states.
- An **architecture view** represents selected concerns of identified stakeholders according to a declared viewpoint. No single diagram is the architecture.
- A **quality scenario** specifies source, stimulus, environment, affected artifact or boundary, expected response, and measurable response condition.
- A **capability allocation** assigns required outcomes and behavior to accountable domains, products, platforms, services, controls, people, and external providers.
- A **target contract** defines the semantics, schema, behavior, service, policy, evidence, change, and closure expected at a future boundary.
- An **architecture invariant** is a condition that must remain true across allowed implementations and transitions.
- A **guardrail** constrains decisions while leaving bounded implementation choice; it includes rationale, scope, conformance evidence, exceptions, owner, and expiry.
- A **deferred decision** is an intentionally unresolved choice with a latest responsible date, required evidence, owner, options, dependency, and safe default.
- An **architecture assumption** is a material proposition accepted provisionally and linked to validation, sensitivity, owner, and expiry.
- **Coherence** is the absence of material contradiction among outcomes, views, allocations, interfaces, policies, qualities, economics, transition, recovery, and lifecycle.
- **Transition feasibility** means a credible sequence can move from current to target conditions within constraints while preserving service, semantics, policy, evidence, recovery, and rollback.
- **Closure** retires superseded target descriptions, decisions, contracts, interfaces, exceptions, data paths, credentials, recovery assets, and commitments while preserving required history and preventing obsolete designs from regaining authority.

### Central model, mechanism, or theorem

Represent a target-state architecture as:

`T = (U, H, C, O, D, I, P, G, Q, E, M, R, L)`

where `U` is users, outcomes, and decisions; `H` horizon, context, assumptions, and uncertainty; `C` capabilities and allocations; `O` ownership and operating model; `D` data, domains, products, semantics, and topology; `I` interfaces, flows, and interoperability; `P` platforms, storage, processing, and serving; `G` governance, security, privacy, and policy; `Q` quality, service, resilience, and recovery; `E` evidence, conformance, observation, and economics; `M` migration, dependencies, rollback, and transition feasibility; `R` review, change, risk, and reconsideration; and `L` lifecycle and closure. A target is defensible only when these components trace to bounded stakeholder outcomes and constraints, agree across views, admit a credible transition, and define evidence that could falsify the hypothesis.

### Critical invariants

- Target, version, horizon, stakeholder, outcome, constraint, capability, domain, product, platform, interface, contract, policy, scenario, assumption, decision, exception, evidence, transition, and retirement have distinct stable identities.
- The current state, target state, transition architecture, and deployed state remain distinguishable and are related by explicit traceability.
- Every target claim names its scope, horizon, owner, rationale, source decisions, assumptions, evidence or acceptance criteria, dependencies, and review trigger.
- Outcome, capability, logical, information, semantic, operational, security, deployment, transition, economic, and lifecycle views describe the same architecture and expose conflicts.
- Conceptual intent is solution-neutral where choice remains valuable and implementation-specific where interoperability, assurance, feasibility, or commitment requires precision.
- Global invariants and platform guardrails do not erase domain authority; local autonomy does not bypass cross-boundary obligations.
- Interfaces define semantics, behavior, policy, service, evolution, failure, and closure—not merely transport and schema.
- Quality claims are expressed as measurable normal, stress, change, failure, recovery, and exit scenarios.
- Unknowns and assumptions remain visible; uncertainty cannot be converted silently into target fact.
- Target selection includes economics, organizational capacity, dependency ownership, migration, rollback, recovery, and exit.
- Conformance proves only declared target conditions; user and mission outcomes require separate validation.
- Superseded target artifacts cannot continue to approve work or reactivate retired architecture.

### Common failures

Common failures include drawing the desired technology stack before defining outcomes; renaming the current architecture as target; treating a cloud move as a target state; describing only data at rest; centralizing all semantics for diagram simplicity; declaring domains without decision rights; publishing products without obligations; listing principles without conformance; drawing interfaces without failure or evolution behavior; making every future choice now; hiding unresolved choices as generic boxes; assuming growth, skills, funding, regulation, or vendor behavior; omitting negative and recovery scenarios; creating inconsistent views; selecting a target that has no viable transition; ignoring dual operation and rollback; funding build but not operation or exit; measuring delivery milestones as outcomes; and leaving obsolete diagrams, standards, routes, or recovery paths active.

### Compact example

Ten invented target claims are checked against six mandatory design gates. Four are ready; one each lacks an outcome, accountable owner, explicit interface, verifiable scenario, funded lifecycle, or transition path. The program also counts eight architecture views, seven stakeholder groups, three decision horizons, ten traceability receipts, and ten decisions. It verifies declared structure and counts only—not target correctness, coherence, feasibility, conformance, migration safety, cost, risk, or value.

### Connections

[DARCH-002](002-business-strategy-and-data-outcomes.md), [DARCH-003](003-current-state-data-landscape.md), [DARCH-006](006-data-principles-and-decision-rules.md), [DARCH-007](007-architecture-drivers-and-constraints.md), [DARCH-008](008-data-risk-and-criticality.md), [DARCH-009](009-architecture-views-and-stakeholders.md), [DARCH-010](010-writing-a-data-architecture-charter.md), [DARCH-050](050-mapping-data-workloads-to-platforms-and-serving-systems.md), [DARCH-080](080-embedding-governance-into-data-flows-and-products.md), [DARCH-090](090-evaluating-mesh-fabric-warehouse-and-hybrid-options.md), and [DARCH-091](091-assessing-data-architecture-maturity.md) establish outcomes, baseline, principles, alternatives, and readiness. [DARCH-093](../ROADMAP.md) next defines transition architectures.

## Governing Question

A target architecture is often drawn as several tidy boxes with arrows and product logos. Such a picture may communicate procurement preference, yet it says little about who owns customer meaning, how late events correct financial reports, where a privacy decision executes, which workload gets which consistency, how consumers survive contract change, what happens during regional failure, or whether the organization can reach and operate the design. A diagram can be internally elegant and externally useless.

The governing question is how to create an architecture hypothesis that constrains present decisions while remaining accountable to future outcomes and uncertainty. The target must be specific enough to test coherence, interfaces, qualities, controls, cost, and transition; abstract enough to preserve safe local choice and learning; and temporary enough to change when assumptions, evidence, or context change. It is not the future itself. It is the current best governed statement of the future conditions the organization intends to create.

## Why This Matters

The Open Group's [TOGAF standards catalog](https://publications.opengroup.org/standards/togaf) identifies a maintained enterprise-architecture standard accompanied by methods, guides, templates, patterns, and reference material. It supplies industry context for baseline, target, views, gaps, and roadmaps. Access to a method does not establish that a target is coherent, feasible, or locally valuable.

The NASA [Systems Engineering Handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf) describes architecture concepts in terms of functional elements, interfaces, and a concept of operations, developed iteratively with stakeholder, reviewer, designer, and operator feedback. It also connects functions to inputs, outputs, failure modes, consequences, and interface requirements. This supports a target as an operational system description rather than a component inventory.

NIST [SP 1301 on organizational profiles](https://csrc.nist.gov/pubs/sp/1301/final) describes current and target cybersecurity outcomes tailored to mission objectives, stakeholder expectations, threats, and requirements. The profile idea usefully separates desired outcomes from one prescribed implementation. Cybersecurity profiles remain one view of a data architecture, not the whole target.

NIST's [Privacy Framework 1.1](https://www.nist.gov/privacy-framework/using-privacy-framework-11) uses core outcomes, profiles, and implementation tiers to manage privacy risk. A target data architecture should therefore represent desired privacy outcomes in collection, joining, use, access, retention, sharing, and deletion rather than adding privacy as a late control box.

The [arc42 documentation](https://docs.arc42.org/home/) organizes architecture descriptions around goals, constraints, context, strategy, building blocks, runtime, deployment, cross-cutting concepts, decisions, quality, risks, and terminology. It illustrates why target communication needs several stakeholder-oriented views and explicit decisions, not one universal drawing.

The arc42 [quality-requirements guidance](https://docs.arc42.org/section-10/) makes quality claims concrete through usage, change, and failure scenarios containing stimulus, environment, response, and measurable response conditions. Such scenarios can falsify or refine target claims that words such as scalable, secure, and flexible leave ambiguous.

The official [C4 model](https://c4model.com/) uses hierarchical system-context, container, component, and code diagrams plus dynamic and deployment views. It provides one practical notation for communicating software structure at different abstraction levels. A notation still needs data semantics, ownership, policies, operational scenarios, and lifecycle context.

The Bitol [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/) provides machine-readable schema, quality, service, role, support, and infrastructure sections. A future interface can therefore be expressed as an owned, testable contract rather than an arrow, while actual producer and consumer behavior must still be validated.

W3C [Data Catalog Vocabulary 3](https://www.w3.org/TR/vocab-dcat-3/) represents catalogs, datasets, distributions, data services, relationships, versions, and profiles. It demonstrates how a target discovery and sharing view can preserve different datasets, services, representations, and versions without forcing one physical platform.

OpenLineage's [object model](https://openlineage.io/docs/spec/object-model/) represents datasets, jobs, runs, events, namespaces, names, and facets. Stable target identities and intended lineage coverage can become conformance requirements. Runtime events later show deployment behavior, not whether the target was intrinsically correct.

The Open Policy Agent [policy language documentation](https://www.openpolicyagent.org/docs/policy-language) describes structured policy decisions using Rego. Target policy architecture can specify decision inputs, bundles, enforcement points, tests, and evidence. Authority, coverage, exceptions, rollout, and recovery still require organizational and operational design.

The OpenTelemetry [specification](https://opentelemetry.io/docs/specs/otel/) standardizes telemetry concepts and signals. A target observability view can define identities, context propagation, semantic conventions, sampling, and required signals across platforms. Instrumentation is evidence plumbing, not proof of service or user value.

NIST [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) applies systems-security engineering across the system lifecycle and emphasizes trustworthy secure systems. Security should shape target boundaries, functions, interfaces, supply chains, operations, and retirement rather than decorate a completed design.

The FinOps Foundation's [FinOps Framework](https://www.finops.org/framework/) connects engineering, finance, product, leadership, procurement, and other stakeholders to usage, cost, value, optimization, and governance. A target needs allocation, unit economics, commitments, capacity, and accountability, not an unbounded promise that consolidation or cloud will be cheaper.

NASA's [Decision Analysis](https://www.nasa.gov/reference/6-8-decision-analysis/) describes criteria, alternatives, evaluation, uncertainty reduction, robustness, results, and recommendations. The chosen target should retain rejected alternatives, assumptions, sensitivity, and rationale instead of erasing how the architecture was selected.

The AWS [Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) is vendor guidance organized around operational excellence, security, reliability, performance efficiency, cost optimization, and sustainability. It offers implementation questions for one ecosystem; its scope and commercial provenance must remain explicit, and local evidence must test all adopted claims.

Together these sources support outcome profiles, concepts of operation, multiple views, quality scenarios, explicit contracts, catalog and lineage identities, policy and telemetry, security throughout the lifecycle, economics, and decision evidence. They do not produce one correct target, reconcile stakeholder conflict, validate assumptions, prove feasibility, transfer cloud guidance, or demonstrate outcomes. Those conclusions require local current-state evidence, architecture synthesis, trade studies, experiments, transition design, and stakeholder validation.

## Prerequisites and Retrieval

You should understand strategy, outcomes, stakeholders, current-state discovery, capabilities, domains, products, semantics, data flows, interfaces, contracts, platforms, storage and processing, governance, security, privacy, quality, reliability, recovery, economics, maturity, architecture views, decisions, migration, and closure.

Retrieve target state, target horizon, current profile, target profile, concept of operations, stakeholder concern, viewpoint, view, capability allocation, domain topology, product topology, semantic model, target contract, invariant, guardrail, quality scenario, assumption, uncertainty, deferred decision, traceability, conformance, validation, gap, dependency, transition feasibility, rollback, recovery, review trigger, and closure.

As a retrieval test, inspect a proposed target in which domain-owned data products run on a shared lakehouse and supply a reporting warehouse, operational APIs, and external partners. Ask which outcomes and consumers justify the arrangement; which horizons it covers; who owns product meaning, shared platform service, conformed reporting, policy, and incidents; which semantics and contracts cross boundaries; which normal, change, failure, recovery, and exit scenarios apply; what data may move; how lineage and cost follow it; which assumptions remain; what current-state dependencies block it; how rollback works; and what evidence would reject or revise the target. A box labeled “modern data platform” answers none of these questions.

## Learning Objectives

After completing this module, you should be able to:

1. define target-state architecture as a time-bounded, falsifiable hypothesis rather than a future inventory or fixed blueprint;
2. derive target outcomes, constraints, capability needs, principles, and quality scenarios from stakeholders and evidence;
3. construct coherent outcome, capability, ownership, data, semantic, interface, platform, governance, security, operational, deployment, economic, transition, and lifecycle views;
4. allocate responsibilities to domains, products, platforms, services, controls, people, and providers with explicit decision rights;
5. define future interfaces and data products through semantics, behavior, service, policy, evidence, change, and closure contracts;
6. distinguish invariants, guardrails, implementation choices, assumptions, unknowns, and deferred decisions;
7. evaluate target coherence, organizational and technical feasibility, economics, reversibility, recovery, and transition viability;
8. trace target claims to outcomes, constraints, decisions, evidence, acceptance criteria, dependencies, and review triggers;
9. govern target versions, conformance, validation, exceptions, drift, and supersession as evidence changes; and
10. retire obsolete target artifacts and prevent stale designs from authorizing current work or reviving closed architecture.

## Core Exposition

**Charter the target decision.** Name sponsor, decision authority, affected stakeholders, outcomes, scope, horizon, risk tolerance, constraints, resources, evidence, review cadence, and prohibited claims. “Design the future data platform” is a solution-shaped request, not a sufficient charter.

**Anchor in observed current state.** Use inventories, flows, contracts, configurations, runtime evidence, incidents, costs, recovery results, consumer journeys, and maturity findings. Preserve current strengths as well as debt. A target based on assumed current state creates imaginary gaps and unsafe dependencies.

**Preserve the selected alternatives analysis.** Link the target to considered options, mandatory gates, trade-offs, uncertainty, experiments, dissent, and decision receipts. A target diagram should not erase why a centralized, decentralized, mesh, fabric, warehouse, lakehouse, hybrid, or incremental choice was accepted or rejected.

**Define target horizons.** Separate near decision constraints, medium operating changes, and longer directional intent without treating dates as delivery labels. Give each horizon assumptions, decisions, qualities, commitments, unknowns, and review triggers. Farther horizons normally contain fewer irreversible details.

**Write outcome statements first.** Name the user or mission decision, current limitation, desired condition, measure, population, time, risk, and owner. “Single source of truth,” “data democratization,” “AI ready,” and “real time” are slogans until bounded this way.

**Translate outcomes into capabilities.** Determine what the organization must be able to do: identify data, preserve meaning, publish products, enforce contracts, integrate changes, authorize purposes, observe flows, recover history, attribute cost, or retire use. Capabilities remain distinct from the products or technologies that may implement them.

**Derive constraints explicitly.** Include law, policy, ethics, sovereignty, contractual duties, safety, security, privacy, latency, consistency, availability, recovery, budget, skill, procurement, compatibility, physical limits, and deadlines. Record source, interpretation authority, scope, conditions, and expiry.

**Use principles as decision rules.** A principle should contain statement, rationale, implications, counterexamples, conformance evidence, exception authority, and review. “Prefer open standards” is incomplete until openness, required operations, exit, and justified exceptions are testable.

**Separate invariants from preferences.** Identity isolation, lawful purpose, traceable correction, or bounded loss may be invariants. A particular database, cloud region, or orchestration product may be a current implementation preference. Misclassifying preferences as invariants freezes avoidable coupling.

**Describe a concept of operations.** Walk through normal publication and consumption, schema change, late correction, policy update, demand surge, dependency loss, regional outage, security incident, restoration, provider exit, and product retirement. Allocate human and automated responsibilities in every state.

**Identify stakeholders by concern.** Include decision makers, domain owners, producers, consumers, platform operators, security, privacy, risk, legal, finance, procurement, support, auditors, external partners, and people represented in the data. A view exists to answer their material questions, not to satisfy a template.

**Choose viewpoints deliberately.** Define concerns, audience, notation, model elements, relationships, consistency rules, and evidence for each viewpoint. Avoid both one overloaded diagram and dozens of unmaintained pictures. Keep the minimum view set needed to expose decisions and risks.

**Build an outcome and capability view.** Trace stakeholder outcomes and constraints to capabilities, owners, measures, and dependencies. This view prevents technical components from becoming ends in themselves and reveals a target that depends on an unfunded capability.

**Build an ownership and operating-model view.** Show decision rights, domain boundaries, product ownership, platform responsibilities, federated forums, support, funding, incident authority, policy authorship, exception approval, and closure. A team label without authority and capacity is not allocation.

**Build a domain and product topology.** Define domain purposes, bounded models, products, consumers, upstream sources, downstream decisions, shared kernels, mappings, conformed models, and cross-domain obligations. Preserve legitimate differences instead of drawing one universal enterprise model.

**Build semantic views.** Identify concept and model authorities, stable identifiers, vocabulary and code sets, grain, keys, units, time, population, null meanings, mappings, loss, versions, and historical interpretation. A logical entity relationship diagram alone cannot govern cross-context meaning.

**Build information-lifecycle views.** Trace collection, generation, validation, transformation, use, sharing, correction, retention, legal hold, archival, deletion, and proof of deletion. Relate each state to owner, purpose, policy, lineage, quality, access, and recovery.

**Build interface and flow views.** Show producer, consumer, direction, purpose, operation, data product or event, semantics, transport, service, ordering, duplication, errors, policy, lineage, versioning, and closure. Draw control, metadata, identity, policy, and evidence flows as well as business data.

**Write target contracts.** Bind interface identity to semantic and physical schemas, quality, service, roles, access, purpose, support, change, compatibility, incidents, evidence, cost, and retirement. A target contract may remain implementation-independent in transport while being precise about required behavior.

**Build platform and deployment views.** Allocate storage, compute, streaming, batch, query, metadata, identity, policy, observability, network, regions, tenants, isolation, control planes, data planes, and external dependencies. Label managed, owned, shared, replicated, cached, ephemeral, and recoverable state.

**Place workloads, not brands.** Assign reporting, operational analytics, exploration, machine learning, streaming, exchange, and archival according to data shape, volume, latency, consistency, concurrency, mutability, semantics, policy, service, skills, and economics. Record why the placement holds and when it should change.

**Distinguish logical and physical targets.** Logical targets establish responsibilities, products, semantics, capabilities, and interfaces. Physical targets establish deployable components, technologies, regions, networks, and configurations. Keep traceability between them without allowing one to masquerade as the other.

**Design shared control planes.** Catalog, contract registry, policy distribution, identity, lineage, orchestration, telemetry, and cost allocation can connect heterogeneous data planes. Model availability, consistency, versioning, tenancy, blast radius, bootstrap, degraded operation, and recovery.

**Embed governance in flows.** Allocate classification, consent, purpose, retention, quality, contract, access, change, exception, and deletion decisions to named points. Define authoritative inputs, policy versions, enforcement behavior, evidence, appeals, safe failure, and recovery.

**Engineer security from the target boundary.** Identify assets, actors, trust zones, privileges, attack paths, supply chain, secrets, isolation, encryption, monitoring, response, recovery, and retirement. Threats cross data, control, management, metadata, backup, and human paths.

**Engineer privacy from data use.** Model people, purposes, collection, inference, joins, disclosure, retention, rights, consent or other authority, jurisdiction, minimization, explainability, correction, deletion, and downstream propagation. A centralized privacy service cannot compensate for an incoherent use model.

**Specify quality as consumer fitness.** Define dimensions, metrics, populations, thresholds, observation windows, owners, actions, and consequences at producer, transformation, product, and decision boundaries. “Trusted data” is not a target condition.

**Write quality scenarios.** Cover normal use, peak demand, source delay, malformed change, unknown code, policy denial, partial outage, regional loss, compromised credential, model change, consumer migration, restore, and exit. Specify environment, stimulus, response, response measure, evidence, and owner.

**Design failure behavior.** State which functions degrade, stop, retry, queue, quarantine, shed load, serve stale results, fail closed, or require human decision. Preserve data and decision semantics during partial failure. The target must include undesirable states, not only the happy path.

**Design recovery as a target state.** Specify authoritative recovery points, dependencies, ordering, identities, policy versions, contracts, reference data, keys, capacity, reconciliation, validation, consumer acceptance, and nonactivation of retired paths. A backup icon is not recovery architecture.

**Model observability and evidence.** Define stable identities, required signals, lineage, policy decisions, contract results, quality measurements, service indicators, cost, sampling, retention, access, and cross-boundary correlation. Every critical target claim should name evidence that can confirm or falsify deployment behavior.

**Model economics explicitly.** Include discovery, design, procurement, migration, dual operation, licenses, compute, storage, network, platform, domain capacity, quality, security, support, incidents, recovery, commitments, stranded assets, and exit. Allocate costs and define units tied to products, consumers, workloads, or outcomes.

**Include organizational capacity.** Target ownership consumes domain expertise, engineering, product management, platform support, security, privacy, finance, procurement, and on-call attention. A technically feasible target can remain organizationally impossible or economically irrational.

**Choose the right precision.** Fix semantics, authorities, mandatory interfaces, policy, service, and evidence where interoperability or risk demands it. Use guardrails and reference patterns where local experimentation is safe. Defer vendor or component choices when future evidence has material value.

**Record deferred decisions.** State options, current safe default, evidence needed, owner, dependency, irreversible boundary, and latest responsible date. A box labeled “future service” without this record is an unowned gap.

**Maintain an assumption register.** Record proposition, source, scope, confidence, sensitivity, validation, owner, expiry, and consequence if false. Examples include volume growth, domain staffing, platform adoption, price, jurisdiction, vendor feature, partner compatibility, and migration rate.

**Design for reversibility.** Identify portability of data, semantics, contracts, policies, metadata, lineage, identities, skills, and operations. Bound extraction, validation, consumer migration, egress, commitments, service impact, and permitted loss. Open storage is only one part of exit.

**Prove internal coherence.** Check that every outcome has capabilities; every capability has accountable allocation; every product has consumers and contracts; every flow has policy and evidence; every quality scenario maps to structure and operation; every dependency has service and recovery; and every commitment has economics and exit.

**Use bidirectional traceability.** Trace outcome to scenario, capability, decision, view element, contract, policy, implementation constraint, conformance check, transition, and observed result—and back. Traceability should answer impact questions, not merely create identifiers.

**Test cross-view consistency.** A product cannot be domain-owned in one view and centrally changed in another without an explicit joint rule. A deleted dataset cannot remain a recovery dependency. A regional boundary cannot conflict with a global replica. Automate mechanical checks and review semantic conflicts.

**Express machine-testable rules carefully.** Validate contract registration, approved regions, encryption, identity, retention, lineage, tagging, dependency, and telemetry where authoritative inputs exist. Policy-as-code implements a target rule; it does not establish that the rule is legitimate, complete, or beneficial.

**Run architecture scenarios and prototypes.** Use production-shaped data, workload traces, failure injection, policy changes, schema evolution, recovery, and exit to target decision-changing uncertainty. A prototype validates selected mechanisms and assumptions, not the whole architecture.

**Check transition feasibility before approval.** Inventory current-to-target gaps, dependency ordering, bridge interfaces, dual authority, data reconciliation, consumer migration, policy continuity, capacity, funding, rollback, recovery, and retirement. If no credible transition exists, the target is not actionable.

**Do not confuse target with transition.** Temporary adapters, replicas, dual writes, compatibility layers, and manual controls may be necessary but should have owners and expiry. Conversely, the long-term target may retain multiple platforms or mappings intentionally. Label each state by durable purpose.

**Use multiple horizons without one grand reveal.** Define coherent target profiles at decision-relevant horizons, each useful if later assumptions change. Avoid a distant perfect architecture whose value arrives only after every dependency completes.

**Validate with stakeholders and operators.** Walk real decisions and adverse scenarios with people who produce, consume, operate, govern, finance, audit, and are affected by data use. Agreement shows shared understanding; evidence and trials remain necessary.

**Baseline only governed decisions.** A baseline records approved target components, rationale, authority, evidence, assumptions, exceptions, and open decisions under change control. It is not immutable. Changes create new versions and impact analysis rather than silent diagram edits.

**Define conformance levels.** Distinguish intended, designed, implemented, deployed, observed, and outcome-validated. A component can match the target schema while violating ownership, service, policy, or user outcomes. Report partial and exception states explicitly.

**Govern divergence.** Detect drift in infrastructure, products, contracts, policies, flows, metadata, ownership, and costs. Classify it as approved evolution, temporary exception, incident, obsolete target, or nonconformance. Do not force deployment back to a target disproved by evidence.

**Set reconsideration triggers.** Revisit the target when laws, threats, strategy, demand, prices, staffing, provider capabilities, acquisitions, incidents, recovery results, outcomes, or critical assumptions cross declared thresholds. Scheduled review alone may be too late.

**Preserve rejected choices and dissent.** Record why plausible alternatives lost, which evidence was disputed, who bears adverse effects, and what would reverse the decision. Future teams need the decision boundary, not merely the selected picture.

**Plan supersession and closure.** Mark obsolete versions, notify dependent decisions, remove them from standards portals and automated approvals, retire related exceptions and interfaces, reconcile open commitments, preserve required receipts, and test that restored tooling cannot reauthorize a closed target.

## Definitions and Notation

Let `T = (U, H, C, O, D, I, P, G, Q, E, M, R, L)` be the target-state architecture defined in the review. Let `V_t` be its immutable version, `h` its target horizon, `S` stakeholders, `K` concerns and constraints, `A` architecture elements, and `W` views.

Represent a target claim as:

`TC = (id, outcome, scope, h, owner, element, rationale, assumptions, dependencies, acceptance, transition, trigger)`

A claim without an outcome, owner, acceptance condition, or transition relationship is incomplete even if a diagram contains the element.

Represent a view as `View(vp, S_v, K_v, A_v, R_v, N_v)` where `vp` is the viewpoint, `S_v` stakeholders, `K_v` concerns, `A_v` elements, `R_v` relationships, and `N_v` notation and consistency rules. Coverage by many views does not imply coherence.

Represent a quality scenario as `QS = (source, stimulus, environment, artifact, response, measure, evidence, owner)`. Terms such as available, scalable, secure, interoperable, and maintainable become architecture claims only through bounded scenarios or equivalent acceptance conditions.

Let `Trace(x, y, type, rationale, evidence, version)` relate outcomes, constraints, capabilities, decisions, elements, contracts, controls, tests, transitions, and results. Bidirectional navigation is required for impact analysis; graph reachability alone does not prove semantic validity.

Define coherence `Coherent(T)` to require no known material contradiction among outcomes, constraints, capability allocations, owners, semantic authorities, views, interfaces, policies, quality scenarios, dependencies, economics, transitions, recovery, and closure. Absence of detected contradiction is not proof of completeness.

Define transition feasibility `Reachable(C_0, T, B)` to mean at least one evidence-backed transition path can move current state `C_0` toward `T` under bounds `B` for time, capacity, cost, service, loss, policy, risk, rollback, and recovery. DARCH-093 develops this path in detail.

Represent a deferred decision as `DD = (question, options, default, evidence, owner, dependency, irreversible_boundary, due, trigger)`. Expired deferral becomes a target risk or explicit exception.

Define `Closed(V_t)` to require no active or recoverable standard, portal, rule, contract, decision, exception, route, credential, or automation can treat superseded version `V_t` as current authority, while required historical evidence remains controlled.

## Mechanisms, Invariants, or Proof Structure

Use the following assurance gates.

**Charter gate.** Name authority, stakeholders, outcomes, scope, horizons, risk tolerance, constraints, resources, evidence, review, and prohibited claims.

**Baseline gate.** Verify current capabilities, inventories, flows, semantics, interfaces, controls, runtime behavior, incidents, cost, recovery, debt, and strengths.

**Outcome gate.** Bind each desired condition to users, decisions, measures, populations, time, risk, and accountable owners.

**Alternative gate.** Preserve credible options, gates, trade-offs, experiments, uncertainty, rejected choices, dissent, and selection rationale.

**Capability gate.** Trace outcomes and constraints to coherent capabilities, dependencies, organizational capacity, funding, and allocation.

**View gate.** Cover stakeholder concerns through consistent outcome, ownership, domain, semantic, lifecycle, interface, platform, policy, security, operational, deployment, economic, transition, and closure views.

**Interface gate.** Define producer, consumer, semantics, schema, behavior, service, failure, policy, evidence, versioning, change, compatibility, cost, and retirement.

**Scenario gate.** Test normal, peak, change, malformed, denied, partial-failure, disaster, incident, restore, migration, provider-exit, and closure conditions with measurable responses.

**Governance gate.** Allocate decision rights, policy authority, enforcement points, exceptions, evidence, appeals, safe failure, change, and recovery.

**Security and privacy gate.** Model trust, identity, privilege, isolation, purpose, movement, joining, disclosure, retention, deletion, supply chain, response, recovery, and affected people.

**Operations gate.** Define service, quality, telemetry, lineage, cost, capacity, support, incidents, dependencies, degraded modes, reconciliation, and recovery.

**Economics gate.** Fund discovery, design, build, migration, dual operation, run, change, incident, recovery, commitments, capacity, stranded assets, and exit.

**Uncertainty gate.** Record assumptions, unknowns, deferred decisions, confidence, sensitivity, validation, owners, due dates, and consequences.

**Coherence gate.** Check allocations, semantics, relationships, policies, scenarios, dependencies, economics, transition, recovery, and closure across all views.

**Traceability gate.** Connect outcomes, constraints, capabilities, decisions, elements, contracts, controls, evidence, transitions, deployments, and observed results bidirectionally.

**Feasibility gate.** Demonstrate at least one bounded migration path with capacity, service continuity, reconciliation, rollback, recovery, funding, and retirement.

**Change gate.** Version baselines, detect divergence, distinguish nonconformance from disproved target, govern exceptions, preserve dissent, and trigger reconsideration.

**Closure gate.** Retire obsolete target artifacts, standards, rules, contracts, exceptions, routes, credentials, commitments, and recoverable authority while retaining required history.

### Executable evidence: target-claim readiness

The following program classifies ten invented target claims against six mandatory design gates.

<!-- bijux-verify: {"id":"target-claim-readiness","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"claims=10\nready=4\nmissing_outcome=1\nmissing_owner=1\nmissing_interface=1\nunverifiable_scenario=1\nunfunded_lifecycle=1\nmissing_transition_path=1\narchitecture_views=8\nstakeholder_groups=7\ndecision_horizons=3\ntraceability_receipts=10\ndecision_events=10\n","stderr":""}} -->
```python
claims = [
    {"view": "outcome", "stakeholders": {"consumer", "executive"}, "horizon": "near", "outcome": True, "owner": True, "interface": True, "scenario": True, "funded": True, "transition": True},
    {"view": "ownership", "stakeholders": {"domain", "platform"}, "horizon": "near", "outcome": True, "owner": True, "interface": True, "scenario": True, "funded": True, "transition": True},
    {"view": "semantic", "stakeholders": {"domain", "consumer"}, "horizon": "medium", "outcome": True, "owner": True, "interface": True, "scenario": True, "funded": True, "transition": True},
    {"view": "deployment", "stakeholders": {"platform", "security"}, "horizon": "medium", "outcome": True, "owner": True, "interface": True, "scenario": True, "funded": True, "transition": True},
    {"view": "platform", "stakeholders": {"platform"}, "horizon": "far", "outcome": False, "owner": True, "interface": True, "scenario": True, "funded": True, "transition": True},
    {"view": "governance", "stakeholders": {"security", "executive"}, "horizon": "near", "outcome": True, "owner": False, "interface": True, "scenario": True, "funded": True, "transition": True},
    {"view": "interface", "stakeholders": {"domain", "consumer"}, "horizon": "medium", "outcome": True, "owner": True, "interface": False, "scenario": True, "funded": True, "transition": True},
    {"view": "operations", "stakeholders": {"operator", "consumer"}, "horizon": "near", "outcome": True, "owner": True, "interface": True, "scenario": False, "funded": True, "transition": True},
    {"view": "governance", "stakeholders": {"security", "finance"}, "horizon": "far", "outcome": True, "owner": True, "interface": True, "scenario": True, "funded": False, "transition": True},
    {"view": "deployment", "stakeholders": {"operator", "finance"}, "horizon": "medium", "outcome": True, "owner": True, "interface": True, "scenario": True, "funded": True, "transition": False},
]

def evaluate(claim):
    if not claim["outcome"]:
        return "missing_outcome"
    if not claim["owner"]:
        return "missing_owner"
    if not claim["interface"]:
        return "missing_interface"
    if not claim["scenario"]:
        return "unverifiable_scenario"
    if not claim["funded"]:
        return "unfunded_lifecycle"
    if not claim["transition"]:
        return "missing_transition_path"
    return "ready"

results = [evaluate(claim) for claim in claims]
print(f"claims={len(claims)}")
for outcome in ["ready", "missing_outcome", "missing_owner", "missing_interface", "unverifiable_scenario", "unfunded_lifecycle", "missing_transition_path"]:
    print(f"{outcome}={results.count(outcome)}")
print(f"architecture_views={len({claim['view'] for claim in claims})}")
print(f"stakeholder_groups={len(set().union(*(claim['stakeholders'] for claim in claims)))}")
print(f"decision_horizons={len({claim['horizon'] for claim in claims})}")
print(f"traceability_receipts={len(claims)}")
print(f"decision_events={len(results)}")
```

The output reports ten claims, four ready and one of each declared failure, eight architecture views, seven stakeholder groups, three decision horizons, ten receipts, and ten decisions.

The evidence is deliberately narrow. Invented Booleans, labels, and sets establish deterministic gate order and counts only. They do not establish that an outcome matters, an owner has authority, an interface is sufficient, a scenario is representative, lifecycle funding exists, a transition is safe, views agree, or the target is feasible or valuable. Production assurance requires current-state evidence, decision records, stakeholder validation, coherent models, executable contracts and policies, quality scenarios, prototypes, cost and capacity evidence, transition and rollback design, recovery exercises, and observed outcomes.

## Alternatives and Trade-Offs

**Technology-led target.** Procurement and implementation direction become concrete quickly. Outcomes, semantics, ownership, operating model, and transition can be forced around products.

**Capability-led target.** Outcomes and responsibilities remain portable across implementations. Teams may lack enough technical specificity for interoperability, feasibility, cost, or procurement.

**Principles-and-guardrails target.** Local choice and evolutionary learning are strong. Inconsistent interpretation, duplicated capability, and unresolved cross-boundary contracts can grow.

**Detailed prescriptive blueprint.** Integration and conformance are clearer. Assumptions age, local context is suppressed, and costly commitments occur early.

**One enterprise target.** Shared direction and portfolio reasoning improve. Domain, jurisdiction, workload, and horizon differences can disappear into generic boxes.

**Federated target profiles.** Local outcomes and constraints remain visible. Cross-profile consistency, shared services, policy, and dependency governance become harder.

**Logical target only.** Durable semantics, capabilities, and interfaces avoid premature vendor decisions. Performance, deployment, security, recovery, and cost feasibility can remain untested.

**Physical target only.** Deployable components and commitments are visible. Technology topology can hide business decisions and semantic ownership.

**One distant horizon.** A simple north star coordinates narrative. Uncertainty, delayed value, dependency concentration, and brittle sequencing increase.

**Multiple bounded horizons.** Near decisions stay concrete while distant choices remain flexible. Traceability and consistency across horizons require active governance.

**Centralized target authority.** Cross-domain coherence and standards can improve. Decision queues, semantic errors, and weak local ownership can grow.

**Domain-owned target evolution.** Local learning and accountability improve. Shared interfaces, policy, cost, and common failures require federated controls.

**Architecture documents.** Human reasoning, nuance, and explanation remain accessible. Drift, mechanical inconsistency, and conformance evidence are difficult.

**Architecture as code.** Versioning, validation, generation, and automation improve. Executable schemas can create false confidence and omit intent or stakeholder concerns.

**Immediate implementation commitment.** Delivery begins quickly. Decision-changing uncertainty and transition hazards remain unexplored.

**Prototype before commitment.** Performance, integration, policy, recovery, and operator evidence improve. Prototypes cost time and can be mistaken for production assurance.

**Optimize for reversibility.** Learning and provider exit remain viable. Some short-term cost or specialized capability may be sacrificed.

**Optimize for efficiency.** Standardization and commitments can lower unit cost. Concentration, lock-in, systemic failure, and change cost can rise.

**Target conformance governance.** Portfolio consistency and risk control improve. Teams can satisfy checks while missing outcomes or route around burdensome rules.

**Outcome-based evolutionary governance.** Evidence can revise disproved targets. Comparability, funding commitments, and coordinated long-lived interfaces need stable baselines.

## Failure Modes and Misconceptions

1. **“The target is the future technology stack.”** Architecture includes outcomes, ownership, semantics, behavior, policy, and lifecycle.
2. **“A target diagram is the architecture.”** One view cannot answer every stakeholder concern.
3. **“The target should contain every implementation detail.”** Premature precision destroys learning and portability.
4. **“The target should remain solution-neutral.”** Some interfaces, controls, and qualities require implementable precision.
5. **“Cloud is a target state.”** It is a placement and service context, not a complete architecture.
6. **“A lakehouse is a target state.”** Ownership, products, consumers, contracts, policy, and operations remain.
7. **“Mesh is a target topology.”** Its operating principles need technical and organizational realization.
8. **“One source of truth is a sufficient outcome.”** Scope, authority, time, semantics, and consumers are undefined.
9. **“Real time is a requirement.”** A bounded freshness and latency scenario is required.
10. **“AI ready is an architecture quality.”** Data, model, decision, risk, service, and evidence conditions must be named.
11. **“The current state contains only debt.”** Working capabilities and constraints are transition assets.
12. **“The target can ignore the current state.”** Reachability and gap claims require an observed baseline.
13. **“The chosen option needs no retained rationale.”** Rejected alternatives define decision boundaries.
14. **“Far horizons deserve more detail.”** Uncertainty usually warrants fewer irreversible choices.
15. **“All stakeholders want the same target.”** Concerns, authority, costs, and adverse effects conflict.
16. **“A template determines the required views.”** Views exist for material stakeholder concerns.
17. **“More diagrams improve completeness.”** Unmaintained or inconsistent views reduce trust.
18. **“A domain box creates ownership.”** Authority, capacity, funding, support, and closure are required.
19. **“A product box creates consumers.”** Purpose, contracts, adoption, service, and outcomes are required.
20. **“A canonical model resolves semantics.”** Authority, mappings, bounded contexts, and loss remain.
21. **“An arrow defines an interface.”** Semantics, behavior, failure, policy, service, and evolution are absent.
22. **“A schema defines a target contract.”** Quality, roles, support, access, change, evidence, and closure remain.
23. **“A catalog makes data discoverable.”** Metadata correctness, understanding, access, and use matter.
24. **“Lineage will be added after delivery.”** Stable identities and instrumentation boundaries must be designed.
25. **“One control plane always simplifies governance.”** Blast radius, tenancy, availability, and recovery may worsen.
26. **“A common platform creates common meaning.”** Physical consistency cannot assign semantic authority.
27. **“Shared infrastructure requires central ownership.”** Domains can own products on common services.
28. **“Domain ownership requires separate infrastructure.”** Semantic authority and physical placement are distinct.
29. **“Encryption completes security architecture.”** Identity, privilege, isolation, supply chain, detection, response, and retirement remain.
30. **“A privacy service makes every data use legitimate.”** Purpose, minimization, joins, retention, and affected people remain.
31. **“Trusted data is measurable.”** Consumer-specific quality dimensions and thresholds are needed.
32. **“Availability is one percentage.”** Scope, window, dependency, degraded mode, and consumer effect matter.
33. **“Backups define recovery.”** Ordering, policy, semantics, reconciliation, validation, and service matter.
34. **“The target needs only normal operation.”** Stress, change, failure, incident, restore, and exit shape structure.
35. **“Observability means deploying a collector.”** Identity, signals, coverage, semantics, action, and retention matter.
36. **“Consolidation is automatically cheaper.”** Migration, coordination, concentration, commitments, and exit can dominate.
37. **“Open storage guarantees reversibility.”** Contracts, policies, metadata, skills, and consumers also bind exit.
38. **“Organizational capacity will follow architecture.”** Ownership and operation consume scarce skills and attention.
39. **“Unknowns should be resolved before approval.”** Some choices are safer and more valuable to defer explicitly.
40. **“A placeholder is a deferred decision.”** It lacks options, owner, evidence, safe default, and due date.
41. **“Assumptions are harmless annotations.”** False assumptions can invalidate the architecture.
42. **“Traceability proves correctness.”** Connected claims can still be wrong or incomplete.
43. **“Automated checks prove architecture conformance.”** Only encoded and observed conditions are tested.
44. **“A prototype proves the target.”** It validates bounded mechanisms and configurations.
45. **“A good target will reveal its migration path.”** Transition feasibility requires separate design and evidence.
46. **“Dual writes belong in the target.”** They may be temporary transition mechanisms with expiry.
47. **“Stakeholder approval proves outcomes.”** Shared understanding is not operational validation.
48. **“A baseline must never change.”** Governed evolution creates new versions and impact analysis.
49. **“Deployment divergence is always wrong.”** It may reveal that the target is obsolete or disproved.
50. **“Archiving a diagram closes the target.”** Standards, rules, contracts, exceptions, portals, and recovery authority may remain.

## Worked Examples

### Example 1

A retailer's target begins with a two-hour inventory decision outcome, not a streaming product. Quality scenarios show stores tolerate five-minute freshness but require local degraded operation during network loss. The target allocates event publication centrally supported by a platform while stores retain bounded state and reconcile after recovery.

### Example 2

A bank draws customer as one enterprise entity. Semantic review finds legal party, account holder, beneficiary, prospect, and authenticated user have different owners and valid times. The target replaces universal truth with bounded models, stable identities, a small shared kernel, and directional mappings with explicit loss.

### Example 3

A shared lakehouse target lists domains but assigns platform administrators authority over product schema changes. Ownership and interface views conflict. The coherence review gives domains semantic change authority, keeps platform authority over safe infrastructure constraints, and defines joint rules for shared contracts.

### Example 4

A health provider's target profile requires purpose-limited access and regional retention. The flow view exposes a global metadata service receiving sensitive sample values. The target changes metadata collection to minimize payloads, partitions policy and audit evidence by jurisdiction, and adds a recovery scenario that prevents cross-region restoration.

### Example 5

A target says all queries use federation. Production-shaped trials show filtered discovery succeeds while a cross-source clinical join overloads an operational database. The revised target retains federation for bounded exploration and materializes the recurring join as an owned product with freshness and policy contracts.

### Example 6

A platform selection depends on a promised multi-engine table feature. The feature is recorded as an assumption with required operations, exact versions, validation fixture, owner, and procurement boundary. Failure before that boundary switches to a portable subset rather than invalidating the whole target.

### Example 7

A distant target specifies a vendor scheduler, catalog, and policy engine even though procurement is two years away. The architecture retains required orchestration, metadata, decision, evidence, and interface capabilities but defers products until benchmark, integration, exit, and cost evidence is timely.

### Example 8

A finance target is logically coherent but requires every domain to operate products without funded engineers. Capability allocation and economics expose the gap. The revised target gives domains semantic and service ownership while a shared platform team operates the common runtime and supports bounded product onboarding.

### Example 9

A migration prototype copies data and passes row counts. Target scenarios also require historical corrections, policy version replay, consumer compatibility, regional recovery, and exit. The expanded experiment reveals incompatible time semantics before a production commitment.

### Example 10

A superseded target is removed from the architecture repository, but an old standards portal still approves its schema and a restored automation service republishes its rules. Closure revokes integrations, versions authority, removes obsolete conformance paths, preserves decision receipts, and tests recovery nonactivation.

## Cross-Program Connections

- [Data Engineering](../../19-data-engineering/ROADMAP.md) realizes target products, contracts, flows, transformations, quality, lineage, orchestration, reconciliation, migration, and retirement.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md) tests storage, streaming, batch, query, consistency, scaling, isolation, metadata, and recovery assumptions under production-shaped conditions.
- [Database Engineering](../../18-database-engineering/ROADMAP.md) refines logical and physical models, transactions, constraints, indexes, partitions, query behavior, backups, restoration, and schema evolution.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) turns target arrows into behavioral contracts, compatibility policies, errors, service objectives, observability, and client migrations.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns shared capabilities, control planes, self-service paths, tenancy, policy, telemetry, cost, support, recovery, and platform lifecycle.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) shapes trust boundaries, identity, access, isolation, supply chain, monitoring, response, recovery, and secure retirement.
- [Network Engineering](../../24-network-engineering/ROADMAP.md) grounds target topology in connectivity, segmentation, latency, throughput, routing, egress, regional failure, and recovery behavior.
- [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) challenges target claims with consistency, partial failure, clocks, ordering, duplication, coordination, convergence, replay, and common-mode risk.
- [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md) connects viewpoints, quality scenarios, modular boundaries, decisions, fitness functions, evolutionary architecture, and technical debt.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies stakeholder, concept-of-operations, functional allocation, interface, trade-study, verification, validation, configuration, risk, and lifecycle discipline.

## References

1. The Open Group, [TOGAF Standards](https://publications.opengroup.org/standards/togaf), maintained enterprise-architecture standards, methods, guides, templates, patterns, and reference material.
2. NASA, [Systems Engineering Handbook](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf), architecture concepts, functions, interfaces, concepts of operation, stakeholder feedback, and lifecycle design.
3. NIST, [SP 1301: Creating and Using Organizational Profiles](https://csrc.nist.gov/pubs/sp/1301/final), current and target outcomes tailored to mission, stakeholders, threats, and requirements.
4. NIST, [Privacy Framework 1.1](https://www.nist.gov/privacy-framework/using-privacy-framework-11), privacy outcomes, profiles, implementation context, and risk management.
5. arc42, [Architecture Documentation](https://docs.arc42.org/home/), goals, constraints, context, strategy, structures, runtime, deployment, decisions, quality, risks, and terminology.
6. arc42, [Quality Requirements](https://docs.arc42.org/section-10/), usage, change, and failure scenarios with measurable response conditions.
7. C4 Model, [Visualising Software Architecture](https://c4model.com/), hierarchical context, container, component, code, dynamic, and deployment views.
8. Bitol, [Open Data Contract Standard](https://bitol-io.github.io/open-data-contract-standard/latest/), machine-readable schema, quality, service, role, support, and infrastructure contracts.
9. W3C, [Data Catalog Vocabulary 3](https://www.w3.org/TR/vocab-dcat-3/), catalogs, datasets, distributions, services, relationships, versions, and profiles.
10. OpenLineage, [Object Model](https://openlineage.io/docs/spec/object-model/), dataset, job, run, event, namespace, name, and facet identities.
11. Open Policy Agent, [Policy Language](https://www.openpolicyagent.org/docs/policy-language), structured policy decisions, rules, tests, and runtime implementation context.
12. OpenTelemetry, [Specification](https://opentelemetry.io/docs/specs/otel/), signals, resources, context propagation, semantic conventions, compatibility, and versioning.
13. NIST, [SP 800-160 Volume 1 Revision 1](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final), systems-security engineering and trustworthy secure systems across the lifecycle.
14. FinOps Foundation, [FinOps Framework](https://www.finops.org/framework/), cross-functional ownership, usage and cost, value, optimization, governance, and technology decisions.
15. NASA, [Decision Analysis](https://www.nasa.gov/reference/6-8-decision-analysis/), criteria, alternatives, evaluation, uncertainty, robustness, results, and recommendation.
16. Amazon Web Services, [Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html), vendor guidance on operation, security, reliability, performance, cost, and sustainability.

## Exercises

### Exercise 1

Define a target-state architecture charter for a regulated enterprise replacing fragmented analytical platforms. Include outcomes, stakeholders, scope, horizons, constraints, current evidence, alternatives, decision authority, assumptions, prohibited claims, validation, and review triggers.

### Exercise 2

Create the minimum coherent view set for domain-owned products on shared infrastructure. Cover capabilities, ownership, domains and semantics, lifecycle, interfaces and flows, platforms and deployment, governance, security and privacy, quality and recovery, economics, transition, and closure.

### Exercise 3

Specify target contracts and quality scenarios for an order product consumed by reporting, fraud detection, operational APIs, and a partner. Include meaning, versions, service, policy, failures, corrections, evidence, change, migration, recovery, and retirement.

### Exercise 4

Evaluate the coherence and feasibility of a target using federated query, open tables, a shared catalog, policy as code, and regional stores. Identify assumptions, cross-view conflicts, workload tests, organizational capacity, lifecycle cost, transition dependencies, rollback, recovery, and reconsideration triggers.

### Exercise 5

Design target-state governance from approval through supersession. Include baselines, traceability, conformance levels, executable rules, exceptions, drift, stakeholder validation, decision records, model versions, impact analysis, evidence, closure, and restored-system nonactivation.

## Answers to the Exercises

### Answer 1

State the user and mission outcomes—such as reproducible regulated reporting, bounded decision latency, lawful sharing, and reduced reconciliation—along with populations, measures, owners, and horizons. Include executives, domain and product owners, consumers, platform and operations teams, security, privacy, legal, finance, procurement, audit, partners, and affected people. Bound domains, products, jurisdictions, workloads, and interfaces. Record current inventories, runtime flows, incidents, cost, recovery, and maturity evidence. Preserve baseline repair, strengthened warehouse, shared open-table, fabric-capability, and explicit hybrid alternatives with gates and dissent. Identify legal, semantic, security, privacy, service, recovery, budget, skill, and timing constraints. Version assumptions and validation. Prohibit certification, guaranteed savings, and future-outcome claims. Assign approval and reconsideration authority.

### Answer 2

Use an outcome-capability view that traces decisions to required abilities; an operating-model view with semantic, platform, policy, support, funding, incident, and closure authority; and a domain-product view with bounded models, consumers, shared kernels, mappings, and conformed products. Add information-lifecycle and flow views for collection through deletion, target-contract views for behavior and change, platform and deployment views for control and data planes, and security-privacy views for trust, purpose, access, movement, retention, and response. Quality and operational views cover normal, stress, failure, recovery, and exit scenarios. Economic and transition views show capacity, lifecycle cost, dependencies, bridges, rollback, and retirement. Define cross-view consistency rules and trace every element to outcomes, constraints, decisions, evidence, and owners.

### Answer 3

Give the order product a stable identity, authoritative domain, population, grain, keys, money and time semantics, status model, correction rules, schema, code sets, and historical interpretation. Bind each consumer profile to purpose, fields, quality, freshness, latency, ordering, duplication, access, retention, support, cost, and version compatibility. Reporting needs complete cutoff and restatement; fraud needs low-latency events and uncertainty; operational APIs need idempotent behavior and bounded errors; the partner needs a policy-limited profile and revocation. Test malformed values, late correction, enum growth, duplicate delivery, policy denial, dependency loss, regional outage, consumer version skew, replay, restore, and termination. Emit contract, lineage, policy, quality, and service evidence. Define canary change, rollback, migration, deprecation, and closure.

### Answer 4

Test whether federated filters and joins push down for exact connectors, whether source load and partial failure meet service, whether open-table readers and writers support required evolution and delete behavior, whether catalog identities and lineage are consistent, and whether policy executes at every query, copy, cache, and recovery path. Check that domain ownership agrees with catalog and schema authority, regional rules agree with replicas and metadata, and deleted data does not remain a recovery dependency. Record assumptions about volumes, prices, provider capabilities, staffing, adoption, and regulatory stability. Price build, migration, dual operation, network, support, incident, recovery, commitments, and exit. Identify catalog, identity, policy, network, and skill dependencies. Prototype adverse scenarios. Require reversible product slices, reconciliation, old-path capacity, and recovery before commitment. Reconsider when assumptions or observed thresholds fail.

### Answer 5

Create an immutable target version containing charter, views, model identities, decisions, assumptions, contracts, quality scenarios, transition relationship, evidence, dissent, and approval. Trace outcomes and constraints bidirectionally to capability allocations, elements, interfaces, policies, conformance checks, deployments, and observed results. Distinguish intended, designed, implemented, deployed, observed, and outcome-validated states. Automate only authoritative, mechanically testable rules and keep semantic review. Give exceptions scope, risk, compensating control, owner, expiry, and removal. Classify drift as approved evolution, exception, incident, obsolete target, or nonconformance. New evidence creates impact analysis and a new baseline. Supersession removes obsolete standards, portals, rules, exceptions, contracts, routes, credentials, and automated approvals, preserves required receipts, notifies dependents, and verifies that isolated recovery cannot restore old authority.
