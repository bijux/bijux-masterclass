# Module 04 lab — Optimize owner-filtered run listing with a real plan

## Objective

Capture representative before/after plans, add migration 009, and prove that the index improves the target query without breaking pagination, authorization, or write budgets.

## Setup conditions

- `TEST_DATABASE_URL` points to a disposable PostgreSQL database for the full route
- migrations 001–008 apply cleanly
- the data generator creates skewed owners/status values at declared scale
- the pagination and owner-isolation vectors pass before tuning

## Failure action and investigation


1. Load `DS-RUNS-1M` or the largest feasible declared fixture.
2. Capture pool wait and `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` for representative parameter sets.
3. Record list workload and run-submission baseline.
4. Apply migration 009.
5. Refresh appropriate statistics and rerun identical parameters.
6. Compare plan summaries, latency, buffers, write latency, and index size.
7. Run stable-pagination and wrong-owner tests.
8. Roll back in a disposable clone or document concurrent-index rollback procedure.



### Investigation notes

Before editing, write a one-sentence hypothesis answering: **Which query plan, index, lock, pool, or pagination behavior is the first persistence bottleneck for a declared workload?** Record the first observation that contradicts the expected model. After the repair, explain why the capstone can now claim: Capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics. A passing command without this causal explanation is insufficient.

## Operational oracle

- owner and high-water predicates remain present
- page contents match the baseline semantics
- wrong-owner access remains invisible/rejected
- read plan and buffer behavior improve for the target distribution
- write and storage costs are quantified
- migration behavior is safe for the declared environment

## Required evidence

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

## Cleanup and reset

Drop the disposable database or restore the snapshot, terminate benchmark clients, and confirm no migration session or long transaction remains.

## Completion gate

- [ ] exact query semantics are documented
- [ ] representative parameter distributions are retained
- [ ] before/after plans are comparable
- [ ] read and write workloads are both measured
- [ ] pagination and owner-isolation vectors pass
- [ ] decision includes index size and migration cost

The lab is incomplete when the candidate is merely faster. It must preserve the inherited correctness oracle and explain the observed resource change.
