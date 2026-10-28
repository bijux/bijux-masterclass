# Reference Answers — Module 08: Abuse Resistance and Resource Budgets

Read after attempting all twelve Abuse Resistance and Resource Budgets exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is request count an incomplete cost metric?

**Answer.** A health read, multipart upload, long stream, and analysis submission consume different resources and durations.

**Capstone check.** Use the principal/tenant/operation cases in `capstone/shared/vectors/abuse.json`; one broad IP bucket cannot represent the policy.

## 2. What does burst capacity represent?

**Answer.** The maximum short-term accumulation allowed before sustained refill becomes the limiting factor.

**Capstone check.** Run the fixed-point token-bucket refill vector and assert deterministic behavior without floating-point drift.

## 3. Why use a monotonic clock?

**Answer.** Wall-clock jumps should not create or erase budget unexpectedly; elapsed time is the relevant measure.

**Capstone check.** Exhaust the analysis-submission budget while a cheap read remains available; cost classes must not collapse into one limit.

## 4. Where should an upload permit be acquired?

**Answer.** Before body consumption or staging resources are allocated, after enough identity/context exists to select the budget.

**Capstone check.** Leak one concurrency permit in the planted mutant; the focused test must detect permanent capacity loss after cancellation.

## 5. What must happen on cancellation?

**Answer.** Release concurrency and partial resources exactly once, while durable work follows its own cancellation protocol.

**Capstone check.** Stream beyond the configured byte or duration budget and verify bounded termination without publishing a partial artifact.

## 6. How do tenant and global budgets interact?

**Answer.** A request must pass both: tenant fairness cannot override total service capacity, and global capacity cannot permit one tenant to monopolize it.

**Capstone check.** Fill the queue/storage budget and assert truthful `429` or `503` behavior rather than accepting work the system cannot start.

## 7. Why is in-memory rate limiting not multi-instance proof?

**Answer.** Each process sees only its own counters, so aggregate allowance multiplies with replicas and restarts reset state.

**Capstone check.** Probe many object identifiers and compare status, body shape, timing class, and audit evidence for absent and concealed foreign resources.

## 8. What should `Retry-After` avoid?

**Answer.** Unrealistically precise or identical advice that causes synchronized retries; combine policy with client-side jitter guidance.

**Capstone check.** Combine client retries with server retries in the amplification vector; one request must have a bounded total attempt budget.

## 9. How does enumeration resistance differ from authorization?

**Answer.** Authorization denies foreign data; enumeration controls volume and equalizes observable behavior to reduce discovery.

**Capstone check.** Verify `Retry-After` describes the actual limiter state and does not invite synchronized retry storms.

## 10. Why charge rejected malicious input?

**Answer.** Parsing and validation consume resources; free failure paths can be abused.

**Capstone check.** Record whether the local limiter is single-process or distributed; do not claim cross-replica enforcement without shared state.

## 11. Trace resource budgets and abuse admission in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/abuse.py` and `capstone/tracks/typescript-fastify/src/security/abuse.ts`. The required invariant is that cost is charged before expensive work and bounded by principal, tenant, operation, concurrency, storage, and time dimensions.

## 12. Compare resource budgets and abuse admission across Python and TypeScript

Both tracks must preserve this invariant: cost is charged before expensive work and bounded by principal, tenant, operation, concurrency, storage, and time dimensions. The intentional difference is that permit and clock implementations differ; no exception or disconnect may leak capacity.
