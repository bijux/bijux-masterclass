# MetricRail

## Course role

MetricRail is a bounded telemetry aggregator with offline and network paths, representative benchmarks, profiling hooks, memory and byte ledgers, structured tracing, overload policy, security and dependency records, release manifests, runbooks, and rollout exercises.

MetricRail is not a showcase of ten independent features. It is the place where the course’s mechanisms must coexist without creating a second owner for state, validation, order, failure, compatibility, or resource policy.

## Invariants carried through the product

- Every performance claim names workload, metric, population, percentile or statistic, and correctness oracle.
- Profiles, allocation counts, byte traces, and saturation curves are observations of named artifacts and environments.
- Live metrics never replace authoritative post-operation state.
- Overload, retry, degradation, recovery, and terminal accounting share one bounded policy.
- Threat models and dependency records state assets, actors, entry points, controls, and residual risk.
- Release manifests tie source, toolchain, target, profile, features, lock state, artifact digest, and rollback plan together.

## Module-to-product map

| Module | Mechanism added | Acceptance criterion |
|---:|---|---|
| 81 | Performance Contracts, Workloads, and Benchmark Design | Turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle |
| 82 | CPU Profiling, Cost Models, and Hot-Path Optimization | Choose sampling, instrumentation, counters, and targeted tracing based on the question being asked |
| 83 | Allocation, Memory Footprint, and Ownership Cost | Distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count |
| 84 | Data Movement, Buffering, and Zero-Copy Boundaries | Trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers |
| 85 | Runtime Efficiency: Contention, Queueing, Batching, and Async Load | Separate service time, wait time, queue depth, concurrency, throughput, and utilization |
| 86 | Observability: Structured Tracing, Metrics, and Diagnostic Context | Separate events, spans, metrics, profiles, and domain audit records by the questions they can answer |
| 87 | Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation | Write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous |
| 88 | Security and Supply-Chain Engineering | Identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service |
| 89 | Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases | Explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy |
| 90 | Production Readiness, Capacity Planning, Rollouts, and Incident Learning | Write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery |

## Reading route

1. Read the MetricRail contract and non-goals in the [engineering guide](../course-book/capstone.md).
2. Locate the type or component that owns each invariant above.
3. Run the baseline tests and one end-to-end demonstration before changing code.
4. Implement only the current module increment and its adversarial test.
5. Trace success, rejection, partial failure, cleanup, order, and capacity through the public surface.
6. Re-run the complete course route, then explain which claims remain conditioned on a compiler, target, scheduler, peer, workload, or operating system.

MetricRail is the cumulative capstone for Rust Performance and Production Engineering. It is a bounded telemetry aggregator used to practice benchmark design, profiling, allocation analysis, byte-lifecycle design, load behavior, observability, resilience, security review, release engineering, and production readiness.

## Record format

```text
tenant<TAB>metric<TAB>timestamp_ms<TAB>value
```

Identifiers are bounded ASCII names. Values must be finite. Timestamps are monotonically nondecreasing within one series.

## Commands

```text
metricrail analyze <events.tsv>
metricrail serve <address>
metricrail load <address> <events.tsv> [connections]
metricrail version
metricrail help
```

## TCP protocol

```text
INGEST<TAB>tenant<TAB>metric<TAB>timestamp_ms<TAB>value
SNAPSHOT
HEALTH
QUIT
```

The service rejects lines, identifiers, queues, connections, series, retained identifier bytes, and snapshots above configured limits. It owns aggregation through one broker task, which gives the product one semantic commit point and deterministic update order.

## Engineering boundaries

### Correctness

Unit and integration tests preserve parser grammar, failure atomicity, timestamp ordering, deterministic snapshots, physical source lines, redaction, and protocol responses.

### Performance

`benches/ingest.rs` provides microbenchmarks for parsing, applying one record, and rendering a snapshot. The benchmark charter in the course book requires representative corpora and end-to-end confirmation. No nanosecond threshold is treated as portable.

### Memory

Borrowed parsing delays identifier allocation until after validation. The store owns only durable identifiers. Queue, line, series, identifier storage, and snapshot limits are explicit.

### Observability

`tracing` spans identify connections and decisions without emitting tenant or metric values by default. In-process counters are advisory operational telemetry; the broker’s store remains authoritative for series state.

### Reliability

The broker mailbox rejects before semantic commit when full. Network overload is a typed response. Shutdown stops listener admission, drains connection tasks for one grace interval, aborts remaining tasks, and joins the broker.

### Security

The parser validates sizes before ownership promotion. Diagnostic types redact identifiers. The teaching service intentionally omits authentication and TLS; deploy it only on a trusted interface or behind a suitable authenticated encrypted proxy.

### Release

Build metadata contains source revision, target, profile label, toolchain, and package version without wall-clock timestamps. The `profiling` and `dist` profiles are separate products and must be measured independently.

## Commands for development

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace --all-targets
cargo test --workspace --doc
cargo bench --bench ingest
cargo build --profile dist
```

## Operations material

- `operations/CONFIGURATION.md`
- `operations/CAPACITY.md`
- `operations/OBSERVABILITY.md`
- `operations/SECURITY.md`
- `operations/RUNBOOK.md`
- `operations/ROLLOUT.md`
- `operations/INCIDENT-DRILL.md`

These files are part of the product. They state the workload envelope, signal meanings, threat boundaries, mitigations, rollout criteria, and learning route.
