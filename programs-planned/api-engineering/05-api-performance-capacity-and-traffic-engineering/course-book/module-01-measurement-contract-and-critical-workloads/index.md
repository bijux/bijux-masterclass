# Module 01 — Measurement Contract and Critical Workloads

> **Program stage:** Course 5 of 6 — Sustain the promise under pressure.

> **Central question:** What exactly is being measured, under which workload and environment identity, and which correctness oracle still applies?

## Where this module fits


Performance work fails early when “the API is slow” is accepted as a problem statement. An API has many journeys, each with different payloads, dependencies, and value. A project metadata read, a streaming upload, an idempotent run submission, and a webhook backlog drain cannot share one meaningful latency target.

Course 4 already defined critical user journeys and reliability populations. This module extends those assets into a performance measurement contract. It does not replace an SLO. An SLO describes the level of service expected over time; a benchmark describes behavior under a specified experiment. The two inform one another, but neither can impersonate the other.

The central discipline is identity. A result belongs to a workload, data set, environment, build, and correctness oracle. If any identity-bearing field changes, the experiment is a new experiment. This is how the course prevents a common form of accidental dishonesty: changing the workload until the result looks good while retaining the original label.


## Capstone result

Freeze six critical workloads, measurement envelopes, outcome populations, evidence classes, and comparable baselines.

Create performance profile 1.0, the six-workload catalogue, environment fingerprint schema, and correctness-first benchmark envelope.

## Learning outcomes

By the end of this module, you can:

- distinguish performance requirements from reliability objectives and capacity claims
- derive critical workloads from inherited user journeys instead of endpoint popularity
- choose an open, closed, or mixed load model deliberately
- define offered, admitted, completed, rejected, and failed populations
- hash identity-bearing workload and environment fields deterministically
- write correctness oracles that survive optimization
- reject an incomparable baseline before calculating improvement

## Core performance model

### 1. Performance is a constrained property


Performance is not the smallest observed response time. It is behavior under demand while other requirements remain true. For this course, a candidate must preserve the API contract, authorization, durable effects, idempotent replay, error classification, and reliability populations.

This changes the optimization objective. Suppose removing response validation lowers p95 from 80 ms to 62 ms. The change is not an 18 ms improvement; it is an invalid candidate. The inherited promise defines the feasible region. Performance engineering searches inside that region.

A useful requirement names the journey, population, demand, environment, and bound:

```text
Under WL-RUN-LIST at 120 offered requests/s,
with dataset DS-MEDIUM and environment ENV-4CPU,
at least 99.5% of eligible requests preserve conformance,
p95 server-observed latency is <= 180 ms,
and database shared reads per request are <= 40.
```

The numbers are project policy. The structure is the transferable skill.


### 2. Critical journey becomes critical workload


A journey is a user outcome across stages. A workload is an executable demand model for that journey. Derive workloads from the Course 4 journey catalogue, then specify request mix, data distribution, arrival process, think time, concurrency, duration, and correctness checks.

Do not use uniform random identifiers when production access is skewed. Do not use one-row tables for a pagination query. Do not measure only successful requests when overload is part of the experiment. Representativeness is not perfect imitation; it is an explicit, testable rationale for the aspects that matter to the claim.

The capstone catalogue includes six workloads because each stresses a different resource. Adding dozens of microbenchmarks would dilute attention. A microbenchmark may explain a mechanism, but release decisions are made on critical workloads.


### 3. Open and closed demand models


In an **open model**, arrivals follow an external schedule. A slow response does not automatically reduce future arrivals. This exposes queue growth and overload for traffic driven by independent clients or upstream systems.

In a **closed model**, a fixed population waits for completion or think time before sending the next request. When the service slows, the generated arrival rate falls. Closed models are appropriate for bounded interactive users or worker pools, but they can conceal overload if used for externally driven traffic.

A mixed model is often correct. The capstone models run submissions with an open arrival stream while each virtual client has bounded outstanding idempotent retries. The workload file records the model explicitly; a tool’s default is not accepted as design.


### 4. Outcome populations


Record at least five populations:

- **offered** — work the schedule intended to send;
- **started** — work for which a request attempt began;
- **admitted** — work accepted into the service;
- **completed** — work that reached a terminal observed outcome;
- **rejected or dropped** — work intentionally refused or never started.

Then classify completed outcomes by correctness and status. Throughput is not offered load. A service receiving 1,000 requests/s and completing 400 requests/s has 400 requests/s throughput, not 1,000.

The denominator for latency quantiles also matters. If timed-out requests disappear from the sample, latency looks better as the service fails. The benchmark envelope stores outcome counts next to latency samples and treats missing terminal observations as failures.


### 5. Workload and environment identity


A workload identity is a stable ID plus a canonical hash of semantic fields. Comments and display labels may be excluded; arrival rate, request mix, payload distribution, duration, and correctness policy are included.

The environment fingerprint includes runtime versions, CPU and memory limits, process count, worker count, database settings, data scale, source revision, and relevant feature flags. Hostnames and secret values are excluded or pseudonymized.

Fingerprinting does not make unlike environments comparable. It makes the difference visible. The comparison engine rejects mismatched workload hashes and labels environment mismatches as non-comparable unless the report explicitly declares a controlled dimension.


### 6. Correctness oracle before metric


Each workload names a decisive correctness oracle. For `WL-RUN-SUBMIT`, the oracle checks that repeated idempotency keys create one logical run and replay the stored public outcome. For `WL-ARTIFACT-DOWNLOAD`, it checks exact bytes, checksum, authorization, range semantics, and validators.

A benchmark harness must execute the oracle during or immediately after the run. “The endpoint returned 2xx” is insufficient. Database and artifact state may be authoritative; telemetry remains evidence, not business truth.

Correctness results are recorded independently from latency. This allows a report to say “candidate is faster but rejected” without burying the reason.


### 7. Baseline as a decision record


A baseline is not the first number produced. It is an accepted, reproducible envelope whose workload and environment are suitable for the intended comparison. Store raw samples when practical, summary algorithm names, warmup and measurement windows, start time, source revision, and all outcome counts.

Repeat the baseline. If two runs in the same controlled environment differ beyond a predeclared noise band, do not optimize yet. First investigate environment noise, data-state drift, thermal throttling, background work, or benchmark errors.

The capstone baseline is dependency-light and therefore Class B evidence. It is useful for regression and mechanism learning, not for claiming production capacity.


## Course requirements

| Rule | Required behavior | Failure if omitted | Decisive evidence |
|---|---|---|---|
| Identity first | Every result carries workload, dataset, environment, build, and profile identities. | A changed experiment is reported as the old one. | Envelope schema and canonical hashes |
| Correctness first | Correctness oracle passes before latency or throughput can approve a candidate. | Fast but wrong changes are accepted. | Correctness report and durable checks |
| Demand model explicit | Workload states open, closed, or mixed behavior. | Slow systems generate less load and look healthy. | Workload file and schedule trace |
| All outcomes counted | Offered, started, admitted, completed, rejected, failed, and missing outcomes reconcile. | Errors vanish from latency populations. | Outcome conservation check |
| Units mandatory | Every quantity includes units and interval. | Requests, seconds, and bytes are mixed. | Schema validation |
| Repeat baseline | At least three comparable baseline runs precede a release comparison. | Noise is mistaken for improvement. | Run series and variability report |
| Evidence class named | Report states deterministic, local, live dependency, representative, or operated evidence. | Laptop result becomes production capacity claim. | Envelope field and review |
| Inherited profiles frozen | API, security, and reliability versions remain fixed unless separately versioned. | Benchmark is improved by weakening the promise. | Predecessor manifest and conformance checks |

## Worked failures

### Case 1 — The faster unauthorized path

**Initial condition.** A candidate skips owner-aware database filtering and fetches by artifact ID alone. p95 falls by 22%.

**Analysis.** The candidate changes the security oracle. It may expose another tenant’s artifact and performs less work only because it removed a required policy.

**Correct response.** Reject before comparing latency. Repair authorization-aware query performance in Module 4.

**Lesson.** Performance is optimized inside correctness constraints.

### Case 2 — The self-throttling benchmark

**Initial condition.** Fifty closed virtual users issue a new request only after the prior one completes. At saturation, reported throughput remains flat and latency rises modestly.

**Analysis.** The generator reduced arrival rate as responses slowed. It did not represent independent external arrivals.

**Correct response.** Use an open arrival schedule for the capacity question and record scheduled versus actually started iterations.

**Lesson.** The workload model can hide overload.

### Case 3 — The missing timeouts

**Initial condition.** A summary includes only successful response durations. Two percent of requests timed out and were absent.

**Analysis.** The slowest outcomes were censored. p99 is not meaningful for the full eligible population.

**Correct response.** Count timeouts as bad terminal outcomes, retain timeout duration or censoring metadata, and fail the correctness/coverage gate.

**Lesson.** Outcome conservation precedes quantiles.

### Case 4 — The incomparable improvement

**Initial condition.** Baseline used four workers and candidate used eight, but the report attributes the gain to a code change.

**Analysis.** Both code and environment changed. Causality is not identified.

**Correct response.** Repeat with one controlled variable or present it honestly as a combined capacity configuration change.

**Lesson.** A fingerprint makes hidden variables reviewable.

## Python implementation

### Mechanism

The Python package defines immutable dataclasses for workload, environment, correctness, outcomes, and benchmark envelopes. Canonical JSON excludes display-only fields and rejects non-finite numeric values.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_performance/models.py`
- `capstone/tracks/python-fastapi/src/api_performance/identity.py`
- `capstone/tracks/python-fastapi/tests_performance/test_models_identity.py`

### Focused example

```python
from api_performance.models import WorkloadSpec

workload = WorkloadSpec(
    id="WL-RUN-LIST",
    model="open",
    rate_per_second=120,
    duration_seconds=60,
    dataset_id="DS-MEDIUM",
    request_mix={"listRuns": 1.0},
)
assert workload.identity.startswith("sha256:")
```

The identity is derived from semantic fields, not from object identity or Python’s randomized hash. The model validates positive rates, complete request-mix weights, and supported load models before hashing.

### Python-specific failure to avoid

Do not use `hash()` for persisted identity; Python deliberately randomizes string hashes between processes. Do not serialize `float('nan')`, which is not interoperable canonical JSON.

## TypeScript implementation

### Mechanism

The TypeScript track mirrors the data contract with runtime validation and canonical key ordering. It represents counts as bigint-safe decimal strings in serialized envelopes.

### Repository paths

- `capstone/tracks/typescript-fastify/src/performance/models.ts`
- `capstone/tracks/typescript-fastify/src/performance/identity.ts`
- `capstone/tracks/typescript-fastify/test-performance-core/models-identity.test.mjs`

### Focused example

```typescript
const workload = createWorkloadSpec({
  id: "WL-RUN-LIST",
  model: "open",
  ratePerSecond: 120,
  durationSeconds: 60,
  datasetId: "DS-MEDIUM",
  requestMix: { listRuns: 1.0 },
});
if (!workload.identity.startsWith("sha256:")) {
  throw new Error("missing workload identity");
}
```

The TypeScript implementation refuses unsafe integer counts and normalizes semantic keys before SHA-256. The serialized envelope uses strings for values that may exceed JavaScript’s safe-integer range.

### TypeScript-specific failure to avoid

Do not coerce PostgreSQL counts or nanosecond timestamps into `number` when they can exceed `Number.MAX_SAFE_INTEGER`.

## Cross-language invariant

The same workload JSON must produce the same SHA-256 identity in both languages. Shared vectors include key-order changes, display-only annotations, unsafe integers, and non-finite values.

## Failure patterns

- **Endpoint-only thinking.** A single route latency ignores the multi-stage user outcome. **Decisive check:** critical workload maps to inherited journey.
- **Unversioned workload drift.** Payload size or data distribution changes under the same ID. **Decisive check:** canonical workload hash.
- **Success-only denominator.** Timeouts and rejected work disappear. **Decisive check:** outcome conservation.
- **Environment amnesia.** Worker count, data size, or runtime changes. **Decisive check:** environment fingerprint.
- **Metric-first optimization.** Code is tuned before a violated budget is named. **Decisive check:** performance requirement.
- **Local-to-production leap.** A laptop result becomes a capacity claim. **Decisive check:** evidence class.

## Evidence and design review

Before accepting the module increment, answer:

1. Which workload is decision-critical, and which smaller experiment merely explains a mechanism?
2. Do offered, admitted, completed, rejected, failed, and missing counts reconcile?
3. Can the correctness oracle detect a faster but unauthorized or non-durable candidate?
4. Which identity-bearing field would make the next run incomparable?
5. What evidence class does the report actually reach?
6. Which inherited profile would be violated by the most tempting shortcut?

## Module synthesis

A performance result is trustworthy only when its workload, environment, correctness, and outcome populations are explicit. Module 1 turns inherited journeys into executable measurement contracts and prevents later optimization from redefining success.

Proceed to [Exercises](exercises.md), then complete the [Lab](lab.md) and [Checkpoint](checkpoint.md).

## Next in the story

The next module, **Benchmark Design and Statistical Interpretation**, asks: How do open and closed demand, warmup, sample size, missing outcomes, variation, and statistical uncertainty change benchmark meaning? It builds on the evidence produced here rather than reopening this module's decisions.
