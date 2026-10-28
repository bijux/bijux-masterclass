# Node.js Streams, Filesystems, and Data Pipeline Architecture

**Course 5 of the Node.js Programming program — Modules 41–50**

Course 5 moves from owning individual asynchronous tasks to owning sustained flows of bytes and records. It teaches how Node.js buffers, streams, file handles, incremental decoders, compression transforms, hashes, child-process pipes, and publication protocols become one bounded product rather than a chain of convenient APIs.

The course is standard-library-only. That constraint keeps the mechanics visible: `Buffer`, `Uint8Array`, `node:stream`, `node:stream/promises`, `node:fs`, `node:string_decoder`, `node:zlib`, `node:crypto`, and `node:child_process` are enough to build a serious data pipeline and to understand what higher-level libraries later automate.

## Entry standard

Begin only when you can independently build TaskHarbor or an equivalent strict TypeScript ESM system: validate external input, own promises and task trees, compose AbortSignals, publish typed events, bound concurrency, and complete graceful shutdown. Course 5 retains those responsibilities while adding stream and operating-system resource lifecycles.

## Course promise

After ten dense modules, you can:

- reason about byte allocations, views, copies, encodings, and endianness;
- trace Readable, Writable, Duplex, and Transform state;
- preserve backpressure and own complete pipeline teardown;
- cross Node stream, async iterable, and Web Stream boundaries deliberately;
- implement staged file replacement with honest durability claims;
- parse text incrementally with bounded unfinished state;
- compose compression and hashing without confusing representations;
- supervise direct child-process filters and all three standard streams;
- coordinate required branches, conservation, and publication policy;
- build and defend FlowLedger, a bounded NDJSON transformation CLI.

## Ten-module path

| Module | Subject | Independent product |
|---:|---|---|
| 41 | [Binary Data: Buffer, Uint8Array, Encodings, and Memory Views](course-book/module-41-binary-data-buffer-uint8array-encodings-and-memory-views/index.md) | [Bounded Binary Envelope](labs/module-41-bounded-binary-envelope/README.md) |
| 42 | [Stream Contracts: Readable, Writable, Duplex, and Transform](course-book/module-42-stream-contracts-readable-writable-duplex-and-transform/index.md) | [Stream State Observatory](labs/module-42-stream-state-observatory/README.md) |
| 43 | [Backpressure, Pipeline, Completion, and Failure](course-book/module-43-backpressure-pipeline-completion-and-failure/index.md) | [Backpressure Copy Engine](labs/module-43-backpressure-copy-engine/README.md) |
| 44 | [Async Iteration, Web Streams, and Adapter Boundaries](course-book/module-44-async-iteration-web-streams-and-adapter-boundaries/index.md) | [Async Record Window](labs/module-44-async-record-window/README.md) |
| 45 | [Files, File Handles, Paths, and Transactional Replacement](course-book/module-45-files-file-handles-paths-and-transactional-replacement/index.md) | [Transactional File Sink](labs/module-45-transactional-file-sink/README.md) |
| 46 | [Incremental Text Decoding, Framing, and Bounded Parsers](course-book/module-46-incremental-text-decoding-framing-and-bounded-parsers/index.md) | [Bounded NDJSON Decoder](labs/module-46-bounded-ndjson-decoder/README.md) |
| 47 | [Transform Pipelines: Compression, Hashing, and Integrity](course-book/module-47-transform-pipelines-compression-hashing-and-integrity/index.md) | [Compressed Digest Pipeline](labs/module-47-compressed-digest-pipeline/README.md) |
| 48 | [Child Processes, Stdio, and Supervised Pipelines](course-book/module-48-child-processes-stdio-and-supervised-pipelines/index.md) | [Supervised Child Filter](labs/module-48-supervised-child-filter/README.md) |
| 49 | [Multi-Stage Dataflow, Fan-Out, and Commit Coordination](course-book/module-49-multi-stage-dataflow-fan-out-and-commit-coordination/index.md) | [Coordinated Fan-Out Writer](labs/module-49-coordinated-fan-out-writer/README.md) |
| 50 | [Integrated Streaming Architecture, Testing, and Independent Change](course-book/module-50-integrated-streaming-architecture-testing-and-independent-change/index.md) | [Streaming Architecture Audit](labs/module-50-streaming-architecture-audit/README.md) |

## Primary learning route

Start with the [course book](course-book/index.md). For each module, read the authoritative chapter, complete the workbook, predict the eight investigations, build the independent laboratory, and only then transfer the mechanism into [FlowLedger](course-book/capstone.md).

## Course boundary

Course 5 does not yet teach HTTP servers, TCP protocol design, databases, worker threads, or production observability platforms. It provides the byte, stream, filesystem, and subprocess foundations those later courses require.

## Verification

```bash
make verify
```

This compatibility route runs the structural audit, links, TypeScript source policy, 80 investigations, and all 21 executable packages. `make proof` additionally requires the exact pinned Node.js, npm, TypeScript, ambient type, and MkDocs baseline.
