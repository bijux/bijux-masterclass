# Workbook — Module 82: CPU Profiling, Cost Models, and Hot-Path Optimization

[Chapter](index.md) · [Laboratory](../../labs/module-02-profile-guided-query-engine/README.md) · [MetricRail guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **CPU Profiling, Cost Models, and Hot-Path Optimization** has become a usable model rather than remembered vocabulary. Its governing question is: *Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?* Preserve your first prediction and record decisive facts in a **profile and cost model**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 81 — Performance Contracts, Workloads, and Benchmark Design that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?**
3. Draw the smallest **profile and cost model** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### 1. Inclusive versus exclusive cost

A flame graph attributes 38% inclusive time to `handle_batch`, 31% to `parse_line`, and 2% exclusive time to `handle_batch` itself. Which function is the stronger initial investigation target? Explain why the widest parent frame is not automatically the hottest implementation.

### 2. Call count versus cost per call

Version A invokes `normalize_key` once per record at 90 ns per call. Version B invokes it four times per record at 35 ns per call. Predict the total effect at one million records and identify the more useful optimization question.

### 3. Scaling signature

Observed time for input sizes 1k, 2k, 4k, and 8k is 1.1, 2.2, 4.5, and 9.0 ms. A second path measures 1.0, 2.4, 5.8, and 13.8 ms. Classify the likely scaling of each and state what additional measurement is needed before naming an algorithmic cause.

### 4. Debug versus shipped profile

A developer profiles a debug build and finds bounds checks and formatting at the top. Predict why the ranking may change under the release artifact and what metadata belongs in the profile record.

### 5. A cache that wins the hot path

A query cache cuts repeated lookup CPU by 70% but increases cold-start time, invalidation work, and retained memory. List the workload variables needed to decide whether the cache is beneficial.

## Part 2 — Diagnose and repair

### Case A — Editing the widest frame

The team rewrites `process_request` because it owns the widest frame, but almost all samples are in a hash function called below it. Write a profile-driven investigation plan that distinguishes high call count, expensive keys, poor hashing, and unrelated downstream work.

### Case B — Optimizing an irrelevant micro-path

A hand-tuned integer parser is 40% faster, but end-to-end ingestion changes by less than 0.5%. Give four explanations and identify the next evidence to collect.

### Case C — One profile, four changes

A patch adds an index, changes the hash function, batches updates, and removes validation. It is 25% faster. Explain why the result is scientifically weak even if repeatable. Design a sequence of changes that preserves attribution.

### Case D — Sampling blind spot

A short operation completes too quickly for a sampling profiler to attribute reliably. Choose among repetition, instrumentation, a microbenchmark, and tracing. State the trade-off of each.

## Part 3 — Focused exercises

### Exercise 1 — Query engine accounting

For a document search, define counters for:

- documents considered;
- candidate documents after indexing;
- token comparisons;
- result materializations;
- index-build work.

Write formulas for linear search and indexed search. Identify the crossover variables.

### Exercise 2 — Profile interpretation table

Create a table with columns: symbol, inclusive share, exclusive share, call count, input sensitivity, suspected mechanism, and confirming experiment. Fill it for parsing, hashing, allocation, sorting, and rendering.

### Exercise 3 — Select one change

Given a profile where 46% is repeated tokenization, 18% hashing, 14% allocation, 8% sorting, and the remainder elsewhere, propose one change. State the expected profile movement and a displaced cost to measure.

### Exercise 4 — Reject a seductive optimization

Write a short decision record rejecting one optimization because the profiled phase is not dominant, the workload is not representative, or the semantic cost is unacceptable.

### Exercise 5 — Optimization dossier

Prepare a one-page dossier for a proposed query optimization. Include the exact scenario profile, the top three stacks or instrumented phases, call counts, a scaling table, the causal hypothesis, the one mechanism to change, the semantic oracle, and displaced costs. Write the result you expect to see if the hypothesis is correct and the result that would falsify it. Finish with a stop condition: when would you abandon the optimization rather than keep tuning the micro-path?

### Interleaved reasoning pass

1. For **Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the profile and cost model.
2. For **Read call stacks and flame graphs without confusing inclusive cost with exclusive cost**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the profile and cost model.
3. For **Separate algorithmic work from parsing, allocation, hashing, formatting, synchronization, and system calls**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the profile and cost model.
4. For **Form a cost hypothesis that predicts how runtime changes with input size and distribution**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the profile and cost model.

5. Identify one guarantee from an earlier course that a careless implementation of **CPU Profiling, Cost Models, and Hot-Path Optimization** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build the [Profile-Guided Query Engine](../../labs/module-02-profile-guided-query-engine/README.md). Preserve source-order results. Add counters that reveal work rather than time, build an index without changing query semantics, and compare linear and indexed paths over varied corpus sizes and selectivities. The goal is not to make the indexed path win every case; it is to explain where and why it wins.

### Laboratory acceptance trace

Before opening the reference implementation for **Profile-Guided Query Engine**, record:

- the public behavior that demonstrates **Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Profile four MetricRail scenarios separately:

1. valid line ingestion with a hot series;
2. valid ingestion with mostly unique series;
3. snapshot rendering;
4. malformed-line rejection.

For each scenario, record release profile, toolchain, input corpus, call stacks, phase counters, and one hypothesis. Change only one mechanism in the first optimization patch. Re-run semantic tests and the full scenario after the local benchmark.

### Capstone invariant trace

For the Module 82 MetricRail increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Without notes:

1. Define inclusive and exclusive profile cost.
2. Why can a cheap function dominate total CPU?
3. How does a scaling curve constrain causal hypotheses?
4. Why must the profiled binary match the shipped configuration?
5. When is instrumentation more useful than sampling?
6. What makes an optimization patch attributable?
7. Why can a successful cache still reduce production capacity?
8. Describe the evidence chain from profile to accepted change.

### Exercise 6 — Distinguish a hot symbol from a useful intervention

Suppose `hash_one` accounts for 22% of sampled CPU in the unique-series workload. Construct three competing explanations: the hash implementation is expensive, the program hashes more often than the design requires, or the key representation causes avoidable preprocessing before hashing. For each explanation, name one measurement that could falsify it. Then write a proposed experiment that changes only one cause while preserving the same keys, outputs, and workload. Include the displaced costs you would recheck: allocation, cache footprint, lock hold time, and snapshot order. Your answer must make clear why replacing the hash function before counting calls would be premature.

### Profile review gate

Before accepting an optimization, another reader should be able to answer four questions from your dossier alone: which shipped scenario was measured, where the cost accumulated, why the proposed edit should affect that cost, and which semantic oracle proves that the result is still the same program. A faster local benchmark without those links is an observation, not an optimization case.

### Closed-book defense

In five minutes, answer “Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?” using the **profile and cost model**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside MetricRail. A list of APIs without the deciding relationship is incomplete.
