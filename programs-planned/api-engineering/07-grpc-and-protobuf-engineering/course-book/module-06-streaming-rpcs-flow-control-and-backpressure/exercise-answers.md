# Worked answers — Streaming RPCs, Flow Control, and Backpressure

These are reference answers, not scripts to memorize. Compare the decision rule and evidence, then revise your answer.

## 1. Choose the RPC shape for GetRun, WatchRun, UploadDataset, and Work.

GetRun is unary; WatchRun is server-streaming; UploadDataset is client-streaming; Work is bidirectional. Each matches who sends a sequence and whether both sides communicate independently.

**Decisive evidence:** RPC shape decision table

## 2. Why does HTTP/2 flow control not prove bounded application memory?

The runtime can bound network windows while user code drains into an unbounded queue or creates unbounded tasks. Application buffers and work concurrency still need limits.

**Decisive evidence:** queue high-water test

## 3. Define the legal frame order for UploadDataset.

Exactly one metadata frame comes first, followed by zero or more data chunks, then normal client completion. Data-before-metadata and repeated metadata are invalid.

**Decisive evidence:** upload state-machine vector

## 4. What must happen to a staging file after checksum failure?

Close and remove it, record a safe integrity failure, and avoid publishing metadata or content. Cleanup must also occur on cancellation and write failure.

**Decisive evidence:** staging cleanup test

## 5. Why must a download client verify completion even after receiving many chunks?

A stream can terminate with an error after partial bytes. The client must validate declared length/range and digest before atomically exposing the result.

**Decisive evidence:** partial-download integrity test

## 6. Differentiate WatchRun sequence from the public event sequence.

WatchRun sequence is scoped to an operational observation stream with bounded retention. The event sequence belongs to durable integration history and independent consumers.

**Decisive evidence:** sequence scope policy

## 7. How should a client recover when its WatchRun resume position is outside retention?

Perform authoritative GetRun, accept the declared gap, reset local snapshot, and resume from the current supported sequence rather than inventing missing transitions.

**Decisive evidence:** resume-gap vector

## 8. Why is an authenticated worker stream insufficient authority to complete an assignment?

The lease generation in durable state is authoritative. The connection may outlive a lease, reconnect, or coexist with a newer attempt.

**Decisive evidence:** stale-generation test

## 9. What ordering guarantee exists within one gRPC stream, and what can application concurrency break?

Messages are delivered in send order per direction, but concurrently spawned handlers can commit effects out of order. Protocol state must remain serial.

**Decisive evidence:** adversarial schedule trace

## 10. Name four independent budgets required for a long-lived stream.

Per-message bytes, total stream bytes/frames, idle or total duration, concurrent streams, and queued bytes are all relevant; at least four must be explicit.

**Decisive evidence:** stream budget table

## 11. How should a server react to a slow consumer?

Stop pulling or await writer readiness, bound queued output, and eventually cancel/reject under policy. Never continue buffering invisibly.

**Decisive evidence:** slow-peer test

## 12. Define the proof that backpressure is end-to-end rather than a local queue trick.

Drive offered load through every stage and show bounded queue high-water marks, controlled admission/rejection, stable memory, no lost durable work, and recovery after pressure falls.

**Decisive evidence:** end-to-end pressure report
