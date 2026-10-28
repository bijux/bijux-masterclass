---
module_id: SARCH-074
program: Software Engineering: Software Architecture
level: 2
module_number: 74
title: Incremental Decomposition
status: complete
last_verified: 2026-09-06
---

# Incremental Decomposition

## One-Page Review

### Governing question

How can architects separate a tightly connected system into clearer responsibilities through small, evidence-bearing changes while preserving business invariants, keeping one authority for mutable facts, and avoiding a distributed monolith?

### Essential definitions

- **decomposition** assigns responsibilities, information, and relations to architectural elements according to explicit criteria;
- a **decomposition seam** is a controlled interception point through which behavior or ownership can be separated, observed, and changed;
- **information hiding** assigns a likely-to-change design decision to a module whose interface conceals that decision;
- a **business capability** is an enduring ability the organization performs, independent of one process step or software product;
- a **bounded context** is a boundary within which a domain model and its language have consistent meaning;
- **logical decomposition** separates responsibilities and dependencies; **physical decomposition** separates processes, deployments, or infrastructure;
- **change coupling** is the observed tendency for elements to change together; it is evidence about coordination, not proof of one correct boundary;
- a **transactional invariant** is a condition that authoritative state transitions must preserve atomically or through an explicitly designed distributed mechanism;
- a **modular monolith** is one deployable system with enforced internal module boundaries, not an undifferentiated codebase;
- a **distributed monolith** has networked deployment units that still require coordinated change, shared authority, or lockstep operation.

### Central model, mechanism, or theorem

Represent a selected concern as a weighted graph $G=(V,E,w)$ and a candidate partition $\Pi$ of $V$. The cut is

$$
E_{\mathrm{cut}}(\Pi)=\{(u,v)\in E\mid \pi(u)\ne\pi(v)\},
$$

with weighted cut cost $C(\Pi)=\sum_{e\in E_{\mathrm{cut}}}w(e)$. The weights may represent call frequency, change coupling, data consistency, latency sensitivity, or another declared concern. Minimizing $C$ alone gives the useless one-partition solution. A valid decomposition also requires coherent responsibility, hidden volatility, explicit authority, acceptable quality behavior, and feasible team and operational ownership.

### Critical invariants

- decomposition begins from a named outcome and current evidence, not a required service count;
- each boundary has coherent responsibility, vocabulary, authority, and consumers;
- transactional and safety properties hold in every intermediate state;
- one authoritative writer exists for each mutable business fact during ownership transfer;
- logical seams are proven before physical distribution unless distribution itself is the tested need;
- cut dependencies are explicit contracts with latency, failure, consistency, and lifecycle semantics;
- preparatory abstractions are narrow, owned, observable, and removable;
- extraction order follows dependency, risk, and learning—not organizational prestige;
- temporary duplication and routing have reconciliation, expiry, and retirement evidence;
- stopping with a well-modularized system is a valid outcome when further distribution lacks value.

### Common failures

Common failures include splitting by technical layer; equating classes, tables, teams, endpoints, or nouns with services; choosing boundaries from one metric; extracting the most entangled core first; sharing a database while claiming independent authority; replacing local calls with chatty remote calls; moving code without moving decisions; creating an anemic data service; copying business rules; allowing dual writers; building a generic abstraction before identifying a seam; leaving compatibility scaffolding permanently; requiring synchronized releases; ignoring operations and support; measuring service count as progress; and continuing decomposition after the intended outcome is already met.

### Compact example

An order system changes pricing rules weekly, while fulfillment changes quarterly. Change history and domain workshops show pricing concepts are coherent, but checkout reaches pricing tables directly from twelve places. The team first creates an internal pricing interface, routes one calculation through it, characterizes current behavior, then moves callers gradually. Only after the module owns its rules and data access does the team test whether independent deployment reduces coordination enough to justify network and operational costs. Decomposition creates a trustworthy logical boundary before assuming a service boundary.

### Connections

[SARCH-073](073-versioned-contracts-and-compatibility.md) supplies mixed-version contract discipline, and [SARCH-071](071-architectural-drift-and-erosion.md) supplies dependency and authority evidence. [SARCH-075](../ROADMAP.md) next develops strangler routing and parallel-run architectures for replacement at larger boundaries.

## Governing Question

A large system is not made understandable by placing code in more repositories or processes. Decomposition succeeds when it localizes decisions and change, clarifies authority, and makes important interactions explicit at an acceptable operational cost. It fails when physical distribution preserves the old coupling while adding networks, partial failure, versioning, and coordination.

The difficult work is identifying a seam and a safe sequence. Existing systems rarely respect the boundary one would choose on a blank page. Data, transactions, user flows, build dependencies, operational procedures, and team knowledge cross prospective boundaries. Incremental decomposition must progressively create the conditions for separation rather than pretending they already exist.

## Why This Matters

Poorly chosen boundaries amplify change. A minor feature touches presentation, shared utilities, central orchestration, and one global schema. Teams wait on each other, regression scope expands, and no owner can reason locally. Parnas showed that decomposition quality depends on the criteria used and argued for modules that hide design decisions likely to change [1]. That principle remains more durable than any prescribed deployment size.

Large-batch rewrites defer evidence. They reproduce behavior incompletely, freeze product development, and discover hidden consumers late. Incremental decomposition keeps the system usable, makes one hypothesis testable at a time, and allows the organization to stop when benefit no longer exceeds cost.

Distribution also raises the consequence of mistakes. Local calls become fallible remote calls; in-memory invariants become coordination protocols; shared debugging becomes trace reconstruction; and version coexistence becomes normal. The architecture must earn those costs through a concrete outcome such as independent change, isolation, scale, security, or ownership.

## Prerequisites and Retrieval

Retrieve module, component, connector, responsibility, cohesion, coupling, information hiding, abstraction, dependency inversion, domain, business capability, bounded context, aggregate, invariant, transaction, authority, system of record, call graph, dependency graph, change coupling, strongly connected component, graph cut, interface, compatibility, idempotency, partial failure, latency budget, observability, deployment, rollback, feature flag, anti-corruption layer, and decommissioning.

SARCH-065 supplies coupling metrics and their limitations. SARCH-071 supplies observed architecture and drift analysis. SARCH-072 supplies safe state transitions, and SARCH-073 supplies compatibility windows. This chapter covers boundary discovery and incremental separation; it deliberately leaves detailed strangler traffic replacement to SARCH-075 and data migration mechanisms to SARCH-076.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish logical, code, data, process, deployment, and organizational decomposition;
2. choose decomposition criteria based on outcomes, volatility, domain meaning, authority, and quality attributes;
3. combine dependency, runtime, change, incident, and stakeholder evidence without treating one graph as truth;
4. identify candidate seams and test whether they hide a coherent decision;
5. design preparatory refactoring that creates interception and characterization without premature distribution;
6. preserve transactional invariants and one authoritative writer during ownership transfer;
7. quantify selected cut dependencies while recognizing the degeneracy and limits of cut minimization;
8. sequence extractions by risk, dependency, reversibility, and learning value;
9. detect data services, nanoservices, shared databases, chatty calls, and other distributed-monolith outcomes;
10. decide whether to extract, retain a modular monolith, merge, revise, or stop.

## Core Exposition

**Begin with the outcome.** State which pain or opportunity decomposition should address: independent release of pricing rules, isolation of image processing, restricted access to health data, regional ownership, elastic scaling of search, replacement of a supplier, or reduced coordination for a product team. Define measures and an acceptable horizon.

“Break up the monolith” is an activity without a success condition. Service count and repository count are implementation measures, not stakeholder outcomes. A decomposition can succeed entirely inside one process when it restores local reasoning and independent code ownership.

**Baseline the current system.** Inventory code and build dependencies, runtime calls, data reads and writes, transactions, schemas, messages, identities, deployments, release coordination, support paths, incidents, performance, recovery, and team ownership. Identify generated code, batch jobs, administrative tools, reports, and external consumers.

Record revision and observation windows. Static graphs include possible dependencies; traces include exercised paths; change history includes observed co-change; interviews reveal rationale and hidden work. Reconcile differences instead of selecting the cleanest artifact.

**Select decomposition criteria.** Useful criteria include information hiding, domain meaning, business capability, rate and reason for change, transactional authority, quality-attribute needs, security and privacy boundaries, failure containment, scaling profile, replaceability, and team cognitive capacity. No criterion produces a complete architecture alone.

Technical layers usually conceal little business volatility: every feature still crosses UI, logic, and data elements. A capability boundary can localize change, but capabilities may be too broad for one owner. A bounded context clarifies model meaning, yet its optimal deployment granularity may contain several modules. Preserve these distinctions.

**Find hidden decisions.** Ask what design facts callers should not know: pricing algorithm, tax source, route optimization, identity provider, file format, supplier protocol, storage engine, or risk policy. Group behavior that changes when that decision changes, and expose an interface in terms of the responsibility rather than the current implementation.

An interface named after a database table merely exports storage. An interface such as `quote_order` can own eligibility, price components, currency, validity, and evidence. The seam should reduce consumer knowledge rather than relocate the same structure.

**Model domain language.** A word such as “customer,” “order,” or “account” can have different meanings in sales, fulfillment, support, and finance. Do not force one enterprise object across contexts. Identify model invariants, lifecycle, identifiers, and translations within each boundary.

Domain workshops, event histories, workflow observation, support cases, and decision records help expose language. Nouns suggest concepts, but verbs, policies, temporal rules, and authority reveal responsibilities. Entity lists alone create data-centric services with scattered behavior.

**Map change coupling.** Analyze which files, schemas, tests, services, and teams change together for representative reasons. Separate mechanical co-change—formatting, generated files, mass renames, release metadata—from semantic co-change. Segment by feature and incident type.

High internal co-change and low external co-change may support a candidate boundary. High cross-boundary co-change can reveal either a poor seam or a missing stable contract. History reflects the current design and team process, so it cannot dictate the future architecture without interpretation.

**Map runtime coupling.** Record call frequency, payload, latency, concurrency, failure, retry, ordering, fan-out, and critical-path position. A boundary crossed once per order is different from one crossed for every item and rule. Batch and asynchronous interactions may reduce temporal coupling while adding staleness and recovery complexity.

Do not assume a local call can become a remote call unchanged. Define latency budgets, timeout hierarchy, idempotency, backpressure, partial failure, authorization, observability, and capacity. If the interaction remains extremely chatty and transactional, the proposed boundary may be wrong or premature.

**Map data authority.** For each mutable business fact, identify the authoritative decision and writer, readers, derived copies, invariants, transaction scope, retention, and recovery. Tables rarely align automatically with domain boundaries. One table may mix concepts; one invariant may span several tables.

Decomposition does not require an immediate physical database split, but it requires controlled ownership. Other modules must not retain arbitrary writes to owned data. Encapsulate access, inventory consumers, and make violations visible before transferring storage.

**Preserve transactional invariants.** If an invariant requires atomic decisions over candidate boundaries, consider keeping the behavior together, redesigning the invariant, assigning one coordinator, using reservations or escrow, or accepting a clearly modeled distributed protocol. Do not replace a transaction with eventual consistency as a slogan.

State intermediate authority. During extraction, one component remains authoritative. Shadow calculations can compare without committing. Dual writes need failure, ordering, idempotency, and reconciliation design; they are not a default shortcut. SARCH-076 treats data transfer in depth.

**Create a candidate boundary map.** Draw elements and relations for code, runtime, data, deployment, and team views. Propose several partitions. For each, list hidden decisions, owned language, inward and outward dependencies, invariants, expected changes, quality consequences, and organizational owner.

Calculate selected graph cuts only when weights have defensible meaning. A low static-edge cut may have high runtime cost; a low call-volume cut may cross critical authority. Preserve separate measures rather than manufacturing one weighted score.

**Choose the first seam for learning.** Favor a coherent capability with real value, manageable dependencies, observable outcomes, limited transaction entanglement, and a willing owner. It should be representative enough to test assumptions without placing the organization's most irreversible core at risk.

Avoid both triviality and maximal difficulty. Extracting a static reference lookup may prove only that deployment works. Extracting the central ledger first can combine every unknown. A “Goldilocks” seam reveals contract, data, operations, and team issues within recoverable bounds.

**Build characterization evidence.** Before changing poorly understood behavior, capture representative inputs, outputs, side effects, timing, and error behavior. Feathers describes seams as places where behavior can be altered without editing at that point and emphasizes feedback around legacy change [2]. Characterization tests record what exists; they do not declare every observed quirk correct.

Classify observations against intended contract. Preserve behavior required by stakeholders, expose ambiguous cases, and deliberately correct defects through separate decisions. Tests that snapshot every byte can freeze incidental detail and make the seam unusable.

**Introduce a narrow interception point.** Redirect one class of calls through a responsibility-oriented interface while the old implementation remains behind it. Fowler's branch-by-abstraction description uses an abstraction to permit old and new suppliers to coexist during gradual replacement [5]. The technique can occur inside one deployable system.

Avoid a universal facade with dozens of unrelated methods. Such a facade creates a new monolith and hides coupling rather than reducing it. Introduce seams slice by slice, with contract and owner evidence.

**Invert dependencies where appropriate.** Move the stable policy-facing interface toward the module that owns the need, while implementation adapters depend on it. This prevents domain behavior from depending directly on a volatile supplier or infrastructure API.

Dependency inversion is not merely moving an interface file. The interface vocabulary, lifecycle, error semantics, and tests must belong to the consuming policy. If it mirrors the supplier exactly, replacement remains costly.

**Create an internal module before a service.** Enforce package, namespace, build, and data-access boundaries within the existing process. Route all relevant calls through the module interface. Give the module its own tests, ownership, metrics, and decision records.

This produces evidence about cohesion and contract adequacy without network cost. If independent deployment later has demonstrated value, the internal boundary becomes an extraction seam. If not, the modular monolith may be the better architecture.

**Move behavior with responsibility.** An extracted component should own decisions, not merely CRUD over tables. Moving data access while leaving rules in the old orchestrator creates an anemic service and more remote calls. Move a thin vertical capability slice: policy, state transitions, relevant data authority, contract, and operations.

Some cross-boundary orchestration is legitimate. Distinguish a workflow that coordinates autonomous capabilities from one that contains all domain decisions. The former asks participants to uphold their invariants; the latter treats services as remote functions.

**Protect the old model with translation.** An anti-corruption layer translates between models so the new boundary does not inherit legacy vocabulary and semantics wholesale. Define mappings, loss, defaults, identity, errors, and versioning. A translation that guesses meaning can be more dangerous than explicit coupling.

Keep translation near the boundary and assign ownership. Observe mismatches. Retire or simplify it when the old model disappears; otherwise recognize it as a permanent integration component with full operational responsibilities.

**Design the extracted contract.** Apply SARCH-073: state behavior, versions, compatibility, errors, timing, idempotency, security, deprecation, and mixed-version support. Minimize chatty getters and expose operations aligned with the responsibility.

Do not publish internal implementation detail merely to accelerate extraction. Public contracts are costly to retract. Start with controlled consumers, narrow capabilities, and explicit evolution rules.

**Separate call redirection from data ownership transfer.** A caller can route to new behavior while data authority remains old, or a new component can own data behind an old facade. Each state has different failure and recovery properties. Name them explicitly.

Never leave authority implicit between two stores or writers. If data is copied for reads, identify freshness and source. If authority transfers, define fencing, reconciliation, replay, rollback boundary, and audit.

**Sequence by a dependency graph.** List preparatory changes and their prerequisites: characterize behavior, introduce interface, route internal callers, restrict direct access, establish observability, create new implementation, migrate a cohort, transfer authority, remove bypasses, and retire old code. A topological order exposes impossible schedules and parallel work.

Dependency order is not the whole priority. Choose early steps that reduce uncertainty or blast radius. Limit simultaneous seams so temporary states do not combine unpredictably. Preserve a coherent repository and deployable system after each increment.

**Observe before physical extraction.** Measure whether changes localize, tests become narrower, direct data access falls, and ownership clarifies. Exercise failure and recovery through the internal boundary. If callers still need continuous cross-boundary negotiation, revisit the boundary.

Physical extraction adds process isolation, independent scaling, technology choice, or security controls only when implemented. It also adds serialization, network failure, deployment, capacity, discovery, identity, and observability. Compare measured benefit with this full cost.

**Prevent the distributed monolith.** Warning signs include synchronized releases, shared database writes, cross-service transactions for routine behavior, chatty calls, common scaling and failure domains, one integration environment, centralized orchestration of every rule, and teams unable to operate their services independently.

Do not celebrate repository separation while those relations remain. Merge components, revise contracts, or continue logical modularization when distribution has not earned its cost. Physical consolidation can be an architectural improvement.

**Measure outcomes, not motion.** Relevant measures may include lead time for representative changes, number of required team handoffs, test scope, deployment independence, fault containment, recovery, access boundary, capacity isolation, and change failure. Define populations and confounders.

Service count, commits, extracted lines, and migration percentage can track activity but not value. Use baseline and comparison cases. A temporary worsening may be expected during coexistence; set a time and decision threshold so it does not become permanent.

**Plan completion and stopping.** Define retirement evidence for old call paths, direct database access, flags, adapters, permissions, jobs, dashboards, runbooks, and code. Remove them deliberately. An unused bypass is future erosion.

Stop when the outcome is achieved, further separation has negative expected value, or evidence invalidates the boundary. Preserve learned contracts and modules. Decomposition is a means of architecture evolution, not a one-way maturity ladder.

## Definitions and Notation

Let:

- $G=(V,E,w)$ be a directed weighted graph for one declared concern;
- $V$ be implementation, data, runtime, or organizational elements in that view;
- $E\subseteq V\times V$ be observed relations;
- $w:E\rightarrow\mathbb{R}_{\ge0}$ be concern-specific weights with stated units;
- $\Pi=\{B_1,\ldots,B_k\}$ be a partition of $V$ into nonempty, disjoint blocks;
- $\pi(v)$ identify the block containing $v$;
- $E_{\mathrm{cut}}(\Pi)=\{(u,v)\in E\mid\pi(u)\ne\pi(v)\}$;
- $C(\Pi)=\sum_{e\in E_{\mathrm{cut}}(\Pi)}w(e)$ be weighted cut cost for that view;
- $H(B_i)$ be design decisions and information hidden by block $B_i$;
- $A(f)$ be the authoritative owner of mutable fact $f$;
- $K_t$ be invariants required in transition state $t$;
- $S$ be the selected decomposition seam;
- $T=(t_0,\ldots,t_n)$ be the ordered transition path.

Weights from different meanings must not be added without a legitimate common model. Static dependency, runtime frequency, change coupling, and loss exposure should normally remain separate views.

## Mechanisms, Invariants, or Proof Structure

**Degenerate-cut proof.** If the only objective is minimizing nonnegative $C(\Pi)$ and one block is allowed, choose $\Pi=\{V\}$. Then every edge has endpoints in the same block, $E_{\mathrm{cut}}=\varnothing$, and $C=0$, the minimum possible value. Therefore cut minimization alone cannot discover a useful decomposition; additional responsibility and outcome constraints are necessary.

**Executable cut comparison.** The following toy graph uses call counts per request as weights for one runtime view.

<!-- bijux-verify: {"id":"compare-candidate-cuts","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"by-layer: cut=11\npricing-seam: cut=6\nshipping-seam: cut=3\nsingle-block: cut=0\nlowest_nontrivial=shipping-seam\n","stderr":""}} -->
```python
edges = {
    ("checkout", "orders"): 5,
    ("orders", "pricing"): 4,
    ("orders", "payments"): 3,
    ("orders", "shipping"): 2,
    ("pricing", "catalog"): 2,
    ("shipping", "catalog"): 1,
}
partitions = {
    "by-layer": {"checkout": 0, "orders": 1, "pricing": 1, "payments": 2, "shipping": 1, "catalog": 2},
    "pricing-seam": {"checkout": 0, "orders": 0, "pricing": 1, "payments": 0, "shipping": 0, "catalog": 0},
    "shipping-seam": {"checkout": 0, "orders": 0, "pricing": 0, "payments": 0, "shipping": 1, "catalog": 0},
    "single-block": {name: 0 for edge in edges for name in edge},
}

costs = {}
for label, blocks in partitions.items():
    costs[label] = sum(weight for (u, v), weight in edges.items() if blocks[u] != blocks[v])
    print(f"{label}: cut={costs[label]}")
nontrivial = {label: cost for label, cost in costs.items() if label != "single-block"}
print(f"lowest_nontrivial={min(nontrivial, key=nontrivial.get)}")
```

Execution checks arithmetic for one graph. It does not show shipping is the best domain boundary: the weights omit authority, volatility, latency, failure, data, and team consequences.

**Authority invariant.** For each mutable fact $f$ and every admitted transition state $t$, exactly one component has final decision authority unless a formally defined shared-authority protocol preserves the invariant. Replicas, caches, shadows, and comparison outputs are not additional authorities merely because they store values.

**Seam closure.** A seam is established only when all in-scope consumers use it or remaining bypasses have explicit disposition. Otherwise the abstraction is an optional route and direct coupling can continue growing.

**Distribution test.** Logical modularity is necessary but not sufficient for valuable physical separation. The case for extraction must identify at least one benefit requiring or materially improved by a process/deployment boundary and show that network, consistency, operational, security, and organizational costs remain acceptable.

**Path invariant.** Every $t_i$ must satisfy $K_i$. A final decomposition with clean ownership cannot justify an intermediate dual-writer state that violates financial or safety integrity. This follows the transition reasoning of SARCH-072.

## Alternatives and Trade-Offs

**Business capability versus bounded context.** Capabilities describe what the organization can do and tend to be stable; bounded contexts protect model meaning. They often align but need not. Use both views and avoid turning an org chart or noun list into a deployment topology.

**Modular monolith versus services.** A modular monolith retains simple local calls and transactions while enforcing logical boundaries. Services provide stronger deployment, scaling, or isolation potential but add distributed-systems cost. Choose based on demonstrated outcome, not fashion.

**Code-first versus data-first separation.** Code-first can establish behavior and contracts while temporarily encapsulating shared storage. Data-first can expose ownership early but risks moving tables without decisions. Select order based on invariant, authority, and available seams; make temporary access explicit.

**Read-first versus write-first extraction.** Read paths often have lower consequence and can use derived data, but may postpone true authority. Write-first establishes ownership yet demands transaction and rollback rigor. Use the path that tests the critical hypothesis within acceptable risk.

**Branch by abstraction versus traffic interception.** An in-process abstraction suits library or internal-module replacement and supports continuous integration. External routing can replace a deployed boundary without changing all callers but introduces route and identity concerns. SARCH-075 explores larger-scale interception.

**General interface versus use-case-specific port.** A general interface may reduce duplication but often exposes supplier concepts and speculative operations. Narrow ports localize consumer needs but can multiply translations. Prefer coherent use-case semantics, then consolidate only proven commonality.

**Fast extraction versus preparatory refactoring.** Immediate extraction produces visible motion but carries hidden coupling into production. Preparatory work reduces risk but can become endless. Time-box it around a concrete seam and validate progress through bypass removal and characterization.

## Failure Modes and Misconceptions

1. **“A monolith is unmodular.”** Deployment topology and internal modularity are separate properties.
2. **“More services mean more progress.”** Service count measures topology, not value, autonomy, or quality.
3. **“One table equals one service.”** Storage shape does not define coherent behavior or domain authority.
4. **“Nouns reveal boundaries.”** Policies, verbs, invariants, temporal rules, and language differences are essential.
5. **“The smallest graph cut is correct.”** The one-block partition proves the objective is degenerate without other constraints.
6. **“Static dependencies are the architecture.”** Runtime, data, deployment, identity, change, and organization provide different views.
7. **“High co-change means keep together.”** Co-change may reflect the current bad interface, generation, or release process.
8. **“Replace a local call with HTTP.”** Remote interaction adds latency, partial failure, capacity, security, and versioning.
9. **“A facade creates a boundary.”** Callers can retain direct bypasses and shared authority unless closure is enforced.
10. **“CRUD is a capability.”** Data access without owned decisions produces an anemic remote data service.
11. **“Shared tables preserve autonomy.”** Uncontrolled writers couple schema, invariants, releases, and recovery.
12. **“Dual write transfers ownership.”** It can create partial failure and conflicting authorities.
13. **“Characterization blesses behavior.”** It records observations; stakeholders still decide which behavior is contractual.
14. **“The hardest core should go first.”** Excess unknowns can prevent learning and make reversal impossible.
15. **“The easiest edge proves the strategy.”** A trivial extraction may exercise none of the relevant risks.
16. **“Independent deployment exists because pipelines differ.”** Required synchronized changes and shared recovery preserve lockstep.
17. **“Temporary adapters need little design.”** They can persist and must meet security, capacity, and operational needs.
18. **“Decomposition must continue.”** Stopping or merging is correct when further separation does not serve the outcome.

## Worked Examples

### Example 1

**Situation.** A retail system is organized into UI, business-logic, and database services, yet every pricing change touches all three.

**Reasoning.** The layer split optimizes technical specialization but does not hide pricing volatility. The team identifies quoting as a coherent responsibility with rules, currency, validity, and evidence. It creates an internal quote module spanning input translation, policy, and owned persistence. Technical layers remain implementation details inside the module.

**Conclusion.** Decomposition by information-hiding responsibility can localize change that a technical-layer split amplifies.

### Example 2

**Situation.** A static graph suggests shipping is the cheapest seam with cut cost 3, while pricing costs 6.

**Reasoning.** Runtime evidence shows the shipping edge is on a low-latency checkout path and its data participates in an atomic inventory reservation. Pricing is called more often but has a stable batchable contract and changes weekly under a separate team. The graph arithmetic is correct for call count, yet the broader evidence favors pricing as the first learning seam.

**Conclusion.** A cut metric answers one declared graph question; architecture selection integrates authority, volatility, and quality consequences.

### Example 3

**Situation.** Order and support code use the term `customer`, but workshops show different meanings.

**Reasoning.** Orders mean the purchasing legal party at transaction time; support means a current contact with permissions and case history. One shared object causes support updates to alter historical order views. The team separates models, maintains stable party identifiers, and translates only the facts each context needs.

**Conclusion.** Shared words can conceal distinct models; explicit context boundaries prevent accidental semantic coupling.

### Example 4

**Situation.** A team extracts catalog CRUD endpoints but leaves pricing, availability, and validation in the monolith.

**Reasoning.** Each page now makes dozens of remote getters, releases remain coordinated, and the new service owns no decision. It is a data service, not an autonomous capability. The team either folds it back or moves a coherent catalog responsibility with query shapes, rules, ownership, and cache behavior, reducing conversational calls.

**Conclusion.** Moving tables and accessors without decisions distributes latency while preserving architectural coupling.

### Example 5

**Situation.** Twelve callers access a tax library directly, and the supplier must be replaced.

**Reasoning.** The team characterizes required calculations, introduces a narrow `assess_tax` port owned by checkout policy, and moves callers one at a time. The old supplier remains behind an adapter. Bypass checks prevent new direct calls. A second implementation is compared on governed examples before selection, and the migration abstraction is simplified after retirement.

**Conclusion.** Branch by abstraction creates a controlled seam while the system remains buildable and deployable.

### Example 6

**Situation.** Payment data is copied to a new component, and both old and new code can update refund state.

**Reasoning.** A retry reaches both writers during a partition, creating conflicting terminal outcomes. Copying data did not transfer authority. The safe sequence retains the old authority while the new component shadows; introduces idempotent commands and reconciliation; fences authority per account; transfers a bounded cohort; and removes the old write grant after evidence passes.

**Conclusion.** Data location and decision authority are separate, and decomposition must preserve one accountable writer.

### Example 7

**Situation.** Change history shows reporting and orders co-change in 80% of commits.

**Reasoning.** Inspection finds generated schema snapshots and release-version bumps dominate the co-change. After filtering mechanical commits, semantic co-change is 12% and occurs when reports query undocumented order columns. A published projection and independent release metadata remove the coupling. The initial statistic described repository process, not inherent domain unity.

**Conclusion.** Change-coupling evidence requires classification and can identify a missing contract rather than a permanent boundary.

### Example 8

**Situation.** An extracted search service has its own repository and pipeline but every release requires monolith deployment.

**Reasoning.** Search consumes an unpublished database schema, shares one integration environment, and its client has no mixed-version contract. It also shares a global capacity pool. The topology is distributed, but change and operations remain lockstep. The team adds a versioned index feed, compatibility tests, isolated capacity, and independent recovery—or consolidates if those costs lack value.

**Conclusion.** Independent repositories do not prevent a distributed monolith; authority and operating relations determine autonomy.

### Example 9

**Situation.** A hospital scheduling team proposes extracting its most complex allocation engine first to prove commitment.

**Reasoning.** The engine combines clinical rules, union rules, rooms, staff credentials, and emergency override with incomplete tests. Reversal would be difficult. A smaller appointment-notification capability still exercises privacy, accessibility, integration, and operations while preserving scheduling authority. It provides evidence about platform and team readiness before the core is touched.

**Conclusion.** The first seam should be consequential enough to teach and bounded enough to recover, not politically impressive.

### Example 10

**Situation.** After three extractions, product lead time and fault isolation meet the original targets, while a fourth boundary would split one transaction and add two teams.

**Reasoning.** The remaining modules have coherent ownership and enforced internal access in one deployment. Modeling the fourth extraction adds network coordination, compensating actions, and on-call cost without a scaling or security need. The organization records the modular monolith as the accepted state and retires unused migration scaffolding.

**Conclusion.** Stopping decomposition when its outcome is achieved is evidence-based architecture, not unfinished work.

## Cross-Program Connections

- [SEPAT](../../11-software-engineering-patterns/ROADMAP.md) supplies dependency inversion, facade, adapter, anti-corruption, and modularity patterns used to create seams.
- [SDRE](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) supplies characterization, pipelines, progressive delivery, telemetry, and recovery evidence for each increment.
- [DBE](../../18-database-engineering/ROADMAP.md) develops transactions, constraints, schemas, access control, replication, and migration behind data authority.
- [DARCH](../../20-data-architecture-engineering/ROADMAP.md) supplies lineage, semantic ownership, contracts, and lifecycle evidence for downstream consumers.
- [DIST](../../27-distributed-systems-engineering/ROADMAP.md) explains partial failure, coordination, consistency, time, and messaging costs introduced by physical separation.
- [API](../../28-api-and-service-engineering/ROADMAP.md) develops the service contract, idempotency, error, and lifecycle mechanics used at extracted boundaries.
- [PLAT](../../29-platform-engineering/ROADMAP.md) provides reusable deployment, identity, telemetry, policy, and recovery capabilities needed before teams own services independently.
- [SYSENG](../../26-systems-engineering/ROADMAP.md) connects decomposition to interface control, configuration, suppliers, lifecycle, and whole-system verification.

## References

1. David L. Parnas. “On the Criteria to Be Used in Decomposing Systems into Modules.” *Communications of the ACM* 15, no. 12 (1972): 1053–1058. https://doi.org/10.1145/361598.361623
2. Michael Feathers. *Working Effectively with Legacy Code*. Prentice Hall, 2004.
3. Sam Newman. *Monolith to Microservices: Evolutionary Patterns to Transform Your Monolith*. O'Reilly Media, 2019.
4. Eric Evans. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2003.
5. Martin Fowler. “Branch by Abstraction.” 7 January 2014. Checked 2026-09-06. https://martinfowler.com/bliki/BranchByAbstraction.html
6. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*. 4th ed. Addison-Wesley, 2021.
7. Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage. *Building Evolutionary Architectures*. 2nd ed. O'Reilly Media, 2022.
8. Carliss Y. Baldwin and Kim B. Clark. *Design Rules, Volume 1: The Power of Modularity*. MIT Press, 2000.
9. Chris Richardson. *Microservices Patterns*. Manning, 2018.
10. ISO, IEC, and IEEE. *ISO/IEC/IEEE 42010:2022, Software, Systems and Enterprise—Architecture Description*. 2nd ed., November 2022. https://www.iso.org/standard/74393.html

## Exercises

### Exercise 1

Define decomposition seam, information hiding, business capability, bounded context, logical decomposition, physical decomposition, transactional invariant, modular monolith, and distributed monolith.

### Exercise 2

For edges $A\to B:4$, $B\to C:3$, $C\to A:2$, and $C\to D:5$, compute the weighted cut of partitions $\{A,B,C\}|\{D\}$ and $\{A,B\}|\{C,D\}$. Explain why the lower cut does not prove the better architecture.

### Exercise 3

A proposed inventory service has its own codebase but shares database writes, requires synchronous calls per order line, and deploys with checkout. Diagnose the boundary and propose a focused sequence toward either autonomy or justified consolidation.

### Exercise 4

Design an incremental decomposition plan for pricing inside a large retail application. Include evidence, model boundary, characterization, seam, data authority, contract, rollout, measures, stop rules, and retirement.

### Exercise 5

A national benefits system combines decades-old rules, sensitive citizen data, batch payment, appeals, fraud investigation, call-center tools, and external agencies. Propose a governed incremental decomposition approach without claiming that ordinary software review authorizes benefits, privacy, accessibility, legal, or anti-fraud policy.

## Answers to the Exercises

### Answer 1

A decomposition seam is a controlled interception point for separating, observing, and changing behavior or ownership. Information hiding assigns a likely-changing decision to a module whose interface conceals it. A business capability is an enduring organizational ability. A bounded context is the scope within which one domain model and language remain consistent. Logical decomposition separates responsibilities and dependencies; physical decomposition separates runtime processes, deployments, or infrastructure.

A transactional invariant must hold across authoritative state transitions atomically or through an explicitly designed mechanism. A modular monolith is one deployable system with enforced internal module boundaries. A distributed monolith uses networked units but preserves coordinated change, shared authority, or lockstep operation. These concepts overlap but none implies a particular number of services.

### Answer 2

For $\{A,B,C\}|\{D\}$, only $C\to D$ crosses blocks, so $C(\Pi_1)=5$. For $\{A,B\}|\{C,D\}$, $B\to C$ and $C\to A$ cross, so $C(\Pi_2)=3+2=5$. The cuts tie under the supplied weights.

Even if one were lower, the weights represent only the declared concern. The graph says nothing about responsibility, information hiding, change reason, data authority, transactions, latency sensitivity, failure propagation, security, or ownership. The one-block partition would have cost zero, proving that cut minimization without boundary requirements is insufficient.

### Answer 3

The component is physically separate but not autonomous. Shared writes couple schema and invariants; per-line synchronous calls create latency and availability multiplication; coordinated deployment shows contract and release coupling. It is a distributed-monolith boundary unless a required isolation benefit already justifies those costs.

First name the desired outcome. If inventory autonomy is valuable, establish one reservation and availability authority, characterize checkout behavior, define coarse idempotent operations, and introduce an internal port. Restrict direct writes, publish an owned projection or command path, batch or aggregate line interactions, and test mixed versions. Transfer data authority through fenced, reconciled states; provide isolated telemetry, capacity, and recovery; then demonstrate independent deployment. If no outcome needs distribution, consolidate the process while retaining a strongly enforced inventory module. A good answer permits either evidence-backed result.

### Answer 4

Define the outcome as localizing frequent pricing-policy change while preserving quote integrity, latency, audit, and currency semantics. Baseline callers, rules, tables, discounts, tax interactions, caches, batch jobs, contracts, incidents, change history, and owners. Model a pricing context around quote decisions rather than table CRUD, including price components, validity, rounding, and evidence.

Characterize representative and boundary quotes, errors, timing, and side effects. Introduce a narrow `quote_order` seam backed by the old logic; move callers and block bypasses. Encapsulate price data access and retain one writer. Create an alternative module implementation, compare governed cases, and route a bounded cohort with rollback before considering a process boundary. If extracted, define coarse contracts, idempotency, latency, partial failure, security, capacity, and mixed-version behavior.

Measure representative pricing-change lead time, handoffs, regression scope, quote discrepancies, tail latency, availability, and operating cost. Stop or revise on integrity discrepancy or excessive synchronous coupling. Retire old rule paths, direct table access, flags, adapters no longer needed, permissions, tests, jobs, and runbooks. Keeping the result as an internal module is valid if independent deployment adds no sufficient benefit.

### Answer 5

Establish accountable benefits-policy, legal, privacy, security, accessibility, payments, appeals, fraud, operations, data-governance, labor, and external-agency authorities. They define policy and nondelegable constraints; architecture teams implement and evidence technical boundaries but do not decide eligibility law or authorize data use. Baseline rules, decisions, identifiers, data flows, batch windows, manual overrides, appeal history, reports, external interfaces, identities, suppliers, recovery, and seasonal deadlines.

Identify contexts through language and authority: eligibility determination, case evidence, payment instruction, appeal, investigation, and contact may differ, but do not assume each becomes a service. Define invariants for lawful authority, one decision record, explainability and audit, privacy purpose, accessible service, payment integrity, appeal preservation, and continuity. Choose a bounded first seam such as notification or a read-only case projection that exercises integration without transferring eligibility authority.

Characterize behavior with governed de-identified or protected evidence; introduce a narrow internal interface; block bypasses; and validate in authorized environments. For later authority transfer, use compatible contracts, one fenced writer, reconciliation, controlled cohorts, rollback or roll-forward evidence, and independent review required by the domain. Account for batch, call-center, offline, recovery, and external-agency consumers. Measure policy-change lead time and error outcomes by affected cohort without using staff surveillance metrics. Retire old permissions, data copies, routes, procedures, and supplier dependencies only with evidence. The answer must explicitly defer benefit entitlement, accessibility compliance, anti-fraud policy, legal interpretation, and regulatory approval to authorized institutions.
