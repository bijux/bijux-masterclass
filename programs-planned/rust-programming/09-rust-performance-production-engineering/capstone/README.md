# MetricRail

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
