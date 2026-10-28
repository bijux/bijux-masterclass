# Lab — Module 07 lab — Build an authorization-safe cache and trigger a stampede

> **Module 07:** Caching, Freshness, and Invalidation

## Objective

Cache versioned project metadata, reproduce unsafe cross-tenant reuse and miss amplification, then prove key completeness, durable freshness, and bounded fills.

## Why this lab matters

This lab turns the module’s governing question—**Which data is safe to cache, for whom, for how long, and who owns invalidation after mutation or failure?**—into a falsifiable experiment. immutable content-addressed artifact metadata — key includes checksum/version; long reuse possible; versioned project metadata — key includes owner and version/ETag; old entries become unreachable after version change; mutable authorization decisions — generally short-lived or uncached because roles/revocation change; list/query results — high invalidation complexity and key cardinality; cache only with strong evidence; negative lookups — can reduce repeated.

It advances the cumulative Analysis Runs Platform by requiring this result: **Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

- project metadata baseline and authorization vectors pass
- two tenants have overlapping-looking resource identifiers
- origin call counter and delay injection are enabled
- cache starts empty with an injected clock

## Hypothesis

The clean implementation should satisfy this claim: **cross-tenant value is never reused; 100 concurrent misses produce one bounded origin fill per key; failed fill leaves no poisoned entry; post-commit version change makes old entry unreachable; negative cache stores only authoritative absence; entries and bytes remain within capacity.** When the lab introduces this fault—**Inject origin timeout and ensure it is not cached as not-found**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Demonstrate the planted resource-ID-only key leak.
2. Replace it with the complete authorized/versioned key.
3. Run 100 concurrent requests for one expired hot key without single-flight.
4. Enable bounded single-flight and repeat.
5. Commit a project update and simulate crash before cleanup.
6. Prove the new version uses a new key.
7. Inject origin timeout and ensure it is not cached as not-found.
8. Exhaust cache capacity and inspect deterministic eviction.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Inject origin timeout and ensure it is not cached as not-found**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Cache versioned project metadata, reproduce unsafe cross-tenant reuse and miss amplification, then prove key completeness, durable freshness, and bounded fills**, and identify one attractive implementation that would pass the happy path while failing the oracle.

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

## Interpretation and defense

1. Which state or effect is authoritative for **Caching, Freshness, and Invalidation**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Inject origin timeout and ensure it is not cached as not-found** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Caching, Freshness, and Invalidation**. A green command without the negative case and causal explanation does not satisfy this gate.
