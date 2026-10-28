# Module 81 — Performance Contracts, Workloads, and Benchmark Design

**81/90** · Course 9 · Module 81 of 90

[Course 9 overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [MetricRail guide](../capstone.md)

## The question

> What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception?

## Why this comes now

Courses 1–8 gave you enough Rust to change almost any local mechanism. That power creates a new risk: improving something that was never the product bottleneck, or comparing two implementations that no longer mean the same thing. Module 81 establishes the discipline that every later module depends on. Before you profile, pool, batch, cache, strip, retry, or roll out, you must state which operation matters and what evidence could justify the change.

A performance contract is not a universal promise that code is “fast.” It is a decision rule tied to a workload and environment. It says which semantics remain fixed, which costs matter, which inputs represent the product, and what regression is unacceptable. Without that contract, faster numbers can reward weaker validation, smaller inputs, warmer caches, different profiles, or work moved outside the timer.

## What you will be able to do

After completing this module, you will be able to:

- turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle
- separate latency, throughput, utilization, memory footprint, startup cost, binary size, and tail behavior instead of combining them into one score
- design microbenchmarks that exclude setup and validation costs unless those costs belong to the product operation
- choose warm-up, sample, batching, parameterization, and baseline policy deliberately
- detect dead-code elimination, constant folding, cache-only workloads, allocator contamination, and benchmark-driven semantic drift
- interpret distributions and confidence rather than trusting one timing value
- decide when a benchmark is too synthetic and must be complemented by a scenario or load test

## Core model

### The governing model

A benchmark is a controlled comparison, not a stopwatch. Model it as `claim = operation × workload × environment × metric × correctness`. If any term is missing, the number cannot support a production decision. The workload names input shapes and distributions. The environment names target, profile, features, and competing load. The metric names what is measured and how it is summarized. The correctness oracle proves that both implementations still compute the required result.

### 1. The contract before the clock

A performance requirement must identify an operation and a service boundary. “Parsing is slow” is not actionable. “Decode a valid 128-byte telemetry line under the release profile with no more than two heap allocations and a median below the recorded baseline on the reference host” is testable. The contract also states what may not change: accepted grammar, error offsets, ordering, overflow behavior, and resource limits.


### 2. Metric families are not substitutes

Latency answers how long one operation takes. Throughput answers how many operations complete per unit time. Utilization explains how much CPU or another resource was consumed. Memory footprint distinguishes retained state, temporary peaks, and allocation churn. Tail percentiles expose rare slow paths that averages hide. A change can improve one family while damaging another, so the decision table must state priority and acceptable trade-offs.


### 3. Workload design is product modeling

Uniform random input is rarely representative. Real workloads contain skew: common short records, occasional long labels, hot tenants, repeated keys, malformed lines, bursts, and quiet periods. Parameterized benchmarks should include a normal case, an adversarial-but-valid case, a boundary case, and a malformed case when failure performance matters. Corpora must be versioned because changing a corpus changes the experiment.


### 4. Measurement boundaries

Place setup outside the timed operation unless the product pays setup on every request. Put input construction, file loading, and expected-result calculation in fixtures when the claim concerns only the algorithm. Conversely, include allocation, decoding, synchronization, or rendering when those are part of the user-visible operation. Use black-boxing or consumed outputs so the optimizer cannot remove the work.


### 5. Baselines and noise

A baseline is meaningful only when environment and workload are comparable. Record compiler version, target, profile, features, dependency lockfile, hardware class, and benchmark parameters. Random noise, thermal changes, turbo behavior, background processes, and allocator state can move results. Use distributions and repeated samples; do not declare victory from one favorable run.


### 6. Correctness remains the first gate

Optimization cannot redefine the product silently. Every benchmarked path needs an oracle: a reference implementation, invariant checks, property tests, or exact expected output. A faster parser that accepts malformed records, loses source order, or changes overflow policy has failed. Benchmark assertions need not be inside the timed region, but they must run.

The benchmark therefore has two outputs. The obvious output is a distribution of observations. The more important output is a defensible comparison: both candidates performed the same product operation, against the same corpus, under the same profile and resource policy, and the observed difference was large enough to cross a threshold chosen before the result was known.

### A module-specific decision table

| Design question | Evidence that can answer it | Result that invalidates the conclusion |
|---|---|---|
| Is parsing itself costly? | in-memory parser benchmark with exact-output oracle | file I/O or corpus construction occurs inside one candidate only |
| Does the change help realistic records? | parameterized common, boundary, malformed, and skewed corpora | only one tiny constant input was measured |
| Is the gain product-relevant? | end-to-end ingestion scenario | microbenchmark gain disappears or tail latency worsens |
| Is the result stable? | repeated samples, distribution, baseline history | difference is smaller than normal run-to-run variation |
| Are semantics preserved? | differential tests and invariant checks | accepted grammar, ordering, errors, or limits change |
| Was cost displaced? | allocation, CPU, memory, and output-size checks | local latency improves by retaining more memory or doing later work |

### Working procedure

1. Write the operation as a sentence with a start and end boundary. “Parse one already received line into a validated record” is different from “receive, parse, commit, and acknowledge one record.”
2. List the semantic invariants that both implementations must satisfy. Make the oracle executable before timing either candidate.
3. Build a workload matrix from product behavior: common records, hot identifiers, maximum valid records, malformed records, and any distribution that exercises failure cost.
4. Freeze the environment: toolchain, target, Cargo profile, features, lockfile, corpus digest, and relevant host settings.
5. Separate fixture construction, measured work, and post-measurement validation. Consume outputs so the compiler cannot erase the operation.
6. Choose the metric and decision threshold before seeing results. Report absolute values and uncertainty, not only percentages.
7. Confirm the chosen change in a scenario that includes the surrounding queues, allocation, synchronization, and response path.

### Failure patterns and principled repairs

#### A single `Instant` measurement is treated as a benchmark result. It is a useful smoke measurement, but it gives no stable comparison, distribution, warm-up, or noise estimate.

A single timing is a smoke check, not a comparison. Keep it for local feedback, then replace it with repeated measurements and an explicit baseline before using it to choose an implementation.

#### The optimized implementation changes input validation or ordering and is still compared against the old baseline. The experiment no longer measures the same product.

Once validation or ordering changes, the experiment has two variables: semantics and implementation. Restore one oracle and compare only candidates that pass it.

#### Only the tiny happy path is benchmarked, so the chosen design overfits caches and branch prediction while large or malformed production inputs regress.

A tiny happy path measures a narrow cache and branch regime. Add boundary, malformed, and skewed corpora before treating the result as a product claim.

#### Setup is accidentally included for one implementation and excluded for the other.

Asymmetric setup can dominate the result while appearing to measure the algorithm. Move equivalent setup outside the measured region or include it for both because the product pays it.

#### A percentage improvement is reported without absolute values; a 50% gain may be irrelevant if the operation changed from two nanoseconds to one.

Percentages hide scale and relevance. Report absolute latency or throughput, variance, and the product threshold that makes the difference worth maintaining.

## Use the idea in a complete program

```rust
use std::hint::black_box;
use std::time::{Duration, Instant};

fn checksum(bytes: &[u8]) -> u64 {
    bytes.iter().fold(0_u64, |acc, &b| acc.wrapping_mul(16_777_619) ^ u64::from(b))
}

fn sample_operation(input: &[u8], iterations: usize) -> (Duration, u64) {
    let started = Instant::now();
    let mut result = 0_u64;
    for _ in 0..iterations {
        result ^= checksum(black_box(input));
    }
    (started.elapsed(), black_box(result))
}

fn main() {
    let input = vec![b'x'; 4096];
    let (elapsed, result) = sample_operation(&input, 10_001);
    assert_ne!(result, u64::MAX);
    println!("{elapsed:?}");
}
```

The checksum program demonstrates only how to keep a result observable and how to time a repeated operation. It does not warm up intelligently, estimate variance, control the host, or prove that the input represents MetricRail. Its most useful feature is the visible boundary: allocation happens before `sample_operation`, while checksum work occurs inside it.

Change the example in three ways. First, parameterize input length rather than measuring one constant buffer. Second, compare its result with a simple oracle before timing. Third, record enough samples to see whether the difference between two checksum implementations is larger than ordinary noise. Those changes still do not create a production benchmark, but they teach you to stop smuggling assumptions into the measured region.

### MetricRail consequence

Module 81 creates MetricRail’s performance charter before any optimization. Define three operations separately: borrowed line parsing, committing one validated record to the store, and rendering a deterministic snapshot. Each operation gets its own oracle and workload matrix. The service-level scenario then measures the complete `INGEST` path so a local gain cannot hide queueing or response costs.

Version the telemetry corpus and record its digest. Include short common identifiers, repeated hot series, maximum-length identifiers, new-series churn, malformed numbers, and old timestamps. The malformed cases remain part of the benchmark plan because rejection consumes resources and can become an attack surface.

Do not add a portable nanosecond gate. The teaching release instead records relative regression on a controlled host, absolute resource ceilings, and a scenario-level acceptance rule. A candidate parser is rejected if it changes error classes, source-line behavior, finite-value policy, or allocation bounds, even when it benchmarks faster.

### Boundary case: a faster parser with a changed failure population

Suppose the candidate parser is 18% faster on valid 128-byte lines. During differential testing, it also accepts leading `+` on timestamps, while the baseline rejects that syntax. If the benchmark corpus contains only valid positive timestamps, the numerical result is stable and repeatable—but it compares different languages. The candidate may receive more work in production because records previously rejected now enter validation, lookup, storage, and snapshot paths.

The correct response is not to add the newly accepted syntax to the benchmark and continue. First decide whether the product grammar should change. If it should not, repair the candidate and rerun the exact comparison. If it should, treat that as a separate compatibility decision with protocol tests, release notes, and new workload populations. The original speed result cannot authorize both changes at once.

Now add a second complication: the candidate allocates fewer objects but retains a 4 KiB input buffer for every accepted record. Module 81 does not yet solve the memory design, but its contract must name retained memory as a displaced-cost gate. This is why the charter precedes the implementation. It forces later evidence to answer the whole decision rather than the easiest metric.

## Practice sequence

1. Rewrite one vague complaint—such as “snapshots are slow”—as a contract naming operation, workload, profile, percentile, memory limit, and correctness oracle.
2. Build a four-class corpus and freeze its digest. Explain why every class exists.
3. Run the focused checksum example and identify three conclusions it cannot support.
4. Complete the Benchmark Integrity Clinic. In the comparison report, separate invalid experiment, inconclusive result, and product-relevant regression.
5. Add MetricRail benchmark groups for parse, first-series insert, existing-series update, and snapshot rendering. Keep setup symmetrical.
6. Run one end-to-end ingestion scenario and write a decision record that either accepts the candidate, rejects it, or requests one discriminating experiment.

Use the [workbook](workbook.md) to freeze predictions and complete the causal repairs. Build the module laboratory before reading its reference implementation, then transfer the mechanism into the [MetricRail engineering guide](../capstone.md).

## Ready to continue

Continue only when you can:

- state one performance contract without using the word “fast”;
- design a workload matrix that includes normal, boundary, malformed, and skewed input;
- separate setup, measured work, and validation for two candidates;
- explain which environment facts make a result non-portable;
- reject a faster result when semantics or a resource contract changed;
- name the end-to-end scenario required before a microbenchmark can guide MetricRail.

## Primary Rust references

- The Rust standard library documentation for `std::hint::black_box` and `std::time::Instant`
- The Criterion.rs user guide for statistical benchmarking and parameterized benchmark groups
- Cargo documentation for build profiles and benchmark targets

These references are for verification and deeper lookup after the chapter’s model is understood. The course-book chapter remains the complete learning route for the required concepts.

## Continue

1. Complete the [Module 81 workbook](workbook.md).
2. Use the [reasoned solutions](solutions.md) only after writing your own answers.
3. Build the [Benchmark Integrity Clinic laboratory](../../labs/module-01-benchmark-integrity-clinic/README.md).
4. Apply the module to [MetricRail](../capstone.md).
