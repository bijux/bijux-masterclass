# Module 05 — Telemetry Architecture and Structured Events

> **Program stage:** Course 4 of 10 — Observe, diagnose, contain, and recover the promise.

> **Central question:** Which operational events are useful, bounded, redacted, versioned, and clearly separated from business truth?

## Where this module fits

Module 04 produced **Implement lifecycle states, liveness/readiness separation, graceful draining, lease handling, and startup reconciliation**. This module extends that result by asking: **Which operational events are useful, bounded, redacted, versioned, and clearly separated from business truth?**

The new capstone increment is **Create the telemetry vocabulary, correlation rules, bounded sinks, exporter failure behavior, and privacy policy**. It becomes the prerequisite for **Metrics and Service-Level Indicators**, so the previous module’s guarantees must remain visible in the new evidence.

## Learning outcomes

- Separate logs, metrics, traces, and audit records by purpose.
- Use stable event names and fields.
- Propagate correlation and trace context safely.
- Bound queues and drop behavior.
- Treat telemetry as evidence about execution, not the authority on durable state.

## Capstone increment

Create the telemetry vocabulary, correlation rules, bounded sinks, exporter failure behavior, and privacy policy.

## Core reliability model

### Driving question

> How do we produce diagnostic evidence that is correlated, bounded, privacy-safe, and useful even when export is delayed or partially lost?

Logs, metrics, traces, and operational events are complementary evidence streams. They share bounded context and vocabulary but never replace durable business state or inherit untrusted data without policy.

### 1. Signal purpose

Logs explain discrete records, metrics aggregate populations, traces show causal execution, and operational events record bounded transitions. One signal cannot safely impersonate all others.

**Failure if confused.** Encoding every request as a unique metric label creates a database of logs inside the metrics system.
### 2. Telemetry schema

Stable names, severity, timestamps, service identity, trace correlation, event fields, and privacy classification form a versioned contract.

**Failure if confused.** Free-form strings make alert queries and incident comparison unreliable.
### 3. Trace context

W3C `traceparent` supplies bounded correlation across trusted hops. Parsing is strict and invalid context starts a new trace rather than poisoning state.

**Failure if confused.** Echoing arbitrary caller trace identifiers into logs without validation enables injection and cardinality abuse.
### 4. Baggage

Baggage is propagated application metadata, not a secret store or authorization channel. The capstone accepts none by default.

**Failure if confused.** Putting tenant roles or access tokens in baggage leaks them to downstream systems and exporters.
### 5. Structured redaction

Redaction operates recursively on field names and value patterns before buffering or export. It cannot rely on operators remembering not to log secrets.

**Failure if confused.** A nested authorization header survives a top-level-only redactor.
### 6. Bounded buffering

Queues, batch sizes, retry time, and local retention are finite. When full, telemetry drops are measured rather than blocking customer work.

**Failure if confused.** An unbounded log queue converts collector outage into memory exhaustion.
### 7. Clock evidence

Events use wall time for human ordering and monotonic duration for elapsed time. Clock uncertainty is stated.

**Failure if confused.** Subtracting wall-clock timestamps across hosts can produce negative latency.
### 8. Sampling and loss

Sampling changes diagnostic completeness. Durable correctness proofs cannot require every span or log.

**Failure if confused.** A missing sampled span cannot prove an operation never happened.

For a new Analysis Runs failure:

Apply **Signal purpose, Telemetry schema, Trace context** to this module’s capstone increment: Define the telemetry schema, W3C trace-context boundary, structured event vocabulary, redaction policy, bounded exporters, and collector-failure behavior across API, worker, storage, and webhook paths. State one misleading green signal and the durable observation that would overrule it.

## Operational requirements

“Normative” means the capstone is evaluated against these course requirements. It does not mean every row is an Internet standard.

| # | Rule | Required behavior | Failure if omitted | Decisive evidence |
| --- | --- | --- | --- | --- |
| 1 | Version the telemetry vocabulary | Event and attribute names have owners, types, privacy classes, and bounded value rules. | Free-form event vocabulary: Queries and alerts silently diverge | `telemetry-schema validation` |
| 2 | Validate incoming trace context | Accept only the supported W3C profile and reject invalid identifiers or flags. | Unvalidated trace context: Correlation injection and malformed traces | `trace-context vectors` |
| 3 | Do not trust baggage | No security decision or secret uses propagated baggage. | Secrets in local queue: Collector-side redaction is too late | `baggage rejection test` |
| 4 | Redact before buffering | Sensitive material is removed before any local queue, file, stdout, or exporter. | Unbounded exporter retry: Collector outage consumes memory/threads | `recursive redaction tests` |
| 5 | Bound every exporter | Queue capacity, batch size, retry duration, and drop accounting are explicit. | Baggage as authorization: Downstream privilege spoofing | `collector outage experiment` |
| 6 | Keep telemetry fail-open for business work | Export failure cannot roll back or reject otherwise valid durable operations. | Wall time for duration: Clock jumps corrupt latency | `exporter failure test` |
| 7 | Keep cardinality bounded | Identifiers and user-controlled values are logs/trace attributes only when reviewed, never default metric labels. | Identifiers as metric labels: Series count grows with traffic | `schema/cardinality guard` |
| 8 | Correlate without claiming authority | Trace IDs connect evidence; database keys and immutable checksums decide durable truth. | Missing span treated as failure: Sampling changes business conclusion | `reconciliation comparison` |


### Evidence boundary

Bounded in-memory sinks prove redaction and drop policy; collector queues, exporter backpressure, and backend retention require the live telemetry topology.

## Worked failures

### Case 1 — Secret enters batch buffer

#### Initial system

A structured event contains a nested `authorization` field. Redaction is applied only by the remote collector, so the process queue and stdout already contain the token.


#### Correct design

Apply recursive structural and pattern redaction before enqueue. Test the sink contents, not only exported output.


#### Lesson

The earliest copy is the security boundary.
### Case 2 — Invalid traceparent explosion

#### Initial system

The API accepts any caller string as a trace ID. Attackers create malformed high-cardinality correlation values and broken downstream traces.


#### Correct design

Strictly parse the supported W3C version, length, hexadecimal constraints, non-zero IDs, and flags. Start a new trace on invalid input and record a bounded reason.


#### Lesson

Correlation context is input and must be validated.
### Case 3 — Collector outage blocks requests

#### Initial system

Synchronous export waits for the collector and customer latency rises until requests fail.


#### Correct design

Use bounded asynchronous batching with a small local queue and explicit drop counter. The durable response is independent of exporter success.


#### Lesson

Observability must remain observable when degraded.
### Case 4 — One giant log message

#### Initial system

Every failure is rendered as free text containing stack, request, tenant, and payload. Queries are brittle and redaction uncertain.


#### Correct design

Emit a small event name and typed fields; retain stack only in a bounded diagnostic field after sanitization.


#### Lesson

Structure enables policy and stable investigation.

## Python implementation

### Mechanism under review

Validate trace context, apply recursive redaction before the bounded sink, and demonstrate optional OpenTelemetry export without making the SDK authoritative.

### Repository paths

- `capstone/tracks/python-fastapi/src/api_reliability/context.py`
- `capstone/tracks/python-fastapi/src/api_reliability/telemetry.py`
- `capstone/tracks/python-fastapi/src/api_reliability/otel_adapter.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_telemetry_reconcile.py`

### Executable invariant

```python
from api_reliability.clock import ManualClock
from api_reliability.telemetry import InMemoryEventSink, StructuredLogger

sink = InMemoryEventSink(maximum_events=1)
logger = StructuredLogger(
    clock=ManualClock(1), sink=sink, service_name="analysis-api",
    service_version="1.3.0", deployment_environment="course",
)
logger.emit("analysis.request.completed", attributes={"authorization": "Bearer secret"})
assert sink.events[0].to_dict()["attributes"]["authorization"] == "[REDACTED]"
```

The cited files must expose the complete **Telemetry Architecture and Structured Events** implementation path and its negative regression evidence.

### Guided failure investigation — Secret enters batch buffer

**Initial condition.** A structured event contains a nested `authorization` field. Redaction is applied only by the remote collector, so the process queue and stdout already contain the token.

**Expected repair.** Apply recursive structural and pattern redaction before enqueue. Test the sink contents, not only exported output.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=05 TRACK=python` and explain why the same public and durable outcome holds in the other language.

### Python-specific review

Use an injected clock and explicit adapters; cancellation must release async resources and preserve committed durable work.

### Module-specific hazards

- **Free-form event vocabulary.** Queries and alerts silently diverge The decisive check is schema conformance.
- **Unvalidated trace context.** Correlation injection and malformed traces The decisive check is trace vector tests.
- **Secrets in local queue.** Collector-side redaction is too late The decisive check is sink inspection.
- **Unbounded exporter retry.** Collector outage consumes memory/threads The decisive check is outage resource test.
- **Baggage as authorization.** Downstream privilege spoofing The decisive check is policy rejection.
- **Wall time for duration.** Clock jumps corrupt latency The decisive check is monotonic-clock test.

## TypeScript implementation

### Mechanism under review

Use AsyncLocalStorage/context boundaries for correlation, preserve the same event schema, and prove queue/drop behavior without assuming Node console output is structured telemetry.

### Repository paths

- `capstone/tracks/typescript-fastify/src/reliability/context.ts`
- `capstone/tracks/typescript-fastify/src/reliability/telemetry.ts`
- `capstone/tracks/typescript-fastify/src/reliability-otel.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/context-deadline.test.mjs`

### Executable invariant

```typescript
const sink = new InMemoryEventSink(1);
const clock = new ManualClock(1);
const logger = new StructuredLogger({
  nowMs: () => clock.nowMs(), sink, serviceName: "analysis-api",
  serviceVersion: "1.3.0", deploymentEnvironment: "course",
});
logger.emit("analysis.request.completed", {
  attributes: { authorization: "Bearer secret" },
});
if (sink.events[0]?.attributes.authorization !== "[REDACTED]") throw new Error("leak");
```

The cited files must expose the complete **Telemetry Architecture and Structured Events** implementation path and its negative regression evidence.

### Guided failure investigation — Secret enters batch buffer

**Initial condition.** A structured event contains a nested `authorization` field. Redaction is applied only by the remote collector, so the process queue and stdout already contain the token.

**Expected repair.** Apply recursive structural and pattern redaction before enqueue. Test the sink contents, not only exported output.

**Review procedure.** Predict the first violated requirement, run the focused test, introduce the corresponding planted defect, and stop at the smallest failing oracle. After repair, rerun `make module-proof MODULE=05 TRACK=typescript` and explain why the same public and durable outcome holds in the other language.

### TypeScript-specific review

Use explicit promises, abort signals, and bounded numeric representations; event-loop progress is not a substitute for dependency readiness.

### Module-specific hazards

- **Free-form event vocabulary.** Queries and alerts silently diverge The decisive check is schema conformance.
- **Unvalidated trace context.** Correlation injection and malformed traces The decisive check is trace vector tests.
- **Secrets in local queue.** Collector-side redaction is too late The decisive check is sink inspection.
- **Unbounded exporter retry.** Collector outage consumes memory/threads The decisive check is outage resource test.
- **Baggage as authorization.** Downstream privilege spoofing The decisive check is policy rejection.
- **Wall time for duration.** Clock jumps corrupt latency The decisive check is monotonic-clock test.

## Failure patterns

The following defects are plausible precisely because the normal path can remain green. Review the failure mechanism, not only the symptom.

| Defect | Why it is tempting | What breaks | Why a happy-path test misses it | Decisive check |
|---|---|---|---|---|
| **Free-form event vocabulary** | Developers can log arbitrary messages quickly. | Queries, alerts, and redaction policies cannot rely on stable fields. | One test only checks that something was emitted. | schema conformance. |
| **Unvalidated trace context** | Propagating inbound headers preserves continuity. | Malformed or attacker-controlled context contaminates traces and sampling. | Test clients send valid headers. | trace vector tests. |
| **Secrets in local queue** | A bounded queue feels internal and safe. | Sensitive values remain in memory, dumps, or exporter retries. | Normal output assertions ignore the queue contents. | sink inspection. |
| **Unbounded exporter retry** | Retaining telemetry seems preferable to loss. | Memory grows while the exporter is unavailable. | The exporter is healthy in the success path. | outage resource test. |
| **Baggage as authorization** | Baggage is conveniently available across services. | Untrusted propagated values influence access decisions. | Trusted test traces carry expected tenant values. | policy rejection. |
| **Wall time for duration** | Wall clocks are easy to read and format. | Clock adjustment produces negative or distorted durations. | Short tests run without clock changes. | monotonic-clock test. |
| **Identifiers as metric labels** | Per-resource troubleshooting seems useful. | Cardinality grows without bound and destabilizes the metric system. | A small fixture population never reaches the limit. | cardinality guard. |
| **Missing span treated as failure** | Traces are expected for every journey. | Sampling or exporter loss becomes a false business failure. | The local sampler records everything. | durable reconciliation. |

## What you add to the capstone

### Increment

Define the telemetry schema, W3C trace-context boundary, structured event vocabulary, redaction policy, bounded exporters, and collector-failure behavior across API, worker, storage, and webhook paths.

### Files to inspect or modify

- `capstone/tracks/python-fastapi/src/api_reliability/context.py`
- `capstone/tracks/python-fastapi/src/api_reliability/telemetry.py`
- `capstone/tracks/python-fastapi/src/api_reliability/otel_adapter.py`
- `capstone/tracks/python-fastapi/tests_reliability/test_telemetry_reconcile.py`
- `capstone/tracks/typescript-fastify/src/reliability/context.ts`
- `capstone/tracks/typescript-fastify/src/reliability/telemetry.ts`
- `capstone/tracks/typescript-fastify/src/reliability-otel.ts`
- `capstone/tracks/typescript-fastify/test-reliability-core/context-deadline.test.mjs`

The shared requirement, vector, SLO, runbook, or scenario evidence lives under `capstone/reliability-case/`, `capstone/shared/`, and `capstone/incident/`.

### Module constraints

- Preserve public API 1.2 and security profile 1.0.
- **Version the telemetry vocabulary.** Event and attribute names have owners, types, privacy classes, and bounded value rules.
- **Validate incoming trace context.** Accept only the supported W3C profile and reject invalid identifiers or flags.
- **Do not trust baggage.** No security decision or secret uses propagated baggage.
- **Redact before buffering.** Sensitive material is removed before any local queue, file, stdout, or exporter.
- The planted failure **Secret enters batch buffer** must be detectable without treating telemetry as business truth.

### Acceptance narrative

Begin with the failure **Secret enters batch buffer**. A reviewer must be able to identify the affected journey and requirement, reproduce the failure, distinguish public behavior from durable state and diagnostic signals, apply the bounded design **Apply recursive structural and pattern redaction before enqueue. Test the sink contents, not only exported output.**, and rerun the focused regression in both languages. Completion is not a screenshot or a green dashboard; it is a reproducible chain from failure hypothesis to decisive oracle.

## Design review

### Peer-review prompts

1. Which part of “How do we produce diagnostic evidence that is correlated, bounded, privacy-safe, and useful even when export is delayed or partially lost?” is decided by durable state rather than telemetry?
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

These are the smallest useful entry points for **Telemetry Architecture and Structured Events**.

### Python — `capstone/tracks/python-fastapi/src/api_reliability/telemetry.py`

```python
_ALLOWED_SEVERITIES = frozenset({"TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"})


def _redact_string(value: str) -> str:
    candidate = _BEARER_RE.sub(r"\1 [REDACTED]", value)
    try:
        parsed = urlsplit(candidate)
        if parsed.scheme and parsed.hostname and (
            parsed.username is not None or parsed.password is not None
        ):
            host = parsed.hostname
            if parsed.port is not None:
                host = f"{host}:{parsed.port}"
            return urlunsplit(
                (
                    parsed.scheme,
                    f"[REDACTED]@{host}",
                    parsed.path,
                    parsed.query,
                    parsed.fragment,
                )
            )
    except ValueError:
        pass
    return candidate


def redact(value: Any, *, key: str | None = None) -> Any:
    """Recursively remove structured and embedded credential material.

    Redaction is a last-resort disclosure boundary. Callers should still avoid
    attaching sensitive values to telemetry in the first place.
    """

    normalized = key.lower().replace("-", "_") if key else None
    if normalized is not None and (
        normalized in SENSITIVE_KEYS
        or normalized.replace("_", "") in SENSITIVE_KEYS
    ):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {str(k): redact(v, key=str(k)) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [redact(item) for item in value]
    if isinstance(value, str):
        return _redact_string(value)
    return value


@dataclass(frozen=True, slots=True)
class TelemetryEvent:
    timestamp_ms: int
    severity: str
    event_name: str
    service_name: str
    service_version: str
    deployment_environment: str
    schema_version: str
    trace_id: str | None = None
    span_id: str | None = None
    attributes: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.timestamp_ms < 0:
            raise ValueError("timestamp_ms must be non-negative")
```

### TypeScript — `capstone/tracks/typescript-fastify/src/reliability/telemetry.ts`

```text
// Abridged source excerpt; intentionally non-executable. Follow the cited repository path for the complete implementation.
export const SENSITIVE_KEYS = new Set([
  "authorization", "api_key", "apikey", "password", "secret", "token",
  "access_token", "refresh_token", "webhooksecret", "webhook_secret",
  "private_key", "pepper", "cookie", "set_cookie",
]);
const BEARER = /(Bearer)\s+[A-Za-z0-9._~+/-]+={0,2}/giu;
const EVENT_NAME = /^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$/;
const SEVERITIES = new Set(["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"]);

function redactString(value: string): string {
  const candidate = value.replace(BEARER, "$1 [REDACTED]");
  try {
    const url = new URL(candidate);
    if (url.username !== "" || url.password !== "") {
      url.username = "[REDACTED]";
      url.password = "";
      return url.toString().replace("%5BREDACTED%5D", "[REDACTED]");
    }
  } catch {
    // Ordinary text is not required to be a URL.
  }
  return candidate;
}

export function redact(value: unknown, key?: string): unknown {
  const normalized = key?.toLowerCase().replaceAll("-", "_");
  if (normalized !== undefined &&
      (SENSITIVE_KEYS.has(normalized) ||
       SENSITIVE_KEYS.has(normalized.replaceAll("_", "")))) {
    return "[REDACTED]";
  }
  if (Array.isArray(value)) return value.map((item) => redact(item));
  if (value !== null && typeof value === "object") {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .map(([name, item]) => [name, redact(item, name)]),
    );
  }
  if (typeof value === "string") return redactString(value);
  return value;
}

export interface TelemetryEvent {
  readonly timestampMs: number;
  readonly severity: string;
  readonly eventName: string;
  readonly serviceName: string;
  readonly serviceVersion: string;
  readonly deploymentEnvironment: string;
  readonly schemaVersion: string;
  readonly traceId?: string;
  readonly spanId?: string;
  readonly attributes: Readonly<Record<string, unknown>>;
}

function validateEvent(event: TelemetryEvent): void {
  if (!Number.isSafeInteger(event.timestampMs) || event.timestampMs < 0) {
    throw new Error("timestampMs must be a non-negative safe integer");
  }
  if (!SEVERITIES.has(event.severity)) throw new Error("unsupported telemetry severity");
  if (!EVENT_NAME.test(event.eventName)) {
    throw new Error("eventName must be a stable dotted identifier");
  }
  for (const [name, value] of Object.entries({
    serviceName: event.serviceName,
```

Compare the two tracks by this invariant: **events use versioned names and bounded attributes, are recursively redacted, and never replace durable business records**. The intended implementation difference is: logging/export APIs differ; the serialized safe event contract is shared.

## Module synthesis

You are ready to leave this module when you can **Separate logs, metrics, traces, and audit records by purpose, Use stable event names and fields, and Propagate correlation and trace context safely** without relying on framework vocabulary or a happy-path demonstration. The lab makes that competence falsifiable by introducing **Remove or bypass the central control for Telemetry Architecture and Structured Events in a temporary branch** and requiring the following oracle: **No raw secret appears in any buffered or exported event; Invalid context cannot control trace identity; Queue memory remains bounded; Collector outage does not change durable API outcome.**

The cumulative platform now includes **Create the telemetry vocabulary, correlation rules, bounded sinks, exporter failure behavior, and privacy policy**. Carry forward the resulting source changes, negative regression, evidence record, and limitation statement; the next module assumes all four, not merely a passing command.

## Next in the story

Continue to [Metrics and Service-Level Indicators](../module-06-metrics-and-service-level-indicators/index.md). Before moving on, complete the exercises, lab, and checkpoint in this module; the next chapter assumes their evidence.
