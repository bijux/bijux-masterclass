# Workbook — Module 76: Backpressure, Admission Control, and Fair Work Distribution

[Chapter](index.md) · [Laboratory](../../labs/module-06-bounded-relay-broker/README.md) · [JobWire guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Backpressure, Admission Control, and Fair Work Distribution** has become a usable model rather than remembered vocabulary. Its governing question is: *When demand exceeds service capacity, where may work wait, which bound is authoritative, and how does overload become an explicit product outcome instead of memory growth, latency collapse, or starvation?* Preserve your first prediction and record decisive facts in a **capacity and admission ledger**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 75 — Protocol State Machines, Versioning, and Defensive Parsing that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **When demand exceeds service capacity, where may work wait, which bound is authoritative, and how does overload become an explicit product outcome instead of memory growth, latency collapse, or starvation?**
3. Draw the smallest **capacity and admission ledger** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

1. A service limits active jobs to 16 but creates one waiting task for every request. Is task memory bounded?
2. The broker mailbox is bounded at 128, but each of 1,000 connections retains one decoded request while waiting to send. What is the real queued request bound?
3. A broker acquires a job semaphore inside its only receive loop and waits. Which messages become head-of-line blocked?
4. A response writer holds the job permit until a slow client reads the result. Which capacities have become coupled?
5. The server returns `BUSY retry-after=100` and every client retries exactly after 100 ms. What load pattern can result?
6. A per-connection limit is one request, but one tenant opens 500 connections. Which fairness problem remains?
7. A bounded queue is consistently 90% full. Is the service necessarily healthy because the hard bound is not reached?
8. TCP flow control eventually slows the sender. Why is that not a complete application bound?

## Part 2 — Diagnose and repair

A server accepts unlimited connections, reads requests continuously, sends them to an unbounded channel, spawns one task per request, and limits only the CPU section with a semaphore. Responses are stored until clients read them.

Build a capacity ledger, then redesign admission, queueing, active work, result retention, and writer deadlines. State which requests wait and which receive immediate overload responses.

## Part 3 — Focused exercises

### Exercise 1 — Resource envelope

Calculate a conservative envelope for 200 connections, 32 KiB input frame, one request per connection, 64 broker slots, eight active jobs, 64 KiB result maximum, and 5,000 idempotency records.

### Exercise 2 — Commit point

Choose the JobWire commit point. Explain what a connection timeout means before and after it.

### Exercise 3 — Fair scheduler

Design round-robin scheduling across three tenants with per-tenant queue limits and one global worker limit. State starvation and ordering behavior.

### Exercise 4 — Slow consumer

Refactor result ownership so compute permits release before network output. Bound retained completed results.

### Exercise 5 — Saturation test

Use notifications to hold all active jobs, fill the queue exactly, submit one additional request, and prove the configured overload result.

### Interleaved reasoning pass

1. For **Find every accumulation point in an async service**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the capacity and admission ledger.
2. For **Distinguish connection admission, queue capacity, active-work permits, response buffering, and retry budgets**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the capacity and admission ledger.
3. For **Choose between waiting, rejecting, shedding, degrading, and disconnecting under overload**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the capacity and admission ledger.
4. For **Acquire permits before irreversible commitment**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the capacity and admission ledger.

5. Identify one guarantee from an earlier course that a careless implementation of **Backpressure, Admission Control, and Fair Work Distribution** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build [Bounded Relay Broker](../../labs/module-06-bounded-relay-broker/README.md). Required evidence:

- separate mailbox and active-work bounds;
- no task-per-waiting-request escape;
- exact overload behavior;
- deterministic terminal replies;
- complete task draining;
- a capacity table with units;
- a test where a slow reply receiver does not occupy active-work capacity.

### Laboratory acceptance trace

Before opening the reference implementation for **Bounded Relay Broker**, record:

- the public behavior that demonstrates **Find every accumulation point in an async service**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Add JobWire’s broker mailbox, connection request limit, active-job semaphore, result-size bound, idempotency retention bound, and `BUSY` response. Calculate maximum retained request and response bytes. Ensure the broker remains responsive to `STATS` and duplicate requests while jobs execute.

### Capstone invariant trace

For the Module 76 JobWire increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

1. What is end-to-end backpressure?
2. Why are channel capacity and concurrency limit different?
3. Where should admission occur relative to commitment?
4. Why can a queue harm latency below its hard maximum?
5. How does a slow writer retain service resources?
6. What fairness guarantee is actually implemented?

### Independent transfer

Design overload policy for an image-resize API with small and large jobs. Choose separate or shared queues, per-client limits, retry behavior, and which metrics reveal approaching collapse.

### Closed-book defense

In five minutes, answer “When demand exceeds service capacity, where may work wait, which bound is authoritative, and how does overload become an explicit product outcome instead of memory growth, latency collapse, or starvation?” using the **capacity and admission ledger**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside JobWire. A list of APIs without the deciding relationship is incomplete.
