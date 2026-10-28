# ServiceWire Engineering Guide

ServiceWire is the cumulative Course 6 product: a bounded in-memory job service with several network adapters and one supported client.

The capstone is not a framework survey. It is a proof that one application contract can remain coherent across HTTP/1.1, HTTPS, HTTP/2, server-sent events, UDP discovery, retries, overload, and shutdown.

## Product boundary

ServiceWire accepts small jobs and executes four deterministic operations:

| Operation | Payload | Result |
|---|---|---|
| `uppercase` | UTF-8 text | uppercase text |
| `word-count` | UTF-8 text | decimal word count |
| `checksum` | UTF-8 text | SHA-256 hexadecimal digest |
| `sleep` | decimal milliseconds | confirmation after bounded cooperative delay |

The system is process-local. Jobs, idempotency records, and event history are lost when the process exits. That is deliberate. Course 7 adds durable persistence and distributed workflow mechanisms.

## Public HTTP contract

### `POST /v1/jobs`

Required headers:

```text
Content-Type: application/json
Idempotency-Key: <validated key>
```

Body:

```json
{
  "operation": "uppercase",
  "payload": "hello"
}
```

Success:

```http
202 Accepted
Location: /v1/jobs/job-000001
ETag: "job-job-000001-rev-1"
Content-Type: application/json
```

```json
{
  "id": "job-000001",
  "revision": 1,
  "state": "queued",
  "operation": "uppercase"
}
```

Same key and same semantic command returns the existing submission result. Same key and different command returns a stable conflict problem.

### `GET /v1/jobs/:id`

Returns current job representation and ETag.

`If-None-Match` with the current tag returns 304 without a body.

### `HEAD /v1/jobs/:id`

Returns the same representation metadata as GET without body bytes.

### `GET /v1/stats`

Returns bounded current application state:

```json
{
  "health": "healthy",
  "readiness": "ready",
  "queued": 0,
  "active": 1,
  "retainedJobs": 8,
  "idempotencyRecords": 8,
  "eventSequence": 24,
  "subscribers": 2
}
```

### `GET /v1/health`

Returns liveness and readiness. `HEAD` is supported.

### `GET /v1/events`

Opens SSE. Cursor can be supplied by `Last-Event-ID` or `after` query. The server rejects conflicting cursor sources.

A replay gap is reported before event-stream headers are committed.

## Problem contract

Every finite application error uses `application/problem+json`:

```ts
export interface Problem {
  readonly type: string;
  readonly title: string;
  readonly status: number;
  readonly code: string;
  readonly detail: string;
  readonly requestId: string;
}
```

Stable codes include:

```text
ROUTE_NOT_FOUND
METHOD_NOT_ALLOWED
UNSUPPORTED_MEDIA_TYPE
BODY_REQUIRED
BODY_TOO_LARGE
MALFORMED_JSON
INVALID_REQUEST
IDEMPOTENCY_KEY_REQUIRED
IDEMPOTENCY_CONFLICT
JOB_NOT_FOUND
PRECONDITION_FAILED
OVER_CAPACITY
NOT_READY
REPLAY_GAP
INTERNAL
```

Peer-visible details are bounded. Internal causes and stack traces never enter the response.

## Domain model

### Job identity

Job IDs are assigned by one application authority:

```text
job-000001
job-000002
...
```

They are stable within one process lifetime. ID exhaustion is handled explicitly rather than wrapping.

### Job states

```ts
type JobState =
  | { readonly kind: 'queued' }
  | { readonly kind: 'running'; readonly startedAtMs: number }
  | {
      readonly kind: 'succeeded';
      readonly startedAtMs: number;
      readonly completedAtMs: number;
      readonly result: string;
    }
  | {
      readonly kind: 'failed';
      readonly startedAtMs: number;
      readonly completedAtMs: number;
      readonly code: string;
      readonly message: string;
    }
  | {
      readonly kind: 'cancelled';
      readonly completedAtMs: number;
      readonly cause: 'shutdown' | 'user';
    };
```

The base reference uses queued, running, succeeded, and failed. Cancelled exists internally for shutdown. Public user cancellation is the final independent feature.

Every transition increments revision and appends one event.

### State authority

The `ServiceWire` application object owns:

- next job ID;
- job collection;
- queue;
- active count;
- maximum jobs and active operations;
- idempotency records;
- event journal;
- readiness/quiescing state;
- executor scheduling;
- transition and event publication.

Transport adapters cannot mutate jobs directly.

## Configuration

A validated configuration includes:

```ts
interface ServiceLimits {
  readonly maxConnections: number;
  readonly maxHttp2Sessions: number;
  readonly maxHttp2Streams: number;
  readonly maxRequestBodyBytes: number;
  readonly maxResponseBodyBytes: number;
  readonly maxJobs: number;
  readonly maxActiveJobs: number;
  readonly maxIdempotencyRecords: number;
  readonly maxEvents: number;
  readonly maxSubscribers: number;
  readonly maxSubscriberQueueBytes: number;
  readonly maxOperationMs: number;
  readonly heartbeatMs: number;
  readonly shutdownGraceMs: number;
}
```

Configuration validation rejects non-integers, unsafe values, inconsistent limits, and impractical zeroes. The course uses conservative small defaults to make overload tests easy.

## Commit sequence

Submission occurs synchronously under one process authority:

```text
validate command
        ↓
validate key
        ↓
compute semantic fingerprint
        ↓
look up idempotency record
        ↓
reject conflict or replay existing
        ↓
check capacity
        ↓
assign job ID
        ↓
insert in-progress idempotency record
        ↓
insert queued job revision 1
        ↓
append job-created event
        ↓
store terminal submission result in idempotency record
        ↓
schedule executor pump
```

No `await` appears inside this commit section. Later durable persistence will require a stronger serialization or transaction boundary.

## Executor

The executor keeps at most `maxActiveJobs` running. It selects queued jobs in job-ID order.

Transition:

```text
queued → running
```

is synchronous and emits an event before operation execution begins.

Operations:

- `uppercase`, `word-count`, and `checksum` complete synchronously but are wrapped in an owned async task so their terminal transition is observed uniformly;
- `sleep` uses a cancellable delay bounded by `maxOperationMs`.

Every task settles through one completion path. Internal task rejection cannot leave a job permanently running.

## Event journal

The journal owns:

- monotonic sequence;
- bounded retained events;
- subscriber set;
- subscriber queue bound;
- replay selection;
- replay-gap detection;
- shutdown close.

An event:

```ts
interface ServiceEvent {
  readonly sequence: number;
  readonly type:
    | 'job-created'
    | 'job-running'
    | 'job-succeeded'
    | 'job-failed'
    | 'job-cancelled'
    | 'service-quiescing';
  readonly jobId?: string;
  readonly revision?: number;
  readonly occurredAtMs: number;
}
```

The event payload is intentionally small. Clients fetch job representations for details.

## HTTP adapter architecture

The application protocol is split into two layers.

### Finite dispatcher

A transport-neutral dispatcher receives:

```ts
interface FiniteHttpRequest {
  readonly method: string;
  readonly url: URL;
  readonly headers: ReadonlyMap<string, string | readonly string[]>;
  readonly body: Uint8Array;
  readonly requestId: string;
}
```

and returns:

```ts
interface FiniteHttpResponse {
  readonly status: number;
  readonly headers: ReadonlyMap<string, string>;
  readonly body: Buffer;
  readonly omitBody: boolean;
}
```

This layer owns route selection and response representation. It does not own sockets.

### Transport adapters

HTTP/1.1 and HTTP/2 adapters own:

- request object/stream;
- bounded body collection;
- connection/session/stream registries;
- pressure;
- response writes;
- early close;
- transport diagnostics;
- graceful shutdown.

Both call the same finite dispatcher.

SSE is handled by the HTTP/1.1 adapter because it has a long-lived body and separate ownership.

## HTTP/1.1 and HTTPS runtime

A shared factory starts either `http.Server` or `https.Server`. Required TLS materials are loaded before the listener is published.

The adapter configures:

- maximum connections;
- request and headers timeouts;
- keep-alive timeout;
- body deadline;
- active request registry;
- socket registry;
- quiescing admission;
- graceful close and force destroy.

Tests use port zero and actual bound ports.

## HTTP/2 runtime

The base implementation uses cleartext prior-knowledge h2c for local study.

It tracks:

- sessions;
- streams;
- maximum concurrent streams;
- per-stream body bytes;
- global active finite requests;
- stream reset;
- session errors;
- GOAWAY;
- drain and forced destroy.

It supports finite routes only. SSE remains HTTP/1.1.

## TLS fixtures

The repository includes a dedicated local teaching CA certificate, server certificate, and server key.

They are used only for tests and demos. They are not production credentials. The certificate identifies `localhost` and `127.0.0.1`. Clients explicitly configure the CA and expected server name.

The course never sets `rejectUnauthorized: false`.

## UDP discovery

Discovery request:

```text
SERVICEWIRE-DISCOVER-V1<TAB><32-lowercase-hex-nonce>
```

Response:

```text
SERVICEWIRE-HERE-V1<TAB><nonce><TAB><advertised-url><TAB><version>
```

The component:

- binds to configured local host/port;
- enforces datagram byte limit;
- validates exact syntax;
- echoes only the accepted nonce;
- advertises configured URL;
- rate-limits or bounds concurrent handling;
- closes during quiesce;
- does not authorize clients.

The supported client can discover an endpoint in local tests, but ordinary HTTP/TLS validation still applies afterward.

## Supported client

`ServiceWireClient` owns:

- private HTTP and HTTPS agents;
- base URL;
- CA/servername policy;
- one deadline per semantic operation;
- response-byte limit;
- redirect policy;
- attempt history;
- retry policy;
- close lifecycle.

Methods:

```ts
submit(command, idempotencyKey, options?)
getJob(id, options?)
stats(options?)
health(options?)
close()
```

The client returns typed results and problems rather than raw response objects.

Submission retries preserve key and exact body. The client does not invent a key silently because semantic identity belongs to the caller.

## CLI

```text
servicewire serve [options]
servicewire submit <base-url> --key <key> --operation <op> --payload <text>
servicewire get <base-url> <job-id>
servicewire stats <base-url>
servicewire discover <host> <port>
servicewire demo
servicewire help
servicewire version
```

`serve` reports actual bound endpoints only after startup succeeds. Signals initiate the complete runtime shutdown route. The process chooses exit status after owned output and cleanup complete.

`demo` starts a local service, submits jobs through the supported client, reads them, opens a small event subscription, and closes every resource in `finally`.

## Startup

Startup stages:

1. validate configuration;
2. construct application and journal;
3. load TLS materials;
4. create server objects;
5. bind HTTP;
6. bind HTTPS if configured;
7. bind HTTP/2 if configured;
8. bind UDP discovery if configured;
9. publish ready state;
10. return runtime handle.

Any required-stage failure triggers reverse-order cleanup. Endpoint output is not printed before publication.

## Shutdown

```text
ready
   ↓
quiescing
   ↓
draining
   ↓
aborting when grace expires
   ↓
joining
   ↓
stopped
```

The runtime:

- marks readiness false;
- stops discovery;
- closes listeners;
- rejects new submission commands;
- ends SSE subscriptions;
- sends/initiates HTTP/2 graceful closure;
- waits for active finite requests and jobs under one deadline;
- cancels remaining cooperative work;
- destroys remaining sockets and sessions;
- clears timers;
- joins every owner;
- produces terminal report.

Repeated `close()` calls return the same completion.

## Required tests

### Domain

- all operation results;
- operation bounds;
- job state transitions;
- revisions;
- event publication;
- active job limit;
- retained job limit;
- shutdown cancellation.

### Idempotency

- first commit;
- same-key replay;
- same-key conflict;
- capacity;
- no duplicate job after response loss;
- no eviction of in-progress identity.

### HTTP/1.1

- route and method matrix;
- media type;
- body limit;
- JSON and schema failure;
- HEAD;
- ETag and 304;
- problem details;
- early disconnect;
- quiescing.

### Client

- bounded success and error bodies;
- deadline;
- retry;
- ambiguous commit;
- close;
- no redirect or controlled redirect policy.

### TLS

- trusted localhost;
- wrong hostname;
- untrusted issuer;
- ALPN;
- shutdown.

### HTTP/2

- equivalent finite routes;
- concurrent streams;
- stream reset;
- body limit;
- GOAWAY;
- forced session destroy.

### SSE

- encoding;
- replay;
- replay gap;
- race-free opening;
- heartbeat;
- slow subscriber;
- shutdown.

### UDP

- valid discovery;
- wrong nonce;
- malformed input;
- timeout;
- close.

### Lifecycle

- port-zero actual reporting;
- injected startup failure at each stage;
- reverse rollback;
- one shutdown grace;
- terminal report;
- no owned resources remain.

## Module increments

| Module | Increment |
|---:|---|
| 51 | endpoint types, resolver boundary, deadline, actual address reporting |
| 52 | connection registry, body/framing discipline, socket shutdown |
| 53 | optional UDP discovery |
| 54 | finite HTTP/1.1 adapter |
| 55 | routes, validation, jobs, idempotency, revisions, ETags |
| 56 | supported client |
| 57 | HTTPS and trusted client configuration |
| 58 | h2c finite adapter |
| 59 | SSE event stream |
| 60 | startup rollback, overload, health/readiness, complete shutdown |

## Independent mastery extension — conditional cancellation

Add:

```text
POST /v1/jobs/:id/cancel
If-Match: "<current-job-etag>"
```

Requirements:

- bodyless request;
- valid job ID;
- required current `If-Match`;
- 412 for stale precondition;
- queued job transitions to cancelled;
- cooperative running sleep can transition to cancelled;
- synchronous operation can win race and remain terminal;
- terminal job follows documented conflict/idempotent policy;
- repeated successful cancellation does not increment revision again;
- cancellation event;
- HTTP/1.1 and HTTP/2 parity;
- client method;
- shutdown cause remains distinguishable from user cause;
- updated stats, tests, docs, and final review.

The extension is complete only when every supported protocol surface follows the same new domain contract.

## Completion standard

ServiceWire is complete when:

- every package type-checks and tests;
- all investigations produce expected outcomes;
- no unbounded peer-controlled retention exists in the declared product;
- every private agent, socket, session, stream, subscriber, timer, and task has a terminal owner;
- the final report reconciles accepted and terminal work;
- the independent cancellation feature is implemented and defended;
- limitations are stated without presenting process-local state as durable or distributed.
