# Capstone — Analysis RPC Control Plane

Course 7 continues the Analysis Runs Platform. The public HTTP API and Analysis Events API remain intact. The capstone adds a controlled internal RPC surface:

```text
Public clients
    |
    v
HTTP/OpenAPI gateway ---------------------> public resource semantics
    |
    v
AnalysisControlService (gRPC) ------------> authoritative run decisions
    |                 |
    |                 +-------------------> transactional event outbox
    v
WorkerPlaneService (bidirectional stream) -> assignments, progress, results
    |
    v
DatasetTransferService -------------------> bounded binary upload/download
```

## Services

### AnalysisControlService

- `CreateRun` — unary, idempotent mutation;
- `GetRun` — unary authoritative read;
- `CancelRun` — unary conditional mutation;
- `WatchRun` — resumable server stream.

### DatasetTransferService

- `UploadDataset` — client stream with metadata-first framing;
- `DownloadArtifact` — bounded server stream with offsets and checksum.

### WorkerPlaneService

- `Work` — bidirectional worker session with durable assignment and lease authority.

## What remains outside gRPC

- the public HTTP API remains the external client contract;
- integration events remain the durable independent-consumer contract;
- domain invariants and same-process application logic remain local calls;
- PostgreSQL remains the authority for idempotency, leases, state, and outbox records.

## Evidence classes

The capstone separates schema evidence, generated-surface evidence, deterministic in-process behavior, live Python gRPC network evidence, full TypeScript network evidence, and TLS or infrastructure-backed evidence. Missing environment-backed evidence is reported as not executed. It is never inferred from a model test.


## End-to-end capstone progression

The capstone is built in ten increments. Each increment is useful by itself and preserves the predecessor guarantees.

### Increment 1 — interaction decision

Before a proto exists, create an interaction matrix. For each candidate call, record:

- caller and callee;
- capability and state owner;
- whether the caller needs an answer now;
- public, internal, or operator audience;
- expected latency and availability path;
- deadline and retry owner;
- transaction boundary;
- rollback path;
- reason not to use HTTP, an event, or a local call.

The approved RPC surface is intentionally small. The exercise includes rejected candidates because architecture quality depends on what the system refuses to distribute.

### Increment 2 — semantic message model

Model resources, requests, snapshots, stream frames, and worker assignments. Every field receives a semantic record: creator, unit, range, presence, sensitivity, identity scope, and compatibility rule. Cross-language fixtures prove optional fields, enum zero behavior, `oneof`, 64-bit integers, and canonical golden bytes.

### Increment 3 — compatibility policy

Freeze RPC 1.0. Build a descriptor inventory, consumer declarations, and golden binary fixtures. Evaluate candidates across wire, source, ProtoJSON, and behavioral dimensions. Reserve removed tags and names. Treat enum additions and field renames according to actual consumer evidence.

### Increment 4 — unary outcomes

Implement `CreateRun`, `GetRun`, and `CancelRun`. The handler layer performs transport mapping and delegates to existing application behavior. Expected application errors map to stable gRPC statuses and bounded details. The HTTP adapter preserves the public Problem Details contract. Response-loss experiments prove durable idempotency and reconciliation.

### Increment 5 — time and retry

Propagate one absolute deadline from the HTTP edge. Implement method-specific retry profiles. Query retries remain bounded; mutation retries require persistent request identity and fingerprint binding. Cancellation stops unnecessary work but never claims rollback after commit. Every ambiguous outcome has a query or replay path.

### Increment 6 — streams

Implement metadata-first upload, bounded artifact download, resumable run observation, and a worker bidirectional session. Define legal frame order, total and per-message size, queue capacity, maximum age, cancellation cleanup, reconnection, duplicate handling, and durable authority. HTTP/2 flow control is treated as one layer, not the whole backpressure system.

### Increment 7 — security

Bind calls to trusted workload identity and, where required, a delegated end-user principal. Enforce default-deny method policy, tenant-aware resource access, stream freshness, and assignment-generation fencing. Keep credentials out of statuses, logs, metrics, and traces. The fixture issuer and certificates remain educational material, not production identity claims.

### Increment 8 — operation

Manage reusable channels, health, resolution, balancing, reconnect backoff, keepalive, and graceful drain. Run two server instances to reveal hidden process-local state. A draining server stops admission, completes or terminates active work within a bound, and leaves durable state reconcilable.

### Increment 9 — generation and governance

Generate or inspect language surfaces, descriptor sets, catalogues, and reflection. Build representative clients. Run local and optional external compatibility checks. Detect drift between proto, generated code, registered services, policy, and documentation. Record unexecuted tool capabilities explicitly.

### Increment 10 — reversible release

Route public HTTP behavior through the internal RPC adapter under shadow and canary controls. Compare public responses, durable state, event history, security decisions, reliability signals, and performance budgets. Rehearse response loss, stale completion, slow streams, drain, and rollback. Export a service-boundary dossier for Course 8.

## Repository reading order

Use the implementation in this order:

1. `rpc-case/interaction-decisions.yaml`
2. `rpc-case/service-ownership.yaml`
3. `contracts/proto/bijux/analysis/v1/analysis.proto`
4. `contracts/descriptors/analysis-v1.json`
5. `rpc-case/rpc-catalog.yaml`
6. shared vectors and golden fixtures
7. primary language semantic adapters
8. primary language live server/client
9. second language comparison
10. release and handoff evidence

Starting with the server encourages framework-first reasoning. Starting with ownership and contract makes the runtime code explainable.

## Correctness invariants

The final system preserves these invariants:

- one request identifier and semantic input produce at most one logical run;
- changed semantic input under the same identifier is rejected;
- no read operation advances application state;
- no RPC response claims success before authoritative commit;
- no worker result is accepted without the current assignment and lease generation;
- no upload publishes unverified or partial content;
- no artifact download is trusted without completion and digest evidence;
- no stream can grow without message, byte, queue, concurrency, and time bounds;
- no internal metadata can assert unverified tenant or user authority;
- no schema release reuses a published field or enum number;
- no RPC migration changes the documented public HTTP or Event API behavior;
- rollback never requires duplicate mutation or historical event rewriting.

## Final evidence package

A complete learner submission contains:

```text
rpc-source-and-descriptor/
interaction-and-ownership/
model-vectors/
compatibility-report/
unary-status-report/
deadline-and-retry-report/
stream-pressure-report/
security-report/
lifecycle-report/
generation-and-catalogue-report/
public-http-and-event-comparison/
rollback-trace/
service-boundary-dossier/
```

Every report names its evidence class and limitations. A deterministic state-machine proof does not claim live load-balancer behavior. A successful Python network test does not claim TypeScript network parity. A tool that was unavailable is recorded as not executed.

## What Course 8 receives

Course 8 receives a system with three mature communication contracts:

- OpenAPI/HTTP for public resource behavior;
- AsyncAPI/events for durable facts and independent consumers;
- Protobuf/gRPC for controlled internal synchronous and streaming capabilities.

It also receives evidence that some capabilities should remain together. That is essential. Distributed architecture begins with ownership and failure boundaries, not with a target service count.
