# Module 08 Exercise Answers

Use these answers only after running the corresponding proof. Compare reasoning,
failure analysis, and architectural boundaries rather than copying assertions.

## Async plans: prove fresh execution without promising equal effects

Calling an `async def` function creates a coroutine object. A coroutine object is
single-use, so caching it and returning it twice makes the second await fail with
`RuntimeError: cannot reuse already awaited coroutine`.

The defensible shape is a callable such as `lambda: read_sequence()`.
`async_lift` stores that callable as the plan. Construction does not call it;
each `plan()` call asks it for a new coroutine.

Common wrong turns:

- creating `coroutine = read_sequence()` outside the plan performs premature
  coroutine allocation and makes replay invalid;
- asserting the two results are equal confuses replayability with deterministic
  effect output;
- driving the plan from domain code erases the interpreter boundary;
- testing only `callable(plan)` says nothing about deferral.

The test proves zero calls during construction and one fresh execution per plan
call. It does not prove the external capability is deterministic, idempotent, or
safe to retry.

In FuncPipe, the shell may replay an async description when policy allows it.
Whether the underlying storage or embedding effect may be repeated remains a
separate domain decision.

## Async generators: observe a partial pull

`async_gen_map` returns a new `AsyncGen`; it does not iterate its input. The
mapped iterator requests one source result for each downstream `anext`, applies
the pure mapping only to `Ok`, and yields that result. A four-value source
consumed three times must therefore produce a three-entry pull trace.

Closing the iterator is part of the proof. It states that the consumer owns the
active traversal and is responsible for ending partial consumption. The
description remains replayable because the source is a callable that creates a
new async iterator.

Common wrong turns:

- list-comprehending the output consumes every source value and hides the
  demand boundary;
- asserting only mapped output misses eager upstream work;
- omitting `aclose` teaches unsafe partial-consumption habits;
- returning one cached async generator object destroys replayability.

The proof establishes demand-driven evaluation for this composition. It does
not establish bounded parallelism; Core 3 adds an explicit concurrency policy
for that separate concern.

## Backpressure: expose the bounded window

The worker increments its active counter immediately before the await and
decrements it immediately after. A scheduling yield allows several calls to
overlap without introducing real-time delays. `maximum_active` therefore
captures the widest observed window directly.

With six inputs and `max_concurrent=3`, the bounded combinator starts no fourth
worker until one of the first three releases capacity. In ordered mode it also
buffers completions by input index, so the resulting values retain input order
even if individual workers finish differently.

Common wrong turns:

- checking only output order says nothing about bounded fan-out;
- sleeping for fixed real durations makes the proof slow and timing-sensitive;
- asserting exact task scheduling order promises more than the policy;
- putting a semaphore inside every worker creates separate limits instead of
  one shared stream limit.

The policy is immutable description data. The semaphore, tasks, active counter,
and work all come into existence only when the shell drives the returned
`AsyncGen`.

## Retry policy: inspect attempts and backoff

With `backoff_base_ms=5`, zero jitter, and four permitted attempts, exponential
backoff records `[0.005, 0.01, 0.02]`. There is no delay after the final
successful attempt. The attempt counter remains zero at wrapper construction
because `async_with_resilience` returns another `AsyncPlan`.

The retriable `TRANSIENT` code permits policy to continue. A different code
would return immediately, while exhausting all four attempts would produce the
wrapper's `MAX_RETRIES` error rather than the step's final raw error.

Common wrong turns:

- asserting elapsed time couples the test to scheduler and machine load;
- injecting a blocking synchronous sleeper stalls the event loop;
- expecting a fourth delay adds sleep after work has already succeeded;
- assuming a retriable code means a non-idempotent write is safe to repeat.

This proof covers bounded attempts and the exponential schedule. Timeout
translation, cancellation, and randomized jitter are distinct policy behaviors
and deserve separate evidence.

## Deterministic testing: replay a timeout boundary

`FakeTimeout` compares the injected clock with its deadline on context exit and
uses `>=`. Advancing from zero to exactly `0.1` seconds therefore triggers a
100 ms timeout. Rebuilding the clock, timeout context, environment, and plan
gives the second execution the same initial state and the same result.

Common wrong turns:

- reusing the advanced clock changes the second execution's starting state;
- injecting a fake clock but allowing the real timeout context mixes two time
  models;
- adding a real sleep defeats both speed and determinism;
- claiming this test proves cancellation overstates a logical timeout fake.

The appropriate evidence is structural: equal typed results, equal logical-time
observations, and no real delay. Production cancellation still belongs in a
narrow integration test using the actual timeout context.

## Fairness: inspect a weighted prefix

With weights `{0: 1, 1: 2}`, the selector compares emitted-count divided by
weight and breaks equal ratios by lower stream index. Over six selections, the
tags are `A, B, B, A, B, B`: two positions for A and four for B. Both streams
are assumed to remain ready throughout the observation.

Common wrong turns:

- checking only final counts misses a starving prefix;
- adding sleeps changes readiness and tests the event loop instead of policy;
- leaving an infinite iterator open abandons both source iterators;
- claiming six values prove long-run proportionality overstates the example.

The small trace explains the selection rule. Property tests provide broader
evidence across weights and prefix lengths. Rate limiting can then wrap the fair
merge to cap total throughput without changing which ready stream owns each
position.

## Async adapters: preserve the synchronous core

`lift_sync` returns a function that captures arguments in an `AsyncPlan`.
Neither lifting nor applying that function executes the synchronous core. Each
plan call performs the work and catches exceptions at the adapter boundary.

For a positive and a negative input, build both plans first and assert zero
calls. Driving the positive plan produces its original `Ok`; driving the
negative plan increments the trace again and returns `Err(ErrInfo(...))` with
code `UNEXPECTED` and the exception message.

Common wrong turns:

- invoking the core to create a `Result` before lifting loses deferral;
- making the core `async def` introduces the async creep this adapter prevents;
- wrapping the test in `try/except` accepts an escaping exception;
- sending trivial work to an executor adds scheduling overhead without benefit.

The public `lift_sync` import is preserved in later snapshots even though Module
09 consolidates its implementation into `plan.py`. Learner code depends on the
stable capability, not its internal file location.

## Service integrations: release a partial stream

The async context manager appends `enter` only when iteration begins. Each
`anext` advances the response generator once. Calling `aclose` on the outer
iterator unwinds `async_gen_using`, which exits the context manager and appends
`exit`.

For two requested values, the expected trace is therefore `enter`, `pull:0`,
`pull:1`, `exit`. No later pull is permitted because downstream demand ended.

Common wrong turns:

- opening the session when constructing the description performs an eager
  external effect;
- consuming to a list defeats the partial-demand proof;
- omitting `aclose` delegates correctness to garbage collection;
- creating a fresh long-lived HTTP client per item confuses shell and stream
  ownership.

The fake records the resource protocol directly. Provider-specific status
mapping and transport behavior remain the responsibility of focused adapter
integration tests.
