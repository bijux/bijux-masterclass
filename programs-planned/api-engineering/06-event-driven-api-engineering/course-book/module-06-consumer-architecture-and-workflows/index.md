# Module 06 — Consumer Architecture and Asynchronous Workflows

> **Program stage:** Course 6 of 6 — Extend the promise across asynchronous time.

> **Central question:** How do idempotent consumers, projections, and process managers coordinate asynchronous workflows without hidden synchronous coupling?

## Where this module fits

A consumer is not a callback attached to a topic. It is an application with an owner, accepted message
versions, durable state, transaction boundaries, deadlines, retry policy, observability, release process,
and recovery procedure. Treating handlers as anonymous functions produces systems that are easy to start
and difficult to operate.

Some consumers build projections. Some create one external effect. Some coordinate a long-running process
across several facts and commands. Those responsibilities should not be collapsed. A projection can usually
rebuild from history with side effects disabled. A notification consumer cannot “rebuild” sent emails. A
process manager owns workflow state and emits commands; it must not pretend that commands succeeded until
corresponding facts arrive.

This module also resolves the false choice between orchestration and choreography. Pure choreography can
hide the business process in subscriptions spread across teams. Central orchestration can become a
controlling distributed monolith. The right design assigns one owner to a process that genuinely requires
coordination while allowing independent reactions to facts that do not belong in that process.

## Capstone result

Build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state.

Implement three independent consumers and one process manager:

```text
notification-v1   → one outbound notification intent per completed run
analytics-v1      → replayable completion/failure projection
audit-v1          → append-only safe audit projection
run-process-v1    → requested → started → completed/failed workflow state
```

Each consumer has a catalogue entry, group identity, accepted types, effect version, ordering requirement,
retry/dead-letter policy, replay mode, and owner.

## Learning outcomes

- treat a consumer as a versioned application rather than a handler function
- separate projections, external effects, and process coordination
- choose orchestration, choreography, or a hybrid from ownership and failure needs
- model process-manager transitions idempotently from facts
- emit commands without assuming that the requested action succeeded
- use correlation and causation to reconstruct asynchronous workflows
- handle out-of-order facts without inventing global broker order
- define timeouts and compensations as explicit process decisions

## Core event model

### 1. Consumer identity includes effect and version

A stable group name tells the broker which instances share delivery progress. An effect identity tells the
application which durable outcome is deduplicated. A deployment version tells operators which code is
running. These may be related but should not be collapsed into one string.

`analytics-v1` can have many replicas in one group and one effect version. `analytics-v2` may run
alongside it with a separate group, inbox identity, and projection. A rolling deployment of v1 does not
create a new logical effect; it preserves compatible state and group identity.

The consumer catalogue records these distinctions so a new replica cannot accidentally start from the
beginning or share a group with an unrelated effect.

### 2. Projection consumers and side-effect consumers need different replay rules

An analytics projection is derived state. It can be rebuilt into a new target from retained events. An
audit projection may also be rebuildable if it is not itself the legal record. A notification consumer
creates an external, human-visible effect that should not repeat during ordinary replay.

Use capability boundaries: replay-mode analytics receives a projection writer but no email adapter.
Notification’s inbox retains permanent effect identity and replay policy defaults to skip.

Lab and runbook instructions must not say “replay the consumer” without naming which effect and side
effects are permitted.

### 3. A process manager owns a specific long-running outcome

The run process manager correlates facts for one run and records an explicit state machine. It may emit a
`StartAnalysis` command after `AnalysisRunRequested`, start a timeout, and await `AnalysisRunStarted`.
It moves to completed only after the authoritative completion event.

The process manager is not the owner of run truth; the control plane remains authoritative. It owns the
coordination state: which expected facts arrived, which commands were issued, and which deadline or
compensation is pending.

Persist process state and emitted-command outbox rows atomically. Otherwise a crash can advance state
without issuing the command or issue the command twice without a stable identity.

### 4. Choreography is appropriate for independent reactions

Analytics and audit can subscribe independently to completion because neither controls the other and
their failure does not alter the fact. Forcing them through one central workflow service adds coupling
without clarifying ownership.

Choreography becomes opaque when a business outcome depends on a chain of implicit reactions:
A emits, B emits, C waits for B, D compensates C. No component owns the total process or timeout. In that
case, introduce a process manager whose state and decisions are explicit.

Use choreography for independent consequences; use orchestration for a coordinated outcome with
deadlines, alternatives, or compensation.

### 5. Commands and facts form a protocol

A process manager emits a command with stable command ID, target, subject, correlation, causation, and
idempotency identity. The target either rejects it through a command-result channel or later emits an
authoritative fact. The manager cannot update its state to “started” merely because it published
`StartAnalysis`.

Duplicate commands are expected after uncertainty. The command handler applies Course 2 idempotency and
records one accepted result. The resulting fact references the command as causation.

Commands require expiry or deadline semantics when action after a certain time would be harmful.

### 6. Out-of-order handling uses state and prerequisites

Cross-partition or cross-channel facts may arrive in an order different from business causation. A
process manager should check whether a transition’s prerequisites are already known, buffer a bounded
pending fact, query authoritative state under policy, or mark an inconsistency for reconciliation.

Silently sorting by timestamp is unsafe: clocks skew, timestamps may represent event time rather than
commit order, and a late fact can be legitimate. Discarding “old” events without a version/state rule
can lose corrections.

The run process uses one run partition for lifecycle facts, reducing but not eliminating reorder with
artifact events on another channel.

### 7. Timeouts are domain events, not sleeping threads

A process waiting for `AnalysisRunStarted` needs a durable deadline. A scheduler emits or records a
timeout fact/command when the deadline expires. The process manager evaluates it against current state
and a timeout generation so a late timer cannot fail a process already advanced.

`sleep(300)` in a handler loses the wait on restart and consumes resources. Broker redelivery delay is
not a general workflow timer because it couples process state to one delivery attempt.

Timeout actions may retry, compensate, escalate, or mark uncertainty. They should not infer that the
requested remote action definitely did not occur.

### 8. Compensation is a new action, not rollback through time

Distributed effects cannot usually be rolled back atomically. A compensation requests a new state
transition that mitigates or reverses a prior effect where business rules allow it. It may fail and need
its own retries and evidence.

Cancelling a queued run is possible; deleting an already delivered email is not. Refunding a charge is a
new financial fact, not erasure of the charge. The process model must name which effects are
compensatable and which require reconciliation or human handling.

A saga diagram without compensation failure paths is incomplete.

## Engineering requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Consumer catalogue | Every consumer names owner, group, effect version, accepted types, replay, and failure policy. | Anonymous handlers cannot be deployed or recovered safely. | Consumer catalogue |
| Effect separation | Projection, external effect, and process coordination use distinct consumers/transactions. | Replay repeats side effects or workflow state becomes inseparable. | Architecture map and inbox identities |
| Explicit process state | Long-running coordinated outcomes have a durable state machine. | Business flow is hidden in subscription chains. | Process transition table |
| Command-result discipline | Publishing a command does not mark the requested action complete. | Workflow advances on intent rather than fact. | Causation and transition tests |
| Durable timer | Timeout has deadline, generation, owner, and idempotent handling. | Sleep-based waits disappear or fire stale actions. | Timer record and stale-timeout test |
| Bounded reorder | Out-of-order policy buffers, reconciles, or rejects with limits. | Timestamp sorting invents order or memory grows without bound. | Reorder vectors |
| Compensation semantics | Every compensation is a new command/fact with its own failure policy. | Distributed rollback is assumed. | Workflow failure table |

## Worked failures

### Case 1 — notification and analytics shared one consumer

Replay was needed for analytics, but the combined handler also resent emails. Split projection and
external-effect consumers, give them separate groups/inboxes, and deny outbound capability during
analytics replay.

### Case 2 — process advanced after command publish

The manager moved to started after sending `StartAnalysis`. The command was later rejected. Keep state at
start-requested and advance only on `AnalysisRunStarted` or an explicit rejection result.

### Case 3 — timestamp sorting hid a late correction

A consumer dropped a correction because its event time preceded the latest completion timestamp. Treat
correction semantics explicitly; event time does not make the fact obsolete.

### Case 4 — timeout fired after completion

A durable timer from an earlier process generation emitted a failure after the run completed. Include
process generation and evaluate current state transactionally; stale timeout becomes a no-op with
evidence.

## Python implementation

`RunProcessManager` models allowed transitions and ignores duplicate facts idempotently.

```text
capstone/tracks/python-fastapi/src/event_engineering/workflows.py
capstone/tracks/python-fastapi/src/event_engineering/inbox.py
capstone/event-case/consumer-catalog.yaml
```

The application layer receives a validated event, obtains the effect-scoped inbox transaction, loads process
state, checks transition prerequisites, updates state, and writes any outbound command to an outbox before
acknowledgement.

Use pure state-transition tests for legal, duplicate, stale, and impossible inputs. Use database tests for
concurrent duplicates and command-outbox atomicity.

## TypeScript implementation

The TypeScript reference keeps the same state table but may express it with discriminated unions and
exhaustive internal transitions. Public event types still require an unknown-version boundary before the
exhaustive switch.

Avoid spawning untracked promises from a handler. A handler may acknowledge only after its owned transaction
and durable outbound intent complete. Process timer scheduling must return a durable identifier, not a
JavaScript timer handle.

The comparative exercise maps one Python transition test to idiomatic TypeScript without forcing identical
class layout.

## Cross-language invariant

Both tracks must reach the same process state for every shared event trace, issue commands with the same
stable logical IDs, classify duplicates and stale timers identically, and keep notification, analytics, and
audit effects independent. Internal state representation may differ.

## Design review

Draw each consumer as a box with inputs, owned state, outputs, transaction boundary, replay policy, and
external capabilities. Then draw the process manager separately. If two boxes write the same owned state or
one handler has unrelated effects, revisit the boundary.

For each workflow transition, list the authoritative input fact, current allowed states, new state, optional
command, deadline change, duplicate result, and impossible-state action.

## End-to-end worked example

`AnalysisRunRequested` enters `run-process-v1`. The process transaction records state `requested`, writes a
`StartAnalysis` command outbox row with command ID derived from run and process generation, and schedules a
start deadline. Duplicate requested events find the inbox and do nothing.

The control plane accepts the command idempotently and later publishes `AnalysisRunStarted` caused by that
command. The process advances and cancels the active deadline. `AnalysisRunCompleted` transitions to
terminal, while analytics and notification independently apply their effects.

If the start deadline arrives first, the process checks current generation and state. It may issue a status
reconciliation command or cancellation, but it does not assert that the control plane failed merely because
an event was delayed.

## Failure patterns

- **Callback consumer.** A handler has no explicit owner, state, effect identity, or recovery policy.
- **Mixed effects.** Projection rebuild and external notification live in one transaction/handler.
- **Choreography fog.** No component owns a multi-step outcome or deadline.
- **Command optimism.** Publishing intent is treated as successful completion.
- **Sleep timer.** Workflow timing exists only in process memory.
- **Timestamp ordering.** Clock values are used as a substitute for causal/state rules.
- **Compensation fantasy.** A new distributed action is described as atomic rollback.

## Module synthesis

Build notification, analytics, audit, and orchestration consumers with stable derived-command identities and explicit state. The central distinction is this: how do idempotent consumers, projections, and process managers coordinate asynchronous workflows without hidden synchronous coupling? The checkpoint is complete only when the mechanism, failure, oracle, and evidence limitation can all be explained together.

## Next in the story

Consumer architecture explains who processes facts, but continuous analytics introduces another time model.
Module 07 distinguishes event time from processing time, defines windows and watermarks, handles late data
and corrections, and makes stream-state replay deterministic.
