---
module_id: DSE-060
program: Data Structures Engineering
level: 2
module_number: 60
title: Measuring Persistent-Structure Time and Memory
status: complete
last_verified: 2026-08-30
---

# Measuring Persistent-Structure Time and Memory

## One-Page Review

### Governing question

How can an experiment distinguish the time and memory consequences of persistence from language runtime, allocator, garbage collector, cache, workload, retention, and statistical noise—and produce evidence another engineer can reproduce and challenge?

### Essential definitions

- A **benchmark question** names the population, workload, implementations, metric, and decision the experiment informs.
- An **experimental unit** is the independently randomized/repeated unit supporting inference, such as a fresh process—not every inner-loop operation.
- A **warmup** prepares caches, runtime/JIT, lazy code, and allocators before the declared measured interval when steady-state behavior is the target.
- **logical size** counts abstract elements or occurrences; **physical size** counts distinct representation objects/bytes.
- **allocated bytes** count allocation traffic; **live bytes** remain reachable at a point; **peak live/managed bytes** are a high-water mark; **RSS** is process resident memory and includes more than language objects.
- A **retention set** is the version roots/readers/exports kept alive; it determines which shared nodes are live.
- **allocation amplification** is bytes or objects allocated per logical update; **write amplification** includes copied/persisted bytes.
- **structural sharing** means several logical roots reach the same physical node; identity-aware traversal must count it once.
- A **confidence interval** quantifies uncertainty for a defined estimator under stated assumptions/resampling design; it is not a correctness probability.
- A **practical threshold** is the smallest effect large enough to change an engineering decision.

### Central model, mechanism, or theorem

Measurement begins with a semantic oracle and deterministic structural counters. For each operation, record abstract result, comparisons/field reads, copied/allocated nodes, changed frontier, path depth, and retained distinct reachability. These counters explain *why* elapsed time or memory moves and remain reproducible when clocks vary.

Then run controlled experiments at the layer of the claim. Separate setup from measured work; consume results; use an appropriate monotonic/high-resolution clock or mature harness; randomize/counterbalance implementation order; repeat within and across independent processes; retain raw observations; and estimate effect plus uncertainty. Warm/cold, latency/throughput, current/old versions, and semantic-equivalent baselines are separate questions.

Persistent memory requires at least five ledgers: logical occurrences across versions, distinct nodes reachable from the declared retention set, cumulative allocations, peak traced/managed memory, and process/OS memory. None alone is “the memory footprint.” A path-copying tree can have 35 logical node occurrences across eight versions but only 20 distinct allocated/reachable nodes; retaining only two roots can reduce distinct reachability to 10 without changing either root's seven-element value.

### Critical invariants

1. Every compared implementation returns the same abstract answers for the same validated operation/version trace.
2. The workload distribution, version topology, retention policy, seeds, and operation ordering are explicit and reproducible.
3. Setup, warmup, measurement, validation, teardown, and profiling intervals are named; results cannot be optimized away or precomputed.
4. Timing reports clock/harness, units, batch size, process/fork hierarchy, environment, raw samples, estimator, interval, and exclusions.
5. Memory reports the allocator/runtime layer captured and distinguishes cumulative allocation, live/peak, distinct reachability, RSS, mapped/native, and retained-but-unused memory.
6. Shared physical nodes are identity-deduplicated; logical occurrences remain multiplicity-sensitive.
7. Reclamation experiments pin/unpin declared roots/readers and reach quiescence according to the collector/allocator model before interpretation.
8. Instrumentation overhead and unavailable counters are measured/reported, not silently mixed with uninstrumented results.
9. Complexity/empirical claims state their unit, workload, hardware/runtime/compiler/build, uncertainty, and external-validity boundary.
10. Evidence artifacts contain code/commit, commands, tool versions, environment, raw data, analysis, validation, and limitations.

### Common failures

- Timing one operation once or treating inner-loop observations as independent machines/processes.
- Measuring construction in one implementation but only queries in another.
- Allowing dead-code elimination, constant folding, cached results, or unconsumed outputs.
- Reporting a ratio without raw distributions, uncertainty, units, or a practical threshold.
- Comparing different abstract semantics, key distributions, retention sets, or GC policies.
- Summing shallow object sizes and double-counting shared subtrees—or missing referents entirely.
- Calling RSS “heap size” or traced Python memory “whole-process memory.”
- Measuring only the latest root when the product retains a version tree/DAG.
- Forcing GC for one candidate but including GC pauses for another.
- Publishing only a chart after discarding raw data, failures, environment, and commands.

### Compact example

Insert keys `4,2,6,1,3,5,7` into an immutable path-copying BST, retaining every root, then branch from the six-key version by inserting 8. Main updates allocate `1,2,2,3,3,3,3` nodes; the branch allocates 3. Across all eight nonempty roots there are 35 logical node occurrences but 20 distinct nodes. Retaining only the latest main root and branch leaves 14 logical occurrences, 10 distinct nodes, and 4 nodes shared by both roots. These exact counters explain retention/sharing independently of runtime byte layout.

### Connections

[DSE-051](051-path-copying.md) supplies changed-frontier costs; [DSE-052](052-structural-sharing.md) supplies identity/reachability; [DSE-053](053-persistent-lists-and-queues.md) supplies persistent amortization pitfalls; [DSE-059](059-full-and-confluent-persistence.md) supplies version-tree/DAG and logical amplification. The [program roadmap](../ROADMAP.md) next begins concurrent structures, where schedules and synchronization add further experimental dimensions.

## Governing Question

For a named persistent data structure, implementation, version/retention workload, runtime, and deployment target, what evidence establishes its semantic correctness and estimates its operation latency, throughput, allocation, live/peak/process memory, sharing, cache/GC behavior, and tail risk with enough provenance and uncertainty to guide a decision?

## Why This Matters

Asymptotic analysis remains necessary, but persistent structures expose constants and workload dimensions that a one-root ephemeral analysis can hide. A balanced-tree update may copy `O(log n)` nodes, yet node headers, allocator size classes, pointer indirection, cache misses, reference counting, tracing, and retained roots decide observed cost. A persistent vector may allocate a shallow trie frontier but retain pages through many snapshots. A confluent rope may represent enormous logical output in a tiny physical DAG until somebody flattens it.

Bad measurements are persuasive because they produce precise numbers. A single nanosecond result can measure clock overhead, constant folding, a hot cache, or an optimizer deleting the result. A shallow `sizeof` can exclude every child. RSS can remain high after objects die because the allocator retains arenas. A mean over one process's million inner iterations can suggest unjustified confidence because the process—not each correlated iteration—is the experimental unit.

Persistent-versus-mutable comparisons also invite semantic unfairness. Does the mutable baseline copy a snapshot so callers can retain old states? Are all versions kept or only the latest? Does one implementation validate keys, synchronize, hash, canonicalize, or persist to disk while the other does not? Do both support branching? A fast operation answering a weaker question is not an optimization of the same contract.

The objective is not one universal score. It is a chain of evidence: correctness first; deterministic mechanism counters; controlled microbenchmarks; memory accounting at declared layers; production-shaped macro/trace experiments; statistical uncertainty; sensitivity across environments; and a decision tied to service-level, cost, and operational constraints.

## Prerequisites and Retrieval

Retrieve asymptotic/worst-case/amortized/expected analysis, probability summaries, confidence intervals, graph reachability, memory hierarchy, allocators, garbage collection, compiler optimization, processes/threads, and experiment design. From [DSE-051](051-path-copying.md) and [DSE-052](052-structural-sharing.md), retrieve version roots, changed frontiers, distinct reachability, lifetimes, and aliases.

From [DSE-053](053-persistent-lists-and-queues.md), retrieve version-sensitive amortization. From [DSE-058](058-fat-nodes-and-partial-persistence.md), retrieve history skew and retention/rebase. From [DSE-059](059-full-and-confluent-persistence.md), retrieve version topology, logical-versus-physical size, path multiplicity, and materialization risk. You should be able to implement an independent semantic model and read basic distributions rather than treating one average as truth.

## Learning Objectives

After completing this module, you can:

1. translate a performance question into falsifiable hypotheses, metrics, units, workloads, and decisions;
2. validate semantic equivalence before comparing performance;
3. instrument persistent structures with deterministic operation/allocation/sharing counters;
4. design timing experiments resistant to setup leakage, optimizer removal, warmup, order, and process-level variation;
5. distinguish logical occurrences, distinct reachable nodes, allocation traffic, managed live/peak bytes, RSS, and native/mapped memory;
6. construct linear, branching, confluent, adversarial, and production-replay version traces with explicit retention;
7. choose experimental units, repetitions, estimators, intervals, randomization, and practical thresholds;
8. interpret cache, branch, allocator, GC, page-fault, and hardware-counter evidence without overclaiming causality;
9. specify reproducible benchmark artifacts, CI regression policy, security, and privacy controls; and
10. make a bounded engineering recommendation whose limitations remain visible.

## Core Exposition

**Start from a decision, not a stopwatch.** Write a question such as: “On ARM64 production hosts, does implementation P keep p99 lookup below 200 microseconds and retained physical memory below 2 GiB for the recorded 24-hour branching/retention trace, while matching implementation E's abstract map results?” This names platform, operations, tail, memory layer/retention, workload, baseline, and correctness.

State a null/comparison and practical threshold. A statistically detectable 0.3% speedup may not justify implementation risk; a noisy 20% p99 regression may violate a service objective. Decide thresholds before looking at results when possible. Record which outcome triggers adoption, more evidence, or rejection.

Claims have scopes. “Lookup performs at most `h` key comparisons” is algorithmic. “Median latency was 80 ns in this harness” is empirical and environment-specific. “Production p99 will remain below 200 microseconds” needs a production-representative system experiment, not merely a hot microbenchmark. Keep proof, mechanism counter, controlled measurement, and operational forecast separate.

**Correctness is the first gate.** Feed every candidate the same typed trace `(operation, base version(s), arguments, retention action)`. Compare returned values/errors, every sampled or all small version contents, and structural invariants with an independent simple model. A mutable baseline must emulate the same persistence contract—perhaps by copying snapshots—if the claim compares total contract cost.

Validate before and after measured runs, not necessarily inside the timed interval. Consume a digest/checksum or opaque result so the compiler/runtime cannot remove work, but compute expensive validation outside timing. For JIT/AOT compilers, inspect generated code or use a mature harness's blackhole/escape patterns. Vary inputs so constant folding/precomputation is unavailable.

Semantic dimensions include duplicate policy, key comparator/hash seed, error validation, thread safety, old-version query/update permissions, iteration order, stable identity, serialization, and durability. Publish exclusions. An immutable in-memory map and a transactional durable index are not comparable by a bare insertion loop.

**Instrument the mechanism first.** Add counters at stable abstraction boundaries: key comparisons, hash evaluations, parent/child reads, node visits, rotations/rebalances, nodes/bytes allocated, nodes copied, history lookups, modification-slot overflows, predecessor redirects, reroots, page writes, reference-count operations, and materialized elements.

Counters should be exact under a deterministic trace and removable/disabled for timing. Compare them with analytic predictions and invariant checks. If a height-`h` path-copy update allocates `h+1` nodes, a sudden `2h` reveals representation or rebalance work. Time alone cannot localize that.

Distinguish allocation traffic from live representation. A transient rebuilt path may allocate nodes later unreachable. Cumulative allocations affect allocator/GC bandwidth; distinct retained nodes determine logical representation liveness; allocator arenas may keep process RSS after reclamation. Record all applicable ledgers.

**Define persistent workloads as version traces.** An operation distribution without parent/root choices is incomplete. Include:

- linear latest-only history;
- full-persistent branching with specified base-version age/distribution;
- hot latest plus cold historical reads;
- breadth/depth/version-tree shape;
- confluent meld arity, overlap, and logical amplification;
- retained-all, sliding-window, milestones, random roots, readers/iterators, and delete/rebase policy;
- adversarial sorted/collision/hot-field/alternating-version patterns;
- production trace replay with privacy-preserving transformation and validation.

Report universe size, initial state, operation mix, key/value sizes/distributions, hit/miss ratios, update locality, branch factor, version age, retained-root count, logical size, and seed. A trace generator is part of the benchmark, versioned and tested.

Use multiple size regimes around cache/allocator/page/GC thresholds. Tiny workloads measure overhead; larger ones expose memory hierarchy and reclamation. Avoid choosing only the one size that favors a representation.

**Design timing intervals deliberately.** For Python, `time.perf_counter_ns()` provides an integer performance-counter reading; only differences are meaningful. A clock call has overhead/resolution. Batch enough operations that measured work dominates timing and divide only when the batch semantics justify it. Calibrate batch sizes without selecting flattering results.

Mature runtimes need mature harnesses. OpenJDK JMH handles generated benchmark code and offers patterns for warmup, forks, state scope, result consumption, and common JVM pitfalls; its documentation still warns that a harness does not replace benchmark reasoning or review. Comparable language-specific harnesses should be preferred over hand-written loops.

Warmup is a research choice. Steady-state experiments may run until a declared method judges compilation/cache/allocation behavior stable; fixed warmup alone does not prove steady state. Cold-start experiments intentionally include initialization. Tiered/JIT runtimes can change phase during measurement. Plot iteration order/time, compilation and GC logs where applicable, and report non-steady behavior instead of discarding it.

Separate setup/teardown. Prebuild inputs if construction is not the claim; include root selection and version lookup if callers pay them. Do not allocate keys for one candidate but reuse interned keys for another. If each update must create a version handle and publish metadata, time it for all candidates.

Randomize or counterbalance candidate order to reduce thermal, frequency, background-load, and cache-history confounding. Use fresh processes/forks for independent runtime state and repeat on independent machines/builds when the target population requires it. Pinning CPUs, disabling turbo, or isolating hosts can reduce variance but narrows external validity; record every control.

Measure latency distributions at the correct unit. Inner operations in a batch may not each be separately observable. Throughput under load needs arrival model, concurrency, queueing, backpressure, and coordinated-omission avoidance. Report p50/p90/p99/max with sample definition and intervals where defensible; tails require far more observations and process/run coverage than medians.

**Respect hierarchical variation.** Measurements can be nested: operations within iterations, iterations within processes, processes within builds, builds within machines. Values inside one process share runtime compilation, heap, ASLR, allocator, and environment; treating them as independent inflates apparent sample size.

Choose the experimental unit matching inference. For a claim about repeated service launches, fresh processes are units. For a claim about machines, sample machines. Within-unit repetitions estimate noise and can be summarized before across-unit inference. Kalibera and Jones provide a rigorous method for allocating repetition effort across levels and reporting uncertainty efficiently.

Retain raw observations and grouping identifiers. Report sample counts at every level, exclusions/timeouts and prespecified rules. Never delete “outliers” only because they hurt a result; diagnose environmental events, show sensitivity with/without a justified rule, and keep raw records.

Estimate differences or ratios paired by the randomized experimental unit when candidates share conditions. Report point estimate and interval plus distribution plots/raw data. Bootstrap procedures must resample at the independent unit/hierarchy, not individual correlated nanosecond observations. Parametric intervals require checked assumptions; robust summaries do not eliminate dependence.

Multiple operations, sizes, machines, and metrics create multiple comparisons. Identify primary endpoints; treat exploratory results as exploratory or adjust inference. Replicate surprising small effects. Statistical significance does not imply practical importance, causal mechanism, or generalization beyond tested configurations.

**Build a memory measurement stack.** No single function returns “true memory.” Define layers:

1. abstract logical elements/occurrences per version and across retained versions;
2. distinct physical nodes/arrays/pages reachable from the retention set;
3. representation bytes from known object layouts/allocator usable sizes;
4. cumulative allocation/deallocation traffic;
5. managed/runtime live and peak tracked memory;
6. allocator reserved/committed arenas and fragmentation;
7. process RSS/PSS/virtual mappings, native libraries, stacks, code/JIT, mmap, GPU/external buffers;
8. durable/storage bytes, write amplification, compression, and metadata.

Use identity-aware graph traversal for distinct nodes. Mark a node visited by stable physical identity, traverse every child/root, and avoid recursion overflow/cycles. Logical unfolding deliberately counts shared subtrees once per occurrence; do not reuse physical visited semantics. Report root handles/directories and version metadata too.

Shallow object-size APIs usually report the container/object header plus inline storage, not recursively owned referents. Recursively summing without identity dedup double-counts sharing and may count globally interned/runtime objects inconsistently. Define ownership: are keys/values shared with the workload, owned by the structure, or both candidates? Measure both inclusive and representation-only views if useful.

Python `tracemalloc` traces Python memory allocations after tracing begins and supports current/peak readings and snapshot comparison. It does not equal whole-process RSS; extensions/native/GPU/mmap layers may lie elsewhere. Tracing adds overhead and memory, so use it in separate profiling runs or quantify perturbation. Filter attribution carefully and record traceback depth/tool version.

RSS includes resident code, stacks, allocator arenas, shared/private pages, runtime and native memory. It may not fall when objects die because pages stay committed/reusable. PSS apportions shared pages where available. OS sampling has granularity/races. Measure baseline, construction, steady retention, post-release/quiescence, and peak with the same process lifecycle; repeat fresh processes.

For GC/refcount runtimes, record collector mode, heap limits, pauses, collection counts/time, promotion/tenuring, finalizers, weak references, and explicit collection policy. Do not force collections only for one candidate. If comparing application latency with production GC, include it; if isolating allocator cost, run a separate explicitly scoped experiment.

**Retention experiments are controlled reachability experiments.** At checkpoints record all roots and reader/iterator pins. Compute distinct nodes reachable from: latest only; all versions; policy window; milestones; representative branches; and post-release roots. The difference estimates reclaimable representation objects, subject to caches, interning, cycles, epochs, and collector quiescence.

Track cumulative allocated nodes and retained distinct nodes over time. A linear persistent history may allocate `m log n` total nodes yet retain fewer after dropping old roots. A full version tree can retain divergent paths. A fat-node structure keeps histories in-place. A confluent DAG can have huge logical/physical ratios. Memory per “version” without topology/retention is meaningless.

For branch sharing between root sets `A` and `B`, compute `|Reach(A)|`, `|Reach(B)|`, `|Reach(A) union Reach(B)|`, and intersection by identity. Shared nodes equal `|A|+|B|-|union|`. Generalize to many roots with per-node reach counts if attribution matters. Avoid charging one shared node fully to every tenant without explaining allocation policy.

**Use profiles to test mechanisms, not decorate reports.** CPU profiles identify hot instructions/functions but sampling has bias/resolution. Allocation profiles locate churn. Hardware counters can measure cycles, instructions, branches, cache/TLB misses, faults, migrations, and context switches on supported hardware. Linux `perf` documents multiplexing: too many events share limited counters and may introduce measurement error; group dependent events or reduce events.

Hardware event names/semantics vary by microarchitecture/kernel/virtualization and may be unavailable or permission-restricted. Counters are observations, not automatic causal proof. A cache-miss increase concurrent with latency suggests a hypothesis; controlled layout/trace changes and repeated evidence strengthen it.

Profiling tools can expose addresses, paths, process identities, registers, or data. Linux kernel documentation explicitly treats performance-event access as a security concern. Benchmark data/traces may contain customer keys/values and provenance. Use isolated authorized hosts, least privilege, redaction/synthetic traces, access control, retention, and secure artifact publication.

**Reproducibility is a deliverable.** Record repository commit/dirty state, compiler/runtime/harness versions and flags, dependencies/lockfiles, OS/kernel, CPU model/microcode/topology, memory/NUMA, power/frequency/governor, container/VM, limits, GC/allocator/env variables, command, seed/trace hash, timestamps, instrumentation, and failures. Machine-readable metadata should accompany human interpretation.

Store raw observations before aggregation, schema/version them, validate units and missing values, and make analysis deterministic. Generated logs/reports belong under the repository's governed artifacts location. A chart should be regenerable by one documented command and identify the exact input digest.

Regression gates need calibrated noise. Use stable dedicated runners or broad thresholds, compare to a rolling/baseline distribution, require repeated confirmation, and distinguish correctness failure from performance alert. Never make an unstable nanobenchmark a mandatory gate merely because it once produced a precise number.

**Make bounded conclusions.** A useful conclusion states: tested commits/configurations; trace and retention; correctness result; time/memory estimators/intervals; structural/profile evidence; practical threshold; decision; and untested cases. Do not write “persistent structures are slower” from one Python tuple example or “sharing saves 43%” without ownership/retention/error scope.

## Definitions and Notation

- `T`: typed sequence/DAG of operations, base versions, arguments, and retention actions.
- `R_t`: set of retained/pinned version roots after trace event `t`.
- `Reach(R_t)`: set of distinct physical representation nodes reachable from those roots.
- `L(v)`: logical element/occurrence count in version `v`.
- `O(R)=sum_(v in R) L(v)`: logical occurrences across retained roots; sharing is counted per version.
- `P(R)=|Reach(R)|`: distinct physical node count for a retention set.
- `A_t`: cumulative nodes or bytes allocated through event `t`.
- `D_t`: cumulative deallocation/reclamation traffic through event `t`.
- `B_live(t)`: bytes considered live by a declared runtime/ownership layer at time `t`.
- `B_peak`: maximum observed `B_live` within a declared interval/tool.
- `RSS(t)`: process resident set measured by an OS interface at time `t`.
- `X_(i,j,k)`: observation at nested levels such as machine `i`, process `j`, iteration `k`.
- `theta`: target effect, such as paired median/mean latency difference or ratio under a defined population.
- `delta`: practical threshold chosen for an engineering decision.
- **blackhole/result consumption**: mechanism making benchmark results observable so work cannot be removed.
- **counterbalancing**: varying candidate order systematically to reduce order confounding.
- **quiescence**: declared point when pending reclamation/collection relevant to the experiment has completed or stabilized.

Logical sharing factor can be reported as `O(R)/P(R)` when `P(R)>0`, but it is not byte savings: node sizes, roots, metadata, values, and allocator overhead vary. Allocation amplification can be `A_delta / logical_updates`; state whether numerator is nodes, requested bytes, usable bytes, or persisted bytes.

## Mechanisms, Invariants, or Proof Structure

**Experiment protocol.** Freeze question/hypotheses/thresholds. Pin code/configuration. Generate/validate trace. Run semantic oracle/invariants. Calibrate without using final results to cherry-pick. Randomize scheduled independent units. Execute warmup/measurement/validation under resource limits. Persist raw data/metadata. Analyze using the declared hierarchy. Reproduce/sensitivity-check. Publish bounded conclusion.

**Semantic invariant.** For every event and retained version, candidate abstract values/errors equal the reference model under the same contract. A performance result is invalid if semantic equivalence fails, even if latest-state checks pass.

**Structural accounting invariant.** Every allocated physical node has a unique measurement identity; reach traversal counts it at most once per retention set. Every semantic child/reference is traversed. Root/version metadata are counted separately or explicitly excluded. Logical traversal counts occurrences and rejects cycles/amplification beyond limits.

**BST allocation derivation.** In immutable unbalanced BST insertion of a new absent key at search depth `d` edges, allocate one leaf plus one copied node per ancestor: `d+1`. Existing subtrees outside the path are reused. Under retained roots, every allocated node remains reachable from its creation version unless that root is dropped and no other retained root reaches it.

**Two-root intersection.** Let distinct reachable sets be `A` and `B`. Inclusion-exclusion gives `|A intersect B|=|A|+|B|-|A union B|`. This exact physical-node sharing count does not depend on runtime byte sizes.

**Timing invariant.** Measured interval contains the same scoped work for candidates; input/results remain observable; elapsed duration uses differences from a documented clock/harness; setup/warmup/teardown policy is symmetric; units/batches are correct; failures/timeouts are retained.

**Inference invariant.** Randomization and resampling/aggregation operate at the declared independent experimental unit. Nested observations retain group IDs. Estimand, estimator, interval method, primary metrics, exclusions, and sample counts are reported. Conclusions do not exceed sampled environments/workloads.

**Memory invariant.** Each number names its layer/tool/interval/ownership. Traced managed bytes are not relabeled RSS; shallow size is not recursive footprint; allocated is not live; live is not resident; current is not peak; latest-root reach is not all-version retention.

**Profiling invariant.** Instrumented and uninstrumented runs are distinct; overhead is estimated; events/tool permissions/multiplexing/unsupported status are recorded. A profile proposes/locates mechanisms but does not replace controlled comparison.

**Artifact invariant.** Raw data are immutable or digest-bound; analysis output identifies input digest and code/configuration; commands/tools/environment permit reconstruction; sensitive data are excluded or governed; generated artifacts do not masquerade as handwritten source.

## Alternatives and Trade-Offs

| Method | Best evidence | Principal limitation |
|---|---|---|
| Analytic complexity/proof | asymptotic/worst-case mechanism | hides constants/runtime/workload |
| Deterministic counters | exact comparisons/copies/reachability | not elapsed bytes/time |
| Microbenchmark | isolated operation cost | optimizer/cache realism and noise |
| Trace benchmark | production-shaped sequences | trace drift/privacy/portability |
| Macro/end-to-end test | user-visible effect | weak attribution, expensive |
| Managed heap tracer | allocation sites/live/peak layer | instrumentation and native gaps |
| Identity graph census | sharing/retained distinct nodes | ownership/layout bytes separate |
| RSS/PSS sampling | process/OS residency | allocator/code/shared-page ambiguity |
| CPU/allocation profile | hot mechanisms/churn | perturbation and causality limits |
| Hardware counters | microarchitectural symptoms | availability/event/multiplexing variance |

Use a ladder, not one winner. Proof predicts scaling; exact counters validate implementation shape; microbenchmarks estimate isolated constants; traces test version/retention distributions; macro tests test service outcomes; profiles explain observed changes.

In-process alternation pairs candidates tightly but risks cross-candidate cache/JIT/allocator pollution. Separate processes isolate state but add launch/environment variation. Run both when the distinction matters. A/B production experiments offer realism but require user safety, capacity, privacy, and causal design.

Pre-generated traces remove generator cost and ensure equality, but large traces affect cache/storage and may constrain randomness. On-the-fly generation can be included if production pays it, otherwise separate it and verify identical seeds/events.

Fixed iteration counts simplify comparison; fixed time collects different operation counts and can complicate allocation/thermal state. Adaptive harnesses save time but stopping rules must be documented and must not bias candidate selection.

Retain-all reveals worst historical growth; sliding windows test product policy; latest-only measures a different, weaker memory contract. Report all relevant policies rather than choosing the smallest footprint.

## Failure Modes and Misconceptions

- **“Nanoseconds are accuracy.”** Resolution, overhead, batching, optimization, and process variance still govern evidence.
- **“More loop iterations mean independent samples.”** Correlated iterations in one runtime are usually one lower-level cluster.
- **“Warmup count proves steady state.”** Inspect phase behavior and define the target; some runs never stabilize.
- **“Median removes all noise.”** It does not fix dependence, confounding, biased sampling, or wrong semantics.
- **“A non-overlapping interval proves practical superiority.”** Compare effect with the decision threshold and scope.
- **“No significant difference means equivalence.”** Equivalence/noninferiority requires a margin and suitable design/power.
- **“`sizeof(root)` is the tree footprint.”** It is generally shallow and excludes/reuses referents.
- **“Recursive sum is correct.”** Without identity/ownership it double-counts sharing and external objects.
- **“Traced peak equals RSS.”** Managed tracing and process residency observe different layers.
- **“RSS should fall after GC.”** Allocators/OS may retain reusable pages; measure live objects and RSS separately.
- **“Allocated nodes equal retained nodes.”** Dropped versions/transients can become unreachable; retained roots can keep old nodes.
- **“All versions cost versions times latest size.”** Sharing reduces physical nodes, but metadata/history can add other costs.
- **“Latest-only memory represents persistence.”** It omits the retention contract that creates the feature.
- **“A profile proves cause.”** It identifies correlations/hot locations; controlled changes test causal hypotheses.
- **“Hardware counters are portable facts.”** Event definitions, availability, virtualization, and multiplexing vary.
- **“A harness makes the benchmark valid.”** It mitigates mechanics; question, semantics, design, statistics, and review remain yours.
- **“A green CI benchmark proves no regression.”** Runner noise and threshold calibration determine signal quality.

## Worked Examples

### Example 1

**Situation.** An engineer times one insertion with `perf_counter_ns()` and reports 240 ns.

**Reasoning.** One difference includes two clock calls, interpreter/runtime state, cache state, branch path, allocation state, possible interruption, and resolution. Measure clock/batch overhead, consume results, predefine a distribution of keys/versions, batch enough operations, repeat randomized fresh processes, and retain raw values. The defensible result is a distribution/estimate for that declared workload—not “insertion takes 240 ns.”

**Conclusion.** A precise integer from one timing interval is an observation, not an estimate of a useful population.

### Example 2

**Situation.** Candidate P supports persistent roots; baseline M mutates one map. The benchmark retains 10,000 P versions but only M's latest state.

**Reasoning.** This compares different contracts. If the decision needs history, M must produce equivalent snapshots/log/replay and include their time/memory. If the question isolates latest-operation overhead, drop old P roots and explicitly label the weaker workload. Both experiments may be useful but answer different questions.

**Conclusion.** Semantic and retention equivalence precede performance comparison.

### Example 3

**Situation.** A shallow size call reports 56 bytes for both a one-node and million-node tree root.

**Reasoning.** The root object header/inline fields can be the same while referent graphs differ. Traverse semantic child pointers, deduplicate by physical identity, decide key/value ownership, add version/root metadata, and map nodes to runtime/allocator bytes. Separately measure traced managed live/peak and RSS.

**Conclusion.** Shallow size describes one object, not the transitive persistent representation.

### Example 4

**Situation.** Ten retained roots each contain 1,000 logical nodes, and identity traversal finds 1,900 distinct physical nodes.

**Reasoning.** Logical occurrences are 10,000; physical nodes 1,900; sharing factor is about `10,000/1,900=5.26`. This does not mean 81% byte savings because roots, version metadata, values, node sizes, fragmentation, and allocator/runtime memory remain. Measure those layers.

**Conclusion.** Logical/physical counts expose sharing but do not replace byte accounting.

### Example 5

**Situation.** Candidate A is always measured before B on a laptop.

**Reasoning.** Order is confounded with cache warming, JIT state, allocator reuse, background load, thermal rise, and frequency throttling. Randomize/counterbalance per independent process, record environment/temperatures/frequency where relevant, and use paired analysis by process/order block. Separate-process experiments avoid cross-candidate state but still randomize launch order.

**Conclusion.** Fixed order can manufacture an apparent candidate effect.

### Example 6

**Situation.** Reproduce deterministic allocation and sharing counters for path-copying BST versions.

**Reasoning.** The executable retains every main root, branches from the six-key root, validates every abstract key set/BST, and computes reachability by object identity. No wall-clock or object-byte result is asserted, so exact output remains stable across machines.

<!-- bijux-verify: {"id":"persistent-bst-structural-metrics","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"main_allocations=1,2,2,3,3,3,3\nbranch_allocations=3\nall_versions_logical_occurrences=35\nall_versions_distinct_nodes=20\nlatest_and_branch_logical_occurrences=14\nlatest_and_branch_distinct_nodes=10\nlatest_and_branch_shared_nodes=4\nlatest_height=3\nbranch_height=3\nlookup_steps_latest_7=3\nlookup_steps_branch_8=3\nbranch_excludes_7=True\nold_versions_unchanged=True\nall_invariants=True\nevidence=finite_persistent_bst_structural_metrics\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    key: int
    left: "Node | None" = None
    right: "Node | None" = None


class Allocator:
    def __init__(self) -> None:
        self.total = 0

    def node(self, key: int, left: Node | None, right: Node | None) -> Node:
        self.total += 1
        return Node(key, left, right)


def insert(root: Node | None, key: int, allocator: Allocator) -> Node:
    if root is None:
        return allocator.node(key, None, None)
    if key < root.key:
        return allocator.node(root.key, insert(root.left, key, allocator), root.right)
    if key > root.key:
        return allocator.node(root.key, root.left, insert(root.right, key, allocator))
    return root


def keys(root: Node | None) -> tuple[int, ...]:
    if root is None:
        return ()
    return keys(root.left) + (root.key,) + keys(root.right)


def height(root: Node | None) -> int:
    return 0 if root is None else 1 + max(height(root.left), height(root.right))


def lookup_steps(root: Node | None, key: int) -> tuple[bool, int]:
    steps = 0
    while root is not None:
        steps += 1
        if key == root.key:
            return True, steps
        root = root.left if key < root.key else root.right
    return False, steps


def identities(roots: list[Node | None]) -> set[int]:
    seen: set[int] = set()
    stack = [root for root in roots if root is not None]
    while stack:
        node = stack.pop()
        identity = id(node)
        if identity in seen:
            continue
        seen.add(identity)
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)
    return seen


allocator = Allocator()
versions: list[Node | None] = [None]
main_allocations: list[int] = []
expected: list[tuple[int, ...]] = [()]
for key in (4, 2, 6, 1, 3, 5, 7):
    before = allocator.total
    versions.append(insert(versions[-1], key, allocator))
    main_allocations.append(allocator.total - before)
    expected.append(tuple(sorted((*expected[-1], key))))

before_branch = allocator.total
branch = insert(versions[6], 8, allocator)
branch_allocations = allocator.total - before_branch
all_roots = versions[1:] + [branch]
all_occurrences = sum(len(keys(root)) for root in all_roots)
latest = versions[-1]
two_roots = [latest, branch]
latest_ids = identities([latest])
branch_ids = identities([branch])
two_ids = identities(two_roots)
latest_found, latest_steps = lookup_steps(latest, 7)
branch_found, branch_steps = lookup_steps(branch, 8)
branch_has_7, _ = lookup_steps(branch, 7)
old_unchanged = all(keys(root) == value for root, value in zip(versions, expected))
valid = (
    old_unchanged
    and keys(branch) == (1, 2, 3, 4, 5, 6, 8)
    and all(tuple(sorted(keys(root))) == keys(root) for root in all_roots)
    and latest_found
    and branch_found
    and not branch_has_7
)

print("main_allocations=" + ",".join(map(str, main_allocations)))
print(f"branch_allocations={branch_allocations}")
print(f"all_versions_logical_occurrences={all_occurrences}")
print(f"all_versions_distinct_nodes={len(identities(all_roots))}")
print(f"latest_and_branch_logical_occurrences={sum(len(keys(r)) for r in two_roots)}")
print(f"latest_and_branch_distinct_nodes={len(two_ids)}")
print(f"latest_and_branch_shared_nodes={len(latest_ids & branch_ids)}")
print(f"latest_height={height(latest)}")
print(f"branch_height={height(branch)}")
print(f"lookup_steps_latest_7={latest_steps}")
print(f"lookup_steps_branch_8={branch_steps}")
print(f"branch_excludes_7={not branch_has_7}")
print(f"old_versions_unchanged={old_unchanged}")
print(f"all_invariants={valid and allocator.total == 20}")
print("evidence=finite_persistent_bst_structural_metrics")
```

The identity values themselves are never printed; only set cardinalities are. The trace proves finite Python object sharing/allocation counts under this implementation, not byte footprint, allocator behavior, elapsed performance, balance, GC, concurrency, or production fitness.

**Conclusion.** Exact mechanism/reachability evidence can be deterministic while timing/memory-layer measurements remain separate experiments.

### Example 7

**Situation.** `tracemalloc` current drops after roots are deleted and collection runs, but RSS stays flat.

**Reasoning.** The traced Python allocation layer released objects, while the allocator may retain arenas/pages for reuse and the OS may keep them resident. Native/runtime components may also dominate RSS. Record traced current/peak/snapshots, allocator stats if available, RSS/PSS, and subsequent reuse/fresh-process behavior. Do not label either tool wrong.

**Conclusion.** Different memory layers can move differently without contradiction.

### Example 8

**Situation.** `perf stat` reports cache misses for one candidate while too many events are requested.

**Reasoning.** Limited hardware counters can multiplex events; workload phases then receive unequal observation time and derived ratios may be distorted. Inspect supported event definitions and scaling, reduce events, group jointly required counts where supported, repeat, and record CPU/kernel/perf/virtualization/permissions. Use the result to test a cache hypothesis, not declare universal causality.

**Conclusion.** Hardware counters require event/model and multiplexing validation.

### Example 9

**Situation.** A 2% median improvement has a narrow interval, but adoption needs at least 10% to offset maintenance risk.

**Reasoning.** The experiment may provide strong evidence for a small effect yet fail the practical decision threshold. Report both: statistically resolved improvement around 2%, below prespecified 10%; retain current design unless other metrics justify adoption. Do not inflate “significant” into “important.”

**Conclusion.** Uncertainty and practical magnitude answer different questions.

### Example 10

**Situation.** A CI runner flags a 4% regression intermittently.

**Reasoning.** Inspect dedicated-versus-shared host variation, candidate order, process sample size, thermal/frequency changes, build/runtime drift, trace digest, and correctness. Calibrate baseline distribution and threshold from historical independent runs, rerun confirmation, and make alerts distinct from correctness gates. Preserve failed/noisy results rather than automatically retrying until green.

**Conclusion.** Performance gates are measurement systems that need their own reliability evidence.

## Cross-Program Connections

- **Statistics and Probability:** hierarchical sampling, uncertainty, estimands, multiple comparisons, and equivalence margins determine valid inference.
- **Systems Performance:** caches, TLBs, NUMA, page faults, allocators, GC, CPU frequency, queueing, and observability shape measured costs.
- **Software Engineering:** benchmark code/review, fixtures, reproducible environments, raw artifacts, and regression governance are production assets.
- **Database Engineering:** MVCC/index snapshots require retention/vacuum/write-amplification and transaction-equivalent workload accounting.
- **Data Engineering:** trace capture/replay, schema/digest provenance, aggregation correctness, and privacy govern benchmark datasets.
- **Concurrent Programming:** schedules, contention, throughput/latency, linearizability checking, pinning, and reclamation require specialized experiments.
- **Security Engineering:** profiling privileges/data, hostile amplification traces, cross-tenant sharing attribution, and artifact access are security concerns.
- **Formal Methods:** refinement and exact counters connect abstract complexity claims to implementation events before empirical measurement.

## References

1. Python Software Foundation, [Python `time` documentation](https://docs.python.org/3/library/time.html), accessed 2026-08-30. Official clock semantics including `perf_counter_ns()`.
2. Python Software Foundation, [Python `tracemalloc` documentation](https://docs.python.org/3/library/tracemalloc.html), accessed 2026-08-30. Official traced-memory, peak, snapshot, and filtering interfaces.
3. OpenJDK, [Java Microbenchmark Harness](https://github.com/openjdk/jmh), official project and samples. Harness scope, setup, and benchmark-review guidance.
4. Tomas Kalibera and Richard E. Jones, [“Rigorous Benchmarking in Reasonable Time”](https://kar.kent.ac.uk/33611/45/p63-kaliber.pdf), ISMM 2013. Primary methodology for hierarchical variation, repetition, and uncertainty.
5. Google, [Benchmark user guide](https://google.github.io/benchmark/user_guide.html), official documentation for a mature native-code microbenchmark harness.
6. Linux kernel project, [`perf-list` documentation](https://github.com/torvalds/linux/blob/master/tools/perf/Documentation/perf-list.txt), official source-tree documentation including event grouping and multiplexing caveats.
7. Linux kernel project, [Perf events and tool security](https://www.kernel.org/doc/html/latest/admin-guide/perf-security.html), official security guidance for performance monitoring.
8. NIST/SEMATECH, [e-Handbook of Statistical Methods: Confidence Limits for the Mean](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm), official statistical reference for estimator uncertainty under stated assumptions.

## Exercises

### Exercise 1

For three retained versions with logical sizes 5, 7, and 8 and distinct reachable sets of sizes 5, 7, and 8, suppose their union has 12 physical nodes. Compute logical occurrences, distinct physical nodes, sharing factor, and explain what byte/RSS conclusions are not justified.

### Exercise 2

Design a timing experiment comparing persistent and mutable maps for a latest-only lookup question. Specify semantic oracle, trace, measured interval, result consumption, warmup/cold policy, independent unit, randomization, repetitions, estimator/interval, practical threshold, and recorded environment.

### Exercise 3

A benchmark reports Python `tracemalloc` peak 400 MiB, post-GC current 80 MiB, and RSS 900 MiB. Diagnose at least six possible contributors/gaps and propose focused follow-up measurements without claiming a leak from these three numbers alone.

### Exercise 4

Design memory experiments for an immutable tree under retain-all, sliding-window-100, milestone-every-1,000, and latest-only policies across a branching update trace. Define exact counters, byte layers, quiescence, attribution, and evidence needed to compare policies fairly.

### Exercise 5

Prepare a production-grade benchmark plan for a confluently persistent multi-tenant rope service with self-composition, slicing, streaming, deletion, concurrency, and hostile inputs. Include correctness, workloads, time/memory metrics, statistics, profiling, security/privacy, reproducibility, regression policy, and decision criteria.

## Answers to the Exercises

### Answer 1

Logical occurrences are `5+7+8=20`. The declared union contains 12 distinct physical nodes, so physical node count is 12 and the logical-occurrence/physical-node sharing factor is `20/12=5/3≈1.67`. Per-root set sizes alone do not reveal pairwise/triple intersections uniquely, but the union is enough for total distinct count.

This does not prove a 40% byte reduction or any RSS value. Nodes may have different sizes; roots/version directories, keys/values, cached metadata, allocator headers/rounding/fragmentation, runtime/GC tables, stacks/code/native buffers, and resident-page policy are omitted. Define ownership and measure representation bytes, managed live/peak, allocation traffic, allocator arenas, and RSS/PSS separately.

### Answer 2

Define both candidates as maps with identical comparator/hash seed, duplicate/error semantics, key/value ownership, and thread-safety scope. Because the question is latest-only lookup, build semantically equal latest maps and drop historical roots before measurement; label this as not measuring retention. Generate a fixed/versioned trace of hit/miss queries across sizes/distributions with seeds and validate every answer against a simple dictionary/reference plus pre/post digests.

Exclude construction if the question is lookup but include version/root lookup if callers pay it. Consume each returned value/digest through the language harness so work cannot disappear. Use a mature harness; define separate cold-start and steady-state experiments rather than mixing them. For steady state, record iteration/compilation/GC behavior and a declared warmup assessment.

Use a fresh process/fork as the main independent unit, randomize/counterbalance candidate order and trace blocks, take sufficient within-process batches for clock dominance, and sample enough independent processes based on pilot variance without treating operations as independent. Pair candidate summaries within process/order block; report the prespecified effect (for example median or mean throughput/latency ratio) with an interval resampled/analyzed at process level, raw distributions, all failures, and counts.

Choose a practical threshold such as at least 8% latency reduction with no correctness/memory regression before viewing final data. Record commit/dirty state, compiler/runtime/harness/dependencies/flags, OS/kernel, CPU/microcode/topology, memory/NUMA, governor/frequency/container, allocator/GC/env, commands, trace hash/seeds, timestamps, and raw artifact digest. Replicate on the deployment hardware population before generalizing.

### Answer 3

Possible explanations include: (1) `tracemalloc` began after preexisting allocations; (2) native extension/runtime allocations are not in its traced domain; (3) allocator arenas retain freed blocks/pages; (4) code/JIT/shared libraries/stacks contribute RSS; (5) memory maps/file cache or external buffers contribute; (6) fragmentation prevents page return; (7) RSS sampling and traced peak cover different intervals; (8) live objects outside the intended structure remain referenced; (9) cyclic/finalizer/reader pins delay reclamation; (10) tracing itself perturbs memory. The 80 MiB traced current suggests decline in that observed layer, while 900 MiB RSS describes residency; neither alone proves or disproves a leak.

Repeat fresh isolated processes with baseline/build/post-drop/post-quiescence timestamps and identical lifecycle. Take filtered `tracemalloc` snapshot differences with declared start/depth; inspect object/reachability/root pins; collect allocator/runtime/GC statistics; measure RSS and PSS/maps over time; profile native allocations where authorized; test whether subsequent allocations reuse retained RSS; compare a no-work control and uninstrumented run; repeat across processes and increasing trace sizes. A leak claim needs monotone retained growth attributable to unintended reachability/allocation under repeated steady workload.

### Answer 4

Use one validated branching trace whose events specify base version, operation, arguments, and retention action. At every checkpoint record abstract contents/sizes, allocated/copied nodes/bytes, changed depth, version metadata, and identity-deduplicated `Reach(R)` for exactly each policy: all roots; latest 100 by declared version/topology rule; every 1,000th milestone plus any latest/root policy; latest only. Readers/iterators/exports are explicit pins shared across compared implementations.

Measure cumulative allocation/deallocation, distinct representation nodes/known layout or allocator usable bytes, managed current/peak and allocation profiles in separate instrumented runs, allocator reserved/fragmentation, and fresh-process RSS/PSS at common lifecycle points. Include keys/values/roots consistently. After policy drops roots, wait for declared epoch/refcount/GC quiescence with the same collector settings; do not force collection asymmetrically. Report unreclaimed-but-reusable allocator pages separately.

Validate every retained version against the oracle and check dropped handles fail according to policy. Repeat independent processes, randomize candidate order, retain raw time series and environment. Report per-policy live curves, peak, allocation traffic, reclamation lag, metadata, sharing/intersection, and uncertainty—not merely final bytes/version. Retain-all is a stronger contract; latest-only results cannot be presented as its optimization.

### Answer 5

Specify an immutable abstract rope with ordered concatenation, slicing, streaming range, exact/limited length, version handles, tenant/schema compatibility, retention/deletion, and atomic multi-parent publication. Compare implementation answers and all small/generated versions with a simple bounded string/reference DAG; validate node/version acyclicity, cached measures, operand preservation, authorization, and failure noninterference. Never validate large logical outputs by unbounded flattening.

Workloads include latest/old reads, branch depth/breadth, distinct and overlapping/self operands normalized by the API, slice/range distributions, streaming cancellation/backpressure, logical/physical ratios, retained windows/milestones/readers, deletion/reclamation, concurrency/arrival/load, production-derived redacted traces, and adversarial deep/path-amplifying/cyclic/oversized/cross-tenant inputs. Sweep physical/logical size, overlap, arity, output limit, concurrency, and retention.

Exact counters cover version/data nodes/edges, path/effective-depth bounds, cached length operations, node visits, allocations, shared reachability, materialized/streamed bytes, pins, and reclaimed objects. Time metrics cover publish, character/slice, first-byte and stream throughput/tails, cancellation, GC/reclamation, and recovery. Memory layers cover logical occurrences, distinct nodes, metadata, allocation traffic, managed live/peak, allocator/RSS/PSS, buffers, and durable bytes/write amplification.

Use independent process/host/load-run units, randomized implementations/configurations, prespecified primary endpoints and practical SLO/cost margins, raw grouped observations, suitable estimates/intervals, tail sample planning, multiple-comparison discipline, and replication on deployment hosts. Profile CPU/allocation/GC/hardware counters in separate authorized runs, validate multiplexing, and test causal layout/algorithm hypotheses.

Security includes tenant-compatible authorization/result labels, input and output/CPU/memory/depth/path/arity/pin quotas, streaming backpressure, parser quarantine, provenance authentication, profiler privilege/data protection, trace redaction/access/retention, and deletion audits. Artifacts record commits/configuration/toolchains/hardware/OS/runtime/commands/seeds/trace digests/raw data/analysis digest/failures. CI uses stable runners, correctness hard gates, calibrated performance alerts with confirmation, and no retry-until-green bias.

Adopt only if correctness/security gates pass and prespecified production-shaped p99/throughput, memory/cost, recovery, and deletion thresholds beat the baseline by the practical margin across required hosts; otherwise reject or gather named missing evidence. Explicitly exclude untested operand growth, runtimes, hardware, failure modes, and external review from the conclusion.
