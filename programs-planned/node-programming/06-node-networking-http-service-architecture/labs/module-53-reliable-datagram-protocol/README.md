# Laboratory 3 — Reliable Datagram Protocol

**Module 53**

## Product

Build a request/response datagram protocol with version, message type, random nonce, bounded payload, one total deadline, retries, duplicate handling, and a bounded responder replay cache. A controlled local socket or injected exchange drives every test.

## Governing question

> How can a small UDP protocol correlate replies, tolerate ordinary loss and duplication, and remain bounded without pretending UDP is reliable or authenticated?

## Public surface

- `encodeRequest` and `decodeRequest` implement strict canonical syntax.
- `requestWithRetry(exchange, request, policy)` returns one correlated response.
- `ReplayCache` remembers bounded terminal responses.
- `startResponder(options)` owns and closes one UDP socket.

## Required invariants

- Datagrams above the declared bound are rejected before parsing.
- Retransmissions preserve semantic request identity.
- Only matching nonce and accepted peer can complete the operation.
- Unrelated malformed traffic cannot terminate the current request.
- Replay cache count and lifetime are bounded.
- Discovery or response correlation does not grant authorization.

The laboratory is complete only when the tests distinguish these invariants from a smaller implementation that happens to pass the normal path.

## Implementation sequence

1. Define and parse the wire grammar.
2. Generate strong nonces.
3. Implement deterministic retry planning under one deadline.
4. Filter by nonce and peer.
5. Ignore stale and duplicate responses.
6. Add responder replay behavior and capacity.
7. Close socket, timers, and listeners on every terminal path.

Keep the sequence causal. A later feature should not hide an earlier failure. For example, do not add retry before a single attempt has one clear terminal owner, and do not add shutdown before the normal resource lifecycle is observable.

## Adversarial cases

- dropped first request
- duplicate response
- reordered stale response
- wrong nonce
- correct nonce from wrong peer
- oversized datagram
- malformed unrelated datagram
- deadline before retry
- replay-cache capacity

For each case, write the predicted state transition and the exact terminal evidence before running the test. Prefer injected clocks, deterministic fake peers, explicit counters, and local ephemeral ports to arbitrary sleeps.

## Prohibited shortcuts

- first datagram wins
- new nonce for each retransmission
- one full timeout per attempt
- unbounded replay map
- treating source endpoint as strong identity
- large unauthenticated responses

A shortcut is prohibited because it removes the mechanism under study. It is not a style preference.

## Completion evidence

1. attempt history
2. one terminal completion under duplicate replies
3. wrong-peer test
4. bounded replay eviction test
5. amplification ratio note

Also include a small ownership table naming every socket, timer, listener, queue, request, response, or subscription created by the product and its cleanup transition.

## Independent transfer

Design a telemetry acknowledgment protocol with duplicate suppression. State what happens when an acknowledgment arrives after local timeout and what requires authentication.

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
