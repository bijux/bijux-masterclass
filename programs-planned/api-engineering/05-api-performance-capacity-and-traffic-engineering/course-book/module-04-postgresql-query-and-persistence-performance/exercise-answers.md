# Reference Answers — Module 04: Module 04 exercise answers — PostgreSQL Query and Persistence Performance

Read after attempting all twelve PostgreSQL Query and Persistence Performance exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Propose an index for owner, status, descending created_at/id pagination.

A reasonable hypothesis is `(owner_id, status, created_at DESC, id DESC)`, optionally including narrow projected columns. Equality predicates lead, then range/order columns. It must be tested against actual selectivity and write cost; it is not universally optimal.

## 2. Why can an index-only scan still read heap pages?

PostgreSQL must verify row visibility unless the visibility map shows the page is all-visible. Recent updates, vacuum state, and table churn affect this. `INCLUDE` does not guarantee zero heap fetches.

## 3. Actual rows are 100,000 while estimated rows are 100. What does that suggest?

The planner severely underestimated cardinality. Investigate stale statistics, data skew, correlated columns, parameter distribution, or expression statistics. The misestimate may explain a poor join or scan choice.

## 4. A query executes in 8 ms but request span shows 240 ms database time. What next?

Separate connection-pool acquisition, network, lock wait, transaction setup, result transfer, and row mapping. The plan’s 8 ms does not include all application-observed database latency.

## 5. Why is `EXPLAIN ANALYZE DELETE ...` dangerous?

`ANALYZE` executes the statement. In a test, wrap it in a transaction and roll back if safe, or use non-mutating alternatives. Never run it casually on valuable data.

## 6. For 8 API instances with pool max 20, 4 workers with pool max 5, and reserve 10, calculate possible connections.

`8×20 + 4×5 + 10 = 190`. This must fit PostgreSQL capacity and account for other clients. It does not mean 190 active queries are desirable.

## 7. Why may status be a poor leading index column?

If it has few values and one value dominates, selectivity is low. Leading with owner may partition more effectively. The decision depends on actual distributions and query mix.

## 8. What does a sort spill indicate?

The sort exceeded available memory for that operation and used temporary disk blocks. An index matching order may avoid it, or query/page size and memory settings may need review. Raising memory globally without capacity analysis is unsafe.

## 9. How does high-water pagination affect the index query?

The query must constrain rows to the captured maximum traversal position as well as the current page boundary. Both use the same ordered tuple, allowing the index to preserve stable traversal while excluding new rows.

## 10. Why should exact planner cost not be a cross-version gate?

Planner cost is an internal estimate influenced by version, statistics, and settings; it is not elapsed time or a stable API. Gate semantic indicators and measured workload outcomes instead.

## 11. When is a partial index appropriate?

When a stable predicate selects a subset heavily used by critical queries, such as active states, and the query predicate implies the index predicate. It adds operational and evolution complexity; status transitions and other workloads must be measured.

## 12. Design a read/write index decision.

Compare list-run latency, buffers, and plan before/after; measure submission and state-transition latency, WAL or write counters, index size, migration time/locking, and workload mix. Accept only if aggregate objective and budgets improve with documented cost.
