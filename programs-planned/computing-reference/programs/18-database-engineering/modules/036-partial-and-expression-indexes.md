---
module_id: DBE-036
program: Database Engineering
level: 1
module_number: 36
title: Partial and Expression Indexes
status: complete
last_verified: 2026-08-30
---

# Partial and Expression Indexes

## One-Page Review

### Governing question

When is it correct and worthwhile to index a computed value or only a subset of rows, and what must the optimizer, write path, and operator prove before such an index can answer a query or enforce a constraint?

### Essential definitions

An **expression/functional index** stores the result of a declared expression `E(row)` as an index key. **Expression matching** is the engine's recognition that a query expression has the same indexed meaning, including types, casts, collation, operator class, and function identity. **Volatility/determinism** states whether the same row inputs always produce the same index result across statements, settings, versions, and time. A **partial/filtered index** stores entries only for rows satisfying predicate `P(row)`. It is safe for query condition `Q` only when `Q => P` under SQL's NULL and type semantics and the optimizer can prove that implication at planning time. A **partial unique index** enforces uniqueness only among rows satisfying `P`. **Predicate transition** occurs when an update moves a row into or out of the indexed subset.

### Central model, mechanism, or theorem

Expression correctness requires write-time `E(row)` and lookup-time expression semantics to agree for the index lifetime; nondeterministic, setting-dependent, or version-drifting results require prohibition or rebuild/version controls. Partial-index lookup is sound exactly when every row allowed by `Q` is included by `P`: `Q => P`. If implication is absent, scanning only the partial index can create false negatives. Even a mathematically valid implication may be unusable when the optimizer's bounded prover cannot recognize its syntax, types, parameters, or prepared-plan context. Expression and predicate specialization can be combined, but their proof obligations accumulate.

### Critical invariants

- Stored expression values equal the declared computation under the index's type, collation, configuration, function, and version contract.
- Functions admitted to persistent index keys satisfy the engine's required determinism/immutability promise; dependencies are tracked or operationally rebuilt.
- Every row satisfying partial predicate `P` has the required entry; no row failing `P` participates in the partial index's lookup or uniqueness scope.
- A query uses the partial index alone only when its conditions provably imply `P` for every permitted parameter value.
- SQL three-valued logic is respected: `UNKNOWN` does not silently become `TRUE`, and `IS NULL` is distinct from `= NULL`.
- Expression recognition preserves result type, collation, cast, operator class, and canonical form required by the engine.
- Inserts and updates evaluate old/new membership and keys atomically with the base-row transaction and recovery protocol.
- Partial uniqueness is checked on entry into the predicate set and released only when departure/deletion is transactionally safe.
- Statistics, validation, replication, backup, upgrade, and rebuild cover the specialized indexed population and expression version.
- Smaller read structures are justified against computation, maintenance, plan-cache, and operational complexity.

### Common failures

Failures include marking a time-zone/configuration-dependent function immutable; assuming algebraic equivalence implies optimizer expression matching; forgetting a cast or collation; using a partial index when the query merely overlaps rather than implies its predicate; expecting `x < ?` to imply `x < 10` for every bound parameter; treating NULL as false/equal without declared logic; omitting predicate transitions from updates; using a partial index as table partitioning; creating many non-overlapping partial indexes instead of a real partitioning design; assuming partial uniqueness applies to excluded rows; changing function/collation versions without rebuild; and declaring an unused index successful because its DDL succeeded.

### Compact example

An index on `(tenant,lower(trim(email))) WHERE deleted_at IS NULL` contains active normalized emails only. Query `tenant=7 AND lower(trim(email))='ada@example.com' AND deleted_at IS NULL` implies the predicate and can return active row 1. Omitting `deleted_at IS NULL` asks for active and deleted rows; the partial index lacks deleted row 2, so using it alone is unsound. A generic prepared clause `deleted_at IS ?` is not universally sufficient at plan time. A unique version prevents two active normalized emails per tenant but permits archived duplicates outside the predicate.

### Connections

This module extends [DBE-035](035-composite-and-covering-indexes.md)'s key/payload design with computed keys and subset membership. DBE-037–039 cover specialized structures, selectivity, and maintenance cost; later optimizer modules formalize predicate reasoning and plan caching.

## Governing Question

The governing question separates **semantic validity**, **planner recognition**, and **economic value**. A definition may be semantically sound but not matched by the optimizer. It may be matched but costed poorly. It may accelerate one probe while adding expensive expression evaluation and predicate transitions to every write. Each layer needs its own evidence.

For an expression index, ask: is the stored value stable and identical to the query's value? For a partial index, ask: can any row satisfying the query be absent from the indexed subset? For both, ask: will the actual engine/version prove usability, maintain it correctly under MVCC/recovery, and improve the measured workload?

## Why This Matters

Expression indexes turn expensive or otherwise unsearchable computations—normalized email, date extraction, JSON paths, geometric transforms—into ordered/hashable keys. Partial indexes can exclude common/uninteresting rows, shrink hot structures, reduce write/storage cost for excluded rows, and enforce conditional business rules such as one active assignment.

Their precision is also their risk. A plain column index has an obvious mapping; a specialized index embeds program logic and a logical subset in physical state. Configuration drift, prepared statements, NULL, function upgrades, predicate evolution, and ORM query rewrites can silently change usability. The design needs durable ownership, versioning, plan tests, and rebuild procedures.

## Prerequisites and Retrieval

Retrieve SQL NULL/three-valued logic, constraints, and MVCC from DBE-011–020. Retrieve physical keys and comparator requirements from [DBE-031](031-b-tree-structure.md), scan bounds/rechecks from [DBE-032](032-b-tree-search-and-range-scan.md), mutation/recovery from [DBE-033](033-b-tree-insertion-splitting-and-deletion.md), and composite design/coverage from [DBE-035](035-composite-and-covering-indexes.md).

Before proceeding, construct a truth table for predicates `x IS NULL`, `x = 5`, `x <> 5`, and `NOT(x = 5)` when `x` is NULL. Distinguish mathematical equivalence from syntactic identity, and explain why a cached plan with an unknown parameter cannot rely on a condition true only for some executions.

## Learning Objectives

After completing this module, you should be able to:

1. define expression-index semantics across types, casts, collations, functions, and settings;
2. distinguish deterministic/immutable promises from merely stable-within-statement behavior;
3. prove or refute `Q => P` for partial-index safety under three-valued SQL logic;
4. predict planner-recognition limits for syntax, parameters, prepared plans, and generated columns;
5. design partial unique constraints with exact membership and NULL semantics;
6. trace insert/update/delete transitions among excluded, included, and changed-expression states;
7. reason about expression plus partial plus composite/covering designs without conflating roles;
8. plan version, collation, function, dependency, validation, and rebuild lifecycle;
9. quantify population, selectivity, computation, write, WAL, cache, and operational costs; and
10. test logical equivalence, plan usability, false negatives, concurrency, recovery, and drift.

## Core Exposition

An expression index materializes a function of a row in index entries. Given `E(row)=lower(trim(email))`, insertion evaluates `E`, encodes it with a result type/collation/operator class, and stores it with a locator. A lookup is not “call any equivalent normalization”; it must use an expression the engine recognizes as matching the indexed computation, then follow ordinary access-method comparison and visibility rules.

Matching capability varies. PostgreSQL describes indexes on expressions and requires functions/operators used in index definitions to meet immutability requirements. MySQL functional key parts are implemented through hidden virtual generated columns, and its optimizer documents exact expression/result-type matching restrictions; `f1+1` need not match `1+f1`. SQLite similarly states that expression forms must match essentially as written rather than relying on algebraic theorem proving. Verify current behavior, not a portable canonicalizer that does not exist.

Types and collations are semantic. `lower(email)` returning text under one collation can order/equal values differently after a collation-library change. JSON extraction may return quoted JSON versus unquoted text; an implicit cast can choose another operator class. Timestamp-to-date depends on time zone unless fixed in the expression/semantics. A query that appears visually similar can have a different result type or comparison.

Persistent keys need stronger stability than “does not change during this query.” PostgreSQL's volatility categories illustrate the distinction: `VOLATILE` can change within a scan, `STABLE` is fixed within one statement, and `IMMUTABLE` promises the same result for the same arguments indefinitely. Mislabeling configuration/table/time-dependent logic immutable can persist keys that no longer agree with queries. The database cannot validate arbitrary human promises about function bodies or external state.

A robust expression contract records function/schema identity, argument/result types, collation/operator class, relevant fixed settings, NULL behavior, algorithm/data/library version, and rebuild trigger. Prefer built-in, simple, truly deterministic expressions. If behavior changes, mark invalid or rebuild from base rows before relying on the index. Replicas, restore environments, and rolling upgrades must compute compatible values.

A partial index with predicate `P` stores row `r` iff SQL evaluation of `P(r)` is `TRUE`; `FALSE` and `UNKNOWN` are excluded unless the product states otherwise. Query condition `Q` can rely solely on it only if for every row and permitted parameter assignment, `Q(r)=TRUE` implies `P(r)=TRUE`. This is ordinary logical containment adapted to SQL semantics.

Example: `Q: status='ready' AND deleted_at IS NULL` implies `P: deleted_at IS NULL`. `Q: status IN ('ready','retry')` does not imply `P: status='ready'`. `Q: amount<5` mathematically implies `P: amount<10` for compatible non-NULL numeric semantics; NULL never makes `Q` true. Yet an optimizer supports only bounded implication rules, so semantic truth does not guarantee plan use.

PostgreSQL's current documentation explicitly says partial-index matching happens at planning time, its prover is not a general theorem prover, and a parameterized clause such as `x < ?` cannot imply `x < 2` for all possible values. Custom versus generic prepared plans, ORM literalization, casts, and rewritten predicates therefore affect usability. Never solve this by forcing an index that is not logically safe.

Partial indexes are best for a stable, meaningful minority: active jobs, unbilled events, unarchived rows, exceptional values, or rows needing work. They are poor substitutes for partitioning a table into many categories. PostgreSQL warns against many disjoint partial indexes as a partitioning surrogate because the planner must reason across them and the physical design lacks partition management/pruning semantics.

The predicate need not mention the key column. Index `(tenant,run_at,id) WHERE status IN ('ready','retry')` supports a claim queue when the query repeats/implies the status predicate. The index stays small if terminal rows dominate. But frequent ready↔running transitions create delete/insert maintenance, contention, WAL, dead tuples, and statistics churn precisely on the hot path.

Partial uniqueness encodes conditional constraints. Unique `(tenant,normalized_email) WHERE deleted_at IS NULL` means no two active rows in the same tenant share the normalized email, subject to NULL semantics. Deleted rows are not checked against one another or active rows. Transitioning a deleted row to active must perform uniqueness checking atomically; concurrent activations require transaction-level conflict handling beyond page latches.

Combining expression and partial indexing accumulates conditions. The query must match `E`, imply `P`, use compatible operators/types, and satisfy access-method bounds; returned entries still undergo visibility and residual rechecks. Adding included payload only affects coverage, not expression matching or predicate implication. A smaller index can be covering, but “partial” and “covering” answer different questions.

Write-path cases are explicit. Insert evaluates `P(new)`; if true, evaluate `E(new)` and insert/check. Update evaluates old and new states: false→false does nothing to this index; false→true inserts/checks; true→false deletes later under MVCC rules; true→true updates the entry if expression/key/payload changed. Delete logically removes the row while old snapshots may still require its entry. WAL/recovery must reproduce membership and value consistently.

Generated/stored columns offer an alternative: name and type the computation, test it directly, then index the column. This can improve query/ORM matching and observability but adds schema/storage or engine-specific behavior. Application-maintained normalized columns make dependencies explicit but risk dual-write drift unless database constraints/triggers/generated definitions verify them. Compute-on-query avoids write cost but gives up direct index lookup.

Cost includes evaluating `P` and `E` on writes, population fraction, entry width, fan-out/height, uniqueness conflicts, transitions, WAL/replication, cache, vacuum/cleanup, statistics, plan-cache behavior, build/rebuild, dependency upgrades, and debugging. Partial indexes can make estimates fragile because subset distribution differs from table distribution. A tiny subset can still be hot and contentious.

Observability records index/expression/predicate version, validity, population estimate/actual, entry/page size, distinct/NULL distribution, scans, candidates/rechecks, heap fetches, plan type (custom/generic), implication/match failures where observable, expression evaluation time/errors, membership transitions, uniqueness conflicts/waits, WAL/splits/dead entries, build/rebuild age, dependency/collation versions, and p50/p99. Do not log sensitive normalized values.

Testing starts with a full-table reference evaluation of `E`, `P`, and `Q` under exact types/collation/NULL/settings. Generate boundary values and syntactic variants; assert every index result matches the reference and every qualifying row is reachable. Test prepared literals/parameters and inspect actual plans without making plan selection the correctness oracle. Mutate indexed dependencies/settings in controlled upgrade tests, inject concurrent predicate transitions and crashes, recover twice, and validate base-to-index membership/value/uniqueness.

The executable model below implements a fixed normalized-email expression and active-row partial predicate. It proves safe use for a query that declares `deleted_at IS NULL`, demonstrates the deleted row missing from an unrestricted query, rejects an unknown parameter at plan time, and validates active-scope uniqueness. It is not a SQL planner, three-valued theorem prover, B+ tree, MVCC engine, or performance model.

<!-- bijux-verify: {"id":"partial-expression-safety","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"index_ids=(1, 3, 4)\nactive_query_ids=(1,)\nunrestricted_query_ids=(1, 2)\npartial_safe_active=True\npartial_safe_unrestricted=False\nparameterized_safe=False\nuniqueness_scope='active-normalized-email-per-tenant'\ninvariants=True\n","stderr":""}} -->
```python
rows = (
    {"id": 1, "tenant": 7, "email": " Ada@example.com ", "deleted_at": None},
    {"id": 2, "tenant": 7, "email": "ADA@example.com", "deleted_at": "2026-01-01"},
    {"id": 3, "tenant": 7, "email": "bob@example.com", "deleted_at": None},
    {"id": 4, "tenant": 8, "email": "ada@example.com", "deleted_at": None},
)


def normalized_email(row: dict[str, object]) -> str:
    return str(row["email"]).strip().lower()


def in_partial_index(row: dict[str, object]) -> bool:
    return row["deleted_at"] is None


entries = tuple(
    sorted(
        (row["tenant"], normalized_email(row), row["id"])
        for row in rows
        if in_partial_index(row)
    )
)


def reference_query(include_deleted: bool) -> tuple[int, ...]:
    return tuple(
        int(row["id"])
        for row in rows
        if row["tenant"] == 7
        and normalized_email(row) == "ada@example.com"
        and (include_deleted or row["deleted_at"] is None)
    )


def index_query() -> tuple[int, ...]:
    return tuple(
        int(row_id)
        for tenant, email, row_id in entries
        if tenant == 7 and email == "ada@example.com"
    )


def query_implies_partial(deleted_clause: object) -> bool:
    return deleted_clause == "is-null-literal"


active_query_ids = reference_query(False)
unrestricted_query_ids = reference_query(True)
partial_safe_active = query_implies_partial("is-null-literal") and index_query() == active_query_ids
partial_safe_unrestricted = query_implies_partial("unrestricted")
parameterized_safe = query_implies_partial("unknown-parameter")
active_keys = tuple((tenant, email) for tenant, email, _ in entries)
invariants = (
    tuple(entry[2] for entry in entries) == (1, 3, 4)
    and len(active_keys) == len(set(active_keys))
    and not partial_safe_unrestricted
    and index_query() != unrestricted_query_ids
)

print(f"index_ids={tuple(entry[2] for entry in entries)}")
print(f"active_query_ids={active_query_ids}")
print(f"unrestricted_query_ids={unrestricted_query_ids}")
print(f"partial_safe_active={partial_safe_active}")
print(f"partial_safe_unrestricted={partial_safe_unrestricted}")
print(f"parameterized_safe={parameterized_safe}")
print("uniqueness_scope='active-normalized-email-per-tenant'")
print(f"invariants={invariants}")
```

## Definitions and Notation

Let row domain be `R`; expression `E:R→K`; partial predicate `P:R→{TRUE,FALSE,UNKNOWN}`; query predicate `Q` likewise. Indexed set `I_P={r | P(r)=TRUE}`. Safe partial-only answering requires `{r | Q(r)=TRUE} subset I_P`, written `Q => P`. Let `match(E_q,E_i)` be the engine's expression-recognition relation; mathematical equivalence does not imply `match`.

Let population fraction be `rho=|I_P|/|R|`, membership transitions per interval be `t`, expression evaluation cost `c_E`, predicate cost `c_P`, index bytes `S`, and false-negative count `FN`. Correctness requires `FN=0`; smaller `rho` or faster plans cannot compensate for any missing qualifying row.

## Mechanisms, Invariants, or Proof Structure

A defensible workflow is:

1. Declare business equality/subset semantics, NULL truth table, expression/predicate, types, collation, operator class, and constraint scope.
2. Audit every function/dependency/setting/version for the engine's determinism requirement; reject false immutability promises.
3. Prove `Q => P` independently for every intended query family and parameter domain.
4. Verify the actual optimizer recognizes expression and implication for literals, prepared custom/generic plans, ORM output, casts, and collations.
5. Trace insert and all four old/new membership transitions plus expression/payload changes and concurrent uniqueness conflicts.
6. Define WAL/recovery, replication, backup/restore, dependency upgrade, invalidation, validation, and rebuild behavior.
7. Measure subset distribution, plan candidates/rechecks/base fetches, write/transition cost, cache/WAL, and contention against alternatives.
8. Canary rollout with a full-table result oracle, plan monitoring, rollback, and drift alarms.
9. Periodically revalidate base-to-index membership/value/uniqueness and dependency versions.

Soundness proof is direct: if `Q => P`, each qualifying row is in `I_P`; assuming complete correct maintenance and access-method search, scanning the relevant index keys cannot omit it due solely to partiality. If implication fails, a witness row with `Q=TRUE` and `P!=TRUE` is absent, so partial-only execution can miss it. This is a proof sketch conditioned on SQL semantics, expression match, maintenance, visibility, and scan correctness.

## Alternatives and Trade-Offs

Plain indexes are larger but broadly usable and simpler. Partial indexes reduce population and conditionalize uniqueness but narrow query matching and add transitions. Expression indexes make computation searchable but embed function semantics. Generated columns name/type computations; application-maintained columns increase portability but require drift prevention. Materialized views can precompute broader query results with refresh/consistency cost.

A composite partial expression index may precisely fit a hot queue or active-key constraint, but each specialization reduces reuse and increases operational knowledge. Partitioning provides explicit data boundaries/lifecycle when subsets are large/disjoint; many partial indexes are not a substitute. Full-text, inverted, and JSON-specific indexes may better represent token/containment queries than scalar extraction.

## Failure Modes and Misconceptions

- “Deterministic today means immutable forever.” Settings, libraries, collation, lookup tables, and code versions can drift.
- “`STABLE` is enough for a persistent key.” Stable-within-statement is weaker than same-input-forever.
- “Equivalent algebra matches.” Optimizers commonly use bounded structural matching, not general algebra.
- “Overlap implies usability.” Partial safety requires query subset, `Q => P`.
- “The parameter is always small in practice.” A generic plan must be safe for its declared domain.
- “NULL fails the predicate.” SQL returns UNKNOWN in many comparisons; spell out membership.
- “Partial unique means table unique.” Excluded rows are outside the constraint.
- “Changing status is a cheap non-key update.” It can insert/delete the partial entry and conflict.
- “A tiny index is never hot.” Queue/active subsets often concentrate all writers.
- “Many partial indexes are partitions.” They lack partition ownership/pruning/lifecycle semantics.
- “Forcing the index fixes matching.” It can produce false negatives if implication is invalid.
- “Rebuild is optional after semantic drift.” Persisted keys must be recomputed before trusted use.
- “Planner use proves correctness.” Compare complete query results to a reference oracle.
- “No plan use means no cost.” Writes still maintain a valid but unused index.

## Worked Examples

### Example 1

Index `lower(email)` is queried with `lower(email)=x`; types/collation match, so it is a candidate. Querying `upper(email)=upper(x)` may be mathematically related for limited alphabets but is not the same expression/semantics. Conclusion: use the declared normalization exactly.

### Example 2

An expression converts timestamp to local date using session time zone. The same timestamp maps to different dates after a setting change. Marking it immutable corrupts logical agreement. Conclusion: fix the zone explicitly or do not persist that expression key.

### Example 3

Partial predicate is `amount<10`; query has literal `amount<5`. The implication is valid for compatible numeric semantics, and PostgreSQL documents recognizing simple inequalities. `amount<?` is not universally sufficient. Conclusion: proof and planner recognition are separate gates.

### Example 4

Partial predicate is `deleted_at IS NULL`; query omits deletion state. An archived matching row witnesses `Q=TRUE,P=FALSE`, so using the index alone misses it. Conclusion: one counterexample refutes safety.

### Example 5

Predicate `status<>'done'` excludes NULL because the comparison is UNKNOWN, while an application might call NULL “not done.” Use a deliberate predicate such as `status IS DISTINCT FROM 'done'` where supported. Conclusion: membership follows SQL truth, not prose intuition.

### Example 6

Unique normalized email applies only to active rows. Two archived duplicates coexist; activating one succeeds, concurrent activation of the other must conflict. Conclusion: uniqueness is enforced at predicate entry under transaction rules.

### Example 7

A job moves pending→ready and enters the partial queue index, ready→running and leaves it, then retry→ready and re-enters. Each transition creates maintenance/dead versions/WAL. Conclusion: small population can have high churn.

### Example 8

MySQL generated expression is `f1+1`; query uses `1+f1`. Current official documentation says the match requires identical expression/result type. Conclusion: ordinary algebraic commutativity does not guarantee plan recognition.

### Example 9

A collation upgrade changes normalized ordering/equality. Index pages remain structurally valid and checksummed but logically stale. Mark/rebuild and validate against base rows. Conclusion: physical integrity is not semantic validity.

### Example 10

An active-row partial index is 2% of the table yet receives 90% of updates and all claim scans. It saves read pages but causes latch/WAL p99. Compare a queue table/partition and measure transitions. Conclusion: population fraction alone is not an economic model.

## Cross-Program Connections

- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies purity, referential transparency, and evaluation semantics.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies implication proofs, counterexamples, and differential oracles.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) supplies canonicalization hazards and constraint-bypass analysis.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) supplies prepared-query/ORM shapes and idempotent active-key contracts.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies rollout, dependency/version drift, telemetry, and rebuild operations.

## References

1. PostgreSQL Global Development Group, [Partial Indexes](https://www.postgresql.org/docs/current/indexes-partial.html), current predicate implication, parameterization, uniqueness, and anti-partitioning guidance.
2. PostgreSQL Global Development Group, [Indexes on Expressions](https://www.postgresql.org/docs/current/indexes-expressional.html), current expression maintenance and uniqueness guidance.
3. PostgreSQL Global Development Group, [Function Volatility Categories](https://www.postgresql.org/docs/current/xfunc-volatility.html), current `VOLATILE`, `STABLE`, and `IMMUTABLE` promises and hazards.
4. PostgreSQL Global Development Group, [CREATE INDEX](https://www.postgresql.org/docs/current/sql-createindex.html), current expression, predicate, collation, operator-class, and concurrent-build rules.
5. SQLite Project, [Partial Indexes](https://www.sqlite.org/partialindex.html), official membership, uniqueness, and restriction semantics.
6. SQLite Project, [Indexes on Expressions](https://www.sqlite.org/expridx.html), official expression matching and deterministic-function requirements.
7. SQLite Project, [Deterministic SQL Functions](https://www.sqlite.org/deterministic.html), official corruption/rebuild implications for nondeterministic functions.
8. Oracle, [MySQL 8.4 Optimizer Use of Generated Column Indexes](https://dev.mysql.com/doc/refman/8.4/en/generated-column-index-optimizations.html), current expression/result-type matching rules.
9. Oracle, [MySQL 8.4 CREATE INDEX](https://dev.mysql.com/doc/refman/8.4/en/create-index.html), current functional-key implementation and restrictions.
10. Ramakrishnan and Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, selection predicates, access paths, and constraint foundations.

## Exercises

### Exercise 1

For partial predicate `P: tenant=7 AND deleted_at IS NULL`, classify six queries as implying, not implying, or dependent on planner/parameter domain. Include tenant 7 active, tenant parameter active, tenant 7 unrestricted, tenant 7 deleted, tenant 7 with `NOT(deleted_at IS NOT NULL)`, and tenant 7 active plus status.

### Exercise 2

Trace old/new partial membership and expression maintenance for inserts and updates across false→false, false→true, true→false, true→true unchanged key, and true→true changed normalized key.

### Exercise 3

Design an expression index for a JSON email field. Specify extraction/unquoting, cast/type/length, normalization, collation, NULL/missing behavior, determinism, matching query, collision/recheck, and upgrade/rebuild plan.

### Exercise 4

Design and analyze a partial unique constraint “one active lease per resource,” including predicate, key, concurrent activation, expiration/time, soft deletion, NULL, MVCC, recovery, and why `now()` in the predicate is hazardous.

### Exercise 5

Design a production experiment comparing plain, expression, partial, combined partial-expression, generated-column, and partition/queue-table alternatives for a hot claim workload. State correctness oracle, plan variants, workload variables, evidence, and rollback.

## Answers to the Exercises

### Answer 1

Literal `tenant=7 AND deleted_at IS NULL` implies P. Adding status preserves implication. `tenant=? AND deleted_at IS NULL` does not universally imply `tenant=7` unless the planner has a custom/literal fact that the parameter equals 7 and recognizes it; generic unknown does not. `tenant=7` unrestricted does not imply active. `tenant=7 AND deleted_at IS NOT NULL` contradicts rather than implies P and cannot use it for those rows. `NOT(deleted_at IS NOT NULL)` is semantically equivalent to `deleted_at IS NULL` under SQL, but optimizer recognition is engine/syntax dependent; verify actual planning rather than assuming theorem proving.

### Answer 2

Insert evaluates new P: false creates no entry; true computes E and inserts/checks. false→false needs no entry change unless implementation dependency bookkeeping applies. false→true computes new E, checks uniqueness, and inserts atomically. true→false logically removes the old entry while retaining MVCC visibility as required. true→true with unchanged E/key/payload may avoid index change only if the engine's update optimization proves it; changed E removes/versions old and inserts/checks new. Concurrent operations serialize constraint conflicts under transaction rules; recovery replays the declared old/new membership/value actions idempotently.

### Answer 3

Define a JSON path with missing/JSON-null/SQL-NULL semantics, unquote scalar text, cast to a bounded string type, trim/case-normalize under a fixed named collation, and reject/handle non-string values. Index the exact expression and make queries use the engine-recognized identical form or named generated column. Only deterministic built-ins/fixed settings qualify; record database/collation/function versions. Full normalized value comparison remains the semantic check where the access representation is lossy. Test multibyte limits, absent/null, case, malformed JSON, casts/collation, prepared plans, and upgrades. On dependency change, invalidate/rebuild from base JSON, differential-validate every entry, canary, then cut over with rollback.

### Answer 4

Use unique key `resource_id` with predicate representing a stored, transactionally maintained active state such as `released_at IS NULL`, with explicit NULL and soft-delete rules. Do not use `expires_at>now()` as persistent membership: time passes without a row update, so entries would become stale and `now()` is not immutable. Expiration processing must update stored state. Concurrent activations both attempt predicate entry; the unique-index/transaction protocol permits one and blocks/aborts the other. Old snapshots, logical release, physical cleanup, crash redo, and failover preserve the committed constraint. If multiple NULL resource IDs are allowed, declare that; usually make resource non-NULL. Validate base rows against active index after recovery and lifecycle changes.

### Answer 5

Define exact claim semantics, snapshot/locking, result order, no-double-claim invariant, normalized expression, subset predicate, parameter/prepared forms, and a full-table transactional oracle. Vary table/subset size, transitions, skew/hot tenant, claim batch, cache, visibility/dead rows, write concurrency, failures, and dependency versions. Capture actual custom/generic plans, candidates/rechecks/heap fetches, correctness, index/base pages, expression/predicate CPU, conflicts/waits, WAL/splits/dead tuples, storage, build/rebuild, throughput, and p50/p99. Plain is broad/simple; partial is small but transition-heavy; expression handles computation; combined adds both proof gates; generated column improves matching/ownership; queue table/partition changes data lifecycle and consistency. Canary with shadow result comparison and rollback; choose only when zero false negatives/duplicate claims and declared latency/write/operability thresholds all pass.
