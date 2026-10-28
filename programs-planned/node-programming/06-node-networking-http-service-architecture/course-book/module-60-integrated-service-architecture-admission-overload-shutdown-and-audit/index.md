# Module 60 — Integrated Service Architecture: Admission, Overload, Shutdown, and Audit

**Progress: 60/100**

## The governing question

> Can the complete service account for every accepted connection, request, job, event subscription, retry identity, timer, and terminal state under success, overload, failure, and shutdown?

## Why this module comes now

The preceding modules established each boundary in isolation. Integration creates failures that no local mechanism can see alone:

- connection capacity can remain while job capacity is exhausted;
- an HTTP request can be accepted while the service is quiescing;
- a job can commit before its response fails;
- an SSE subscriber can outlive the job that caused its event;
- an HTTP/2 session can contain both completed and active streams;
- a UDP discovery socket can continue advertising after readiness becomes false;
- a client agent can keep the process alive after the server stops.

The final module treats ServiceWire as one owned runtime. Its product is not “the server started.” Its product is a complete lifecycle with bounded admission and authoritative terminal evidence.

## Observable outcomes

By the end of the module, you can:

- produce a complete capacity map;
- distinguish listener, connection, request, application, and subscriber admission;
- design healthy, ready, degraded, quiescing, and stopped states;
- reject overload before semantic commit;
- implement startup as staged publication with reverse-order rollback;
- implement quiesce, drain, abort, join, and report;
- apply one shutdown grace deadline;
- coordinate HTTP/1.1, HTTPS, HTTP/2, SSE, UDP, jobs, timers, and clients;
- reconstruct authoritative terminal counts;
- audit a cross-layer feature for protocol and compatibility impact.

## The integrated authority map

| Authority | Owns |
|---|---|
| runtime | startup order, listeners, discovery, shutdown |
| connection adapters | sockets, sessions, streams, request lifecycle |
| HTTP dispatcher | route mapping, body and response representation |
| ServiceWire application | job IDs, state transitions, revisions, idempotency |
| event journal | event sequence, retention, subscribers |
| client | agents, attempts, redirects, retries, deadline |
| configuration | all bounds and enabled transports |
| terminal reporter | post-join authoritative summary |

No two components should both believe they own the same state transition.

## Capacity is multidimensional

A complete map names at least:

```text
HTTP/1.1 connections
HTTPS connections
HTTP/2 sessions
HTTP/2 streams
finite requests parsing bodies
request body bytes
retained jobs
queued jobs
active jobs
idempotency records
event journal entries
SSE subscribers
queued bytes per subscriber
UDP requests in flight
client agent sockets
client operation attempts
```

Each row needs:

- unit;
- maximum;
- current observation;
- admission authority;
- overload response;
- release transition;
- shutdown behavior.

One global “max connections” value does not bound application memory.

## Admission layers

### Listener admission

Can the operating system and server accept another transport connection? Limits include socket backlog and server connection policy.

### Connection admission

Can the runtime own another HTTP/1.1/TLS connection or HTTP/2 session?

### Request admission

Can the adapter parse and retain another finite request body or open another stream?

### Application admission

Can the job store and idempotency store commit another job?

### Subscription admission

Can the journal own another SSE subscriber and its queue?

A request can pass early layers and fail later. Overload responses should identify the rejecting layer through bounded operational evidence, while clients receive a stable product response such as 503 or 429 under policy.

## Health and readiness

Separate:

- **liveness health**: the process and core runtime can make progress;
- **readiness**: the service is willing and able to accept its supported workload;
- **degraded**: some optional or capacity-sensitive feature is unavailable;
- **quiescing**: no new work is admitted; accepted work drains;
- **stopped**: all owned resources terminated.

A full idempotency store can make submission readiness false while health remains true. Optional UDP discovery failure might mark degraded without preventing direct HTTP service, depending on configuration.

Health routes must be cheap and bounded. They should not perform unbounded downstream checks on every call.

## Startup is a transaction-like publication protocol

Possible startup sequence:

```text
1. validate configuration
2. construct application state
3. load TLS materials
4. create event journal
5. create HTTP server objects
6. bind HTTP/HTTPS listeners
7. bind HTTP/2 listener
8. bind UDP discovery
9. publish ready state and endpoint report
```

If step 8 fails and discovery is required, close resources 7 through 5 and settle every close. Never print “ready” before all required resources are published.

If discovery is optional, the policy may continue degraded. That decision belongs to configuration, not an incidental catch block.

## Quiesce before drain

On shutdown request:

1. transition runtime to quiescing;
2. readiness becomes false;
3. stop UDP advertising or respond not-ready;
4. stop accepting new connections and sessions;
5. reject new application submissions on existing keep-alive connections;
6. permit documented read-only requests if policy allows;
7. close or notify SSE subscribers according to protocol;
8. wait for accepted finite requests and jobs.

A listener can stop accepting while existing connections continue to send requests. The application admission authority must therefore also know the quiescing state.

## One grace deadline

Compute one absolute shutdown deadline. Every drain phase shares it. Do not grant a fresh grace period to HTTP, then jobs, then SSE, then HTTP/2.

The runtime can perform drains concurrently:

```text
close listeners
request connection/session close
wait jobs
end SSE
wait active requests
```

At deadline:

- abort remaining requests;
- destroy sockets and sessions;
- cancel active jobs if policy permits;
- clear timers;
- close discovery;
- destroy client agents;
- join all owners.

## Jobs and cancellation

The base ServiceWire course supports job completion and service shutdown cancellation policy internally. The final independent feature adds a public conditional cancellation endpoint.

Cancellation must distinguish:

- queued job: can become cancelled before execution;
- running `sleep`: cooperative cancellation can stop it;
- running synchronous checksum/uppercase: may complete before cancellation is observed;
- terminal job: cancellation is conflict or idempotent no-op under policy;
- stale ETag: precondition failure;
- duplicate cancellation request: stable replay behavior.

This extension deliberately crosses domain, HTTP, ETag, event, client, and shutdown layers.

## Terminal accounting

Every accepted semantic job ends exactly once:

```text
succeeded
failed
cancelled
```

Every accepted network operation also terminates, but its result may differ from the job:

```text
response completed
client disconnected after commit
deadline
protocol rejection
server shutdown
```

Do not force these into one enum. A job can succeed while the submitting HTTP request reports transport failure.

After all owners join, produce an authoritative report:

```ts
interface TerminalReport {
  readonly acceptedConnections: number;
  readonly closedConnections: number;
  readonly acceptedRequests: number;
  readonly terminalRequests: number;
  readonly acceptedJobs: number;
  readonly succeededJobs: number;
  readonly failedJobs: number;
  readonly cancelledJobs: number;
  readonly openedSubscribers: number;
  readonly closedSubscribers: number;
  readonly remainingTimers: number;
}
```

Live counters can help detect leaks, but the final report should reconcile authoritative collections and terminal records where possible.

## Error boundaries

A network service has several error directions:

- peer-visible stable problem;
- client-visible typed failure;
- internal structured diagnostic;
- process-level fatal startup or shutdown failure.

Do not return internal stack traces. Do not suppress fatal startup errors behind a healthy route. Do not terminate the process directly from a low-level adapter; propagate to runtime ownership.

Uncaught exceptions and unhandled rejections are not ordinary recovery channels. The runtime should fail closed and report incomplete lifecycle honestly.

## Determinism

Network schedules vary. Product output can still be deterministic:

- job IDs assigned by one authority;
- revisions monotonic;
- event IDs monotonic;
- list output sorted by job ID;
- problem codes stable;
- stats fields ordered in rendering;
- final report authoritative;
- tests associate concurrent responses by identity rather than arrival order.

Do not claim deterministic completion timing.

## Testing the full lifecycle

Required test families:

### Protocol

- method, path, media type, body, schema;
- idempotency replay and conflict;
- ETag and 304;
- HTTP/2 equivalent behavior;
- SSE replay and gap;
- TLS identity;
- UDP correlation.

### Capacity

- connection limit;
- body limit;
- job/idempotency limit;
- HTTP/2 stream limit;
- subscriber limit;
- slow-subscriber queue;
- response body limit in client.

### Failure

- client disconnect before commit;
- disconnect after commit;
- server response write failure;
- TLS mismatch;
- session reset;
- startup component failure;
- deadline;
- forced shutdown abort.

### Lifecycle

- startup ready only after all required binds;
- reverse-order rollback;
- quiesce rejects new submissions;
- accepted work drains;
- one grace deadline;
- no remaining sockets, sessions, subscribers, timers, or agents.

## Worked shutdown case

State at signal:

```text
2 HTTP/1.1 connections
1 HTTPS connection
1 HTTP/2 session with 3 streams
4 active jobs
2 queued jobs
3 SSE subscribers
UDP discovery open
```

The runtime:

1. marks not-ready;
2. closes all listeners and discovery;
3. rejects new submissions on existing connections;
4. sends GOAWAY to the HTTP/2 session;
5. tells event streams shutdown is beginning and ends them;
6. allows admitted requests/jobs to finish until the shared deadline;
7. cancels remaining cooperative jobs;
8. destroys sockets/sessions after deadline;
9. joins every tracked owner;
10. reconstructs report and chooses process exit status.

A server object closing early does not make step 9 true.

## Common wrong models

### “Healthy means ready”

A live process can be overloaded or quiescing.

### “Closing listeners stops all work”

Existing connections can send more requests unless application admission closes.

### “Each subsystem gets its own shutdown timeout”

That multiplies the promised grace period.

### “All errors become HTTP problems”

Handshake and process startup failures can occur before HTTP.

### “One terminal enum covers request and job”

Network observation and semantic operation have different lifecycles.

## Architecture review procedure

For every cross-layer change:

1. update wire/API grammar;
2. update runtime validation;
3. update domain state machine;
4. update idempotency;
5. update revisions and ETags;
6. update events;
7. update HTTP/1.1;
8. update HTTP/2;
9. update client;
10. update capacity;
11. update shutdown;
12. update tests and docs.

A feature is incomplete when one supported adapter or lifecycle path still follows the old contract.

## ServiceWire completion

Finish all adapters, the client, discovery, tests, CLI, demo, and operational documentation. Then implement public conditional cancellation as the independent change.

## Ready to complete the course

You have completed Course 6 when you can defend:

- every identity;
- every queue;
- every byte and record bound;
- every deadline;
- every retry;
- every semantic commit;
- every replay cursor;
- every shutdown transition;
- every limitation that remains process-local.

## Final architecture exercise — overload during shutdown

Assume ServiceWire has these limits:

```text
HTTP/1.1 connections: 4
HTTP/2 sessions:      2
HTTP/2 streams:       8
retained jobs:       16
active jobs:          2
idempotency records: 16
SSE subscribers:      2
subscriber queue:  4096 bytes each
shutdown grace:     200 ms
```

At time zero:

- four HTTP/1.1 connections are open;
- one HTTP/2 session has three active streams;
- two jobs are running;
- five jobs are queued;
- two SSE subscribers are connected, one slow;
- a UDP discovery socket is active.

A termination signal arrives while another client attempts a new submission.

A defensible shutdown sequence is:

1. transition readiness from ready to quiescing;
2. reject the new submission before semantic commit;
3. stop or close UDP discovery;
4. stop accepting new HTTP/1.1 connections and HTTP/2 sessions;
5. refuse new SSE subscribers and close existing delivery within policy;
6. let accepted finite requests and jobs drain under one grace deadline;
7. send HTTP/2 shutdown signals and allow existing streams to complete;
8. at grace expiry, abort remaining operations, reset streams, and destroy sockets;
9. observe every task, response, stream, session, and socket terminal event;
10. produce a terminal report from authoritative application state plus cleanup errors.

The order is not arbitrary. Quiescing application admission before closing listeners prevents an already accepted connection from committing new work during the gap. Closing discovery early prevents advertising a service that no longer accepts submissions. Waiting for cleanup before producing the terminal report prevents a misleading “stopped” state while handles remain live.

### Conservation equations

Use these equations during review:

```text
accepted jobs = queued + running + succeeded + failed + cancelled

opened subscriptions = active subscriptions + disposed subscriptions

started transport resources
  = active resources + closed resources + failed-start resources
```

The exact counters may differ, but every accepted unit needs one terminal category. If a category can disappear between layers, shutdown and overload behavior are not auditable.

### Startup rollback

Production lifecycle begins before readiness. If HTTP starts successfully, HTTPS fails because the key is invalid, and discovery has not started, the runtime must close HTTP and the application authority before returning the startup error. Readiness must never be published partially.

Model startup as a stack of acquired resources. Each successful acquisition registers an idempotent cleanup action. On failure, run cleanups in reverse order and retain all cleanup errors without hiding the initiating failure.

### Review the unsupported claims

ServiceWire is process-local. It does not provide:

- durable jobs or idempotency across restart;
- distributed exactly-once execution;
- multi-process coordination;
- authenticated UDP discovery;
- automatic certificate rotation;
- protection against adversarial DNS or routing by itself;
- durable event delivery beyond the retained journal.

Stating these limits is part of architecture quality. A smaller honest service is more trustworthy than a demonstration that borrows production terminology without the corresponding mechanisms.

### Independent change impact map

The final cancellation feature must cross at least these surfaces:

```text
HTTP method and route
request precondition
application transition authority
running-operation AbortController
revision and ETag
job-cancelled event
SSE replay
client method
shutdown interaction
tests and documentation
```

If the feature is implemented only in the router or only by aborting a promise, the architecture has been bypassed. The value of the final task is learning to preserve one coherent contract through all layers.

## Primary Node.js references

- [HTTP](https://nodejs.org/docs/latest-v24.x/api/http.html)
- [HTTPS](https://nodejs.org/docs/latest-v24.x/api/https.html)
- [HTTP/2](https://nodejs.org/docs/latest-v24.x/api/http2.html)
- [Net](https://nodejs.org/docs/latest-v24.x/api/net.html)
- [Datagram](https://nodejs.org/docs/latest-v24.x/api/dgram.html)
- [Process](https://nodejs.org/docs/latest-v24.x/api/process.html)

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-60-network-service-audit/README.md)
- [ServiceWire engineering guide](../capstone.md)
