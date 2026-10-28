# Module 60 Workbook — Integrated Service Architecture

## 1. Predict

1. The listener is open, but job capacity is exhausted. Is the service ready?
2. Shutdown closes the listening socket. Can existing keep-alive clients submit more jobs?
3. A job succeeds after its submitting connection closed. Which terminal facts differ?
4. HTTP/2 sends GOAWAY. Are all streams joined?
5. The UDP discovery socket still advertises after readiness becomes false. What contract is violated?

## 2. Diagnose and repair

- Build a multidimensional capacity map.
- Separate health and readiness.
- Add startup rollback.
- Make quiescing visible to application admission.
- Replace sequential subsystem grace periods with one deadline.
- Reconcile request and job outcomes independently.
- Close SSE, HTTP/2, UDP, timers, and client agents.
- Build an authoritative terminal report.
- Add deterministic rendering.

## 3. Focused construction

1. Validate all configuration before bind.
2. Start required resources in order.
3. Roll back after injected failure at every step.
4. Expose health and readiness.
5. Reject overload before semantic commit.
6. Track active requests and jobs.
7. Quiesce listeners and application.
8. Drain under one deadline.
9. Abort and join leftovers.
10. Assert no active resources remain.

## 4. Independent laboratory

Build the [Network Service Audit](../../labs/module-60-network-service-audit/README.md).

## 5. ServiceWire completion

Complete ServiceWire and its supported client. Run all protocol, capacity, failure, and lifecycle tests.

## 6. Independent feature — conditional job cancellation

Add:

```text
POST /v1/jobs/:id/cancel
If-Match: "<current-etag>"
```

The feature must update:

- route grammar;
- validation;
- job state machine;
- revisions;
- ETags and preconditions;
- idempotency/repetition policy;
- HTTP/1.1;
- HTTP/2;
- SSE events;
- client;
- shutdown interaction;
- tests;
- documentation.

## 7. Closed-book defense

1. Name every admission layer.
2. Define health versus readiness.
3. Explain startup rollback.
4. Explain one shutdown deadline.
5. Reconcile request and job terminal states.
6. State every process-local limitation.

## 8. Whole-service incident simulation

Using the scenario in the chapter, produce a terminal accounting table for connections, HTTP/2 sessions, streams, jobs, subscribers, discovery socket, timers, and agents. Every accepted resource must end in a named terminal category.

Inject two cleanup failures after the original shutdown trigger. Define the returned error/report structure so the initiating cause remains primary while cleanup failures remain visible.

## 9. Final design defense

Present ServiceWire in ten minutes without naming Node APIs first. Begin with authorities, invariants, bounds, commit points, and lifecycle. Only then map those ideas to HTTP, TLS, HTTP/2, SSE, UDP, and the supported client. A presentation organized as an API inventory does not pass this exercise.

## 10. Release checklist

Write a pre-release checklist with at least one executable test for each of these claims: strict request bounds, idempotent replay, ETag behavior, TLS hostname verification, independent HTTP/2 stream failure, SSE replay gap, UDP correlation, overload rejection, startup rollback, and bounded shutdown. A statement such as “covered by integration tests” is insufficient; name the fixture and observable terminal evidence.
