---
module_id: SARCH-077
program: Software Engineering: Software Architecture
level: 2
module_number: 77
title: Modularizing a Distributed Monolith
status: complete
last_verified: 2026-09-06
---

# Modularizing a Distributed Monolith

## One-Page Review

### Governing question

How can an organization diagnose a system that is physically distributed but changes, releases, stores data, and fails as one unit, then create useful module autonomy without multiplying remote-call, consistency, and operational complexity?

### Essential definitions

- a **distributed monolith** has multiple runtime or deployment units yet retains tight change, data, release, temporal, or failure coupling;
- **physical distribution** places execution in separate processes, hosts, or networks but establishes no semantic autonomy by itself;
- a **module** owns a cohesive responsibility, hidden decisions, an explicit contract, and governed dependencies;
- **effective autonomy** is the demonstrated ability to change and operate a module within supported contracts without routine coordination with unrelated modules;
- **change coupling** means one intended change commonly requires coordinated edits across units;
- **release coupling** means units must be built, tested, deployed, or rolled back together;
- **data coupling** means multiple units depend on another unit's private representation or share write authority;
- **temporal coupling** requires participants to be available in the same interaction window;
- **failure coupling** lets failure or saturation in one unit disable unrelated outcomes;
- a **strongly connected component** (SCC) is a maximal set of graph vertices mutually reachable through directed dependencies;
- a **modularization seam** is an enforceable boundary through which responsibility can be reorganized without uncontrolled access;
- a **coordinated monolith** is an intentional single deployment; unlike a distributed monolith, it does not pay network cost while pretending to offer independent operation.

### Central model, mechanism, or theorem

Model runtime units as vertices $V$ with directed dependencies $E$. Label each edge by contract, latency, failure, data, and release evidence. If a set $C\subseteq V$ is one SCC, every member lies on a dependency cycle. No member can be topologically ordered before all others without first removing or reversing an edge. SCC detection therefore identifies a structural obstacle to independent evolution, not a complete domain boundary.

Modularization repeatedly chooses an outcome-bearing capability, assigns its decision and data authority, replaces private-representation access with a contract, breaks cycles, and proves reduced coordination through deployment and failure evidence. The target may be a modular monolith, coarser services, or autonomous services. Service count is not the objective.

### Critical invariants

- every mutable business fact has one named authority;
- modules own decisions and data semantics, not only endpoints or tables;
- dependencies use supported contracts and do not bypass ownership;
- remote interactions have explicit timeout, retry, idempotency, and overload behavior;
- cross-module workflows state their consistency and compensation model;
- a module can be tested and changed without a universal integrated environment for routine work;
- releases tolerate supported mixed versions or are intentionally one deployment;
- failures are contained according to named outcome and blast-radius boundaries;
- shared libraries contain stable mechanisms, not coupled domain policy;
- each intermediate state is coherent and retirement removes superseded paths.

### Common failures

Common failures include counting repositories as modules; drawing boundaries from tables or controllers; extracting facades while all services share writes; moving every call to synchronous HTTP; preserving cyclic call chains; calling retries resilience; using one release train and one full-stack test environment; centralizing domain decisions in a coordinator; publishing private database-shaped events; sharing mutable libraries; splitting teams while work remains cross-cutting; creating tiny CRUD services; optimizing a coupling score without domain judgment; extracting before observing current behavior; and assuming every distributed monolith must become microservices.

### Compact example

Orders, Pricing, and Inventory are three services. Orders calls Pricing, Pricing calls Inventory, and Inventory calls Orders during reservation repair. They read and write shared order tables, release together, and one slow inventory database exhausts all request pools. Graph analysis identifies one SCC, but the remedy is not “delete any edge.” The team defines Checkout as the cohesive decision boundary, gives Inventory exclusive reservation authority, moves pricing snapshots into the order contract, replaces repair callbacks with idempotent facts, and sets bounded failure policy. It may consolidate Checkout into one deployment while keeping Inventory separate. Fewer processes can produce more genuine modularity.

### Connections

[SARCH-032](032-modular-monoliths.md) defines strong modules inside one deployment, [SARCH-039](039-microservices-architecture.md) defines service autonomy, and [SARCH-048](048-deployment-units-and-release-independence.md) separates code, runtime, and release boundaries. [SARCH-076](076-data-migration-architecture.md) supplies data-authority transfer. [SARCH-078](../ROADMAP.md) next compares modernization strategies.

## Governing Question

Distribution and modularity are different properties. Processes, containers, repositories, queues, gateways, and deployment manifests can separate execution while business decisions, private schemas, releases, tests, and failure remain entangled. The resulting system pays serialization, network, partial-failure, security, observability, and operations cost without obtaining independent change.

The architectural task is not to make services smaller. It is to identify which outcomes need autonomy, discover why current units cannot provide it, and reshape responsibility, data, contracts, workflows, and operation. Sometimes the most effective move is consolidation into a well-governed modular monolith. Sometimes it is a coarser service boundary or a carefully extracted capability. The answer follows evidence and desired outcomes rather than topology fashion.

## Why This Matters

A distributed monolith slows both product work and incident response. A local-looking change crosses repositories, schemas, generated clients, pipelines, and teams. Releases require a synchronized window. One downstream timeout becomes thread or connection exhaustion across a synchronous chain. Operators see many dashboards but cannot identify the decision owner. Testing depends on a scarce full-stack environment, so feedback arrives late.

Mechanical decomposition often worsens the condition. Turning every internal function into a remote call preserves the original coupling and adds unreliable communication. Splitting normalized tables into CRUD services exposes storage rather than capabilities. A central orchestrator can retain every business decision while nominal services remain anemic. Fowler's analysis of distributed objects emphasizes that remoteness cannot be encapsulated like an in-process boundary; latency, failure, consistency, and availability remain architectural concerns [3].

Modularization must improve a named result: change lead time, release independence, failure containment, workload isolation, security boundary, ownership clarity, or cognitive load. If none requires distribution, one deployment with strong internal boundaries may be the durable result.

## Prerequisites and Retrieval

Retrieve module, information hiding, cohesion, coupling, bounded context, business capability, aggregate, invariant, source of authority, contract, compatibility window, dependency graph, cycle, SCC, synchronous and asynchronous interaction, temporal coupling, partial failure, timeout, retry, idempotency, circuit breaker, bulkhead, backpressure, transaction, eventual consistency, saga, outbox, deployment unit, release train, consumer-driven test, observability, service objective, blast radius, Conway's law, cognitive load, strangler, backfill, CDC, fencing, rollback, and retirement.

SARCH-032 established modular-monolith mechanics; SARCH-039 and SARCH-048 distinguished microservices and release boundaries; SARCH-065 introduced dependency metrics; SARCH-074 through SARCH-076 supplied incremental decomposition, transition routing, and data movement. This module integrates those tools for an already distributed but entangled system.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish physical distribution from module and operational autonomy;
2. diagnose change, data, release, temporal, test, and failure coupling with evidence;
3. use dependency graphs and SCCs without mistaking them for domain design;
4. select a capability-sized target from outcomes and hidden decisions;
5. establish single data and decision authority and remove schema bypasses;
6. redesign remote workflows with explicit consistency and failure semantics;
7. reduce synchronized releases through versioned contracts and mixed-version tests;
8. choose consolidation, internal modularization, or service separation deliberately;
9. sequence changes as coherent reversible or forward-repairable states;
10. demonstrate autonomy using change and operational evidence rather than service count.

## Core Exposition

**Define the desired autonomy.** Start with a concrete problem. Examples are “Pricing must release weekly without coordinating Fulfillment,” “Search overload must not prevent checkout,” or “Health records require a separately governed access boundary.” Name the capability, affected stakeholders, constraints, baseline, and observable improvement.

Autonomy is multidimensional and never absolute. A team may release independently while sharing incident response, or scale independently while using a common deployment window. Declare which dimension matters and which coordination is acceptable. Eliminating all dependencies is neither possible nor desirable; stable intentional dependencies enable a system.

**Establish the topology without trusting labels.** Inventory repositories, build artifacts, deployment units, processes, endpoints, queues, data stores, jobs, teams, pipelines, and runtime environments. Then trace actual call, data, release, and ownership relationships. A component named `customer-service` may only expose shared customer tables and own no customer decision.

Capture both designed and bypass paths. Direct queries, copied libraries, shared caches, batch files, support scripts, common credentials, and manual runbooks often create stronger coupling than official APIs. Observe production traces, database access, release history, incidents, change sets, and team handoffs. Diagrams alone describe intent.

**Measure change coupling.** Sample completed product changes and map every repository, service, schema, test suite, pipeline, and team they touched. Distinguish inherent cross-capability outcomes from accidental scattering of one decision. Co-change frequency is a clue, not proof: mechanical version bumps and generated clients can inflate it, while fragile implicit contracts can hide until an incident.

Record where developers must understand remote internals or wait for another team. A useful module localizes most changes to its owned decision and contract. If a tax rule requires edits in six services, identify which service should own the rule rather than teaching six teams a synchronized procedure.

**Measure release and test coupling.** Examine which units could, in fact, deploy alone during recent releases. Look for lockstep versions, one release train, coordinated database scripts, shared artifact versions, incompatible clients, and rollback dependencies. A nominally separate pipeline does not prove independent release if policy or fear forces coordinated deployment.

Map test feedback. If routine correctness can be established only in a scarce full-system environment, boundaries are not independently testable. Build module contract tests, domain tests, compatibility tests, and focused integration tests. Retain selected end-to-end journeys for assembly risk rather than using them to compensate for missing ownership.

**Map data authority.** For every mutable fact, name who defines meaning, validates invariants, writes, publishes, retains, and repairs it. Shared database access is especially revealing. Separate schemas in one engine can be sound; separate engines can still be coupled through duplicated writes and private representations. The issue is authority and contract, not server count.

Other modules should request behavior or consume supported facts, not update private tables. Move writes behind the owner, then move readers through contracts or replicated views. Use SARCH-076's snapshot and change-boundary discipline when transferring data. Do not physically split the store before an authority model exists.

**Model dependency direction and cycles.** Construct a directed graph for a specific concern. A runtime-call graph differs from a source-import, release, data-write, or team-dependency graph. Label edges with reason, frequency, latency budget, availability need, data semantics, compatibility, and owner. Combining every relationship into one unlabeled graph obscures remedies.

Compute SCCs to locate cycles. A cycle means no topological ordering exists until an edge changes, but it does not say which edge is wrong. The right repair may move a decision, introduce a stable fact, merge cohesive units, invert a dependency, or create an anti-corruption boundary. Domain meaning and outcome evidence choose among them.

**Find hidden decisions, not noun-shaped services.** A cohesive module owns policies that change together for one capability. “Customer,” “Order,” and “Product” nouns may appear everywhere without identifying decisions. Ask who decides price eligibility, inventory promise, refund authorization, identity proof, or delivery commitment. Separate facts from requests and policies from representations.

Domain-driven bounded contexts can clarify where a term has one model, but each context need not be a separate service. Begin with macro capability boundaries. Zhamak Dehghani's monolith-decomposition guidance warns that tiny CRUD services derived from normalized data create high-friction distributed systems rather than useful autonomy [1].

**Choose whether to consolidate first.** When several services form one SCC, share data and release, and serve one cohesive capability, consolidation can remove network failure while internal modularization creates seams. This is not regression. It converts accidental distribution into an intentional deployment boundary that can later be split if evidence justifies it.

Alternatively, keep processes separate but treat the coupled cluster as one operated and released unit while repairing internal boundaries. Honest naming improves risk decisions. Do not advertise independent availability for units whose synchronous cycle makes them share fate.

**Create enforceable module boundaries.** Assign each target module owned decisions, data semantics, public contract, allowed dependencies, events, service objectives, and accountable team. Hide implementation and representation. Enforce source dependencies with module systems, architecture tests, visibility rules, ownership checks, and database permissions.

An API gateway is not a module boundary if services bypass it through shared tables. Conversely, an in-process contract can be strong when visibility and governance prevent bypass. Parnas's information-hiding criterion remains durable: decompose around design decisions likely to change, exposing assumptions only through interfaces [6].

**Reduce chatty synchronous collaboration.** Remote calls impose latency and partial failure. Replace getter-style networks with coarser outcome-oriented commands or queries. Move decisions to the module that owns the required data. Replicate stable facts when freshness and policy allow, and include provenance and version.

Do not replace every call with an event. Asynchrony changes temporal and consistency semantics, creates queues and replay, and can hide coupling rather than remove it. Select request-response when an immediate answer is essential; use facts and asynchronous workflows when participants can proceed independently and delayed completion is acceptable.

**Design workflow consistency explicitly.** A transaction that formerly spanned local modules may not remain atomic across processes. Identify the invariant and the authority able to enforce it. Sometimes the correct result is keeping participants in one transaction boundary. Otherwise use reservations, idempotent state machines, sagas, durable intent, outbox publication, and compensation.

Compensation is not time reversal. An email cannot be unsent and a shipped item cannot be unshipped; a compensating action creates a new fact. Specify intermediate user-visible states, timeouts, retry ownership, duplicate policy, and manual resolution. Do not scatter one business transaction across services merely to preserve a topology goal.

**Break cycles by changing knowledge.** Suppose Orders asks Pricing, Pricing synchronously asks Inventory, and Inventory calls Orders. One repair may give Pricing a versioned inventory classification fact rather than request live order state. Another may put the whole checkout decision in one module. A third may make Orders coordinate explicit reservations while dependencies no longer call back.

Choose based on who should know which policy and which consistency is required. Introducing a generic mediator that knows every workflow can move the cycle into a central brain. Orchestration is legitimate when one capability owns the process; it is harmful when it drains decisions from all participants.

**Version contracts for mixed operation.** Independent release requires old and new peers to coexist during a compatibility window. Add before remove, tolerate unknown fields, preserve meanings, define defaults, and test supported version combinations. Consumer-driven tests can expose expectations, but provider and domain owners still decide the supported contract.

Avoid lockstep shared domain libraries. A library containing stable serialization or observability mechanisms can be useful; one carrying rapidly changing pricing rules creates compile-time distribution of one policy. Version bumps across every service are release coupling made visible.

**Contain failures and load.** Give remote calls deadlines within an end-to-end budget. Bound retries with idempotency and jitter; unlimited or layered retries amplify load. Use concurrency limits, bulkheads, queues, backpressure, load shedding, and circuit behavior according to the outcome. A circuit breaker prevents repeated calls; it does not make stale or missing data acceptable.

Trace the failure graph. Separate processes sharing one database, identity provider, queue partition, or connection pool can still share blast radius. Test dependency slowness, partial response, duplicate, reordering, saturation, control-plane loss, and recovery. Measure user outcome, not only container health.

**Align ownership with the target boundary.** A module needs a team able to change its code, contract, data, and operation. If work always crosses teams, architecture and organization may be misaligned. Team Topologies describes cognitive load and interaction modes useful for this analysis [10], but organization charts alone do not establish good domain boundaries.

Platform teams should provide paved mechanisms—delivery, identity, telemetry, policy, messaging—without taking domain decisions. A ticket queue for every deployment preserves coordination. Self-service must have usable defaults, support, and escape or exception governance.

**Make observability respect ownership.** Correlation identifiers, traces, structured events, dependency metrics, and version information help diagnose remote interaction. Each module needs signals for its own service objectives and domain outcomes. A central dashboard without module ownership becomes a wall of symptoms.

Record route, contract version, retry, timeout, queue age, saturation, authority, and state transition without leaking sensitive data. Build diagnostic paths before changing topology. Distributed tracing can reveal a call chain; it cannot decide whether the chain represents the right responsibility.

**Sequence vertical, coherent changes.** Select one capability whose boundary is understandable and whose improvement matters. Characterize behavior, create an internal seam, assign authority, replace bypasses, establish a contract, and prove focused tests. Then consolidate or extract only as needed. Migrate data and consumers, observe mixed operation, fence old writes, and retire obsolete paths.

Every intermediate state must be operable and move toward the target. Avoid a long-lived facade that calls back into every old service for every decision. If a step adds distribution without removing coupling, define its short exit condition or choose another step.

**Use evidence to evaluate autonomy.** Compare lead time, number of touched units, coordinating teams, independent deployment success, rollback scope, contract break frequency, full-stack test dependence, synchronous critical-path depth, incident blast radius, recovery, and cognitive load. Control for mechanical changes and product scope.

Metrics can be gamed. Fewer calls can hide a shared database; more deployments can reflect churn; fewer coordinated releases can mean untested incompatibility. Combine measurements with concrete change traces, incident analysis, architecture review, and team interviews.

**Stop at the architecture that fits.** The goal may be a modular monolith for a cohesive workload, a small number of coarse services for distinct operational needs, or multiple autonomous services. Keep a module in-process when local transactions, low latency, and simple operation dominate. Distribute when independent scale, failure, security, jurisdiction, ownership, or lifecycle value exceeds the cost.

Modernization is complete for a slice when authority, contracts, callers, data, tests, release, operation, and retirement align. A diagram containing more boxes is not evidence of progress.

## Definitions and Notation

Let:

- $V$ be runtime or deployment units for one declared view;
- $E\subseteq V\times V$ be directed dependencies in that view;
- $G=(V,E)$ be the resulting graph;
- $C\subseteq V$ be a strongly connected component when every pair in $C$ is mutually reachable;
- $M$ be proposed capability modules;
- $owner(d)\in M$ be the sole authority for mutable decision or datum $d$;
- $touch(x)$ be units changed for product change $x$;
- $teams(x)$ be teams requiring active coordination for $x$;
- $P_i$ be the probability dependency $i$ satisfies its obligation over a declared interval under stated assumptions;
- $L_i$ be latency contribution of dependency $i$;
- $B(o)$ be the set of dependencies whose failure can defeat outcome $o$;
- $R$ be the set of release units and $compat(r_i,r_j)$ state supported mixed-version compatibility.

For a strictly sequential critical path with independent success events, a simplified success estimate is $P_{path}=\prod_i P_i$ and latency is approximately $L_{path}=\sum_i L_i$ plus processing and queueing. Independence is often false, so the product is an illustration, not a production reliability proof. The graph must also be separated by concern: an SCC in source imports need not be an SCC in runtime calls.

## Mechanisms, Invariants, or Proof Structure

**Cycle theorem.** Collapse every SCC of a directed graph into one vertex. The condensation graph is acyclic. If it contained a cycle, all components on that cycle would be mutually reachable and therefore one SCC, a contradiction. Consequently SCCs identify the minimal cyclic regions that must be treated together or have dependency knowledge changed before topological sequencing is possible.

**Executable cycle detection.** This finite graph contains a three-service checkout cycle and an isolated outbound Notifications dependency. Kosaraju's two-pass traversal reports its SCCs deterministically.

<!-- bijux-verify: {"id":"find-service-cycles","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"components=[['inventory', 'orders', 'pricing'], ['notifications']]\ncyclic=[['inventory', 'orders', 'pricing']]\n","stderr":""}} -->
```python
graph = {
    "orders": ["pricing", "notifications"],
    "pricing": ["inventory"],
    "inventory": ["orders"],
    "notifications": [],
}
seen, finish = set(), []
def visit(node):
    if node in seen:
        return
    seen.add(node)
    for nxt in graph[node]:
        visit(nxt)
    finish.append(node)
for node in sorted(graph):
    visit(node)
reverse = {node: [] for node in graph}
for node, targets in graph.items():
    for target in targets:
        reverse[target].append(node)
seen, components = set(), []
def collect(node, component):
    if node in seen:
        return
    seen.add(node)
    component.append(node)
    for nxt in reverse[node]:
        collect(nxt, component)
for node in reversed(finish):
    if node not in seen:
        component = []
        collect(node, component)
        components.append(sorted(component))
components.sort()
cyclic = [component for component in components if len(component) > 1]
print(f"components={components}")
print(f"cyclic={cyclic}")
```

Execution verifies one graph traversal and output. It neither selects a business boundary nor proves that any dependency should be removed.

**Single-authority invariant.** For every mutable fact $d$, exactly one $owner(d)$ validates and commits it in a migration state. Other modules may hold versioned replicas or derived views but cannot independently redefine the fact. A shared table with multiple writers violates the invariant even if writes rarely conflict.

**Release-independence obligation.** A unit is independently releasable only for a supported change when its deployment does not require simultaneous unaffected-unit deployment and every communicating version pair in the window satisfies `compat`. Separate pipelines are mechanisms; observed mixed-version releases and bounded rollback are evidence.

**Sequential-chain counterexample.** Five independent remote dependencies each succeeding 99.9% of the time give $0.999^5\approx0.99501$, or about 99.501%, before shared failures and local work. Calling every service “three nines” does not give the path three nines. Retries may raise success for transient faults but can also amplify load and latency.

**Consolidation proposition.** If a set of processes has one cohesive authority, releases together, requires local atomicity, and has no independent scale, security, failure, or lifecycle need, consolidating it can remove distribution cost without reducing demonstrated autonomy. Process count is therefore neither a lower nor an upper bound on useful modularity.

## Alternatives and Trade-Offs

**Modular monolith versus autonomous services.** A modular monolith keeps calls, transactions, delivery, and diagnosis local but shares runtime and release fate. Services add operational isolation and independent lifecycle while adding network, consistency, security, and platform cost.

**Consolidate first versus decouple in place.** Consolidation quickly removes fragile remote cycles but may require deployment and ownership change. In-place repair preserves topology but can leave cost during a long transition. Choose the smallest coherent path.

**Orchestration versus choreography.** An owning orchestrator makes workflow state visible but can centralize unrelated policy. Choreography reduces central control but can hide process flow and amplify event coupling. Assign the end-to-end decision to a capability.

**Synchronous query versus replicated fact.** A live query offers freshness but creates temporal and availability coupling. A versioned replica improves independence but adds staleness, lineage, and reconciliation. The outcome determines acceptable freshness.

**Shared library versus service contract.** A library avoids network overhead and can standardize stable mechanisms. Rapidly changing shared domain code synchronizes releases. A service centralizes one authority but adds remote failure. Place policy with its owner.

**Repository consolidation versus separation.** Repository shape affects tooling and visibility but does not define runtime or ownership. A monorepo can enforce modules and independent artifacts; many repositories can still be one release train.

## Failure Modes and Misconceptions

1. **“Many deployables mean microservices.”** deployment count establishes no autonomy.
2. **“A shared database is always the whole diagnosis.”** authority and bypass matter more than engine count.
3. **“Separate schemas guarantee ownership.”** credentials and private-query contracts can still cross them.
4. **“Events remove coupling.”** schemas, timing, ordering, and process meaning can couple publishers and consumers.
5. **“SCCs reveal bounded contexts.”** they reveal graph cycles under one chosen view.
6. **“Delete any cyclic edge.”** domain responsibility determines which knowledge should change.
7. **“Every remote call can become asynchronous.”** some outcomes require an immediate authoritative answer.
8. **“Retries make calls reliable.”** they require idempotency, budgets, and overload control.
9. **“A coordinator is neutral plumbing.”** it may become the owner of every business decision.
10. **“CRUD services are cohesive.”** storage nouns do not define capability or policy.
11. **“Shared libraries are free reuse.”** changing domain libraries can impose lockstep releases.
12. **“Contract tests prove the workflow.”** state, timing, failure, and business invariants remain.
13. **“One percent canary means one percent blast radius.”** shared dependencies can spread failure.
14. **“Teams create boundaries by assignment.”** cross-cutting work reveals unresolved architecture.
15. **“Consolidation is architectural failure.”** it can remove accidental distribution and clarify modules.
16. **“More deployments prove faster delivery.”** coordination and rework may still dominate lead time.
17. **“Temporary compatibility can remain forever.”** it expands states and obscures ownership.
18. **“The destination must be microservices.”** the simplest architecture meeting evidenced forces is preferable.

## Worked Examples

### Example 1

**Situation.** Eight services have separate repositories, but a routine discount change touches six repositories and three teams.

**Reasoning.** Repository count suggests distribution, while change history shows one policy scattered across units. The team assigns discount eligibility to Pricing, defines an outcome-oriented pricing contract, moves rule data and validation behind it, and removes duplicated rule libraries. It measures subsequent touched units and coordination rather than celebrating a ninth service.

**Conclusion.** Change locality is stronger autonomy evidence than repository topology.

### Example 2

**Situation.** Orders, Pricing, and Inventory form the cycle used by the executable example.

**Reasoning.** SCC analysis proves no topological ordering of the three exists, but not which service boundary is correct. Domain analysis gives Inventory reservation authority and lets Pricing consume a versioned availability class; Orders owns checkout process state. The callback from Inventory becomes an idempotent reservation fact, breaking mutual reachability.

**Conclusion.** Graph structure locates cyclic knowledge; domain authority determines its repair.

### Example 3

**Situation.** Customer and Address services use different databases, yet both update the legal mailing address.

**Reasoning.** Physical storage is separate but authority is duplicated. The team decides Customer owns legal address and Address owns geocoding as a derived fact, exposes versioned contracts, migrates direct writers, reconciles state, fences obsolete credentials, and records lineage.

**Conclusion.** Separate databases do not compensate for ambiguous fact ownership.

### Example 4

**Situation.** A checkout path synchronously calls five nominally 99.9%-successful dependencies.

**Reasoning.** Under the deliberately simplified independence assumption, path success is $0.999^5\approx0.99501$. Shared dependencies can make the estimate worse, and latency sums along the chain. The team moves cohesive decisions together, removes getter calls, defines fallbacks only where semantically valid, and tests saturation rather than stacking retries.

**Conclusion.** Fine-grained distribution compounds path obligations even before correlated failure.

### Example 5

**Situation.** All services import a shared library containing eligibility rules and must upgrade together monthly.

**Reasoning.** Runtime calls are absent, but domain change and release coupling are strong. Eligibility becomes owned policy behind a compatible contract, or the affected services consolidate into one module if the decision is inseparable. The remaining shared library keeps stable value types and telemetry helpers only.

**Conclusion.** Compile-time reuse can create a distributed monolith as surely as synchronous calls.

### Example 6

**Situation.** A team replaces twenty request-response calls with twenty event subscriptions.

**Reasoning.** Consumers still require the same sequence within seconds, share one schema, and cannot operate if any event is missing. Coupling moved into timing and replay. The team models the real workflow, combines cohesive steps, publishes stable facts at authority boundaries, and declares ordering, idempotency, lateness, and compensation.

**Conclusion.** Asynchrony changes coupling; it does not automatically reduce it.

### Example 7

**Situation.** Three tiny services implement one invoice transaction and always release together.

**Reasoning.** They have one team, workload, security boundary, data authority, and failure objective. Network calls and distributed compensation add cost without a named benefit. Consolidating them into an Invoice module inside one deployment preserves contracts internally and restores local atomicity.

**Conclusion.** Fewer deployment units can increase effective modularity.

### Example 8

**Situation.** A candidate service can deploy alone, but every change waits two days for a full-stack test environment.

**Reasoning.** Pipeline separation hides test coupling. The team creates domain and contract tests, replaceable dependency fixtures, schema compatibility checks, and focused failure tests; a small set of end-to-end journeys remains for assembly risk. It tracks feedback time and escaped incompatibility.

**Conclusion.** Independent deployment requires independently obtainable evidence, not merely a deploy button.

### Example 9

**Situation.** Search is a separate service, but when it slows, checkout thread pools exhaust.

**Reasoning.** Search sits synchronously on a critical path despite not being essential to submitting an already selected cart. The team removes the call from checkout, uses a bounded cached or replicated product fact where valid, budgets deadlines, isolates pools, and sheds optional work. It tests slow and unavailable Search.

**Conclusion.** Process isolation does not contain failure when resource and temporal dependencies propagate it.

### Example 10

**Situation.** A modernization program has produced twelve services but retained old database access “temporarily.”

**Reasoning.** Direct readers and writers make private schema the real contract and prevent retirement. The program pauses extraction, inventories access, selects one capability, moves writes to one authority, migrates readers to contracts or governed views, rehearses data transfer, revokes credentials, and deletes the old path before selecting the next slice.

**Conclusion.** Completing one authority boundary is more valuable than starting many service shells.

## Cross-Program Connections

- [CONPAR](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies atomicity, concurrency, ordering, and interference models.
- [SEPAT](../../11-software-engineering-patterns/ROADMAP.md) owns implementation patterns such as outbox, saga, facade, adapter, and strangler fig.
- [SDRE](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) develops pipelines, deployment, observability, resilience, recovery, and incident practice.
- [DBE](../../18-database-engineering/ROADMAP.md) owns transaction, schema, replication, and database performance mechanisms.
- [DARCH](../../20-data-architecture-engineering/ROADMAP.md) owns shared meaning, lineage, master data, governance, and analytical consumption.
- [DIST](../../27-distributed-systems-engineering/ROADMAP.md) supplies partial failure, consistency, replication, consensus, and coordination theory.
- [API](../../28-api-and-service-engineering/ROADMAP.md) develops contract, compatibility, idempotency, gateway, and service interaction design.
- [PLAT](../../29-platform-engineering/ROADMAP.md) supplies self-service delivery and runtime capabilities without owning domain decisions.

## References

1. Zhamak Dehghani. “How to break a Monolith into Microservices.” MartinFowler.com, 24 April 2018. Checked 2026-09-06. https://martinfowler.com/articles/break-monolith-into-microservices.html
2. Martin Fowler. “Microservice Trade-Offs.” 1 July 2015. Checked 2026-09-06. https://martinfowler.com/articles/microservice-trade-offs.html
3. Martin Fowler. “Microservices and the First Law of Distributed Objects.” 13 August 2014. Checked 2026-09-06. https://martinfowler.com/articles/distributed-objects-microservices.html
4. Sam Newman. *Building Microservices*. 2nd ed. O'Reilly Media, 2021.
5. Sam Newman. *Monolith to Microservices: Evolutionary Patterns to Transform Your Monolith*. O'Reilly Media, 2019.
6. David L. Parnas. “On the Criteria To Be Used in Decomposing Systems into Modules.” *Communications of the ACM* 15(12), 1972. https://doi.org/10.1145/361598.361623
7. Eric Evans. *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley, 2003.
8. Chris Richardson. *Microservices Patterns*. Manning, 2018.
9. Michael Nygard. *Release It!*. 2nd ed. Pragmatic Bookshelf, 2018.
10. Matthew Skelton and Manuel Pais. *Team Topologies*. IT Revolution, 2019.
11. Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage. *Building Evolutionary Architectures*. 2nd ed. O'Reilly Media, 2022.
12. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*. 4th ed. Addison-Wesley, 2021.

## Exercises

### Exercise 1

Define distributed monolith, physical distribution, module, effective autonomy, change coupling, release coupling, data coupling, temporal coupling, failure coupling, SCC, and modularization seam.

### Exercise 2

A strictly sequential path calls four independent dependencies, each with success probability 0.998. Compute the simplified path success probability and failure probability. State why the result is not a production availability prediction.

### Exercise 3

Services A, B, and C release together. A calls B, B calls C, C reads A's tables, and all import a mutable rule library. Diagnose the coupling views and propose the first evidence-gathering and boundary-enforcement actions.

### Exercise 4

Design an incremental modularization of a retail checkout cluster. Address desired outcome, hidden decisions, graph views, data authority, transaction semantics, calls and events, contracts, mixed versions, testing, failure containment, ownership, migration, and retirement. Explain whether you would consolidate or further distribute it.

### Exercise 5

A city emergency-response platform links dispatch, hospitals, transport, shelters, identity, public alerts, maps, and volunteer organizations. Propose a modularization approach without claiming that architecture alone determines emergency policy, clinical priority, accessibility, privacy, labor responsibility, or legal authority.

## Answers to the Exercises

### Answer 1

A distributed monolith has multiple runtime or deployment units while tight change, data, release, temporal, or failure assumptions make them operate as one. Physical distribution means separate process, host, or network placement and establishes no autonomy. A module owns cohesive responsibility, hidden decisions, contract, and dependencies. Effective autonomy is demonstrated bounded independent change and operation. Change coupling spreads one intended change; release coupling forces coordinated delivery; data coupling depends on private representation or shared authority; temporal coupling requires simultaneous availability; failure coupling propagates defeat of an otherwise separate outcome. An SCC is a maximal mutually reachable vertex set in a directed graph. A modularization seam is an enforceable boundary for reorganizing responsibility safely.

### Answer 2

Under the stated and usually unrealistic independence assumption, $P_{path}=0.998^4=0.992023968$, about 99.2024%. Failure probability is $1-P_{path}=0.007976032$, about 0.7976%.

This is not a production prediction because calls may share infrastructure and fail dependently; traffic, retries, queueing, timeouts, local processing, partial responses, recovery, maintenance, and observation windows are omitted; and success may not mean the user outcome is correct. It is a counterexample to assuming each dependency's advertised probability transfers unchanged to the sequential path.

### Answer 3

The runtime graph contains A to B to C, while C's direct table read creates data and representation coupling back to A. Release history shows release coupling among all three. The mutable rule library creates source, change, and binary compatibility coupling even if no network edge returns to A. Teams may also be coupled if ownership follows repositories but each change crosses all of them.

First sample real change sets, releases, traces, database access, incidents, and team handoffs. Build separate runtime, source, data-write/read, release, and ownership graphs rather than one unlabeled picture. Identify which capability owns the mutable rule and A's data semantics. Deny new table bypasses, introduce a characterized contract or governed replica for C, and move rule authority behind its owner or consolidate the cohesive capability. Add focused domain and compatibility tests before moving processes. Use SCCs to locate cycles but domain evidence to choose the changed edge.

### Answer 4

Define the outcome—for example, independent evolution of promotion policy and containment of inventory overload—plus baselines for touched units, lead time, releases, and incidents. Trace Checkout, Pricing, Promotions, Inventory, Payment, Orders, jobs, stores, teams, and bypasses across runtime, source, data, release, test, and failure views. Identify decisions such as price eligibility, inventory promise, payment authorization, and order acceptance rather than copying controller or table boundaries.

Give one owner to each decision and mutable fact. Keep order acceptance and its hard local invariants together; give Inventory reservation authority; snapshot accepted price and promotion provenance into Orders; keep Payment authorization behind an idempotent contract. Replace chatty getters with outcome-oriented calls or versioned facts. State which workflow steps are local transactions and which are durable state machines with reservation, timeout, outbox publication, replay, compensation, and manual repair.

Expand contracts for mixed versions, add domain, contract, schema, and failure tests, and retain only risk-based end-to-end journeys. Bound deadlines, retries, pools, queues, and optional work. Align accountable teams and self-service platform support. Create seams internally, migrate one authority and cohort at a time using snapshot/CDC and fencing, observe, then remove direct data access, obsolete events, flags, jobs, credentials, and old code.

I would consolidate services that form one cohesive transaction, release together, and have no independent operational need into a modular Checkout deployment. I would keep Inventory or Payment separate only where scale, failure, security, ownership, or lifecycle evidence warrants it. An acceptable alternative can keep coarser services if it demonstrates single authority, compatible releases, focused tests, and contained failure. Evaluation rests on outcomes and autonomy, not the number of resulting processes.

### Answer 5

Establish accountable emergency-management, dispatch, clinical, transport, shelter, identity, accessibility, privacy, security, labor, legal, public-information, mapping, and volunteer-organization authorities. Inventory decisions, facts, interfaces, data classifications, callers, radio or offline paths, manual work, dependencies, releases, teams, recovery, and degraded modes. Map separate runtime, data, change, authority, and failure graphs under ordinary and disaster load.

Choose capability boundaries around decisions such as dispatch assignment, hospital capacity fact, transport request, shelter availability, identity proof, and public-alert authorization. Name one authority for each fact and preserve provenance. Avoid a universal central service or shared writable database. Use synchronous interaction only when an immediate answer is essential; otherwise exchange versioned facts with ordering, staleness, idempotency, replay, confidentiality, accessibility, and correction rules. Keep decisions requiring one atomic invariant together.

Begin with observability and internal seams, then one bounded high-learning but safely governed slice. Test network partition, stale maps, inaccessible alerts, duplicate dispatch, unavailable identity, overload, manual fallback, recovery, and cross-agency handoff. Fence authority during data and workflow transfer and retain auditable degraded operation. Consolidate tightly coupled processes when distribution has no outcome benefit; isolate capabilities when jurisdiction, security, failure, scale, or ownership requires it.

Architecture can provide explicit authority, provenance, containment, accessibility mechanisms, and review evidence. It cannot determine emergency priorities, clinical triage, lawful processing, collective responsibility, public communication policy, or adequate accessibility. Those decisions require the responsible institutions, professionals, affected communities, and applicable processes.
