# Laboratory 2 — Bounded TCP Frame Server

**Module 52**

## Product

Build a local TCP request/response server using a four-byte big-endian length prefix. Each accepted payload is decoded as UTF-8, transformed to uppercase, and returned in another frame. The laboratory's purpose is the transport state machine, not the transformation.

## Governing question

> How can one TCP connection carry several bounded messages while arbitrary chunking, EOF, half-close, pressure, and shutdown remain correct?

## Public surface

- `encodeFrame(payload)` creates canonical wire bytes.
- `FrameDecoder` accepts arbitrary chunks and emits complete payloads.
- `finish()` distinguishes clean EOF from truncated prefix or payload.
- `startFrameServer(options)` returns actual endpoint and a complete close handle.

## Required invariants

- No declared length above `maxFrameBytes` causes allocation.
- Chunk partitioning does not change emitted frames.
- EOF is clean only between frames.
- A peer half-close can still receive the final response under the protocol.
- Every accepted socket is tracked until observed close.
- Output respects writable pressure.

The laboratory is complete only when the tests distinguish these invariants from a smaller implementation that happens to pass the normal path.

## Implementation sequence

1. Implement canonical encoding.
2. Implement prefix state and exact boundary tests.
3. Implement payload state and several frames per chunk.
4. Add truncation finalization.
5. Add server, response framing, and half-close policy.
6. Add connection limit, idle policy, and shutdown escalation.

Keep the sequence causal. A later feature should not hide an earlier failure. For example, do not add retry before a single attempt has one clear terminal owner, and do not add shutdown before the normal resource lifecycle is observable.

## Adversarial cases

- prefix split at every byte
- payload split at every byte
- three frames in one chunk
- empty frame
- length exactly at limit and one above
- EOF in prefix and payload
- slow incomplete frame
- peer half-close
- shutdown with open clients

For each case, write the predicted state transition and the exact terminal evidence before running the test. Prefer injected clocks, deterministic fake peers, explicit counters, and local ephemeral ports to arbitrary sleeps.

## Prohibited shortcuts

- treating each `data` chunk as a message
- allocating before validating length
- discarding partial state at EOF
- retrying bytes after `write()` returns false
- assuming `server.close()` closes clients

A shortcut is prohibited because it removes the mechanism under study. It is not a style preference.

## Completion evidence

1. partition-invariance tests
2. exact truncation error codes
3. half-close response test
4. socket-registry reconciliation
5. shutdown test that ends without active handles

Also include a small ownership table naming every socket, timer, listener, queue, request, response, or subscription created by the product and its cleanup transition.

## Independent transfer

Design a frame with a fixed header followed by metadata and payload sections. Give each section an independent bound and define EOF in every state.

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
