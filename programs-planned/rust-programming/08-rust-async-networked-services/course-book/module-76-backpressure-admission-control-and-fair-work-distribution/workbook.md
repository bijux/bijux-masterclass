# Workbook — Module 76: Backpressure, Admission Control, and Fair Work Distribution

[Return to the chapter](index.md) · [Open the solutions](solutions.md) · [Open the JobWire guide](../capstone.md)

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

## Part 4 — Independent laboratory

Build [Bounded Relay Broker](../../labs/module-06-bounded-relay-broker/README.md). Required evidence:

- separate mailbox and active-work bounds;
- no task-per-waiting-request escape;
- exact overload behavior;
- deterministic terminal replies;
- complete task draining;
- a capacity table with units;
- a test where a slow reply receiver does not occupy active-work capacity.

## Part 5 — Capstone transfer

Add JobWire’s broker mailbox, connection request limit, active-job semaphore, result-size bound, idempotency retention bound, and `BUSY` response. Calculate maximum retained request and response bytes. Ensure the broker remains responsive to `STATS` and duplicate requests while jobs execute.

## Part 6 — Reconstruct and defend

1. What is end-to-end backpressure?
2. Why are channel capacity and concurrency limit different?
3. Where should admission occur relative to commitment?
4. Why can a queue harm latency below its hard maximum?
5. How does a slow writer retain service resources?
6. What fairness guarantee is actually implemented?

### Independent transfer

Design overload policy for an image-resize API with small and large jobs. Choose separate or shared queues, per-client limits, retry behavior, and which metrics reveal approaching collapse.
