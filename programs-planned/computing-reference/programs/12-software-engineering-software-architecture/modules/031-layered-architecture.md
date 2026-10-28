---
module_id: SARCH-031
program: Software Engineering: Software Architecture
level: 1
module_number: 31
title: Layered Architecture
status: complete
last_verified: 2026-09-06
---

# Layered Architecture

## One-Page Review

### Governing question

When does ordering software into layers create useful abstraction and replaceability, and how can architects prevent the layers from becoming ceremonial folders, bypass networks, or latency-producing indirection?

### Essential definitions

- A **layer** is a set of responsibilities at a related abstraction or policy level with explicit rules governing allowed dependencies.
- A **layered architecture** orders layers and constrains how elements in one layer may use elements in another.
- A **uses dependency** means one element requires another's correctly functioning provided behavior to meet its own responsibility.
- A **strict** or **closed** layering rule permits a layer to use only the adjacent lower layer; a **relaxed** or **open** rule permits declared downward skips.
- A **bypass** is a dependency that crosses a layer contrary to the declared rule or through an undeclared mechanism.
- **dependency inversion** places an abstraction where stable policy owns it so lower-level mechanisms implement that abstraction rather than higher policy importing their concrete details.
- **control flow** is runtime transfer of execution; **dependency direction** is static knowledge or required-contract direction. They need not match.
- A **tier** is a separately deployed or physically located part of a system; a layer is a logical dependency boundary. One tier may contain several layers and one layer may span tiers.
- A **vertical slice** groups responsibilities needed for one capability across technical concerns; it can coexist with layers inside the slice.
- A **layer violation** is an observed dependency outside the allowed relation, not merely an aesthetic disagreement.

### Central model, mechanism, or theorem

Let modules $M$ be assigned to ordered layers by $\lambda:M\rightarrow\{0,\ldots,n\}$, where larger numbers represent higher-level policy. If edge $(a,b)$ means $a$ depends on $b$, relaxed downward layering requires

$$
(a,b)\in E\Rightarrow\lambda(a)>\lambda(b),
$$

while strict layering additionally requires $\lambda(a)=\lambda(b)+1$. Same-layer dependencies require a separate declared rule. Acyclic downward edges admit a topological order, but conformance alone does not prove cohesive responsibilities, usable abstractions, acceptable runtime cost, or independent deployment.

### Critical invariants

- state the concern, layer ordering, element kinds, edge semantics, and same-layer rule;
- assign each responsibility to an accountable layer rather than placing files by suffix;
- orient compile-time dependencies toward stable policy and abstractions;
- distinguish static dependency from runtime calls, data flow, deployment, and organization;
- expose provided contracts, hidden decisions, and allowed downward knowledge;
- declare whether layers are strict, relaxed, or selectively open and justify each skip;
- prevent access through shared databases, reflection, generated code, configuration, or framework callbacks from evading the model;
- keep cross-cutting mechanisms behind bounded contracts instead of a universal utility layer;
- test behavior at layer contracts and verify the observed dependency graph against policy;
- treat cycles, bypasses, change scattering, forwarding, latency, and transaction leakage as review signals;
- combine horizontal layering with capability boundaries when global technical layers increase coupling;
- evolve or remove layers when their abstraction no longer protects a meaningful decision.

### Common failures

Common failures include naming `controllers`, `services`, and `repositories` and declaring success; equating layers with network tiers; assuming runtime control must always move downward; allowing every layer to query shared tables; putting business policy in framework callbacks; building an unbounded `common` layer; passing persistence records through all layers; creating pass-through methods with no abstraction; skipping layers secretly for performance; cyclic same-layer imports; applying one global stack to unrelated capabilities; and reporting an acyclic import graph as proof of maintainability.

### Compact example

An order policy calls an `OrderStore` interface it owns. A SQL adapter in the mechanism layer implements that interface. At runtime, the web adapter invokes the policy, and the policy invokes the adapter through the abstraction. Static source dependency from the SQL adapter points inward to the stable interface; runtime control crosses outward. The design preserves policy from SQL detail without pretending execution follows dependency arrows.

### Connections

[SARCH-022](022-module-and-code-views.md) defines dependency and module-view semantics; [SARCH-030](030-creating-an-architecture-description-for-different-audiences.md) governs its communication. [SARCH-032](../ROADMAP.md) next develops modular monoliths, and [SARCH-033](../ROADMAP.md) develops ports, adapters, and inward dependency direction. Software Design and Domain Modeling owns code-level dependency choices; Patterns owns Service Layer and other implementation patterns.

## Governing Question

Layering is among the oldest and most reusable ways to organize software: place responsibilities at different abstraction levels, define what each level provides, and restrict what higher policy may know about lower mechanisms. When the abstractions are real, a reader can reason about one level while relying on contracts below it.

Yet many so-called layered systems are only directory templates. Business rules know SQL schemas, controllers perform transactions, shared utilities know every domain, and any module can bypass the nominal service layer. Other systems enforce every hop so mechanically that simple work crosses five pass-through objects and several network calls.

The governing question is not whether to have three, four, or seven boxes. It is which decisions deserve abstraction boundaries, which dependency relation the layers constrain, how those rules are enforced, and whether the resulting isolation is worth its cognitive and runtime costs.

## Why This Matters

Layers can localize change, protect policy from volatile technology, establish security and validation gates, enable substitution, constrain dependencies, and provide teachable navigation. Operating systems, protocol stacks, compilers, enterprise applications, and platforms all use forms of layering because abstraction lets one level rely on services without understanding every mechanism below.

Layering can also obscure ownership and performance. A global presentation/business/data stack often scatters one capability across distant directories and teams. A request can traverse mechanically thin layers while sharing one database and release. A policy that exists only on a slide provides no boundary at all.

Architectural evaluation must therefore distinguish the intended dependency model, the mechanisms enforcing it, the runtime consequences, and observed change behavior. Layering is a means of controlling knowledge, not a guarantee of quality.

## Prerequisites and Retrieval

Retrieve module, responsibility, information hiding, abstraction, encapsulation, interface, provided service, uses dependency, dependency direction, control flow, data flow, cycle, topological order, cohesion, coupling, stability, policy, mechanism, adapter, dependency inversion, deployment unit, tier, transaction, latency, bypass, conformance, and evidence.

From SARCH-022 retrieve directed module graphs, edge kinds, allowed and observed dependency relations, and the distinction between conceptual modules and language units. From the quality-attribute modules retrieve modifiability, testability, performance, security, availability, and interoperability consequences. Do not assume a source import, runtime call, network hop, and organizational coordination edge are the same relation.

## Learning Objectives

After completing this module, you should be able to:

1. define layers by abstraction and dependency policy rather than directory names;
2. distinguish strict, relaxed, open, closed, opaque, and transparent layer rules;
3. derive conformance conditions over a labeled dependency graph;
4. separate static dependency direction from runtime control and data flow;
5. apply dependency inversion without creating empty interfaces;
6. distinguish logical layers from deployment tiers and trust boundaries;
7. identify bypasses through data, generation, reflection, configuration, and frameworks;
8. compare global horizontal layers with capability slices and hybrid structures;
9. evaluate change isolation, testing, performance, security, and operational consequences;
10. govern exceptions and evolve layers using declared evidence.

## Core Exposition

**Begin with the concern.** Layers can order abstraction, policy, trust, protocol function, hardware dependence, or lifecycle responsibility. These are different dimensions. A diagram that stacks boxes vertically does not reveal which ordering is intended.

State the system of interest, audience, decision, module kinds, edge semantics, current or target state, and evidence. In this chapter, $a\rightarrow b$ means “$a$ statically depends on $b$.” If a tool uses the reverse convention, label it. Do not let page position silently define dependency.

**Define what each layer hides and provides.** A useful layer owns decisions that clients should not know: a representation, device mechanism, transport, persistence strategy, workflow policy, or domain rule. It provides a bounded vocabulary and service. Higher layers depend on that abstraction; lower implementation detail can change without forcing every client to change, within compatibility assumptions.

Dijkstra's account of the THE multiprogramming system described a hierarchy in which each level relied on facilities established below it, enabling construction and reasoning in stages [1]. Parnas later made the change-oriented principle explicit: decomposition should hide design decisions likely to change rather than merely follow processing steps [2]. Modern application layering inherits both ideas but must state its own dependency semantics.

**Name layers by responsibility.** `Presentation`, `business`, and `data` can be useful orientation labels, but they are not definitions. A responsibility-based description says: interaction adapters translate external requests; application policy coordinates use cases and authorization context; domain policy owns business invariants; persistence adapters translate stable storage contracts into a database mechanism.

Names such as `service`, `manager`, `helper`, and `common` are especially weak when nothing bounds their ownership. For each layer, state what belongs, what does not, what it may use, what uses it, which decisions it hides, and which contracts it provides.

**Choose the ordering.** Let layer 0 be the lowest mechanism and layer $n$ the highest policy. A dependency from higher to lower follows the declared order. This numbering is conventional; the invariant, not visual height, matters.

The order should reflect stable knowledge. Higher policy can depend on a stable lower abstraction without knowing its implementation. If low-level code imports high-level policy to register callbacks or implement an interface owned above, the architecture may be applying inversion rather than violating it. Model the interface and implementation relation separately.

**Distinguish strict and relaxed layering.** In strict layering, layer $i$ uses only layer $i-1$. This forces every service to be mediated through the adjacent abstraction. It can simplify substitution and ensure validation, authorization, translation, or instrumentation occurs at one boundary.

In relaxed layering, a layer may use any lower layer. This reduces pass-through code and sometimes cost, but higher levels know more lower-level contracts. A selectively open design names permitted skips, their purpose, and their consequences. “Open” does not mean unrestricted.

The terms **closed layer** and **opaque layer** are often used for a layer that cannot be bypassed; **open** or **transparent layer** can allow clients to reach lower services. Because literature varies, define the local meaning rather than relying on the adjective alone [3].

**Specify same-layer rules.** An ordered layer model says nothing automatically about dependencies within one layer. If every domain module may import every other domain module, the system can form a large strongly connected region while conforming to vertical ordering.

Define whether peer modules may depend on one another, through which contracts, and whether capability or ownership boundaries constrain them. A useful policy might permit acyclic peer dependencies within a capability, prohibit cross-capability internals, and require shared concepts to have explicit owners.

**Separate dependency from control flow.** A runtime request often enters through a low-level mechanism such as an HTTP controller, then calls high-level policy. Static source dependency can still point from the controller to a policy interface. Later, policy calls a persistence interface that an outer adapter implements. Runtime control crosses the boundary in both directions; source knowledge can point consistently toward policy.

Conflating the two leads to claims such as “the domain must call downward into the database.” The domain needs storage behavior, not database detail. The interface can be owned by the policy that consumes it. The adapter depends on that interface and supplies the mechanism.

**Use dependency inversion deliberately.** Dependency inversion changes source knowledge by introducing an abstraction owned on the stable side. It is valuable when the abstraction expresses a real policy need, supports alternatives or testing, and keeps volatile details out.

It is not valuable merely because every class must have an interface. An interface identical to one implementation's methods, stored beside that implementation, and exposing its data types does not invert a design decision. Ask who owns the vocabulary and which change it isolates.

**Distinguish layers from tiers.** A logical layer constrains knowledge. A deployment tier identifies location, process, node, zone, or independently deployed unit. A browser, application server, and database server form tiers; each may contain several logical layers. Conversely, one logical policy layer can execute in several tiers.

Moving each logical layer into a network service changes latency, failure, versioning, security, observability, and deployment coordination. It does not make the layering “more architectural.” Keep module, runtime, deployment, data, and ownership views separate and relate them through stable identifiers.

**Account for data dependencies.** A clean import graph can conceal shared schemas, tables, files, caches, and messages. If two layers read and write the same record representation, they depend on its semantics even without imports. Passing database entities from persistence through domain to presentation leaks storage decisions upward.

Translate at boundaries when representations encode different responsibilities or change reasons. Translation has code and runtime cost, so do not copy fields by ritual. Preserve domain invariants, absence semantics, identity, units, versioning, and error information explicitly.

**Control framework dependence.** Framework annotations, base classes, callbacks, global registries, reflection, code generation, and dependency injection configuration can pull mechanism concerns into every layer. Decide whether the convenience is an accepted constraint, isolated behind adapters, or represented as a dependency.

Do not claim framework independence when domain classes require framework lifecycle, serialization, or persistence behavior. Conversely, a small stable annotation may be a rational trade-off. Measure the actual change and test consequences instead of treating purity as an end.

**Constrain cross-cutting concerns.** Authentication context, authorization decisions, observability, transactions, error handling, configuration, and caching cross many paths. Placing all of them in a “common” layer creates universal coupling.

Separate policy from mechanism. Authentication adapters establish verified identity; application policy decides authorization; infrastructure emits telemetry through bounded instrumentation; transaction ownership belongs with the consistency boundary; error translation occurs at interfaces. Some cross-cutting mechanisms may be woven or provided by a platform, but their semantics and failure behavior remain architectural.

**Preserve transaction and consistency boundaries.** A presentation layer should not open a database transaction that spans unbounded business work. A domain layer should not assume remote operations participate atomically. An application layer may coordinate a local consistency boundary and record outbound work, while integration mechanisms handle retries and partial failure.

Layering cannot create distributed atomicity. If logical layers become remote tiers, every crossing acquires partial failure and version skew. Re-evaluate contracts, idempotency, timeout, and observability rather than keeping an in-process abstraction unchanged over the network.

**Evaluate performance honestly.** Additional function calls or translations are usually cheap relative to network and storage work, but allocation, serialization, copying, synchronization, and repeated queries can matter. Strict layering can route hot operations through unnecessary indirection or prevent specialized lower-level access.

Measure representative workloads and isolate the actual cost. A justified bypass states the scenario, evidence, scope, owner, security and change consequences, and review trigger. Do not dissolve the entire dependency rule because one path is hot, nor hide a permanent exception in undocumented code.

**Evaluate security boundaries separately.** Layers can centralize input validation, authorization, output encoding, and access to sensitive mechanisms. Yet a layer is not automatically a trust boundary. Code in one process may share identity, memory, privileges, and failure fate.

Map trust, privilege, and data classification explicitly. Prevent lower mechanism code from making policy decisions it cannot contextualize. Ensure alternate entry points, jobs, administrative paths, and generated clients cannot bypass security policy. Defense in depth may repeat validation at distinct trust boundaries; that is not necessarily a layering defect.

**Use layers with capability boundaries.** A global horizontal stack makes all presentation code peers, all application services peers, and all persistence code peers. One business change may touch distant folders and teams. It also makes cross-capability access easy because same-layer boundaries are weak.

A vertical-slice design groups one capability's interface, policy, domain, and mechanism adapters while preserving inward dependency rules within that slice. Shared capabilities expose explicit contracts. This hybrid keeps local navigation and ownership while retaining layered isolation where it protects policy.

Neither geometry is universally superior. Global layers can fit small applications, common workflow, and specialized teams. Capability slices fit distinct domain ownership and independent evolution. Examine change history, coordination, invariants, and deployment rather than following fashion.

**Avoid pass-through layers.** A layer that forwards every call and data object without translation, policy, validation, isolation, or ownership adds cost without abstraction. Before removing it, check whether it is an intended future seam, an access-control point, a compatibility facade, or a transaction owner.

If it owns no durable decision, merge it or redefine responsibility. Do not preserve empty ceremony because a template says every request needs a controller, service, manager, repository, and data-access object.

**Test at contracts and behavior.** Unit-test policy without volatile mechanisms when substitution is part of the design. Contract-test implementations against required semantics. Integration-test translations, transactions, errors, concurrency, security, and framework wiring. End-to-end tests verify selected behavior across layers but provide poor localization alone.

Do not mock every adjacent object automatically. Over-mocking reproduces implementation choreography and makes refactoring expensive. Use fakes or real bounded dependencies where behavior matters, and reserve mocks for observable collaboration obligations.

**Enforce the dependency graph.** Define allowed edges by source sets, namespaces, packages, modules, build targets, or architecture rules. Extract observed imports and build dependencies. Include generated code, schema dependencies, plugins, reflection registrations, and configuration where possible.

Conformance requires $E_{observed}\subseteq E_{allowed}$ within the extractor's scope. Unknown dynamic edges are evidence gaps. Maintain exceptions with owner, rationale, risk, scope, and expiry. A green check proves only that modeled observed edges satisfy modeled rules.

**Diagnose cycles.** Because all permitted inter-layer edges descend under $\lambda$, they cannot form an inter-layer directed cycle: following an edge strictly decreases a nonnegative integer and cannot return to its starting value. A cycle therefore exposes an upward edge, a same-layer cycle, or an edge excluded from the model.

Break harmful cycles by reassigning ownership, splitting responsibility, moving a shared concept to the module that owns it, introducing a policy-owned contract, using an event, or admitting that the modules form one unit. Do not mechanically move code into `common`, which often preserves the coupling under a less informative name.

**Assess change evidence.** For changes $X$, record touched modules, layers, owners, build targets, releases, incidents, and defects. A layer boundary is useful if changes to hidden decisions remain localized and clients rely on stable contracts. High scattering may mean a leaky abstraction, a cross-cutting policy without ownership, or an incorrectly chosen layer dimension.

Change metrics need interpretation. A regulatory change legitimately touching several capabilities is different from a database column rename rippling into user interfaces. Combine structural graphs, history, interviews, tests, and incident evidence.

**Evolve the architecture.** Layers should change when abstraction, technology, policy, or ownership changes. Split an overloaded layer, merge empty forwarding layers, introduce a capability boundary, retire a bypass, or make a hidden cross-layer dependency explicit.

Preserve decision rationale and migration states. During transition, label old and target dependency rules, permitted bridges, owners, and removal criteria. A half-migrated system must not be described as if only the target graph exists.

## Definitions and Notation

Let $M$ be modules and $E\subseteq M\times M\times K$ observed dependency edges labeled by kind $K$. Let $\lambda:M\rightarrow\{0,\ldots,n\}$ assign each module to a layer, where larger values mean higher policy.

For dependency kinds governed by relaxed downward layering,

$$
E_{down}=\{(a,b,k)\in E:\lambda(a)>\lambda(b)\}.
$$

Strict adjacency further requires $\lambda(a)-\lambda(b)=1$. Let $A\subseteq M\times M\times K$ be explicitly allowed edges. A violation is $E_{observed}\setminus A$; an unused allowance is not a violation but may indicate overbroad policy.

Let $P\subseteq M$ contain stable policy modules and $I\subseteq M$ mechanism implementations. Dependency inversion introduces contract $c$ owned with policy such that policy depends on $c$ and implementation realizes $c$; the policy does not require the implementation's concrete representation.

A **layer crossing cost** for scenario $s$ can be decomposed as

$$
C_s=\sum_{e\in path(s)}(c_{call}(e)+c_{translate}(e)+c_{io}(e)+c_{coord}(e)).
$$

This accounting model identifies sources of cost; it does not assume each term is independent or constant.

## Mechanisms, Invariants, or Proof Structure

**Downward-order theorem.** If every dependency edge strictly decreases $\lambda$, the inter-layer graph is acyclic. Proof: assume a cycle $m_0\rightarrow m_1\rightarrow\cdots\rightarrow m_k=m_0$. Strict decrease gives $\lambda(m_0)>\lambda(m_1)>\cdots>\lambda(m_k)=\lambda(m_0)$, an impossibility.

The theorem does not cover same-layer edges, unobserved dynamic dependencies, shared data, or edge kinds outside the rule. It proves an ordering property, not good decomposition.

**Abstraction invariant.** A layer exposes a stable contract in its own vocabulary and hides lower representation choices. Leaking SQL rows, transport status codes, framework request objects, or vendor types upward weakens this invariant unless declared as a deliberate constraint.

**Policy-ownership invariant.** When high policy must be independent of a lower mechanism, the required contract belongs with the policy boundary. Locating the abstraction beside the mechanism can retain conceptual outward dependence even if imports look inverted.

**Bypass invariant.** Every cross-layer access follows an allowed contract or a governed exception. Shared storage, reflection, generated clients, configuration, background jobs, and administrative entry points count as access paths.

**Layer/tier distinction.** Logical conformance makes no claim about process or network placement. A separate deployment mapping is required before reasoning about latency, partial failure, independent release, or privilege isolation.

**Evidence invariant.** Static checks establish only their extracted graph. Runtime traces establish only observed paths for a window. Change history establishes past co-change. Combine evidence and state limitations before concluding the layers isolate change.

## Alternatives and Trade-Offs

**Strict versus relaxed layers.** Strict layers make mediation and substitution explicit but can create forwarding, translation, and hot-path cost. Relaxed layers reduce ceremony but expose lower abstractions to more clients. Selective openness keeps exceptions visible.

**Global horizontal layers versus vertical capability slices.** Horizontal layers centralize technical expertise and common policy but scatter capabilities and invite peer coupling. Slices improve ownership and navigation but can duplicate mechanisms or diverge in conventions. Shared platform contracts and local inward layers form a common hybrid.

**Direct dependency versus inverted contract.** Direct use is simpler when the implementation is stable and substitution has no value. Inversion protects policy and testability when mechanism volatility matters, at the cost of another abstraction and mapping.

**Shared model versus boundary translation.** Sharing reduces mapping code and short-term friction. Translation preserves autonomy and vocabulary but can lose information or consume resources. Translate where representations encode different ownership or change reasons.

**In-process layers versus remote tiers.** In-process calls are simpler and share failure and transaction context. Remote placement can isolate scaling or ownership but adds latency, partial failure, security, observability, and compatibility work. Do not distribute a system solely to make layers visible.

**Framework-centered versus policy-centered organization.** Framework conventions accelerate routine delivery. Policy-centered boundaries protect durable rules from tool churn. Accept framework coupling explicitly where its productivity benefit exceeds expected change cost.

**Automatic enforcement versus review.** Automated rules provide repeatable coverage over modeled edges. Human review interprets responsibility, semantic leakage, and justified exceptions. Neither substitutes for the other.

## Failure Modes and Misconceptions

1. **“Folders are layers.”** Directories show placement; layers require responsibility and dependency rules.
2. **“UI/business/data is universally correct.”** The right ordering depends on hidden decisions and change forces.
3. **“All calls must move downward.”** Runtime control and static dependency are different relations.
4. **“A layer is a deployment tier.”** Logical knowledge boundaries do not imply network placement.
5. **“Strict layering is always cleaner.”** Mandatory forwarding may add no abstraction and harm performance.
6. **“Relaxed layering means any bypass is acceptable.”** Permitted skips still require explicit policy.
7. **“Interfaces automatically invert dependencies.”** Ownership and vocabulary determine which decision is protected.
8. **“A clean import graph means no coupling.”** Data, schemas, configuration, reflection, generation, and releases can couple layers.
9. **“Shared utilities are the bottom layer.”** An unbounded common bucket becomes a high-fan-in change surface.
10. **“Entities can pass unchanged everywhere.”** Shared representations often leak persistence, transport, or UI decisions.
11. **“Cross-cutting concerns belong in every layer.”** Their policy and mechanism need explicit ownership and boundaries.
12. **“More layers mean more architecture.”** Empty pass-through layers add indirection without information hiding.
13. **“Acyclic means modular.”** An acyclic graph can still contain incoherent responsibilities and unstable contracts.
14. **“Layer conformance proves maintainability.”** It proves a bounded graph property, not change isolation or usability.
15. **“Once established, layers are permanent.”** Boundaries must evolve with decisions, evidence, and ownership.

## Worked Examples

### Example 1

**Situation.** A four-layer application assigns web adapters to layer 3, application policy to 2, domain policy to 1, and persistence mechanisms to 0. A web module imports a SQL mapper.

**Reasoning.** The edge descends from 3 to 0, so it satisfies relaxed downward order but violates strict adjacency. More importantly, it leaks storage representation into interaction code. Either route through the application/domain contract, declare and justify a read-optimized exception with its consequences, or revise the architecture if direct querying is intentional.

**Conclusion.** Numeric order detects one rule; responsibility and information-hiding review determine architectural fitness.

### Example 2

**Situation.** A controller invokes an application use case, which invokes an `InvoiceStore` interface implemented by a SQL adapter. A reviewer says the SQL adapter receives control from above, so dependency direction is violated.

**Reasoning.** Runtime control reaches the adapter, but source knowledge differs. Application policy owns and imports the storage contract. The adapter imports and implements that contract. Wiring supplies the implementation. No policy source import targets SQL types.

**Conclusion.** Control flow can cross outward while static dependencies continue to point toward stable policy.

### Example 3

**Situation.** A strict architecture requires presentation to call application, application to call domain, and domain to call infrastructure through three forwarding interfaces.

**Reasoning.** The domain should not call infrastructure detail. Move the required persistence abstraction to the policy side and let the adapter implement it. Remove forwarding layers that own no validation, policy, translation, transaction, or compatibility decision. Retain only boundaries that hide something meaningful.

**Conclusion.** Strictness cannot justify empty indirection or outward policy dependence.

### Example 4

**Situation.** Imports are acyclic, but billing and shipping write the same `orders` table and interpret status values differently.

**Reasoning.** The import extractor omitted a shared-data dependency. Model the schema, write authority, invariants, and compatibility. Assign order-state authority, expose a contract or events, and migrate unauthorized writes. Until then, the nominal layers do not isolate either capability.

**Conclusion.** Data semantics can bypass clean source layering.

### Example 5

**Situation.** A team proposes deploying presentation, application, domain, and persistence as four network services.

**Reasoning.** Logical separation does not require remote boundaries. The proposal adds four-version coordination, authentication, tracing, timeouts, partial failure, and latency without establishing independent capabilities. Keep cohesive logical layers in one deployment unless scaling, security, ownership, or release evidence justifies a remote boundary.

**Conclusion.** Turning layers into tiers can exchange cheap in-process structure for distributed-systems cost.

### Example 6

**Situation.** One request crosses six in-process boundaries, copies a 2 MB structure four times, and misses its latency objective.

**Reasoning.** Use the crossing-cost model to separate call, translation, I/O, and coordination cost. Measurement shows copying dominates. Replace whole-object mappings with a bounded immutable view on this path or fuse two non-owning transformations while preserving policy contracts. Record the exception and regression evidence.

**Conclusion.** Optimize measured mechanisms without discarding unrelated boundaries.

### Example 7

**Situation.** All capabilities depend on `common`, which contains dates, authorization shortcuts, database access, and customer rules.

**Reasoning.** High fan-in hides unrelated ownership and makes small changes system-wide. Keep only genuinely stable primitives with explicit semantics. Move customer rules to their capability, authorization decisions to application policy, database access behind owned ports, and context-specific date policy to its owner.

**Conclusion.** A universal bottom layer often conceals a dependency hub rather than providing a coherent abstraction.

### Example 8

**Situation.** A background job writes directly to persistence and bypasses validation used by the HTTP path.

**Reasoning.** Entry points differ, but policy invariants do not. Route both through the same application/domain operation, or place invariant enforcement in the authoritative domain/storage boundary when every writer must obey it. Add architecture checks for job wiring and tests covering alternate paths.

**Conclusion.** Layer rules must include noninteractive and administrative entry points.

### Example 9

**Situation.** A global technical-layer layout makes one refund change touch nine directories and three teams.

**Reasoning.** The change graph shows capability ownership cuts across horizontal placement. Group refund interaction, application, domain, and adapters within a refund slice; retain inward dependencies and shared payment contracts. Compare subsequent change scattering, boundary violations, and duplicated mechanisms.

**Conclusion.** Capability slices can preserve local layering while reducing global horizontal coupling.

### Example 10

**Situation.** A medical device controller uses layers for device I/O, signal processing, safety policy, clinical workflow, and interface presentation.

**Reasoning.** Define the ordering and evidence separately for control latency, safety, and human interaction. Safety policy owns threshold and fail-safe contracts; device adapters implement bounded acquisition and actuation interfaces. A time-critical stop path may have a governed skip with independent safety analysis. Map logical layers to processes and hardware, validate alternate entry paths, measure worst-case cost, and trace hazards to tests.

**Conclusion.** High-consequence layering needs explicit exceptions, physical mappings, timing evidence, and safety assurance—not only an import rule.

## Cross-Program Connections

- **Software Design and Domain Modeling:** dependency direction, responsibility, cohesion, and component-scale inversion refine layer internals.
- **Software Engineering Patterns:** Service Layer, Repository, Facade, Adapter, Dependency Injection, and Gateway can implement boundaries without defining the entire architecture.
- **Operating Systems:** hardware abstraction and subsystem layering illustrate ordered facilities, privileged crossings, and performance exceptions.
- **Network Engineering:** protocol layering distinguishes service, interface, encapsulation, and peer communication, with deliberate cross-layer mechanisms.
- **Compiler Engineering:** front ends, intermediate representations, optimization, and back ends show both pipeline and abstraction layering.
- **Database Engineering:** schemas, transactions, query mechanisms, and mapping reveal hidden data-layer coupling.
- **Security Engineering:** trust and privilege boundaries may align with layers but require separate threat and enforcement models.
- **Testing and Quality Engineering:** contract, integration, architecture, and end-to-end tests provide different evidence at layer boundaries.
- **Platform Engineering:** platform APIs can stabilize lower mechanisms, while universal platform dependencies can become broad coupling.

## References

1. Edsger W. Dijkstra, “The Structure of the ‘THE’-Multiprogramming System,” *Communications of the ACM*, vol. 11, no. 5, pp. 341–346, 1968. https://doi.org/10.1145/363095.363143
2. David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM*, vol. 15, no. 12, pp. 1053–1058, 1972. https://doi.org/10.1145/361598.361623
3. Frank Buschmann et al., *Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*, Wiley, 1996.
4. Paul Clements et al., *Documenting Software Architectures: Views and Beyond*, 2nd ed., Addison-Wesley, 2010.
5. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.
6. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002.
7. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003.
8. Robert C. Martin, *Clean Architecture: A Craftsman's Guide to Software Structure and Design*, Prentice Hall, 2017.

## Exercises

### Exercise 1

Define layer, uses dependency, strict layering, relaxed layering, bypass, dependency inversion, control flow, tier, vertical slice, and conformance. Explain why a directory stack is insufficient evidence of layering.

### Exercise 2

Modules have layer assignments $\lambda(A)=3$, $\lambda(B)=2$, $\lambda(C)=1$, and $\lambda(D)=0$. Edges are $A\rightarrow B$, $A\rightarrow C$, $B\rightarrow C$, $C\rightarrow D$, and $D\rightarrow B$. Classify each under strict and relaxed downward rules, and identify the cycle.

### Exercise 3

Diagnose an application where controllers pass database entities to services, services expose the same entities to user interfaces, scheduled jobs update tables directly, and all modules import a framework-specific base class. Propose a layered repair with enforceable boundaries.

### Exercise 4

Compare a global presentation/application/domain/infrastructure stack with vertical capability slices for an insurance platform. Address ownership, data authority, transactions, shared policy, testing, build structure, deployment, and change evidence.

### Exercise 5

Transfer layering to an autonomous greenhouse system containing sensors, local control, safety cutoffs, optimization, cloud analytics, technician interfaces, intermittent connectivity, and physical actuators. Define layers, exceptions, deployment mappings, and evidence.

## Answers to the Exercises

### Answer 1

A **layer** groups related responsibilities at an abstraction or policy level and constrains dependencies. A **uses dependency** means a client requires a provider's correct service. **Strict layering** permits only adjacent downward dependencies; **relaxed layering** permits declared downward skips. A **bypass** crosses contrary to the rule or through an undeclared access path.

**Dependency inversion** makes lower mechanisms implement an abstraction owned by stable policy. **Control flow** describes runtime execution and need not follow static dependency direction. A **tier** is a deployment or location boundary. A **vertical slice** groups one capability across technical concerns, possibly with internal layers. **Conformance** compares observed dependencies with allowed ones within stated evidence limits.

Directories show file placement but not responsibilities, hidden decisions, dependency semantics, shared data, reflection, configuration, generation, runtime behavior, or enforcement. They become evidence only when mapped to declared layers and checked alongside other access paths.

### Answer 2

$A\rightarrow B$ moves $3\rightarrow2$ and satisfies strict and relaxed rules. $A\rightarrow C$ moves $3\rightarrow1$ and violates strict adjacency but satisfies relaxed downward order. $B\rightarrow C$ and $C\rightarrow D$ each descend by one and satisfy both. $D\rightarrow B$ moves $0\rightarrow2$, so it violates both downward rules.

The path $B\rightarrow C\rightarrow D\rightarrow B$ is a cycle. It includes the upward edge $D\rightarrow B$. Removing that edge can restore the numeric order, but the repair must address responsibility: introduce a policy-owned contract, move ownership, publish a suitable event, or merge falsely separated modules. Merely hiding the import does not remove a shared-data or runtime dependency.

### Answer 3

The persistence representation has leaked through every nominal layer, alternate jobs bypass policy, and the framework is a system-wide dependency. Define interaction adapters, application operations, domain policy, policy-owned required contracts, and infrastructure adapters. Create domain types that express business identity, absence, units, and invariants; translate database records at the persistence boundary and view representations at the interaction boundary.

Route controllers and jobs through the same application operations. Place invariant enforcement in domain policy and authoritative constraints where all writers must obey it. Make transaction ownership explicit. Isolate framework request, lifecycle, persistence, and scheduling types in adapters where practical; document accepted stable annotations if full isolation is not worthwhile.

Enforce imports and build dependencies by module or package rules. Inspect job configuration, dependency-injection wiring, generated code, schemas, and reflective registrations. Add domain tests, contract tests for adapters, integration tests for mapping and transactions, and end-to-end tests for HTTP and job paths. Migrate incrementally with governed exceptions rather than claiming the target structure already exists.

### Answer 4

A global stack centralizes interaction, application, domain, and infrastructure conventions. It can suit a small coherent platform and specialized teams, but an insurance capability change may scatter across claims, policy, billing, and persistence folders. Same-layer imports and one shared model make ownership and authority porous.

Capability slices group claims, underwriting, billing, and policy administration around their own vocabulary, application operations, domain rules, adapters, tests, and owners. Each slice can use inward dependency rules. Shared identity, pricing, audit, or document capabilities need explicit contracts and owners rather than a common bucket. Duplication is acceptable when concepts differ; shared mechanisms can be provided through narrow platform contracts.

Data authority and transaction boundaries should follow business invariants, not folders. Cross-capability workflows need messages or explicit services with idempotency and partial-failure handling. Repository and build layout can remain one deployment while enforcing modules; independent services require separate evidence for scaling, ownership, security, or release benefit. Compare approaches using change scattering, cross-owner coordination, unauthorized data access, build scope, defect propagation, contract stability, and operational cost—not aesthetics alone.

### Answer 5

Define device adapters for sensor acquisition and actuation; local signal processing for validation, calibration, and derived state; safety policy for hard limits and fail-safe actions; greenhouse control policy for temperature, moisture, ventilation, and irrigation; optimization policy for longer-horizon plans; synchronization adapters for cloud exchange; cloud analytics for fleet learning; and technician interaction adapters.

Static dependencies point toward stable acquisition, actuation, safety, and policy contracts. Runtime sensor events enter from device mechanisms and control actions return to actuators. Safety owns its contracts and can preempt normal optimization. A hard-wired emergency cutoff may deliberately bypass higher layers; document its authority, conditions, independence, and test evidence. Cloud recommendations cannot override local safety and must tolerate stale, duplicate, or missing connectivity.

Map logical layers to the embedded controller, safety hardware, gateway, cloud services, and technician device without treating those tiers as layers. Define state authority, clocks, units, calibration, manual override, authentication, update, and degraded behavior. Verify dependency rules, contract semantics, worst-case control latency, sensor boundary values, actuator failures, disconnected operation, stale recommendations, unsafe commands, recovery, and operator comprehension. A passing import graph is only one part of the safety and operational evidence.
