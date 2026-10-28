---
module_id: SEPAT-018
program: Software Engineering: Patterns
level: 1
module_number: 18
title: Dependency Injection as a Creation Pattern
status: complete
last_verified: 2026-08-28
---

# Dependency Injection as a Creation Pattern

## One-Page Review

### Governing question

How can a system construct a complete, valid, least-authority object graph at an explicit boundary while keeping domain objects independent of concrete creation policy and container lookup?

### Essential definitions

- **Dependency Injection (DI)** supplies an object's required collaborators from outside rather than letting the object construct or locate them.
- A **composition root** is the narrow application boundary that selects implementations, validates configuration, constructs the graph, starts resources, and owns shutdown.
- **constructor injection** makes dependencies required for valid construction; **method/parameter injection** supplies an operation-specific collaborator.
- **property or field injection** mutates dependencies after construction and can expose partially valid objects.
- A **binding** maps a dependency key—type plus optional qualifier—to a provider or instance.
- A **provider/factory** defers or parameterizes creation while keeping lookup authority narrow.
- A **scope** defines instance reuse and lifetime: graph, application, request, transaction, tenant, operation, or no reuse.
- A **dependency graph** has objects/providers as vertices and directed consumer-to-dependency edges.
- A **captive dependency** occurs when a longer-lived object directly retains a shorter-lived one.
- **Service Locator** lets product code query a registry; it hides requirements and gives broad resolution authority, unlike injection.

### Central model, mechanism, or theorem

Model a constructed graph as \(G=(V,E)\), where \((u,v)\in E\) means consumer \(u\) requires dependency \(v\). A direct eager construction order exists exactly when the required subgraph is acyclic; a reverse topological order constructs dependencies before consumers. For each required dependency key, resolution must be total and unambiguous:

\[
\forall k\in K_{required},\quad |bindings(k)|=1.
\]

If lifetime rank increases with longevity, direct retention requires \(life(v)\ge life(u)\). A longer-lived consumer may access a shorter-lived object only through an explicit scope/provider boundary evaluated in the shorter-lived context. Graph validation does not prove provider behavior or domain correctness, but it can reject missing, ambiguous, cyclic, and scope-invalid wiring before serving traffic.

### Critical invariants

- Every required dependency is explicit, satisfied exactly once, and valid before the consumer escapes construction.
- Product/domain code does not query the container or ambient registry.
- Bindings and qualifiers encode domain meaning, not arbitrary strings scattered through consumers.
- Direct dependency edges respect lifetime; scoped providers make shorter-lived creation explicit.
- Cycles are redesigned or represented by an intentional runtime protocol, never hidden by partial objects.
- Construction side effects are bounded, failure-safe, observable, and cleaned up in reverse ownership order.
- Configuration and secrets are validated and transformed into narrow typed values/capabilities at the root.
- Tests substitute behavior at owned boundaries and also verify the production graph.

### Common failures

Common failures include injecting a container, using field injection for required invariants, constructor signatures that expose unrelated framework detail, ambiguous same-type values without semantic qualifiers, request objects captured by singletons, circular proxies that expose partial initialization, providers that perform unbounded network I/O, hidden construction in domain methods, mocks that accept impossible behavior, graph startup that leaks earlier resources after a later failure, and dynamic configuration that mutates a live graph inconsistently.

### Compact example

An explicit root creates one tax policy, receipt store, and audit sink, then injects them into two checkout handlers. The handlers share root-owned state within one application graph. A separate test graph injects a zero-tax policy and isolated state without changing product code or querying a container. The graph owns instance choice; the checkout owns business behavior.

### Connections

[SEPAT-011](011-simple-factory-and-creation-functions.md) locates construction policy, [SEPAT-016](016-singleton-and-its-hidden-global-state.md) separates instance scope from global access, and [SEPAT-017](017-object-pool.md) makes pooled-resource ownership explicit. [SEPAT-019](../ROADMAP.md) studies deferred providers. DI also connects to [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md) and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

Which boundary knows enough to choose concrete implementations and lifetimes, and how can it build the application so every consumer declares only the capabilities it genuinely needs?

Dependency Injection is a creation pattern before it is a framework feature. Plain constructor calls at `main`, a generated compile-time graph, and a runtime container can all implement it. The architectural outcome—not annotations—is decisive: creation policy is concentrated, dependencies are visible, and consumers do not pull collaborators from ambient state.

## Why This Matters

When a class creates its database, clock, HTTP client, and logger internally, it combines domain behavior with environment selection and lifecycle. Tests must either touch the environment or intercept construction. Reuse in another application becomes difficult, and failures can occur deep inside operations.

DI moves choices to a boundary with configuration and ownership context. This improves substitution and reasoning, but a poorly governed container can become an opaque second programming language. Production rigor requires validating the graph, lifetimes, startup, shutdown, authority, and generated/reflection behavior—not merely showing that unit tests can pass with mocks.

## Prerequisites and Retrieval

You should understand interfaces, constructors, factories, object graphs, directed acyclic graphs, ownership, concurrency, configuration, and test doubles. Retrieve these facts:

1. A constructor dependency states what must exist for the object to be valid.
2. Interface abstraction is useful at volatility or authority boundaries, not automatically for every class.
3. A long-lived object retaining request state creates lifetime and concurrency defects.
4. Creation order and startup order can differ; asynchronous resources may need explicit readiness.
5. Tests of components do not validate the real production binding graph.
6. Resolution authority is a capability: a general container can expose secrets and powerful services.

## Learning Objectives

After completing this module, you should be able to:

- model DI as explicit graph construction and ownership;
- choose constructor, parameter, provider, or property injection deliberately;
- specify binding keys, qualifiers, scopes, and lifecycle constraints;
- detect missing/ambiguous bindings, cycles, captive dependencies, and graph drift;
- distinguish injection from Service Locator and container-coupled domain code;
- design startup rollback, readiness, graph replacement, and reverse-order shutdown;
- use test doubles without substituting impossible contracts;
- evaluate compile-time, reflection-based, generated, and manual wiring trade-offs.

## Core Exposition

### Begin with plain construction

Write the composition root manually until repetition or variation justifies tooling. Explicit code reveals constructor order, shared identities, configuration transformations, and shutdown owners. A container should automate a graph you can explain, not invent an architecture.

Keep the root near the executable boundary. Domain packages should not import container APIs, annotations that dictate environment policy, or application configuration structures unless those annotations are an accepted portable contract.

### Constructor injection

Constructor injection is the default for required, stable collaborators. It prevents use before wiring, supports immutable fields, and makes dependencies visible to readers and tests.

A very large constructor is diagnostic evidence, not a reason to hide dependencies through field injection. It may indicate mixed responsibilities, an application service coordinating too much, or low-cohesion parameter groups. Refactor by domain ownership, not by placing every dependency inside one vague context object.

### Parameter and method injection

Pass dependencies as method parameters when they belong to one operation, vary per call, or are already carried by the caller. Request context, cancellation, transaction, and authenticated principal often belong at this boundary.

Avoid passing a general request/service context from which the method can fetch anything. A narrow value or capability keeps authority auditable.

### Property and field injection

Property injection can represent a genuinely optional, replaceable collaborator when absence has defined semantics. It is hazardous for required dependencies because the object exists in an invalid intermediate state and can be observed before injection.

Framework field injection also hides requirements from ordinary construction and complicates immutability. If legacy constraints require it, validate completion before exposure and plan contraction toward constructor/factory wiring.

### Bindings and qualifiers

A type alone may not identify a dependency. Two strings could be a region and an API base URL; two clocks could be monotonic and civil. Use typed wrappers or semantic qualifiers owned by the domain boundary.

Require explicit bindings in critical graphs when implicit construction could silently select an unintended concrete type. Detect duplicate keys and configuration shadowing. Emit graph diagnostics without printing secrets.

### Scopes and lifetime

Scope is ownership policy. Application-scoped objects must be thread-safe when used concurrently. Request-scoped objects must not be retained by application singletons. Transaction-scoped values must not escape commit/rollback.

When a long-lived service needs per-request behavior, inject a provider whose call requires the active request scope, or pass the request-specific capability into the operation. The provider is not permission for arbitrary resolution.

### Cycles

Constructor cycles have no complete eager construction order. Proxies, mutable setters, or lazy providers can make them run, but may expose methods before initialization and conceal a design cycle.

First seek a domain correction: extract shared policy, introduce an event or mediator, reverse an incorrect dependency, split orchestration from state, or pass data rather than a service. Retain a runtime cycle only when its protocol and initialization states are intentional and tested.

### Composition root and capability security

The root reads raw configuration and secrets, validates them, constructs typed policies and narrow clients, then discards broad parsing/lookup authority where possible. A report generator may need `ReadInvoices`, not a database handle; a notifier may need `SendNotification`, not a container capable of resolving signing keys.

Do not inject secret stores, filesystem roots, or generic HTTP clients everywhere for convenience. Inject constrained capabilities whose authorization and endpoint policy are controlled at the boundary.

### Providers and assisted creation

Use a provider when instances are intentionally fresh, expensive and lazy, scoped to a context, or require runtime values not known at graph construction. An assisted factory combines injected stable dependencies with caller-supplied domain values.

Providers can hide failure, blocking I/O, and lifecycle. Their interface should expose failure/cancellation semantics and ownership. Do not call providers from constructors when that merely recreates eager construction invisibly.

### Startup and failure atomicity

Separate allocation, configuration validation, dependency wiring, resource startup, readiness, and traffic admission. If starting component \(n\) fails, stop already-started components in reverse order and report the causal chain.

Avoid network calls in arbitrary provider evaluation. Make external acquisition explicit and bounded. A graph can be structurally valid while the database is unavailable; diagnostics must distinguish configuration, wiring, and runtime readiness failures.

### Shutdown

The root owns every closeable resource it creates. Stop consumers before their dependencies, drain traffic before closing shared transports, and make repeated shutdown safe. Container disposal order must be verified rather than assumed.

Factories that create owned child resources must return a lease/handle or register ownership with a clear scope. Garbage collection is not deterministic resource lifecycle.

### Testing strategy

Unit tests construct consumers with small fakes that enforce real invariants, failure modes, and concurrency constraints. Prefer behavioral fakes over interaction-heavy mocks when state matters. Reject test-only constructors that permit invalid production states.

Add graph tests that instantiate production bindings, validate qualifiers and scopes, run startup/readiness against controlled dependencies, and close the graph. Architecture checks can forbid container access outside roots and modules.

### Graph evolution

Treat binding configuration as versioned code. Review graph diffs: implementation changes, new transitive dependencies, scope changes, eager/lazy transitions, and authority expansion.

For live reconfiguration, build and validate a new graph generation, switch traffic atomically at an owned boundary, drain the old generation, then close it. Mutating scattered singleton fields creates mixed-generation behavior.

## Definitions and Notation

Let \(K\) be dependency keys, \(P\) providers, and binding map \(B:K\to P\). A qualified key includes semantic type and qualifier. Let \(G=(V,E)\) be the realized graph, with edge \((u,v)\) from consumer to dependency.

Let \(scope(v)\) identify instance-reuse context and \(life(v)\) rank lifetime duration. Direct retention requires

\[
(u,v)\in E \Longrightarrow life(v)\ge life(u),
\]

unless \(v\) is reached through a provider evaluated inside the correct shorter scope. Let \(start(v)\) and \(stop(v)\) denote lifecycle events. For a direct dependency:

\[
start(v) < start(u),\qquad stop(u) < stop(v).
\]

These order constraints apply to owned startable resources, not pure immutable values.

## Mechanisms, Invariants, or Proof Structure

### Graph validation

For requested roots, enumerate transitive keys and providers. Reject missing or multiply bound required keys; incompatible qualifiers; prohibited implicit bindings; cycles in eager edges; direct long-to-short lifetime capture; and inaccessible or unauthorized capabilities. Report the shortest causal path from root to defect.

### Construction argument

If the eager dependency graph is a finite DAG and every required key has one provider, reverse topological order gives a dependency-before-consumer construction order. If each provider returns a value satisfying its contract or fails without publishing partial state, the root either obtains a complete graph or a classified failure. This does not prove behavioral substitutability or side-effect rollback; those remain provider and integration obligations.

### Lifecycle rollback

Record each successfully started owned component. On failure, traverse that record in reverse and attempt bounded cleanup while preserving the primary error and reporting cleanup failures. Readiness becomes true only after all required starts and checks pass.

### Executable explicit graph

<!-- bijux-verify: {"id":"explicit-dependency-graph","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"charge=12000\nshared-audit=True\nisolated-graphs=True\ntest-charge=10000\n","stderr":""}} -->
```python
class TaxPolicy:
    def __init__(self, basis_points):
        self.basis_points = basis_points

    def apply(self, subtotal):
        return subtotal + subtotal * self.basis_points // 10000


class ReceiptStore:
    def __init__(self):
        self.receipts = []

    def save(self, total):
        self.receipts.append(total)


class AuditSink:
    def __init__(self):
        self.events = []


class Checkout:
    def __init__(self, tax_policy, receipt_store, audit_sink):
        self.tax_policy = tax_policy
        self.receipt_store = receipt_store
        self.audit_sink = audit_sink

    def charge(self, subtotal):
        total = self.tax_policy.apply(subtotal)
        self.receipt_store.save(total)
        self.audit_sink.events.append(f"charged:{total}")
        return total


def build_application(tax_basis_points):
    policy = TaxPolicy(tax_basis_points)
    store = ReceiptStore()
    audit = AuditSink()
    return {
        "primary": Checkout(policy, store, audit),
        "retry": Checkout(policy, store, audit),
        "store": store,
        "audit": audit,
    }


production = build_application(2000)
testing = build_application(0)
charge = production["primary"].charge(10000)

print(f"charge={charge}")
print(f"shared-audit={production['primary'].audit_sink is production['retry'].audit_sink}")
print(f"isolated-graphs={production['audit'] is not testing['audit']}")
print(f"test-charge={testing['primary'].charge(10000)}")
```

The run proves the stated integer calculation and identity relationships for two finite, sequential graphs. It does not prove concurrent safety, tax correctness for any jurisdiction, durable receipt storage, provider rollback, or container behavior.

## Alternatives and Trade-Offs

**Internal construction** is acceptable for value-only implementation details that are cheap, deterministic, and not environment choices. Injecting every tiny value object adds noise.

**Manual composition** maximizes language-level transparency and is often enough for small or stable applications. Large repetitive graphs may motivate generated or runtime tooling.

**Compile-time/generated DI** can detect missing bindings and cycles early and avoid reflection. It adds generated code, build tooling, and framework-specific diagnostics.

**Runtime/reflection containers** support dynamic module assembly and rich scopes but move errors to startup/runtime and can obscure control flow. Require explicit validation and observability.

**Service Locator** reduces constructor plumbing but hides dependencies and expands resolver authority. Restrict locator use to integration boundaries when legacy frameworks demand it.

**Modules/plugins** can provide controlled extension points. Validate signatures, compatibility, authority, isolation, failure, unloading, and ownership; dynamic choice is not automatically safe substitution.

Use DI where it makes creation policy, volatility, lifetime, or authority clearer. Keep domain behavior ordinary and container-independent.

## Failure Modes and Misconceptions

- **“DI means using a container.”** Manual constructor composition is DI.
- **“Every class needs an interface.”** Abstract at meaningful substitution, authority, or ownership boundaries.
- **“Field injection is concise.”** It conceals required state and permits invalid construction.
- **“The container solves lifecycle.”** Only verified scope, startup, rollback, and disposal policies do.
- **“A provider fixes a cycle.”** It may delay the same design defect and expose runtime recursion.
- **“Singleton scope is globally one.”** It is usually one per graph/container/runtime scope and implies thread-safety obligations.
- **“Mocks prove wiring.”** Component substitutions do not validate production bindings or provider effects.
- **“Inject configuration everywhere.”** Broad config objects hide requirements and allow unrelated reads.
- **“The root may be anywhere.”** Scattered roots recreate inconsistent policy and duplicate resources.
- **“Dynamic rebinding updates the system atomically.”** Existing objects may retain old dependencies; use graph generations.

## Worked Examples

### Example 1

A command-line tool manually constructs a parser, policy, repository, and command handler in `main`. No container is introduced because the graph has eight stable nodes. **Conclusion:** DI is an architectural relation, not a framework quota.

### Example 2

An HTTP handler receives a request-scoped authenticated principal as a method parameter while its application-scoped authorization policy is constructor-injected. **Conclusion:** Lifetime and variability determine injection form.

### Example 3

Two strings represent a public API URL and an audit endpoint. Typed `PublicApiEndpoint` and `AuditEndpoint` values replace string-name qualifiers. **Conclusion:** Semantic types prevent ambiguous but type-correct wiring.

### Example 4

A singleton report scheduler captures a request-scoped locale through constructor injection. Graph validation rejects it; the operation instead receives locale with each job. **Conclusion:** Visible injection can still be lifetime-invalid.

### Example 5

Billing and ledger services depend on each other. Analysis extracts settlement policy and lets an orchestrator call both, producing an acyclic graph. **Conclusion:** Redesign cycles before reaching for proxies.

### Example 6

A generated DI tool reports a missing `FraudPolicy` binding at compile time. The team also runs a startup graph test because provider constructors can still reject deployment configuration. **Conclusion:** Structural and runtime validation are complementary.

### Example 7

A test mock returns negative inventory, a state the real repository forbids. It makes compensation logic appear correct. A contract-enforcing fake and shared provider tests replace it. **Conclusion:** Easy substitution can create impossible evidence.

### Example 8

Graph startup opens a pool, starts a consumer, then fails to bind a port. The root stops the consumer and closes the pool in reverse order while retaining the bind error as primary. **Conclusion:** Construction failure needs ownership rollback.

### Example 9

Credential rotation builds graph generation 44 with new clients, verifies readiness, switches requests, drains generation 43, and closes it. **Conclusion:** Whole-graph replacement prevents mixed configuration.

### Example 10

An avionics component receives a generic service resolver capable of producing command channels and signing keys. The design is rejected in favor of a narrow read-only sensor capability, with timing and safety evidence reviewed by named specialists. **Conclusion:** Injection shape is part of authority design.

## Cross-Program Connections

- **Object-Oriented Programming:** constructors, interfaces, immutability, and behavioral subtyping shape injectable contracts.
- **Functional Programming:** explicit parameters and pure construction reduce hidden effects; effect capabilities can remain narrow.
- **Software Design:** dependency direction, cohesion, information hiding, and modular boundaries determine graph quality.
- **Concurrent Programming:** singleton scopes, publication, request contexts, and shutdown require memory/lifecycle safety.
- **Security Engineering:** binding choice distributes capabilities, secrets, filesystem, network, and signing authority.
- **Platform Engineering:** configuration, readiness, deployment overlap, graph generations, and drain meet at the root.
- **Testing and Quality:** fakes, contract tests, graph tests, and architecture rules provide distinct evidence.
- **Programming Languages:** reflection, annotations, code generation, type systems, and modules change failure timing.
- **Distributed Systems:** injected clients still need retries, deadlines, idempotency, and failure semantics.
- **Systems Engineering:** high-stakes capabilities require traceability and named multidisciplinary review.

## References

1. Martin Fowler, [“Inversion of Control Containers and the Dependency Injection Pattern”](https://martinfowler.com/articles/injection.html), 2004, accessed 2026-08-28. Defines constructor, setter, and interface injection and compares DI with Service Locator.
2. Mark Seemann and Steven van Deursen, *Dependency Injection Principles, Practices, and Patterns*, Manning, 2019, ISBN 978-1-61729-473-0. Develops composition roots, constructor injection, scopes, lifetime, and container-independent application design.
3. Google, [“Dagger Developer Guide”](https://dagger.dev/dev-guide/), accessed 2026-08-28. Documents generated binding graphs, `@Inject`, modules, components, qualifiers, scopes, and lazy/provider bindings.
4. Google, [“Getting Started with Guice”](https://github.com/google/guice/wiki/GettingStarted), accessed 2026-08-28. Defines external provision, constructor injection, modules, bindings, injectors, and transitive object graphs.
5. Google, [“Guice Scopes”](https://github.com/google/guice/wiki/Scopes), accessed 2026-08-28. Documents application/request reuse, eager creation, thread-safety obligations, and the longer-lived-to-shorter-lived scope hazard.
6. VMware, [“Dependency Injection”](https://docs.spring.io/spring-framework/reference/core/beans/dependencies/factory-collaborators.html), Spring Framework reference, accessed 2026-08-28. Documents constructor and setter injection, dependency resolution, validation timing, and circular-dependency consequences.
7. Robert C. Martin, *Clean Architecture*, Pearson, 2017, ISBN 978-0-13-449416-6. Provides dependency-rule and boundary context for directing source dependencies toward stable policy.

## Exercises

### Exercise 1

Formalize the executable graph: list vertices, edges, scopes, construction order, and identity properties. Add a third handler that needs audit but not receipt storage without giving it excess authority.

### Exercise 2

Given application-scoped `ReportScheduler`, request-scoped `Principal`, transaction-scoped `UnitOfWork`, and immutable `ReportPolicy`, diagnose valid and captive edges and redesign the invalid ones.

### Exercise 3

Design production graph validation for a service using qualified bindings, generated DI, database and message resources, optional plugins, and configuration generations. Separate static, startup, readiness, and behavioral evidence.

### Exercise 4

Migrate a legacy codebase whose domain classes call `Services.resolve(type)` to constructor/parameter injection incrementally without one massive rewrite or parallel global registries.

### Exercise 5

An unfamiliar infusion-pump controller proposes runtime plugin bindings for dose policy and actuator access. Produce a graduate-level safety and authority review, including evidence and named human roles required before deployment.

## Answers to the Exercises

### Answer 1

Vertices are `TaxPolicy`, `ReceiptStore`, `AuditSink`, `primary Checkout`, and `retry Checkout`. Each checkout has edges to all three dependencies. All values are application-graph scoped in this finite example. Construct the three dependencies in any order, then both checkouts. The two checkouts are distinct; their policy, store, and audit references are identical within a graph; corresponding objects in separate `build_application` calls are nonidentical.

Define `AuditReporter(audit_sink)` with exactly one edge to `AuditSink`. The root constructs it from the already-owned audit instance and returns it as another entry. Do not inject Checkout, ReceiptStore, the graph dictionary, or a generic resolver merely to reach audit. Tests assert shared audit identity and absence of storage operations in the reporter interface.

### Answer 2

`ReportScheduler -> ReportPolicy` is valid because immutable policy is at least as long-lived. Direct `ReportScheduler -> Principal` and `ReportScheduler -> UnitOfWork` are captive dependencies: one request/transaction value would be retained and potentially shared across callers.

Pass Principal into each scheduling operation after authentication, or inject a narrow `CurrentPrincipalProvider` that requires an active request scope and never caches its result. Create UnitOfWork per job/transaction through an owned factory or pass it to the operation; commit/rollback and close within that boundary. A request operation may directly use its Principal and a transaction operation may use its UnitOfWork. Verify no shorter-scoped reference is stored in scheduler fields, callbacks, tasks, or caches after scope completion.

### Answer 3

Static/generated validation checks exactly one binding per required qualified key, no prohibited implicit binding, eager DAG acyclicity, accessible constructors/providers, scope compatibility, plugin interface/version metadata, and forbidden container imports outside roots. Emit a secret-redacted graph and diff it in review.

Startup validation parses raw configuration into typed values, verifies required plugin signatures/allowlists, constructs generation \(g\), opens resources with deadlines, starts them in dependency order, and rolls back in reverse on failure. Readiness performs bounded dependency-specific checks without claiming future availability. Behavioral evidence includes contract tests for implementations, controlled database/broker integration, failure injection, concurrency tests, authorization tests, and shutdown/drain tests. Deployment builds the new generation alongside the old only within capacity, switches traffic atomically, observes it, drains, and closes. Static graph success is not behavioral or operational proof.

### Answer 4

Inventory locator calls by domain and capability. Freeze new calls with an architecture check. Establish one composition root that initially wraps the existing registry behind narrow adapters. For one vertical slice, add required constructor/operation parameters to leaf consumers, choose implementations in the root, and update callers outward. Commit each coherent slice with characterization and contract tests.

Where framework callbacks construct objects, use an adapter factory at that boundary; do not expose the container to domain code. Replace broad `Services` access with narrow capabilities, then remove resolved keys as call-site count reaches zero. Track lifetime and shutdown ownership during migration, because merely passing the old singleton values preserves hidden shared state. Delete each compatibility adapter immediately after its last consumer; never introduce a second general registry. Production graph tests prevent missing bindings throughout.

### Answer 5

Runtime substitution does not establish that a dose-policy plugin is behaviorally compatible or that actuator authority is constrained. Reject generic resolver access. Define narrow, versioned capability interfaces: validated patient/order inputs to dose computation; bounded, unit-safe outputs; and a separately guarded actuator command interface. The plugin must not receive signing keys, raw device buses, arbitrary network/filesystem access, or container resolution unless a hazard analysis explicitly requires and constrains them.

Enforce signed allowlisted artifacts, provenance, reproducible builds, API/schema compatibility, configuration generation, least privilege, deterministic/resource bounds, and fail-closed loading. A graph generation becomes eligible only after dose constraints, units, calibration, device identity, command epoch, and readiness validate. Switch at a medically safe boundary; fence and drain the old generation; never mix a new policy with stale calibration or actuator state. Independent hardware safety limits must reject unsafe commands even if injected software fails.

Evidence includes requirements traceability, dimensional/unit analysis, formal or exhaustive state/property analysis where tractable, dose-bound and boundary testing, static analysis, independent code review, software-bill/provenance verification, timing and resource analysis, simulation, hardware-in-the-loop, fault injection, cybersecurity assessment, usability/human-factors validation, clinical risk evaluation, and controlled release under applicable medical-device quality/regulatory processes. Named clinical, pharmacy, biomedical, controls, functional-safety, real-time, cybersecurity, human-factors, quality, regulatory, operations, and independent verification authorities must approve. Repository graph validation or an executable toy graph proves no clinical safety or production suitability.
