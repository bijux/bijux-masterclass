---
module_id: SEPAT-025
program: Software Engineering: Patterns
level: 1
module_number: 25
title: Facade
status: complete
last_verified: 2026-08-28
---

# Facade

## One-Page Review

### Governing question

How can a subsystem expose a small, stable, task-oriented entry point without hiding essential failure states, concentrating domain authority, or making the underlying components impossible to evolve and use directly?

### Essential definitions

- A **facade** is a higher-level interface that makes a subsystem easier to use for a defined client task.
- The **subsystem** is the set of components and collaborations behind the facade.
- A **task-oriented operation** represents a client goal rather than leaking the subsystem's call sequence.
- A **boundary contract** specifies inputs, outputs, errors, side effects, consistency, deadlines, cancellation, authorization, compatibility, and observability.
- **orchestration** coordinates participants while leaving their owned domain rules with those participants.
- A **bypass policy** states which clients may use lower-level interfaces and which invariants they must preserve.
- A **god facade** accumulates unrelated responsibilities, policy, and state until it becomes the subsystem's new monolith.
- A **remote facade** is deliberately coarse-grained to reduce costly cross-process calls; it is not merely an in-process facade exposed over a network.
- **compensation** is a domain action that semantically amends an earlier committed action; it is not physical rollback.
- An **outcome model** makes success, rejection, partial progress, compensation, and indeterminate state explicit.

### Central model, mechanism, or theorem

Let a client goal (g) require a protocol over subsystem operations (s_1,\ldots,s_n). A facade defines

$$
F(g,c): Context\times Input\to Outcome(Output,State,Error)
$$

and owns the protocol's ordering, translation, deadline allocation, and progress reporting. It must not falsely strengthen the guarantees of its participants. If participant (s_i) can commit before (s_{i+1}) fails, the facade cannot honestly advertise atomic rollback without a mechanism that supplies it. A good facade reduces client-visible coupling while keeping ownership, failure, and bypass rules explicit.

### Critical invariants

- Every operation corresponds to a cohesive client goal and has a documented boundary contract.
- The facade preserves participant preconditions and never invents stronger atomicity, durability, or safety guarantees.
- Domain rules remain with their owning model or service; orchestration does not hollow out the domain.
- Identity, authorization, tenant, trace, deadline, cancellation, idempotency, and locale context cross the boundary correctly.
- Partial progress, compensation, and indeterminate outcomes are durable and observable when effects span authorities.
- Error translation is stable and retains actionable cause without exposing secrets or implementation detail.
- Direct subsystem access is either prohibited by enforceable boundaries or governed by an explicit bypass contract.
- Facade size, dependency fan-out, latency, and change frequency are measured so simplification does not become centralization.

### Common failures

Common failures include exposing a bag of thin pass-through methods, moving all domain logic into one service, claiming distributed atomicity, using one timeout independently for every call, retrying non-idempotent work after an unknown result, swallowing causes into `operation failed`, returning internal entities as public contracts, bypassing authorization through lower-level APIs, sharing mutable request state, creating cycles between facades, letting every client add bespoke methods, coupling one release to many teams, and measuring only facade success while ignoring participant attempts and compensation.

### Compact example

A checkout facade accepts one purchase goal, validates it, reserves stock, charges once under an idempotency key, and dispatches. If dispatch rejects, it issues domain compensations for charge and reservation and returns `compensated`, not `rolled_back`. Repeating a completed order returns its stored outcome without consuming stock or charging again.

### Connections

[SEPAT-024](024-decorator.md) adds responsibilities around one component; Facade defines a simpler entry to several collaborators. [SEPAT-026](../ROADMAP.md) shares representation state, and [SEPAT-029](../ROADMAP.md) places application ports around domain logic. Facade also connects to [Software Architecture](../../12-software-engineering-software-architecture/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md).

## Governing Question

Which client goal deserves a stable subsystem entry point, and what must the boundary reveal so that convenience does not become a lie about ownership, failure, or consistency?

Facade is not “one class in front of many classes.” It is a deliberate contract that compresses a recurring interaction while preserving the facts clients need to act correctly. Its quality depends more on semantic honesty than method count.

## Why This Matters

Without a facade, clients learn subsystem topology, call order, conversions, recovery, and policy. That knowledge multiplies across callers and makes internal evolution expensive. A task-oriented boundary concentrates protocol knowledge once.

Concentration also creates risk. The facade can become a high-fan-out release bottleneck, accidental domain model, security choke point, and misleading promise of atomicity. Production design therefore treats the facade as an owned boundary with compatibility, failure, and operability obligations.

## Prerequisites and Retrieval

You should understand interfaces, dependency direction, domain services, transactions, idempotency, retries, authorization, deadlines, and distributed failure. Retrieve these facts:

1. Information hiding reduces what clients must know; it does not erase subsystem complexity.
2. A sequence of local commits is not one atomic distributed transaction.
3. An indeterminate response does not reveal whether a side effect occurred.
4. A deadline is an absolute operation budget; nested full timeouts can exceed it.
5. HTTP safety and idempotency are method semantics, not guesses based on endpoint names.
6. Translation at a boundary must preserve information needed for diagnosis and recovery.

## Learning Objectives

After completing this module, you should be able to:

- identify a cohesive client goal that merits a facade;
- design a small boundary contract with explicit outcomes and context;
- separate orchestration from domain policy and infrastructure mechanics;
- reason about partial progress, compensation, retry, and idempotency;
- define enforceable bypass and dependency-direction rules;
- distinguish Facade from Adapter, Gateway, Service Layer, API Gateway, and Mediator;
- test contract, interactions, failure matrix, compatibility, and observability;
- detect and split a facade that has become a change bottleneck.

## Core Exposition

### Start from a client goal

Observe repeated client protocols: `validate → reserve → charge → dispatch`, or `load → compile → link → run`. Name the goal in domain language. Do not begin by mirroring every subsystem method.

The facade may expose several cohesive operations, but each should be independently meaningful. A large “manager” with unrelated administration, reporting, configuration, and workflow methods is a warning.

### Write the boundary contract first

Specify accepted data, validation ownership, outcome variants, externally visible side effects, consistency point, idempotency scope, deadline/cancellation, authorization subject, versioning, and telemetry. Make illegal or indeterminate states representable when clients must react to them.

Return stable boundary values, not internal mutable entities. A snapshot or DTO can decouple representation, but unnecessary copying and mapping also carry cost.

### Keep orchestration thin and domain behavior rich

The facade chooses participants, orders calls, supplies operation context, and translates outcomes. Inventory decides whether stock may be reserved; payments decide charge rules; a domain aggregate decides its invariants.

If every business rule migrates into facade conditionals, lower-level objects become anemic data holders and alternative workflows cannot reuse the rules safely. “Thin” means no stolen authority, not no meaningful coordination.

### Respect real consistency boundaries

Inside one database transaction, the facade may rely on atomic commit if the repository contract actually provides it. Across databases, services, devices, or queues, record progress durably and use idempotent steps, reconciliation, or compensating actions.

Compensation can fail and can differ from inversion: refunding a payment does not erase fees, exchange-rate movement, notification, or observed history. Return states such as `accepted`, `rejected`, `compensating`, `compensated`, and `indeterminate` as the domain requires.

### Make repeated requests safe by design

An idempotency key identifies one logical command within a declared caller/tenant, operation, payload-digest, and retention scope. Store enough outcome and progress to distinguish replay from conflicting reuse.

Do not infer that every facade operation is retryable. RFC 9110 distinguishes HTTP method idempotency and cautions against automatic retry of non-idempotent requests without knowledge that repetition is safe or that the original was not applied.

### Propagate one operation context

Carry principal, tenant, authorization evidence, trace, locale, idempotency key, absolute deadline, and cancellation as explicit or language-standard context. Derive remaining time for each participant.

Never widen authority at the facade. Perform coarse authorization at entry and preserve fine-grained checks where resources are owned. Redact telemetry and errors at the boundary.

### Translate without destroying evidence

Map volatile implementation errors into stable boundary categories: invalid request, forbidden, conflict, unavailable, deadline exceeded, partial, or indeterminate. Preserve cause and correlation internally, and document which failures clients may retry.

Avoid catching all failures and returning false success. Cleanup or telemetry failure must not silently replace the primary failure; simultaneous failures need an explicit reporting rule.

### Decide bypass policy

GoF Facade does not inherently prevent knowledgeable clients from using subsystem classes. That can preserve advanced capabilities. In a security or integrity boundary, however, casual bypass can violate invariants.

Enforce intended access using package/module visibility, dependency rules, ports, capability-bearing references, or deployment/network policy. Document privileged bypasses, audit them, and test that ordinary clients cannot import or call internals.

### Design for evolution

Add operations for stable client goals, not each caller's screen shape. Preserve semantic compatibility: widening a timeout or adding an optional field can still change resource consumption, ordering, or security.

Version at the boundary only when compatibility cannot be maintained. Use consumer contract tests and deprecation telemetry. Do not keep contradictory legacy behavior forever inside one method.

### Operate the boundary

Trace one logical facade operation and separate participant attempts. Record outcome class, latency budget consumption, retry/compensation counts, and bounded subsystem identifiers. Never attach secrets or high-cardinality raw payloads.

Expose progress for long workflows. Operators need to answer which step committed, which compensation ran, whether replay is safe, and who owns intervention.

### Prevent the god facade

Watch dependency fan-out, method count, unrelated reasons to change, owner count, compile/deploy blast radius, and tail latency. Split by cohesive capability or bounded context when these signals diverge.

Do not create chains or cycles of facades solely to hide poor boundaries. A useful facade simplifies a stable collaboration; it does not make arbitrary architecture simple.

## Definitions and Notation

Let (S=\{s_1,\ldots,s_n\}) be subsystem operations and (g) a client goal. A facade protocol is a state machine (P_g=(Q,q_0,\delta,T)), where (Q) is durable progress state, (q_0) is the initial state, (\delta) selects a participant action and transition from context plus outcome, and (T) contains terminal outcomes.

Let (D) be an absolute deadline. Before step (i), remaining budget is (r_i=\max(0,D-t_i)). A correct facade passes a budget no greater than (r_i); it does not grant each step the original duration.

For idempotency key (k), operation (o), scope (a), and payload digest (h(x)), define identity (I=(a,o,k,h(x))). Reuse with the same tuple returns or resumes the same logical result; reuse with the same ((a,o,k)) but different digest is a conflict.

If completed effect (e_i) has compensation (c_i), (c_i(e_i(state))) need not equal `state`. Compensation is semantic repair under declared postconditions, not algebraic inverse or deletion of history.

## Mechanisms, Invariants, or Proof Structure

### Derive an operation

1. Name one client goal and its owner.
2. Trace the current successful and failing protocols.
3. Assign each rule and side effect to an authoritative participant.
4. Define boundary inputs, outcomes, context, and compatibility.
5. Model progress and recovery for every effect boundary.
6. Define retry/idempotency and absolute deadline behavior.
7. Establish bypass and dependency-direction enforcement.
8. Add contract, interaction, fault, and observability tests.
9. Measure coupling and operate the realized workflow.

### Executable mechanism

The following in-memory example demonstrates task-oriented orchestration, one idempotent result, and explicit compensation. It does not model durable storage, concurrency, crash recovery, payment regulation, or distributed atomicity.

<!-- bijux-verify: {"id":"facade-checkout-outcomes","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"first=accepted stock=3 active=2500\nreplay=accepted stock=3 active=2500\nfailed=compensated stock=3 active=2500\n","stderr":""}} -->
```python
class Inventory:
    def __init__(self, available):
        self.available = available
        self.reserved = {}

    def reserve(self, order_id, quantity):
        if quantity <= 0 or quantity > self.available:
            return False
        self.available -= quantity
        self.reserved[order_id] = quantity
        return True

    def release(self, order_id):
        quantity = self.reserved.pop(order_id, 0)
        self.available += quantity


class Payments:
    def __init__(self):
        self.charges = {}

    def charge(self, order_id, cents):
        if cents <= 0:
            return False
        self.charges[order_id] = cents
        return True

    def refund(self, order_id):
        self.charges.pop(order_id, None)

    def active_total(self):
        return sum(self.charges.values())


class Dispatch:
    def accept(self, order_id, accepted):
        return accepted


class CheckoutFacade:
    def __init__(self, inventory, payments, dispatch):
        self.inventory = inventory
        self.payments = payments
        self.dispatch = dispatch
        self.outcomes = {}

    def place(self, order_id, quantity, cents, dispatch_accepted):
        previous = self.outcomes.get(order_id)
        if previous is not None:
            return previous
        if not self.inventory.reserve(order_id, quantity):
            return "rejected"
        if not self.payments.charge(order_id, cents):
            self.inventory.release(order_id)
            return "compensated"
        if not self.dispatch.accept(order_id, dispatch_accepted):
            self.payments.refund(order_id)
            self.inventory.release(order_id)
            return "compensated"
        self.outcomes[order_id] = "accepted"
        return "accepted"


inventory = Inventory(5)
payments = Payments()
checkout = CheckoutFacade(inventory, payments, Dispatch())

first = checkout.place("order-1", 2, 2500, True)
print("first=" + first + " stock=" + str(inventory.available) + " active=" + str(payments.active_total()))
replay = checkout.place("order-1", 2, 2500, True)
print("replay=" + replay + " stock=" + str(inventory.available) + " active=" + str(payments.active_total()))
failed = checkout.place("order-2", 1, 900, False)
print("failed=" + failed + " stock=" + str(inventory.available) + " active=" + str(payments.active_total()))
```

The replay leaves stock and charge unchanged. The failed dispatch is labeled compensated. A production workflow must durably store intent and progress before effects, bind payload digest to the key, handle concurrent duplicates, make compensations idempotent, and represent crashes or compensation failure.

### Proof obligations

For a local facade, verify that every accepted input follows an allowed transition, every terminal result satisfies its postcondition, forbidden imports are impossible, and error translation is total. For a distributed workflow, prove only properties supplied by durable protocols and participant contracts.

The example's finite sequential trace establishes only its printed state. It does not prove atomicity under crashes, isolation under concurrency, or exact-once external effects.

## Alternatives and Trade-Offs

| Approach | Primary intent | Strength | Main risk |
|---|---|---|---|
| Facade | simplify a subsystem for client goals | reduces client coupling | god facade or hidden failures |
| Adapter | translate one incompatible contract | isolates representation/protocol mismatch | semantic loss |
| Gateway | encapsulate an external resource/system | localizes integration concerns | vendor semantics leak |
| Service Layer | define an application's use-case boundary | coordinates application response | anemic domain model |
| Remote Facade | coarse boundary across a network | reduces chatty remote calls | oversized payloads and coupling |
| API Gateway | route/policy/aggregation at a deployment edge | cross-service entry and policy | distributed bottleneck |
| Mediator | coordinate peer interactions | reduces peer-to-peer dependencies | centralized behavioral complexity |
| Direct subsystem API | retain full capability | no additional abstraction | clients duplicate protocol knowledge |

A facade can coexist with these patterns. Name the boundary by its actual responsibility rather than treating every public service as a facade.

## Failure Modes and Misconceptions

### “A facade must forbid direct access”

Classic Facade simplifies access but does not inherently make subsystem classes private. Restriction is a separate architectural and security decision that must be enforced.

### “A facade is only forwarding”

Pure forwarding adds little. A facade earns its existence by representing a cohesive goal, coordinating a protocol, or stabilizing translation—without stealing domain rules.

### “One method makes the work atomic”

Call shape does not change transaction physics. Distributed effects require durable progress, idempotency, compensation/reconciliation, and explicit uncertain states.

### “Compensation is rollback”

External observers, fees, messages, and irreversible physical actions may remain. Compensation establishes a declared acceptable state and preserves history.

### “The facade should catch everything”

Stable translation is valuable; information destruction is not. Preserve causes and distinguish rejection, retryable unavailability, partial completion, and indeterminate result.

### “All clients need one universal facade”

Different goals and bounded contexts can justify different facades. A universal surface often centralizes unrelated change and weakens language.

### “Testing the happy path is sufficient”

The critical behavior lies at every failure boundary, replay, deadline, cancellation, compensation, duplicate request, and version transition.

## Worked Examples

### Example 1

A compiler client repeatedly creates scanner, parser, semantic analyzer, optimizer, and emitter in a fixed sequence. A `compile(source, target, options)` facade owns orchestration while diagnostic objects retain phase and source locations. **Conclusion:** Simplification should preserve actionable detail.

### Example 2

A reporting facade mirrors 42 repository methods one-for-one. Clients still know tables and join order. Replacing it with `quarterly_tax_summary(account, period)` plus a stable result removes protocol knowledge. **Conclusion:** Method count is not the measure; goal-level compression is.

### Example 3

A checkout reserves stock and charges, then dispatch fails. It records `compensating`; refund succeeds, release fails, so it remains nonterminal for reconciliation. **Conclusion:** Compensation needs durable progress and can itself fail.

### Example 4

A facade grants each of four calls a 500 ms timeout although the user deadline is 700 ms. It can run for two seconds. Passing the absolute deadline and allocating remaining budget preserves the operation limit. **Conclusion:** Nested timeouts must not reset the clock.

### Example 5

Two concurrent requests reuse one key with different payloads. The facade compares payload digests and returns conflict rather than replaying the first result. **Conclusion:** An idempotency key needs caller, operation, payload, and retention scope.

### Example 6

A facade returns `not found` for both missing and forbidden records to limit enumeration, while internal audit retains the authorization decision and correlation. **Conclusion:** Boundary translation can protect information without erasing operational evidence.

### Example 7

An advanced analytics client bypasses a facade to query subsystem objects. Package rules allow it only through a read-only capability and contract tests verify the same tenant filter. **Conclusion:** Bypass is a governed contract, not an accidental import.

### Example 8

A remote facade replaces 120 fine-grained calls with one coarse request, but its 20 MB response increases tail latency and compatibility cost. Pagination and goal-specific projections restore bounded transfer. **Conclusion:** Coarse-grained does not mean unbounded.

### Example 9

One facade has 68 dependencies, eight owners, and weekly conflicting releases. It is split by bounded capabilities; shared rules move into owned domain services, not copied facades. **Conclusion:** Organizational and change coupling reveal a god facade.

### Example 10

An emergency-stop facade coordinates software validation, authorization, logging, and a device command. It exposes `accepted`, `confirmed`, and `indeterminate`, never retries an uncertain actuation automatically, and preserves independent hardware safety. **Conclusion:** A simple API cannot create physical safety guarantees.

## Cross-Program Connections

- **Software Design and Domain Modeling:** use-case language, aggregates, services, and bounded contexts decide facade cohesion.
- **Software Architecture:** information hiding, dependency direction, modularity, and deployment boundaries constrain access.
- **Testing and Quality Engineering:** consumer contracts, interaction traces, fault injection, and model-based tests verify boundaries.
- **Delivery and Reliability:** progressive rollout, reconciliation, operability, and rollback/roll-forward support workflows.
- **Database Engineering:** local atomicity, isolation, outbox/inbox records, and durable idempotency underpin guarantees.
- **Security Engineering:** entry authorization, resource checks, capability access, redaction, and audit must align.
- **Distributed Systems Engineering:** partial failure, retries, deadlines, sagas, duplicate delivery, and uncertainty are central.
- **API and Service Engineering:** coarse contracts, HTTP semantics, compatibility, pagination, and error models shape remote facades.
- **Platform Engineering:** platform facades can reduce cognitive load but can also become bottlenecks or lowest-common-denominator APIs.
- **Systems Engineering:** physical effects, hazard controls, authority, and human intervention limit abstraction promises.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Facade intent, applicability, structure, and consequences.
2. Martin Fowler, [*Patterns of Enterprise Application Architecture* catalog](https://martinfowler.com/eaaCatalog/), 2003, site refreshed 2024. Defines Service Layer, Remote Facade, Gateway, and related boundary patterns.
3. Martin Fowler, [“Gateway”](https://martinfowler.com/articles/gateway-pattern.html), 2021, accessed 2026-08-28. Distinguishes a client-written external-system gateway from a provider-oriented facade.
4. Eric Evans, [*Domain-Driven Design: Tackling Complexity in the Heart of Software*](https://www.informit.com/store/domain-driven-design-tackling-complexity-in-the-heart-9780321125217), Addison-Wesley, 2003. Provides application-layer, domain-service, bounded-context, and model-ownership foundations.
5. Hector Garcia-Molina and Kenneth Salem, [“Sagas”](https://www.cs.cornell.edu/andru/cs711/2002fa/reading/sagas.pdf), *Proceedings of ACM SIGMOD*, 1987. Introduces long-lived transactions composed with compensating transactions.
6. R. Fielding, M. Nottingham, and J. Reschke, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), IETF Standards Track, June 2022. Defines safety, idempotency, method semantics, and automatic-retry constraints.
7. OpenTelemetry, [Context specification](https://opentelemetry.io/docs/specs/otel/context/), accessed 2026-08-28. Defines propagation of execution-scoped values across API boundaries and associated execution units.

## Exercises

### Exercise 1

For the executable facade, trace success, replay, and dispatch rejection. State exactly what is established and list the crash/concurrency cases that remain unproved.

### Exercise 2

Design a facade contract for document publication across validation, storage, indexing, and notification. Specify outcomes, idempotency, deadline, compensation, and error ownership.

### Exercise 3

Design an architecture test and runtime audit for bypass policy around a billing subsystem, including privileged read-only analytics access.

### Exercise 4

A 70-method facade has 55 dependencies and six owners. Produce a decomposition proposal and migration plan that avoids duplicating domain rules or breaking clients.

### Exercise 5

Review a proposed emergency-control facade for an unfamiliar industrial plant. Give a rigorous boundary and evidence plan without claiming safety or regulatory suitability.

## Answers to the Exercises

### Answer 1

Success starts with stock 5, reserves 2 to reach 3, charges 2,500, accepts dispatch, and stores `accepted`. Replay finds that stored result before participants, so stock remains 3 and active charge remains 2,500. The second order reserves one to reach 2 and charges 900; dispatch rejects, refund removes 900 and release restores stock to 3, yielding `compensated`.

This establishes only the deterministic sequential trace and printed values. It does not establish atomic persistence, concurrent duplicate exclusion, payload/key conflict detection, crash recovery between any two statements, durable dispatch knowledge, compensation retry, compensation failure, timeout/cancellation behavior, exactly-once charging, security, or accounting correctness. A production implementation needs durable state transitions and participant contracts for each claim.

### Answer 2

Define `publish(command, context) -> Published(version, locations) | Rejected(reasons) | InProgress(operation_id) | Compensating(operation_id) | Compensated(details) | Indeterminate(operation_id)`. Bind the idempotency identity to tenant, publication operation, key, document/version digest, and retention. Validate authorization/schema/domain rules before irreversible work, then durably record intent.

Within one storage authority, commit canonical content and an outbox record atomically if supported. Indexing and notification consume idempotent messages; neither defines publication truth. A failed index is retryable/reconcilable rather than grounds to delete accepted canonical content unless policy explicitly requires compensation. Notification is usually best effort with durable retry. Pass one absolute deadline and preserve cancellation only until the acceptance point; after acceptance, background completion continues with queryable progress. Storage owns version conflicts/durability, index owns search freshness, notification owns delivery, and facade owns outcome translation/progress. Tests inject failure before and after every durable transition, duplicate messages, stale versions, deadline, and restart.

### Answer 3

Place billing internals in a module/package not exported to ordinary clients. Export a command facade and a separate read-only analytics port whose types cannot express charge, refund, or mutation. Static architecture tests reject dependencies from client packages to internal repositories, provider SDKs, tables, and mutable entities. Build configuration fails on forbidden edges; deployment policy prevents direct database credentials for clients.

Runtime authorization gives analytics a least-privilege capability scoped by tenant, approved fields, purpose, and time. The port enforces row/tenant filtering and redaction even if callers already checked. Audit records actor, purpose, query class, result count, policy version, and correlation without sensitive values. Contract tests compare facade and analytics tenant isolation; adversarial tests try reflection/dynamic loading, alternate credentials, stale replicas, bulk extraction, and confused-deputy paths. Exceptions require named owner, expiry, compensating controls, and review.

### Answer 4

Cluster methods by client goal, bounded context vocabulary, authoritative data, dependencies, owner, transaction boundary, and change history. Likely targets might be ordering, fulfillment, billing, account administration, and reporting facades. Shared business rules move to explicitly owned aggregates/domain services used by those facades; provider integration stays behind gateways. Do not make a “common facade” or copy validation.

Characterize current contracts and telemetry first. Add consumer contract tests and dependency/fan-out fitness functions. Introduce cohesive new facades behind the old boundary; the old facade delegates without changing semantics. Migrate consumers goal by goal with deprecation metrics and compatible outcome mapping. Prevent new calls to deprecated methods, compare shadow results for read paths, progressively route traffic, and retain rollback. Remove old methods only after named consumers migrate and the compatibility window closes. Track dependency count, owner count, build/release coupling, latency, failure isolation, and domain-rule duplication.

### Answer 5

Define the physical goal, plant modes, equipment identity, authority hierarchy, preconditions/interlocks, accepted/confirmed/failed/indeterminate outcomes, deadline, cancellation point, and manual recovery before choosing an interface. The facade may coordinate authenticated request validation, policy decision, redundant command channels, confirmation, and audit, but device/controllers retain independent safety interlocks and safe-state logic. Do not automatically retry an indeterminate physical action unless the validated protocol supplies authenticated sequence/idempotency and state reconciliation.

Model hazards including wrong asset, stale topology, conflicting commands, replay, partial actuation, communication loss, clock failure, power loss, sensor disagreement, operator override, facade unavailability, and common-mode failure. Evidence requires traceable safety requirements/hazard analysis, formal or model checking where appropriate, timing and fail-safe analysis, independent authorization/threat review, static analysis, simulator/digital-twin and hardware-in-the-loop tests, duplicate/loss/delay/reorder/partition/restart faults, disaster exercises, audit integrity, human-factors validation, and controlled deployment/rollback. Named process/control, functional-safety, domain operations, cybersecurity, human-factors, quality, regulatory, reliability, and independent verification authorities must approve. This software-pattern chapter establishes no plant safety or regulatory fitness.
