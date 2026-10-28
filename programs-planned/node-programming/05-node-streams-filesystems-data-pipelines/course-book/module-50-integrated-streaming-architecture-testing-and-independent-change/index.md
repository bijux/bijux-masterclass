# Module 50 — Integrated Streaming Architecture, Testing, and Independent Change

**Progress: 50/100**

## The governing question

> Can you review and evolve a complete Node.js dataflow system without losing byte semantics, pressure, parser bounds, resource ownership, commit rules, or deterministic evidence?

## Why this module comes now

The previous nine modules introduced local mechanisms. Module 50 treats the pipeline as one product. The challenge is not remembering every API; it is preserving one coherent story from external bytes to a committed output while failures, cancellation, subprocesses, compression, and reporting cross several layers.

The first nine modules each isolated one boundary. Module 50 removes that isolation. A complete data pipeline can be locally correct at every stage and still fail globally because two stages disagree about representation, cancellation stops at an adapter, a child exits after its stdout is committed, or a report is built before the final pathname changes.

Mastery therefore means constructing and reviewing the end-to-end proof. The reader must trace one byte from source to publication, one failure from detection to cleanup, and one cancellation request through every pending wait.

## Observable outcomes

By the end of this module, you can:

- produce a complete dataflow map with representations, queues, owners, limits, and terminal conditions

- select tests that prove chunk-boundary independence, pressure, cleanup, failure atomicity, and deterministic output

- review a streaming API for hidden retention and unsupported durability claims

- implement an unseen cross-cutting feature through parser, transforms, reporting, CLI, tests, and documentation

- defend FlowLedger’s architecture without relying on implementation order or incidental traces

## The module ledger

Use this ledger while reading examples and before writing the laboratory design. It is deliberately specific to this module.

| Dimension | Question to answer |
|---|---|
| representation graph | What does data mean on every edge from input bytes to final bytes? |
| resource tree | Which owner closes each stream, handle, child, iterator, timer, and stage file? |
| capacity map | Which queue or retained state can grow, in what unit, and to what maximum? |
| failure graph | Which failures cancel which stages and which evidence survives? |
| commit matrix | What is visible before, at, and after publication? |
| verification map | Which test, investigation, or review can falsify each product claim? |

## The full ledger has six dimensions

For every stage, record representation, ownership, capacity, cancellation, failure, and completion. Representation says what chunks mean. Ownership says who creates and destroys the stage. Capacity lists queues and item limits. Cancellation lists the signal and blocking edges. Failure records causal translation. Completion identifies the observation that authorizes the next product state.

A diagram that shows only arrows between classes is insufficient. A correct system can still be unbounded, leak a child process, commit partial output, or publish nondeterministic evidence.

## Testing must vary boundaries, not only values

Stream bugs hide in chunking, timing, and terminal order. Re-run the same logical input under one-byte chunks, large chunks, delimiters at every boundary, slow sinks, early abort, transform failure after partial output, destination failure, and child exit races. The semantic result should remain stable where the product claims stability.

Use small deterministic custom Readables and Writables rather than sleeps. Fault-injection stages can fail after a named byte or record count. Temporary directories let tests inspect whether the previous destination, stage file, and final output match the commit matrix.

## Performance claims need the correct denominator

A streaming system can reduce peak retained memory while being slower on tiny files. It can increase throughput while increasing tail latency or buffering. Course 5 does not perform full production benchmarking, but it requires honest counters: source bytes, expanded bytes, records, emitted bytes, queue thresholds, and elapsed phases. Course 8 and 9 will deepen concurrency and production measurement.

Do not use the number of data events as a record count or treat chunk count as stable across platforms. Chunks are transport observations.

## Public APIs should expose product outcomes, not stream internals

Most callers need a typed operation result and cancellation input, not access to every internal Transform. Keep the pipeline assembly private. Expose options that correspond to policy: maximum line bytes, gzip input, filter predicate, overwrite behavior, stderr limit, and signal. Avoid leaking highWaterMark controls unless the caller has enough context to use them responsibly.

When a caller does need a reusable transform, document input and output modes, retention, error codes, cancellation expectations, and whether chunks may be aliased or mutated.

## Independent change reveals architectural truth

The final feature is a rejects-output bundle. It adds a required side output for invalid domain records while preserving fatal syntax errors. The reader must decide whether invalid records are terminal rejects or pipeline failures, how the second file is staged, how both outputs are published, how conservation changes, and how old CLI behavior remains compatible.

A change that touches only one Transform is incomplete. Grammar, types, commit protocol, report, tests, help text, and failure matrix must agree.

## Local correctness does not compose automatically

A decoder may bound lines correctly while a reporter retains every diagnostic. A stream pipeline may preserve pressure while a child-process helper buffers complete stdout. A transactional sink may preserve the old file while a separate metadata file is published early. Whole-system review searches for these contract gaps between components.

Draw edges, not just boxes. Each edge should name representation, ownership, pressure, cancellation, error translation, and completion. Most integration defects occur where one component’s output is described more strongly than the next component can rely on.

## Testing must vary chunking, timing, and failure position

A pipeline that passes one fixture with default chunk sizes has weak evidence. Repartition the same bytes into one-byte chunks, large chunks, and splits around delimiters and multibyte characters. Slow each destination. Fail sources, transforms, sinks, child stdio, and publication after exact progress counts. Abort while waiting at every blocking edge.

The expected semantic report should remain stable whenever the product promises chunk- and schedule-independence. Differences in internal event order are acceptable; differences in records, digests, terminal categories, or visible files require explanation.

## Architecture records make future change safer

A representation graph, capacity ledger, resource tree, and commit matrix are not internal bureaucracy when they directly explain the product. They tell the next maintainer where to place a new gzip stage, which digest it changes, which limit protects it, and which tests must be updated.

Keep these records beside the course capstone and write them in reader language. Avoid release-process jargon. The point is to make code review and independent extension possible without reconstructing every hidden assumption from implementation details.

## Worked case — The flowledger stage ledger

```ts
export interface StageContract {
  readonly name: string;
  readonly input: string;
  readonly output: string;
  readonly capacity: string;
  readonly owner: string;
  readonly completion: string;
  readonly failure: string;
}

export const FLOW_LEDGER_STAGES: readonly StageContract[] = [
  { name: 'source', input: 'pathname', output: 'raw bytes', capacity: 'readable queue', owner: 'operation', completion: 'readable end', failure: 'I/O error' },
  { name: 'decoder', input: 'raw bytes', output: 'validated events', capacity: 'max line bytes', owner: 'pipeline', completion: 'flush with no partial frame', failure: 'decode, syntax, or schema error' },
  { name: 'sink', input: 'canonical bytes', output: 'staged file', capacity: 'writable queue', owner: 'transaction', completion: 'finish, sync, close', failure: 'write or sync error' },
];
```

The ledger is documentation as data, not a substitute for executable tests. It exposes missing dimensions: the source also needs a maximum accepted file policy; the decoder needs explicit cancellation; the sink needs a publication step after completion. Reviewing an intentionally incomplete table is part of the module’s method.

## Extended case analysis

FlowLedger normalizes a gzip input through an optional child filter into a staged gzip output. A complete review asks: Is the input digest compressed or expanded? Is the child before or after schema validation? Can cancellation stop while waiting for stderr? Is the expanded-byte limit before the parser? Does the final report appear only after rename? Which file remains after nonzero child exit? One diagram can expose contradictions that isolated unit tests miss.

## What this mechanism establishes

A correct implementation establishes these local facts:

- Input chunking does not change accepted records or canonical output.

- Every inspected record becomes emitted or filtered exactly once.

- Source SHA-256 identifies the exact incoming bytes.

It does **not** establish the stronger claims hidden by these shortcuts:

- calling a diagram complete without queues and terminal states;

- using live counters as authoritative final accounting;

Those distinctions are part of the public contract. Later modules may add stronger guarantees, but they must not be backdated into this mechanism.

## Decision procedure

1. Draw the end-to-end representation graph and label every edge.

2. List all queues, accumulators, stages, handles, child processes, and temporary files.

3. Assign one lifecycle owner and one terminal observation to each resource.

4. Write the failure and commit matrix before implementing a cross-layer feature.

5. Test semantic invariance across chunking, timing, and pressure variations.

6. Review public claims for unsupported words such as atomic, durable, zero-copy, bounded, and validated.

Make each answer visible in an API, graph, or test. Labels such as “streaming,” “safe,” and “atomic” are incomplete until representation, owner, bound, and terminal evidence are named.

## Common wrong models

### Testing only happy-path files

Chunking, slow destinations, abort, and partial failure contain the important stream defects.

### Exposing internal streams as the primary API

Callers inherit cleanup and state obligations that the product should own.

### Using zero-copy as an unconditional goal

Aliasing and retained backing stores can make a copy the safer and cheaper boundary.

### Adding a feature without updating conservation and commit rules

The implementation and product contract diverge.

## Apply the mechanism in FlowLedger

Complete FlowLedger, its process-level CLI tests, compatibility fixtures, fault-injection suite, architecture ledger, and final independent rejects-bundle extension.

Before editing FlowLedger, record the changed edge, owner, bound, and success observation. Update implementation, errors, tests, documentation, and report as one feature.

## Independent transfer

Add a resumable import checkpoint to a streaming system. Define what state can be replayed safely, what byte position means after decoding and filtering, and how the checkpoint is committed with the data.

The transfer is successful when the new design preserves the module’s governing relationship without copying the laboratory’s domain names or relying on its exact data shape.

## Practice sequence

1. Reconstruct the module ledger from memory.
2. Read the worked case and mark every copy, view, queue, wait, and terminal observation.
3. Predict all eight Module 50 investigations before running them.
4. Complete the workbook’s diagnosis section without broad assertions or whole-input shortcuts.
5. Build **Streaming Architecture Audit** from the starter package.
6. Compare only after your adversarial tests pass, beginning with the first different design decision.
7. Transfer the mechanism into FlowLedger and explain one earlier-course invariant that could regress.

## Readiness standard

Continue only when you can:

- Produce a complete dataflow map with representations, queues, owners, limits, and terminal conditions

- Select tests that prove chunk-boundary independence, pressure, cleanup, failure atomicity, and deterministic output

- Review a streaming API for hidden retention and unsupported durability claims

- Implement an unseen cross-cutting feature through parser, transforms, reporting, CLI, tests, and documentation

- Defend FlowLedger’s architecture without relying on implementation order or incidental traces
- explain which observation is necessary but insufficient for product completion;
- state one capacity or durability guarantee this module deliberately does not make;
- defend the laboratory’s failure path without reading the reference source.

## Primary references

- [https://nodejs.org/docs/latest-v24.x/api/stream.html](https://nodejs.org/docs/latest-v24.x/api/stream.html)
- [https://nodejs.org/docs/latest-v24.x/api/test.html](https://nodejs.org/docs/latest-v24.x/api/test.html)

The chapter is self-contained. These links are primary-source routes for checking version-sensitive Node.js details.

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-50-streaming-architecture-audit/README.md)
- [FlowLedger engineering guide](../capstone.md)
