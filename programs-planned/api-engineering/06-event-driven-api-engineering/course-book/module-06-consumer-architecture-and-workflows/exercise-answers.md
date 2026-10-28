# Reference Answers — Module 06: Worked answers — Module 06 — Consumer Architecture and Asynchronous Workflows

Read after attempting all twelve Consumer Architecture and Asynchronous Workflows exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Classify four consumers

Analytics is a replayable projection, e.g. `analytics-completion:v1`. Notification is an external-effect consumer, `notification-completion:v1`. Audit is an append-only safe projection/sink, `audit-events:v1`. Run coordination is a process manager, `run-process:v1`. Separate identities prevent replay or dedupe rules from crossing effects.

## 2. Choose choreography

Completion is already an authoritative fact. Analytics and audit own independent derived outcomes and neither requires the other’s success. A central orchestrator would add availability and deployment coupling without clarifying a shared process. Separate groups let each recover independently.

## 3. Choose orchestration

Start, timeout, cancellation, and reconciliation are one coordinated outcome with alternatives and durable deadlines. Scattering those decisions among event reactions hides state and ownership. A process manager records the workflow while the control plane remains owner of run truth.

## 4. Model command state

Before publication the process is `requested`. In the transaction that creates the command outbox it becomes `start-requested`, not started. Only `AnalysisRunStarted` moves it to `running`. An explicit command rejection moves it to a defined blocked/failed path according to policy.

## 5. Handle rejection

The command handler should publish or return a versioned rejection/result fact tied to command ID, run, reason code, and authority. The process manager moves from start-requested to blocked or failed, clears the timer, and may emit a user-facing problem/notification. It must not infer rejection from timeout alone.

## 6. Design a durable timer

Use `(processId, timerKind, generation)` as identity, store deadline and expected current state, and emit a timeout command/fact once. On fire, lock process state and compare generation/state. If advanced or terminal, record stale no-op; otherwise apply the timeout transition and durable outputs.

## 7. Handle out-of-order events

Artifact publication can update an artifact projection independently because it owns artifact facts. A process manager that requires completion should not infer completion from the artifact. It may store a bounded pending reference or reconcile authoritative state. The right choice depends on whether the workflow requires the relationship.

## 8. Separate replay policy

Analytics: rebuild into isolated target, side effects disabled. Notification: skip by existing inbox unless an explicit reissue operation is approved. Audit: replay only if it is a derived copy, not if it is the legal immutable log. Process manager: generally rebuild into isolated state or reconcile; do not reissue historical commands.

## 9. Plan compensation

Issue an idempotent `CancelAnalysis` command if the run state permits cancellation. The owner emits `AnalysisRunCancelled` or a rejection fact. If computation or delivery already completed, record the non-compensatable outcome and escalate policy rather than deleting history.

## 10. Avoid command duplication

The process-state update and command outbox row commit together with a stable command ID. Recovery republishes the same command ID if needed. The command handler’s idempotency record returns the original acceptance/rejection, so two deliveries produce one logical command effect.

## 11. Version a consumer

Use group `analytics-v2`, effect `analytics-completion:v2`, new projection target, and independent inbox. Replay/catch up, compare with v1, then switch readers by a versioned configuration. Keep v1 group/target for rollback until the window closes.

## 12. Draw a consumer contract

Inputs: completed/failed events v1. State: inbox plus notification intent/delivery records. Output: `SendCompletionEmail` command outbox. Transaction: inbox + intent. Deadline/retry: bounded dispatcher policy. Recovery: duplicate-safe replay skipped, dead-letter runbook, reconciliation against completed runs. Owner and tenant policy are explicit.
