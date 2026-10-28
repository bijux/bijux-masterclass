# Reference Answers — Module 06: Durable Workers and Recovery

Read after attempting all twelve Durable Workers and Recovery exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is 202 dishonest for an in-memory task?

The server has acknowledged future processing without durable evidence that any process can recover after failure.

## 2. What guarantee does `SKIP LOCKED` provide and not provide?

It lets concurrent claimers skip rows locked by others; it does not by itself update lease state, ensure ordering fairness, or fence stale workers.

## 3. Why increment lease generation on reclaim?

Owner names can repeat and old processes may survive; a monotonically newer token makes old authority distinguishable.

## 4. Can exactly-once execution be guaranteed here?

The course does not claim it. Crash ambiguity permits repeated computation; idempotent/guarded effects provide one logical visible result.

## 5. Why process outside the claim transaction?

Long analysis would hold locks/connections and increase contention. The lease represents authority while short transactions record progress and completion.

## 6. How should cancellation race with completion?

Whichever guarded terminal transaction first observes valid authority and current state commits the deterministic outcome; the other receives no authority/conflict.

## 7. What makes a retryable job error?

A condition expected to succeed later without changing the request, such as temporary storage unavailability. Invalid content or unsupported algorithm is permanent.

## 8. Why can a heartbeat not prove useful progress?

It proves liveness of the worker loop, not that computation advances. Progress and timeout policy remain separate.

## 9. What is a poison job?

A job that repeatedly fails deterministically or cannot complete. Attempt caps and terminal failure prevent infinite resource consumption.

## 10. How can duplicate artifact publication converge?

Use deterministic content checksum/path, atomic publication, unique metadata identity, and guarded run completion so repeats observe existing result.

## 11. Trace durable job leasing and fencing in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/worker.py` and `capstone/tracks/typescript-fastify/src/worker.ts`. The required invariant is that a lease generation prevents an expired worker from committing effects after another worker takes ownership.

## 12. Compare durable job leasing and fencing across Python and TypeScript

Both tracks must preserve this invariant: a lease generation prevents an expired worker from committing effects after another worker takes ownership. The intentional difference is that worker loops and cancellation primitives differ, but claim, renew, recover, and complete transitions must match.
