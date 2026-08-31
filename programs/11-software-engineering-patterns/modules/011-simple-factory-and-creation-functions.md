---
module_id: SEPAT-011
program: Software Engineering: Patterns
level: 1
module_number: 11
title: Simple Factory and Creation Functions
status: complete
last_verified: 2026-08-28
---

# Simple Factory and Creation Functions

## One-Page Review

### Governing question

When should object or resource creation move from direct construction into a named function or simple factory, and what correctness obligations move with it?

### Essential definitions

- A **constructor** is a language mechanism that initializes a value or object of a declared concrete type.
- A **creation function** is an ordinary named function whose result is a newly constructed value, object, handle, or explicit creation error.
- A **simple factory** is a function or object that selects among concrete products and constructs one behind a common client-facing contract; the term is common but is not one of the twenty-three GoF pattern names.
- A **static factory method** is a class- or type-associated creation operation; it is not necessarily the GoF **Factory Method**, which delegates creation through an overridable creator operation.
- A **named constructor** communicates a creation variant such as `from_bytes`, `empty`, or `for_testing` when overloaded constructors would be ambiguous.
- A **composition root** is the owned boundary where an application's concrete components are selected, created, and connected.
- A **product invariant** is a property that every successfully returned product must satisfy.
- **Ownership transfer** defines who must release, close, cancel, or otherwise manage a created resource.
- A **registry factory** selects a registered provider by key; it adds registration lifecycle and trust obligations beyond a closed simple factory.

### Central model, mechanism, or theorem

Model a creation boundary as a partial, explicit result function

$$
F:K\times C\rightarrow Result(P,E),
$$

where (K) is a selection key, (C) validated creation configuration, (P) the client contract, and (E) a bounded error set. For every successful result (p):

$$
valid_C(p)\land owns(p,owner(F,C))\land usable(p).
$$

Selection must be total over the documented supported key set and reject unsupported or unsafe configurations explicitly. A factory centralizes creation variability; it should not become a hidden global dependency source or an unbounded container.

### Critical invariants

- A successful result is fully initialized and satisfies the product contract.
- Unsupported keys and invalid configuration fail explicitly and predictably.
- No partially acquired resource escapes on failure.
- Ownership, lifecycle, caching, and concurrency semantics are documented.
- Selection and construction are separated from ordinary product use.
- The factory depends on concrete products; clients depend only on the returned contract when substitution is intended.
- Configuration is validated at the boundary and secrets are not leaked through errors or logs.
- A factory is removed when it no longer owns meaningful creation policy.

### Common failures

Common failures include renaming every constructor `Factory`, confusing static factories with GoF Factory Method, accepting arbitrary reflective class names, hiding network or filesystem work behind an innocent-looking function, returning `null` for unsupported keys, leaking partial resources, caching without lifecycle or concurrency rules, turning a factory into a service locator, letting product code call back into the factory for dependencies, and retaining a switch wrapper after only one trivial product remains.

### Compact example

A report service supports `json` and `lines` formats selected at startup. A creation function validates the key once, returns a formatter implementing one operation, and rejects `xml` with a bounded error. Clients format records without importing concrete formatter classes. If only JSON remains permanently, direct construction at the composition root may be clearer than preserving the selector.

### Connections

[SEPAT-010](010-selecting-a-pattern-from-forces-rather-than-names.md) determines whether centralized selection is justified. [SEPAT-012](../ROADMAP.md) adds subclass-controlled creation through Factory Method; [SEPAT-013](../ROADMAP.md) coordinates product families with Abstract Factory. Creation and ownership connect to [Object-Oriented Programming](../../02-programming-languages-object-oriented-programming/ROADMAP.md), [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md), and application wiring to [Software Engineering: Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md).

## Governing Question

What is the smallest explicit creation boundary that localizes a real construction decision while preserving validity, ownership, failure visibility, and simple client code?

Direct construction is the baseline. It makes the concrete type, arguments, cost, and ownership visible. Move creation when a name clarifies an invariant, constructor syntax is insufficient, selection varies, acquisition must be coordinated, or clients should not know concrete products.

A creation function is often enough. It does not require an inheritance hierarchy or a class named `Factory`. The design goal is to own construction policy at one boundary, not to reproduce a canonical diagram.

## Why This Matters

Construction is where configuration becomes runtime authority. A key chooses an algorithm; a URL selects a provider; credentials enter a client; a pool determines resource sharing; a schema version selects a parser. Scattered creation duplicates policy and makes unsafe combinations possible.

Centralization can enforce valid-by-construction products, normalize errors, isolate concrete dependencies, and make application wiring reviewable. It can also hide expensive effects and grow into a universal locator. Clear semantics matter more than the word “factory.”

Resource-producing factories carry additional risk. Allocation, file opening, sockets, threads, database sessions, and cryptographic providers have cleanup, cancellation, and security obligations. A successful type alone does not establish correct lifecycle.

## Prerequisites and Retrieval

You should understand functions, constructors, interfaces or protocols, exceptions or result types, ownership, and dependency inversion. Retrieve these facts:

1. A constructor names a concrete type and may be constrained by language overload rules.
2. A function can validate, choose a subtype, return an interface, cache, or fail explicitly.
3. Returning an abstraction moves concrete dependency inward but does not remove it.
4. Resource acquisition requires a paired release strategy on every path.
5. Configuration and service use are separate responsibilities.
6. Dynamic registration increases extension power and trust, lifecycle, and diagnosability costs.

## Learning Objectives

After completing this module, you should be able to:

- distinguish constructors, named constructors, creation functions, simple factories, and GoF Factory Method;
- identify forces that justify a creation boundary;
- specify key, configuration, product, error, and ownership contracts;
- implement a closed simple factory with exhaustive selection and explicit failure;
- decide between functions, factory objects, registries, containers, and direct construction;
- handle resources, asynchronous acquisition, caching, and cancellation safely;
- test product invariants and every selection/error partition;
- refactor toward or away from a factory without breaking clients.

## Core Exposition

### Direct construction is the baseline

Use a constructor directly when one concrete type is intended, arguments are clear, construction is cheap and local, and clients legitimately own the dependency. `Point(x, y)` needs no factory merely because it creates a value.

Direct construction is informative. Moving it behind `make_point` adds a symbol and navigation. The function must contribute a durable responsibility: naming, validation, selection, ownership, caching, compatibility, or dependency isolation.

### Named creation communicates intent

Constructors often share one type name. Named operations such as `Duration.from_seconds`, `UserId.parse`, and `Document.empty` state distinct preconditions and semantics. They can return errors or canonical instances and can evolve independently from raw representation.

Do not use names to hide equivalent trivial forwarding. `create_user(name)` that only calls `User(name)` adds little unless it owns validation, defaults, privacy rules, or compatibility.

### Simple factory centralizes closed selection

A closed factory knows a finite product set. It maps a trusted key or configuration to a product. Centralized selection prevents each client from importing all concrete types and duplicating a switch.

The coupling has moved into the factory. Adding a product changes the factory, tests, documentation, and perhaps configuration schema. This is acceptable when the factory owns that closed policy. If independently deployed providers must extend selection, a registry or plugin boundary may fit—but its obligations are substantially larger.

### Simple factory is terminology, not GoF Factory Method

The GoF Factory Method pattern defines an interface for creation while allowing subclasses to decide the concrete class. A plain function containing a switch is not that collaboration. A static method named `of` or `from` is likewise a language-level creation idiom unless overridable creator structure is present.

Precise naming prevents misleading diagrams and prepares comparison in the next module. Teams may use “factory method” informally; design records should state the actual binding mechanism.

### Define the creation contract

Specify accepted keys, configuration schema, validation order, defaults, result contract, error taxonomy, side effects, latency, ownership, thread safety, caching, and observability. If creation performs I/O, make that visible through naming, asynchronous type, documentation, or boundary placement.

A safe error names the invalid field or unsupported key without printing secrets. Distinguish configuration errors, unavailable dependencies, authentication failure, capacity exhaustion, timeout, cancellation, and internal defects when clients respond differently.

### Valid by construction

Every successful product satisfies invariants. Validate before acquiring expensive resources when possible. If acquisition has several stages, either clean up completed stages on failure or use scoped resource handles that do so automatically.

Do not return a half-configured product that requires callers to remember `initialize()`. Two-phase lifecycle may be necessary for cyclic systems or frameworks, but then intermediate state and authority must be explicit and inaccessible to ordinary use.

### Ownership and lifecycle

Returning a resource also transfers or retains obligations. State whether the caller owns a fresh resource, borrows a pooled resource, shares a cached immutable product, or receives a process-scoped service. The same return type can conceal very different release rules.

Prefer language mechanisms that encode ownership: values, scoped handles, context managers, unique owners, or explicit leases. On failure and cancellation, release every acquired subordinate resource exactly once.

### Factory function or factory object

A function fits stateless or explicitly parameterized creation. A factory object fits cohesive shared configuration, injected dependencies, test clocks, quotas, product-family state, or creation metrics. Its own construction must remain explicit.

Avoid giving the factory every application service. A factory with a database, HTTP client, cache, logger, feature service, and container may be an application composition root disguised as a local collaborator.

### Configuration and use

At the composition root, parse and validate external configuration, choose concrete products, and inject them into consumers. Product code should not repeatedly read environment variables or query a global factory. This keeps ordinary behavior deterministic and dependencies visible.

A factory passed as a dependency is appropriate when creation must occur during product behavior, such as per-request sessions or per-document exporters. Pass the narrow creation capability, not a universal container.

### Registries and plugins

A registry maps keys to providers added outside the closed factory. Define duplicate-key policy, registration timing, unloading, version compatibility, trust, isolation, enumeration, deterministic order, and concurrency. Arbitrary import or reflection from untrusted configuration is code execution, not mere object selection.

Prefer a closed allowlist when extension is not a real requirement. If plugins are required, authenticate artifacts, validate metadata, constrain capabilities, and expose diagnostics.

### Async and fallible creation

Remote clients, pools, and resource handles may require asynchronous acquisition. Make cancellation and deadline propagation part of the contract. If the caller cancels after a socket opens but before authentication completes, the creation operation still owns cleanup.

Separate object allocation from readiness when useful. A lightweight client can be constructed synchronously while `connect()` is explicit; alternatively an async factory can return only ready clients. Choose one lifecycle and make unusable states unrepresentable where practical.

### Caching and pooling are separate policies

A factory may return a new value, memoized immutable instance, shared service, or lease from a pool. These choices change identity, mutability, concurrency, shutdown, and tests. Do not introduce caching silently as an optimization.

Cache keys must include every configuration dimension affecting semantics. Pools require capacity, fairness, health checks, timeout, leak detection, and release. The name `create` should not imply freshness if identity is shared.

## Definitions and Notation

Let supported keys be (K_S\subseteq K), validated configurations (C_V\subseteq C), product contract (P), and bounded creation errors (E). Define

$$
F:K\times C\to Result(P,E).
$$

Selection completeness and rejection require

$$
\forall k\in K_S,\forall c\in C_V:\ F(k,c)\text{ returns }Ok(p)\text{ or a documented environmental }Err(e),
$$

$$
\forall k\notin K_S:\ F(k,c)=Err(UnsupportedKey(k)).
$$

For success, postcondition (I(p,c)) captures product invariants and configuration correspondence. For acquired resource set (R) and escaped owned resources (R_e), failure cleanup requires

$$
F(k,c)=Err(e)\implies R_e=\varnothing
\quad\text{and every }r\in R\text{ is released exactly once}.
$$

If a factory caches by key function (q(k,c)), semantic correctness requires

$$
q(k_1,c_1)=q(k_2,c_2)
\implies compatible(F(k_1,c_1),F(k_2,c_2)).
$$

This implication is a design obligation, not proof that a chosen key is complete.

## Mechanisms, Invariants, or Proof Structure

### Identify the construction decision

List concrete products, binding time, configuration, invariants, acquisition effects, ownership, and client knowledge. Keep direct construction if no meaningful policy is centralized.

### Specify selection and errors

Define an allowlisted key set and exhaustive mapping. Validate external configuration before selection and produce bounded safe errors.

### Return one stable product contract

Clients use the result without concrete type checks. If concrete-only capabilities are needed routinely, the common contract may be false.

### Verify a closed creation function

The executable example selects two formatters, returns fully usable products, and rejects an unsupported key explicitly.

<!-- bijux-verify: {"id":"closed-formatter-factory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"json: {\"id\":7,\"state\":\"ready\"}\nlines: id=7|state=ready\nunknown: unsupported format: xml\n","stderr":""}} -->
```python
class JsonFormatter:
    def format(self, record):
        return f'{{"id":{record["id"]},"state":"{record["state"]}"}}'


class LinesFormatter:
    def format(self, record):
        return "|".join(f"{key}={record[key]}" for key in sorted(record))


def make_formatter(kind):
    products = {
        "json": JsonFormatter,
        "lines": LinesFormatter,
    }
    try:
        product = products[kind]
    except KeyError:
        raise ValueError(f"unsupported format: {kind}") from None
    return product()


record = {"state": "ready", "id": 7}
for kind in ("json", "lines"):
    formatter = make_formatter(kind)
    print(f"{kind}: {formatter.format(record)}")

try:
    make_formatter("xml")
except ValueError as error:
    print(f"unknown: {error}")
```

The run proves exact behavior for two products and one rejected key. It does not prove thread safety, arbitrary value serialization, security, performance, or completeness if the supported-key declaration changes.

### Test every partition

Test each supported key, unknown and malformed keys, configuration boundaries, environmental failures, cleanup, ownership, caching identity, concurrency, cancellation, and contract behavior shared by all products.

### Review contraction

If only one trivial product remains and compatibility does not require selection, inline direct construction. Preserve the function only if its name, validation, ownership, or abstraction boundary remains valuable.

## Alternatives and Trade-Offs

**Direct constructor.** Maximizes visibility and minimizes concepts. It duplicates policy when selection or invariants recur.

**Named constructor or creation function.** Communicates intent and can return errors or abstractions. It adds an API and can hide effects.

**Closed simple factory.** Centralizes finite selection and concrete dependencies. Adding a product modifies the selector.

**Factory object.** Carries cohesive dependencies, state, quotas, or family configuration. Its lifecycle and construction add another responsibility.

**Registry or plugin factory.** Enables independent extension. It adds trust, discovery, collision, versioning, concurrency, and unloading problems.

**Dependency injection container.** Assembles large graphs using conventions. It can obscure control flow and make product code depend on container lookup if boundaries erode.

**Builder.** Stages many optional or ordered construction parameters. It does not inherently select among product implementations.

**Prototype.** Creates products by copying configured exemplars. Identity, deep-copy, resource, and mutation semantics become central.

## Failure Modes and Misconceptions

1. **Every creation helper is a design pattern.** Many are useful language idioms without a larger pattern collaboration.
2. **Static factory equals GoF Factory Method.** Static association does not provide subclass-overridden creation.
3. **Returning an interface removes coupling.** Concrete dependencies move into the creation boundary.
4. **Unknown keys can return null.** Ambiguous absence delays failure and loses diagnostic context.
5. **Factories may perform arbitrary hidden I/O.** Effect and latency contracts must remain visible.
6. **A factory should resolve all dependencies.** Universal lookup becomes Service Locator and hides product requirements.
7. **Caching is an implementation detail.** It changes identity, lifetime, mutation, concurrency, and shutdown.
8. **Registration is free extensibility.** It creates code-loading, trust, collision, version, and lifecycle obligations.
9. **Tests need only check concrete type.** Contract behavior, configuration correspondence, errors, and cleanup matter.
10. **Factories should never be removed.** When policy disappears, indirection may no longer earn its cost.

## Worked Examples

### Example 1

**Question:** What does the executable formatter factory establish?

**Reasoning:** It allowlists two keys, constructs one fully usable product, exposes a shared `format` operation, produces deterministic ordering, and rejects `xml`. It does not validate arbitrary JSON values or external configuration.

**Conclusion:** A small closed selection boundary can be explicit and exhaustively tested.

### Example 2

**Question:** When is a named constructor better than overloaded constructors?

**Reasoning:** `Money.from_minor_units(125, "EUR")` and `Money.parse("1.25 EUR")` have distinct preconditions and failures that parameter types alone may not communicate. Names preserve intent and allow parsing errors.

**Conclusion:** Use named creation to distinguish semantics, not merely to avoid the `new` keyword.

### Example 3

**Question:** Should a factory read environment variables on every call?

**Reasoning:** Repeated ambient reads hide dependency and can produce inconsistent products. Parse and validate configuration once at the composition root, then pass a typed configuration or a configured factory.

**Conclusion:** Separate external configuration acquisition from deterministic product creation.

### Example 4

**Question:** Factory parameter or dependency injection for a consumer?

**Reasoning:** Inject one ready dependency when the consumer uses one stable service. Inject a narrow factory when the consumer legitimately creates per-operation products with runtime parameters or lifetimes.

**Conclusion:** Do not inject creation power when a product suffices.

### Example 5

**Question:** When may a closed factory become a registry?

**Reasoning:** Independently shipped providers and post-deployment extension create the force. Define signed discovery, API version, duplicate keys, isolation, ordering, diagnostics, registration freeze, and unloading before opening registration.

**Conclusion:** Plugin extensibility is an architectural capability, not a dictionary substitution.

### Example 6

**Question:** How should an async database-client factory handle cancellation?

**Reasoning:** Validate configuration, acquire socket, authenticate, and initialize session under one deadline. On cancellation at any stage, close completed resources exactly once and return no usable handle. Report safe classified failure.

**Conclusion:** Async creation owns partial resources until successful transfer.

### Example 7

**Question:** Can a factory return a pooled connection as if newly created?

**Reasoning:** A pool returns a lease, not an owned connection. The contract must specify timeout, health check, transaction reset, release, leak detection, and behavior after pool shutdown.

**Conclusion:** Name and type the lifecycle actually transferred.

### Example 8

**Question:** Does memoizing a formatter turn the factory into Singleton?

**Reasoning:** Caching immutable formatters may be valid if keys cover all semantic configuration. It does not require global access, and one cached instance per configuration differs from a universal singleton.

**Conclusion:** Creation count, cache identity, and access mechanism are separate decisions.

### Example 9

**Question:** How should a cryptographic provider factory select algorithms?

**Reasoning:** Accept a policy identifier, not arbitrary class name; enforce an approved allowlist, key compatibility, parameter bounds, provider integrity, error hygiene, and migration policy. Named security review owns changes.

**Conclusion:** Security-sensitive factories enforce policy and must fail closed.

### Example 10

**Question:** When should a one-product factory disappear?

**Reasoning:** If it forwards unchanged to one cheap constructor and owns no validation, name, compatibility, dependency boundary, or lifecycle, migrate callers to the composition root and remove it. Retain a named function if it still enforces invariants.

**Conclusion:** Centralize real policy; do not preserve empty ceremony.

## Cross-Program Connections

- **Object-Oriented Programming:** constructors, protocols, polymorphism, and subtype contracts shape returned products.
- **Functional Programming:** higher-order creation functions and closures often replace factory classes.
- **Systems Programming:** RAII, ownership, allocation, handles, and cleanup define resource correctness.
- **Programming Languages:** effect systems, result types, modules, reflection, and async semantics change factory design.
- **Software Design:** information hiding and dependency inversion determine the creation boundary.
- **Software Architecture:** composition roots and configuration separate assembly from use.
- **Testing & Quality Engineering:** contract suites, fault injection, and leak checks validate every product and failure partition.
- **Security Engineering:** allowlists, trusted loading, secret handling, and fail-closed selection constrain factories.
- **Database Engineering:** connection pools, transactions, and session reset require explicit lease semantics.
- **Cloud Engineering:** client factories coordinate credentials, regions, retries, endpoints, and shutdown.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Defines GoF Factory Method and Abstract Factory, providing the terminology boundary against a simple factory.
2. Joshua Bloch, [*Effective Java*, 3rd ed.](https://www.pearson.com/en-gb/subject-catalog/p/effective-java/P200000000138), Addison-Wesley, 2018. Develops static factory methods, valid object construction, resource management, and related Java creation guidance.
3. Eric Evans, [*Domain-Driven Design: Tackling Complexity in the Heart of Software*](https://www.pearson.com/en-gb/subject-catalog/p/domain-driven-design-tackling-complexity-in-the-heart-of-software/P200000009375/9780321125217), Addison-Wesley, 2003. Treats factories as lifecycle constructs for creating valid domain objects and aggregates without exposing internal assembly.
4. Martin Fowler, [“Inversion of Control Containers and the Dependency Injection Pattern”](https://martinfowler.com/articles/injection.html), 2004, accessed 2026-08-28. Separates configuration from use and compares injection, service location, constructors, and factory services.
5. Bjarne Stroustrup and Herb Sutter, editors, [*C++ Core Guidelines*](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines), accessed 2026-08-28. Rules I.11, R.1, R.3, R.5, and R.20 clarify ownership transfer, scoped resources, values, and owning handles.
6. Robert C. Martin, *Agile Software Development: Principles, Patterns, and Practices*, Prentice Hall, 2002, ISBN 978-0-13-597444-5. Discusses dependency inversion, abstract interfaces, and creation-boundary consequences in object-oriented design.
7. Mark Seemann and Steven van Deursen, *Dependency Injection Principles, Practices, and Patterns*, Manning, 2019, ISBN 978-1-61729-473-0. Develops composition roots, explicit dependency graphs, lifetime, and container boundaries.

## Exercises

### Exercise 1

Specify a creation contract for the executable formatter factory: supported keys, configuration, success postconditions, errors, ownership, thread safety, effects, and at least eight test partitions.

### Exercise 2

Extend the factory with a `csv` formatter for records whose keys may differ. Define deterministic column ownership and escaping, then state what the chapter's one-record example cannot verify.

### Exercise 3

Design an async factory for an authenticated cloud-storage client. Include validation order, deadlines, cancellation, partial cleanup, credentials, retry ownership, observability, and shutdown.

### Exercise 4

A service has a global factory/container queried from forty domain classes. Plan a migration to one composition root and narrow per-operation factories without changing observable behavior.

### Exercise 5

An unfamiliar hospital device platform loads independently supplied treatment-algorithm plugins. Produce a graduate-level registry-factory design covering trust, compatibility, deterministic selection, lifecycle, isolation, resource limits, evidence, rollback, and clinical authorization.

## Answers to the Exercises

### Answer 1

Supported keys are exactly `json` and `lines`; the configuration is empty in the current example. Success returns a non-null formatter with callable `format(record)`. JSON uses sorted compact keys; lines uses sorted `key=value` fields separated by `|`. Unknown keys raise `ValueError` with a bounded message. Products own no external resource, are fresh instances, perform no I/O, and are safe for concurrent calls only because current implementations hold no mutable state; that statement must change if state is added.

Partitions include both supported keys, unknown string, empty string, wrong key type, empty record, one field, key-order permutation, values containing separators, non-JSON-serializable values, mutation during formatting, concurrent use, and error-message secret hygiene. Contract tests should run against both products where semantics overlap; format-specific escaping needs separate tests.

### Answer 2

Define the product over a declared schema, not whichever keys the first record happens to contain. The factory accepts an ordered column tuple, validates uniqueness and allowed names, and returns a CSV formatter that emits that header and uses a standards-compliant writer for quoting delimiters, quotes, newlines, null policy, and encoding. Each row must have the declared columns; missing or extra fields follow explicit error policy. Determinism comes from the supplied schema order.

The one-record example cannot verify multirow header consistency, different key sets, delimiters inside values, quotes, embedded newlines, Unicode, nulls, binary values, spreadsheet-formula injection, encoding, large streams, partial writes, or schema evolution. Executing one happy row is bounded evidence, not universal CSV correctness.

### Answer 3

Parse endpoint and region, validate transport/TLS policy and bucket scope, obtain a credential handle without logging secret material, then create transport, authenticate, and perform a bounded readiness check. One parent deadline and cancellation token cover all stages. The factory owns every partial handle until successful transfer; cancellation or failure closes transport and credential leases exactly once.

Return a ready client with explicit async close or context-manager ownership. Classify invalid configuration, unavailable credential, authentication, policy denial, DNS/connect/TLS, timeout, cancellation, and capacity errors. Decide whether retries belong inside creation; bound attempts by the same deadline and expose attempt telemetry without secrets. Record endpoint, region, provider, duration, and safe failure class. Shutdown rejects new creation, cancels or drains in-flight attempts, and closes shared resources according to documented ordering. Fault tests cancel after each acquisition boundary and verify no sockets, tasks, or leases remain.

### Answer 4

Inventory all lookups, keys, scopes, reset hooks, hidden optional dependencies, and lifecycle behavior. Characterize outputs, failures, startup/shutdown, identity sharing, and tests. At the application entry point, construct the existing container once. Introduce explicit constructor parameters in leaf domain classes, temporarily supplying values from an adapter at the nearest boundary. Move construction upward layer by layer and track migrated call sites.

Inject ready stable services. Where behavior legitimately creates per-request resources, define a narrow typed factory such as `SessionFactory.create(request_context)` with explicit ownership; do not pass the container. Preserve existing scopes initially, then correct scope in separate behavior work. Add a rule preventing new global lookups. When inventory reaches zero, remove locator fallback, global reset, and domain dependency on container APIs. Verify behavior and lifecycle after every slice; retain the composition root as the sole concrete assembly authority.

### Answer 5

Use a closed trust root and signed plugin artifacts; verify provenance, integrity, revocation, clinical approval identifier, API/ABI version, declared treatment scope, and deterministic priority before registration. Never load a class name directly from an unauthenticated order. Freeze the registry for a treatment session or use an immutable versioned snapshot so concurrent updates cannot change selection mid-treatment. Reject duplicate keys and ambiguous matches; log the exact approved artifact and policy version without patient secrets.

Run plugins in a constrained process or stronger isolation boundary with bounded CPU, memory, I/O, time, and capabilities. Define initialization, health, invocation, timeout, cancellation, crash, upgrade, rollback, and unloading; ensure partial initialization releases resources. Selection must fail safe when no approved compatible plugin exists. Contract, property, simulation, hardware-in-the-loop where relevant, fault, resource-exhaustion, malicious-input, concurrency, and clinical scenario tests provide distinct evidence. Maintain a known-safe version and atomic rollback, but prevent rollback to revoked artifacts.

Software validation cannot grant clinical authority. Named security, safety, privacy, platform, operations, regulatory, and clinical reviewers must approve the trust model, algorithms, evidence, deployment scope, monitoring, and incident response. Record every decision and patient-impact boundary; no dynamic extensibility benefit compensates for violating a safety constraint.
