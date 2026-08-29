---
module_id: CONPAR-065
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 65
title: Deterministic Parallel Execution
status: complete
last_verified: 2026-08-29
---

# Deterministic Parallel Execution

## One-Page Review

### Governing question

How can a parallel program guarantee the same specified observable result for the same declared inputs even when task placement, execution speed, and physical completion order vary?

### Essential definitions

- **Determinism** means a declared observation is a mathematical function of declared inputs and configuration; it must name both domains.
- **output determinism** requires the same externally observed values, while **state determinism** also constrains a specified internal final state.
- **schedule determinism** constrains synchronization/interleaving decisions; it is stronger than needed for many deterministic results.
- **deterministic by construction** means the programming model excludes or orders interfering effects rather than hoping schedules coincide.
- **noninterference** means parallel tasks' effects are disjoint or commute under the specified observation.
- A **logical order** is a stable order derived from input identity, graph structure, epochs, or sequence numbers rather than wall-clock completion.
- A **deterministic reduction** has a fixed grouping/order or an operation whose relevant result is associative and commutative in the actual value model.
- **logical time** advances by program events, not elapsed physical time.
- **deterministic commit** allows speculative work to finish arbitrarily but publishes effects in a stable validated order.
- **replay** records one execution for later reproduction; deterministic execution constrains every execution without requiring that prior log.

### Central model, mechanism, or theorem

Define an observation function `O`, declared input `I`, and configuration `C`. The program is deterministic for that contract when every permitted parallel execution e yields `O(e)=F(I,C)`. Establish this by composing deterministic tasks through immutable inputs, single assignment, disjoint regions, commutative effects with deterministic identities, stable reductions, deterministic dataflow, or logical serialization of conflicts. Physical schedules may differ; only decisions capable of changing O must be eliminated, isolated, or ordered.

### Critical invariants

Inputs include every source allowed to affect observations: files, environment, configuration, random seeds, clocks, locale, dependency/toolchain semantics, and external responses. Parallel effects are disjoint, proven commutative, or committed in stable order. Collection traversal and tie-breaking are stable. Floating-point grouping is specified when bitwise results matter. Exceptions, cancellation, timeouts, resource limits, and overflow select deterministic outcomes. Side effects are buffered and ordered. Logical IDs do not depend on addresses or completion timing. Determinism scope is tested across schedules and platforms actually claimed.

### Common failures

Programs call race freedom determinism; reduce floating-point values in arrival order; iterate hash tables with unspecified order; let “first completed wins”; draw from one shared random stream scheduled by timing; use wall clock in computation; expose pointer addresses; select whichever exception arrives first; append logs from workers directly; depend on filesystem enumeration; confuse a replay log with deterministic semantics; or guarantee identical output while ignoring nondeterministic resource failure and external effects.

### Compact example

Tasks compute operations for logical positions 0, 1, and 2 but physically finish 2, 0, 1. The coordinator buffers proposals and commits in logical order: add 3, multiply by 2, subtract 1, producing 7 from initial 1 every time. Applying completion order would produce 6. Stable commit restores determinism but serializes this order-sensitive effect; the computations can remain parallel.

### Connections

[Conflict Detection and Contention](064-conflict-detection-and-contention.md) identifies incompatible speculative effects. [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md) supplies reduction structure. The next module develops deterministic schedulers for testing; later modules develop reproducible randomness and replayable concurrency.

## Governing Question

What exactly must remain invariant across permitted parallel executions, and which language, algorithm, runtime, and system mechanisms are sufficient to establish that invariant without unnecessarily serializing all work?

“It usually prints the same answer” is an observation. Determinism is a quantified contract over inputs, executions, and observations.

## Why This Matters

Nondeterministic parallel programs can be correct: a server may accept requests in any order while preserving its API. But uncontrolled nondeterminism makes failures difficult to reproduce, golden results unstable, caches and build artifacts untrustworthy, scientific comparisons noisy, and incident evidence ambiguous. It can also turn one tested execution into weak evidence for deployed executions.

Serial execution is deterministic under many models but forfeits parallelism. The engineering goal is to retain independent computation while controlling only communication and observation that can change semantics. Functional dataflow, regions/effects, immutable snapshots, indexed output, deterministic reductions, epochs, and ordered speculative commit offer different points in that design space.

Determinism is not universal correctness. A deterministic program can always produce the wrong answer, deadlock at the same point, expose secrets consistently, or deterministically choose an unsafe action. Conversely, varying internal schedules can be harmless when the observable result is fixed. The contract must name what matters.

## Prerequisites and Retrieval

Retrieve:

- task graphs from [Task Parallelism and Dependency Graphs](041-task-parallelism-and-dependency-graphs.md);
- reductions and their numerical ordering from [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md);
- optimistic validation from [Optimistic Concurrency and Validation](062-optimistic-concurrency-and-validation.md); and
- transactional conflict order from [Conflict Detection and Contention](064-conflict-detection-and-contention.md).

Retrieval prompt: list five scheduling decisions in a parallel map/reduce implementation, then classify which can change the declared result and which may vary without observable effect.

## Learning Objectives

After completing this module, a learner can:

1. specify input, configuration, execution, and observation domains for a determinism claim;
2. distinguish output, state, schedule, timing, and replay determinism;
3. prove deterministic composition from pure tasks and noninterfering effects;
4. design stable logical identities, tie-breaking, reductions, and exception aggregation;
5. use dataflow, isolated regions, deterministic consistency, or ordered speculative commit;
6. control randomness, time, external I/O, collection order, and floating-point variability;
7. reason about cancellation, resource failure, adaptive behavior, and lifecycle;
8. choose where intentional nondeterminism belongs in an API;
9. construct schedule-diverse verification and cross-platform evidence; and
10. apply higher assurance to safety-critical deterministic decisions.

## Core Exposition

### Specify the claim before the mechanism

Let `E(I,C)` be all executions permitted for declared input I and configuration C. Let O project an execution to observations: returned value, bytes written, exception, final database state, event order, or another explicit surface. Determinism means there exists F such that for every `e ∈ E(I,C)`, `O(e)=F(I,C)`.

This definition forces scope. If thread count belongs to C, results may differ across thread counts while remaining deterministic within each. If the requirement is reproducibility across thread counts, exclude it from result-affecting C. If only a set of output records matters, their byte order may vary; if consumers hash the file, byte order matters.

Timing is normally excluded because physical load varies. A real-time contract instead specifies bounds or trace equivalence under a timing model, not identical nanoseconds. Internal schedule determinism may be useful for debugging, but it is stronger and often costlier than output determinism.

### Sources of nondeterminism

Thread scheduling changes read/write races, atomic winner choices, completion order, lock acquisition, callback order, exception arrival, and allocation addresses. Runtime behavior can change hash iteration, work stealing, GC timing, signal delivery, and fallback. Hardware changes floating-point instructions, vector width, memory failures, and timing.

External inputs include time, entropy, files and directory order, environment variables, locale/time zone, process IDs, network replies, database snapshots, dependency data, and operator actions. A program cannot claim same-input determinism while leaving these unnamed. Capture, normalize, seed, version, snapshot, or explicitly exclude them from scope.

Resource availability is particularly subtle. One run may allocate successfully and another fail. If failure is observable, resource budgets/platform belong to C or the implementation needs deterministic admission/preallocation. Timeouts convert variable duration into semantic variation unless logical deadlines or a scoped timing model define them.

### Pure task graphs

A pure task computes a value only from explicit immutable inputs. For a DAG of deterministic tasks, each node's value is a deterministic function of predecessor values. Induction over a topological order proves every node and output deterministic, even if the runtime chooses any ready task physically.

Futures/single-assignment variables embody this rule: multiple consumers may await one value, but no racing writer chooses it. Kahn process networks obtain determinate results under conditions including deterministic sequential processes and unbounded FIFO channels; bounded implementations require new progress and scheduling analysis.

Purity is sufficient, not necessary. Parallel tasks can mutate disjoint regions, or use controlled operations whose effects commute. The proof must cover aliasing and hidden global state.

### Disjoint regions and effect systems

Partition an array into nonoverlapping indexed slices. Each task writes only its slice; join establishes that all writes completed before observation. Physical order cannot change the final array. Divide-and-conquer extends this recursively when subregions are demonstrably separate.

A region/effect type system can record read/write effects and reject parallel tasks with interfering effects, or permit declared commutative operations. Deterministic Parallel Java demonstrated this approach for an object-oriented setting. Static checking can make guarantees modular, but annotations/inference, unsafe/foreign code, reflection, and coarse regions define the trusted boundary.

Ownership and isolated/unique values provide another route: transfer an object to one task, mutate privately, then return it. Immutability makes sharing safe; uniqueness makes mutation unshared. Data-race freedom alone is weaker because atomic operations or locks can implement intentionally nondeterministic “first winner.”

### Commutativity and deterministic identities

If two effects commute—`a ⊗ b = b ⊗ a` under the actual state and observation—order need not matter. Integer set union commutes; appending to a list does not. Incrementing an exact unbounded counter commutes; fixed-width overflow behavior and associated metadata need checking.

Associativity is also needed to regroup reductions: `(a⊗b)⊗c = a⊗(b⊗c)`. Mathematical real addition is associative, IEEE floating-point addition is not generally. Even associative/commutative values may carry nondeterministic witnesses: a map merge that keeps “any” equal-scored item needs stable tie-breaking if item identity is observed.

Commutativity must include errors and side effects. Two updates may yield the same final count but emit differently ordered audit records. Either exclude order from O, assign stable event IDs and sort, or serialize emission.

### Deterministic reductions

Fix a reduction tree based on input indices, not worker count or arrival order. Each leaf corresponds to a stable range; internal nodes combine in a defined shape. Workers may compute nodes whenever dependencies are ready, but the expression tree remains fixed.

For bitwise floating-point reproducibility, specify format, rounding, contraction/FMA, exceptional values, compiler flags, library algorithms, and reduction tree. Compensated or exact/superaccumulator schemes can improve stability/reproducibility but have costs. “Parallel sum” alone is not a bitwise contract.

Scans similarly use a fixed tree and stable input order. If only a tolerance is required, define metric and bound; do not call unequal bits identical. Numerical accuracy and determinism are separate: a fixed poor order is reproducibly inaccurate.

### Logical identities and stable ordering

Assign task IDs from input structure: array interval, DAG node key, record offset, or deterministic child numbering. Never derive semantic order from thread ID, address, insertion race, or completion timestamp. Use a total tie-break key where equal priorities occur.

Stable collection traversal requires sorted keys, insertion order with deterministic construction, or a container whose specification guarantees relevant order. Hash seeds can improve denial-of-service resistance; do not disable them casually. Instead separate map lookup from deterministic output sorting.

Logs and metrics from workers can carry `(logical_operation, task_id, local_sequence)` and be merged deterministically when ordered audit output is required. Operational live logs may remain arrival-ordered if their nondeterminism is explicitly outside product results.

### Deterministic commit after parallel speculation

Order-sensitive effects can be computed speculatively then validated and published in logical order. Each task produces a proposal from a declared snapshot. A coordinator considers task 0, 1, 2, validates dependencies against state produced by prior logical commits, and either commits or recomputes/aborts according to deterministic policy.

This resembles ordered transactions. Physical computation overlaps; conflict serialization is stable. It can waste work when an earlier commit invalidates later proposals and can bottleneck at commit. Partitioned logical orders reduce cost when cross-partition effects are absent or a deterministic global merge exists.

The following model receives proposals in completion order 2, 0, 1 but applies operations in logical order. It is sequential teaching code, not parallel execution, validation, or an ordering runtime.

<!-- bijux-verify: {"id":"deterministic-logical-commit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"completion_order=[2, 0, 1]\ncommit_order=[0, 1, 2]\nlogical_result=7\ncompletion_order_result=6\naudit=['0:add:3', '1:mul:2', '2:sub:1']\n","stderr":""}} -->
```python
proposals = {
    0: ("add", 3),
    1: ("mul", 2),
    2: ("sub", 1),
}
completion_order = [2, 0, 1]


def apply(value, proposal):
    operation, argument = proposal
    if operation == "add":
        return value + argument
    if operation == "mul":
        return value * argument
    return value - argument


logical = 1
audit = []
for task_id in sorted(proposals):
    logical = apply(logical, proposals[task_id])
    operation, argument = proposals[task_id]
    audit.append(f"{task_id}:{operation}:{argument}")

arrival = 1
for task_id in completion_order:
    arrival = apply(arrival, proposals[task_id])

print(f"completion_order={completion_order}")
print(f"commit_order={sorted(proposals)}")
print(f"logical_result={logical}")
print(f"completion_order_result={arrival}")
print(f"audit={audit}")
```

The result difference proves order matters for these operations, not that stable commit is always the best architecture.

### Deterministic consistency and epochs

Another model isolates each worker's writes during an epoch. Workers read a stable input snapshot, compute privately, then reconcile writes at a deterministic synchronization point. Conflicting writes can be rejected, reduced with a specified operator, or ordered by logical identity. Workers do not observe timing-dependent intermediate updates.

Bulk-synchronous parallel and deterministic consistency models follow this broad shape. Barriers can limit communication nondeterminism but add waiting and stragglers. A fixed epoch size based on logical work is more reproducible than “commit every 10 ms,” though adaptive sizes may improve throughput at the price of placing the adaptation input in C.

Deterministic shared-memory multiprocessing systems instead constrain inter-thread communication at runtime, potentially supporting legacy code. They can impose deterministic quantum/commit order, buffering, or hardware rules. This is a system guarantee with trusted compiler/runtime/OS boundaries, not an application proof automatically supplied by a marketing label.

### Randomness

One global pseudorandom generator consumed by whichever task runs first is schedule-dependent even with a fixed seed. Derive an independent stream/key from `(master_seed, logical_task_id, sample_index)` using a specified generator, or preassign fixed subsequences. Stable splitting must avoid overlap and specify version/endianness where cross-platform reproduction matters.

Statistical independence and deterministic reproducibility are different claims. A convenient hash is not necessarily a suitable random generator. Cryptographic randomness intentionally resists reproduction and should not be replaced by deterministic streams in security protocols. Tests can inject a deterministic source while production uses an authorized entropy boundary.

Module 069 develops reproducible randomness in depth.

### Time, I/O, and external state

Capture an immutable input snapshot before parallel computation, or make each external observation an explicitly ordered event. Directory entries are sorted by normalized path; file bytes and metadata are versioned; environment and locale are recorded; database reads use a declared snapshot; network responses carry stable request identity and are incorporated by logical policy rather than arrival race.

Wall time can be an output annotation excluded from semantic hashes, or an input captured once. Reading “now” independently in workers makes results schedule-dependent. Monotonic deadlines are operational controls; if timeout changes the product result, the platform/load timing model is part of C.

External writes cannot be rolled back by reordering memory. Buffer intents and dispatch in logical order with idempotency/durability appropriate to the system. Parallel completion should not send customer-visible actions in arbitrary order when order is contractual.

### Exceptions, cancellation, and partial failure

“Throw the first exception observed” is completion-order nondeterminism. Define a deterministic policy: lowest logical task ID failure; aggregate all failures sorted by ID/type; or fail one epoch after all tasks reach a boundary. This can delay failure reporting, a trade-off to document.

Cancellation can produce different partial work depending on timing. If partial work is unobservable and the result is simply Cancelled, output remains deterministic at that coarse observation, but resource usage/traces vary. If completed prefixes are returned, choose prefixes by logical order and define the cancellation input/event.

Worker loss, allocation failure, and retry need stable outcomes or declared environmental configuration. Retrying a failed task on another worker must preserve logical identity, random stream, snapshot, and effect idempotency.

### Intentional nondeterminism

Some operations should expose choice: a server accepts whichever healthy replica answers first; search returns any satisfying witness; load balancing samples current capacity. Make nondeterminism explicit in types/APIs or isolate it at a boundary that returns a captured choice as new input to a deterministic core.

Safe nondeterminism can constrain all outcomes to preserve invariants without requiring equality. Specify the allowed result set and observation. Do not hide it behind a deterministic API whose tests assume one answer.

Deterministic tie-breaking can introduce bias or hot spots. Fair/random selection may be a product requirement. Reproducibility and fairness trade off; use seeded epochs or auditable choice when both matter.

### Determinism versus deterministic testing and replay

A deterministic scheduler for testing chooses controlled schedules so failures can be reproduced and state space explored. It does not prove production executions have identical results. Module 066 develops this method.

Record/replay logs nondeterministic decisions during one production execution and enforces them later. It helps diagnosis but may miss races that did not occur, logs sensitive/large state, and depends on binary/environment compatibility. Deterministic execution constrains decisions in the original run. Module 070 develops replayable concurrency.

Using one fixed deterministic schedule for every test can reduce schedule coverage. Combine deterministic-by-construction result tests with systematic or randomized schedule exploration for concurrency mechanisms that remain schedule-sensitive.

### Performance and operations

Determinism may serialize communication, buffer effects, sort output, fix suboptimal partitions, wait for slow logical predecessors, and redo invalidated speculation. Measure parallel work, span, commit width, buffer bytes, validation/recompute, straggler delay, stable-sort cost, task granularity, and cross-partition conflicts.

Do not sacrifice the contract silently under overload. A “fast nondeterministic mode” is a different API/configuration whose artifacts must be labeled. Adaptive scheduling can vary freely if results are protected; adaptive semantic grouping belongs to C or must preserve equivalence.

Operators need logical IDs and deterministic artifact hashes, plus physical timing/worker traces for performance. Separating semantic from physical telemetry lets equal outputs coexist with different schedules.

### Evidence plan

Prove task determinism and noninterference/commutativity or stable conflict order. Prove each external input is captured and each observation constructed deterministically. For DAGs, induct over nodes. For reductions, prove the fixed tree/operator properties in the actual numeric model. For ordered commit, prove proposal identity, validation, and publish order.

Run the same captured inputs under varied worker counts, work-stealing seeds, yields, delays, CPU affinity, architectures/toolchains in scope, vectorization settings, hash seeds, allocation pressure, exceptions, cancellation points, and failures. Compare semantic output/state hashes and ordered errors; separately inspect race, memory, and lifecycle correctness.

Use metamorphic properties and a sequential reference. Deliberately perturb completion order and verify invariant results. Test undeclared inputs by changing locale, time zone, directory order, environment, dependency version, and random source. One hundred equal runs increase confidence but do not prove universal determinism; static/formal arguments cover the quantified claim.

## Definitions and Notation

- `I`: declared semantic input.
- `C`: declared configuration/environment allowed to affect observation.
- `E(I,C)`: permitted executions, including physical schedules.
- `O(e)`: declared observation of execution e.
- `F(I,C)`: uniquely specified result for deterministic contract.
- `eff(T)`: read/write/external effect summary of task T.
- `T_i ≺ T_j`: stable logical order, independent of physical completion.
- `⊗`: reduction or merge operator under the actual value model.
- `G=(V,E)`: deterministic task DAG.
- `H_sem`: hash of canonical semantic outputs, excluding declared physical telemetry.

The central property is `∀e1,e2∈E(I,C): O(e1)=O(e2)`. It says neither that e1 and e2 have the same timing/interleaving nor that the common observation is correct.

## Mechanisms, Invariants, or Proof Structure

### DAG induction

Base nodes are deterministic functions of captured I/C. For any node v, assume all predecessors have unique values. If v's code is deterministic over those values and its effects do not interfere outside declared ordering, v has one value. A topological induction gives unique observed sink values.

### Noninterference or commutativity proof

For parallel T and U, show their writes are disjoint from the other's reads/writes, or show both compositions produce observationally equal state/effects. Cover aliases, errors, overflow, allocation identity, logs, and external effects. Join establishes completion before observation.

### Stable reduction proof

Map each input index to one leaf and define one binary tree independent of worker/schedule. Each internal result is fixed by child values and the specified operator implementation. Induction produces one root, even when the operator is nonassociative; changing tree is prohibited for that contract.

### Ordered-commit proof

Assign unique logical sequence numbers from I. Proposals remain private. At sequence k, validate against state after commits `<k`, recompute deterministically if needed, publish exactly once, and advance. Induction on k gives one committed state and audit sequence.

## Alternatives and Trade-Offs

| Approach | Main advantage | Principal limitation |
|---|---|---|
| Pure immutable DAG | simple compositional proof | copying/data representation/effect boundary |
| Region/effect system | compile-time noninterference | annotations, unsafe/foreign trusted base |
| Ownership/isolated values | local mutation without sharing | transfers and global aggregation |
| Fixed reduction tree | reproducible aggregation | may constrain load balancing/numerics |
| Deterministic epochs | controlled shared-state visibility | barriers, buffering, stragglers |
| Ordered speculative commit | parallel compute, stable conflicts | validation, redo, commit bottleneck |
| System-enforced schedule | supports broader legacy code | runtime/OS cost and trusted complexity |
| Record/replay | reproduces one observed run | not deterministic original semantics |
| Explicit nondeterminism | supports racing/fair choice honestly | larger allowed outcome/test space |

Prefer the weakest mechanism that proves the declared observation. Do not force identical physical traces when stable values suffice; do not claim stable values when exceptions, effects, or bytes remain variable.

## Failure Modes and Misconceptions

- **“Race-free means deterministic.”** Locks and atomics can safely choose different winners.
- **“Same output means same execution.”** Schedules and resource use may differ.
- **“Fixed seed is enough.”** Shared-stream consumption can depend on schedule.
- **“Addition is associative.”** Not generally in floating-point arithmetic.
- **“Hash map order is irrelevant.”** Serialization, tie-breaking, and hashes may observe it.
- **“First completed is fastest and harmless.”** It makes result depend on physical timing.
- **“Replay provides deterministic production.”** It reproduces a logged run after the fact.
- **“One scheduler improves testing.”** It can hide untested schedules.
- **“Sorting at the end fixes everything.”** Earlier choices/effects may already differ.
- **“Timeout is purely operational.”** If it changes output, timing is semantic input.
- **“Exceptions do not count.”** Error identity/order are observations.
- **“Deterministic means correct.”** Wrong or unsafe results can be repeatable.
- **“Commutative state implies commutative effects.”** Audit/event order may differ.
- **“Determinism is free.”** Stable ordering, buffers, barriers, and redo cost resources.
- **“Cross-platform is automatic.”** numeric, library, locale, and compiler semantics vary.

## Worked Examples

### Example 1

**Disjoint array map.** Task i writes only output slice i from immutable input slice i; join precedes read. Schedules vary but the final indexed array is fixed. **Conclusion:** disjoint effects give deterministic shared-memory mutation.

### Example 2

**Atomic winner.** Two race-free threads compare-exchange an empty winner slot with A/B. Exactly one wins safely, but schedule selects which. **Conclusion:** data-race freedom is not output determinism.

### Example 3

**Floating reduction.** Parallel grouping of `[1e20,-1e20,3]` can yield 3 or 0 in binary floating point. Fix the tree or use a reproducible accumulator. **Conclusion:** mathematical associativity cannot be assumed in machine arithmetic.

### Example 4

**Random streams.** Fixed seed plus shared generator assigns samples by scheduling. Deriving stream from `(seed,task_id,sample_index)` stabilizes assignment. **Conclusion:** logical identity, not consumption timing, owns randomness.

### Example 5

**Stable error.** Tasks 2 and 7 fail; arrival policy reports either. Aggregate sorted failures or choose lowest ID 2. **Conclusion:** exception policy belongs to O.

### Example 6

**Hash output.** Map lookup is correct but iteration bytes vary across seeds. Sort normalized keys before serialization while retaining protected hashing internally. **Conclusion:** canonicalization belongs at observation boundaries.

### Example 7

**Ordered speculation.** Task 9 finishes before task 8, but their noncommuting writes commit 8 then 9; task 9 revalidates after 8. **Conclusion:** computation order can vary while effect order is logical.

### Example 8

**Timeout variation.** Same values run on loaded and idle hosts; one hits 100 ms and returns partial output. Either include timing platform in C or make timeout operational with no partial semantic result. **Conclusion:** resource/time failures bound claims.

### Example 9

**Intentional replica race.** The first healthy replica response is a product latency choice. Capture chosen response as input to a deterministic validation core and expose that selection may vary. **Conclusion:** isolate, do not deny, required nondeterminism.

### Example 10

**Radiotherapy dose calculation.** Parallel numerical planning must bind patient/model inputs, algorithm/toolchain, floating rules, reduction trees, random streams, error behavior, artifact canonicalization, and independent verification. Deterministic bytes do not prove clinical correctness. Named medical-physics, radiation-oncology, numerical, software/runtime, hardware, cybersecurity, quality/regulatory, clinical-operations, and independent safety reviewers must approve requirements and evidence; none is claimed here. **Conclusion:** high-stakes reproducibility is necessary evidence, not sufficient safety.

## Cross-Program Connections

- **Programming languages:** purity, ownership, effects, regions, and controlled nondeterminism enforce contracts.
- **Numerical computing:** reduction order, rounding, vectorization, and error bounds define reproducibility.
- **Distributed systems:** logical time, stable IDs, snapshots, and deterministic state machines share mechanisms.
- **Operating systems:** deterministic communication/scheduling can support legacy programs at system level.
- **Testing:** schedule control and replay complement rather than replace semantic determinism.
- **Security:** entropy, hash randomization, timing, and priority mean reproducibility must respect threat models.
- **Data engineering:** canonical serialization and provenance make artifacts comparable/cacheable.
- **Safety engineering:** repeatable evidence must connect to independent correctness and hazard review.

## References

1. Gilles Kahn, “The Semantics of a Simple Language for Parallel Programming,” IFIP Congress 1974, pp. 471–475. <https://dblp.org/rec/conf/ifip/Kahn74>
2. Edward A. Lee, “The Problem with Threads,” *Computer* 39(5), 2006. <https://doi.org/10.1109/MC.2006.180>
3. Robert L. Bocchino Jr. et al., “A Type and Effect System for Deterministic Parallel Java,” OOPSLA 2009. <https://doi.org/10.1145/1639949.1640097>
4. Joseph Devietti, Brandon Lucia, Luis Ceze, and Mark Oskin, “DMP: Deterministic Shared Memory Multiprocessing,” ASPLOS 2009. <https://doi.org/10.1145/1508244.1508255>
5. Tom Bergan, Owen Anderson, Joseph Devietti, Luis Ceze, and Dan Grossman, “CoreDet: A Compiler and Runtime System for Deterministic Multithreaded Execution,” ASPLOS 2010. <https://doi.org/10.1145/1736020.1736029>
6. Amittai Aviram, Shu-Chun Weng, Sen Hu, and Bryan Ford, “Efficient System-Enforced Deterministic Parallelism,” OSDI 2010. <https://www.usenix.org/legacy/events/osdi10/tech/full_papers/Aviram.pdf>
7. Robert L. Bocchino Jr., Vikram S. Adve, Sarita V. Adve, and Marc Snir, “Parallel Programming Must Be Deterministic by Default,” HotPar 2009. <https://www.usenix.org/event/hotpar09/tech/full_papers/bocchino/bocchino.pdf>
8. Robert L. Bocchino Jr. et al., “Safe Nondeterminism in a Deterministic-by-Default Parallel Language,” POPL 2011. <https://doi.org/10.1145/1926385.1926394>
9. OpenMP Architecture Review Board, *OpenMP API Specification 5.2*, November 2021; retrieved 2026-08-29. <https://www.openmp.org/spec-html/5.2/openmp.html>
10. IEEE, *IEEE Standard for Floating-Point Arithmetic*, IEEE 754-2019. <https://doi.org/10.1109/IEEESTD.2019.8766229>

## Exercises

### Exercise 1

Define output, state, schedule, timing, and replay determinism. Give one pair of executions that differs physically but satisfies an output-determinism contract.

### Exercise 2

Prove a parallel map over four disjoint output slices deterministic, naming alias, input, join, exception, and observation assumptions.

### Exercise 3

Diagnose a fixed-seed floating Monte Carlo program whose results change with worker count. Redesign random streams, reduction, errors, and provenance.

### Exercise 4

Design deterministic parallel processing of files from a directory with failures and external result publication. Specify input capture, IDs, ordering, cancellation, retries, and effect commit.

### Exercise 5

A genomic clinical pipeline requires reproducible parallel variant results across approved machines. Specify claim scope, proof, verification matrix, residual nondeterminism, and mandatory human review.

## Answers to the Exercises

### Answer 1

Output determinism fixes declared returned/external values; state determinism fixes specified internal final state; schedule determinism fixes chosen synchronization/interleaving decisions; timing determinism constrains event times under a model; replay determinism reproduces one recorded run. Two map tasks can execute and finish in opposite orders yet write disjoint indexed slices and produce the same final array. Their physical trace differs while O projects only the joined array, so output determinism holds.

### Answer 2

Capture immutable input I. Assign each logical task one nonoverlapping output interval covering all indices exactly once. Prove no alias lets a task write another interval or mutate/read changing hidden state. Each element function is deterministic for I/C. Task exceptions use one deterministic aggregate/lowest-ID rule. Join completes all writes before O reads the entire array; partial arrays are unobservable. By per-element function uniqueness and disjoint writes, order commutes; union of four slices yields one array. Allocation/resource failure and toolchain numeric semantics are included in C or handled deterministically.

### Answer 3

The shared PRNG assigns samples by schedule, and worker-count-dependent floating grouping changes rounding. Derive each sample from a specified counter/keyed generator using `(master_seed,logical_sample_index)` so partitioning does not change values. Use a fixed index-derived reduction tree, reproducible accumulator, or declared tolerance; fix numeric format/compiler contraction rules. Define NaN/overflow/allocation/worker-failure handling and stable exception aggregation. Record seed, generator/version, sample count, tree, algorithm, toolchain/platform, configuration, and semantic hash. Test varied workers/schedules/vector widths within scope against a sequential reference and statistical-quality evidence separately.

### Answer 4

Snapshot the directory into sorted normalized relative paths plus file identity/content digest and configuration; reject or explicitly handle mutation during capture. Derive task ID from path/digest, not enumeration/completion. Parse purely to private proposals. Aggregate failures sorted by task ID or use a declared lowest-ID rule. Cancellation yields no published partial result or a logical-prefix contract. Retries preserve ID/input/random stream and are bounded. Canonicalize result records and commit in task/path order; dispatch external writes from idempotent stable intents with durability appropriate to requirements. Record provenance and separate physical logs/timing from semantic artifacts.

### Answer 5

Define I as immutable samples, reference genome/version, annotations, parameters, consent/access context, and captured external databases; define C as approved algorithm, library/toolchain, numeric, hardware/OS settings allowed to affect O. O includes canonical variants, scores, warnings, failures, provenance, and ordering. Prove pure/disjoint stages, fixed IDs/random streams, stable joins/reductions/ties, complete conflict order, and deterministic error/effect policy. Verify repeated schedule perturbation, worker counts, approved architectures, vectorization, locales, hash seeds, resource pressure, faults, cancellation/restart, dependency data, and sequential/independent reference comparisons. Residual external acquisition timing, hardware faults, and explicitly probabilistic algorithms are captured or excluded visibly. Named clinical-genetics, molecular-pathology, bioinformatics, statistical/numerical, software/runtime, security/privacy, laboratory operations, quality/regulatory, and independent assurance reviewers must approve intended use, validation, fallback, and residual risk. Reproducibility alone is not clinical validity.
