---
module_id: SARCH-022
program: Software Engineering: Software Architecture
level: 1
module_number: 22
title: Module and Code Views
status: complete
last_verified: 2026-09-06
---

# Module and Code Views

## One-Page Review

### Governing question

How should an architecture description expose the static organization of implementation responsibilities so that developers can reason about change, allowed dependencies, visibility, ownership, build impact, and conformance without confusing source structure with runtime behavior?

### Essential definitions

- A **module** is a statically identifiable implementation unit with responsibilities, provided surface, hidden decisions, and dependency rules.
- A **code element** is a repository, package, namespace, source set, library, file group, generated unit, or other build-visible implementation artifact.
- **decomposition** is the containment relation that partitions a system into implementation units.
- A **uses dependency** means one module requires another's correctly functioning provided surface to meet its own responsibilities.
- **visibility** determines which names or implementation details another unit may access.
- An **interface** is the declared externally usable surface; it is not identical to every public symbol.
- **information hiding** assigns likely-to-change design decisions behind stable module interfaces.
- A **layer** constrains allowed use according to an abstraction or responsibility ordering; a directory level alone is not a layer.
- A **dependency cycle** is a directed path from a module back to itself through one or more dependency edges.
- **conformance** is agreement between declared module rules and the actual source, build, and generated dependency graph within stated limits.

### Central model, mechanism, or theorem

Represent a module view as a directed labeled graph $G_M=(M,E)$, where $M$ is a set of modules and an edge $(a,b,k)$ means module $a$ depends on module $b$ by dependency kind $k$. Let $A\subseteq M\times M\times K$ be allowed dependencies. Structural conformance requires

$$
E_{observed}\subseteq A.
$$

For a change to hidden decision $x$ owned by module $m$, define an observed change set $C(x)$. Effective information hiding aims to keep $C(x)$ near the owning boundary. Neither a small graph nor an acyclic graph alone proves good modularity.

### Critical invariants

- state the viewpoint, audience, concern, scope, lifecycle state, and dependency semantics;
- give each module a cohesive responsibility and accountable owner;
- separate provided interface, required interface, and hidden implementation decisions;
- distinguish containment, uses, visibility, build, generation, and test dependencies;
- orient every dependency edge explicitly and define what its direction means;
- prohibit bypasses around declared interfaces, including reflection and generated code where relevant;
- map conceptual modules to actual code and build units without claiming a false one-to-one relation;
- expose cycles, shared mutable state, unstable dependencies, and fan-out as review signals rather than verdicts;
- reconcile module views with runtime, deployment, data, and organizational views;
- check declared rules against source and build evidence and maintain justified exceptions.

### Common failures

Common failures include drawing folders instead of responsibilities; treating every public symbol as supported API; labeling a package diagram “architecture”; reversing dependency arrows; mixing containment with uses; assuming imports equal semantic dependencies; ignoring generated code, reflection, configuration, tests, and build plugins; demanding zero cycles without defining edge kinds; placing shared data or utilities outside ownership; using layers that any module can bypass; equating compile-time modules with deployment services; and reporting a green dependency tool as proof of evolvability.

### Compact example

An order module calculates order state and exposes `place`, `cancel`, and query contracts. It may depend on a pricing interface, but pricing must not import order internals. A database adapter implements an order repository interface owned by the order boundary. If the source graph shows domain code importing the adapter, the observed edge violates the allowed dependency set even when the program builds.

### Connections

[SARCH-015](015-modifiability-and-evolvability-tactics.md) supplies change-localization tactics; [SARCH-016](016-testability-tactics.md) supplies controllability and substitution; [SARCH-021](021-context-views.md) fixes the system boundary. [SARCH-023](../ROADMAP.md) introduces runtime components and connectors, while [SARCH-027](../ROADMAP.md) later specializes development and build views.

## Governing Question

Source trees always have structure, but incidental structure is not necessarily architectural structure. A directory may collect files by framework convention while one business rule is scattered across controllers, services, jobs, database callbacks, and configuration. Conversely, several repositories can implement one coherent module under shared ownership and contracts.

The governing question is how to describe static implementation responsibilities and dependency constraints at a resolution useful for change. The description must connect conceptual decisions to observable code without pretending that packages, libraries, repositories, processes, and teams are interchangeable.

## Why This Matters

Most software evolution occurs through code changes. If a business rule, security policy, protocol decision, or storage assumption lacks an owning module, every change becomes a search problem. Undocumented dependencies increase build scope, regression risk, coordination, and accidental exposure.

Module views support onboarding, impact analysis, parallel development, reuse, test strategy, build partitioning, and architectural conformance. They reveal whether a promised boundary has a real interface and whether forbidden knowledge leaks through imports, schemas, shared state, generated clients, reflection, or deployment configuration.

Static views also have sharp limits. A clean package graph does not show runtime call order, queueing, concurrency, failure propagation, data consistency, or deployment coupling. A cyclic import can be harmful, but an acyclic graph can still centralize every decision in a “common” library. Evidence must match the claim.

## Prerequisites and Retrieval

Retrieve system of interest, responsibility, module, interface, implementation, dependency, containment, visibility, abstraction, information hiding, cohesion, coupling, cycle, layer, namespace, package, repository, library, build unit, generated code, test double, ownership, change scenario, evidence, and conformance.

From prior modules, retrieve architectural significance, scope, quality scenarios, decisions, modifiability tactics, test seams, interoperability contracts, conflict resolution, and context boundaries. You should be able to distinguish a conceptual module from a runtime component and a source dependency from a network interaction.

## Learning Objectives

After completing this module, you should be able to:

1. select module-view concerns, scope, element types, and dependency semantics;
2. decompose implementation around hidden decisions and coherent responsibilities;
3. distinguish containment, uses, visibility, build, generation, and test relations;
4. specify provided and required interfaces without exposing implementation details;
5. reason about dependency direction, cycles, fan-in, fan-out, and instability;
6. define allowed dependency rules and justified exceptions;
7. map conceptual modules to repositories, packages, namespaces, and build targets;
8. detect hidden dependencies through shared data, reflection, configuration, and generation;
9. reconcile static organization with runtime, deployment, data, and ownership views;
10. evaluate structural conformance without overstating modularity or changeability.

## Core Exposition

**Define the viewpoint before drawing.** State the stakeholders and concerns: developers may need navigation and allowed dependencies; maintainers need change ownership; build engineers need target relationships; security reviewers need visibility and privileged surfaces; managers need coordination boundaries. Define element and relation types, notation, scope, abstraction, current or target state, and known omissions.

ISO/IEC/IEEE 42010:2022 is the current published architecture-description edition as checked on 2026-09-06. It treats model kinds and viewpoints as governed conventions rather than assuming one universal diagram [1]. “Module diagram” is therefore insufficient unless readers know what nodes, edges, nesting, color, and status mean.

**Use module as an architectural term.** Languages and build systems use “module” differently. A Java module, Python module, Rust crate, Go package, C translation unit, library target, and repository provide different enforcement. An architectural module is a responsibility and dependency boundary that may map to one or several technical units. Record the mapping and enforcement rather than relying on the shared word.

**Decompose by hidden decisions.** Parnas's foundational comparison showed that decomposition effectiveness depends on the criterion used; organizing modules around design decisions likely to change can improve flexibility and comprehensibility [2]. Information hiding is not hiding all information. A module exposes stable facts collaborators need while concealing representation, algorithm, supplier, persistence, caching, and policy choices they should not depend upon.

Begin with change scenarios. If tax rules change, which module should change? If the database is replaced, which code should remain unaffected? If a third notification channel is added, where does variation belong? A responsibility is cohesive when its information and rules change for related reasons under accountable ownership, not merely because its classes share a suffix.

Avoid turning “business,” “service,” “utility,” or “common” into unbounded buckets. A shared utility with high fan-in becomes a broad change and release surface. Give it a precise stable capability or keep behavior with the responsibility that owns it.

**Distinguish relations.** Containment says element A includes B. Uses says A requires B's provided behavior. Visibility says A can name or access B. Build dependency says A must be available or built before B can be compiled, packaged, tested, or generated according to defined semantics. Generation says one artifact produces another. Test dependency may be intentionally broader than production access.

These relations do not imply one another universally. A visible symbol may not be semantically used. A generated client may create a use dependency without a handwritten import. Two modules can communicate through shared storage while neither imports the other. Draw different edge kinds separately or create different projections.

**Orient edges explicitly.** In this chapter, $a\rightarrow b$ means “a depends on b.” Some tools draw arrows toward callers or providers. Put the convention in the legend. Never infer dependency direction from visual vertical position.

A uses relation should answer what provided behavior is required and under which assumptions. “Orders uses pricing” is stronger when linked to the price-quote contract and change scenario. The interface can be a type, function set, event schema, file schema, generated contract, or disciplined procedure. Public language visibility alone does not create a stable supported interface.

**Control visibility and access.** Minimize exported surface. Distinguish supported public interface, internal extension point, test surface, generated surface, and incidental public symbol required by a framework. Document compatibility and ownership expectations.

Language enforcement can support the view. Current Java SE 26 module configuration documentation describes a readability graph in which vertices are resolved modules and edges represent readability [6]. Java exports and readability are one concrete mechanism; they do not automatically express domain responsibility, semantic stability, or every runtime access path.

Reflection, dependency injection, serialization, plugin discovery, dynamic loading, macros, code generation, and configuration can bypass ordinary import analysis. Either constrain and inspect them or state the evidence gap. A boundary that exists only in a slide is not enforced.

**Use layers as dependency policy.** A layer groups modules at a related abstraction or responsibility level and constrains allowed use. In a strict layer, a module may use only the adjacent lower layer; in a relaxed layer it may skip downward. Upward calls can be mediated through inversion, callbacks, events, or interfaces owned by the higher-level policy.

Layers are not UI/business/data folders by definition, nor do they require all runtime calls to flow one way. The layer view concerns static allowed dependencies. Runtime control can enter infrastructure while compile-time policy dependencies still point toward stable domain interfaces. SARCH-031 develops layered architecture in depth.

**Analyze cycles by kind.** In a directed graph, modules $a$ and $b$ participate in a cycle if each is reachable from the other. Strongly connected components identify maximal cyclic regions. Inside such a region, independent replacement, build ordering, and change reasoning may be impaired because no topological order exists.

Not every reported cycle has the same consequence. A production uses cycle differs from a test-fixture cycle or mutually generated metadata. Determine the edge semantics and change scenario. To break a harmful cycle, move a shared concept to its rightful owner, split responsibilities, introduce an interface owned by policy, publish an event, or merge modules that are not genuinely independent. Do not create a meaningless interface solely to make a tool green.

**Examine fan-in, fan-out, and stability.** High fan-in can indicate a stable widely reused capability or a dangerous shared bottleneck. High fan-out can indicate orchestration or an incoherent module with too much knowledge. Count edges only after defining types and resolution; generated and transitive dependencies can distort numbers.

Stable dependencies should be depended upon more than they depend on volatile details. This is a design heuristic, not a theorem that highly depended-on code never changes. Examine change frequency, semantic volatility, ownership, compatibility, and propagation together.

**Map concepts to code.** Maintain identifiers from architectural modules to repositories, source roots, packages, namespaces, build targets, generated artifacts, tests, and owners. Allow many-to-many mappings when honest, but explain them. If one package implements pieces of several modules, static enforcement and change ownership become harder.

Monorepository versus multirepository layout is separate from modularity. A monorepository can enforce strong module boundaries; separate repositories can share schemas, databases, release pipelines, and coordinated changes. Measure the actual dependency and change graph.

**Make rules executable where practical.** Encode allowed dependencies in compiler/module visibility, build declarations, package rules, static architecture tests, ownership files, generated-code policy, and review. Compare $E_{observed}$ with $A$. Reject unauthorized edges or manage time-bounded exceptions with owner, rationale, risk, and expiry.

Automation sees only what its extractor models. Static imports may miss runtime loading and shared data; build graphs may overapproximate optional paths; dynamic traces miss dormant behavior. Successful conformance means the observed graph satisfies declared rules within the tool's scope, not that the architecture is correct or maintainable.

**Reconcile views.** A static module can produce several runtime components, and one process can host several modules. A deployment unit can package many modules. A database schema can couple modules despite an acyclic import graph. Team ownership can span or split modules. Record correspondence rather than forcing one diagram to answer every concern.

Check the context view: every owned capability needs implementation responsibility. Check component-and-connector and runtime views: each runtime behavior should map to code. Check data views for shared authority, deployment views for release coupling, and operational views for configuration and generated dependencies.

**Govern evolution.** Baseline the declared and observed graphs. Review new edges, exports, shared schemas, code-generation inputs, and exceptions. Reopen boundaries after repeated cross-module changes, cyclic coordination, ownership transfer, performance workarounds, security incidents, or framework migration.

A module view is useful when it helps predict and constrain change. Update it from code and decisions, but retain intended rules not observable in source. Delete stale edges and obsolete modules deliberately; do not preserve them because an old diagram once looked complete.

## Definitions and Notation

Let a module view be

$$
G_M=(M,E),\qquad E\subseteq M\times M\times K,
$$

where $K$ contains dependency kinds such as production-use, visibility, build, generation, or test. In this chapter $(a,b,k)$ means $a$ depends on $b$ by kind $k$.

Let $A\subseteq M\times M\times K$ be the allowed relation and $E_{observed}$ the relation extracted under a declared tool model. Structural conformance is

$$
Conf(E_{observed},A)\iff E_{observed}\subseteq A.
$$

This does not prove that $A$ is well designed or extraction complete.

For a dependency kind $k$, define direct fan-out and fan-in:

$$
fo_k(m)=|\{n:(m,n,k)\in E\}|,
\qquad
fi_k(m)=|\{n:(n,m,k)\in E\}|.
$$

Let $Reach_k(a,b)$ mean a path of $k$-edges exists from $a$ to $b$. Modules are mutually cyclic for $k$ when $Reach_k(a,b)\land Reach_k(b,a)$. A directed acyclic projection admits a topological order; that order does not establish responsibility quality.

For hidden decision $x$ owned by module $m$, let $C(x)$ be code units changed to implement one representative change. The ratio $|C(x)\setminus map(m)|/|C(x)|$ is an observed leakage indicator when $C(x)$ is nonempty. It depends on the sampled change and mapping and is not a universal modularity score.

## Mechanisms, Invariants, or Proof Structure

Use this module-view mechanism.

1. **Frame:** name stakeholders, concerns, scope, state, resolution, element kinds, and edge direction.
2. **Elicit change:** identify decisions likely to change and scenarios that should remain localized.
3. **Assign:** give each responsibility, rule, data authority, and interface an accountable module.
4. **Hide:** expose required stable semantics and conceal representation and volatile mechanisms.
5. **Relate:** distinguish containment, uses, visibility, build, generation, and test dependencies.
6. **Constrain:** declare allowed directions, exports, layers, cycles, and exceptions.
7. **Map:** connect conceptual modules to code, build, generated artifacts, tests, and ownership.
8. **Observe:** extract dependencies with explicit tool and dynamic-path limitations.
9. **Reconcile:** compare runtime, deployment, data, context, and organizational correspondence.
10. **Govern:** enforce new edges, expire exceptions, sample changes, and update on triggers.

The governing invariants are cohesive responsibility, hidden volatile decisions, explicit interfaces, typed directed dependencies, minimum necessary visibility, no unowned shared state, traceable conceptual-to-code mapping, scoped conformance evidence, cross-view consistency, and lifecycle maintenance.

If $E_{observed}\subseteq A$, every observed edge is allowed by the declared policy. This follows directly from set inclusion. It cannot establish that unobserved reflection, generated code, shared data, or runtime loading conforms, nor that allowed edges produce a good design.

## Alternatives and Trade-Offs

**Responsibility-first decomposition** localizes domain decisions but may not align with frameworks. **Technical-layer decomposition** standardizes mechanics but can scatter one behavior across layers. Use mappings and dependency inversion rather than letting a framework silently own the architecture.

**Fine-grained modules** can narrow change and visibility but add interfaces, build nodes, ownership, and navigation. **Coarse modules** reduce coordination surfaces but can mix volatile decisions. Choose granularity from change, ownership, enforcement, and evidence—not a file-count target.

**Strict layering** makes allowed direction simple and substitution easier. It can create forwarding code and performance pressure. **Relaxed layering** reduces indirection but increases knowledge and bypass risk. Declare skips explicitly.

**Compile-time enforcement** catches violations early and reproducibly but covers only modeled dependencies. **Review and dynamic observation** can find semantic, generated, and runtime coupling but are less complete or repeatable. Combine them.

**Acyclic dependencies** support ordering and independent reasoning. **Intentional cycles** may reflect inseparable concepts or tool constraints. Merge false boundaries or document the precise edge kind; do not normalize a harmful production cycle.

## Failure Modes and Misconceptions

- **“Folders are modules.”** Layout does not supply responsibility, interface, or enforcement.
- **“Public means supported.”** Framework and language visibility can exceed the promised interface.
- **“Imports are all dependencies.”** Shared data, generation, reflection, configuration, and runtime loading remain.
- **“No imports means decoupled.”** Two modules can couple through schemas, files, global state, or coordinated releases.
- **“Acyclic means modular.”** An acyclic graph can contain incoherent responsibilities and unstable surfaces.
- **“Every cycle is equally bad.”** Dependency kind, consequence, and change scenario matter.
- **“High fan-in is good reuse.”** It can also be a volatile common bottleneck.
- **“One repository is a monolith.”** Repository topology and architectural modularity are different relations.
- **“One service is one module.”** Static responsibility and runtime deployment need explicit correspondence.
- **“Layers describe call order.”** Module layers constrain static dependency, not every runtime control transfer.
- **“Dependency inversion removes dependency.”** It redirects source dependency while semantic reliance remains.
- **“Architecture tests prove evolvability.”** They show selected structural conformance in a recorded model.
- **“Generated code is outside architecture.”** Generated artifacts and inputs can create broad coupling and exposure.

## Worked Examples

### Example 1

**Question:** A tax-rate change modifies controllers, services, database code, and reports. What does the module view reveal?

**Reasoning:** The tax decision lacks one owner or stable interface. Define a tax-policy module exposing calculation inputs, effective-date semantics, jurisdiction, result, and explanation. Keep storage and transport adapters outside its rules. Map existing code and migrate callers; do not merely move files while retaining duplicated logic.

**Conclusion:** A change scenario tests whether decomposition hides the intended decision.

### Example 2

**Question:** Graph edges are A→B, A→C, B→C, and C→D. What are A's fan-out and C's fan-in?

**Reasoning:** Under the declared “dependent points to provider” convention, $fo(A)=2$ because A directly depends on B and C. $fi(C)=2$ because A and B depend on C. These counts do not include transitive A→D or say whether any edge is harmful.

**Conclusion:** Graph metrics need explicit direction, edge kind, and interpretation.

### Example 3

**Question:** Modules orders, pricing, and discounts form orders→pricing→discounts→orders. What should be done?

**Reasoning:** First confirm all are production-use edges. Identify the hidden decisions: perhaps discount eligibility belongs with pricing, while order supplies a stable order-facts interface. Move concepts, invert one interface toward policy, or merge modules if they cannot vary independently. Adding a façade that preserves the cycle does not solve it.

**Conclusion:** Break a harmful cycle by correcting ownership, not decorating the graph.

### Example 4

**Question:** Domain code imports a SQL repository implementation even though an architecture picture shows dependency inversion. Is the view conformant?

**Reasoning:** No. If the allowed rule is adapter→domain and the observed graph contains domain→adapter, $E_{observed}\nsubseteq A$. Define the repository contract in the policy-owning boundary, inject an implementation, and test behavior. The domain still semantically requires persistence capability, but it no longer depends on SQL details.

**Conclusion:** Dependency inversion changes source knowledge while retaining an explicit required capability.

### Example 5

**Question:** A package has 50 public classes, but only three are supported. How should the view model it?

**Reasoning:** Record the three provided interface types and mark the rest incidental or internal. Reduce visibility where the toolchain permits, add compatibility tests for the supported surface, and prevent external imports of internals. Do not promise compatibility for symbols made public only for reflection or serialization.

**Conclusion:** Language visibility and architectural interface are related but distinct.

### Example 6

**Question:** A static import tool reports no dependency between billing and analytics, yet billing changes repeatedly break analytics. Why?

**Reasoning:** Both read a shared table and interpret status codes without an owned contract. Add the shared schema and semantic dependency to the model, assign data authority, version or publish the required information, and test compatibility. Import-only extraction was incomplete.

**Conclusion:** Hidden data coupling can dominate an apparently clean source graph.

### Example 7

**Question:** A generated API client changes 80 modules after one schema revision. What architectural issue appears?

**Reasoning:** Generation has propagated provider representation broadly. Place generated types behind a consumer-owned adapter or stable domain interface, limit generation targets, separate transport from domain models, and test version compatibility. Record generator and schema dependencies in the build view.

**Conclusion:** Generated code is a dependency mechanism that can defeat information hiding.

### Example 8

**Question:** A test imports internal classes forbidden to production modules. Is every such edge a violation?

**Reasoning:** Classify it as a test dependency. It may be allowed for white-box verification but increases refactoring cost and can encourage production bypass. Prefer testing provided behavior when possible; isolate privileged test fixtures and ensure they cannot enter production artifacts. The policy may differ by edge kind.

**Conclusion:** Typed dependency relations avoid false conclusions from one undifferentiated graph.

### Example 9

**Question:** A team wants to split one repository into six repositories to obtain modularity. What evidence is needed?

**Reasoning:** Measure responsibility boundaries, change coupling, builds, interfaces, versioning, shared data, release coordination, ownership, and incident response. Repository separation can add version and integration overhead while preserving semantic coupling. Enforce modules first or split only where independent lifecycle and ownership justify it.

**Conclusion:** Repository topology is not a substitute for modular design.

### Example 10

**Question:** How should code modules be governed in a medical-infusion controller?

**Reasoning:** Separate dose policy, sensor validity, actuator command, alarm, audit, configuration, communication, and display responsibilities under qualified safety analysis. Define permitted dependencies, units, timing assumptions, privilege, generated code, compiler configuration, and traceability. Independently verify hazardous paths and actual binaries. No external medical, clinical, controls, hardware, real-time, functional-safety, cybersecurity, regulatory, quality, or practitioner review is claimed; named qualified authorities must approve decomposition, evidence, release, and residual risk.

**Conclusion:** High-consequence module views require enforced boundaries and assurance beyond source-graph neatness.

## Cross-Program Connections

- [Software Engineering: Software Design & Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) owns code-level responsibility, domain boundaries, and detailed object or functional design.
- [Software Engineering: Patterns](../../11-software-engineering-patterns/ROADMAP.md) owns recurring structural and dependency patterns rather than the architecture-specific module map.
- [Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns architecture tests, static analysis validity, test seams, and conformance evidence.
- [Compilers & Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) owns language modules, name resolution, linking, and compilation mechanisms.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns privilege, trust, attack surface, information-flow, and enforcement review across modules.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns build and developer-platform capabilities used to enforce repository and dependency rules.

## References

1. ISO/IEC/IEEE. [ISO/IEC/IEEE 42010:2022, Software, systems and enterprise—Architecture description](https://www.iso.org/standard/74393.html), edition 2, November 2022. Architecture descriptions, viewpoints, views, model kinds, and correspondence; consulted 2026-09-06.
2. David L. Parnas. [On the Criteria To Be Used in Decomposing Systems into Modules](https://doi.org/10.1145/361598.361623), *Communications of the ACM* 15(12), 1053–1058, December 1972. Primary paper on decomposition criteria and information hiding; consulted 2026-09-06.
3. Paul Clements, Felix Bachmann, Len Bass, David Garlan, James Ivers, Reed Little, Paulo Merson, Robert Nord, and Judith Stafford. *Documenting Software Architectures: Views and Beyond*, 2nd edition. Addison-Wesley, 2010. Module structures, decomposition, uses, layers, interfaces, and documentation.
4. Len Bass, Paul Clements, and Rick Kazman. *Software Architecture in Practice*, 4th edition. Addison-Wesley, 2021. Modifiability tactics, module structures, quality scenarios, and architecture evaluation.
5. Robert C. Martin. *Clean Architecture*. Pearson, 2018. Dependency direction, component principles, boundaries, and changeability; used as practitioner guidance rather than universal law.
6. Oracle. [Java SE 26 `Configuration`](https://docs.oracle.com/en/java/javase/26/docs/api/java.base/java/lang/module/Configuration.html), Java Platform API. Current readability-graph and module-resolution behavior; consulted 2026-09-06.
7. John Lakos. *Large-Scale C++ Software Design*. Addison-Wesley, 1996. Physical design, dependency cycles, levels, and build consequences.

## Exercises

### Exercise 1

Define module, provided interface, uses dependency, visibility, containment, information hiding, and conformance for an order-processing codebase.

### Exercise 2

For production edges A→B, A→C, B→C, C→D, and D→B, compute direct fan-in and fan-out for B and C, identify the cyclic region, and state what the result cannot prove.

### Exercise 3

Diagnose a codebase organized into controller, service, utility, model, and repository folders where business changes touch every folder, internals are public, generated clients spread transport types, modules share tables, and architecture tests inspect only imports.

### Exercise 4

Design module and code views for a modular monolith that may later extract notifications. Address responsibilities, interfaces, dependency direction, data ownership, mapping, tests, build enforcement, migration, and triggers.

### Exercise 5

Design and assure the module structure for an unfamiliar wildfire-warning controller. Separate static architecture evidence from runtime, physical, safety, and operational assurance.

## Answers to the Exercises

### Answer 1

An order module owns order state transitions, invariants, and decision semantics. Its provided interface exposes supported placement, cancellation, and query behavior; a required pricing interface states what price evidence it needs. A uses dependency points from order to that provided pricing capability under this chapter's convention. Visibility determines which pricing and order names can be accessed, while containment records which code units belong to order.

Information hiding keeps persistence, caching, representation, and supplier decisions behind stable surfaces. Conformance means the observed typed dependency graph lies within declared allowed relations for the stated extractor. It does not prove that the responsibilities are cohesive or that reflection, shared data, and runtime loading conform unless included in evidence.

### Answer 2

$fo(B)=1$ because B→C, and $fi(B)=2$ because A→B and D→B. $fo(C)=1$ because C→D, and $fi(C)=2$ because A→C and B→C. B, C, and D form a strongly connected region: B reaches C then D, D reaches B, and each can reach the others. A is outside because no path returns to A.

This graph result cannot prove the cycle is harmful, because dependency kinds and change consequences may differ. It also cannot establish responsibility quality, runtime calls, data coupling, visibility, or extraction completeness.

### Answer 3

The technical-folder decomposition scatters each business responsibility, so change scenarios cross every layer. Reframe modules around owned domain decisions and stable capabilities, then map framework adapters into those boundaries. Reduce exports, distinguish supported interfaces, and isolate generated transport types behind consumer-owned adapters.

Assign shared-table authority and expose governed queries, events, or interfaces instead of undocumented schema interpretation. Extend evidence beyond imports to build inputs, generation, configuration, reflection, schemas, tests, and selected runtime discovery. Use typed dependency policies, record exceptions, and compare actual change sets. Moving files alone does not repair semantic coupling.

### Answer 4

Define order, customer, inventory, payment coordination, and notification responsibilities with explicit provided and required interfaces. Policy modules must not import database, messaging, or web adapters; adapters implement interfaces owned by the relevant policy boundary. Notification owns templates, channel selection, delivery request identity, and outcomes, while upstream modules publish a stable notification intent rather than using channel SDK types.

Give notification its data authority and prohibit direct access to order tables. Map modules to packages, build targets, tests, generated clients, and owners. Enforce production edges, exports, schema compatibility, and privileged test exceptions. Measure change coupling, build scope, failure behavior, delivery volume, on-call ownership, and release coordination.

Preserve an extraction seam through versioned contracts and adapter boundaries, but keep notification in-process until independent scaling, release, failure isolation, or ownership evidence justifies distribution. Reopen after sustained independent demand, repeated coordination, incidents, or changed delivery guarantees. Repository separation alone is not the trigger.

### Answer 5

Define modules for hazard inputs, sensor validity, fire-behavior model boundary, warning policy, geographic targeting, message preparation, channel adapters, operator authorization, configuration, audit, and health evidence. State units, time validity, data authority, privilege, provided and required surfaces, allowed dependencies, generation inputs, and ownership. Keep policy independent of supplier and transport implementations, and prevent adapters from changing warning meaning.

Static assurance includes compiler and build configuration, source and generated dependency extraction, visibility checks, forbidden-edge tests, traceability, change-impact review, and exact binary provenance. It cannot prove sensor accuracy, model validity, timing, communications, human response, power continuity, physical safety, or operational readiness. Link runtime, deployment, data, security, hazard, human-factors, and operational views and test them with appropriate methods.

No external wildfire-science, meteorology, emergency-management, geospatial, accessibility, telecommunications, control-systems, safety, regulatory, security, human-factors, or practitioner review is claimed. Named qualified authorities and affected communities must approve assumptions, boundaries, warnings, tests, release, and residual risk. Unknown hazard thresholds, ambiguous authority, invalid units or time, inaccessible warnings, unverified generated code, forbidden critical dependencies, or absent degraded operation blocks readiness.
