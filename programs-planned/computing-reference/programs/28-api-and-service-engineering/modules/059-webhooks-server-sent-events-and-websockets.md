---
module_id: API-059
program: API & Service Engineering
level: 2
module_number: 59
title: Webhooks, Server-Sent Events, and WebSockets
status: complete
last_verified: 2026-09-02
---

# Webhooks, Server-Sent Events, and WebSockets

## One-Page Review

### Governing question

How should an API choose and operate webhook delivery, Server-Sent Events, or WebSockets so direction, ownership, acknowledgement, replay/resume, authentication, flow control, failure recovery, and lifecycle semantics remain explicit rather than being inferred from a persistent connection?

### Essential definitions

- A **webhook** is sender-initiated HTTP delivery to a receiver-registered endpoint, normally as discrete POST attempts.
- A **delivery attempt** is one HTTP exchange for an immutable event envelope; multiple attempts can carry the same event ID.
- An **acknowledgement** confirms only the documented receiver boundary—often durable acceptance—not completion of all downstream business work.
- **Server-Sent Events (SSE)** is the WHATWG `text/event-stream` format and `EventSource` API for one-way server-to-client events over an HTTP response.
- An **SSE event ID** updates client resume state; on reconnection a user agent can send `Last-Event-ID`.
- A **WebSocket** is a bidirectional framed protocol established by an HTTP opening handshake (or extended CONNECT where supported).
- **application acknowledgement** is an explicit protocol message proving a peer accepted/processed a particular application message; WebSocket transport success is not this proof.
- **backpressure** prevents a fast producer from creating unbounded queues for a slow receiver.
- A **resume token/sequence** identifies the last application event processed so a reconnect can request replay; it is application protocol, not automatic WebSocket reliability.
- **connection lifecycle** covers authenticate, authorize, open, keepalive/liveness, reauthorize, drain, close, reconnect, and cleanup.

### Central model, mechanism, or theorem

For immutable event identity $e$, webhook attempts $a_1,\ldots,a_n$ may be duplicated, delayed, or reordered. Receiver correctness therefore uses a durable inbox transition:

$$
accept(e)\iff e\notin Inbox,\qquad Inbox:=Inbox\cup\{e\}
$$

atomically with the receiver's accepted-work record. A 2xx response states only that this boundary succeeded.

For any push channel, bounded outstanding work requires

$$
Q(t)\le Q_{max};
$$

when the queue reaches the bound, the protocol must pause, coalesce, shed, disconnect, or persist elsewhere. A socket remaining open does not prove the peer processed prior messages.

### Critical invariants

Every event has a stable ID, type, schema version, occurred/produced time, subject/tenant scope, and documented ordering key. Webhook bodies are immutable across retries; receivers verify TLS plus authenticated sender/signature over exact governed components, timestamp/expiry/nonce as applicable, size/content type, and replay/idempotency before effects. Endpoint registration proves control and prevents SSRF/flooding; redirect, DNS/IP, egress, scheme/port, and metadata-network policy are explicit. Retry classes, backoff/jitter, attempt/age limits, `Retry-After`, disablement, redrive, and observability are governed.

SSE emits valid UTF-8 `text/event-stream` records, stable authorized event IDs, bounded replay retention, heartbeats, no-transform/no-buffer configuration, and cleanup on disconnect. `Last-Event-ID` is untrusted resume input and never authorization. WebSocket handshakes validate TLS, Origin where browsers apply, credentials, route, and subprotocol; messages have typed versioned envelopes, bounded frames/messages/queues/rates, ping/pong and idle/absolute lifetimes, reauthorization/credential-expiry behavior, application ack/resume rules, clean drain, and reconnect backoff. All channels reauthorize event visibility and redact secrets/personal payloads from logs.

### Common failures

Calling a webhook “exactly once”; generating a new event ID per retry; signing parsed/re-serialized JSON rather than agreed bytes/components; accepting old timestamps indefinitely; signature without replay defense; one forever-secret with no key ID/rotation; acknowledging before durable inbox insert; doing slow business work before response; retrying every 4xx; following redirects to internal hosts; DNS rebinding; registration test used as SSRF oracle; unbounded retry storms; event payload as database snapshot without schema/privacy policy; assuming SSE IDs guarantee retained replay; trusting `Last-Event-ID`; missing blank lines; proxy buffering/compression delay; heartbeats treated as domain events; one SSE connection per topic without browser/infra limits; authorizing WebSocket only at upgrade forever; token in URL logs; accepting any Origin/subprotocol; no message size/rate/queue bound; broadcast queues shared by slow clients; ping/pong confused with application ack; resume assumed from TCP ordering; reconnect without jitter; load balancer drain that drops sessions; and using a bidirectional socket for a durable integration that actually needs receiver-owned retries/audit.

### Compact example

A payment service emits event `evt-42` and stores one delivery record. Attempt 1 times out after the receiver atomically records `evt-42`; attempt 2 repeats the identical signed event. The receiver finds its inbox record and returns success without repeating the credit. A browser dashboard receives status events over SSE and resumes from a retained sequence; an operator-control session uses WebSocket only for interactive low-latency commands with explicit command IDs/acks. **Conclusion:** choose different channels for durable delivery, one-way observation, and bidirectional interaction; state their guarantees separately.

### Connections

[Idempotency Keys](037-idempotency-keys.md), [Deadlines, Cancellation, and Metadata](054-deadlines-cancellation-and-metadata.md), and [GraphQL Pagination and Incremental Delivery](057-graphql-pagination-and-incremental-delivery.md) provide effect, lifecycle, and streaming foundations. The next module synthesizes interface choice from interaction semantics.

## Governing Question

Who owns connection establishment and delivery state, which direction(s) carry application messages, what does acknowledgement prove, how are missed/duplicate/out-of-order messages recovered, and which bounds protect each participant during failure or slow consumption?

## Why This Matters

“Real time” hides several different requirements. A SaaS producer notifying a customer's backend needs durable attempts, endpoint governance, signature verification, and replay tooling. A browser observing a one-way feed often benefits from ordinary HTTP semantics and automatic SSE reconnection. A collaborative control surface needs low-latency messages in both directions and may justify WebSocket session complexity.

Choosing from fashion creates reliability/security gaps. Webhooks cross an outbound SSRF boundary. SSE is text-only and one-way in the browser API, but its simplicity fits proxies and authorization models better than a custom socket in many cases. WebSockets preserve framed message ordering on one live connection but provide no durable event history, application acknowledgement, or reconnect resume by themselves.

All three expose partial failure. A response can be lost after webhook acceptance; an SSE connection can break after bytes reach the client but before application state commits; a WebSocket process can die after accepting a command. Correct protocols use stable identities, explicit state machines, bounded buffers, and recovery queries/replay rather than claiming the transport eliminated ambiguity.

## Prerequisites and Retrieval

Retrieve [Idempotency Keys](037-idempotency-keys.md), [API Threat Modeling](041-api-threat-modeling.md), [Credential and Token Handling](042-credential-and-token-handling.md), [Deadlines, Cancellation, and Metadata](054-deadlines-cancellation-and-metadata.md), and [GraphQL Pagination and Incremental Delivery](057-graphql-pagination-and-incremental-delivery.md). Be able to distinguish transport receipt, durable acceptance, business completion, ordering, idempotency, liveness, replay, backpressure, and cancellation.

## Learning Objectives

After completing this module, you can:

1. select webhook, SSE, or WebSocket from direction, participant, durability, latency, and client constraints;
2. design a webhook sender/receiver state machine with signature, replay, inbox, retry, disablement, and redrive;
3. secure endpoint registration and outbound delivery against SSRF, redirects, DNS changes, and credential leakage;
4. encode and parse SSE events with IDs, resume, retention, heartbeats, buffering, and authorization semantics;
5. design a WebSocket subprotocol with handshake authentication, versioned messages, application acks, resume, and close behavior;
6. enforce per-message, queue, connection, rate, concurrency, and lifetime bounds;
7. reason about ordering and duplicate/loss windows across reconnects;
8. operate deployment, draining, observability, secret rotation, and incident recovery; and
9. verify wire behavior and business effects through faults and adversarial tests.

## Core Exposition

### Choose by interaction semantics

Start with producer/consumer location, connection initiator, direction, browser/native/server constraints, delivery durability, latency, message frequency/size, ordering scope, offline duration, network/proxy environment, and operational ownership.

Use webhooks when a producer must notify an independently operated server endpoint and own retry/audit state. Use SSE when an HTTP client opens a long-lived one-way server feed, especially for browser notifications, progress, or read models. Use WebSocket when both peers need frequent low-latency messages on one session and the organization can operate stateful connections and an application subprotocol.

Polling or conditional GET may be better for low frequency, tolerant latency, offline clients, or simple infrastructure. A broker is better when durable high-volume fan-out, replay, partitions, or consumer groups are core. Do not make a public WebSocket impersonate a broker without persistence/flow-control semantics.

### Define a stable event envelope

Across mechanisms, define event ID, type, schema/spec version, source, subject/resource, tenant/audience, occurred time, produced time, ordering/partition key, trace correlation, and typed data. Distinguish domain event from delivery attempt metadata. Do not put attempt number into the event identity or sign only mutable transport metadata.

Events state facts in past tense; commands request effects. A WebSocket may carry both, so envelope `kind` and correlation/causation IDs are essential. Webhook endpoints normally receive notifications rather than arbitrary commands unless the contract explicitly authorizes them.

Schema evolution follows additive/default/deprecation policy with consumer testing. Payload minimization matters because events may be retained, retried, cached, or logged. Prefer resource ID plus essential fact over copying an entire sensitive record; provide an authorized fetch for current state when appropriate.

CloudEvents can standardize event metadata/HTTP bindings, but it does not by itself define persistence, integrity, authorization, or delivery guarantee. Adopt a named release/profile rather than mixing headers ad hoc.

### Implement webhook sender state as durable work

Create one immutable event and one delivery record per subscription/endpoint. State might be pending, leased/in-flight, succeeded, scheduled-retry, exhausted, or disabled/cancelled. Lease attempts so worker death returns work safely. Record attempt number, start/end, classified result, next time, response status/latency, and bounded diagnostic—not response secrets/body dumps.

Send HTTPS POST with content type, event/delivery ID, timestamp, schema/type, user agent, trace linkage, and authentication/signature. Use one shrinking attempt timeout with connect/read/body limits. Do not follow redirects by default: a previously validated destination can redirect to internal infrastructure or leak credentials/signatures.

Interpret success under the contract—commonly selected 2xx. `202 Accepted` means receiver accepted but has not completed processing, not business success. Permanent 4xx such as invalid schema/authorization/410 normally stop or disable; 408/429/5xx/network ambiguity may retry. Honor valid bounded `Retry-After` where policy permits. Classify per provider contract; status code alone cannot express every case.

Use exponential backoff with full/decorrelated jitter, maximum delay, attempt count, and event age. Per-endpoint concurrency/rate plus global bulkheads prevent one failing receiver from causing a retry storm. Dead-letter/exhausted state supports inspected redrive of the same event ID; manual resend never changes semantics silently.

### Verify webhook authenticity and prevent replay

TLS authenticates the connection endpoint, but a receiver still needs sender authentication/integrity. Options include mTLS, OAuth-style credentials, standardized HTTP Message Signatures, or a documented HMAC envelope. Do not invent cryptography. RFC 9421 signs covered HTTP components with `Signature-Input`/`Signature` and parameters including created/expires/nonce as chosen; security depends on sufficient covered components and key policy.

For common HMAC profiles, sign a canonical prefix containing version, timestamp, event ID, and exact raw body bytes. Verify header syntax/count/size, key ID/algorithm allowlist, timestamp window/expiry, signature in constant time, then event replay/idempotency. Verify before JSON parsing when the signature covers raw bytes. Re-serialization changes bytes and can break or weaken the agreement.

A timestamp window limits replay but does not prevent duplicates inside it. Durable inbox/idempotency keyed by sender + event ID does. Nonces require a retained uniqueness store. Decide retention at least as long as sender retry/redrive risk. Signature success proves possession of a key over covered components, not domain authorization or schema validity.

Rotate secrets/keys with explicit key IDs and overlap. Accept old/current verification keys during a bounded window; send with current key or multiple signatures only under the adopted profile; revoke compromised keys and redrive safely. Never place secrets in query strings or log signature/authorization values.

### Acknowledge after a durable receiver boundary

The receiver should authenticate/verify, bound/decode/validate, authorize sender/event/tenant, and atomically insert inbox event plus accepted-work/outbox/domain transition before responding success. If downstream processing is slow, enqueue durably then return. If no durable acceptance exists, a 2xx can lose the event after crash.

If insertion finds existing event ID, compare immutable identity/type/payload digest according to contract. Same ID with different payload is an integrity incident, not an idempotent duplicate. Return stable success for true duplicates so sender stops retrying; do not repeat effects.

An inbox cannot make arbitrary side effects exactly once. External calls need their own idempotency/reconciliation. State the effective guarantee: at-least-once attempts plus idempotent/deduplicated acceptance, bounded retention, and possible reordering.

### Secure endpoint registration and outbound networking

Webhook URL registration is an SSRF and reflected-flooding surface. Authenticate/authorize the registering principal and bind endpoint to tenant/product/event types. Require HTTPS except narrowly controlled development. Parse URLs with one maintained library; allow schemes/ports/domains by policy; reject userinfo/fragments and ambiguous encodings.

Resolve DNS and reject loopback, link-local, private/internal, multicast, metadata, and reserved destinations unless explicitly supported. Revalidate resolved IP on every connection to counter DNS rebinding; connect to the vetted address while preserving correct TLS hostname/SNI verification. Use egress proxies/firewall allowlists and separate delivery network identity. IPv4/IPv6 and redirects need equal checks.

Prove endpoint control with an authenticated challenge/response or webhook validation handshake before normal volume. A successful arbitrary HTTP response is not enough if it can be forged; do not expose response bodies/timing as a general network scanner. Limit validation rate/bytes/time and require reconfirmation after material URL/ownership changes.

### Encode SSE exactly

An SSE response uses `Content-Type: text/event-stream` and UTF-8 event records. Lines can carry `event`, `data`, `id`, and `retry`; a blank line dispatches an event. Multiple `data` lines join with newline. Lines beginning with colon are comments and can serve as heartbeats. Unknown fields are ignored by the standard parser.

Use a maintained serializer; escape/split data line-by-line so embedded newlines cannot inject unintended fields. Event names and payload schemas are versioned. Flush complete records. Configure caching and intermediary buffering appropriately (`Cache-Control`/proxy-specific no-buffer behavior) and test compression, HTTP/2, CDN, service mesh, and runtime flushing rather than assuming headers work.

Browser `EventSource` initiates the request and receives server-to-client text events. Client-to-server actions use separate HTTP requests. Native/custom clients may expose extra header features; document portability because browser EventSource authentication choices (cookies/URL/CORS) differ. Never put bearer tokens in URLs.

### Make SSE resume semantics honest

When an SSE event contains `id`, the user agent updates last-event-ID state. On reestablishment it can send `Last-Event-ID`; the `retry` field can update reconnection delay. These are transport/application hooks, not guaranteed durable replay.

Treat `Last-Event-ID` as untrusted input. Authenticate current request, authorize the stream/topic/tenant, parse/bound the ID, and seek only within that authorized retained log. Define IDs as monotonic within a stream/partition or opaque resume tokens bound to scope. Return a reset/snapshot-required event or appropriate HTTP error when the position expired; never silently replay another tenant.

Delivery between network and browser application is ambiguous. Client handling must be idempotent by event ID if duplicates matter. If exactly-once UI application is required, persist client checkpoint after state update; browser EventSource internal state alone may advance before application durability.

Heartbeats keep intermediaries active and reveal liveness, not event delivery. Set server idle timeout above heartbeat interval and client reconnect with jitter around native behavior where controllable. Bound connections per actor/tenant/IP, replay batch/bytes, stream lifetime, and server queues.

### Establish WebSockets securely

RFC 6455 starts with an HTTP/1.1 opening handshake using Upgrade; RFC 8441 defines extended CONNECT for WebSockets over HTTP/2 when client/server/intermediaries support it. Feature-test deployment paths. Use `wss` in production and validate certificate/hostname.

Authenticate during handshake using safe headers/cookies/tickets supported by the client. Browser WebSocket APIs constrain custom headers, so use secure same-site cookies with CSRF/Origin defenses or a short-lived single-use connection ticket—not long-lived tokens in URLs. Validate `Origin` against an allowlist for browser-accessible endpoints; non-browser clients require their own authenticated identity. Origin is not authentication.

Select only supported `Sec-WebSocket-Protocol` values and make subprotocol version part of the contract. Do not echo arbitrary protocol strings. Authorize connection scope (tenant/topics/actions) and each command/subscription/resource. Credential expiry or policy revocation requires reauth, scope downgrade, or bounded close—not an immortal session.

### Define a WebSocket application protocol

RFC 6455 supplies text/binary messages, fragmentation, masking rules, Ping/Pong, and Close. It does not define domain message schemas, request/response correlation, subscriptions, application acknowledgements, replay, or durability.

Define an envelope with protocol version, message kind, message ID, correlation ID, optional subscription/topic, sequence/resume data, timestamp, and typed payload. State which peer can send each kind, state-machine prerequisites, ordering scope, max size, error response, ack meaning, retry/idempotency, and close code/reason.

TCP/WebSocket preserves byte/message order on one connection subject to API framing, but concurrent application handlers can complete out of order. If order matters, serialize per key or carry sequence/version and reject/reconcile. Across reconnect there is no continuity unless the server retains an authorized log/session and client presents a valid resume token/checkpoint.

Ping/Pong shows protocol peer responsiveness. An application ack says a particular command/event reached a documented boundary. Use command IDs/idempotency because response loss/reconnect leaves outcomes uncertain. Provide a status/query recovery path for committed effects.

### Enforce backpressure and bounds

Every connection has bounded inbound frame/message bytes, decompressed bytes/ratio, JSON depth/fields/strings, messages per interval, outstanding requests, subscriptions/topics, outbound queue messages/bytes/age, replay size, and lifetime. Validate before allocation/parse where possible. Compression extensions need explicit negotiation and bomb/side-channel analysis; disable when value is small.

When outbound queue is full, choose by semantics: coalesce replaceable state updates, drop low-priority telemetry with gap signal, pause upstream, persist to a broker/log, or close slow consumers with a reconnect/resync reason. Never let one client retain unbounded shared objects. Broadcast uses per-client bounds rather than waiting for the slowest or sharing one mutable queue.

Apply global/tenant/actor/IP connection and message quotas, handshake rate limits, concurrency bulkheads, OS descriptor/memory limits, and load shedding. Long-lived sessions must not bypass the request rate controls applied elsewhere.

### Operate liveness, drain, reconnect, and recovery

Set protocol Ping/Pong or application heartbeat policy consistent with intermediaries. Detect half-open sessions after bounded missed liveness. Use absolute maximum lifetime to exercise reauthentication, load redistribution, and cleanup. Close with a documented code/reason, then release subscriptions, loaders, buffers, and presence leases idempotently.

During deploy, stop accepting new sessions, signal restart/retry hints if the subprotocol supports them, drain for a bound, persist checkpoints if owned, then close. Clients reconnect with exponential jitter and stable resume/session identity; servers prevent thundering herds and reject expired/forged tokens.

Load balancing can use any instance if subscriptions/state live in a shared broker/log; sticky sessions simplify local state but complicate failover/drain. Presence is leased/ephemeral and must tolerate disconnect races. Do not infer user logout/business absence immediately from TCP close.

### Observe and test each guarantee

For webhooks record event/delivery ID, endpoint/subscription ID, attempt, classified outcome, latency, next retry, signature key/version (not value), duplicate/inbox result, age, redrive/disablement, and safe response diagnostics. For SSE/WebSocket record connection ID, authenticated scope, protocol/version, open/close reason, duration, resume point/gap, messages/bytes, queue high-water, drops/coalesces, heartbeats, auth expiry, and errors. Avoid payload/token/cursor/signature logging.

Fault tests drop responses after receiver commit, reset connections mid-body/message, reorder/duplicate webhook attempts, expire keys/timestamps/replay retention, return each HTTP class/`Retry-After`, rebind DNS/redirect, and crash worker leases. SSE tests split every byte/line boundary, multi-line data, ID/reset, expired/spoofed resume, proxy buffering, heartbeat, slow client, and authorization revocation. WebSocket tests malformed/unmasked/fragmented/oversize/compressed frames, invalid UTF-8, Origin/subprotocol, flood/slow consumer, concurrent commands, ack loss, reconnect/resume, reauth, process death, and deploy drain.

## Definitions and Notation

Let immutable event $e=(id,type,version,scope,time,data)$ and delivery attempt $a=(e,endpoint,attempt,time)$. Let receiver inbox $I$ retain accepted event IDs/digests, sender delivery state $D$, and retry schedule $t_n$. Let SSE retained sequence $L_s=[e_k,\ldots,e_m]$ for authorized stream scope $s$ and client checkpoint $c$.

For WebSocket connection $w$, let identity/scope $A_w$, subprotocol version $v_w$, inbound/outbound queue lengths $Q_i,Q_o$, maximums $Q_{i,max},Q_{o,max}$, last confirmed application sequence $q_w$, and deadline/credential expiry $T_w$. Transport liveness $Live(w)$ is distinct from application acknowledgement $Ack(w,message)$.

At-least-once webhook delivery means successful events can have $attempts(e)\ge1$ and duplicates are allowed; it does not imply infinite retry. SSE/WebSocket resume is defined only for positions retained and authorized under the current scope.

## Mechanisms, Invariants, or Proof Structure

Webhook ambiguity follows from a lost response after receiver commit: sender observes timeout and cannot distinguish commit from no receipt, so safe retry produces a possible duplicate. Stable event identity plus atomic receiver inbox/effect acceptance makes the duplicate observationally idempotent within retention. Transport alone cannot prove exactly-once effects.

Signature verification without freshness/nonce/inbox accepts captured valid messages again. Timestamp expiry bounds capture utility but two deliveries within the window still verify; event-ID inbox supplies semantic duplicate protection. Thus integrity, freshness, and idempotency are complementary.

An SSE ID enables resume only if the server maps it to an authorized retained ordering position. The WHATWG parser/user-agent behavior does not create server persistence. A forged `Last-Event-ID` proves nothing about prior receipt or entitlement.

WebSocket ordering on one live connection does not imply processing order if handlers execute concurrently, nor continuity after reconnect. Application sequence, serialization, ack, durable log, and resume policy are necessary when those properties matter.

Bounded queue safety is immediate: if producer rate exceeds consumer rate for long enough and no shed/pause/persist action occurs, $Q(t)$ grows without bound. Enforcing $Q_{max}$ forces an explicit semantic choice before memory exhaustion.

## Alternatives and Trade-Offs

Webhooks shift connection initiation/retry ownership to producer and work across organizations/firewalls, but create endpoint SSRF, signature, retry, and support burden. Pull polling is simpler for consumers, naturally handles offline periods, and can use caching, but adds latency/repeated empty requests.

SSE uses ordinary HTTP, UTF-8 text, native browser reconnect/ID hooks, and one-way semantics. WebSocket supports bidirectional text/binary and lower per-message overhead after setup, but requires subprotocol, session infrastructure, backpressure, reauth, drain, and custom resume.

A broker provides durable log/replay/consumer groups and stronger internal scale primitives but requires shared infrastructure/protocol access. Webhooks can bridge broker events to external receivers. SSE/WebSocket can project a broker/log to interactive clients with authorization and per-client bounds.

HMAC shared secrets are simple but duplicate secret material and complicate sender attribution. Asymmetric/HTTP message signatures can centralize public verification and richer component coverage but add key distribution/profile complexity. mTLS strongly authenticates workloads but not event identity/replay alone. Layer as needed.

Full event payload enables offline processing but increases privacy/staleness/schema burden. Thin notification plus authorized fetch minimizes event data but depends on resource availability/current-state semantics and extra calls.

## Failure Modes and Misconceptions

- **“A webhook 2xx means the business process completed.”** It proves only the documented acknowledgement boundary.
- **“Retries make webhooks exactly once.”** Response loss forces possible duplicates; idempotent inbox/effects handle them.
- **“A valid signature is fresh.”** Captured valid requests replay unless timestamp/expiry/nonce and event deduplication are enforced.
- **“HTTPS makes arbitrary registered URLs safe.”** SSRF, DNS rebinding, redirects, internal PKI, and reflected flooding remain.
- **“SSE automatically replays everything.”** EventSource carries a resume hint; server retention/scope define replay.
- **“SSE heartbeats prove event processing.”** Comments/bytes show connection activity, not application durability.
- **“WebSocket is guaranteed delivery.”** It frames an ordered live byte stream; application ack/durability/reconnect are separate.
- **“Ping/Pong acknowledges my command.”** Control frames test protocol liveness, not domain acceptance.
- **“One socket avoids rate limiting.”** Message/work/queue and connection lifetime require semantic quotas.
- **“TCP backpressure protects application memory.”** Libraries often queue above the socket; explicit application bounds are required.
- **“Sticky sessions solve state.”** They reduce routing change but do not provide failover, durable resume, or drain correctness.
- **“Real time is one architecture.”** Durable integration, one-way observation, and interactive duplex control have different owners and guarantees.

## Worked Examples

### Example 1

**Situation:** Webhook response is lost after inbox commit. **Reasoning:** sender retries same event ID/body; receiver detects existing identical digest and returns success without repeating effect. **Conclusion:** stable identity resolves the acknowledgement gap.

### Example 2

**Situation:** Signature over JSON object is recomputed after parser normalizes whitespace. **Reasoning:** byte agreement is lost. Verify the specified raw body/components before parsing and use a standard profile. **Conclusion:** signatures cover defined representations.

### Example 3

**Situation:** Customer registers `https://169.254.169.254/...` through a redirecting domain. **Reasoning:** delivery becomes metadata SSRF. Reject internal/reserved resolved addresses on every connection, forbid redirects, and use constrained egress. **Conclusion:** webhook sending is an outbound security boundary.

### Example 4

**Situation:** Receiver returns 429 with bounded `Retry-After`. **Reasoning:** sender schedules under per-endpoint/global limits and jitter, preserving event ID; it does not busy-loop. **Conclusion:** retries are governed durable state.

### Example 5

**Situation:** SSE disconnects after event ID 81. **Reasoning:** client reconnects with `Last-Event-ID: 81`; server authenticates, validates scope/retention, and resumes after 81 or signals snapshot reset. **Conclusion:** ID is a scoped resume request.

### Example 6

**Situation:** Proxy buffers SSE for 60 seconds. **Reasoning:** valid records arrive too late. Disable/adjust buffering/compression, emit heartbeats, and verify through the production path. **Conclusion:** streaming is end-to-end behavior.

### Example 7

**Situation:** Browser opens WebSocket from an attacker origin using victim cookies. **Reasoning:** server authenticated cookie but failed Origin/CSRF-style handshake policy. Allowlist Origin and use connection tickets/same-site defenses. **Conclusion:** browser handshake needs cross-site protection.

### Example 8

**Situation:** Client sends command 17, connection dies, and no response arrives. **Reasoning:** command may have committed. Reconnect and query by idempotent command ID/status rather than issue a new identity. **Conclusion:** sockets retain distributed outcome ambiguity.

### Example 9

**Situation:** One slow WebSocket client accumulates 500 MB broadcast queue. **Reasoning:** impose per-client byte/age bound; coalesce state or close with resync requirement while other clients continue. **Conclusion:** backpressure is per consumer and semantic.

### Example 10

**Situation:** Deploy kills 100,000 sockets simultaneously and clients reconnect immediately. **Reasoning:** drain in waves, send restart hints, close boundedly, require exponential jitter, and admission-limit reconnects. **Conclusion:** lifecycle behavior determines availability.

## Cross-Program Connections

- **Distributed Systems Engineering:** partial failure, at-least-once attempts, deduplication, ordering, leases, replay logs, and reconciliation define guarantees.
- **Security Engineering:** HTTP signatures, key rotation, replay, SSRF, Origin, CSRF, credentials, tenant scope, and side channels protect participants.
- **Network Engineering:** HTTP semantics, DNS/TLS, proxies, framing, flow control, Ping/Pong, buffering, and load balancing implement channels.
- **Concurrent Programming:** bounded queues, per-key serialization, cancellation, leases, and cleanup prevent races/leaks.
- **Event-Driven Architecture:** event envelopes, schemas, brokers, partitions, consumer checkpoints, and outbox/inbox connect internal and external delivery.
- **Reliability Engineering:** retry budgets, jitter, bulkheads, dead letters, drain, load shedding, and fault injection make recovery operational.

## References

1. WHATWG, “HTML Standard: Server-sent events,” current EventSource processing, `text/event-stream`, fields, reconnection, and `Last-Event-ID`, verified 2026-09-02. [WHATWG HTML](https://html.spec.whatwg.org/multipage/server-sent-events.html).
2. IETF, RFC 6455, “The WebSocket Protocol,” December 2011, handshake, framing, masking, control frames, Origin, closing, and security. [RFC Editor](https://www.rfc-editor.org/rfc/rfc6455.html).
3. IETF, RFC 8441, “Bootstrapping WebSockets with HTTP/2,” September 2018, extended CONNECT and HTTP/2 stream behavior. [RFC Editor](https://www.rfc-editor.org/rfc/rfc8441.html).
4. IETF, RFC 9421, “HTTP Message Signatures,” February 2024, component signatures, key identifiers, created/expires/nonce, verification, and replay considerations. [RFC Editor](https://www.rfc-editor.org/rfc/rfc9421.html).
5. CNCF CloudEvents, “HTTP Web Hooks for Event Delivery,” HTTPS POST, response classification, `Retry-After`, authorization, and abuse-protection handshake, verified 2026-09-02. [CloudEvents specification](https://github.com/cloudevents/spec/blob/main/cloudevents/http-webhook.md).
6. Standard Webhooks, “Standard Webhooks Specification,” event/timestamp/signature headers, exact payload signing, constant-time verification, replay protection, idempotency, and rotation, verified 2026-09-02. [Specification](https://github.com/standard-webhooks/standard-webhooks/blob/main/spec/standard-webhooks.md).
7. OWASP, “API7:2023 Server Side Request Forgery,” webhook URL registration and server-side URL-fetch risk, verified 2026-09-02. [OWASP API Security](https://owasp.org/API-Security/editions/2023/en/0xa7-server-side-request-forgery/).

## Exercises

### Exercise 1

Define webhook attempt, acknowledgement, SSE, Last-Event-ID, WebSocket, application acknowledgement, backpressure, resume token, and connection lifecycle. Compare their guarantees.

### Exercise 2

Design webhook sender/receiver state machines for an event that times out after receiver commit, then gets 429, then succeeds as a duplicate. Include event identity, leases, signature/replay, inbox transaction, backoff, and evidence.

### Exercise 3

Design an SSE incident feed with tenant authorization, event format, sequence IDs, retention expiry, reconnect/reset, heartbeats, proxy configuration, slow-client bounds, revocation, and client idempotency.

### Exercise 4

Design a WebSocket collaborative-control subprotocol with browser handshake, message envelope, subscriptions/commands, application acks, ordering, resume, bounds, heartbeats, reauth, close/drain, and recovery.

### Exercise 5

Choose and compose mechanisms for emergency dispatch: partner-system durable notifications, browser operator status, and interactive unit commands. Specify security, durability, partial failure, backpressure, deployment, observability, and adversarial verification; justify where polling/broker fits.

## Answers to the Exercises

### Answer 1

A webhook attempt is one sender-initiated HTTP exchange for an immutable event/endpoint. Acknowledgement confirms only the declared receiver boundary, ideally durable acceptance. SSE is a one-way UTF-8 HTTP event stream; Last-Event-ID is client resume state sent on reestablishment, not proof of authorization or replay retention. WebSocket is a bidirectional framed protocol after handshake. Application ack names a message and proves a documented app boundary; Ping/Pong does not. Backpressure bounds producer/consumer imbalance. A resume token/sequence asks an application log/session to continue after reconnect. Lifecycle covers open/auth, use/liveness/reauth, drain/close/reconnect/cleanup.

Webhook delivery can own durable retries across offline receivers but duplicates/reordering remain. SSE has standardized parsing/reconnect hooks but server retention and client application durability determine replay. WebSocket provides live bidirectional framing/order on one connection, while durability, ack, resume, and reconnect are application protocol.

### Answer 2

Sender stores immutable event ID/type/version/scope/body digest and per-endpoint delivery pending. Worker leases it, signs exact governed timestamp+ID+body components with current key, sends under timeout, and records attempt safely. Receiver bounds headers/body, verifies TLS/sender signature in constant time, timestamp/expiry/nonce as profile requires, then parses/schema-validates/authorizes. In one transaction it inserts `(sender,event_id,digest)` into inbox plus accepted work/domain/outbox. It responds success only after commit.

First response is lost after commit, so sender classifies ambiguous timeout and schedules exponential full-jitter retry under attempt/age/rate limits. If a later attempt receives 429 with valid bounded Retry-After, it reschedules without changing event ID/body. When receiver sees retry, identical inbox digest proves duplicate; it does not repeat effect and returns success. Sender marks delivery succeeded. Same ID/different digest is an integrity incident.

Evidence includes delivery/attempt IDs, lease, key version, safe HTTP class/latency, retry time/reason, event age, receiver signature/freshness result, inbox inserted/duplicate/conflict, accepted-work ID, and final state—never secrets/raw sensitive payload. Fault tests lose response at each commit boundary, crash leases, replay within/outside window, rotate/revoke keys, and verify one accepted effect.

### Answer 3

Expose authenticated HTTPS GET returning `text/event-stream`; authorize tenant/feed at open and every event or on policy-version change. Emit complete records such as `event: incident-status`, `id: <tenant-bound-monotonic-sequence>`, and one/multiple safe `data:` lines containing versioned minimal JSON, terminated by blank line. Serialize safely and use comment heartbeats.

Retain a per-tenant authorized log for a documented window. On reconnect, treat Last-Event-ID as untrusted: validate syntax/bounds/scope and current authorization; replay only later retained events. If expired/unknown, return a versioned reset/snapshot-required event or documented HTTP response so client fetches current snapshot and checkpoints anew. Client applies by event ID idempotently and persists checkpoint after state update when durability matters.

Configure/test no caching transformation, proxy/CDN buffering, compression flush, HTTP/2, idle timeouts, CORS/cookie credentials, heartbeat interval, disconnect cleanup, and load balancer drain. Bound connections per actor/tenant/IP, replay events/bytes, outbound queue/age, lifetime, and slow consumption; coalesce replaceable status or disconnect with resync rather than buffer indefinitely. On revocation stop events and close. Test spoofed/cross-tenant IDs, byte/line fragmentation, multiline data, duplicate/gap, retention expiry, slow readers, proxy buffering, network resets, secret leakage, and reconnect herd.

### Answer 4

Use `wss`; validate route, TLS, allowed Origin, short-lived single-use browser connection ticket or protected same-site cookie, and an allowlisted versioned subprotocol. Connection context records actor/tenant/scopes/policy/credential expiry. Authorize each subscribe/unsubscribe/command/resource; reauthorize on changes or close/downgrade at expiry.

Envelope has protocol version, kind, message ID, correlation ID, channel/document, sequence/base version, timestamp, and typed payload. Kinds include subscribe, unsubscribe, command, command-ack/result, event, gap/reset, error, reauth, and drain. Commands use idempotent IDs and optimistic/base versions; server serializes per collaboration key or exposes sequence/conflict. Ack states durable acceptance or completion explicitly. Events carry monotonic per-channel sequence; server retains a bounded log/session and signed scope-bound resume token. On gap/expiry client fetches snapshot.

Bound frame/message/decompressed/input structure, messages/rate, outstanding commands, subscriptions, connection count, outbound queue bytes/messages/age, replay, idle/absolute lifetime, and concurrency. Ping/Pong detects liveness; application acks track commands. Slow client gets coalescing/gap+resync or close. Reject invalid UTF-8/masking/Origin/subprotocol/types/state transitions.

Drain stops upgrades, signals retry hint, lets bounded in-flight commands settle, persists outcomes/checkpoints, closes with documented code, and releases leases/subscriptions. Client reconnects with exponential jitter, resumes or snapshots, and queries uncertain command IDs. Test ack/response loss after commit, concurrent edits, duplicates, out-of-order handler completion, auth revocation, oversize/compression bombs, flood/slow consumer, process death, failover, resume forgery/expiry, and mass deploy reconnect.

### Answer 5

Use a durable broker/outbox as internal source of truth. Deliver partner notifications through webhooks because partners operate server endpoints and need producer-owned retry/audit. Event IDs are stable across attempts; HTTPS plus vetted signature/mTLS profile, freshness/replay/inbox requirements, endpoint-control handshake, SSRF-safe egress, classified jittered retry, per-partner bulkheads, dead-letter/redrive, and schema/privacy contracts apply. Acknowledgement means partner durable acceptance, not dispatch completion.

Use SSE for browser operator status because direction is primarily server-to-browser. Project authorized minimal events from broker/log, with tenant-bound sequence, retention and snapshot reset, heartbeats, proxy flush tests, bounded connections/replay/queues, revocation, and idempotent UI checkpoint. Polling/conditional snapshot is fallback for offline/old/proxy-constrained clients and recovery from expired gaps.

Use WebSocket for frequent interactive unit commands/status only where bidirectionality/latency justify it. Authenticate `wss` handshake and Origin/subprotocol, authorize every unit/incident action, use idempotent command IDs plus explicit durable-acceptance/result acks, per-unit sequence/resume, snapshot recovery, queue/rate/frame/lifetime limits, slow-consumer policy, reauth, drain, and reconnect jitter. Durable command workflow/outbox survives socket/process loss; socket is session transport, not record of truth.

Across channels define versioned event/command envelopes, tenant/subject/order keys, deadlines/cancellation, minimal sensitive location data, protected audit, and outcome status. Isolate failing partners/clients, reconcile broker offsets/inboxes/command ledger, and never infer rollback from disconnect. Observe safe identities, attempts, gaps, queues, drops, acks, latency, close reasons, replay age, and no tokens/payload secrets.

Fault/adversarial tests cover lost webhook response after commit, duplicate/reorder/retry storm, key rotation/replay, SSRF/DNS rebinding/redirect, SSE fragmentation/buffering/gap/revocation, WebSocket cross-site handshake/flood/slow queue/ack loss/resume/process death/drain, broker lag/duplication, cross-tenant IDs, and recovery drills. Polling is the universal low-complexity fallback; the broker supplies durable internal replay/fan-out rather than forcing public transports to emulate it.
