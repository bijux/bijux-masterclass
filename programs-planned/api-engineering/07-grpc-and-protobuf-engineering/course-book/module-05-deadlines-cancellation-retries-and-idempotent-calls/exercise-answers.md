# Worked answers — Deadlines, Cancellation, Retries, and Idempotent Calls

These are reference answers, not scripts to memorize. Compare the decision rule and evidence, then revise your answer.

## 1. Why are three sequential five-second RPC timeouts not equivalent to one five-second user budget?

Each hop can consume its full timeout and retries can reset it, so the end-to-end journey exceeds the user budget. Child calls need the remaining absolute budget.

**Decisive evidence:** deadline timeline

## 2. Which clock should calculate remaining duration, and why?

Use a monotonic clock for elapsed and remaining time because wall clocks can jump. Wall time remains for interoperable timestamps.

**Decisive evidence:** monotonic clock test

## 3. What must a server do when its context is cancelled after commit?

It should stop nonessential work and return promptly, but preserve and expose the committed authoritative state. Cancellation cannot retroactively roll back it.

**Decisive evidence:** post-commit cancellation oracle

## 4. Differentiate transparent retry from configured retry.

Transparent retry is a narrowly inferred transport replay before application handling; configured retry is an explicit method/status policy. Both still require safe operation semantics.

**Decisive evidence:** retry capability report

## 5. Why is `UNAVAILABLE` alone insufficient permission to retry CreateRun?

The server may have committed before the transport failed. Retry is safe only with a bound request identifier, matching fingerprint, remaining deadline, and policy budget.

**Decisive evidence:** mutation retry policy

## 6. Which fields belong in an idempotency fingerprint?

Include normalized semantic request fields, method identity, and principal/tenant binding. Exclude volatile trace data and record identity separately when appropriate.

**Decisive evidence:** fingerprint vector

## 7. How should changed input under a reused request identifier behave?

Reject visibly as an idempotency conflict. Never replay the old response for a semantically different request.

**Decisive evidence:** idempotency conflict test

## 8. Why does jitter improve retry safety?

It desynchronizes clients, reducing correlated retry bursts and the chance that recovery is immediately overwhelmed.

**Decisive evidence:** retry-wave simulation

## 9. When is wait-for-ready appropriate, and what bound remains mandatory?

For bounded startup or brief connectivity recovery when the result remains valuable. An absolute deadline and admission/memory bound are still mandatory.

**Decisive evidence:** queued-call budget test

## 10. Differentiate an HTTP deadline, a worker lease, and event retention.

The HTTP deadline bounds one synchronous user journey; the lease authorizes one worker attempt; retention governs how long durable events remain available.

**Decisive evidence:** temporal identity table

## 11. How should a client reconcile a deadline exceeded after CancelRun?

Re-read authoritative run state and revision or query the persisted request outcome. Do not infer rollback from the transport status.

**Decisive evidence:** reconciliation trace

## 12. What cross-language timing property should be compared instead of exact sleep timestamps?

Compare the attempt decision, total maximum budget, backoff bounds, and final classification using an injected clock—not exact real-time scheduling.

**Decisive evidence:** shared retry vector
