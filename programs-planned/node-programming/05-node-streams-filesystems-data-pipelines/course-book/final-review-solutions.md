# Course 5 Final Review — Reasoned Solutions

Use this page only after completing the review unaided. The purpose is not to compare wording. It is to test whether your model preserves the same ownership, representation, pressure, failure, and publication facts.

## Whole-course construction

A defensible converter starts with a representation graph, not a chain of convenience calls:

```text
source file bytes
    -> optional gzip decoder
    -> expanded NDJSON bytes
    -> complete framed line bytes
    -> strictly decoded text
    -> parsed unknown JSON
    -> validated FlowEvent
    -> transformed FlowEvent
    -> canonical NDJSON bytes
    -> optional gzip encoder
    -> staged output bytes
    -> visible destination pathname
```

Every edge has a unit and every stateful stage has a bound. The compressed source limit, decompressed-byte limit, unfinished-line limit, event-count limit, final-output limit, child-output limit, and retained-stderr limit are different controls. A single `highWaterMark` cannot substitute for them. One operation scope owns the source, every transform, the stage file, an optional child process, cancellation, and the terminal report. The destination becomes visible only after the candidate pipeline succeeds, the stage is flushed and synchronized according to the stated policy, and the handle is closed. A successful stream event alone is not publication.

The adversarial suite should include at least: a split multibyte character; a newline split across chunks; invalid UTF-8; one overlong unfinished line; decompression expansion beyond policy; a slow destination; a transform failure after partial output; child spawn failure; child stderr flood or output overflow; cancellation during a blocked write; and rename or synchronization failure. The report is built from terminal observations after cleanup, not from optimistic counters sampled while work remains active.

## Module 41 — Byte ownership and representation

A correct answer identifies four independent facts for every binary value: the logical representation, the visible byte range, the backing allocation, and the mutation authority. `Buffer`, `Uint8Array`, `ArrayBuffer`, and `DataView` can describe overlapping memory without representing the same API promise. Converting bytes to a string changes representation; slicing may only change the visible range. An API that returns an owned payload must copy even when a view would be cheaper, because ownership is part of the contract rather than an implementation detail.

For the thumbnail record, validate the fixed header before allocating or slicing the payload. Check the media-type code, width, height, payload length, checked offset arithmetic, and total frame size. Specify endianness in the format. Return a copied payload when the record must survive reuse or mutation of the input buffer; return a documented borrowed view only when the caller controls the backing allocation and lifetime.

The falsifying test for “`Buffer.slice` copies” is direct: create a buffer, slice it, mutate the original, and observe the slice. A retention test also matters: hold a tiny view into a large allocation and inspect whether the backing store remains reachable. FlowLedger therefore distinguishes visible ranges from owned copies, counts source bytes at the raw boundary, and names the SHA-256 value `sourceSha256`. Runtime validation from Course 1 still occurs after framing; Course 2’s identity model prevents a byte view from being mistaken for independent state; Course 4’s cancellation owner still controls the operation.

## Module 42 — Stream direction and terminal state

A stream design begins by naming direction from the caller’s perspective and the unit carried on each side. A `Readable` produces values, a `Writable` accepts them, a `Duplex` owns both protocols, and a `Transform` relates accepted input to produced output. Byte mode and object mode have different queue units. `end`, `finish`, `close`, `error`, destruction, and abort are observations of different state transitions; no single event proves the whole product succeeded.

The command/response `Duplex` should accept command objects on its writable side and emit encoded response bytes on its readable side. That requires separate object-mode and byte-mode configuration, separate pressure units, and a clear policy for command failure. Its owner must observe both sides and the underlying resource; a readable `close` cannot prove that pending writable work or response encoding succeeded.

A stream can emit `close` because it was destroyed after an error, so treating `close` as success is falsified by destroying the stream with an error and observing both events. FlowLedger uses transparent counting stages only where they preserve chunk identity, and each linear chain has one completion authority. The prior-course rule is unchanged: a resource has one lifecycle owner, and events are evidence delivered to that owner rather than ownership themselves.

## Module 43 — Pressure, completion, and causal failure

Backpressure is a protocol between production and available downstream capacity. `writable.write(chunk)` returning `false` means the producer must stop writing until the writable signals renewed capacity through `drain`; it is not a promise. A high-water mark is a queue threshold in a particular unit, not a global bound on memory or unfinished product state. `pipeline` is normally preferable for a linear chain because it coordinates error propagation and teardown, but the caller must still distinguish pipeline completion from domain commit.

For the network uploader, request-body pressure, request-stream completion, remote response status, response-body consumption, and product success are separate. The producer obeys the body stream’s pressure. The operation is not semantically committed until the expected server acknowledgement has been fully received and validated. An HTTP response arriving does not retroactively prove that local source reading, request upload, or cleanup completed correctly.

`await writable.write(chunk)` is falsified because `await` immediately accepts the Boolean result; it never waits for `drain`. FlowLedger’s pipeline owner connects source counting, optional decompression, framing, validation, transformation, serialization, optional compression, and staged output beneath one cancellation signal. If cleanup produces a secondary premature-close error after a causal parse or source failure, the report preserves the original cause rather than overwriting it with teardown noise.

## Module 44 — Sequence adapters and lifecycle preservation

Choose a Node stream when Node resource integration and stream completion semantics dominate; choose an async iterable when pull-based record traversal is the clearer contract; choose a Web Stream at a Web-platform boundary. An adapter is not a semantic no-op. It may change chunk type, lock or disturb the source, alter cancellation propagation, or obscure which object owns resource closure.

A log-tail API expressed as `AsyncIterable<LogRecord>` should be a factory when each iteration must reopen the file. The iterator scope owns the `FileHandle`, decoder, unfinished frame, cancellation listener, and cleanup. Early `return` from the consumer must run the generator’s `finally` block and close the resource. A one-shot iterator should be documented as such rather than silently returning an already-consumed object on the second iteration.

Async iteration controls when the consumer asks for the next item, but it does not erase buffering inside the file stream, decoder, transform, or adapter. A falsifying test inserts a source that eagerly buffers ahead despite slow iteration. FlowLedger uses async generators for record-level transformations only where they make demand and cleanup clearer; byte framing remains a byte-oriented trust boundary. A zero-count adapter must not pull upstream even once, because “produce no values” also implies “start no unnecessary effect.”

## Module 45 — Candidate files and publication

Whole-file helpers are appropriate only under an explicit size bound. Streaming file operations need a scope that owns the handle from acquisition through terminal cleanup. Write completion, userspace flush, kernel acceptance, file synchronization, pathname replacement, directory-entry persistence, and crash durability are different claims. The product must state the narrowest one it actually establishes.

A checkpoint system should first decide its recovery model. Replacing one checkpoint file provides a single latest candidate; immutable versioned checkpoints preserve history at the cost of retention and cleanup; a directory manifest introduces a second publication authority. In every case, stage beside the destination, create the stage exclusively, write and synchronize the candidate, close it, then perform the chosen publication step. Tests must examine visible artifacts after failure before writing, during writing, during sync, before rename, and after rename.

Directly writing the final pathname is falsified by injecting a transform failure after partial output and then reading the destination. FlowLedger’s transactional sink keeps the prior visible file unchanged until the candidate has passed the complete transformation protocol. It does not claim cross-process writer coordination, adversarial race resistance, or universal crash durability that the implementation does not prove.

## Module 46 — Framing before meaning

Framing and decoding must follow the format’s definition. NDJSON uses a byte delimiter, so FlowLedger searches for newline bytes while maintaining one bounded unfinished frame, then decodes the complete frame with a fatal UTF-8 decoder. This prevents replacement characters from laundering malformed input. Byte offsets, physical line numbers, JSON syntax, schema validation, and domain errors remain separate evidence.

For a length-prefixed JSON protocol, read exactly the fixed-width prefix, validate its endianness and length before allocation, enforce the payload limit, read exactly that many bytes, decode UTF-8 strictly, parse JSON, validate the runtime schema, and reject trailing or truncated states according to the protocol. An EOF during a prefix is not the same error as an EOF during a payload.

Splitting each decoded chunk on newline fails under two ordinary partitions: a multibyte character split across chunks and a line split across chunks. FlowLedger tests the same logical input under many chunk boundaries, rejects invalid UTF-8, and keeps line and byte context in typed diagnostics. A malformed event never reaches the candidate publication boundary.

## Module 47 — Representation-specific integrity

Compression and hashing are placed on representation edges, not added as generic “security” stages. Source bytes, decompressed NDJSON, canonical NDJSON, and compressed output are different byte sequences. A digest identifies exactly one of them. It can reveal accidental change when recomputed under the same rules, but an unauthenticated digest does not prove who created the data or protect against a malicious party able to replace both data and digest.

For a compressed backup verifier, store or compute separately named digests such as compressed-source and canonical-expanded content. Enforce the compressed input limit before or during reading and the expanded-byte limit immediately after decompression, before unbounded framing or allocation can occur. Corrupt gzip, empty input, tiny chunks, over-expansion, abort, and destination failure all need independent tests.

FlowLedger reports `sourceSha256`, `canonicalSha256`, and `outputSha256` only when those representations were actually completed. For an uncompressed canonical output the latter two should agree; for gzip output they should differ while each remains reproducible. Digest metadata is returned after candidate commit so a caller cannot mistake an abandoned stage for a published artifact.

## Module 48 — Child-process supervision

Use direct `spawn` when executable identity and argument boundaries must remain data, not shell syntax. `exec` is justified only when the shell is intentionally part of the contract. The supervisor owns stdin completion, stdout consumption, stderr drainage, spawn failure, exit or signal status, close, cancellation, and destination cleanup. Every retained output surface has an explicit byte limit.

For an image-conversion wrapper, allow or resolve executables through a stated policy, pass validated arguments as an array, use a controlled environment and working directory, stream input and output, retain only bounded stderr, cap output bytes, apply one deadline, and define acceptable exit statuses. The candidate file is staged and is replaced only after stdout completed, stderr was drained, the child closed acceptably, and the output pipeline succeeded.

Interpolation into `exec` is falsified with an argument containing shell metacharacters: data becomes syntax and behavior changes across shells. FlowLedger’s `through` command avoids that ambiguity. It also avoids a subtler defect: a child `exit` event is not complete stdio evidence. The operation waits for stdin, stdout, stderr, and child close, while preserving the earliest causal failure.

## Module 49 — Required branches and coordinated commit

Observation, optional telemetry, and required outputs have different authority. A required branch must participate in pressure and failure; a lossy observer may drop data under a documented policy. Fan-out needs one coordinator that admits the next item only when every required destination can accept it or has recovered capacity. Otherwise the fastest branch can cause unbounded retention for the slowest.

For `data.ndjson`, `rejects.ndjson`, and `manifest.json`, first decide whether the bundle is all-or-nothing, independently committed, or versioned through a manifest pointer. Ordinary filesystems do not provide one portable atomic rename covering three unrelated pathnames. A defensible design stages all candidates under a unique version directory, completes and synchronizes them, then publishes one small manifest or directory pointer whose semantics are documented. Failure-state tests inspect what remains visible after each branch fails.

`EventEmitter` is unsuitable for required side output because listener invocation is synchronous but asynchronous completion, pressure, and failure are not coordinated by the emitter. FlowLedger V1 therefore commits one main output and returns derived metadata after commit. Its conservation equations distinguish source bytes, expanded bytes, accepted events, rejected operations, canonical bytes, and final bytes rather than presenting one misleading total.

## Module 50 — Whole-system review and independent change

The final review should produce a single architecture map containing every representation, queue, accumulator, resource, owner, bound, cancellation edge, terminal observation, and publication transition. Correctness is then tested for invariance under legal chunking, slow destinations, scheduling differences, and injected failures. Claims such as “bounded,” “atomic,” “durable,” “validated,” and “zero-copy” must name the exact scope in which they are true.

A resumable-import checkpoint cannot simply store the latest raw byte offset. After decompression, framing, filtering, and canonicalization, several positions exist. The design must identify a replay-safe authority—for example, a source representation with stable seek semantics plus a hash of the preceding committed prefix, or an application-level event identifier. The checkpoint must be published with data under an explicit protocol; otherwise a newer checkpoint can point past an older visible output.

Happy-path tests cannot reveal chunk-boundary corruption, pressure failure, leaked handles, orphan children, abandoned stages, or ambiguous commit. FlowLedger’s final evidence therefore includes process-level CLI tests, fault injection, compatibility fixtures, strict limits, deterministic reports, and an independent multi-file rejects-bundle design. The extension is accepted only if it updates the representation graph, failure matrix, publication protocol, CLI, tests, and documentation together.

## Oral-defense standard

A strong defense traces one input byte all the way from source acquisition to final publication. At every edge it names the representation, current owner, possible aliases, queue or retained state, active limit, cancellation path, and remaining failures. It never calls a chunk a record, a digest authentication, a writable `finish` durable storage, child exit complete stdio, or several renames one transaction. It states the narrower fact and identifies the additional mechanism or evidence required for the stronger claim.
