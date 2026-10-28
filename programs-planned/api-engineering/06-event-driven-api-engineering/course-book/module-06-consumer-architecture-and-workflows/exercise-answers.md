# Worked Answers — Module 06: Consumer Architecture and Asynchronous Workflows

Use these solutions to audit your reasoning for **Consumer Architecture and Asynchronous Workflows**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Classify four consumers

Analytics is a replayable projection, e.g. `analytics-completion:v1`. Notification is an external-effect consumer, `notification-completion:v1`. Audit is an append-only safe projection/sink, `audit-events:v1`. Run coordination is a process manager, `run-process:v1`. Separate identities prevent replay or dedupe rules from crossing effects.

The chapter’s decisive distinction is this: An analytics projection is derived state. It can be rebuilt into a new target from retained events. An audit projection may also be rebuildable if it is not itself the legal record. A notification consumer creates an external, human-visible effect that should not repeat during ordinary replay.

## 2. Choose choreography

Completion is already an authoritative fact. Analytics and audit own independent derived outcomes and neither requires the other’s success. A central orchestrator would add availability and deployment coupling without clarifying a shared process. Separate groups let each recover independently.

In the cumulative capstone, the rule becomes concrete: Analytics and audit can subscribe independently to completion because neither controls the other and their failure does not alter the fact. Forcing them through one central workflow service adds coupling without clarifying ownership.

## 3. Choose orchestration

Start, timeout, cancellation, and reconciliation are one coordinated outcome with alternatives and durable deadlines. Scattering those decisions among event reactions hides state and ownership. A process manager records the workflow while the control plane remains owner of run truth.

A useful way to reason about the boundary is: The process manager is not the owner of run truth; the control plane remains authoritative. It owns the coordination state: which expected facts arrived, which commands were issued, and which deadline or compensation is pending.

## 4. Model command state

Before publication the process is `requested`. In the transaction that creates the command outbox it becomes `start-requested`, not started. Only `AnalysisRunStarted` moves it to `running`. An explicit command rejection moves it to a defined blocked/failed path according to policy.

The implementation consequence is: AnalysisRunRequested enters run-process-v1. The process transaction records state requested, writes a StartAnalysis command outbox row with command ID derived from run and process generation, and schedules a start deadline. Duplicate requested events find the inbox and do nothing.

## 5. Handle rejection

The command handler should publish or return a versioned rejection/result fact tied to command ID, run, reason code, and authority. The process manager moves from start-requested to blocked or failed, clears the timer, and may emit a user-facing problem/notification. It must not infer rejection from timeout alone.

The important nuance is: A process manager emits a command with stable command ID, target, subject, correlation, causation, and idempotency identity. The target either rejects it through a command-result channel or later emits an authoritative fact. The manager cannot update its state to “started” merely because it published StartAnalysis.

## 6. Design a durable timer

Use `(processId, timerKind, generation)` as identity, store deadline and expected current state, and emit a timeout command/fact once. On fire, lock process state and compare generation/state. If advanced or terminal, record stale no-op; otherwise apply the timeout transition and durable outputs.

Under concurrency or failure, the distinction becomes: A process waiting for AnalysisRunStarted needs a durable deadline. A scheduler emits or records a timeout fact/command when the deadline expires. The process manager evaluates it against current state and a timeout generation so a late timer cannot fail a process already advanced.

## 7. Handle out-of-order events

Artifact publication can update an artifact projection independently because it owns artifact facts. A process manager that requires completion should not infer completion from the artifact. It may store a bounded pending reference or reconcile authoritative state. The right choice depends on whether the workflow requires the relationship.

The design remains honest only if: Cross-partition or cross-channel facts may arrive in an order different from business causation. A process manager should check whether a transition’s prerequisites are already known, buffer a bounded pending fact, query authoritative state under policy, or mark an inconsistency for reconciliation.

## 8. Separate replay policy

Analytics: rebuild into isolated target, side effects disabled. Notification: skip by existing inbox unless an explicit reissue operation is approved. Audit: replay only if it is a derived copy, not if it is the legal immutable log. Process manager: generally rebuild into isolated state or reconcile; do not reissue historical commands.

The consumer-facing consequence is: Draw each consumer as a box with inputs, owned state, outputs, transaction boundary, replay policy, and external capabilities. Then draw the process manager separately. If two boxes write the same owned state or one handler has unrelated effects, revisit the boundary.

## 9. Plan compensation

Issue an idempotent `CancelAnalysis` command if the run state permits cancellation. The owner emits `AnalysisRunCancelled` or a rejection fact. If computation or delivery already completed, record the non-compensatable outcome and escalate policy rather than deleting history.

The operational consequence is: Cancelling a queued run is possible; deleting an already delivered email is not. Refunding a charge is a new financial fact, not erasure of the charge. The process model must name which effects are compensatable and which require reconciliation or human handling.

## 10. Avoid command duplication

The process-state update and command outbox row commit together with a stable command ID. Recovery republishes the same command ID if needed. The command handler’s idempotency record returns the original acceptance/rejection, so two deliveries produce one logical command effect.

The strongest engineering interpretation is: The control plane accepts the command idempotently and later publishes AnalysisRunStarted caused by that command. The process advances and cancels the active deadline. AnalysisRunCompleted transitions to terminal, while analytics and notification independently apply their effects.

## 11. Version a consumer

Use group `analytics-v2`, effect `analytics-completion:v2`, new projection target, and independent inbox. Replay/catch up, compare with v1, then switch readers by a versioned configuration. Keep v1 group/target for rollback until the window closes.

The defect-oriented view is: analytics-v1 can have many replicas in one group and one effect version. analytics-v2 may run alongside it with a separate group, inbox identity, and projection. A rolling deployment of v1 does not create a new logical effect; it preserves compatible state and group identity.

## 12. Draw a consumer contract

Inputs: completed/failed events v1. State: inbox plus notification intent/delivery records. Output: `SendCompletionEmail` command outbox. Transaction: inbox + intent. Deadline/retry: bounded dispatcher policy. Recovery: duplicate-safe replay skipped, dead-letter runbook, reconciliation against completed runs. Owner and tenant policy are explicit.

Across the Python and TypeScript tracks, the invariant is: If the start deadline arrives first, the process checks current generation and state. It may issue a status reconciliation command or cancellation, but it does not assert that the control plane failed merely because an event was delayed.
