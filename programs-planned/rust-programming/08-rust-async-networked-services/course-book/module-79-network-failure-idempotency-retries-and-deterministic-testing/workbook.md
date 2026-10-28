# Workbook — Module 79: Network Failure, Idempotency, Retries, and Deterministic Testing

[Return to the chapter](index.md) · [Open the solutions](solutions.md) · [Open the JobWire guide](../capstone.md)

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

## Part 5 — Capstone transfer

Add JobWire’s idempotency map and client retry helper. Scope keys to the service process and state that limitation. Keep a bounded terminal cache. Test duplicate while in progress, duplicate after success, duplicate after terminal domain error, conflict, eviction, disconnect after commit, and deadline exhaustion.

## Part 6 — Reconstruct and defend

1. What makes remote commit ambiguous?
2. What information belongs in an idempotency record?
3. Why is request correlation not enough?
4. Which failures should never retry?
5. Why must attempts share one deadline?
6. What makes an async timing test causal?

### Independent transfer

Design idempotent retry for an email-send service. State whether provider acceptance, actual delivery, and local response are different commits, and what result can honestly be cached.
