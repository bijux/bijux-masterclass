---
module_id: DBE-062
program: Database Engineering
level: 2
module_number: 62
title: Predicate Pushdown and Projection Pruning
status: complete
last_verified: 2026-08-30
---

# Predicate Pushdown and Projection Pruning

## One-Page Review

### Governing question

How can an optimizer place predicates and eliminate unused columns at the earliest legal boundaries, while preserving SQL bags, null extension, effects, errors, ordering, policies, and source semantics—and while proving that less work actually reaches execution?

### Essential definitions

**Predicate pushdown** moves or derives a filter closer to data production. **Projection pruning** computes the columns required by all ancestors and asks each child for no others. A **required-column set** includes output, predicate, join, group, order, window, correlation, policy, row-identity, and physical columns. A **barrier** is an operator across which a transformation lacks a sound theorem. A predicate is **null-rejecting** for an input when null-extending that input can never make it TRUE. A **sargable** predicate can be mapped to a source access condition. **Partition/file/row-group/page pruning** proves a region cannot contain a match. **Residual filtering** rechecks predicates not fully or exactly enforced below. **Late materialization** delays fetching wide columns until a smaller row-position set survives.

### Central model, mechanism, or theorem

For every operator v, propagate a demand set Req(v) backward from the root. Each operator adds columns needed to compute its own semantics and maps demanded outputs to child inputs. A column may be removed only if no semantic, policy, identity, or physical obligation reaches it. A predicate p may move from above operator F to below it only when `Filter(p,F(X))` is observationally equivalent to `F(Filter(p',X))`, with bindings remapped and effects/calls preserved under the contract. Pushdown is an exact transformation only when the lower layer fully implements p; otherwise it is an opportunistic pruning hint plus a residual exact filter.

### Critical invariants

- Source and rewritten plans return the same schema, bag/order, values, nulls, errors, authorized rows, and promised effects.
- Predicate references are available at the destination and are remapped by stable binding identity.
- Required columns include hidden dependencies: predicates, keys, grouping, sorting, windows, policies, row IDs, delete vectors, and rechecks.
- Outer joins, aggregates, windows, limits, recursion, volatile/throwing expressions, and security boundaries are crossed only by purpose-built guarded rules.
- Metadata pruning may skip only when impossibility is proven; “possibly present” must be scanned and rechecked.
- Approximate indexes such as Bloom filters may yield false positives but not false negatives under their integrity contract.
- Remote/source pushdown is governed by versioned capability, type, null, collation, time-zone, error, authorization, and snapshot compatibility.
- Evidence distinguishes logical row/column reduction from bytes read, decoded, transferred, allocated, and timed.

### Common failures

Failures include pushing a WHERE predicate into the null-supplying side of an outer join; dropping a filter-only or policy column; moving filters across limit/window; pushing HAVING below grouping without group-key proof; trusting min/max metadata with truncated/corrupt/NaN semantics; treating a Bloom “maybe” as a match; claiming row-store I/O savings from logical column pruning; sending sensitive literals remotely; omitting residual filters after inexact pushdown; changing collation/time-zone behavior; pruning row identity needed for update/recheck; or measuring only final row counts.

### Compact example

A six-column event scan ultimately emits customer and amount, but filters tenant and status. Backward liveness therefore requests four columns, not two and not six. If 100,000 rows have modeled widths 289 bytes full versus 25 bytes required, the logical byte opportunity is 28.9 MB versus 2.5 MB (91.35% lower). At 2% selectivity, an exact source filter emits 2,000 rows. These are opportunity calculations, not proof of physical I/O savings.

### Connections

Retrieve [Relational Rewrite Rules](061-relational-rewrite-rules.md), [Joins and Join Semantics](012-joins-and-join-semantics.md), [Composite and Covering Indexes](035-composite-and-covering-indexes.md), and [Heap Files](024-heap-files.md). Continue through [the roadmap](../ROADMAP.md) to statistics, cardinality estimation, costs, join ordering, access paths, columnar analytical databases, and production plan diagnosis.

## Governing Question

The cheapest tuple and byte are often the ones never produced. Predicate pushdown attempts to reject rows before expensive joins, decoding, transfer, and computation. Projection pruning attempts to avoid carrying or materializing columns that cannot influence the observable result. Both sound simple; both become whole-plan semantic analyses in a real SQL engine.

“As early as possible” is not the objective. The correct objective is the earliest legal and profitable boundary under explicit capabilities. A predicate below a left join can manufacture an unmatched row that a WHERE clause would have removed. A filter below LIMIT can select a different population. A column absent from SELECT can still be required by row security, a join, ORDER BY, a window frame, a foreign-data recheck, or an UPDATE row locator. A remote service may spell the same predicate yet implement different collation, time zone, overflow, or null behavior.

This chapter develops two coupled dataflow analyses: predicate placement/derivation and column demand. It then follows their consequences through logical plans, scans, columnar files, partitions, indexes, federated sources, vector execution, security, and evidence. DBE-061 supplied the rule-soundness framework; here every useful transformation is an instance of it.

## Why This Matters

Row reduction compounds. Filtering a fact table before a join can reduce hash probes, join output, exchange bytes, aggregation state, sort volume, memory, spill, and client serialization. Column reduction compounds differently: narrower batches improve cache residency and copying; columnar readers can skip unneeded chunks; remote systems return fewer bytes; late materialization avoids fetching wide payloads for rejected rows.

But logical plan shape and physical work are not identical. A row-oriented heap may still read the full page even if the executor projects two attributes. A columnar file can avoid entire column chunks, yet predicate columns still must be read and metadata may only skip row groups. Compression, encoding, nested reconstruction, page indexes, caches, and object-store request granularity determine actual bytes. Correct reporting names the layer.

Pushdown is also a distributed trust decision. Apache Calcite's current adapter documentation describes planner rules that push operations into sources according to implemented conventions and capabilities. PostgreSQL's FDW interfaces distinguish remotely executable clauses and local rechecks; its documentation notes special complexity when outer joins are pushed down. Apache Arrow's current Dataset API calls filtering opportunistic and requires guarantee-aware residual filtering when only part is enforced. Those designs encode the same principle: lower layers may accelerate a predicate without becoming the final semantic authority unless the contract is exact.

Metadata pruning is a proof of nonexistence. PostgreSQL partition pruning excludes a partition when bounds prove it cannot satisfy the WHERE clause, independently of whether an index exists, and can repeat at execution when parameter values become known. Parquet statistics, dictionaries, page indexes, and Bloom filters can similarly rule out regions. A Bloom filter's useful answer is “definitely absent”; “probably present” still requires reading and exact evaluation.

## Prerequisites and Retrieval

You should understand relational algebra, SQL bags and three-valued logic, inner/outer joins, grouping, windows, order/limit, logical/physical plans, row and column storage, indexes, partitions, vector batches, and function volatility. Recall from DBE-061 that a rewrite is a guarded semantic theorem, not a textual substitution.

Retrieve: predicate references; output lineage; required/delivered schema; null rejection; deterministic/total/leakproof expression; sargability; partition constraint; min/max zone map; dictionary; Bloom false positive; exact versus inexact pushdown; residual predicate; static versus dynamic filter; late materialization; selection vector; row locator; policy column; remote capability; and reproduction envelope.

## Learning Objectives

After this module, you can:

1. derive whole-plan required-column sets backward from root observations;
2. prove legal predicate movement through filters, projections, unions, inner and outer joins, and selected aggregates;
3. identify barriers created by null extension, grouping, windows, limits, recursion, effects, errors, and policies;
4. normalize predicates into sargable access conditions without changing type/collation/null semantics;
5. distinguish logical pushdown from partition, file, row-group, page, index, and remote pruning;
6. design exact, inexact, and residual-filter capability contracts;
7. combine projection pruning with late materialization and row-position reconciliation;
8. verify row, column, byte, decode, transfer, memory, spill, and latency effects independently;
9. test rewrites with finite counterexamples, generated differential queries, metadata corruption, and capability mismatch; and
10. operate pushdown safely with privacy, observability, budgets, canaries, and fallback.

## Core Exposition

**Compute column demand backward.** Begin at the root with columns observable to the consumer plus columns required to establish requested order or identity. For each operator, map required outputs to child inputs and add local semantic dependencies.

- A filter preserves demanded outputs and adds every column referenced by its predicate.
- A projection maps demanded aliases/expressions to their transitive input references; unused expressions may disappear only if their evaluation is unobservable.
- A join splits demanded outputs by child and adds join predicates, residuals, correlation parameters, and row identity needed by join/recheck.
- An aggregate adds group keys and arguments/filter/order expressions of demanded aggregate outputs.
- A window adds partition keys, order keys, frame dependencies, and arguments.
- Sort/limit preserve demanded outputs and add sort expressions; update/delete add target row locators and concurrency recheck data.
- Scans add policy, partition, generated-column, visibility, delete-vector, and format-specific dependencies.

This is liveness analysis over a relational IR. Names alone are unsafe: use stable binding IDs and typed expression lineage. Nested values may admit path-level pruning, but reconstructing a parent struct/list can require repetition/definition levels, offsets, validity, or sibling metadata even when one leaf is selected.

Projection pruning is semantics-preserving only when removing an expression cannot change errors, volatile calls, audit effects, or timing promises. SQL engines often permit substantial evaluation reordering, but an optimizer must follow its exact language and extension contract. Security expressions are never “unused” merely because they are absent from output.

**Split and place predicates by conjunct.** A conjunction often becomes individually placeable predicates. Compute each conjunct's referenced bindings, volatility/totality, null behavior, correlation, policy class, estimated cost/selectivity, and source capabilities. Place independently; retain original order only if the semantic contract requires it. Do not split constructs whose error/effect behavior makes independent evaluation observable.

Through a projection, substitute output expressions into the predicate only when the expressions are binding-safe and duplication/movement is legal. A predicate on a simple renamed column is easy. A predicate on `price_with_tax` may become arithmetic with different overflow/rounding or may duplicate an expensive expression. Sometimes materializing once is preferable.

Through `UNION ALL`, a predicate can commonly be copied into every branch after schema remapping. Copying a volatile or stateful predicate changes call scheduling and potentially results. `UNION DISTINCT`, INTERSECT, and EXCEPT add duplicate/membership semantics; branch pushdown requires a theorem for the specific operator and predicate.

Through an inner join, a conjunct referencing only one input can usually move to that input; a conjunct referencing both remains a join predicate. Equality can derive transitive filters—if `R.k=S.k` and R.k is restricted to `[10,20]`, an equivalent compatible restriction on S.k may aid pruning. Derivation must preserve types, casts, collation, null rules, and domain bounds.

Outer joins require matched/unmatched case analysis. A predicate in ON is not a WHERE predicate. Moving a WHERE predicate into the preserved side can change which rows participate; moving one into the null-supplying side can retain null-extended rows that WHERE rejected. A null-rejecting predicate above a left join may justify converting to inner join and then pushing, with exact binding/effect guards. Semi and anti joins also have specialized rules because they observe existence rather than joined multiplicity.

Aggregation is a barrier except for proven cases. A HAVING predicate using only group keys can often move before grouping because every row in one group shares those keys. A predicate on `SUM(x)` cannot. Grouping sets, empty-input aggregates, null grouping, and volatile/set-returning expressions complicate the rule. Windows normally require the full partition and order before computing row-relative values; filtering on a window result cannot move below the window. LIMIT/OFFSET and top-k select a population, so arbitrary filters cannot cross them.

**Normalize for access without losing meaning.** A source can exploit predicates in forms it recognizes: direct range/equality on indexed or partition columns, compatible prefix/LIKE patterns, spatial bounds, or format-supported expressions. Rewrite `date(ts)=D` to a half-open timestamp range only with correct time zone, calendar, precision, and function semantics. Avoid implicit casts on the indexed column when a safe cast of the literal is possible. Sargability is capability-relative, not a universal syntactic property.

Separate the original predicate from access predicates. An index condition, partition bound, or min/max test may return a superset. Keep a residual exact filter for lossy indexes, collation differences, rechecks, false positives, or only partially pushed conjunctions. Tag each conjunct as exact, inexact, unsupported, or unsafe, and reconcile source guarantees per batch/fragment.

**Understand pruning layers.** Logical filter pushdown changes operator placement. Partition pruning proves a partition impossible from declarative bounds. File pruning uses directory/manifest partition facts or file statistics. Row-group/page pruning uses format metadata. Index access locates candidate rows. Vector filtering creates selection vectors. Dynamic filters communicate runtime bounds or membership summaries from joins/top-k/aggregates to active scans. Remote pushdown serializes work to another engine. Each layer has different evidence and failure modes.

Metadata must be conservative. Min/max can skip a region only if the predicate cannot be TRUE for any value consistent with metadata, including null/NaN/collation/truncation rules. Dictionaries can prove absence when complete. Bloom filters intentionally overapproximate membership: false positives cost work, false negatives would corrupt results. Parquet's current Bloom-filter specification describes “definitely no” versus “probably yes” and calls out encryption for sensitive-column filters.

Static pruning uses constants known at planning. Initialization pruning uses bound parameters. Dynamic pruning can react to nested-loop parameters, join-build values, or tightening top-k thresholds. Dynamic state needs version/epoch, monotonicity, thread-safe publication, bounded memory, cancellation, and correctness under late arrival. A filter arriving late may reduce future work but cannot retract already emitted rows unless the algorithm accounts for it.

**Couple projection with materialization.** In a columnar scan, request predicate columns first, evaluate/prune, then materialize projected payload columns only for surviving row positions when the reader supports it. Preserve position mapping across pages, nested encodings, deletes, and batches. Sparse selection may make gathers expensive; dense selections may favor decoding whole vectors. Row stores may still benefit from narrower executor tuples and covering indexes even if heap-page bytes remain unchanged.

The executable performs a small backward-demand and opportunity calculation. It does not model a storage engine.

<!-- bijux-verify: {"id":"scan-demand-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"scan_columns=('tenant_id', 'customer_id', 'amount', 'status')\npruned_columns=('created_at', 'payload')\nfull_width_bytes=289\nrequired_width_bytes=25\nfull_logical_mb=28.900\nrequired_logical_mb=2.500\nlogical_width_reduction_pct=91.35\ninput_rows=100000\nsource_filtered_rows=2000\nsource_row_reduction_pct=98.00\nevidence=logical_opportunity_not_physical_io\n","stderr":""}} -->
```python
schema_widths = {
    "tenant_id": 8,
    "customer_id": 8,
    "amount": 8,
    "status": 1,
    "created_at": 8,
    "payload": 256,
}
root_outputs = {"customer_id", "amount"}
filter_references = {"tenant_id", "status"}
scan_columns = tuple(name for name in schema_widths if name in root_outputs | filter_references)
pruned_columns = tuple(name for name in schema_widths if name not in scan_columns)

full_width = sum(schema_widths.values())
required_width = sum(schema_widths[name] for name in scan_columns)
rows = 100_000
selectivity = 0.02
filtered_rows = int(rows * selectivity)

print(f"scan_columns={scan_columns}")
print(f"pruned_columns={pruned_columns}")
print(f"full_width_bytes={full_width}")
print(f"required_width_bytes={required_width}")
print(f"full_logical_mb={rows * full_width / 1_000_000:.3f}")
print(f"required_logical_mb={rows * required_width / 1_000_000:.3f}")
print(f"logical_width_reduction_pct={(1 - required_width / full_width) * 100:.2f}")
print(f"input_rows={rows}")
print(f"source_filtered_rows={filtered_rows}")
print(f"source_row_reduction_pct={(1 - selectivity) * 100:.2f}")
print("evidence=logical_opportunity_not_physical_io")
```

The model's 2.5 MB assumes fixed logical widths and counts all input rows before filtering. A late-materializing columnar reader might read predicate columns for many rows but payload columns for survivors; a row store might read the same pages but build narrower tuples. Compression, metadata, alignment, encoding, cache, and requests invalidate direct physical-byte inference.

**Federation requires negotiated semantics.** A pushdown contract should identify supported operators/functions/casts, null and NaN behavior, collation, time zone/calendar, precision/overflow, parameter binding, authorization identity, snapshot/isolation, error mapping, result ordering, maximum expression size, and whether enforcement is exact. Version this contract and test it against the source. PostgreSQL 18's `postgres_fdw` documentation describes remote-estimate and shippability controls and notes that local and remote servers should have compatible settings; its FDW callbacks preserve local recheck paths, especially for outer joins.

Pushdown can leak. A remote predicate exposes column names, constants, distributions, and query intent; metadata indexes and Bloom filters may reveal membership information. Apply data classification, tenant isolation, encryption, least privilege, redaction, and audit. Do not push a local row-policy expression to a source that cannot enforce it with the same authenticated principal and semantics.

**Prove benefit with layered measurements.** Record source/rewritten logical plans and digests; predicate placement and exactness; required/delivered columns; partitions/files/row groups/pages considered/skipped; columns/chunks read; compressed/uncompressed bytes; decoded values; rows before/after each filter; false-positive/recheck counts; remote requests/bytes/CPU; batch density; peak memory/spill; planning time/memory; and end-to-end latency/throughput under repeated representative load.

Hold data version, statistics, parameters, cache, concurrency, and software constant. Validate results first. A plan with more pruning metadata work may lose on small inputs. An expensive low-selectivity predicate may be cheaper after a simple selective predicate even if both are legal at the scan. Remote CPU or request fan-out can offset transfer savings. Cost-based placement belongs after semantic eligibility.

Operate with rule-level counters and privacy-safe traces: eligible/pushed/residual conjuncts, required/pruned columns, capability rejection reasons, metadata skip ratios, dynamic-filter arrival/use, planning budget, and fallback. Canary by fingerprint/source/version, compare result digests when safe, and keep a kill switch. Metadata corruption or capability drift must fail conservative—scan and recheck—not silently skip.

## Definitions and Notation

- **Req(v)**: set of bound columns demanded from operator v by ancestors plus v's local semantics.
- **Refs(e)**: bound input columns referenced transitively by expression e.
- **Exact pushdown**: lower layer enforces the complete predicate under equivalent semantics.
- **Inexact pushdown**: lower layer returns a conservative candidate superset.
- **Residual**: exact local predicate applied after inexact/partial lower filtering.
- **Barrier**: operator/policy boundary without a sound movement rule for the predicate.
- **Sargable**: expressible as an exploitable search/access condition for a named capability.
- **Pruning**: excluding a region after proving it cannot contain a qualifying row.
- **Static/dynamic filter**: filter known before execution / derived or bound during execution.
- **Selection vector**: ordered row positions surviving a vector predicate.
- **Late materialization**: delayed fetch/decode of projected values using surviving positions.
- **False positive**: candidate retained by approximate metadata but rejected exactly.
- **False negative**: qualifying candidate incorrectly skipped; forbidden for sound pruning.

For a filter, child demand is `Req(child)=Req(filter) union Refs(predicate)`. For a simple projection mapping outputs y to expressions e_y, child demand is the union of `Refs(e_y)` for demanded y, plus dependencies of semantically observable unused expressions. More complex operators add their own equations.

## Mechanisms, Invariants, or Proof Structure

**Demand fixed point.** Seed root observations; propagate demand backward until sets stop growing. Monotone finite set union terminates. Validate every expression reference is available at its evaluation site and every scan request is supported. For DAG/shared subplans, union demands from all parents; pruning for one consumer cannot starve another.

**Predicate-placement proof.** Partition inputs by operator semantics. For inner join, show a one-sided pure predicate accepts the same joined pairs whether evaluated before or after. For left join, split matched and unmatched left rows; null extension exposes the counterexample and the null-rejecting guard for outer-to-inner conversion. For grouping, prove group-key constancy; for limit/window, exhibit population/order counterexamples unless a stronger theorem applies.

**Conservative metadata proof.** Let M describe a superset of values possible in region G. Skip G only if no value allowed by M can make p TRUE. Incomplete metadata yields “unknown,” never “skip.” Approximate membership may keep extra regions. Integrity/version/schema mismatch disables pruning or fails safely according to policy.

**Residual invariant.** Decompose p into exact pushed E, inexact/partial hint H, and local residual R such that every row satisfying p survives H and `E AND R` is equivalent to p for returned candidates. Source guarantees are evidence, not assumptions; absent guarantees, re-evaluate locally.

**Position invariant.** Late materialization maintains a stable mapping from logical row occurrence to fragment/page/vector position through deletes, nulls, nested encoding, and selection composition. Gathered payload values must align one-for-one and in order with surviving rows.

**Security invariant.** Required-column analysis never removes authorization/masking/audit dependencies. Predicate movement cannot cross a policy boundary unless the policy model proves equivalence and nonleakage. Remote serialization follows data-classification and principal rules.

**Evidence invariant.** Report reduction at the measured layer. Logical width is not bytes read; skipped row groups are not skipped rows; buffer hits are not storage reads; remote returned bytes exclude remote scan work. Performance claims include controls and distributions.

## Alternatives and Trade-Offs

**Early eager filtering** reduces downstream rows but may decode costly predicate columns and destroy vector density. **Cost-ordered filtering** evaluates cheap/selective predicates first but needs stable semantics and estimates.

**Early projection** narrows tuples and transfer. **Late materialization** can avoid payload decode for rejected rows but adds position vectors, random gathers, and nested reconstruction complexity.

**Metadata pruning** is cheap and conservative but coarse. **Indexes** give finer candidate access at maintenance/storage cost. **Full scans** can win for high selectivity, small/cached data, or sequential bandwidth.

**Static filters** are ready before scanning. **Dynamic filters** exploit runtime values and adaptive thresholds but may arrive late, consume memory/network, and require concurrency-safe monotone publication.

**Remote pushdown** saves transfer and uses source capabilities. **Local evaluation** preserves one semantic authority and observability but may move far more data. Hybrid inexact pushdown plus residual is common.

**Rule-based eligibility** is auditable. **Cost-based placement** handles expensive predicates and physical trade-offs but inherits estimate errors. Use rules for legality and costs for choice.

## Failure Modes and Misconceptions

1. “Earlier is always faster” ignores expression cost, vector density, cache, and remote overhead.
2. “SELECT lists define required columns” omits predicates, keys, order, policy, identity, and recheck.
3. “Pushdown means exact enforcement” confuses opportunistic pruning with semantic filtering.
4. “Bloom match means present” reverses the one-sided guarantee.
5. “Min/max inside range means scan can answer” only means a match is possible.
6. “Outer joins are inner joins with nulls” ignores match absence and ON/WHERE placement.
7. “HAVING is just WHERE” ignores group formation and aggregate semantics.
8. “Filter below LIMIT is equivalent” changes the selected population.
9. “Pruned columns save disk bytes” depends on row/column layout, indexes, compression, and cache.
10. “Same SQL remotely means same result” ignores types, collation, time zones, errors, and policies.
11. “Dynamic filters are harmless hints” stale or nonconservative filters can lose rows.
12. “Unused volatile expressions may be deleted” call/error effects may be observable.
13. “A plan proves physical reduction” only execution counters at named layers do.
14. “Pruning failure should fail closed by skipping” correctness-safe fallback is usually scan plus exact recheck.

## Worked Examples

### Example 1

**Backward column demand.** Final output needs customer and amount; filter needs tenant and status; scan also stores timestamp and payload. Demand is `{tenant,customer,amount,status}` and the latter two columns are prunable. Conclusion: filter-only columns remain required even when absent from output.

### Example 2

**Projection through an alias.** Project defines `gross=net+tax`; parent filters `gross>100`. Substitution can push `net+tax>100` only if numeric type, overflow, nulls, and evaluation multiplicity agree. Conclusion: lineage enables movement, but expression semantics guard it.

### Example 3

**Inner-join placement.** `Orders JOIN Customers ON customer_id` followed by `Orders.status='open'` can filter Orders first under pure predicate semantics. Every surviving joined pair has an open order in both forms. Conclusion: one-sided inner-join predicates are canonical pushdown candidates.

### Example 4

**Outer-join counterexample.** With left keys 1,2 and one right match for 1, WHERE `right.flag='x'` removes key 2; filtering right first then left joining retains key 2/null. Conclusion: pushdown without outer-to-inner proof is wrong.

### Example 5

**Group-key HAVING.** `GROUP BY region HAVING region='SE'` can filter region before grouping because every member of a group shares region. `HAVING SUM(amount)>1000` cannot. Conclusion: group-key dependency, not clause spelling, determines eligibility.

### Example 6

**Partition pruning with a parameter.** Monthly partitions cannot be statically removed for an unbound date parameter. Once bound, initialization or execution pruning can prove months outside its range impossible. Conclusion: delayed knowledge changes pruning time, not query meaning.

### Example 7

**Parquet Bloom behavior.** A filter for customer 42 queries a row-group Bloom filter. “Definitely no” permits skipping; “probably yes” requires reading and exact comparison. Conclusion: false positives affect performance, while any false negative violates correctness.

### Example 8

**Late materialization.** Read status for 1,000,000 rows; 1% survive; then gather 4 KB payloads for 10,000 positions. This can avoid decoding most payloads, but sparse gathers and object-store ranges may dominate. Conclusion: measure bytes, requests, decode, and gather—not just logical width.

### Example 9

**Remote semantic mismatch.** Local text comparison uses one collation; remote source uses another. Pushing `name<'z'` can change membership/order. Mark it unsupported or inexact and recheck a conservative superset locally. Conclusion: capability negotiation includes semantic environment, not only operator names.

### Example 10

**Production regression.** A release shows fewer rows and 90% fewer scanned row groups. Investigation finds truncated string min/max metadata was treated as exact. Disable metadata pruning, restore results, minimize the counterexample, repair conservative bound logic, fuzz prefixes/collations/nulls, canary, and retain residual checks. Conclusion: spectacular skip ratios are not success without semantic reconciliation.

## Cross-Program Connections

- [Functional Programming](../../03-programming-languages-functional-programming/ROADMAP.md): purity, totality, substitution, and equational reasoning govern legal movement.
- [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md): backward liveness, dataflow fixed points, alias/binding identity, and effect barriers mirror IR optimization.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md): Bloom filters, bitmaps, selection vectors, tries, and interval structures implement pruning evidence.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): columnar lakes, manifests, partition evolution, schema evolution, and distributed scans operationalize pushdown.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): ownership, classification, policy, lineage, and federation constrain remote movement.
- [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md): capability negotiation and backward-compatible semantic contracts apply to query connectors.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): tenant isolation, budgets, observability, rollout, and kill switches make optimizer features operable.

## References

1. Hamid Pirahesh, Joseph M. Hellerstein, and Waqar Hasan, [“Extensible/Rule Based Query Rewrite Optimization in Starburst”](https://research.ibm.com/publications/extensiblerule-based-query-rewrite-optimization-in-starburst), *SIGMOD 1992*. Primary rule-based query-rewrite foundation including predicate movement and projection work.
2. Apache Calcite Project, [Algebra](https://calcite.apache.org/docs/algebra.html), retrieved 2026-08-30. Current relational expression, filter, projection, and planner-rule documentation.
3. Apache Calcite Project, [Adapters](https://calcite.apache.org/docs/adapter), retrieved 2026-08-30. Current source pushdown, convention, capability, metadata, and cost documentation.
4. PostgreSQL Global Development Group, [PostgreSQL 18: Expression Evaluation Rules](https://www.postgresql.org/docs/18/sql-expressions.html#SYNTAX-EXPRESS-EVAL), retrieved 2026-08-30. Current reordering, side-effect, and error constraints.
5. PostgreSQL Global Development Group, [PostgreSQL 18: Table Partitioning—Partition Pruning](https://www.postgresql.org/docs/18/ddl-partitioning.html#DDL-PARTITION-PRUNING), retrieved 2026-08-30. Current planning, initialization, and execution pruning behavior.
6. PostgreSQL Global Development Group, [PostgreSQL 18: Foreign Data Wrapper Callback Routines](https://www.postgresql.org/docs/18/fdw-callbacks.html), retrieved 2026-08-30. Current remote-clause, recheck, and outer-join pushdown interfaces.
7. PostgreSQL Global Development Group, [PostgreSQL 18: `postgres_fdw`](https://www.postgresql.org/docs/18/postgres-fdw.html), retrieved 2026-08-30. Current remote optimization, shippability, execution environment, and cross-version constraints.
8. Apache Arrow Project, [Tabular Datasets](https://arrow.apache.org/docs/cpp/dataset.html), retrieved 2026-08-30. Current projection/filter pushdown and necessary-column behavior.
9. Apache Parquet Project, [Parquet Bloom Filter](https://parquet.apache.org/docs/file-format/bloomfilter/), retrieved 2026-08-30. Official one-sided membership and sensitive-column encryption specification.
10. DuckDB Foundation, [Overview of DuckDB Internals](https://duckdb.org/docs/current/internals/overview.html), retrieved 2026-08-30. Current expression rewriting, filter pushdown, equivalence-derived filters, and logical/physical pipeline.
11. Sergey Melnik et al., [“Dremel: Interactive Analysis of Web-Scale Datasets”](https://www.vldb.org/pvldb/vol3/R29.pdf), *PVLDB* 3(1), 2010. Primary nested columnar representation and selective analytical execution foundation.

## Exercises

### Exercise 1

Give backward required-column equations for filter, simple projection, inner join, aggregate, window, and scan. Name at least four hidden scan dependencies.

### Exercise 2

Prove one-sided predicate pushdown through an inner join under bag semantics, then construct the corresponding left-join counterexample and state a sufficient guarded repair.

### Exercise 3

A Parquet scan reports 99% row-group pruning but reads nearly the same bytes and is slower. Give a layered diagnosis covering metadata, columns, encoding, selectivity, late materialization, requests, cache, and counters.

### Exercise 4

Design a capability contract for pushing predicates/projections to a remote source with different software versions and collation. Specify exact/inexact/unsupported outcomes and residual behavior.

### Exercise 5

Design an elite release gate for dynamic join filters and nested-column late materialization in a multitenant engine, including proofs, generated tests, concurrency, corruption, security, performance, rollout, and limitations.

## Answers to the Exercises

### Answer 1

For filter p, child demand is parent demand union `Refs(p)`. For projection outputs `y=e_y`, child demand is the union of `Refs(e_y)` for demanded y, plus any effectful/error-observable expressions. For inner join, split demanded outputs by child and add join/residual/correlation references to each side. For aggregate, add group keys and arguments/filter/order dependencies of demanded aggregates. For window, add partition/order/frame/argument references. At scan, request the accumulated set plus hidden necessities. These include row-security/masking columns, MVCC/visibility or row locators, delete-vector/position data, partition/generated-column dependencies, recheck columns, nested offsets/validity/repetition metadata, and source-specific physical keys. Shared subplans union demand from every parent.

### Answer 2

For bags R,S and pure total p referencing only R, each joined pair `(r,s)` appears with multiplicity `m_R(r)*m_S(s)` when join condition j is TRUE. Filtering after join retains it iff p(r) is TRUE. Filtering R first sets `m_R(r)` to zero exactly when p is not TRUE, producing identical retained pairs and multiplicities. Stable bindings/types/null semantics and no effect/policy barrier are premises. For left join with R keys 1,2 and S `(1,x)`, WHERE `S.value='x'` returns only `(1,x)`; filtering S first then left joining also returns `(2,NULL)`. A sufficient repair is convert to inner join and push when the above predicate is proven null-rejecting for S and pure/total, with ON/WHERE, schema, and policy semantics preserved.

### Answer 3

First validate equal results and plan/filter identity. Count files, row groups, pages, and rows skipped—not only a percentage whose denominator may be tiny. Determine which columns/chunks are still read: predicate columns, wide projected columns, nested parents/offsets, deletes, or footer/index data. Check whether “pruned” groups had few bytes while survivors were huge; whether compression makes logical width misleading; whether the predicate is high-selectivity inside surviving groups; whether late materialization actually defers payload decode; and whether sparse gathers inflate CPU. Measure object-store requests/ranges, retries, footer/cache hits, compressed/uncompressed bytes, decode values/time, selection density, allocations, and concurrency. Compare warm/cold repeated controls with pruning disabled and isolate metadata CPU. The 99% figure can coexist with similar bytes when one surviving group dominates or when projection/requests defeat physical savings.

### Answer 4

Version the source and connector; define types/casts, null/NaN, collation, time zone/calendar, precision/overflow, supported functions/operators, parameter binding, errors, ordering, authorization principal/policies, snapshot/isolation, expression limits, and projected nested paths. For each conjunct/column return: exact (source fully enforces equivalent semantics; no local predicate needed except defensive policy), inexact (source returns a proven superset plus a per-batch guarantee; retain exact local residual), unsupported (evaluate locally and fetch its dependencies), or unsafe (do not serialize because semantics/security cannot be established). A different collation makes text ranges unsafe or at best conservatively inexact; never call them exact. Bind output lineage and required columns, include residual/recheck fields, test across version pairs, and fall back to local scan/evaluation on unknown capabilities.

### Answer 5

Prove dynamic filter conservatism: published membership/range state may retain extras but cannot reject a future valid join match; define epochs, monotonic updates, build completeness, outer/semi/anti join restrictions, late arrival, cancellation, and retry. Prove nested position mapping through repetition/definition levels, nulls, pages, batches, deletes, and gathers. Exhaustively test empty/duplicate/null/skewed bags and nested shapes; generate differential plans with filters arriving before/during/after scan; fuzz metadata, corrupt/truncate indexes, reorder tasks, inject cancellation/retry, and verify conservative fallback. Test policy columns, tenant isolation, encrypted metadata, literal leakage, principals, and remote capabilities. Benchmark planning/memory, filter build/network, row-group/page/column bytes, decode/gather, selection density, peak memory/spill, throughput/tails, and concurrency against controls. Cap filter size/time, validate epochs/checksums, expose privacy-safe counters, canary by tenant/fingerprint with result reconciliation, and keep independent switches for dynamic filtering and late materialization. State that internal proofs and tests cover the modeled engine/version, not arbitrary formats, corruptions, sources, policies, workloads, or deployment fitness; named external review is required before claiming it.
