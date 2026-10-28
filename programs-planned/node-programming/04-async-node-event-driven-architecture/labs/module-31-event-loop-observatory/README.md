# Event Loop Observatory

## Product

Build two related tools: a **schedule observatory** that records a controlled event-loop trace, and a **cooperative mapper** that performs bounded in-memory work without monopolizing the event loop. The observatory is allowed to report the exact order it saw. The mapper may rely only on documented partial orders and its own explicit sequencing.

Read [Module 31](../../course-book/module-31-event-loop-scheduling-fairness-and-blocking/index.md) before implementation.

## Public API

The package should export:

```ts
export interface TraceEntry {
  readonly label: string;
  readonly source: 'sync' | 'next-tick' | 'microtask' | 'timer' | 'immediate';
  readonly sequence: number;
}

export function observeTurn(): Promise<readonly TraceEntry[]>;

export function cooperativeMap<T, U>(
  values: readonly T[],
  chunkSize: number,
  map: (value: T, index: number) => U,
  signal?: AbortSignal,
): Promise<readonly U[]>;
```

`observeTurn` must terminate without relying on a global listener or an unbounded recursive queue. `cooperativeMap` must preserve source order and must not create one promise per element.

## Required behavior

- Synchronous entries are recorded before scheduled entries.
- The trace identifies the scheduling surface instead of pretending all callbacks are equivalent.
- Tests assert guaranteed relations and separately display context-specific observations.
- Invalid chunk sizes fail before any mapper invocation.
- Cancellation is checked before a chunk begins.
- A nonfinal chunk yields through an ordinary event-loop phase.
- Mapping failure rejects the operation and does not fabricate partial success.
- The result array contains exactly one value for every successfully processed source element, in source order.

## Adversarial evidence

Add tests for an empty source, one element, a chunk larger than the source, exact chunk boundaries, mapper failure, pre-abort, and abort requested between chunks. Include a controlled “other immediate” that proves the mapper relinquishes the event loop before a sufficiently large job completes. Do not use an arbitrary sleep as proof.

Add a capped recursive microtask experiment. The cap is part of the safety contract: the laboratory demonstrates how starvation begins without allowing the test suite itself to starve indefinitely.

## Prohibited shortcuts

`await Promise.resolve()` is not accepted as the only fairness yield. A huge chunk is not accepted merely because the output is correct. A test that asserts a universal timer/immediate total order is incorrect. Do not use `any`, suppress checker errors, or leave a promise without an owner.

## Design record

Submit a one-page schedule ledger with columns for operation, readying authority, queue or phase, earliest legal execution, and potential delay. State which observations are platform traces, which relations are documented guarantees, and which ordering is established by your own code.

## Independent transfer

Apply the cooperative pattern to a log-search or validation workload. Change the result policy—such as returning only matches or stopping at the first match—and re-derive cancellation latency and deterministic ordering. The transfer should prove that you understand the scheduling boundary rather than the laboratory’s names.

## Implementation stages

1. Implement trace recording with monotonically increasing sequence numbers.
2. Add one case for synchronous, next-tick, microtask, timer, and immediate scheduling.
3. Separate assertions about guaranteed edges from the displayed full trace.
4. Implement cooperative mapping with a pluggable yield function so tests can observe yields directly.
5. Add abort and mapper-failure cleanup.
6. Add an adaptive time-slice variant as an optional extension and compare its API cost with fixed chunks.

## Review questions

Why is the trace not a scheduler authority? Which source contexts may alter timer/immediate observation? What bounds the largest synchronous region? What happens to the partially built result after mapper failure or cancellation? When would this design become inappropriate compared with a stream or worker?

## Completion evidence

Include the public declarations, a trace annotated as guarantee or observation, source-order tests, cancellation tests, and a short blocking-budget calculation. The reference implementation is useful only after these artifacts exist.
