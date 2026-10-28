# Graceful Lifecycle Harness

## Product

Build a lifecycle host that starts several resources transactionally and shuts them down through quiesce, drain, optional force, and close. Repeated shutdown requests must share one completion promise.

Read [Module 39](../../course-book/module-39-process-lifecycle-signals-cleanup-and-graceful-shutdown/index.md).

## Resource contract

Each resource exposes a name and lifecycle operations appropriate to the laboratory: start, stop admission, request cancellation, join or drain, force close, and dispose. The host owns operation order and one absolute grace deadline.

## Startup requirements

Acquire resources in declared order. Register cleanup immediately after success. On failure, release already-started resources in reverse order. Preserve the startup failure and collect cleanup failures. Do not transition to ready early.

## Shutdown requirements

The first request transitions to quiescing and returns a memoized promise. Stop admission before cancellation. Drain accepted work while budget remains. Enter force only after the deadline or an explicit escalation policy. Join every resource and remove process-facing listeners before closed.

## Tests

Inject failures at each startup point. Test normal shutdown, repeated shutdown calls, shutdown before ready, one stuck resource, force escalation, cleanup failure aggregation, and no remaining listener or timer after close. Use a manual clock or deferred gates.

## Process-level lifecycle evidence

Unit tests are not sufficient. Spawn a small executable that prints a ready marker, owns at least two resources, and handles termination. Send one and then two signals. Assert startup rollback, idempotent shutdown, grace deadline, escalation policy, exit status, and output completion.

Inject cleanup failures and preserve them without losing the initiating failure. Confirm that signal listeners and timers are removed so repeated tests in one process do not accumulate global state.

## Startup rollback evidence

Fail each acquisition step in turn and verify that only previously acquired resources are released, in legal dependency order. Include one rollback failure and preserve both the initiating and cleanup causes.

## Escalation evidence

Add a resource that ignores cooperative cancellation. After the grace deadline, record the abort request and complete the lifecycle without claiming that arbitrary JavaScript was forcibly stopped. The final report must name the unresolved component.

## Independent transfer

Apply the host to a CLI that owns a temporary workspace and a child process. Define behavior for SIGINT during startup, during child execution, and after result rendering has begun.

## Implementation stages

Model states and legal methods before wiring signals. Implement transactional startup with reverse cleanup. Implement memoized shutdown. Add one clock-governed grace budget and force escalation. Only the executable adapter should install process listeners.

## Review questions

What failure is expected versus process fatal? What does a second signal do? Can output be truncated? Which cleanup failures change exit status? Are signal listeners removed after closure?

## Completion evidence

Provide state-transition tests, acquisition-failure injection, repeated-signal behavior, stuck-resource force, output/exit analysis, and proof that the reusable lifecycle host installs no global handlers itself.
