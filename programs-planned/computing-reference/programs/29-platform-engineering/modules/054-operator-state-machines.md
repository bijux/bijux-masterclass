---
module_id: PLAT-054
program: Platform Engineering
level: 2
module_number: 54
title: Operator State Machines
status: complete
last_verified: 2026-09-02
---

# Operator State Machines

## One-Page Review

### Governing question

How should an operator represent and execute long-running, failure-prone lifecycle workflows so every transition is authorized, guarded, recoverable, observable, compatible with changing desired state, and safe to repeat after a crash?

### Essential definitions

- A **state machine** consists of states, initial state/configuration, events or observations, guarded transitions, actions, and terminal or continuing configurations.
- **control state** records where a workflow is in its protocol; **domain state** records facts about the managed system; neither is identical to one display phase.
- A **guard** is a predicate that must hold before a transition; an **invariant** must hold in every reachable state.
- A **transition action** changes durable control data or the external world; it can partially succeed even when its caller receives failure.
- A **terminal state** ends one workflow execution as succeeded, failed, cancelled, or superseded; the long-lived resource can still be reconciled later.
- **orthogonal state** represents independent dimensions—such as availability, backup, traffic, and upgrade—without forcing their Cartesian product into hand-named phases.
- **supersession** marks an in-flight plan obsolete because newer desired state owns the next outcome.
- **compensation** is a domain-specific action that mitigates a completed step; it is not transaction rollback and may be impossible.
- A **durable checkpoint** preserves enough transition identity, inputs, and effect evidence for another process/version to resume safely.
- **safety** means prohibited states/actions never occur; **liveness** means required progress eventually occurs under explicit fairness and environment assumptions.

### Central model, mechanism, or theorem

Model an operator workflow as $M=(S,S_0,E,G,A,\delta)$ with legal states $S$, initial set $S_0$, observations/events $E$, guards $G$, actions $A$, and transition relation $\delta\subseteq S\times E\times G\times A\times S$. A safety invariant $I$ is established initially and preserved by every reachable transition: $I(s)\land T(s,s')\Rightarrow I(s')$. This induction proves safety only if the modeled state/action boundary is complete. Liveness such as eventual terminal outcome additionally needs fair scheduling, eventually resolved dependencies, bounded retry semantics, and an attainable target. If independent dimensions have sizes $n_1,\ldots,n_k$, a naive combined phase space has $\prod_i n_i$ configurations; explicit legal combinations and orthogonal conditions prevent accidental state explosion.

### Critical invariants

- Consumer desired state, observed domain facts, workflow control state, and human-facing conditions remain distinct and generation-correlated.
- Every effectful transition has a stable operation identity, precondition/guard, durable before/after evidence, bounded retry policy, and unknown-outcome path.
- The next step is derived from current durable state and observations; process memory and event order are never the sole workflow record.
- At most one authority advances a workflow step, while stale leaders and delayed provider requests are contained by conditional writes, fencing where possible, and idempotency.
- New desired generations explicitly continue, restart, branch, compensate, or supersede in-flight work; obsolete destructive plans never proceed silently.
- Pause, cancel, delete, retry, force, rollback, and resume have defined legal states, authority, response latency, and irreversible boundaries.
- Timeouts classify lack of evidence rather than pretending an external action failed; deadlines and timers survive restart.
- Status conditions describe current observations; a compact phase or step never becomes the only source of truth for readiness, failure, or progress.
- Workflow-definition upgrades can interpret every persisted state, correlation, timer, and effect created during the supported skew window.
- Safety, liveness, reachability, terminality, compensation, crash boundaries, and retirement are tested from generated/model traces and real integrations.

### Common failures

Encoding the whole lifecycle in one `phase` string; treating conditions as mutually exclusive steps; storing progress only in local memory; running a multi-hour action inside one reconcile; writing “next phase” before an effect without correlation or after an effect without recovery evidence; retrying timeout as definite failure; allowing two leaders to advance the same step; continuing generation 4 replacement after generation 5 changes strategy; equating cancel request with effect cancellation; compensating irreversible deletion with recreation; letting poison workflows occupy all workers; resetting deadlines on restart; making `Failed` permanent when changed intent could repair it; changing enum values underneath stored objects; replaying nondeterministic workflow code; exposing secret activity output in status; and deleting an operator while states, timers, finalizers, or effects remain.

### Compact example

A database upgrade workflow persists `workflowID`, desired generation, definition revision, target version, current step, attempt, deadlines, provider operation IDs, and verified checkpoints. `Planning` validates compatibility and backup requirements. `BackingUp` submits one correlated job, then later observes integrity. `ProvisioningReplica` and `Replicating` preserve the old primary. `SwitchingTraffic` has a guarded commit point: replica healthy, lag bounded, approval current, and desired generation unchanged. A timeout becomes `OutcomeUnknown`, not a second switch. New intent before the commit point supersedes safely; after it, the machine chooses forward completion or explicit reverse traffic, not imaginary rollback. Conditions independently report `Ready`, `Progressing`, `BackupVerified`, and `Degraded`. Any leader can resume from durable evidence; old binaries are prevented from processing states they cannot understand.

### Connections

This module builds on reconciliation from [PLAT-052](052-desired-state-and-reconciliation.md), CRD persistence/versioning from [PLAT-053](053-custom-resource-definitions.md), workload controllers from [PLAT-024](024-pods-workloads-and-controllers.md), and upgrade policy from [PLAT-049](049-upgrade-and-deprecation-policies.md). PLAT-055 and PLAT-056 deepen idempotent effects and deletion, while PLAT-057 through PLAT-060 apply state reasoning to status, dependencies, recovery, and domain APIs.

## Governing Question

How can an operator make a complex lifecycle—provision, restore, upgrade, fail over, rotate, scale, or delete—durable and comprehensible when steps are asynchronous, desired state changes, processes restart, effects become ambiguous, and some transitions cannot be reversed?

A reconciliation loop can repeatedly compare desired and observed state, but a complex workflow also needs memory of protocol decisions. A database replacement must know which candidate was created, which backup was verified, whether traffic switched, and which irreversible boundary was crossed. Recomputing blindly from a broad phase can repeat damage; relying on an in-memory call stack loses work on restart.

An explicit state machine makes legal progress, guards, effects, failure, and recovery reviewable. It should remain subordinate to current desired state and observation. Otherwise it becomes an imperative script embedded inside a declarative API, continuing obsolete actions because a stale step says so.

## Why This Matters

Operators encode specialist operational knowledge and execute it repeatedly with privileged access. A missing transition or ambiguous retry can duplicate infrastructure, corrupt data, expose traffic prematurely, strand deletion, or block every resource managed by the controller.

Long workflows cross many failure boundaries. Kubernetes API writes, provider requests, Jobs, callbacks, watches, leader leases, and process restarts can fail independently. There is no atomic transaction spanning them. Durable state and effect correlation are required at every boundary.

Desired state is not static during execution. Users fix mistakes, automation changes scale, incidents request pause, and policy invalidates a target. The workflow must say when new intent can retarget safely, when it supersedes an execution, and when a commit point requires forward recovery.

Status design affects human safety. One `Upgrading` phase cannot simultaneously express that the old service remains ready, backup is verified, traffic has not switched, and the candidate is degraded. Orthogonal conditions preserve those facts.

Upgrades of the operator itself replay the past through new code. Persisted enum states, operation payloads, timers, and correlations become compatibility APIs even when declared only in `status`.

## Prerequisites and Retrieval

Retrieve finite-state machines, statecharts, transition systems, safety/liveness, invariants and induction, graph reachability, guards/actions, hierarchical/orthogonal states, desired-state reconciliation, spec/status and conditions, optimistic concurrency, leader election/fencing, idempotency, timeouts/retries/backoff, queues, external consistency, long-running operations, sagas/compensation, cancellation, deadlines/timers, event sourcing and replay, deterministic durable workflows, schema evolution, progressive delivery, backup/restore, incident operations, authorization, audit, and decommissioning.

You should distinguish resource lifecycle from one workflow execution; desired/domain/control/display state; observation event from durable fact; phase from condition; guard from validation; retry from loop transition; timeout from known failure; cancellation request from cancellation completion; compensation from rollback; terminal workflow from permanently terminal resource; concurrency control from exactly-once effects; deterministic decision replay from idempotent activity; safety from liveness; reachability from production likelihood; and a diagram from an executable/verifiable specification.

## Learning Objectives

After completing this module, you should be able to:

1. model operator workflows as legal states, transitions, guards, effects, terminal outcomes, and invariants;
2. separate desired, observed domain, durable control, operation, and human-facing condition state;
3. design crash-safe transition protocols for synchronous, asynchronous, ambiguous, and irreversible effects;
4. handle generation change, supersession, pause, resume, cancellation, deletion, force, and compensation;
5. use orthogonal/hierarchical state without uncontrolled Cartesian-product phases;
6. persist timers, attempts, deadlines, approvals, correlations, and definition versions safely;
7. coordinate workers/leaders with conditional writes, fencing, idempotency, and fair scheduling;
8. evolve workflow definitions and persisted states across rolling upgrade, rollback, restore, and retirement; and
9. verify safety, liveness assumptions, reachability, crash boundaries, and domain outcomes with models and tests.

## Core Exposition

### Begin with the domain protocol, not enum names

Describe the lifecycle in domain verbs and facts: requested, admitted, backup required, backup verified, candidate created, data synchronized, cutover authorized, traffic switched, old resource retained, cleanup complete. Identify irreversible effects and externally observable commitments.

List actors and authority: consumer, operator controller, admission/policy, provider, workload agent, approver, incident commander, and successor controller. A legal transition names who may cause it and which evidence is trusted.

Write safety properties before the graph. Examples: never direct traffic to an unverified candidate; never delete the only recoverable copy; never advance an approval-bound step with expired approval; never use an operation from another resource UID; never remove the finalizer before all deletion obligations are dispositioned.

Then define progress goals and environment assumptions. “Every admitted upgrade eventually succeeds or reports terminal failure” requires scheduled workers, available dependencies, an attainable target, bounded human wait, and a response from external systems. Without those assumptions, surface `Blocked` or `Unknown` rather than promising liveness.

### Separate four state layers

Desired state belongs in spec or another consumer-owned input. It says the requested target and policies, not `currentStep: SwitchTraffic`. Consumers may request pause/cancel through a dedicated field or operation API, but should not mutate controller internals.

Domain state is observed reality: versions running, replication lag, backup integrity, routes, credentials, provider operations, and health. Qualify it by source, revision, and time.

Control state records protocol memory that cannot be reconstructed cheaply or safely: workflow identity, generation/definition revision, selected strategy, current checkpoint, effect correlations, attempts, deadlines, approval token, commit point, and disposition. Store only what is durable and needed for recovery.

Presentation state summarizes for people and automation. Conditions express orthogonal facts with observed generation and stable reasons. A phase/step can be a compact diagnostic, but it must not replace the facts and cannot silently drive effects without rechecking guards.

### Define legal transitions explicitly

Represent each transition as source configuration, trigger/observation, guard, action, target, status/condition changes, retry/timeout, and audit class. Include negative paths, not just the happy sequence.

Guards inspect current authoritative facts: resource UID/generation, ownership, approval validity, backup evidence, candidate health, policy, lease/fence, provider state, and deletion/cancel request. Re-evaluate immediately before an irreversible action.

Transitions should be deterministic given recorded inputs and observations where possible. If several transitions are enabled, define priority or prove commutativity. Hidden iteration order is not policy.

Make illegal states unrepresentable or detectable. Reject unknown state enum values only if downgrade/forward-compatibility behavior is defined. Otherwise an old controller can corrupt a state written by a new controller; safer behavior is often to stop with `UnsupportedWorkflowRevision`.

### Use guarded state advancement around effects

There is no universal choice between persisting before or after an external call. Persisting “done” before action can skip an effect after crash. Acting first and persisting later can duplicate it. Use a protocol with stable operation identity and intermediate intent/evidence.

Before an effect, persist the workflow/generation, step intent, operation/idempotency identity, request digest, authority epoch, attempt/deadline, and preconditions. Submit the effect. Later observe its result by stable identity and persist verified completion before advancing.

For a synchronous idempotent API, submission and observation may happen in one reconcile, but crash tests must still cover the gap. For asynchronous work, create a Job/operation and return; watch or poll it later rather than holding a worker.

If the response is lost, enter or report outcome unknown. Do not transition to failure merely from timeout and do not submit a new non-idempotent effect until observation resolves or an authorized risk decision is recorded.

### Derive next work from state and current intent

The persisted step is a checkpoint, not a command to execute unconditionally. Every reconcile reads the latest desired generation and deletion/pause/cancel state, observes relevant effects, validates ownership, and decides the next legal transition.

An event only enqueues the workflow. Duplicate, reordered, or missing events must not cause illegal progression. Timed resync and direct observation repair lost signals.

Use compare-and-swap/resource-version writes so two workers cannot both claim advancement from the same state. After conflict, discard the proposed transition and recompute from current data.

The state machine may emit one bounded effect/checkpoint per reconcile. This improves fairness, shutdown, leader transfer, and review. Micro-steps need not become public phases; keep internal steps versioned and conditions meaningful.

### Design supersession for changing desired state

Bind every execution and condition to the desired generation it implements. When generation changes, classify the active protocol: retarget in place, restart before effects, complete a safe checkpoint then supersede, compensate, or cross an irreversible point and finish/forward-repair.

Persist `supersededBy` and outcome for old execution records when histories are separate. Never overwrite correlation needed to discover an old in-flight effect. A newer workflow may need to adopt, wait for, or dispose it.

Define coalescing semantics. Scaling from 3 to 4 to 5 may safely converge directly to 5. Upgrading 12 to 13 to 14 might require compatibility hops. A backup request can be an independent obligation that must not disappear when a later spec arrives.

Before destructive transitions, recheck generation and strategy. A stale plan that passed validation hours ago may no longer be authorized.

### Treat pause, cancel, and delete as protocols

Pause can mean stop starting new steps at the next checkpoint, freeze external work, or keep health/repair reconciliation active. State which behaviors continue. A pause request cannot instantly stop an already committed provider operation.

Cancellation is requested, accepted, cancelling, and terminal cancelled/failed/succeeded-after-cancel-race as appropriate. Define whether activities receive a cancellation signal, how long they may finish, and what happens if they cannot be stopped.

Deletion changes the desired lifecycle and may preempt ordinary work, but it still needs an ordered state machine. Decide whether to complete/abort upgrade, retain backup, drain traffic, delete candidates and primary, revoke identity, and remove finalizers.

Force and orphan are privileged transitions with explicit consequence, owner, reason, audit, and retained evidence. They are not error handling shortcuts.

### Model irreversible boundaries and compensation honestly

Mark commit points: traffic cutover, data-format upgrade, destructive schema migration, credential revocation, data deletion, or external publication. Before the point, cancellation may remove a candidate. After it, forward completion or a distinct reverse operation may be safer than rollback.

Compensations are ordinary failure-prone effects with identity, guards, retries, observation, and possible partial completion. Deleting a newly created replica compensates provisioning; recreating a deleted database does not restore its data or identity.

Keep evidence needed to decide compensation: old/new resource IDs, backup and restore proof, routing revisions, consumer compatibility, and elapsed time. Compensation policy may change with data written after cutover.

If no safe automatic action exists, transition to a blocked/manual-intervention configuration that preserves service and facts. Do not choose a destructive path merely to reach a terminal enum.

### Use orthogonal and hierarchical state carefully

Lifecycle, readiness, backup, traffic, policy, and deletion can vary independently. If dimensions have $n_i$ states, naming every combined phase yields up to $\prod_i n_i$ combinations. Many are illegal or irrelevant, and missing ones become ambiguous.

Use a small workflow checkpoint for the active protocol and conditions for orthogonal observed facts. Define cross-dimension invariants: `TrafficActive=True` implies candidate `Ready=True`; deletion may coexist with `BackupVerified=True`; `Progressing=True` does not imply `Ready=False` when the old version serves.

Hierarchical state groups shared behavior such as all `Upgrading` substates responding to cancel or timeout. History/resume can be useful, but persisted resume state must still be compatible with current intent and observations; blindly resuming a pre-incident substate can be unsafe.

Parallel branches need joins and failure policy: all required, quorum, best effort, fail fast, or tolerate bounded failures. “Parallel” does not eliminate shared-resource conflicts or define completion.

### Design time as durable data

Persist start time, last transition time, next eligible attempt, absolute deadline, lease/approval expiry, and heartbeat observation as required. A process-local timer disappears on restart; recompute scheduling from durable timestamps.

Use monotonic elapsed clocks inside one process for local timeout measurement, but persisted wall-clock deadlines require bounded clock assumptions. Never infer that an external effect failed only because its deadline passed.

Separate operation timeout, heartbeat timeout, retry delay, workflow deadline, approval expiry, and business deadline. Each has a different transition and consequence.

Avoid resetting attempts or deadlines whenever a reconcile restarts or status is rewritten. Define scope: per activity, per error class, per generation, or whole execution. Apply jitter and caps; a million workflows reaching a deadline together can create a recovery storm.

### Classify failure and terminality

Classify invalid desired state, unauthorized transition, missing dependency, transient provider failure, permanent provider rejection, outcome unknown, invariant violation, unsupported workflow revision, cancellation, supersession, and controller defect separately.

Terminal means no further automatic progress for this execution under unchanged inputs. A resource can become actionable again after generation/policy/permission changes, so avoid a forever `Failed` phase that the controller never reevaluates.

Record a stable machine reason, human message, observed generation, failed step, attempt/deadline, and safe next action. Do not expose raw secret/provider payloads.

Use circuit breaking or global dependency conditions for systemic failure rather than individually exhausting every workflow. Preserve fair progress for unrelated tenants and lifecycle-critical cleanup.

### Coordinate authority and concurrency

Leader election reduces concurrent active controllers but does not eliminate delayed writes or external effects. Use resource-version preconditions on checkpoints, stable activity identity, and provider fencing/conditional versions where available.

For parallel workflow branches, allocate owned fields/resources and define join coordination. Two branches must not patch one broad status object from stale reads; use granular conditions or a single aggregator with conflict retry.

Limit per-resource concurrency to one state advancement unless the model explicitly permits independent branches. Limit global and per-tenant activity concurrency, provider rate, and queue age so a large workflow does not starve deletion or incident actions.

Human approvals need immutable scope: workflow/resource UID, desired generation, transition, plan digest, risk, actor, issued/expiry time. Approval of one plan must not authorize a mutated plan.

### Choose persistence and execution mechanisms deliberately

For short/simple protocols, CR status plus owned Jobs/resources and level-based reconciliation can be sufficient. Persist compact checkpoints and reconstruct observed facts; avoid writing an event history into status.

A separate immutable operation resource helps when attempts are independently visible, multiple operations can coexist, audit/history is meaningful, or terminal records outlive the primary resource. Bound retention and sensitive data.

A durable workflow engine can supply event history, timers, retries, signals, and replay. It adds another control-plane dependency and requires deterministic workflow decisions plus idempotent/observable external activities. Do not duplicate incompatible truth between engine history and CR status; define authority and recovery.

An external state-machine service may improve long-running orchestration, but Kubernetes desired state still needs correlated status and deletion behavior. Select based on failure domain, scale, query, retention, transaction, upgrade, and operator skills—not diagram preference.

### Make status describe facts rather than narration

Kubernetes API conventions favor conditions describing current observed properties rather than a procession of verbs. Use `Ready`, `Progressing`, `Degraded`, `BackupVerified`, `TrafficSwitched`, or domain terms with documented polarity and stable reasons.

Keep internal step/workflow revision for diagnosis and recovery, but do not require clients to reverse-engineer readiness from it. Report active revision separately from requested target and preserve old service health during an upgrade.

Only change `lastTransitionTime` when the condition status changes, not every message/reason refresh according to the adopted condition contract. Set observed generation to the intent evaluated. Stale conditions become visibly stale/unknown.

Expose bounded progress such as completed/required shards when meaningful, but never fabricate a percentage for incomparable steps. Link to authorized detailed operation evidence rather than growing status without bound.

### Version the state machine as persisted data

Assign a workflow-definition revision to each execution or checkpoint. New code must recognize every state/revision it may encounter during rollout, rollback, restore, and queued-work delay.

Prefer additive transitions and explicit migration adapters. Renaming a state constant, changing step meaning, reordering activities, or changing operation-key derivation can corrupt in-flight workflows even if the CRD schema accepts the status.

During rolling upgrade, old and new replicas may alternate. Either guarantee compatible transition semantics, route/fence workflows by revision, or drain old workers before new states can be written. Unknown newer revisions should stop safely.

Replay-based engines require deterministic workflow code for recorded history. Version branching or worker routing must preserve prior decisions. Live network, time, randomness, and mutable configuration belong in recorded activities/side effects, not unrecorded replay decisions.

### Secure state transitions and evidence

Least privilege by activity and resource can reduce harm: the ordinary health reconciler need not hold deletion or backup-destroy authority. Where one controller identity must be broad, enforce policy and explicit high-risk guards.

Validate all activity outputs before they become guards or resource identifiers. Bind correlations to tenant and UID. Protect credentials, backup locations, approval tokens, provider errors, and customer data in status/log/history.

Audit desired generation changes, approvals, commit points, force/orphan, cancellation races, invariant violations, workflow migrations, and manual state repair. Routine no-op reconciles need metrics/traces but may not warrant high-volume audit records.

State repair tools are privileged APIs. Validate expected current state/resource version, preview consequences, preserve before/after evidence, and require a recovery runbook. Direct status patching can cause skipped or repeated effects.

### Verify safety, liveness, and recovery

Represent the transition graph in code/data from one authoritative definition where practical. Check that every nonterminal state has intended outgoing paths, terminal states do not emit effects, unreachable states are removed or justified, and guards cover defaults/errors.

For invariant proof by induction, establish $I$ in every initial state and show each legal transition preserves it. The proof is only as complete as the model: a provider side effect or concurrent controller outside $T$ can invalidate it.

Model-check a bounded instance for concurrent cancel/update/delete, leader change, timeout before/after effect, duplicate callback, stale observation, approval expiry, and compensation failure. Inspect counterexample traces rather than only state coverage.

Test real crash points before intent persistence, after intent/before call, after call/before result, after result/before checkpoint, and during status conflict. Include process/cluster restore, queue loss, timer expiry, old/new code, and external provider inventories.

Liveness tests require controlled eventual recovery assumptions and deadlines. Fault injection that leaves a dependency permanently down should produce truthful blocked/unknown status and bounded load, not a false expectation of success.

### Retire workflows and their executor

Stop admitting new executions, inventory active/paused/blocked/unknown states, timers, activities, finalizers, external effects, operation records, approvals, credentials, queues, and backups. Decide finish, migrate, compensate, cancel, or explicitly orphan each.

A successor must understand existing definition revisions and correlations before ownership transfers. Do not strand statuses that only the old binary can decode or finalizers only it can remove.

Drain workers after proving no new tasks target them. Revoke authority after effects are dispositioned. Remove schedules/callbacks so delayed messages cannot resurrect old transitions.

Update restore bundles and replay/worker routing. Preserve required audit evidence without preserving executable credentials or an engine capable of resuming obsolete destructive work.

### Use an executable state-machine inventory

The following synthetic inventory counts foundational properties across ten workflow situations. It does not prove a real transition system, activity, provider, controller, safety invariant, liveness property, migration, or recovery path.

<!-- bijux-verify: {"id":"operator-state-machine-inventory","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"situations 10\ndesired_correlated 10\nstate_durable 9\nguards_explicit 9\neffects_correlated 9\ntime_bounded 9\nsupersession_defined 9\ncancellation_defined 8\ninvariants_checked 9\nupgrade_compatible 8\nrecovery_tested 8\n","stderr":""}} -->
```python
situations = [
    ("provision", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("async-timeout", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("generation-change", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("pause-resume", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("cancel-race", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("leader-change", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("commit-compensate", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("definition-upgrade", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("legacy-local-step", 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("forced-orphan", 1, 1, 1, 1, 1, 1, 0, 1, 0, 0),
]
fields = [
    "desired_correlated", "state_durable", "guards_explicit",
    "effects_correlated", "time_bounded", "supersession_defined",
    "cancellation_defined", "invariants_checked", "upgrade_compatible",
    "recovery_tested",
]
print("situations", len(situations))
for index, field in enumerate(fields, start=1):
    print(field, sum(situation[index] for situation in situations))
```

The local-only legacy step is not crash-safe. A forced orphan can be authorized, yet still lacks completed cancellation, executor compatibility, and recovery evidence; those consequences must remain visible.

## Definitions and Notation

- $M=(S,S_0,E,G,A,\delta)$: state-machine model.
- $S$: legal control-state configurations; $S_0\subseteq S$: initial configurations.
- $E$: events or observations that prompt evaluation, not necessarily durable truth.
- $G$: guarded predicates over desired, observed, control, authority, and time state.
- $A$: bounded internal/external transition actions.
- $\delta\subseteq S\times E\times G\times A\times S$: transition relation.
- $T(s,s')$: a legal transition from current state $s$ to successor $s'$.
- $I(s)$: safety invariant intended to hold in every reachable $s$.
- $n_i$: number of states in orthogonal dimension $i$; naive product space is $\prod_i n_i$.
- **commit point**: boundary after which the original state cannot be restored by simple cancellation.
- **checkpoint**: durable protocol/effect evidence sufficient for safe resumption.
- **terminal execution**: one workflow has no further automatic steps under its outcome; the resource can still reconcile future intent.
- **fairness assumption**: an enabled required action is eventually scheduled/executed rather than starved forever.

## Mechanisms, Invariants, or Proof Structure

1. Elicit domain facts, actors, irreversible effects, safety invariants, progress goals, and environment assumptions.
2. Separate consumer intent, time-qualified domain observation, durable protocol checkpoint, and presentation conditions.
3. Define every transition by source, trigger, guard, action identity, target, status, timeout/retry, and audit class.
4. Persist workflow/generation/definition and operation intent before effects; observe by stable identity before marking completion or retrying ambiguity.
5. Recompute next legal work from current desired/observed/checkpoint state and advance using conditional writes under one authority.
6. Specify retarget/restart/supersede/compensate/forward-complete behavior for every desired-generation change and commit-point position.
7. Treat pause, cancel, delete, force, and orphan as stateful protocols with authority and races.
8. Model orthogonal conditions and hierarchical shared behavior while enumerating legal cross-dimension configurations and joins.
9. Persist deadlines/timers/approvals, classify errors and terminality, bound queue/concurrency/retry, and preserve fair cleanup.
10. Version persisted workflow semantics and test rolling workers, replay, migration, rollback/forward recovery, and restore.
11. Prove/model-check invariants and reachability under bounded models, then crash/fault/load-test real effects and retire all executions/authority.

Safety induction establishes $I$ for reachable modeled states when $I(s_0)$ holds for every $s_0\in S_0$ and every legal $T$ preserves it. It cannot cover an omitted actor, unmodeled provider effect, corrupted observation, or implementation that bypasses $\delta$.

Liveness cannot be derived from safety. A machine that never moves can preserve every safety invariant. Eventual success/terminal reporting needs fair workers, bounded backoff, available dependencies/approvals, resolvable unknown effects, and an attainable target; otherwise truthful stable blocking is expected.

## Alternatives and Trade-Offs

- **Implicit branch logic versus explicit machine:** implicit code is quick for tiny flows; an explicit graph makes complex legal/illegal progress reviewable and testable.
- **Single phase versus orthogonal conditions:** one phase is compact; conditions preserve simultaneous readiness, progress, backup, degradation, and deletion facts.
- **Status checkpoint versus operation resource:** status keeps simple ownership; operation resources support concurrent/history/audit lifecycles with more objects.
- **Controller loop versus workflow engine:** a loop fits level-based control; an engine supplies durable history/timers/signals but adds replay rules and dependency.
- **Persist before versus after effect:** either alone has a crash gap; intent/correlation plus observation bridges ambiguity.
- **Retarget versus supersede:** retarget reduces churn for monotonic changes; supersession keeps noncommutative/irreversible plans distinct.
- **Automatic compensation versus manual block:** automation reduces recovery time; human decision protects data when compensation is lossy or ambiguous.
- **Hierarchical versus flat states:** hierarchy shares behavior; it can hide inherited transitions and resume complexity.
- **Parallel branches versus serialized steps:** parallelism lowers latency; joins, shared state, resource pressure, and partial failure multiply.
- **Absolute deadline versus inactivity timeout:** deadline bounds total execution; inactivity detects stalls but can reset or overlook slow progress.
- **Fail-fast versus keep old service:** terminal rejection clarifies impossible targets; preserving an old healthy revision can protect availability during failed change.
- **Compatible workers versus revision routing:** universal compatibility simplifies scheduling; routing isolates versions but complicates queues and retirement.
- **Model checking versus scenario tests:** model exploration finds interleavings in an abstraction; integration tests validate real API/provider semantics.
- **Rollback versus forward repair:** rollback works before compatible reversible boundaries; forward repair respects effects/data written after commit.

## Failure Modes and Misconceptions

- **“Phase is the state machine.”** It usually hides correlations, orthogonal facts, guards, and recovery evidence.
- **“Conditions should follow workflow order.”** Conditions describe current properties and can coexist; they are not mutually exclusive steps.
- **“The event advances the state.”** It prompts reevaluation; current durable state and guards authorize advancement.
- **“Writing the next state then acting is safe.”** A crash can skip the effect; acting then writing can duplicate it without correlation/observation.
- **“Timeout is failure.”** Remote effect may have committed; outcome is unknown until authoritative observation.
- **“Only one leader means one effect.”** Delayed old calls and crash gaps remain; conditional writes, fencing, and idempotency are still needed.
- **“New desired state can wait until the workflow ends.”** Stale destructive actions may no longer be authorized; define supersession at every step.
- **“Cancel is immediate.”** Activities and external providers may not support cancellation, and success can race the request.
- **“Compensation rolls back.”** It is a new fallible action and cannot undo lost data or all external observation.
- **“Terminal failure means ignore forever.”** Changed desired state, policy, permission, or dependency can make a new execution valid.
- **“More states mean more precision.”** Unstructured Cartesian-product enums create unreachable, contradictory, and unhandled configurations.
- **“Parallel state means independent work.”** Branches can contend on objects, quota, identities, and join outcomes.
- **“Restart resets the timeout.”** Durable deadlines and attempts must retain their defined scope.
- **“Status can store the full history.”** It bloats API/watch paths; use bounded checkpoints and separate evidence.
- **“A workflow engine makes activities exactly once.”** Replay can make decisions durable, while external effects still need idempotency and observation.
- **“New code can reinterpret old state.”** Persisted meanings are compatibility contracts; silent reinterpretation can repeat or skip effects.
- **“The diagram proves safety.”** Proof requires complete transitions/invariants, and implementation/integration must conform.
- **“Stopping the operator retires it.”** Workflows, finalizers, effects, callbacks, credentials, queues, and restore paths can remain.

## Worked Examples

### Example 1

An upgrade phase says `Upgrading`, but the old service is ready, candidate backup is verified, replication is lagging, and traffic is unswitched. Separate conditions expose all four facts. Conclusion: one phase cannot represent orthogonal operational truth.

### Example 2

A controller writes `BackupComplete` before launching a Job and crashes. On restart it skips backup. The redesign persists operation intent/ID, observes the owned Job, and marks verification only after integrity evidence. Conclusion: state advancement must bridge the effect gap.

### Example 3

A provider cutover times out after committing. A stable operation token lets the next leader query the active route; it records success instead of switching again. Conclusion: timeout creates uncertainty, not known failure.

### Example 4

Generation 8 requests blue-green upgrade; generation 9 requests in-place before traffic switches. The machine cancels the candidate and starts a new execution. After switch, the same change would require forward completion or reverse cutover. Conclusion: supersession depends on commit position.

### Example 5

A cancel request races task success. Status records `CancellationRequested`, then observes success and transitions to `SucceededAfterCancelRequest` before applying declared post-success disposition. Conclusion: cancellation is a protocol with races.

### Example 6

Lifecycle has six states, backup four, traffic three, and approval three: $6\times4\times3\times3=216$ naive combinations. A workflow checkpoint plus orthogonal conditions and invariants avoids naming most illegal combinations. Conclusion: product phases scale poorly.

### Example 7

Old and new controllers alternate after rollout; the old binary sees unknown `VerifyingRestore` and would map it to `Provisioning`. Revision fencing makes it stop instead. Conclusion: safe incompatibility beats creative downgrade.

### Example 8

Three parallel shard restores share one quota and all retry together. Per-workflow concurrency, jitter, shard operation IDs, and an all-required join prevent overload and premature readiness. Conclusion: parallelism needs scheduling and join semantics.

### Example 9

A human approves plan digest A, but a policy refresh changes endpoints to digest B. The cutover guard rejects the stale approval. Conclusion: authorization must bind the exact transition plan.

### Example 10

An operator is removed with two paused upgrades and one finalizer. Callbacks later enqueue nonexistent workers and deletion remains stuck. Retirement resumes/migrates or dispositions every execution before revoking workers and schedules. Conclusion: executor lifecycle is part of workflow state.

## Cross-Program Connections

- **Automata/formal methods:** transition systems, invariants, induction, reachability, temporal properties, and counterexamples provide precise review tools.
- **Distributed systems:** partial failure, ambiguous effects, leader churn, fencing, retries, clocks, and eventual observation determine transition safety.
- **Database systems:** write-ahead intent, conditional updates, durable checkpoints, transaction gaps, sagas, and recovery logs shape persistence.
- **Control theory:** feedback repeatedly regulates domain state, while workflow state captures discrete modes, hysteresis, guards, and safety interlocks.
- **API engineering:** long-running operations, cancellation, conditions, idempotency, errors, compatibility, and deprecation are public workflow contracts.
- **Reliability engineering:** timeouts, retries, queues, circuit breaking, graceful degradation, fault injection, and recovery objectives govern progress.
- **Security engineering:** least privilege, transition authorization, approval binding, audit, secret history, force/orphan, and state repair limit power.
- **Data engineering:** checkpointing, replay, watermarks, backfill, exactly-once myths, and schema evolution resemble durable operator execution.
- **Systems engineering:** operational modes, statecharts, hazard analysis, interface control, verification, lifecycle, and disposal prevent happy-path automation.
- **Organizational design:** consumer, platform, provider, approver, incident, and successor authority must align with transition ownership.

## References

1. Kubernetes Authors, “Operator Pattern,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
2. Kubernetes Authors, “Controllers,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/architecture/controller/
3. Kubernetes Authors, “Extending Kubernetes,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/extend-kubernetes/
4. Kubernetes SIG Architecture, “API Conventions,” current repository documentation, retrieved 2026-09-02. https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md
5. Kubernetes SIG API Machinery, “controller-runtime reconcile package,” current Go package documentation, retrieved 2026-09-02. https://pkg.go.dev/sigs.k8s.io/controller-runtime/pkg/reconcile
6. Kubernetes Authors, “Kubernetes API Concepts,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/reference/using-api/api-concepts/
7. Kubernetes Authors, “Finalizers,” current documentation, retrieved 2026-09-02. https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/
8. World Wide Web Consortium, “State Chart XML (SCXML): State Machine Notation for Control Abstraction,” W3C Recommendation, September 2015. https://www.w3.org/TR/scxml/
9. Amazon Web Services, “Amazon States Language,” current specification, retrieved 2026-09-02. https://states-language.net/spec.html
10. Amazon Web Services, “Handling Errors in Step Functions Workflows,” current documentation, retrieved 2026-09-02. https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html
11. Temporal Technologies, “Workflow Execution,” current documentation, retrieved 2026-09-02. https://docs.temporal.io/workflow-execution
12. Temporal Technologies, “Safe Deployments,” current documentation, retrieved 2026-09-02. https://docs.temporal.io/develop/safe-deployments
13. Leslie Lamport, “Specifying and Verifying Systems with TLA+,” current manuscript, retrieved 2026-09-02. https://lamport.org/pubs/spec-and-verifying.pdf
14. Pat Helland, “Life beyond Distributed Transactions: An Apostate’s Opinion,” CIDR 2007. https://www.cidrdb.org/cidr2007/papers/cidr07p15.pdf

## Exercises

### Exercise 1

Design an operator state machine for database version upgrade. Define desired/domain/control/presentation state, legal transitions, guards, effect correlations, commit points, invariants, and liveness assumptions.

### Exercise 2

Model pause, cancellation, deletion, and a desired-generation change at each of these points: before backup, after verified backup, during replication, just before traffic switch, after traffic switch, and during old-primary deletion.

### Exercise 3

A design proposes lifecycle 6 states, backup 4, traffic 3, approval 3, and deletion 4. Compute the naive product space. Replace it with a small active-workflow checkpoint plus orthogonal conditions and state five cross-dimension invariants.

### Exercise 4

Design crash tests for one asynchronous provider action across intent persistence, request send, response, observation, and checkpoint. Include leader change, timeout, duplicate callback, stale observation, and provider lacking fencing.

### Exercise 5

Plan a rolling upgrade and eventual retirement of an operator with three persisted workflow revisions, replayed durable workflows, active/paused/unknown executions, finalizers, callbacks, provider credentials, and disaster-recovery backups.

## Answers to the Exercises

### Answer 1

Spec owns target version, strategy, maintenance/approval policy, pause/cancel request, and data guarantees. Domain observations cover current/candidate versions, backup integrity, replication lag, health, traffic revision, and provider operations with freshness. Control state stores resource UID/generation, workflow/definition revision, chosen plan digest, step, attempt/deadline, activity IDs, approval scope, and commit point. Conditions independently report Ready, Progressing, BackupVerified, CandidateReady, TrafficSwitched, and Degraded with observed generation. Legal flow is plan → backup intent/observe/verify → provision candidate → replicate/verify → authorize cutover → switch/observe → monitor → retire old → succeed, with error/unknown/cancel/supersede branches. Guards recheck generation, UID, compatibility, backup, lag, candidate health, current approval/digest, and authority immediately before cutover/deletion. Invariants include never switch to unverified candidate and never delete the only recoverable copy. Liveness assumes fair workers, attainable versions, bounded approval, recovering dependencies, and resolvable provider operations; otherwise report blocked/unknown.

### Answer 2

Before backup, pause stops planning/effects; cancel terminates cleanly; delete enters deletion; generation change restarts/retargets. After verified backup, preserve its immutable evidence and reuse only if policy/age/generation permits. During replication, pause stops new transitions but may keep safe replication/health; cancellation requests provider stop then disposes candidate; delete chooses whether backup must remain; new generation may retarget only if compatibility permits. Just before switch, every request rechecks generation/approval and can supersede without traffic effect. After switch, cancellation cannot pretend rollback: choose monitored reverse cutover or forward completion using post-switch writes/compatibility. During old-primary deletion, preserve correlation and outcome unknown; a generation requesting rollback may be impossible and needs forward repair/manual decision. Deletion of the control resource remains a separate finalizer protocol. Every point defines race outcomes and service continuity.

### Answer 3

The naive product is $6\times4\times3\times3\times4=864$ configurations. Keep an active protocol checkpoint such as `Planning`, `BackingUp`, `ProvisioningCandidate`, `Replicating`, `SwitchingTraffic`, `RetiringOld`, plus execution outcome; represent backup, traffic, approval, readiness/degradation, and deletion as bounded conditions/data. Example invariants: traffic on candidate implies candidate ready and compatible; old primary deletion implies traffic switch verified and backup retained/verified; cutover requires unexpired approval matching plan/generation; deletion requested forbids starting a new ordinary upgrade; and `Ready=True` must identify a fresh serving revision even while `Progressing=True`. Enumerate legal cross-condition combinations in tests/model rather than naming all 864.

### Answer 4

Crash before persisted intent must yield no call. Crash after intent/operation ID but before call resumes by observing then submitting the same identity. Crash after provider commit but before response enters/resolves unknown by lookup, never blind duplicate. Crash after response but before checkpoint observes the same activity and records completion. Crash after observation but during resource-version conflict rereads and avoids stale advancement. Change leader at each boundary and send duplicate/out-of-order callbacks; callbacks only enqueue/correlate and cannot override guards. Inject timeout before and after commit, stale not-found/list, and recovery. Without provider fencing, use deterministic/idempotency identity when supported, conditional control writes, observation, and quarantine/manual resolution for unresolved ambiguity; do not claim exactly once. Verify no duplicate logical effect and correct condition/generation evidence.

### Answer 5

Inventory executions by workflow revision/state and all activities, timers, finalizers, callbacks, effects, approvals, credentials, queues, and backups. New workers replay/interpret every live history through versioned deterministic branches; activities remain stable/idempotent. During rollout, route workflow revisions to compatible workers or maintain bidirectional compatibility; old workers must not process newer states. Test histories from all three revisions, code changes, leader/process restart, pause/resume, unknown effects, rollback before incompatible writes, and forward recovery afterward. Resolve or migrate active, paused, and unknown executions before retirement; transfer finalizers and provider correlations to the successor. Stop admission/schedules, drain callbacks/queues, disposition effects, then revoke credentials/workers. Update restore bundles so old workers cannot return and replay destructive steps. Remove finalizers, engine namespaces/queues, images, RBAC, webhooks, alerts, and docs only after negative inventories; retain bounded non-secret audit evidence.
