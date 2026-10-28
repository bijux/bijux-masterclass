# Module 58 Solutions — HTTP/2 Sessions and Streams

## Prediction reasoning

A stream reset is normally local; other streams may continue. Peer protocol limits do not replace application capacity. GOAWAY communicates closure state but does not prove active streams have finished. Worst-case retained body memory includes the number of simultaneously admitted streams multiplied by each body bound, plus overhead. A committed job remains committed after response stream reset.

## Repair reasoning

Track sessions and streams separately. Each stream owner registers on creation and removes on terminal close. A session owner records all streams it owns.

Normalize pseudo-headers to a neutral finite request, then call the same application dispatcher. This prevents transport-specific semantics.

Per-stream body limits stop one stream. Application request admission bounds aggregate work. Neither alone implies the other.

Write responses through stream backpressure and observe close/error. A problem response for invalid input is stream-local. Destroy the whole session only for session-level failure or shutdown escalation.

During shutdown, stop new sessions, send GOAWAY, wait under one deadline, then destroy remaining sessions. Join stream owners and report terminal outcomes.

Tests should map responses by stream/request identity rather than expected completion order.

## Construction notes

Node's HTTP/2 API can operate through `'stream'` events. Validate `:method` and `:path` types. Reject connection-specific HTTP/1.1 headers when constructing HTTP/2 responses.

A client opens streams and consumes each response. Close the client session after all planned streams or on failure. A hanging session is a leaked handle.

The laboratory can set a low maximum concurrent streams to make rejection or queueing observable.

## Laboratory evidence

Use cases:

- concurrent fast and slow streams;
- one invalid stream returning a problem;
- client reset before commit;
- client reset after commit;
- over-limit body on one stream;
- session failure affecting all streams;
- GOAWAY with active streams;
- forced destroy after grace;
- deterministic association of responses;
- no divergent HTTP/1.1 versus HTTP/2 application result.

## ServiceWire transfer

The HTTP/2 adapter supports health, stats, submit, and get. It uses the same JSON serialization, problem mapping, idempotency store, revisions, and ETags. It does not implement SSE in the base product.

## Independent transfer

The client connects through TLS with `ALPNProtocols: ['h2']`, verifies the selected protocol, bounds open streams, and closes the session. A reset after an idempotency-keyed submit is reconciled through the same key.

## Defense summary

HTTP/2 adds concurrency inside one transport owner. Correct architecture preserves stream isolation while accounting for shared session capacity and failure. Multiplexing changes schedule, not application truth.

## Multiplexing solution

The health stream completes successfully, the slow stream completes later unless shutdown grace expires, and the oversized upload receives a stream-local 413. The session remains usable after the application rejection. Results are associated with their own stream promises, not with completion order.

During shutdown, the application quiesces first, the listener stops new acceptance, and sessions receive graceful close/GOAWAY behavior. Existing streams drain under one deadline. Leftovers are reset, sessions destroyed, and listener close observed. Awaiting listener close before signaling sessions can deadlock.

A third session is rejected by session admission. A fifth stream is constrained by session/stream policy. A valid stream with no job capacity receives an application 503. An oversized body receives a stream-local transport-adapter rejection. Four distinct authorities produce four distinct evidence paths.

## Failure-scope solution

Malformed JSON and job overload are application-stream responses. Oversized body is a stream-local adapter rejection. A peer reset is one stream terminal outcome. Invalid connection preface and session protocol errors are connection-wide. GOAWAY is a session lifecycle signal, not automatically an error. The classification follows the smallest authority whose invariant failed; destroying the session for every application error violates multiplexing isolation.
