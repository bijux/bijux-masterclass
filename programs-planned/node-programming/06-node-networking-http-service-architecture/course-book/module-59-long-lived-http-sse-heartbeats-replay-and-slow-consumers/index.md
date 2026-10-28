# Module 59 — Long-Lived HTTP: SSE, Heartbeats, Replay, and Slow Consumers

**Progress: 59/100**

## The governing question

> How do you keep an HTTP response open for ordered event delivery while bounding retained history, per-subscriber pressure, replay work, heartbeat resources, and shutdown?

## Why this module comes now

All earlier HTTP routes were finite. Server-sent events turn one response into a long-lived subscription. The server owns not only the connection but also replay position, event formatting, heartbeat timers, subscriber registration, slow-consumer policy, and cleanup after disconnect.

This module demonstrates that “streaming” is not enough. A long-lived channel needs a protocol above the stream and separate bounds for global history and each consumer.

ServiceWire uses SSE to publish job state transitions. It does not claim durable event history or exactly-once delivery. Those require persistent and distributed mechanisms in Course 7.

## Observable outcomes

By the end of the module, you can:

- encode valid SSE events and comments;
- assign monotonic opaque event IDs;
- maintain a bounded event journal;
- select replay after a client cursor;
- detect and report a replay gap;
- register a subscriber without losing events between replay and live delivery;
- enforce subscriber count and queued-byte bounds;
- use heartbeats as connection-liveness traffic rather than domain freshness;
- clean up listeners, queues, timers, and responses on disconnect;
- close all subscriptions during service shutdown.

## The SSE ownership ledger

| Resource | Owner | Bound or terminal rule |
|---|---|---|
| event sequence | event journal | monotonic safe integer |
| retained events | journal | maximum count and bytes |
| replay selection | subscription opening | cursor and oldest retained ID |
| subscriber record | event hub | maximum subscribers |
| subscriber queue | subscriber | maximum events or bytes |
| heartbeat timer | subscriber or shared ticker | cleared on close |
| HTTP response | subscriber owner | end, error, close, shutdown |
| live callback | hub subscription | disposed exactly once |
| request context | connection/request scope | bounded immutable fields |

## SSE wire format

An event can contain:

```text
id: 42
event: job-state
data: {"jobId":"job-000001","state":"running"}

```

The blank line commits the event. If data contains line breaks, encode each line with its own `data:` field. Do not place raw JSON containing literal newlines into one line without normalization.

A comment heartbeat:

```text
: heartbeat

```

does not change the client's last event ID.

The server should send:

```http
Content-Type: text/event-stream; charset=utf-8
Cache-Control: no-cache
Connection: keep-alive
```

Connection headers vary with HTTP version and intermediaries; the base course uses HTTP/1.1 directly.

## Event IDs are replay cursors

An event ID identifies one journal position. It is not a job ID, request ID, or timestamp. Use a monotonic sequence under one journal authority.

A client reconnects with a known last ID, commonly through `Last-Event-ID` or an explicit query parameter. The server selects events whose IDs are greater than the cursor.

A cursor can be:

- absent: begin with live delivery or documented initial replay;
- before oldest retained: replay gap;
- within retained range: replay later events;
- equal to current latest: live only;
- after current latest: invalid cursor under a strict policy.

## Bounded history

A process-local journal can retain:

- maximum event count;
- maximum total encoded bytes;
- maximum age.

Count alone is insufficient when event sizes vary. ServiceWire bounds event payloads and journal count, making total retained bytes derivable. A stronger implementation can track both directly.

Eviction advances the oldest retained ID. Once an event is evicted, the server must not silently pretend replay is complete.

## Replay-gap policy

If a client asks after ID 10 but the oldest retained event is 30, it has missed events 11–29. Options:

- return a finite 409 problem before opening SSE;
- open SSE with a synthetic `replay-gap` event requiring a full state refresh;
- redirect the client to a snapshot route;
- close and require resynchronization.

ServiceWire returns a finite problem response before committing the event-stream headers. The client then fetches current state through ordinary endpoints and reconnects from the current journal position.

Do not send HTTP status changes after SSE headers have been committed.

## The replay-to-live race

A naïve sequence:

```text
1. read journal snapshot
2. write replay
3. subscribe to future events
```

can lose an event appended between steps 1 and 3.

A safe journal API can atomically establish a high-water boundary and subscription:

```ts
interface OpenSubscription {
  readonly replay: readonly ServiceEvent[];
  readonly dispose: () => void;
}
```

Under one synchronous JavaScript authority:

1. validate cursor;
2. register subscriber;
3. capture replay through current high-water;
4. return both.

Live events appended after registration enter the subscriber queue. The response owner writes replay first, then drains queued live events in sequence.

Another design captures high-water, replays through it, then subscribes and requests events after high-water under the journal's serialized authority. The key is explicit gap avoidance.

## Slow subscribers

A response stream has its own writable pressure. If `response.write()` returns false, stop writing and wait for `'drain'`. New events can continue arriving, so the subscriber needs a bounded queue.

Policy:

- maximum queued encoded bytes or events;
- queue in event order;
- on overflow, remove subscriber and close the response;
- record a stable slow-subscriber terminal cause;
- do not block the global journal on one client.

Global journal history and per-subscriber queue are independent. A bounded journal does not bound bytes waiting on a slow socket.

## Heartbeats

Heartbeats help detect broken connections and prevent some intermediaries from considering an otherwise quiet stream idle. They prove only that the server attempted to write heartbeat traffic and that the connection remained writable at that point.

They do not prove:

- jobs are progressing;
- event history is current;
- the client processed prior events;
- the server is ready for new submissions.

Use a shared heartbeat ticker when appropriate rather than one timer per subscriber, but keep ownership and cleanup explicit. The laboratory compares both designs.

## Event publication authority

Job transitions append events within the domain transition:

```text
queued → running → succeeded
```

The HTTP adapter does not synthesize those transitions. It merely subscribes to the journal.

Each event should contain a bounded immutable representation:

```ts
interface JobEvent {
  readonly sequence: number;
  readonly type: 'job-created' | 'job-running' | 'job-succeeded' | 'job-failed';
  readonly jobId: string;
  readonly revision: number;
  readonly occurredAtMs: number;
}
```

Avoid placing full unbounded job payloads in every event. Clients can fetch the current job representation when needed.

## Disconnect and cleanup

A subscriber can terminate through:

- client close;
- request abort;
- response error;
- response close;
- slow-consumer overflow;
- server shutdown;
- internal formatting failure.

One owner must:

- dispose journal subscription;
- clear or detach heartbeat;
- clear queued events;
- remove response listeners;
- end or destroy response as appropriate;
- settle terminal state once.

Repeated close signals are normal. Cleanup must be idempotent.

## SSE and proxies

Intermediaries can buffer, time out, or transform responses. A production deployment needs proxy-specific configuration and testing. Course 6 tests a direct Node server and does not claim universal intermediary behavior.

Compression can also increase buffering and latency for SSE. Avoid enabling generic response compression without testing event flush behavior.

## Worked case — reconnect after bounded history

Journal retains IDs 101–110. Client reconnects with ID 106.

The server:

1. validates 106;
2. registers subscriber;
3. returns replay 107–110;
4. writes replay in order;
5. drains live events beginning at 111;
6. sends heartbeats when no events occur;
7. removes subscriber on close.

A client with ID 90 receives replay-gap response because required events are no longer retained. It fetches `/v1/stats` or job resources and then reconnects from the latest known cursor.

## Delivery semantics

The process-local SSE channel provides:

- ordered delivery per connection;
- at-least-once possibility across reconnect because replay can repeat an event the client already processed before losing its acknowledgment state;
- bounded replay window;
- no durable guarantee across process restart;
- no exactly-once processing guarantee.

Event IDs let the client deduplicate if its own state records the last processed ID.

## Common wrong models

### “The journal bound protects slow consumers”

It bounds global history, not socket-specific queued output.

### “Heartbeat means the system is healthy”

It indicates channel activity, not domain readiness.

### “Subscribe after replay”

That can lose an event.

### “Event ID is a timestamp”

It is an opaque ordered cursor. Time can move backward or collide.

### “SSE is durable messaging”

It is a long-lived HTTP delivery mechanism. Durability requires another system.

## Decision procedure

1. Define event schema and maximum encoded size.
2. Assign monotonic IDs.
3. Bound journal history.
4. Define cursor grammar.
5. Define replay gap.
6. eliminate replay-to-live race.
7. bound subscriber count.
8. bound per-subscriber queue.
9. define heartbeat ownership.
10. define every close cause.
11. integrate service shutdown.
12. state delivery guarantees honestly.

## ServiceWire increment

Add `/v1/events`:

- query or `Last-Event-ID` cursor;
- replayable bounded journal;
- stable replay-gap problem;
- heartbeats;
- bounded subscribers;
- bounded subscriber queues;
- job-transition events;
- shutdown close.

## Case study — replay window and a slow subscriber

ServiceWire retains events with sequences 101 through 200. A reconnecting client supplies `Last-Event-ID: 175`; the server can replay 176–200 and then attach the live listener. A client supplies 40; the server must report a replay gap before committing `text/event-stream` headers.

The race between replay selection and live subscription matters. If the server first copies retained events and only later registers the listener, events appended between those steps are lost. The journal should create one atomic subscription result under its synchronous authority: validate cursor, register listener, and return the replay slice corresponding to the same sequence boundary.

### Four separate memory resources

Long-lived delivery introduces resources that are easy to collapse:

1. retained journal history;
2. number of active subscribers;
3. queued unsent bytes per subscriber;
4. bytes already accepted by the underlying socket buffers.

A bound on history does not bound slow-consumer queues. A bound on subscriber count does not bound each subscriber’s queued bytes. `response.write()` returning `false` is evidence of pressure, not permission to keep enqueuing indefinitely.

### Slow-consumer policy

Possible policies include:

- disconnect once queued bytes exceed a limit;
- drop intermediate events and send a gap marker;
- coalesce replaceable state updates;
- pause the upstream source when every consumer is required;
- move durable delivery to a different subsystem.

ServiceWire chooses bounded per-subscriber delivery and disconnection. Events are notifications; the client can reconnect and replay while retained history permits. If it falls behind the journal window, it receives a gap and must refetch authoritative job state.

### Heartbeats are lifecycle traffic

An SSE heartbeat keeps intermediaries and clients aware that the connection remains active. It is not a domain event and should not consume event sequence numbers. The heartbeat timer belongs to the subscription owner and must be cleared on response close, error, service quiescence, or setup failure.

A heartbeat does not prove the consumer processed prior events. It only proves the server attempted to write transport traffic.

### Event payload discipline

Events should remain small and stable:

```ts
interface ServiceEvent {
  readonly sequence: number;
  readonly type: 'job-created' | 'job-running' | 'job-succeeded' | 'job-failed' | 'job-cancelled' | 'service-quiescing';
  readonly occurredAtMs: number;
  readonly jobId?: string;
  readonly revision?: number;
}
```

Large results remain behind `GET /v1/jobs/:id`. This avoids duplicating mutable representations in event history and makes replay memory predictable.

### Shutdown

Quiescence ends new subscriptions. Existing subscribers receive the final quiescing event if capacity and timing permit, then responses close. The service does not wait indefinitely for a slow subscriber during shutdown. Subscriber disposal, timer cleanup, response end, and socket close must all be observable in tests.

## Ready to continue

You are ready for the final integration when you can explain why event history, subscriber queue, socket pressure, and domain state are four different resources.

## Primary references

- [Node HTTP](https://nodejs.org/docs/latest-v24.x/api/http.html)
- [HTML Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [Node events](https://nodejs.org/docs/latest-v24.x/api/events.html)

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-59-replayable-sse-channel/README.md)
- [ServiceWire engineering guide](../capstone.md)
