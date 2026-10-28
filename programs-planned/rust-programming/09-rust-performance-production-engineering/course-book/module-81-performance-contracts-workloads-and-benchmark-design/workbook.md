# Workbook — Module 81: Performance Contracts, Workloads, and Benchmark Design

[Chapter](index.md) · [Laboratory](../../labs/module-01-benchmark-integrity-clinic/README.md) · [MetricRail guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Performance Contracts, Workloads, and Benchmark Design** has become a usable model rather than remembered vocabulary. Its governing question is: *What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?* Preserve your first prediction and record decisive facts in a **performance claim and workload record**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 80 — Integrated Async Service Architecture, Testing, and Audit that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?**
3. Draw the smallest **performance claim and workload record** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

### 1. Setup or product work?

A benchmark compares two telemetry parsers. The first iteration constructs a 64 KiB input string, parses it, and drops the result. The second parser receives a prebuilt `&str`, parses it, and returns borrowed fields. Predict which parser appears faster and explain why the comparison cannot yet support a parser-performance claim.

Then state two legitimate product boundaries for which different placements of input construction would both be correct.

### 2. Same answer, different product

Implementation A rejects trailing fields and reports the physical source line. Implementation B ignores trailing fields and returns the first two values. B is 22% faster on the current corpus. Is “B is a faster implementation of A” a valid conclusion? List every semantic property that must be held constant before the result can be compared.

### 3. Median, tail, and throughput

A service change reduces median ingestion latency from 180 μs to 150 μs, increases p99 from 2.1 ms to 7.8 ms, and raises saturated throughput by 8%. Predict which product policies could rationally accept the change and which should reject it. Do not choose a winner without naming the workload and objective.

### 4. A three-percent CI gate

A team proposes failing CI whenever a microbenchmark is 3% slower than yesterday. Predict the false-positive and false-negative modes. What evidence would be needed before a non-negotiable requirement becomes defensible?

### 5. Representative skew

Production traffic is 82% short valid records, 12% repeated hot-tenant records, 4% maximum-length valid records, and 2% malformed records. The benchmark uses uniformly random valid records of one length. Predict which costs it is likely to hide.

### 6. Optimizer visibility

A benchmark computes a checksum and discards it. Another sends the input and result through `std::hint::black_box`. Explain what each benchmark permits the optimizer to remove. State clearly what `black_box` does **not** guarantee.

## Part 2 — Diagnose and repair

### Case A — Setup contamination

```rust
b.iter(|| {
    let input = std::fs::read_to_string("corpus.tsv").unwrap();
    parse(&input).unwrap()
});
```

The report claims parser latency. Diagnose the measured operation. Rewrite the experiment boundary for:

1. parser-only latency;
2. end-to-end file-import latency.

### Case B — The faster invalid parser

An optimization replaces checked decimal parsing with unchecked byte arithmetic. It is faster on valid input but silently wraps on overflow. Write the smallest repair that preserves the original performance question. Explain why “the input is trusted in practice” is not a repair unless the public contract changes.

### Case C — A noisy baseline

Twenty measurements alternate between two clusters. The author averages them and reports a 6% improvement. Give at least four plausible causes of the two modes and a procedure for deciding whether they represent environmental noise, warm/cold state, or two real product paths.

### Case D — Benchmarking only the toy case

A new index wins on 32 records and loses on 10,000. The published chart contains only the 32-record result. Design a parameterized experiment that reveals the crossover point and includes the index build cost where relevant.

## Part 3 — Focused exercises

### Exercise 1 — Define one falsifiable claim

Write a performance contract for parsing one MetricRail line. It must include:

- exact operation boundary;
- release profile and target class;
- at least four workload parameters;
- primary metric and one displaced-cost metric;
- semantic oracle;
- resource limit;
- baseline identity;
- conditions that make the result invalid.

### Exercise 2 — Design a corpus family

Design four versioned corpora:

1. common production shape;
2. adversarial-but-valid shape;
3. legal boundary shape;
4. malformed shape.

For each, state what mechanism it exercises and why a uniform random generator would be insufficient.

### Exercise 3 — Separate benchmark layers

Design three related experiments for the same operation:

- a microbenchmark;
- a scenario benchmark;
- a saturation/load experiment.

State what each can conclude and what it cannot conclude.

### Exercise 4 — Write a regression decision record

Assume a candidate is 11% faster in a microbenchmark, unchanged end to end, and uses 19% more retained memory. Write a release recommendation. Include the decision owner, uncertainty, and next experiment.

### Interleaved reasoning pass

1. For **Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the performance claim and workload record.
2. For **Separate latency, throughput, utilization, memory footprint, startup cost, binary size, and tail behavior instead of combining them into one score**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the performance claim and workload record.
3. For **Design microbenchmarks that exclude setup and validation costs unless those costs belong to the product operation**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the performance claim and workload record.
4. For **Choose warm-up, sample, batching, parameterization, and baseline policy deliberately**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the performance claim and workload record.

5. Identify one guarantee from an earlier course that a careless implementation of **Performance Contracts, Workloads, and Benchmark Design** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build the [Benchmark Integrity Clinic](../../labs/module-01-benchmark-integrity-clinic/README.md). Before looking at its reference implementation:

- preserve the checksum oracle;
- reject zero iterations and checked byte-count overflow;
- keep workload construction outside the measured loop;
- make the consumed byte count explicit;
- parameterize at least three input sizes;
- separate the smoke timer from any statistical performance claim.

Your report must include the exact code revision, workload name, bytes processed, result, elapsed time, and a paragraph explaining what the observation cannot establish.

### Laboratory acceptance trace

Before opening the reference implementation for **Benchmark Integrity Clinic**, record:

- the public behavior that demonstrates **Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Create `PERFORMANCE_CHARTER.md` for MetricRail and add benchmark fixtures for line parsing, batch ingestion, snapshot rendering, and end-to-end TCP ingestion. Define:

- the semantic oracle for each path;
- which setup occurs once and which occurs per operation;
- the normal, boundary, malformed, and skewed workloads;
- the primary and secondary metrics;
- the reference profile, toolchain, target, and dependency lock;
- the policy for recording a baseline without making noisy CI timing a unit-test assertion.

No production optimization is allowed in this increment. The product of Module 81 is trustworthy experimental infrastructure.

### Capstone invariant trace

For the Module 81 MetricRail increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Without notes, answer:

1. What five terms make a benchmark claim interpretable?
2. When is setup legitimately inside the measured interval?
3. Why can equal outputs still represent different products?
4. What does a correctness oracle protect during optimization?
5. Why is a distribution more informative than one elapsed duration?
6. How do microbenchmarks, scenarios, and load tests complement one another?
7. What environmental metadata belongs beside a baseline?
8. Name one result you would refuse to publish and explain why.

Continue only when you can design the experiment before seeing the number.

### Closed-book defense

In five minutes, answer “What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?” using the **performance claim and workload record**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside MetricRail. A list of APIs without the deciding relationship is incomplete.
