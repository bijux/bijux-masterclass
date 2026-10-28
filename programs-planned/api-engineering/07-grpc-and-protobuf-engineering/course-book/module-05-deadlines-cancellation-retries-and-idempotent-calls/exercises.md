# Exercises — Module 05: Deadlines, Cancellation, Retries, and Idempotent Calls

Work through all twelve problems before opening the answers. In **Deadlines, Cancellation, Retries, and Idempotent Calls**, every response must settle this question: **How can callers bound remote work and recover from transient failure without multiplying timeouts or duplicating durable effects?** A useful solution connects semantics to mechanism: who owns the decision, what can go wrong, and which retained artifact proves the claimed outcome.

## 1. Why are three sequential five-second RPC timeouts not equivalent to one five-second user budget?

Write a concise engineering answer and name the decisive proof.

## 2. Which clock should calculate remaining duration, and why?

Write a concise engineering answer and name the decisive proof.

## 3. What must a server do when its context is cancelled after commit?

Write a concise engineering answer and name the decisive proof.

## 4. Differentiate transparent retry from configured retry.

Write a concise engineering answer and name the decisive proof.

## 5. Why is `UNAVAILABLE` alone insufficient permission to retry CreateRun?

Write a concise engineering answer and name the decisive proof.

## 6. Which fields belong in an idempotency fingerprint?

Write a concise engineering answer and name the decisive proof.

## 7. How should changed input under a reused request identifier behave?

Write a concise engineering answer and name the decisive proof.

## 8. Why does jitter improve retry safety?

Write a concise engineering answer and name the decisive proof.

## 9. When is wait-for-ready appropriate, and what bound remains mandatory?

Write a concise engineering answer and name the decisive proof.

## 10. Differentiate an HTTP deadline, a worker lease, and event retention.

Write a concise engineering answer and name the decisive proof.

## 11. How should a client reconcile a deadline exceeded after CancelRun?

Write a concise engineering answer and name the decisive proof.

## 12. What cross-language timing property should be compared instead of exact sleep timestamps?

Write a concise engineering answer and name the decisive proof.
