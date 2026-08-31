---
module_id: DBE-055
program: Database Engineering
level: 2
module_number: 55
title: Single-Node Sort-Merge Joins
status: complete
last_verified: 2026-08-30
---

# Single-Node Sort-Merge Joins

## One-Page Review

### Governing question

How can one database node exploit compatible input order to join bags correctly—especially duplicate key groups, NULLs, residual predicates, and unmatched rows—while accounting for sorting, spill, rewind, and delivered order?

### Essential definitions

A **merge join** advances two inputs ordered by compatible join keys. If one key is smaller, it advances that side; if keys compare equal, it emits all TRUE-qualified pairs from the two equal-key groups. A **sort-merge join** first sorts inputs that do not already deliver the required order. An **equality band/group** is the consecutive run of occurrences equal under join semantics. **Mark/restore** records a position in one input so a duplicate group can be replayed. A **materialized group** stores a duplicate band in memory or temporary storage. A **run** is an ordered sequence produced by an external-sort pass. **Interesting order** is an input/output order useful to other operators. **Residual qualification** is any join condition not discharged by key comparison.

### Central model, mechanism, or theorem

With total, mutually compatible sort comparators and join equality, ordered inputs partition into key groups. Unequal leading groups cannot match and may advance safely; equal groups contain every possible equality pair for that key. Their Cartesian product, followed by residual qualification, yields correct bag multiplicity. Outer/semi/anti variants additionally track per-occurrence matches and emit unmatched rows at the right transition. If sorting is required, correctness composes from sort permutation preservation plus merge correctness; cost includes sorting and spill, not just the linear merge pass.

### Critical invariants

- Both streams use compatible type, coercion, collation, direction, and NULL ordering for the merge key.
- Join equality and ordering agree: values that join equal occupy the same consecutive equality band.
- Each input occurrence is retained; duplicate groups produce the full cross product unless join kind permits existence-only output.
- Residual predicates determine matched state where required, not key equality alone.
- NULL behavior follows the join comparator: ordinary `=` produces no NULL match even if sort order colocates NULLs.
- Mark/restore or group materialization replays exactly the intended band and releases bounded resources.
- Outer/full unmatched emission occurs once per row occurrence and only after absence is established.
- Any claimed output ordering describes exact keys, direction, NULL placement, collation, and tie behavior.

### Common failures

Failures include merging streams sorted under different collations; treating equal sort position as TRUE SQL equality; advancing once through duplicate keys and losing the cross product; marking rows matched before residual qualification; emitting an unmatched row before the opposite equal-key group is exhausted; assuming sorting is always in memory; forgetting that two sorts can dominate the join; claiming stable tie order; trusting an index order that does not match direction/NULL rules; retaining an unbounded duplicate group; and forcing merge when skewed equality bands generate enormous output.

### Compact example

Two left key-1 occurrences and two right key-1 occurrences yield four pairs; key 4 yields one. Left key 2 and left NULL are unmatched; right key 3 and right NULL are unmatched. A group-aware merge compares only four leading non-null keys, but it still emits five inner occurrences and must materialize or replay duplicate bands. The executable proves this finite case, not arbitrary SQL comparators, external sorting, or engine behavior.

### Connections

Retrieve [Joins and Join Semantics](012-joins-and-join-semantics.md), [B+ Tree Search and Range Scan](032-b-tree-search-and-range-scan.md), [Logical and Physical Plans](051-logical-and-physical-plans.md), [Sequential and Index Scans](052-sequential-and-index-scans.md), [Nested-Loop Joins](053-nested-loop-joins.md), and [Hash Joins](054-hash-joins.md). Continue through the Database Engineering [roadmap](../ROADMAP.md) to aggregation and external sorting.

## Governing Question

What ordering, equality-band, state-machine, memory, and spill proofs make a single-node sort-merge join semantically correct and operationally preferable?

## Why This Matters

Merge join converts order into progress. Once both inputs are compatibly ordered, the executor can discard whole prefixes from further consideration: a smaller key cannot match a larger current key or anything later on that side. The merge pass is linear in input occurrences plus output, supports broad joins without a build hash table, and can preserve useful order for downstream grouping, windows, merge joins, or final presentation.

Order is not free. Inputs may require full or incremental sorts, each with memory, temporary I/O, CPU comparisons, and startup latency. Persistent indexes can supply order but may cause scattered base-row fetches. One side might already be ordered while the other sorts. An optimizer must compare the global plan: hash plus final sort, merge using existing order, or nested loop with an ordered index can trade different startup, total cost, memory, and delivered properties.

Duplicate groups are the semantic center. A merge that advances both sides after one equal pair implements set-like behavior and is wrong for SQL bags. For left group size (m) and right group size (n), an inner equality join has (mn) candidate pairs before residual filtering. Implementations mark and restore one input, materialize a band, or buffer both groups. A single heavy key can therefore dominate memory, replays, CPU, and unavoidable output despite otherwise linear scanning.

NULLs and collations separate physical order from join truth. Sorts place NULLs somewhere; ordinary SQL equality still evaluates NULL comparisons as UNKNOWN. Nondeterministic collations may consider strings equal for ordering/search purposes under documented semantics, and every operator must use compatible comparison support. Mixing indexes, sorts, or workers built with incompatible collation versions risks wrong grouping or invalid order claims.

## Prerequisites and Retrieval

You should understand SQL bag/null join semantics, total ordering and equality, indexes, internal/external sorting, iterators, pages, snapshots, physical properties, and join cost models. Retrieve merge key, comparator, equality band, mark/restore, rewindability, materialize, run generation, merge fan-in, spill, residual qualification, matched flag, null extension, interesting order, startup/total cost, incremental sort, and deterministic tie-breaker.

DBE-054 specialized equality through hashing. This module instead specializes compatible ordered comparison on one node. DBE-057 will study external sorting and spill in depth; here those mechanisms are included only enough to price and verify the join.

## Learning Objectives

After this module, you can:

1. derive merge progress from compatible sorted-stream invariants;
2. implement duplicate-band inner, outer, semi, and anti joins under bag/null semantics;
3. distinguish sort comparison, join equality, residual qualification, and presentation order;
4. compare mark/restore, one-band materialization, and symmetric group buffering;
5. derive linear merge work and external-sort page-I/O approximations;
6. reason about index-delivered, explicit, incremental, and partially useful ordering;
7. diagnose sort spill, duplicate skew, comparison cost, estimate error, and output explosion;
8. state which output order a merge join can and cannot deliver;
9. test comparator compatibility, duplicates, NULLs, spills, cancellation, and faults; and
10. choose merge versus hash or nested loop using global workload evidence.

## Core Exposition

**Define the comparators first.** Let left bag (L), right bag (R), join equality ∼, and ordering comparator (cmp). A correct equi-merge requires values equal under join semantics to form one contiguous band in both sorted streams. Operationally, (l∼r) must be compatible with `cmp(l,r)=0`, while any order-equivalent values that are not a TRUE join match must still receive full equality/residual recheck. Types, coercions, collations, directions, and NULL policy must agree.

For ordinary SQL `=`, a NULL key produces UNKNOWN rather than TRUE. Sorting NULLs first or last makes them traversable but not matching. Null-safe equality is a different operator whose comparator/grouping must deliberately treat NULLs as one equality class. Composite keys apply component semantics lexicographically, including direction and NULL placement per component.

**The distinct-key merge is simple.** Read current non-null keys (l) and (r). If (l<r), no current or future right key can equal (l), so advance left (emitting it as unmatched if the join kind preserves it). If (l>r), symmetrically advance right. If they compare equal, evaluate full equality and qualification, emit as required, then advance. Exhaustion permits remaining rows only for the preserved sides.

The safety argument depends on monotonicity. When (l<r), every future right key is at least (r), hence greater than (l); discarding (l) cannot omit an equal pair. This proof fails if streams are not ordered under the same comparator, the comparator changes mid-query, or an expression is volatile.

**Duplicate bands require a cross product.** When current keys compare equal, collect the maximal left group (G_L(k)) and right group (G_R(k)). For inner join, test all |(G_L)||(G_R)| pairs and emit those whose equality/residual qualification is TRUE. This is not an avoidable algorithmic defect: bag semantics demand the pairs. Semi join can emit each qualifying left occurrence once after any TRUE pair; anti emits only left occurrences with no TRUE pair. Outer/full joins require per-occurrence match flags because a residual may match some rows in the same key band and not others.

An iterator may mark the first right row and restore for every additional left duplicate. This keeps little explicit state but requires a rewindable right path and can repeat reads. Materializing the smaller/right equality band allows replay from memory or spill. Buffering both bands simplifies full-outer residual tracking but can consume more memory. Adaptive band handling must preserve occurrence identity during a switch.

The executable below performs group-aware merge on finite sorted non-null inputs, handles ordinary NULL equality separately as unmatched, and derives inner/left/full/semi/anti output. It deliberately excludes SQL type/collation complexity, MVCC, sorting/spill, faults, and performance.

<!-- bijux-verify: {"id":"sort-merge-duplicate-band-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"inner_rows=(('A', 'x'), ('A', 'y'), ('A2', 'x'), ('A2', 'y'), ('C', 'w'))\nleft_rows=(('A', 'x'), ('A', 'y'), ('A2', 'x'), ('A2', 'y'), ('B', None), ('C', 'w'), ('N', None))\nfull_rows=(('A', 'x'), ('A', 'y'), ('A2', 'x'), ('A2', 'y'), ('B', None), (None, 'z'), ('C', 'w'), ('N', None), (None, 'N2'))\nsemi_rows=('A', 'A2', 'C')\nanti_rows=('B', 'N')\nleading_key_comparisons=4\ninner_multiplicity=5\nevidence=finite_duplicate_band_merge\n","stderr":""}} -->
```python
left = (("A", 1), ("A2", 1), ("B", 2), ("C", 4), ("N", None))
right = (("x", 1), ("y", 1), ("z", 3), ("w", 4), ("N2", None))


def groups(rows):
    result = []
    for name, key in sorted((row for row in rows if row[1] is not None), key=lambda row: row[1]):
        if not result or result[-1][0] != key:
            result.append((key, []))
        result[-1][1].append(name)
    return result


lg, rg = groups(left), groups(right)
i = j = comparisons = 0
inner = []
left_out = []
full = []
semi = []
anti = []

while i < len(lg) and j < len(rg):
    lk, lnames = lg[i]
    rk, rnames = rg[j]
    comparisons += 1
    if lk < rk:
        left_out.extend((name, None) for name in lnames)
        full.extend((name, None) for name in lnames)
        anti.extend(lnames)
        i += 1
    elif lk > rk:
        full.extend((None, name) for name in rnames)
        j += 1
    else:
        pairs = [(lname, rname) for lname in lnames for rname in rnames]
        inner.extend(pairs)
        left_out.extend(pairs)
        full.extend(pairs)
        semi.extend(lnames)
        i += 1
        j += 1

for _, lnames in lg[i:]:
    left_out.extend((name, None) for name in lnames)
    full.extend((name, None) for name in lnames)
    anti.extend(lnames)
for _, rnames in rg[j:]:
    full.extend((None, name) for name in rnames)
for name, key in left:
    if key is None:
        left_out.append((name, None)); full.append((name, None)); anti.append(name)
for name, key in right:
    if key is None:
        full.append((None, name))

print(f"inner_rows={tuple(inner)}")
print(f"left_rows={tuple(left_out)}")
print(f"full_rows={tuple(full)}")
print(f"semi_rows={tuple(semi)}")
print(f"anti_rows={tuple(anti)}")
print(f"leading_key_comparisons={comparisons}")
print(f"inner_multiplicity={len(inner)}")
print("evidence=finite_duplicate_band_merge")
```

**Residual predicates refine band matches.** Suppose keys equal on customer ID but residual requires temporal overlap. The executor must test every candidate pair needed by that predicate or use another proven ordered sub-algorithm. A left row is matched only if at least one pair passes the full join qualification. Key equality alone cannot suppress null extension. Post-join filters remain above null extension unless a rewrite proof moves them.

**Sorting composes with merging.** A correct sort is a permutation: it retains every occurrence and orders keys under the declared comparator. If both sides sort correctly and merge is correct, sort-merge produces the logical join. In-memory comparison sort uses $O(N\log N)$ comparisons. External sorting generates memory-sized runs, writes them, then merges runs in passes determined by memory/fan-in. The join's single linear pass is only the last component.

With (B) input pages and (M) buffer pages, a simplified external merge sort with initial runs of about (M) pages and fan-in about (M-1) has approximately $1+\lceil\log_{M-1}\lceil B/M\rceil\rceil$ read/write passes, often modeled as (2B) I/Os per full pass. Exact engines use replacement selection, bounded heaps, compression, asynchronous I/O, tapes, incremental sort, top-N, or radix techniques. The formula is explanatory, not a product guarantee.

If both inputs require full sorts, price both. A merge join can sometimes consume the final merge of sorted runs directly, avoiding an extra materialized final output, but only with lifecycle and rewind requirements satisfied. A sort spill can still be an intentional bounded-memory strategy; uncontrolled temporary growth, disk-full, or concurrent spill storms are operational failures.

**Existing order can dominate plan choice.** A B-tree scan may deliver compatible join-key order. PostgreSQL 18 documents B-tree ordering and forward/backward direction, including NULL placement, while other index types/engines differ. A clustered/covering ordered path may be excellent; a noncovering index that fetches most heap pages randomly can lose to sequential scan plus sort. Partial ordering can support incremental sort, reducing memory/startup when long prefixes are already ordered.

Ordering has an identity, not a boolean. Record expressions/columns, ascending/descending direction, NULLS FIRST/LAST, collation/operator family, and whether the stream is global or merely per worker/partition. A parallel gather may destroy worker-local order unless a merge exchange restores it. Single-node here excludes network shuffle but still includes workers and gather behavior only when their final stream meets the same property contract.

**Output order is useful but conditional.** A merge inner join generally emits nondecreasing join keys when both inputs and band replay respect that sequence. Within equal keys, tie order may depend on sort stability, row identifiers, run merge, mark/restore, parallelism, or plan changes and is not a SQL contract. Outer unmatched rows can be integrated in key order if the algorithm emits them at comparison transitions. Residual filtering preserves subsequence order.

If a query needs deterministic presentation or keyset pagination, the final `ORDER BY` must include sufficient tie-breakers. An optimizer may recognize that merge-delivered order satisfies part/all of that property, but applications must depend on SQL order rather than the observed operator. A later hash aggregate, exchange, or unordered operator can destroy it.

**Memory pressure concentrates in sorts and bands.** Account for sort tuples/keys/payload, run buffers, merge fan-in, comparison state, equality-band materialization, matched flags, child buffers, and concurrent operators/workers. Wide payloads can be late-materialized through row identifiers if locator/version validity is guaranteed. A massive duplicate band can exceed memory even when both inputs are already sorted; spill the band or choose a controlled alternative.

Skew has two forms: sort skew affects comparison/compression/partition balance, while equality skew creates (mn) candidate/output work. Sorting does not remove logical output. Semi/anti joins can use existence and avoid cross-product emission; inner/outer cannot unless a higher-level rewrite proves reduction. Estimate most-common values and cross-table frequency products rather than only distinct counts.

**Comparator correctness is high stakes.** Test antisymmetry/transitivity/totality as applicable and compatibility with equality. Locale/collation implementations and versions can change ordering; persisted indexes may need rebuilding according to engine guidance. Do not compare one input with byte order and another with locale order. Nondeterministic collations, NaNs, signed zeros, time zones, mixed numeric types, and invalid encodings require documented operator semantics.

A comparator exception or corrupt value is failure, not “greater” or “unmatched.” External run records need integrity and version metadata. Cancellation must release pins, mark/restore state, sort memory, and temporary files. A retry after partial output needs a query/operator boundary that prevents duplicate visible results.

**Plan diagnosis joins estimates to evidence.** Capture engine/build, SQL/parameters, input paths, exact sort keys/collations/directions, estimated/actual rows and widths, rows per key/fanout, residual removals, sort method, memory, runs/passes, temporary read/write, duplicate-band spill/replay, buffers/CPU, first/last-row latency, workers, and output order requirements. A sort node may be absent because an index delivers order; verify that property rather than assuming missing work.

Common regressions include stale cardinality choosing two spills; a collation/cast preventing index order; widened rows increasing sort state; one heavy key expanding band output; changed `ORDER BY` direction needing another sort; lower memory or higher concurrency; and a parent no longer consuming the merge's order. Remedies address statistics, sargability, projection width, indexes, join order, memory/concurrency, heavy keys, or algorithm choice. Hints are scoped and expiring.

**Verification uses two independent oracles.** First, compare merge output bags with a simple nested-loop evaluator over generated duplicates, NULLs, empty sides, residuals, composite/collated/boundary values, and every join kind. Second, verify emitted order with the exact comparator/property. Mutate one input out of order and require assertion/failure in debug verification rather than silently accepting bad output.

Force in-memory and multi-pass sorts, tiny/huge duplicate bands, mark/restore and materialization, spill corruption/disk-full, cancellation at each state, comparator exceptions, version mismatch, worker imbalance, and resource concurrency. Performance experiments sweep order availability, rows/width, distinctness/skew, memory, temp device, cache, comparison cost, residual selectivity, output demand, and competing operators. Gate correctness first, then p95/p99, memory/temp, CPU/I/O, fairness, cleanup, and rollback.

## Definitions and Notation

- (L,R): left and right input bags; occurrences remain distinct.
- ∼: join equality; (cmp): compatible ordering comparator.
- (G_L(k),G_R(k)): maximal consecutive equality bands for key (k).
- **Merge key**: ordered expression tuple used to align candidates.
- **Residual qualification**: remaining TRUE/FALSE/UNKNOWN join condition after key alignment.
- **Mark/restore**: remember and revisit an input position for duplicate replay.
- **Materialized band**: stored equality group, in memory or spill.
- **Run**: sorted sequence created during external sorting.
- (B,M): input pages and available sort buffers in the simplified I/O model.
- **Interesting/delivered order**: precise physical sequence useful above the join.
- **Stable sort**: preserves input order among comparator-equal items; not automatically an SQL tie guarantee.
- **Incremental sort**: sorts within groups sharing an already ordered prefix.

## Mechanisms, Invariants, or Proof Structure

Maintain that all pairs involving fully consumed key groups have been emitted exactly according to join kind. For current keys, if left is smaller, sortedness proves it cannot match current/future right keys; process it as unmatched where applicable. The symmetric case follows. For equal keys, maximality makes all possible same-key occurrences exactly the Cartesian product of the two bands; equality/residual checks establish soundness and match flags establish outer/semi/anti behavior. Advancing both bands preserves the invariant until exhaustion.

Sort-merge correctness composes two claims: each sort preserves the input bag and establishes the comparator order, then merge establishes join output. Output-order proof additionally shows comparison transitions and band emission never decrease the claimed key. Tie order needs a stronger explicit property.

Cost is (C_{sortL}+C_{sortR}+O(|L|+|R|+N_c+|J|)), with (N_c) band candidate pairs. Existing order can reduce a sort term to zero; residuals/skew can make (N_c) large. These are conditional models, not measured latency.

## Alternatives and Trade-Offs

Merge join uses order, supports broad equality processing, can deliver order, and manages memory through sort/band spill, but pays comparison/sort startup. Hash accepts unordered equality inputs and often has lower comparison cost, but needs build memory/spill and destroys order. Index nested loop streams selective parameterized lookups with low startup but multiplies probes. Block nested loop supports arbitrary predicates but can rescan heavily. Range/as-of/interval joins may use specialized sweep/merge variants only with their own proofs; an equi-merge description does not validate them.

Choose using semantic predicate, existing/required order, rows/width, distinctness/fanout/skew, comparison/hash cost, memory/temp, startup versus completion, indexes/locality, downstream consumers, concurrency, and fault model.

## Failure Modes and Misconceptions

1. **“Two sorted inputs are enough.”** Their comparator, collation, direction, NULL, and type semantics must be compatible.
2. **“Comparator zero means SQL TRUE.”** Full equality/residual qualification may still reject candidates.
3. **“Advance both after an equal row.”** Duplicate bands require a cross product or join-kind-specific existence logic.
4. **“Key equality marks the row matched.”** Residual qualification determines TRUE matches.
5. **“NULLs adjacent in sort order match.”** Ordinary equality remains UNKNOWN.
6. **“Merge join is always linear.”** Sorting, spill, comparison cost, duplicate cross products, and output dominate.
7. **“Index order is free.”** Random base fetches, visibility, coverage, and direction can make it expensive or incompatible.
8. **“Merge output satisfies every ORDER BY.”** Only its exact delivered property, and later operators may destroy it.
9. **“Stable sort guarantees deterministic SQL ties.”** Determinism requires an explicit sufficient final order.
10. **“A duplicate group fits because rows are sorted.”** One heavy band can require unbounded replay/materialization.
11. **“Spill is automatically bad.”** Bounded spill can preserve safety; temp exhaustion and storms are failures.
12. **“Force merge to avoid hash memory.”** Two sorts, temp I/O, or skew may cost more; compare the whole plan.

## Worked Examples

### Example 1

Left keys `[1,2,4]`, right `[1,3,4]`. Compare 1=1 and emit; 2<3 advances left; 4>3 advances right; 4=4 emits. Conclusion: four leading comparisons cover both streams because sorted prefixes become impossible matches.

### Example 2

Left key 7 occurs twice and right key 7 three times. Materialize one band and replay it, emitting six pairs. Conclusion: linear stream advancement coexists with multiplicative duplicate output.

### Example 3

Keys compare equal but residual `left.start < right.end` passes only some pairs. Per-row match flags make failed left occurrences null-extended in a left join. Conclusion: band equality is candidate alignment, not final match state.

### Example 4

Both streams place NULL last. Ordinary equality emits no NULL pairs; full join emits each NULL occurrence unmatched. Conclusion: physical adjacency does not override three-valued semantics.

### Example 5

Left arrives from a covering `(tenant_id,time)` index; right needs one external sort. Merge preserves tenant/time prefix used by downstream grouping. Conclusion: one existing order plus downstream reuse can justify merge globally.

### Example 6

Both broad inputs use noncovering ordered indexes and fetch nearly every heap page randomly. Sequential scans plus sorts are faster on the measured storage. Conclusion: ordered access must include reconstruction/locality cost.

### Example 7

A 10-million-row side is 80,000 pages, memory holds 1,000 pages, and merge fan-in is 999. Initial 80 runs need one merge pass, so the simplified sort model has two read/write passes, about 320,000 I/Os. Conclusion: price sort passes before calling merge linear.

### Example 8

One key has one million rows on each side. The logical inner result has (10^{12}) pairs. Extra memory or a different join cannot remove required output. Conclusion: detect fanout and question/query-govern the logical workload.

### Example 9

A collation library upgrade changes key ordering while an index retains old order. Treating it as compatible can violate monotonic merge progress. Conclusion: versioned collation/index validity is correctness state.

### Example 10

Cancellation occurs while a duplicate band is spilled and right input is marked. The operator releases mark state and deletes owned files only after readers stop; it reports failure, not partial success. Conclusion: lifecycle and cleanup belong to operator correctness.

## Cross-Program Connections

- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md) supplies merge invariants, sorting bounds, external-memory analysis, and adversarial testing.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies heaps, B+ trees, buffers, runs, and stable/unstable ordering structures.
- [Programming Languages and Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) supplies comparator laws, effects, exceptions, and observational equivalence.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies temporary files, asynchronous I/O, memory quotas, cancellation, and cleanup.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies comparison cost, cache locality, branch behavior, and memory bandwidth.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) extends merge processing to sorted files, compaction, partitioned datasets, and stream/batch joins.

## References

1. PostgreSQL Global Development Group, [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; merge plans, sort methods, estimates, and runtime evidence.
2. PostgreSQL Global Development Group, [Query Planning Configuration](https://www.postgresql.org/docs/current/runtime-config-query.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; merge-join and sort planner controls.
3. PostgreSQL Global Development Group, [Indexes and ORDER BY](https://www.postgresql.org/docs/current/indexes-ordering.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; B-tree direction, NULL placement, broad scans, and limit trade-offs.
4. PostgreSQL Global Development Group, [Collation Support](https://www.postgresql.org/docs/current/collation.html), PostgreSQL 18 current documentation, retrieved 2026-08-30; provider/version, deterministic behavior, and collation semantics.
5. PostgreSQL Global Development Group, [`nodeMergejoin.c`](https://github.com/postgres/postgres/blob/REL_18_STABLE/src/backend/executor/nodeMergejoin.c), PostgreSQL 18 stable source, retrieved 2026-08-30; merge state machine, mark/restore, join qualification, and fill behavior.
6. PostgreSQL Global Development Group, [`nodeSort.c`](https://github.com/postgres/postgres/blob/REL_18_STABLE/src/backend/executor/nodeSort.c), PostgreSQL 18 stable source, retrieved 2026-08-30; executor sorting, bounded output, random access, and instrumentation integration.
7. Goetz Graefe, [“Query Evaluation Techniques for Large Databases”](https://web.stanford.edu/class/cs346/2014/graefe.pdf), *ACM Computing Surveys* 25(2), 1993; merge joins, duplicate handling, sorting, interesting order, and external-memory techniques.
8. Andy Pavlo, [“Join Algorithms”](https://15445.courses.cs.cmu.edu/fall2023/slides/11-joins.pdf), CMU 15-445/645 lecture notes, Fall 2023; sort-merge phases, costs, and join comparison.
9. SQLite Project, [Query Planning](https://www.sqlite.org/queryplanner.html), current official documentation, retrieved 2026-08-30; index/search ordering and sorting integration.
10. DuckDB Foundation, [`ORDER BY` Clause](https://duckdb.org/docs/current/sql/query_syntax/orderby.html), current official documentation, retrieved 2026-08-30; current configurable default order and NULL ordering, illustrating engine-specific order semantics.

## Exercises

### Exercise 1

Trace inner, left, full, semi, and anti merge joins for left `[1a,1b,2,NULL]` and right `[1x,3,NULL]` under ordinary equality. Show comparisons, bands, and unmatched transitions.

### Exercise 2

Derive the simplified sort passes and I/O for 80,000-page left and 20,000-page right inputs with 1,000 buffers and fan-in 999, followed by one merge scan. State reuse and omission assumptions.

### Exercise 3

Design a spillable duplicate-band implementation for full outer merge join with a residual predicate. Specify row identity, match tracking, mark/materialize choice, memory, files, cancellation, and oracle tests.

### Exercise 4

Diagnose a regression from hash join to merge join after a collation/query-order change: both sorts spill, p99 rises, and output tests intermittently disagree on tie order. Propose evidence and remedies.

### Exercise 5

Design a single-node temporal merge strategy for two large version histories ordered by `(entity_id,valid_from)`. State why ordinary equi-merge is insufficient, define interval semantics, bounded state, skew behavior, spill/failure handling, and release gates.

## Answers to the Exercises

### Answer 1

Compare key 1 bands: left has `1a,1b`, right has `1x`, yielding inner pairs `(1a,1x),(1b,1x)`; both left occurrences are matched. Next 2<3, so left 2 is unmatched. Left non-null exhausts; right 3 is unmatched. NULLs do not TRUE-match. Left join yields the two pairs plus `(2,null-extended)` and `(left-NULL,null-extended)`. Full adds `(null-extended,3)` and `(null-extended,right-NULL)`. Semi is `[1a,1b]`; anti is `[2,left-NULL]`. The comparison transitions are 1=1 then 2<3; remaining right and NULL handling follow exhaustion. Each equality band is maximal and every occurrence remains distinct.

### Answer 2

Initial run counts are `ceil(80000/1000)=80` and `ceil(20000/1000)=20`. Both are at most fan-in 999, so each sort needs run generation plus one merge pass: two full read/write passes, modeled as `4B` I/Os. Left costs 320,000 and right 80,000 page I/Os. If final sorted runs are fully materialized, the join then reads 100,000 pages, totaling 500,000 modeled transfers before output. A pipelined final run merge into the join may avoid writing and rereading final sorted outputs, reducing the accounting depending on the exact executor. Omitted are output, band spill, page utilization, cache, prefetch, compression, async I/O, comparison CPU, row width, temporary metadata, concurrency, and already ordered prefixes.

### Answer 3

Assign stable occurrence IDs. At equal keys, materialize the smaller or chosen band into a bounded store; spill records with key/comparator version, occurrence ID, payload/locator, checksum, and ownership. Keep a matched bit per left and right occurrence because residual qualification may pass only selected pairs. Replay all cross-band candidates, evaluate full equality and residual, emit each TRUE pair once, and mark both exact occurrences. After the band cross product, emit unmatched preserved occurrences once, then discard the band only after output reaches a retry-safe boundary. Mark/restore is acceptable only if the child is rewindable and its snapshot/effects remain stable. On cancellation/error/disk-full/corruption, report failure, stop readers, release marks, and delete owned files. Compare bags with a tuple-loop full-join oracle across duplicate/residual/null/skew cases and force memory thresholds and faults at each transition.

### Answer 4

Capture engine/build and collation provider/version, SQL and exact final order, schemas/indexes, delivered and required properties, estimates/actual rows/widths/fanout, sort keys/methods/memory/runs/temp I/O, merge residuals, concurrency, and final result bags/order. Tie disagreements may be invalid tests if final `ORDER BY` lacks a unique tie-breaker; add one when deterministic presentation is required. Also verify indexes remain valid under collation changes and both inputs use compatible comparator semantics. Remedies can rebuild invalid indexes, correct casts/collations, restore useful compatible order, narrow early projection, correct statistics, use incremental sort, govern memory/concurrency, or choose hash plus only the necessary final sort. Compare whole-plan p95/p99/temp and correctness; any hint is scoped with expiry and rollback.

### Answer 5

Equi-merge only pairs equal keys; temporal overlap requires `left.start < right.end AND right.start < left.end` (with explicitly chosen closed/half-open and infinity/NULL semantics). Partition the ordered streams by entity, then sweep start times while retaining active intervals from the opposite side whose end exceeds the current start. Emit every overlap occurrence, preserving duplicates; expire intervals only when ordering proves they cannot overlap future rows. State behavior for zero-length, open-ended, late/out-of-order, and identical boundaries. A high-overlap entity can create unbounded active state and output, so spill an entity group, use interval indexes/chunked ownership, or resource-govern it without losing pairs. Bind comparator/collation/time-zone and snapshot, checksum/version spill, fail explicitly on disorder/corruption, and make retries output-safe. Gate against a quadratic oracle on generated histories, boundary/time-zone cases, forced spill/cancellation, skew, p99/memory/temp, and deterministic final ordering where promised.
