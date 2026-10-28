# Worked answers — Synchronous Collaboration, API Composition, and Dependency Budgets

These answers demonstrate reasoning. Revise your own answer when its decision rule or evidence is weaker.

## 1. Why does a three-service serial path reduce availability?

The path requires all dependencies simultaneously. Approximate availability multiplies, so each additional required edge consumes the public objective.

**Decisive evidence:** dependency availability worksheet

## 2. Why is a synchronous cycle more than a diagram smell?

It creates recursive failure, retry, deployment, and recovery coupling. Neither service can recover or release independently when each requires the other.

**Decisive evidence:** cycle detection proof

## 3. Who owns the deadline for a public request?

The edge that knows when the result loses user value. Downstream services receive remaining budget, not fresh timeouts.

**Decisive evidence:** deadline allocation trace

## 4. What is wrong with retries in client, gateway, mesh, and callee simultaneously?

Attempts multiply, overload worsens, and ownership becomes invisible. One layer must own retries per edge with idempotency and remaining budget.

**Decisive evidence:** attempt-count fault test

## 5. How should the gateway represent an unavailable artifact service for a completed run?

Return authoritative run state and explicit partial artifact status or warning, according to the public contract. Do not return an empty authoritative artifact list.

**Decisive evidence:** partial-response conformance

## 6. Why can parallel fan-out still be harmful when it lowers latency?

It increases instantaneous load, failure combinations, and downstream concurrency. Bound it and prefer batch interfaces.

**Decisive evidence:** fan-out resource profile

## 7. A run list triggers one artifact RPC per row. What should change?

Use summaries, a batch lookup, a local projection, or separate client-requested artifact connection. Remote N+1 is rejected.

**Decisive evidence:** call-count budget

## 8. When can a read retry be safe?

When the operation is semantically safe, the status is retryable, remaining deadline covers another attempt, and one layer owns the retry.

**Decisive evidence:** retry policy vector

## 9. Why can service discovery not decide retry safety?

Discovery selects an address. It does not know whether a mutation committed or whether durable idempotency exists.

**Decisive evidence:** interaction ownership map

## 10. What does maximum public synchronous depth protect?

It limits compounded latency, availability, and operational dependency on user-facing paths.

**Decisive evidence:** dependency graph fitness function

## 11. When should the gateway skip optional composition?

When remaining budget cannot satisfy the downstream call and the contract permits explicit partial data. It must not silently change semantics.

**Decisive evidence:** deadline degradation test

## 12. Why is a batch endpoint sometimes better than client-side concurrency?

It lets the owner optimize data access and enforce one bounded request, reducing network attempts and preserving authorization in one service.

**Decisive evidence:** batch contract and load evidence
