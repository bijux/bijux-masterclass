# Async Node.js Reference Desk

This page is for retrieval after the chapters have been studied. It is not a substitute for the reasoning developed in Modules 31–40.

## Scheduling

| Surface | What it means | Frequent false claim |
|---|---|---|
| current callback | ordinary JavaScript runs to completion | another timer can preempt halfway through |
| `process.nextTick` | Node-specific priority queue | safe to recurse without starving phases |
| microtask | promise reaction or `queueMicrotask` job | equivalent to yielding to I/O |
| timer | eligible after threshold | runs exactly at the requested time |
| immediate | check-phase callback | universally before or after zero timer |
| I/O continuation | JavaScript callback made ready after host completion | host completion means callback already ran |

## Promise policy

| Tool | Reports | Does not provide |
|---|---|---|
| `all` | values or first observed rejection | sibling cancellation or complete failure report |
| `allSettled` | one settlement per input | capacity or fail-fast policy |
| `race` | first settlement | loser cancellation or joining |
| `any` | first fulfillment or aggregate rejection | loser cancellation or effect reconciliation |
| supervisor | policy-defined terminal set | implicit external rollback |

## Cancellation and deadlines

- Controller owns cancellation authority; signal exposes observation.
- Abort is one-shot and carries a reason.
- Check pre-abort before admission and at bounded cooperative checkpoints.
- Timeout proves a waiting deadline expired, not that an effect did not commit.
- Child deadline is no later than parent deadline.
- Clear timer and listener resources in every terminal path.

## Events

- Ordinary EventEmitter listeners run synchronously in registration order.
- Returned promises are not awaited.
- Reentrancy is possible.
- Unhandled `'error'` has special fatal behavior.
- Events should follow authoritative transitions.
- Every subscription requires an owner and disposer.

## Async sequences

```text
open → closing-with-buffer → closed
  ↘ failed
  ↘ consumer-returned
```

Pull at the consumer boundary does not prove upstream backpressure. State capacity, overflow, close, failure, abort, and early-return policy. Single-consumer queue and broadcast stream are different abstractions.

## Context

Use AsyncLocalStorage for small immutable correlation metadata. Pass security and domain authority explicitly. Prefer run-scoped context. Stable diagnostics channels carry structured messages; identifiers belong in messages, not dynamically generated channel names.

## Supervision

```text
accepted = succeeded + failed + timed-out + cancelled + blocked
```

Gate producer invocation with capacity. Join running work after cancellation. Reconstruct final output by stable source identity.

## Process lifecycle

```text
new → starting → ready → quiescing → draining → forcing? → closed
             ↘ startup-failed ↗
```

The executable owns signals. Stop admission first. Use one absolute grace deadline. Set `process.exitCode` after awaited cleanup; do not use `process.exit` as a cleanup mechanism.

## Primary references

- Event loop guide: <https://nodejs.org/en/learn/asynchronous-work/event-loop-timers-and-nexttick>
- Timers: <https://nodejs.org/api/timers.html>
- Events: <https://nodejs.org/api/events.html>
- Async context: <https://nodejs.org/api/async_context.html>
- Diagnostics channel: <https://nodejs.org/api/diagnostics_channel.html>
- Process: <https://nodejs.org/api/process.html>
- ECMAScript specification: <https://tc39.es/ecma262/>
