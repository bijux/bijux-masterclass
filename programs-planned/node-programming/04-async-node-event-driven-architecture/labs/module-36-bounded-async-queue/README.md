# Bounded Async Queue

## Product

Build a single-consumer bounded asynchronous queue that can bridge a cooperative producer to `for await`. The queue must distinguish open, normal close, failure, producer abort, and consumer early return.

Read [Module 36](../../course-book/module-36-async-iterables-generators-and-pull-based-sequences/index.md).

## Public behavior

`push(value, signal?)` resolves when the value has been accepted into capacity or delivered directly to a waiting consumer. `take()` returns one item, done after normal close and drain, or rejects after failure. `close()` ends admission but preserves buffered values. `fail(reason)` rejects waiters and ends the sequence. The object supports exactly one async consumer.

## Capacity invariant

At all times:

```text
0 <= buffered <= capacity
```

When the buffer is full, producers wait in FIFO order. Taking one item creates at most one free slot and admits exactly one waiting producer. Pending-producer count may grow only if the calling application itself admits unbounded producers; the laboratory must document this outer bound rather than claim the queue bounds all memory by itself.

## Terminal obligations

Normal close rejects blocked producers, drains accepted buffered values, then returns done. Failure rejects consumers and producers and discards buffered values. Consumer early return detaches the sequence and settles all waiters. Abort of one blocked producer removes only that producer.

## Required tests

Cover direct handoff to a waiting consumer, full-buffer producer waiting, FIFO admission, close-after-drain, fail with pending consumer, fail with pending producer, producer abort, early `break`, and second-consumer rejection. Use deferred control rather than sleeps.

## Demand and memory ledger

For every public operation, record how many unresolved producer admissions, buffered items, waiting consumers, and in-flight callbacks can exist. Add a byte estimate when item size varies. Tests should fill the queue, block one producer, consume one item, and prove exactly one admission proceeds.

Early consumer return must invoke queue or upstream cleanup. Test failure while a producer is waiting, close with buffered items, close with waiting consumers, repeated close, and cancellation during a pending `next()`.

## Early-return proof

Use `for await...of` with an early `break` and prove that pending producers or listeners are released. Include upstream `return()` failure. The terminal report must preserve the reason iteration stopped and any cleanup defect.

## Adapter extension

Add one cancellation-aware `take` or `map` adapter and prove upstream close occurs on early completion, failure, and consumer cancellation.

## Independent transfer

Adapt the queue to a “latest value” telemetry channel that coalesces old values instead of preserving every item. Explain why this is a different delivery contract and which applications may safely use it.

## Implementation stages

Implement direct consumer handoff, finite buffering, blocked producers, and FIFO capacity release. Add normal close, failure, abort, and early return in that order. Only then expose `[Symbol.asyncIterator]`. Ensure every pending promise has a terminal path.

## Review questions

Are concurrent pulls allowed? Does close drain or discard? Does failure preserve buffered items? What happens to blocked producers after consumer return? Is capacity item-based, byte-based, or both?

## Completion evidence

Include a waiter-state diagram, tests with several pending `next()` calls, early-return cleanup, and a retention calculation for large items. Explain how this queue differs from the streams introduced in Course 5.
