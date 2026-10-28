# TaskHarbor Engineering Guide

TaskHarbor is a dependency-aware asynchronous job orchestrator. It exists to integrate Course 4’s runtime models, not to imitate a general workflow platform.

## Command surface

```text
taskharbor inspect <manifest.json>
taskharbor run <manifest.json> [--concurrency <n>] [--policy continue|fail-fast] [--timeout-ms <n>]
taskharbor demo
taskharbor help
taskharbor version
```

## Manifest

```json
{
  "version": "TASK_HARBOR_V1",
  "tasks": [
    { "id": "warmup", "kind": "delay", "milliseconds": 25, "priority": "high" },
    { "id": "message", "kind": "uppercase", "text": "harbor", "dependsOn": ["warmup"] },
    { "id": "audit", "kind": "echo", "text": "complete", "dependsOn": ["message"] }
  ]
}
```

Built-in task kinds are `delay`, `echo`, `uppercase`, and `fail`. A task may declare dependencies, a timeout, and `low`, `normal`, or `high` priority. The implementation uses only Node’s standard library.

## Architecture and authorities

```text
unknown JSON
    ↓ manifest validator
trusted task descriptions
    ↓ graph validator
acyclic dependency graph
    ↓ scheduler authority
ready / running / terminal state
    ↓ executor
cooperative task effect
    ↓ indexed outcome registry
source-ordered report
```

The event hub and diagnostics channel sit beside this path. They observe transitions but cannot establish task state. The executable owns process signals. The clock owns deadline arithmetic. The CLI owns token parsing and exit translation.

## State model

A task moves through internal states:

```text
pending → ready → running → succeeded
                   ↘ failed
                   ↘ timed-out
                   ↘ cancelled
pending/ready → blocked
pending/ready → cancelled
```

`blocked` means a dependency reached a nonsuccess terminal state. `cancelled` means the run stopped admission or requested stop for this task. `timed-out` preserves a task-local deadline cause. These meanings remain distinct in events and final reports.

## Named invariants

1. Manifest input is validated from `unknown`; extra or malformed fields are rejected.
2. Task IDs are valid and unique.
3. Dependencies name existing tasks and the graph is acyclic.
4. No task starts before all dependencies succeed.
5. Active tasks never exceed configured concurrency.
6. Producer invocation occurs only after a scheduler slot exists.
7. Every manifest index receives exactly one terminal outcome.
8. Failed, timed-out, or cancelled prerequisites block dependents.
9. Fail-fast stops new starts, requests cancellation, and joins running tasks.
10. Continue mode allows independent ready tasks to proceed.
11. Final outcomes follow manifest order.
12. Priority affects only simultaneously ready selection.
13. Equal priority preserves source order.
14. Events follow authoritative transitions and may vary among independent tasks.
15. Diagnostic context contains only correlation identifiers.
16. Timers, abort listeners, event subscriptions, and context scopes are released.
17. Process shutdown returns only after the active run has a complete terminal report.

## Scheduling algorithm

Validation happens before execution. The scheduler maintains an internal state per source index and an indexed outcome array initialized with real `undefined` entries rather than sparse holes. It first marks tasks blocked by nonsuccessful dependencies, then marks newly eligible tasks ready. Ready tasks are sorted by priority rank and source index. The scheduler invokes producers only while capacity exists.

`Promise.race` is used only to discover the next completed running task. It is not the join boundary. After a completion, the scheduler records the outcome, emits observation, applies fail-fast policy if required, and continues until every source index is terminal. Running work remains owned through settlement even after cancellation.

## Failure policy

Continue mode records failure and keeps independent tasks eligible. Fail-fast aborts the run after the first failure or timeout, prevents further starts, classifies pending tasks as cancelled or blocked, and joins active siblings. Cancellation is cooperative; a task that ignores its signal may delay run completion. The built-in tasks obey signals at their waiting boundaries.

## Time model

A `Clock` abstraction supplies monotonic `now` and abortable `sleep`. Run timeout and task timeout create distinct typed reasons. Task duration is diagnostic and does not influence semantic ordering. Tests use controlled executors and clocks rather than arbitrary sleeps.

## Event and diagnostics model

The typed event hub publishes run and task lifecycle observations after state changes. Observer failure is isolated. A bounded async sequence can adapt events for pull consumption; overflow and early return are explicit. AsyncLocalStorage attaches `runId`, `taskId`, and source index to executor diagnostics. Neither event nor context can mutate scheduler state.

## Process boundary

`main.ts` translates SIGINT or SIGTERM into abort of the active CLI run. It does not force immediate exit. The CLI awaits TaskHarbor’s complete summary, renders output, assigns an exit code, removes listeners, and returns. Reusable library modules install no global process handlers.

## Module increments

| Module | Concrete change | Invariant introduced |
|---:|---|---|
| 31 | schedule vocabulary and cooperative test task | observed completion cannot define final order |
| 32 | run-owned task registry | every accepted promise is joined |
| 33 | run and task cancellation | cause is preserved; abort is not rollback |
| 34 | typed lifecycle events | observation follows authority |
| 35 | injected clock | time tests avoid probabilistic sleeps |
| 36 | bounded async event sequence | slow observers cannot create silent unbounded memory |
| 37 | correlation context and diagnostics | ambient metadata is observational only |
| 38 | finite concurrency and failure policies | producer invocation is bounded and outcomes complete |
| 39 | executable lifecycle | signals trigger joined shutdown rather than forced exit |
| 40 | graph validation and priority | cross-layer feature preserves earlier invariants |

## Test strategy

Unit tests own validator, graph, clock, event, context, and renderer claims. Scheduler tests use controlled executors to reverse completion, trigger failure, and observe priority without sleeps. Integration tests combine manifest, graph, scheduler, and rendering. Process tests spawn the real CLI and assert stdout, stderr, and exit status. No test treats one total event-loop trace as a portable contract.

## Independent extension: retries

After priority, add optional `maxAttempts` for selected built-in tasks. The impact map must cover validation, domain types, executor policy, per-task deadline, event payloads, rendering, tests, and compatibility. Retries remain under one task deadline. Only explicitly retryable failures qualify. A task effect that may commit externally requires idempotency or reconciliation; TaskHarbor’s built-in local operations avoid pretending this problem is solved generically.

## Completion standard

TaskHarbor is complete when all named invariants have executable evidence, the CLI behaves consistently under success and failure, no owned task or listener survives a run, final output remains source ordered under schedule variation, and the reader can implement the retry extension from an impact map without weakening cancellation or lifecycle semantics.
