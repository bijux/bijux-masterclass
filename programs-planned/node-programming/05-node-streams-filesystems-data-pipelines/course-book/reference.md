# Course 5 Reference Desk

Use this page after learning a module, not instead of learning it. It collects the decision procedures and primary platform references in one place.

## Shared vocabulary

- **chunk** — one unit delivered by a stream implementation; it is not automatically a record;
- **backpressure** — a protocol by which downstream capacity controls upstream continuation;
- **highWaterMark** — a local queue threshold, not a complete memory bound;
- **framing** — reconstruction of logical records from arbitrary byte chunks;
- **stage** — one transformation or resource boundary in a dataflow;
- **candidate** — complete output not yet published as the visible product;
- **publication point** — the operation after which readers can observe the new product;
- **post-commit failure** — a failure after publication that must not be reported as if no change occurred;
- **conservation equation** — an invariant that accounts for every accepted byte, record, or operation exactly once.

## Module 41 — Binary Data: Buffer, Uint8Array, Encodings, and Memory Views

**Decision procedure**

1. Name the logical representation: raw bytes, encoded text, decoded string, or typed fields.
2. Record the backing allocation and visible range for every view.
3. Decide whether the API promises borrowed observation, shared mutation, or an owned copy.
4. Validate lengths and integer arithmetic before allocation, slicing, or decoding.
5. Specify endianness and canonical encoding in the format contract.
6. Test aliasing explicitly by mutating the source after the operation.

**Primary sources**

- https://nodejs.org/docs/latest-v24.x/api/buffer.html
- https://nodejs.org/docs/latest-v24.x/api/util.html#class-utiltextdecoder

## Module 42 — Stream Contracts: Readable, Writable, Duplex, and Transform

**Decision procedure**

1. Name the stream direction from the caller’s perspective.
2. State whether the unit is bytes, strings, or objects.
3. Choose one consumption style and one completion primitive.
4. Identify every internal or external queue and its measurement unit.
5. State who destroys the stream after error, cancellation, or early return.
6. Keep custom hook callbacks single, causal, and terminally complete.

**Primary sources**

- https://nodejs.org/docs/latest-v24.x/api/stream.html

## Module 43 — Backpressure, Pipeline, Completion, and Failure

**Decision procedure**

1. List every queue and identify its unit and maximum admitted item.
2. Choose pipeline unless manual fan-out or a special protocol genuinely requires custom coordination.
3. Give one scope ownership of completion, failure translation, and cancellation.
4. Separate stream completion from product commit.
5. Test a slow destination, a failing transform, a failing destination, source abort, and early source end.
6. Measure retained memory under sustained mismatch rather than only throughput on a fast path.

**Primary sources**

- https://nodejs.org/docs/latest-v24.x/api/stream.html#buffering
- https://nodejs.org/docs/latest-v24.x/api/stream.html#streampipelinesource-transforms-destination-options

## Module 44 — Async Iteration, Web Streams, and Adapter Boundaries

**Decision procedure**

1. Identify whether the source is a resource, a sequence, or both.
2. State whether the value is one-shot or repeatable.
3. Choose the abstraction whose lifecycle operations match the caller’s responsibility.
4. Trace demand and cancellation in both directions through every adapter.
5. Normalize chunk ownership when an adapter crosses Buffer and Uint8Array expectations.
6. Test early return, source error, consumer error, abort, and repeated iteration.

**Primary sources**

- https://nodejs.org/docs/latest-v24.x/api/stream.html#streams-compatibility-with-async-generators-and-async-iterators
- https://nodejs.org/docs/latest-v24.x/api/webstreams.html

## Module 45 — Files, File Handles, Paths, and Transactional Replacement

**Decision procedure**

1. State the maximum input or output size and choose whole-file or streaming I/O accordingly.
2. Name the scope that owns each FileHandle or file stream.
3. Separate candidate completion, synchronization, visibility, and durability claims.
4. Choose no-overwrite, replace-existing, or versioned-output policy explicitly.
5. Place the stage beside the destination and create it exclusively.
6. Test failure before write, during write, during sync, before rename, and after rename.

**Primary sources**

- https://nodejs.org/docs/latest-v24.x/api/fs.html
- https://nodejs.org/docs/latest-v24.x/api/path.html

## Module 46 — Incremental Text Decoding, Framing, and Bounded Parsers

**Decision procedure**

1. Specify whether framing is byte-defined or text-defined.
2. Choose strict or replacement decoding and state the consequence.
3. Bound one unfinished frame independently of stream queue thresholds.
4. Advance line and byte positions only after a frame is accepted.
5. Keep framing, syntax, schema, and domain errors distinct.
6. Test all boundary splits, empty records, final records, malformed encoding, and over-limit input.

**Primary sources**

- https://nodejs.org/docs/latest-v24.x/api/string_decoder.html
- https://nodejs.org/docs/latest-v24.x/api/util.html#class-utiltextdecoder

## Module 47 — Transform Pipelines: Compression, Hashing, and Integrity

**Decision procedure**

1. Draw every representation edge from source bytes to final bytes.
2. Place each digest at the edge whose identity the product needs.
3. Define compressed-input, expanded-byte, frame, and record limits separately.
4. Keep transform finalization owned by the pipeline scope.
5. Publish digests only with status that distinguishes attempted, staged, and committed data.
6. Test empty input, tiny chunks, corrupt compressed data, expansion limits, destination failure, and abort.

**Primary sources**

- https://nodejs.org/docs/latest-v24.x/api/zlib.html
- https://nodejs.org/docs/latest-v24.x/api/crypto.html

## Module 48 — Child Processes, Stdio, and Supervised Pipelines

**Decision procedure**

1. Decide whether shell syntax is truly required; default to direct spawn.
2. Specify the executable-resolution, environment, and working-directory policy.
3. Bound retained stdout or stream it; always drain stderr with a retention limit.
4. Own stdin completion, stdout completion, stderr drain, and child close together.
5. Define acceptable exit codes and signal outcomes separately from byte validity.
6. Test spawn failure, early child exit, nonzero exit with output, stderr flood, abort, and destination failure.

**Primary sources**

- https://nodejs.org/docs/latest-v24.x/api/child_process.html

## Module 49 — Multi-Stage Dataflow, Fan-Out, and Commit Coordination

**Decision procedure**

1. Classify every side output by authority and failure policy.
2. Draw each queue and identify which branches must receive every item.
3. Coordinate pressure at the branch point rather than after memory has accumulated.
4. Choose one explicit multi-output publication protocol and state its limits.
5. Define conservation equations for bytes, records, and terminal outcomes.
6. Test every branch failing at several positions and inspect visible artifacts afterward.

**Primary sources**

- https://nodejs.org/docs/latest-v24.x/api/stream.html
- https://nodejs.org/docs/latest-v24.x/api/fs.html

## Module 50 — Integrated Streaming Architecture, Testing, and Independent Change

**Decision procedure**

1. Draw the end-to-end representation graph and label every edge.
2. List all queues, accumulators, stages, handles, child processes, and temporary files.
3. Assign one lifecycle owner and one terminal observation to each resource.
4. Write the failure and commit matrix before implementing a cross-layer feature.
5. Test semantic invariance across chunking, timing, and pressure variations.
6. Review public claims for unsupported words such as atomic, durable, zero-copy, bounded, and validated.

**Primary sources**

- https://nodejs.org/docs/latest-v24.x/api/stream.html
- https://nodejs.org/docs/latest-v24.x/api/test.html
