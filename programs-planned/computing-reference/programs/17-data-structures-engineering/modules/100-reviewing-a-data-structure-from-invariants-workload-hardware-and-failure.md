---
module_id: DSE-100
program: Data Structures Engineering
level: 2
module_number: 100
title: Reviewing a Data Structure from Invariants, Workload, Hardware, and Failure
status: complete
last_verified: 2026-08-30
---

# Reviewing a Data Structure from Invariants, Workload, Hardware, and Failure

## One-Page Review

### Governing question

How should an expert review turn an abstract data-structure claim into reproducible evidence about semantics, invariants, workload fit, hardware cost, concurrency, persistence, failure recovery, security, and operational limits?

### Essential definitions

A **review contract** names operations, inputs, outputs, errors, coordinate/order/equality semantics, consistency, durability, and resource limits. An **invariant** is a property required after every allowed transition or at a named quiescent boundary. A **reference oracle** implements the same semantics independently, usually more simply.

A **workload model** describes data distributions, operation mix/order, locality, concurrency, history, and scale. A **cost model** counts relevant comparisons, probes, bytes, cache lines, allocations, I/O, synchronization, messages, and amplification. A **failure model** enumerates faults and required post-fault behavior. A claim is accepted only within the environment and evidence that support it.

### Central model, mechanism, or theorem

Review proceeds as a chain: specify observable semantics; derive representation invariants and proof obligations; test deterministic boundary traces and independent oracles; generate properties/adversarial histories; measure on declared workloads/hardware; inject allocation, crash, corruption, concurrency, and distributed faults; inspect persistence/recovery/security; then report pass/fail/skip/unavailable evidence and limitations.

Big-O is necessary but incomplete. Two (O(1))-expected tables can differ in tail probes, cache misses, resize pauses, memory overhead, deletion correctness, collision attacks, and crash behavior. Conversely, a slower asymptotic structure may win at bounded scale or for ordered operations.

### Critical invariants

- The review tests a fixed semantic contract, not whichever behavior the implementation exhibits.
- Reference oracle and candidate do not share the same risky mechanism.
- Every mutation is followed by narrow structural checks or sampled/exhaustive audit proportional to risk.
- Workloads include boundaries, history-dependent states, skew, adversarial cases, and production-like traces.
- Metrics include distributions and total owned resources; warmup, environment, versions, and raw results are retained.
- Concurrent/distributed claims use histories and consistency checkers or model/simulation evidence, not final state alone.
- Failure injection checks recovery state and invariants, not merely process survival.
- Benchmark success never substitutes for correctness, security, durability, or external review.

### Common failures

Failures include benchmarking before specifying semantics, testing only random happy paths, using the candidate as its own oracle, checking only final values, measuring averages without tails, omitting build/resize/GC/repair, ignoring cache/NUMA/I/O, comparing unequal functionality, running too-small data, optimizing to one benchmark, suppressing failed runs, assuming sanitizer/fuzzer coverage proves correctness, injecting crashes without durable-state validation, calling a checksum authenticity, and generalizing one machine/workload to universal superiority.

### Compact example

A bounded linear-probing table is reviewed against a dictionary through colliding inserts, lookup, tombstone deletion, and reuse. The trace ends with identical items, records probe counts `[1,2,3,3,2,4,2]`, and validates reachability/uniqueness/live count. Injecting a duplicate live key makes the invariant checker fail. This proves only the fixture semantics and operation-count evidence, not production hashing, concurrency, persistence, or speed.

### Connections

This capstone applies to all earlier DSE modules: lists/trees/heaps/hashes/graphs, succinct/probabilistic/spatial/approximate structures, persistence/concurrency, and distributed structures. Database, systems, security, performance, formal methods, numerical computing, and SRE provide stronger domain-specific oracles, failure models, and observability. The next course focus is Database Engineering.

## Governing Question

What evidence is sufficient to accept, reject, or narrowly qualify a data structure for a named product workload and failure environment?

## Why This Matters

Textbook correctness usually assumes unbounded mathematics, valid inputs, sequential execution, and reliable memory. Production adds finite integers, allocators, caches, storage, threads, processes, networks, corruption, upgrades, untrusted inputs, and operators. A structure can implement its algorithm faithfully yet fail its service.

Reviews also fail through vague confidence. A green unit suite says little about untested histories; a fast median hides tail collapse; a successful restart may return stale or corrupt state. A disciplined evidence ladder makes disagreements auditable and completion claims reproducible.

## Prerequisites and Retrieval

Retrieve abstract data types, representation invariants, induction/refinement, asymptotic/amortized/expected bounds, reference models, property-based/fuzz/metamorphic/differential testing, concurrency histories/linearizability, memory hierarchy/NUMA, performance counters/statistics, serialization/durability/recovery, threat modeling, fault injection, deterministic simulation, and reproducible experiments.

The reviewer distinguishes **proof**, **automated check**, **independent recomputation**, **empirical observation**, **external review**, and **unavailable evidence**. None may be relabeled as another.

## Learning Objectives

After this chapter, you should be able to:

1. turn an ADT and implementation into a reviewable semantic/invariant contract;
2. build independent oracles and trace/property/metamorphic test suites;
3. derive operation, space, cache, allocation, I/O, synchronization, and message cost models;
4. design fair statistically defensible benchmarks and comparisons;
5. inject corruption, allocation, crash, concurrency, network, and upgrade failures;
6. review persistence, security, observability, capacity, and operational lifecycle;
7. write a calibrated decision and evidence record whose claims match its scope.

## Core Exposition

### Freeze the contract before results

Name key/value domains, duplicates, equality/order/hash/normalization, null/NaN/sentinel behavior, ownership/lifetimes, zero/one-based coordinates, range endpoints, errors, and determinism. List operations and required complexities. For concurrent/distributed structures, name consistency, progress, membership, replica, and snapshot semantics. For persistent structures, name commit, durability, recovery, compatibility, and corruption policy.

Separate required, optional, and out-of-scope capabilities. Comparing a count-only compressed index with a mutable locate/extract index is not fair. Record environment/feature flags and the exact artifact digest/commit under review.

### Derive invariants and proofs

Representation invariants connect bytes/pointers to the ADT: ordering, balance, sizes, parent/child consistency, ownership, permutation, probe reachability, sample/rank support, causal context, checksums, and generation identity. State when each must hold—after every public operation, while locked, after recovery, or after convergence.

Prove local preservation where feasible: base construction, each mutation case, rotations/splits/merges, resize/migration, lazy/persistent updates, and error rollback. Qualify amortized or probabilistic claims with potential/distribution/adversary assumptions. Mark proof sketches and unproved implementation correspondence.

Implement validators independent of mutation paths. Avoid a validator that calls the same search routine to prove search correctness unless supplemented by a full structural scan/oracle. Expensive validators belong in build/test and sampled production diagnostics.

### Construct an evidence matrix

Map every claim to evidence and owner: static/type check, unit/boundary trace, invariant scan, reference differential, property/metamorphic test, exhaustive small-state enumeration, fuzz/sanitizer, formal proof/model check, benchmark/counter, failure injection, compatibility/corruption test, operational observation, or human review. A missing row is visible rather than silently assumed.

Deterministic fixtures pin conventions and regressions. Exhaustive small states expose boundary combinations. Random generators need seeds, shrinking, valid-state construction, and coverage dimensions. Metamorphic properties—permutation invariance where valid, round trip, split/merge equivalence, monotonicity, idempotence—work when exact outputs are hard.

### Workload and cost model

Describe cardinality, size distributions, key entropy/skew, duplication, graph degree/depth, locality, update/query mix, range length, success/miss ratio, concurrency, batch size, history/tombstones, version count, and failure/churn. Use synthetic controlled axes plus anonymized/replayable production traces; neither alone is universal.

Derive costs beyond Big-O: comparisons/probes, pointer dereferences, bytes/cache lines/pages, branches, allocations/copies, hashes, compression/decompression, locks/atomics/retries, syscalls/I/O, messages/replicas, background repair, and peak construction space. Measure tail distributions by operation class and state age.

### Hardware and runtime reality

Flat contiguous layouts exploit spatial locality/prefetch; pointer structures incur latency but support incremental shape/persistence. Element size changes cache/TLB residency. False sharing, NUMA placement, atomic contention, allocator fragmentation, GC, JIT, vectorization, endianness, unaligned access, and mapped I/O can dominate asymptotics.

Record CPU/model/microcode, cores/pinning/frequency, memory/NUMA, storage/filesystem, OS/kernel, compiler/runtime/flags, dependencies, power/thermal state, dataset placement, and counter tooling. Separate cold/warm cache and single/contended cases. Hardware counters are measurements with multiplexing/sampling caveats, not direct causal proof.

### Benchmark discipline

Warm up when the runtime/workload requires it; calibrate duration; randomize/interleave candidate order; isolate setup; retain raw per-iteration results, failures, seeds, and environment. Use enough independent samples, confidence intervals/quantiles, and practical effect sizes. Investigate multimodality/outliers rather than deleting them silently.

Prevent dead-code elimination and benchmark-special shortcuts; verify outputs during runs. Compare equal semantics, safety, durability, capacity, and tuning effort. Include construction, resize/compaction/GC/rebuild/recovery and peak memory. Report where curves cross rather than declaring one winner from one point.

### Concurrency and distributed histories

Thread sanitizer/race detectors find some implementation races but do not prove linearizability. Generate histories with invocation/response times and operation arguments/results; check against the promised consistency model. Stress small interleavings, model-check core algorithms where possible, and test progress under pauses, preemption, cancellation, overflow, ABA, and reclamation.

Distributed final-state equality misses stale reads, lost acknowledgments, split brain, and temporary invariant violations. Deterministic simulation/model checking controls message delay/loss/duplication/reorder, clocks, crashes, disks, partitions, membership, and retries, while deployed fault tests reveal runtime/network assumptions. Use both and record fault schedules/seeds.

### Failure, persistence, and security

Enumerate invalid input, overflow, allocation failure, partial mutation, exception/panic, cancellation, corrupt/truncated/malicious serialization, wrong version/endianness, crash at every persistence boundary, torn/lost/reordered writes under the declared storage model, disk full, restart, replica/network faults, and dependency failures.

After each fault, validate ADT state, generation/manifest, committed/rolled-back operations, leaks/locks, retry idempotence, and recoverability. Crash survival without semantic verification is not a pass. Backups/rebuilds need restore/reconciliation evidence.

Threat-model attacker control of keys, operation order, serialized bytes, network messages, identities, workloads, and timing. Review collision/algorithmic-complexity attacks, parser bounds, memory/CPU amplification, authorization, tenant isolation, secrets, integrity/authenticity, replay/downgrade, and deletion. Constant time is relevant only under a stated side-channel model and evidence.

### Decision, limitations, and ongoing operation

Conclude accepted, accepted with limits, rejected, or evidence unavailable for each requirement. State tested envelope, counterexamples, unverified surfaces, external review status, and triggers for reevaluation. A benchmark winner may still be rejected for recovery or security; a slower structure may be chosen for simpler proofs/operations.

Production monitors expose load factor/depth/probes/collisions, memory owned/garbage, hit/miss, version/tombstone age, compaction/repair, contention/retries, corruption/recovery, and capacity headroom. Canary upgrades, compatibility matrices, rollback, rebuild, and periodic adversarial/trace replay keep the review alive.

The executable model below demonstrates a small review harness for linear probing. Its stable integer hash and list storage are pedagogical, not production choices.

<!-- bijux-verify: {"id":"data-structure-review-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"capacity=11\ntrace_items=[(1, 'a'), (23, 'c'), (34, 'd')]\noracle_items=[(1, 'a'), (23, 'c'), (34, 'd')]\nprobe_counts=[1, 2, 3, 3, 2, 4, 2]\ntotal_probes=17\nmax_probes=4\ninvariant_valid=True\noracle_valid=True\ncorruption_detected=True\nvalid=True\nevidence=bounded_data_structure_review_model\n","stderr":""}} -->
```python
EMPTY = 0
LIVE = 1
DELETED = 2


class LinearProbingTable:
    def __init__(self, capacity=11):
        self.capacity = capacity
        self.slots = [(EMPTY, None, None) for _ in range(capacity)]
        self.live = 0
        self.probe_counts = []

    def _scan(self, key):
        first_deleted = None
        for distance in range(self.capacity):
            index = (key % self.capacity + distance) % self.capacity
            state, stored_key, _ = self.slots[index]
            if state == DELETED and first_deleted is None:
                first_deleted = index
            if state == EMPTY:
                return "empty", first_deleted if first_deleted is not None else index, distance + 1
            if state == LIVE and stored_key == key:
                return "found", index, distance + 1
        return "full", first_deleted, self.capacity

    def put(self, key, value):
        result, index, probes = self._scan(key)
        self.probe_counts.append(probes)
        if result == "found":
            self.slots[index] = (LIVE, key, value)
        elif index is not None:
            self.slots[index] = (LIVE, key, value)
            self.live += 1
        else:
            raise OverflowError("table is full")

    def get(self, key):
        result, index, probes = self._scan(key)
        self.probe_counts.append(probes)
        return self.slots[index][2] if result == "found" else None

    def discard_key(self, key):
        result, index, probes = self._scan(key)
        self.probe_counts.append(probes)
        if result == "found":
            self.slots[index] = (DELETED, None, None)
            self.live -= 1

    def validate(self):
        keys = [key for state, key, _ in self.slots if state == LIVE]
        return (
            len(keys) == self.live == len(set(keys))
            and all(self._scan(key)[0] == "found" for key in keys)
        )

    def items(self):
        return sorted(
            (key, value) for state, key, value in self.slots if state == LIVE
        )


table = LinearProbingTable()
oracle = {}
for key, value in [(1, "a"), (12, "b"), (23, "c")]:
    table.put(key, value)
    oracle[key] = value
assert table.get(23) == oracle[23]
table.discard_key(12)
oracle.pop(12)
table.put(34, "d")
oracle[34] = "d"
assert table.get(34) == oracle[34]

corrupt = LinearProbingTable()
corrupt.slots = table.slots.copy()
corrupt.live = table.live + 1
corrupt.slots[5] = (LIVE, 1, "evil")

print(f"capacity={table.capacity}")
print(f"trace_items={table.items()}")
print(f"oracle_items={sorted(oracle.items())}")
print(f"probe_counts={table.probe_counts}")
print(f"total_probes={sum(table.probe_counts)}")
print(f"max_probes={max(table.probe_counts)}")
print(f"invariant_valid={table.validate()}")
print(f"oracle_valid={table.items() == sorted(oracle.items())}")
print(f"corruption_detected={not corrupt.validate()}")
print(f"valid={table.validate() and table.items() == sorted(oracle.items()) and not corrupt.validate()}")
print("evidence=bounded_data_structure_review_model")
```

The validator calls `_scan` for reachability, so uniqueness/count are independently scanned but probe-search implementation is not fully independent. A stronger review also reconstructs clusters with a separate oracle and exhaustively enumerates small states/traces.

## Definitions and Notation

- An **ADT contract** defines observable legal behavior independently of representation.
- A **representation invariant** connects implementation state to valid ADT state.
- A **refinement/proof obligation** shows implementation transitions preserve/implement the contract.
- An **oracle** is an independently implemented expected-result source.
- A **trace/history** records ordered or concurrent invocations, responses, faults, and relevant state.
- A **workload envelope** bounds distributions, scale, concurrency, history, and environment covered by a claim.
- A **cost model** maps operations/state to counted abstract/hardware/system resources.
- **Amplification** is physical work/bytes relative to logical requested work/bytes.
- A **failure model** states faults and required safety/liveness/recovery behavior.
- A **claim-evidence matrix** maps each acceptance statement to direct evidence and limitations.
- **Practical significance** asks whether an observed effect matters under service constraints, beyond statistical detectability.

## Mechanisms, Invariants, or Proof Structure

### Refinement chain

Define abstraction function (A) from representation (R) to ADT state. Prove initialized representation satisfies invariant (I); each public operation on an (I)-state either fails without forbidden change or produces another (I)-state whose abstraction matches the ADT transition/result. Serialization/recovery/concurrency add corresponding boundaries. Tests sample this argument; they do not replace uncovered proof obligations.

### Oracle independence

An oracle should prefer clarity and a different algorithm/layout. Differential equality is meaningful only for identical semantics. For approximate/probabilistic structures, compare declared error/coverage properties against exact data, distributions, confidence procedures, and adversarial cases rather than demanding bit-identical output.

### Complexity-to-measurement bridge

Asymptotic analysis identifies growth terms and assumptions. An operation-count model predicts comparisons/probes/bytes; hardware/system measurements test whether those costs explain observed latency/throughput on a declared environment. Disagreement prompts investigation of caches, branches, allocation, runtime, I/O, contention, and background work—not immediate rejection of either layer.

### Failure refinement

For each fault point, define allowed externally visible histories and recovery state. Inject the fault, reopen/rejoin using the real recovery path, then validate committed effects, rolled-back effects, invariants, leaks, and continued progress. A process exit code cannot establish durable correctness.

### Claim calibration

Evidence directly supports only the tested/proved domain. A finite fixture proves its exact result; a property campaign increases confidence over its generator; a theorem proves its premises/conclusion; a benchmark observes one configuration; internal review is not external peer review. The final statement preserves these labels.

## Alternatives and Trade-Offs

**Proof-first review:** strongest for crisp algorithms/invariants, but implementation/runtime/failure correspondence still needs evidence.

**Test-first review:** fast feedback and broad examples, but coverage gaps and shared-oracle bugs remain.

**Formal model checking:** exhaustive within bounded models/interleavings and excellent for concurrency/distribution; abstraction/state explosion limit scope.

**Fuzz/property testing:** discovers unexpected inputs/histories with shrinking and instrumentation; passing does not prove absence.

**Benchmark-led selection:** essential for workload/hardware fit, dangerous without semantic equivalence and correctness gates.

**Operational canary/A-B:** exposes real integrations/scale, but must protect users/data, control confounders, and never be the first correctness test.

**Third-party library adoption:** may bring maturity/ecosystem, while requiring version-specific contract, dependency, vulnerability, and local-workload review.

**Build versus buy/simpler baseline:** a sorted vector, database index, standard map, or rebuildable snapshot may outperform a sophisticated structure in total engineering risk/cost.

## Failure Modes and Misconceptions

1. Contract is inferred from current implementation bugs.
2. Required and optional functionality are compared unequally.
3. Candidate and oracle share the same faulty helper.
4. Only final state is checked, missing transient/history violations.
5. Random happy paths omit empty/full/boundary/collision cases.
6. Invalid states are generated and mistaken for meaningful coverage.
7. Big-O omits constants, distributions, amortization, and adversaries.
8. Average latency hides p99/max/resize/compaction stalls.
9. Throughput hides fairness, starvation, retries, or dropped work.
10. Final size omits build peak, scratch, allocator, indexes, replicas, and retained source.
11. Microbenchmark removes compiler work or measures setup/noise.
12. Candidate order, thermal state, cache warmth, or NUMA confounds results.
13. Failed/outlier runs are deleted without rule/explanation.
14. Hardware counters are treated as direct causal proof.
15. Race detectors are treated as linearizability proof.
16. Crash injection stops before reopening and validating data.
17. Checksums are treated as authenticity or semantic validation.
18. Fuzz/sanitizer/model bounds are generalized beyond coverage.
19. One machine/dataset is called universally fastest/best.
20. Internal author/reviewer evidence is called external validation.

## Worked Examples

### Example 1

For a map, specify duplicate insert as replace versus reject before testing. An oracle using replace cannot validate a candidate whose documented contract rejects duplicates.

### Example 2

A red-black tree validator checks BST order, root black, no red-red edge, equal black height, parent links, and stored sizes after every rotation/delete case. Sorted iteration alone can pass with broken balancing.

### Example 3

Linear probing needs empty/tombstone/live states. Deleting by clearing to empty can make later collided keys unreachable; the capstone fixture explicitly tests tombstone preservation/reuse.

### Example 4

Two hash tables both claim expected (O(1)). Under 90% load one has median two probes but p99 80; another uses more memory and p99 12. The service tail/memory limits, not notation alone, decide.

### Example 5

A pointer tree wins at 1,000 elements but loses to a sorted array at read-heavy 100,000 elements due to cache locality. Report the crossover and update/build tradeoff, not a universal winner.

### Example 6

A persistent B-tree commit is killed after page writes but before root-manifest swap. Recovery must select the old complete root and ignore orphan pages; merely restarting successfully is insufficient.

### Example 7

A concurrent queue produces a history where dequeue returns an item before its enqueue invocation. Final contents may match, but a linearizability checker rejects the history.

### Example 8

A Bloom filter has no false negatives only under its exact insertion/query/hash lifecycle; measure false-positive distribution against expected parameters and adversarial/corrupt inputs, not exact set equality.

### Example 9

A distributed index converges after partition but acknowledged a write later lost. Convergence/final state does not satisfy the durability history; fault tests must retain client responses.

### Example 10

A benchmark shows 15% speedup on one compiler/CPU with overlapping confidence intervals and 3x build memory. A calibrated decision may require more samples and reject it under memory limits even if median improves.

## Cross-Program Connections

- **Algorithms/Formal Methods:** specifications, induction, amortized/probabilistic analysis, refinement, and model checking.
- **Computer Architecture/Performance:** caches, TLB/NUMA, branches, SIMD, counters, Roofline-style bounds, and statistics.
- **Operating/Storage Systems:** allocators, VM, filesystems, I/O, crashes, persistence ordering, recovery, and corruption.
- **Concurrent/Distributed Systems:** histories, consistency, progress, reclamation, simulation, partitions, and fault schedules.
- **Security Engineering:** threat models, malicious inputs, algorithmic complexity, authentication, quotas, and fuzzing.
- **Database/SRE:** workload traces, durability, migrations, observability, capacity, canaries, rollback, and incidents.

## References

1. Robert Sedgewick and Kevin Wayne, [*Algorithms, 4th Edition* companion site](https://algs4.cs.princeton.edu/home/), Princeton University. Author-maintained algorithms, implementations, and analysis reference.
2. Ulrich Drepper, [“What Every Programmer Should Know About Memory”](https://people.freebsd.org/~lstewart/articles/cpumemory.pdf), 2007. Systems memory/cache/NUMA review context.
3. Lawrence Berkeley National Laboratory, [“The Roofline Model: Visualizing and Optimizing Performance”](https://amcr.lbl.gov/departments/computer-science-department/ppan/roofline-performance-model/), official project page. Machine-bound performance-model context and primary publications.
4. Google, [Benchmark User Guide](https://google.github.io/benchmark/user_guide.html), official documentation. Reproducible microbenchmark controls and reporting mechanics.
5. SPEC, [CPU Run and Reporting Rules](https://www.spec.org/cpu2026/docs/runrules.html), official benchmark disclosure/reproducibility methodology.
6. FoundationDB authors, [“FoundationDB: A Distributed Unbundled Transactional Key Value Store”](https://www.foundationdb.org/files/fdb-paper.pdf), *SIGMOD*, 2021. Primary deterministic simulation/fault-testing production evidence.
7. ACM SIGPLAN, [Empirical Evaluation Guidelines](https://www.sigplan.org/Resources/EmpiricalEvaluation/), official experimental design and reporting guidance.

## Exercises

### Exercise 1

Write a claim-evidence matrix for a concurrent persistent hash map covering semantics, expected/amortized complexity, linearizability, lock freedom or blocking, resize, memory reclamation, serialization, crash recovery, corruption, and collision attacks.

### Exercise 2

Design independent validators and exhaustive small traces for the capstone linear-probing table, including update, miss, duplicate replacement, tombstone chains, wrap, full table, deletion/reinsertion, and injected corruption.

### Exercise 3

Design a fair benchmark comparing a B-tree, LSM-backed index, ordered vector snapshot, and hash map for mixed point/range queries and updates across RAM/SSD limits. Define environment, datasets, statistics, full resource accounting, and claims.

### Exercise 4

Design a crash/concurrency/security campaign for a persistent lock-free queue. Include histories, reclamation, allocation failure, persistence points, torn/corrupt images, restart, untrusted serialization, and evidence boundaries.

### Exercise 5

Produce an acceptance decision template for any advanced data structure in this course that prevents a benchmark, test suite, proof sketch, citation count, or internal review from being overstated.

## Answers to the Exercises

### Answer 1

Rows name exact map operations/equality/errors; reference differential and invariant scan; expected probe/hash assumptions plus adversarial collisions; resize potential argument and measured pause/tails; history-based linearizability checker; documented progress premise plus stalled-thread tests/model; sanitizer plus hazard/epoch invariant and delayed-reader tests; canonical versioned serialization; crash-at-every-write recovery oracle; corrupt/truncated/overflow parser rejection; keyed/robust hashing and quotas; total bytes/build peak; and compatibility upgrade/rollback. Each row records artifact/version, command/model, pass/fail/skip, environment, raw evidence, limitations, and owner. Lock freedom requires an algorithmic proof against its machine/memory assumptions; stress success cannot relabel it.

### Answer 2

Build a simple separate model from key to value and a separate cluster scanner: verify legal slot states, live count, unique keys, each live key appears before the first empty from its home along circular scan, tombstones do not count as live, and lookup/update results match the model. Exhaustively enumerate capacities 1–5, bounded keys/values, and all legal traces through a chosen length, including colliding keys, wrap, replacement, misses, delete absent/present, full insertion, tombstone reuse, and repeated cycles. After every step check result and invariants. Mutate slots/count/state/key/value independently—duplicate key, unreachable live after empty, bad state, wrong count—and require detection. Keep candidate `_scan` out of the reachability validator.

### Answer 3

Freeze equal key/order/range/durability semantics and logical dataset. Vary cardinality, key/value sizes, insertion order, skew/locality, hit/miss, range length/selectivity, read/update mix, batch/concurrency, memory pressure, history/compaction, and cold/warm restart. Declare CPU/NUMA/RAM/SSD/filesystem/OS/compiler/runtime/config, pinning/cache protocol, run order, warmup, samples/seeds, confidence/quantiles, correctness checks, and raw artifacts. Measure build/ingest, point/range/update p50/p95/p99/max, throughput/fairness, CPU/counters, bytes read/written/amplification, resident/final/peak/scratch space, resize/flush/compaction/GC, durability/recovery, and background interference. Report Pareto/crossover regions within tested envelopes; do not compare a volatile hash map directly with durable indexes without labeling functionality.

### Answer 4

Specify queue FIFO/empty/errors, linearization/persistence points, progress, durability, and recovery. Generate invocation/response histories across enqueue/dequeue, pauses, cancellation, counter wrap/ABA, delayed reclaimers, allocator failure, and crash at every flush/fence/root update; check linearizability before crash and allowed durable prefix after reopen. Use sanitizers plus model checking for memory ordering, hazard/epoch lifetime assertions, forced reuse, and leak/backlog measures. Corrupt/truncate/swap/version/downgrade serialized fields with checked lengths and bounded allocations; authenticate images if adversarial integrity is required. Reopen through real recovery, validate queue graph/count/order/checksums and retry idempotence. State that bounded models, sanitizer runs, one storage platform, and internal review do not prove universal lock freedom, hardware persistence, security certification, or deployment fitness.

### Answer 5

Template fields: artifact/commit and reviewer/date; ADT and nonfunctional requirements; assumptions/workload/hardware/failure/threat envelope; invariant/proof table; evidence matrix with exact commands/raw artifacts and independent-oracle description; correctness/fuzz/model coverage; benchmark methodology/raw distributions/full resource accounting; concurrency/persistence/recovery/security/compatibility results; counterexamples/failed/skipped/unavailable checks; external review named records; requirement-by-requirement verdict; accepted limits/capacity/operational monitors; rollback/review triggers; residual risks; and decision owner. Every conclusion cites direct evidence and uses “observed,” “checked,” “proved,” or “reviewed” accurately. Overall acceptance requires all mandatory rows pass or an explicit authorized risk decision; one green evidence class cannot erase another failed/missing row.
