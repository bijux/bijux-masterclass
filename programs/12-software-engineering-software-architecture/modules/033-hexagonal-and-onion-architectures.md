---
module_id: SARCH-033
program: Software Engineering: Software Architecture
level: 1
module_number: 33
title: Hexagonal and Onion Architectures
status: complete
last_verified: 2026-09-06
---

# Hexagonal and Onion Architectures

## One-Page Review

### Governing question

How do hexagonal and onion architectures protect application and domain policy from interfaces, databases, frameworks, and delivery mechanisms while keeping ports meaningful, adapters honest, and runtime behavior operable?

### Essential definitions

- The **application core** contains policy and use-case behavior that should remain independent of particular delivery and infrastructure mechanisms.
- A **port** is an application-owned contract through which an external actor drives the application or the application requires an external capability.
- A **driving** or **inbound port** exposes an application operation to a driver such as HTTP, a command line, a scheduler, or a test.
- A **driven** or **outbound port** expresses a capability the core requires, such as persistence, payment authorization, time, messaging, or identity verification.
- An **adapter** translates between a port and a particular external mechanism, protocol, representation, or device.
- **hexagonal architecture**, also called ports and adapters, arranges the application around explicit ports so it can be driven and tested independently of external technologies.
- **onion architecture** depicts concentric policy layers with source dependencies directed inward toward domain and application abstractions.
- A **composition root** assembles concrete adapters with application ports and owns process-level wiring and lifecycle.
- A **domain service** expresses domain policy that does not naturally belong to one entity; an **application service** coordinates a use case, authorization context, transactions, and external capabilities.
- A **leaky port** exposes an adapter's types or lifecycle so the core remains coupled to the mechanism despite an interface.

### Central model, mechanism, or theorem

Let $C$ be core policy modules, $P_i$ inbound ports, $P_o$ outbound ports, $A_i$ driving adapters, and $A_o$ driven adapters. With edge $x\rightarrow y$ meaning “$x$ statically depends on $y$,” the intended relation permits

$$
A_i\rightarrow P_i\rightarrow C,qquad C\rightarrow P_o,qquad A_o\rightarrow P_o,
$$

while prohibiting core dependencies on concrete adapters. Runtime control may enter through $A_i$, traverse the core, and reach $A_o$ through a bound port; static dependency still points toward core-owned contracts.

### Critical invariants

- define the core by policy and decisions worth protecting, not by a prescribed folder diagram;
- let the application own port vocabulary, semantics, errors, and compatibility;
- keep transport, persistence, framework, vendor, and device types outside core contracts;
- distinguish driving from driven roles without assuming all externals are either UI or database;
- direct static dependencies inward even when runtime control and data move both ways;
- put composition, startup, configuration, and adapter selection outside the core;
- translate identity, absence, units, errors, concurrency, and lifecycle explicitly at boundaries;
- assign transaction and consistency ownership to the use case and authoritative data boundary;
- prevent alternate adapters, jobs, tests, migrations, and administrative paths from bypassing policy;
- test ports as behavioral contracts and adapters against real mechanism semantics;
- expose adapter latency, failure, capacity, security, and observability instead of pretending infrastructure is interchangeable;
- introduce a port only when it protects a stable need or useful seam; avoid interface ceremony.

### Common failures

Common failures include drawing a hexagon without dependency rules; placing framework annotations in every core type while claiming independence; defining ports in the adapter module; mirroring a vendor API exactly; calling repositories from domain entities; passing ORM entities through inbound ports; one interface per class; service-locator lookups from the core; confusing inbound/outbound with network direction; treating adapters as behavior-free; assuming tests with mocks prove production compatibility; and forcing every operation through remote adapters.

### Compact example

`PlaceOrder` is an inbound port using application vocabulary. The HTTP adapter parses and authenticates a request, then invokes it. The use case applies domain invariants and calls an `AuthorizePayment` outbound port. A provider adapter implements that port and translates provider errors into application outcomes. The composition root supplies the adapter. The core has no HTTP or provider dependency, while runtime control traverses both.

### Connections

[SARCH-031](031-layered-architecture.md) supplies inward dependency reasoning; [SARCH-032](032-modular-monoliths.md) supplies internal module and data authority. [SARCH-034](../ROADMAP.md) next examines pipe-and-filter systems. Software Engineering Patterns owns Adapter, Gateway, Repository, Dependency Injection, Service Layer, and related code patterns; Software Design and Domain Modeling owns entity and code-level responsibility design.

## Governing Question

Applications live between external forces. Users, schedulers, messages, tests, and devices initiate work. Databases, payment providers, file systems, clocks, networks, and other applications supply capabilities. If policy is written directly in those mechanisms' vocabulary, every technical change becomes a policy change and core testing requires the world.

Hexagonal and onion architectures reorganize dependency so the application defines how the outside may drive it and what it needs from the outside. Adapters perform translation and integration. The governing challenge is to make those boundaries semantically meaningful rather than decorate conventional layers with ports and interfaces.

## Why This Matters

The style can protect business and system policy from framework churn, improve testability, support several delivery mechanisms, make external dependencies explicit, and create extraction seams. It also clarifies which side owns a contract and why static dependencies need not follow runtime calls.

Misapplied, it creates dozens of empty interfaces, mapping code, and mocks while vendor details still leak through exceptions, annotations, transactions, and data types. The core becomes anemic orchestration or an isolated model that ignores production failure.

The quality test is not whether the source tree resembles a hexagon or onion. It is whether valuable policy can be reasoned about, tested, and changed independently while adapters faithfully implement explicit semantics under real operational constraints.

## Prerequisites and Retrieval

Retrieve policy, mechanism, abstraction, dependency, inversion, interface, contract, module, domain model, application service, adapter, gateway, repository, transaction, consistency boundary, idempotency, error, concurrency, composition root, dependency injection, protocol, representation, data authority, observability, and evidence.

From SARCH-031 retrieve static dependency versus runtime control, policy-owned abstraction, strict and relaxed layering, framework leakage, and enforceable dependency graphs. From SARCH-032 retrieve module contracts, data authority, internal events, transaction boundaries, and extraction consequences.

## Learning Objectives

After completing this module, you should be able to:

1. explain hexagonal and onion architectures without relying on diagram shape;
2. identify application policy worth isolating from external mechanisms;
3. design inbound and outbound ports in application-owned vocabulary;
4. implement driving and driven adapters with explicit translation;
5. distinguish static dependency direction from runtime control and data flow;
6. locate domain, application, adapter, and composition responsibilities;
7. specify transaction, error, concurrency, identity, and security semantics at ports;
8. test core behavior, port contracts, adapters, and complete wiring appropriately;
9. detect leaky abstractions, interface ceremony, and mock-shaped architecture;
10. evaluate when the style's isolation benefit justifies its added boundaries.

## Core Exposition

**Start with the inside/outside distinction.** The “inside” is not everything written by the application team. It is the policy and use-case behavior whose meaning should not be governed by a particular UI, database, broker, cloud API, or framework. The “outside” contains mechanisms that drive or serve that policy.

This is a dependency boundary, not necessarily a process, deployment, trust, or team boundary. Core and adapters may compile into one artifact and execute on one call stack. Separate views are needed for runtime, deployment, security, and ownership.

**Understand the hexagonal idea.** Cockburn introduced ports and adapters to let an application be driven by users, programs, automated tests, or batch scripts and to let replaceable devices or databases serve it without contaminating its inside [1]. The hexagon's sides are not six mandatory layers. The shape emphasizes symmetry among external mechanisms.

The important distinction is not “top” versus “bottom.” A web controller and a scheduled job can both be driving adapters. A database and a payment provider can both be driven adapters. A message consumer drives one use case, while a message publisher is driven by another.

**Understand the onion idea.** Onion architecture presents concentric policy boundaries: domain model and policy near the center, application behavior around them, and infrastructure and user-interface mechanisms outside [2]. Static source dependencies point inward. The exact number and names of rings vary; dependency and responsibility are the durable ideas.

Hexagonal architecture foregrounds ports and adapter symmetry. Onion architecture foregrounds concentric policy and dependency. They are compatible but not identical brands. Use the vocabulary that makes the local design clearest, and define it in the architecture description.

**Identify policy worth protecting.** Begin with use cases, invariants, decisions, and change scenarios. Pricing rules, scheduling constraints, identity policy, safety limits, or document acceptance may deserve a core boundary. A CRUD screen over one stable store may need far less structure.

Do not call code “domain” merely because it has no framework import. A core responsibility should express system meaning. Equally, do not strip operational constraints from policy: retries, deadlines, duplicate commands, authorization, and stale data can affect correctness and need explicit application semantics.

**Design inbound ports around intentions.** An inbound port represents what an authorized actor can ask the application to do or learn. Use names such as `PlaceOrder`, `RescheduleVisit`, or `GetAccountStatement`, not `POST /v2/orders` or `handleClick`.

Specify input meaning, identity, authorization context, preconditions, result, errors, idempotency, concurrency, timeout responsibility, and consistency. Avoid one generic `execute(map)` port that discards domain vocabulary. Do not embed HTTP status codes, JSON nodes, framework requests, or UI widgets in the contract.

An inbound port can be a function, interface, message schema, command handler, or stable module API. The form matters less than ownership and semantics. Several driving adapters can implement translation into the same application operation.

**Design outbound ports around required capabilities.** An outbound port says what the core requires, not what a chosen vendor happens to provide. `LoadOrder`, `AuthorizePayment`, `PublishOrderPlaced`, `CurrentTime`, and `ReserveInventory` name application needs.

Define success, absence, conflict, retry, timeout, duplicate, ordering, atomicity, and security behavior. A port that copies every method and error code from a vendor SDK does not isolate the vendor. Model the smallest capability the use case truly needs.

**Place port ownership deliberately.** Inbound ports are generally owned by application policy because they define supported operations. Outbound ports are also owned on the policy side because they define required capability. Concrete adapters depend on these contracts and implement them.

This ownership is dependency inversion. If the database adapter owns `OrderRepository` and the core imports database record types from it, the source graph may have an interface but the design vocabulary still points outward. Put stable requirements with their consumer.

**Keep domain and application responsibilities distinct.** Domain entities, value objects, and domain services enforce business or system invariants in domain vocabulary. Application services coordinate a use case: load state, authorize, invoke domain behavior, manage a transaction boundary, call external capabilities, publish facts, and shape the outcome.

Not every system needs rich entities. A calculation service or workflow policy can be the core. Avoid an anemic domain forced by framework entities, but also avoid placing transport parsing, transaction APIs, or provider retries inside domain objects.

**Build driving adapters.** A driving adapter accepts an external stimulus, authenticates or receives identity, validates representation, translates it to a port request, invokes the application, and translates the result. Examples include HTTP, CLI, GUI, scheduler, message consumer, test harness, and hardware input.

Representation validation and domain validation differ. The adapter can reject malformed JSON; the core decides whether an order can be cancelled. The adapter maps a conflict outcome to HTTP 409 or a CLI exit status. That mapping must not redefine policy.

**Build driven adapters.** A driven adapter implements an outbound port with a database, filesystem, network provider, queue, clock, random source, device, or another module. It translates application types and semantics into mechanism behavior.

Adapters are not trivial plumbing. They own connection handling, serialization, schema mapping, provider error classification, timeout, retry where safe, circuit behavior, observability, authentication to the provider, capacity, and cleanup. The port constrains observable semantics; the adapter manages mechanism detail.

**Separate translation from loss.** Boundary mapping must preserve identity, units, absence, precision, ordering, error cause, concurrency version, and security classification. A provider may offer more states than the application contract. Decide whether to map, reject, preserve as unknown, or extend the port.

Do not catch every adapter exception and return `false`. That erases unavailable, rejected, timed out, conflicted, and malformed outcomes. The application cannot then choose safe behavior. Define a bounded error algebra in application vocabulary and preserve diagnostic cause outside sensitive responses.

**Keep framework types outside the core when valuable.** Framework request objects, ORM entities, annotations, base classes, reactive streams, cancellation tokens, and transaction handles can carry useful semantics. Excluding all of them has cost; including them creates coupling.

Choose deliberately. A standard cancellation abstraction may be appropriate; a vendor query builder in a domain invariant usually is not. Record accepted constraints and their change consequences. “Framework independent” is a bounded claim, not a purity label.

**Use a composition root.** Startup code chooses adapters, supplies configuration, establishes process resources, registers routes and consumers, and binds implementations to ports. Keep this wiring at the outside. The core should not call a global service locator or read environment variables to choose its database.

The composition root also owns lifecycle: start dependencies, validate configuration, expose readiness, drain work, stop consumers, and release resources. It may be framework-specific. It should not become a place for business decisions.

**Distinguish dependency injection from inversion.** Constructor injection or a container can provide implementations, but injection alone says nothing about contract ownership. A core class injected with a vendor client still depends on the vendor.

Dependency inversion exists when source knowledge and vocabulary point toward stable policy. Manual wiring can achieve it. A dependency-injection framework can undermine it through global lookup, reflection, runtime ambiguity, and configuration that no static rule checks.

**Own transactions in the application boundary.** A use case determines which local changes form one atomic operation. The application service can request a transaction capability or repository unit of work without exposing database handles to domain policy.

Do not hold local database transactions open across slow remote calls unless the protocol and consequences are explicit. Often authorize or reserve externally, persist intent, and coordinate outcomes with compensation or reconciliation. Ports must reveal when atomicity is impossible.

**Model time and concurrency.** `CurrentTime` as a port can make policy deterministic, but it needs clock and timezone semantics. Repositories should expose version or conflict behavior rather than silently overwriting. Commands need identity and idempotency when adapters can retry.

An in-memory test adapter must reproduce essential conflict, ordering, absence, and transaction behavior if tests rely on them. A dictionary that never fails is not a faithful substitute for a database port with uniqueness and optimistic concurrency.

**Handle security at the right boundaries.** A driving adapter establishes authenticated evidence and parses untrusted input. Application policy authorizes the requested operation in context. Domain policy enforces invariants that apply regardless of actor. Driven adapters protect credentials and secure outgoing connections.

Do not let adapters decide business authorization they cannot understand, and do not pass raw tokens deep into the domain. Alternate adapters—jobs, messages, administration, and tests—must not bypass authorization or audit obligations.

**Expose operational semantics.** Ports should make deadline, cancellation, retry safety, and unavailable outcomes visible when they affect decisions. Adapters emit mechanism-level signals; application behavior emits use-case outcomes. Correlate them without leaking secrets or high-cardinality payloads.

An adapter swap is not free. Providers differ in consistency, rate limit, availability, latency, error, and security. Substitutability requires behavioral contracts and evidence, not matching method signatures.

**Test in layers of evidence.** Core unit tests drive inbound ports with deterministic outbound fakes to explore policy, boundary, and adversarial cases. Port contract suites check every adapter against required semantics. Integration tests use real databases, brokers, or provider sandboxes where available. Composition tests verify wiring; end-to-end tests verify selected paths.

Mocks prove expected interaction with the mock, not compatibility with production. Test error classification, transaction behavior, concurrency, serialization, retry, timeouts, and cleanup. Record unavailable external evidence honestly.

**Avoid interface proliferation.** Add a port when the core needs a capability whose mechanism should remain outside, when several adapters are real or plausible under a change scenario, or when deterministic testing needs control over a nondeterministic boundary.

Do not create an interface for every class. Internal policy collaborations can use concrete types. Each boundary imposes vocabulary, mapping, navigation, testing, and governance cost. An interface with one implementation can still be valuable, but its value must be the protected decision rather than a numeric target.

**Avoid a generic adapter layer.** Organize adapters by port and mechanism, with clear ownership. A giant `infrastructure` package containing databases, mail, messages, HTTP, configuration, and security becomes another catch-all. Keep internal visibility and dependency rules precise.

Multiple adapters for one port should not fork semantics. If a CLI adapter can cancel an order without the authorization required by HTTP, either the policy boundary is wrong or the CLI represents a distinct privileged operation that must be explicit.

**Combine with modular monoliths.** Each module in a modular monolith can expose inbound ports and own outbound needs. An adapter may connect modules in-process. Avoid one global application core with every port; preserve capability and data authority.

Internal module calls can remain direct when semantics are stable. Ports and adapters do not require messages or services. If a module is later extracted, the port provides a starting seam, but remote failure, versioning, security, and data migration remain new work.

**Know the limits.** Hexagonal and onion structures primarily address dependency and testability. They do not by themselves establish scalability, availability, security isolation, concurrency correctness, data consistency, usability, or good domain modeling.

They can also be excessive for simple bounded scripts, stable CRUD utilities, or performance-critical code where translation dominates. Apply the architecture at the granularity where policy and volatile mechanisms genuinely differ.

**Review conformance and outcomes.** Extract source dependencies and compare them with allowed relations. Inspect port vocabulary for vendor leakage. Review composition and alternate entry points. Audit database and message access. Exercise adapters against contracts.

Then examine change evidence: do provider or framework changes remain outside? Can policy be tested without infrastructure? Are errors and concurrency represented? Do mappings cause defects or latency? Structural conformance is necessary only for the declared dependency goal; outcome evidence decides whether the style helps.

## Definitions and Notation

Let $C$ be core modules, $P_i$ inbound ports, $P_o$ outbound ports, $A_i$ driving adapters, and $A_o$ driven adapters. Let $E\subseteq X\times X\times K$, where $X=C\cup P_i\cup P_o\cup A_i\cup A_o$, and $(x,y,k)$ means $x$ statically depends on $y$ by kind $k$.

The intended source relation $R$ permits adapter dependencies on ports, inbound-port dependencies on core policy, core dependencies on required outbound ports, and driven-adapter dependencies on those outbound ports. It prohibits $C\rightarrow A_i$ and $C\rightarrow A_o$ for governed production-use edges.

Let $bind:P_o\rightarrow A_o$ be configuration supplied by the composition root. Binding selects an implementation at runtime without changing source ownership. Let $call_s$ be a runtime trace for scenario $s$; $call_s$ may move from driving adapter to core to driven adapter even though static edges never point from core to concrete adapter.

For port $p$, define semantic obligations $O(p)$ including input, result, error, identity, authorization, time, concurrency, idempotency, atomicity, and operational conditions. An adapter conforms only to the applicable obligations it can implement under declared assumptions.

## Mechanisms, Invariants, or Proof Structure

**Inward-dependency invariant.** Core production-use edges do not target concrete adapters or their mechanism types. The composition root may depend on both because its responsibility is assembly.

**Port-ownership invariant.** Port vocabulary expresses the consuming application's intention. An outbound port can be satisfied by several mechanisms without importing their types into the core.

**Runtime/static distinction.** Binding an adapter to a port allows runtime control to reach the adapter through dynamic dispatch while the core's static dependency remains on the port. Therefore outward runtime flow does not imply outward source dependency.

**Translation invariant.** Boundary translation preserves application-relevant identity, value, units, absence, ordering, concurrency, and error distinctions. Deliberate loss is documented and tested.

**Policy invariant.** Driving adapters establish external representation and authenticated context; application and domain policy decide authorized behavior and invariants. Alternate adapters cannot silently bypass those rules.

**Transaction invariant.** The application use case names its consistency boundary. An outbound port does not promise remote atomicity unless the contract and mechanism truly establish it.

**Substitution limitation.** Equal signatures are insufficient. If two adapters differ on ordering, duplicate effects, timeout, conflict, or durability required by $O(p)$, they are not behavioral substitutes for that port.

**Evidence invariant.** Core tests validate policy under fake assumptions; contract and integration tests validate adapters in recorded environments; end-to-end tests validate selected compositions. No layer alone proves the whole system.

## Alternatives and Trade-Offs

**Direct mechanism use versus a port.** Direct use minimizes indirection and mapping. A port protects policy and enables substitution when mechanism volatility, testing, or ownership matters. Use direct dependencies for stable details whose abstraction cost exceeds benefit.

**Rich core versus transaction script.** Rich domain policy localizes invariants and vocabulary. Simple transaction scripts can be clearer for straightforward workflows. Both can sit behind ports; do not force object complexity as proof of architecture.

**Repository-style port versus capability port.** CRUD repositories resemble persistence and may leak storage thinking. Capability ports express application needs but can proliferate. Choose the level matching the protected decision and consistency boundary.

**Synchronous versus asynchronous adapter.** Synchronous calls simplify immediate outcomes but propagate latency and failure. Asynchronous mechanisms decouple time but add durable delivery, ordering, duplicate, reconciliation, and observability obligations.

**Handwritten mapping versus shared types.** Mapping preserves vocabulary and ownership but adds code and possible information loss. Shared stable types reduce overhead but increase coordination. Decide by semantic and change differences, not mapping aversion.

**Manual composition versus injection framework.** Manual wiring is explicit and statically visible but can be verbose. Frameworks support configuration and lifecycle but can introduce reflection, hidden graphs, and global lookup. Keep assembly at the edge either way.

**One architecture around the whole system versus per-module boundaries.** A single core is simple for one cohesive capability. Large systems need bounded cores so ports do not become universal gateways and models do not collapse.

## Failure Modes and Misconceptions

1. **“The hexagon has six layers.”** The shape represents multiple external sides, not a fixed count.
2. **“Inbound means incoming network traffic.”** Schedulers, tests, devices, and local modules can drive ports.
3. **“Outbound means an HTTP request.”** Persistence, clocks, files, queues, and devices can be driven capabilities.
4. **“Every dependency should have an interface.”** Ports protect meaningful boundaries, not class counts.
5. **“Dependency injection equals dependency inversion.”** Contract ownership and vocabulary determine inversion.
6. **“The domain calls the database adapter.”** It calls a policy-owned required capability; wiring binds the adapter.
7. **“Adapters contain no logic.”** Translation, protocol, failure, security, and lifecycle logic belong there.
8. **“Framework annotations are always harmless.”** They may impose lifecycle, serialization, or persistence coupling.
9. **“Repository ports should mirror tables.”** Ports express application data needs and invariants.
10. **“One generic error is portable.”** Erasing conflict, timeout, rejection, and unavailability prevents safe policy.
11. **“An in-memory fake proves database conformance.”** It may omit uniqueness, isolation, failure, and concurrency.
12. **“A second adapter is always cheap.”** Behavioral semantics, operations, and evidence differ between mechanisms.
13. **“A port makes extraction ready.”** Remote communication and data migration add new obligations.
14. **“The core should ignore operations.”** Deadlines, duplicates, stale data, and authorization can affect correctness.
15. **“Diagram conformance proves value.”** Change, test, failure, and runtime evidence must show the boundary helps.

## Worked Examples

### Example 1

**Situation.** An HTTP controller passes a framework request object to `PlaceOrder`.

**Reasoning.** The inbound port now depends on header, JSON, and request-lifecycle concepts. Define an application request with customer identity, items, idempotency key, and authorization context. Let the adapter parse and authenticate HTTP and map application outcomes back to status and response representations.

**Conclusion.** A driving adapter translates transport semantics without making them application vocabulary.

### Example 2

**Situation.** `PaymentGateway` repeats every method and exception from one provider SDK.

**Reasoning.** The supposed port is vendor-shaped. Derive the application's required operations: authorize amount in currency, capture authorization, cancel, and query outcome. Define rejected, unavailable, timed-out, conflict, and unknown-result semantics. The adapter maps provider-specific behavior and preserves diagnostics outside public policy.

**Conclusion.** A useful outbound port expresses application need rather than disguising a vendor API.

### Example 3

**Situation.** A reviewer sees runtime calls from core policy to a SQL adapter and reports an outward dependency violation.

**Reasoning.** Inspect source edges. The core imports `OrderStore`; the SQL adapter imports and implements it; the composition root supplies the implementation. Dynamic dispatch transfers control to SQL, but no core source imports SQL types. The runtime and module views are consistent.

**Conclusion.** Runtime direction and static knowledge must be modeled separately.

### Example 4

**Situation.** An in-memory repository accepts two concurrent updates that a production repository rejects by version.

**Reasoning.** The fake does not satisfy the port's conflict obligation. Add versioned saves and a deterministic conflict mode to the fake; run a shared contract suite against both. Integration-test actual database isolation and retry behavior.

**Conclusion.** Test adapters must reproduce behavior relevant to policy, not merely method signatures.

### Example 5

**Situation.** A use case opens a database transaction, calls a remote shipping provider, and waits 20 seconds.

**Reasoning.** The local lock and transaction outlive an unreliable remote call, increasing contention without creating cross-system atomicity. Persist intent, commit local invariants, invoke shipping under an idempotent workflow, and record or reconcile the outcome. State cancellation and compensation policy.

**Conclusion.** A port boundary must expose remote failure rather than letting a local transaction imply atomicity.

### Example 6

**Situation.** A CLI adapter can issue refunds without the authorization checks used by HTTP.

**Reasoning.** Authorization belongs in the application operation, using authenticated actor and purpose supplied by each adapter. If the CLI is an emergency privileged operation, model a distinct port, approval, audit, scope, and safety conditions instead of bypassing the common use case.

**Conclusion.** Multiple driving adapters must not silently fork policy.

### Example 7

**Situation.** Mapping a million-row export through three object forms exhausts memory.

**Reasoning.** Measure allocation and ownership. Define a streaming export port with bounded batches and cancellation in application vocabulary; let the database adapter stream stable projections and the output adapter encode them. Preserve ordering and snapshot assumptions. Do not expose raw database cursors to the core.

**Conclusion.** Boundary isolation can coexist with efficient streaming when the port models the real workload.

### Example 8

**Situation.** A dependency container permits any core class to resolve any registered adapter by string name.

**Reasoning.** The service locator hides dependencies and lets policy select mechanisms. Move selection to the composition root, inject narrow ports explicitly, fail startup on missing configuration, and export a reviewable wiring graph. Restrict dynamic plugin discovery to an adapter boundary.

**Conclusion.** Runtime flexibility should not erase source-visible dependency ownership.

### Example 9

**Situation.** A weather provider returns `unknown`, but the adapter maps it to temperature zero.

**Reasoning.** Zero is a valid measurement and changes control policy. Model observed value, unavailable, stale, and invalid states distinctly, with unit and observation time. The application chooses safe degraded behavior. Log provider diagnostics without exposing credentials.

**Conclusion.** Translation must preserve absence and uncertainty rather than invent domain facts.

### Example 10

**Situation.** A laboratory instrument controller accepts operator, scheduled, calibration, and remote-maintenance commands and drives sensors, actuators, storage, and alarms.

**Reasoning.** Define distinct inbound ports with identity and safety authority; core policy enforces operating modes and invariants. Define outbound ports for timestamped sensing, bounded actuation, durable records, and alarm delivery. Adapters manage protocols and devices. A hardware cutoff remains an independent safety mechanism represented outside the application guarantee. Test fakes, real devices, timing, disconnects, stale data, unauthorized commands, and composition.

**Conclusion.** High-consequence ports and adapters require explicit authority, timing, physical limits, and layered evidence.

## Cross-Program Connections

- **Software Design and Domain Modeling:** entities, value objects, domain services, application services, and dependency inversion refine the core.
- **Software Engineering Patterns:** Adapter, Gateway, Repository, Dependency Injection, Facade, Service Layer, and Unit of Work implement recurring boundary roles.
- **Testing and Quality Engineering:** fakes, mocks, contract suites, integration environments, fault injection, and composition tests provide distinct evidence.
- **Database Engineering:** transactions, isolation, schema mapping, optimistic concurrency, and migrations constrain persistence adapters.
- **API and Service Engineering:** precise request, result, error, compatibility, idempotency, and version semantics shape ports.
- **Security Engineering:** authentication evidence, authorization policy, secrets, trust boundaries, audit, and alternate entry points cross adapters and core.
- **Distributed Systems:** remote adapters introduce partial failure, retry, ordering, duplicate effects, reconciliation, and time uncertainty.
- **Embedded and Systems Engineering:** device adapters, timing, modes, safety authority, and physical feedback extend the boundary model.

## References

1. Alistair Cockburn, “Hexagonal Architecture,” 2005. https://alistair.cockburn.us/hexagonal-architecture/
2. Jeffrey Palermo, “The Onion Architecture: Part 1,” 29 July 2008. https://jeffreypalermo.com/2008/07/the-onion-architecture-part-1/
3. David L. Parnas, “On the Criteria To Be Used in Decomposing Systems into Modules,” *Communications of the ACM*, vol. 15, no. 12, pp. 1053–1058, 1972. https://doi.org/10.1145/361598.361623
4. Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003.
5. Vaughn Vernon, *Implementing Domain-Driven Design*, Addison-Wesley, 2013.
6. Robert C. Martin, *Clean Architecture: A Craftsman's Guide to Software Structure and Design*, Prentice Hall, 2017.
7. Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2002.
8. Len Bass, Paul Clements, and Rick Kazman, *Software Architecture in Practice*, 4th ed., Addison-Wesley, 2021.

## Exercises

### Exercise 1

Precisely distinguish application core, policy, inbound port, outbound port, driving adapter, driven adapter, composition root, dependency injection, dependency inversion, application service, and domain service.

### Exercise 2

Given modules `Http`, `PlaceOrder`, `Domain`, `PaymentPort`, `ProviderAdapter`, and `Composition`, list the intended static edges and a plausible runtime call sequence. Explain why the two relations differ without contradiction.

### Exercise 3

Diagnose a system whose core imports ORM entities, HTTP status codes, a provider client, environment variables, and a dependency-injection container. Propose a bounded repair without creating one interface per class.

### Exercise 4

Compare direct database use, a CRUD repository port, and capability-specific outbound ports for a high-volume inventory application. Address semantics, transactions, performance, mapping, testing, concurrency, and change.

### Exercise 5

Transfer ports and adapters to a harbor gate-control system involving badge readers, vehicle sensors, operator consoles, scheduling, customs holds, barrier actuators, audit storage, intermittent networks, and emergency access. Define boundaries and evidence.

## Answers to the Exercises

### Answer 1

The **application core** contains policy and use-case behavior protected from mechanisms. **Policy** makes meaningful decisions and enforces rules. An **inbound port** is an application-owned operation through which a driver requests behavior; an **outbound port** is an application-owned required capability.

A **driving adapter** translates an external stimulus into an inbound-port call. A **driven adapter** implements an outbound port using a mechanism. The **composition root** assembles adapters, configuration, and lifecycle. **Dependency injection** supplies dependencies; **dependency inversion** makes mechanism code depend on policy-owned abstractions rather than policy importing mechanisms.

An **application service** coordinates a use case, identity, transaction, and external capabilities. A **domain service** expresses domain policy that does not belong naturally to one entity. Neither term requires a network service.

### Answer 2

Intended source edges are `Http -> PlaceOrder`, `PlaceOrder -> Domain`, `PlaceOrder -> PaymentPort`, `ProviderAdapter -> PaymentPort`, and `Composition` to the concrete modules it assembles. `PlaceOrder` does not import `ProviderAdapter`; `Domain` does not import HTTP, payment, or composition mechanisms.

A runtime sequence can be `Http -> PlaceOrder -> Domain -> PaymentPort binding -> ProviderAdapter`, followed by results returning through the stack. Dynamic binding lets control reach the adapter. Static edges describe source knowledge, while the call sequence describes one execution. The composition root knows both contract and implementation specifically because it owns assembly.

### Answer 3

Identify which policy actually needs protection. Define intention-based inbound operations and only the outbound capabilities those operations require. Translate HTTP representations and status at driving adapters. Translate ORM records in persistence adapters. Wrap the provider behind a capability port with application errors, timeout, duplicate, and unknown-result semantics.

Move environment and container access to the composition root. Inject explicit ports into application services. Keep core concrete classes where no volatile boundary or useful test seam exists; do not add interfaces between ordinary policy collaborators. Decide whether a small stable annotation or cancellation type is an accepted dependency and record the constraint rather than chasing absolute purity.

Enforce source rules, inspect generated and reflective wiring, contract-test adapters, integration-test database/provider behavior, and composition-test startup. Migrate one use case at a time with no false claim that untouched core code is already mechanism-independent.

### Answer 4

Direct database use minimizes abstraction and mapping and can be appropriate inside a bounded application module. It couples policy to query language, schema, transaction API, and engine behavior; deterministic tests require the database or extensive stubbing.

A CRUD repository port hides basic persistence and supports fakes, but it can mirror tables and encourage chatty load-modify-save behavior. Define identity, absence, version conflict, atomicity, and query limits. A capability port such as `ReserveStock` or `LoadAvailableInventory` matches use-case need and can support optimized atomic SQL, but many tiny ports increase navigation and may duplicate capabilities.

For high volume, begin with consistency and concurrency: stock reservation should be atomic at the authority, not implemented as an unsafe read then write. Measure query, mapping, allocation, and transaction cost. Use projections or streaming for large reads. Contract-test conflict and absence; integration-test real isolation, indexes, failure, and contention. Choose a repository when aggregate persistence is the protected decision and capability ports when operations require specialized semantics or mechanisms.

### Answer 5

Define inbound ports for authorized vehicle admission, operator override, scheduled access, customs hold/release, maintenance, and emergency action. Inputs carry stable identity, evidence, mode, request identity, and time. Core application and domain policy decide access, interlocks, current mode, hold priority, duplicate commands, and audit obligations.

Define outbound ports for badge verification, vehicle presence and position, schedule/customs status, bounded barrier actuation, alarm delivery, current time, and durable audit. Device and network adapters implement protocols, calibration, authentication, retry, and diagnostics. The composition root selects local and remote adapters and manages startup, readiness, drain, and safe shutdown.

Runtime control can enter from readers or consoles and reach actuators while static dependencies point toward policy contracts. Local safety interlocks and emergency hardware cutoffs remain independent physical safeguards; do not present application architecture as their proof. Model offline authority, stale schedule data, conflicting customs status, manual approval, fail-safe barrier state, and restoration.

Validate core rules with deterministic fakes; contract-test every device and network adapter; test actual sensors, timing, loss, duplicates, disconnects, power failure, unauthorized access, emergency modes, audit durability, and composition. Review operators' comprehension and preserve evidence scope, physical assumptions, and residual risk.
