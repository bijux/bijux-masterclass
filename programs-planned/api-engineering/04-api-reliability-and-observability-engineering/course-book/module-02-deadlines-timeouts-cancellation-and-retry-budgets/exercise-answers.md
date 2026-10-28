# Worked Answers — Module 02: Deadlines, Cancellation, and Retry Budgets

Use these solutions to audit your reasoning for **Deadlines, Cancellation, and Retry Budgets**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is a deadline stronger than a timeout?

A deadline bounds the whole operation with one absolute expiry; a timeout often bounds only one wait and can be reset by nested layers.

The chapter’s decisive distinction is this: Apply Absolute deadline, Timeout scope, Cancellation to this module’s capstone increment: Add absolute deadlines, child budgets, safe retry classification, Retry-After handling, cancellation observation, and one retry owner per dependency. State one misleading green signal and the durable observation that would overrule it.

## 2. May a child deadline equal the parent?

Yes when local maximum does not require a smaller expiry, but it may never exceed the parent and often should reserve cleanup time.

In the cumulative capstone, the rule becomes concrete: Begin with the failure Timeout multiplication . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Create a five-second absolute ingress deadline. Each child gets the lesser of remaining time and dependency maximum, with time reserved for cleanup and response. , and rerun the focused regression in both languages.

## 3. When is POST retryable?

When the effect is inherently idempotent or protected by a durable idempotency key bound to the request and replay result.

A useful way to reason about the boundary is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=02 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 4. What does a transport timeout prove about the server effect?

Nothing definitive: the request may not have arrived, may be running, may have committed, or may have completed with a lost response.

The implementation consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=02 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

## 5. How should Retry-After interact with a deadline?

Use it as a minimum delay only for an otherwise retryable operation and only if delay plus another meaningful attempt fits.

**Common mistake.** Describing a procedure for “How should Retry-After interact with a deadline?” without a falsifiable completion condition.

The important nuance is: Apply Absolute deadline, Timeout scope, Cancellation to this module’s capstone increment: Add absolute deadlines, child budgets, safe retry classification, Retry-After handling, cancellation observation, and one retry owner per dependency. State one misleading green signal and the durable observation that would overrule it.

## 6. Why may jitter sequences differ across languages?

The invariant is bounded randomized distribution, not identical pseudo-random bytes. Seeds are language-local test aids.

Under concurrency or failure, the distinction becomes: Begin with the failure Timeout multiplication . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Create a five-second absolute ingress deadline. Each child gets the lesser of remaining time and dependency maximum, with time reserved for cleanup and response. , and rerun the focused regression in both languages.

## 7. Where should automatic retry live?

At one named layer understanding dependency semantics and effect safety; other layers do not add hidden loops.

The design remains honest only if: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=02 TRACK=python and explain why the same public and durable outcome holds in the other language.

**Evidence.** Inject delay and ambiguity at each dependency while asserting one absolute budget, bounded attempts, cancellation propagation, and no effect after expiry.

## 8. Should disconnect cancel a committed run?

No. Durable accepted work follows domain cancellation, not TCP connection lifetime.

**Common mistake.** Giving an unconditional answer to “Should disconnect cancel a committed run?” without classifying responsibility and failure semantics.

The consumer-facing consequence is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=02 TRACK=typescript and explain why the same public and durable outcome holds in the other language.

## 9. Which status codes are always retryable?

None without context. Even 503 is unsafe for a mutation without idempotency.

The operational consequence is: Apply Absolute deadline, Timeout scope, Cancellation to this module’s capstone increment: Add absolute deadlines, child budgets, safe retry classification, Retry-After handling, cancellation observation, and one retry owner per dependency. State one misleading green signal and the durable observation that would overrule it.

**Evidence.** Inject delay and ambiguity at each dependency while asserting one absolute budget, bounded attempts, cancellation propagation, and no effect after expiry.

## 10. Why reserve minimum attempt time?

Otherwise the service can sleep until expiry and start a call that cannot finish, adding load without chance of success.

The strongest engineering interpretation is: Begin with the failure Timeout multiplication . A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design Create a five-second absolute ingress deadline. Each child gets the lesser of remaining time and dependency maximum, with time reserved for cleanup and response. , and rerun the focused regression in both languages.

## 11. Trace absolute deadline propagation in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/deadline.py` and `capstone/tracks/typescript-fastify/src/reliability/deadline.ts`. The required invariant is that one caller budget is partitioned across attempts and dependencies without resetting at each layer or retrying unsafe effects.

The defect-oriented view is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=02 TRACK=python and explain why the same public and durable outcome holds in the other language.

## 12. Compare absolute deadline propagation across Python and TypeScript

Both tracks must preserve this invariant: one caller budget is partitioned across attempts and dependencies without resetting at each layer or retrying unsafe effects. The intentional difference is that clock and cancellation APIs differ; remaining time and retry eligibility must match.

Across the Python and TypeScript tracks, the invariant is: Review procedure. Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun make module-proof MODULE=02 TRACK=typescript and explain why the same public and durable outcome holds in the other language.
