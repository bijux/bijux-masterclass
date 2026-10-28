# Reasoned Solutions — Module 81: Performance Contracts, Workloads, and Benchmark Design

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-01-benchmark-integrity-clinic/README.md) · [MetricRail guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 81: Performance Contracts, Workloads, and Benchmark Design**. Compare the reasoning against this question: *What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction reasoning

### 1. Setup or product work?

The first parser is charged for file-independent input allocation and initialization while the second is not. The result mainly compares two **different operations**. A parser-only benchmark should construct and validate fixtures before the timed loop, then time only parsing. An end-to-end request benchmark may legitimately include receiving or constructing the request because the product pays that cost on every request. A startup benchmark may include corpus loading when startup is the product boundary. The rule is not “setup always outside”; it is “the timed interval must equal the named operation.”

### 2. Same answer, different product

B is not an implementation of A because it changes accepted language and failure evidence. A valid comparison must preserve at least field-count validation, numeric range behavior, UTF-8 policy, line-number reporting, ordering, duplicate handling, overflow semantics, trailing-byte policy, limits, and output representation. If the product intentionally adopts B’s grammar, that is an API or data-format change requiring versioning and migration before it becomes a performance comparison.

### 3. Median, tail, and throughput

A batch-oriented internal pipeline with spare deadline budget might accept the change because saturated throughput is primary and the p99 remains below its deadline. An interactive ingestion endpoint with a 3 ms tail objective should reject it. A cost-minimization policy might request CPU-utilization data before deciding. The example proves why one scalar “performance score” is inadequate: the change improves common-path latency and throughput while worsening rare-path delay.

### 4. A three-percent CI gate

Ordinary shared CI hosts often vary by more than three percent because of scheduling, frequency scaling, thermal state, neighboring workloads, allocator state, and toolchain changes. The gate will fail good changes and miss real regressions hidden by a favorable run. A defensible non-negotiable requirement needs a controlled runner, stable workload and profile, repeated samples, a historical noise model, a minimum practical effect size, semantic tests, and a review route for borderline cases. Even then, broad scenario regressions often deserve a report rather than an automatic block.

### 5. Representative skew

The uniform corpus hides short-record dominance, hot-key cache and contention behavior, maximum-length allocation and branch paths, and malformed-input validation cost. It may also hide repeated identifier retention and cardinality growth. A representative suite does not need to reproduce every production request; it must preserve the mechanisms that dominate cost and risk.

### 6. Optimizer visibility

If the checksum result is unused, the compiler may prove that some or all computation has no observable effect and remove it. `black_box` inhibits selected optimizer assumptions at that boundary and makes dead-code elimination less likely. It does not create a hardware barrier, guarantee identical machine code across compilers, prevent all constant propagation, or make an unrealistic workload representative.

## Part 2 — Repairs

### Case A

For parser-only latency, load the corpus once, keep it outside the timed loop, and consume the result:

```rust
let input = std::fs::read_to_string("corpus.tsv")?;
b.iter(|| {
    let records = parse(std::hint::black_box(&input))?;
    std::hint::black_box(records);
    Ok::<_, ParseError>(())
});
```

For end-to-end import, file open, reading, parsing, and validation all belong inside, but the file should be reset or reopened consistently for every sample. The report should call this “file import,” not “parser latency.” OS page-cache state must be recorded because a warm cached file and a cold durable read are different workloads.

### Case B

Restore checked arithmetic and benchmark the same grammar. If decimal conversion is suspected, compare two checked decoders against an oracle covering zero, signs, boundaries, overflow, malformed bytes, and trailing data. “Trusted input” becomes defensible only if the boundary is moved behind a validator whose cost is included somewhere and the public documentation makes the new assumption explicit.

### Case C

Two clusters may indicate warm versus cold cache, allocator reuse, CPU frequency modes, background interference, or two input/state paths. Tag every sample with corpus case, cache state, batch size, and relevant internal counters. Randomize or block the execution order, inspect time sequence rather than only a histogram, run on an isolated host, and correlate clusters with product state. If clusters correspond to real states, report both; averaging them destroys the causal information.

### Case D

Parameterize document count, query selectivity, token count, and number of repeated queries. Report index construction separately and amortize it over realistic query counts. Include a linear oracle and compare total cost:

```text
T_linear(n, q) = q × scan(n)
T_indexed(n, q) = build(n) + q × lookup(n)
```

The crossover is the smallest workload where indexed total cost wins while memory remains within budget. Publishing only the winning 32-record point is selection bias.

## Part 3 — Model answers

### Exercise 1

A defensible charter could read:

> On the pinned Rust 1.97.1 toolchain, `profiling` profile, and reference x86-64 host, decode one valid MetricRail line from an already received byte slice. Measure median and p95 wall time for lengths 24, 128, 1,024, and the configured maximum; use common, hot-tenant, boundary, and malformed corpora. Preserve exact parse result, error class, source offset, identifier validation, and numeric overflow behavior against the reference parser. Record allocations per operation as the displaced-cost metric. Reject a candidate that exceeds the configured line or identifier allocation budget. Compare only against a baseline with the same corpus digest, lockfile, target, profile, and CPU governor.

Invalidators include changed corpus, changed semantics, thermal throttling, toolchain/profile changes, or a result below the established noise floor.

### Exercise 2

- **Common:** short ASCII identifiers and ordinary timestamps/values, weighted by observed production frequencies. Exercises branch and token patterns actually paid most often.
- **Adversarial valid:** maximum legal identifiers, extreme numeric values, hot repeated tenant/metric keys, and legal whitespace/format boundaries. Exercises worst legal work and retention.
- **Boundary:** exactly maximum line length, identifier length, record count, and checked numeric endpoints. Exercises off-by-one and allocation-before-validation defects.
- **Malformed:** missing fields, extra fields, invalid UTF-8 where applicable, overflow, empty names, and over-limit lines. Exercises rejection cost and causal errors.

Uniform random bytes do not preserve grammar or observed skew and often spend time in irrelevant early-rejection paths.

### Exercise 3

A microbenchmark isolates parse mechanics and can compare implementations under controlled inputs. It cannot establish service capacity. A scenario benchmark includes request framing, parsing, aggregation, and rendering for a named workflow; it reveals displaced costs but still lacks concurrency and saturation. A load experiment varies offered load, connection count, queue capacity, and key skew; it can identify saturation, tail latency, and overload behavior, but is less precise for one instruction-level change. Together they connect mechanism to product behavior.

### Exercise 4

The candidate should not be released as a performance improvement yet. The end-to-end path is unchanged and retained memory is materially worse, so the microbenchmark gain is not currently product-relevant. Record the negative result, profile the scenario to determine whether the microbenchmarked phase is dominant, and measure whether the memory increase reduces safe capacity. Release only for another independent reason or after evidence connects the local gain to an accepted product objective.

## Part 4 — Laboratory review

A strong implementation keeps `Workload` construction outside `measure`, rejects zero iterations, computes `bytes_processed` with checked multiplication, consumes the checksum result, and verifies it against `expected_result`. The `Observation` is a smoke observation—not a statistical benchmark result. The most important sentence in the report is the limitation: one duration on one host cannot establish a stable regression threshold or production throughput.

## Part 5 — MetricRail transfer

The charter should keep four distinct routes: parser microbenchmarks, batch/aggregation scenarios, snapshot scenarios, and TCP load tests. Each route needs its own oracle and environment record. The baseline should be stored with source revision, corpus digest, toolchain, lockfile, target, profile, and parameters. CI may verify that the harness runs and semantics hold; timing changes should be analyzed through a controlled regression workflow rather than nanosecond assertions in ordinary tests.

## Part 6 — Defense

The five terms are operation, workload, environment, metric, and correctness oracle. Setup belongs inside only when the named product operation pays it. Equal outputs may still differ in accepted input, error semantics, ordering, limits, or resource behavior. The oracle prevents optimization from silently changing those properties. Distributions expose variability and tail paths. Microbenchmarks identify mechanisms, scenarios expose integration costs, and load tests expose saturation. Baselines need source, toolchain, profile, target, lockfile, corpus, parameters, and host conditions. Refuse to publish any result whose boundary or comparison changed after measurements were seen.

## Deep reasoning and transfer

### Decisive model

> What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?

Build a **performance claim and workload record**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Separate latency, throughput, utilization, memory footprint, startup cost, binary size, and tail behavior instead of combining them into one score.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Design microbenchmarks that exclude setup and validation costs unless those costs belong to the product operation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Choose warm-up, sample, batching, parameterization, and baseline policy deliberately.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Detect dead-code elimination, constant folding, cache-only workloads, allocator contamination, and benchmark-driven semantic drift.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the performance claim and workload record.

### Reference implementation comparison

For [Benchmark Integrity Clinic](../../labs/module-01-benchmark-integrity-clinic/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In MetricRail, Module 81 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Performance Contracts, Workloads, and Benchmark Design**, which relationship decides this question: “What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to MetricRail?
