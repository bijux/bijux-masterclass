---
module_id: SARCH-032
program: Software Engineering: Software Architecture
level: 1
module_number: 32
title: Modular Monoliths
status: complete
last_verified: 2026-09-06
---

# Modular Monoliths

## One-Page Review

### Governing question

How can a system retain one primary deployment and process boundary while establishing real internal modules that localize decisions, data authority, change, testing, and ownership—and when do scale, failure, or release forces justify splitting a module out?

### Essential definitions

- A **monolith** is a system whose substantial application capabilities are built and deployed as one primary unit; the word alone says nothing about internal quality.
- A **modular monolith** is a monolith with explicit, cohesive internal modules, owned contracts, controlled dependencies, and enforceable visibility.
- A **module** is a responsibility and information-hiding boundary with a provided contract and hidden decisions; it is not merely a folder or namespace.
- **data authority** identifies the module that owns the meaning and invariants of a data set and controls its writes.
- An **internal contract** is a governed interface used between modules inside the deployment; it still needs semantics and compatibility during change.
- An **internal event** records a fact one module exposes to decouple other modules from its internals; in-process delivery does not automatically make it durable.
- A **distributed monolith** is a set of separately deployed parts that retain tightly coupled change, data, release, and failure assumptions.
- **change scattering** measures how one bounded change touches modules or owners; **co-change** observes modules that often change together.
- **extraction** moves a module across a deployment or process boundary while preserving or deliberately revising its contract and data authority.
- A **seam** is a boundary at which behavior can be substituted, observed, migrated, or separated with controlled consequences.

### Central model, mechanism, or theorem

Represent internal structure as a labeled graph $G=(M,E)$, where modules $M$ own contracts and data, and edge $(a,b,k)$ means $a$ depends on $b$ by kind $k$. Let $A$ be allowed dependencies and $E_o$ observed dependencies. Structural conformance requires $E_o\subseteq A$ within the extractor's scope.

A modular monolith additionally maps most application modules to one primary deployment unit $u$:

$$
deploy(m)=u\quad\text{for most }m\in M.
$$

Shared deployment does not erase module boundaries; conversely, an acyclic package graph does not prove coherent responsibility, data ownership, or change isolation.

### Critical invariants

- define modules around cohesive responsibilities and hidden decisions, not technical suffixes;
- give each module stable identity, contract, owner, data authority, and dependency policy;
- prohibit direct access to another module's internals, including its tables and framework objects;
- separate synchronous calls, internal events, shared primitives, data dependencies, and test dependencies;
- preserve local atomic transactions only within a declared consistency boundary;
- keep in-process calls explicit about failure, reentrancy, concurrency, and transaction participation;
- enforce visibility and allowed dependencies through language, build, architecture tests, schemas, and review;
- prevent a universal `common` module, global mutable state, and shared database writes from defeating ownership;
- measure change scattering, co-change, build/test impact, violations, runtime cost, and operational simplicity;
- do not call a module independently deployable merely because it has an interface;
- treat extraction as a distributed-systems change involving latency, partial failure, identity, data, and operations;
- split only when evidence supports a deployment boundary, not to imitate an organizational fashion.

### Common failures

Common failures include equating monolith with spaghetti; creating packages called modules with public internals; letting every module query every table; sharing one domain object everywhere; depending on a large `common` library; using synchronous internal events as if they were durable; holding one transaction across unrelated capabilities; allowing tests to bypass production boundaries; claiming independent deployment without separate artifacts; splitting by CRUD entity; replacing function calls with network calls; and calling tightly coordinated services “microservices.”

### Compact example

`Orders` owns order state and exposes `place`, `cancel`, and query contracts. `Billing` cannot write order tables; it receives an `OrderPlaced` fact and owns payment state. Both run in one process and release together. A local transaction can update order state and an internal outbox record atomically. If Billing is later extracted, the fact gains durable transport, idempotency, versioning, authentication, timeout, and replay semantics without changing who owns each invariant.

### Connections

[SARCH-031](031-layered-architecture.md) supplies dependency rules within and across modules. [SARCH-033](../ROADMAP.md) develops ports and adapters; [SARCH-035](../ROADMAP.md) develops event-driven architecture; [SARCH-039](../ROADMAP.md) develops microservices. [SARCH-041](../ROADMAP.md), [SARCH-042](../ROADMAP.md), and [SARCH-048](../ROADMAP.md) later deepen data authority, database sharing, and release independence.

## Governing Question

A single deployable can contain excellent modular architecture, and a fleet of services can contain a tangled monolith connected by a network. Deployment topology and design quality are different dimensions. The modular-monolith style deliberately keeps operational unity while imposing meaningful internal boundaries.

The governing question is how to make those boundaries real enough to control knowledge, state, and change without paying distributed-systems costs prematurely. It also asks when the shared deployment becomes the wrong boundary because a capability needs distinct scale, failure isolation, security, ownership, or release cadence.

## Why This Matters

One deployment can simplify transactions, local calls, debugging, testing, version compatibility, release coordination, and operations. It avoids network latency and partial failure between internal modules. Early systems often benefit because domain boundaries and load patterns are still being learned.

Without internal governance, however, convenience becomes global coupling. Every class is reachable, every table shared, one change triggers the whole test suite, and no team owns an invariant. Extraction then requires disentangling semantics and data while simultaneously introducing distributed failure.

A modular monolith separates these decisions. It invests in cohesive modules and explicit authority now while deferring the cost of separate deployment until evidence supports it. The goal is not eventual microservices by default; a well-governed monolith can be the durable production architecture.

## Prerequisites and Retrieval

Retrieve module, responsibility, cohesion, coupling, information hiding, interface, visibility, dependency graph, layer, capability, bounded context, invariant, data authority, transaction, consistency boundary, internal event, idempotency, versioning, deployment unit, process, release, scaling, fault isolation, observability, ownership, change scattering, conformance, and evidence.

From SARCH-022 retrieve module and code views. From SARCH-031 retrieve allowed dependencies, inversion, same-layer rules, hidden data coupling, and the layer/tier distinction. From quality-attribute modules retrieve modifiability, performance, availability, security, testability, interoperability, and operability trade-offs.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish monolith, modular monolith, module, service, process, and distributed monolith;
2. define internal modules around capabilities, policy, and information hiding;
3. assign contracts, visibility, ownership, and data authority;
4. choose synchronous calls, internal events, or shared primitives deliberately;
5. reason about transactions and consistency across module boundaries;
6. enforce dependency and data-access rules with bounded evidence;
7. design tests, builds, observability, and operations around internal identity;
8. evaluate modularity using structural and change evidence without metric theater;
9. plan safe extraction across process and deployment boundaries;
10. decide whether to retain or split a module from architectural forces rather than fashion.

## Core Exposition

**Separate deployment shape from internal structure.** A monolith usually produces one main application artifact or coordinated deployment. That fact does not imply one source file, one module, one database schema, one team, or poor design. Conversely, separate processes do not imply autonomy.

Describe module, runtime, deployment, data, and ownership views separately. A module may be one package, several packages, or a build subproject. Several modules can run in one process. A deployment may include sidecars, jobs, migrations, and static assets while still operating as one primary application release.

**Define modular monolith precisely.** A modular monolith has named responsibility boundaries, stable provided contracts, hidden internals, controlled dependency direction, owned data semantics, enforceable access, and evidence that changes remain reasonably localized. The modules share a deployment boundary by design.

The modifier “modular” is a claim requiring evidence. A folder per feature helps navigation but does not prevent cross-feature imports, shared writes, reflection, generated dependencies, or global state. A build with one artifact can still enforce many internal modules; a repository split is not required.

**Find modules from decisions and capabilities.** Begin with business or system capabilities, invariants, vocabulary, change forces, security obligations, data authority, and accountable ownership. Ask which facts must remain consistent, which policies change together, and which knowledge other parts should not possess.

Parnas's information-hiding criterion remains foundational: modules should conceal design decisions likely to change behind stable interfaces [1]. Domain-driven design contributes bounded models and explicit language boundaries [2]. Neither provides a mechanical one-module-per-noun rule. `Customer`, `Address`, or `Invoice` may participate in several contexts with different meanings.

**State module contracts.** A module contract includes commands, queries, events, data types, errors, authorization context, invariants, concurrency behavior, compatibility, and ownership. In-process does not mean informal. Callers still need to know whether an operation is atomic, reentrant, blocking, idempotent, or permitted inside another transaction.

Keep contract types separate from implementation and persistence types. Public visibility in a language is broader than supported architectural API unless constrained. Mark internal extension points and test surfaces distinctly.

**Hide internals with multiple mechanisms.** Use language modules, package visibility, build targets, namespaces, internal APIs, architecture tests, dependency rules, schema permissions, ownership review, and generated-code policy. Each sees different paths.

Static imports miss reflection, dependency-injection configuration, shared tables, messages, file paths, and framework callbacks. Database permissions miss copied data and privileged migrations. Tests may have broader access than production. State the scope of every conformance mechanism.

**Control the dependency graph.** Let $A$ declare allowed edges and $E_o$ contain observed edges of defined kinds. Reject $E_o\setminus A$ or govern a time-bounded exception. Prefer acyclic capability dependencies or explicit orchestration where possible, but do not treat acyclicity as the whole design.

A highly connected acyclic graph can still scatter changes. A small cycle may reveal two responsibilities that are actually one module. Diagnose vocabulary, invariants, data, and changes before adding an interface merely to satisfy a graph checker.

**Assign data authority.** A module owns the meaning, invariants, write policy, and lifecycle of its data. Storage can remain in one physical database, but ownership must be visible. Other modules use the owner's command/query contract, a governed read projection, or a published fact.

Physical database sharing does not require logical table sharing. Separate schemas, users, migrations, and access rules can help. Direct cross-module reads create schema and semantic dependency; direct writes are more dangerous because they bypass invariants and audit. Record necessary reporting or migration exceptions explicitly.

**Define transaction boundaries.** One process and database make local atomic transactions possible, which is a major benefit. Use them within a cohesive consistency boundary. Do not make every use case one global transaction merely because it can be.

If one command must update invariants owned by several modules atomically, ask whether the modules are split incorrectly, whether one module should orchestrate a documented contract, or whether eventual coordination is acceptable. Cross-module atomicity increases knowledge of internal ordering and makes future extraction harder.

An outbox can atomically record a domain change and pending publication in the owning module's transaction. Delivery and downstream processing still require duplicate, ordering, retry, and failure semantics. In-process execution does not remove these conceptual obligations if future or current asynchronous handling is possible.

**Choose synchronous calls deliberately.** A direct in-process call is fast, debuggable, and naturally propagates return values and exceptions. It also couples the caller to the callee's availability within the same process, latency, transaction context, and call stack.

Use synchronous calls when the caller needs a result now and the dependency is part of the same bounded operation. Define errors and reentrancy. Avoid chains in which one high-level action synchronously traverses many module internals; they hide orchestration and create fragile cycles.

**Choose internal events deliberately.** An internal event expresses that a fact occurred and lets several modules react without the publisher knowing each subscriber. It can reduce direct knowledge and support later extraction. It can also hide control flow and failure.

Synchronous in-process event dispatch shares the publisher's call stack and often its transaction; one subscriber failure may abort all work. Asynchronous in-process dispatch can lose events on crash. Durable outbox delivery adds persistence, retry, idempotency, ordering, and observability. Name the mechanism and guarantee rather than calling all three “events.”

**Avoid shared-domain-object coupling.** One global entity model lets every module call methods and inspect state conveniently. It also merges vocabulary, lifecycle, persistence, and invariants. A change in one context becomes a system-wide change.

Use module-owned contract types and explicit translation when meanings or change rates differ. Do not duplicate blindly: stable primitives such as a validated currency code can be shared under a precise owner, while `CustomerStatus` may require distinct sales, billing, and compliance meanings.

**Keep cross-cutting policy bounded.** Identity, authorization, audit, time, money, configuration, telemetry, feature flags, and transactions appear everywhere. A universal `common` module becomes a hidden architecture.

Separate reusable mechanism from contextual policy. A security capability verifies identity; the consuming module decides whether that identity may perform its operation. A telemetry library emits structured data; each module owns meaningful events and objectives. Shared primitives should be small, stable, and explicitly governed.

**Design the application shell.** One composition root can wire modules, adapters, configuration, and lifecycle. It may own startup order, migrations, routing, and process-wide resources. It should not accumulate domain policy.

Keep the shell thin and observable. Module initialization must expose dependencies and failures. Avoid a global service locator that lets any module retrieve any implementation, defeating compile-time rules. Dependency injection is a wiring mechanism, not proof of inversion or modularity.

**Make modules visible at runtime.** Include module identity in structured logs, traces, metrics, audit events, and failure reports. Track module-to-module calls or event handling where useful. In-process boundaries will not appear automatically as network spans.

Do not create expensive instrumentation solely to mimic services. Observe decisions and failure paths: operation, caller module, outcome, latency, transaction, event, queue age, and relevant correlation. Protect sensitive data and avoid high-cardinality identifiers.

**Design testing around boundaries.** Unit-test policy inside a module. Contract-test provided interfaces and adapter implementations. Integration-test persistence, transactions, events, configuration, and the composition root. Test module boundaries for forbidden imports and data access. End-to-end tests cover selected system behavior.

Avoid test helpers that give every test direct database access or construct internal objects across modules. They teach developers to bypass the architecture and can make production boundaries untestable. Provide module-owned fixtures, builders, and test APIs where justified.

**Optimize build and feedback without false independence.** Separate build targets and focused test suites can reduce feedback time. Dependency graphs can select affected tests. A shared release remains a shared release: all modules must be compatible in the assembled artifact.

Do not label a module “independently deployable” until it has a separately versioned artifact, deployment, compatibility policy, operational ownership, and failure boundary. Independent build or team ownership is valuable but different.

**Understand operational advantages.** One application generally means fewer deployments, network policies, service identities, certificates, dashboards, on-call routes, and compatibility matrices. Local calls avoid network partial failure. One process can simplify debugging and resource management.

It also creates a larger blast radius, shared resource contention, coordinated scaling, and one release gate. A memory leak or stop-the-world pause can affect all modules. Process-wide overload controls need fairness so one capability cannot consume every worker, connection, or heap resource.

**Plan resource isolation.** Use bounded pools, queues, concurrency limits, budgets, and scheduling by module or workload. Measure allocation, CPU, blocking, database use, and tail latency. A module boundary alone does not isolate resources.

If one capability needs radically different compute, hardware, scaling, or security, extraction may be justified. First test whether an internal queue, dedicated pool, separate job, or process within the same release resolves the force with lower complexity.

**Assess security and fault isolation.** In-process modules usually share memory, operating-system identity, secrets, and failure fate. Visibility rules prevent accidental access, not a malicious module. Use process or stronger isolation when threat assumptions require it.

Still enforce least access in a monolith: scoped database credentials where practical, module APIs, authorization policy, secret ownership, audited administrative paths, and sensitive-data minimization. Never claim a package boundary is a security sandbox.

**Measure modularity from several kinds of evidence.** Structural measures include forbidden edges, cycles, fan-in, fan-out, contract size, and data access. Change measures include scattering, co-change, owner coordination, build/test impact, and regression distribution. Runtime measures include call cost, contention, error propagation, and resource use.

Let $V=|E_o\setminus A|$ be violation count and $N=|E_o|$. A violation ratio $V/N$ can track one declared graph when $N>0$. It does not weight consequences, reveal missing edges, establish cohesion, or compare systems with different extraction rules. One write bypass can be more serious than many harmless imports.

**Use change scenarios.** Ask what happens if a tax rule, database engine, notification provider, identity policy, report format, or deployment topology changes. Record which modules, owners, schemas, tests, and releases change. A good boundary keeps unrelated decisions stable.

Historical co-change is evidence, not destiny. Files may co-change during a one-time migration or because teams habitually bundle unrelated work. Combine history with responsibility and domain review.

**Recognize extraction forces.** A module becomes a candidate for separate deployment when it has a coherent contract and data authority and when evidence shows sustained need for independent scaling, release, fault isolation, security boundary, technology, geography, regulatory control, or team autonomy.

Pressure alone is insufficient. A hot module sharing transactions and tables with five others is not ready. Extraction readiness requires understanding callers, data, consistency, events, errors, identity, operations, and migration.

**Treat extraction as architecture change.** A function call becomes remote communication with latency, timeout, retry, partial failure, serialization, compatibility, authentication, authorization, observability, and capacity. A local transaction becomes a distributed workflow or redesigned consistency boundary. In-memory shared state needs authority and synchronization.

First stabilize the internal contract, remove unauthorized data access, assign ownership, measure traffic, and exercise failure. Then introduce a local adapter or process boundary, migrate data with reconciliation, add durable communication, and shift callers. Preserve rollback and avoid two uncontrolled writers.

**Avoid the distributed monolith.** Separate services form a distributed monolith when changes require synchronized releases, callers depend on internals, services share database writes, request chains assume atomic success, or no team owns failure. The system pays network and operational cost without gaining autonomy.

Microservice count is not an outcome. Evaluate release coupling, data authority, failure containment, compatibility, ownership, and change. Returning a service to a modular monolith can be a sound correction.

**Govern the monolith as a product.** Maintain a module catalogue, contracts, owners, dependencies, data authority, architectural decisions, exceptions, and review triggers. Require module-aware code review and migrations. Keep generated dependency maps tied to source revisions.

Review boundaries when change scattering, violations, incidents, new scale, ownership, security, or regulation changes. Split, merge, or redefine modules deliberately. A modular monolith is maintained architecture, not a one-time package layout.

## Definitions and Notation

Let $M$ be internal modules, $K$ dependency kinds, and $E_o\subseteq M\times M\times K$ observed edges. Let $A$ be permitted edges. Structural violations are

$$
E_v=E_o\setminus A.
$$

Let $D$ be deployment units and $deploy:M\rightarrow D$ map modules to their main runtime artifact. A modular monolith has one primary $u\in D$ such that most application modules map to $u$; auxiliary jobs do not change the internal modularity claim.

Let $owner(d)\in M$ identify the authority for governed data item $d$. A write by module $x$ is authorized only if $x=owner(d)$ or a declared migration or administrative rule permits it through the owner's invariant-preserving mechanism.

For change scenario $c$, let $T(c)\subseteq M$ be touched modules and $O(c)$ involved owners. Change scattering can be reported as $|T(c)|$ and coordination breadth as $|O(c)|$, but both require interpretation against the scenario.

For $N=|E_o|>0$, $V=|E_v|$, the ratio $r=V/N$ summarizes detected violations. If $N=0$, the ratio is undefined; reporting zero would conceal missing extraction or an empty system.

## Mechanisms, Invariants, or Proof Structure

**Contract invariant.** Other modules depend only on a module's supported contract and documented events, not internal types, tables, files, configuration keys, or framework objects.

**Data-authority invariant.** Every governed mutable datum has one authority for meaning and invariant-preserving writes at a time. Replicas and projections do not become authorities merely because they contain copies.

**Dependency invariant.** Every observed dependency belongs to the allowed labeled relation or a governed exception. Same-process convenience is not an exception mechanism.

**Transaction invariant.** A local atomic transaction has one declared consistency purpose. Cross-module atomic work must be justified and represented; a future deployment split cannot preserve it merely by changing transport.

**Event invariant.** An event identifies the fact, producer authority, payload semantics, occurrence time, ordering scope, delivery mechanism, failure behavior, and consumer idempotency needs. “In process” does not define those properties.

**Deployment invariant.** Shared deployment implies coordinated assembly and release unless a distinct governed mechanism establishes otherwise. Internal API stability can reduce risk but does not create independent deployment.

**Extraction-consequence argument.** Moving a call across a process boundary adds communication and independent failure states. Therefore evidence for an in-process call does not establish remote latency, availability, retry safety, security, or version compatibility. These obligations must be designed and tested explicitly.

**Evidence invariant.** Import checks observe only modeled static edges; database audits observe configured access; traces observe exercised paths; history observes past changes. Modularity conclusions must name and combine their evidence.

## Alternatives and Trade-Offs

**Modular monolith versus unstructured monolith.** Both may deploy once. The modular form invests in contracts, data authority, visibility, and governance; it pays internal mapping and enforcement costs to localize change.

**Modular monolith versus microservices.** The monolith minimizes distribution and operational overhead but shares release, process fate, and coarse scaling. Services can isolate those dimensions but require mature contracts, data ownership, reliability, security, and operations.

**Synchronous contracts versus internal events.** Calls provide immediate results and visible control but couple execution. Events decouple knowledge and support multiple consumers but complicate ordering, failure, transactions, and diagnosis. Use facts for genuine asynchronous reactions, not to hide every dependency.

**One physical database versus separate stores.** One database supports local transactions and simpler operations. Schema and permission boundaries can preserve logical authority. Separate stores increase autonomy and isolation but introduce distributed consistency, replication, and reconciliation.

**Shared kernel versus duplicated concepts.** A small stable shared kernel reduces mapping and inconsistency. It raises coordination and blast radius. Duplicate representations preserve contextual meaning when names coincide but policy differs.

**Global framework conventions versus module autonomy.** Common conventions reduce cognitive and tool cost. They can spread vendor types and constrain every module. Keep conventions at composition and adapter boundaries when policy longevity matters.

**Early extraction versus deferred extraction.** Early services can fit strong known boundaries and isolation requirements. Deferral preserves learning speed and cheap calls. Delay becomes costly if teams ignore internal boundaries; disciplined modularity keeps both options open.

## Failure Modes and Misconceptions

1. **“Monolith means bad architecture.”** Deployment shape does not determine internal responsibility or quality.
2. **“Feature folders make a modular monolith.”** Contracts, access, data authority, and enforcement are required.
3. **“Everything in one process may share everything.”** Convenience is precisely why boundaries need governance.
4. **“One database means every module owns every table.”** Physical storage and semantic write authority are separate.
5. **“Internal interfaces need no contract.”** Callers still depend on semantics, errors, transactions, and compatibility.
6. **“In-process events are reliable.”** Delivery depends on dispatcher, transaction, crash, and persistence behavior.
7. **“Acyclic imports prove modularity.”** Hidden data and change coupling can remain.
8. **“A common module reduces duplication.”** It can centralize unrelated volatility and erase ownership.
9. **“Tests may bypass boundaries safely.”** Test architecture shapes production habits and can hide invalid integrations.
10. **“Separate build targets are independently deployable.”** Deployment, version, operation, and failure boundaries are absent.
11. **“Extracting a module changes only transport.”** It changes timing, failure, consistency, identity, and operations.
12. **“Every module should become a service.”** Many modules lack a deployment force or operationally coherent boundary.
13. **“More services mean more autonomy.”** Shared writes and synchronized releases create a distributed monolith.
14. **“Co-change proves modules should merge.”** Migration and workflow can produce legitimate temporary correlation.
15. **“A modular monolith is transitional.”** It can be the durable best fit for the system's forces.

## Worked Examples

### Example 1

**Situation.** A codebase has `orders`, `billing`, and `shipping` packages, but every package imports every other's internal classes.

**Reasoning.** Names provide navigation, not information hiding. Define supported contracts and data authority, make internal packages invisible, declare allowed edges, and move orchestration to an explicit owner. Architecture tests can then detect new bypasses.

**Conclusion.** Module labels become architecture only when responsibilities and dependencies are controlled.

### Example 2

**Situation.** Billing updates `orders.payment_status` directly because all modules share PostgreSQL.

**Reasoning.** Physical co-location does not grant semantic authority. Orders owns order status and its invariants; Billing owns payment state. Billing reports a payment result through an Orders contract or published fact. Restrict writes by schema role or review and migrate existing direct writes.

**Conclusion.** One database can support modular ownership when access and meaning remain explicit.

### Example 3

**Situation.** `OrderPlaced` is dispatched synchronously before the order transaction commits, and a mail subscriber fails.

**Reasoning.** The event name hides mechanism. If subscriber failure aborts the transaction, this is synchronous collaboration. If the message must survive commit and crash, record it in an outbox atomically and deliver later with retry and idempotency. Define whether consumers may observe an order that later rolls back.

**Conclusion.** Event semantics must include transaction and failure behavior even inside one process.

### Example 4

**Situation.** One tax-rule change touches 2 of 24 modules, while a database column rename touches 17.

**Reasoning.** Tax policy appears localized. Persistence representation leaks broadly through records, queries, and tests. Inventory actual dependencies, place translation behind owned storage contracts, and prevent other modules reading the column directly. Counts guide investigation but do not weight consequences.

**Conclusion.** Change scattering can expose a leaky representation boundary that import rules miss.

### Example 5

**Situation.** Search consumes 70% of CPU during peaks, but it shares the monolith's worker pool and heap.

**Reasoning.** First allocate a bounded pool, queue, cache budget, and admission policy; observe module-level load and tail latency. If search still requires independent compute scaling or process isolation, its coherent read model and contract may support extraction. Do not split before identifying state and update flows.

**Conclusion.** Resource pressure is an extraction force only after the boundary and cheaper isolation mechanisms are evaluated.

### Example 6

**Situation.** Tests construct another module's internal aggregate because it is faster than calling the public API.

**Reasoning.** The tests couple to representation and will not detect contract or authorization errors. Provide module-owned test builders or fixtures, contract tests, and bounded setup APIs. Keep white-box tests inside the owning module and integration tests outside it.

**Conclusion.** Test visibility must reinforce rather than dissolve production boundaries.

### Example 7

**Situation.** An organization extracts Billing by replacing an in-process call with HTTP but keeps shared table writes and one release train.

**Reasoning.** The new service adds latency, timeout, authentication, deployment, and observability while retaining data and release coupling. Restore the module or complete authority separation: contract versioning, billing-owned data, workflow semantics, independent operation, and failure handling.

**Conclusion.** Network separation without semantic and operational autonomy creates a distributed monolith.

### Example 8

**Situation.** The observed graph has 120 edges and 6 forbidden edges.

**Reasoning.** The detected violation ratio is $6/120=5\%$. Review every violation by consequence: a direct cross-module write may be critical; a test-only helper may be lower risk. Confirm the extractor includes generated and reflective paths. The ratio is a trend indicator, not a modularity score.

**Conclusion.** Structural metrics require edge semantics, coverage, and risk interpretation.

### Example 9

**Situation.** Compliance needs a stronger isolation boundary around identity verification, but request policy remains in the main application.

**Reasoning.** Separate credential handling and verification into a restricted process or service with a narrow attestation contract. Keep contextual authorization in consuming modules. Model secrets, identities, timeouts, outage behavior, audit evidence, and fallback. Do not move all authorization merely because identity crossed a process boundary.

**Conclusion.** Extraction can isolate a sensitive mechanism while preserving policy ownership in the monolith.

### Example 10

**Situation.** A regional library system handles cataloguing, membership, loans, fines, notifications, acquisitions, and public search with a small operations team.

**Reasoning.** Define capability modules, catalogue and member data authority, loan invariants, internal contracts, events, schema permissions, module-level telemetry, and focused tests. Retain one deployment to minimize operational overhead. Isolate public-search resources internally; extract only if sustained traffic, public attack surface, or independent availability justifies it.

**Conclusion.** A governed modular monolith can be a deliberate durable architecture for broad capability with limited operational capacity.

## Cross-Program Connections

- **Software Design and Domain Modeling:** bounded contexts, aggregates, invariants, and dependency direction refine module semantics.
- **Software Engineering Patterns:** Facade, Service Layer, Repository, Adapter, Domain Event, and Unit of Work can implement boundaries.
- **Database Engineering:** schemas, transactions, permissions, migrations, projections, and replication shape data authority.
- **Distributed Systems:** extraction introduces partial failure, concurrency, idempotency, ordering, consistency, and reconciliation.
- **Software Delivery and Reliability Engineering:** build selection, releases, telemetry, incidents, recovery, and on-call capacity determine operational fit.
- **Security Engineering:** process identity, secrets, privilege, trust, data classification, and attack surfaces determine isolation needs.
- **Platform Engineering:** catalogues, build systems, policy checks, templates, and observability can support module governance.
- **API and Service Engineering:** internal contracts need precise semantics and become remote contracts if extracted.
- **Testing and Quality Engineering:** architecture, contract, integration, mutation, and end-to-end testing provide complementary evidence.

## References

1. David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM*, vol. 15, no. 12, pp. 1053–1058, 1972. https://doi.org/10.1145/361598.361623
2. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003.
3. Vaughn Vernon, *Implementing Domain-Driven Design*, Addison-Wesley, 2013.
4. Sam Newman, *Building Microservices*, 2nd ed., O'Reilly Media, 2021.
5. Martin Fowler, “MonolithFirst,” *martinfowler.com*, 3 June 2015. https://martinfowler.com/bliki/MonolithFirst.html
6. Neal Ford, Rebecca Parsons, Patrick Kua, and Pramod Sadalage, *Building Evolutionary Architectures*, 2nd ed., O'Reilly Media, 2022.
7. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
8. Paul Clements et al., *Documenting Software Architectures: Views and Beyond*, 2nd ed., Addison-Wesley, 2010.

## Exercises

### Exercise 1

Precisely distinguish monolith, modular monolith, module, service, deployment unit, data authority, internal contract, internal event, distributed monolith, and extraction seam.

### Exercise 2

An extractor reports 200 internal dependency edges, of which 12 violate policy. Three violations are direct writes to another module's tables, four are production imports, and five are test-only imports. Compute the ratio and explain how to triage it without turning the metric into a score.

### Exercise 3

Diagnose a monolith where one shared entity model crosses all modules, every migration can write every schema, synchronous event subscribers run inside caller transactions, and the integration test suite accesses tables directly. Produce an enforceable repair plan.

### Exercise 4

Compare keeping Notifications inside a retail modular monolith with extracting it. Address contract, data authority, scale, failures, transactions, privacy, operations, release, testing, and migration evidence.

### Exercise 5

Transfer the style to a national museum platform with collection management, conservation records, ticketing, membership, donations, research access, public search, sensitive provenance, seasonal load, and a small operations team. Design modules and extraction criteria.

## Answers to the Exercises

### Answer 1

A **monolith** has one primary application deployment. A **modular monolith** keeps that deployment while enforcing cohesive internal modules. A **module** owns responsibilities, contracts, hidden decisions, and usually data semantics. A **service** is a provided capability; the word may refer to an in-process contract or independently operated deployment, so scope must be stated. A **deployment unit** is a separately released artifact or coordinated runtime unit.

**Data authority** owns meaning, invariants, and writes. An **internal contract** governs module collaboration inside the deployment. An **internal event** exposes a fact; delivery may be synchronous, asynchronous, or durable and must be specified. A **distributed monolith** pays for separate deployments while retaining tight data, change, release, or failure coupling. An **extraction seam** is a controlled boundary through which a module can be moved while its contract, state, and behavior are preserved or deliberately changed.

### Answer 2

The detected ratio is $12/200=6\%$. It describes only the extractor's labeled graph and does not weight risk. Triage the three direct writes first because they can bypass another module's invariants and authority. Review the four production imports by exposed internal decision and change consequence. Review test-only imports separately: they may not affect production execution but can conceal invalid integration and create maintenance coupling.

For each violation, record owner, path, dependency kind, affected invariant, current use, remediation, risk, and expiry if temporarily accepted. Verify generated code, reflection, configuration, messages, and data access coverage. Track counts by kind and consequence over time. Do not compare the percentage with another system whose graph or extraction rules differ, and do not infer cohesion or correctness from a reduction.

### Answer 3

First define capability modules, owners, supported contracts, data authority, and allowed edges. Split the shared model into module-owned domain and contract types where meanings or change forces differ. Add explicit translation. Restrict public visibility and production imports; encode architecture rules in modules, packages, and builds.

Assign schema ownership and migration roles. Cross-module data access goes through an owner contract or governed projection; direct writes are prohibited. Classify events by delivery and transaction semantics. Keep genuinely synchronous policy collaboration explicit; use an outbox and idempotent consumers when facts must survive commit and crash. Define failure and ordering.

Move white-box persistence tests into owning modules. Provide module-owned fixtures and bounded setup contracts for integration tests. Add contract, transaction, event, schema-access, composition-root, and end-to-end tests. Inventory reflection, dependency injection, generated code, jobs, and administrative paths. Migrate incrementally with monitored exceptions and compare change scattering, violations, test scope, and incidents.

### Answer 4

Keeping Notifications internal preserves local calls, one release, simple authentication, and cheap access to governed projections. Give it a contract for delivery requests and status, own channel policy and delivery records, minimize copied personal data, and deliver asynchronously when external providers can fail. It can use dedicated pools and queues inside the application.

Extraction is justified if notification load, provider isolation, independent release, security controls, regional delivery, or operational ownership remain distinct enough to outweigh distribution. Then define versioned commands/events, idempotency keys, status queries, retry and duplicate behavior, recipient-data purpose and retention, authentication, authorization, observability, capacity, and outage policy. It owns delivery state; retail modules own business decisions about when a message is required.

Before migration, remove direct table access, stabilize the internal contract, measure volume and latency, and create an outbox. Introduce a transport adapter, shadow or reconcile results, move state with one writer at a time, test provider and service failures, and preserve rollback. Separate deployment is not successful until releases and operations are genuinely independent within declared compatibility.

### Answer 5

Define Collection, Conservation, Ticketing, Membership, Donations, Research Access, Public Search, Identity, and Audit capabilities. Collection owns object identity and catalogue authority; Conservation owns treatment and condition history; Research Access governs scholarly records and restrictions; Public Search consumes approved projections rather than source tables. Ticketing, Membership, and Donations own their financial and personal-data lifecycles.

Use explicit commands, queries, and facts; one physical database may contain owner-specific schemas and permissions. Sensitive provenance and donor data receive classification, narrow contracts, audited access, and retention. Conservation and collection invariants use local transactions where their true consistency boundary requires it. Projection publication uses outbox delivery with replay and correction. The composition shell owns wiring, not museum policy.

Keep one primary deployment to fit operational capacity. Give public search bounded workers, cache, admission, and read projections for seasonal load. Consider extraction when sustained independent scaling, public attack isolation, geographic delivery, or separate availability has evidence and Public Search has a coherent contract, data copy, refresh semantics, and owner. Consider stronger isolation for sensitive provenance only if the threat and regulatory model requires it. Validate import and schema rules, change scenarios, privacy access, seasonal load, degraded operation, restoration, evidence provenance, and staff comprehension.
