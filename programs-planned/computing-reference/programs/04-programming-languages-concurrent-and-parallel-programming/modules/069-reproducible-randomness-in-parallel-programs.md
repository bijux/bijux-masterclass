---
module_id: CONPAR-069
program: Programming Languages: Concurrent & Parallel Programming
level: 2
module_number: 69
title: Reproducible Randomness in Parallel Programs
status: complete
last_verified: 2026-08-29
---

# Reproducible Randomness in Parallel Programs

## One-Page Review

### Governing question

How can a parallel computation assign pseudorandom values to logical samples reproducibly across schedules, worker counts, retries, and checkpoints without overstating statistical independence, cross-version stability, or cryptographic security?

### Essential definitions

- A **pseudorandom number generator** (PRNG) deterministically expands finite state or a key/counter into a sequence intended to have specified statistical properties.
- A **seed** initializes a generator; it is neither automatically sufficient provenance nor proof of an independent stream.
- A **stream** is an ordered generator sequence, and a **substream** is a disjoint or separately derived region assigned to one logical consumer.
- A **stateful sequential generator** advances state on every draw; shared consumption makes value assignment schedule-dependent.
- A **counter-based generator** maps `(key,counter)` directly to output, enabling random access without mutable sequential state.
- A **splittable generator** derives child generators from a parent according to a specified splitting algorithm and pedigree.
- A **jump-ahead** operation advances a generator by a known distance to allocate separated subsequences.
- A **logical random identity** is a stable tuple such as `(experiment,record,algorithmic_stage,sample_index,attempt_role)` independent of physical worker or completion time.
- **bitwise reproducibility** means exact bits repeat under the declared algorithm/version/platform scope; **statistical reproducibility** may permit different samples with equivalent inference.
- **distribution transformation** converts uniform bits to values from another distribution; it is part of the reproducibility contract.
- **common random numbers** deliberately couple simulations using matched streams to reduce comparison variance.
- A **cryptographically secure RNG** meets adversarial unpredictability requirements that ordinary simulation PRNGs do not.

### Central model, mechanism, or theorem

Define random bits as `R = G(algorithm_version, master_key, logical_domain, logical_counter)`. Every sample owns a stable domain-separated identity; scheduling merely decides when that pure mapping is evaluated. Counter-based generators implement this directly. Splittable or jump-ahead designs can implement an equivalent allocation if child derivation, limits, and nonoverlap assumptions are explicit. Reproducibility requires recording generator and distribution algorithms, versions, seed/key material or protected derivation, identity schema, numeric conversion, rejection-consumption rules, and reduction semantics. Passing statistical batteries is empirical evidence, not proof of independence or application validity.

### Critical invariants

No semantic sample index derives from worker ID, queue position, arrival order, thread count, or retry timing. Domain tags distinguish uses such as initialization, mutation, resampling, and fault injection. Key/counter widths cannot collide within the declared workload. Split pedigrees are stable under decomposition changes that the contract promises to tolerate. Rejection loops consume a sample-owned counter lane. Checkpoints preserve logical progress rather than a fragile set of worker-local states. Distribution conversion, floating arithmetic, reductions, and library versions are fixed or scoped. Security keys never appear in ordinary reproducibility logs. Quality and cross-stream evidence covers the real allocation pattern.

### Common failures

Programs share one seeded generator across workers; seed each worker with `seed+worker_id`; change worker count and silently change results; split in task-creation order; reuse streams after retry; overlap jump ranges; truncate logical IDs; use modulo reduction with bias; let rejection sampling shift later draws; rely on unspecified library stability; serialize endianness incorrectly; compare Monte Carlo means while ignoring identical underlying samples; call deterministic output secure; publish sensitive keys as provenance; or treat a statistical test suite as proof that every downstream estimator is unbiased.

### Compact example

Six logical samples use identities `(stage=7,index=0…5)`. Evaluating indices as chunks `[0,1,2]` and `[3,4,5]`, or as three interleaved workers `[0,3]`, `[1,4]`, `[2,5]`, yields the same indexed vector because each value is a pure function of seed, stage, and sample index. A generator owned by each physical worker would generally change the mapping.

### Connections

[Deterministic Parallel Execution](065-deterministic-parallel-execution.md) defines reproducible observations. [Deterministic Schedulers for Testing](066-deterministic-schedulers-for-testing.md) controls schedule choices but should not own product samples. [Parallel Functional Evaluation](068-parallel-functional-evaluation.md) supplies stable logical task identities. [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md) governs aggregation.

## Governing Question

Which generator family, stream-allocation scheme, identity model, distribution algorithm, and provenance record make stochastic parallel results repeatable under the exact changes an experiment claims to tolerate?

“We set the seed” answers only the first initialization question. It says nothing about which logical operation receives each draw after concurrency, branching, rejection, failure, or refactoring.

## Why This Matters

Parallel randomness drives Monte Carlo methods, randomized algorithms, simulation, machine learning, testing, rendering, cryptography, scientific inference, and fault injection. A schedule-dependent draw assignment makes failures hard to replay, checkpoint/restart inconsistent, worker-count comparisons confounded, and research artifacts irreproducible.

Naively serializing one global generator restores a sequence but adds contention and still couples every later draw to control flow. Per-worker generators remove contention but make worker topology semantic. The more durable design attaches randomness to logical work.

Reproducibility is not always the primary goal. Independent production runs may intentionally use fresh entropy; cryptographic protocols require unpredictability; replicated security services must avoid key reuse; statistical studies may require multiple independent seed families. The interface must separate “replay this experiment,” “generate a new independent experiment,” and “generate adversarially secure material.”

## Prerequisites and Retrieval

Retrieve:

- logical task identities from [Deterministic Parallel Execution](065-deterministic-parallel-execution.md);
- immutable configuration snapshots from [Immutable Snapshots and Multi-Version State](067-immutable-snapshots-and-multi-version-state.md);
- task decomposition from [Parallel Functional Evaluation](068-parallel-functional-evaluation.md); and
- numeric aggregation from [Parallel Loops and Reductions](044-parallel-loops-and-reductions.md).

Retrieval prompt: start with a single stateful PRNG and two tasks whose draw counts differ. Show two schedules assigning different draws to the same logical sample, then propose an identity tuple that removes physical scheduling from the mapping.

## Learning Objectives

After completing this module, a learner can:

1. distinguish entropy, seeds, state, streams, substreams, keys, and counters;
2. explain why shared and per-worker sequential generators are decomposition-sensitive;
3. design stable domain-separated logical sample identities;
4. compare counter-based, splittable, leapfrog, block-split, and jump-ahead allocation;
5. preserve rejection sampling, variable draw counts, retry, checkpoint, and nested parallelism;
6. specify distribution and floating conversion for bitwise reproduction;
7. separate statistical quality, scientific validity, and cryptographic security;
8. test stream overlap, correlation, schedule invariance, and provenance replay;
9. manage seed/key material safely across experiments and deployments; and
10. construct higher-assurance review for stochastic parallel systems.

## Core Exposition

### Four independent claims

First, **determinism**: fixed declared inputs produce fixed bits. Every PRNG provides some form of this. Second, **allocation reproducibility**: the same logical sample receives the same bits despite allowed parallel decomposition changes. Third, **statistical quality**: outputs and allocated streams pass justified theoretical and empirical criteria for the application. Fourth, **security**: an adversary cannot predict or reconstruct protected outputs under a threat model.

These claims do not imply each other. A poor linear congruential generator is deterministic. A high-quality stateful generator can be allocated schedule-dependently. A simulation generator can pass demanding batteries but remain predictable from observed state. A secure generator may deliberately refuse cross-run replay unless keys are retained under strict controls.

Scientific validity adds another layer: correct sampling distributions, estimators, convergence diagnostics, bias control, sensitivity analysis, and domain assumptions. Perfectly reproduced wrong samples are still wrong.

### Why one global stream fails

Let a global PRNG emit `r0,r1,r2,…`. Task A needs one draw; task B uses rejection and may need three. If A runs first, A gets r0. If B runs first and consumes r0–r2, A gets r3. A fixed seed reproduces each complete schedule, not the logical mapping across schedules.

A lock makes advancement race-free but not logically deterministic: lock acquisition order selects ownership. Recording draw order can replay one execution but does not make worker-count changes invariant. Preassigning fixed blocks helps only when maximum consumption and branching are bounded and blocks never overlap.

Per-worker state changes which sample uses which stream when work stealing, chunking, scaling, failure, or affinity changes. Worker identities are deployment facts, not stable experiment identities.

### Logical random identities

Define a canonical tuple with a master experiment identity and domain path. For a particle filter this might be `(run, time_step, particle_id, operation=resample, draw_index)`. For randomized testing: `(suite, case_id, generation_stage, shrink_or_mutation_role, attempt)`. Encode fields unambiguously with widths, lengths, endianness, and version.

Domain separation prevents accidental reuse. Drawing initialization noise and dropout with the same `(seed,item,index)` is a collision even if types differ. Include stable tags derived from governed names or assigned constants. Do not use language hash functions whose salt/algorithm can change.

Logical indices must survive retries: a retry that semantically repeats the same attempt reuses identity; a new independent attempt increments an explicit attempt coordinate. Make this a domain decision. Idempotent replay and statistical independence pull in opposite directions if “retry” is undefined.

### Counter-based generators

A counter-based RNG applies a keyed bijective or mixing transformation to a counter block. It has no mutable sequence position: output block k is directly addressable. Parallel tasks can evaluate arbitrary counters independently, vectorize them, and reproduce values after failure without saving prior generator state.

Partition key and counter fields deliberately. A master seed can derive a key; a domain/sample tuple encodes into counter lanes or feeds a specified key-derivation function. Prove capacity: no two requested logical values map to the same effective `(key,counter,lane)` within scope, and no field truncation or wrap occurs.

Philox and Threefry, described by Salmon et al., are established counter-based designs. Do not invent a mixer for production merely because it is deterministic. Use a reviewed implementation with published statistical evidence, exact round count, word size, endianness, and version.

### Splittable generators

A splittable generator returns child generators intended to behave as independent streams. Recursive fork-join computations can carry a generator with each logical subtree. A pedigree or split path determines the child stream.

Splitting in runtime creation order is unstable: a refactoring or scheduler may create children differently. Tie left/right child derivation to the algorithm's stable tree, not physical spawn order. If chunk size changes tree shape, results may change unless identity is defined below that shape or the contract explicitly scopes chunking.

Splittable designs have mathematical and empirical assumptions about stream separation. Record algorithm/version and path depth limits. Repeated splitting is not a generic substitute for a key-derivation function in security-sensitive code.

### Jump-ahead, block splitting, and leapfrogging

Jump-ahead advances a stateful generator by an exact distance. Block splitting assigns worker or logical partition j a block starting at `j·L`; prove each consumes at most L. Leapfrogging assigns every Pth draw to one of P streams. Both can work when P and consumption are fixed, but changing P changes mapping.

For stable logical records, blocks should belong to record/sample IDs rather than workers. Variable rejection counts complicate fixed blocks. Large nonoverlapping formal periods do not alone establish negligible cross-stream correlation for an application.

State serialization supports checkpointing but is generator/version/endianness specific. Jump operations may change across generator variants. Store schema and compatibility checks, never opaque bytes without metadata.

### Executable partition-invariance model

The following pure teaching function maps `(seed,stage,index)` to a small modulus. It demonstrates logical identity and partition invariance only. Its arithmetic is **not** a statistically validated PRNG, distribution sampler, or cryptographic construction.

<!-- bijux-verify: {"id":"logical-random-identity","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"logical=[69, 82, 95, 11, 24, 37]\ntwo_chunks=[69, 82, 95, 11, 24, 37]\nthree_workers=[69, 82, 95, 11, 24, 37]\npartition_invariant=True\ndifferent_stage=[86, 2, 15, 28, 41, 54]\n","stderr":""}} -->
```python
def teaching_value(seed, stage, index):
    return (seed * 31 + stage * 17 + index * 13) % 97


seed = 2026
indices = list(range(6))
logical = [teaching_value(seed, 7, index) for index in indices]

two_chunk_parts = [[0, 1, 2], [3, 4, 5]]
two_chunk_pairs = []
for part in two_chunk_parts:
    for index in part:
        two_chunk_pairs.append((index, teaching_value(seed, 7, index)))
two_chunks = [value for _, value in sorted(two_chunk_pairs)]

worker_parts = [[0, 3], [1, 4], [2, 5]]
worker_pairs = []
for part in worker_parts:
    for index in part:
        worker_pairs.append((index, teaching_value(seed, 7, index)))
three_workers = [value for _, value in sorted(worker_pairs)]

different_stage = [teaching_value(seed, 8, index) for index in indices]

print(f"logical={logical}")
print(f"two_chunks={two_chunks}")
print(f"three_workers={three_workers}")
print(f"partition_invariant={logical == two_chunks == three_workers}")
print(f"different_stage={different_stage}")
```

Stable result ordering here is reconstructed by logical index. The example demonstrates neither randomness nor that stage values are collision-free in a real finite encoding.

### Uniform integers and modulo bias

Mapping a w-bit uniform integer U to `U mod n` is biased unless n divides `2^w`. Some residues receive one extra preimage. Rejection sampling chooses a largest multiple `m=floor(2^w/n)·n`, rejects `U≥m`, and returns `U mod n` otherwise.

In a global stream, rejections shift all later assignments. Give each logical sample a local counter `(sample_id,attempt=0,1,…)`; a rejected candidate advances only that sample. Record the exact conversion algorithm and word interpretation.

Bounded multiplication methods can reduce bias efficiently but are algorithm-specific. Never replace a library sampler while claiming bitwise compatibility merely because both target the same distribution.

### Floating uniforms and distributions

Converting bits to `[0,1)`, `(0,1)`, or `[0,1]` requires a defined number of mantissa bits and arithmetic. Endpoints matter for logarithms and inverse CDFs. Floating contraction, extended precision, GPU math, and library functions can change bits.

Normal, gamma, Poisson, and other samplers use transforms, tables, rejection, branches, and transcendental functions. A stable underlying bit stream does not guarantee stable distributed values across library versions or backends. Record distribution implementation and version; use golden vectors within supported compatibility claims.

Variable draw count belongs to one sample identity. One approach assigns a counter prefix to sample and a suffix to proposal number. Another uses a per-sample child stream. Establish capacity and termination behavior for extreme parameters.

### Nested parallel algorithms

Recursive algorithms need identities independent of steal order. Derive child paths from stable problem structure: tree node ID, array interval, particle ID, graph vertex plus iteration, or deterministic child labels. Avoid sequence numbers allocated by racing tasks.

Adaptive algorithms are harder. If refinement decisions depend on floating reductions or asynchronous convergence, the logical work tree itself may change. First make the decision process deterministic or accept that sample identities differ under the declared configuration.

Randomized load balancing and algorithmic randomness should use distinct domains. Otherwise changing runtime scheduling consumes product randomness. Testing scheduler randomness belongs to test provenance, not the scientific stream.

### Checkpoint, retry, and replay

Counter-based code checkpoints logical progress, input/configuration digest, and master derivation metadata. Recomputed values require no worker-local RNG state. Stateful streams must record each logical stream's algorithm state plus ownership and completed boundaries atomically with application state.

Checkpoint consistency matters: storing generator advancement before a sample result can skip work after crash; storing it after an externally committed result can duplicate. Use transactional checkpoint/commit or idempotent sample identity.

Retry semantics state whether the same failed logical operation receives identical values. Reusing aids exact replay and idempotency. A statistically new trial needs a new attempt identity. Backoff jitter should usually be stable per logical retry attempt, not per process restart, unless operational decorrelation requires otherwise.

### Reproducible aggregation

Stable sample values do not ensure stable final results. Arrival-ordered floating reductions, early stopping, adaptive confidence intervals, and “first success wins” can change with schedules. Use an index-fixed reduction tree, reproducible accumulator, stable tie rules, and deterministic convergence checkpoints when bitwise results are required.

Early stopping can evaluate different sample prefixes under parallel overshoot. Define the accepted prefix by logical index or epoch, not completion. Extra speculative samples remain unobserved and must not affect later identities.

Common random numbers intentionally align identities across compared configurations so sample-wise differences have lower variance. Changing only one method while preserving logical sample keys is useful; accidentally reusing identical streams for quantities assumed independent is not.

### Statistical quality and stream evidence

Generator evaluation combines theoretical structure, known weaknesses, period/state analysis, equidistribution or spectral properties where relevant, application-specific tests, and empirical batteries such as TestU01. No finite battery proves randomness. Passing says no tested statistic detected a problem at configured thresholds.

Test the actual parallel allocation: adjacent counters, related keys, split siblings, deep pedigrees, jump boundaries, interleaved lanes, truncated outputs, and distribution transforms. Many independent p-values also create expected false alarms; interpret them with a predeclared procedure rather than selecting favorable results.

Application validation matters more than generic batteries alone. Compare estimators across multiple independent master seeds and generator families; check convergence, confidence coverage, rare-event sensitivity, and known analytic cases. Preserve failing seeds as regression cases without overfitting to them.

### Security boundary

Simulation PRNGs are generally predictable and unsuitable for tokens, keys, nonces, password salts, or adversarial lotteries. Use an approved CSPRNG and protocol-specific derivation. Deterministic reproducibility may itself be a vulnerability if secrets or future outputs can be recovered.

For secure deterministic derivation, protect a high-entropy master key, use reviewed domain-separated KDF/DRBG constructions, enforce nonce/counter uniqueness, rotate and revoke keys, audit access, and avoid logging secret state. A public experiment seed and a secret production key are different data classifications.

Reusing a key/counter pair in stream-cipher-like constructions can be catastrophic. Availability retry and restore must not roll back nonce state. Security review is mandatory; ordinary PRNG quality evidence is irrelevant to adversarial unpredictability.

### Provenance and compatibility

A reproducibility manifest records generator family, exact implementation/library version, word size, rounds/variant, seed or protected key reference, seed-expansion/KDF, domain schema/version, counter encoding and endianness, stream limits, distribution algorithms/parameters, numeric/backend/toolchain, reduction and stopping rules, input/configuration digests, and result digest.

Compatibility policies vary. Some libraries promise stable core integer streams for a generator but not distributions; defaults can switch algorithms; performance upgrades can change sequences. Pin explicitly and test golden vectors. If migration intentionally changes streams, version the experiment and never label outputs bitwise comparable.

Seeds should be parseable canonical integers/bytes, not platform hashes or decimal floats. Record fresh experiment entropy at creation. Avoid human-small seeds across unrelated studies unless a robust seed-expansion scheme and uniqueness process are used.

### Performance and operations

Counter-based generators vectorize and avoid shared state, but key/counter construction, conversion, distribution transforms, memory writes, and reductions can dominate. Stateful local generators may be faster for sequential chunks but require stable logical allocation. Benchmark the whole stochastic kernel.

Measure generated bits/s, samples/s, CPU/GPU utilization, vector width, distribution rejection rate, branch divergence, memory traffic, task/chunk overhead, checkpoint size/time, retry recomputation, reduction cost, and estimator variance per unit time. Faster biased or correlated output is not an optimization.

Operational monitoring must not expose keys or sensitive seeds. Log experiment IDs, algorithm versions, allowed public seed references, collision/overflow assertions, checkpoint compatibility, and replay digest. Fail closed on unknown schema or counter exhaustion.

### Evidence strategy

Use published test vectors for generator primitives and golden vectors for seed expansion, identity encoding, distribution conversion, and checkpoint recovery. Verify schedule, worker-count, chunk, steal, retry, restart, and backend invariance inside the stated scope. Inject rejection paths and near-capacity counters.

Test uniqueness of encoded domains/counters over generated workloads and property-test serialization round trips. Run statistical batteries on individual and related parallel streams, then application-specific inference tests across independent seeds. Compare with another trusted implementation or generator family.

Separate the report: bitwise replay evidence, allocation/nonoverlap proof, statistical evidence, numeric/reduction evidence, scientific validation, performance, and security review. A single “randomness tests passed” checkbox cannot support these distinct claims.

## Definitions and Notation

- `s`: public experiment seed or protected master-key input.
- `D`: versioned logical domain tuple.
- `c`: logical counter/sample coordinate.
- `G(k,c)`: counter-based output block under key k.
- `KDF(s,D)`: specified derivation of a domain key from seed/key material and D.
- `R(D,c)`: random bits assigned to logical identity `(D,c)`.
- `P`: physical worker count, excluded from R when worker-count invariance is claimed.
- `L`: allocated block/substream length.
- `A`: rejection attempt coordinate owned by one sample.
- `H`: canonical digest of provenance and inputs.

The allocation invariant is `(D,c)≠(D',c') ⇒ effective_input(D,c)≠effective_input(D',c')` within the declared namespace. Statistical independence is a stronger claim not proved by input uniqueness alone.

## Mechanisms, Invariants, or Proof Structure

### Partition-invariance proof

For each logical index i, define value `v_i=F(s,D,i)` without P or schedule. Any partition covering each i exactly once computes the same pair set `{(i,v_i)}`. Canonical ordering by i yields the same vector. This proves allocation determinism, not statistical quality.

### Counter-uniqueness proof

Define an injective bounded encoding from domain fields and sample/attempt/lane coordinates into key/counter inputs. Prove every field range, domain-tag separation, no truncation, and no wrap. If hashing replaces injection, quantify collision assumptions and do not call uniqueness absolute.

### Stateful block proof

Assign logical partition j interval `[jL,(j+1)L)`. Prove partition j consumes fewer than or equal to L generator positions under every branch/rejection/failure path, and intervals do not exceed the period or jump guarantee. Otherwise block splitting is unsound.

### Replay induction

Given equal canonical inputs/provenance, each logical identity encodes identically, generator primitive returns identical bits, distribution conversion returns identical values within platform scope, and stable reduction/decision rules produce identical observations by induction over the algorithmic DAG.

## Alternatives and Trade-Offs

| Approach | Main benefit | Principal limitation |
|---|---|---|
| Locked global PRNG | simple one sequence | contention and schedule-dependent ownership |
| Per-worker seeded PRNG | fast local state | worker/decomposition-sensitive mapping |
| Fixed block splitting | simple with jump-ahead | must bound consumption and allocation |
| Leapfrogging | separated fixed-P streams | changes with P and can hurt locality |
| Splittable PRNG | natural recursive fork-join | pedigree/tree/version stability |
| Counter-based PRNG | random access by logical identity | careful key/counter/domain engineering |
| Logged draw trace | exact replay of one run | volume, sensitivity, no decomposition invariance |
| CSPRNG/KDF | adversarial security when correctly used | key management and often no public replay |

Prefer counter or stable logical splitting for decomposition-invariant simulations. Retain stateful local streams when topology is fixed and their performance advantage is measured, but state that scope honestly.

## Failure Modes and Misconceptions

- **“A fixed seed is reproducible parallelism.”** Draw ownership may still follow scheduling.
- **“A lock fixes it.”** It fixes races, not logical assignment order.
- **“Worker ID is a stream ID.”** Scaling and work stealing change workers.
- **“Seed plus ID is always safe.”** Naive initialization can create related or weak states.
- **“Long period prevents overlap.”** Allocation and correlations still need analysis.
- **“Different counters prove independence.”** They prove distinct inputs, not statistical independence.
- **“Modulo gives a uniform bounded integer.”** It is biased unless divisibility holds.
- **“Stable bits give stable normals.”** Distribution algorithms and floating libraries can change.
- **“Rejection is local detail.”** Global consumption shifts later samples unless attempts are sample-owned.
- **“Retry should always redraw.”** Replay/idempotency may require identical values; define semantics.
- **“More seeds validate a model.”** They test variability, not scientific assumptions by themselves.
- **“TestU01 proves randomness.”** A finite battery detects known statistical defects only.
- **“Simulation PRNGs are secure.”** Predictable state is unacceptable for adversarial uses.
- **“Logging the key aids reproducibility.”** It can compromise every protected output.
- **“Stable samples mean stable result.”** reductions and early stopping may remain schedule-dependent.

## Worked Examples

### Example 1

**Shared stream.** A rejection-heavy task consumes three draws before a one-draw task runs; reversing order changes the latter's value. **Conclusion:** seed fixes sequence, not ownership.

### Example 2

**Logical index.** Two and three worker partitions compute the same six indexed teaching values. **Conclusion:** physical partition can disappear from the mapping.

### Example 3

**Domain collision.** Initialization and dropout both use `(seed,layer,index)` and receive identical bits. Add stable operation tags. **Conclusion:** typed semantic domains need encoded separation.

### Example 4

**Modulo bias.** Eight-bit U modulo 100 gives residues 0–55 three preimages and 56–99 two. Reject U≥200. **Conclusion:** deterministic conversion can still be statistically wrong.

### Example 5

**Rejection locality.** Sample 9 rejects twice using attempts 0,1,2; sample 10 still begins at its own attempt 0. **Conclusion:** variable draw counts need hierarchical coordinates.

### Example 6

**Checkpoint restart.** A counter-based simulation stores completed logical epoch and provenance; restarted workers recompute any incomplete samples identically. **Conclusion:** logical progress outlives worker state.

### Example 7

**Adaptive tree.** A floating convergence decision changes refinement and split pedigree across backends. Stabilize decision epochs or scope backend-specific streams. **Conclusion:** generator allocation cannot repair nondeterministic control structure.

### Example 8

**Common random numbers.** Two queue policies use matching arrival/service sample IDs to estimate their difference with lower variance. **Conclusion:** controlled dependence can be beneficial when intentional.

### Example 9

**Nonce rollback.** Restoring a VM reuses a secure generator counter with the same key. Repetition breaks protocol security. **Conclusion:** reproducible simulation and nonce uniqueness require different designs.

### Example 10

**Clinical trial simulation.** Reproducibility must bind protocol, population model, endpoint, missingness, estimand, generator/streams, distribution transforms, stopping, numeric reduction, independent seeds, provenance, and sensitivity analysis. Named biostatistical, clinical-domain, epidemiology, numerical, RNG, concurrency/runtime, data-governance, security/privacy, quality/regulatory, and independent methodology reviewers must approve the model and evidence; none is claimed here. **Conclusion:** repeatable random bits do not establish clinical validity.

## Cross-Program Connections

- **Algorithms:** randomized choices need stable identities and theoretical probability guarantees.
- **Numerical computing:** distribution conversion, reduction, and stopping govern bitwise output.
- **Scientific computing:** independent replications, variance reduction, and provenance support inference.
- **Distributed systems:** retries, checkpoints, scaling, and failure make worker-local state fragile.
- **Security:** CSPRNGs, KDFs, nonce uniqueness, and key protection form a separate threat-model discipline.
- **Testing:** controlled seeds reproduce failures while distinct campaigns need independence.
- **Data engineering:** schema-versioned identities and manifests make stochastic artifacts auditable.
- **Safety engineering:** higher-stakes stochastic evidence requires domain review beyond generator tests.

## References

1. John K. Salmon, Mark A. Moraes, Ron O. Dror, and David E. Shaw, “Parallel Random Numbers: As Easy as 1, 2, 3,” SC 2011. <https://doi.org/10.1145/2063384.2063405>
2. Guy L. Steele Jr., Doug Lea, and Christine H. Flood, “Fast Splittable Pseudorandom Number Generators,” OOPSLA 2014. <https://doi.org/10.1145/2660193.2660195>
3. Pierre L'Ecuyer, Richard Simard, E. Jack Chen, and W. David Kelton, “An Object-Oriented Random-Number Package with Many Long Streams and Substreams,” *Operations Research* 50(6), 2002. <https://doi.org/10.1287/opre.50.6.1073.358>
4. Pierre L'Ecuyer and Richard Simard, “TestU01: A C Library for Empirical Testing of Random Number Generators,” *ACM TOMS* 33(4), 2007. <https://doi.org/10.1145/1268776.1268777>
5. Makoto Matsumoto and Takuji Nishimura, “Mersenne Twister: A 623-Dimensionally Equidistributed Uniform Pseudo-Random Number Generator,” *ACM TOMACS* 8(1), 1998. <https://doi.org/10.1145/272991.272995>
6. David Blackman and Sebastiano Vigna, “Scrambled Linear Pseudorandom Number Generators,” *ACM TOMS* 47(4), 2021. <https://doi.org/10.1145/3460772>
7. NumPy Developers, *Parallel Random Number Generation*, NumPy 2.5 documentation; retrieved 2026-08-29. <https://numpy.org/doc/stable/reference/random/parallel.html>
8. NumPy Developers, *SeedSequence*, NumPy 2.5 documentation; retrieved 2026-08-29. <https://numpy.org/doc/stable/reference/random/bit_generators/generated/numpy.random.SeedSequence.html>
9. NIST, *Recommendation for Random Number Generation Using Deterministic Random Bit Generators*, SP 800-90A Rev. 1, 2015. <https://doi.org/10.6028/NIST.SP.800-90Ar1>
10. Melissa E. O'Neill, *PCG: A Family of Simple Fast Space-Efficient Statistically Good Algorithms for Random Number Generation*, 2014. <https://www.pcg-random.org/paper.html>

## Exercises

### Exercise 1

Explain schedule dependence for a shared stateful PRNG, then design a versioned logical identity schema for a nested Monte Carlo computation.

### Exercise 2

Compare counter-based, splittable, block-split, and leapfrog allocation under worker-count changes, rejection sampling, retries, and checkpoint/restart.

### Exercise 3

Design an unbiased reproducible sampler for integers `[0,n)` and a variable-draw distribution. Specify counters, capacity, numeric conversion, and error behavior.

### Exercise 4

Create a validation and provenance plan for a CPU/GPU stochastic simulation claiming bitwise replay across worker counts but not across backends.

### Exercise 5

A regulated risk model uses parallel Monte Carlo. Specify statistical, reproducibility, security, operational, and human-review requirements without conflating them.

## Answers to the Exercises

### Answer 1

A shared state emits one sequence, but whichever task acquires it first owns the next value; variable draw counts shift all later ownership. Locking removes a data race only. Define a canonical run ID and tuple `(model_version,scenario_id,outer_replication,algorithmic_stage,logical_entity,inner_sample,proposal_attempt,lane)`. Assign stable domain tags, explicit unsigned widths/lengths/endianness, no language hash, and a schema version. Prove field ranges and injective encoding into counter/key space or quantify a reviewed hash/KDF collision model. Physical worker, thread, chunk, completion, and retry timing are absent. A semantic new retry increments an attempt role; exact replay retains the same tuple. Record generator/derivation/distribution versions and protected seed/key provenance.

### Answer 2

Counter-based mapping gives direct random access and naturally survives workers, rejection, and restart when each sample owns counters. Splittable generators suit stable recursive trees, but tree/refactoring/chunk changes alter pedigrees unless identities are below the split structure. Block splitting works if each logical partition consumes at most L and jump intervals never overlap; variable rejection and retries threaten the bound. Leapfrogging depends directly on P and therefore fails worker-count invariance, though it can serve fixed topology. Stateful split/block/leapfrog checkpoints must atomically store every logical stream state and ownership; counter designs store logical completion and derivation metadata. Statistical quality and cross-stream evidence are required for each actual scheme.

### Answer 3

For a w-bit uniform U and positive n, set `m=floor(2^w/n)·n`. Sample candidates for logical item i at counters `(domain,i,attempt,word_lane)`, incrementing attempt only for i. Reject `U≥m`; otherwise return `U mod n`. Prove counter encoding, attempts, lanes, and maximum workload cannot wrap/collide; define behavior for n=0, n>2^w, and attempt/resource exhaustion. A variable-draw distribution similarly owns a per-sample proposal counter so one rejection never shifts another sample. Specify bit-to-float endpoints/precision, tables/transcendentals, NaN/parameter errors, generator/distribution version, and golden vectors. Use a reviewed sampler rather than the teaching arithmetic.

### Answer 4

Bind source, inputs, master seed record, generator/rounds, derivation and domain schema, counter encoding, distribution versions, CPU backend/toolchain/math settings, reduction tree, and stopping rule. Golden-test primitives, derivation, distributions, checkpoint recovery, and final artifacts. Run identical CPU experiments across schedules, workers, chunks, stealing, retries, cancellation, and restarts; compare indexed sample bits and canonical results. Run counter uniqueness/capacity checks, related-stream batteries, application analytic/convergence tests, and independent seeds/generator families. Treat GPU as a separately versioned backend: validate statistical/scientific equivalence and declared tolerances, not bitwise equality, because floating transforms may differ. Record both manifests and prevent cross-backend cache/result mislabeling. Benchmark throughput, rejection, transfers, reduction, memory, and variance.

### Answer 5

Define model, inputs, estimand, distributions/dependencies, tail behavior, convergence/error targets, seed-family plan, variance reduction, and independent replications. Allocate reviewed streams through stable logical identities and prove capacity/nonoverlap assumptions; pin generator, transforms, numeric reductions, stopping, toolchain, and provenance. Separate public replay seeds from protected production entropy and never use simulation PRNGs for authentication, secrets, or nonces. Check generic batteries plus model-specific analytic cases, sensitivity, confidence coverage, rare events, alternative generators, and independent implementation. Specify checkpoint/retry/idempotency, access control, audit, retention, monitoring, collision/overflow failure, and disaster recovery. Named risk/domain, statistical, actuarial/economic as applicable, RNG/numerical, concurrency/runtime, model-validation, security/privacy, data-governance, operations, quality/regulatory, and independent assurance reviewers must approve intended use, thresholds, limitations, and residual risk. Reproducibility is evidence, not model validity or regulatory approval.
