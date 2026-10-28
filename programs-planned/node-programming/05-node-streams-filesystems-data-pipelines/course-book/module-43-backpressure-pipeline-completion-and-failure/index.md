# Module 43 — Backpressure, Pipeline, Completion, and Failure

**Progress: 43/100**

## The governing question

> How does a producer learn that downstream capacity is temporarily exhausted, and which component owns failure propagation and teardown across the complete chain?

## Why this module comes now

Module 42 described the state of one stream. Real programs connect several stages whose service rates differ. Without a backpressure protocol, a fast producer converts downstream delay into retained memory. Without a single pipeline owner, each stage may report failure while other stages remain open.

Module 42 established the stream state machine. Module 43 adds the economic rule that makes long-running pipelines viable: a producer cannot be allowed to create work indefinitely when a consumer is slower. Course 4’s admission-versus-active-work distinction now appears inside dataflow as readable queues, writable queues, transform state, and application accumulators.

Backpressure is not an optimization toggle. It is the protocol by which the downstream side communicates temporary inability to accept more data. The owner must preserve that signal through every custom stage and every manual loop.

## Observable outcomes

By the end of this module, you can:

- interpret writable.write return values and the drain event as a capacity protocol

- explain highWaterMark as a threshold rather than a universal memory bound

- use pipeline and finished with correct completion, error, and cancellation ownership

- distinguish source failure, transform failure, destination failure, and abort

- design bounded manual writers when pipeline is not the right abstraction

## The module ledger

Use this ledger while reading examples and before writing the laboratory design. It is deliberately specific to this module.

| Dimension | Question to answer |
|---|---|
| producer pace | What operation creates the next chunk or item? |
| pressure signal | Which return value or promise indicates that capacity is exhausted? |
| resume condition | What exact event or settlement permits production to continue? |
| queue unit | Is the threshold measured in bytes, chunks, or objects? |
| semantic bounds | Which record, expansion, history, or diagnostic limits exist beyond stream queues? |
| teardown | How does one failure or abort reach every stage and every pending wait? |

## Backpressure is permission to continue, not a speed measurement

Writable.write returns false when the writable buffer has reached or exceeded its threshold. The chunk has still been accepted; false means the producer should wait before writing more. The drain event later restores permission. Ignoring false does not make writes asynchronous or faster. It keeps enqueueing and transfers the cost into memory, garbage collection, and tail latency.

A correct manual writer owns one loop: write a chunk, inspect the Boolean, await drain when necessary, stop on error or abort, and call end exactly once after the source completes. It must also handle a destination that fails while the producer is waiting. stream.pipeline exists because coordinating all of those edges manually is easy to get wrong.

## highWaterMark is local and compositional

Each stage has its own readable and writable queues. A ten-stage pipeline can retain data in every stage, and transforms may hold additional algorithmic state. The total memory model is therefore the sum of queue thresholds, in-flight chunks, transform state, source and sink buffers, and domain objects. One configured highWaterMark is not a whole-pipeline bound.

Chunk size also matters. A single chunk can exceed the threshold. Object mode counts objects rather than their byte footprint. A defensible capacity statement lists each queue, its unit, and the maximum item size admitted to that queue.

## pipeline is an ownership boundary

The promise returned by pipeline settles when the connected chain reaches terminal completion or failure. It destroys participating streams when an error or abort occurs. The caller that creates the chain should await that promise and translate its result once. Attaching independent error handlers that also mutate application state can create duplicate reporting and ambiguous cleanup.

Pipeline can connect Node streams, async iterables, generators, and Web Streams. Flexibility does not remove the need for a single source of cancellation and a clear output commit point. A pipeline that writes directly to a final pathname may leave a partial file after failure even though all streams were destroyed correctly.

## Completion is not commit

A writable finishing means its stream protocol completed. It does not necessarily mean bytes are durable on storage, a remote peer accepted them semantically, or multiple outputs became visible atomically. Product-level commit requires additional steps after the pipeline: file synchronization and rename, protocol acknowledgment, manifest installation, or coordinated result publication.

Keep these layers named separately. Pipeline success authorizes the next commit step; it is not automatically the commit itself. If commit then fails, report whether the candidate remains staged, whether the previous output remains visible, and what cleanup occurred.

## Cancellation must reach every blocking edge

Passing an AbortSignal to pipeline destroys the chain with an AbortError. Custom async generators inside the pipeline also receive a signal and must observe it during their own waits. A generator that ignores the signal can prevent the pipeline promise from settling even after the surrounding streams have been destroyed.

Cancellation is cooperative at user-defined boundaries. If a Transform performs a long synchronous computation inside _transform, abort cannot interrupt that JavaScript until it returns. Course 4’s fairness rule therefore remains active inside stream stages.

## `write()` returning false is a contract

A writable accepts the chunk passed to `write()` even when the method returns `false`. The false result means the caller should stop producing until `drain`. Writing the same chunk again after `drain` duplicates data; continuing to write new chunks ignores the pressure protocol and can grow memory. This subtle point is central to manual stream loops.

The promise-based `pipeline` helper exists to coordinate pressure, errors, closure, and teardown for common linear graphs. Prefer it when its ownership model matches the product. Manual loops are appropriate when the application needs custom branching, per-item decisions, or protocol steps that cannot be expressed as a stream chain—but then the application inherits the complete pressure and lifecycle proof.

## A high-water mark is a threshold, not a memory budget

The threshold is measured in bytes for byte-mode streams and in objects for object-mode streams. It describes a queue state at one stream boundary. It does not include native buffers, in-flight transform work, unfinished records, retained views, child-process pipes, compressed expansion, or arrays collected by application code.

A credible memory argument enumerates every retained region and gives a unit and limit for each. Backpressure prevents one important class of unbounded producer/consumer mismatch; semantic limits prevent an individual item or side structure from defeating that protection.

## Failure ownership is inseparable from pressure ownership

A producer waiting for `drain` must also be released when the destination errors, closes unexpectedly, or the operation is aborted. Waiting only for `drain` can hang forever after failure. `events.once` with an AbortSignal, `pipeline`, or a carefully constructed race can make the wait terminal on every relevant path.

The function that connects the stages should own the resulting promise. It should not expose a writable and separately tell callers to listen for errors. One promise should settle only after the graph has either completed or been torn down sufficiently for the next product action.

## Worked case — A manual writer that respects pressure

```ts
import { once } from 'node:events';
import type { Writable } from 'node:stream';

export async function writeChunks(
  destination: Writable,
  chunks: AsyncIterable<Uint8Array>,
  signal?: AbortSignal,
): Promise<void> {
  for await (const chunk of chunks) {
    signal?.throwIfAborted();
    if (!destination.write(chunk)) {
      await once(destination, 'drain', { signal });
    }
  }
  destination.end();
  await once(destination, 'finish', { signal });
}
```

This example illustrates the capacity loop but is still incomplete as a general replacement for pipeline: an error event while no drain or finish wait is active can become unowned, and aborting the once wait does not automatically destroy the destination. The principled production design either wraps the full error and destroy protocol or uses pipeline. The course asks the reader to recognize the missing obligations rather than copy a superficially plausible helper.

## Extended case analysis

A source can produce one million 1 KB chunks while the destination accepts one chunk per second. If a manual loop ignores `write() === false`, the destination queue can retain roughly a gigabyte plus overhead. If the loop pauses on `drain`, queued data remains near the configured threshold—but an unfinished 200 MB logical record or an array of all diagnostics can still dominate memory. The complete capacity proof therefore combines pressure with semantic limits.

## What this mechanism establishes

A correct implementation establishes these local facts:

- Each source chunk is written exactly once.

- Production pauses after `write()` returns false and resumes only after capacity returns.

- Abort and destination failure settle the owning promise.

It does **not** establish the stronger claims hidden by these shortcuts:

- writing the false-return chunk a second time;

- continuing production after false;

Those distinctions are part of the public contract. Later modules may add stronger guarantees, but they must not be backdated into this mechanism.

## Decision procedure

1. List every queue and identify its unit and maximum admitted item.

2. Choose pipeline unless manual fan-out or a special protocol genuinely requires custom coordination.

3. Give one scope ownership of completion, failure translation, and cancellation.

4. Separate stream completion from product commit.

5. Test a slow destination, a failing transform, a failing destination, source abort, and early source end.

6. Measure retained memory under sustained mismatch rather than only throughput on a fast path.

Make each answer visible in an API, graph, or test. Labels such as “streaming,” “safe,” and “atomic” are incomplete until representation, owner, bound, and terminal evidence are named.

## Common wrong models

### Awaiting write()

write returns a Boolean, not a promise. Treating it as awaitable ignores the drain protocol.

### Calling end after pipeline

Pipeline normally owns destination end. A second end obscures lifecycle and can cause errors.

### Setting a tiny highWaterMark as a global fix

It changes local scheduling but does not bound item size, stage count, or algorithmic retention.

### Catching pipeline failure and keeping the partial output

Stream cleanup does not make the file semantically complete.

## Apply the mechanism in FlowLedger

Create FlowLedger’s pipeline owner. Connect source, counting, decoding, transformation, serialization, optional compression, and staged output under one AbortSignal and one terminal report.

Before editing FlowLedger, record the changed edge, owner, bound, and success observation. Update implementation, errors, tests, documentation, and report as one feature.

## Independent transfer

Design a network uploader whose request body is a Readable and whose response acknowledgment is the semantic commit. Separate write pressure, pipeline completion, HTTP response, and final product success.

The transfer is successful when the new design preserves the module’s governing relationship without copying the laboratory’s domain names or relying on its exact data shape.

## Practice sequence

1. Reconstruct the module ledger from memory.
2. Read the worked case and mark every copy, view, queue, wait, and terminal observation.
3. Predict all eight Module 43 investigations before running them.
4. Complete the workbook’s diagnosis section without broad assertions or whole-input shortcuts.
5. Build **Backpressure Copy Engine** from the starter package.
6. Compare only after your adversarial tests pass, beginning with the first different design decision.
7. Transfer the mechanism into FlowLedger and explain one earlier-course invariant that could regress.

## Readiness standard

Continue only when you can:

- Interpret writable.write return values and the drain event as a capacity protocol

- Explain highWaterMark as a threshold rather than a universal memory bound

- Use pipeline and finished with correct completion, error, and cancellation ownership

- Distinguish source failure, transform failure, destination failure, and abort

- Design bounded manual writers when pipeline is not the right abstraction
- explain which observation is necessary but insufficient for product completion;
- state one capacity or durability guarantee this module deliberately does not make;
- defend the laboratory’s failure path without reading the reference source.

## Primary references

- [https://nodejs.org/docs/latest-v24.x/api/stream.html#buffering](https://nodejs.org/docs/latest-v24.x/api/stream.html#buffering)
- [https://nodejs.org/docs/latest-v24.x/api/stream.html#streampipelinesource-transforms-destination-options](https://nodejs.org/docs/latest-v24.x/api/stream.html#streampipelinesource-transforms-destination-options)

The chapter is self-contained. These links are primary-source routes for checking version-sensitive Node.js details.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-43-backpressure-copy-engine/README.md)
- [FlowLedger engineering guide](../capstone.md)
