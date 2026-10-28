# Workbook — Module 79: Network Failure, Idempotency, Retries, and Deterministic Testing

[Chapter](index.md) · [Laboratory](../../labs/module-09-idempotent-retry-client/README.md) · [JobWire guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Network Failure, Idempotency, Retries, and Deterministic Testing** has become a usable model rather than remembered vocabulary. Its governing question is: *When a network operation fails without revealing whether the remote side committed it, how do idempotency, retry budgets, failure classification, and deterministic tests preserve one semantic outcome?* Preserve your first prediction and record decisive facts in a **retry and commit matrix**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 78 — HTTP Services with Hyper: Requests, Bodies, and Connections that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **When a network operation fails without revealing whether the remote side committed it, how do idempotency, retry budgets, failure classification, and deterministic tests preserve one semantic outcome?**
3. Draw the smallest **retry and commit matrix** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

1. A client times out after fully writing a request but before reading a response. Is “not committed” a valid conclusion?
2. The client retries with a newly generated idempotency key. What semantic behavior can result?
3. The same key and different payload arrive. May the server return the first cached result?
4. A record expires before the documented client retry window ends. Which guarantee fails?
5. A malformed response is retried because all I/O/protocol errors are marked transient. What risk appears?
6. Backoff uses exact 100, 200, 400 ms delays for every client. What system behavior can emerge?
7. A test sleeps 50 ms and expects retry attempt two to have started. Why is the test weak?
8. In-memory idempotency survives a TCP reconnect. Does it survive process restart?

## Part 2 — Diagnose and repair

A client retries every error three times, creates a new request and key each time, resets the timeout for every attempt, and tests with real sleeps. The server caches only successful results and permits key reuse for different payloads.

Repair the semantic identity, failure classifier, in-progress record, terminal error retention, deadline, jitter source, and tests.

## Part 3 — Focused exercises

### Exercise 1 — Failure matrix

Classify resolve failure, connect refusal, reset before write, reset after write, busy response, invalid request, malformed response, domain rejection, and deadline exhaustion.

### Exercise 2 — Record state machine

Design `Vacant`, `InProgress`, `Completed`, and `TerminalFailure` states. Specify duplicate behavior and bounded waiters.

### Exercise 3 — Fingerprint

Create a canonical fingerprint input for JobWire submit requests. Include operation and payload; exclude request ID; justify every field.

### Exercise 4 — Paused-time retry

Test attempt timing, attempt limit, overall deadline, and jitter with Tokio time paused.

### Exercise 5 — Ambiguous commit

Script a server that commits once, closes before response on attempt one, and returns cached success on attempt two. Assert one execution.

### Interleaved reasoning pass

1. For **Classify failures by phase, scope, retryability, and commit ambiguity**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the retry and commit matrix.
2. For **Distinguish idempotent operation semantics from retrying an HTTP or TCP request**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the retry and commit matrix.
3. For **Design idempotency keys with scope, fingerprint, in-progress state, terminal result, and retention**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the retry and commit matrix.
4. For **Reject key reuse with different request content**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the retry and commit matrix.

5. Identify one guarantee from an earlier course that a careless implementation of **Network Failure, Idempotency, Retries, and Deterministic Testing** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Idempotent Retry Client](../../labs/module-09-idempotent-retry-client/README.md). Required evidence:

- structured failure classification;
- one semantic key across attempts;
- key/payload conflict rejection;
- bounded in-progress and completed state;
- overall deadline;
- deterministic jitter;
- paused-time tests;
- exact commit and attempt counts.

### Laboratory acceptance trace

Before opening the reference implementation for **Idempotent Retry Client**, record:

- the public behavior that demonstrates **Classify failures by phase, scope, retryability, and commit ambiguity**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Add JobWire’s idempotency map and client retry helper. Scope keys to the service process and state that limitation. Keep a bounded terminal cache. Test duplicate while in progress, duplicate after success, duplicate after terminal domain error, conflict, eviction, disconnect after commit, and deadline exhaustion.

### Capstone invariant trace

For the Module 79 JobWire increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. What makes remote commit ambiguous?
2. What information belongs in an idempotency record?
3. Why is request correlation not enough?
4. Which failures should never retry?
5. Why must attempts share one deadline?
6. What makes an async timing test causal?

### Independent transfer

Design idempotent retry for an email-send service. State whether provider acceptance, actual delivery, and local response are different commits, and what result can honestly be cached.

### Closed-book defense

In five minutes, answer “When a network operation fails without revealing whether the remote side committed it, how do idempotency, retry budgets, failure classification, and deterministic tests preserve one semantic outcome?” using the **retry and commit matrix**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside JobWire. A list of APIs without the deciding relationship is incomplete.
