---
module_id: SEPAT-035
program: Software Engineering: Patterns
level: 1
module_number: 35
title: Mediator
status: complete
last_verified: 2026-08-28
---

# Mediator

## One-Page Review

### Governing question

How can interaction policy among a cohesive set of objects be owned explicitly so colleagues remain independently understandable, without merely moving all coupling, authority, and failure into a god object?

### Essential definitions

- A **mediator** owns a collaboration protocol among named **colleagues**.
- A **colleague** publishes an intent or fact to the mediator and receives only the commands/state it is responsible for.
- **interaction topology** identifies who may communicate directly; **semantic coupling** identifies whose meaning must be understood. A star topology reduces pairwise links but does not erase semantic dependence.
- A **command** requests an action and may be rejected; an **event** reports a fact; a **query** asks for state without intentional domain mutation.
- **orchestration** centrally directs a multi-step process; **choreography** lets participants react to facts without one controller.
- A **reentrancy** occurs when a mediator-triggered colleague action synchronously calls back into the mediator before the outer transition finishes.
- A **broker** transports/routes messages; a **workflow engine** durably manages long-running state. Neither is automatically a domain mediator.

### Central model, mechanism, or theorem

For mediator state (m), colleague input (i), trusted context (ctx), define one transition

\[
\delta:(m,i,ctx)\rightarrow(m',O),
\]

where (O=[o_1,...,o_k]) is an explicitly ordered set of colleague commands and/or domain facts. Direct undirected acquaintance among (n) colleagues can require up to (n(n-1)/2) links; a mediator topology needs (n) colleague-to-mediator links. This graph result concerns communication structure only: the mediator now owns cross-colleague rules, ordering, and failure policy.

### Critical invariants

- The mediator has one cohesive collaboration purpose and does not absorb unrelated domain, transport, persistence, or presentation responsibilities.
- Colleagues do not bypass the mediator for interactions whose invariant it owns.
- Inputs are typed/versioned and distinguish commands, events, queries, identities, and trusted context.
- One transition validates current authority/preconditions before emitting effects and either establishes atomicity or documents partial failure/reconciliation.
- Reentrancy, cycles, ordering, duplicate delivery, concurrency, deadlines, and cancellation have explicit rules.
- Colleague registration/lifetime is owned; stale references and unbounded subscriptions cannot accumulate.
- Failures identify which transition/effects committed, which may retry, and which require compensation or repair.
- Observability preserves correlation and bounded state transitions without leaking sensitive colleague payloads.

### Common failures

Common failures include a `notify(any, string)` switch, a mediator that knows every field and service, hidden global singleton access, colleagues that sometimes bypass it, confusing events with commands, forwarding mutable objects, trusting caller-supplied roles, synchronous callback loops, holding locks while invoking colleagues, nondeterministic handler order, swallowing colleague failure, retrying non-idempotent effects, using an in-memory mediator as a distributed transaction, unbounded queues, central hot spots, stale registrations, schema drift, logging secrets, and tests that mock every colleague but never verify the collaboration invariant.

### Compact example

A registration mediator alone decides whether Submit is enabled: the normalized name must be nonempty and terms accepted. Name and terms colleagues report changes; the mediator recomputes and commands the button. Three transitions move disabled → disabled → enabled → disabled without colleagues knowing each other.

### Connections

[SEPAT-034](034-iterator.md) separates traversal state from aggregates; [SEPAT-036](../ROADMAP.md) captures state for restoration. Mediator connects to [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md), and [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

Which cross-object interaction rules form one coherent policy, who owns their state and ordering, and where must direct collaboration remain visible rather than routed through a universal hub?

Mediator is useful when peers become entangled because each needs to coordinate several others. The pattern succeeds only when the central object has a durable domain or presentation responsibility, not “all messages pass here.”

## Why This Matters

Dialog controls, air-traffic sectors, game rooms, scheduling subsystems, transaction coordinators, and application use cases contain interactions that do not belong inside any one participant. A mediator can make the collaboration a named, testable unit.

Centralization also creates a dependency and failure concentration. In a process, this may become a god object and reentrancy trap. Across services, it becomes a protocol with persistence, concurrency, security, retry, and availability requirements. The pattern name supplies none of those mechanisms.

## Prerequisites and Retrieval

You should understand encapsulation, dependency graphs, commands/events, state machines, transactions, concurrency, queues, idempotency, authorization, and failure recovery. Retrieve these facts:

1. Reducing edges in a graph does not reduce the amount of domain knowledge automatically.
2. A fact that already occurred cannot be rejected like a command asking for an action.
3. Synchronous callbacks can re-enter shared mutable state before invariants are restored.
4. A local call stack and a distributed message flow have different atomicity and failure models.
5. Authorization is checked at the action-owning boundary using trusted current context.
6. Centralized coordination needs explicit ownership, capacity, partitioning, recovery, and observability.

## Learning Objectives

After completing this module, you should be able to:

- recognize a cohesive collaboration that merits a mediator;
- distinguish topology reduction from semantic coupling;
- model typed transitions, outputs, and collaboration invariants;
- separate mediator, facade, controller, broker, event bus, and workflow engine;
- control reentrancy, cycles, ordering, concurrency, and mutation;
- design local and durable distributed failure semantics honestly;
- partition, secure, observe, evolve, and test a mediator;
- detect and decompose a mediator that has become a god object.

## Core Exposition

### Start with a collaboration, not a class name

Identify an invariant involving several colleagues: a form's submit eligibility, a room's membership and message policy, or a bounded scheduling decision. Name the mediator after that responsibility—`RegistrationInteraction`, `RoomCoordinator`, or `DispatchScheduler`—rather than `GlobalMediator`.

If two objects naturally form one aggregate and can call directly without creating cycles, a mediator may add indirection. If the “collaboration” spans unrelated business areas, first find domain boundaries instead of centralizing everything.

### Reduce acquaintance deliberately

Without a mediator, each colleague may know several peers and encode fragments of the same rule. With a mediator, colleagues know one interface and the mediator knows their roles. This makes interaction changes local when the rule changes more often than colleague internals.

But semantic coupling moves: the mediator must understand the collaboration vocabulary. Keep colleague interfaces narrow and role-based so it does not depend on every implementation detail.

### Define typed inputs and outputs

Avoid string topics and unstructured payloads. Inputs should identify sender role, message type/version, immutable owned data, trusted context reference, correlation, and expected state where relevant.

Separate facts such as `NameChanged` from requests such as `EnableSubmit`. A UI colleague may report a local fact; the mediator evaluates policy and sends a command to the button. In a domain system, events should be named in past tense and commands by intent.

### Own collaboration state explicitly

Mediator state might include current normalized fields, membership, workflow position, outstanding correlation, or per-key sequence. Define its lifecycle and persistence. Derived state should be recomputable from authoritative inputs when practical.

Do not let the mediator reach into arbitrary colleague fields. Colleagues report relevant changes or the mediator queries an explicit read interface at a defined point; otherwise ownership and test boundaries dissolve.

### Specify one transition boundary

For each input, declare validation, state read, state transition, outputs, and failure. In a local UI mediator, updating state and computing commands can be one synchronous transition. Invoke external callbacks only after internal invariants are restored.

If state and durable output must agree, use one database transaction with an outbox or a documented reconciliation protocol. A mediator object cannot make calls to independent databases atomically.

### Control reentrancy and feedback loops

Suppose the mediator commands a text field to normalize its value; that field emits `Changed`, which re-enters the mediator. The result may be recursion, duplicate work, or observation of half-updated state.

Options include making commands idempotent, suppressing notifications for programmatic updates under a documented rule, comparing old/new state, queuing inputs until the current transition ends, and attaching causation IDs/hop budgets. Do not use a global “busy” flag that silently drops legitimate inputs.

### Define ordering and concurrency

A local mediator may serialize transitions on one event loop. A multithreaded mediator can use ownership confinement, a lock around state (without calling unknown code while held), or immutable state with compare-and-swap/version checks.

Distributed inputs can duplicate, reorder, and race. Define the narrow ordering key—form, room, aggregate, workflow—and expected sequence/version. Do not promise global order when partitioned processing provides only per-key order.

### Model failure, retry, and cancellation

In-process calls can throw after earlier colleagues have changed. Prefer computing a plan first and applying only reversible local changes, or define rollback/compensation. Never swallow exceptions and leave the collaboration silently inconsistent.

Across processes, persist mediator/workflow state and step identity. Retry only idempotent or effect-queryable operations with one retry owner, bounded attempts/backoff/deadline, and stable command IDs. After an indeterminate external effect, reconcile rather than blindly repeat.

Cancellation is another transition that can race with completion. Define `requested`, `accepted`, `executing`, `committed`, `completed`, `cancelled`, and `too_late` only as mechanisms support them.

### Preserve authority boundaries

The mediator may decide coordination, but each resource owner still enforces authorization and invariants. Derive tenant/actor from trusted transport/session context; do not accept a payload role as authority.

Minimize data passed between colleagues. Avoid broadcasting secrets because routing is convenient. Redact logs and traces, restrict subscriptions/registration, and validate message size, depth, type/version, and origin.

### Distinguish nearby patterns

A **Facade** offers a simpler entry point to a subsystem; it need not coordinate peers bidirectionally. A **Controller** accepts external input and invokes application behavior; it may delegate collaboration to a mediator. An **Observer/event bus** broadcasts facts to interested listeners without necessarily owning their combined invariant.

A **message broker** routes/transforms messages and owns delivery mechanics. A **workflow/orchestrator** is a durable mediator for long-running steps when it explicitly owns state, timeouts, retry, and recovery. An **actor** owns state and processes messages, but a mediator is about the collaboration role, not the concurrency primitive.

### Avoid the god mediator

Warning signs include hundreds of message types, unrelated state, direct database/network/UI access, generic lookup of colleagues, cross-domain routing, frequent conflicts, and inability to test one rule without the world.

Split by cohesive protocol and partition key. Extract pure policy functions, domain services, repositories, transport adapters, and workflow infrastructure. Colleagues may participate in several small mediators through narrow roles.

### Scale by ownership key

A global mediator is a throughput and availability bottleneck. Many collaborations naturally partition: one form instance, chat room, order, account, device, or workflow. Route each key to one logical owner when serialization is required, and make failover/recovery explicit.

Measure queue depth/age, transition latency, per-key hot spots, retries, cycles suppressed, duplicate/stale inputs, failures by output, reconciliation backlog, and state-store health. Apply quotas and backpressure before memory becomes the queue.

### Evolve protocols safely

Version externally durable message schemas and mediator state. Use allowlisted decoders/upcasters; retain old fixtures and replay tests. A rolling deployment must define how old/new mediators and colleagues coexist and what happens to in-flight correlations.

Do not serialize arbitrary colleague objects or callbacks. Persist owned data and stable identities, and rebuild runtime wiring from controlled configuration.

### Test collaboration behavior

Test the mediator as a state machine: given state/input/context, assert new state and ordered outputs. Use real lightweight fakes that record commands rather than mocks coupled to incidental call structure.

Cover invalid inputs, boundary states, repeated/no-op changes, reentrancy, duplicate/reorder, concurrent versions, colleague exception/timeout, partial output, cancellation, authorization changes, schema/state migration, crash/restart, load/hot keys, and observability redaction. For distributed workflows, fault-inject at every persistence and effect boundary.

## Definitions and Notation

Let colleagues be (C=\{c_1,...,c_n\}). A fully connected undirected acquaintance graph has

\[
|E_{pair}|=\binom{n}{2}=\frac{n(n-1)}{2},
\]

while a star centered at mediator (mu) has (|E_{star}|=n). Directed request/response interfaces may count differently; the comparison illustrates topology, not total semantic complexity.

Let mediator state be (m=(id,v,q)): collaboration identity, version, and owned policy state. Transition (delta(m,i,ctx)=(m',O)), with ordered outputs (O=[o_1,...,o_k]). Safety invariant (P(m)) should satisfy (P(m)\land Valid(i,ctx)\Rightarrow P(m')), under stated assumptions about output application.

For durable output identity (j=(collaboration,version,outputIndex)), duplicate-safe receivers bind (j) to the same payload digest/outcome. This supports retry of one logical output but does not prove exactly-once external effects.

## Mechanisms, Invariants, or Proof Structure

### Mediator design procedure

1. Name one cohesive multi-colleague invariant and its owner.
2. Define colleague roles and forbid bypass for owned interactions.
3. Specify typed/versioned inputs, trusted context, state, and ordered outputs.
4. Establish transition atomicity or explicit partial-failure reconciliation.
5. Define reentrancy, cycles, per-key order, duplicates, concurrency, and cancellation.
6. Protect authority/data and bound registration, queues, work, and retries.
7. Partition by collaboration identity and design persistence/recovery if durable.
8. Test the state machine, wiring, faults, migrations, capacity, and redaction.

### Executable mechanism

This UI example centralizes one submit-eligibility invariant and suppresses redundant output by comparing derived state. It demonstrates deterministic local transitions only; it does not model threads, persistence, authentication, distributed messages, or irreversible effects.

<!-- bijux-verify: {"id":"mediator-registration-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"initial=False\nafter-name=False\nafter-terms=True\nafter-clear=False\ntransitions=3 commands=2\n","stderr":""}} -->
```python
class SubmitButton:
    def __init__(self):
        self.enabled = False
        self.commands = 0

    def apply_enabled(self, enabled):
        if self.enabled != enabled:
            self.enabled = enabled
            self.commands += 1


class RegistrationMediator:
    def __init__(self, button):
        self.button = button
        self.name = ""
        self.terms_accepted = False
        self.transitions = 0

    def notify(self, event, value):
        if event == "name_changed":
            self.name = value.strip()
        elif event == "terms_changed":
            self.terms_accepted = bool(value)
        else:
            raise ValueError("unknown registration event")
        self.transitions += 1
        eligible = bool(self.name) and self.terms_accepted
        self.button.apply_enabled(eligible)


button = SubmitButton()
mediator = RegistrationMediator(button)
print(f"initial={button.enabled}")
mediator.notify("name_changed", " Ada ")
print(f"after-name={button.enabled}")
mediator.notify("terms_changed", True)
print(f"after-terms={button.enabled}")
mediator.notify("name_changed", "   ")
print(f"after-clear={button.enabled}")
print(f"transitions={mediator.transitions} commands={button.commands}")
```

### Local invariant argument

After every successful `notify`, the mediator normalizes exactly one owned input, computes (eligible=(name\ne\epsilon)\land terms), and commands the button only if its state differs. Therefore on return, `button.enabled == eligible`; three transitions yield two actual button changes. The argument assumes no concurrent/reentrant mutation and that `apply_enabled` terminates without failure.

### Distributed review obligations

When boundaries become durable/distributed, separately review state/output atomicity, idempotency, ordering, authorization, timeouts, partial effects, retries, cancellation, schema migration, capacity, failover, and reconciliation. A local invariant proof cannot be lifted across those boundaries without mechanisms and evidence.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or limitation | Prefer when |
|---|---|---|---|
| Direct collaboration | Behavior stays near participants | Pairwise coupling/cycles can grow | Few stable collaborators |
| Mediator | Names and tests cross-object policy | Central semantic/failure concentration | One cohesive interaction changes independently |
| Facade | Simple subsystem entry | Does not own peer conversation | Clients need simplified access |
| Observer/event bus | Extensible fact distribution | Ordering and combined invariants diffuse | Independent reactions to facts |
| Choreography | Local autonomy and loose central control | Global flow/recovery harder to see | Reactions are independent and bounded |
| Durable orchestrator | Explicit long-running state/recovery | Infrastructure and central availability cost | Multi-step work needs timeouts/retry/compensation |
| Message broker | Delivery, routing, buffering | Does not supply domain decisions | Transport concerns dominate |
| Shared state/blackboard | Decoupled producers/consumers | Consistency, polling, ownership ambiguity | Collaboration is data-centric and governed |

## Failure Modes and Misconceptions

- **“Fewer edges means less coupling.”** Direct acquaintance falls, but semantic knowledge and change pressure may concentrate in the mediator.
- **“Everything should communicate through one mediator.”** Scope by one invariant; universal hubs become god objects.
- **“A string topic is decoupled.”** It replaces compiler-checked contracts with runtime ambiguity and schema drift.
- **“Mediator and event bus are synonyms.”** A mediator owns collaboration decisions; a bus primarily transports/distributes.
- **“Centralized means atomic.”** Independent resources require transactions, workflows, compensation, and reconciliation.
- **“Callbacks are sequential, so reentrancy is impossible.”** Synchronous colleague notification can re-enter before the outer call returns.
- **“Failing one output rolls back earlier calls.”** Only an explicit mechanism provides rollback; external effects may be irreversible.
- **“The mediator authorizes everything.”** Resource owners still enforce current policy at action time.
- **“Retrying the transition is safe.”** Only stable identity plus idempotent/effect-queryable outputs makes retry defensible.
- **“One process ordering extends across services.”** Networks introduce duplication, reordering, delay, and partial failure.
- **“The mediator must be a singleton.”** Per-collaboration instances improve isolation, lifecycle, testing, and partitioning.
- **“Mocks prove the protocol.”** State-model, race, crash, migration, security, and load evidence remain necessary.

## Worked Examples

### Example 1

Six peers with all possible undirected direct links have (6\cdot5/2=15) links; a star has six. The mediator still understands all six roles. **Conclusion:** Topology shrinks, while semantic complexity moves rather than vanishes.

### Example 2

A form has name, terms, and button colleagues. Encoding submit rules in all three permits divergence; one registration mediator computes the invariant after every relevant change. **Conclusion:** Centralize one cross-colleague rule, not all widget behavior.

### Example 3

The mediator commands a field to trim text; the field reports another change synchronously. Comparing normalized old/new state and queuing nested inputs prevents infinite recursion without dropping distinct user input. **Conclusion:** Reentrancy needs a protocol, not a busy flag.

### Example 4

A mediator holds its state lock and calls a colleague that calls back to query the mediator, deadlocking. It instead computes an immutable output plan under lock, commits state, releases the lock, then dispatches. **Conclusion:** Do not invoke unknown code while holding internal locks.

### Example 5

A payment-reservation mediator commits inventory, then payment times out after possibly charging. A local exception cannot roll back either external authority; durable step IDs, provider reconciliation, and compensation are required. **Conclusion:** The pattern is not a distributed transaction.

### Example 6

Two duplicate `MemberJoined` inputs arrive for room version 12. Binding transition/output identity to room and expected version prevents duplicate welcome commands; a different payload under the same identity conflicts. **Conclusion:** Durable mediation needs payload-bound idempotency and concurrency control.

### Example 7

A caller claims `role=admin` in a mediator payload. The mediator derives actor/tenant from authenticated context and the document service rechecks permission before mutation. **Conclusion:** Coordination never replaces authority at the resource boundary.

### Example 8

A single global chat mediator receives one celebrity room's traffic and delays every other room. Partitioning by room ID isolates ordering and capacity while cross-room operations use an explicit higher-level protocol. **Conclusion:** Partition by the narrow invariant ownership key.

### Example 9

During rolling deployment, an old colleague emits v1 while a new mediator expects v2. An allowlisted v1 upcaster plus retained fixtures preserves meaning; unknown future versions quarantine rather than guess. **Conclusion:** Message and state evolution are part of mediator correctness.

### Example 10

A clinical alert mediator routes observations, but it lacks validated medical policy, provenance, timing, human workflow, fail-safe behavior, and independent review. Routing tests cannot establish clinical validity. **Conclusion:** High-stakes domain correctness is evidence beyond collaboration structure.

## Cross-Program Connections

- **Object-Oriented Programming:** interfaces, role objects, dependency inversion, and object lifetimes shape colleagues.
- **Software Design and Domain Modeling:** aggregates, application services, domain events, and bounded contexts locate policy ownership.
- **Distributed Systems Engineering:** ordering, idempotency, consensus boundaries, partial failure, and reconciliation constrain remote mediation.
- **Concurrency and Parallelism:** confinement, locks, reentrancy, queues, actors, and partitioning govern transition execution.
- **Cloud and Platform Engineering:** brokers, workflow engines, autoscaling, quotas, and observability support durable coordination.
- **Security Engineering:** trusted context, resource-owner authorization, message validation, tenant isolation, and data minimization apply.
- **Database Engineering:** transactions, optimistic versions, outboxes, and persisted workflow state align decisions and outputs.
- **API Engineering:** typed/versioned envelopes, correlation, deadlines, errors, and compatibility expose protocols safely.
- **Testing and Quality:** state-machine tests, fault injection, replay, migration, load, and recovery drills provide evidence.
- **Systems Engineering:** safety-critical coordination requires hazard analysis, independent controls, and domain validation beyond the pattern.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Mediator intent, structure, applicability, and consequences.
2. Frank Buschmann et al., *Pattern-Oriented Software Architecture, Volume 1: A System of Patterns*, Wiley, 1996, ISBN 978-0-471-95869-7. Provides durable architectural pattern vocabulary and distinctions around coordination and communication.
3. Gregor Hohpe and Bobby Woolf, [*Enterprise Integration Patterns*](https://www.enterpriseintegrationpatterns.com/), Addison-Wesley, 2003. Distinguishes brokers, routers, channels, messages, correlation, and integration failure from in-process object collaboration.
4. Carl Hewitt, Peter Bishop, and Richard Steiger, [“A Universal Modular ACTOR Formalism for Artificial Intelligence”](https://www.ijcai.org/Proceedings/73/Papers/027B.pdf), IJCAI 1973. Primary actor-model foundation for isolated state and message-driven computation.
5. Cloud Native Computing Foundation, [CloudEvents specification](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md), version 1.0.2, 2022. Defines interoperable event context, source/ID identity, type/version-related fields, and privacy/security boundaries.
6. OWASP Foundation, [Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), accessed 2026-08-28. Provides deny-by-default, per-request permission validation, and authorization testing guidance.
7. Caitie McCaffrey, [“Distributed Sagas: A Protocol for Coordinating Microservices”](https://www.youtube.com/watch?v=0UTOLRTwOX0), 2017. Practitioner treatment of durable orchestration, compensation, and partial failure; useful as experience evidence, not a formal correctness proof.
8. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, ISBN 978-1-4493-7332-0. Provides durable foundations for logs, messaging, distributed transactions, ordering, and failure reasoning.

## Exercises

### Exercise 1

Recompute the collaboration graph counts and prove the executable mediator's eligibility invariant under its assumptions.

### Exercise 2

Diagnose a synchronous mediator whose colleague callback re-enters it while a lock is held, and design a safe transition/dispatch protocol.

### Exercise 3

Design a typed mediator for a multi-user document session, including membership, ordering, authorization, duplicates, and lifecycle.

### Exercise 4

Compare direct calls, event choreography, an in-process mediator, and a durable orchestrator for an order-fulfillment flow.

### Exercise 5

Review a proposed mediator for safety-critical industrial actuation without claiming functional safety.

## Answers to the Exercises

### Answer 1

For six colleagues, pairwise undirected acquaintance has \(\binom{6}{2}=6\cdot5/2=15\) links; the mediator star has one link per colleague, six. This counts topology only and ignores direction, interface breadth, and semantic knowledge.

In the executable example, base state has empty name, false terms, and disabled button, so the invariant holds. Each valid input updates exactly one mediator field, increments transition count, derives `eligible = nonempty(normalized name) and terms`, and applies that Boolean. Thus after successful return button state equals the predicate. The trace yields false, false, true, false; only false→true and true→false change the button, so three transitions produce two commands. The proof assumes serialization, accepted event types, terminating nonfailing button application, and no external button mutation; it proves no thread, persistence, security, or distributed property.

### Answer 2

The deadlock arises because the mediator holds a nonreentrant ownership lock while invoking unknown colleague code, which calls back and waits for the same lock. Even a reentrant lock can expose half-applied state or produce recursion. Define transition processing as: enqueue typed input; if a dispatcher is already active, return after enqueue; otherwise dequeue one input, acquire ownership, validate expected version/context, compute and commit new mediator state plus immutable ordered output plan, release ownership, then invoke outputs. Nested notifications enqueue behind the current transition.

Attach transition/causation identity, suppress only provably redundant state changes, cap hops/queue/work, and surface cycles rather than silently discarding. Define whether output failure stops remaining outputs, retries idempotently, or records repair; never hold the state lock during callbacks. Tests cover self-loop, two-colleague loop, same-value normalization, nested distinct input, colleague exception, cancellation, concurrent enqueue, output order, queue overflow, and state visibility.

### Answer 3

Use one `DocumentSessionMediator` per document/session key. State contains schema version, document version, authenticated membership/roles references, presence leases, per-participant sequence, outstanding operations, and bounded recent deduplication records. Typed inputs include `JoinRequested`, `EditSubmitted(baseVersion,opId,operation)`, `PresenceRenewed`, `LeaveRequested`, and connection facts; outputs are role-specific commands/events, not generic topics.

Derive actor/tenant from trusted connection context, authorize join and every edit against current resource policy, validate operation size/type, and apply the collaboration's chosen concurrency algorithm. Bind deduplication to session/actor/op ID/payload digest; order by document version or algorithm-specific causality, reject/quarantine conflicting IDs, and never trust client clocks. Persist document changes and durable events atomically where required; presence may be ephemeral with lease expiry. Bound participants, operation bytes/rate, queues, history, and reconnect replay. Test concurrent edits, duplicates/reorder/gaps, revoked access, stale base, disconnect/reconnect, expired lease, schema migration, hot sessions, crash/recovery, redaction, and cross-tenant attempts.

### Answer 4

Direct calls are clearest when a few components share one transaction/process and the sequence is stable; coupling grows as participants and conditional flow grow. Event choreography fits independent reactions to durable facts and reduces one central owner, but global progress, deadlines, failure, and compensation become distributed and harder to inspect. An in-process mediator is appropriate for one local application-use-case transaction or UI collaboration, but cannot survive process loss or coordinate independent authorities atomically.

A durable orchestrator is appropriate when fulfillment spans inventory, payment, shipment, timeouts, retries, and compensation. It persists workflow state/step identities, emits commands through outbox-like mechanisms, consumes facts idempotently, reconciles indeterminate effects, and exposes status. It costs infrastructure and central availability/throughput ownership and should partition by order. A sound design can combine them: direct calls inside one aggregate/transaction, local mediator for application policy, durable orchestration across services, and facts for independent analytics—each with explicit authority and failure semantics.

### Answer 5

First define controlled equipment, hazards, operating modes, physical limits, timing, sensor validity/provenance, command authority, interlocks, manual/emergency control, degraded/fail-safe states, and the exact safety claim. Separate supervisory coordination from independent safety mechanisms; loss or corruption of the mediator must not defeat hardwired/independently verified limits. Authenticate devices/operators, authorize at actuation, use freshness/sequence and command identity, bound queues/deadlines/retries, reject stale/conflicting state, and design watchdog, redundancy, isolation, reconciliation, and safe shutdown according to the applicable system context.

Evidence includes hazard/risk analysis, requirements traceability, formal state/invariant/timing analysis where tractable, independent control review, calibrated sensor/actuator evidence, simulator/hardware-in-loop tests, fault injection, network partition/reorder/duplication, overload, power/restart, cybersecurity assessment, human-factors/operational drills, configuration/version validation, and controlled release/rollback. Named domain, controls, functional-safety, software verification, cybersecurity, human-factors, operations/maintenance, quality, and relevant regulatory reviewers approve. Mediator structure and ordinary tests alone establish no functional safety, reliability level, or regulatory conformity.
