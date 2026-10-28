# Module 04 — PostgreSQL Query and Persistence Performance

> **Program stage:** Course 5 of 6 — Sustain the promise under pressure.

> **Central question:** Which query plan, index, lock, pool, or pagination behavior is the first persistence bottleneck for a declared workload?

## Where this module fits


The database is often blamed because it is visible in traces, but a slow query is not a diagnosis. The cause may be poor selectivity, missing statistics, a mismatched index order, excessive round trips, lock waiting, connection-pool queueing, serialization, or simply a data set too small to reveal the real plan.

This module teaches plan reading as hypothesis testing. You begin with the exact SQL and parameter distribution from a critical workload. You inspect estimated and actual rows, node timing, buffer activity, sorts, loops, and index conditions. You then make one change and measure both the target read and its write, storage, and maintenance cost.

The capstone focuses on the owner-authorized, status-filtered, cursor-paginated analysis-run listing. It is deliberately realistic: authorization predicates are mandatory, ordering must be stable, and the high-water cursor semantics from Course 2 cannot be removed. The fastest incorrect query is rejected.


## Capstone result

Capture before/after plans, add evidence-backed indexes, size database connections, and preserve owner-aware query semantics.

Add migration 009 with evidence-backed indexes, plan fixtures, query-plan comparison, and a live PostgreSQL proof route for run listing and job claiming.

## Learning outcomes

By the end of this module, you can:

- separate client wait, pool wait, lock wait, planning, execution, and transfer
- read PostgreSQL text and JSON plans from the root downward
- compare estimated and actual row counts
- interpret sequential scans, index scans, bitmap scans, sorts, joins, and loops
- design composite index column order from equality, range, and ordering predicates
- preserve authorization and stable keyset pagination
- measure read gain alongside write amplification and index size
- size connection pools against database capacity rather than request concurrency
- use `pg_stat_statements` as aggregate evidence without losing workload identity
- write a reversible migration and a plan-regression gate

## Core performance model

### 1. Start with the query contract


The target query is not “list runs.” It is:

```sql
SELECT id, project_id, status, created_at, version
FROM analysis_runs
WHERE owner_id = $1
  AND status = $2
  AND (created_at, id) < ($3, $4)
  AND (created_at, id) <= ($5, $6)
ORDER BY created_at DESC, id DESC
LIMIT $7;
```

The exact SQL may differ, but its semantics include owner isolation, status filter, keyset boundary, high-water bound, deterministic order, and page limit. Removing one predicate changes correctness.

Record parameter distributions. A plan for an owner with three rows may differ from an owner with three million rows. A status value matching 80% of the table has different selectivity from one matching 0.1%.


### 2. Where database time actually goes


A request can wait before PostgreSQL executes:

```text
application admission
→ connection-pool wait
→ network
→ lock wait
→ planning
→ execution
→ row transfer
→ application mapping
```

An execution plan explains planning and execution inside PostgreSQL; it does not show application pool wait. Tracing and pool metrics from Course 4 remain necessary.

Measure pool acquisition separately. A query that executes in 5 ms but waits 300 ms for a connection is not fixed by another index. Conversely, increasing the pool can overload PostgreSQL and worsen all queries.


### 3. Reading a plan


Use `EXPLAIN` for the proposed plan and `EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)` for actual execution in a safe test environment. `ANALYZE` executes the statement; wrap mutating statements in a transaction and roll back, or avoid executing destructive plans.

Read:

- node type and relation;
- estimated cost and rows;
- actual time, rows, and loops;
- filter and rows removed;
- index condition;
- sort method and memory/disk use;
- shared buffer hits and reads;
- temporary blocks;
- planning time and execution time.

A large difference between estimated and actual rows can cause poor choices. Investigate statistics, data skew, correlation, and parameter sensitivity before forcing an index.


### 4. Composite index design


B-tree indexes are most effective when their leading columns align with query predicates. A practical heuristic for this query is:

1. equality partition: `owner_id`, then perhaps `status`;
2. range and order: `created_at DESC, id DESC`;
3. included output columns only when index-only scans are plausible and write cost is acceptable.

Candidate:

```sql
CREATE INDEX CONCURRENTLY idx_runs_owner_status_created_id
ON analysis_runs (owner_id, status, created_at DESC, id DESC)
INCLUDE (project_id, version);
```

This is a hypothesis, not a universal recipe. If status is low-selectivity, separate indexes or a different order may perform better. `INCLUDE` increases index size and update cost. Index-only scans still depend on visibility-map state.


### 5. Keyset pagination and high-water bounds


Offset pagination asks the database to skip increasing amounts of work and can become unstable under concurrent changes. Course 2 implemented keyset pagination with a server-side cursor bound to principal, filters, current boundary, and a traversal high-water position.

The database query must use the same tuple order as the cursor. For descending `(created_at, id)`, the next-page boundary uses `<`. The high-water condition excludes rows newer than the captured traversal start. Index order must support both.

A plan improvement that drops the high-water predicate may make later pages faster while changing traversal semantics. The correctness vector catches duplicates or newly inserted rows appearing in an existing traversal.


### 6. N+1, batching, and row shape


One well-indexed query can still be followed by one query per result. Detect N+1 behavior through traces, query counts, and `pg_stat_statements`. Prefer a bounded join, aggregate, or batch query when it preserves authorization and avoids row explosion.

Select only fields needed by the representation. A covering index can reduce heap access for narrow pages, but returning large JSON or artifact metadata from the index is often counterproductive.

Batch size is not automatically “larger is faster.” Large batches hold memory and locks longer, create bigger responses, and may worsen tail latency. Measure page size as part of the workload identity.


### 7. Connection-pool capacity


Application request concurrency and database connection capacity are not the same. PostgreSQL performs useful work with a finite number of concurrent active queries; too many sessions create CPU contention, memory pressure, and lock queues.

Model:

```text
total_possible_connections =
    service_instances × pool_max_per_instance
    + workers × worker_pool_max
    + operational_reserve
```

This total must fit the database limit and measured service demand. Pool wait can be a healthy backpressure mechanism when bounded and timed. An unbounded queue is not.

The course stores pool configuration in the environment fingerprint, because changing it changes the experiment.


### 8. Read gain has write cost


Each index consumes storage and must be maintained on insert, delete, and updates to indexed columns. Measure:

- index size;
- run-submission transaction latency;
- job state-transition latency;
- WAL volume where available;
- vacuum and maintenance implications;
- lock behavior during index creation.

Migration 009 uses concurrent index creation in an operated PostgreSQL path. Because `CREATE INDEX CONCURRENTLY` cannot run inside a normal transaction block, the migration runner must support and document that operational distinction. The dependency-light course fixture remains a plan and schema assertion, not a live build claim.


### 9. Aggregate query evidence


`pg_stat_statements` can reveal total time, mean time, calls, and rows for normalized statements. It is valuable for identifying high aggregate cost and validating whether a query matters in an environment.

It does not replace workload-level evidence. Normalization may combine parameter distributions, and the extension’s statistics cover an interval. Correlate query ID or normalized text with the benchmark window and reset or snapshot responsibly.

The capstone live proof captures plans and selected aggregate statistics before and after migration 009.


## Course requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Exact semantics preserved | Owner, filters, order, high-water, and limit remain in query. | Fast query leaks or changes pages. | Pagination/security vectors |
| Plan parameters representative | Plan uses declared data scale and value distribution. | Tiny or atypical data selects irrelevant plan. | Dataset manifest |
| Actual plan safe | `EXPLAIN ANALYZE` is used only where execution is safe. | Benchmark mutates production-like data unexpectedly. | Lab transaction/reset |
| Estimates inspected | Estimated/actual row divergence is reported. | Index treats symptom while statistics remain wrong. | Plan summary |
| Read and write measured | Index candidate includes write latency and size cost. | Read improves while submissions degrade. | Paired workloads |
| Pool wait separate | Connection acquisition and query execution are distinct. | Index added for pool saturation. | Trace/pool metrics |
| Migration operationally valid | Concurrent index semantics are supported by runner. | Deployment blocks writes or migration fails. | Migration proof |
| Plan gate bounded | Gate checks semantic indicators, not brittle total cost alone. | Minor version changes cause meaningless failure. | Plan policy |

## Worked failures

### Case 1 — The missing owner predicate

**Initial condition.** A developer removes `owner_id` because the caller already has a scope and the plan becomes an index scan.

**Analysis.** Scope does not replace object/tenant policy. The query now leaks resources and changes selectivity.

**Correct response.** Keep owner filtering and design an owner-leading index or authorization-aware join.

**Lesson.** Security predicates are part of the query contract.

### Case 2 — The tiny-table sequential scan

**Initial condition.** A 500-row fixture uses a sequential scan, so the team forces an index scan globally.

**Analysis.** For a tiny table, sequential scan may be cheaper. The fixture does not represent production scale.

**Correct response.** Use representative scale and distributions; do not disable planner methods as a release fix.

**Lesson.** Plan shape without context is not a defect.

### Case 3 — The read-only benchmark

**Initial condition.** The new index cuts list p95 by 60%, but run submission p95 rises 25% and storage doubles.

**Analysis.** The index has significant maintenance cost. Whether it is acceptable depends on workload mix and budgets.

**Correct response.** Evaluate the complete critical workload mix and capacity model; adjust index or reject.

**Lesson.** An index participates in writes.

### Case 4 — The pool explosion

**Initial condition.** Every API instance increases its pool from 10 to 100 to remove pool wait.

**Analysis.** Aggregate active connections exceed database capacity, increasing context switching and query latency.

**Correct response.** Bound total connections, retain pool-wait metrics, and scale from measured service demand.

**Lesson.** Removing one queue can overload the next resource.

## Python implementation

### Mechanism

The Python plan module parses PostgreSQL JSON plans into a stable summary of node counts, rows, loops, buffers, sorts, and sequential scans. A psycopg live script captures plans when `TEST_DATABASE_URL` is provided.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_performance/query_plans.py`
- `capstone/tracks/python-fastapi/src/api_performance/db_budget.py`
- `capstone/tracks/python-fastapi/tests_performance/test_query_plans.py`
- `capstone/database/queries/list_runs.sql`

### Focused example

```python
from api_performance.query_plans import summarize_plan

summary = summarize_plan(plan_json)
assert summary.actual_rows == 50
assert summary.sequential_scans == ()
assert summary.shared_read_blocks <= 40
```

The summary walks nested `Plans`, multiplies per-loop row observations carefully, and records relation-scoped sequential scans. The release gate does not compare planner cost across versions as an absolute truth.

### Python-specific failure to avoid

Psycopg pool acquisition time must be measured outside the query timer. Avoid constructing a new pool or connection for every request in the benchmark.

## TypeScript implementation

### Mechanism

The TypeScript parser validates unknown JSON before traversal and preserves large block/row counts. The node-postgres live route records pool wait and execution separately.

### Repository paths

- `capstone/tracks/typescript-fastify/src/performance/query-plans.ts`
- `capstone/tracks/typescript-fastify/src/performance/db-budget.ts`
- `capstone/tracks/typescript-fastify/test-performance-core/query-plans.test.mjs`
- `capstone/database/queries/list_runs.sql`

### Focused example

```typescript
const summary = summarizePlan(planJson);
if (summary.actualRows !== 50n) throw new Error("unexpected rows");
if (summary.sequentialScans.length !== 0) throw new Error("unexpected scan");
if (summary.sharedReadBlocks > 40n) throw new Error("read budget exceeded");
```

Counts are bigint because PostgreSQL plan totals and cumulative statistics can exceed safe integers. Presentation converts them to decimal strings.

### TypeScript-specific failure to avoid

node-postgres returns many PostgreSQL integer types as strings by default. Do not install a global parser that silently converts every bigint to unsafe `number`.

## Cross-language invariant

Both tracks produce identical stable summaries for packaged before/after plan fixtures, including nested loops, buffer counts, sort spills, and sequential-scan relation names.

## Failure patterns

- **Plan-shape dogma.** Any sequential scan is called bad. **Decisive check:** representative cost and rows.
- **Authorization optimization.** Mandatory owner predicate is removed. **Decisive check:** security/conformance vectors.
- **Pool/query conflation.** Pool wait is attributed to SQL. **Decisive check:** separate timers.
- **Index-only fantasy.** Included columns guarantee no heap reads. **Decisive check:** visibility and buffer evidence.
- **Write cost blindness.** Read-only workload approves expensive index. **Decisive check:** mixed workload report.
- **Brittle plan gate.** Exact textual plan must match forever. **Decisive check:** semantic plan summary.

## Evidence and design review

Before accepting the module increment, answer:

1. Which exact SQL and parameter distribution does the plan represent?
2. Where is time spent before and after PostgreSQL execution?
3. Which estimated/actual row divergence matters?
4. How does index column order follow equality, range, and ordering predicates?
5. What write, storage, and migration cost does the candidate add?
6. Does the plan preserve owner filtering and high-water pagination?

## Module synthesis

Database performance is a query-and-data problem, not an index-collection exercise. Module 4 connects exact semantics, representative plans, pool behavior, read/write trade-offs, and operational migration evidence.

Proceed to [Exercises](exercises.md), then complete the [Lab](lab.md) and [Checkpoint](checkpoint.md).

## Next in the story

The next module, **Runtime Profiling and Allocation Control**, asks: Which Python or Node.js runtime phase consumes wall time, CPU, allocations, event-loop capacity, or serialization effort? It builds on the evidence produced here rather than reopening this module's decisions.
