---
module_id: LSDS-068
program: Large-Scale Data Systems Engineering
level: 2
module_number: 68
title: Adaptive Query Execution
status: complete
last_verified: 2026-09-04
---

# Adaptive Query Execution

## One-Page Review

### Governing question

How should a distributed query engine revise a running query's physical plan from runtime evidence so the revision preserves the original logical result, reuses valid work, respects recovery boundaries, converges under noise, and saves more remaining cost than measurement and transition consume?

### Essential definitions

- **adaptive query execution (AQE)** measures a running query and changes undecided or remaining physical execution without changing its logical request.
- An **observation point** records runtime facts such as completed stage bytes, rows, partition sizes, key frequencies, memory pressure, or source delay.
- A **decision point** is a boundary at which the engine may select a different valid physical continuation.
- A **materialization boundary** produces a stable intermediate relation or shuffle that later stages can consume under a new plan.
- A **plan revision** is an immutable, versioned physical-plan snapshot associated with a query and plan epoch.
- **state compatibility** means existing materialized or operator state can be interpreted by the revised continuation without semantic repair.
- A **transition cost** includes optimization, coordination, cancellation, draining, repartitioning, rebuilding, discarded work, and cache loss.
- **hysteresis** requires stronger evidence to change a choice than to retain it, reducing oscillation around a threshold.
- A **fallback plan** is a valid conservative continuation used when evidence is late, partial, inconsistent, or adaptation fails.
- **adaptive budget** bounds observation overhead, optimizer time, revision count, state migration, and control-plane work.

### Central model, mechanism, or theorem

AQE is a feedback loop: measure a versioned execution scope; validate complete attempt-fenced evidence; estimate valid continuations; choose only if expected remaining benefit exceeds decision and transition cost plus a safety margin; actuate at a safe boundary; then verify semantics and effect. For old continuation $P_o$ and candidate $P_n$, a useful gate is

$$C_{rem}(P_o)-C_{rem}(P_n) > C_{decide}+C_{transition}+C_{discard}+M,$$

where every term applies to work still avoidable and $M$ covers model uncertainty and operational risk. Logical expressions, snapshot, parameters, row semantics, and required physical properties remain fixed. Only compatible future work changes. A revision must either reuse fully identified materialized outputs or fence and recompute affected work exactly once.

### Critical invariants

- Query text/parameters, catalog snapshot, logical algebra, security policy, functions, null/collation/time semantics, and output contract do not change across plan revisions.
- Every observation names query, logical node, plan epoch, stage, partition, selected task attempt, statistic definition, units, completeness, and collection time.
- Decisions distinguish complete materialized facts from estimates over partial streams.
- A new physical continuation satisfies required partitioning, ordering, grouping, uniqueness, and distribution properties.
- Reused intermediate data has compatible schema, encoding, partition map, snapshot, integrity, and producing epoch.
- Cancellation and retry fence losing attempts so old and new outputs cannot both commit.
- Adaptation never assumes already emitted output can be retracted unless the protocol explicitly supports retractions.
- Revision count, optimizer time, metadata, retained intermediates, repartitioning, and state migration are bounded.
- Hysteresis, cooldown, minimum evidence, and a stable fallback prevent noisy plan oscillation.
- Metrics attribute observation, decision, transition, reused/discarded work, and realized benefit to one revision chain.

### Common failures

Common failures include changing plans from incomplete partition statistics; comparing estimated total cost with already-spent actual cost; broadcasting a relation that fits compressed but not decoded/hash-table memory; coalescing away needed parallelism on a busy cluster; splitting skew without preserving join multiplicity; changing join order after stateful output escaped; reusing a shuffle under a different partition function; accepting duplicate output from old and new attempts; repeatedly flipping near one threshold; spending longer optimizing than the remaining stage; hiding regressions by reporting only the final plan; and claiming savings from work that had already completed.

### Compact example

A shuffle completes with 800 GiB in 4,000 small partitions. With a measured 2 GiB target and bounds of 64–512 tasks, the next stage may coalesce contiguous inputs to 400 tasks if its distribution contract permits. A candidate join revision reduces predicted remaining cost from 920 to 540 units but costs 20 to decide, 90 to transition, and 30 in discarded work. Net expected saving is 240 units; it is eligible only if this exceeds the uncertainty/risk margin and resource constraints. Neither calculation proves speedup—post-revision telemetry must compare realized critical-path and resource cost.

### Connections

[LSDS-031](031-shuffle-architecture.md) supplies stable shuffle boundaries, [LSDS-061](061-distributed-logical-and-physical-plans.md) separates logical and physical plans, [LSDS-062](062-coordinator-and-worker-architecture.md) owns revision epochs, [LSDS-063](063-exchange-operators.md) enforces physical properties, [LSDS-064](064-distributed-hash-and-merge-joins.md) constrains join changes, [LSDS-065](065-partial-and-final-aggregation.md) constrains state reuse, and [LSDS-067](067-runtime-filtering-and-dynamic-pruning.md) supplies runtime evidence without itself replacing the plan.

## Governing Question

Static optimization chooses a physical plan from estimates available before execution. Those estimates may be stale, absent, or incapable of describing intermediate data after correlated filters, user-defined functions, remote sources, or earlier joins. Execution reveals actual stage bytes, row counts, key distributions, partition skew, available resources, and delays. AQE turns those facts into safer decisions for work that has not yet run.

The word *adaptive* covers different mechanisms. One engine may coalesce completed shuffle partitions. Another may defer construction of later stages, replace a sort-merge join with broadcast hash join, reorder partitioned join inputs, split skewed partitions, or choose downstream parallelism. Research systems may route tuples continuously. These mechanisms differ in when facts become complete, which state is reusable, and how hard it is to prove equivalent output.

The governing question is not merely whether the new plan looks cheaper. It is whether the evidence is valid, the candidate satisfies the unchanged logical contract, the transition is safe under concurrency and failure, the decision will converge, and the remaining savings justify all adaptation cost.

## Why This Matters

Cardinality errors compound through a plan. If each of four joins is underestimated by a factor of ten, a nominally tiny intermediate can become enormous. A static broadcast choice may exhaust every worker. Too many tiny partitions create scheduler and network overhead; too few produce long tails. One hot key may dominate a stage even when total bytes were estimated correctly.

Runtime evidence can correct these mistakes after a stable boundary. Current Spark documentation describes adaptive coalescing, join-strategy conversion, local shuffle readers, and skew handling. Current Flink documentation describes incremental graph decisions for downstream parallelism, distribution balancing, broadcast join, and skewed joins. Current Trino documentation describes runtime join-input reordering when fault-tolerant execution is enabled. These are product-specific capabilities, not one universal AQE contract.

Adaptation also adds risk and cost. Statistics collection consumes CPU and control bandwidth. Materialization improves observability but can add I/O and latency. Reoptimization can serialize the coordinator. Holding both old and candidate state inflates memory. Cancellation may waste completed work. A new plan can interact badly with retry, speculation, connectors, security, or output commit. AQE must therefore be engineered as a bounded fault-sensitive control system.

## Prerequisites and Retrieval

Review worker serialization in [LSDS-008](008-serialization-across-workers.md), shuffle architecture in [LSDS-031](031-shuffle-architecture.md), fair and capacity scheduling in [LSDS-053](053-fair-and-capacity-scheduling.md), resource isolation in [LSDS-057](057-memory-cpu-and-i-o-isolation.md), physical plans in [LSDS-061](061-distributed-logical-and-physical-plans.md), coordinator state in [LSDS-062](062-coordinator-and-worker-architecture.md), exchange in [LSDS-063](063-exchange-operators.md), joins in [LSDS-064](064-distributed-hash-and-merge-joins.md), aggregation state in [LSDS-065](065-partial-and-final-aggregation.md), and runtime filters in [LSDS-067](067-runtime-filtering-and-dynamic-pruning.md).

You should understand relational equivalence, physical properties, cardinality estimation, cost models, materialization, shuffle partitions, join algorithms, skew, task attempts, cancellation, output commit, snapshots, null semantics, and production experimentation.

## Learning Objectives

After this module, you should be able to:

1. model AQE as a versioned measure–decide–actuate–verify loop;
2. distinguish complete stage statistics from partial streaming estimates;
3. select observation and decision points by information value and transition safety;
4. compute bounded downstream parallelism and identify skew candidates from runtime distributions;
5. evaluate adaptive join distribution, algorithm, input order, and local-read alternatives;
6. prove that a plan revision preserves logical and required physical properties;
7. manage materialized state, plan epochs, retries, speculation, cancellation, and output commit;
8. prevent oscillation with margins, hysteresis, cooldown, evidence floors, and revision budgets;
9. attribute adaptation overhead, avoided work, tail behavior, and realized cost by revision; and
10. validate AQE through differential, metamorphic, fault, concurrency, and performance tests.

## Core Exposition

### Treat adaptation as a control loop

Define five explicit phases:

1. **Measure:** collect typed, scoped observations from execution.
2. **Validate:** establish lineage, attempt selection, completeness, freshness, and uncertainty.
3. **Decide:** enumerate semantically valid alternatives and compare remaining cost.
4. **Actuate:** install one immutable revision at a safe point, fence old work, and preserve or rebuild state.
5. **Verify:** compare predicted and realized behavior and feed bounded learning into later decisions.

Skipping validation turns retries into double counting. Skipping transition accounting favors plans that are cheap only if started from scratch. Skipping verification lets a rule remain enabled even when it consistently moves cost rather than removes it.

### Freeze logical meaning, version physical choice

The logical plan identifies expressions, join type, grouping, snapshot, authorization, and output. AQE should not reinterpret that contract. It chooses among physical implementations that are equivalent under declared preconditions.

Assign every physical snapshot a monotonically increasing `plan_epoch`. Record its parent epoch, trigger evidence, candidate set, chosen rule, expected costs, transition recipe, and fallback. Tasks accept descriptors only for an authorized epoch. Consumers reject output from fenced epochs unless it is an explicitly reusable materialization.

A plan revision is not an in-place mutation scattered across worker objects. Treat it as a durable control-plane event so recovery can reconstruct what ran and why.

### Design observation contracts

Useful observations include rows and logical bytes, serialized and decoded bytes, per-partition sizes, key-frequency samples, null fractions, distinct estimates, spill, peak memory, CPU time, remote wait, and resource availability. Each needs units and semantics. “Size” may mean compressed shuffle bytes, decoded rows, or predicted hash-table footprint; these are not interchangeable.

An observation record should name query, logical node, physical epoch, stage and partition, selected attempt, collection interval, statistic definition/version, exact-versus-estimated status, error bound when known, completeness, and timestamp. Aggregators deduplicate retries by logical partition and selected attempt.

Completed stage statistics are exact for that materialized stage under their defined measurement. They do not automatically predict decoded memory, later selectivity, or network cost. Partial observations need extrapolation and wider uncertainty.

### Place decision points deliberately

Blocking exchanges, completed build sides, sorts, and explicit materializations create strong decision points. Their output is a named relation with known schema and often complete partition statistics. Later operators can be regenerated while preserving that output.

Pipelined decision points react sooner but face partially processed input and state. Switching may require discarding work, replaying input, migrating state, or emitting corrections. Once non-retractable rows or external side effects escape, many revisions become unsafe.

Materialization is therefore an option with a price. It buys exact information, restartability, and plan freedom but costs storage, serialization, latency, and lifetime management. Place it where uncertainty multiplied by downstream sensitivity justifies the boundary.

### Compare remaining cost, not total cost

Let $C_{rem}(P)$ estimate future critical-path/resource cost from the decision point. A candidate is economically eligible when

$$S=C_{rem}(P_o)-C_{rem}(P_n)-C_{decide}-C_{transition}-C_{discard}>M.$$

Already spent cost is sunk. Work completed into a reusable materialization is not discarded. Work that cannot be consumed by the new plan belongs in $C_{discard}$. Transition includes cancellation delay, control messages, repartitioning, rebuilding, dual-state peak memory, cache coldness, and recovery exposure.

The margin $M$ can reflect confidence intervals, risk class, query remaining time, tenant priority, and historical rule error. A large estimated gain with fragile memory feasibility is not eligible merely because its mean cost is low.

### Detect meaningful estimate error

For actual $a$ and estimate $e>0$, ratio $a/e$ is intuitive but asymmetric. A log error

$$E=\left|\log\frac{a+\epsilon}{e+\epsilon}\right|$$

treats equal multiplicative over- and underestimates similarly; $\epsilon$ handles zero. Error alone is not a switch rule. A hundredfold mistake at a cheap leaf may not matter, while a twofold mistake near a memory cliff may.

Trigger on plan sensitivity: would the updated observation change a physical choice enough to exceed the remaining-cost gate? Combine minimum evidence, uncertainty, and cooldown so early noisy samples do not cause churn.

### Adapt downstream parallelism

For $B$ measured input bytes, target $T>0$, and bounds $p_{min}\le p_{max}$, a baseline is

$$p=\min\left(p_{max},\max\left(p_{min},\left\lceil B/T\right\rceil\right)\right).$$

Then adjust for partition indivisibility, CPU intensity, decoded expansion, memory per task, slots, locality, downstream concurrency, network buffers, and tenant limits. Byte targets are policy inputs, not truths.

Coalescing contiguous hash/range shuffle partitions may reduce tiny tasks while retaining logical partition ownership. Arbitrarily merging or splitting without a partition map can violate grouping or ordering. Increasing task count after upstream output exists requires the shuffle representation to expose sufficiently fine subpartitions or a new repartition.

### Split skew without changing multiplicity

One robust flag combines relative and absolute conditions. For partition size $x_i$, median $m$, factor $f>1$, and absolute floor $A$, mark skew when

$$x_i>\max(fm,A).$$

Median reduces sensitivity to a few large values. Yet total partition bytes do not explain a single hot key, decoded expansion, or CPU-heavy values. Include key-frequency and processing-time evidence when available.

Splitting a join partition may require replicating the matching slice of the other side. Preserve every qualifying pair exactly once. Join type constrains which side may be split or replicated because unmatched-row production depends on global knowledge. Bound replication and extra shuffle; otherwise a “skew fix” can amplify network and memory.

### Revise join distribution and algorithm

Runtime size can make broadcast attractive when a side is genuinely small. Feasibility must use per-worker decoded/hash-table memory, concurrency, allocator overhead, replication factor, and broadcast timeout—not compressed input bytes alone. Join type constrains valid build sides.

A completed shuffle may still be reusable after converting sort-merge to broadcast through local readers, but the earlier shuffle cost is sunk, not saved. Alternatively, if all partitions fit bounded local hash tables, shuffled hash join may avoid sort work. A revision may swap partitioned join inputs or reorder later joins only where intermediate relations and required properties permit.

Candidate enumeration should begin from equivalence and resource feasibility, then cost. A cheaper illegal join is not a candidate.

### Preserve physical properties

Every edge has requirements: partition keys and hash version, range boundaries, ordering and null placement, collation, uniqueness, bucketing, locality, row format, and retry semantics. Each candidate declares what it requires and produces. The optimizer must re-derive properties across the replacement subgraph.

Reusing an old exchange solely because schemas match is unsafe. Two exchanges over the same keys may use different hash seeds, partition counts, normalization, or range maps. Similarly, coalescing can retain grouping while losing useful parallelism; local reads can change placement without changing logical partitioning.

### Manage state and transition

Classify state as immutable reusable materialization, reconstructible cache, migratable operator state, or epoch-local disposable state. Reuse requires a stable identifier, producing epoch, schema/encoding, partition map, snapshot, checksums, and lifetime. Migration needs a tested transformation and an atomic ownership handoff.

At a revision barrier, stop issuing old work; mark affected attempts draining or canceled; choose whether their completed materializations remain valid; install the new epoch; and let only authorized attempts publish downstream output. If fencing or migration fails, resume a conservative plan from the last valid boundary.

Pipelined hash tables, partial aggregations, sort runs, and runtime filters are not automatically reusable across changed keys, order, algorithms, or epochs. Conservative recomputation is preferable to ambiguous state stitching.

### Integrate retries and speculation

Observations and outputs are keyed by logical task and selected attempt. A speculative duplicate must not double observed bytes or make a stage appear complete. A retry after plan revision receives the current epoch and must not publish under an obsolete descriptor.

Recovery replays the revision log, validates retained exchanges, and reconstructs the active plan. If an engine cannot durably reconstruct adaptive decisions, it should discard affected state and reoptimize from a stable earlier boundary. Adaptation cannot silently weaken exactly-once output commit.

### Bound adaptation and prevent oscillation

Cap revisions per query and per logical region, optimizer CPU/wall time, observation bytes/messages, retained candidate/intermediate state, transition bytes, and coordinator memory. Apply per-tenant quotas so one unstable query cannot monopolize planning.

Use hysteresis: require a higher gain to switch than to stay, and do not immediately reconsider the reverse choice. Add cooldown, minimum newly completed evidence, and monotone decisions where practical—for example coalescing a completed shuffle once rather than repeatedly changing its partition count.

When budgets expire or evidence conflicts, freeze the current valid plan. Predictability and correctness outrank endless pursuit of an uncertain optimum.

### Keep hints and operator controls explicit

Hints may express user knowledge, contractual constraints, or preferences. Define whether a hint is mandatory, advisory, or disables a class of adaptation. Record when AQE overrides an advisory hint and why. Never override a correctness, governance, or resource isolation constraint.

Expose rule-level kill switches and session controls. Configuration defaults and supported transformations vary by product and release, so operational policy must be tied to deployed versions and verified behavior rather than copied blindly from another engine.

### Observe prediction and realization

For every revision, retain old/candidate plan hashes, trigger observations, completeness, cost ranges, decision duration, transition duration/bytes, state reused/discarded, tasks canceled, work completed before switch, and fallback. Stage metrics need plan epoch labels.

Measure realized bytes read/shuffled, CPU, spill, peak memory, task count, scheduler delay, locality, skew, retries, critical path, query latency, and monetary/energy cost. Compare against a shadow estimate or matched control cohort. AQE success is net query and fleet value, not the number of applied rules.

### Validate and roll out conservatively

Differentially execute AQE enabled and disabled against the same immutable snapshots. Cover nulls, outer/semi/anti joins, duplicates, nondeterministic and erroring expressions, order-sensitive operators, empty/huge intermediates, skew, compressed/decoded expansion, and connector behavior.

Property-test partition and multiplicity preservation. Inject partial statistics, retry, speculation, stale epochs, optimizer timeout/crash, coordinator recovery, missing/corrupt shuffle, cancellation races, memory pressure, worker loss, and output-commit failure. Verify fallback produces the same result.

Shadow candidate decisions before actuation. Canary by rule, workload, connector, and query risk. Stop on any result mismatch, duplicate/lost output, recovery failure, resource-bound breach, or severe tail regression. Rollback disables the adaptive rule and preserves the known-valid static continuation.

## Definitions and Notation

Let logical query $Q$ be evaluated at catalog/data snapshot $\sigma$ with parameters $\theta$. Let $L(Q,\sigma,\theta)$ denote its logical semantics. A physical revision $P^{(r)}$ has epoch $r$ and must implement the same $L$.

At decision point $d$, let $O_d$ be validated observations, $M_d$ be reusable materialized relations, and $W_d$ be already committed external output. Let $\mathcal{P}(L,M_d,W_d)$ be the set of physically valid continuations consistent with those states. AQE may select $P_n\in\mathcal{P}$; it cannot choose from arbitrary plans.

For logical partitions $i=1,\ldots,n$, let $b_i$ be measured bytes, $t_i$ time, and $a_i$ the selected attempt. A complete stage observation contains exactly one authorized successful contribution per $i$. Define total $B=\sum_i b_i$, median $m=\operatorname{median}(b_i)$, and maximum $b_{max}$.

Let $C_{rem}(P\mid O_d)$ be an uncertain estimate of future cost conditional on observations. Let $C_D$, $C_T$, and $C_X$ denote decision, transition, and discarded-work costs. Let $M$ be the required margin. Switch only when the candidate is valid, feasible, and expected net saving exceeds $M$ under policy.

## Mechanisms, Invariants, or Proof Structure

### The plan-revision safety argument

1. Fix $L(Q,\sigma,\theta)$ and all authorization and semantic settings.
2. Validate $O_d$ by epoch, definition, attempt selection, units, freshness, and completeness.
3. Identify $M_d$ and $W_d$ with schema, partition/property, snapshot, integrity, and commit status.
4. Enumerate candidates whose relational transformations preserve $L$.
5. Derive required and produced physical properties across each candidate.
6. Reject candidates incompatible with retained state or non-retractable output.
7. Reject candidates violating memory, network, concurrency, connector, recovery, or governance constraints.
8. Compare only remaining costs, including decision, transition, discarded work, and uncertainty margin.
9. Atomically install a new epoch, fence obsolete work, and authorize one output path.
10. Verify result equivalence, resource bounds, realized benefit, and recovery; otherwise use the conservative fallback.

The proof obligation has three layers. Relational equivalence shows the candidate computes the same logical multiset/order contract. State compatibility shows reused bytes represent the right subexpressions and physical properties. Execution fencing shows concurrency, retry, and cancellation cannot lose or duplicate committed effects.

### Complete facts versus early estimates

A materialized stage can provide complete $b_i$ only after every logical partition has one selected successful attempt. Before then, $\sum b_i$ is a lower bound, not final size. An early controller may estimate final size, but it must label uncertainty and must not make a memory-safety decision as if the estimate were exact.

Some decisions can be safely monotone. If observed bytes already exceed a hard broadcast maximum, the engine may rule out broadcast without waiting for completion. It cannot prove the relation fits until the relevant complete size and decoded-memory model are known.

### Output-commit invariant

For each logical output partition, at most one authorized attempt/epoch may commit, and all committed partitions collectively implement one compatible revision chain. A coordinator cannot accept some partitions under incompatible hash maps or duplicate a partition from both old and new epochs.

If output has reached a client or external sink without a retraction/transaction protocol, revisions must not invalidate it. This normally confines plan replacement to downstream work behind stable boundaries.

## Alternatives and Trade-Offs

### Static robust plans

A conservative static plan avoids observation and transition overhead and can be easier to recover. It may deliberately choose repartitioned joins or more partitions to tolerate uncertainty. This is attractive for short queries, tiny remaining work, strict latency predictability, or weak control planes.

The cost is missed opportunity when runtime facts differ sharply. Robustness is not the same as optimality, and one global conservative choice can be expensive for heterogeneous data.

### Precomputed alternative plans

Parametric or choose-plan approaches prepare alternatives before execution and select when parameters become known. Decision latency is low and transition behavior is easier to validate. Candidate coverage is limited to scenarios anticipated during planning, and compilation/state retention may be larger.

### Stage-boundary reoptimization

Reinvoking an optimizer over completed intermediate relations uses accurate facts and preserves reusable work. Blocking boundaries make state and recovery tractable. The engine may learn too late, and materialization can add cost.

### Continuous tuple routing

Eddy-style routing adapts operator order frequently and can respond to volatile rates/selectivities. It requires operators and state designed for moments of reorderability, routing history, and migration. This is far more invasive than choosing downstream partitions after a shuffle.

### Rule-based versus cost-based AQE

Rules such as “coalesce tiny partitions” are fast, explainable, and easily bounded. Cost-based search can combine interactions and resource constraints but depends on runtime models and coordinator budget. A practical design often uses legality/feasibility rules, a small candidate set, and cost comparison with guardrails.

### Reuse versus recompute

Reusing materialized work saves time and cost but constrains the candidate to compatible properties. Recomputing enables broader revisions and simpler correctness reasoning but discards work. State migration lies between and is worthwhile only with explicit schemas, atomic handoff, and strong testing.

## Failure Modes and Misconceptions

- **“Actual rows make the new cost exact.”** Later selectivity, decoded size, resource contention, and remote delay remain uncertain.
- **“A hundredfold estimate error requires reoptimization.”** Only plan-sensitive remaining benefit justifies a transition.
- **“Completed shuffle bytes equal broadcast memory.”** Deserialization, hash tables, values, fragmentation, and concurrency can multiply footprint.
- **“Coalescing is only scheduling.”** It changes task count, locality, concurrency, and possibly physical-property representation.
- **“Any skewed partition can be split.”** Join multiplicity, unmatched rows, hot keys, and replication bound legality.
- **“Schema equality permits shuffle reuse.”** Hash/range function, seed, partition count/map, ordering, encoding, and snapshot also matter.
- **“Canceling old tasks prevents duplicates.”** Outputs already committed or racing require epoch-aware commit fencing.
- **“Partial bytes can prove that a relation is small.”** Partial size is a lower bound; it can prove a hard maximum was exceeded, not that completion fits.
- **“More adaptations approach the optimum.”** Noise, delayed feedback, transition cost, and interacting rules can oscillate or diverge.
- **“Final-plan metrics explain AQE.”** Without revision history, discarded work and transition overhead disappear.
- **“AQE fixes bad logical semantics.”** It must preserve the logical contract; incorrect predicates, snapshots, or policies are separate defects.
- **“A product default is a universal threshold.”** Hardware, workload, release, concurrency, and cost objectives differ.

## Worked Examples

### Example 1

**Gate a join revision by remaining cost.**

The old continuation costs 920 units; the candidate costs 540. Decision, transition, and discard cost 20, 90, and 30. Net expected saving is $920-540-20-90-30=240$. With margin 50 and feasible memory, the candidate is eligible. If 700 old-cost units were already spent and cannot be avoided, they never enter the comparison.

### Example 2

**Coalesce completed shuffle inputs.**

A stage produces 800 GiB. With a 2 GiB target, $\lceil800/2\rceil=400$ tasks, within bounds 64–512. The planner builds a map from 4,000 fine shuffle partitions to 400 contiguous task inputs. It retains the partitioning contract needed by the consumer and reports both upstream and downstream counts.

### Example 3

**Rule out broadcast monotonically.**

Only 20% of build partitions have completed, already totaling 18 GiB. The hard per-query broadcast input cap is 16 GiB. Because complete size cannot shrink, broadcast may be removed immediately. Conversely, observing 2 GiB at 20% cannot prove final build size is below 16 GiB.

### Example 4

**Size decoded broadcast state.**

A 6 GiB compressed shuffle expands to 18 GiB of key/value pages. Hash buckets, metadata, and allocator overhead are measured at 1.5×, yielding 27 GiB per worker before transient build space. On workers with 24 GiB governed query memory, broadcast is infeasible despite being below a 10 GiB compressed-byte threshold.

### Example 5

**Detect and split skew.**

Median partition size is 1.5 GiB, factor is 5, and absolute floor is 6 GiB. The skew threshold is $\max(7.5,6)=7.5$ GiB. A 9 GiB partition qualifies. The engine divides splittable ranges and replicates only the compatible other-side slice, checking join type and a replication cap.

### Example 6

**Reject an incompatible shuffle.**

Epoch 3 used 256 partitions and hash function `h3`. The candidate expects 128 partitions and `h4`. Although row schema and keys match, the exchange cannot be read as candidate partitions. The engine must insert a repartition transition or reject that candidate; relabeling the files would corrupt grouping.

### Example 7

**Fence a cancellation race.**

Epoch 7 tasks are canceled while epoch 8 starts. One epoch 7 attempt finishes concurrently. The output service accepts only the coordinator-authorized `(query, logical_partition, epoch, attempt)` token, so the late output is ignored. Reusable epoch 7 shuffle blocks are consumed only if the revision explicitly listed their stable identifiers.

### Example 8

**Apply hysteresis.**

Broadcast is chosen only when expected net saving exceeds 200 ms and predicted peak memory remains below 70% of its limit. Once chosen, reversal requires either a feasibility breach or 400 ms expected gain after cooldown. A noisy size estimate around the boundary cannot flip the join repeatedly.

### Example 9

**Recover a revision chain.**

The coordinator fails after epoch 4 installed but before all downstream tasks launch. Recovery replays the durable revision event, validates checksums and partition maps for epoch 3 materialized inputs, restores epoch 4 as active, and rejects epoch 3 task commits. If the event or intermediates are incomplete, it falls back to a stable earlier barrier.

### Example 10

**Execute bounded AQE calculations.**

The following fixture recomputes the eligibility, downstream parallelism, and skew conditions used above.

<!-- bijux-verify: {"id":"adaptive-decision","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"net_savings=240\nswitch=yes\npartitions=400\nskew_threshold_mib=7680\nis_skewed=yes\n","stderr":""}} -->
```python
import math

remaining_old = 920
remaining_new = 540
decision = 20
transition = 90
discard = 30
margin = 50
net = remaining_old - remaining_new - decision - transition - discard

input_mib = 800 * 1024
target_mib = 2 * 1024
partitions = min(512, max(64, math.ceil(input_mib / target_mib)))

median_mib = 1536
skew_threshold_mib = max(5 * median_mib, 6144)
observed_mib = 9216

print(f"net_savings={net}")
print(f"switch={'yes' if net > margin else 'no'}")
print(f"partitions={partitions}")
print(f"skew_threshold_mib={skew_threshold_mib}")
print(f"is_skewed={'yes' if observed_mib > skew_threshold_mib else 'no'}")
```

The arithmetic validates the policy inputs, not the candidate's semantic legality or real-world performance.

## Cross-Program Connections

- **Database systems:** logical equivalence, cardinality, costs, joins, properties, materialization, and optimizer search define candidates.
- **Distributed systems:** epochs, barriers, attempts, retries, speculation, fencing, recovery, and commit define safe actuation.
- **Control theory:** observation delay, noise, hysteresis, cooldown, gain, stability, and bounded feedback explain convergence.
- **Data engineering:** shuffle sizes, partitions, skew, storage expansion, connectors, and snapshots supply runtime evidence.
- **Platform engineering:** scheduler load, worker memory, locality, network buffers, quotas, and multi-tenancy constrain choices.
- **Reliability engineering:** conservative fallback, durable decision logs, fault injection, canaries, kill switches, and rollback bound risk.
- **Security and governance:** fixed authorization, snapshot, tenant isolation, telemetry redaction, and retained-state lifecycle preserve policy.
- **Performance engineering:** remaining critical path, transition overhead, discarded work, tails, fleet utilization, and cost determine value.

## References

1. Apache Spark. [SQL Performance Tuning.](https://spark.apache.org/docs/latest/sql-performance-tuning.html) Current AQE, runtime statistics, partition coalescing, local readers, join conversion, and skew controls.
2. Apache Spark. [Web UI.](https://spark.apache.org/docs/latest/web-ui.html) Current stage, task, SQL, plan, metric, executor, and diagnostic surfaces.
3. Apache Spark. [Configuration.](https://spark.apache.org/docs/latest/configuration.html) Current scheduler, memory, network, retry, speculation, and runtime configuration context.
4. Apache Spark. [Monitoring and Instrumentation.](https://spark.apache.org/docs/latest/monitoring.html) Current event-log, history-server, REST, metrics, and query-observation interfaces.
5. Apache Flink. [Adaptive Batch Execution.](https://nightlies.apache.org/flink/flink-docs-stable/docs/deployment/adaptive_batch/) Current incremental graph decisions, parallelism, distribution balancing, adaptive broadcast, skew optimization, and limitations.
6. Apache Flink. [AdaptiveBatchScheduler API.](https://nightlies.apache.org/flink/flink-docs-stable/api/java/org/apache/flink/runtime/scheduler/adaptivebatch/AdaptiveBatchScheduler.html) Current dynamic execution-graph and data-volume-based parallelism interface.
7. Apache Flink. [Recovery Job Progress from JobMaster Failures.](https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/batch/recovery_from_job_master_failure/) Current retained-intermediate, coordinator-event, source, timeout, and recovery constraints.
8. Trino. [Adaptive Plan Optimizations.](https://trino.io/docs/current/optimizer/adaptive-plan-optimizations.html) Current runtime plan adjustment and partitioned-join input reordering behavior.
9. Trino. [Fault-Tolerant Execution.](https://trino.io/docs/current/admin/fault-tolerant-execution.html) Current task/query retry, spooled exchange, task sizing, partitioning, memory, encryption, and adaptive-plan context.
10. Trino. [Cost in EXPLAIN.](https://trino.io/docs/current/optimizer/cost-in-explain.html) Current estimated rows/bytes and relative CPU, memory, and network cost representation.
11. Deshpande, Ives, and Raman. [Adaptive Query Processing.](https://www.cs.umd.edu/~amol/papers/fnt-aqp.pdf) Foundational monograph on feedback loops, eddies, state, plan staging, checkpoints, mid-query reoptimization, and scrambling.
12. Kabra and DeWitt. [Efficient Mid-Query Re-Optimization of Sub-Optimal Query Execution Plans.](https://courses.cs.washington.edu/courses/cse590q/01wi/papers/kabra_dewitt.pdf) Primary work on runtime statistics, checkpoints, resource reallocation, and plan revision.
13. Armbrust et al. [Spark SQL: Relational Data Processing in Spark.](https://jkbradley.github.io/assets/papers/2015_sigmod_spark_sql.pdf) Primary account of Spark SQL, Catalyst, physical planning, data sources, and distributed relational execution.

## Exercises

### Exercise 1

Design an AQE decision record and control loop for a six-stage query. Include observation identity/completeness, candidates, legality, resource feasibility, remaining-cost gate, transition, epochs, fallback, and verification.

### Exercise 2

A 3.2 TiB shuffle has 8,192 fine partitions. Derive downstream parallelism for a 4 GiB target and bounds 128–1,024. Then explain how CPU intensity, decoded expansion, slots, locality, and ordering can change the answer.

### Exercise 3

Design a safe sort-merge-to-broadcast join revision after both sides have already shuffled. Address join type, complete evidence, decoded memory, sunk cost, local readers, physical properties, cancellation, retries, and metrics.

### Exercise 4

Design skew adaptation for an outer join with a few hot keys. Include detection, splittability, replication, unmatched-row semantics, partition mapping, attempt fencing, cost bounds, and tests.

### Exercise 5

Design a production validation and rollout campaign for AQE across mixed workloads and connectors. Include semantic oracles, failure injection, performance attribution, security, shadowing, canaries, kill switches, and rollback.

## Answers to the Exercises

### Answer 1

Use an immutable record keyed by query and new `plan_epoch`, with parent epoch, fixed logical-plan/snapshot/security/parameter hashes, decision point, evidence records, selected attempt per logical partition, units, definition versions, completion/error bounds, candidate plan/property hashes, legality and feasibility results, remaining-cost ranges, transition/discard/memory costs, margin, chosen rule, state reuse map, cancellation/fencing actions, fallback, and decision timestamp. The coordinator first measures, validates lineage/completeness, enumerates equivalent candidates, derives physical properties, rejects resource/recovery violations, applies the net remaining-cost gate, durably installs one epoch, fences old outputs, and verifies result/resource/benefit. Optimizer time, revisions, metadata, retained state, and transition bytes have explicit budgets. Timeout or disagreement retains the current valid plan.

### Answer 2

$3.2$ TiB is $3.2\times1024=3276.8$ GiB, so $\lceil3276.8/4\rceil=820$ tasks, inside 128–1,024. Since 8,192 fine partitions exist, create a deterministic map to roughly 820 contiguous groups if the shuffle/order contract permits. Four GiB serialized input may expand beyond per-task memory or be CPU-heavy, requiring more tasks; limited slots or high scheduler/network overhead may favor fewer. Locality may constrain grouping. A global order or range boundary may forbid arbitrary merges. Govern by measured decoded peak, CPU time, downstream concurrency, tenant quota, buffer needs, and tails rather than bytes alone.

### Answer 3

Require a join type/build side for which broadcast preserves semantics and complete attempt-fenced build bytes for one snapshot. Predict decoded rows, hash table/buckets, allocator/transient memory, per-worker concurrency, replication network, and timeout; compressed shuffle size is insufficient. The completed shuffles are sunk costs. If the engine can read the large side locally without requiring its old partitioning, reuse its blocks through a compatible local reader; otherwise include repartition/read transition cost. Re-derive distribution/order properties above the join. Install a new epoch, cancel/fence old join attempts, and accept output only from authorized new attempts while allowing explicitly identified shuffle blocks as immutable inputs. Report decision/transition time, sunk shuffle, local/remote bytes, broadcast bytes, peak memory, canceled/discarded work, retries, join time, critical path, and net cost against a control.

### Answer 4

Measure complete per-partition bytes, time, decoded expansion, and key frequencies. Flag candidates using both median-relative and absolute thresholds. For each hot key, determine whether a side can be range/salt split and whether the other side may be replicated under that outer-join orientation. Preserve each matching pair once and designate exactly one subtask to emit unmatched preserved-side rows after all matching slices are known. Version the new partition/salt map and require every consumer to use it. Cap replicated bytes, subpartitions, task count, transition shuffle, and memory. Fence old attempts and deduplicate observations. Differentially test duplicates, null keys, no-match/all-match keys, residual predicates, both preserved orientations, retry/speculation, missing slices, and cancellation; compare multisets and required order separately.

### Answer 5

Run AQE disabled/enabled on immutable snapshots and compare exact results, errors, ordering contracts, and committed side effects. Cover empty and huge intermediates, correlation, stale estimates, null/outer/semi/anti joins, nondeterministic functions, skew/hot keys, compressed expansion, connectors, and concurrent tenants. Property-test partition maps and exactly-once output. Inject partial/inconsistent statistics, losing attempts, optimizer timeout/crash, coordinator restart, missing/corrupt exchanges, memory pressure, worker loss, and commit races. Verify fixed authorization/snapshot, tenant-scoped telemetry, encrypted retained state, expiry, and redaction. Shadow decisions first; then canary by rule, workload, connector, and risk. Attribute observation, optimizer, transition, discarded/reused work, latency tails, memory, spill, network, retries, fleet cost, and realized versus predicted gain. Kill-switch on mismatch, duplicate/lost output, recovery failure, bound breach, or severe regression; rollback to the static valid plan and compatible stable boundary.
