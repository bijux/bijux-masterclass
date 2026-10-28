# Module 06 — Metrics and Service-Level Indicators

> **Program stage:** Course 4 of 10 — Observe, diagnose, contain, and recover the promise.

> **Central question:** How are counters, gauges, histograms, and SLI populations defined so the math means what operators think it means?

## Where this module fits

Module 05 produced **Create the telemetry vocabulary, correlation rules, bounded sinks, exporter failure behavior, and privacy policy**. This module extends that result by asking: **How are counters, gauges, histograms, and SLI populations defined so the math means what operators think it means?**

The new capstone increment is **Implement bounded metric dimensions, units, good/bad/eligible/excluded populations, and aggregation semantics**. It becomes the prerequisite for **Distributed Tracing Across Asynchronous Work**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Choose metric instruments from the measured quantity.
- Control label dimensions and series count.
- Measure latency distributions rather than averages.
- Define good, bad, eligible, and excluded events.
- Use durable timestamps for asynchronous journey indicators.

## Capstone increment

Implement bounded metric dimensions, units, good/bad/eligible/excluded populations, and aggregation semantics.

## Core reliability model

### Driving question

> How do we turn events into bounded measurements that represent user journeys rather than process vanity or accidental query semantics?

A useful metric has a stable event population, unit, monotonicity, and bounded dimensions. An SLI is a versioned interpretation of those observations with explicit good, bad, eligible, and excluded events.

### 1. Metric instrument

Counters accumulate events, gauges report current state, and histograms preserve distributions. Choosing the wrong instrument produces invalid aggregation.

**Failure if confused.** A gauge for total requests can decrease on restart and cannot be safely summed.
### 2. Event population

Every measurement names what event causes observation and who owns it.

**Failure if confused.** Counting retries as requests without classification inflates availability denominator.
### 3. Label dimension

Labels partition a population. They must be bounded, stable, useful for action, and privacy reviewed.

**Failure if confused.** `run_id` creates one series per run and can exhaust the metrics backend.
### 4. Histogram

A histogram records a distribution using cumulative buckets, count, and sum. Buckets must reflect decisions and units.

**Failure if confused.** Only average latency can hide a long tail that violates the objective.
### 5. Service-level indicator

An SLI is a ratio or distribution tied to a critical journey. It is not simply whatever metric already exists.

**Failure if confused.** CPU usage may explain latency but is not API availability.
### 6. Recording rule

A recording rule centralizes reviewed query semantics and reduces repeated expensive or inconsistent expressions.

**Failure if confused.** Three dashboards independently define “success” and disagree.
### 7. Counter reset

Process restart resets in-process counters; rate calculations must handle resets and aggregation.

**Failure if confused.** Subtracting raw values across restart can produce negative requests.
### 8. Insufficient data

Small or empty populations cannot always support a confident conclusion. The course reports this state explicitly.

**Failure if confused.** Zero requests is not evidence of 100% availability.

For a new Analysis Runs failure:

Apply **Metric instrument, Event population, Label dimension** to this module’s capstone increment: Implement bounded counters, gauges, and histograms; define journey SLIs; add recording rules; and prove cardinality limits and event-population semantics. State one misleading green signal and the durable observation that would overrule it.

## Operational requirements

“Normative” means the capstone is evaluated against these course requirements. It does not mean every row is an Internet standard.

| # | Rule | Required behavior | Failure if omitted | Decisive evidence |
| --- | --- | --- | --- | --- |
| 1 | Name metrics by semantic event | Names include stable domain and unit suffixes, not implementation accidents. | Unique-ID label: Series grow with traffic | `metric schema check` |
| 2 | Use bounded labels only | Label values come from reviewed finite sets; unique identifiers are forbidden. | Average-only latency: Tail failure remains hidden | `max-series test` |
| 3 | Record durations in one base unit | Histogram names and values use seconds consistently at export boundary. | Undefined denominator: Availability changes by dashboard | `unit tests` |
| 4 | Preserve distributions | Latency objectives use histograms or equivalent event samples, not averages. | Wrong gauge aggregation: Replica count changes value | `bucket/query proof` |
| 5 | Define SLI populations in versioned files | Good, bad, eligible, and excluded events are explicit. | Unit mismatch: Milliseconds recorded as seconds | `slo-catalog.yaml` |
| 6 | Treat provider overload as bad | 5xx, provider timeout, and rejected valid work cannot be excluded for convenience. | Counter reset ignored: Negative or missing rate | `availability vectors` |
| 7 | Handle counter resets | Queries use reset-safe rates and aggregate across instances correctly. | Provider failures excluded: Objective becomes self-fulfilling | `recording rule review` |
| 8 | Report insufficient data | Empty or undersized windows are distinct from success. | Zero traffic marked perfect: No evidence becomes success | `SLO core tests` |


### Evidence boundary

Synthetic events prove population math and cardinality guards; production traffic shape and appropriate histogram boundaries require measured workload evidence.

## Worked failures

### Case 1 — Run IDs as labels

#### Initial system

A completion counter labels each sample by `run_id` to simplify debugging. Series count grows without bound and the metrics system becomes unstable.


#### Correct design

Keep result, operation, and bounded failure class as labels. Put run ID in trace/log correlation and use exemplars only when supported and privacy-reviewed.


#### Lesson

Metrics aggregate populations; identifiers belong in diagnostic detail.
### Case 2 — Average latency dashboard

#### Initial system

Mean latency is 120 ms, but ten percent of requests take eight seconds. The team reports the objective met.


#### Correct design

Use a histogram and evaluate the proportion under the threshold or a percentile with understood estimation. Inspect bucket coverage.


#### Lesson

Averages erase tail behavior.
### Case 3 — Perfect availability from exclusions

#### Initial system

All 429, 503, and timeout outcomes are excluded, leaving only successful responses.


#### Correct design

Define eligibility from valid customer attempts. Provider overload and provider-owned timeout are bad; invalid credentials may be excluded under the security profile.


#### Lesson

The denominator is part of the reliability contract.
### Case 4 — Gauge summed across replicas

#### Initial system

A worker-backlog gauge is emitted by every instance from the same global database count. Summing multiplies the backlog by replica count.


#### Correct design

Choose one collection ownership or aggregate with `max` under documented semantics. Prefer direct database-backed collector ownership.


#### Lesson

Aggregation semantics must match observation ownership.

## Python implementation

### Mechanism under review

Build the bounded registry, reject unexpected labels and series growth, then compute exact ratio states from shared event counts.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_reliability/metrics.py`
- `capstone/tracks/python-fastapi/src/api_reliability/slo.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_metrics_health.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_slo_alerts.py`

### Executable invariant

```python
from api_reliability.metrics import MetricDescriptor, MetricRegistry

registry = MetricRegistry()
histogram = registry.histogram(
    MetricDescriptor(
        "analysis_request_duration_seconds", "Request latency.", "seconds",
        labels=("operation",), max_series=10,
    ),
    (0.1, 0.25, 0.5),
)
histogram.observe(0.2, labels={"operation": "getAnalysisRun"})
assert histogram.values[("getAnalysisRun",)].buckets == [0, 1, 1, 1]
```

The cited files must expose the complete **Metrics and Service-Level Indicators** implementation path and its negative regression evidence.

### Guided failure investigation — Run IDs as labels

**Initial condition.** A completion counter labels each sample by `run_id` to simplify debugging. Series count grows without bound and the metrics system becomes unstable.

**Expected repair.** Keep result, operation, and bounded failure class as labels. Put run ID in trace/log correlation and use exemplars only when supported and privacy-reviewed.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=06 TRACK=python` and explain why the same public and durable outcome holds in the other language.

### Python-specific review

Use an injected clock and explicit adapters; cancellation must release async resources and preserve committed durable work.

### Module-specific hazards

- **Unique-ID label.** Series grow with traffic The decisive check is series cardinality test.
- **Average-only latency.** Tail failure remains hidden The decisive check is histogram query.
- **Undefined denominator.** Availability changes by dashboard The decisive check is catalog validation.
- **Wrong gauge aggregation.** Replica count changes value The decisive check is ownership test.
- **Unit mismatch.** Milliseconds recorded as seconds The decisive check is unit vector.
- **Counter reset ignored.** Negative or missing rate The decisive check is restart query test.

## TypeScript implementation

### Mechanism under review

Preserve finite label domains and count precision, using explicit result unions for pass, fail, and insufficient-data rather than truthy numeric shortcuts.

### Repository paths

- `capstone/tracks/typescript-fastify/src/reliability/metrics.ts`
- `capstone/tracks/typescript-fastify/src/reliability/slo.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/metrics-health.test.mjs`
- `capstone/tracks/typescript-fastify/test-reliability-core/slo-reconcile.test.mjs`

### Executable invariant

```typescript
const registry = new MetricRegistry();
const histogram = registry.histogram({
  name: "analysis_request_duration_seconds", description: "Request latency.",
  unit: "seconds", labels: ["operation"], maxSeries: 10,
}, [0.1, 0.25, 0.5]);
histogram.observe(0.2, { operation: "getAnalysisRun" });
```

The cited files must expose the complete **Metrics and Service-Level Indicators** implementation path and its negative regression evidence.

### Guided failure investigation — Run IDs as labels

**Initial condition.** A completion counter labels each sample by `run_id` to simplify debugging. Series count grows without bound and the metrics system becomes unstable.

**Expected repair.** Keep result, operation, and bounded failure class as labels. Put run ID in trace/log correlation and use exemplars only when supported and privacy-reviewed.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=06 TRACK=typescript` and explain why the same public and durable outcome holds in the other language.

### TypeScript-specific review

Use explicit promises, abort signals, and bounded numeric representations; event-loop progress is not a substitute for dependency readiness.

### Module-specific hazards

- **Unique-ID label.** Series grow with traffic The decisive check is series cardinality test.
- **Average-only latency.** Tail failure remains hidden The decisive check is histogram query.
- **Undefined denominator.** Availability changes by dashboard The decisive check is catalog validation.
- **Wrong gauge aggregation.** Replica count changes value The decisive check is ownership test.
- **Unit mismatch.** Milliseconds recorded as seconds The decisive check is unit vector.
- **Counter reset ignored.** Negative or missing rate The decisive check is restart query test.

## Failure patterns

The following defects are plausible precisely because the normal path can remain green. Review the failure mechanism, not only the symptom.

| Defect | Why it is tempting | What breaks | Why a happy-path test misses it | Decisive check |
|---|---|---|---|---|
| **Unique-ID label** | It enables direct lookup in a metric query. | Every request creates a new time series. | Small tests do not reveal storage and query explosion. | series cardinality test. |
| **Average-only latency** | A mean is compact and familiar. | Tail failures disappear inside the average. | Uniform local traffic has little skew. | histogram query. |
| **Undefined denominator** | A percentage can be produced quickly when the eligible population is left implicit. | Different readers include retries, cancellations, or no-traffic windows differently. | A happy-path test observes one event, not the population definition. | catalog validation. |
| **Wrong gauge aggregation** | Summing every gauge seems consistent. | Values such as utilization or temperature acquire meaningless totals. | One-instance tests have no aggregation step. | ownership test. |
| **Unit mismatch** | Libraries accept raw numbers without dimensional types. | Milliseconds, seconds, bytes, and counts are combined incorrectly. | Fixtures happen to use values where the error is not obvious. | unit vector. |
| **Counter reset ignored** | Counters are assumed monotonic forever. | Restart produces negative rates or missing work. | The test process never restarts. | restart query test. |
| **Provider failures excluded** | Only application-classified errors are convenient to count. | Dependency-caused user failures vanish from the SLI. | The normal fixture has no provider outage. | eligibility audit. |
| **Zero traffic marked perfect** | No bad events yields a mathematical 100 percent. | A no-data interval is confused with demonstrated availability. | Traffic is always present in the basic test. | insufficient-data test. |

## What you add to the capstone

### Increment

Implement bounded counters, gauges, and histograms; define journey SLIs; add recording rules; and prove cardinality limits and event-population semantics.

### Files to inspect or modify

- `capstone/tracks/python-fastapi/src/api_reliability/metrics.py`
- `capstone/tracks/python-fastapi/src/api_reliability/slo.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_metrics_health.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_slo_alerts.py`
- `capstone/tracks/typescript-fastify/src/reliability/metrics.ts`
- `capstone/tracks/typescript-fastify/src/reliability/slo.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/metrics-health.test.mjs`
- `capstone/tracks/typescript-fastify/test-reliability-core/slo-reconcile.test.mjs`

The shared requirement, vector, SLO, runbook, or scenario evidence lives under `capstone/reliability-case/`, `capstone/shared/`, and `capstone/incident/`.

### Module constraints

- Preserve public API 1.2 and security profile 1.0.
- **Name metrics by semantic event.** Names include stable domain and unit suffixes, not implementation accidents.
- **Use bounded labels only.** Label values come from reviewed finite sets; unique identifiers are forbidden.
- **Record durations in one base unit.** Histogram names and values use seconds consistently at export boundary.
- **Preserve distributions.** Latency objectives use histograms or equivalent event samples, not averages.
- The planted failure **Run IDs as labels** must be detectable without treating telemetry as business truth.

### Acceptance narrative

Begin with the failure **Run IDs as labels**. A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design **Keep result, operation, and bounded failure class as labels. Put run ID in trace/log correlation and use exemplars only when supported and privacy-reviewed.**, and rerun the focused regression in both languages. Completion is not a screenshot or a green dashboard; it is a reproducible chain from failure hypothesis to decisive oracle.

## Design review

### Peer-review prompts

1. Which part of “How do we turn events into bounded measurements that represent user journeys rather than process vanity or accidental query semantics?” is decided by durable state rather than telemetry?
2. What is the smallest fault that disproves the design?
3. Which label, context value, or event field could become unbounded?
4. What happens after restart halfway through the operation?
5. Which Course 3 security constraint could observability violate?
6. Which proof is local and which needs a live environment?
7. How do the two tracks preserve the same invariant idiomatically?
8. What behavior would block release despite OpenAPI compatibility?

### Required artifacts

Record `accept`, `accept-with-residual-risk`, or `reject`. A rejection names the failed requirement and exact evidence needed for reconsideration.

## Representative implementation

These are the smallest useful entry points for **Metrics and Service-Level Indicators**.

### Python — `capstone/tracks/python-fastapi/src/api_reliability/metrics.py`

```python
from typing import Iterable


class MetricError(ValueError):
    pass


_METRIC_NAME = re.compile(r"^[a-zA-Z_:][a-zA-Z0-9_:]*$")
_LABEL_NAME = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")

_FORBIDDEN_IDENTIFIER_LABELS = frozenset(
    {
        "user_id",
        "tenant_id",
        "project_id",
        "dataset_id",
        "run_id",
        "artifact_id",
        "request_id",
        "trace_id",
        "span_id",
    }
)
LabelValues = tuple[str, ...]


@dataclass(frozen=True, slots=True)
class MetricDescriptor:
    name: str
    description: str
    unit: str
    labels: tuple[str, ...] = ()
    max_series: int = 100

    def __post_init__(self) -> None:
        if not _METRIC_NAME.fullmatch(self.name):
            raise MetricError(f"invalid metric name {self.name!r}")
        if not self.description.strip():
            raise MetricError("metric description must not be empty")
        if self.max_series < 1:
            raise MetricError("max_series must be positive")
        if len(self.labels) != len(set(self.labels)):
            raise MetricError("metric labels must be unique")
        if any(not _LABEL_NAME.fullmatch(label) for label in self.labels):
            raise MetricError("invalid metric label name")
        if _FORBIDDEN_IDENTIFIER_LABELS.intersection(self.labels):
            raise MetricError("metric labels contain a forbidden identifier")


@dataclass(slots=True)
class Counter:
    descriptor: MetricDescriptor
    values: dict[LabelValues, float] = field(default_factory=dict)

    def add(
        self,
        amount: float = 1.0,
        *,
        labels: dict[str, str] | None = None,
    ) -> None:
        if not math.isfinite(amount) or amount < 0:
            raise MetricError("counter increments must be finite and non-negative")
        key = _label_key(self.descriptor, labels)
        _guard_series(self.descriptor, self.values, key)
        self.values[key] = self.values.get(key, 0.0) + amount
```

### TypeScript — `capstone/tracks/typescript-fastify/src/reliability/metrics.ts`

```text
// Abridged source excerpt; intentionally non-executable. Follow the cited repository path for the complete implementation.
export class MetricError extends Error {}

export interface MetricDescriptor {
  readonly name: string;
  readonly description: string;
  readonly unit: string;
  readonly labels?: readonly string[];
  readonly maxSeries?: number;
}

type LabelKey = string;
const METRIC_NAME = /^[a-zA-Z_:][a-zA-Z0-9_:]*$/;
const LABEL_NAME = /^[a-zA-Z_][a-zA-Z0-9_]*$/;
const FORBIDDEN_IDENTIFIER_LABELS = new Set([
  "user_id", "tenant_id", "project_id", "dataset_id", "run_id",
  "artifact_id", "request_id", "trace_id", "span_id",
]);

function validateDescriptor(descriptor: MetricDescriptor): void {
  if (!METRIC_NAME.test(descriptor.name)) {
    throw new MetricError(`invalid metric name ${descriptor.name}`);
  }
  if (descriptor.description.trim() === "") {
    throw new MetricError("metric description must not be empty");
  }
  const labels = [...(descriptor.labels ?? [])];
  if (new Set(labels).size !== labels.length ||
      labels.some((label) => !LABEL_NAME.test(label))) {
    throw new MetricError("metric labels must be unique valid names");
  }
  if (labels.some((label) => FORBIDDEN_IDENTIFIER_LABELS.has(label))) {
    throw new MetricError("metric labels contain a forbidden identifier");
  }
  const maximum = descriptor.maxSeries ?? 100;
  if (!Number.isSafeInteger(maximum) || maximum < 1) {
    throw new MetricError("maxSeries must be a positive safe integer");
  }
}

function labelKey(
  descriptor: MetricDescriptor,
  labels: Readonly<Record<string, string>> = {},
): LabelKey {
  const names = [...(descriptor.labels ?? [])];
  const supplied = Object.keys(labels).sort();
  if (JSON.stringify([...names].sort()) !== JSON.stringify(supplied)) {
    throw new MetricError(`metric ${descriptor.name} label mismatch`);
  }
  const values = names.map((name) => String(labels[name]));
  if (values.some((value) => value.length > 120)) {
    throw new MetricError("metric label value exceeds 120 characters");
  }
  return values.join("\u0000");
}

function valuesFromKey(key: LabelKey): string[] {
  return key === "" ? [] : key.split("\u0000");
}

function guard(
  descriptor: MetricDescriptor,
  values: Map<LabelKey, unknown>,
  key: LabelKey,
): void {
  if (!values.has(key) && values.size >= (descriptor.maxSeries ?? 100)) {
```

Compare the two tracks by this invariant: **instrument type, labels, eligibility, good/bad classification, and reset handling are explicit and bounded**. The intended implementation difference is: metric libraries differ; descriptors and resulting counts/histograms must match shared vectors.

## Module synthesis

You are ready to leave this module when you can **Choose metric instruments from the measured quantity, Control label dimensions and series count, and Measure latency distributions rather than averages** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Remove or bypass the central control for Metrics and Service-Level Indicators in a temporary branch** and requiring the following oracle: **Instrument type matches event semantics; Series count remains within declared maximum; Provider-owned failures remain in the denominator; Latency tail is visible in histogram buckets.**

The cumulative platform now includes **Implement bounded metric dimensions, units, good/bad/eligible/excluded populations, and aggregation semantics**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Distributed Tracing Across Asynchronous Work](../module-07-distributed-tracing-across-http-workers-storage-and-webhooks/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
