# JobWire Engineering Guide

JobWire is the cumulative capstone for Course 8. It is a bounded single-process service that accepts a custom framed TCP protocol for job submission and exposes a small HTTP/1 operational surface. The product exists to force every major mechanism in the course to coexist under one explicit contract.

The capstone is not a framework. It is intentionally narrow:

- four deterministic operations;
- one protocol version;
- one in-flight request per TCP connection;
- one process-local broker authority;
- bounded queued and active work;
- process-local idempotency retention;
- read-only HTTP health and statistics;
- finite graceful shutdown.

The constraints make deep reasoning possible. Adding authentication, durable storage, TLS, multiplexing, distributed brokers, or a high-level web framework before the base contracts are proved would blur the learning target.

## How this capstone completes the course

JobWire is a bounded async job service with a framed TCP protocol, version negotiation, a broker authority, bounded queued and active work, idempotency records, structured cancellation, a small Hyper health surface, and deterministic tests.

The ten increments form one product history. An increment is accepted only when the new behavior fits the existing ownership and authority map, has a causal failure model, and preserves every earlier invariant not explicitly revised. The independent lab proves the mechanism in isolation; JobWire proves that it can coexist with nine other mechanisms.

### Product invariants

| # | Invariant that must survive every increment |
|---:|---|
| 1 | Every future that can remain pending has a wake source or terminal event. |
| 2 | Listeners, connections, broker work, HTTP tasks, and shutdown handles form one owned task tree. |
| 3 | Frame lengths are bounded before reserve or allocation and partial reads preserve parser state. |
| 4 | Protocol legality is an explicit state machine selected by negotiated version. |
| 5 | Mailbox, queued work, active work, retained results, and duplicate waiters are independently bounded. |
| 6 | Idempotency, retry, cancellation, quiescence, draining, abort, and join have separate semantics. |

For each JobWire change, annotate the owning component, state before and after success, state after every rejected or partial path, cleanup, order, capacity, and public compatibility. Where the course concerns compiler, platform, scheduler, workload, or peer behavior, label that condition rather than promoting it into an unconditional guarantee.

### Ten-module integration map

| Module | Mechanism | Capability visible in the product | Independent laboratory |
|---:|---|---|---|
| 71 | Futures, Polling, Wakers, and Async State Machines | Explain why a future is inert until polled | [One-Shot Signal](../labs/module-01-one-shot-signal/README.md) |
| 72 | Tokio Runtimes, Tasks, and Structured Async Lifecycles | Distinguish a runtime, worker thread, task, future, reactor, and blocking pool | [Task Nursery](../labs/module-02-task-nursery/README.md) |
| 73 | Async I/O, Buffers, Streams, and Framing | Distinguish readiness from transfer completion | [Bounded Length Codec](../labs/module-03-bounded-length-codec/README.md) |
| 74 | TCP, UDP, DNS, and Connection Lifecycles | Distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close | [Deadline Echo Service](../labs/module-04-deadline-echo-service/README.md) |
| 75 | Protocol State Machines, Versioning, and Defensive Parsing | Separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution | [Negotiated Command Protocol](../labs/module-05-negotiated-command-protocol/README.md) |
| 76 | Backpressure, Admission Control, and Fair Work Distribution | Find every accumulation point in an async service | [Bounded Relay Broker](../labs/module-06-bounded-relay-broker/README.md) |
| 77 | Cancellation Safety, Deadlines, and Graceful Shutdown | Derive cancellation behavior from future-owned state and external side effects | [Graceful Task Tree](../labs/module-07-graceful-task-tree/README.md) |
| 78 | HTTP Services with Hyper: Requests, Bodies, and Connections | Distinguish accepted transport, HTTP connection future, request future, body stream, and application service | [Hyper Health Surface](../labs/module-08-hyper-health-surface/README.md) |
| 79 | Network Failure, Idempotency, Retries, and Deterministic Testing | Classify failures by phase, scope, retryability, and commit ambiguity | [Idempotent Retry Client](../labs/module-09-idempotent-retry-client/README.md) |
| 80 | Integrated Async Service Architecture, Testing, and Audit | Construct a complete async service dossier | [Async Service Audit](../labs/module-10-async-service-audit/README.md) |

### How to read the implementation

Begin with the product promise and private invariant-bearing types. Next locate validation and conversion boundaries, state transitions, effectful operations, cleanup, deterministic rendering or wire behavior, and finally the tests. This order prevents `main.rs` call order from being mistaken for architecture.

Use a **async service dossier** to connect the implementation to the course. Every row should point to code, a test or review, and a documented limit on the claim. Missing evidence is not repaired by a stronger adjective.

### Acceptance traces

Preserve at least these six traces while completing the capstone:

1. JobWire ordinary success from external input to visible output;
2. malformed or unsupported input rejected before trusted state changes;
3. domain or capacity rejection with the original authoritative state preserved;
4. partial work followed by failure, including cleanup and retry state;
5. the largest accepted and smallest rejected order, size, lifetime, or capacity boundary;
6. one compatibility, platform, scheduler, peer, compiler, or workload edge specific to this course.

A passing test suite is necessary, but the final defense also names a simpler architecture and explains why this product’s requirements justify the additional mechanism. If the simpler design would satisfy the real contract, prefer it.

## Product story

A client connects and sends a length-delimited `HELLO` frame. After version 1 is accepted, it may send one request, receive one response, and continue. A `SUBMIT` request carries both a request ID and an idempotency key. The connection task validates the message and asks the broker to own the semantic operation. The broker either rejects admission, attaches the caller to an existing operation, or commits a new in-progress record and schedules bounded work. The terminal result remains retrievable through the same key during the process-local retention window.

A second listener serves `/health` and `/stats` through Hyper. This surface observes a broker snapshot; it does not submit jobs and does not wait behind the saturated work queue. The top-level supervisor owns listeners, service tasks, the broker, cancellation, grace, abort, joins, and process exit.

## Architecture

```text
                                  ┌──────────────────────────┐
TCP clients ──> TCP listener ───> │ framed connection tasks │
                                  └────────────┬─────────────┘
                                               │ bounded command
                                               ▼
                                      ┌─────────────────┐
                                      │ broker authority │
                                      └───────┬─────────┘
                                              │ bounded scheduling
                                              ▼
                                      ┌─────────────────┐
                                      │ async job tasks  │
                                      └─────────────────┘

HTTP clients ─> HTTP listener ─> Hyper connection tasks ─> status snapshot

supervisor ─> stop admission ─> cancel ─> drain ─> abort ─> join
```

## Public configuration

The `Config` type names all principal limits:

| Setting | Meaning |
|---|---|
| `max_connections` | simultaneous admitted JobWire TCP connections |
| `max_http_connections` | simultaneous admitted HTTP connections |
| `max_frame_bytes` | maximum TCP frame payload before protocol parsing |
| `broker_capacity` | maximum commands waiting in the broker mailbox |
| `max_queued_jobs` | committed jobs waiting for active execution capacity |
| `max_active_jobs` | jobs executing concurrently |
| `max_result_bytes` | terminal result payload retained by the broker |
| `max_idempotency_records` | process-local key records retained |
| `max_waiters_per_key` | duplicate callers attached to one in-progress operation |
| `handshake_timeout` | transport-to-ready protocol budget |
| `request_timeout` | per-request connection and broker wait budget |
| `write_timeout` | maximum response-write wait |
| `shutdown_grace` | drain time before abort |
| `max_sleep` | maximum teaching operation delay |

`max_result_bytes` is intentionally smaller than `max_frame_bytes`. A successful `OK` response adds a response tag, request identifier, separators, and framing overhead around the result. Configuration validation reserves a conservative 128-byte protocol envelope, so the broker never accepts a result size that the configured frame codec cannot later transmit. This is a product invariant, not an estimate of typical output.

Every value is validated as nonzero. Frame size also fits the protocol’s `u32` length prefix. The course’s memory estimate remains conservative and explicitly excludes runtime task allocation, channel overhead, hash-map capacity, allocator fragmentation, kernel buffers, socket structures, and Hyper internals.

## Binary framing

Every protocol payload is encoded as:

```text
4-byte unsigned big-endian payload length
payload bytes
```

The codec:

- peeks at a complete prefix before consuming it;
- converts and checks the length;
- rejects payloads above `max_frame_bytes` before reserve;
- uses checked total arithmetic;
- leaves incomplete bytes buffered;
- extracts one frame while preserving following frames;
- distinguishes clean EOF from a truncated prefix or payload;
- emits one canonical representation.

Framing knows nothing about `HELLO`, `SUBMIT`, or application state.

## JobWire V1 grammar

Payloads are UTF-8 and use tab-separated fields. Identifiers contain 1–64 ASCII alphanumeric, hyphen, underscore, or dot bytes. Payloads cannot contain tabs or line breaks in V1; a future version could introduce escaping or binary payload fields.

Client messages:

```text
HELLO\t1
SUBMIT\trequest-id\tidempotency-key\toperation\tpayload
STATS\trequest-id
PING\trequest-id
QUIT
```

Server messages:

```text
WELCOME\t1
OK\trequest-id\tresult
BUSY\trequest-id\tretry-after-ms
ERR\trequest-id-or-dash\tcode\tmessage
STATS-OK\trequest-id\thealth\tactive\tqueued\trecords\tcompleted\tfailed
PONG\trequest-id
BYE
```

The protocol parser is pure. It converts one frame payload into one typed message. The connection state machine decides whether the message is legal now. The broker decides whether a valid submission commits.

## Connection state

```text
Negotiating
    HELLO 1 ─────────> Ready(V1), WELCOME 1
    other message ───> terminal protocol error
    unsupported HELLO > terminal version error

Ready(V1)
    SUBMIT ──────────> one broker result, remain Ready
    STATS ───────────> snapshot, remain Ready
    PING ────────────> PONG, remain Ready
    QUIT ────────────> BYE, close
    HELLO ───────────> terminal state error
```

V1 is sequential within one connection. The connection does not read another request while waiting for the current response. This bounds per-connection in-flight state to one and makes response ordering obvious. Concurrency remains available across connections and broker jobs.

## Broker authority

The broker task owns:

- the idempotency map;
- record insertion and conflict detection;
- queued-job order;
- active-job task set;
- terminal result caching;
- waiter lists;
- status snapshot publication.

A connection never mutates these structures directly. This single authority avoids lock composition and makes the application commit point explicit.

### Commit point

A new request commits when the broker inserts:

```text
key → fingerprint + InProgress(waiters)
```

Before insertion, overload rejection means no semantic operation was accepted. After insertion, connection timeout or disconnect does not remove the operation. A retry with the same key and fingerprint attaches to the same record or obtains its terminal result.

### Duplicate behavior

| Existing state | Same fingerprint | Different fingerprint |
|---|---|---|
| no record | insert and schedule | not applicable |
| in progress | attach bounded waiter | `IDEMPOTENCY_CONFLICT` |
| completed | return cached result | `IDEMPOTENCY_CONFLICT` |

Waiters per key are bounded. Completed records are bounded by count. When capacity is reached, the broker evicts a completed record in deterministic insertion order. It does not evict an in-progress record merely to admit new work.

### Work scheduling

The broker separates:

- bounded mailbox capacity;
- bounded committed waiting jobs;
- bounded active jobs.

It never creates one async task per waiting request. It starts a job only when active count is below `max_active_jobs`. A terminal job updates the authoritative record before waiters are notified.

The teaching implementation’s operations are:

| Operation | Meaning |
|---|---|
| `uppercase` | Unicode uppercase conversion |
| `word-count` | whitespace-separated token count |
| `checksum` | deterministic FNV-1a corruption hash |
| `sleep-ms` | bounded async delay for lifecycle tests |

`checksum` is not a cryptographic integrity or authentication primitive.

## Capacity ledger

A JobWire deployment should complete a table with configured numbers:

| Location | Maximum | Saturation behavior |
|---|---:|---|
| admitted TCP connections | `max_connections` | accept loop waits; OS backlog may fill |
| decoded request per connection | 1 | connection stops reading until response |
| broker mailbox | `broker_capacity` | sender waits within request deadline |
| committed queued jobs | `max_queued_jobs` | new request receives `BUSY` before commit |
| active jobs | `max_active_jobs` | committed work remains in bounded queue |
| result per job | `max_result_bytes` | terminal domain failure |
| idempotency records | `max_idempotency_records` | completed record eviction or `BUSY` when all are active |
| waiters per key | `max_waiters_per_key` | `TOO_MANY_WAITERS` |
| admitted HTTP connections | `max_http_connections` | accept loop waits |
| HTTP request body | 1 KiB inspected maximum; routes require empty | 400/413 and connection close when needed |

The server also has kernel and runtime buffers outside these application bounds. State them as excluded rather than presenting the table as exact process memory.

## Cancellation and deadline model

### Connection cancellation

The connection task owns its socket, framed buffer, admission permit, and current reply future. Dropping it:

- closes the socket;
- releases the permit;
- drops any reply receiver;
- does not remove broker-owned committed work;
- does not erase the idempotency record.

An interrupted frame write closes the connection. JobWire does not attempt to resume a partially written frame.

### Broker cancellation

During service shutdown, the broker:

- stops accepting commands;
- marks queued work cancelled;
- signals active jobs;
- drains task results;
- publishes a shutting-down snapshot;
- exits only after its owned work reaches terminal state.

The top-level supervisor keeps the broker alive while connection tasks drain.

### Deadlines

The capstone uses stage-specific configuration for clarity, but client retry carries an overall deadline. A stronger production client would pass one absolute request deadline through connect, handshake, submit, and read. Workbook exercises require that improvement.

Timeout does not imply rollback. After broker commit, retry must reuse the same idempotency key.

## HTTP operational surface

JobWire exposes:

```text
GET /health
GET /stats
```

`/health` returns one of:

```text
state=starting
state=ready
state=shutting-down
state=failed
```

The current implementation publishes starting, ready, and shutting-down from broker lifecycle. A supervisor can extend it to publish failed after an unexpected authority exit.

`ready` means the process, listeners, and broker admission path are operating at the sampled instant. It does not guarantee a future job result or dependency availability.

`/stats` returns deterministic plain text:

```text
state=ready
active_jobs=0
queued_jobs=0
records=1
completed_jobs=1
failed_jobs=0
```

These counts are advisory snapshots. The broker’s own state remains authoritative.

HTTP request bodies are bounded and the two routes require an empty body. Hyper connection tasks are admission-limited, tracked, drained for a grace period, then aborted and joined.

## Client retry

`submit_with_retry` constructs one semantic key and reuses it across attempts. Each attempt uses a distinct request ID. Retryable categories are deliberately narrow:

- local I/O failure;
- stage timeout;
- server `BUSY`.

Protocol errors and domain rejections are terminal. The retry loop has an attempt maximum, exponential delay cap, and overall deadline. The teaching implementation uses deterministic delay rather than random jitter; a production client should add a tested jitter strategy.

## Error hierarchy

Public TCP error codes include:

```text
UNSUPPORTED_VERSION
HANDSHAKE_REQUIRED
ALREADY_NEGOTIATED
INVALID_UTF8
INVALID_SYNTAX
INVALID_ARGUMENT
UNKNOWN_OPERATION
IDEMPOTENCY_CONFLICT
TOO_MANY_WAITERS
JOB_FAILED
JOB_CANCELLED
SHUTTING_DOWN
```

Internal Rust errors retain I/O, Hyper, task, and protocol categories. Public rendering removes tabs and line breaks from messages so one error remains one protocol frame with stable field structure.

## Shutdown protocol

The top-level service owns one cancellation token and tracked TCP, HTTP, and broker tasks.

```text
1. signal arrives or a critical service task exits
2. root cancellation is triggered
3. TCP and HTTP accept loops stop admission
4. TCP connections observe cancellation
5. broker stops accepting work and settles owned jobs
6. service tasks drain within their configured grace
7. remaining connection tasks are aborted
8. every service and broker handle is awaited
9. the supervisor returns success or the first causal failure
```

The HTTP driver does not receive a per-connection graceful signal in the teaching implementation; keep-alive connections are allowed the service grace and then aborted. This is an explicit limitation, not an accidental omission.

## Testing strategy

### Pure tests

- frame split points and truncated EOF;
- protocol parse/render and identifier policy;
- operation execution and result bounds;
- configuration validation.

### Broker tests

- first submission;
- duplicate after completion;
- duplicate while in progress;
- changed fingerprint conflict;
- queue saturation;
- waiter maximum;
- result failure caching;
- record eviction;
- shutdown cancellation.

### Network tests

- handshake requirement;
- unsupported version;
- one-byte frame chunks;
- coalesced messages where legal;
- clean EOF;
- oversized frame;
- request timeout;
- connection admission saturation.

### HTTP tests

- exact status and deterministic body;
- method mismatch;
- unknown route;
- nonempty/oversized body;
- health under broker saturation;
- connection shutdown.

### Retry tests

- retryable versus terminal failures;
- same key across attempts;
- disconnect after commit;
- exact attempt count;
- overall deadline;
- in-memory scope limitation.

### Shutdown tests

- idle connections;
- active pre-commit request;
- committed sleeping job;
- grace expiry;
- repeated cancellation;
- all task sets empty before return.

## Increment 1 — Freeze the async state vocabulary

Before Tokio code, write the future-state ledger for connection handshake, frame read, broker wait, and response write. Record wake source and drop behavior. Implement no socket yet.

Completion evidence:

- every `Pending` state has a wake source;
- every suspension point lists retained values;
- response-write cancellation has a close policy;
- broker-wait cancellation does not claim rollback.

## Increment 2 — Own the runtime and task tree

Create the top-level supervisor and task-tree document. The supervisor will eventually own TCP service, HTTP service, and broker. Use `JoinSet` or explicit handles; no detached task.

Completion evidence:

- parent and join owner for every task class;
- startup and unexpected-exit policy;
- blocking-work policy;
- cancellation direction and terminal reporting.

## Increment 3 — Establish bounded framing

Implement `LengthCodec` and its split/coalescing/EOF tests. Keep protocol parsing in a separate module.

Completion evidence:

- maximum checked before reserve;
- checked prefix-plus-payload arithmetic;
- all representative split points;
- clean and truncated EOF distinction;
- canonical encode/decode round trip.

## Increment 4 — Own the connection lifecycle

Bind an ephemeral listener in tests, add connection admission, and track connection tasks. Implement handshake only.

Completion evidence:

- permit moves into each task;
- shutdown releases idle connections;
- unsupported version closes deliberately;
- accepted peer address remains an observation, not identity.

## Increment 5 — Freeze the wire protocol

Implement pure messages, parser, renderer, state machine, and public error codes. V1 remains sequential.

Completion evidence:

- complete grammar;
- state/message matrix;
- request and idempotency IDs separated;
- version and compatibility note;
- no socket in parser tests.

## Increment 6 — Bound demand end to end

Add the broker, bounded mailbox, bounded committed queue, active-job maximum, result maximum, waiter maximum, and record maximum.

Completion evidence:

- one authoritative commit point;
- exact overload behavior before commit;
- no task-per-waiting-request pattern;
- slow reply consumer does not retain active-job capacity;
- full capacity ledger.

## Increment 7 — Make cancellation and shutdown explicit

Add root and child cancellation tokens, connection selection, broker drain, grace, abort, and joins.

Completion evidence:

- stop admission first;
- pre-commit versus post-commit cancellation tests;
- repeated cancellation requests are harmless;
- all task handles reach terminal observation;
- blocking-work limitation documented.

## Increment 8 — Add an honest HTTP operational surface

Serve `/health` and `/stats` with Hyper over a separate listener. Read a snapshot rather than queueing behind jobs.

Completion evidence:

- pure route tests;
- body policy;
- deterministic output;
- explicit readiness meaning;
- tracked connection tasks and bounded admission.

## Increment 9 — Resolve ambiguous failure

Add idempotency records and client retry. Reuse one semantic key, preserve fingerprints, bound retention, and distinguish retryable failures.

Completion evidence:

- one execution after disconnect-after-commit;
- changed fingerprint rejected;
- duplicate in progress bounded;
- overall retry deadline;
- process-local guarantee stated.

## Increment 10 — Complete the service dossier

Finish all ledgers, integration tests, runbook, compatibility note, and architecture defense. Remove mechanisms without product responsibility.

Completion evidence:

- one successful request trace and every failure cut;
- resource envelope with exclusions;
- intersection test matrix;
- shutdown proof;
- explicit non-guarantees;
- explanation of the first assumption that fails under multiple replicas.

## Non-goals and honest limitations

JobWire does not claim:

- durable jobs or idempotency across restart;
- multi-process or multi-region authority;
- TLS, authentication, or authorization;
- cryptographic checksums;
- HTTP/2 or TCP request multiplexing;
- a hard memory byte limit including runtime and kernel resources;
- preemptive cancellation of arbitrary CPU or native work;
- exactly-once effects outside its process-local broker;
- stable scheduler order or exact timing.

These are not missing footnotes. They are boundaries that determine whether the design is suitable for a real product.

## Completion standard

The capstone is complete when you can run the full proof route and then defend, without reading source:

1. which event wakes each pending future;
2. who owns every task and handle;
3. how frame bytes are bounded;
4. which messages are legal in each state;
5. where semantic commitment occurs;
6. what bounds every accumulation point;
7. what cancellation leaves behind;
8. why one retry does not duplicate work;
9. what health and statistics prove;
10. how shutdown reaches and joins every descendant.


## Architecture defense checklist

Before treating JobWire as complete, defend the following claims from code and tests rather than intention:

1. **Future ownership:** every long-lived future owns the state it retains across suspension, and no borrowed stack state is smuggled into a detached task.
2. **Task accounting:** the supervisor observes the TCP service, HTTP service, and broker; connection and job task sets are drained or aborted under explicit deadlines.
3. **Frame safety:** a hostile length prefix is rejected before payload allocation, EOF distinguishes a clean boundary from truncation, and every split point produces the same decoded message.
4. **Protocol legality:** `HELLO` is required exactly once, unsupported versions close after a causal response, and malformed messages cannot mutate broker state.
5. **Admission authority:** one broker owns queued work, active work, idempotency records, duplicate waiters, and overload decisions. Connection tasks do not maintain competing capacity counters.
6. **Idempotency:** the key identifies one semantic operation; equal repeats share or retrieve one terminal result; changed content conflicts; bounded record retention is explicit.
7. **Panic terminality:** a job panic is mapped back to its semantic key, releases every waiter, increments failure accounting, and never leaves a permanent in-progress record.
8. **Cancellation safety:** dropping a client exchange does not roll back accepted work; retry uses the same key; shutdown cancels queued and active work according to documented policy.
9. **HTTP honesty:** `/health` reports broker state rather than claiming whole-system perfection, request bodies are bounded, connection shutdown is requested gracefully, and a grace deadline still bounds termination.
10. **Retry bounds:** attempts, per-attempt time, delay, server overload hints, and total deadline are finite. A timeout is represented as ambiguity, not proof of non-commit.
11. **Deterministic meaning:** protocol rendering, status fields, error codes, and terminal results do not depend on task completion order.
12. **Non-guarantees:** process-local idempotency is not durable across restart; plaintext TCP is not authenticated; health is an instantaneous observation; the service does not claim exactly-once execution across process failure.

For each claim, point to one implementation boundary, one adversarial test, and one failure path. A claim without all three is still an architectural intention.

## Final independent change

Add a `reverse` operation without altering the wire grammar, broker protocol, or retry machinery. The change should require one domain variant, parsing and rendering support, execution logic, help text, and tests. Then add a deliberately slow variant in a private test and prove that shutdown still produces one terminal result for every accepted key. The exercise is complete only when you can explain why the first change is local while the second crosses cancellation and lifecycle boundaries.
