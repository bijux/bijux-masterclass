# Worked Answers — Module 06: Streaming RPCs, Flow Control, and Backpressure

Use these solutions to audit your reasoning for **Streaming RPCs, Flow Control, and Backpressure**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Choose the RPC shape for GetRun, WatchRun, UploadDataset, and Work.

GetRun is unary; WatchRun is server-streaming; UploadDataset is client-streaming; Work is bidirectional. Each matches who sends a sequence and whether both sides communicate independently.

**Decisive evidence:** RPC shape decision table

The chapter’s decisive distinction is this: Unary is appropriate when one bounded request yields one bounded response. Server streaming fits a bounded request followed by an ordered sequence, such as watching run snapshots or downloading chunks. Client streaming fits a sequence of frames that produce one authoritative result, such as a metadata-first upload. Bidirectional streaming fits a session in which both sides send independently, such as a controlled worker channel.

## 2. Why does HTTP/2 flow control not prove bounded application memory?

The runtime can bound network windows while user code drains into an unbounded queue or creates unbounded tasks. Application buffers and work concurrency still need limits.

**Decisive evidence:** queue high-water test

In the cumulative capstone, the rule becomes concrete: gRPC uses HTTP/2 flow control so a sender cannot write infinite bytes directly into a receiver's network window. But application code can still read as fast as the library delivers and append messages to an unbounded queue. It can also produce results faster than a writer awaits readiness. Every queue between source and sink needs a capacity, ownership, overflow behavior, and metric.

## 3. Define the legal frame order for UploadDataset.

Exactly one metadata frame comes first, followed by zero or more data chunks, then normal client completion. Data-before-metadata and repeated metadata are invalid.

**Decisive evidence:** upload state-machine vector

A useful way to reason about the boundary is: The first UploadDatasetRequest frame must contain UploadMetadata; subsequent frames contain bytes. Metadata declares parent, request identifier, filename, media type, expected digest, and optional expected size. The server validates authorization and admission before accepting content. A second metadata frame, a data frame before metadata, or a missing content sequence is invalid.

## 4. What must happen to a staging file after checksum failure?

Close and remove it, record a safe integrity failure, and avoid publishing metadata or content. Cleanup must also occur on cancellation and write failure.

**Decisive evidence:** staging cleanup test

The implementation consequence is: Write bytes to a confined staging file while incrementally hashing and counting them. Do not hold the full upload in memory. On completion, compare expected size and digest, fsync as required by the storage profile, and atomically publish. If cancellation, limit violation, checksum mismatch, or write failure occurs, remove the stage and never expose a partial artifact.

## 5. Why must a download client verify completion even after receiving many chunks?

A stream can terminate with an error after partial bytes. The client must validate declared length/range and digest before atomically exposing the result.

**Decisive evidence:** partial-download integrity test

The important nuance is: Now examine a download. The server authorizes the artifact before the first byte, reads fixed-size chunks, and awaits each write. If storage fails after several chunks, the stream finishes with a non-OK status. The client does not publish the partial file merely because it received data; it validates completion, selected size/range, and digest, then renames its own stage atomically.

## 6. Differentiate WatchRun sequence from the public event sequence.

WatchRun sequence is scoped to an operational observation stream with bounded retention. The event sequence belongs to durable integration history and independent consumers.

**Decisive evidence:** sequence scope policy

Under concurrency or failure, the distinction becomes: WatchRunRequest includes a run name and resume after sequence. Analysis Control emits monotonically increasing observation sequence numbers for one run. On reconnect, the client asks for values after the last fully processed sequence. The server may serve a bounded retained observation history or reconstruct current state and declare a gap; the policy states which.

## 7. How should a client recover when its WatchRun resume position is outside retention?

Perform authoritative GetRun, accept the declared gap, reset local snapshot, and resume from the current supported sequence rather than inventing missing transitions.

**Decisive evidence:** resume-gap vector

The design remains honest only if: This stream is not the Course 6 event log. Sequence numbers are scoped to the run observation service, retention is shorter, and the payload is an authoritative snapshot plus transition type. If the requested sequence is too old, the server returns a structured out-of-range or failed-precondition outcome instructing the client to perform GetRun and resume from current state.

## 8. Why is an authenticated worker stream insufficient authority to complete an assignment?

The lease generation in durable state is authoritative. The connection may outlive a lease, reconnect, or coexist with a newer attempt.

**Decisive evidence:** stale-generation test

The consumer-facing consequence is: The database lease and generation remain authoritative. On reconnect, a worker re-identifies and receives current assignments according to policy. A late result from a stale generation is rejected even if it arrives on a healthy authenticated stream. A disconnected worker may still be running; lease expiry and fencing prevent two attempts from publishing conflicting effects.

## 9. What ordering guarantee exists within one gRPC stream, and what can application concurrency break?

Messages are delivered in send order per direction, but concurrently spawned handlers can commit effects out of order. Protocol state must remain serial.

**Decisive evidence:** adversarial schedule trace

The operational consequence is: gRPC preserves message order within one direction of one stream as observed by the API, but application processing can reorder effects when messages are handled concurrently. Partition protocol state by stream and use a serial state machine for control frames. Expensive work can run concurrently under bounded permits, but completion messages re-enter an ordered validation boundary.

## 10. Name four independent budgets required for a long-lived stream.

Per-message bytes, total stream bytes/frames, idle or total duration, concurrent streams, and queued bytes are all relevant; at least four must be explicit.

**Decisive evidence:** stream budget table

The strongest engineering interpretation is: A per-message maximum does not bound a stream. A client can send many legal chunks forever. Define maximum total bytes, maximum frames, maximum metadata size, idle timeout, overall duration where appropriate, and per-tenant concurrent-stream budget. Streaming is not permission to avoid admission control.

## 11. How should a server react to a slow consumer?

Stop pulling or await writer readiness, bound queued output, and eventually cancel/reject under policy. Never continue buffering invisibly.

**Decisive evidence:** slow-peer test

The defect-oriented view is: Use pull or awaitable write APIs correctly. Do not spawn one task per message without a concurrency bound. Bound decoded message size before expensive processing. Bound stream count, per-stream queued bytes, total queued bytes, and time spent blocked. When pressure exceeds policy, slow the source, reject admission, or terminate with a stable resource-exhausted outcome.

## 12. Define the proof that backpressure is end-to-end rather than a local queue trick.

Drive offered load through every stage and show bounded queue high-water marks, controlled admission/rejection, stable memory, no lost durable work, and recovery after pressure falls.

**Decisive evidence:** end-to-end pressure report

Across the Python and TypeScript tracks, the invariant is: A bounded stream can still move overload downstream. An API accepts uploads, storage writes quickly, database metadata commits, and workers cannot process the new datasets. The course traces demand through admission, stream queues, storage, database, worker capacity, and event publication. Each stage exposes backlog and rejection behavior.
