---
module_id: ALGE-020
program: Algorithm Engineering
level: 1
module_number: 20
title: Engineering a Sort for Real Data Distributions
status: complete
last_verified: 2026-09-04
---

# Engineering a Sort for Real Data Distributions

## One-Page Review

### Governing question

How should an engineer select, compose, measure, and operate a sorting policy for observed data distributions without weakening its order, stability, memory, failure, or worst-case contract?

### Essential definitions

- A **sort contract** declares ordering, identity, stability, mutation, key evaluation, exceptional values, memory, failure, and resource guarantees.
- A **workload family** is a reproducible generator or corpus slice with named size, key, order, duplication, record, and environment properties.
- A **distribution profile** is a vector of measured descriptors such as key span, distinct count, multiplicities, inversions, runs, key width, and record width.
- **Dispatch** chooses an implementation from a portfolio after enforcing hard constraints.
- A **cost vector** counts comparisons, key projections, moved bytes, initialized slots, allocations, cache misses, and other relevant events separately.
- A **calibrated cost model** combines a cost vector with coefficients measured for a specific environment.
- An **uncertainty band** records the estimation error around a sampled descriptor.
- A **decision boundary** is the region where two candidate policies have similar predicted or measured cost.
- **Hysteresis** requires stronger evidence to change a deployed policy than to retain it, reducing oscillation under noise.
- A **deterministic fallback** preserves the promised ceiling when a speculative fast path encounters hostile or misclassified input.

### Central model, mechanism, or theorem

For an algorithm $a$ and input $x$, keep operations visible:

$$
\mathbf v(a,x)
=
(C,P,B,Z,A,Q,\ldots),
$$

where $C$ is comparisons, $P$ key projections, $B$ bytes moved, $Z$ auxiliary slots initialized, $A$ allocations, and $Q$ measured cache misses. A calibrated scalar proxy may be

$$
\widehat T(a,x)
=
c_C C+c_P P+c_B B+c_Z Z+c_A A+c_Q Q+\cdots,
$$

but its coefficients are local measurements, not universal constants.

For $s$ independent uniformly sampled index pairs, let $\widehat q$ estimate the inversion fraction $q$. Hoeffding's inequality gives

$$
\Pr\left(\lvert\widehat q-q\rvert\ge\varepsilon\right)
\le
2e^{-2s\varepsilon^2}.
$$

Thus, with failure probability at most $\delta$,

$$
\varepsilon
=
\sqrt{\frac{\ln(2/\delta)}{2s}}.
$$

This bound applies to that sampling model; it does not justify arbitrary clustered, dependent, or adaptive sampling.

### Critical invariants

- Contract requirements eliminate infeasible algorithms before performance scoring.
- Every candidate implements the same ordering and key snapshot used by its fallback.
- Profiles are computed without unchecked range arithmetic, unbounded allocation, or comparator side effects.
- Every reported descriptor states whether it is exact, sampled, estimated, or observed after preprocessing.
- Dispatch thresholds name their workload, machine, build, data type, and policy version.
- A sampled decision incorporates confidence and has a conservative uncertainty region.
- Portfolio members preserve ordered identity permutation; stable members preserve equivalent source order.
- Counting and radix candidates include range/table initialization, buffers, and checked size arithmetic.
- Indirect sorting includes later gather or materialization cost when the consumer requires it.
- Production rollout retains a known-safe policy, bounded telemetry, canary comparison, and rollback.

### Common failures

Common failures include selecting by $n$ alone; assuming uniformly random distinct keys; calling $\Theta(n+K)$ counting work linear in $n$; allocating from untrusted key extrema; treating entropy as elapsed time; estimating inversions from adjacent pairs; branching on a noisy point estimate at a sharp threshold; benchmarking only the winning algorithm; excluding preprocessing, allocation, or gather cost; changing comparator or NaN semantics across fallback; tuning on one warm-cache machine; publishing only averages; learning synchronously from tenant traffic without limits; and removing the deterministic fallback after ordinary cases look fast.

### Compact example

Six stable records have keys $(3,1,3,0,2,1)$. Their span is $K=4$, distinct count is $u=4$, duplicate excess is $2$, and there are four maximal nondecreasing runs. A teaching policy whose integer-table guard is $K\le\max(16,2n)$ chooses stable counting. The output identity order is

$$
(D,B,F,E,A,C),
$$

so equal-key identities $B,F$ and $A,C$ retain source order. The choice is defensible only with the stated memory guard and contract; it is not a universal threshold.

### Connections

[ALGE-013](./013-merge-sort.md) supplies stable merging, [ALGE-014](./014-quicksort-and-partitioning.md) supplies robust partitioning, [ALGE-016](./016-counting-radix-and-bucket-sorting.md) supplies distribution sorting, [ALGE-018](./018-stable-sorting-and-indirect-sorting.md) supplies identity and movement contracts, and [ALGE-019](./019-adaptive-and-hybrid-sorting.md) supplies run adaptation and bounded hybrid fallback.

## Governing Question

How can a team engineer one sorting service for dense integers, sparse identifiers, duplicate-heavy categories, existing runs, expensive keys, wide records, memory ceilings, and hostile callers without turning a benchmark winner into an unsupported universal rule?

The answer is a versioned policy, not a favorite algorithm. First specify what outputs and failures mean. Then describe workloads with measurements that discriminate among feasible mechanisms. Retain multidimensional costs long enough to expose why a result changes. Validate every member and every handoff. Finally, tune and deploy the policy with evidence that includes uncertainty, tails, and rollback.

The word “distribution” here is broad. It includes the statistical distribution of keys, their order in the input, duplicate multiplicities, record and key representation, request sizes, consumer behavior, and deployment environment. A list of uniformly random integers is one family, not the definition of real data.

## Why This Matters

Sorting is often infrastructure hidden behind a small API. A query engine may sort narrow row handles and gather wide columns later. A user interface may repeatedly sort an almost ordered list. A compiler may sort interned identifiers. A service may accept public keys chosen to exhaust comparisons or memory. The same asymptotic label can conceal radically different projection, movement, allocation, cache, and tail costs.

A comparison sort remains broadly applicable, while a distribution sort can win decisively when key representation and range permit it. Natural merging can exploit existing runs. Three-way partitioning can exploit duplicates without stability. Indirection can spare movement of wide records but burden the next consumer. No single descriptor selects among all these cases.

Poor engineering also creates correctness failures. A fast path may compare normalized keys while its fallback compares raw values. A table size computed as $\max-\min+1$ may overflow before a memory check. An unstable path may accidentally serve a stable request. An online tuner may switch algorithms at a noisy boundary and cause latency oscillation. These are system defects, not small constant-factor mistakes.

## Prerequisites and Retrieval

Retrieve:

- strict weak ordering, equivalence classes, totalization, identity permutation, and stability;
- comparison lower bounds and decision trees;
- stable merge, three-way partition, heap fallback, insertion cutoffs, and natural runs;
- counting, radix, and bucket sorting with range, digit, and occupancy costs;
- direct and indirect sorting, cached keys, and downstream materialization;
- inversions, multiplicity entropy, sampling, confidence bounds, and paired experiments;
- checked integer arithmetic, bounded allocation, cancellation, callbacks, and failure atomicity;
- cache hierarchy, branches, bandwidth, NUMA, accelerators, external memory, and concurrency;
- reproducible benchmarks, workload stratification, telemetry, canaries, and rollback.

You should be able to prove an ordered identity permutation, distinguish a theorem from a measured claim, and explain why two $O(n\log n)$ implementations can exchange rank across workloads.

## Learning Objectives

After completing this module, you should be able to:

1. write a complete sort contract before selecting an implementation;
2. characterize a workload with size, key, order, duplication, representation, and consumer descriptors;
3. derive comparison, counting, radix, merge, and indirection cost proxies without hiding required terms;
4. use exact scans and statistically bounded samples appropriately;
5. construct a constraint-first portfolio dispatcher with a deterministic fallback;
6. explain when key caching, direct movement, indirection, and materialization change the decision;
7. design stratified benchmarks that measure full-path distributions and tails;
8. validate algorithms, dispatch boundaries, resource ceilings, and adversarial behavior;
9. version, canary, observe, and roll back a production policy;
10. defend a sorting choice with proof obligations, measurements, uncertainty, and stated limitations.

## Core Exposition

### Freeze the contract before profiling

Begin with the observable contract. Specify:

- the ordering relation and whether it is ascending, descending, lexicographic, locale-aware, or application-defined;
- treatment of nulls, NaNs, signed zero, invalid encodings, and incomparable values;
- whether equivalent records must be stable;
- whether output is an in-place permutation, a new sequence, an index permutation, or grouped buckets;
- whether keys are evaluated once, may be reevaluated, or can observe mutation;
- accepted sizes and representations;
- auxiliary-memory, stack, wall-time, cancellation, and concurrency limits;
- behavior when comparison, key projection, allocation, or cancellation fails;
- whether partial mutation is allowed before an error is returned.

These requirements are hard constraints. A stable request cannot enter an unstable quicksort merely because sampling predicts a favorable distribution. A no-allocation request cannot enter an $O(n)$-buffer merge. A deterministic worst-case service cannot rely on randomized sampling without retaining the promised fallback.

Define comparator equivalence by

$$
x\sim y
\quad\Longleftrightarrow\quad
\neg(x\prec y)\land\neg(y\prec x).
$$

Every accepted result must be ordered and contain each input identity exactly once. Stable mode additionally preserves source order within each $\sim$ class. These properties apply across dispatch and fallback boundaries, not only within each algorithm in isolation.

### Describe the workload as a vector

For input $x$ with $n$ records, useful descriptors include:

- key representation, width $w_k$, and projection cost;
- record width $w_r$ and whether movement is trivial, reference-counted, or exception-prone;
- integer span $K=\max k-\min k+1$ when safely representable;
- distinct count $u$ and multiplicities $n_1,\ldots,n_u$;
- maximum multiplicity $m_{\max}$ and duplicate excess $n-u$;
- multiplicity entropy $H$;
- inversion count $I$ or inversion fraction $q$;
- number $\rho$ and lengths of natural runs;
- common prefixes for strings or digits;
- skew, heavy hitters, missing values, and exceptional-value rate;
- original location, partitioning, storage medium, and next consumer.

The multiplicity probabilities $p_i=n_i/n$ give

$$
H=\sum_{i=1}^{u}p_i\log_2\frac1{p_i}.
$$

For distinguishable identities whose order matters only across key classes, the exact number of class-label sequences is

$$
\frac{n!}{\prod_{i=1}^{u}n_i!}.
$$

The method-of-types bounds give the precise information-scale statement

$$
nH-u\log_2(n+1)
\le
\log_2\frac{n!}{\prod_{i=1}^{u}n_i!}
\le
nH.
$$

This explains why duplicates can reduce necessary comparison information without claiming exact equality to $nH$. It does not, by itself, predict branches, movement, allocation, or elapsed time.

Order descriptors are not interchangeable. Under the declared strict relation, normalize the inversion fraction as

$$
q=\frac{I}{\binom n2}
$$

when $n\ge2$. Adjacent descents can count natural-run boundaries cheaply, but they do not estimate all pair inversions. A rotated sorted array can have two runs and many inversions. Preserve each descriptor's meaning.

### Separate exact scans from samples

Some facts are already cheap to compute during an unavoidable pass. Exact minimum, maximum, simple type checks, and adjacent descents need $O(n)$ operations. Exact distinct count may require a set with $O(u)$ storage. Exact inversion count normally costs more than a linear scan.

Profiling itself consumes time, memory, comparisons, and possibly key callbacks. Fuse safe descriptors into key materialization or validation when possible. Stop collecting a feature when its maximum possible decision value is below its cost. Do not perform an expensive profile merely to rediscover what the selected algorithm would learn naturally.

Sampling can reduce profiling cost, but every sampling claim needs a population, estimator, and error model. If $s$ index pairs are drawn independently and uniformly from all $i<j$, define indicator $X_t=1$ when pair $t$ is inverted. Then

$$
\widehat q=\frac1s\sum_{t=1}^{s}X_t
$$

is an unbiased estimate of pair inversion fraction under fixed input, and Hoeffding gives

$$
\Pr\left(\lvert\widehat q-q\rvert\ge\varepsilon\right)
\le2e^{-2s\varepsilon^2}.
$$

Solving for an error bound at confidence $1-\delta$ yields

$$
\varepsilon=\sqrt{\frac{\ln(2/\delta)}{2s}}.
$$

Sampling adjacent pairs instead estimates descent rate, not $q$. Sampling one clustered region can miss global structure. Sampling without replacement has a related but different analysis. If an adversary can infer sample positions, preserve a deterministic ceiling regardless of the estimate.

### Keep a vector cost model

For each candidate algorithm $a$, record a vector rather than only “operations”:

$$
\mathbf v(a,x)=(C,P,B,Z,A,Q,R,S,\ldots),
$$

where, for example:

- $C$ counts comparisons;
- $P$ counts key projections;
- $B$ counts bytes copied or moved;
- $Z$ counts initialized table or buffer slots;
- $A$ counts allocations;
- $Q$ counts cache misses measured by a declared counter;
- $R$ counts branch mispredictions;
- $S$ records peak auxiliary bytes or stack depth.

The vector prevents one workload's cheap operation from being mistaken for another's expensive operation. If business decisions require one score, calibrate coefficients on the target environment:

$$
\widehat T(a,x)=\sum_j c_jv_j(a,x).
$$

Coefficients may depend on size, cache state, concurrency, runtime, compiler, CPU, allocator, and data type. Interaction effects mean a linear model can be imperfect. Retain raw counters and measured wall-time distributions even when a model fits ordinary observations.

Use the model for explanation and candidate pruning, then confirm decisions with end-to-end measurements. Never relabel fitted coefficients as machine-independent complexity constants.

### Compare portfolio cost shapes honestly

A comparison sort has a generic comparison scale of $O(n\log n)$, but duplicates, runs, pivot shape, and key costs can change its actual vector. Stable merge usually writes $O(n\log n)$ record or reference units across levels. Introspective partitioning retains a deterministic $O(n\log n)$ comparison-style ceiling when its heap fallback is correctly enforced.

Stable counting over integer span $K$ has

$$
T(n,K)=\Theta(n+K),
\qquad
S(n,K)=\Theta(n+K)
$$

for the conventional output-buffer implementation. Its memory guard must include at least counter storage and output storage. If counters use $b_c$ bytes and output records or references use $b_o$ bytes, a first proxy is

$$
M_{\mathrm{count}}=Kb_c+nb_o+M_{\mathrm{overhead}}.
$$

Compute $K$ with widened or checked arithmetic before allocation. A huge sparse range makes the $K$ terms decisive.

An LSD radix sort over a fixed $W$-bit key with digit width $r$ uses

$$
d=\left\lceil\frac Wr\right\rceil
$$

passes. A coarse operation proxy is

$$
d\left(n+2^r\right),
$$

plus output buffers, digit extraction, table clearing, and full-record or reference movement. Larger digits reduce passes but enlarge tables and can damage locality.

Comparison-based stable sorting with multiplicities can exploit equivalence, while three-way partitioning can finish equal regions efficiently in unstable mode. Run-adaptive stable merging may approach linear work when $\rho$ is small. These benefits require the corresponding implementation and proof; a generic $O(n\log n)$ label does not confer them automatically.

### Treat key work as a first-class decision

If key projection costs $t_k$ and a comparison sort invokes it repeatedly, projection can dominate. Materializing exactly one key per record changes the vector from potentially repeated projections to

$$
P=n
$$

plus key storage and movement. The snapshot also prevents a mutable or nondeterministic key callback from changing meaning between fast path and fallback.

Caching introduces obligations:

- define when projection occurs and in what source order;
- retain the record-key association through every permutation;
- handle projection failure before publication according to the mutation contract;
- bound key bytes and release them on all exits;
- ensure every portfolio member compares the cached representation identically.

Decorating records with $(key,source\_index)$ can impose stable tie-breaking even through an otherwise unstable mechanism, but it increases key width and comparisons. It is a deliberate transformation, not “free stability.”

### Decide between direct and indirect movement

Direct sorting moves records. Indirect sorting permutes indices or references and may later gather records. A movement proxy for $m$ moved units is

$$
B_{\mathrm{direct}}\approx mw_r,
\qquad
B_{\mathrm{indirect}}\approx mw_i+B_{\mathrm{gather}},
$$

where $w_i$ is index width. If the next operator accepts an index order, the gather term may disappear. If it requires contiguous records, gather traffic and random access must be measured.

Indirect sorting can improve cache behavior for wide records and expensive moves. It also consumes index storage, changes locality for later consumers, and may extend object lifetimes. Include the complete pipeline rather than ending the benchmark at the permutation vector.

### Build a constraint-first dispatcher

A defensible dispatch sequence is:

1. validate size, comparator/key policy, and exceptional values;
2. materialize or freeze keys if the contract requires it;
3. eliminate candidates that violate stability, mutation, memory, representation, or worst-case constraints;
4. collect exact descriptors that can be fused into existing passes;
5. sample only descriptors whose expected decision value exceeds their cost;
6. attach uncertainty to sampled estimates;
7. predict or measure feasible candidates with a versioned policy;
8. use a conservative default near decision boundaries;
9. retain a deterministic bounded fallback and identical comparison semantics;
10. emit bounded telemetry explaining the chosen path.

One policy might admit stable counting only for safely ranged integers whose table and output fit a budget; select natural merge for sufficiently run-rich stable requests; select index sorting for wide records when the consumer accepts a permutation; and otherwise use a reviewed stable merge or introspective comparison fallback. The exact boundaries are environment-specific.

Use an uncertainty interval, not just a point estimate. If candidate $A$ is preferred only when $q<\tau$ and sampling yields $\widehat q\pm\varepsilon$ crossing $\tau$, choose the conservative default, collect more samples within a fixed budget, or run a bounded pilot. Do not claim the estimate establishes which candidate is faster.

### Preserve a deterministic safety envelope

Classification can be wrong. A distribution can change after sampling only if the input or keys are mutable, which the contract should prevent; nevertheless, finite samples can miss structure. An adaptive fast path can encounter an adversarial case. A performance model can drift after a deployment change.

Therefore preserve invariants independent of policy accuracy:

- checked arithmetic precedes every range-derived allocation;
- all allocations respect request and process budgets;
- recursion or explicit work stacks have proven bounds;
- partition work has a depth or bad-progress budget and heap fallback;
- run stacks have capacity and progress proofs;
- callbacks, cancellation, and time budgets are enforced at defined points;
- a partial in-place permutation is never described as atomic rollback;
- private-copy publication is used when failure atomicity is required.

An estimator can improve ordinary path selection. It must not be the sole protection against catastrophic resource behavior.

### Preserve an executable policy trace

The following teaching implementation profiles three small inputs, applies explicit stable dispatch rules, and verifies ordered identity permutation and stability. Its constants demonstrate auditable structure; they are not production recommendations.

<!-- bijux-verify: {"id":"real-distribution-sort-policy","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"dense metrics=(6, 4, 2, 4, 4) policy=stable_counting labels=('D', 'B', 'F', 'E', 'A', 'C')\nsparse metrics=(4, 4, 0, 1000000001, 2) policy=stable_comparison labels=('A', 'C', 'D', 'B')\nrun_rich metrics=(6, 5, 1, None, 2) policy=stable_natural_merge labels=('A', 'B', 'D', 'E', 'C', 'F')\ncontracts=True\n","stderr":""}} -->
~~~python
from collections import Counter


def profile(records):
    keys = tuple(record[0] for record in records)
    size = len(keys)
    distinct = len(set(keys))
    duplicate_excess = size - distinct
    all_integers = all(isinstance(key, int) for key in keys)
    span = max(keys) - min(keys) + 1 if keys and all_integers else None
    runs = 0 if not keys else 1 + sum(
        keys[index] < keys[index - 1] for index in range(1, size)
    )
    return size, distinct, duplicate_excess, span, runs


def stable_counting_sort(records):
    if not records:
        return ()
    minimum = min(record[0] for record in records)
    maximum = max(record[0] for record in records)
    counts = [0] * (maximum - minimum + 1)
    for key, _ in records:
        counts[key - minimum] += 1
    next_position = []
    total = 0
    for count in counts:
        next_position.append(total)
        total += count
    output = [None] * len(records)
    for record in records:
        slot = record[0] - minimum
        output[next_position[slot]] = record
        next_position[slot] += 1
    return tuple(output)


def stable_merge(left, right):
    output = []
    left_index = 0
    right_index = 0
    while left_index < len(left) and right_index < len(right):
        if right[right_index][0] < left[left_index][0]:
            output.append(right[right_index])
            right_index += 1
        else:
            output.append(left[left_index])
            left_index += 1
    output.extend(left[left_index:])
    output.extend(right[right_index:])
    return tuple(output)


def stable_natural_merge_sort(records):
    runs = []
    start = 0
    while start < len(records):
        end = start + 1
        while end < len(records) and not records[end][0] < records[end - 1][0]:
            end += 1
        runs.append(tuple(records[start:end]))
        start = end
    while len(runs) > 1:
        merged = []
        for index in range(0, len(runs), 2):
            if index + 1 == len(runs):
                merged.append(runs[index])
            else:
                merged.append(stable_merge(runs[index], runs[index + 1]))
        runs = merged
    return runs[0] if runs else ()


def engineered_sort(records):
    metrics = profile(records)
    size, _, _, span, runs = metrics
    if span is not None and span <= max(16, 2 * size):
        policy = "stable_counting"
        output = stable_counting_sort(records)
    elif size >= 6 and runs <= 2:
        policy = "stable_natural_merge"
        output = stable_natural_merge_sort(records)
    else:
        policy = "stable_comparison"
        output = tuple(sorted(records, key=lambda record: record[0]))
    return output, metrics, policy


def contract_holds(source, output):
    positions = {record[1]: index for index, record in enumerate(output)}
    ordered = all(
        output[index][0] <= output[index + 1][0]
        for index in range(len(output) - 1)
    )
    stable = all(
        positions[source[left][1]] < positions[source[right][1]]
        for left in range(len(source))
        for right in range(left + 1, len(source))
        if source[left][0] == source[right][0]
    )
    return ordered and stable and Counter(source) == Counter(output)


workloads = {
    "dense": ((3, "A"), (1, "B"), (3, "C"), (0, "D"), (2, "E"), (1, "F")),
    "sparse": ((0, "A"), (1_000_000_000, "B"), (2, "C"), (999_999_999, "D")),
    "run_rich": (("a", "A"), ("b", "B"), ("d", "C"), ("c", "D"), ("c", "E"), ("e", "F")),
}

checks = []
for name, records in workloads.items():
    result, metrics, policy = engineered_sort(records)
    labels = tuple(record[1] for record in result)
    checks.append(contract_holds(records, result))
    print(f"{name} metrics={metrics} policy={policy} labels={labels}")
print(f"contracts={all(checks)}")
~~~

This trace covers finite examples and three portfolio paths. It does not validate unchecked-language arithmetic, allocation failure, arbitrary comparators, parallel execution, external memory, or the displayed thresholds on production workloads.

### Benchmark families rather than anecdotes

Construct a factorial or stratified workload matrix. Include:

- sizes below, at, and above every cutoff and cache boundary;
- integer spans from dense to sparse, including negative and extreme values;
- distinct, all-equal, low-cardinality, Zipf-like, and heavy-hitter keys;
- ordered, reverse, rotated, run-rich, locally perturbed, organ-pipe, sawtooth, and randomized order;
- cheap and expensive key functions;
- narrow references and wide records;
- stable and unstable contracts;
- direct-output and permutation-consuming pipelines;
- warm and cold data, isolated and contended execution;
- honest production corpora with privacy and sampling controls;
- adversarial patterns designed for the actual pivot, table, and run policies.

Randomize candidate execution order, separate setup from included full-path cost explicitly, and repeat enough to report distributions. Use paired trials when algorithms see equivalent generated inputs under the same environmental block. Record raw observations, generation seed, corpus version, policy version, CPU, topology, memory, operating system, runtime/compiler, allocator, flags, and load.

Report median and tail latency, dispersion or confidence intervals, peak memory, comparisons, key calls, bytes moved, allocations, fallback rate, and chosen-path rate. Means alone can hide rare catastrophic paths. Minimum time alone often measures luck.

### Fit, validate, and challenge the decision policy

Partition evidence into tuning and evaluation data. If the same cases choose thresholds and report victory, the estimate is optimistically biased. Cross-validation across workload strata can expose overfitting, while a held-out corpus tests the final policy.

Compare against simple baselines:

- one robust stable comparison sort;
- one robust unstable introspective sort where allowed;
- the existing deployed policy;
- an oracle that selects the fastest observed candidate after the fact.

The oracle is unattainable online but measures available headroom. If a complicated classifier barely improves over a simple guarded rule, prefer the auditable rule. Include profiling overhead and misclassification regret:

$$
R(x)=T(\widehat a(x),x)-\min_{a\in\mathcal F(x)}T(a,x),
$$

where $\mathcal F(x)$ is the feasible set under the hard contract. Measure regret distributions, not only selection accuracy, because choosing the second-best close candidate matters less than rare catastrophic choices.

Probe boundaries directly. Sweep both sides of table-density, run-count, record-width, and size thresholds. Add perturbations smaller than measurement noise. Apply hysteresis or a conservative region if repeated trials alternate choices.

### Design for parallel, external, and accelerator contexts

Parallel sorting changes the vector. Include task creation, synchronization, partition skew, false sharing, NUMA placement, merge bandwidth, worker availability, and deterministic output. A sequentially fast candidate may scale poorly; a higher-work candidate may parallelize predictably.

External sorting includes run formation, block I/O, merge fan-in, file descriptors, compression, spill space, checksums, restart, and cleanup. Key distribution influences partition skew, but device throughput and write amplification can dominate comparisons. Preserve stable tie-breaking across run files when promised.

Accelerators add transfer, kernel launch, device memory, digit-table, synchronization, and fallback costs. Benchmark the complete host-to-result path unless data already reside on the device under the production pipeline. A kernel-only result cannot justify service dispatch.

In every context, the selected candidate must preserve the same logical contract. Physical nondeterminism in task scheduling must not reorder equivalent records in stable mode.

### Operate the policy as versioned software

Give every deployed policy a durable version tied to code, thresholds, feature definitions, and model coefficients. Emit bounded metrics such as:

- request size and coarse approved workload bucket;
- chosen candidate and reason code;
- profile cost and sampled uncertainty;
- comparisons, projections, bytes, allocations, and peak memory when available;
- depth/run-stack maxima and fallback events;
- cancellation, timeout, allocation, comparator, and validation failures;
- p50, p95, p99, and maximum observed full-path time.

Avoid logging raw sensitive keys. Cardinality sketches and buckets still require privacy review and resource bounds.

Canary a new policy on a controlled fraction, shadow it only when duplicate work is safe and budgeted, and compare contract fingerprints or outputs on sampled requests. Define rollback triggers before rollout. Retain the old safe policy until the new one meets correctness, memory, and tail criteria across the agreed observation window.

Distribution drift is expected. Detect it with descriptor and path-rate changes, then rerun the versioned benchmark suite. Do not let an unconstrained online learner modify production thresholds directly from noisy tenant requests.

## Definitions and Notation

- $n$: number of input records.
- $k_i$: frozen key of source identity $i$.
- $w_k$: physical key width or retained key bytes.
- $w_r$: record width or movement payload.
- $w_i$: index or reference width used by an indirect sort.
- $K$: checked inclusive integer span, $\max k-\min k+1$.
- $u$: number of distinct equivalence classes or keys under the declared policy.
- $n_i$: multiplicity of class $i$, with $\sum_i n_i=n$.
- $p_i=n_i/n$: empirical multiplicity probability for nonempty input.
- $H=\sum_i p_i\log_2(1/p_i)$: multiplicity entropy in bits per identity.
- $I$: number of inverted index pairs under a consistent strict relation.
- $q=I/\binom n2$: inversion fraction for $n\ge2$.
- $\rho$: number of normalized natural runs.
- $C,P,B,Z,A,Q,R,S$: comparisons, projections, moved bytes, initialized slots, allocations, cache misses, branch misses, and space/stack measurements.
- $\mathbf v(a,x)$: cost vector for algorithm $a$ on input $x$.
- $\widehat T(a,x)$: calibrated cost prediction, distinguished from observed $T(a,x)$.
- $s$: number of sampled pairs.
- $\widehat q$: sampled inversion-fraction estimate.
- $\varepsilon$: absolute estimation-error radius.
- $\delta$: upper bound on the stated sampling failure probability.
- $\mathcal F(x)$: candidates feasible under the input's hard contract and resource constraints.
- $R(x)$: measured dispatch regret relative to the fastest feasible observed candidate.

“Exact” means computed over the defined complete input. “Estimated” means accompanied by its estimator and uncertainty assumptions. “Observed” means measured in a named finite environment. “Bounded” means supported by a mathematical or enforced resource argument, not merely absent from tests.

## Mechanisms, Invariants, or Proof Structure

The engineered system has five proof layers.

1. **Contract layer.** Validate or freeze comparator, keys, range, exceptional values, stability, output form, and failure semantics. Establish that each source identity has one immutable sorting key for the operation.
2. **Feasibility layer.** Eliminate candidates whose stability, storage, mutation, representation, parallelism, or worst-case properties violate hard requirements. Check derived sizes before allocating.
3. **Profile layer.** Compute exact descriptors and bounded estimates without mutating the identity association. Record definitions, costs, and uncertainty.
4. **Dispatch layer.** Select only from the feasible set. Near an uncertain boundary, use a conservative candidate or a bounded refinement. Attach a reason and policy version.
5. **Execution layer.** Maintain the chosen algorithm's invariants and invoke a contract-equivalent deterministic fallback when its progress budget requires it. Validate publication and release resources on every exit.

For ordered identity permutation, prove that preprocessing creates one decorated item per source identity, internal steps only permute or stably bucket those items, and publication removes decoration without dropping or duplicating identities. For stability, prove that equivalent identities never cross: stable counting places records in source order, stable merge chooses left on equivalence, and decorated unstable sorting uses source index as a final tie-break when that contract is selected.

For range safety, compute extrema in the key type, convert to a widened nonnegative representation, check subtraction and addition, then check multiplication and total allocation against the budget. Only after those proofs allocate $K$ counters and $n$ output slots. Reject or dispatch elsewhere on failure.

For sampled dispatch, state the random experiment. Under independent uniform pair samples, derive the Hoeffding interval. If the interval lies wholly on one side of a validated threshold and all other requirements hold, the rule may choose that side. If it intersects the boundary, the rule must not pretend certainty: default, refine within budget, or compare bounded pilots.

For introspective fallback, show that every partition consumes depth or bad-progress budget, that exhaustion sorts exactly the unresolved range with the same frozen keys, and that disjoint unresolved ranges have total size at most $n$. For natural merge, prove run coverage, stable normalization, adjacent stable merge, stack capacity, progress, and final collapse.

For policy validation, separate:

- **logical evidence:** order, identity, stability, comparator agreement, and failure behavior;
- **resource evidence:** overflow checks, allocations, stack/depth, cancellation, and adversarial ceilings;
- **statistical evidence:** estimator calibration, interval coverage under its model, paired trials, uncertainty, and held-out evaluation;
- **physical evidence:** elapsed distributions and counters on named environments;
- **operational evidence:** canary comparisons, bounded telemetry, drift alerts, and rollback rehearsal.

No layer can substitute for another. A benchmark does not prove permutation correctness. A worst-case proof does not predict cache performance. A confidence interval under uniform sampling does not protect an unbounded allocation.

## Alternatives and Trade-Offs

- **Single robust stable comparison sort:** simplest policy and strongest auditability; may leave dense-key, run-rich, or wide-record performance unused.
- **Introspective unstable comparison sort:** strong general fallback and in-place options; cannot serve native stability without decoration or another mechanism.
- **Natural stable merge:** exploits runs and gives predictable stability; needs auxiliary storage or complex in-place merging and a sound run policy.
- **Stable counting:** excellent for safely dense integral ranges; pays $K$ initialization and table memory and needs stable output storage.
- **LSD radix:** predictable fixed-digit passes and stability by pass; requires key encoding, buffers, digit tuning, and care with signed or variable-length keys.
- **MSD radix or trie-like partitioning:** can skip irrelevant suffixes and support strings; recursion, skew, prefix handling, and cache behavior complicate it.
- **Direct sorting:** simple final layout and sequential consumption; wide or nontrivially movable records increase byte and semantic costs.
- **Indirect sorting:** reduces sort-time movement and can publish a permutation; adds index storage and potentially expensive downstream gather.
- **Exact profiling:** deterministic descriptors and easy audit; can duplicate full-pass work or allocate large sets.
- **Sampled profiling:** bounded overhead for some features; introduces estimation error, model assumptions, seeds, and adversarial visibility.
- **Rule-based dispatch:** inspectable and easy to roll back; interactions and drifting environments can outgrow simple thresholds.
- **Fitted model dispatch:** can represent multiple features and costs; needs held-out validation, drift controls, explainability, and a safety envelope.
- **Offline tuning:** reproducible and isolated; may lag production change.
- **Online adaptation:** responds to drift; risks feedback, exploration cost, nondeterminism, tenant interference, and unsafe threshold changes.
- **Sequential CPU execution:** low setup and deterministic resource reasoning; may miss large-input parallelism.
- **Parallel, external, or accelerator paths:** can exploit scale and specialized hardware; add transfer, coordination, skew, and failure surfaces that full-path measurements must include.

## Failure Modes and Misconceptions

1. **Size-only dispatch:** $n$ hides key span, order, duplicates, record width, and consumer needs.
2. **Random-distinct monoculture:** the benchmark suite omits common and hostile distributions.
3. **Contract-after-algorithm:** stability or failure semantics are retrofitted inconsistently.
4. **Comparator drift:** fast path, fallback, and validation use different totalization rules.
5. **Repeated mutable keys:** callbacks observe changing state during one sort.
6. **Unchecked span:** $\max-\min+1$ overflows before the allocation guard.
7. **Counting-is-linear shorthand:** the $K$ initialization and storage terms disappear from the claim.
8. **Radix pass fantasy:** digit table, buffers, extraction, sign mapping, and cache costs are omitted.
9. **Entropy-as-time:** information scale is presented as a hardware prediction.
10. **Adjacent-as-inversion sample:** descent rate is mislabeled as pair inversion fraction.
11. **Dependent-sample confidence:** Hoeffding is quoted after clustered or adaptive sampling without a matching model.
12. **Point-estimate cliff:** tiny noise around a threshold flips the chosen algorithm.
13. **Profile-for-free:** scanning, hashing, key projection, and sampling costs are excluded.
14. **Winner-only timing:** baselines, failed candidates, raw trials, and uncertainty vanish.
15. **Mean-only reporting:** fallback spikes and memory tails are hidden.
16. **Warm-cache assumption:** a laboratory steady state is generalized to service arrivals.
17. **Kernel-only acceleration:** transfer and synchronization are outside the measured interval.
18. **Indirect-sort truncation:** downstream gather and locality costs are ignored.
19. **Wide-record unit moves:** moving 512 bytes is counted like moving an eight-byte index.
20. **Fallback semantic mismatch:** emergency sorting changes stability, key snapshot, or exceptional-value order.
21. **Sampling as protection:** a probabilistic classifier replaces deterministic resource guards.
22. **Unbounded telemetry:** high-cardinality keys or raw customer data create cost and privacy hazards.
23. **Self-tuning feedback:** production exploration changes latency and trains on its own interventions.
24. **Train-test reuse:** thresholds are praised on the same cases that selected them.
25. **Versionless evidence:** results cannot identify code, model, machine, or corpus.
26. **Rollback optimism:** the old safe policy or compatible state is removed before observation completes.

## Worked Examples

### Example 1

**Question:** Profile keys $(3,1,3,0,2,1)$ for a stable integer sort.

**Reasoning:** Here $n=6$, extrema are $0$ and $3$, so $K=4$. Distinct keys are $\{0,1,2,3\}$, hence $u=4$ and duplicate excess is $n-u=2$. Descents occur at $3\to1$, $3\to0$, and $2\to1$, producing four maximal nondecreasing runs.

**Conclusion:** Stable counting is feasible under the teaching guard $K\le\max(16,2n)$, but the real decision must also check counter/output bytes and contract requirements.

### Example 2

**Question:** Why is counting sort unsuitable for one million 64-bit records whose observed nonnegative keys span all $2^{32}$ values?

**Reasoning:** With eight-byte counters alone,

$$
2^{32}\cdot8=2^{35}\text{ bytes}=32\text{ GiB}.
$$

This excludes output storage and overhead. The time is $\Theta(n+2^{32})$, not $\Theta(n)$.

**Conclusion:** A checked memory guard rejects the table before allocation and dispatches to another stable mechanism.

### Example 3

**Question:** Compare radix digit widths $r=8$ and $r=16$ for $W=64$ bits and $n=10^6$ using $d(n+2^r)$.

**Reasoning:** For $r=8$, $d=8$ and the proxy is

$$
8(10^6+256)=8{,}002{,}048.
$$

For $r=16$, $d=4$ and the proxy is

$$
4(10^6+65{,}536)=4{,}262{,}144.
$$

The second proxy is smaller but its digit table is 256 times larger.

**Conclusion:** The arithmetic nominates candidates; cache, clearing, buffers, extraction, and measured time decide the implementation.

### Example 4

**Question:** What multiplicity entropy follows from class sizes $(8,4,4)$ for $n=16$?

**Reasoning:** Probabilities are $(1/2,1/4,1/4)$, so

$$
H=\frac12(1)+\frac14(2)+\frac14(2)=1.5.
$$

The leading information scale is $nH=24$ bits.

**Conclusion:** Duplicates reduce comparison information relative to 16 distinct ranks, but 24 is not a prediction of comparisons or nanoseconds for an arbitrary implementation.

### Example 5

**Question:** Do two natural runs imply few inversions?

**Reasoning:** Rotate $(0,1,2,3,4,5,6,7)$ to $(4,5,6,7,0,1,2,3)$. It has two ascending runs. Every one of the first four values exceeds every one of the last four, so $I=4\cdot4=16$ out of $\binom82=28$ pairs.

**Conclusion:** Run count predicts natural merging opportunities; inversion count predicts a different kind of disorder.

### Example 6

**Question:** With $s=10{,}000$ independent uniform pair samples and $\delta=0.05$, what Hoeffding radius is justified?

**Reasoning:**

$$
\varepsilon
=
\sqrt{\frac{\ln(40)}{20{,}000}}
\approx0.01358.
$$

**Conclusion:** Under the stated model, the interval $\widehat q\pm0.01358$ has failure probability at most $0.05$; it says nothing about adjacent-only or clustered sampling.

### Example 7

**Question:** A sorting path moves each of one million items 20 times. Compare 256-byte records with eight-byte indices before gather.

**Reasoning:** Direct traffic is approximately

$$
10^6\cdot20\cdot256=5.12\text{ GB},
$$

while index traffic is

$$
10^6\cdot20\cdot8=0.16\text{ GB}.
$$

This is a 32-fold sort-phase byte ratio.

**Conclusion:** Indirection is a strong candidate, but its index allocation and any later gather must be added before claiming a pipeline win.

### Example 8

**Question:** A run-adaptive path is allowed when $q<0.10$. Sampling reports $\widehat q=0.095$ with radius $0.012$. What should dispatch infer?

**Reasoning:** The interval is $[0.083,0.107]$, which crosses the policy boundary. The sample does not establish either side.

**Conclusion:** Use the conservative default, refine within a fixed budget, or run a bounded pilot; do not flip policy from the point estimate alone.

### Example 9

**Question:** In 101 paired trials, candidate $A$ beats $B$ in median time by 6%, but $A$ has 4 times the p99 latency and invokes fallback on 3% of requests. Is $A$ the clear winner?

**Reasoning:** The median answers only an ordinary-case question. Tail latency and fallback rate may violate the service objective. Inspect paired differences by workload stratum, confidence intervals, memory peaks, and fallback inputs.

**Conclusion:** No universal winner follows; the service contract determines whether the median gain compensates for tail risk.

### Example 10

**Question:** How should a public stable sort handle sparse attacker-chosen integers, expensive key callbacks, and a memory ceiling?

**Reasoning:** Evaluate each key once into bounded private storage, check exceptional values, compute extrema with checked arithmetic, reject table candidates whose complete allocation exceeds the budget, and use a robust stable comparison path. Bound callbacks and work, keep cancellation points, and publish only according to the failure contract.

**Conclusion:** Profiling can find safe dense cases, while checked allocation and the deterministic stable fallback protect hostile cases.

## Cross-Program Connections

- [Theory of Computation & Complexity](../../15-theory-of-computation-and-complexity/ROADMAP.md) owns comparison lower bounds, parameterized analysis, probability bounds, and adversarial models.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns cache, branch, bandwidth, NUMA, vectorization, accelerators, and hardware counters.
- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) owns arrays, buffers, index permutations, sketches, and representation costs used by the portfolio.
- [Programming Languages & Semantics](../../01-programming-languages-and-semantics/ROADMAP.md) owns comparator laws, callbacks, exceptions, ownership, moves, and generic library contracts.
- [Software Engineering, Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) owns property testing, benchmark reproducibility, regression design, canaries, and observability.
- [Security Engineering](../../25-security-engineering/ROADMAP.md) owns algorithmic-complexity attacks, tenant isolation, resource budgets, sensitive telemetry, and hostile callbacks.
- [Data Engineering](../../19-data-engineering/ROADMAP.md) owns external sorting, partition skew, columnar indirection, spills, restarts, and downstream consumers.
- [Concurrent & Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) owns task decomposition, synchronization, work/span, contention, and deterministic parallel results.

## References

1. Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, and Clifford Stein. [*Introduction to Algorithms*, fourth edition](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/), MIT Press, 2022. Comparison, counting, radix, bucket, stability, lower-bound, and correctness foundations.
2. Donald E. Knuth. [*The Art of Computer Programming, Volume 3: Sorting and Searching*, second edition](https://www.informit.com/store/art-of-computer-programming-volume-3-sorting-and-searching-9780321635785), Addison-Wesley Professional, 1998. Quantitative sorting analysis, distributions, implementations, and external considerations.
3. Jon L. Bentley and M. Douglas McIlroy. [“Engineering a Sort Function”](https://doi.org/10.1002/spe.4380231105), *Software: Practice and Experience* 23(11), 1993, pp. 1249–1265. Primary engineering evidence on sampling, three-way partitioning, robustness, testbeds, and performance certification.
4. Vladimir Estivill-Castro and Derick Wood. [“A Survey of Adaptive Sorting Algorithms”](https://doi.org/10.1145/146370.146381), *ACM Computing Surveys* 24(4), 1992, pp. 441–476. Measures of disorder and theoretical/practical adaptivity.
5. David R. Musser. [“Introspective Sorting and Selection Algorithms”](https://doi.org/10.1002/%28SICI%291097-024X%28199708%2927%3A8%3C983%3A%3AAID-SPE117%3E3.0.CO%3B2-%23), *Software: Practice and Experience* 27(8), 1997, pp. 983–993. Primary bounded hybrid sorting and fallback design.
6. Tim Peters and CPython contributors. [“listsort.txt”](https://github.com/python/cpython/blob/main/Objects/listsort.txt), CPython source-tree design note; consulted 2026-09-04. Current implementation rationale for stable natural merging, key comparisons, working memory, runs, and Powersort.
7. J. Ian Munro and Sebastian Wild. [“Nearly-Optimal Mergesorts: Fast, Practical Sorting Methods That Optimally Adapt to Existing Runs”](https://doi.org/10.4230/LIPIcs.ESA.2018.63), ESA 2018, LIPIcs 112, article 63. Run-length entropy and practical merge scheduling.
8. ACM, IEEE Computer Society, and AAAI. [*Computer Science Curricula 2023: Algorithmic Foundations*](https://csed.acm.org/al-cs-core/), endorsed 2024; consulted 2026-09-04. Current curricular scope for sorting, algorithm engineering, empirical analysis, parallelism, and probability.

## Exercises

### Exercise 1

Profile stable records with keys $(5,1,5,2,1,0,2,5)$. Compute $n$, $K$, $u$, duplicate excess, multiplicities, $H$, adjacent descents, and maximal nondecreasing run lengths. Identify feasible candidates among stable counting, stable natural merge, and stable comparison sorting under a 1 KiB auxiliary budget with eight-byte counters and eight-byte output references. State what the profile cannot determine.

### Exercise 2

Two feasible algorithms have cost vectors. Candidate $A$ has $C=1{,}200{,}000$, $P=100{,}000$, $B=64{,}000{,}000$, and $Z=0$. Candidate $B$ has $C=0$, $P=100{,}000$, $B=160{,}000{,}000$, and $Z=65{,}536$. With calibrated coefficients $c_C=5$, $c_P=40$, $c_B=0.02$, and $c_Z=1$ cost units, compute both predictions. Explain why the answer is not a universal benchmark result.

### Exercise 3

Derive the minimum integer number of independent uniform index-pair samples required by Hoeffding's inequality for inversion-fraction error at most $0.02$ with failure probability at most $0.01$. Then explain whether sampling 6,623 adjacent pairs satisfies the conclusion.

### Exercise 4

Design a reproducible benchmark to choose among stable comparison, stable natural merge, stable counting, radix, and indirect stable sorting. Specify factors, boundary cases, full-path timing, counters, repetitions, randomization, baselines, held-out evaluation, statistical reporting, artifacts, and criteria for rejecting a complex dispatcher.

### Exercise 5

Design a production sorting policy for a multitenant analytics service. Inputs include narrow integers, expensive strings, wide rows, existing runs, extreme sparse values, and hostile requests. Stability is request-selectable. Specify contracts, profiling, sampling, portfolio, decision uncertainty, memory and work budgets, fallbacks, validation, privacy-safe telemetry, drift handling, canary rollout, and rollback.

## Answers to the Exercises

### Answer 1

For keys

$$
(5,1,5,2,1,0,2,5),
$$

$n=8$, minimum is $0$, maximum is $5$, and

$$
K=5-0+1=6.
$$

The distinct set is $\{0,1,2,5\}$, so $u=4$ and duplicate excess is $8-4=4$. Multiplicities in key order are $(1,2,2,3)$, giving probabilities $(1/8,1/4,1/4,3/8)$. Therefore

$$
H
=
\frac18\log_2 8
+2\left(\frac14\log_2 4\right)
+\frac38\log_2\frac83
\approx1.906.
$$

Descents occur at $5\to1$, $5\to2$, $2\to1$, and $1\to0$. The maximal nondecreasing runs are

$$
(5),\quad(1,5),\quad(2),\quad(1),\quad(0,2,5),
$$

with lengths $(1,2,1,1,3)$ and $\rho=5$.

Stable counting needs a first-order auxiliary estimate

$$
Kb_c+nb_o=6\cdot8+8\cdot8=112\text{ bytes},
$$

so it fits 1 KiB before implementation overhead, which must also be bounded. Stable natural merge and stable comparison sorting are logically feasible if their actual chosen implementations fit the same budget; the labels alone do not establish that. A buffer-heavy merge may exceed the budget, while an in-place stable algorithm may satisfy it with different time costs.

The profile does not determine elapsed time, key callback cost, record width, cache behavior, allocation overhead, comparator behavior, downstream gather cost, concurrency, or which feasible implementation is fastest on the target system.

### Answer 2

For candidate $A$,

$$
\begin{aligned}
\widehat T_A
&=5(1{,}200{,}000)+40(100{,}000)+0.02(64{,}000{,}000)+1(0)\\
&=6{,}000{,}000+4{,}000{,}000+1{,}280{,}000\\
&=11{,}280{,}000.
\end{aligned}
$$

For candidate $B$,

$$
\begin{aligned}
\widehat T_B
&=5(0)+40(100{,}000)+0.02(160{,}000{,}000)+1(65{,}536)\\
&=4{,}000{,}000+3{,}200{,}000+65{,}536\\
&=7{,}265{,}536.
\end{aligned}
$$

The calibrated proxy predicts $B$ lower by $4{,}014{,}464$ cost units for the modeled environment and workload. It is not a universal result because the coefficients are empirical and environment-specific, linear additivity may omit interactions, and the vector omits such terms as allocation latency, cache state, contention, tails, and downstream work. Measure both candidates end to end on held-out representative cases before deployment.

### Answer 3

Hoeffding requires

$$
2e^{-2s\varepsilon^2}\le\delta.
$$

Rearranging,

$$
s
\ge
\frac{\ln(2/\delta)}{2\varepsilon^2}
=
\frac{\ln 200}{2(0.02)^2}
=
\frac{5.298317\ldots}{0.0008}
=6622.896\ldots.
$$

The smallest integer satisfying the bound is

$$
s=6623.
$$

No, 6,623 adjacent pairs do not satisfy the stated conclusion. They estimate the frequency of local descents and are dependent when they overlap; the derivation defined independent pairs sampled uniformly from the complete population of index pairs. A different sampling design needs its own estimator and bound.

### Answer 4

Define the shared stable contract first: frozen keys, exceptional-value order, ordered identity permutation, stable equivalence, output form, allocation/failure semantics, and resource ceilings. Implement differential property checks against a trusted decorated baseline before timing.

Stratify by logarithmic $n$ plus dense points around every cutoff and cache transition; integer $K/n$ ratio; digit width; $u/n$ and heavy-hitter multiplicities; run count and length distribution; inversion fraction; ordered, reverse, rotated, organ-pipe, sawtooth, random, and local-edit order; cheap versus expensive keys; narrow versus wide records; direct versus permutation consumer; cold/warm state; isolated/contended execution; and honest versioned corpus slices. Include extreme keys, empty/singleton, all equal, and adversarial cases for the actual pivot and run policies.

Time the full requested path. Counting includes extrema, table initialization, allocation, and output. Radix includes encoding and buffers. Indirect sorting includes gather when the consumer needs materialized rows. Profiling and sampling belong in dispatcher time. Record comparisons, projections, initialized slots, bytes, allocations, peak memory, cache/branch counters, run/depth states, fallbacks, and error paths.

Use reproducible generators and seeds. Randomize candidate order within environmental blocks, use paired equivalent inputs, warm up only according to a declared protocol, and retain every raw repetition. Report median, quantiles, paired differences, uncertainty intervals, maxima, and failures rather than only the best mean. Record source revision, policy/model version, machine topology, OS, runtime/compiler, flags, allocator, load, generator, seed, and corpus digest under `artifacts/`.

Use one portion for threshold/model selection and held-out strata for final evaluation. Compare the dispatcher with the current policy, one robust stable comparison baseline, and a post-hoc oracle. Reject the complex dispatcher if its held-out improvement is negligible, profiling overhead erases gains, regret tails are unsafe, memory grows, decisions are unstable at boundaries, or the policy cannot be explained and rolled back reliably.

### Answer 5

Expose stable and unstable modes explicitly. Both freeze one key per identity, define null/NaN/locale handling, return an ordered identity permutation or declared output form, and specify allocation, cancellation, callback failure, partial mutation, and failure atomicity. Stable mode preserves source order within equivalence classes. Put untrusted work in request, tenant, and process budgets.

During bounded key materialization, collect exact $n$, safe type facts, extrema, and adjacent descents. Compute $K$ only with widened checked arithmetic. Use bounded cardinality or heavy-hitter structures only if their decision value justifies them. For expensive disorder features, use a fixed-budget sampling scheme with documented random population and confidence interval. Do not log raw keys.

Eliminate infeasible paths before scoring. Stable counting is eligible only for integral encodings whose counter plus output plus overhead bytes fit the request budget. Radix is eligible only for reviewed total encodings and buffers. Natural merge is eligible for stable requests with a proven bounded run policy. Indirect sorting is eligible for wide rows, especially when the next operator consumes a permutation. A robust stable comparison sort is the stable default. Three-way introspective sort with heap fallback can serve unstable requests. All paths use the frozen keys and identical exceptional-value order.

Choose with a versioned, offline-validated rule or model. Include profile overhead and downstream gather. If a confidence interval crosses a decision boundary, use the conservative default or a bounded refinement. Apply hysteresis to policy replacement, not to per-request correctness. Enforce checked allocation, bounded stack/depth, cancellation points, key/callback budgets, and deterministic fallback regardless of predicted distribution.

Validate order, identity, stable pairs, key-call counts, fast/fallback equivalence, range arithmetic, allocation rejection, cancellation, exceptions, and partial mutation. Fuzz boundary handoffs and adversarial distributions. Benchmark full paths across the factorial matrix, report tails and peak resources, and retain raw artifacts.

Emit privacy-reviewed buckets, policy/reason version, uncertainty, selected path, bounded counters, fallback events, failures, resource peaks, and latency quantiles. Alert on workload drift, path-rate change, fallback growth, and tails. Refit only through an offline reproducible process with held-out validation.

Canary new policy versions, shadow only within explicit duplicate-work budgets, compare sampled result fingerprints and resource objectives, and rehearse rollback. Keep the previous safe policy available until correctness, memory, tail latency, and drift criteria pass. Disable the new version automatically on predefined contract mismatches, allocation/fallback spikes, or service-level regressions.
