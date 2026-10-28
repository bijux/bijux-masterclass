# Reasoned Solutions — Module 80: Integrated Async Service Architecture, Testing, and Audit

[Return to the workbook](workbook.md) · [Return to the chapter](index.md) · [Open the JobWire guide](../capstone.md)

The governing correction is that service correctness lives at mechanism boundaries. An inventory of APIs is not an architecture; the architecture is the set of authorities, transitions, bounds, deadlines, commit points, failure scopes, and terminal lifecycles.

## Part 1 — Prediction solutions

1. Per-connection pending work and response state are unbounded despite the connection limit.
2. Memory and semantic retention are unbounded; eviction and retry-window policy are missing.
3. Cancellation intent is broadcast, but completion, panic observation, and cleanup are not proved.
4. Retries become new semantic operations and may duplicate committed work.
5. Health confuses HTTP liveness with broker readiness.
6. A second untrusted-byte boundary remains unbounded.
7. The codec may still lose or delay frames when several arrive together. Chunk invariance requires both fragmentation and coalescing.
8. Identical retries can reach different authorities and execute more than once. Shared or routed idempotency authority is required.

## Part 2 — Repair reasoning

Prioritize unbounded growth, semantic duplication, and incomplete shutdown first because they threaten service survival and correctness. Bound result retention and request topology; establish one commit/idempotency authority; stop holding the mutex through network output; propagate one deadline; separate health from saturated work; classify retry; then own and join the task tree. Additional tasks or locks without authority and capacity analysis would worsen the design.

## Part 3 — Focused exercise guidance

The nine ledgers should agree. If the task tree says the broker owns jobs but the cancellation ledger assumes connections abort them directly, the architecture conflicts. Resource estimates must list exclusions. Compatibility review should classify behavior visible to clients, not only types visible in source.

The strongest intersection tests assert exact terminal states: one commit, one cached result, permit count restored, task set empty, and protocol connection closed or preserved according to policy.

## Part 4 — Laboratory comparison

A strong independent audit product is smaller than JobWire but equally explicit. It proves that the reasoning transfers. It does not copy JobWire names or rely on the capstone’s broker implementation. Failure injection should target after-frame/before-parse, after-commit/before-reply, and shutdown-during-active-work or equivalent intersections.

## Part 5 — Capstone comparison

The finished capstone should have one responsibility per mechanism. The custom TCP protocol handles job interaction; Hyper handles operational reads; the broker owns commits; connection tasks own wire state; the supervisor owns lifecycle. Remove decorative abstractions and leave documented non-guarantees.

## Part 6 — Reconstruction and defense

A complete defense can answer each question with an owner, transition, bound, and test. It states that process-local idempotency is the first scaling assumption to fail under replicas, followed by instance-local health and capacity accounting. It also explains when a synchronous daemon is the more honest design.
