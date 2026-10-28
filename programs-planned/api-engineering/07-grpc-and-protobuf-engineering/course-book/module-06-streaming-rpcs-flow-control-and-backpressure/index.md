# Streaming RPCs, Flow Control, and Backpressure

**Module 06 of 10**

> **Governing question:** How do we design long-lived and bulk-transfer RPCs so that slow peers, reconnects, oversized messages, and stale attempts cannot exhaust memory or corrupt state?

## Place in the program

Unary calls established outcome, time, and retry semantics. Streaming adds a protocol that unfolds over many messages and often outlives one request path. The learner must now govern framing, sequence, resumption, flow control, cancellation, memory, and durable authority. HTTP/2 provides transport flow control, but the application still owns every queue and semantic limit.

## Learning outcomes

- choose unary, server-streaming, client-streaming, or bidirectional RPC from interaction semantics
- design protocol frames and state machines rather than treating a stream as an unbounded message list
- combine HTTP/2 flow control with bounded application queues and backpressure
- implement resumable ordered observation without claiming a durable event log
- stream large uploads and downloads with exact size, checksum, and cancellation guarantees
- keep durable worker leases authoritative when bidirectional sessions disconnect or reconnect

## Capstone result

Implement `WatchRun`, `UploadDataset`, `DownloadArtifact`, and the worker `Work` stream with shared schedule vectors, bounded buffers, resumable observation, and stale-attempt fencing.

## Choose the streaming shape from the protocol

Unary is appropriate when one bounded request yields one bounded response. Server streaming fits a bounded request followed by an ordered sequence, such as watching run snapshots or downloading chunks. Client streaming fits a sequence of frames that produce one authoritative result, such as a metadata-first upload. Bidirectional streaming fits a session in which both sides send independently, such as a controlled worker channel. Selecting bidirectional streaming merely because it is powerful makes lifecycle, ordering, and testing harder.

Write the protocol state machine before the `.proto`. Define which side speaks first, permitted frame order, terminal conditions, resumption, duplicate behavior, and what durable state exists outside the stream. Generated APIs enforce message types, not legal conversation order.

A stream is not automatically a durable event feed. `WatchRun` is an operational observation of authoritative run state. The AsyncAPI event log remains the replayable integration contract. Keeping these roles separate prevents internal transport frames from acquiring accidental public retention promises.

## HTTP/2 flow control is necessary but insufficient

gRPC uses HTTP/2 flow control so a sender cannot write infinite bytes directly into a receiver's network window. But application code can still read as fast as the library delivers and append messages to an unbounded queue. It can also produce results faster than a writer awaits readiness. Every queue between source and sink needs a capacity, ownership, overflow behavior, and metric.

Use pull or awaitable write APIs correctly. Do not spawn one task per message without a concurrency bound. Bound decoded message size before expensive processing. Bound stream count, per-stream queued bytes, total queued bytes, and time spent blocked. When pressure exceeds policy, slow the source, reject admission, or terminate with a stable resource-exhausted outcome.

Measure application backlog separately from transport windows. A healthy TCP/HTTP2 connection can coexist with an overloaded consumer.

## Message-size and stream-lifetime budgets

A per-message maximum does not bound a stream. A client can send many legal chunks forever. Define maximum total bytes, maximum frames, maximum metadata size, idle timeout, overall duration where appropriate, and per-tenant concurrent-stream budget. Streaming is not permission to avoid admission control.

Unary default message limits may be too small for bulk data and too large for control messages. Configure method-specific limits. `UploadDataset` uses bounded chunks and a declared total/checksum. `DownloadArtifact` uses bounded chunks and optional offset/limit. Worker control frames remain small. Reject compressed-message bombs based on decompressed size and work, not only wire bytes.

The error contract distinguishes invalid framing, exceeded resource policy, deadline, cancellation, and integrity failure.

## Metadata-first upload protocol

The first `UploadDatasetRequest` frame must contain `UploadMetadata`; subsequent frames contain bytes. Metadata declares parent, request identifier, filename, media type, expected digest, and optional expected size. The server validates authorization and admission before accepting content. A second metadata frame, a data frame before metadata, or a missing content sequence is invalid.

Write bytes to a confined staging file while incrementally hashing and counting them. Do not hold the full upload in memory. On completion, compare expected size and digest, fsync as required by the storage profile, and atomically publish. If cancellation, limit violation, checksum mismatch, or write failure occurs, remove the stage and never expose a partial artifact.

Idempotent upload replay needs a bound request identity and content digest. A repeated identical upload can return the existing dataset; changed bytes under the same identity fail.

## Bounded artifact download

`DownloadArtifact` is server streaming because the caller provides one artifact name and optional range, and the server yields ordered chunks. Authorization and existence concealment occur before the first byte. The response metadata or first chunk communicates digest and selected range according to the profile.

Read bounded chunks from the artifact adapter and await each send. Do not pre-read the whole file or queue the entire range. Observe cancellation and close the file promptly. If a storage error occurs after some bytes were delivered, the final status marks the stream incomplete; the client must verify total length and digest before publication.

For public clients, HTTP range semantics remain available. The internal RPC stream is not automatically a better public download interface.

## Resumable WatchRun semantics

`WatchRunRequest` includes a run name and `resume_after_sequence`. Analysis Control emits monotonically increasing observation sequence numbers for one run. On reconnect, the client asks for values after the last fully processed sequence. The server may serve a bounded retained observation history or reconstruct current state and declare a gap; the policy states which.

This stream is not the Course 6 event log. Sequence numbers are scoped to the run observation service, retention is shorter, and the payload is an authoritative snapshot plus transition type. If the requested sequence is too old, the server returns a structured out-of-range or failed-precondition outcome instructing the client to perform `GetRun` and resume from current state.

Clients deduplicate sequence numbers and apply snapshots idempotently. Reconnection uses deadline and backoff policy, not a tight loop.

## Worker bidirectional sessions

A worker opens `Work`, sends `WorkerHello`, then readiness frames. Analysis Control sends assignments carrying assignment identity, run name, lease generation, and lease expiry. The worker sends progress and result frames. Heartbeat or readiness timing keeps the session useful, but the stream connection is not the authority to complete work.

The database lease and generation remain authoritative. On reconnect, a worker re-identifies and receives current assignments according to policy. A late result from a stale generation is rejected even if it arrives on a healthy authenticated stream. A disconnected worker may still be running; lease expiry and fencing prevent two attempts from publishing conflicting effects.

Bound in-flight assignments per worker and per tenant. Do not let a fast control plane overwhelm a worker because the socket accepts writes.

## Ordering and concurrency

gRPC preserves message order within one direction of one stream as observed by the API, but application processing can reorder effects when messages are handled concurrently. Partition protocol state by stream and use a serial state machine for control frames. Expensive work can run concurrently under bounded permits, but completion messages re-enter an ordered validation boundary.

Across streams there is no global order. Across reconnects, use explicit sequence and attempt identities. Server instances may observe different sessions. Durable state decides order where business correctness requires it.

Tests generate adversarial schedules: progress before hello, duplicate hello, completion before assignment, slow reader, fast writer, cancellation during staging, reconnect after lease change, and repeated sequence delivery.

## Backpressure is an end-to-end property

A bounded stream can still move overload downstream. An API accepts uploads, storage writes quickly, database metadata commits, and workers cannot process the new datasets. The course traces demand through admission, stream queues, storage, database, worker capacity, and event publication. Each stage exposes backlog and rejection behavior.

Backpressure may reduce read rate, withhold assignments, stop requesting messages, reject a new stream, or return resource exhaustion. It should not silently drop control messages or accept work that cannot be durably owned. Course 5 traffic budgets and Course 4 reliability signals remain active.

The stream proof records queue high-water marks, blocked durations, dropped/ rejected counts, memory bounds, and durable state. Throughput without these bounds is not success.

## Worked protocol review: a two-gigabyte upload

A client wants to upload a two-gigabyte dataset. Increasing the unary message limit to two gigabytes would make retries expensive, force large allocations, and obscure partial-transfer cleanup. Client streaming is appropriate, but the stream still needs a protocol. The first frame declares parent, request identity, filename, media type, expected size, and digest. Only after authenticating the caller, authorizing the project, and reserving upload capacity does the server accept chunks.

The server writes each bounded chunk into a confined staging object while updating size and digest. It never joins the entire body in memory. The educational in-memory reference uses a small limit so the invariant is testable; the production adapter uses streaming storage. A second metadata frame fails. A data frame before metadata fails. An oversized chunk fails before expensive processing. Exceeding total bytes stops reads, closes the stage, and returns resource exhaustion.

HTTP/2 flow control can pause network delivery, but it cannot stop application code from reading every frame into an array. The proof therefore observes both transport behavior and application queue high-water marks. The queue has a fixed capacity. Writers await capacity or the server terminates under policy. “No process crash” is not evidence of boundedness.

Cancellation halfway through the transfer closes and removes the stage. A matching retry uses the same request identifier and digest. If the previous upload completed, it returns the existing dataset. If the identifier is bound to different bytes, it fails. The server never publishes an object before checksum and atomic-finalization succeed.

Now examine a download. The server authorizes the artifact before the first byte, reads fixed-size chunks, and awaits each write. If storage fails after several chunks, the stream finishes with a non-OK status. The client does not publish the partial file merely because it received data; it validates completion, selected size/range, and digest, then renames its own stage atomically.

The same reasoning governs `WatchRun` and worker streams. A Watch client resumes after the last processed sequence and deduplicates repeats. A stale resume position triggers an authoritative snapshot reset, not invented history. A worker’s connection can be healthy while its lease is stale; completion still fails. Across all four streams, the contract names frame order, durable authority, queue bounds, byte bounds, time bounds, cancellation cleanup, and resumption. That is the difference between “using streaming” and engineering a streaming protocol.

## Implementation reading

Read the streaming methods in `analysis.proto`, `capstone/rpc-case/streaming-policy.yaml`, and vectors `streaming.json` and `flow-control.json`. Compare Python generators/iterators with TypeScript async-iterable state machines. The live Python reference covers network streaming; dependency-light tests prove both language protocols.

## Failure checklist

- Is the chosen unary or streaming shape justified by interaction semantics?
- Can any queue, stream, message, total byte count, or lifetime grow without a bound?
- Does the upload protocol publish partial or unverified content?
- Can a reconnect duplicate observations or lose the authoritative current state?
- Can a live stream let a stale worker bypass lease fencing?
- Does backpressure stop at one layer while overload accumulates downstream?

## Transition

After preserving the checkpoint evidence, continue to **Identity, Authorization, mTLS, and Tenant Isolation**. Do not progress while the non-compensable gate remains unresolved.
