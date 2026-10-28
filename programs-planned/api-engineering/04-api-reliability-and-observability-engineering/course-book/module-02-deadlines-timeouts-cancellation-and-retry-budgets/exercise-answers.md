# Reference Answers — Module 02: Deadlines, Cancellation, and Retry Budgets

Read after attempting all twelve Deadlines, Cancellation, and Retry Budgets exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is a deadline stronger than a timeout?

**Answer.** A deadline bounds the whole operation with one absolute expiry; a timeout often bounds only one wait and can be reset by nested layers.

## 2. May a child deadline equal the parent?

**Answer.** Yes when local maximum does not require a smaller expiry, but it may never exceed the parent and often should reserve cleanup time.

## 3. When is POST retryable?

**Answer.** When the effect is inherently idempotent or protected by a durable idempotency key bound to the request and replay result.

## 4. What does a transport timeout prove about the server effect?

**Answer.** Nothing definitive: the request may not have arrived, may be running, may have committed, or may have completed with a lost response.

## 5. How should Retry-After interact with a deadline?

**Answer.** Use it as a minimum delay only for an otherwise retryable operation and only if delay plus another meaningful attempt fits.

**Common mistake.** Describing a procedure for “How should Retry-After interact with a deadline?” without a falsifiable completion condition.

## 6. Why may jitter sequences differ across languages?

**Answer.** The invariant is bounded randomized distribution, not identical pseudo-random bytes. Seeds are language-local test aids.

## 7. Where should automatic retry live?

**Answer.** At one named layer understanding dependency semantics and effect safety; other layers do not add hidden loops.

## 8. Should disconnect cancel a committed run?

**Answer.** No. Durable accepted work follows domain cancellation, not TCP connection lifetime.

**Common mistake.** Giving an unconditional answer to “Should disconnect cancel a committed run?” without classifying responsibility and failure semantics.

## 9. Which status codes are always retryable?

**Answer.** None without context. Even 503 is unsafe for a mutation without idempotency.

## 10. Why reserve minimum attempt time?

**Answer.** Otherwise the service can sleep until expiry and start a call that cannot finish, adding load without chance of success.

## 11. Trace absolute deadline propagation in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/deadline.py` and `capstone/tracks/typescript-fastify/src/reliability/deadline.ts`. The required invariant is that one caller budget is partitioned across attempts and dependencies without resetting at each layer or retrying unsafe effects.

## 12. Compare absolute deadline propagation across Python and TypeScript

Both tracks must preserve this invariant: one caller budget is partitioned across attempts and dependencies without resetting at each layer or retrying unsafe effects. The intentional difference is that clock and cancellation APIs differ; remaining time and retry eligibility must match.
