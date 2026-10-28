# Worked Answers — Module 08: Abuse Resistance and Resource Budgets

Use these solutions to audit your reasoning for **Abuse Resistance and Resource Budgets**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is request count an incomplete cost metric?

A health read, multipart upload, long stream, and analysis submission consume different resources and durations.

**Capstone check.** Use the principal/tenant/operation cases in `capstone/shared/vectors/abuse.json`; one broad IP bucket cannot represent the policy.

The chapter’s decisive distinction is this: Inventory expensive resources per operation. Dataset upload consumes ingress bandwidth, staging space, checksum CPU, and storage. Analysis submission consumes a durable row, queue capacity, worker time, artifact space, and possible webhook retries. Event streaming consumes a connection and periodic work over time. Assign admission checks before the first expensive or irreversible effect.

## 2. What does burst capacity represent?

The maximum short-term accumulation allowed before sustained refill becomes the limiting factor.

**Capstone check.** Run the fixed-point token-bucket refill vector and assert deterministic behavior without floating-point drift.

In the cumulative capstone, the rule becomes concrete: Implement a deterministic fixed-point token bucket with injected monotonic clock, a context-managed concurrency permit, and a composite budget key. Keep the in-memory reference labeled single-process. Add an interface for a durable/distributed store without pretending the local map coordinates replicas.

## 3. Why use a monotonic clock?

Wall-clock jumps should not create or erase budget unexpectedly; elapsed time is the relevant measure.

**Capstone check.** Exhaust the analysis-submission budget while a cheap read remains available; cost classes must not collapse into one limit.

A useful way to reason about the boundary is: Retry responses must not synchronize clients into another burst. Retry-After should be truthful for the enforced budget; clients should still use jitter where policy permits. Use 429 for a caller budget and 503 for service-wide inability to admit valid work, with documented bodies and no false promise that retry is always safe.

## 4. Where should an upload permit be acquired?

Before body consumption or staging resources are allocated, after enough identity/context exists to select the budget.

**Capstone check.** Leak one concurrency permit in the planted mutant; the focused test must detect permanent capacity loss after cancellation.

The implementation consequence is: Concurrency permits protect scarce simultaneous resources. Acquire before opening the expensive dependency or reading the full upload. Release in a finally path on success, exception, cancellation, and client disconnect. A leaked permit is a slow availability incident; a permit acquired after work starts is not admission control.

## 5. What must happen on cancellation?

Release concurrency and partial resources exactly once, while durable work follows its own cancellation protocol.

**Capstone check.** Stream beyond the configured byte or duration budget and verify bounded termination without publishing a partial artifact.

The important nuance is: Use integer microtokens or bigint nanounits and an injected monotonic time source. Make permit release idempotent and safe in finally. Avoid timers as the authority; compute refill from stored timestamp. Test abort/cancellation and queue admission explicitly.

## 6. How do tenant and global budgets interact?

A request must pass both: tenant fairness cannot override total service capacity, and global capacity cannot permit one tenant to monopolize it.

**Capstone check.** Fill the queue/storage budget and assert truthful `429` or `503` behavior rather than accepting work the system cannot start.

Under concurrency or failure, the distinction becomes: The completion proof measures bounded behavior under bursts, low-and-slow streams, canceled uploads, repeated invalid credentials, noisy tenants, and failing webhook destinations. The service must degrade by rejecting new work before it corrupts accepted work.

## 7. Why is in-memory rate limiting not multi-instance proof?

Each process sees only its own counters, so aggregate allowance multiplies with replicas and restarts reset state.

**Capstone check.** Probe many object identifiers and compare status, body shape, timing class, and audit evidence for absent and concealed foreign resources.

The design remains honest only if: An in-process limiter protects one process. It does not enforce a tenant-wide budget across replicas. A database- or Redis-backed design introduces consistency, latency, partition, and fail-open/fail-closed choices. The course can prove local arithmetic and lifecycle while explicitly reserving distributed enforcement for a later performance/traffic course.

## 8. What should `Retry-After` avoid?

Unrealistically precise or identical advice that causes synchronized retries; combine policy with client-side jitter guidance.

**Capstone check.** Combine client retries with server retries in the amplification vector; one request must have a bounded total attempt budget.

The consumer-facing consequence is: A token bucket permits bounded bursts and refills over time. Use integer or fixed-point arithmetic so Python and JavaScript do not diverge at floating boundaries. Charge attempts that consume parsing or cryptographic work even when they fail. Define whether a rejected request consumes a token and test the boundary exactly.

## 9. How does enumeration resistance differ from authorization?

Authorization denies foreign data; enumeration controls volume and equalizes observable behavior to reduce discovery.

**Capstone check.** Verify `Retry-After` describes the actual limiter state and does not invite synchronized retry storms.

The operational consequence is: Enumeration resistance combines authorization-aware queries, concealment, bounded invalid attempts, and uniform response shape. It does not require making every response take exactly the same time, which is usually impractical; it requires removing deterministic high-signal differences and monitoring repeated probes.

## 10. Why charge rejected malicious input?

Parsing and validation consume resources; free failure paths can be abused.

**Capstone check.** Record whether the local limiter is single-process or distributed; do not claim cross-replica enforcement without shared state.

The strongest engineering interpretation is: Availability security requires explicit budgets for rate, concurrency, bytes, queue depth, storage, and stream lifetime. Controls must be keyed to the protected resource, cost-aware, deterministic under test, and honest about single-process versus distributed scope.

**Evidence.** Run the shared hostile-input corpus through raw edge parsing and both implementations, asserting rejection, bounded resource use, cleanup, and non-leaking problem responses.

## 11. Trace resource budgets and abuse admission in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/abuse.py` and `capstone/tracks/typescript-fastify/src/security/abuse.ts`. The required invariant is that cost is charged before expensive work and bounded by principal, tenant, operation, concurrency, storage, and time dimensions.

The defect-oriented view is: A token bucket permits bounded bursts and refills over time. Use integer or fixed-point arithmetic so Python and JavaScript do not diverge at floating boundaries. Charge attempts that consume parsing or cryptographic work even when they fail. Define whether a rejected request consumes a token and test the boundary exactly.

## 12. Compare resource budgets and abuse admission across Python and TypeScript

Both tracks must preserve this invariant: cost is charged before expensive work and bounded by principal, tenant, operation, concurrency, storage, and time dimensions. The intentional difference is that permit and clock implementations differ; no exception or disconnect may leak capacity.

Across the Python and TypeScript tracks, the invariant is: Concurrency permits protect scarce simultaneous resources. Acquire before opening the expensive dependency or reading the full upload. Release in a finally path on success, exception, cancellation, and client disconnect. A leaked permit is a slow availability incident; a permit acquired after work starts is not admission control.
