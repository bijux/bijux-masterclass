---
module_id: API-053
program: API & Service Engineering
level: 2
module_number: 53
title: Unary and Streaming gRPC
status: complete
last_verified: 2026-09-02
---

# Unary and Streaming gRPC

## One-Page Review

### Governing question

How should a service choose and operate unary, server-streaming, client-streaming, or bidirectional-streaming gRPC so message cardinality, ordering, flow control, partial progress, failure, and resource ownership match the real interaction?

### Essential definitions

- A **unary RPC** carries one request message and at most one successful response message before terminal status.
- A **server-streaming RPC** carries one request followed by an ordered response-message sequence and terminal status.
- A **client-streaming RPC** carries an ordered request-message sequence, a client half-close, and at most one successful response.
- A **bidirectional-streaming RPC** carries two independently scheduled, per-direction ordered message sequences.
- A **channel** is a reusable logical connection to a service; a **call** normally occupies one HTTP/2 stream on a selected connection/backend.
- A **half-close** says one sender will emit no more messages while the opposite direction may continue.
- **flow control** limits bytes/messages in flight so a receiver is not overrun; a successful application write does not necessarily mean bytes reached the peer.
- **terminal status** completes the RPC and applies to the whole call, not each individual streamed message.
- An **application checkpoint** is a durable sequence/cursor/acknowledgment used to resume logical work after a stream fails.

### Central model, mechanism, or theorem

The four method shapes are the Cartesian product of request and response cardinalities:

$$
(C_{req},C_{resp})\in\{1,*\}\times\{1,*\}.
$$

For each direction $d$, gRPC preserves the order of messages within one call:

$$
send_d(m_i)\prec send_d(m_j)\Rightarrow receive_d(m_i)\prec receive_d(m_j),\quad i<j,
$$

provided both messages are delivered. This does not establish ordering across calls, backends, retries, or domain events. A stream is one failure and load-balancing unit: if it terminates after prefix $m_1\ldots m_k$, the application needs its own stable cursor/deduplication protocol to determine whether and how to resume.

### Critical invariants

Choose method shape from interaction semantics, not expected payload count alone. Message schemas are bounded and evolution-safe. Per-direction sequence is explicit; cross-stream/global ordering is never inferred. The protocol defines when request input is complete, when effects commit, what each response means, and whether partial messages remain valid after non-OK status. Writers respect readiness/flow control and cap application queues. Readers keep draining or deliberately cancel; synchronous peers do not both write indefinitely without reads. Every stream has finite lifetime or an owned renewal policy, idle handling, message/count/byte limits, and cleanup. Retriable unary mutations remain idempotent. Streaming retries are not transparent resumption: stable session/record IDs, sequence numbers, acknowledgments, checkpoints, deduplication, and gap policy belong to the application. Authorization covers the method and every message-level resource/action. One long-lived stream is pinned to one selected backend, so balancing, draining, deployment, and failover are designed explicitly. Terminal status and trailers are observed before declaring whole-call success.

### Common failures

Using streaming merely to avoid pagination; one giant message disguised as unary; one unbounded stream per user; assuming message write equals network delivery or durable commit; buffering an entire stream despite claiming incremental processing; ignoring flow-control readiness; both sides synchronously writing until deadlock; treating per-stream order as global order; assigning meaning to arrival timing; allowing concurrent writes unsupported by the language API; forgetting client half-close; returning OK before durable effect; discarding useful prefix on any final error without contract; retrying a stream from the beginning without deduplication; using transport sequence as domain identity; assuming a resumed call reaches the same backend; keeping mutable state only in the stream handler; overusing keepalive; failing to drain on deploy; logging message bodies; and measuring only completed calls while hiding active-stream age, stalls, queue growth, and partial progress.

### Compact example

A change-feed server accepts `Watch(from_sequence=40)` and emits records 41, 42, 43 in order. The connection fails after the client durably applies and checkpoints 42 but before it receives 43. The client opens a new call with `from_sequence=42`; the server may replay 43 (or an overlap), and the client deduplicates by record ID/sequence. **Conclusion:** server streaming supplies ordered delivery within each call; application cursors and idempotent apply supply cross-call recovery.

### Connections

[Remote Procedure Call Semantics](051-remote-procedure-call-semantics.md) defines attempts and uncertain outcomes, [Protocol Buffers and Schema Evolution](052-protocol-buffers-and-schema-evolution.md) owns message compatibility, and [Filtering, Sorting, and Pagination](017-filtering-sorting-and-pagination.md) offers bounded pull-based collections. [Deadlines, Cancellation, and Metadata](../ROADMAP.md) next develops call context and lifecycle budgets.

## Governing Question

What does each gRPC method shape guarantee, what remains application policy, and how can an implementation avoid converting convenient streams into unbounded queues, hidden state, irrecoverable partial progress, or backend imbalance?

## Why This Matters

gRPC exposes four compact method declarations, but cardinality changes the protocol rather than merely the generated method signature. Unary has one request/response boundary and one terminal outcome. Server streaming exposes an incremental response prefix. Client streaming introduces input completion and aggregation semantics. Bidirectional streaming creates two independent schedules, half-close states, and application-level correlation. Each shape changes buffering, testing, retries, authorization, observability, and deployment.

Streaming can reduce repeated call setup and deliver incremental results with flow control. It can also pin work to one backend for hours, retain memory and authorization context, obscure partial effects, amplify slow consumers, and fail after meaningful progress. HTTP/2 multiplexes many calls on a connection, but connection-level loss affects all its streams; a single stream cannot be moved to another backend in place. A retry creates a new call and does not know which application messages committed.

The API must therefore name the unit of meaning. Is every message an independent command, one chunk of a single upload, a state snapshot, a delta, an acknowledgment, or a request correlated to a response? Does a non-OK final status invalidate the prior response prefix, or does it mean “partial results valid through cursor 91”? Can a client resume after failure? What happens when the producer is faster than the consumer? Generated stubs and HTTP/2 flow control cannot answer domain questions.

Correct designs treat flow control as necessary but not sufficient backpressure, distinguish application acceptance from transport writes, bound every queue and lifetime, and make progress durable where recovery matters. They test through real proxies, load balancers, languages, and deployments because streaming support and defaults vary even when the gRPC protocol is common.

## Prerequisites and Retrieval

Retrieve RPC attempts/outcome ambiguity, protobuf evolution, HTTP/2 streams/frames/multiplexing/flow-control windows, generated stubs, synchronous versus asynchronous APIs, iterators/async streams, producer-consumer queues, backpressure, half-close, status codes, deadlines/cancellation, authentication/authorization, load balancing, idempotency, sequence numbers/cursors, deduplication, checkpoints, graceful shutdown, metrics/traces, and resource limits.

Before declaring a method, retrieve request/response cardinality; whether items are independent or one aggregate; ordering scope; latency to first/last item; total bytes and item count; producer/consumer rates and burst size; commit/acknowledgment point; resume and duplicate/gap policy; authentication lifetime and per-message authorization; maximum stream age/idle duration; client/proxy/load-balancer support; backend state placement; deployment draining; compression sensitivity; message/metadata limits; retry ownership; and the evidence needed to validate slow, failed, and adversarial peers.

## Learning Objectives

By the end of this module, you should be able to:

1. derive the four gRPC method shapes from request/response cardinality and choose among them;
2. trace a call through headers, length-prefixed messages, half-close, response messages, trailers, and terminal status;
3. distinguish per-call per-direction ordering from cross-call or domain ordering;
4. design bounded flow-control and application-backpressure behavior for slow peers;
5. specify partial progress, acknowledgment, resume, deduplication, and gap semantics;
6. account for channel reuse, backend pinning, connection failure, graceful draining, and security; and
7. verify unary and streaming behavior with model, integration, fault, concurrency, and load evidence.

## Core Exposition

### Choose cardinality from the interaction contract

The service definition declares whether `stream` appears on the request and/or response. Conceptually:

<!-- bijux-verify: {"id":"grpc-method-shapes","mode":"schematic","language":"protobuf","toolchain":"none","reason":"the declarations illustrate gRPC method cardinalities; no repository protoc/gRPC build target is required for this language-neutral contract"} -->
```protobuf
service Catalog {
  rpc Get(GetRequest) returns (GetResponse);
  rpc Watch(WatchRequest) returns (stream WatchEvent);
  rpc Upload(stream UploadChunk) returns (UploadResult);
  rpc Exchange(stream ClientFrame) returns (stream ServerFrame);
}
```

Unary suits one bounded request and one bounded answer, including commands whose idempotency is independently specified. Do not place an unbounded list in one response merely to preserve unary shape; paginate, stream, or create a job according to semantics.

Server streaming suits an incrementally consumable ordered response: search hits, snapshot chunks, or a change subscription. A stream is not automatically a durable subscription; disconnect behavior, cursor, retention, replay, heartbeats, and snapshot/delta boundaries must be defined.

Client streaming suits a sequence whose collective completion yields one result: chunked upload, batch ingest, or incremental aggregation. If each input requires an independent response, client streaming alone hides necessary acknowledgments; use bidi or independent unary calls. Define whether effects happen per message or only after half-close and validation of the whole aggregate.

Bidirectional streaming suits a long-lived protocol in which both directions contain multiple messages: interactive session, replication exchange, or correlated requests/responses. It is not “faster unary.” It requires an application protocol for message kind, identity, correlation, state transitions, and errors. The request and response sequences are independent; the server may wait, respond immediately, or interleave according to the contract.

### Trace the gRPC-over-HTTP/2 lifecycle

The standard gRPC-over-HTTP/2 mapping normally uses one HTTP/2 stream per call. Request headers identify `POST`, the canonical service/method path, content type, compression, timeout, and application metadata. Each gRPC message is framed within HTTP/2 DATA as a one-byte compressed flag, a four-byte big-endian message length, and that many message bytes. HTTP/2 frame boundaries need not align with gRPC message boundaries; libraries reassemble them.

The request body contains zero or more length-prefixed messages followed by end-of-stream from the client. A unary/server-streaming request has exactly one request message by method contract; client/bidi input may have many. Response headers can precede messages. Successful response messages are followed by trailers containing `grpc-status` and optional details/metadata; trailers-only represents a call with no response messages.

HTTP status and gRPC status have different roles. A correctly formed gRPC response often uses HTTP `:status 200` while the application gRPC status is non-OK in trailers. A client must use the gRPC library's terminal status rather than treating HTTP 200 or receipt of some messages as whole-call success.

The application should not hand-code this wire mapping unless implementing infrastructure. It should nevertheless understand it to diagnose proxies that drop trailers, enforce incorrect content types, buffer streaming bodies, impose idle limits, or report HTTP health while gRPC calls fail.

### State the exact ordering guarantee

Official gRPC concepts document message ordering within an individual RPC. If one sender serially emits $m_1,m_2,m_3$, a receiving application will not observe $m_3$ before $m_2$ within that direction of that call. Bidirectional RPCs have two ordered sequences, not a single total order.

Suppose the client sends `request A`, then `request B`, while the server sends `response B`, then `response A` according to independent processing. Per-direction order can hold even though request/response business correlation differs. Include a correlation ID if association matters. If concurrent application tasks write, obey the language runtime's rule—many APIs allow one concurrent reader and one writer but not multiple writers—and serialize emissions deliberately.

No guarantee orders messages across separate RPCs, channels, backend instances, retries, or a stream restart. TCP/HTTP/2 ordering does not establish database commit order or event causality. Domain sequence numbers, versions, timestamps with stated semantics, or a sequencer/partition own those claims.

### Understand flow control and application backpressure

HTTP/2 and gRPC flow control keep a fast sender from placing unlimited bytes into a receiver/transport window. When the receiver consumes data, window credit eventually permits more sending. The official gRPC guide emphasizes that an application write returning does not mean the value has left the machine or reached the peer; it may only have entered framework buffers.

Transport flow control does not bound every application queue. A handler can eagerly read into an unbounded work queue, defeating backpressure. A producer can generate huge objects before awaiting readiness. An interceptor can buffer. Downstream databases can saturate while the network remains writable. Bound item count and bytes at every handoff; couple reading to actual processing capacity; expose saturation; and reject/cancel under policy rather than accumulate memory.

Manual flow control can improve precise resource ownership but creates deadlock hazards. If both synchronous peers write enough data without reading, both can block waiting for the other's window. Safe bidi loops either read and write concurrently within supported API rules, alternate according to a protocol, or use an asynchronous select/event loop with bounded outgoing queues.

Flow control is per transport direction and typically byte-oriented; it does not express business priority or fairness. A tiny expensive message can consume little window but much CPU. Add admission, per-principal quotas, concurrency limits, cost-aware scheduling, and maximum message/stream budgets.

### Define half-close and terminal state

In client or bidi streaming, the client half-closes after its final request message. This means “no more request messages,” not “cancel the call.” The server may still emit responses and a final status. A server that waits for complete input cannot decide until it sees half-close; a client that forgets to close can wait forever under an absent deadline.

Model each direction as open → half-closed/closed, plus call terminal. The call ends successfully only when terminal status is OK and the method's response contract is satisfied. Cancellation, connection loss, and non-OK status may terminate both directions. The server and client can still reach different local observations as API-051 established.

Do not return status OK before the claimed durable result exists. Conversely, a server-streaming method may legitimately send useful items then fail. The contract states whether the delivered prefix is independently valid, provisional, or must be discarded. If partial results are valid, include a cursor/checkpoint and expose the final incompleteness clearly.

The following executable model uses one message of send credit, explicit receiver consumption, client half-close, and terminal success. It illustrates lifecycle invariants, not a network implementation.

<!-- bijux-verify: {"id":"bounded-stream-lifecycle","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"sent=1\nblocked=2\nreceived=1\nsent=2\nclient=half_closed\nstatus=OK\n","stderr":""}} -->
```python
class Stream:
    def __init__(self, credit):
        self.credit = credit
        self.in_flight = []
        self.client_open = True

    def offer(self, item):
        if not self.client_open:
            raise RuntimeError("send after half-close")
        if len(self.in_flight) >= self.credit:
            return False
        self.in_flight.append(item)
        return True

    def receive(self):
        return self.in_flight.pop(0)

    def half_close(self):
        self.client_open = False

stream = Stream(credit=1)
print("sent=1" if stream.offer(1) else "blocked=1")
print("sent=2" if stream.offer(2) else "blocked=2")
print("received=" + str(stream.receive()))
print("sent=2" if stream.offer(2) else "blocked=2")
stream.receive()
stream.half_close()
print("client=half_closed")
print("status=OK" if not stream.in_flight else "status=INTERNAL")
```

### Make progress and acknowledgment semantic

A streaming write can be accepted by the local API, framed, placed on the wire, parsed by the peer runtime, read by the peer handler, validated, durably committed, and acknowledged at distinct times. Name the acknowledgment level. “Received” is ambiguous.

For an upload, each chunk carries upload/session ID, offset or chunk sequence, size/digest, and perhaps total/terminal marker. The server acknowledges the highest contiguous durable offset, not merely the last frame seen. Duplicate chunks are idempotent or rejected consistently; gaps and conflicts are explicit. Final success follows complete validation and durable assembly.

For server feeds, each item carries stable record identity/sequence. The client checkpoints only after applying effects durably. On reconnect it supplies the checkpoint, and the server defines inclusive/exclusive resume plus retention expiration. Overlap is safer than gaps when application apply is idempotent. If the cursor is too old, return an explicit resnapshot path.

For bidi exchanges, use application frames such as `open`, `data`, `ack`, `error`, `close` with correlation/session identity and a documented state machine. Do not use arbitrary metadata or stream timing as the durable protocol.

### Treat a failed stream as a failed call, not a resumable socket

If a connection closes, the in-progress RPC terminates. Unsafely retransmitting an entire client stream can duplicate committed messages. Transparently continuing a server stream can omit or duplicate items because a new backend lacks the prior handler's state. General gRPC retries are much easier to reason about for unary calls before commitment; streaming recovery belongs to the application protocol.

Resume creates a new call. It reauthenticates, may reach another backend, and supplies durable session/cursor state. The server consults shared storage or a properly routed/fenced owner. It rejects stale epochs, invalid gaps, or expired sessions. Sequence numbers alone do not prevent replay across users/sessions; scope them to authenticated identity and resource.

Exactly-once stream delivery is not a defensible generic claim. Prefer at-least-once messages plus idempotent application, or at-most-once processing within clearly stated ledger retention. End-to-end effect correctness includes downstream effects and recovery just as unary idempotency does.

### Account for channels, multiplexing, and backend pinning

A client normally reuses channels/stubs rather than creating one per RPC. A channel manages connections, name resolution, balancing, and connectivity. HTTP/2 multiplexes multiple RPC streams on one connection, reducing per-call handshakes. Connection-level limits and failures therefore affect multiple calls; too many concurrent streams may queue or motivate additional connections according to implementation and server policy.

Load balancing normally selects a backend when a call starts. A long-lived stream stays on that backend; it is not rebalanced as endpoints change. Large populations of unequal stream duration can skew load even if new-call selection is fair. Scale using stream-aware metrics, connection/stream age policies, sharding by durable identity when required, and graceful renewal with checkpointed resume.

Creating multiple channels to work around concurrent-stream limits may help a measured implementation, but it adds connections and is not a timeless semantic prescription. Official performance guidance itself flags implementation-specific workarounds. Measure the supported language/runtime/proxy path and prefer reusable channels.

### Design lifecycle, keepalive, health, and draining separately

Keepalive PING tests an HTTP/2 connection during inactivity; it does not prove application health, authorization validity, consumer progress, or durable state. Aggressive client keepalive can overload a service and trigger `GOAWAY` for excessive pings. Coordinate settings with the service owner and intermediaries. Application heartbeats can carry domain liveness/cursor information, but they consume messages and require their own timeout semantics.

Long-lived streams cross deployments. On graceful shutdown, stop accepting new calls, signal/allow existing streams to finish within a drain budget, checkpoint or send a reconnect hint where the contract permits, then force termination at the boundary. Clients reconnect with jitter and resume state rather than forming a synchronized storm. Test proxy maximum connection/stream duration and idle timeout; do not rely on undocumented defaults.

Health checking decides whether new calls should be routed to a service; it does not migrate established streams. Connection keepalive decides whether a path responds; it does not certify the handler. These mechanisms solve different problems.

### Secure every stream throughout its lifetime

TLS and authentication establish peer/caller context at call start, but a long-lived stream may outlive a credential, authorization grant, tenant membership, or policy decision. Decide whether authorization is fixed for the call, rechecked per message/action, or forces bounded stream renewal. High-risk commands need per-message resource authorization even inside an authenticated stream.

Validate each message's size, type, identifier, sequence, ownership, state transition, and cost. Cap messages per time/stream and concurrent streams per principal. Protect against compression bombs and secrets chosen to share compression contexts; compression policy can differ by message. Never trust client-declared offsets/counts for allocation.

Avoid logging raw messages/metadata. Streaming bodies can contain an entire sensitive session. Audit stable protected IDs, action, sequence/cursor, authorization decision, and effect outcome under retention policy. Errors should not disclose other sessions, offsets, or backend identity.

### Observe and verify the interaction, not only call totals

Record active streams, starts/completions by method/status, stream age, messages/bytes each direction, time to first/last message, inter-message gaps, application queue depth/bytes, flow-control stalls where supported, half-close-to-status time, cancellation, reconnect/resume, replay/duplicate/gap, checkpoint lag, backend distribution, and drain outcomes. Bound labels; do not attach arbitrary session or message IDs to metrics.

Trace the full call and create message events/spans selectively to avoid unbounded trace volume. A stream spanning hours may outlive ordinary sampling/export assumptions. Logs and durable progress records should permit reconstruction without assuming telemetry is complete.

Verification includes schema/generated-code compilation in supported languages, unary and each streaming shape through actual intermediaries, ordering/property tests, slow reader/writer tests, manual flow-control deadlock tests, bounded-queue load tests, malformed/oversized/compressed input, half-close/cancel races, drop before/after commit/ack, reconnect overlap/gap, backend restart/failover, credential/policy change, connection loss affecting multiplexed calls, graceful drain, and version-skew interoperability.

## Definitions and Notation

Let a call $c$ have client-to-server sequence $Q_c=(q_1,\ldots,q_n)$ and server-to-client sequence $P_c=(p_1,\ldots,p_m)$, where $n,m$ are 1 or unbounded-by-cardinality (`*`) but bounded by operational policy. Let $sent_d(x)$, $delivered_d(x)$, $read_d(x)$, $committed(x)$, and $acked(x)$ be distinct events. Let $W_d(t)$ be available transport credit, $B_d(t)$ application-buffer bytes, $L$ the configured buffer limit, $h_d$ a half-close event, and $T(c)$ the terminal status.

**Per-direction ordering** preserves sender order among delivered messages in one call. **Half-close** is a monotone transition after which that sender emits no more messages. **Flow-control stall** occurs when insufficient credit prevents progress until the receiver consumes. **Backpressure** is the wider application mechanism that slows/rejects production based on downstream capacity. **Checkpoint** is durable application progress. **Resume token/cursor** identifies a safe restart position under defined retention and authorization. **Stream pinning** means an established call remains on its selected backend/connection for its lifetime.

The resource invariant is $0\le B_d(t)\le L$, not merely $W_d(t)\ge0$. A valid terminal success requires the declared message cardinality/protocol state, durable effect conditions, and $T(c)=OK$.

## Mechanisms, Invariants, or Proof Structure

The method-shape model follows directly from two independent cardinality choices. It does not rank shapes; it exposes the state added by each `*`. Each streaming direction introduces repeated framing, ordering, flow control, partial progress, and termination policy.

Within one direction, let messages be passed serially to a conforming gRPC runtime. The transport carries ordered bytes within its HTTP/2 stream, and the runtime reassembles length-prefixed messages, so delivered application messages preserve that order. This is a bounded argument: concurrent unsupported writes, separate streams, reconnects, and domain commits are outside the premise.

Flow control preserves a byte-window invariant but cannot prove bounded application memory. A handler can read every message as credit allows and enqueue them faster than workers drain. Therefore require both transport credit and $B_d(t)\le L$ at each application boundary. When the queue is full, stop reading/producing, shed according to policy, or cancel; silently allocating violates the invariant.

For recoverable server stream, if checkpoint $k$ means all records through $k$ are durably applied, reconnect requests records after $k$. A server may replay $k$ or later overlap; idempotent apply ensures duplicates do not change the result. Retention and gap detection are hypotheses. Neither per-call ordering nor terminal status alone proves cross-call completeness.

The executable lifecycle model checks four invariants: one-credit capacity blocks the second write; consuming restores capacity; half-close is explicit; terminal OK occurs only after the in-flight queue drains. It is deterministic local evidence, not empirical evidence about a gRPC implementation.

## Alternatives and Trade-Offs

**Unary versus server streaming.** Unary offers a simple atomic response contract and easy retries/caching, but must remain bounded and delays all results. Server streaming improves time-to-first-item and memory behavior when processed incrementally, but adds partial-result and resume semantics.

**Pagination versus server streaming.** Pagination makes progress/client pacing explicit and survives disconnection through page cursors; it adds round trips and can face snapshot drift. Streaming provides push-like incremental flow and one snapshot/session context; it pins resources and needs recovery. Choose from consistency, latency, duration, intermediaries, and client control.

**Client streaming versus repeated unary.** Client streaming amortizes call setup and supports one aggregate result/flow control. Repeated unary gives each item status, balancing, and independent retry. If item-level acknowledgment is essential, bidi or unary may fit better.

**Bidirectional stream versus paired streams/messages.** Bidi supplies low-latency correlated exchange on one call. Separate durable channels/jobs decouple availability and replay but add infrastructure and eventual coordination. A long-lived interactive session differs from durable event delivery.

**Automatic versus manual flow control.** Automatic control is safer and portable. Manual control can tie reads to exact capacity but is language-specific and deadlock-prone. Use it only with measured need and concurrency tests.

**Stateful pinned handler versus externalized session state.** Handler-local state is fast/simple but cannot resume elsewhere. Shared/fenced durable state supports failover at latency/complexity cost. Bounded ephemeral sessions may accept restart; critical transfers should externalize checkpoints.

**Compression versus raw messages.** Compression saves bandwidth for compressible large data but costs CPU/latency and can expose compression side channels or bombs. Negotiate supported algorithms, cap decompressed size, and disable for secrets/small data where appropriate.

## Failure Modes and Misconceptions

- **“Streaming means arbitrary size.”** Operational byte, count, time, and queue bounds remain mandatory.
- **“A successful write reached the server.”** It may only be buffered locally.
- **“Flow control is complete backpressure.”** Application queues and expensive work can still grow.
- **“HTTP/2 frames equal protobuf messages.”** gRPC messages can span/cohabit DATA frames.
- **“HTTP 200 means RPC success.”** gRPC terminal status in trailers decides the call.
- **“Bidi has one total order.”** Each direction is ordered independently.
- **“Order survives reconnect.”** A new call needs application sequence/cursor semantics.
- **“Half-close cancels.”** It closes one sending direction while the peer can continue.
- **“Cancellation retracts streamed effects.”** Already committed per-message effects remain.
- **“Retry resumes a stream.”** Retry creates a new call; recovery is application protocol.
- **“One stream balances continuously.”** It stays pinned to its selected backend.
- **“Keepalive proves service health.”** It tests connection responsiveness, not application correctness.
- **“One concurrent writer per message is harmless.”** Many language APIs prohibit simultaneous writes; serialize them.
- **“A prefix plus error is obviously useless.”** Validity is a contract decision, not a universal rule.
- **“Generated stubs ensure interoperability.”** Proxies, limits, status/trailer handling, schemas, and runtime versions still matter.
- **“Long-lived authorization stays valid.”** Policy/credentials may change; define recheck/renewal.

## Worked Examples

### Example 1

**Situation:** `GetInvoice(id)` returns one bounded invoice. **Reasoning:** No incremental result or repeated input exists. Unary gives one status and supports ordinary idempotent read retry. Server streaming one item adds lifecycle without meaning. **Conclusion:** choose unary.

### Example 2

**Situation:** Search can yield 50,000 independently useful hits under one snapshot. **Reasoning:** One unary list risks large allocation and delays first hit. Server streaming can deliver bounded messages and use flow control. Include snapshot/query ID and final completeness; use pagination instead if clients need durable pull cursors. **Conclusion:** server streaming is justified by incremental consumption, not count alone.

### Example 3

**Situation:** Upload 2 GiB as chunks and return one verified artifact ID. **Reasoning:** Client streaming bounds individual messages and yields one aggregate response. Each chunk carries session, offset, length/digest; server acknowledges durability only through stored progress and final OK after full digest/atomic publish. **Conclusion:** client streaming fits one aggregate, with application resume state.

### Example 4

**Situation:** A device sends readings while the server sends configuration commands. **Reasoning:** Both directions repeat independently, so bidi fits. Frames need type, ID/sequence, acknowledgments, authorization, and state machine. Per-direction order does not imply a command was caused by the immediately preceding reading. **Conclusion:** bidi requires explicit correlation/causality.

### Example 5

**Situation:** Both synchronous bidi peers write 1,000 large messages before reading. **Reasoning:** Each exhausts transport/window or buffers, then blocks while neither consumes to return credit. Alternate, run one reader and one serialized writer concurrently, or bound outgoing queues. **Conclusion:** manual/synchronous flow control can deadlock despite ordered reliable transport.

### Example 6

**Situation:** A server sends 20 valid rows, then returns `RESOURCE_EXHAUSTED`. **Reasoning:** If the contract says the prefix is independently valid with a resume cursor, the client may commit it and continue later. If it promises an all-or-nothing snapshot, the client discards/provisionally isolates it. **Conclusion:** terminal error does not universally decide prefix validity; the API must.

### Example 7

**Situation:** A feed disconnects after item 101 was sent, while client checkpoint is 99. **Reasoning:** “Sent” does not prove durable client apply. Reconnect after 99, accept overlap 100–101, and deduplicate by stable sequence/ID. Starting after 101 risks a gap. **Conclusion:** checkpoint tracks durable progress, not last observed network write.

### Example 8

**Situation:** Ten backends each receive roughly equal new streams, but one holds several day-long streams. **Reasoning:** call-start balancing cannot move established streams; active resource use becomes skewed. Use maximum age/renewal with checkpoints, stream-aware capacity, or durable shard routing. **Conclusion:** stream duration changes the balancing unit.

### Example 9

**Situation:** A proxy returns HTTP 200 but strips trailers. **Reasoning:** The client cannot observe the required `grpc-status`; a correct gRPC library reports protocol/unknown failure, not success. Test native streaming and trailers through the deployment path. **Conclusion:** generic HTTP success is insufficient gRPC evidence.

### Example 10

**Situation:** An operator's role is revoked during a four-hour command stream. **Reasoning:** Call-start authorization alone lets later privileged commands continue. Use bounded renewal and/or authorize each command against current policy; terminate safely on denial and audit processed sequence. **Conclusion:** long stream lifetime expands authorization policy.

## Cross-Program Connections

- **Network Engineering:** HTTP/2 multiplexing, stream/window flow control, connection failure, PING, and proxy behavior underpin transport mechanics.
- **Distributed Systems Engineering:** partial failure, replay, sequence/checkpoint, partition, and state placement govern stream recovery.
- **Concurrent & Parallel Programming:** async iteration, producer-consumer queues, one-reader/one-writer rules, and deadlock shape handlers.
- **Data Engineering:** chunked ingest, ordered feeds, watermarks/checkpoints, deduplication, and replay give concrete stream semantics.
- **Security Engineering:** long-lived authorization, quotas, decompression, metadata/body privacy, and message validation bound abuse.
- **Software Delivery & Reliability:** draining, reconnect storms, active-stream SLOs, overload, and fault injection make streaming operable.

## References

1. gRPC Authors, “Core concepts, architecture and lifecycle,” official four-method-shape, ordering, and lifecycle documentation, verified 2026-09-02. [gRPC documentation](https://grpc.io/docs/what-is-grpc/core-concepts/).
2. gRPC Authors, “gRPC over HTTP2,” official protocol mapping for headers, length-prefixed messages, trailers, status, and compression, verified 2026-09-02. [gRPC protocol specification](https://github.com/grpc/grpc/blob/master/doc/PROTOCOL-HTTP2.md).
3. IETF, RFC 9113, “HTTP/2,” June 2022, transport streams, multiplexing, flow control, frames, and connection management. [RFC Editor](https://www.rfc-editor.org/rfc/rfc9113.html).
4. gRPC Authors, “Flow Control,” official guide, verified 2026-09-02. [gRPC documentation](https://grpc.io/docs/guides/flow-control/).
5. gRPC Authors, “Performance Best Practices,” channel reuse, streaming, concurrent-stream, and measurement guidance, verified 2026-09-02. [gRPC documentation](https://grpc.io/docs/guides/performance/).
6. gRPC Authors, “Keepalive” and “Graceful Shutdown,” official lifecycle guidance, verified 2026-09-02. [Keepalive](https://grpc.io/docs/guides/keepalive/) and [graceful shutdown](https://grpc.io/docs/guides/server-graceful-stop/).
7. gRPC Authors, “Status Codes,” “Error Handling,” and “Compression,” official status/protocol/compression guidance, verified 2026-09-02. [Status codes](https://grpc.io/docs/guides/status-codes/), [error handling](https://grpc.io/docs/guides/error/), and [compression](https://grpc.io/docs/guides/compression/).

## Exercises

### Exercise 1

For each interaction—one bounded lookup, incremental change feed, chunked upload with one result, and interactive command/acknowledgment session—select a gRPC method shape and state the message cardinalities.

### Exercise 2

Trace a client-streaming call with two request messages through request headers, message frames, client half-close, one response, trailers, and status. Distinguish application write, peer read, durable commit, and terminal success.

### Exercise 3

Diagnose a bidi service whose memory grows with slow clients. HTTP/2 flow control is enabled, but each handler reads eagerly into an unbounded queue and four tasks write concurrently. Give a bounded, concurrency-safe repair and evidence plan.

### Exercise 4

Compare server streaming with cursor pagination for exporting a consistent million-row dataset through mobile clients and load balancers with five-minute idle/connection limits. Recommend a design including snapshot, recovery, and resource behavior.

### Exercise 5

Design the gRPC interaction for regional replication of safety-critical configuration. Peers exchange snapshots/deltas and acknowledgments; connections fail, backends restart, schemas skew, and stale writers must be fenced. Specify method shape, messages, ordering, flow control, commit/ack, resume, security, draining, and verification without claiming transport-level exactly-once delivery.

## Answers to the Exercises

### Answer 1

The bounded lookup is unary $(1,1)$. The change feed is server streaming $(1,*)$ when one subscription request yields many ordered events. The chunked upload is client streaming $(*,1)$ when many chunks collectively yield one artifact result. The interactive command/acknowledgment session is bidirectional $(*,*)$ because both directions repeat and interleave. These selections still require size/lifetime bounds and domain semantics; expected item count alone does not force streaming.

### Answer 2

The client opens one HTTP/2 stream and sends gRPC request headers. Each protobuf request is encoded into a gRPC length-prefixed message (compressed flag, four-byte length, bytes) carried across DATA frames. The local write may return when accepted/buffered by the runtime; it does not prove peer read or durable effect. After two messages the client sends end-of-stream/half-close, promising no more input. The server reads/validates according to flow control, commits the aggregate under its stated transaction, then sends response headers if not already sent, exactly one successful response message, and trailers with terminal `grpc-status`. Only observing the response and OK terminal status proves call-level success to the client; the server's durable record remains the authority if the response/status is lost.

### Answer 3

Transport flow control is being defeated after reads: memory moved from transport buffers into an unbounded application queue. Stop requesting/reading when a per-stream and per-principal byte/item queue reaches $L$; resume only as workers drain. Bound message/decompressed size, concurrent streams, work cost, and total lifetime; shed/cancel with a specific status under overload. Use one serialized writer task fed by a bounded outgoing queue and one reader task if the language permits concurrent read/write; never four concurrent writes unless the API explicitly guarantees it. Propagate cancellation and drain buffers on terminal state. Test a non-reading client, producer bursts, maximum messages, queue invariants, concurrent termination, flow-control stalls, CPU-heavy tiny messages, and load until rejection. Observe active streams, queue bytes, read/write stalls, message rates, cancellations, and memory.

### Answer 4

A single million-row stream can minimize round trips and preserve one server snapshot context, but mobile disconnection and five-minute connection limits make completion unlikely; it pins snapshot/backend resources and needs application resume anyway. Cursor pagination gives bounded calls, explicit client pacing, natural retry/load balancing, and durable progress. Recommend an idempotent export job or snapshot token plus cursor-paginated pages: create/freeze a snapshot with retention/authorization, return bounded pages ordered by stable key, and resume via opaque cursor tied to snapshot/query/principal. If low time-to-first-row is essential, short server streams per page can be used, but checkpoint at page/record boundaries. Expire snapshots visibly and offer restart; cap page bytes/time, rate-limit, and clean up. Test duplicate/missing rows across retries, snapshot expiry, mobile drops, proxy limits, and concurrent data changes.

### Answer 5

Use bidirectional streaming because each peer repeatedly sends snapshot/delta frames and acknowledgment/control frames, but make the durable replication protocol independent of one call. An `Open` frame authenticates peer, replica/config domain, supported schema/capabilities, current epoch/fence, and durable checkpoint. Data frames carry domain, epoch, monotonic sequence, stable change ID, schema version, previous/base version, payload/digest, and snapshot boundaries. Ack frames state the highest contiguous sequence durably validated and committed—not merely read—plus explicit gaps/rejections. Half-close/terminal rules distinguish planned drain from failure.

Serialize each direction; ordering applies only within this call/epoch. Bound messages, decompressed bytes, in-flight unacknowledged window, queues, snapshot size, stream age, and concurrency. Sender advances only within an application credit window derived from durable acknowledgments, in addition to transport flow control. Receiver enforces authenticated peer/domain authorization, current fencing epoch, schema compatibility, sequence continuity, idempotent change ID, and atomic config transition. Stale epochs are rejected. Checkpoints live in shared/fenced durable storage so a new backend resumes after the last committed ack; allow overlap and deduplicate, reject/repair gaps, and resnapshot when history expired.

Use mutual authentication/TLS, rotate through bounded stream renewal, authorize each domain/action, redact payloads, and rate-limit peers. Graceful drain stops new streams, sends reconnect intent if supported, persists checkpoints, permits bounded completion, then closes; clients reconnect with jitter. Verify old/new schema pairs, snapshots/deltas, concurrent/stale writers, reordered/gapped/duplicate application frames, slow peers, bounded queues, disconnect before/after commit/ack, crash/failover, lost trailers, connection-level multi-stream failure, credential/policy changes, drain/reconnect storms, and reconciliation of both replicas. The defensible guarantee is ordered per-call transport plus at-least-once replay and idempotent/fenced durable application within stated ledger/retention assumptions—not exactly-once delivery.
