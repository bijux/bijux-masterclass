---
module_id: DBE-069
program: Database Engineering
level: 2
module_number: 69
title: Adaptive Query Processing
status: complete
last_verified: 2026-08-30
---

# Adaptive Query Processing

## One-Page Review

### Governing question

How can a query processor use observations made during or after execution to improve physical decisions without changing results, violating isolation, duplicating effects, oscillating, or spending more on adaptation than it saves?

### Essential definitions

**Adaptive query processing (AQP)** uses runtime evidence to revise query-processing decisions. **Intra-query adaptation** changes an active execution; **inter-query feedback** changes later executions. An **observation point** measures cardinality, bytes, skew, latency, memory, or availability. A **decision point** admits a choice. A **safe cut** is an execution boundary at which state and output obligations can be transferred without loss or duplication. **Reoptimization** invokes planning with runtime facts. **Operator morphing** selects or changes algorithms inside a prepared physical operator. A **dynamic filter** is a runtime-derived conservative predicate. **State transfer** maps the old execution state to the replacement. **Adaptation regret** is realized objective under the adaptive policy minus a reference-best policy with the same information and constraints.

### Central model, mechanism, or theorem

At decision point (t), switch from incumbent (p) to alternative (q) only if both are semantically interchangeable from the current state and

\[
C_{observe}+C_{decide}+C_{transfer}+E[C_{remaining}(q)] + R_{risk}
< E[C_{remaining}(p)]-H,
\]

where already incurred cost is sunk, (H) is hysteresis, and (R_{risk}) prices uncertainty and operational risk. Correctness requires a state relation: every not-yet-produced logical result remains reachable exactly once, every already committed result is excluded from replay, snapshot and authorization remain unchanged, and failure recovery agrees with the engine's execution protocol.

### Critical invariants

- Runtime evidence is bound to query, plan/operator, input epoch, snapshot, parameter/security context, and measurement semantics.
- Adaptation changes physical execution only; bag results, ordering guarantees, transaction behavior, privileges, and row policies remain identical.
- Costs already incurred are sunk; compare remaining alternatives plus transition overhead.
- A checkpoint is safe only with explicit ownership of buffered, in-flight, emitted, spilled, and remotely committed state.
- Dynamic filters may retain false positives but cannot reject a possible match; join type and filter completeness govern where they are legal.
- Decisions are bounded by time, memory, variants, retries, and plan-search budget, with a deterministic fallback.
- Feedback has versioning, confidence, decay, isolation, poisoning resistance, and anti-oscillation controls.
- Evaluation includes adaptation overhead and negative cases where remaining static is correct.

### Common failures

Failures include adapting at an arbitrary operator edge; replanning from original estimates rather than materialized facts; comparing full alternative cost with only incumbent remaining cost; replaying already emitted rows; losing unmatched rows in outer/anti joins through a dynamic filter; changing snapshot or policy on restart; waiting indefinitely for runtime evidence; using one execution's spill or skew as universal truth; repeatedly flipping near a threshold; persisting feedback across incompatible schema or resource generations; and reporting only successful adaptations.

### Compact example

A barrier reveals 40,000 rows where 2,000 were estimated. Including upstream work, a static nested-loop continuation costs 1,220,000 normalized units. Reoptimization plus a hash continuation costs 155,000, saving 1,065,000. If 10,000 rows have already passed through the loop, that 300,000 cost is sunk; switching the remaining 30,000 rows costs 125,000 versus 900,000 to continue, for a final 425,000. A 20 GiB shuffle coalesces to 80 target-sized partitions; a 3 GiB skewed partition splits into 12. A dynamic filter arriving after 30% of a 10-million-row scan reduces processed rows to 3.35 million, not the ideal 0.5 million. These are finite equations, not universal engine behavior.

### Connections

Retrieve [Cardinality Estimation](064-cardinality-estimation.md), [Cost Models](065-cost-models.md), [Join Ordering](066-join-ordering.md), [Access-Path Selection](067-access-path-selection.md), and [Plan Caching and Parameter Sensitivity](068-plan-caching-and-parameter-sensitivity.md). Continue through [the roadmap](../ROADMAP.md) to plan diagnosis.

## Governing Question

Traditional query processing draws a clean line: optimization predicts; execution obeys. The line is useful but artificial. During execution, the engine learns actual row counts, widths, distinct values, skew, partition sizes, spill behavior, service latency, and available resources—precisely the quantities that compilation had to estimate. Adaptive query processing asks when that information arrives early enough, at a safe enough boundary, and with enough expected benefit to change course.

The hard part is not detecting that an estimate was wrong. It is changing an active distributed state machine without changing the query. An operator may have emitted rows, built a hash table, spilled partitions, sent exchange messages, acquired locks, invoked a remote system, or updated progress durable enough to survive retry. A replacement plan must account for every one of those effects. AQP is therefore a correctness-and-control problem before it is an optimization technique.

## Why This Matters

Estimates fail for reasons that cannot always be eliminated before execution: correlation, user-defined functions, temporary/intermediate data, remote sources, rapidly changing partitions, parameter values, data skew, stale or absent statistics, and concurrent resource variability. One cardinality error propagates through join ordering, build-side selection, memory grants, parallelism, exchange layout, and access paths. Long analytical or federated queries make the resulting regret large enough to justify adaptation.

Distributed engines also create natural observation barriers. A shuffle or materialized stage has an exact byte and row distribution before downstream work starts. That information can coalesce tiny partitions, split skewed ones, change join strategy, or reorder remaining joins. Pipelined engines have fewer cheap barriers but can morph a prepared adaptive join, route tuples continuously, publish a runtime filter, or stop and reoptimize after a guarded checkpoint.

Current implementations occupy different points in this design space. Spark 4.0.2 documents Adaptive Query Execution using runtime statistics to coalesce post-shuffle partitions, convert join strategies, and handle skew. Trino 483 documents adaptive partitioned-join input reordering under fault-tolerant execution and dynamic filters that flow from join build to scans. SQL Server documents adaptive joins that defer hash-versus-loop choice and feedback for memory grants and cardinality assumptions. Oracle documents adaptive plans and statistics mechanisms. BigQuery documents history-based optimization for later similar executions. Product names differ; the durable axes are observation time, decision scope, state boundary, evidence lifetime, and recovery contract.

## Prerequisites and Retrieval

Retrieve these concepts before proceeding:

- cardinality and cost estimates are conditional models with uncertainty;
- physical plans carry order, partitioning, parameter, memory, and execution-mode properties;
- pipeline breakers materialize state, while pipelined operators exchange incremental batches;
- joins have bag/null semantics and preserved sides;
- snapshots, row policies, remote side effects, and retry protocols are semantic constraints;
- distributed exchanges have epochs, partitions, acknowledgements, cancellation, and failure recovery;
- a cache or feedback store needs precise identity, dependencies, generations, and eviction.

The chapter assumes familiarity with hash and nested-loop joins, shuffles, memory grants, runtime filters, cost-based optimization, and latency percentiles.

## Learning Objectives

After completing this module, you should be able to:

1. classify an adaptive mechanism by observation time, decision time, scope, and state boundary;
2. derive whether a switch is beneficial using remaining cost and transition overhead;
3. prove state-transfer and output-accounting obligations at a safe cut;
4. design conservative dynamic filters and adaptive join/partition choices;
5. distinguish intra-query adaptation from feedback that affects later executions;
6. prevent oscillation, feedback poisoning, unbounded planning, and resource amplification;
7. validate and roll out adaptation with semantic, performance, failure, security, and rollback evidence.

## Core Exposition

**Map the adaptation space.** An adaptive system has five independent choices. It observes something: rows, bytes, distinctness, skew, latency, memory, spill, selectivity, resource availability, or failure. It observes at some time: per tuple/batch, operator completion, stage barrier, query completion, or across many executions. It controls something: routing, join algorithm/order/distribution, access path, filter, partition count, parallelism, memory, materialization, remote placement, or future compilation. It operates at a scope: operator, pipeline, remaining subplan, whole query, fingerprint, tenant, or workload. Finally, its evidence expires under some dependency and drift policy.

Calling all of these “reoptimization” hides important distinctions. An adaptive join can include both loop and hash continuations in one compiled operator and decide after seeing build cardinality. Stage replanning invokes optimizer rules after materialization. Eddies continuously route tuples among eligible operators. A runtime filter adds conservative knowledge without replacing the plan. Memory-grant feedback modifies a later execution. Each has different correctness, latency, and observability obligations.

**Observation must be trustworthy and scoped.** Define what a counter means. Rows entering an operator differ from rows surviving its residual; bytes compressed differ from decompressed resident bytes; observed build distinctness may be incomplete; elapsed time includes queueing and interference. Bind an observation to query attempt, operator and plan version, input epoch/partition, snapshot, parameter class, principal/tenant, resource class, and measurement version. Mark whether it is complete, sampled, censored by cancellation, or affected by failure.

Runtime evidence is more concrete than a compile-time estimate, but not automatically representative. A first partition may be unskewed while a later one contains a heavy hitter. A remote source may recover after a slow batch. A completed shuffle gives exact sizes for that attempt yet says little about tomorrow's workload. Match the decision horizon to the evidence horizon.

**Choose decision points deliberately.** Cheap decision points already exist at materialization, sort, hash-build completion, exchange/stage boundaries, cursor suspension, or transactional statement boundaries. They expose complete state and often have not emitted downstream output. Pipelined decision points react earlier but require accounting for in-flight batches and partially built operator state. Adding a checkpoint can improve decisions while increasing memory, disk I/O, latency, and lost pipelining. The checkpoint itself belongs in the cost model.

The 2007 AQP survey organizes foundational approaches and settings; Kabra and DeWitt detect suboptimality during execution and reoptimize; Markl and colleagues' progressive optimization uses cardinality checks to trigger controlled reoptimization; Avnur and Hellerstein's Eddies continuously reorder tuple routing at moments of symmetry. These are not interchangeable recipes. Stop-and-restart favors clear materialization boundaries; continuous routing favors operators that expose symmetric, composable state.

**Compare remaining cost, never alternate total cost.** Suppose an incumbent has consumed 30% of its input. That work cannot be recovered. The decision compares `continue_remaining` against `observe + decide + drain/cancel + state_transfer + alternative_remaining + risk`. Including the alternative's work from the beginning double-counts; ignoring its rebuild or replay understates switching cost. If already emitted output cannot be revoked or deduplicated, some alternatives are simply infeasible.

Use uncertainty. A measured cardinality can be exact while future selectivity, cache, or network cost is uncertain. Require an improvement margin larger than model error and transition risk. A low-regret robust continuation can be preferable to a nominally cheapest switch. Place hard budgets on optimizer time, number of switches, materialization bytes, additional network, and recovery complexity.

**Define the safe-cut proof.** Let logical output be a bag (O). At switch time, partition it into already committed output (O_c), buffered/in-flight output (O_b), and not-yet-produced output (O_r). The transition must prove:

1. `O_c` is never replayed;
2. every occurrence in `O_b` has exactly one owner and is committed or discarded/recomputed consistently;
3. the replacement produces exactly `O_r`, including duplicates and null-extended rows;
4. snapshot, parameter, collation, function, authorization, and row-policy semantics are unchanged;
5. locks, spills, remote reads, memory, and generated code are released or transferred safely;
6. cancellation, retry, and worker loss cannot mix incompatible epochs.

A materialized relation with stable row occurrence identities is a convenient restart input. A pipeline that has sent unacknowledged batches needs sequence/epoch ownership. A query that performs external writes or volatile calls may not admit replay at all. Adaptive execution should be conservative around side effects, nondeterminism, and user-visible streaming.

**Reoptimize from facts, not from the original fiction.** Materialized intermediates become temporary base relations with exact row count and measurable width/distribution. Preserve lineage, schema, nullability, keys where proven, ordering/partitioning, snapshot, and security labels. The optimizer may still estimate downstream predicates and joins, but it must not replace an observed 40,000 rows with the original 2,000 estimate. Avoid double-applying a predicate already embodied in the materialization.

Reoptimization search must honor state constraints. Already chosen scans, emitted partitions, remote requests, or built structures may limit join orders and physical properties. The remaining plan's cost includes reading/materializing the checkpoint and transferring useful state. A fresh unconstrained whole-query optimum may be impossible from the current execution state.

**Operator morphing narrows the proof surface.** An adaptive join can defer loop-versus-hash choice until its build input count is known. Both alternatives are embedded and share one input/output contract. SQL Server's current documentation describes an adaptive join threshold after the first input is scanned. Similar operators can switch aggregation representation, spilling strategy, vector mode, or probe batching. The narrower scope reduces replan time and state complexity, but only choices anticipated at compilation are available.

Thresholds derive from remaining costs. If loop cost is (aN+b) and hash cost (hN+k), solve the crossover and add memory/parallelism constraints. Equality belongs deterministically to one branch. Validate below, at, and above threshold; include row width, duplicates, residual work, ordering, and memory denial. A cardinality threshold alone is not universally sufficient.

**Adapt at stage boundaries in distributed engines.** A completed shuffle reveals total bytes and per-partition distribution. The engine can coalesce many tiny downstream partitions to reduce scheduler overhead, split a skewed partition to limit stragglers, or select broadcast versus partitioned join if the materialized side meets memory and network constraints. Spark's current AQE documentation is a concrete example. Trino's current fault-tolerant adaptive planning can reorder partitioned join inputs using actual sizes.

Stage replacement must version exchanges. Consumers accept only the selected plan/partition epoch; abandoned tasks are cancelled; speculative duplicates have one committed owner; shuffle files remain until all selected consumers finish; retry reconstructs the same logical stage or advances atomically to a new epoch. A “better” partition count that loses locality, exceeds open-file/scheduler limits, or conflicts with failure recovery is not better.

**Dynamic filters adapt data movement conservatively.** After building a selective join side, the engine can publish its keys, ranges, or Bloom filter toward probe scans, partition enumeration, and remote connectors. Trino documents build-side value collection, coordinator/worker distribution, connector-specific pushdown, thresholds, and fallbacks from distinct values toward coarser ranges.

Correctness depends on join semantics and filter lifecycle. For an inner or semi join, a complete no-false-negative membership filter can reject probe rows absent from build keys; positives still require the join. Filtering the preserved side of an outer join can erase required unmatched rows. Anti joins need special null semantics. An incomplete filter cannot reject keys that may arrive later unless publication is monotone and rejection waits for a completeness barrier. Type, collation, canonicalization, hash seed/version, null/NaN, corruption, epoch, and retry must match. Failure or timeout disables filtering and continues safely.

Late filters have partial value. If 30% of a scan completed before a 5%-selective filter arrived, only the remaining 70% benefits. Waiting for the filter trades reduced I/O against idle latency and possible failure. Use a bounded wait based on expected remaining savings, not an unconditional barrier.

**Continuous routing expands flexibility.** Eddies route tuples through operators in variable orders and learn which routes make progress. Moments of symmetry permit reordering; synchronization barriers constrain it. This can respond to changing source latency or selectivity without choosing one static order. It also complicates tuple lineage, routing state, fairness, memory, backpressure, and reproducibility. Starving a slow route can delay the only tuples that produce results. Use bounded exploration and preserve exact operator eligibility per tuple.

**Feedback across executions is different.** Query completion can update future cardinality assumptions, memory grants, parallelism, or plan choices. SQL Server documents memory-grant feedback—including persistence and percentile behavior in current versions—and cardinality-estimation feedback. BigQuery documents history-based optimizations that use prior similar executions and revoke changes that do not help. This evidence arrives too late for the completed execution; its correctness and economics depend on stable identity across future executions.

Feedback needs the cache discipline from DBE-068: fingerprint and parameter/context class; schema, policy, model, and resource generations; sample count; confidence; decay; persistence and replica/failover semantics; and bounded influence. Oscillating workloads can alternate between under- and over-grants. Last-observation control amplifies the oscillation; percentile/history-based policies reduce spills but may reserve too much memory and lower concurrency. Detect instability, keep class-specific feedback where justified, apply hysteresis, or disable/fallback safely.

**Control loops can become unstable.** A controller observes delayed consequences of its previous action. If it reacts too aggressively, thresholds chase noise: increase memory after a spill, then shrink after an unusually small execution, then spill again. Changing parallelism alters queueing, which changes measured latency and triggers another change. Multiple controllers—join choice, memory, autoscaling, admission—can fight.

Specify controlled variable, actuator, sampling window, delay, bounds, and objective. Prefer monotone decisions within one query unless a formally safe reversal exists. Add deadbands/hysteresis, minimum residence time, rate limits, confidence thresholds, and maximum adaptations. Coordinate resource changes with workload admission. Record non-adaptation reasons; restraint is an outcome, not missing telemetry.

The executable below verifies finite cost, partition, and filter arithmetic only.

<!-- bijux-verify: {"id":"finite-adaptive-query-decisions","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"estimated_rows=2000\nactual_rows=40000\nestimate_ratio=20.00\nstatic_total_cost=1220000\nadaptive_checkpoint_cost=155000\ncheckpoint_savings=1065000\ncheckpoint_switch=true\nlate_sunk_cost=300000\nlate_continue_cost=900000\nlate_switch_remaining_cost=125000\nlate_total_cost=425000\nlate_savings=775000\nsafe_cut_required=true\nshuffle_mib=20480\ncoalesced_partitions=80\nskew_partition_mib=3072\nskew_splits=12\ndynamic_filter_processed_rows=3350000\ndynamic_filter_saved_rows=6650000\ndynamic_filter_false_negatives_allowed=false\nfeedback_epoch_required=true\nevidence=finite_adaptive_decisions\n","stderr":""}} -->
```python
from math import ceil

estimated_rows = 2_000
actual_rows = 40_000
upstream_cost = 20_000
nested_per_row = 30
hash_fixed = 50_000
hash_per_row = 2
reoptimization = 5_000

static_total = upstream_cost + actual_rows * nested_per_row
adaptive_checkpoint = upstream_cost + reoptimization + hash_fixed + actual_rows * hash_per_row

processed_before_late_switch = 10_000
remaining_rows = actual_rows - processed_before_late_switch
late_sunk = processed_before_late_switch * nested_per_row
late_continue = remaining_rows * nested_per_row
state_transfer = 15_000
late_switch_remaining = state_transfer + hash_fixed + remaining_rows * hash_per_row
late_total = late_sunk + late_switch_remaining

shuffle_mib = 20 * 1024
target_partition_mib = 256
skew_partition_mib = 3 * 1024

fact_rows = 10_000_000
fraction_scanned_before_filter = 0.30
filter_selectivity = 0.05
before_filter = int(fact_rows * fraction_scanned_before_filter)
after_filter = int((fact_rows - before_filter) * filter_selectivity)
processed_with_filter = before_filter + after_filter

print(f"estimated_rows={estimated_rows}")
print(f"actual_rows={actual_rows}")
print(f"estimate_ratio={actual_rows / estimated_rows:.2f}")
print(f"static_total_cost={static_total}")
print(f"adaptive_checkpoint_cost={adaptive_checkpoint}")
print(f"checkpoint_savings={static_total - adaptive_checkpoint}")
print(f"checkpoint_switch={str(adaptive_checkpoint < static_total).lower()}")
print(f"late_sunk_cost={late_sunk}")
print(f"late_continue_cost={late_continue}")
print(f"late_switch_remaining_cost={late_switch_remaining}")
print(f"late_total_cost={late_total}")
print(f"late_savings={actual_rows * nested_per_row - late_total}")
print("safe_cut_required=true")
print(f"shuffle_mib={shuffle_mib}")
print(f"coalesced_partitions={ceil(shuffle_mib / target_partition_mib)}")
print(f"skew_partition_mib={skew_partition_mib}")
print(f"skew_splits={ceil(skew_partition_mib / target_partition_mib)}")
print(f"dynamic_filter_processed_rows={processed_with_filter}")
print(f"dynamic_filter_saved_rows={fact_rows - processed_with_filter}")
print("dynamic_filter_false_negatives_allowed=false")
print("feedback_epoch_required=true")
print("evidence=finite_adaptive_decisions")
```

**Diagnose first divergence.** Freeze query text/bindings, snapshot, parameter and security context, schema/statistics/model generations, input data, resource class, configuration, and attempt/epoch. Compare original and adapted traces. Ask: which estimate or runtime condition diverged; was observation complete and correctly scoped; why was this decision point legal; which alternatives were eligible; did remaining benefit exceed observation/replan/transfer/risk; was state accounted exactly once; did the system adapt too early, too late, repeatedly, or not at all; and did failure/retry alter the result?

An adaptation marker without the trigger, evidence, old/new state, and rejection alternatives is not diagnosable. Preserve privacy-safe decision records and sampled operator metrics. Explain why adaptation was skipped: insufficient benefit, unsafe state, low confidence, budget exhausted, unsupported operator, resource denial, or fallback.

**Validate from semantics outward.** Use small exhaustive bags with duplicates, nulls, empty inputs, heavy hitters, adversarial partitions, outer/semi/anti joins, ordering, LIMIT, nondeterministic expressions, row policies, and multiple snapshots. Differentially compare adaptive output with a nonadaptive oracle as a bag plus required properties. Inject observation at every boundary and failure before/during/after state transfer. Duplicate, delay, reorder, corrupt, and lose exchange/filter/control messages. Exercise cancellation and retry epochs.

Then validate decision arithmetic against enumerated alternatives for finite plans, and replay representative distributions with adaptation disabled as the control. Report trigger coverage, false/late triggers, regret, planning/transition overhead, materialization and network, peak memory/spill, task count/skew, filter arrival/use, CPU, throughput, latency tails, fairness, and workload interference. Include queries where static execution wins.

**Productionize reversibly.** Version observation schema, decision rules/model, thresholds, physical alternatives, state-transfer protocol, feedback, and compatibility dependencies. Shadow observations and decisions without switching. Canary bounded fingerprints, tenants, join types, connectors, and resource pools. Gate on result equivalence, no unauthorized access, bounded adaptation/retry, p50/p95/p99 and worst-class regret, memory/disk/network, compile/scheduler pressure, error rate, and recovery. A kill switch must stop new adaptations without invalidating correct in-flight work; rollback restores the prior compatible plan/control policy and invalidates incompatible feedback.

## Definitions and Notation

- **Observation point**: location/time at which runtime evidence becomes available.
- **Decision point**: location/time at which an alternative may legally be chosen.
- **Safe cut**: boundary with a proof of state, output, snapshot, and failure ownership.
- **Incumbent / alternative**: current continuation and candidate replacement.
- **Sunk cost**: incurred cost that cannot influence the remaining-choice comparison.
- **State transfer**: transformation from incumbent state to the alternative's valid starting state.
- **Epoch**: version distinguishing compatible execution, exchange, filter, or feedback state.
- **Operator morphing**: selecting/changing an algorithm inside an operator contract.
- **Stage reoptimization**: replanning a remaining subgraph from materialized runtime facts.
- **Continuous routing**: choosing eligible next operators per tuple/batch during execution.
- **Dynamic filter**: runtime-derived exact or conservative predicate used to avoid future work.
- **Inter-query feedback**: observations from completed attempts used for later attempts.
- **Hysteresis/deadband**: margin that prevents decisions from flipping on small/noisy changes.
- **Adaptation regret**: realized adaptive objective minus reference-best eligible objective with comparable information.
- **Fallback**: deterministic safe continuation when adaptation is unsafe, unavailable, or uncertain.

Adaptivity is not approximation. Unless the query explicitly permits approximate results, every adaptive path must implement the exact query semantics.

## Mechanisms, Invariants, or Proof Structure

**Remaining-cost rule.** At time t, the same incurred cost appears in both “continue” and “switch” totals and cancels. Switch exactly when transition plus alternative remaining cost and risk is lower than incumbent remaining cost by the hysteresis margin. This proof prevents two symmetric errors: charging the alternative for already completed work and pretending rebuild/transfer is free.

**Output partition proof.** At a safe cut, occurrence identities divide logical output obligations into committed, buffered/in-flight, and remaining disjoint bags. Ownership and acknowledgement decide whether each buffered occurrence commits or returns to remaining. The replacement consumes only the remaining domain under the same snapshot/policy and emits each remaining occurrence once. If no such partition can be established, restart is unsafe.

**Dynamic-filter proof.** For build keys B and probe occurrence r with key k, reject r only if a complete filter F guarantees `F(k)=false => k not in B` under identical equality/hash/null semantics and the join may legally discard unmatched r. False positives add work but preserve results. An incomplete, corrupt, mismatched, or stale filter becomes “unknown/keep,” never “reject.”

**Stage-epoch invariant.** Each producer output, partition map, consumer, and acknowledgement binds one selected epoch. Publication atomically chooses the downstream graph; consumers reject abandoned-epoch data. Retry either reproduces the same epoch contract or publishes a later complete mapping. This prevents mixtures of old/new partitioning and duplicated speculative output.

**Bounded-controller invariant.** Per query/fingerprint, adaptation consumes declared budgets for observations, planning time, state bytes, switches, and retries. Decisions require confidence and improvement margin; a deadband and residence rule prevent oscillation. Exhaustion selects fallback and is observable, never an unbounded search.

**Evidence separation.** Formal invariants establish semantic obligations. Executable arithmetic establishes finite model outputs. Fault injection establishes behavior for tested schedules. Replay establishes scoped economics. Canary establishes bounded production behavior. None proves universal safety, representativeness, optimality, or absence of security leakage.

## Alternatives and Trade-Offs

**Static robust planning** has low overhead and reproducible behavior; it may accept some regret to avoid catastrophic plans. **Operator morphing** reacts cheaply at a narrow choice but must anticipate alternatives. **Checkpoint reoptimization** uses richer optimizer logic and accurate intermediate facts but pays materialization, planning, and state-transfer cost.

**Stop-and-restart** offers a clean state boundary when output is uncommitted; it discards work. **Reuse/materialize-and-continue** preserves expensive intermediates; it constrains the remaining search and consumes storage. **Continuous routing** adapts quickly to latency/selectivity changes; it increases per-item control overhead and state complexity.

**Dynamic filters** reduce scan/network work and are easy to ignore safely; they can arrive late, cost collection/distribution, leak sensitive value summaries, and are restricted by join semantics. **Adaptive repartitioning** combats skew and tiny tasks; more tasks/files/messages can harm scheduler and storage systems.

**Within-query facts** are timely and specific but may arrive after much work. **Cross-query feedback** amortizes learning and can persist improvements; workload/parameter/schema/resource drift makes old feedback hazardous. **Last-value feedback** reacts fast but oscillates; **percentile/windowed feedback** is stable against individual noise but may overprovision and lag change.

**Full reoptimization** explores broad alternatives; timeouts and plan churn grow. **Rule-based adaptation** is predictable and cheap; thresholds age. **Learned control** can use multidimensional evidence; it adds training bias, uncertainty, poisoning, privacy, interpretability, and versioning concerns. Always preserve a deterministic safe fallback.

## Failure Modes and Misconceptions

1. “Actual rows make the next plan correct” ignores downstream uncertainty and model error.
2. “Any operator boundary is a checkpoint” ignores buffered, in-flight, emitted, spilled, and external state.
3. “Restarting a SELECT is harmless” ignores streaming output, volatile calls, locks, snapshots, remote effects, and retries.
4. “The new full plan is cheaper” is the wrong comparison after sunk work.
5. “Reoptimization starts from the original query” ignores materialized facts and irreversible choices.
6. “A dynamic filter is only a hint” false negatives or illegal preserved-side filtering change results.
7. “Bloom filters are safe by definition” construction, completeness, hashing, corruption, and epochs can violate the premise.
8. “Wait for the runtime filter” can stall longer than remaining saved work.
9. “More partitions fix skew” can amplify scheduler, metadata, file, and network overhead.
10. “Adaptive join depends only on row count” ignores width, order, memory, residuals, and resource availability.
11. “Feedback from one run improves the next” ignores parameter class, concurrency, censoring, and drift.
12. “Fast reaction is good control” delayed aggressive controllers can oscillate or fight other controllers.
13. “No adaptation means the feature failed” staying static can be the optimal bounded decision.
14. “Mean latency proves value” hides transition spikes, stragglers, worst classes, and fleet interference.
15. “Canary rollback means clearing all state” indiscriminate cache/feedback clearing destroys evidence and affects unrelated work.

## Worked Examples

### Example 1

**Checkpoint crossover.** A materialized stage contains 40,000 rows, 20 times the estimate. Continuing nested loops costs 1,200,000 downstream units; hash costs 130,000 plus 5,000 reoptimization. With 20,000 already spent upstream, totals are 1,220,000 and 155,000. Conclusion: the barrier provides both a safe cut and enough remaining benefit to switch.

### Example 2

**Sunk-cost correction.** After 10,000 rows cost 300,000 under loops, only 30,000 remain. Continue costs 900,000; transfer plus hash costs 125,000. Final adaptive cost is 425,000, not 125,000, yet the decision compares 125,000 with 900,000. Conclusion: report total outcome but decide on remaining costs.

### Example 3

**Unsafe streamed restart.** A client has acknowledged 1,000 duplicate-bearing rows without stable occurrence IDs. Restarting from the original scan could replay them, while filtering by values could remove legitimate duplicates. Conclusion: without a committed-output boundary or exact resume token, full restart is not a legal alternative.

### Example 4

**Adaptive join threshold.** Loop cost is `30N`; hash cost is `50,000+2N`. Equality occurs at `N=50,000/28≈1,785.71`, so integers through 1,785 choose loops and 1,786+ choose hash under this model. Memory denial can remove hash eligibility. Conclusion: threshold ownership and feasibility must be explicit.

### Example 5

**Post-shuffle sizing.** A 20 GiB shuffle and 256 MiB target yield 80 partitions. One 3 GiB partition splits into 12 target-size pieces. Empty/tiny partitions may be coalesced, but locality and task/file limits constrain the final map. Conclusion: actual bytes improve sizing, while operational properties remain part of the decision.

### Example 6

**Late dynamic filter.** A 5%-selective complete filter arrives after 30% of 10 million probe rows were scanned. Work is 3 million unfiltered plus 350,000 filtered survivors: 3.35 million, saving 6.65 million. Conclusion: arrival time belongs in benefit estimation; ideal full-scan filtering would overstate savings.

### Example 7

**Outer-join counterexample.** A left join's probe/preserved row has no build match. Applying a build membership filter to discard it loses the required null-extended result. The filter may instead optimize the non-preserved input or mark “definitely unmatched” while retaining the row for null extension. Conclusion: filter legality derives from join semantics.

### Example 8

**Epoch race.** Stage plan epoch 7 has 100 partitions. Reoptimization publishes epoch 8 with 40 partitions while a delayed epoch-7 task completes. Epoch-8 consumers reject its message; ownership metadata retains or deletes old shuffle files only after all epoch-7 claims close. Conclusion: atomic graph publication and epoch validation prevent mixed layouts.

### Example 9

**Feedback oscillation.** Alternating executions use 100 MiB and 1,000 MiB. A controller granting the last observed usage repeatedly overgrants then spills. A class-aware policy separates parameters; a percentile policy avoids spills but may reserve 1,000 MiB for small runs; instability detection can disable feedback. Conclusion: adaptation objective includes concurrency and stability, not only spill avoidance.

### Example 10

**Production regression.** An adaptive repartitioner lowers one query's p95 but doubles task count fleet-wide, overwhelms the scheduler during retries, and exposes tenant-key ranges in diagnostics. The revision caps tasks/metadata, redacts ranges, injects retry and coordinator-failure tests, shadows decisions, canaries workload cohorts, and retains the static mapping. Conclusion: query-local gain cannot override system, security, and recovery gates.

## Cross-Program Connections

- [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md): safe points, state transfer, epochs, atomic publication, backpressure, and control races implement adaptation.
- [Algorithm Engineering](../../16-algorithm-engineering/ROADMAP.md): online algorithms, competitive/regret analysis, thresholds, robust choice, and bounded search evaluate decisions.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md): Bloom filters, sketches, routing tables, queues, partition maps, and versioned state support observations and control.
- [Data Engineering](../../19-data-engineering/ROADMAP.md): shuffles, partitions, skew, stage materialization, lineage, and replay provide distributed adaptation boundaries.
- [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md): workload boundaries, data placement, tenant isolation, and serving contracts constrain evidence reuse.
- [Large-Scale Data Systems Engineering](../../21-large-scale-data-systems-engineering/ROADMAP.md): fault tolerance, speculative execution, scheduling, exchanges, and autoscaling interact with adaptive plans.
- [Security Engineering](../../25-security-engineering/ROADMAP.md): runtime summaries, feedback poisoning, cross-tenant leakage, authorization, and audit govern adaptive evidence.
- [Platform Engineering](../../29-platform-engineering/ROADMAP.md): capacity, fleet configuration, canaries, observability, kill switches, and rollback operationalize control loops.

## References

1. Amol Deshpande, Zachary Ives, and Vijayshankar Raman, [“Adaptive Query Processing”](https://doi.org/10.1561/1900000001), *Foundations and Trends in Databases* 1(1), 2007. Foundational survey and framework for intra-query adaptivity.
2. Ron Avnur and Joseph M. Hellerstein, [“Eddies: Continuously Adaptive Query Processing”](https://doi.org/10.1145/342009.335420), *SIGMOD 2000*. Primary continuous tuple-routing and moments-of-symmetry work.
3. Navin Kabra and David J. DeWitt, [“Efficient Mid-Query Re-Optimization of Sub-Optimal Query Execution Plans”](https://doi.org/10.1145/276304.276315), *SIGMOD 1998*. Primary mid-query detection and correction work.
4. Volker Markl et al., [“Robust Query Processing through Progressive Optimization”](https://doi.org/10.1145/1007568.1007642), *SIGMOD 2004*. Primary cardinality-check and progressive-reoptimization work.
5. Apache Spark, [Spark 4.0.2: Performance Tuning—Adaptive Query Execution](https://spark.apache.org/docs/4.0.2/sql-performance-tuning.html#adaptive-query-execution), retrieved 2026-08-30. Current post-shuffle coalescing, join conversion, and skew handling.
6. Trino Software Foundation, [Trino 483: Adaptive Plan Optimizations](https://trino.io/docs/current/optimizer/adaptive-plan-optimizations.html), retrieved 2026-08-30. Current fault-tolerant adaptive join-input reordering.
7. Trino Software Foundation, [Trino 483: Dynamic Filtering](https://trino.io/docs/current/admin/dynamic-filtering.html), retrieved 2026-08-30. Current filter collection, distribution, connector use, thresholds, metrics, and limitations.
8. Microsoft, [Intelligent Query Processing Features in Detail](https://learn.microsoft.com/en-us/sql/relational-databases/performance/intelligent-query-processing-details), retrieved 2026-08-30. Current adaptive joins and feedback-family overview.
9. Microsoft, [Memory Grant Feedback](https://learn.microsoft.com/en-us/sql/relational-databases/performance/intelligent-query-processing-memory-grant-feedback), retrieved 2026-08-30. Current batch/row, percentile, persistence, and instability behavior.
10. Microsoft, [Cardinality Estimation Feedback](https://learn.microsoft.com/en-us/sql/relational-databases/performance/intelligent-query-processing-cardinality-estimation-feedback), retrieved 2026-08-30. Current repeating-query CE feedback and persistence scope.
11. Oracle, [Oracle Database 21c SQL Tuning Guide: Adaptive Query Optimization](https://docs.oracle.com/en/database/oracle/oracle-database/21/tgsql/sql-tuning-guide.pdf), retrieved 2026-08-30. Adaptive plans and runtime-statistics mechanisms.
12. Google Cloud, [Use History-Based Optimizations](https://docs.cloud.google.com/bigquery/docs/history-based-optimizations), retrieved 2026-08-30. Current cross-execution optimization, observability, estimated impact, and revocation behavior.

## Exercises

### Exercise 1

Classify adaptive join morphing, post-shuffle replanning, Eddies, dynamic filters, memory-grant feedback, and history-based optimization by observation time, decision point, scope, state boundary, and evidence lifetime.

### Exercise 2

Recompute every executable result. Derive the loop/hash crossover, explain the late-switch sunk-cost calculation, and state exactly what the executable does and does not prove.

### Exercise 3

A distributed query adapts from 100 to 40 partitions while speculative tasks and a coordinator retry are active; duplicate rows appear. Design a diagnosis and a state/epoch protocol that prevents recurrence.

### Exercise 4

Design a runtime-filter protocol for inner, left outer, semi, and anti joins across remote connectors. Cover completeness, nulls, false positives, arrival/wait policy, thresholds, privacy, corruption, cancellation, and retry.

### Exercise 5

Design an elite validation and rollout system for a learned controller that may reorder joins, change parallelism, and update memory feedback across executions in a multi-tenant service.

## Answers to the Exercises

### Answer 1

Adaptive join morphing observes one input's actual size at build completion, decides inside one operator, chooses among precompiled continuations, and lives for the active execution/plan. Post-shuffle replanning observes complete stage bytes/rows/distribution at a materialized exchange, decides the downstream subgraph, and binds the replacement to a stage epoch. Eddies observe per-tuple/batch operator progress and source behavior, decide routing continuously at moments of symmetry, and retain routing/operator state for the active execution. Dynamic filters observe build keys/ranges during or at build completion, decide future scan/split rejection under join-specific legality, and bind filter completeness/version to the query attempt and epoch. Memory-grant feedback observes usage/spill at query completion, changes the grant for later matching executions, and lives in cache or a versioned persistent feedback store. History-based optimization aggregates completed similar executions, changes future planning, and requires broader identity, confidence, drift, and revocation policy. None may reuse evidence across incompatible schema, policy, parameter/resource, measurement, or security generations.

### Answer 2

Actual/estimated is `40000/2000=20`. Static total is `20000+40000*30=1,220,000`. Checkpoint adaptation is `20000+5000+50000+40000*2=155,000`, saving 1,065,000. At the late switch, 10,000 loop rows cost 300,000 and are sunk. Continuing 30,000 costs 900,000. Switching remaining work costs `15000+50000+30000*2=125,000`; final total is 425,000, saving 775,000 against the 1,200,000 downstream loop total. Solve `30N=50000+2N`: `N=50000/28≈1785.714`, so integer 1,785 favors loop and 1,786 favors hash if both are feasible. `20*1024/256=80` partitions; `3*1024/256=12` skew splits. A filter arriving after 3,000,000 rows processes those plus `7,000,000*.05=350,000`, saving 6,650,000. The code proves these finite arithmetic results under exact costs, sizes, selectivity, and a safe transition assumption. It proves no DBMS's cost model, safe-cut implementation, filter correctness, workload representativeness, or universal advantage of adaptation.

### Answer 3

Capture query/attempt, snapshot, logical stage, plan and partition-map generations, producer attempt, partition, batch sequence, speculative ownership, consumer acknowledgement, and commit records. Determine whether epoch-7 messages were accepted by epoch-8 consumers, whether two speculative producers both committed one logical partition, or whether coordinator recovery reconstructed stale ownership. Reconcile duplicate occurrence IDs back to source partitions and acknowledgements rather than deduplicating values, which would corrupt bags.

The protocol gives each logical stage a monotonically increasing epoch. Reoptimization writes a complete immutable epoch-8 graph and partition mapping, then atomically makes it selected. Every data/control message carries query attempt, stage epoch, logical partition, producer attempt, and sequence. Consumers accept only the selected compatible epoch and deduplicate retried batches by occurrence/sequence contract. A lease or consensus-backed commit record elects one speculative producer per logical output. Acknowledgements identify exact epoch/batches; old shuffle state remains quarantined until no valid consumer/reference exists. Coordinator recovery reads the durable selected epoch and ownership log, never infers from surviving files. Transition is tested with crashes before/after publication, delayed old messages, duplicate producers, lost acknowledgements, cancellation, and repeated coordinator failover. If exact ownership cannot be reconstructed, fail safely rather than return a mixed result.

### Answer 4

Canonicalize join keys with identical types, casts, collation, time-zone, null/NaN, and equality/hash version. For inner and semi joins, a complete exact set or no-false-negative Bloom filter may reject probe keys absent from build; positives still execute the join. A left join cannot discard its preserved left rows: a negative filter can route them directly to null-extension only if residual/other conditions and match semantics are fully accounted for. Filtering the non-preserved build may be legal under ordinary predicate rules. Anti joins require exact SQL null analysis; a build null can change `NOT IN` globally, so an ordinary membership-negative rule is unsafe. Encode join type and allowed action in the filter contract.

Build tasks publish epoch-scoped partial summaries only for monotone positive acceleration; negative rejection waits for a completeness barrier covering all build partitions. Coordinator combines summaries with authenticated checksums and size/distinct/range limits; overflow degrades exact set to a certified conservative representation or disables the filter. Remote connectors advertise supported types/operators and treat timeout, corruption, mismatch, cancellation, retry, or unsupported pushdown as unknown/keep. Wait only while expected remaining I/O/network saving exceeds bounded delay; expose arrival time, scan fraction, collected size, false-positive proxy, rejected/read partitions/rows, and fallback. Encrypt transport, restrict diagnostics, redact value/range summaries, isolate tenants, cap memory/network, and test empty/null/duplicate/skewed builds, late arrival, outer/semi/anti cases, cast/collation mismatch, malicious filters, failures, and epoch races against an unfiltered oracle.

### Answer 5

Define a typed action space and safe-cut/state-transfer proof for every join reorder and parallelism change; memory feedback for future executions has a separate identity/generation contract. Features bind authorized query fingerprint, parameter/resource class, schema/statistics/model, attempt/epoch, completion/censoring, and measurement semantics. Exclude or protect tenant-sensitive literals and distributions. Sign/version model, features, rules, alternatives, and feedback. Bound planning time, exploration, switches, state bytes, task/network amplification, grants, variants, and per-tenant influence. Low confidence, missing features, unsafe state, policy mismatch, budget exhaustion, or detected oscillation selects a deterministic static fallback.

Offline, exhaustively differential-test small relational bags with nulls, duplicates, outer/semi/anti joins, ordering, policies, snapshots, volatile/remote effects, and every decision boundary. Model-check or fault-inject state ownership across delayed/duplicate/corrupt messages, speculative execution, cancellation, worker/coordinator loss, and feedback races. Replay temporally and tenant-separated workloads with static, rule-based, and learned controls; execute eligible alternatives to measure per-class regret, uncertainty calibration, non-adaptation quality, planning/transfer overhead, memory/spill, task/network/disk, throughput, tails, fairness, and interference. Attack feedback with skewed tenants, censored failures, forged summaries, and drift.

Shadow the controller first, retaining decision/evidence/rejection traces without acting. Canary bounded fingerprints, tenant cohorts, connectors, join types, and resource pools against an unchanged control. Gates require exact results and authorization plus bounded p50/p95/p99, worst-class regret, errors, adaptations/retries, compile/scheduler CPU, memory, spill, disk/network, task counts, and fleet SLOs. Promotion widens gradually with automatic drift and oscillation brakes. A kill switch prevents new actions while allowing compatible in-flight epochs to finish; rollback selects the prior static controller and invalidates only feedback incompatible with its exact generations. Internal evidence remains scoped to tested versions and workloads and does not establish universal correctness, optimality, privacy, fairness, certification, or external review.
