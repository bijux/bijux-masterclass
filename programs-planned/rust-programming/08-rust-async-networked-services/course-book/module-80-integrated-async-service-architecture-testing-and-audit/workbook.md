# Workbook — Module 80: Integrated Async Service Architecture, Testing, and Audit

[Chapter](index.md) · [Laboratory](../../labs/module-10-async-service-audit/README.md) · [JobWire guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Integrated Async Service Architecture, Testing, and Audit** has become a usable model rather than remembered vocabulary. Its governing question is: *Can the complete service be explained as one coherent set of lifecycle, protocol, capacity, cancellation, failure, compatibility, and operational contracts rather than as a pile of async APIs?* Preserve your first prediction and record decisive facts in a **async service dossier**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 79 — Network Failure, Idempotency, Retries, and Deterministic Testing that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Can the complete service be explained as one coherent set of lifecycle, protocol, capacity, cancellation, failure, compatibility, and operational contracts rather than as a pile of async APIs?**
3. Draw the smallest **async service dossier** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each design, identify the first failed contract:

1. Connections are bounded, but each can pipeline unlimited requests.
2. The broker queue and active jobs are bounded, but completed idempotency records never expire.
3. Shutdown cancels every token but retains no task handles.
4. The service retries reset-after-write requests with a new key.
5. Health says ready when the HTTP route responds, even after the broker exits.
6. Frame length is bounded, but HTTP bodies are collected without a limit.
7. Tests use one-byte chunks but never test coalesced frames.
8. The service scales to three replicas while idempotency remains process-local.

## Part 2 — Diagnose and repair

Audit a hypothetical service with these properties:

```text
untracked connection spawns
bounded broker queue
unbounded result cache
fresh timeout at every stage
one global mutex held through response writes
HTTP health through broker work queue
retry every I/O error
cancel token on shutdown, no joins
```

Produce a prioritized repair plan. Explain which defects threaten memory, correctness, liveness, compatibility, and observability. Do not solve everything by adding more tasks or locks.

## Part 3 — Focused exercises

### Exercise 1 — Nine ledgers

Complete the full JobWire dossier. Every row must name owner, bound, transition, failure, and test.

### Exercise 2 — Failure-cut trace

Take the 18-step successful request trace and insert failure after every step. Classify commit knowledge and recovery.

### Exercise 3 — Resource envelope

Calculate a conservative payload bound for the configured capstone. List excluded overhead and kernel/runtime resources.

### Exercise 4 — Intersection tests

Implement at least eight tests from the chapter matrix. Every test must control the causal state with a gate, partition, or paused clock.

### Exercise 5 — Compatibility review

Classify ten proposed changes as internal, backward-compatible, versioned, or breaking. Include frame size, new command, new error code, idempotency retention, and HTTP field changes.

### Interleaved reasoning pass

1. For **Construct a complete async service dossier**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the async service dossier.
2. For **Trace one request from accepted socket through terminal response and cleanup**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the async service dossier.
3. For **Identify the authoritative owner of protocol, broker, idempotency, metrics, and shutdown state**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the async service dossier.
4. For **Calculate end-to-end resource bounds and expose assumptions**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the async service dossier.

5. Identify one guarantee from an earlier course that a careless implementation of **Integrated Async Service Architecture, Testing, and Audit** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Async Service Audit](../../labs/module-10-async-service-audit/README.md). It is not JobWire. Produce a small bounded service and a complete dossier, then inject at least three failures at mechanism intersections.

Required evidence:

- no unowned spawned task;
- complete capacity table;
- frame and protocol state tests;
- cancellation ledger;
- idempotency proof;
- graceful shutdown proof;
- honest health semantics;
- explicit non-guarantees.

### Laboratory acceptance trace

Before opening the reference implementation for **Async Service Audit**, record:

- the public behavior that demonstrates **Construct a complete async service dossier**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Finish JobWire. Run all unit, integration, protocol, chunking, saturation, retry, HTTP, and shutdown tests. Produce:

- protocol specification;
- configuration and limits table;
- operational runbook;
- compatibility note;
- single-process scope note;
- final architecture defense.

Then remove any mechanism whose only justification is “the course covered it.” Every remaining task, channel, endpoint, and dependency must have one product responsibility.

### Capstone invariant trace

For the Module 80 JobWire increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without notes:

1. What wakes a pending JobWire future?
2. Who owns every task category?
3. What is the frame maximum and where is it enforced?
4. Which messages are legal before handshake?
5. Where is request commitment?
6. What bounds total waiting work?
7. What happens when the client disappears after commit?
8. What exactly does `/health` prove?
9. What are the shutdown phases?
10. Which guarantee fails first under multi-process deployment?

### Independent transfer

Given a simple synchronous Rust daemon, write the decision memo for whether it should become async. Compare workload, connection count, I/O wait, CPU cost, cancellation, operational complexity, dependency surface, and testability. “Async is faster” is not an acceptable argument.

### Closed-book defense

In five minutes, answer “Can the complete service be explained as one coherent set of lifecycle, protocol, capacity, cancellation, failure, compatibility, and operational contracts rather than as a pile of async APIs?” using the **async service dossier**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside JobWire. A list of APIs without the deciding relationship is incomplete.
