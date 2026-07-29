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
