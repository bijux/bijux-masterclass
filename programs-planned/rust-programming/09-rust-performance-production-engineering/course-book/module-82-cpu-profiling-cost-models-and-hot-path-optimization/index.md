# Module 82 — CPU Profiling, Cost Models, and Hot-Path Optimization

**82/90** · Course 9 · Module 82 of 90

[Course 9 overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [MetricRail guide](../capstone.md)

## The question

> Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?

## Why this comes now

Module 81 told you how to decide whether a difference matters. Module 82 asks where the cost comes from. A profiler is valuable only after the workload and artifact are fixed; otherwise it faithfully explains an irrelevant run. You now move from comparison to causality: which call paths, algorithms, branches, cache behaviors, and repeated operations account for the measured cost?

The goal is not to eliminate every visible frame. It is to construct a cost model that predicts how the program changes as input size, key cardinality, or contention changes. A profile gives evidence about one execution. The model turns that evidence into a hypothesis you can falsify.

## What you will be able to do

After completing this module, you will be able to:

- choose sampling, instrumentation, counters, and targeted tracing based on the question being asked
- read call stacks and flame graphs without confusing inclusive cost with exclusive cost
- separate algorithmic work from parsing, allocation, hashing, formatting, synchronization, and system calls
- form a cost hypothesis that predicts how runtime changes with input size and distribution
- design a focused experiment that can falsify the hypothesis
- optimize the dominant path while preserving uncommon-path behavior and diagnostics
- recognize phase-shifting optimizations that make a microbenchmark faster while leaving end-to-end cost unchanged

## Core model

### The governing model

Profiling is a causal investigation. The loop is `measure → localize → hypothesize → change one cause → remeasure → validate`. A hotspot is evidence of where samples accumulated, not automatically evidence of bad code. The hot function may be unavoidable work, may be called too often, or may merely contain inlined descendants. A useful cost model explains both the stack and how the cost scales.

### 1. Profilers answer different questions

A sampling profiler estimates where CPU time is spent with relatively low perturbation. Instrumentation can provide exact counts or durations but changes execution more. Hardware counters reveal cache misses, branches, cycles, and instructions but require careful interpretation. Application tracing explains product spans and causal context rather than instruction-level cost. Select the tool from the question.


### 2. Inclusive and exclusive cost

Inclusive cost includes time in callees; exclusive cost attributes only the body itself. A function high in every stack can have high inclusive cost because it orchestrates expensive descendants. Optimizing its few local statements may do nothing. Read the stack from product operation to leaf costs and ask whether the problem is per-call expense or excessive call count.


### 3. Build a scaling hypothesis

Suppose snapshot generation sorts `k` series and formats `n` values. A plausible model is `T(n,k) = a·n + b·k log k + c·bytes_rendered`. The coefficients are empirical, but the shape predicts which benchmark parameters should expose the cost. If runtime grows quadratically, search for nested lookup or repeated scanning rather than polishing string formatting.


### 4. Monomorphization and inlining

Generic Rust can produce specialized code that is fast but expands instruction footprint. Inlining can remove call overhead and enable optimization, yet excessive inlining can increase binary size and instruction-cache pressure. Do not add `#[inline(always)]` from habit. Use profile evidence, inspect generated artifacts when necessary, and measure both runtime and size.


### 5. Branches and data locality

A branch is not inherently expensive; an unpredictable branch in a hot loop may be. A hash lookup is not inherently slow; repeated hashing of the same long key may dominate. A cache-friendly linear scan can beat an elaborate structure for small collections. Cost models must include input distribution and memory access, not only Big-O notation.


### 6. End-to-end closure

After a localized optimization, rerun the microbenchmark, the scenario benchmark, and the product tests. If parsing became faster by retaining extra indexes, measure memory and snapshot cost. If work moved from request handling to startup, measure startup. If a cached result is introduced, measure invalidation and cold behavior.

Profile interpretation must connect samples to product work. Inclusive time can identify an expensive operation boundary, while exclusive time can identify the instructions executed in one frame. Neither tells you automatically whether the cost is necessary, repeated too often, caused by poor locality, or merely waiting on another resource.

### A module-specific decision table

| Profile question | Useful observation | Follow-up experiment |
|---|---|---|
| Is cost concentrated or distributed? | top stacks and cumulative share | optimize one isolated frame only if concentration is real |
| Does cost scale with records or unique keys? | profile at several cardinalities | plot work per record and per new series |
| Is a helper expensive or merely frequent? | call count plus exclusive cost | memoize or restructure only after frequency is understood |
| Is time CPU or waiting? | CPU samples, queue wait, lock wait, wall time | separate active service from residence time |
| Did inlining hide boundaries? | annotated assembly or alternate profile | compare with enough debug information for attribution |
| Did the change move cost? | before/after profiles plus memory and latency | inspect callers, callees, cold paths, and cleanup |

### Working procedure

1. Reproduce the regression or target workload with the profiling artifact, not a debug build.
2. Confirm that the scenario still passes its semantic oracle and reaches the code path of interest.
3. Read top-down to locate expensive product operations, then bottom-up to find common callees and repeated mechanisms.
4. Record inclusive cost, exclusive cost, call frequency, and input scale. Do not rank frames by one column alone.
5. Write at least two causal hypotheses and one observation that would falsify each.
6. Vary one scale dimension—records, unique keys, identifier length, snapshot rows, or concurrency—and compare profile shape.
7. Change one mechanism, rerun the same profile, and inspect latency, memory, and cold-path effects before accepting it.

### Failure patterns and principled repairs

#### Optimizing the function with the largest inclusive bar without inspecting its callees or call count.

A large inclusive frame can be a container for expensive callees. Inspect its descendants and invocation count before editing the frame itself.

#### Treating a flame graph as a proof that an algorithm is asymptotically wrong.

A flame graph shows where sampled time appeared, not the asymptotic function. Vary input size and cardinality before making an algorithmic claim.

#### Profiling a debug build and generalizing its cost structure to the release artifact.

Debug artifacts have different inlining, checks, and code generation. Reproduce the shipped or profiling profile before explaining release cost.

#### Adding caching, cloning, or indexes without measuring cold paths, invalidation, retained memory, and downstream work.

Caches and indexes exchange CPU for memory, invalidation, startup, and complexity. Add them only after measuring repeated work and their retained state.

#### Changing several mechanisms at once so no result identifies which change mattered.

Bundled changes erase causality. Revert to one intervention per experiment so the profile can explain why the result moved.

## Use the idea in a complete program

```rust
use std::collections::BTreeMap;

#[derive(Default)]
struct Totals {
    values: BTreeMap<String, i64>,
}

impl Totals {
    fn apply(&mut self, key: &str, delta: i64) {
        *self.values.entry(key.to_owned()).or_default() += delta;
    }

    fn snapshot(&self) -> Vec<(&str, i64)> {
        self.values.iter().map(|(key, value)| (key.as_str(), *value)).collect()
    }
}

fn main() {
    let mut totals = Totals::default();
    for _ in 0..1000 {
        totals.apply("requests", 1);
    }
    assert_eq!(totals.snapshot(), vec![("requests", 1000)]);
}
```

Read the example as a miniature cost-model exercise. Count how often each function runs, identify which work depends on input length, and predict which frame should dominate before measuring. Then change the input distribution so the prediction changes. If the observed profile does not move as predicted, investigate compiler optimization or an incorrect workload before rewriting code.

The important habit is to annotate the profile with product meaning. A frame named `lookup` might represent hash calculation, key comparison, allocation on miss, or lock waiting around the map. Source names are clues; they are not causal explanations.

### MetricRail consequence

Profile MetricRail under three fixed scenarios: repeated updates to one hot series, high-cardinality insertion of new series, and snapshot rendering after a large deterministic store. These scenarios isolate different mechanisms. A single mixed workload can hide whether hash lookup, identifier ownership, ordered-map traversal, formatting, or allocation dominates.

For every profile, record the exact binary profile and corpus. Build a scaling table over record count and unique-series count. If lookup cost rises with unique series while parse cost remains linear in bytes, the next experiment should target key representation or map behavior—not parser unrolling.

The capstone keeps an obviously correct store and parser path as an oracle. Optimization is accepted only when the same records, errors, limits, and snapshot bytes are preserved. The profile report must also state what became worse: binary size, retained memory, cold startup, or implementation complexity.

### Boundary case: the hottest frame is a symptom

Imagine a flame graph in which `BTreeMap::entry` and key comparison dominate MetricRail’s high-cardinality workload. Replacing the map immediately is premature. The profile may be showing genuinely logarithmic lookup cost, repeated construction of long keys, poor locality caused by allocation, or simply the fact that every accepted record must pass through the single broker. Those mechanisms require different repairs.

Run two discriminating sweeps. In the first, hold record count constant and vary unique-series count. In the second, hold unique-series count constant and vary identifier length and hot-key concentration. If cost grows mainly with cardinality, the data structure or ordered-key comparison is implicated. If it grows with identifier length even on hot keys, hashing or comparison bytes matter. If wall time rises while CPU samples do not, queueing or synchronization is the likely cause.

A replacement hash map might reduce update CPU but remove deterministic traversal, forcing snapshot sorting later. The profile review must therefore include the snapshot scenario and memory footprint. The right question is not “can this frame be smaller?” but “which representation minimizes the complete workload while preserving deterministic output and bounded memory?”

## Practice sequence

1. Predict the top three frames for one controlled workload before opening a profiler.
2. Record both inclusive and exclusive interpretations for the largest frame.
3. Run the Profile-Guided Query Engine lab and separate frequency, per-call cost, and scale-dependent cost.
4. Construct two competing hypotheses for MetricRail lookup cost and design one cardinality sweep that distinguishes them.
5. Apply exactly one implementation change and reproduce the original profile.
6. Close with a cost-model paragraph: what mechanism was removed, why the profile changed, and what displaced costs remain.

Use the [workbook](workbook.md) to freeze predictions and complete the causal repairs. Build the module laboratory before reading its reference implementation, then transfer the mechanism into the [MetricRail engineering guide](../capstone.md).

## Ready to continue

Continue only when you can:

- explain the difference between inclusive cost, exclusive cost, and call frequency;
- turn a profile frame into at least two falsifiable hypotheses;
- distinguish CPU execution from queue, lock, or dependency waiting;
- design a scale experiment that tests an algorithmic claim;
- reject a profile-driven change that only moves cost into memory or a cold path;
- identify MetricRail’s dominant mechanism under three different workloads.

## Primary Rust references

- The Rust Performance Book chapters on profiling, heap allocation, bounds checks, and build configuration
- Cargo documentation for release profiles, debug information, code generation units, and link-time optimization
- Platform profiler documentation for the operating systems used by the project

These references are for verification and deeper lookup after the chapter’s model is understood. The course-book chapter remains the complete learning route for the required concepts.

## Continue

1. Complete the [Module 82 workbook](workbook.md).
2. Use the [reasoned solutions](solutions.md) only after writing your own answers.
3. Build the [Profile-Guided Query Engine laboratory](../../labs/module-02-profile-guided-query-engine/README.md).
4. Apply the module to [MetricRail](../capstone.md).
