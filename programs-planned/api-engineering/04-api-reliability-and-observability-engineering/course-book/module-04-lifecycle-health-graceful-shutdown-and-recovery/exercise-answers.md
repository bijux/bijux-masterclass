# Worked Answers — Module 04: Lifecycle, Health, Shutdown, and Recovery

Use these solutions to audit your reasoning for **Lifecycle, Health, Shutdown, and Recovery**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why should a database outage usually affect readiness but not liveness?

The process can still make local progress and expose diagnosis, but it cannot safely admit database-dependent work. Restarting it does not repair the database.

The chapter’s decisive distinction is this: Lifecycle is an explicit state machine. Liveness says the process can make local progress, readiness says this instance may receive new work, and draining prevents new admission while preserving owned work and durable recovery evidence.

**Evidence.** Exercise startup, accepting, draining, stopping, dependency loss, and restart while observing probe status, in-flight work, lease ownership, and recovery.

## 2. What must happen first during graceful shutdown?

New admission must stop: transition to draining and report not-ready before waiting for existing work.

In the cumulative capstone, the rule becomes concrete: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=04 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Exercise startup, accepting, draining, stopping, dependency loss, and restart while observing probe status, in-flight work, lease ownership, and recovery.

## 3. How should a worker handle termination while holding a job lease?

Stop claiming new jobs, finish within the bounded budget when safe, otherwise leave durable state recoverable and never commit after lease generation is stale.

**Common mistake.** Describing a procedure for “How should a worker handle termination while holding a job lease?” without a falsifiable completion condition.

A useful way to reason about the boundary is: Apply Lifecycle state machine, Startup gate, Liveness to this module’s capstone increment: Add startup validation, distinct liveness/readiness/startup decisions, drain transitions, bounded shutdown, lease-aware worker termination, and restart-recovery evidence. State one misleading green signal and the durable observation that would overrule it.

## 4. May telemetry export delay shutdown?

Only inside a bounded sub-budget after correctness-critical work. Export failure is recorded and the process still exits.

The implementation consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=04 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

**Evidence.** Follow one correlation and trace identity from HTTP through database, worker, storage, and webhook while verifying links, attempt identity, bounded attributes, and redaction.

## 5. What is the decisive oracle for safe restart recovery?

Durable job, run, event, artifact, outbox, and repair-journal state—not an in-memory queue or final log line.

The important nuance is: Apply Lifecycle state machine, Startup gate, Liveness to this module’s capstone increment: Add startup validation, distinct liveness/readiness/startup decisions, drain transitions, bounded shutdown, lease-aware worker termination, and restart-recovery evidence. State one misleading green signal and the durable observation that would overrule it.

**Evidence.** Run a bounded fault experiment with a declared durable-state oracle, correlated telemetry, abort condition, cleanup, and a planted mutant that the proof rejects.

## 6. Why is a successful database ping insufficient for readiness?

It proves connectivity, not migration compatibility, pool availability, transaction ability, tenant policy, or required schema invariants.

Under concurrency or failure, the distinction becomes: Lifecycle is an explicit state machine. Liveness says the process can make local progress, readiness says this instance may receive new work, and draining prevents new admission while preserving owned work and durable recovery evidence.

**Evidence.** Exercise startup, accepting, draining, stopping, dependency loss, and restart while observing probe status, in-flight work, lease ownership, and recovery.

## 7. When should liveness fail?

When this process cannot make local forward progress and restart is a plausible repair, such as a deadlocked event loop or corrupted irrecoverable local state.

The design remains honest only if: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=04 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 8. What prevents readiness flapping?

State thresholds, startup grace, consecutive observations, and reasoned transitions rather than one raw sample.

The consumer-facing consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=04 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

**Evidence.** Exercise startup, accepting, draining, stopping, dependency loss, and restart while observing probe status, in-flight work, lease ownership, and recovery.

## 9. How should long-lived SSE connections drain?

Stop new streams, notify or close existing streams according to the contract, bound the wait, and preserve durable progress independent of connection lifetime.

**Common mistake.** Describing a procedure for “How should long-lived SSE connections drain?” without a falsifiable completion condition.

The operational consequence is: Lifecycle is an explicit state machine. Liveness says the process can make local progress, readiness says this instance may receive new work, and draining prevents new admission while preserving owned work and durable recovery evidence.

## 10. What if the shutdown budget expires during a database transaction?

The database transaction must roll back or finish atomically. The process must not acknowledge an uncommitted result; restart recovery uses durable state.

The strongest engineering interpretation is: Apply Lifecycle state machine, Startup gate, Liveness to this module’s capstone increment: Add startup validation, distinct liveness/readiness/startup decisions, drain transitions, bounded shutdown, lease-aware worker termination, and restart-recovery evidence. State one misleading green signal and the durable observation that would overrule it.

## 11. Trace explicit lifecycle and health in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/health.py` and `capstone/tracks/typescript-fastify/src/reliability/health.ts`. The required invariant is that liveness reports process existence, readiness reports safe admission, and draining stops new work before owned work is released.

The defect-oriented view is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=04 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 12. Compare explicit lifecycle and health across Python and TypeScript

Both tracks must preserve this invariant: liveness reports process existence, readiness reports safe admission, and draining stops new work before owned work is released. The intentional difference is that framework shutdown hooks differ; lifecycle states and observable probe results must match.

Across the Python and TypeScript tracks, the invariant is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=04 TRACK=typescript and explain why the same public and durable outcome holds in the other language.
