---
module_id: API-009
program: API & Service Engineering
level: 1
module_number: 9
title: HTTP/1.1, HTTP/2, and HTTP/3 Semantics
status: complete
last_verified: 2026-09-01
---

# HTTP/1.1, HTTP/2, and HTTP/3 Semantics

## One-Page Review

### Governing question

Which parts of an HTTP API remain semantically identical across HTTP/1.1, HTTP/2, and HTTP/3, and which transport differences change performance, failure, security, and observability?

### Essential definitions

- **HTTP semantics** assigns meaning to methods, targets, status codes, fields, and content independently of a particular wire version.
- HTTP/1.1 uses a textual message syntax over ordered byte-stream connections and frames content with lengths, transfer coding, or connection closure.
- HTTP/2 maps messages to binary frames on multiplexed streams over one TCP connection and compresses fields with HPACK.
- HTTP/3 maps messages to frames on QUIC streams, normally over UDP, and compresses fields with QPACK.
- **Multiplexing** interleaves independent streams on one connection; it does not make application work parallel or eliminate every queue.
- **head-of-line blocking** occurs when earlier blocked work prevents later independent work from progressing at some layer.
- **connection coalescing** reuses one connection for more than one origin when protocol identity and certificate requirements permit it.

### Central model, mechanism, or theorem

Model an exchange as semantic message $M$ transformed by version-specific encoder $encode_v(M)$, transported, then decoded. Correct interoperability requires $decode_v(encode_v(M))\equiv M$ for the semantic properties the protocol preserves. Version choice changes framing, ordering, compression, flow control, and failure scope; it must not silently redefine GET, status `404`, `Content-Type`, cache validators, or authorization.

### Critical invariants

Validate semantic behavior independently of protocol version. Never forward HTTP/1.1 connection-specific fields into HTTP/2 or HTTP/3. Treat stream reset, connection failure, and response loss as evidence—not proof of whether an unsafe operation applied. Bound field sizes and decompressed metadata. Coordinate connection-level and stream-level flow control. Preserve authority and certificate checks when coalescing. Measure protocol version, stream outcomes, retries, and downstream latency separately.

### Common failures

Calling HTTP/2 “HTTP/1.1 with compression”; assuming multiplexing removes all blocking; parsing HTTP/1.1 framing inconsistently across proxies; assuming a reset means the origin did nothing; forwarding `Connection` fields; treating QUIC encryption as application authorization; unbounded concurrent streams; ignoring QPACK blocking; and tuning one connection benchmark as universal API capacity.

### Compact example

Ten independent GETs over one non-pipelined HTTP/1.1 connection serialize. HTTP/2 can multiplex them, but a lost TCP packet can delay bytes for every stream on that connection. HTTP/3 uses independent QUIC streams so loss on one stream need not block delivery on another, while all ten can still queue behind one database pool. Transport removes one blocking source, not the application bottleneck.

### Connections

Message, method, status, field, negotiation, caching, conditional, and idempotency semantics precede wire-version choice. Network engineering owns TCP, QUIC, TLS, congestion, and path behavior. API engineering owns how protocol behavior affects request boundaries, retries, limits, and observable contracts.

## Governing Question

When a service supports several HTTP versions, what must remain invariant at the API boundary, and what version-specific mechanisms must engineers account for when diagnosing latency, failures, and security?

## Why This Matters

HTTP versions are not three unrelated API styles. RFC 9110 deliberately separates shared semantics from version-specific messaging. This allows one resource and method contract to operate over HTTP/1.1, HTTP/2, or HTTP/3 while each version uses different framing and transport machinery.

Operational behavior nevertheless changes. HTTP/1.1 framing ambiguity can enable request smuggling. HTTP/2 multiplexing changes concurrency and flow control. HTTP/3 shifts stream delivery to QUIC, changing loss isolation, connection establishment, migration, and tooling. A design that checks only status and JSON can remain semantically correct yet fail under metadata limits, connection churn, stream cancellation, or retry ambiguity.

RFC 9112 specifies HTTP/1.1 messaging, RFC 9113 specifies HTTP/2, and RFC 9114 specifies HTTP/3. RFC 9110 remains the shared semantic authority. The chapter uses these standards rather than treating a framework or browser implementation as the protocol definition.

## Prerequisites and Retrieval

Retrieve byte streams, packets, requests and responses, methods, fields, framing, TLS, TCP ordering, congestion control, multiplexing, flow control, and ambiguous completion. Recall that an HTTP response is correlated with a request by version-specific mechanisms but retains common semantic meaning after decoding.

## Learning Objectives

By the end of this module, you should be able to:

1. separate semantic invariants from messaging and transport mechanisms;
2. trace message framing and request/response correlation in each version;
3. locate head-of-line blocking at connection, transport, stream, and application layers;
4. compare HPACK and QPACK at the level needed for safe API operation;
5. reason about flow control, cancellation, and failure scope;
6. identify cross-version translation and request-smuggling risks; and
7. design version-aware testing and observability without creating version-specific API meaning.

## Core Exposition

### One semantic layer, several mappings

Across versions, a request still has a method, target, fields, and optional content; a response still has a status, fields, and optional content. Safety, idempotency, conditional requests, caching, and representation meaning do not change merely because frames do. Version-specific specifications define how those elements are encoded, transmitted, correlated, limited, and failed.

The invariant is semantic equivalence, not wire equality. HTTP/1.1 field names can arrive with varied casing; HTTP/2 and HTTP/3 require lowercase field names in their mappings. HTTP/2 and HTTP/3 use pseudo-fields such as `:method` and `:authority` rather than an HTTP/1.1 request line and `Host` field. A gateway translating versions must reconstruct the same method, target URI, authority, and field semantics while rejecting forbidden combinations.

### HTTP/1.1 message delimitation

HTTP/1.1 sends textual start lines and field lines over an ordered byte stream. Message content length can be determined by method/status rules, `Content-Length`, chunked transfer coding, or connection closure. Recipients must apply the standardized precedence. If a front proxy and origin disagree about where one request ends, attacker-controlled bytes can be interpreted as a second request: request smuggling.

Persistent connections amortize setup cost. Without pipelining, requests on one connection proceed sequentially. Pipelining permits several requests before responses arrive, but responses must correspond in order, so a slow earlier response blocks delivery of later responses. Deployments often use several connections instead, trading extra handshakes and congestion state for concurrency.

Connection-specific fields such as `Connection` and fields nominated by it apply only to the current connection. An intermediary must remove them before forwarding. HTTP/2 and HTTP/3 prohibit connection-specific field usage because their stream mappings manage connections differently.

### HTTP/2 streams and frames

HTTP/2 uses a binary framing layer. One connection carries frames belonging to many streams. A stream has an identifier, state, and ordering; frames from different streams can interleave while frames within a stream preserve the required order. This reduces application-level serialization caused by one-request-at-a-time connections.

TCP still delivers one ordered byte stream. If a packet is lost, later TCP bytes cannot be delivered to the HTTP/2 implementation until recovery, even when those bytes contain frames for an unrelated stream. This is transport-layer head-of-line blocking across streams. It differs from HTTP/1.1 response-order blocking and from application queues.

HTTP/2 has connection and stream flow-control windows. A recipient grants credit for data it is prepared to receive. Failing to consume data or send window updates can stall a stream; exhausting connection credit can stall all data streams. Flow control protects memory but becomes a liveness and fairness concern when poorly implemented.

HPACK compresses repeated field values using static and dynamic tables. Compression reduces metadata overhead, but decoding state, size limits, sensitive-field handling, and compression attacks matter. A decompressed header list can be much larger than its encoded block. Enforce both encoded/protocol limits and application-level semantic limits.

### HTTP/3 over QUIC

HTTP/3 maps messages to QUIC streams. QUIC provides stream multiplexing, loss recovery, congestion control, and cryptographic protection. Loss in one QUIC stream does not inherently prevent delivery of data already available for another stream, reducing cross-stream transport head-of-line blocking compared with HTTP/2 over TCP.

QUIC connection-level congestion and resource limits still couple streams. A saturated path, exhausted server, blocked dependency, or shared application queue delays many requests. “No head-of-line blocking” is therefore too broad; HTTP/3 removes a specific transport ordering dependency, not every cause of waiting.

QPACK adapts field compression to QUIC stream independence. Encoder instructions and field blocks can arrive in different orders, so references to unavailable dynamic-table entries can block field decoding. QPACK includes mechanisms to bound this risk, but operators must still limit blocked streams and metadata. Compression efficiency and independent progress trade against one another.

QUIC supports connection IDs and can survive some network-path changes, subject to validation and policy. This does not make an authenticated application session transferable to an unauthorized actor. TLS-integrated transport security authenticates the peer and protects traffic according to the protocol; application identity, authorization, replay defenses, and tenant boundaries remain separate.

### Negotiation, fallback, and translation

Clients and servers negotiate protocol support through defined mechanisms such as TLS ALPN, prior knowledge, or upgrades where applicable. A failed HTTP/3 path can lead a client to use another supported version. An API must remain semantically coherent under fallback. It should not make a field required only because one version happens to expose it differently.

Gateways frequently terminate one version and originate another. That translation creates a security boundary. Normalize authority and target once, reject ambiguous framing, strip hop-by-hop fields, enforce field limits, map resets carefully, and preserve end-to-end fields. Differential parsing tests must include the gateway and origin together.

### Failure, cancellation, and retry evidence

HTTP/2 and HTTP/3 can reset one stream without closing the connection; both also have connection-level failures. A reset can occur before or after an application commits an unsafe effect. Some protocol error information can constrain retry reasoning, but clients must follow method idempotency, request replayability, and specified transport semantics rather than interpreting every reset as non-application.

Cancellation is a resource signal, not rollback. When a client resets a stream after its deadline, the server should stop optional work where possible, but an already committed transaction or dispatched external command may remain. Trace attempt identity and authoritative operation state independently of the transport stream.

<!-- bijux-verify: {"id":"blocking-scope-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"http1-delivery-blocked=3\nhttp2-tcp-loss-affected=3\nhttp3-stream-loss-affected=1\napplication-pool-affected=3\n","stderr":""}} -->
```python
streams = {1, 3, 5}
print(f"http1-delivery-blocked={len(streams)}")
print(f"http2-tcp-loss-affected={len(streams)}")
print("http3-stream-loss-affected=1")
print(f"application-pool-affected={len(streams)}")
```

This toy output compares stated failure scopes for three requests. It does not simulate TCP, QUIC, congestion control, packet loss, HTTP framing, scheduling, or a database pool.

## Definitions and Notation

Let $M=(control,fields,content)$ be an abstract HTTP message. For protocol version $v$, $encode_v$ maps $M$ to version-specific framing, and $decode_v$ reconstructs semantic components. Semantic preservation means $decode_v(encode_v(M))\equiv M$ under the specification's normalization rules, not byte equality.

A **connection** is a protocol relationship that can carry messages. A **stream** is an independently identified ordered sequence within a multiplexed connection. **Flow control** bounds how much data a sender may deliver without recipient credit. **Congestion control** bounds network injection based on path conditions. A **stream reset** terminates stream processing; a **connection error** affects the connection scope.

## Mechanisms, Invariants, or Proof Structure

Review a multi-version service in this order:

1. Define one version-independent API semantic contract.
2. Trace target, authority, fields, content length, and response correlation in each version.
3. Define translation and normalization at every intermediary boundary.
4. Bound streams, fields, decompressed metadata, body bytes, queues, and deadlines.
5. Trace flow-control and application backpressure together.
6. Inject stream reset, connection loss, packet loss, fallback, partial content, and response-loss cases.
7. Verify retry decisions against method and operation evidence.
8. Measure version, connection, stream, queue, origin, and dependency dimensions without high-cardinality leakage.

The **semantic-preservation invariant** requires equivalent API meaning across supported versions. The **framing-agreement invariant** requires every HTTP/1.1 recipient on a path to find the same message boundary. The **scope invariant** requires stream-local failures not to be promoted to connection-wide failure without cause. The **bounded-resource invariant** caps concurrency, flow-control credit, compression state, metadata, and queued work.

## Alternatives and Trade-Offs

**One connection versus several.** Multiplexing amortizes handshakes and shares congestion state, but one connection can become a failure or congestion scope. Several connections add overhead and can compete unfairly. Choose using measured path and workload behavior, not a universal connection count.

**End-to-end version versus gateway translation.** End-to-end support preserves transport features and clearer failure evidence. Terminating at an edge centralizes certificates, policy, and compatibility but adds translation, queueing, and observability boundaries. Either design must preserve semantics and authority.

**Large concurrency versus bounded admission.** More streams can hide latency and improve utilization, but unbounded work exhausts memory, downstream pools, and scheduling fairness. Stream capability is not application capacity; enforce admission at the constrained resource.

## Failure Modes and Misconceptions

HTTP/2 does not change REST semantics. HTTP/3 is not “HTTP over unreliable messages”; QUIC provides reliable ordered delivery within streams. QUIC stream independence does not eliminate congestion or application blocking. Binary framing is not inherently secure. TLS does not authorize resources. A stream reset is not transaction rollback. A protocol benchmark without loss, concurrency, payload, field size, and dependency behavior cannot establish production superiority.

## Worked Examples

### Example 1

`GET /orders/7` returns `404` over HTTP/1.1 and HTTP/3 for the same authoritative absence. Framing differs, but method and status meaning do not. If the API returns `200` only under one version, that is an implementation defect, not negotiation.

### Example 2

An HTTP/1.1 proxy accepts both conflicting `Content-Length` and `Transfer-Encoding` interpretations while the origin chooses differently. Extra bytes become another request at one hop. Reject the ambiguous message consistently. The conclusion is that framing disagreement creates a security boundary breach.

### Example 3

Three pipelined HTTP/1.1 requests have origin times 500 ms, 10 ms, and 10 ms. Responses remain ordered, so later completed responses wait behind the first. Multiple connections or multiplexing can remove this response-order dependency.

### Example 4

The same three requests use HTTP/2 streams. Frames can interleave, so the two fast streams can finish first under normal delivery. One lost TCP segment can nevertheless delay delivery of subsequent bytes for all streams until recovery. Multiplexing and transport ordering are separate layers.

### Example 5

Under HTTP/3, loss of data belonging to one stream delays that stream while another stream's available data can be delivered. All streams still slow when the path's congestion controller reduces sending. The conclusion is narrower cross-stream loss coupling, not independent networks.

### Example 6

A client stops reading a large HTTP/2 response. Its stream window closes. If the implementation also exhausts connection credit or fails to schedule updates fairly, unrelated streams stall. Flow-control tests must exercise connection and stream windows together.

### Example 7

A small encoded HPACK/QPACK block expands into a large header list. The edge enforces decoded-list and field-count limits before application allocation. Compression ratio does not excuse unbounded semantic metadata.

### Example 8

An edge receives HTTP/2 and forwards HTTP/1.1. It strips connection-specific fields, reconstructs one authority, emits unambiguous length framing, and rejects pseudo-field conflicts. Translation is an active security function, not a byte-copy operation.

### Example 9

A POST commits, then its HTTP/3 response stream resets. The client sees an ambiguous outcome. It queries the operation identity instead of assuming the stream reset rolled back work. Transport cancellation and application commit have different scopes.

### Example 10

HTTP/3 reduces network blocking, yet requests queue behind a database pool of ten connections. Increasing QUIC streams worsens queue time and memory. Admission control at the database-dependent operation improves latency. The bottleneck model must extend beyond HTTP.

## Cross-Program Connections

[Resources, Representations, and Messages](001-resources-representations-and-messages.md) supplies shared semantics, [Headers and Metadata](004-headers-and-metadata.md) supplies translation rules, and [Idempotency and Safety](008-idempotency-and-safety.md) bounds retry after transport failure. Network engineering owns TCP, UDP, QUIC, TLS, and congestion; systems engineering owns end-to-end bottleneck and failure-scope analysis.

## References

- Fielding, R., Nottingham, M., and Reschke, J. *HTTP Semantics*, RFC 9110, IETF Standards Track, June 2022. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9110.html
- Fielding, R., Nottingham, M., and Reschke, J. *HTTP/1.1*, RFC 9112, Internet Standard, June 2022. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9112.html
- Thomson, M., and Benfield, C. *HTTP/2*, RFC 9113, Internet Standard, June 2022. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9113.html
- Bishop, M. *HTTP/3*, RFC 9114, Standards Track, June 2022. Retrieved 2026-09-01. https://www.rfc-editor.org/rfc/rfc9114.html

## Exercises

### Exercise 1

Name three semantic properties that remain stable across HTTP versions and three mechanisms that change.

### Exercise 2

Trace where head-of-line blocking can occur for three requests under HTTP/1.1 pipelining, HTTP/2 with TCP loss, HTTP/3 with one-stream loss, and a shared database queue.

### Exercise 3

Design safety checks for an HTTP/2-to-HTTP/1.1 gateway, including authority, fields, framing, limits, and error mapping.

### Exercise 4

Compare one HTTP/2 connection carrying 100 streams with ten connections carrying ten streams each. Identify performance and failure trade-offs without choosing universally.

### Exercise 5

A POST response stream resets after the origin may have committed. Design a version-independent recovery contract and the evidence required for an automatic retry.

## Answers to the Exercises

### Answer 1

Method meaning, status meaning, and representation-field meaning remain stable; cache and conditional semantics do too. Message framing, stream multiplexing, field compression, transport, flow-control mechanisms, and failure scope change. A complete answer separates semantic contracts from how a version conveys and schedules them.

### Answer 2

HTTP/1.1 pipelined responses wait for an earlier response because delivery order is fixed. HTTP/2 interleaves streams, but TCP loss withholds later connection bytes from all streams until recovery. HTTP/3 loss on one QUIC stream need not withhold another stream's deliverable bytes, though congestion can slow the connection. In every version, all requests can queue behind the same database pool; transport improvements do not remove application contention.

### Answer 3

Validate pseudo-fields and construct exactly one method, target, scheme, and authority; reject conflicts. Remove prohibited connection-specific fields. Produce one unambiguous HTTP/1.1 message length and reject conflicting input rather than forwarding uncertainty. Bound decoded field bytes, count, body, streams, queue, and deadlines. Map stream errors without asserting rollback, preserve end-to-end fields, and test the edge and origin parsers differentially with adversarial messages.

### Answer 4

One connection amortizes setup and shares compression/congestion state, but connection failure, TCP loss, or connection-level flow control can affect all 100 streams. Ten connections increase handshake, memory, congestion competition, and scheduling complexity but reduce one-connection failure scope and may improve utilization on some paths. Choose through workload measurements including loss, fairness, origin limits, and downstream capacity.

### Answer 5

Use one logical-operation identifier whose status is queryable and whose fingerprint binds principal, target, method, content, and conditions. The origin records application state durably and returns the same operation reference across versions. Automatic retry is allowed only when method/operation semantics are idempotent, the request is replayable, the deadline remains, authorization is current, and status evidence does not already show a terminal result. A stream reset alone is insufficient evidence of non-application.
