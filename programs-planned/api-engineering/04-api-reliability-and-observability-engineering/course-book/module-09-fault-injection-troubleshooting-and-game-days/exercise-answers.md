# Reference Answers — Module 09: Fault Injection, Troubleshooting, and Game Days

Read after attempting all twelve Fault Injection, Troubleshooting, and Game Days exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. What makes a fault experiment scientific enough for this course?

**Answer.** A prewritten falsifiable hypothesis, controlled fault, baseline, bounded scope, authoritative oracle, stop condition, cleanup, and repeatable evidence.

## 2. Why test latency separately from failure?

**Answer.** They exercise different timeout, pool, cancellation, retry, and circuit paths. Immediate failure cannot reveal blocked-resource behavior.

## 3. What is a safe blast radius?

**Answer.** The minimum synthetic tenant/operation/dependency/duration/concurrency needed to test the claim without affecting real data or unrelated journeys.

## 4. When should an experiment abort?

**Answer.** When integrity, resource, security, or unrelated-journey thresholds are exceeded or the fault cannot be controlled/observed.

## 5. Why use an unaffected journey as a control?

**Answer.** It tests isolation and helps distinguish system-wide ambient change from the injected fault.

## 6. What is the first troubleshooting question?

**Answer.** Which critical journey is failing and what public/durable evidence defines the failure?

## 7. Should operators trust the first correlated metric?

**Answer.** No. Correlation guides hypotheses; durable state, controlled reproduction, and counterfactual evidence test mechanism.

**Common mistake.** Giving an unconditional answer to “Should operators trust the first correlated metric?” without classifying responsibility and failure semantics.

## 8. What cleanup evidence is required after a worker-kill test?

**Answer.** No active fault, expired/recovered leases resolved, no stale worker commit, no duplicate terminal effect, and bounded queue/permits.

## 9. How should a discovered failure be retained?

**Answer.** As the smallest deterministic regression test/vector plus updated requirement, alert, dashboard, or runbook where appropriate.

**Common mistake.** Describing a procedure for “How should a discovered failure be retained?” without a falsifiable completion condition.

## 10. When are compound faults appropriate?

**Answer.** After single-fault paths are understood and the interaction itself is a named risk with tighter stop conditions.

## 11. Trace bounded fault injection and diagnosis in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_reliability/faults.py` and `capstone/tracks/typescript-fastify/src/reliability/faults.ts`. The required invariant is that faults have hypotheses, blast-radius guards, abort conditions, cleanup, and an oracle that distinguishes the intended failure.

## 12. Compare bounded fault injection and diagnosis across Python and TypeScript

Both tracks must preserve this invariant: faults have hypotheses, blast-radius guards, abort conditions, cleanup, and an oracle that distinguishes the intended failure. The intentional difference is that injection hooks differ; seed, target, fault decision, and cleanup evidence are shared.
