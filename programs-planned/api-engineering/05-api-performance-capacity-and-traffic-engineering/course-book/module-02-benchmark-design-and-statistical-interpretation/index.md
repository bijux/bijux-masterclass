# Module 02 — Benchmark Design and Statistical Interpretation

> **Program stage:** Course 5 of 10 — Sustain the promise under pressure.

> **Central question:** How do open and closed demand, warmup, sample size, missing outcomes, variation, and statistical uncertainty change benchmark meaning?

## Where this module fits

Module 01 produced **Freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines**. This module extends that result by asking: **How do open and closed demand, warmup, sample size, missing outcomes, variation, and statistical uncertainty change benchmark meaning?**

The new capstone increment is **Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons**. It becomes the prerequisite for **HTTP Efficiency and Representation Cost**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Distinguish load generation, timing, outcome collection, and analysis.
- Design open and closed schedules and explain their different questions.
- Detect coordinated omission using intended start times.
- Choose warmup and measurement windows from observed behavior.
- Calculate nearest-rank quantiles and explain alternative algorithms.
- Separate run-to-run variability from within-run latency distribution.
- Use bootstrap intervals over independent run summaries cautiously.
- Declare regression thresholds before seeing candidate results.

## Capstone increment

Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons.

## Core performance model

### 1. The harness is part of the experiment


The client can saturate before the server. DNS, connection creation, TLS, serialization, logging, and result storage can consume time and CPU. A trustworthy report records client-side resource use and checks whether scheduled work was actually started.

Separate four stages:

```text
schedule intended arrival
→ start request attempt
→ observe terminal outcome
→ analyze recorded events
```

Each stage has its own timestamp. The harness should use a monotonic clock for durations and wall-clock time only for correlation. It must not generate request identifiers or payloads inside the timed region unless that cost is intentionally part of the workload.


### 2. Coordinated omission


Coordinated omission occurs when a generator waits through a slow period and therefore fails to record requests that should have arrived during that period. A closed loop naturally records one long request, while an open schedule would have offered several requests and observed queueing or rejection.

The course’s open scheduler stores both `scheduled_ns` and `started_ns`. Queue delay at the client is `started_ns - scheduled_ns`. If the harness cannot start work on schedule, that delay is evidence, not noise to discard.

Some tools provide scenario executors designed for constant arrival rates. Even then, record dropped or delayed iterations. An executor name does not guarantee that the client had enough resources.


### 3. Warmup and steady state


Early measurements may include process startup, connection establishment, JIT or adaptive runtime effects, filesystem cache population, database buffer warming, and lazy imports. Blindly discarding the first minute is no better than blindly retaining it.

Plot or inspect rolling throughput, latency, CPU, memory, pool use, and cache state. Define warmup completion by a stated condition or a fixed policy justified by evidence. Then separate warmup data from the measurement window rather than deleting it.

For release regression, a cold-start workload may itself be critical. In that case, measure it as a separate named workload rather than hiding cold behavior inside warm steady-state results.


### 4. Latency distributions and quantiles


The mean is sensitive to extreme values and often hides multimodal behavior. Quantiles describe the observation below which a fraction of samples falls, but algorithms differ.

Course vectors use nearest rank:

```text
sort samples ascending
rank = ceil(p × n)
value = samples[rank - 1]
```

For `[10, 20, 30, 40]`, p50 is rank 2, value 20; p95 is rank 4, value 40. A linear-interpolation library may report different values. Store the algorithm with the result.

A p99 from 100 samples is effectively one of the slowest observations. Tail claims need enough samples and repeated runs. Retain histograms or raw samples when storage and privacy allow.


### 5. Within-run and between-run variation


A latency distribution within one run describes requests under that run’s conditions. Variation across independent runs describes reproducibility and environmental noise. Do not merge ten runs into one giant sample and pretend they were one continuous population.

For a release comparison, compute each run’s summary, then compare run summaries. A deterministic bootstrap over independent run-level p95 or throughput values can provide an interval for the difference, but it does not rescue a biased workload or correlated runs.

The capstone requires at least three baseline and three candidate runs for a local regression exercise. In a noisy environment, more runs or a controlled environment may be necessary.


### 6. Thresholds and practical significance


A statistically detectable change may be operationally irrelevant. A 0.5 ms improvement on a 200 ms budget may not justify complexity. Conversely, a 5% p99 regression near an SLO boundary may be important even with limited statistical power.

Define thresholds before inspecting candidate results:

- correctness must pass;
- error and rejection deltas must stay within zero or a named budget;
- p95 regression may not exceed a percentage and absolute amount;
- throughput improvement must exceed a practical minimum;
- CPU or memory increase must remain within a budget.

Use both absolute and relative thresholds to avoid unstable behavior near zero.


### 7. Reproducibility and raw evidence


A summarized report should be derivable from retained events or histograms. Store tool version, command, scenario, random seed, environment, time windows, and dropped work. If raw request data contains sensitive identifiers, pseudonymize or aggregate it before retention.

A benchmark that cannot be rerun is a demonstration, not a regression gate. The capstone harness emits a stable envelope format independent of k6, Locust, Python, or Node. Tool adapters map their output into that format.

## Course requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Monotonic duration clock | Elapsed durations use a monotonic high-resolution clock. | Wall-clock adjustment creates negative or distorted latency. | Clock tests and event schema |
| Intended starts retained | Open workloads record scheduled and actual start times. | Coordinated omission is invisible. | Schedule trace |
| Dropped work counted | Client-side dropped or delayed iterations are first-class outcomes. | Generator saturation looks like server health. | Outcome conservation |
| Warmup separated | Warmup policy and measurement window are stored. | Startup and steady state are blended opportunistically. | Envelope windows |
| Algorithm named | Quantile and histogram algorithms are recorded. | Different summaries are compared as identical. | Statistics profile |
| Independent runs preserved | Run-level identities and summaries remain separate. | Correlated samples create false confidence. | Run series |
| Thresholds predeclared | Regression policy exists before candidate data is inspected. | Decision boundary is moved after seeing results. | Release profile |
| Raw derivation possible | Summary can be recomputed from retained events or buckets. | Calculation cannot be audited. | Replay test |

## Worked failures

### Case 1 — The pause hidden by a closed loop

**Initial condition.** The server freezes for two seconds. Ten closed users each record one two-second request and then continue.

**Analysis.** An external arrival stream of 100 requests/s would have offered roughly 200 requests during the pause. The closed loop did not generate or count them.

**Correct response.** Run an open schedule, retain intended arrival times, and record delayed/dropped starts and server queueing.

**Lesson.** One long latency sample can hide a large backlog.

### Case 2 — The average improvement

**Initial condition.** Mean latency improves 10%, but p95 regresses 35% and errors rise from 0 to 1%.

**Analysis.** The average is dominated by the common fast path. The user-visible tail and correctness worsened.

**Correct response.** Apply the predeclared multi-dimensional release gate. Reject the candidate.

**Lesson.** A single aggregate cannot represent a service.

### Case 3 — The one-run victory

**Initial condition.** Candidate throughput is 4% higher in one run. Repeating the baseline varies by ±7%.

**Analysis.** The apparent gain is smaller than observed noise.

**Correct response.** Control the environment, increase independent runs, or report insufficient evidence.

**Lesson.** Precision of output is not certainty of conclusion.

### Case 4 — The warmed candidate

**Initial condition.** Baseline starts cold; candidate runs immediately afterward with hot database and filesystem caches.

**Analysis.** Run order is confounded with cache state.

**Correct response.** Use randomized or alternating order, reset declared state, or benchmark cold and warm workloads separately.

**Lesson.** Experimental design matters more than decimal places.

## Python implementation

### Mechanism

The Python statistics module implements nearest-rank quantiles, histogram summaries, deterministic bootstrap intervals over run-level values, and schedule/event coverage checks.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_performance/statistics.py`
- `capstone/tracks/python-fastapi/src/api_performance/workload.py`
- `capstone/tracks/python-fastapi/tests_performance/test_statistics_workload.py`

### Focused example

```python
from api_performance.statistics import nearest_rank, summarize

samples_ms = [11.0, 12.0, 13.0, 15.0, 90.0]
assert nearest_rank(samples_ms, 0.95) == 90.0
summary = summarize(samples_ms)
assert summary.count == 5
assert summary.quantile_algorithm == "nearest-rank"
```

The implementation rejects empty or non-finite samples and records units. The bootstrap function accepts run-level summaries and an explicit seed; it does not resample individual requests across runs as if they were independent environments.

### Python-specific failure to avoid

Use `time.perf_counter_ns()` for elapsed time, not `datetime.now()`. Avoid measuring logging, JSON pretty-printing, or result-file writes unless they belong to the workload.

## TypeScript implementation

### Mechanism

The TypeScript track uses `process.hrtime.bigint()` for duration and keeps nanoseconds as bigint until presentation. Its scheduler records intended and actual starts.

### Repository paths

- `capstone/tracks/typescript-fastify/src/performance/statistics.ts`
- `capstone/tracks/typescript-fastify/src/performance/workload.ts`
- `capstone/tracks/typescript-fastify/test-performance-core/statistics-workload.test.mjs`

### Focused example

```typescript
const samplesMs = [11, 12, 13, 15, 90];
if (nearestRank(samplesMs, 0.95) !== 90) {
  throw new Error("unexpected p95");
}
const summary = summarize(samplesMs);
if (summary.quantileAlgorithm !== "nearest-rank") {
  throw new Error("algorithm must be explicit");
}
```

The implementation validates finite numeric samples and separates bigint timing from floating-point millisecond presentation. Schedule drift is retained as a measured field.

### TypeScript-specific failure to avoid

Do not use `Date.now()` for sub-millisecond duration, and do not cast nanosecond bigint values to number before subtracting.

## Cross-language invariant

Given the same samples and algorithm, both tracks produce the same count, minimum, maximum, mean within a defined tolerance, and nearest-rank quantiles. Shared vectors include ties, tiny samples, large values, and invalid input.

## Failure patterns

- **Tool-output worship.** A requests/s line is accepted without understanding executor or population. **Decisive check:** benchmark envelope.
- **Coordinated omission.** Scheduled arrivals disappear during slow periods. **Decisive check:** intended-start trace.
- **Warmup cherry-picking.** Windows are selected after inspecting the graph. **Decisive check:** predeclared or evidence-based policy.
- **Pseudoprecision.** Many decimals imply certainty from one noisy run. **Decisive check:** independent run series.
- **Algorithm drift.** p95 from different tools uses different definitions. **Decisive check:** algorithm field.
- **Client saturation.** The generator, not server, reaches its limit. **Decisive check:** client CPU and dropped iterations.

## Evidence and design review

Before accepting the module increment, answer:

1. Can the client start every scheduled arrival, and where is failure recorded?
2. Which observations belong to warmup, measurement, and cooldown?
3. How many independent runs support the conclusion?
4. Which quantile algorithm and sample count produced the tail claim?
5. Was the practical threshold declared before the candidate result?
6. Can the summary be recomputed from retained evidence?

## Module synthesis

You are ready to leave this module when you can **distinguish load generation, timing, outcome collection, and analysis, design open and closed schedules and explain their different questions, and detect coordinated omission using intended start times** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Compare offered, started, completed, delayed, and dropped populations** and requiring the following oracle: **the open schedule exposes arrivals during the pause; scheduled-to-start delay is retained; closed and open results are not compared as equivalent workloads; summary replay matches packaged calculations.**

The cumulative platform now includes **Build reproducible benchmark profiles, repeated runs, quantile and interval summaries, and accepted/rejected/inconclusive comparisons**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [HTTP Efficiency and Representation Cost](../module-03-http-efficiency-and-representation-cost/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
