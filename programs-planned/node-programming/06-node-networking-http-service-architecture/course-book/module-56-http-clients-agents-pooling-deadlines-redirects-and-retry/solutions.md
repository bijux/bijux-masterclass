# Module 56 Solutions — HTTP Client Ownership

## Prediction reasoning

Agent queue time consumes the caller's end-to-end deadline. A timeout after body write cannot prove rollback. Error responses remain hostile inputs and require body bounds. HTTPS-to-HTTP downgrade should normally be rejected by a service client. A one-shot async iterable is not replayable unless the client has an independent stable source from which to create a new iterable.

## Repair reasoning

Create the deadline before the first attempt. Pass remaining time to connection, response, body, redirect, and delay phases. A new attempt begins only when policy and remaining time allow it.

Every response must be fully consumed within a bound or destroyed. This applies to redirect and error responses too.

Retry the same semantic operation with the same idempotency key and exact validated body. Changing the key converts reconciliation into a new operation.

Classify bodies. A `Buffer` can be replayed. A stream from a live sensor cannot. A file range can be replayed if the file identity and range remain stable and are reopened each attempt.

Redirect policy should reject loops, downgrade, disallowed origin changes, and credential forwarding. A simple service client may reject every redirect.

The client owns its agent and should expose `close()`. Tests should verify no active handles remain after close.

## Construction notes

Response reading should count each chunk before storing it. On limit violation, destroy the response and reject with a structured error. Parse media type before JSON. Validate parsed data.

Attempt history should contain bounded operational facts, not secrets. Include attempt number, target origin, status, duration, and stable error code.

For ambiguous commit tests, the server can commit and then destroy the socket before sending headers. A correct idempotency-keyed retry returns the existing job.

## Laboratory evidence

Strong tests include:

- delayed response headers exhausting deadline;
- oversized success body;
- oversized error body;
- redirect loop;
- cross-origin redirect with authorization header;
- network reset before request write;
- network reset after server commit;
- 503 with bounded retry;
- non-replayable body rejection;
- client close with idle pooled sockets.

## ServiceWire transfer

The CLI creates one client, performs operations, and closes it in `finally`. The client exposes typed results rather than raw `IncomingMessage`. It may surface a reconciliation-required failure when policy cannot decide safely.

## Independent transfer

A file-range uploader records stable file identity, offset, and length. Each attempt reopens and reads the same range under the one deadline. Server-side idempotency or upload-session identity is required to reconcile ambiguous partial commit. Cross-origin redirects and method-changing redirects are rejected.

## Defense summary

A client operation is a resource and semantic owner, not a convenience promise. Correctness depends on agent lifecycle, one time budget, bounded bodies, exact retry identity, and an explicit response-validation boundary.

## Retry-ledger solution

After attempt one, 480 ms remain. After backoff, 450 ms. Attempt two leaves 290 ms; the second backoff leaves 230 ms. Attempt three receives only 230 ms. Headers arrive with 50 ms remaining, but the body needs 100 ms, so the operation deadline expires before a complete response. The client must destroy or abort the request and report deadline, not extend the budget because headers arrived.

After a successful keep-alive request, the agent may retain an idle socket and internal scheduling state. `close()` destroys both HTTP and HTTPS agents. Double close is idempotent; request after close fails before allocating transport resources. Oversize and deadline errors must win over secondary destroy-induced socket errors. Late events are observed but cannot settle twice.

## Redirect-matrix solution

Same-origin HTTPS may be followed under a bounded redirect count with method and replayability rules preserved. A new port changes origin and therefore needs explicit policy. HTTPS-to-HTTP is rejected because it downgrades transport. Another origin is rejected unless credentials, idempotency authority, and body transfer are independently authorized. Authorization and idempotency headers never move merely because a `Location` header exists.
