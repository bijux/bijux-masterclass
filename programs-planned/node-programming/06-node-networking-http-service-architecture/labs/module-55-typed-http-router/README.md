# Laboratory 5 — Typed HTTP Router

**Module 55**

## Product

Build a transport-neutral router and small in-memory command service. It supports submission with an idempotency key, lookup by typed ID, same-key replay, same-key conflict, revisions, quoted ETags, conditional GET, and stable problems.

## Governing question

> How can route grammar, runtime validation, idempotency, revisions, ETags, and stable errors form one application protocol independent of Node request objects?

## Public surface

- `matchRoute(method, url)` returns an exhaustive route union.
- `validateSubmission(value)` converts `unknown` to a command.
- `Application.submit(command, key)` owns semantic commit.
- `dispatch(request)` returns a finite transport-neutral response.

## Required invariants

- Only exact validated commands reach commit.
- Same key and same semantic request returns one job.
- Same key and different request is conflict.
- In-progress identity is never evicted to admit new work.
- Every state transition increments revision exactly once.
- Matching ETag returns 304 without body.

The laboratory is complete only when the tests distinguish these invariants from a smaller implementation that happens to pass the normal path.

## Implementation sequence

1. Define route and problem unions.
2. Implement exact path and identifier parsing.
3. Validate submission objects.
4. Canonicalize and fingerprint semantic input.
5. Implement bounded idempotency records.
6. Add job revisions and ETags.
7. Add conditional responses and tests for response loss.

Keep the sequence causal. A later feature should not hide an earlier failure. For example, do not add retry before a single attempt has one clear terminal owner, and do not add shutdown before the normal resource lifecycle is observable.

## Adversarial cases

- static versus parameter route
- encoded invalid ID
- extra body property
- same-key same request
- same-key different request
- capacity with only in-progress records
- matching/stale ETag
- response rendering failure after commit

For each case, write the predicted state transition and the exact terminal evidence before running the test. Prefer injected clocks, deterministic fake peers, explicit counters, and local ephemeral ports to arbitrary sleeps.

## Prohibited shortcuts

- passing `IncomingMessage` into domain code
- casting JSON
- hashing raw body bytes
- using request ID as idempotency key
- evicting in-progress records
- publishing events from transport adapter

A shortcut is prohibited because it removes the mechanism under study. It is not a style preference.

## Completion evidence

1. route exhaustiveness
2. interleaved duplicate test
3. one-job result after lost response
4. capacity test without partial commit
5. ETag/HEAD matrix

Also include a small ownership table naming every socket, timer, listener, queue, request, response, or subscription created by the product and its cleanup transition.

## Independent transfer

Design idempotent order submission and identify the exact point where durable storage would become necessary.

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
