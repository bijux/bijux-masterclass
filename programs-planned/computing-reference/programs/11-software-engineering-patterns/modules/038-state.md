---
module_id: SEPAT-038
program: Software Engineering: Patterns
level: 1
module_number: 38
title: State
status: complete
last_verified: 2026-08-28
---

# State

## One-Page Review

### Governing question

How can state-dependent behavior and legal transitions be made explicit so an object appears to change class without scattering mode conditionals, while guards, actions, concurrency, persistence, failure, and evolution remain reviewable?

### Essential definitions

- A **context** owns identity, data, current state, and the public transition boundary.
- A **state object** implements behavior valid for one logical state and selects or proposes successor states.
- An **event** is an input to a state machine; a **transition** maps source state and event, subject to a **guard**, to target state and actions.
- An **illegal transition** is an explicit rejection, not an accidental missing branch.
- **entry**, **exit**, and transition actions run at defined points in the transition sequence.
- A **finite-state machine (FSM)** has a finite state set and transition relation; extended state holds data without encoding every value as a state.
- **hierarchical/orthogonal states** factor shared and concurrent logical modes; they do not necessarily imply threads.
- **typestate** makes some legal operations depend on a statically represented state.

### Central model, mechanism, or theorem

Define deterministic partial transition function

$$
\delta:S\times E\times D\times Ctx\to(S\times D\times A^*)\cup Rejected,
$$

where (S) is control state, (D) extended data, and (A^*) ordered actions. A valid implementation preserves invariant (P(s,d)): if (P(s,d)) and the selected guard holds, the committed successor satisfies (P(s',d')). State objects organize this function by source state; they do not prove guards, effect atomicity, termination, or distributed consistency.

### Critical invariants

- The context has exactly one valid active state/configuration under the chosen model.
- Every accepted event has one deterministic transition or an explicitly defined resolution rule; illegal events reject without partial mutation.
- Guards use trusted current data/authority and are side-effect-free where practical.
- Exit, transition, state commit, entry, and emitted effects have a documented order and failure boundary.
- State and version persist atomically with durable transition intent/events when required.
- Concurrent transitions use serialization or expected-version conflict; retries bind stable transition identity/payload.
- Timers, deadlines, cancellation, and external effects are modeled as inputs/actions with durable ownership when necessary.
- Machine/state schemas evolve through explicit compatible migration with old-state and in-flight-event fixtures.

### Common failures

Common failures include one Boolean per mode, impossible Boolean combinations, state classes containing unrelated data access, generic `handle(any)`, silent no-op illegal events, guards with hidden effects, context and state both choosing transitions, changing state before validating, callbacks during half-transition, recursive entry/exit loops, holding locks during external actions, assuming enum persistence is stable, replaying side effects, retrying without idempotency, wall-clock timers without durable identity, overwriting concurrent state, state explosion, premature statecharts, and calling a local FSM a durable workflow.

### Compact example

A document context delegates `submit`, `approve`, and `retract` to Draft, InReview, and Published state objects. Each accepted transition increments a version and records one action; `approve` in Draft rejects without changing state/version. The trace makes legal and illegal behavior explicit.

### Connections

[SEPAT-037](037-observer.md) reports state changes; [SEPAT-039](../ROADMAP.md) selects interchangeable algorithms. State connects to [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md), [Software Design and Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), and [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

Which behaviors and transitions depend on an object's control state, what data/authority guards them, and how can each accepted transition be made atomic, observable, recoverable, and evolvable within its true boundary?

The State pattern distributes transition behavior by source state. It is most valuable when modes are stable domain concepts and operations vary by mode—not when every conditional deserves a class.

## Why This Matters

Documents, connections, parsers, devices, sessions, orders, and workflows behave differently over time. Scattered conditionals make legal combinations, failure paths, and evolution difficult to see.

Explicit state improves vocabulary and testing, but introduces transition ownership, action ordering, persistence, and migration obligations. Across processes or time, an object pattern becomes a durable state-machine protocol with substantially stronger requirements.

## Prerequisites and Retrieval

You should understand polymorphism, invariants, FSMs, commands/events, transactions, optimistic concurrency, idempotency, timers, and partial failure. Retrieve these facts:

1. Control state and extended data are different; encoding every data value as a state causes explosion.
2. Guards decide applicability; actions cause change/effects; mixing them makes retries unsafe.
3. A state transition and independent external effect cannot be made atomic by assignment order.
4. Concurrent events need a linearization/version rule.
5. Persisted state names and queued events are versioned contracts.
6. Hierarchical and orthogonal state-machine semantics require explicit selection/action order.

## Learning Objectives

After completing this module, you should be able to:

- derive State from mode-dependent behavior;
- model states, events, guards, data, actions, and rejection formally;
- locate transition ownership between context and state objects;
- preserve invariants across local and durable transitions;
- control reentrancy, concurrency, timers, retries, and external effects;
- compare enums/tables, State objects, typestate, statecharts, and workflow engines;
- migrate persisted machines and in-flight inputs safely;
- test transition coverage, properties, races, faults, time, and recovery.

## Core Exposition

### Discover real states

A state is a mode with distinct legal operations or behavior, not merely a field value. If `submit` is legal only in Draft and `approve` only InReview, these are control states. Title text and reviewer count are extended data guarded by transitions.

Start with a state/event table. Enumerate every cell as accepted, ignored for a documented reason, deferred, or rejected with a stable error. Missing cells should not inherit accidental behavior.

### Give one layer transition authority

The context owns current state, identity/version, persistence boundary, and dispatch. State objects interpret events for their source state and return/propose a transition plan. Avoid both context and state independently mutating the state pointer.

One design returns `(target,newData,actions)` and lets context validate/commit. Another lets state call a narrow context transition method. The first makes plans easier to test and persist; the second can be simpler locally but needs reentrancy discipline.

### Separate guards from actions

Guards should be deterministic checks over current trusted data/context: reviewer present, token current, capacity available under a reservation protocol. Network calls or mutations hidden in guards make selection nondeterministic and retries dangerous.

Actions can update owned data, emit facts, schedule timers, or request external work. Classify each as transactional, post-commit, idempotent, compensatable, or irreversible.

### Define transition sequencing

A useful local sequence is: validate event/schema/authority; read state/version; select one transition; evaluate guards; build new owned state and ordered actions; atomically commit state/version and durable output; then execute post-commit callbacks/effects.

Entry/exit actions are ordinary ordered actions with explicit failure semantics. Do not publish the target state while required internal invariants remain incomplete.

### Reject illegal transitions clearly

Return stable reason/current-state/allowed-next-actions as appropriate without leaking sensitive policy. Rejection preserves state and version. Idempotent repeat of an already-achieved command may return current success only if the domain defines that semantic.

Never use `null` state or fall through to a default state. Invalid persisted values quarantine/recover rather than guess.

### Control reentrancy

An entry action can cause another event synchronously, observing half-applied work or recursing. Commit invariants first and queue nested events until the transition completes, or forbid synchronous reentry with visible failure.

Attach causation and work/hop limits. A global busy flag that silently drops inputs is not a safe cycle policy.

### Serialize concurrent transitions

For one context identity, use confinement/actor mailbox, transaction row lock, or expected version. With version (v), only one transition may commit `WHERE version=v`; losers reload and reevaluate authority/guards.

Do not calculate target from stale state and overwrite newer data. A queue gives order only at its owned partition; database and external effects still require alignment.

### Persist state and outputs together

Persist stable state code/schema, machine version, extended data, context version, and transition metadata. When a fact/command must follow commit, write it to an outbox in the same transaction.

Recovery rehydrates only valid allowlisted states. Do not serialize executable state objects/class names. Map durable codes to current implementations through an explicit registry and migration.

### Model external work honestly

A transition to `PaymentPending` plus a durable payment command is different from `Paid`. Provider success/failure/unknown arrive as later events. A timeout does not prove failure after an indeterminate request.

Use stable operation identity, reconciliation, bounded retry, cancellation transitions, and compensation. Never hold a database transaction or object lock while waiting for a remote service.

### Treat time as input

Schedule a durable timer with machine ID, expected state/version, timer type, due time, and identity. On delivery, recheck current state/version; late/duplicate timers become stale no-ops or explicit outcomes.

Wall-clock changes, restart, scheduler loss, and clock uncertainty need policy. A local sleep is not a durable deadline.

### Manage state explosion

Do not multiply independent dimensions into names like `ConnectedAuthenticatedWritableHealthy`. Keep extended data, compose orthogonal regions only with clear semantics, or separate collaborating machines.

Hierarchical states factor shared behavior and entry/exit. Statecharts add hierarchy, orthogonality, history, internal events, and selection rules; use a specified engine when complexity warrants it rather than inventing partial semantics.

### Use typestate where it fits

Typestate represents modes as distinct static types so illegal operations may be unrepresentable in one process. It improves compile-time guidance for builders/resources, but dynamic persistence, user inputs, branching, and distributed events still require runtime validation.

### Evolve durable machines

Version state/data and event/command schemas. Adding a state changes reachability, timers, reports, and old code behavior. Define rolling compatibility: which deployment consumes which versions and how in-flight instances migrate.

Keep golden histories for every durable state and pending timer/event. Migration must preserve business meaning, not merely rename enums. Some instances require explicit operator/domain review.

### Verify and operate

Generate transition-coverage tests from the table. Property-test invariant preservation, rejection nonmutation, determinism, reachability, absence of forbidden states, and bounded progress under assumptions. Model-check small critical machines when worthwhile.

Fault-inject before/after state commit, outbox, publish, effect request/response, timer delivery, and acknowledgement. Measure state distribution/age, transition/rejection rates, conflicts, queue/timer lag, retries, stuck/terminal instances, migration failures, and reconciliation backlog.

## Definitions and Notation

Machine $M=(S,E,D,\delta,s_0)$. For current tuple (x=(id,s,d,v)), event (e=(eid,type,payload,expectedVersion)). A transition plan is (p=(s',d',A)).

Commit condition is $expectedVersion=v\land P(s,d)\land Guard(s,e,d,ctx)$. Successful commit yields `(s',d',v+1)`; rejection/conflict preserves `(s,d,v)`.

Transition coverage is not path coverage: with cycles, paths may be infinite. Reachability (Reach(s_0)) and safety (P) can be checked over a finite abstraction; liveness claims need fairness/environment assumptions.

## Mechanisms, Invariants, or Proof Structure

### State design procedure

1. Define context identity, control states, extended data, initial/terminal states, and invariant.
2. Enumerate typed events and every state/event outcome.
3. Separate pure guards, owned data changes, durable outputs, and external actions.
4. Give one layer authority to validate and atomically commit state/version.
5. Define illegal events, reentrancy, per-key concurrency, duplicates, and time.
6. Persist stable codes/data/output intent and reconcile external work.
7. Version/migrate machine, states, events, timers, and in-flight instances.
8. Test transitions/properties/races/faults/time/migration and operate stuck-state recovery.

### Executable mechanism

This document workflow uses state objects to return target state and action. The context commits version/log only after a legal plan. It does not model authorization, concurrency, persistence, callbacks, timers, or external effects.

<!-- bijux-verify: {"id":"state-document-workflow","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"draft --submit--> in-review v1 action=request-review\ninvalid=draft cannot approve state=draft v0\nin-review --approve--> published v2 action=publish\npublished --retract--> in-review v3 action=request-review\n","stderr":""}} -->
```python
class Draft:
    name = "draft"

    def plan(self, event):
        if event == "submit":
            return InReview(), "request-review"
        raise ValueError(f"draft cannot {event}")


class InReview:
    name = "in-review"

    def plan(self, event):
        if event == "approve":
            return Published(), "publish"
        if event == "withdraw":
            return Draft(), "continue-editing"
        raise ValueError(f"in-review cannot {event}")


class Published:
    name = "published"

    def plan(self, event):
        if event == "retract":
            return InReview(), "request-review"
        raise ValueError(f"published cannot {event}")


class Document:
    def __init__(self, state):
        self.state = state
        self.version = 0

    def apply(self, event):
        source = self.state.name
        target, action = self.state.plan(event)
        self.state = target
        self.version += 1
        print(f"{source} --{event}--> {target.name} v{self.version} action={action}")


valid = Document(Draft())
valid.apply("submit")
invalid = Document(Draft())
try:
    invalid.apply("approve")
except ValueError as error:
    print(f"invalid={error} state={invalid.state.name} v{invalid.version}")
valid.apply("approve")
valid.apply("retract")
```

### Local invariant argument

Each state returns only declared successors. `Document.apply` calls `plan` before mutating; a rejection raises and preserves state/version. A successful plan assigns target and increments version exactly once. By inspection, all reachable targets are Draft, InReview, or Published and the demonstrated path is legal.

This finite argument assumes serialized execution, nonfailing assignment/print, trusted event strings, and no external mutation. It proves no guard, authorization, persistence, or effect property.

### Verification layers

Review transition relation and invariants, implementation sequencing, concurrency/persistence, timers/external effects, migration/rolling deployment, and operational recovery separately. Tests are evidence for explored cases, not universal reachability or liveness proofs.

## Alternatives and Trade-Offs

| Approach | Strength | Cost or limitation | Prefer when |
|---|---|---|---|
| Enum plus switch/table | Complete transitions visible centrally | Large switches; behavior not encapsulated | Small stable machines |
| State objects | Behavior grouped by source state | More types and distributed transition view | Substantial mode-specific behavior |
| Strategy | Interchangeable algorithm independent of lifecycle | Does not inherently model legal transitions | Caller/config selects behavior |
| Typestate | Compile-time illegal-operation prevention | Dynamic/persistent states still runtime | Local resource/build protocols |
| Statechart engine | Hierarchy, orthogonality, specified semantics | Tool/runtime complexity | Large event-driven machines |
| Durable workflow engine | Timers, persistence, retry, visibility | Infrastructure and determinism constraints | Long-running cross-boundary coordination |
| Rules/decision table | Policy editable/analyzable | Control lifecycle may be obscured | Guards/decisions dominate |

## Failure Modes and Misconceptions

- **“State is an enum.”** The pattern groups behavior and transition decisions; an enum/table may still be better.
- **“Every conditional becomes a state.”** States represent modes; ordinary data remains data.
- **“State objects own everything.”** Context owns identity, version, persistence, and atomic transition boundary.
- **“Illegal events can be ignored.”** Silent no-ops hide client defects unless explicitly part of idempotent semantics.
- **“Entry actions are atomic with state assignment.”** Only a transaction/outbox/workflow mechanism aligns effects.
- **“A queue prevents races.”** It orders one partition but does not align storage or external authorities.
- **“Timeout means the remote action failed.”** The effect may be indeterminate and require reconciliation.
- **“Parallel states mean threads.”** They are simultaneous logical regions under specified event semantics.
- **“Typestate removes runtime validation.”** External/persisted input remains dynamic and adversarial.
- **“Renaming enum values is safe.”** Persisted states, metrics, events, timers, and old deployments depend on stable meaning.
- **“Transition tests prove liveness.”** Progress depends on environment/fairness and may include cycles.
- **“A state machine is a workflow engine.”** Durability, timers, retry, observability, and recovery are additional mechanisms.

## Worked Examples

### Example 1

Booleans `submitted`, `approved`, and `retracted` allow contradictory combinations. States Draft/InReview/Published plus explicit transitions exclude them. **Conclusion:** Control states compress legal combinations.

### Example 2

Draft receives `approve`; plan rejects before mutation, leaving Draft v0. **Conclusion:** Validate/select before committing and make illegality observable.

### Example 3

Two requests read v7 and propose different successors. Conditional commit lets one produce v8; the loser reloads/rejects instead of overwriting. **Conclusion:** State transitions are concurrency-controlled writes.

### Example 4

State commits `Paid` before provider response, but the request times out after possibly charging. Modeling `PaymentPending` and later reconciled result avoids a false fact. **Conclusion:** External effects need intermediate states.

### Example 5

A deadline timer for v4 arrives after machine reached v6. Expected state/version makes it stale rather than cancelling current work. **Conclusion:** Timers are versioned inputs.

### Example 6

An entry callback emits another event synchronously and recurses. Queueing nested events until commit gives deterministic breadth-first processing. **Conclusion:** Reentrancy policy is part of transition semantics.

### Example 7

Adding `Suspended` while old workers cannot decode it breaks rolling deployment. Dual-readable schemas and staged writer activation preserve coexistence. **Conclusion:** State evolution is a protocol rollout.

### Example 8

Connection×authentication×health creates 12 combined names. Three orthogonal concerns or separate cooperating machines avoid cross-product classes where transitions are independent. **Conclusion:** Factor independent dimensions.

### Example 9

All state/event cells have tests, yet a guard mistakenly authorizes the wrong tenant. Transition coverage does not prove policy correctness. **Conclusion:** Guards and trusted context need separate evidence.

### Example 10

An infusion pump controller's state diagram omits sensor plausibility, timing, actuator feedback, hazards, and independent interlocks. **Conclusion:** Pattern structure is not functional-safety evidence.

## Cross-Program Connections

- **Programming Languages and Semantics:** transition systems, operational semantics, typestate, effects, and bisimulation formalize machines.
- **Object-Oriented Programming:** polymorphism, encapsulation, ownership, and dynamic dispatch implement State.
- **Software Design and Domain Modeling:** aggregate invariants, commands, domain events, and lifecycle vocabulary locate states.
- **Concurrency and Parallel Programming:** serialization, actors, locks, CAS, and memory visibility govern transitions.
- **Database Engineering:** transactions, optimistic versions, outboxes, and recovery persist machines.
- **Distributed Systems Engineering:** partial failure, retries, ordering, timers, reconciliation, and compensation constrain workflows.
- **Testing and Quality:** model/property tests, model checking, fault injection, virtual time, and migration fixtures provide evidence.
- **Security Engineering:** trusted context, current authorization, tamper-resistant state, and safe errors protect transitions.
- **Cloud and Platform Engineering:** workflow engines, queues, timer services, observability, and stuck-instance repair operate durable machines.
- **Systems Engineering:** control/safety state machines require timing, hazard, hardware, and independent assurance.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical State intent, structure, applicability, and consequences.
2. David Harel, [“Statecharts: A Visual Formalism for Complex Systems”](https://doi.org/10.1016/0167-6423(87)90035-9), *Science of Computer Programming* 8(3), 1987. Primary hierarchy, orthogonality, and statechart formalism.
3. Robert E. Strom and Shaula Yemini, [“Typestate: A Programming Language Concept for Enhancing Software Reliability”](https://doi.org/10.1109/TSE.1986.6312929), *IEEE Transactions on Software Engineering* 12(1), 1986. Primary typestate foundation.
4. Object Management Group, [*Unified Modeling Language 2.5.1*](https://www.omg.org/spec/UML/2.5.1/PDF), formal/2017-12-05. Defines UML state-machine concepts and semantics.
5. W3C, [State Chart XML (SCXML) 1.0](https://www.w3.org/TR/scxml/), Recommendation, 2015. Specifies event selection, guards, hierarchy, parallel regions, entry/exit, history, and execution algorithm.
6. Gerard J. Holzmann, *The SPIN Model Checker: Primer and Reference Manual*, Addison-Wesley, 2003, ISBN 978-0-321-22862-8. Provides explicit-state modeling and verification foundations.
7. Leslie Lamport, *Specifying Systems*, Addison-Wesley, 2002, ISBN 978-0-321-14306-8. Provides state-machine safety/liveness and temporal specification foundations.
8. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, ISBN 978-1-4493-7332-0. Provides transactions, logs, concurrency, messaging, and distributed-failure foundations.

## Exercises

### Exercise 1

Trace the executable workflow, derive its reachable transitions, and state exactly what the local argument proves.

### Exercise 2

Design a state/event/guard table for a resource lease with expiry, renewal, release, and revocation.

### Exercise 3

Design atomic persistence, outbox, concurrency, retry, and timer behavior for a durable state machine.

### Exercise 4

Compare enum/table, State objects, typestate, statecharts, and a workflow engine for a protocol client.

### Exercise 5

Review a safety-critical controller state machine without claiming safety integrity.

## Answers to the Exercises

### Answer 1

Initial Draft accepts only submit, yielding InReview v1/action request-review. A separate Draft receiving approve raises before assignment and remains Draft v0. InReview accepts approve, yielding Published v2/action publish. Published accepts retract, yielding InReview v3/action request-review. Other declared transition is InReview withdraw to Draft; all other cells reject.

The argument establishes, by inspection of finite class methods and plan-before-mutate sequencing, that the shown serialized calls reach only declared state objects, accepted calls increment once, and the demonstrated rejection preserves state/version. It proves no completeness against domain requirements, guard/authority correctness, thread safety, atomic persistence, action execution, durability, migration, timing, or safety.

### Answer 2

States: Available, Active, Released, Expired, Revoked. `Acquire(holder,ttl)` moves Available→Active if authority/capacity/TTL bounds hold and creates lease ID/version/deadline. `Renew(lease,extension)` keeps Active with new deadline if current holder/authority/version and policy permit. `Release` moves Active→Released idempotently for the same lease identity. Versioned `ExpiryDue` moves Active→Expired only if timer identity/deadline/current version still match. `Revoke(reason)` moves Active→Revoked under current administrative policy; terminal states reject renewal and define idempotent repeated terminal commands.

Persist holder scope, lease ID, state/version, deadline basis, policy/schema, timer ID, and audit metadata. Guards are pure current checks; scheduling/cancellation are durable outputs. Specify clock uncertainty, late/duplicate timers, authorization revocation, resource fencing tokens, terminal retention, and reacquisition as a new lease. Test every cell, exact deadline boundaries, stale versions/timers, duplicate IDs/different payload, concurrent renew/revoke/expiry, crash/restart, and clock behavior.

### Answer 3

In one transaction, load machine by ID/version, authenticate/authorize trusted context, validate event identity/schema, dedupe payload-bound ID, select transition/guard, write target state/data/version, store outcome, and append outbox commands/events/timer changes. Conditional expected-version update resolves concurrent attempts. After commit, publishers/schedulers deliver at least once using stable output identity; consumers are idempotent or effect-queryable. Record indeterminate external outcomes and reconcile rather than blind retry.

Timers carry machine ID, expected state/version, type, due time, and timer ID; delivery revalidates. One retry owner applies bounded attempts/backoff/deadline. Recovery resumes outbox/timers and quarantines poison/unsupported versions. Fault tests cover before/after event claim, state/outbox/timer commit, publish, provider request/response, acknowledgement, and crash; also duplicate/reorder, conflicts, cancellation races, migration, hot keys, lag, and stuck repair.

### Answer 4

Use enum/table when the machine is small and complete transition visibility outweighs class distribution. Use State objects when substantial behavior varies by stable source state and polymorphic extension/test isolation helps. Use typestate for local compile-time protocols such as Unconnected→Connected resources when state changes can change static value type; retain runtime validation at external/persistence boundaries.

Use a specified statechart engine when hierarchy, orthogonal regions, history, event queues, and entry/exit semantics are truly required; avoid inventing subsets. Use a durable workflow engine when work spans restarts/services/time, needs persisted timers, retries, activity identity, visibility, and operator recovery. A protocol client may combine typestate for local API, a table/state objects for protocol logic, and durable workflow only if sessions must survive process loss; justify each semantic layer and test interoperability.

### Answer 5

Define hazards, controlled process, safe/degraded states, environmental/physical assumptions, sensors/actuators and provenance, timing/deadlines, authority, interlocks, manual/emergency behavior, communication loss, restart, and exact safety claim. Analyze every state/event/guard/action plus unreachable/forbidden configurations; separate logical state from physical plant state and require feedback/fencing. Keep independent safety mechanisms from being bypassed by software state.

Evidence includes hazard/risk analysis and traceability, formal invariant/reachability/timing analysis where tractable, independent code/model review, calibrated simulation and hardware-in-loop reference cases, boundary/fault injection for sensors/actuators/network/power/clock/concurrency/overload, cybersecurity, human-factors/operational drills, configuration/version assurance, and controlled release/rollback. Named domain/controls, functional-safety, verification, hardware, cybersecurity, human-factors, quality/regulatory, and operations reviewers approve. The State pattern, model, and ordinary tests establish no safety integrity level or regulatory conformity.
