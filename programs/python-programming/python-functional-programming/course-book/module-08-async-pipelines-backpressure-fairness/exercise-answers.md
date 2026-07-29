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
