# Worked Answers — Module 04: PostgreSQL Query and Persistence Performance

Use these solutions to audit your reasoning for **PostgreSQL Query and Persistence Performance**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Propose an index for owner, status, descending created_at/id pagination.

A reasonable hypothesis is `(owner_id, status, created_at DESC, id DESC)`, optionally including narrow projected columns. Equality predicates lead, then range/order columns. It must be tested against actual selectivity and write cost; it is not universally optimal.

The chapter’s decisive distinction is this: This is a hypothesis, not a universal recipe. If status is low-selectivity, separate indexes or a different order may perform better. INCLUDE increases index size and update cost. Index-only scans still depend on visibility-map state.

## 2. Why can an index-only scan still read heap pages?

PostgreSQL must verify row visibility unless the visibility map shows the page is all-visible. Recent updates, vacuum state, and table churn affect this. `INCLUDE` does not guarantee zero heap fetches.

In the cumulative capstone, the rule becomes concrete: Migration 009 uses concurrent index creation in an operated PostgreSQL path. Because CREATE INDEX CONCURRENTLY cannot run inside a normal transaction block, the migration runner must support and document that operational distinction. The dependency-light course fixture remains a plan and schema assertion, not a live build claim.

## 3. Actual rows are 100,000 while estimated rows are 100. What does that suggest?

The planner severely underestimated cardinality. Investigate stale statistics, data skew, correlated columns, parameter distribution, or expression statistics. The misestimate may explain a poor join or scan choice.

A useful way to reason about the boundary is: Record parameter distributions. A plan for an owner with three rows may differ from an owner with three million rows. A status value matching 80% of the table has different selectivity from one matching 0.1%.

## 4. A query executes in 8 ms but request span shows 240 ms database time. What next?

Separate connection-pool acquisition, network, lock wait, transaction setup, result transfer, and row mapping. The plan’s 8 ms does not include all application-observed database latency.

The implementation consequence is: Measure pool acquisition separately. A query that executes in 5 ms but waits 300 ms for a connection is not fixed by another index. Conversely, increasing the pool can overload PostgreSQL and worsen all queries.

**Evidence.** Retain before/after EXPLAIN evidence, rows and buffers, write cost, pool pressure, and latency under the declared data distribution and workload.

## 5. Why is `EXPLAIN ANALYZE DELETE ...` dangerous?

`ANALYZE` executes the statement. In a test, wrap it in a transaction and roll back if safe, or use non-mutating alternatives. Never run it casually on valuable data.

The important nuance is: Use EXPLAIN for the proposed plan and EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) for actual execution in a safe test environment. ANALYZE executes the statement; wrap mutating statements in a transaction and roll back, or avoid executing destructive plans.

## 6. For 8 API instances with pool max 20, 4 workers with pool max 5, and reserve 10, calculate possible connections.

`8×20 + 4×5 + 10 = 190`. This must fit PostgreSQL capacity and account for other clients. It does not mean 190 active queries are desirable.

Under concurrency or failure, the distinction becomes: Application request concurrency and database connection capacity are not the same. PostgreSQL performs useful work with a finite number of concurrent active queries; too many sessions create CPU contention, memory pressure, and lock queues.

**Evidence.** Retain before/after EXPLAIN evidence, rows and buffers, write cost, pool pressure, and latency under the declared data distribution and workload.

## 7. Why may status be a poor leading index column?

If it has few values and one value dominates, selectivity is low. Leading with owner may partition more effectively. The decision depends on actual distributions and query mix.

The design remains honest only if: It does not replace workload-level evidence. Normalization may combine parameter distributions, and the extension’s statistics cover an interval. Correlate query ID or normalized text with the benchmark window and reset or snapshot responsibly.

**Evidence.** Retain before/after EXPLAIN evidence, rows and buffers, write cost, pool pressure, and latency under the declared data distribution and workload.

## 8. What does a sort spill indicate?

The sort exceeded available memory for that operation and used temporary disk blocks. An index matching order may avoid it, or query/page size and memory settings may need review. Raising memory globally without capacity analysis is unsafe.

The consumer-facing consequence is: Batch size is not automatically “larger is faster.” Large batches hold memory and locks longer, create bigger responses, and may worsen tail latency. Measure page size as part of the workload identity.

## 9. How does high-water pagination affect the index query?

The query must constrain rows to the captured maximum traversal position as well as the current page boundary. Both use the same ordered tuple, allowing the index to preserve stable traversal while excluding new rows.

The operational consequence is: The database query must use the same tuple order as the cursor. For descending (created at, id), the next-page boundary uses <. The high-water condition excludes rows newer than the captured traversal start. Index order must support both.

## 10. Why should exact planner cost not be a cross-version gate?

Planner cost is an internal estimate influenced by version, statistics, and settings; it is not elapsed time or a stable API. Gate semantic indicators and measured workload outcomes instead.

The strongest engineering interpretation is: pg stat statements can reveal total time, mean time, calls, and rows for normalized statements. It is valuable for identifying high aggregate cost and validating whether a query matters in an environment.

**Evidence.** Retain before/after EXPLAIN evidence, rows and buffers, write cost, pool pressure, and latency under the declared data distribution and workload.

## 11. When is a partial index appropriate?

When a stable predicate selects a subset heavily used by critical queries, such as active states, and the query predicate implies the index predicate. It adds operational and evolution complexity; status transitions and other workloads must be measured.

The defect-oriented view is: One well-indexed query can still be followed by one query per result. Detect N+1 behavior through traces, query counts, and pg stat statements. Prefer a bounded join, aggregate, or batch query when it preserves authorization and avoids row explosion.

## 12. Design a read/write index decision.

Compare list-run latency, buffers, and plan before/after; measure submission and state-transition latency, WAL or write counters, index size, migration time/locking, and workload mix. Accept only if aggregate objective and budgets improve with documented cost.

Across the Python and TypeScript tracks, the invariant is: The Python plan module parses PostgreSQL JSON plans into a stable summary of node counts, rows, loops, buffers, sorts, and sequential scans. A psycopg live script captures plans when TEST DATABASE URL is provided.
