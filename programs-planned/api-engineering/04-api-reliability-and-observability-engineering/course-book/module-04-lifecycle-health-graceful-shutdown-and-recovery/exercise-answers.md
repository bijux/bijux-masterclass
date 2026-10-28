# Reference Answers — Module 04: Lifecycle, Health, Shutdown, and Recovery

Read after attempting all twelve Lifecycle, Health, Shutdown, and Recovery exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why should a database outage usually affect readiness but not liveness?

**Answer.** The process can still make local progress and expose diagnosis, but it cannot safely admit database-dependent work. Restarting it does not repair the database.

## 2. What must happen first during graceful shutdown?

**Answer.** New admission must stop: transition to draining and report not-ready before waiting for existing work.

## 3. How should a worker handle termination while holding a job lease?

**Answer.** Stop claiming new jobs, finish within the bounded budget when safe, otherwise leave durable state recoverable and never commit after lease generation is stale.

**Common mistake.** Describing a procedure for “How should a worker handle termination while holding a job lease?” without a falsifiable completion condition.

## 4. May telemetry export delay shutdown?

**Answer.** Only inside a bounded sub-budget after correctness-critical work. Export failure is recorded and the process still exits.

## 5. What is the decisive oracle for safe restart recovery?

**Answer.** Durable job, run, event, artifact, outbox, and repair-journal state—not an in-memory queue or final log line.

## 6. Why is a successful database ping insufficient for readiness?

**Answer.** It proves connectivity, not migration compatibility, pool availability, transaction ability, tenant policy, or required schema invariants.

## 7. When should liveness fail?

**Answer.** When this process cannot make local forward progress and restart is a plausible repair, such as a deadlocked event loop or corrupted irrecoverable local state.

## 8. What prevents readiness flapping?

**Answer.** State thresholds, startup grace, consecutive observations, and reasoned transitions rather than one raw sample.

## 9. How should long-lived SSE connections drain?

**Answer.** Stop new streams, notify or close existing streams according to the contract, bound the wait, and preserve durable progress independent of connection lifetime.

**Common mistake.** Describing a procedure for “How should long-lived SSE connections drain?” without a falsifiable completion condition.

## 10. What if the shutdown budget expires during a database transaction?

**Answer.** The database transaction must roll back or finish atomically. The process must not acknowledge an uncommitted result; restart recovery uses durable state.

## 11. Trace explicit lifecycle and health in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/health.py` and `capstone/tracks/typescript-fastify/src/reliability/health.ts`. The required invariant is that liveness reports process existence, readiness reports safe admission, and draining stops new work before owned work is released.

## 12. Compare explicit lifecycle and health across Python and TypeScript

Both tracks must preserve this invariant: liveness reports process existence, readiness reports safe admission, and draining stops new work before owned work is released. The intentional difference is that framework shutdown hooks differ; lifecycle states and observable probe results must match.
