# MetricRail Engineering Guide

MetricRail is the cumulative product for Course 9. It is a bounded telemetry aggregation service designed to be measured, profiled, observed, hardened, packaged, and operated. The domain is intentionally compact so that production behavior remains understandable end to end.

The project is not an observability backend and does not attempt distributed storage, replication, arbitrary query languages, authentication infrastructure, or high availability. Those would obscure the course’s purpose. MetricRail is a single-process service with explicit limits and deterministic output. The engineering challenge is to make every production claim precise.

## Product contract

MetricRail accepts telemetry records:

```text
tenant<TAB>metric<TAB>timestamp_ms<TAB>value
```

Example:

```text
acme	request_latency_ms	1723075200000	18.5
acme	request_latency_ms	1723075201000	22.0
north	error_count	1723075201000	1
```

Each accepted record updates one series identified by `(tenant, metric)`. A series retains:

- count;
- finite sum;
- minimum;
- maximum;
- latest timestamp;
- latest value.

The implementation rejects:

- missing or extra fields;
- empty tenant or metric;
- identifiers above configured byte limits;
- tabs, line breaks, control characters, or unsupported identifier characters;
- invalid timestamps;
- non-finite numeric values;
- timestamps that move backwards within one series;
- arithmetic overflow;
- new series after the series limit;
- input lines above the line limit;
- batches above configured record or byte limits.

MetricRail’s deterministic snapshot is ordered first by tenant and then by metric. Floating-point output uses one documented rendering policy. The same accepted record sequence produces the same snapshot regardless of map iteration order, connection scheduling, or load-client concurrency.

## Interfaces

### Offline analysis

```text
metricrail analyze <events.tsv>
```

The command reads a bounded file, validates every physical line, applies records in order, and prints the deterministic snapshot only after the complete input succeeds. A malformed line reports its physical line number; no partial snapshot is emitted.

### TCP service

```text
metricrail serve <address>
```

The service uses a bounded line protocol:

```text
INGEST<TAB>tenant<TAB>metric<TAB>timestamp_ms<TAB>value
SNAPSHOT
HEALTH
QUIT
```

Responses:

```text
OK
ERR<TAB>code<TAB>message
SNAPSHOT-BEGIN<TAB>series-count
SERIES<TAB>tenant<TAB>metric<TAB>count<TAB>sum<TAB>min<TAB>max<TAB>latest-timestamp<TAB>latest-value
SNAPSHOT-END
HEALTHY<TAB>active<TAB>queued<TAB>series
BYE
```

The server bounds:

- accepted connections;
- line bytes;
- broker mailbox;
- active ingestion operations;
- series count;
- retained identifier bytes;
- snapshot bytes;
- shutdown grace period.

### Load client

```text
metricrail load <address> <events.tsv> [connections]
```

The load client is a controlled scenario generator, not a universal load-testing platform. It records offered, completed, rejected, and transport-failed operations. Its response-latency percentiles include requests that received either `OK` or a terminal `ERR`; connection failures and timeouts remain a separate failure count. It uses a versioned corpus and a declared concurrency level.

### Metadata

```text
metricrail version
metricrail help
```

`version` reports semantic version, source revision supplied by the build environment when available, target, profile label, and enabled product features. It does not embed a wall-clock build timestamp.

## Architecture

```text
CLI / TCP connection / load generator
                  ↓
         bounded line decoding
                  ↓
        borrowed record parsing
                  ↓
        validated owned identifiers
                  ↓
       single aggregation authority
                  ↓
       deterministic snapshot model
                  ↓
   CLI text / TCP response / trace events
```

The initial implementation uses one `tokio::sync::mpsc` broker for service mutations. This is not claimed to be universally fastest. It provides a clear semantic commit point, deterministic update order, and one location for series limits. Course 9 measures whether this design meets the declared envelope before considering sharding.

## Domain model

### Identifiers

`Tenant` and `MetricName` are validated newtypes. Validation occurs before allocation when possible. Their public constructors enforce:

- nonempty;
- maximum bytes;
- ASCII alphanumeric plus `-`, `_`, and `.`;
- no control characters;
- no protocol delimiters.

The service owns identifier strings because they outlive input frames. Borrowed parsing prevents temporary field allocations; ownership promotion occurs only after validation.

### Telemetry record

```rust
pub struct Record {
    tenant: Tenant,
    metric: MetricName,
    timestamp_ms: u64,
    value: f64,
}
```

The constructor rejects non-finite values. Parsing errors preserve field and source context without echoing the entire input line into diagnostics.

### Series state

```rust
pub struct Series {
    count: u64,
    sum: f64,
    min: f64,
    max: f64,
    latest_timestamp_ms: u64,
    latest_value: f64,
}
```

Update is failure-atomic. The implementation validates timestamp order and checked count before mutating. Floating-point sum is finite after every transition. This course does not promise numerically exact summation; the policy and its limitations are documented and benchmarked.

### Store

A `BTreeMap<SeriesKey, Series>` provides deterministic ordering directly. A `HashMap` plus explicit sort could be faster for some workloads; Course 9 treats that as a measured design choice rather than assuming either structure wins. The store enforces series and identifier-byte budgets.

## Error taxonomy

MetricRail distinguishes:

- `Usage` — invalid CLI arguments;
- `Io` — filesystem or socket failure;
- `LineTooLong` — line limit exceeded before full accumulation;
- `Parse` — invalid field grammar;
- `Domain` — identifier, timestamp, numeric, or series invariant violation;
- `Overloaded` — admission refused before semantic commit;
- `SnapshotTooLarge` — deterministic response exceeds configured bytes;
- `Protocol` — unsupported command or invalid command shape;
- `Shutdown` — operation rejected because quiescing began;
- `Internal` — invariant or task failure that cannot be attributed to input.

Public protocol errors use stable bounded codes. Detailed source errors remain in structured diagnostics and are not reflected verbatim to untrusted clients.

## Module 81 — Performance charter

Create:

```text
benchmarks/CHARTER.md
benchmarks/corpora/
benches/
```

The charter defines three operations:

1. parse one record;
2. apply a validated record;
3. render a snapshot.

For each, state:

- semantic oracle;
- representative, boundary, skewed, and malformed inputs;
- measured boundary;
- profile and feature set;
- baseline naming;
- latency or throughput metric;
- memory or allocation companion metric;
- regression decision;
- limitations.

The scenario workload includes:

- 80% records for a small hot set of series;
- 19% records spread across a long tail;
- 1% maximum-length valid identifiers;
- a separate malformed corpus;
- a separate high-cardinality corpus.

Do not set arbitrary “must be under N nanoseconds” thresholds before running on a named reference host. The repository includes benchmark structure and comparison policy; local baseline values remain external artifacts tied to hardware.

## Module 82 — Profile and cost model

Add phase-level spans or temporary profiling hooks around:

```text
decode
parse
identifier validation
map lookup
series update
snapshot traversal
snapshot rendering
```

Profile the release or profiling artifact under the charter corpora. Write a cost-model note containing:

- dominant stacks;
- inclusive and exclusive interpretation;
- scaling prediction;
- one rejected hypothesis;
- one selected change;
- end-to-end confirmation.

Possible experiments include:

- `BTreeMap` versus `HashMap` plus sort;
- repeated string hashing;
- snapshot allocation;
- formatting strategy;
- parser scanning.

No implementation is selected from theory alone.

## Module 83 — Allocation ledger

Create an allocation and retention table for:

- receive buffer;
- parsed borrowed fields;
- owned tenant and metric names;
- map nodes or buckets;
- snapshot rows;
- rendered response;
- tracing fields;
- load-client samples.

Define explicit capacities and release conditions. Add a benchmark or test harness that counts product-level allocation events where practical; do not claim a process-wide exact allocator count from a local wrapper.

Introduce reuse only with bounds. A reusable line buffer whose capacity exceeded `max_reusable_buffer_bytes` is dropped rather than pooled. Snapshot buffers are reused only within one request or a bounded pool.

## Module 84 — Byte journey

Use `BytesMut` for network line accumulation and freeze or split only when shared immutable views are useful. The parser accepts `&str` and returns a borrowed record:

```rust
pub struct BorrowedRecord<'a> {
    pub tenant: &'a str,
    pub metric: &'a str,
    pub timestamp_ms: u64,
    pub value: f64,
}
```

After validation, the broker command promotes only tenant and metric to owned newtypes. No borrowed field crosses the channel. This creates a clear lifetime boundary:

```text
connection buffer lifetime
        ↓ parse and validate
borrowed record lifetime
        ↓ promote durable fields
broker command lifetime
```

Document every application-level payload copy. Do not claim kernel-level zero copy.

## Module 85 — Load and saturation

The server exposes separate bounds:

```text
max_connections
mailbox_capacity
max_active_ingest
max_series
max_snapshot_bytes
```

Run the load client repeatedly across a declared concurrency sweep and record:

- offered;
- connected;
- completed;
- overload rejection;
- protocol failure;
- transport failure;
- p50, p95, and p99;
- total elapsed time.

Server telemetry records queue residence and active service separately. Determine the first saturation mechanism and set a recommended initial envelope below the unstable knee.

If batching is introduced, it must have maximum items, bytes, and age. The reference implementation keeps single-record commits so the reader can measure the fixed-cost trade-off before adding batch semantics.

## Module 86 — Observability

Use `tracing` spans:

```text
connection
command
ingest
snapshot
shutdown
```

Stable fields include:

```text
connection_id
command_kind
outcome
series_count
queue_depth_observed
record_bytes
```

Tenant and metric values are not emitted by default. The service can log a bounded classification or one-way test-safe surrogate when debugging policy explicitly permits it.

Metrics are represented by an in-process snapshot structure for the teaching product:

- accepted records;
- rejected records by bounded code;
- overload rejections;
- active connections;
- observed queue depth;
- completed snapshots;
- parse latency histogram buckets;
- queue residence histogram buckets.

Metric labels are enumerated types, not arbitrary strings.

`HEALTH` reports liveness and bounded current state. A separate readiness decision becomes false during quiescing or when an essential broker task has failed.

## Module 87 — Reliability policy

Define two service objectives:

1. admitted valid ingestion completes successfully within the target latency;
2. snapshot requests return a complete response within the target latency.

Overload rejections count as unsuccessful from the user perspective unless the product’s population explicitly excludes pre-admission probes. The report must state the choice.

MetricRail does not automatically retry ingestion on the server, and the supplied load client performs one attempt per record. A future client may retry a capacity response only after the protocol supplies an idempotency token, one overall deadline, a bounded attempt cap, and bounded backoff. The initial protocol has no durable idempotency store, so automatic mutation retries are deliberately disabled. This negative decision prevents a benchmark helper from teaching unsafe retry behavior.

Degraded mode can preserve ingestion while rejecting expensive snapshots when snapshot memory pressure is high. The response is explicit:

```text
ERR	DEGRADED_SNAPSHOT	snapshot temporarily disabled
```

Validation is never weakened.

## Module 88 — Threat model

Create a threat model covering:

### Assets

- aggregate integrity;
- tenant separation;
- service availability;
- release artifact integrity;
- operational diagnostics;
- configuration and credentials.

### Boundaries

- TCP listener;
- offline input file;
- CLI/environment configuration;
- health and metrics surfaces;
- dependency and registry downloads;
- build scripts;
- CI identity;
- release distribution.

### Controls

- line, field, batch, queue, series, and response limits;
- identifier validation;
- no shell execution;
- no dynamic code loading;
- exact dependency pins in the course release;
- secret redaction;
- operator endpoint binding policy;
- least-privilege runtime guidance;
- lockfile and artifact digests;
- advisory and license checks in CI policy.

The teaching service does not implement authentication or TLS. The deployment guide states that it must bind to a trusted interface or operate behind an authenticated encrypted proxy. This limitation is not hidden.

## Module 89 — Release engineering

Define profiles:

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

Measure candidate settings rather than treating them as universal recommendations.

The release process produces:

```text
metricrail
metricrail.manifest
configuration-reference.md
operations.md
LICENSE
```

The manifest contains deterministic sorted fields and SHA-256 for the binary. The course includes a small standard-library SHA-256 implementation only if needed for the lab; the capstone’s release script may use the platform `sha256sum` or `shasum` with explicit availability checks.

CI policy covers:

- format;
- Clippy;
- unit, integration, doc, and CLI tests;
- supported feature set;
- security policy;
- benchmark smoke;
- release build;
- installation smoke;
- manifest generation.

Performance regression comparison runs on controlled workers at a cadence appropriate for stable hardware, not on arbitrary shared runners.

## Module 90 — Production readiness

Create:

```text
operations/CONFIGURATION.md
operations/CAPACITY.md
operations/OBSERVABILITY.md
operations/SECURITY.md
operations/RUNBOOK.md
operations/ROLLOUT.md
operations/INCIDENT-DRILL.md
```

The capacity document names the first saturating resource, initial limits, expected workload, burst policy, headroom, and dependency assumptions.

The rollout uses a staged plan:

1. offline corpus verification;
2. shadow or non-authoritative traffic;
3. small canary;
4. measured expansion;
5. full promotion.

Promotion criteria use user-visible latency, errors, rejection, memory, and readiness. Rollback triggers and commands are written before the canary.

The incident drill simulates queue saturation and snapshot degradation. The runbook begins from symptoms:

```text
p95 queue residence rising
memory increasing with stable series count
readiness false
overload rejection rising
snapshot failures
```

For each, it identifies authoritative signals, safe mitigations, rollback, and escalation.

## Test architecture

### Unit tests

- parser field and limit cases;
- newtype validation;
- series transition invariants;
- deterministic rendering;
- metric bucket classification;
- configuration validation.

### Integration tests

- offline analysis;
- service protocol;
- overload rejection;
- snapshot ordering;
- shutdown;
- redaction;
- release metadata.

### Benchmark targets

- parse;
- apply;
- snapshot;
- representative scenario.

### Load and fault scenarios

- concurrency sweep;
- high-cardinality valid workload;
- hot-key skew;
- malformed burst;
- slow snapshot consumer;
- broker shutdown;
- quiesce under load.

### Security cases

- control characters;
- oversized line;
- huge numeric text;
- non-finite values;
- label-cardinality attempts;
- secrets in diagnostic structures;
- operator endpoint exposure policy.

## Completion defense

MetricRail is complete when you can answer:

1. Which behavior is semantic and which results are measured?
2. Which workload versions support the performance claims?
3. What dominates parse, ingest, and snapshot cost?
4. Which allocations and buffers dominate retained memory?
5. Where are bytes copied, shared, or promoted to ownership?
6. What saturates first and how is work rejected?
7. Which signals are authoritative?
8. What does degraded mode preserve?
9. Which threats remain because authentication and TLS are external?
10. Which exact artifact and profile were reviewed?
11. How is capacity calculated?
12. How is rollout stopped and reversed?
13. Which incident evidence would revise the architecture?

A polished dashboard or fast benchmark is not an adequate substitute for these answers.

## Engineering record

Keep one versioned record beside the capstone for every material change. Each entry should contain:

```text
source revision
claim changed
workload and corpus
environment
before result
after result
correctness result
resource trade-off
security or operability consequence
decision
removal trigger
```

This record prevents future readers from inheriting an optimization without its reason. It also separates historical measurements from current guarantees. When the workload, compiler, target, or architecture changes, mark old measurements as historical rather than quietly comparing incompatible numbers.

## Rejected architecture log

MetricRail should retain several deliberate negative decisions:

- no sharded store until profiles and saturation data show broker serialization is the limiting cause;
- no unbounded high-cardinality metric labels;
- no automatic mutation retry without durable idempotency;
- no shared byte view retained after the frame when copying compact identifiers releases more memory;
- no embedded build timestamp in the distribution artifact;
- no direct untrusted-network deployment without authentication and encryption supplied by the environment;
- no queue increase used as a substitute for capacity analysis;
- no weakened validation in degraded mode.

Rejected decisions are not permanent dogma. They state the current evidence threshold. A later design may reverse one when a new workload, implementation, or product requirement provides stronger evidence.

## Final demonstration

The final demonstration uses a clean checkout and a clean configuration directory:

1. run all behavior and documentation tests;
2. build the profiling artifact and execute the benchmark smoke route;
3. run offline analysis on valid and malformed corpora;
4. start the service on a loopback address;
5. execute a controlled load sweep;
6. request health and a deterministic snapshot;
7. trigger overload and verify typed rejection;
8. quiesce under active connections and verify complete shutdown;
9. build the distribution artifact;
10. generate and verify the release manifest;
11. install into a temporary prefix;
12. execute the rollback rehearsal.

The demonstration report names every unavailable platform tool rather than turning absence into success.

## Reader self-check

Before declaring the capstone complete, choose one ordinary telemetry file and one adversarial file. Trace both through CLI parsing, line bounds, borrowed parsing, ownership promotion, broker admission, store mutation, snapshot generation, diagnostics, and shutdown. For every transition, name the authority that decides success and the state visible after failure.

Then repeat the trace for a saturated service. Separate work rejected before broker commit from work accepted and later rejected by a domain invariant. Confirm that every accepted connection and command has a terminal outcome, every retained allocation has a release condition, every operational signal has bounded fields, and every artifact claim names the build configuration that produced it.

Finally, explain MetricRail to a reader who has not seen its implementation. The explanation should make the following facts predictable: why identifiers become owned, why the store is ordered, why queue growth is bounded, why live gauges are advisory, why mutation retries are disabled, why authentication is external, why profiling and distribution builds differ, and why rollout can stop even when unit tests remain green. If the explanation requires source-level trivia, the architecture is still too implicit.
