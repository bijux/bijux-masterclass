# Worked Answers — Module 05: Deadlines, Cancellation, Retries, and Idempotent Calls

Use these solutions to audit your reasoning for **Deadlines, Cancellation, Retries, and Idempotent Calls**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why are three sequential five-second RPC timeouts not equivalent to one five-second user budget?

Each hop can consume its full timeout and retries can reset it, so the end-to-end journey exceeds the user budget. Child calls need the remaining absolute budget.

**Decisive evidence:** deadline timeline

The chapter’s decisive distinction is this: A timeout attached independently to every hop is not a budget. If an edge request has five seconds and it calls three services with five-second timeouts, the user-visible journey can consume much more than five seconds, especially with retries. Start with one absolute deadline at the caller that knows when the result loses value. Propagate the remaining duration to each child call after reserving time for local work and response translation.

## 2. Which clock should calculate remaining duration, and why?

Use a monotonic clock for elapsed and remaining time because wall clocks can jump. Wall time remains for interoperable timestamps.

**Decisive evidence:** monotonic clock test

In the cumulative capstone, the rule becomes concrete: A deadline is a point in time; a timeout is a relative duration. Relative values are vulnerable to queue delay and repeated resetting. The client adapter computes remaining = deadline - monotonic now, rejects work when the budget is exhausted, and applies a bounded child allowance. Servers inspect the deadline and stop optional work when the result can no longer arrive usefully.

## 3. What must a server do when its context is cancelled after commit?

It should stop nonessential work and return promptly, but preserve and expose the committed authoritative state. Cancellation cannot retroactively roll back it.

**Decisive evidence:** post-commit cancellation oracle

A useful way to reason about the boundary is: Cancellation tests inject the signal before handler entry, during validation, during a dependency call, before commit, after commit, and during response serialization. The oracle is durable state plus final transport outcome, not the exception observed by the caller.

## 4. Differentiate transparent retry from configured retry.

Transparent retry is a narrowly inferred transport replay before application handling; configured retry is an explicit method/status policy. Both still require safe operation semantics.

**Decisive evidence:** retry capability report

The implementation consequence is: The course declares retry behavior by fully qualified method. Read-only GetRun can retry selected transient failures within the deadline. CreateRun can retry only with a persistent request identifier bound to the semantic input. CancelRun likewise requires idempotency and version semantics. Streaming methods have different reconnection and resume rules; unary retry configuration does not apply automatically.

## 5. Why is `UNAVAILABLE` alone insufficient permission to retry CreateRun?

The server may have committed before the transport failed. Retry is safe only with a bound request identifier, matching fingerprint, remaining deadline, and policy budget.

**Decisive evidence:** mutation retry policy

The important nuance is: After a deadline or connection failure, the client asks two questions: could the server have committed, and is the operation idempotently identifiable? For CreateRun, retry with the same request identifier or query the idempotency outcome. For CancelRun, re-read the run and compare state/revision. For a pure query, a retry is sufficient if the result is still useful.

## 6. Which fields belong in an idempotency fingerprint?

Include normalized semantic request fields, method identity, and principal/tenant binding. Exclude volatile trace data and record identity separately when appropriate.

**Decisive evidence:** fingerprint vector

Under concurrency or failure, the distinction becomes: The fingerprint includes semantic request fields after normalization, not volatile metadata such as trace identifiers. It excludes server-derived identity only if the identity is stored separately in the binding. The persisted outcome includes status, response bytes or canonical fields, and selected safe trailing metadata needed for equivalent replay.

## 7. How should changed input under a reused request identifier behave?

Reject visibly as an idempotency conflict. Never replay the old response for a semantically different request.

**Decisive evidence:** idempotency conflict test

The design remains honest only if: An in-memory deduplication map does not survive process restart and cannot coordinate replicas. The service stores request identifier, principal or tenant scope, method identity, canonical request fingerprint, state, and replayable outcome in the same authoritative database boundary as the command effect. Competing identical calls converge on one record. Changed input under the same identifier fails visibly.

## 8. Why does jitter improve retry safety?

It desynchronizes clients, reducing correlated retry bursts and the chance that recovery is immediately overwhelmed.

**Decisive evidence:** retry-wave simulation

The consumer-facing consequence is: A retry budget limits retries relative to useful requests or a fixed capacity. It prevents one failing method from consuming all traffic capacity. Retry throttling may suppress attempts when recent success is too low. Client and server metrics distinguish original calls from attempts.

**Evidence.** Run live calls with expiring deadlines, cancellation, ambiguous transport failure, retry classification, and durable idempotency evidence.

## 9. When is wait-for-ready appropriate, and what bound remains mandatory?

For bounded startup or brief connectivity recovery when the result remains valuable. An absolute deadline and admission/memory bound are still mandatory.

**Decisive evidence:** queued-call budget test

The operational consequence is: Fail-fast behavior returns when no ready channel is available; wait-for-ready may queue the call until connectivity recovers. It is useful for startup races and brief control-plane reconnection, but every waiting call still needs a deadline and admission bound. Unbounded wait-for-ready converts an unavailable service into growing client memory and delayed overload.

## 10. Differentiate an HTTP deadline, a worker lease, and event retention.

The HTTP deadline bounds one synchronous user journey; the lease authorizes one worker attempt; retention governs how long durable events remain available.

**Decisive evidence:** temporal identity table

The strongest engineering interpretation is: The design review also distinguishes other clocks. A worker lease can extend beyond the original HTTP deadline because the accepted run became durable. Event retention lasts much longer and is unrelated to user patience. A WatchRun idle timeout governs a stream connection, not run execution. Naming these clocks prevents accidental propagation of a dead request deadline into independently owned asynchronous work.

## 11. How should a client reconcile a deadline exceeded after CancelRun?

Re-read authoritative run state and revision or query the persisted request outcome. Do not infer rollback from the transport status.

**Decisive evidence:** reconciliation trace

The defect-oriented view is: Do not infer non-commit from CANCELLED, DEADLINE EXCEEDED, or UNAVAILABLE. Status describes the call observation, not necessarily authoritative state. Rich error details may indicate a precondition or known rejection, but absence of success is not proof of absence of effect.

**Evidence.** Run live calls with expiring deadlines, cancellation, ambiguous transport failure, retry classification, and durable idempotency evidence.

## 12. What cross-language timing property should be compared instead of exact sleep timestamps?

Compare the attempt decision, total maximum budget, backoff bounds, and final classification using an injected clock—not exact real-time scheduling.

**Decisive evidence:** shared retry vector

Across the Python and TypeScript tracks, the invariant is: Shared vectors describe absolute deadline, attempt durations, status sequence, backoff parameters, request safety, and expected final decision. Python and TypeScript must agree on whether another attempt is allowed and on maximum possible elapsed budget. Their internal timers and exception types may differ.
