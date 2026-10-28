# Course 6 Final Review — Reasoned Solutions

These are reasoning routes, not scripts to memorize.

## Part I

### 1. One budget across several address candidates

The promise applies to the whole operation. Compute one monotonic deadline before resolution or connection attempts. Before each candidate, calculate remaining time. The second candidate receives only the unused remainder. Two full one-second timers permit nearly two seconds plus resolution overhead, violating the public contract.

A more advanced client may overlap candidate attempts under a documented policy, but all attempts still share one deadline and all losing sockets must be destroyed and observed.

### 2. Complete frame followed by truncated frame

The first frame is valid and may be delivered because its prefix and payload completed before EOF. The second frame is a protocol error because EOF occurred after partial framing state existed. The connection reaches a failed terminal state. Silently discarding the partial frame converts truncation into success and makes corruption invisible.

### 3. Duplicate UDP responses

The first correctly correlated response received while the operation is pending may complete it. Later duplicates are ignored or counted according to policy. Correlation must include request ID and expected peer policy; merely receiving a syntactically valid datagram is insufficient. The second response is not a second application success.

### 4. Trust versus hostname identity

The chain-trust check succeeded: the certificate was issued by a configured trust anchor. Hostname verification failed: the authenticated certificate does not identify the logical service name. Encryption may also be established, but the channel is not acceptable for that requested identity. Disabling verification deletes the identity requirement rather than repairing the certificate.

### 5. Stream reset versus session failure

HTTP/2 multiplexes independent streams over one session. A stream reset terminates that stream. Other streams may remain valid unless the reset results from a connection-level protocol error or the session itself fails. Destroying the session on every stream-local failure creates unnecessary cross-request failure.

## Part II

### 6. Four classifications

Safe describes intended state-changing semantics. Idempotent describes the intended effect of repetition. Cacheable concerns response reuse under protocol metadata. Retriable is an end-to-end product decision based on failure phase, method semantics, idempotency evidence, time budget, and server contract.

A GET is usually safe and idempotent but may be non-cacheable due to response headers. An idempotency-keyed POST is not safe and is not inherently idempotent at the HTTP method level, yet the application may make retries safe for that semantic request.

### 7. Timed-out idempotency-keyed POST

The client knows that it did not receive a complete response within the deadline. It does not know whether the server committed. It should not create a new semantic operation with a new key. A later reconciliation request uses the same key or a returned operation identifier under the documented protocol. Another attempt is permitted only if the retry policy, remaining budget, and server's idempotency contract allow it.

### 8. Failure ownership

- unsupported media type: HTTP application boundary, commonly 415;
- missing required body: application request contract, often 400;
- malformed JSON: syntax validation, 400;
- valid JSON with invalid domain field: runtime/domain validation, usually 422 or a documented 400 policy.

The exact status choice must be stable. The important rule is to preserve which trust transition failed.

### 9. Conditional GET after revision change

Because the current representation has a different ETag, the condition does not match. Return the current representation with status 200 and ETag `"job-2-rev-5"`. A 304 would falsely claim the client's cached representation is current.

### 10. Redirect policy

A redirect can move the operation to another origin, change method semantics according to status and client policy, expose credentials, consume deadline, create loops, and change TLS identity. Following it mechanically treats a new request as if it were the same transport step. Each redirect must be validated against the supported policy.

## Part III

### 11. Capacity map

A complete answer names at least connections, finite requests, request-body bytes, queued jobs, active jobs, retained job records, idempotency records, event-journal entries, subscribers, queued bytes per subscriber, HTTP/2 sessions, and HTTP/2 streams. Each needs a unit and enforcement authority. “Memory limit” is not precise enough.

### 12. Idempotency capacity exhausted

The application admission authority rejects before semantic commit, commonly with a 503 or 429 policy plus bounded retry guidance. Liveness health may remain healthy because the process and event loop work. Readiness should be false or degraded if the service cannot accept its promised class of submissions.

### 13. Slow SSE subscriber

The journal bounds retained history, not bytes waiting for one subscriber's socket. If writes continue while the client does not read, queued output can grow in stream buffers or an application queue. Enforce per-subscriber queued bytes or events; remove the subscriber when the bound is exceeded.

### 14. Phased shutdown

Quiesce both listeners and readiness first. Reject or stop new requests. Signal application cancellation where policy permits. Drain the arriving body only if it was already admitted and the protocol policy allows completion; otherwise terminate it cleanly. Let active jobs and HTTP/2 streams finish under one grace deadline. Send SSE shutdown information if supported, end streams, close idle sessions, then abort remaining sockets and streams. Join every tracked task and timer before reporting termination.

### 15. Live versus authoritative counters

Live metrics can race with work in transition and can be read before final cleanup. After all owned work joins, reconstruct or read authoritative terminal state. A live counter remains useful for observation but is not proof that every accepted operation terminated exactly once.

## Part IV

### 16. Discovery and authorization

UDP discovery is generally unauthenticated and can be spoofed or observed. It identifies a responding endpoint under a local convenience protocol. Authorization must still occur through the service's authenticated application boundary.

### 17. Certificate choices

A dedicated local CA lets tests configure an explicit trust anchor and issue a leaf certificate with realistic hostname identity. A self-signed leaf can be trusted directly but combines trust anchor and endpoint identity in one object. Disabling verification accepts any presented certificate and eliminates the property under test.

### 18. Peer-controlled bounds

Examples include request body bytes, header count and size, path length, JSON nesting or fields, response bytes, frame length, SSE subscriber queue, UDP datagram size, idempotency-key length, and retained error excerpts. Five well-defined independent limits satisfy the question; one global limit does not.

### 19. Causal but bounded errors

Use stable code, status, short bounded detail, request ID, and an internal `cause` chain for logs. Redact authorization and cookies. Do not return stack traces. Truncate or classify peer input rather than echoing an entire body, header, or path.

### 20. Request ID versus idempotency key

A request ID identifies one transport/application attempt for tracing. An idempotency key identifies one semantic operation across retries. Several request IDs may legitimately refer to attempts for the same idempotency key. Reusing request IDs as semantic identity conflates observation with commit authority.

## Part V — Thumbnail service

A defensible design has separate handlers for submission, status, events, and health. The job state machine includes accepted, active, succeeded, failed, and possibly cancelled. The idempotency machine includes in-progress and terminal records keyed by the client key plus a semantic request fingerprint.

Capacity must separately bound request bodies, connections, accepted jobs, active work, retained results, idempotency records, event history, subscriber count, and subscriber queue. One monotonic deadline spans client connection, headers, body, and retry. TLS uses a configured trust anchor and hostname verification. SSE replay either returns all events after the known ID or reports a replay gap; slow subscribers are removed at a declared queue bound.

Startup constructs dependencies in order and rolls them back in reverse order after failure. Shutdown quiesces listeners, marks readiness false, drains accepted jobs and streams under one grace deadline, aborts leftovers, joins all owners, and reports terminal state.

Useful tests include oversized body, same-key conflict, retry after ambiguous response, stale ETag, SSE replay, replay gap, slow subscriber, wrong TLS hostname, graceful drain, forced abort, HTTP/2 stream reset, and startup failure rollback.

Durable idempotency across restarts, persistent jobs, cross-process event history, and coordinated multi-instance admission require Course 7 storage and distributed-workflow mechanisms.
## Part VI — Causal incident diagnosis

### 21. Intermittent reset with green health

`ECONNRESET` says that a connection was reset; it does not identify which side initiated the reset or why. Correlate request IDs with accept, body, response-commit, socket-error, timeout, and shutdown events. Check whether the request was admitted, whether the application committed, whether a response began, and whether the reset coincides with idle policy, overload, proxy behavior, or shutdown. The repair belongs at the authority whose contract is violated, not at the first API that surfaced the symptom.

### 22. Duplicate jobs after a lost response

The missing contract is semantic idempotency. A timeout makes commit ambiguous: the server may have committed before the response was lost. The client must use a stable idempotency key across retries, and the server must bind that key to a semantic request fingerprint and terminal submission result. A longer timeout changes probability but does not remove ambiguity.

### 23. Slow SSE consumer

Bounded event history does not bound bytes already selected for one subscriber but not yet written. The per-subscriber pending queue or socket write backlog is the second retained structure. Enforce a byte or event limit, remove the slow subscriber under explicit policy, and release its heartbeat, listeners, and queued data.

### 24. HTTP/2 concurrency with low CPU

Possible causes include exhausted connection-level flow-control credit, stream-level windows too small for the workload, and application admission that keeps many streams open while only a few can make progress. Also inspect client read behavior and peer-advertised concurrent-stream limits. Test one variable at a time; adding more sessions can hide rather than explain a stream or window protocol error.

### 25. Trusted CA but wrong service name

Trusting the CA proves that the certificate chains to an accepted issuer. Hostname verification separately checks whether the leaf certificate's subject alternative names cover `service.local`. Issue a certificate with that DNS name, or connect using a name the certificate already covers. Disabling verification destroys the identity property being tested.

### 26. Fast shutdown with truncated response

The process may close sockets and exit cleanly while a product response remains only partially transmitted. Quiesce admission, allow accepted finite responses to complete during drain, then abort only after the grace deadline. Track response completion and connection ownership; a clean process exit is not evidence that every accepted request received a valid terminal protocol message.

### 27. Stale UDP response

The request needs a correlation identifier that is unpredictable or at least unique within the client's retained window, and the response must echo it. The client must ignore responses for expired attempts and define endpoint filtering and freshness policy. UDP preserves datagrams, not request/response sessions.

### 28. Redirect method policy

Redirect codes carry different method and body semantics. A reusable body may be required for replay, credentials may need stripping across origins, and an idempotency key may need preservation. The client must implement a bounded redirect state machine for the supported codes; a generic switch hides security, replayability, and semantic-change decisions.

### 29. Readiness under job-capacity exhaustion

This is policy-dependent. A service may remain ready if capacity exhaustion is brief and overload responses are part of normal operation, or become not-ready if the instance cannot accept its advertised workload. The readiness contract must name which resources and thresholds it represents. Liveness should not be used as an overload signal.

### 30. Partial startup failure

The startup owner must close the already-listening HTTP server, stop accepting connections, terminate accepted sockets, close agents, discovery endpoints, HTTP/2 sessions, subscribers, and timers created before failure, and await their terminal observations. Only after reverse-order rollback completes may startup report failure. Otherwise the command can exit while a partially published service remains reachable.

### Oral defense standard

A strong defense identifies one application authority for jobs and idempotency, transport-specific owners for listeners, sockets, sessions, and streams, a bounded event authority, a supported-client authority, and one runtime owner for startup and shutdown. It distinguishes transport completion from semantic commit, names every queue and limit, and traces an accepted request through validation, commit, execution, representation, response completion, event publication, and terminal reconciliation.
