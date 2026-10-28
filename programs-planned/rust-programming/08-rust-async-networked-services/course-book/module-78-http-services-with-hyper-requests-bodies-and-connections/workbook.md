# Workbook — Module 78: HTTP Services with Hyper: Requests, Bodies, and Connections

[Chapter](index.md) · [Laboratory](../../labs/module-08-hyper-health-surface/README.md) · [JobWire guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **HTTP Services with Hyper: Requests, Bodies, and Connections** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you build a small HTTP service while keeping transport ownership, HTTP connection driving, request-body policy, routing, application state, and health semantics separate?* Preserve your first prediction and record decisive facts in a **HTTP boundary map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 77 — Cancellation Safety, Deadlines, and Graceful Shutdown that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you build a small HTTP service while keeping transport ownership, HTTP connection driving, request-body policy, routing, application state, and health semantics separate?**
3. Draw the smallest **HTTP boundary map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

1. A Hyper request handler calls `collect()` on any incoming body without a limit. What resource can a client control?
2. `/health` sends a message through the same saturated job queue as ordinary work. What operational failure appears?
3. A route holds a broker mutex while returning a streaming body. How long can the critical section last?
4. The listener spawns each HTTP connection and drops its handle. What shutdown evidence is missing?
5. `uri.path()` returns `/items/%2Fsecret`. Has percent decoding already produced an application identifier?
6. An application validation error is returned as `Err` from the Hyper service and closes the connection. Is that necessarily the best scope?
7. A response body is produced with `format!("{state:?}")`. What compatibility problem appears?
8. A health response says `healthy=true` because the HTTP event loop responds. Does that prove the broker accepts jobs?

## Part 2 — Diagnose and repair

A single function accepts sockets, constructs Hyper connections, routes requests, locks application state, collects bodies, formats debug output, and handles shutdown. Split it into four layers and define the error boundary of each.

## Part 3 — Focused exercises

### Exercise 1 — Pure router

Implement `GET /health`, `GET /stats`, 404, and 405 as a pure request-to-response function with deterministic bodies.

### Exercise 2 — Body limit

Implement a frame-counting body collector with a 4 KiB maximum. Return 413 without retaining more than the limit plus one inspected frame.

### Exercise 3 — Health semantics

Define liveness, readiness, and degraded states. State data source, staleness, and what each does not prove.

### Exercise 4 — Connection lifecycle

Add a listener, connection semaphore, `JoinSet`, shutdown token, grace period, abort, and join.

### Exercise 5 — Slow client

Prove a slow HTTP reader does not retain a broker lock or job permit.

### Interleaved reasoning pass

1. For **Distinguish accepted transport, HTTP connection future, request future, body stream, and application service**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the HTTP boundary map.
2. For **Serve HTTP/1 connections with Hyper over Tokio I/O**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the HTTP boundary map.
3. For **Construct stable response body types and status codes**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the HTTP boundary map.
4. For **Route by method and path without mixing broker logic into transport code**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the HTTP boundary map.

5. Identify one guarantee from an earlier course that a careless implementation of **HTTP Services with Hyper: Requests, Bodies, and Connections** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Hyper Health Surface](../../labs/module-08-hyper-health-surface/README.md). Required evidence:

- pure route tests;
- exact status and content type;
- bounded or forbidden request bodies;
- explicit health semantics;
- tracked connection tasks;
- bounded admission;
- graceful shutdown under keep-alive.

### Laboratory acceptance trace

Before opening the reference implementation for **Hyper Health Surface**, record:

- the public behavior that demonstrates **Distinguish accepted transport, HTTP connection future, request future, body stream, and application service**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Add JobWire’s `/health` and `/stats` HTTP/1 routes using Hyper. Health must distinguish `starting`, `ready`, `shutting-down`, and `failed`. Stats are advisory and deterministic. The HTTP surface may not submit jobs or share the broker’s saturated work queue.

### Capstone invariant trace

For the Module 78 JobWire increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. Which layer accepts TCP?
2. Which layer drives HTTP connection state?
3. Where is body size enforced?
4. What does readiness prove?
5. Why should application errors often become responses?
6. Who joins HTTP connection tasks?

### Independent transfer

Design an HTTP upload route for a 10 MiB maximum file without collecting the whole body. State streaming ownership, temporary storage, cancellation, commit, response, and shutdown behavior.

### Closed-book defense

In five minutes, answer “How do you build a small HTTP service while keeping transport ownership, HTTP connection driving, request-body policy, routing, application state, and health semantics separate?” using the **HTTP boundary map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside JobWire. A list of APIs without the deciding relationship is incomplete.
