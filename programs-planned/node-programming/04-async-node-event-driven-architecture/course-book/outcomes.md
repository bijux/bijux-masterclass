# Course 4 Outcomes

Completion requires working evidence and an explanation for each outcome.

## Scheduling and responsiveness

- Trace synchronous execution, next-tick work, microtasks, timers, I/O continuations, and immediates as partial-order relations.
- Identify blocking regions before the first `await` and after every resumption.
- Distinguish readiness from execution and starvation from deadlock.
- Introduce cooperative fairness with a documented chunk and cancellation-latency policy.

## Promise and task ownership

- Detect floating promises and orphaned work.
- Select promise combinators by aggregate-result policy while naming the cancellation and joining they do not provide.
- Build a parent scope that owns every accepted child through terminal settlement.
- Reconstruct deterministic source-ordered outcomes from schedule-dependent completion.

## Cancellation and time

- Treat abort as a cooperative request, never as automatic rollback.
- Preserve causes across user cancellation, deadline, fail-fast, and shutdown.
- Derive nested budgets from one monotonic absolute deadline.
- Remove timer and abort listeners on every terminal path.
- Test exact time boundaries with injected clocks rather than probabilistic sleeps.

## Observation and sequences

- Design typed synchronous event contracts with explicit reentrancy and observer-failure policy.
- Keep authoritative state separate from events and diagnostics.
- Own subscription lifetimes and async observer work.
- Build bounded async sequence bridges with close, failure, cancellation, overflow, and early-return semantics.

## Context, supervision, and lifecycle

- Propagate small immutable correlation context without using ambient state for authorization.
- Publish optional diagnostics through stable bounded channels.
- Bound producer invocation rather than merely awaiting already-started work.
- Implement continue and fail-fast policies with exact terminal accounting.
- Perform startup rollback, quiescence, drain, force, cleanup, and complete joining under one lifecycle owner.

## Integrated architecture

- Validate a dependency graph before execution.
- Enforce dependencies, priority among ready tasks, and finite concurrency.
- Give every manifest task exactly one terminal outcome.
- Separate live causal event order from deterministic final report order.
- Implement a cross-layer feature using an impact map that covers syntax, validation, types, runtime policy, observations, rendering, tests, and compatibility.
