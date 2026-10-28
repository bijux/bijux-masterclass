# Laboratory 4 — Strict HTTP Message Server

**Module 54**

## Product

Build a finite JSON HTTP server with GET/HEAD parity, POST validation, 405 handling, strict media type, bounded request bodies, stable problem details, and active request/connection accounting. The domain operation is intentionally trivial so HTTP evidence remains visible.

## Governing question

> How can a low-level Node HTTP server enforce method, representation, body, response, and connection contracts before domain code runs?

## Public surface

- `readBoundedBody(request, limit)` counts observed bytes.
- `parseJsonBody` distinguishes media and syntax failures.
- `startStrictServer(options)` returns bound URL and close handle.
- Responses use a stable problem representation.

## Required invariants

- Observed body bytes never exceed the configured retained limit.
- `HEAD` returns GET metadata without body bytes.
- Known path and unsupported method produce declared behavior.
- No domain call occurs after body/media/schema failure.
- Response errors contain no stack or unbounded peer text.
- Shutdown observes requests and sockets separately.

The laboratory is complete only when the tests distinguish these invariants from a smaller implementation that happens to pass the normal path.

## Implementation sequence

1. Implement health GET and HEAD.
2. Add method table and Allow header.
3. Implement bounded body reading.
4. Add strict JSON and exact object validation.
5. Render bounded problems.
6. Track active requests and sockets.
7. Test quiesce and early client close.

Keep the sequence causal. A later feature should not hide an earlier failure. For example, do not add retry before a single attempt has one clear terminal owner, and do not add shutdown before the normal resource lifecycle is observable.

## Adversarial cases

- unsupported method
- unsupported or missing media type
- declared length above bound
- chunked body above bound
- malformed JSON
- valid JSON primitive
- client closes mid-body
- server closes mid-response
- keep-alive request during quiesce

For each case, write the predicted state transition and the exact terminal evidence before running the test. Prefer injected clocks, deterministic fake peers, explicit counters, and local ephemeral ports to arbitrary sleeps.

## Prohibited shortcuts

- using `Content-Length` as sole limit
- collecting whole body then checking
- treating JSON cast as validation
- sending body for HEAD
- returning stack traces
- using listener close as complete shutdown

A shortcut is prohibited because it removes the mechanism under study. It is not a style preference.

## Completion evidence

1. method/status matrix
2. body-bound test without Content-Length
3. HEAD byte assertion
4. no-domain-call assertion
5. connection/request terminal reconciliation

Also include a small ownership table naming every socket, timer, listener, queue, request, response, or subscription created by the product and its cleanup transition.

## Independent transfer

Design a bounded binary upload route. Separate transport receipt, checksum verification, candidate completion, and publication.

The transfer is not complete when only type names change. Reconstruct the protocol, state, capacity, time, and terminal ledgers for the new domain.

## Using the starter

The starter compiles and exposes the domain vocabulary, configuration validation, and one baseline test. It does not implement the difficult mechanism. Extend it without weakening strict TypeScript settings.

Run:

```bash
npm run typecheck
npm test
```

## Comparing with the reference

Open `reference/` only after your normal and adversarial tests pass. Compare:

1. state representation;
2. bound enforcement point;
3. cleanup ownership;
4. failure classification;
5. test evidence.

Adopt a reference difference only when it proves an invariant your design misses or makes the same contract materially easier to inspect.
