# Lab — Module 04 lab — Optimize owner-filtered run listing with a real plan

> **Module 04:** PostgreSQL Query and Persistence Performance

## Objective

Capture representative before/after plans, add migration 009, and prove that the index improves the target query without breaking pagination, authorization, or write budgets.

## Why this lab matters

This lab turns the module’s governing question—**Which query plan, index, lock, pool, or pagination behavior is the first persistence bottleneck for a declared workload?**—into a falsifiable experiment. Migration 009 uses concurrent index creation in an operated PostgreSQL path. Because CREATE INDEX CONCURRENTLY cannot run inside a normal transaction block, the migration runner must support and document that operational distinction. The dependency-light course fixture remains a plan and schema assertion, not a live build claim.

It advances the cumulative Analysis Runs Platform by requiring this result: **Capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

- `TEST_DATABASE_URL` points to a disposable PostgreSQL database for the full route
- migrations 001–008 apply cleanly
- the data generator creates skewed owners/status values at declared scale
- the pagination and owner-isolation vectors pass before tuning

## Hypothesis

The clean implementation should satisfy this claim: **owner and high-water predicates remain present; page contents match the baseline semantics; wrong-owner access remains invisible/rejected; read plan and buffer behavior improve for the target distribution; write and storage costs are quantified; migration behavior is safe for the declared environment.** When the lab introduces this fault—**the lab introduces its declared planted defect**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Load `DS-RUNS-1M` or the largest feasible declared fixture.
2. Capture pool wait and `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` for representative parameter sets.
3. Record list workload and run-submission baseline.
4. Apply migration 009.
5. Refresh appropriate statistics and rerun identical parameters.
6. Compare plan summaries, latency, buffers, write latency, and index size.
7. Run stable-pagination and wrong-owner tests.
8. Roll back in a disposable clone or document concurrent-index rollback procedure.

### Investigation notes

Before editing code, predict the first observable divergence caused by **the lab introduces its declared planted defect**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Capture representative before/after plans, add migration 009, and prove that the index improves the target query without breaking pagination, authorization, or write budgets**, and identify one attractive implementation that would pass the happy path while failing the oracle.

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

## Interpretation and defense

1. Which state or effect is authoritative for **PostgreSQL Query and Persistence Performance**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **the lab introduces its declared planted defect** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

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

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **PostgreSQL Query and Persistence Performance**. A green command without the negative case and causal explanation does not satisfy this gate.
