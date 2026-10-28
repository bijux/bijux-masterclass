# Checkpoint — Module 07: Caching, Freshness, and Invalidation

## Required result

Build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics.

## Demonstrate

- explain the governing question: Which data is safe to cache, for whom, for how long, and who owns invalidation after mutation or failure?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=07 TRACK=${TRACK:-python}
```

## Evidence to retain

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

## Defend the design

Answer without reading from the chapter:

1. What exact question does your hottest key answer?
2. Why does versioning preserve correctness after invalidation failure?
3. What happens to the origin during a cache outage?

## Continue only when

The module fails if a protected value can be reused across security contexts, if a transient error becomes a cached absence, or if fills/waiters are unbounded.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that build authorization-aware keys, TTL/capacity policy, source-version invalidation, single-flight fills, and failure semantics.
