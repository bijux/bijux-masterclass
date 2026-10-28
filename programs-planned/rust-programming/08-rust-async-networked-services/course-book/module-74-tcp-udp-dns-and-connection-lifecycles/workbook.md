# Workbook — Module 74: TCP, UDP, DNS, and Connection Lifecycles

[Chapter](index.md) · [Laboratory](../../labs/module-04-deadline-echo-service/README.md) · [JobWire guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **TCP, UDP, DNS, and Connection Lifecycles** has become a usable model rather than remembered vocabulary. Its governing question is: *What lifecycle does each network transport actually provide, and where should connection admission, name resolution, deadlines, half-close, datagram loss, and peer identity be represented?* Preserve your first prediction and record decisive facts in a **connection lifecycle map**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 73 — Async I/O, Buffers, Streams, and Framing that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **What lifecycle does each network transport actually provide, and where should connection admission, name resolution, deadlines, half-close, datagram loss, and peer identity be represented?**
3. Draw the smallest **connection lifecycle map** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

1. A service has a listener backlog of 128 but no application connection limit. Is live application work bounded at 128?
2. A TCP `write_all` returns successfully. Has the remote application committed the request?
3. A TCP read returns zero while the local writer remains open. What direction has closed?
4. A client applies a five-second timeout independently to DNS, each of four addresses, and handshake. What maximum user-visible delay can result?
5. A UDP socket is “connected.” Does that guarantee delivery and authentic peer identity?
6. A server acquires a semaphore permit after spawning a connection task. What resource growth remains possible?
7. An idle timeout resets on every received byte. How can a hostile peer retain the connection?
8. A split TCP writer task exits, but the reader task and admission permit remain. Is the connection lifecycle complete?

## Part 2 — Diagnose and repair

A client resolves a hostname, tries only the first address, applies no connect deadline, writes one request, and on read timeout retries on a new connection without an idempotency key. Diagnose phase reporting, overall budget, address selection, and ambiguous commit.

Repair only the transport lifecycle in this module. Record the remaining application-level ambiguity for Module 79 rather than pretending transport can solve it.

## Part 3 — Focused exercises

### Exercise 1 — Admission placement

Compare permit-before-accept and accept-then-try-permit designs under overload. State accepted socket count, response ability, backlog behavior, and fairness.

### Exercise 2 — Deadline propagation

Implement a small `Deadline` wrapper with `remaining()` and use it across resolution, connect, and handshake. Ensure no stage receives a fresh full budget.

### Exercise 3 — Half-close

Write a loopback test where the client sends a request, shuts down its write half, and still reads a response. Explain the protocol meaning.

### Exercise 4 — UDP contract

Design a metrics datagram format. State maximum datagram size, duplicate handling, ordering policy, authentication non-goal, and what loss means.

### Exercise 5 — Connection ledger

Write every state, resource owner, deadline, legal I/O, and close path for a framed request/response connection.

### Interleaved reasoning pass

1. For **Distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the connection lifecycle map.
2. For **Acquire connection admission before spawning unbounded tasks**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the connection lifecycle map.
3. For **Explain the limits of socket backlog as application backpressure**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the connection lifecycle map.
4. For **Model DNS resolution and multi-address connection attempts under one deadline**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the connection lifecycle map.

5. Identify one guarantee from an earlier course that a careless implementation of **TCP, UDP, DNS, and Connection Lifecycles** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Deadline Echo Service](../../labs/module-04-deadline-echo-service/README.md). Prove:

- bounded accepted connections;
- explicit task ownership;
- idle and write-stall timeouts;
- clean EOF handling;
- deterministic shutdown of idle connections;
- release of every admission permit;
- no reliance on one read per message.

### Laboratory acceptance trace

Before opening the reference implementation for **Deadline Echo Service**, record:

- the public behavior that demonstrates **Distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Add JobWire’s TCP listener, admission semaphore, connection `JoinSet`, peer observation, and handshake deadline. Do not add broker work yet. Define which accept errors are fatal, retryable, or shutdown-related. Add a test that saturates connection permits and proves the service does not spawn a task for unadmitted work.

### Capstone invariant trace

For the Module 74 JobWire increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. Why is the listener backlog not the service’s work bound?
2. What does successful local write prove?
3. How can one TCP direction close independently?
4. Why should one deadline cover several stages?
5. What does connected UDP change and not change?
6. Why must split halves retain one lifecycle owner?

### Independent transfer

Design a bounded chat server transport layer for 1,000 clients. Do not design chat semantics. Specify admission, task ownership, read/write halves, idle policy, output queue bound, peer observation, and shutdown.

### Closed-book defense

In five minutes, answer “What lifecycle does each network transport actually provide, and where should connection admission, name resolution, deadlines, half-close, datagram loss, and peer identity be represented?” using the **connection lifecycle map**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside JobWire. A list of APIs without the deciding relationship is incomplete.
