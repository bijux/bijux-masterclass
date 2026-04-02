# Module 07: Time and Concurrency

Object models that look clean in single-threaded examples often break when time,
parallel work, or async coordination enters the picture. This module teaches how to
model clocks, deadlines, concurrency, and async boundaries without turning design
semantics into scheduler folklore.

## Why this module matters

Time and concurrency amplify design mistakes:

- hidden calls to `datetime.now()` make behavior untestable
- shared mutable state turns local changes into races
- async wrappers widen interfaces without clear ownership
- retries and cancellation duplicate side effects unless boundaries are explicit

This module treats temporal and concurrent behavior as part of object design, not as
plumbing to bolt on later.

## Main questions

- Which clock should an object depend on, and why?
- How should deadlines, expiration, and timeouts be represented?
- When do locks belong inside an object, and when are queues or ownership transfer cleaner?
- How do sync and async APIs meet without infecting the whole design?
- How do you design for cancellation and retries without duplicating work?

## Reading path

1. Start with clocks, deadlines, and schedulers.
2. Move into threads, queues, and caches once time semantics are clear.
3. Then study async bridges, cancellation, and API design as one boundary cluster.
4. Finish with the refactor chapter to see the runtime gain temporal discipline without losing readability.

## Common failure modes

- using wall-clock time where monotonic time is required
- sharing mutable objects across threads without a clear owner
- wrapping synchronous code in async entrypoints without documenting blocking behavior
- treating cancellation as an exception detail instead of a state transition concern
- memoizing mutable or time-sensitive results without invalidation rules

## Capstone connection

The monitoring capstone already evaluates live samples and emits incidents. This module
shows how that runtime could grow scheduled polling, worker queues, time-based rules,
and async adapters while preserving aggregate ownership and explicit boundaries.

## Outcome

You should finish this module able to design Python object systems that remain clear,
testable, and safe when clocks, worker concurrency, and async integration pressure are real.
