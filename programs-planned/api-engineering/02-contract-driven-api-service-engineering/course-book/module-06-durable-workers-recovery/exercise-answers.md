# Worked Answers — Module 06: Durable Workers and Recovery

Use these solutions to audit your reasoning for **Durable Workers and Recovery**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is 202 dishonest for an in-memory task?

The server has acknowledged future processing without durable evidence that any process can recover after failure.

The chapter’s decisive distinction is this: The API returns 202 only after run, initial event, durable job, and idempotency outcome are committed. Worker availability is irrelevant to acceptance; the status resource reveals queued progress until a worker claims it.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 2. What guarantee does `SKIP LOCKED` provide and not provide?

It lets concurrent claimers skip rows locked by others; it does not by itself update lease state, ensure ordering fairness, or fence stale workers.

In the cumulative capstone, the rule becomes concrete: A lease is time-bounded authority to execute a job. Heartbeats extend it while work is alive. Expiry makes abandoned work recoverable. Lease duration must exceed normal heartbeat jitter but remain bounded enough for recovery.

**Evidence.** Force competing requests against one database transaction boundary and inspect public responses, uniqueness/version rows, and rollback state after restart.

## 3. Why increment lease generation on reclaim?

Owner names can repeat and old processes may survive; a monotonically newer token makes old authority distinguishable.

A useful way to reason about the boundary is: Progress updates both the run event stream and lease liveness under the active generation. Heartbeats are not terminal commits and should be cheap. A stuck worker that cannot heartbeat eventually loses authority.

**Evidence.** Kill a worker after claim or partial work, expire the lease, start a replacement, and prove one final effect plus rejection of the stale generation.

## 4. Can exactly-once execution be guaranteed here?

The course does not claim it. Crash ambiguity permits repeated computation; idempotent/guarded effects provide one logical visible result.

The implementation consequence is: The system assumes job logic may execute repeatedly because of crash ambiguity. Effects use deterministic artifact content/identity and transactional guards. The goal is one logical result, not proof that CPU instructions ran once.

**Evidence.** Test the use case without the framework, then through the transport and durable adapter, including one restart or failure path.

## 5. Why process outside the claim transaction?

Long analysis would hold locks/connections and increase contention. The lease represents authority while short transactions record progress and completion.

The important nuance is: Transient infrastructure failures may requeue with bounded exponential delay. Permanent input or analysis failures terminate the run. Poison jobs stop after a maximum attempt count and record a stable failure rather than spinning forever.

**Evidence.** Force competing requests against one database transaction boundary and inspect public responses, uniqueness/version rows, and rollback state after restart.

## 6. How should cancellation race with completion?

Whichever guarded terminal transaction first observes valid authority and current state commits the deterministic outcome; the other receives no authority/conflict.

Under concurrency or failure, the distinction becomes: The excerpt for Durable Workers and Recovery isolates one mechanism from the full service. Before copying it, locate the decision or transaction boundary, state the assumption it makes, trace cleanup on failure, and name the regression that would expose moving the guard elsewhere.

## 7. What makes a retryable job error?

A condition expected to succeed later without changing the request, such as temporary storage unavailability. Invalid content or unsupported algorithm is permanent.

The design remains honest only if: with self. source path(job).open("rb") as stream: while block := stream.read(READ CHUNK SIZE): digest.update(block) size += len(block) lines += block.count(b"\n") last byte = block[-1:] chunks += 1 if chunks % 8 == 0: self.repository.renew job lease( job, self.settings.worker lease seconds, )

## 8. Why can a heartbeat not prove useful progress?

It proves liveness of the worker loop, not that computation advances. Progress and timeout policy remain separate.

The consumer-facing consequence is: Progress updates both the run event stream and lease liveness under the active generation. Heartbeats are not terminal commits and should be cheap. A stuck worker that cannot heartbeat eventually loses authority.

**Counterexample.** A crashed or stale worker can still publish an effect after another worker has legitimately taken ownership.

**Evidence.** Kill a worker after claim or partial work, expire the lease, start a replacement, and prove one final effect plus rejection of the stale generation.

## 9. What is a poison job?

A job that repeatedly fails deterministically or cannot complete. Attempt caps and terminal failure prevent infinite resource consumption.

The operational consequence is: For Durable Workers and Recovery , record the inherited API behavior, the new durable rule, one rejected alternative, the first counterexample, and the exact application, adapter, migration, or proof artifact that owns the choice.

**Evidence.** Kill a worker after claim or partial work, expire the lease, start a replacement, and prove one final effect plus rejection of the stale generation.

## 10. How can duplicate artifact publication converge?

Use deterministic content checksum/path, atomic publication, unique metadata identity, and guarded run completion so repeats observe existing result.

The strongest engineering interpretation is: The Durable Workers and Recovery increment must preserve the frozen API and every earlier durability invariant while delivering this result: Add durable jobs, leases, heartbeats, fencing, cancellation, duplicate-safe effects, and abandoned-work recovery The comparison track must expose the same public outcomes even when internal libraries and control flow differ.

## 11. Trace durable job leasing and fencing in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/analysis_service/worker.py` and `capstone/tracks/typescript-fastify/src/worker.ts`. The required invariant is that a lease generation prevents an expired worker from committing effects after another worker takes ownership.

The defect-oriented view is: with self. source path(job).open("rb") as stream: while block := stream.read(READ CHUNK SIZE): digest.update(block) size += len(block) lines += block.count(b"\n") last byte = block[-1:] chunks += 1 if chunks % 8 == 0: self.repository.renew job lease( job, self.settings.worker lease seconds, )

## 12. Compare durable job leasing and fencing across Python and TypeScript

Both tracks must preserve this invariant: a lease generation prevents an expired worker from committing effects after another worker takes ownership. The intentional difference is that worker loops and cancellation primitives differ, but claim, renew, recover, and complete transitions must match.

Across the Python and TypeScript tracks, the invariant is: Claim Required evidence ---: --- --- 1 accepted without worker durable Write the narrow command and machine-readable oracle. 2 workers claim distinct jobs Write the narrow command and machine-readable oracle. 3 killed lease recovered Write the narrow command and machine-readable oracle. 4 generation increments Write the narrow command and machine-readable oracle. 5 stale worker fenced Write the narrow command and machine-readable oracle.
