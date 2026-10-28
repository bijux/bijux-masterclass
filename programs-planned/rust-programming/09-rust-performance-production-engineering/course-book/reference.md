# Course 9 Reference Desk — Rust Performance and Production Engineering

Use this page while designing or reviewing. It is a decision aid, not a replacement for the module explanations.

## Governing question

> Which measurements, resource bounds, signals, security controls, artifact records, and operating policies make a Rust system defensible under representative load?

## Working record

Keep a performance claim, workload description, benchmark boundary, cost model, allocation ledger, byte journey, saturation curve, signal dictionary, SLO/error-budget policy, threat model, dependency dossier, release manifest, and rollout decision. A design is not ready when the record still contains unnamed owners, contradictory states, implicit failure, accidental order, unbounded accumulation, or a claim with no matching evidence.

## Decision rules

| Decision | Rule |
|---|---|
| Claim | State one falsifiable product claim before selecting a benchmark or profiler. |
| Workload | Record scale, skew, data shape, environment, and exclusions. |
| Cost | Separate CPU, allocation, copying, waiting, contention, system calls, and retained state. |
| Signal | Every metric or event answers a named operational question and has a bounded label space. |
| Release | Connect source, lockfile, toolchain, target, profile, features, artifact digest, rollout, and rollback. |

## Module quick reference

| Module | Mechanism | Minimum usable outcome |
|---:|---|---|
| 81 | Performance Contracts, Workloads, and Benchmark Design | turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle |
| 82 | CPU Profiling, Cost Models, and Hot-Path Optimization | choose sampling, instrumentation, counters, and targeted tracing based on the question being asked |
| 83 | Allocation, Memory Footprint, and Ownership Cost | distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count |
| 84 | Data Movement, Buffering, and Zero-Copy Boundaries | trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers |
| 85 | Runtime Efficiency: Contention, Queueing, Batching, and Async Load | separate service time, wait time, queue depth, concurrency, throughput, and utilization |
| 86 | Observability: Structured Tracing, Metrics, and Diagnostic Context | separate events, spans, metrics, profiles, and domain audit records by the questions they can answer |
| 87 | Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation | write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous |
| 88 | Security and Supply-Chain Engineering | identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service |
| 89 | Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases | explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy |
| 90 | Production Readiness, Capacity Planning, Rollouts, and Incident Learning | write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery |

## Claim boundary

Separate language guarantees, library contracts, product policy, target observations, and measured artifact facts. When an exact API or version detail matters, follow the primary source from [Source Notes](../../SOURCE_NOTES.md).

This reference condenses the distinctions used throughout Course 9. It is not a replacement for the chapters. Use it when writing a benchmark contract, reviewing a profile, designing telemetry, or preparing a release.

## Performance vocabulary

### Latency

Latency is elapsed time for one operation. Always name the boundaries: accepted-to-completed, queue-entry-to-dequeue, parse-start-to-domain-value, or connection-open-to-response. Report units and distribution.

Useful summaries:

- **minimum** can reveal the best uncontended path but is usually not representative;
- **median** describes the center of the observed sample;
- **p90, p95, p99** expose progressively rarer slow paths;
- **maximum** is sensitive to sample size and environmental events;
- **mean** is useful for resource accounting but can hide multimodal behavior.

A percentile without the population, window, workload, and sample count is incomplete.

### Throughput

Throughput is completed useful work per unit time. Distinguish:

- offered work;
- admitted work;
- completed work;
- successful work;
- retried work;
- rejected work.

A service can report high completed throughput while silently rejecting most offered traffic. Name the denominator.

### Utilization

Utilization is the fraction of a resource’s capacity that is busy or reserved. CPU utilization does not explain instruction efficiency by itself. A single-threaded bottleneck can leave total-machine CPU low. High utilization near saturation often creates nonlinear queueing delay.

### Queueing relationship

Under stable long-run conditions:

```text
L = λW
```

where:

- `L` is average work in the system;
- `λ` is average arrival or throughput rate;
- `W` is average time in the system.

This is a consistency relation, not a promise for arbitrary bursts or unstable overload.

### Speedup and improvement

For old time `T_old` and new time `T_new`:

```text
speedup = T_old / T_new
relative reduction = (T_old - T_new) / T_old
```

State absolute values as well as percentages. A large relative improvement can be operationally irrelevant when the operation is already negligible.

## Benchmark contract

A benchmark record should contain:

```text
claim
operation
semantic oracle
workload and corpus version
input parameters
setup boundary
measurement boundary
compiler and toolchain
target and hardware class
profile and features
dependency lockfile
sample policy
baseline identifier
result distribution
decision threshold
known limitations
```

### Microbenchmark

A microbenchmark isolates a small operation. It is useful for comparing implementations and scaling shapes. It does not establish service capacity or end-to-end latency.

### Scenario benchmark

A scenario benchmark exercises several layers using a controlled product workflow. It captures interactions omitted by a microbenchmark.

### Load test

A load test applies expected offered demand and records admission, latency, throughput, errors, and resources.

### Stress test

A stress test crosses the expected envelope to reveal saturation, shedding, degradation, and recovery.

### Soak test

A soak test runs long enough to expose retention, fragmentation, leaks, counter rollover, stale state, or periodic behavior.

## Profiling distinctions

### Sampling profile

Periodically samples execution state. Good for locating CPU cost with relatively low perturbation. Sample frequency and stack quality affect interpretation.

### Instrumentation

Records explicit function, span, or event activity. Can provide precise semantic context but adds overhead and only sees instrumented behavior.

### Inclusive cost

Cost attributed to a frame including descendants.

### Exclusive cost

Cost attributed to the frame body excluding descendants.

### Cost model

A cost model predicts how work changes with input and state. Examples:

```text
parse: a × bytes
aggregate: b × records + c × hash_cost
snapshot: d × series + e × series log series + f × rendered_bytes
```

The coefficients are measured; the structure is the hypothesis.

## Memory accounting

### Inline size

Bytes occupied directly by the value representation on the target. `size_of` reports this category.

### Capacity

Storage reserved for possible elements. Capacity can exceed length and can persist after clearing.

### Live bytes

Bytes reachable and required by current state.

### Retained bytes

Bytes kept alive by references, shared ownership, caches, pools, queues, or capacity policy even when only a small part is immediately useful.

### Peak bytes

Maximum observed memory under a named workload and accounting method.

### Allocation churn

Frequency and size distribution of allocations and frees. Churn can affect CPU and fragmentation independently of live bytes.

### Logical retention

Memory remains reachable because the product has no eviction or release transition. This is different from an allocator leak.

## Data movement ledger

For each boundary, record:

| From | To | Operation | Bytes copied? | Owner after | Retention consequence |
|---|---|---|---|---|---|
| socket | receive buffer | read | external transfer | connection | bounded by frame policy |
| buffer | borrowed record | view | no application copy | buffer | view retains buffer |
| borrowed record | series key | promotion | yes | aggregate map | survives frame |
| snapshot model | response buffer | encoding | yes | response | bounded by output policy |

“Zero copy” must name the start and end rows being discussed.

## Queue and batch policy

Every queue should state:

```text
capacity
unit: items and/or bytes
admission owner
full behavior
cancellation behavior
shutdown behavior
metrics
memory estimate
```

Every batch should state:

```text
maximum items
maximum bytes
maximum age
flush triggers
partial-failure policy
ordering
retry scope
```

A batch with only an item count can still hold unbounded bytes. A batch with no age bound can wait forever under low load.

## Observability signal table

### Event

A discrete occurrence with structured fields.

Use for:

- admission decision;
- parse failure;
- state transition;
- retry decision;
- dependency failure;
- rollout or configuration change.

### Span

A causal operation with duration and child activity.

Use for:

- request;
- batch;
- dependency call;
- snapshot generation;
- release step.

### Counter

Monotonically accumulated events.

Examples:

- accepted records;
- rejected records;
- retries;
- completed snapshots.

### Gauge

Current observed state.

Examples:

- active connections;
- queue depth;
- retained series.

State whether it is advisory or authoritative.

### Histogram

Distribution of observations.

Examples:

- request latency;
- queue residence;
- record size;
- batch size.

### Audit record

Durable domain-significant fact with stronger retention and integrity needs than ordinary diagnostics.

## Cardinality review

Safe low-cardinality dimensions:

- operation name;
- outcome class;
- bounded status code;
- deployment version;
- region from a controlled set.

Dangerous high-cardinality dimensions:

- request ID;
- user or tenant ID;
- raw URL or path;
- error text;
- payload content;
- timestamp as a label;
- arbitrary metric name from untrusted input.

High-cardinality identity belongs in traces or sampled events, not metric labels.

## Reliability reference

### Service-level indicator

Define:

```text
population
successful event
measurement point
window
exclusions
data source
```

### Service-level objective

Target for the SLI over a window. Example:

```text
99.9% of admitted snapshot requests complete successfully
within 100 ms over a rolling 28-day window.
```

This still requires precise definitions of admitted, success, and measurement.

### Error budget

For objective `S` over `N` events:

```text
budgeted failures = N × (1 - S)
```

A time-based objective uses a time population instead. Error budgets guide risk; they do not relax correctness or security.

### Retry checklist

- operation idempotent or protected by an idempotency key;
- error classified transient;
- one end-to-end deadline;
- bounded attempts;
- exponential or policy-defined backoff;
- bounded jitter;
- server retry hints considered;
- retry amplification measured;
- terminal failure preserved.

### Degraded response

State:

- which behavior remains;
- what is missing or stale;
- age and completeness;
- whether writes are accepted;
- how clients detect degradation;
- trigger and exit conditions.

## Security review table

| Element | Questions |
|---|---|
| Asset | What must remain confidential, integral, available, or isolated? |
| Actor | Anonymous client, authenticated tenant, operator, dependency, build contributor? |
| Boundary | Network, file, environment, CI, package registry, admin endpoint? |
| Capability | Read, write, execute, allocate, enumerate, impersonate, publish? |
| Abuse | Injection, exhaustion, traversal, confused deputy, leakage, tampering? |
| Control | Validation, authorization, limit, isolation, signature, redaction? |
| Evidence | Test, review, scanner, manifest, runtime signal? |
| Residual risk | What remains and who accepts it? |

## Cargo profile reference

Important profile settings include:

- `opt-level`;
- `debug`;
- `strip`;
- `debug-assertions`;
- `overflow-checks`;
- `lto`;
- `panic`;
- `incremental`;
- `codegen-units`;
- `rpath`.

Measure combinations. A smaller binary profile can reduce runtime speed or diagnostics. A profiling profile often needs optimization and symbols.

Example:

```toml
[profile.profiling]
inherits = "release"
debug = 1
strip = "none"

[profile.dist]
inherits = "release"
lto = "thin"
codegen-units = 1
strip = "symbols"
```

Profile choice is part of the artifact identity.

## Release manifest

Recommended deterministic fields:

```text
artifact name
semantic version
source revision
source-tree status
Cargo.lock digest
toolchain
target triple
profile
feature set
artifact size
artifact SHA-256
configuration schema version
protocol or storage version
build-system identity
```

Wall-clock timestamps make byte-for-byte reproduction harder. Store release time in external metadata unless the binary contract requires it.

## Production readiness questions

### Workload

- expected and peak offered rate;
- burst duration and skew;
- request and payload distributions;
- tenant distribution;
- growth assumption.

### Readiness capacity review

- first saturating resource;
- queue and concurrency limits;
- memory model;
- dependency quotas;
- failover and rollout headroom.

### Failure

- overload response;
- dependency timeout;
- retry amplification;
- partial data;
- restart behavior;
- data compatibility.

### Operation

- liveness and readiness;
- dashboards and alerts;
- configuration ownership;
- runbooks;
- on-call and escalation;
- backup and rollback.

### Security

- authentication and authorization;
- secret lifecycle;
- least privilege;
- dependency policy;
- artifact provenance;
- incident disclosure.

### Rollout

- canary population;
- promotion criteria;
- observation window;
- rollback trigger;
- incompatible data or protocol handling;
- rehearsal result.

## Claim-language discipline

Prefer:

- “On the reference x86_64 host, corpus v3 showed…”
- “The queue type enforces at most 1,024 enqueued items.”
- “The service policy rejects new work when all permits are held.”
- “The release profile selects thin LTO.”
- “The parser preserves source order by contract.”

Avoid:

- “Rust is always zero cost.”
- “This is zero copy.”
- “The service can handle 100k requests.”
- “The binary is reproducible.”
- “Metrics are exact.”
- “Retries make it reliable.”

The precise sentence is not bureaucratic. It tells the reader what may be relied upon.
