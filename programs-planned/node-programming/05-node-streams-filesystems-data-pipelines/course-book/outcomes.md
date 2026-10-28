# Course 5 Observable Outcomes

## Module 41 — Binary Data: Buffer, Uint8Array, Encodings, and Memory Views

- distinguish Buffer, Uint8Array, ArrayBuffer, DataView, Blob, string, and their conversion boundaries
- predict whether an operation copies bytes or creates an aliasing view
- parse and encode fixed binary fields with explicit endianness and checked ranges
- validate text and binary-to-text encodings instead of relying on permissive truncation
- design byte APIs that state ownership, mutation, and lifetime expectations clearly

**Independent proof:** Bounded Binary Envelope  
**Cumulative proof:** Define FlowLedger byte limits and the raw-byte accounting layer. Add a copy-safe buffer utility, SHA-256 input tap, and tests that distinguish visible ranges from backing allocations.

## Module 42 — Stream Contracts: Readable, Writable, Duplex, and Transform

- distinguish Readable, Writable, Duplex, Transform, PassThrough, byte mode, and object mode
- trace readable and writable state without mixing incompatible consumption styles
- separate end, finish, close, error, destroy, and abort observations
- implement a small custom stream while respecting callback and terminal contracts
- choose stream APIs only when incremental data and bounded buffering are actual requirements

**Independent proof:** Stream State Observatory  
**Cumulative proof:** Define FlowLedger’s byte-mode and object-mode boundaries. Add transparent counting transforms and a single completion authority for each linear pipeline.

## Module 43 — Backpressure, Pipeline, Completion, and Failure

- interpret writable.write return values and the drain event as a capacity protocol
- explain highWaterMark as a threshold rather than a universal memory bound
- use pipeline and finished with correct completion, error, and cancellation ownership
- distinguish source failure, transform failure, destination failure, and abort
- design bounded manual writers when pipeline is not the right abstraction

**Independent proof:** Backpressure Copy Engine  
**Cumulative proof:** Create FlowLedger’s pipeline owner. Connect source, counting, decoding, transformation, serialization, optional compression, and staged output under one AbortSignal and one terminal report.

## Module 44 — Async Iteration, Web Streams, and Adapter Boundaries

- consume Readable streams through async iteration without losing cleanup ownership
- write async generators that propagate cancellation and close upstream work on early return
- adapt among Node streams, async iterables, and Web Streams while tracing backpressure direction
- distinguish one-shot iterators from repeatable iterable factories
- select an abstraction based on lifecycle and boundary requirements rather than style preference

**Independent proof:** Async Record Window  
**Cumulative proof:** Express FlowLedger’s record transforms as async-generator stages where that improves clarity. Preserve pipeline cancellation and keep the byte-to-record trust boundary explicit.

## Module 45 — Files, File Handles, Paths, and Transactional Replacement

- choose among whole-file helpers, FileHandle operations, and file streams based on size and lifecycle
- own open handles and close them on every terminal path
- distinguish pathname identity, open-file identity, visibility, replacement, flush, synchronization, and durability
- implement same-directory staged replacement with explicit cleanup and overwrite policy
- state platform and adversarial-race limitations honestly

**Independent proof:** Transactional File Sink  
**Cumulative proof:** Build FlowLedger’s staged output owner. The final pathname must change only after the entire stream pipeline succeeds and the candidate file is synchronized and closed.

## Module 46 — Incremental Text Decoding, Framing, and Bounded Parsers

- decode UTF-8 incrementally across arbitrary chunk boundaries
- distinguish byte limits, character counts, line limits, and record limits
- implement line and length framing with bounded unfinished state
- preserve physical byte and line context in structured parse errors
- separate framing, JSON syntax, runtime schema validation, and domain semantics

**Independent proof:** Bounded NDJSON Decoder  
**Cumulative proof:** Add FlowLedger’s bounded NDJSON decoder, event validator, structured diagnostic types, and canonical serializer. Malformed input must fail before the staged output becomes visible.

## Module 47 — Transform Pipelines: Compression, Hashing, and Integrity

- place compression, decompression, hashing, and serialization stages according to the claimed byte representation
- distinguish a digest of source bytes, canonical bytes, compressed bytes, and domain values
- bound decompression expansion and retained transform state
- use crypto hashes as integrity identifiers without presenting them as authentication
- design transform errors and metadata so a reader can reproduce the claim

**Independent proof:** Compressed Digest Pipeline  
**Cumulative proof:** Add optional gzip input and output to FlowLedger, separate raw-input and canonical-output digests, and ensure digest metadata is committed only with the staged output.

## Module 48 — Child Processes, Stdio, and Supervised Pipelines

- choose spawn, execFile, and exec according to shell and buffering requirements
- preserve executable and argument boundaries without command-string construction
- pipe stdin, stdout, and stderr under explicit backpressure and retention limits
- distinguish spawn error, exit, close, signal termination, and pipeline failure
- abort and join a child process without leaving descendants or partial output unowned

**Independent proof:** Supervised Child Filter  
**Cumulative proof:** Add FlowLedger’s through command. It must preserve raw byte backpressure, reject nonzero child status, retain bounded stderr, abort the direct child, and commit stdout only after process and stream success agree.

## Module 49 — Multi-Stage Dataflow, Fan-Out, and Commit Coordination

- distinguish observation taps, lossy side channels, and required fan-out branches
- coordinate backpressure across multiple required destinations
- define all-or-nothing, best-effort, and independently committed side-output policies
- stage and publish related outputs without claiming impossible filesystem atomicity
- produce deterministic reports from schedule-independent terminal evidence

**Independent proof:** Coordinated Fan-Out Writer  
**Cumulative proof:** Finalize FlowLedger reports and conservation equations. Keep the main output as the sole committed file, return digest and accounting metadata only after commit, and document how a future multi-file bundle would be versioned.

## Module 50 — Integrated Streaming Architecture, Testing, and Independent Change

- produce a complete dataflow map with representations, queues, owners, limits, and terminal conditions
- select tests that prove chunk-boundary independence, pressure, cleanup, failure atomicity, and deterministic output
- review a streaming API for hidden retention and unsupported durability claims
- implement an unseen cross-cutting feature through parser, transforms, reporting, CLI, tests, and documentation
- defend FlowLedger’s architecture without relying on implementation order or incidental traces

**Independent proof:** Streaming Architecture Audit  
**Cumulative proof:** Complete FlowLedger, its process-level CLI tests, compatibility fixtures, fault-injection suite, architecture ledger, and final independent rejects-bundle extension.

## Course completion standard

Completion means more than finishing the pages. You can take an unfamiliar file or process pipeline, draw its representation and ownership graph, identify unbounded state, repair pressure and cancellation, define the publication point, and prove the behavior with adversarial chunking and failure injection. You can also explain which durability, security, and portability claims the design deliberately does not make.
