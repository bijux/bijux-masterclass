# Laboratory 81 — Benchmark Integrity Clinic

**Course 9 · Module 81: Performance Contracts, Workloads, and Benchmark Design**

[Chapter](../../course-book/module-81-performance-contracts-workloads-and-benchmark-design/index.md) · [Workbook](../../course-book/module-81-performance-contracts-workloads-and-benchmark-design/workbook.md) · [MetricRail guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Performance Contracts, Workloads, and Benchmark Design**: What exactly must become faster, under which workload and resource limits, and what experiment would distinguish improvement from noise or self-deception? The product must make **Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **performance claim and workload record** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a small checksum measurement harness whose operation boundary cannot be confused with fixture construction or correctness validation. The starter already provides a checksum and a one-shot smoke timer. Your task is to turn it into an honest experimental unit—not to pretend one elapsed duration is a statistically stable benchmark.

The product accepts a named `Workload` containing bytes and a nonzero iteration count. It returns an `Observation` with elapsed time, the consumed result, and checked bytes processed. It also exposes a small parameterized workload family. The harness must make enough information visible that another reader can reproduce the exact operation and reject invalid comparisons.

## Contract

Preserve the checksum algorithm and its result. `measure` must:

- reject zero iterations;
- compute `bytes.len() × iterations` with checked arithmetic before timing;
- start the clock only after the workload is already constructed and validated;
- prevent the compiler from treating input/result as irrelevant;
- execute the checksum exactly the declared number of times;
- return a result equal to the independent `expected_result` oracle;
- never label the observation a percentile, throughput capacity, or production guarantee.

`parameterized_workloads` must include at least three materially different input sizes with stable names. Avoid “small/medium/large” without exact bytes.

## Why this laboratory is difficult

It is easy to produce a number. It is harder to say what the number measures. If allocation is inside one implementation’s timed interval and outside the other’s, the harness compares different operations. If the result is unused, optimization can remove work. If correctness is not checked, a faster wrong implementation can win. If a one-shot timer is reported as a regression threshold, environmental noise is mistaken for product behavior.

The key distinction is between **smoke measurement** and **benchmark evidence**. This crate intentionally stops at the first. You must document what additional sampling, environment control, and statistical interpretation would be needed for the second.

## Construction route

1. Define `Workload` and `Observation` with explicit units and names.
2. Implement `expected_result` without relying on the measured loop’s state.
3. Validate count and checked byte arithmetic before `Instant::now`.
4. Execute the operation while consuming input and output through `black_box` or an equivalent observable use.
5. Verify the result after the timed region.
6. Add parameterized workloads for 64 bytes, 4 KiB, and 64 KiB or another justified family.
7. Add tests for stable checksum, zero iterations, and exact accounting.
8. Write a short report that names source revision, profile, host context, workload, operation boundary, and limitations.

## Adversarial cases

Test an empty byte slice with nonzero iterations, one iteration, even and odd counts, multiplication overflow, and a large but legal input. Empty bytes are not the same as zero work: the checksum function still executes. Do not allocate a fresh input inside the measured loop merely to make the workload “realistic.”

## Experiment

Run the workload family in the same process and record elapsed time and bytes processed. Compute a derived bytes-per-second value only as a local observation. Repeat the whole run and note how much it moves. Explain why the experiment cannot establish service throughput, tail latency, cross-host performance, or a three-percent CI gate.

## Transfer

Design a second harness for a parser. Separate fixture loading, parsing, validation, and result consumption. Provide two legitimate boundaries: parser-only and end-to-end import. The two measurements may differ dramatically while both remain correct because they answer different questions.

## Completion

The laboratory is complete when invalid workloads fail before timing, arithmetic cannot wrap, the oracle detects semantic drift, setup is outside the named operation, all tests pass, and the report states both the supported claim and the unsupported conclusions.

Only after completing your own design should you inspect `solution/`. Compare the placement of setup and validation, the accounting invariant, and the limitation statement—not line count or naming style.

## Required measurement record

Submit one compact benchmark report containing the benchmark question, hardware and operating environment, exact Rust toolchain and profile, input generator, warm-up policy, sample count, outlier treatment, and raw result location. Include at least one negative control that should not improve and one semantic oracle checked before and after timing. Interpret the confidence interval rather than reporting only a single percentage. If the candidate and baseline distributions overlap materially, record the result as inconclusive rather than manufacturing a winner.

The report must also name one source of systematic bias that repetition cannot remove—for example a different allocator configuration, stale build artifact, changing corpus, or benchmark setup included on only one side. State how the design prevents or detects it.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Benchmark Integrity Clinic**.
2. Draw the smallest **performance claim and workload record** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to MetricRail so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle.
- Separate latency, throughput, utilization, memory footprint, startup cost, binary size, and tail behavior instead of combining them into one score.
- Design microbenchmarks that exclude setup and validation costs unless those costs belong to the product operation.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 81 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **performance claim and workload record**. Defend why your design is simpler than one plausible alternative under the new requirements.
