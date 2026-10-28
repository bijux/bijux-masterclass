# Module 07 lab — Build an authorization-safe cache and trigger a stampede

## Objective

Cache versioned project metadata, reproduce unsafe cross-tenant reuse and miss amplification, then prove key completeness, durable freshness, and bounded fills.

## Setup conditions

- project metadata baseline and authorization vectors pass
- two tenants have overlapping-looking resource identifiers
- origin call counter and delay injection are enabled
- cache starts empty with an injected clock

## Failure action and investigation


1. Demonstrate the planted resource-ID-only key leak.
2. Replace it with the complete authorized/versioned key.
3. Run 100 concurrent requests for one expired hot key without single-flight.
4. Enable bounded single-flight and repeat.
5. Commit a project update and simulate crash before cleanup.
6. Prove the new version uses a new key.
7. Inject origin timeout and ensure it is not cached as not-found.
8. Exhaust cache capacity and inspect deterministic eviction.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **Which data is safe to cache, for whom, for how long, and who owns invalidation after mutation or failure?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics. A passing command without this causal explanation is insufficient.

## Operational oracle

- cross-tenant value is never reused
- 100 concurrent misses produce one bounded origin fill per key
- failed fill leaves no poisoned entry
- post-commit version change makes old entry unreachable
- negative cache stores only authoritative absence
- entries and bytes remain within capacity

## Required evidence

Create:

```text
work/module-07/
├── cache-catalog.yaml
├── unsafe-key.json
├── safe-key.json
├── stampede-before.json
├── stampede-after.json
├── invalidation-crash.json
├── failure-policy.json
└── decision.md
```

Report both hit-path latency and origin load. State which consistency guarantees come from versioned keys and which cleanup depends on invalidation.

## Cleanup and reset

Advance/reset the injected clock, clear the local cache and in-flight registry, disable origin delay, and verify all waiters settled.

## Completion gate

- [ ] cache catalogue is complete
- [ ] cross-tenant planted defect is rejected
- [ ] single-flight bounds origin calls
- [ ] versioned invalidation survives crash
- [ ] error is not cached as absence
- [ ] cache capacity is bounded and observable

The lab is incomplete when the candidate is merely faster. It must preserve the inherited correctness oracle and explain the observed resource change.
