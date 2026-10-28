---
module_id: SEPAT-032
program: Software Engineering: Patterns
level: 1
module_number: 32
title: Command
status: complete
last_verified: 2026-08-28
---

# Command

## One-Page Review

### Governing question

How can an intent to change state be represented as a first-class value so invocation, execution, queuing, retry, authorization, concurrency, audit, undo/compensation, and evolution remain explicit without confusing commands with events, queries, or guaranteed effects?

### Essential definitions

- A **command** represents an intent or request to perform a state-changing operation.
- The **invoker** accepts, schedules, queues, or triggers a command without necessarily knowing its business implementation.
- The **handler/receiver** validates current authority and state, then attempts the operation.
- A **command envelope** carries command identity, type/version, payload, actor/tenant context reference, causation/correlation, deadline, and concurrency/idempotency metadata.
- **acceptance** means the system durably owns further processing; it is not necessarily completion.
- **idempotency** means repeated execution under one declared identity has the same intended effect as one execution.
- **optimistic concurrency** rejects execution when an expected version/precondition no longer holds.
- **undo** restores a prior local model state under declared assumptions; **compensation** is a new domain action that amends an earlier effect.
- An **event** states that something happened; a command asks that something happen and may be rejected.
- A **query** returns information without intentionally changing observable domain state under command-query separation.

### Central model, mechanism, or theorem

Model a command as immutable value (c=(id,type,version,payload,actor,precondition,deadline)). Execution is

$$
Execute:S\times Ctx\times c\to (S',Outcome,Events),
$$

where validation occurs against current state (S) and trusted context. For scoped command identity (id), an idempotency record maps payload digest and outcome. Reusing the same identity and digest returns/resumes the logical outcome; reusing the identity with a different digest is conflict. Neither serialization nor queue delivery proves authorization, atomicity, exactly-once execution, or successful effect.

### Critical invariants

- Command identity, type/version, payload schema, target, and intended effect are explicit and immutable after acceptance.
- Authentication/authorization and domain preconditions are re-evaluated at execution from trusted current evidence.
- Idempotency scope binds actor/tenant, command type, identity, and payload digest with durable retention rules.
- State change, idempotency result, and emitted durable intent/events share the required transaction or reconciliation protocol.
- Ordering and concurrency rules prevent lost updates and invalid interleavings without claiming global serialization.
- Deadline/cancellation distinguish not-started, accepted, executing, committed, completed, and indeterminate states.
- Command evolution preserves old envelopes through explicit upcasting/migration or rejects unsupported versions safely.
- Sensitive payloads, credentials, and personal data are minimized, protected, redacted, and retained by policy.

### Common failures

Common failures include mutable command objects, generic `Execute(any)`, accepting caller-supplied role/tenant, validating only when queued, treating enqueue as completion, acknowledging before durable acceptance, assuming exactly-once delivery, reusing idempotency keys for different payloads, retrying indeterminate non-idempotent effects, storing results outside the state transaction, relying on wall-clock arrival for business order, unlimited queues, serializing code/closures, deserializing arbitrary types, calling compensation rollback, undoing after intervening changes, and logging full command payloads.

### Compact example

An account handler accepts a deposit command with expected version zero, producing balance 1,500 and version one. Replaying the identical command ID returns the stored result without another deposit. A withdrawal exceeding balance is rejected and stored idempotently; a stale expected version yields conflict.

### Connections

[SEPAT-031](031-chain-of-responsibility.md) selects a handler; Command packages the request a handler executes. [SEPAT-033](../ROADMAP.md) represents a language grammar as objects, and [SEPAT-036](../ROADMAP.md) captures recoverable state. Command connects to [Domain Modeling](../../09-software-engineering-software-design-and-domain-modeling/ROADMAP.md), [Database Engineering](../../18-database-engineering/ROADMAP.md), and [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

What exact state-changing intent should survive separation in time/process, and which authority, precondition, idempotency, ordering, failure, and recovery facts must travel with or be re-derived for safe execution?

Command decouples when/who invokes from how work is performed. That temporal decoupling makes stale assumptions, duplicate delivery, compatibility, and operational ownership first-class.

## Why This Matters

Commands enable queues, schedulers, menus, macros, workflows, retries, audit, and testable use-case handlers. They provide durable vocabulary for task-oriented state change instead of exposing receiver call sequences.

Once commands cross time or process boundaries, a simple method object becomes a protocol. A message may be delayed, duplicated, reordered, expired, unauthorized, malformed, or applied despite a lost response. Honest models avoid the myth that “sent” means “done.”

## Prerequisites and Retrieval

You should understand immutable values, transactions, optimistic concurrency, queues, idempotency, authorization, deadlines, event publication, and distributed failure. Retrieve these facts:

1. Intent, acceptance, execution, commit, and externally observed completion are different milestones.
2. At-least-once delivery requires duplicate-safe handling; exactly-once end-to-end effect is not supplied by a queue label alone.
3. Authorization and preconditions can change between command creation and execution.
4. A timeout after send/commit can leave the caller uncertain about the effect.
5. Undo of local reversible state differs from compensation for observed external effects.
6. Commands and events have opposite direction of authority: requests may be refused; facts should not command consumers implicitly.

## Learning Objectives

After completing this module, you should be able to:

- model commands as immutable versioned intent;
- separate invoker, dispatcher, handler, receiver, and outcome responsibilities;
- design durable idempotency and optimistic-concurrency protocols;
- distinguish queued acceptance from execution/completion;
- specify retry, deadline, cancellation, ordering, and uncertainty;
- design safe serialization/version migration and dispatch allowlists;
- reason about undo, compensation, audit, and data retention;
- test handlers, dispatch, persistence, duplication, crash boundaries, and replay.

## Core Exposition

### Name intent in domain language

Prefer `ApproveClaim`, `ReserveSeat`, or `ChangeDeliveryAddress` over `UpdateRecord`. Include target and requested transition, not a precomputed new database row that lets callers bypass invariants.

One command has one logical intent, though fulfilling it may coordinate several domain objects and external capabilities.

### Make the command immutable

Once accepted, identity and payload must not mutate beneath signatures, hashes, audit, or retries. Convert external DTOs into validated owned values; copy mutable buffers and canonicalize only according to explicit domain rules.

Do not serialize receiver objects, database sessions, callbacks, secrets, or ambient context. Commands are data contracts, not executable code shipped to a worker.

### Separate envelope from payload

The payload expresses domain intent. The envelope supplies type/version, command ID, created metadata, deadline, actor/tenant reference, correlation/causation, expected version, trace carrier, and integrity/provenance as required.

Trust differs by field. Authenticate transport and derive authority from trusted evidence; never believe a role or tenant merely because it appears in the payload.

### Validate twice for different reasons

At ingress, validate syntax, schema, size, supported type/version, and basic authentication before consuming resources. At execution, validate current authorization, target state, preconditions, policy version, and deadline.

A command valid yesterday may be forbidden or stale today. Queue acceptance must not freeze authority indefinitely unless that is an explicit delegated capability with bounded scope and expiry.

### Define outcomes and milestones

Useful outcomes include `rejected`, `accepted`, `executing`, `committed`, `completed`, `conflict`, `cancelled`, `expired`, `failed`, and `indeterminate`. Use only distinctions the system can support and clients need.

An asynchronous API often returns an operation ID on durable acceptance. A status query or event reports later progress. Do not return `success` merely because a broker accepted bytes.

### Build idempotency around logical identity

Key by tenant/actor scope, command type, command ID, and payload digest. Atomically claim or load the record; concurrent duplicates wait, share/resume, or get a defined in-progress outcome. Different payload under one scoped ID is conflict.

Persist terminal outcome or durable progress long enough for retry windows. Expiry/reuse rules are part of the contract. Idempotency protects one logical command, not arbitrary semantically similar requests.

### Align state, result, and events

Within one transactional store, update domain state, expected version, command result, and outbox event atomically when required. Publishing after commit without an outbox can lose the event; publishing before commit can announce a change that rolls back.

Across authorities, use durable workflow state, idempotent steps, compensation, and reconciliation. Do not call it one atomic command if mechanisms cannot provide atomicity.

### Control concurrency and order

Use expected aggregate/resource version or a command-specific precondition to reject stale changes. Serialize only the narrow key that needs order; global FIFO is expensive and often unavailable across partitions.

Arrival order, creation timestamps, and broker offsets are not automatically business order. Define per-aggregate sequence, causality, or commutativity and handle gaps/duplicates explicitly.

### Retry only with effect knowledge

Retry transient failures when the handler's operation is idempotent or the system can prove the effect did not apply. One layer owns retry, applies bounded attempts/backoff/jitter, and respects one deadline.

After an indeterminate external effect, query/reconcile using a stable provider idempotency/operation identity. Blind replay can duplicate payments, messages, or physical actions.

### Model cancellation honestly

Before acceptance, cancellation may abandon work. After durable acceptance, it is usually a new `CancelOperation` command subject to current state and races. It may be too late after commit or physical actuation.

Cancellation of caller waiting does not erase the command. Return status/operation identity so clients can reconcile.

### Distinguish undo from compensation

For an editor command with isolated local history, inverse data or a Memento can support undo if no conflicting edit invalidates assumptions. External notifications, payments, and physical actions are observed and often irreversible.

Compensation is a new authorized command with its own failures and audit. A refund does not delete the charge or all consequences.

### Version and dispatch safely

Use an allowlisted registry from stable command type/version to parser/upcaster/handler. Reject unknown types and oversized/deep payloads. Never instantiate arbitrary class names from untrusted data.

Keep old-version fixtures and migration chains. Upcasters preserve original provenance and produce current owned payloads; do not mutate archived evidence silently.

### Operate queues and handlers

Bound queue depth, payload size, attempts, concurrency, per-tenant rate, and dead-letter retention. Backpressure or reject before overload becomes unbounded delay. Poison commands need quarantine and controlled redrive, not infinite retry.

Record command ID/type/version, state transition, bounded reason, latency, attempts, handler version, and correlation without sensitive payloads. Audit authorization and compensations with integrity controls.

### Test crash boundaries

Unit-test domain handlers. Contract-test command parsing and results. Integration-test real transaction/isolation/outbox and broker acknowledgement. Crash/fault-inject before and after claim, state commit, result persistence, event publication, acknowledgement, and response.

Test duplicate/concurrent delivery, conflicting payload ID, stale version, authorization revocation, expiry, cancellation races, poison payload, migration, replay, load, and recovery tooling.

## Definitions and Notation

Let command (c=(i,k,v,p,a,e,D)): ID (i), type (k), schema version (v), payload (p), actor scope (a), expected state version (e), and deadline (D). Let (h(p)) be canonical payload digest under versioned rules.

Idempotency table entry (I[a,k,i]=(h(p),state,outcome)). On repeat:

$$
h(p')=h(p)\Rightarrow return/resume\ same\ logical\ execution,
$$

while $h(p')\ne h(p)$ is conflict. This does not imply every log/metric side effect occurs once.

For aggregate version (n), command with expected (e) may commit only if (e=n); successful commit advances to (n+1). Let acceptance-to-completion state machine include terminal `rejected`, `completed`, `cancelled`, `expired`, `failed`, or `indeterminate` as supported.

## Mechanisms, Invariants, or Proof Structure

### Command design procedure

1. Name one state-changing domain intent and target.
2. Define immutable owned payload and versioned envelope.
3. Specify ingress and execution-time validation/authorization.
4. Model outcomes, milestones, expected version, and idempotency.
5. Align state/result/events transactionally or define reconciliation.
6. Define ordering, retry, deadline, cancellation, and compensation.
7. Build allowlisted version dispatch and bounded operations.
8. Test duplicates, races, crashes, migrations, replay, and recovery.

### Executable mechanism

This sequential account handler demonstrates expected-version checks, payload-bound command IDs, stored outcomes, and replay. It does not model authentication, concurrency, durable transactions, or external effects.

<!-- bijux-verify: {"id":"command-idempotent-account","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"deposit=accepted balance=1500 version=1\nreplay=accepted balance=1500 version=1\nlarge=rejected balance=1500 version=1\nstale=conflict balance=1500 version=1\n","stderr":""}} -->
```python
class Account:
    def __init__(self, balance):
        self.balance = balance
        self.version = 0
        self.results = {}

    def execute(self, command_id, kind, amount, expected_version):
        payload = (kind, amount, expected_version)
        prior = self.results.get(command_id)
        if prior is not None:
            if prior[0] != payload:
                return "id-conflict"
            return prior[1]
        if expected_version != self.version:
            outcome = "conflict"
        elif amount <= 0:
            outcome = "rejected"
        elif kind == "deposit":
            self.balance += amount
            self.version += 1
            outcome = "accepted"
        elif kind == "withdraw" and amount <= self.balance:
            self.balance -= amount
            self.version += 1
            outcome = "accepted"
        else:
            outcome = "rejected"
        self.results[command_id] = (payload, outcome)
        return outcome


account = Account(1000)
first = account.execute("cmd-1", "deposit", 500, 0)
print("deposit=" + first + " balance=" + str(account.balance) + " version=" + str(account.version))
replay = account.execute("cmd-1", "deposit", 500, 0)
print("replay=" + replay + " balance=" + str(account.balance) + " version=" + str(account.version))
large = account.execute("cmd-2", "withdraw", 2000, 1)
print("large=" + large + " balance=" + str(account.balance) + " version=" + str(account.version))
stale = account.execute("cmd-3", "withdraw", 200, 0)
print("stale=" + stale + " balance=" + str(account.balance) + " version=" + str(account.version))
```

A production handler would atomically persist command claim/result with account state and outbox, isolate concurrent executions, authenticate/authorize, use exact money types, and protect sensitive data.

### Proof obligations

Prove state invariants across every handler outcome and transactional crash point. Prove idempotency only for the declared scope, digest, retention, and concurrent-claim protocol. Distributed exactly-once effects, external completion, and compensation require separate evidence.

The snippet proves a finite sequential integer trace only. It establishes no financial correctness, durability, concurrency, authorization, or delivery guarantee.

## Alternatives and Trade-Offs

| Approach | Meaning | Main trade-off |
|---|---|---|
| Command object/message | request state change | rejection, duplication, evolution |
| Direct method call | immediate invocation | temporal/location coupling |
| Event | fact that occurred | consumers should not decide whether fact happened |
| Query | request information | should avoid intentional domain mutation |
| Job/task | scheduled unit of work | may be technical rather than domain intent |
| Workflow/process manager | multi-step durable coordination | state/recovery complexity |
| Function/closure | executable behavior | unsafe/nonportable serialization |
| State-machine transition | explicit allowed transition | less open-ended encapsulation |

Commands can be handled synchronously without a queue. CQRS and event sourcing are separate choices with significant additional complexity.

## Failure Modes and Misconceptions

### “A command must return nothing”

Command-query separation is a useful discipline, but command handling often needs an outcome/operation ID. Returning a result does not make the intent a query if it changes state.

### “Queued means successful”

Queue acceptance means only the queue/system owns further handling under its contract. Domain rejection or execution failure can occur later.

### “Exactly-once delivery solves duplicates”

Effects span broker, handler, database, provider, and response. Durable idempotency and reconciliation are still needed.

### “Authorization was checked at creation”

Authority, policy, ownership, and target state may change before execution. Recheck from trusted current evidence.

### “Undo reverses every command”

Observed and physical effects are not erased. Use conflict-aware undo or explicit compensation with its own consequences.

### “Command serialization can include a class name”

Arbitrary type construction is unsafe and couples deployments. Use allowlisted stable type/version registries and owned schemas.

### “CQRS is required”

Command objects do not require separate read/write models. CQRS is valuable only where its benefits exceed its complexity.

## Worked Examples

### Example 1

A text editor stores `InsertText(position,text,base_revision)` and inverse metadata. Undo is rejected after a conflicting remote edit unless transformed/rebased. **Conclusion:** Undo depends on intervening state.

### Example 2

A payment command times out after provider acceptance. The handler queries by provider idempotency key instead of issuing another charge. **Conclusion:** Indeterminate effects require reconciliation.

### Example 3

Two concurrent withdrawals carry expected version seven. One commits version eight; the other conflicts and must be reconsidered, not blindly replayed. **Conclusion:** Optimistic concurrency protects current invariants.

### Example 4

A queued approval was authorized yesterday, but the approver's role is revoked before execution. Execution-time authorization rejects it. **Conclusion:** Delayed commands cannot freeze ambient authority.

### Example 5

State commits but event publication crashes. A transactionally stored outbox later publishes the event idempotently. **Conclusion:** State and durable publication intent need one acceptance boundary.

### Example 6

The same command ID arrives with a different amount. Digest comparison returns conflict and emits security telemetry. **Conclusion:** Idempotency identity must bind payload.

### Example 7

A cancel request races with shipment. If shipment is already accepted, cancellation becomes a return/recall workflow rather than deletion. **Conclusion:** Cancellation is a state-dependent command.

### Example 8

An old version encodes cents as integer; a new version uses currency plus decimal minor units. An audited upcaster preserves original bytes and rejects unsupported currencies. **Conclusion:** Command evolution needs explicit semantic migration.

### Example 9

A poison command retries forever and blocks its partition. Bounded attempts, quarantine, alerting, inspection, and controlled redrive restore progress. **Conclusion:** Operational limits are part of command handling.

### Example 10

An autonomous actuator command is accepted but acknowledgement is lost. The system reconciles authenticated sequence/state and retains independent interlocks; it never infers “not applied.” **Conclusion:** Command encapsulation cannot create physical exactly-once safety.

## Cross-Program Connections

- **Programming Languages and Semantics:** immutable data, effects, sum types, serialization, and closures shape command representation.
- **Object-Oriented Programming:** invoker/receiver separation, encapsulation, and polymorphic dispatch form the classic pattern.
- **Concurrent Programming:** queues, races, cancellation, ordering, and actor/mailbox processing govern execution.
- **Domain Modeling:** task language, aggregates, invariants, and domain events define command semantics.
- **Software Architecture:** ports, dispatch registries, composition roots, and workflows place handlers.
- **Testing and Quality:** model tests, duplicate/race tests, crash injection, replay, and migration fixtures provide evidence.
- **Database Engineering:** transactions, optimistic versions, idempotency tables, outbox, and isolation underpin durability.
- **Security Engineering:** trusted context, execution-time authorization, allowlisted deserialization, and data retention constrain envelopes.
- **Distributed Systems:** at-least-once delivery, partial failure, causality, idempotency, and reconciliation dominate remote commands.
- **Systems Engineering:** commands to devices require timing, hazard, independent control, and indeterminate-effect analysis.

## References

1. Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides, [*Design Patterns: Elements of Reusable Object-Oriented Software*](https://www.pearson.com/en-us/subject-catalog/p/Gamma-Design-Patterns-Elements-of-Reusable-Object-Oriented-Software/P200000009480/9780321700698), Addison-Wesley, 1994. Canonical Command intent, participants, applicability, undo, and consequences.
2. Bertrand Meyer, *Object-Oriented Software Construction*, second edition, Prentice Hall, 1997, ISBN 978-0-13-629155-8. Establishes command-query separation and design-by-contract foundations.
3. Martin Fowler, [“CQRS”](https://martinfowler.com/bliki/CQRS.html), 2011, accessed 2026-08-28. Distinguishes command/write and query/read models while warning about added complexity.
4. R. Fielding, M. Nottingham, and J. Reschke, [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), IETF Standards Track, June 2022. Defines method semantics, idempotency, conditional requests, and retry constraints.
5. Cloud Native Computing Foundation, [CloudEvents Specification](https://cloudevents.io/), version 1.0 family, accessed 2026-08-28. Provides a portable event-envelope standard useful for distinguishing facts from commands.
6. Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, ISBN 978-1-4493-7332-0. Provides logs, transactions, replication, ordering, messaging, and distributed consistency foundations.
7. Michael Nygard, *Release It!*, second edition, Pragmatic Bookshelf, 2018, ISBN 978-1-68050-239-8. Provides production reasoning for timeouts, retries, capacity, stability, and recovery.

## Exercises

### Exercise 1

Trace the executable account handler, including same-payload replay and the unprinted different-payload ID conflict. State all unproved claims.

### Exercise 2

Design a complete envelope and state machine for asynchronous `PublishDocument` commands with status queries and events.

### Exercise 3

Specify a transactional idempotency/outbox handler and enumerate crash points before and after every durable transition.

### Exercise 4

Design version migration, quarantine, and replay for three historical command schemas while preserving audit provenance.

### Exercise 5

Review a remote command protocol for an unfamiliar safety-critical actuator without claiming functional safety.

## Answers to the Exercises

### Answer 1

`cmd-1` matches version zero, deposits 500, advances balance 1,000→1,500 and version 0→1, then stores the payload/result. Its identical replay finds the stored tuple and returns `accepted` without mutation. `cmd-2` matches version one but 2,000 exceeds balance, so stores `rejected` without version change. `cmd-3` expects zero while current version is one, so stores `conflict` without mutation. Reusing `cmd-1` with any different `(kind,amount,expected)` returns `id-conflict` before execution.

The trace does not prove concurrent claim isolation, atomic result/state persistence, durable storage, exact money arithmetic/currency, authorization, queue delivery, outbox publication, deadline/cancellation, retention, crash recovery, or financial correctness. Storing rejected/conflict outcomes forever is only one policy; production retention/re-evaluation semantics must be explicit.

### Answer 2

Envelope fields include command ID, type `PublishDocument`, schema version, tenant, document ID, base version, immutable content/provenance digest or durable content reference, publication policy/version, actor authentication reference/delegated capability, idempotency key, correlation/causation, created time, absolute deadline, trace carrier, and integrity metadata. Trust and retention classification is explicit; roles are not accepted from payload.

States are `received → rejected` or `accepted → validating/executing → committed → indexing/notifying → completed`, with `conflict`, `expired`, `cancelled`, `compensating`, `compensated`, `failed`, and `indeterminate` where mechanisms justify them. Acceptance atomically stores command/result state plus publication intent. Status query returns operation version and progress; domain events state accepted/completed/failed facts with stable IDs. Recheck authorization/base version at execution, make index/notification idempotent, pass one deadline, and define cancellation before/after commit separately.

### Answer 3

In one serializable transaction: insert/claim scoped `(tenant,type,id)` with payload digest if absent; on existing same digest return/resume its state, and on different digest conflict. Load target with expected version, authorize/validate, update state/version, store terminal or durable-progress result, and append outbox records. Commit is the logical acceptance/effect boundary. A publisher later claims outbox rows, publishes with stable event ID, and marks delivery progress; consumers deduplicate by event ID.

Crash before transaction begins leaves nothing. During claim/validation/update/outbox before commit rolls back. After commit but before response leaves durable result for replay. Before publish leaves pending outbox; after broker accepts but before mark can duplicate publish, so consumer idempotency is required. After mark but before external observation is a delivery-contract issue. Test concurrent duplicate/conflicting claims, deadlock/serialization retry, connection loss around commit, publisher crash at every point, broker duplicates/reorder, poison event, restart, and reconciliation between state/result/outbox.

### Answer 4

Keep immutable original bytes/envelope, schema ID/version, ingestion digest/signature, source, timestamps, and every upcaster version. Use allowlisted deterministic chains `v1→v2→v3→current`; validate at each boundary and produce an owned current command plus migration report. Never overwrite archived original evidence. Golden fixtures cover valid, boundary, malformed, unknown-field, encoding, unit/currency, default, and removed-enum cases; differential tests compare historical handler behavior where required.

Unknown/unmigratable commands enter encrypted access-controlled quarantine with bounded retention, reason code, alert, and no infinite retry. A named operator approves repaired mapping or terminal rejection; redrive creates an auditable attempt linked to the original ID and preserves idempotency. Roll out upcasters in shadow/dry-run over a representative archive, compare counts/digests/outcomes, canary workers, and retain rollback to prior handlers. Security review covers parser depth/size, arbitrary-type construction, signature/provenance, and sensitive data.

### Answer 5

Envelope includes authenticated controller/operator identity, asset and topology/configuration generation, command type/version, exact units and bounds, sequence/idempotency identity, preconditions, allowed mode/window, deadline, and integrity protection. The actuator reports explicit rejected, accepted, confirmed, failed, and indeterminate knowledge states. Do not auto-retry an indeterminate actuation unless a validated device protocol provides authenticated sequence semantics and queryable reconciliation. Cancellation after acceptance is a separate safe-state command when supported.

Independent firmware/hardware interlocks, limits, alarms, and fail-safe behavior remain authoritative below application commands. Evidence requires traceable requirements/hazard/common-cause analysis, formal/state/timing and dimensional analysis where tractable, protocol and authorization threat review, static analysis, independent implementation review, simulator/digital-twin and hardware-in-the-loop tests, loss/duplicate/reorder/delay/partition/restart/power/resource faults, operator/human-factors exercises, and controlled deployment/recovery. Named domain, controls/real-time, functional-safety, hardware, cybersecurity, human-factors, quality, regulatory, operations, reliability, and independent verification authorities approve. This chapter establishes no functional safety, physical exactly-once behavior, or deployment suitability.
