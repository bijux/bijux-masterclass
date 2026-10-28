# Module 56 Workbook — HTTP Client Ownership

## 1. Predict

1. A request is queued inside an agent for 300 ms. Does that time consume the operation deadline?
2. A POST times out after its body was written. Can the client infer that no server state changed?
3. A response status is 500 with a 50 MB body. Must the client still enforce its body limit?
4. A redirect changes HTTPS to HTTP. Should a service client follow automatically?
5. A request body is a one-shot async iterable. Can it be retried unchanged?

## 2. Diagnose and repair

- Replace per-attempt timeouts with one deadline.
- Close or drain every response body.
- Add bounded response retention.
- Preserve same idempotency key across retries.
- Prevent retry of non-replayable bodies.
- Bound redirects and detect loops.
- Stop forwarding credentials across origins.
- Add explicit agent shutdown.

## 3. Focused construction

1. Configure a private agent.
2. Implement bounded response reading.
3. Parse JSON and problem details from `unknown`.
4. Track attempts.
5. Add one absolute deadline.
6. Add cancellation.
7. Implement a conservative redirect policy.
8. Implement retry for idempotent GET and idempotency-keyed POST.
9. Test ambiguous commit.
10. Make `close()` idempotent.

## 4. Independent laboratory

Build the [Deadline-Aware HTTP Client](../../labs/module-56-deadline-aware-http-client/README.md).

## 5. ServiceWire transfer

Add the supported client and use it in the CLI demo. The demo must close client agents and server runtime even after failure.

## 6. Independent transfer

Design a client that uploads a replayable file segment. State how the segment is reopened, how the deadline spans retries, how partial remote commit is reconciled, and which redirects are forbidden.

## 7. Closed-book defense

1. What does the agent own?
2. What does the semantic operation own?
3. Why is body replayability part of retry policy?
4. What is ambiguous commit?
5. When may a response socket be reused?

## 8. Retry ledger

For a 600 ms operation, simulate:

- attempt 1: connection reset after 120 ms;
- 30 ms backoff;
- attempt 2: 503 after 160 ms;
- 60 ms backoff;
- attempt 3: response headers after 180 ms, body after another 100 ms.

Determine the terminal result and remaining budget at every boundary. Do not reset the deadline. Explain whether the last body can legally complete.

## 9. Client ownership review

List every resource retained by a keep-alive client after one successful request. Add a `close()` contract and tests for double close, request after close, oversized response, cancellation during body receipt, and a late socket error after deadline settlement.

## 10. Redirect and credential matrix

Evaluate a request containing authorization, idempotency key, and replayable body across four redirects: same-origin HTTPS, same host with new port, HTTPS to HTTP, and another origin. For each, decide whether the client follows, which headers survive, whether the method changes, and whether the body may be resent. The default should be refusal unless policy establishes every transferred authority.
