# Checkpoint — Module 04: PostgreSQL Query and Persistence Performance

## Required result

Capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics.

## Demonstrate

- explain the governing question: Which query plan, index, lock, pool, or pagination behavior is the first persistence bottleneck for a declared workload?
- show one accepted case and one rejected or failed case;
- identify the authoritative owner and decisive oracle;
- state one evidence limitation.

## Commands

```bash
make module-proof MODULE=04 TRACK=${TRACK:-python}
```

## Evidence to retain

Create:

```text
work/module-04/
├── dataset-manifest.json
├── query.sql
├── parameters.json
├── before-plan.json
├── after-plan.json
├── before-envelope.json
├── after-envelope.json
├── write-cost.json
├── migration-notes.md
└── decision.md
```

When PostgreSQL is unavailable, use packaged plan fixtures and mark the evidence Class A/B. The module cannot claim live index behavior from fixtures alone.

## Defend the design

Answer without reading from the chapter:

1. Why did the planner choose the baseline plan?
2. Which index column order follows your predicates?
3. What resource or workload became worse after the index?

## Continue only when

The module fails if the optimized query changes authorization or pagination semantics, or if read improvement is reported without write and index cost.

You may not compensate for a failed correctness, identity, or reproducibility gate with a better latency number.

The module is incomplete when the result is asserted but the failure path, authoritative evidence, or cross-language invariant is missing. Retain enough evidence for another reader to reproduce the decision that capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics.
