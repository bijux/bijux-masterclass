# Laboratory 6 — Deadline-Aware HTTP Client

**Module 56**

## Product

Build a typed client around Node's `http` and `https` APIs. It uses private agents, collects bounded responses, parses stable problems, records attempts, applies one deadline, follows only a narrow redirect policy, retries supported failures, and closes cleanly.

## Governing question

> How can an HTTP client own pooled sockets, one deadline, bounded response bodies, redirect decisions, and idempotency-aware retries as one semantic operation?

## Public surface

- `HttpClient.request(spec)` returns typed success or failure.
- `readBoundedResponse` enforces observed byte limits.
- `AttemptRecord` preserves bounded causal history.
- `close()` destroys owned agents and rejects new work.

## Required invariants

- All attempts and redirects share one deadline.
- Every response is consumed within a bound or destroyed.
- Retry preserves semantic idempotency identity.
- Non-replayable bodies are not retried.
- Cross-origin credentials are never forwarded implicitly.
- Client close settles once and releases agent sockets.

The laboratory is complete only when the tests distinguish these invariants from a smaller implementation that happens to pass the normal path.

## Implementation sequence

1. Create private agents.
2. Implement one finite request.
3. Add response limit and media validation.
4. Add deadline and cancellation.
5. Add attempt records.
6. Add no-redirect or constrained redirect policy.
7. Add idempotent retry.
8. Add lifecycle close.

Keep the sequence causal. A later feature should not hide an earlier failure. For example, do not add retry before a single attempt has one clear terminal owner, and do not add shutdown before the normal resource lifecycle is observable.

## Adversarial cases

- agent queue delay
- slow headers
- oversized 2xx body
- oversized error body
- redirect loop
- HTTPS downgrade
- cross-origin authorization
- reset before write
- reset after server commit
- close with idle sockets

For each case, write the predicted state transition and the exact terminal evidence before running the test. Prefer injected clocks, deterministic fake peers, explicit counters, and local ephemeral ports to arbitrary sleeps.

## Prohibited shortcuts

- fresh timeout per attempt
- retry with new idempotency key
- retry one-shot body
- ignore error response body
- follow every redirect
- use global agent without lifecycle

A shortcut is prohibited because it removes the mechanism under study. It is not a style preference.

## Completion evidence

1. ambiguous-commit reconciliation
2. deadline includes retry delay
3. agent close test
4. body-limit test for errors
5. attempt history without secrets

Also include a small ownership table naming every socket, timer, listener, queue, request, response, or subscription created by the product and its cleanup transition.

## Independent transfer

Design a replayable file-range upload client with one deadline and server-side reconciliation.

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
