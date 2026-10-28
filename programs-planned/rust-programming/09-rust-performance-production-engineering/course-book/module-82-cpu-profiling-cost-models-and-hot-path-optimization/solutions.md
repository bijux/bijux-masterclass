# Reasoned Solutions — Module 82: CPU Profiling, Cost Models, and Hot-Path Optimization

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-02-profile-guided-query-engine/README.md) · [MetricRail guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 82: CPU Profiling, Cost Models, and Hot-Path Optimization**. Compare the reasoning against this question: *Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Profile reasoning

### 1. Inclusive versus exclusive cost

`handle_batch` is a structural parent, not necessarily the expensive implementation. Its 2% exclusive share means its own instructions are cheap; most time is in descendants. `parse_line` is a better initial target because its 31% is attributed to that phase, but even there you must inspect its callees, call count, and input distribution. A parent frame is useful for identifying the product phase; exclusive and descendant frames localize mechanisms.

### 2. Call count versus cost per call

A performs about 90 ms of normalization per million records. B performs four million calls at 35 ns, about 140 ms. B made the function faster but the system slower because invocation count changed. The better question is why normalization occurs four times and whether a validated/canonical key can be computed once and carried through the pipeline.

### 3. Scaling signature

The first path is approximately linear. The second grows faster than linear over the observed range, but four points do not prove a specific complexity class. Measure larger sizes, normalize by `n` and `n log n`, record the actual operation count, and check whether cache or allocation thresholds explain the curve. Algorithmic labels should follow a model, not visual resemblance alone.

### 4. Debug versus shipped profile

Debug builds alter inlining, optimization, bounds-check elimination, code layout, and generic instantiation cost. The dominant debug stack may disappear or invert in release. Record source revision, toolchain, target, CPU features, Cargo profile, feature set, lockfile, input corpus, profiler settings, and host state.

### 5. A cache that wins the hot path

Decision variables include hit rate, key distribution, entry size, eviction policy, invalidation frequency, cold-start duration, memory budget, cardinality, request latency objective, and restart/deployment frequency. Measure both hit and miss paths plus retained memory. A cache is beneficial only when avoided work exceeds lookup, synchronization, invalidation, and capacity costs under the actual distribution.

## Part 2 — Repairs

### Case A

Start with the shipped scenario and capture stacks plus domain counters. Determine:

1. how many hash calls occur per accepted record;
2. key lengths and repeated-key distribution;
3. whether the hash cost is in lookup, insertion, or rebuilding;
4. whether collisions or allocation dominate;
5. whether snapshot work appears on the ingestion path.

Then run one confirming experiment—for example, precompute canonical key hashes while preserving equality semantics—and expect both hash call count and stack share to move. If total time does not move, the hash phase was not the limiting product cost.

### Case B

The parser may be a tiny fraction of the scenario, input receipt or synchronization may dominate, the benchmark may exercise a different line shape, or cost may have moved into validation/copying. Profile the end-to-end path, measure parse phase duration and call count, and compare the exact corpus. Do not continue hand-tuning until parser share is large enough to explain a meaningful product change.

### Case C

The patch changes four causal variables and one semantic contract. Repeatability proves only that the bundle differs, not which mechanism is responsible. Restore validation first. Establish a baseline, then apply index, hash, and batching changes one at a time, measuring the local mechanism, end-to-end scenario, memory, and semantics after each. Interactions can be tested later as an explicit factorial experiment.

### Case D

Repeat the operation inside one sampled region to accumulate samples, but ensure repetition does not change cache state unrealistically. Instrument phase counters or durations when exact boundaries matter, accepting probe overhead. Use a microbenchmark for instruction-level comparison, accepting reduced product realism. Use tracing for request-phase attribution and rare paths, accepting coarser timing and event cost. The correct tool follows the question.

## Part 3 — Model answers

### Exercise 1

A linear query model is approximately:

```text
build = 0
query = documents_considered × tokens_per_document × comparison_cost
materialize = matches × result_cost
```

An index model is:

```text
build = total_tokens × tokenize/hash/insert cost
query = posting_lookup + candidate_documents × verification cost
materialize = matches × result_cost
```

The crossover depends on corpus size, token count, query count, selectivity, update frequency, index memory, and whether exact source order requires sorting candidates. Counters make these terms observable independent of clock noise.

### Exercise 2

A useful table does not merely copy percentages. Parsing should be paired with line length and malformed rate; hashing with key length and call count; allocation with object count and retained capacity; sorting with result cardinality; rendering with output bytes. Each suspected mechanism needs a confirming experiment that changes only that term.

### Exercise 3

Repeated tokenization is the dominant candidate. Compute tokens once at the ownership boundary or store an index, preserving token definition and source-order results. Predict fewer tokenizer calls and a lower tokenization stack share. Measure retained memory, build/update cost, and cold-query latency as displaced costs.

### Exercise 4

A valid rejection could say: “We will not add a global result cache. The profiled workload spends 3% in result construction, while the cache retains unbounded tenant-specific entries and complicates invalidation. The likely maximum gain cannot justify the capacity and correctness risk. We will instead investigate repeated tokenization, which accounts for 46% of CPU.”

## Part 4 — Laboratory review

The reference engine should preserve document source order and exact token equality. Counters should show that indexed queries consider fewer candidate documents for selective terms, while index construction and memory remain explicit. For a one-off query over a tiny corpus, the linear oracle may remain better; this is a successful result because the cost model explains the boundary rather than forcing one implementation to win universally.

## Part 5 — MetricRail transfer

Hot-series ingestion may be dominated by lookup and counter updates; unique-series ingestion may be dominated by allocation and map growth; snapshots may be dominated by sorting and formatting; malformed input may be dominated by validation and diagnostics. Profile them separately. The first patch should name one hypothesis, such as “canonical identifier parsing occurs twice per accepted record,” and predict a reduction in calls without changing accepted grammar or error evidence.

## Part 6 — Defense

Inclusive cost includes descendants; exclusive cost belongs to the function’s own instructions. Cheap functions dominate through call count. Scaling constrains whether fixed, linear, superlinear, or threshold effects are plausible. The profiled binary must match the artifact whose behavior is being improved. Instrumentation is useful for exact phases, state tags, and operations too short or rare for sampling. Attribution requires one causal change, stable workload, semantic oracle, and before/after evidence. A cache can reduce CPU while consuming memory and invalidation capacity. The complete chain is workload → shipped profile → hypothesis → isolated change → local measurement → end-to-end measurement → semantic and resource revalidation → decision record.

## Deep reasoning and transfer

### Decisive model

> Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?

Build a **profile and cost model**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Read call stacks and flame graphs without confusing inclusive cost with exclusive cost.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Separate algorithmic work from parsing, allocation, hashing, formatting, synchronization, and system calls.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Form a cost hypothesis that predicts how runtime changes with input size and distribution.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Design a focused experiment that can falsify the hypothesis.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the profile and cost model.

### Reference implementation comparison

For [Profile-Guided Query Engine](../../labs/module-02-profile-guided-query-engine/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In MetricRail, Module 82 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **CPU Profiling, Cost Models, and Hot-Path Optimization**, which relationship decides this question: “Where does execution time actually go, why does it go there, and which change removes the dominant cost without moving it into an unmeasured phase?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to MetricRail?
