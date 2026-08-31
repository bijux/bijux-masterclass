---
module_id: SEPAT-029
program: Software Engineering: Patterns
level: 1
module_number: 29
title: Ports and Adapters as a Structural Pattern
status: complete
last_verified: 2026-08-28
---

# Ports and Adapters as a Structural Pattern

## One-Page Review

### Governing question

How can an application own semantically meaningful boundaries so that user interfaces, tests, databases, messages, services, and devices attach through replaceable adapters without moving domain policy outward or pretending unlike technologies have identical guarantees?

### Essential definitions

- A **port** is an application-owned contract for a cohesive interaction with an external actor or capability.
- A **driving port** exposes an application capability to an actor that initiates interaction.
- A **driven port** states what the application requires from an external capability it calls.
- A **driving adapter** translates an outside protocol such as HTTP, CLI, UI, batch, or message delivery into a driving-port call.
- A **driven adapter** implements a driven port using a database, service, clock, queue, filesystem, device, or other mechanism.
- The **application core** contains use-case coordination and domain behavior without depending on concrete edge technologies.
- A **composition root** selects and wires concrete adapters at startup.
- **source dependency direction** concerns which code imports which; **runtime call direction** concerns who invokes whom.
- An **adapter contract test** applies the same semantic cases to every implementation of one port.
- A **test double** is an adapter used to control or observe a boundary in tests; it is evidence only for the behavior it faithfully models.

### Central model, mechanism, or theorem

Let application core (H) own driving ports (P_{in}) and driven ports (P_{out}). Adapters (A_{in}) and (A_{out}) satisfy

$$
A_{in}:ExternalInput\to P_{in},\qquad
A_{out}:P_{out}\to ExternalMechanism.
$$

At runtime a use case may call outward through (P_{out}), but its source dependency remains inward: (A_{out}\to P_{out}\leftarrow H). Replaceability follows only when the port captures the application's semantics and each adapter satisfies them; an interface that merely copies one vendor API does not create independence.

### Critical invariants

- The application owns each port's language, types, errors, consistency, time, and side-effect semantics.
- Core source code does not import framework, transport, persistence, provider, or generated-adapter types.
- Driving adapters validate protocol shape and authentication context but do not own domain rules.
- Driven adapters translate mechanisms without silently strengthening or weakening port guarantees.
- Transaction, idempotency, retry, acknowledgement, deadline, cancellation, and ordering authority are explicit.
- Every production adapter passes shared contract tests plus mechanism-specific integration and fault tests.
- Composition is external to the core, and no service locator hides concrete dependencies inside domain behavior.
- Port count and granularity follow cohesive replaceable boundaries, not one-interface-per-class ceremony.

### Common failures

Common failures include placing repository interfaces beside database code, exposing ORM entities through ports, making every method a port, naming ports after vendors, letting controllers contain business rules, treating an in-memory fake as proof of SQL behavior, using generic CRUD where domain operations need invariants, opening transactions inside unrelated adapters, acknowledging messages before durable acceptance, retrying at multiple edges, injecting a container/service locator into the core, mocking internal objects instead of boundaries, and claiming the database can be swapped when SQL-specific semantics have leaked everywhere.

### Compact example

A `ReserveSeat` use case owns two required capabilities: conditionally reserve one seat and append one domain event. An in-memory inventory and collecting event sink are driven adapters. The first request reserves and emits once; the duplicate is unavailable and emits nothing. The use case imports neither database nor messaging technology.

### Connections

[SEPAT-028](028-module-and-package-facades.md) curates public namespaces; Ports and Adapters controls application-to-environment dependency direction. [SEPAT-030](../ROADMAP.md) evaluates combinations and indirection cost. The topic connects to [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), [Database Engineering](../../18-database-engineering/ROADMAP.md), and [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md).

## Governing Question

Which interactions are genuine application boundaries, what semantics does the application require at each, and can multiple adapters honor those semantics without contaminating the core?

The hexagon's shape is incidental. The enduring idea is symmetry: a human UI, automated test, batch job, or peer application can drive the same application capability, while external mechanisms implement contracts the application owns.

## Why This Matters

When domain logic depends directly on web frameworks, ORM sessions, message clients, or cloud SDKs, technology choices determine testing, deployment, and evolution. Replacing a tool requires changing policy-bearing code, and failures leak in provider vocabulary.

Ports reverse that source dependency. They also add abstractions and translation. If their semantics are vague or copied from infrastructure, the architecture gains files without gaining independence.

## Prerequisites and Retrieval

You should understand dependency inversion, interfaces/protocols, domain modeling, transactions, messaging, distributed failure, testing, and dependency injection. Retrieve these facts:

1. The code that defines an interface owns its vocabulary and evolution pressure.
2. Runtime calls can point outward while compile/import dependencies point inward through inversion.
3. An in-memory data structure usually has different concurrency, transaction, and failure behavior from a database.
4. Network timeout can leave an external effect indeterminate.
5. Message delivery and business acceptance are separate events.
6. Translation includes semantic error and time behavior, not only field mapping.

## Learning Objectives

After completing this module, you should be able to:

- identify driving and driven actors and derive cohesive ports;
- place port ownership and source dependencies correctly;
- design domain-oriented types, operations, and error semantics;
- implement thin adapters without moving domain policy outward;
- define transaction, messaging, deadline, retry, and idempotency boundaries;
- build shared contract tests and mechanism-specific evidence;
- distinguish ports/adapters from layers, facades, gateways, repositories, and dependency injection;
- remove ceremonial ports that do not protect a real boundary.

## Core Exposition

### Start with actors and conversations

Identify who or what initiates a goal and which outside capabilities the application needs. Describe each conversation in application/domain language before choosing HTTP endpoints, tables, SDK calls, or queues.

One actor can use several ports, and one port can have several adapters. Do not assume one port per transport, class, or method.

### Let the application own ports

A driven port such as `SeatInventory.reserve_if_available(show, seat)` belongs near the use case/domain that needs the guarantee. A SQL adapter implements it. If the interface instead says `execute_query(sql)` or returns ORM rows, infrastructure owns the abstraction.

Ownership affects change: the application evolves the required capability, and adapters absorb provider differences. Ports should be named by durable intent, not technology.

### Separate dependency and call arrows

At runtime the core calls a database adapter through a port. In source, both core and adapter depend on the application-owned port. This is dependency inversion, not elimination of runtime I/O.

Make the rule executable with module/package boundaries and architecture tests. Folder diagrams without import enforcement decay.

### Design semantic contracts

Specify inputs, outputs, validation ownership, absent/conflict/forbidden/unavailable/indeterminate outcomes, consistency, atomicity, ordering, idempotency, deadlines, cancellation, pagination, and resource limits.

Do not demand impossible uniformity. A clock port and repository port have different semantics. Two repository adapters are substitutable only for the declared observations and workload limits.

### Keep driving adapters thin

HTTP controllers parse/version transport data, authenticate, derive trusted context, invoke a driving port, and map application outcomes to protocol responses. CLI and message adapters do analogous translation.

Domain validation remains inside. Duplicating policy in each adapter makes behavior depend on entry channel.

### Keep driven adapters honest

A driven adapter maps owned values/errors to one mechanism, enforces port-level limits, and reports weaker guarantees rather than hiding them. Provider retries, caches, or transactions must align with the application contract.

Provider-specific tuning can remain inside, but if it changes externally meaningful semantics, surface configuration or outcomes through an owned contract.

### Put transaction authority deliberately

For one database, an application transaction port or unit-of-work boundary may wrap a complete use case. Repository methods that each commit independently can violate aggregate invariants.

Across independent resources, do not advertise one atomic transaction without a real protocol. Use durable intent/outbox, idempotent consumers, progress state, compensation, and reconciliation as the use case requires.

### Model message acknowledgement

A driving message adapter decodes and authenticates, invokes the application, and acknowledges only according to the delivery/acceptance contract. Rejection, retryable failure, poison message, duplicate, and accepted-but-not-completed are distinct.

The core should not import broker delivery objects. Pass stable message identity, causation, tenant, deadline, and relevant metadata through owned context.

### Propagate time and cancellation

Driving adapters derive one operation deadline from trusted protocol/configuration. The application passes remaining budget through driven ports. Driven adapters must not reset a full timeout.

Cancellation signals lost interest and may stop work; it does not undo accepted effects. Ports for effectful work need explicit knowledge/reconciliation states.

### Compose outside the core

The composition root constructs concrete adapters and injects them. Configuration decides production versus test implementations. The core receives explicit dependencies, not a container it queries dynamically.

This keeps the dependency graph visible and prevents domain methods from selecting infrastructure by ambient global state.

### Test at multiple evidence levels

Fast core tests use deterministic fakes at ports. Shared contract suites test every adapter for semantic cases. Real integration tests cover schema, isolation, encoding, authentication, provider errors, timing, and cleanup.

Fault injection, concurrency, migration, load, and production-like deployment tests cover claims a fake cannot. Test driving adapters separately for protocol translation and end-to-end across representative compositions.

### Avoid boundary theater

Do not create an interface for a pure value object or stable in-process collaborator merely to satisfy a diagram. A port pays when it isolates a volatile/external boundary, enables another driver, makes effects controllable, or protects application vocabulary.

Track port/adapter count, fan-out, duplicate mappings, contract-test burden, and change patterns. Merge or remove boundaries whose abstraction has no independent meaning.

## Definitions and Notation

Let (H) be core modules, (P) application-owned port modules, and (A) adapter modules. Permitted source edges include (H\to P) and (A\to P); forbidden edges include (H\to A) and domain-to-framework/provider imports.

Let port contract be (C_P=(I,O,E,G,T,R)): input domain (I), output domain (O), error/outcome algebra (E), guarantees (G), time/cancellation semantics (T), and resource bounds (R). Adapter (a) conforms under observation set (Q) when (a\models_Q C_P).

For an operation deadline (D), each adapter receives remaining budget (b_i=\max(0,D-t_i)). For message identity (m), idempotent acceptance requires repeated delivery of the same scoped (m) and payload to produce one logical accepted effect, while conflicting payload reuse is rejected.

## Mechanisms, Invariants, or Proof Structure

### Derivation procedure

1. Name application goal and driving actor.
2. Identify required external capabilities and failure boundaries.
3. Define owned driving/driven ports in domain language.
4. Specify complete outcome, guarantee, time, and resource contracts.
5. Implement adapters that translate but do not own domain policy.
6. Wire them in an external composition root.
7. Enforce source dependency rules automatically.
8. Run core, shared contract, integration, fault, and end-to-end tests.
9. Measure ceremony and remove ports without durable boundary value.

### Executable mechanism

This in-memory example demonstrates an application-owned conditional reservation port and event sink. It is sequential and does not model durable atomic commit between reservation and event publication.

<!-- bijux-verify: {"id":"ports-seat-reservation","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=reserved\nsecond=unavailable\nremaining=1 events=1\n","stderr":""}} -->
```python
class ReserveSeat:
    def __init__(self, inventory, events):
        self.inventory = inventory
        self.events = events

    def execute(self, show_id, seat_id):
        if not self.inventory.reserve_if_available(show_id, seat_id):
            return "unavailable"
        self.events.append_event(("seat-reserved", show_id, seat_id))
        return "reserved"


class InMemoryInventory:
    def __init__(self, available):
        self.available = set(available)

    def reserve_if_available(self, show_id, seat_id):
        key = (show_id, seat_id)
        if key not in self.available:
            return False
        self.available.discard(key)
        return True


class CollectingEvents:
    def __init__(self):
        self.events = []

    def append_event(self, event):
        self.events.append(event)


inventory = InMemoryInventory([("show-4", "A1"), ("show-4", "A2")])
events = CollectingEvents()
reserve = ReserveSeat(inventory, events)

print("first=" + reserve.execute("show-4", "A1"))
print("second=" + reserve.execute("show-4", "A1"))
print("remaining=" + str(len(inventory.available)) + " events=" + str(len(events.events)))
```

A production design would make reservation plus durable event atomic through an owned transaction/outbox mechanism, handle concurrent attempts, authenticate the actor, and define cancellation and delivery.

### Proof obligations

Verify the source graph contains no forbidden core-to-adapter/provider edge. For each port guarantee, identify which core rule or adapter mechanism supplies it and test at the level where it can fail. Do not generalize from an in-memory fake to database or broker semantics.

The snippet proves only a finite sequential state transition. It does not prove concurrency, durability, transactional event publication, authorization, delivery, or production replaceability.

## Alternatives and Trade-Offs

| Approach | Organizing idea | Main trade-off |
|---|---|---|
| Ports and Adapters | application-owned boundaries around a core | translation and contract overhead |
| Layered architecture | ordered technical/domain layers | can point dependencies toward infrastructure |
| Facade | simplified subsystem entry | does not alone invert driven dependencies |
| Adapter pattern | one incompatible-interface translation | may be local rather than architectural |
| Plugin architecture | discovered extensions | versioning, trust, and lifecycle complexity |
| Functional core/imperative shell | pure decisions inside effectful shell | effects may still need semantic ports |
| Direct framework use | minimal indirection | couples policy to framework/provider |

These can coexist. Judge the actual dependency graph and contract ownership, not labels or directory shapes.

## Failure Modes and Misconceptions

### “The database is at the bottom”

Hexagonal architecture has inside and outside, not privileged top/bottom devices. The database is one external actor behind an application-owned port.

### “Every interface is a port”

Ports describe meaningful boundary conversations. Internal polymorphism and one-method wrapper interfaces are not automatically architectural ports.

### “Dependency injection creates hexagonal architecture”

Injection supplies objects. If the core imports a provider-owned interface or service locator, ownership and source direction remain wrong.

### “Fakes prove adapters are interchangeable”

Fakes validate core interaction under their model. Real adapters require shared contracts plus mechanism-specific integration, concurrency, and failure evidence.

### “Generic CRUD is reusable”

CRUD often omits domain atomicity, conflict, authorization, and intent. Prefer capability-specific operations where semantics differ.

### “Adapters contain no logic”

They own translation, protocol, encoding, provider configuration, and mechanism-specific recovery—not domain policy.

### “Replaceable means zero migration cost”

Data, indexes, query capabilities, consistency, operational behavior, and performance can differ. Ports bound the impact; they do not erase it.

## Worked Examples

### Example 1

HTTP and CLI adapters both invoke `ApproveClaim`; neither implements eligibility rules. Protocol validation differs, but domain outcome is shared. **Conclusion:** Multiple drivers expose whether policy truly lives inside.

### Example 2

A repository port returns an ORM entity with lazy relationships. Core tests require a session and provider upgrade changes behavior. An owned aggregate snapshot replaces it. **Conclusion:** Provider type leakage defeats inversion.

### Example 3

Each repository method commits independently, so reservation succeeds and event append fails. A transaction/outbox port owns one durable acceptance boundary. **Conclusion:** Port granularity must preserve use-case invariants.

### Example 4

An in-memory adapter allows two sequential reservations correctly but a SQL adapter races under concurrent transactions. A uniqueness constraint and isolation-aware contract test enforce one winner. **Conclusion:** Fakes cannot model every mechanism guarantee.

### Example 5

A message adapter acknowledges before the application records acceptance; a crash loses work. It acknowledges only after durable intent, while duplicate identity is idempotent. **Conclusion:** Delivery acknowledgement belongs to an explicit acceptance protocol.

### Example 6

A payment adapter maps timeout to `declined`. The server may have charged. Replacing it with `indeterminate` plus reconciliation prevents unsafe retry. **Conclusion:** Adapters must not destroy failure knowledge.

### Example 7

The core receives a dependency-injection container and requests a database client by string. Tests can substitute it, but source vocabulary and selection remain infrastructure-coupled. Explicit owned ports restore visibility. **Conclusion:** Service location hides rather than inverts dependencies.

### Example 8

Thirty interfaces wrap stable pure functions one-for-one. No alternative adapter or controlled effect exists. Removing them reduces navigation and preserves tests. **Conclusion:** Architectural ceremony has carrying cost.

### Example 9

A database migration changes an index and p99 latency violates the repository port's 100 ms budget while functional tests pass. Representative load tests catch the nonfunctional contract breach. **Conclusion:** Replaceability includes operational observations.

### Example 10

An autonomous-device adapter translates a domain command into actuator protocol. Independent interlocks remain in hardware/firmware, and indeterminate actuation is reconciled rather than retried blindly. **Conclusion:** Ports cannot manufacture physical safety.

## Cross-Program Connections

- **Programming Languages and Semantics:** interface ownership, modules, effects, and type boundaries implement the source graph.
- **Object-Oriented Programming:** dependency inversion, polymorphism, and substitutability underpin driven ports.
- **Functional Programming:** algebraic effects and functional-core/imperative-shell designs offer related boundaries.
- **Concurrent Programming:** cancellation, races, isolation, and resource ownership cross ports.
- **Domain Modeling:** ubiquitous language, aggregates, invariants, and domain services define port semantics.
- **Software Architecture:** dependency rules, components, composition roots, and fitness functions preserve the shape.
- **Testing and Quality:** fakes, contract suites, integration, fault injection, and architecture tests form layered evidence.
- **Database Engineering:** transactions, isolation, constraints, migrations, and outbox patterns implement persistence ports.
- **Distributed Systems:** deadlines, partial failure, idempotency, messaging, and reconciliation constrain adapters.
- **Systems Engineering:** devices, hazards, timing, and independent controls limit abstraction guarantees.

## References

1. Alistair Cockburn, [“Hexagonal Architecture: The Original 2005 Article”](https://alistair.cockburn.us/hexagonal-architecture), HaT Technical Report 2005.02, September 2005. Original statement of ports and adapters, driver symmetry, and isolated application testing.
2. David L. Parnas, [“On the Criteria To Be Used in Decomposing Systems into Modules”](https://dl.acm.org/doi/10.1145/361598.361623), *Communications of the ACM* 15(12), 1972. Establishes information-hiding decomposition around changeable design decisions.
3. Robert C. Martin, *Agile Software Development: Principles, Patterns, and Practices*, Prentice Hall, 2002, ISBN 978-0-13-597444-5. Provides dependency-inversion and package-design foundations.
4. Eric Evans, [*Domain-Driven Design: Tackling Complexity in the Heart of Software*](https://www.informit.com/store/domain-driven-design-tackling-complexity-in-the-heart-9780321125217), Addison-Wesley, 2003. Provides domain/application/infrastructure separation and owned domain language.
5. Vaughn Vernon, [*Implementing Domain-Driven Design*](https://www.oreilly.com/library/view/implementing-domain-driven-design/9780133039900/), Addison-Wesley, 2013. Connects domain-driven implementation with hexagonal ports and adapters.
6. AWS, [“Hexagonal architecture pattern”](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html), Prescriptive Guidance, accessed 2026-08-28. Describes applicability, implementation, testability, and maintenance overhead.
7. Steve Smith, [“Common web application architectures”](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures), Microsoft Learn, updated 2022, accessed 2026-08-28. Documents inward dependencies and infrastructure implementations around an application core.

## Exercises

### Exercise 1

Trace the executable reservation and identify the exact port semantics and missing production guarantees.

### Exercise 2

Derive driving and driven ports for document publication through HTTP, CLI, storage, search indexing, and notification.

### Exercise 3

Design a shared contract suite for an in-memory and SQL inventory adapter, including concurrency, transaction, and failure cases.

### Exercise 4

Diagnose a “hexagonal” application whose domain imports ORM annotations, controllers own validation, and adapters query a service locator. Give an incremental migration.

### Exercise 5

Design boundaries and evidence for an unfamiliar industrial command application without claiming functional safety.

## Answers to the Exercises

### Answer 1

The first call finds `(show-4,A1)`, removes it, appends one event, and returns `reserved`. The second call does not find the key, returns `unavailable`, and does not append. One of two seats remains and one event exists. The owned operations are conditional reservation and event append; the use case coordinates their order.

The trace lacks atomicity between removal and event append, concurrent one-winner evidence, crash recovery, durable data, event delivery, idempotency keys, authentication/authorization, cancellation, deadlines, capacity validation, and adapter substitutability. A database implementation needs constraint/isolation and transaction/outbox evidence; a broker implementation needs acceptance/delivery semantics.

### Answer 2

Driving ports are `PublishDocument(command, context)` and `PublicationStatus(operation_id, context)`, shared by HTTP and CLI adapters. The command uses owned document/version/content/provenance values; outcomes distinguish rejected, accepted, in-progress, completed, compensating, compensated, and indeterminate as required.

Driven ports include `DocumentStore.commit_version_and_intent`, `SearchIndex.upsert_version`, and `Notifier.request_notification`; define idempotency, version conflict, deadlines, and failure semantics separately. Storage is publication truth and atomically records an outbox intent where supported. Indexing and notification consume idempotently and report progress; neither silently rolls back canonical storage. HTTP maps auth/protocol/status, CLI maps arguments/output, and both leave document rules in the core. Composition chooses adapters; shared contract and end-to-end fault tests cover each boundary.

### Answer 3

Specify `reserve_if_available(show,seat,operation)->reserved|unavailable|conflict|unavailable_system|indeterminate`, with validated IDs, one logical result per scoped operation/payload, and one winner for one available seat. The shared suite covers initial reserve, repeat same operation, conflicting operation reuse, absent seat, invalid IDs, independent seats/shows/tenants, release policy if any, and stable error mapping.

Run concurrent barriers with many contenders and assert exactly one reservation. For SQL, test real supported engines/isolation, unique constraints, deadlock/serialization retry, transaction rollback, connection loss before/after commit, pool exhaustion, migration compatibility, and restart. For memory, synchronize the state and inject failures, but do not claim it models database uncertainty. Both pass semantic cases; mechanism-specific suites establish their different operational behavior. Record p95/p99 and resource bounds under representative distributions.

### Answer 4

Characterize current use cases and tests first. Extract domain decisions from controllers into application operations using owned request/value/outcome types. Keep old controllers as driving adapters that translate and delegate. Move ORM annotations/entities behind persistence mapping; introduce capability-specific repository ports owned by the application, then implement them with existing ORM code.

Replace service-locator calls one boundary at a time with explicit constructor dependencies wired at the composition root. Add architecture rules forbidding domain imports of web/ORM/container/provider packages and prevent regressions before migrating everything. Shared contract tests protect repository semantics; integration tests retain real transaction behavior. Migrate vertical use cases in small coherent commits, measure behavior/latency, and keep rollback. Do not create interfaces for pure internals or rewrite the whole system solely for a target directory diagram.

### Answer 5

Define driving ports by operator/supervisory goals with authenticated identity, asset/topology version, command, preconditions, deadline, and explicit accepted/confirmed/rejected/indeterminate states. Domain/application code owns operating-mode, authority, interlock, sequence, and reconciliation semantics. Driven ports represent trusted state acquisition, command channel, confirmation, durable audit, and clock; adapters expose real timing and failure guarantees rather than generic `send` success.

Independent controller/hardware interlocks and safe-state behavior remain outside application adapters. Do not retry indeterminate actuation unless the validated device protocol provides authenticated sequence/idempotency and state reconciliation. Evidence requires requirements/hazard traceability, formal/state/timing analysis where appropriate, independent control and protocol review, static analysis, simulator and hardware-in-the-loop tests, loss/duplicate/reorder/delay/partition/restart/power fault injection, security threat testing, operator/human-factors exercises, and controlled deployment/recovery. Named domain/process, controls, real-time, functional-safety, hardware, cybersecurity, quality, regulatory, operations, and independent verification authorities approve. This chapter establishes no functional safety or deployment suitability.
