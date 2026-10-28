# Course 6 Final Review

Complete this review without the solution file. Use diagrams and state tables, not only prose.

## Part I — Layer separation

1. A hostname resolves to two addresses. The first connect attempt consumes 800 ms and the second succeeds after 500 ms. The caller promised a one-second operation budget. Explain why two independent one-second connect timers are incorrect and design the correct budget.
2. A TCP server receives one complete frame and half of the next frame before EOF. State the result for each frame and the connection.
3. A UDP client retries with the same request ID. Two valid responses arrive from the expected peer after the first timeout. Which response may complete the operation, and what happens to the other?
4. A TLS handshake succeeds with a trusted certificate whose names do not include the requested hostname. Which layer succeeded and which contract failed?
5. An HTTP/2 stream resets while three other streams continue. Explain why treating this as session failure is too strong.

## Part II — HTTP semantics

6. Define safe, idempotent, cacheable, and retryable. Give one example where these classifications differ.
7. A client times out after sending an idempotency-keyed POST but before receiving headers. State what the client knows and what it must do next.
8. A route accepts JSON but receives `text/plain`, an empty body, malformed JSON, and valid JSON with an invalid domain field. Assign each failure to the correct layer and status family.
9. A GET response has ETag `"job-2-rev-4"`. The next request sends `If-None-Match` with that value, but the job revision is now 5. State the correct response behavior.
10. Explain why redirect following must reconsider origin, method, credentials, and remaining deadline.

## Part III — Capacity and lifecycle

11. Draw every ServiceWire queue and retained structure. State its unit and bound.
12. The listener has capacity, but the idempotency-record limit is full. Which component rejects the request, and what should health and readiness report?
13. An SSE subscriber stops reading. Explain how this can consume server memory even though event history is bounded.
14. Shutdown begins while a body is still arriving, two jobs are active, an SSE client is connected, and one HTTP/2 session contains three streams. Produce a phased shutdown plan.
15. Explain why live counters observed before complete join cannot replace an authoritative post-shutdown report.

## Part IV — Security and trust

16. Explain why UDP discovery must not grant authorization.
17. Explain the difference among a dedicated local CA, a self-signed leaf certificate, and disabling certificate verification.
18. Name five peer-controlled values that need independent bounds.
19. Show how an error response can preserve causal information without echoing secrets or unbounded input.
20. Explain why a request ID and an idempotency key are not interchangeable.

## Part V — Independent construction

Design a bounded thumbnail service with:

- HTTP/1.1 and HTTPS;
- POST submission;
- GET status;
- idempotency keys;
- conditional reads;
- SSE progress;
- one supported client;
- graceful shutdown.

Produce:

1. the route table;
2. state machines for jobs and idempotency records;
3. a capacity map;
4. one absolute-deadline algorithm;
5. the TLS identity policy;
6. replay-gap and slow-subscriber policy;
7. startup rollback and shutdown phases;
8. twelve tests that distinguish the design from common shortcuts.

Your design must remain process-local. State which guarantees would require Course 7 persistence or distributed coordination.
## Part VI — Causal incident diagnosis

For each incident, identify the responsible authority, the evidence needed before changing code, and the smallest contract-preserving repair.

21. Clients report intermittent `ECONNRESET` while health remains green. Explain why this observation is insufficient to blame the listener or the client, and name the connection and application evidence you need.
22. A retrying client creates two jobs after its first response is lost. Locate the missing semantic contract and explain why increasing the timeout is not a repair.
23. Memory grows only when one SSE consumer is connected over a slow link. Event history remains at its configured maximum. Identify the second retained structure that must be bounded.
24. HTTP/2 throughput falls as stream concurrency rises, but CPU remains low. Give three distinct flow-control or admission explanations that should be tested separately.
25. HTTPS works for `127.0.0.1` but fails for `service.local`. The CA is trusted. Explain the identity check that still fails and the correct certificate-side repair.
26. Shutdown completes quickly, but a client receives a truncated JSON response. Explain how process termination can succeed while product completion fails.
27. A UDP discovery client accepts a valid response from an old attempt. Explain the missing correlation or freshness rule.
28. A `307` redirect repeats a POST body, while a `303` changes the request to GET. Explain why redirect handling belongs to explicit client policy rather than a generic “follow redirects” switch.
29. Readiness remains true after job capacity is exhausted. Decide whether this is always wrong, always correct, or policy-dependent, and state the contract needed to decide.
30. A startup error occurs after HTTP/1.1 is listening but before HTTPS is ready. Describe the rollback evidence needed before the CLI may report startup failure and exit.

Complete the review by giving a ten-minute oral defense of ServiceWire. Draw its authorities, name every independent capacity, locate the semantic commit point for submission, and trace one accepted request from DNS resolution through final shutdown accounting.
