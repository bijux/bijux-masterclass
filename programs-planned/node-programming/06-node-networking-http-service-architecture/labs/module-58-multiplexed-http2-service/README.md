# Laboratory 8 — Multiplexed HTTP/2 Service

**Module 58**

## Product

Build an h2c local service with finite health and echo routes. It normalizes pseudo-headers, bounds each body, limits sessions and streams, respects stream pressure, isolates resets, and drains with GOAWAY before forced destruction.

## Governing question

> How can one HTTP/2 session own concurrent streams without mixing stream-local failure, session failure, body bounds, flow control, and application admission?

## Public surface

- `startHttp2Service(options)` returns actual authority and close handle.
- Each stream maps to one finite request/response exchange.
- Session and stream registries are separately observable.
- Client helper opens concurrent streams and closes its session.

## Required invariants

- One stream reset does not destroy unrelated streams.
- Every stream body has an independent bound.
- Aggregate active-stream admission is bounded.
- Application results do not depend on completion order.
- GOAWAY begins closure but all streams are still joined.
- Session destruction gives every open stream a terminal result.

The laboratory is complete only when the tests distinguish these invariants from a smaller implementation that happens to pass the normal path.

## Implementation sequence

1. Start h2c server.
2. Normalize pseudo-headers.
3. Implement bounded body and response.
4. Open concurrent streams.
5. Reset one stream.
6. Set low stream capacity.
7. Track sessions and streams.
8. Implement GOAWAY and force close.

Keep the sequence causal. A later feature should not hide an earlier failure. For example, do not add retry before a single attempt has one clear terminal owner, and do not add shutdown before the normal resource lifecycle is observable.

## Adversarial cases

- concurrent fast/slow streams
- invalid pseudo-header type
- body over limit
- client reset before response
- session error
- stream capacity exceeded
- GOAWAY with active stream
- client session left open

For each case, write the predicted state transition and the exact terminal evidence before running the test. Prefer injected clocks, deterministic fake peers, explicit counters, and local ephemeral ports to arbitrary sleeps.

## Prohibited shortcuts

- one registry for sessions and streams
- destroy session on application error
- duplicate domain router
- assert completion order
- treat GOAWAY as completed shutdown

A shortcut is prohibited because it removes the mechanism under study. It is not a style preference.

## Completion evidence

1. concurrent identity-correct responses
2. stream reset isolation
3. session/stream final counts
4. equivalent HTTP/1.1 semantics
5. grace then destroy test

Also include a small ownership table naming every socket, timer, listener, queue, request, response, or subscription created by the product and its cleanup transition.

## Independent transfer

Build a TLS HTTP/2 client that requires ALPN `h2` and reconciles a reset submission through idempotency.

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
