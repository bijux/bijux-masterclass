# ServiceWire — Executable Capstone

ServiceWire is the cumulative product for Course 6. It is a bounded, process-local job service whose application contract is exposed through HTTP/1.1, HTTPS, h2c HTTP/2, server-sent events, UDP discovery, and a supported client. The implementation exists to make the course-book arguments concrete: transport adapters share one domain authority, every peer-controlled surface has a named bound, and startup and shutdown are owned protocols rather than incidental calls to `listen()` and `close()`.

Read the [ServiceWire engineering guide](../course-book/capstone.md) before reviewing source. The guide is normative for product behavior. Source files are one implementation of that contract.

## Runtime surfaces

ServiceWire provides these commands after compilation:

```text
servicewire serve [options]
servicewire submit <base-url> <operation> <payload> [options]
servicewire get <base-url> <job-id> [options]
servicewire stats <base-url> [options]
servicewire discover [options]
servicewire demo
servicewire help
servicewire version
```

The server owns four related listeners or endpoints:

- HTTP/1.1 for the finite application protocol and SSE;
- HTTPS for the same HTTP/1.1 contract under authenticated transport identity;
- h2c HTTP/2 for local study of sessions and streams without hiding protocol mechanics behind an application framework;
- UDP discovery for a bounded local convenience protocol that never grants authorization.

All adapters call the same `ServiceWire` application object. A transport cannot mutate job state, allocate job identifiers, publish events, or decide idempotency outcomes independently.

## Application contract

The finite HTTP routes are:

```text
POST /v1/jobs
GET  /v1/jobs/:id
HEAD /v1/jobs/:id
GET  /v1/stats
GET  /v1/health
HEAD /v1/health
GET  /v1/events
```

Submission requires a validated `Idempotency-Key`. The first accepted command creates one semantic operation. A repeated key with the same command returns the existing submission result; the same key with a different command is a conflict. A timed-out client therefore does not need to guess whether the server committed before the response was lost.

Job reads use revisions and entity tags. Conditional reads return `304 Not Modified` only when the supplied tag names the current representation. Job transitions append bounded events. SSE subscribers can replay retained events, receive a replay-gap error before stream headers are committed, and are disconnected when their queued bytes exceed the declared limit.

## Capacity model

ServiceWire deliberately separates capacities that weaker designs often collapse into one setting:

```text
accepted HTTP/1.1 and HTTPS connections
HTTP/2 sessions
HTTP/2 concurrent streams
request-body bytes
response-body bytes
retained jobs
active operations
idempotency records
event-journal entries
SSE subscribers
queued bytes per subscriber
operation duration
shutdown grace duration
```

A free socket slot does not imply job capacity. An available worker slot does not imply idempotency-record capacity. Health and readiness report the relevant application state rather than pretending that one listener state describes the complete service.

## Ownership and lifecycle

Startup constructs dependencies in order. If a later listener fails, previously opened listeners, agents, sockets, sessions, timers, and discovery endpoints are closed in reverse order before startup reports failure.

Shutdown has four named phases:

1. **Quiesce** — readiness becomes false and new admission stops.
2. **Drain** — accepted work may finish under one absolute grace deadline.
3. **Abort** — remaining jobs, connections, streams, subscribers, and timers are cancelled or destroyed.
4. **Join and report** — every owned asynchronous branch is observed before the final process status is chosen.

The implementation does not claim persistence, multi-process coordination, or durable idempotency. Those responsibilities begin in Course 7.

## Source map

| File | Authority |
|---|---|
| `domain.ts` | job commands, states, revisions, transitions, and results |
| `service.ts` | job IDs, capacity, idempotency, execution, events, and readiness |
| `events.ts` | bounded event history, replay, subscriber queues, and cleanup |
| `http-shared.ts` | transport-independent finite request dispatch and problem responses |
| `http1.ts` | HTTP/1.1, HTTPS, body collection, finite response commit, and SSE |
| `http2.ts` | HTTP/2 session and stream adaptation |
| `client.ts` | pooled finite requests, one deadline, response limits, retry, and close |
| `discovery.ts` | correlated bounded UDP discovery |
| `runtime.ts` | startup rollback and complete service shutdown |
| `command.ts` / `app.ts` / `main.ts` | CLI grammar, orchestration, rendering, and process status |

## Verification

From this directory:

```bash
npm run typecheck
npm run build
npm test
npm run demo
```

From the Course 6 root:

```bash
make investigations
make test
make verify
```

The tests include domain transitions, idempotency replay and conflict, bounded bodies, HTTP problems, conditional reads, SSE replay, UDP correlation, TLS identity, HTTP/2 stream behavior, startup rollback, graceful drain, forced abort, supported-client deadlines, and real CLI execution.

## Teaching credentials

Files under `fixtures/tls/` are local teaching credentials. The certificate names `localhost` and `127.0.0.1` and chains to a dedicated teaching CA. No CA private key is included. These files are not production credentials and do not establish a general certificate-management policy.

## Independent mastery change

The reference implementation is complete for the documented V1 product. The final assessment adds conditional user cancellation:

```text
POST /v1/jobs/:id/cancel
If-Match: "<current-job-etag>"
```

The change must preserve job-state legality, revisions, ETags, idempotency, HTTP/1.1 and HTTP/2 parity, SSE events, client support, shutdown-cause distinction, tests, and documentation. It is not an unfinished reference feature; it is the independent cross-layer change used to prove mastery.
