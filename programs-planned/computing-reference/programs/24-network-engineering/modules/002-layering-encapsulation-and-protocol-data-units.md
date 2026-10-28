---
module_id: NET-002
program: Network Engineering
level: 1
module_number: 2
title: Layering, Encapsulation, and Protocol Data Units
status: complete
last_verified: 2026-08-29
---

# Layering, Encapsulation, and Protocol Data Units

## One-Page Review

### Governing question

How can independently evolving network functions cooperate across heterogeneous systems, and how can an engineer trace exactly what each layer adds, consumes, forwards, or changes?

### Essential definitions

- A **layer** groups related communication functions behind a service boundary.
- A **protocol** defines messages, state, sequencing, error behavior, and interpretation between peer entities at a conceptual layer.
- A **service** is what one layer offers to the layer above; an **interface** is how a particular implementation exposes that service locally.
- A **service data unit (SDU)** is information passed down to a layer for carriage.
- A **protocol data unit (PDU)** is the complete unit a layer exchanges conceptually with its peer: its control information plus the layer's payload.
- **Encapsulation** constructs a lower-layer PDU by treating an upper-layer PDU as payload and adding the lower layer's header, trailer, or both.
- **Decapsulation** validates and interprets a received PDU, removes the current layer's control information, and passes the recovered payload upward.
- **Multiplexing** carries multiple upper protocols or conversations over one lower service; **demultiplexing** selects the intended next handler or endpoint.
- A **tunnel** treats a complete packet or frame from one context as payload inside another protocol, creating another layer instance rather than erasing the inner structure.

### Central model, mechanism, or theorem

For layer `i`, write

$P_i = H_i \parallel S_i \parallel T_i, \quad S_i=P_{i+1},$

where `H_i` and `T_i` are that layer's header and trailer and `P_{i+1}` is the upper-layer PDU carried as its SDU. The receiver reverses this nesting only after validating lengths, identifiers, integrity rules, and local policy. Encapsulation preserves an inner unit as bytes; it does not preserve every semantic guarantee across the path.

### Critical invariants

- Each field has one declared layer, byte order, length rule, and interpretation.
- A lower layer carries the complete upper PDU unless a specified transformation such as fragmentation or compression applies.
- Every demultiplexing identifier maps to an implemented and permitted next handler.
- Declared total lengths, header lengths, and actual captured boundaries agree.
- Each hop distinguishes end-to-end identifiers from next-hop identifiers.
- Decapsulation rejects truncation, impossible lengths, unsupported protocols, failed integrity checks, and forbidden nesting before unsafe use.
- Observability identifies the capture point and representation: application message, transport PDU, IP packet, link frame, or physical signal.

### Common failures

Frequent mistakes include calling every PDU a packet, treating OSI layer numbers as universal implementation facts, believing peer layers communicate without lower services, assuming routers remove all headers, confusing an IP destination with the next-hop link destination, counting overhead at inconsistent boundaries, ignoring tunnels and middleboxes, trusting a declared length before validating it, and treating successful decapsulation as proof that application data is authentic or meaningful.

### Compact example

An application message becomes the payload of a UDP datagram. The datagram becomes the payload of an IP packet. On an Ethernet link, that packet becomes the payload of a frame. A router validates and removes the incoming link framing, processes the IP packet, then creates new link framing for the next hop. The transport and application bytes usually remain encapsulated end to end, although fragmentation, translation, tunneling, security, or middlebox behavior can complicate the trace.

### Connections

[NET-001](001-network-requirements-reachability-capacity-delay-and-loss.md) defines the communication outcomes whose measurement boundaries must name a layer. [NET-003](../ROADMAP.md) moves below frames to bits, symbols, and encoding; [NET-006](../ROADMAP.md) develops framing. Ethernet, IP, transport, tunneling, security, and packet-tracing modules later instantiate this general model.

## Governing Question

A browser, transport implementation, router, network interface, and physical link solve different problems. Yet one application message must cross them all and remain interpretable at the destination. How should those responsibilities be divided so components can evolve independently, while leaving enough control information to deliver, validate, diagnose, and recover the data?

Layering answers by composing services. Encapsulation gives the composition a concrete wire representation. PDU analysis lets an engineer test whether the representation actually matches the intended protocols at a named observation point.

## Why This Matters

Layering is the vocabulary of network design and diagnosis. A link can be operational while IP has no route. IP can reach a host while a transport port is closed. A transport exchange can succeed while an application rejects authentication. Saying “the network works” hides the failing contract; naming the layer and PDU narrows the evidence.

The abstraction also enables heterogeneity. An IP packet can traverse Ethernet, Wi-Fi, optical transport, a point-to-point link, and tunnels without the application implementing each medium. Conversely, a link technology can carry several upper protocols. This many-above/many-below composition is a central reason internetworks can evolve.

But diagrams can become mythology. The ISO OSI model coordinates standards and vocabulary; its official description says it is not an implementation specification. The Internet suite commonly groups application, transport, internet, and link functions, and RFC 1122 says strict layering is an imperfect model for both protocol interaction and implementation. Engineers use layers to assign contracts and evidence, then inspect the real path.

## Prerequisites and Retrieval

From [NET-001](001-network-requirements-reachability-capacity-delay-and-loss.md), retrieve endpoint, path, packet population, layer-specific capacity, goodput, delay, and loss. You should understand byte strings, fields, lengths, checksums at a conceptual level, and finite-state processing.

Recall three separations:

- representation is not meaning;
- a local function call is not a peer-to-peer wire exchange;
- successful carriage is not end-to-end correctness.

## Learning Objectives

After completing this module, you should be able to:

- distinguish layer, protocol, service, interface, SDU, PDU, and payload;
- compare the OSI reference model with the Internet protocol suite without forcing a one-to-one mapping;
- trace encapsulation and decapsulation through application, transport, internet, and link contexts;
- explain multiplexing and demultiplexing identifiers at several layers;
- distinguish end-to-end and hop-by-hop headers, addresses, checks, and lifetimes;
- calculate encapsulation overhead and payload efficiency at a declared boundary;
- trace routing, tunneling, fragmentation, security, and middlebox effects on nested PDUs;
- identify malformed length, type, integrity, ordering, and nesting failures;
- select layer-specific captures and counters for diagnosis;
- bound the evidence needed before a layered protocol claim can support consequential deployment.

## Core Exposition

### Three relationships, not one stack

A layer participates in three different relationships. Vertically, it consumes the service below and offers a service above. Horizontally, a protocol describes conceptual interaction with a peer at the same layer. Locally, an implementation exposes concrete APIs, queues, buffers, callbacks, or shared structures.

The horizontal diagram is logical. A transport implementation does not send a segment directly through empty space to its peer. It gives bytes and metadata to the internet layer; that layer uses a link service; signals traverse media; the destination reverses the path. The peer protocol explains shared interpretation, while lower services provide actual carriage.

A service contract might promise delivery of best-effort datagrams to an addressed destination. The interface might be a kernel function, descriptor API, device ring, or message queue. Two systems can implement different local interfaces while exchanging conformant protocol units. Conversely, matching APIs do not establish wire interoperability.

### Reference models and real suites

The OSI Basic Reference Model identifies seven layers: physical, data link, network, transport, session, presentation, and application. It is valuable for locating functions and coordinating standards. The Internet suite in RFC 1122 describes application, transport, internet, and link layers. Its application protocols may contain internal sublayers, and implementations may share data structures or couple functions across conceptual boundaries.

Therefore, “TCP is layer 4” is useful within the OSI vocabulary, but it does not prove a seven-module implementation. “TLS is layer 6” is context-dependent shorthand: TLS operates above a reliable transport and below application semantics in many deployments, yet its integration, records, handshakes, and transports deserve their own precise description.

Layer numbers are not packet fields. A capture contains protocol headers whose specifications determine what follows. Diagnosis should say “IPv6 Next Header identifies TCP” or “EtherType identifies IPv6,” not merely “the layer above.”

### SDUs, PDUs, and recursive wrapping

Suppose an application produces message `M`. A transport entity accepts `M` as an SDU and creates transport PDU `P_T`. The internet layer accepts `P_T` and produces IP packet `P_I`. A link entity accepts `P_I` and creates frame `P_L`. Schematically:

$P_T=H_T\parallel M,\quad P_I=H_I\parallel P_T,\quad P_L=H_L\parallel P_I\parallel T_L.$

The same bytes have different roles at different boundaries. The transport PDU is an IP payload; the IP packet is a link payload. “Payload” therefore always means payload **of a named layer**.

Header, trailer, and PDU names depend on protocol. TCP specifications call their PDU a segment; UDP defines a user datagram; IP defines a datagram or packet; Ethernet supplies a frame. Application protocols use message, request, response, record, chunk, or other terms. Vocabulary is a clue, not proof: identify the actual format and context.

### Control information and demultiplexing

Headers carry control information needed at their scope. A link header can identify a local destination and upper protocol. An IP header carries internet-layer source/destination identifiers and a field such as IPv6 Next Header. A transport header can carry ports and conversation state. An application message may carry a method, resource, content type, length, request identifier, or authentication material.

At reception, demultiplexing uses these fields to select the next processor. EtherType can select an IP implementation. An IP protocol or Next Header value can select TCP or UDP. A destination port plus local address and protocol can help select a socket. Application fields select handlers within the service.

These are not interchangeable identities. A port is not a user. An IP address is not necessarily one host over time. A MAC address normally identifies a link-layer interface or group within a link context, not the final application. Authentication and authorization require their own evidence.

### Hop-by-hop and end-to-end scope

On a routed path, link framing is normally hop-specific. Host A frames an IP packet to the first-hop router's link address. The router removes and validates that frame, processes the IP header, chooses a next hop, and emits a new frame suitable for the outgoing link. The final IP destination remains the remote host under ordinary forwarding, while specified IP fields can change.

Transport and application units are designed principally for endpoints, but “unchanged end to end” is not a universal fact. Network address translation can rewrite address and transport fields. A proxy can terminate one transport connection and originate another. Security gateways can add or remove encapsulation. Fragmentation can split an IP packet. Offload can make a host capture differ from on-wire framing. State precisely which entity terminates, transforms, or forwards each protocol.

An integrity check also has scope. Ethernet's frame check sequence protects a received frame under its specified error model and is regenerated per link. An IP or transport checksum has different coverage. Cryptographic authentication can cover still another representation and set of peers. One passing check does not transfer the guarantees of another.

### Encapsulation overhead and limits

If original application data has length `L_0` and each layer adds `h_i` header bytes and `t_i` trailer bytes without other transformation, total length at the chosen boundary is

$L=L_0+\sum_i(h_i+t_i).$

Payload efficiency at that boundary is $\eta=L_0/L$. The ratio says nothing by itself about useful throughput: retransmissions, padding, inter-frame gaps, physical preambles, encryption records, acknowledgements, and competing traffic may sit inside or outside the count. Always publish the boundary.

Maximum transmission unit (MTU) is likewise scoped. A link MTU bounds the network-layer unit carried without link-specific fragmentation. Encapsulation consumes space within an outer path's limit. A tunnel that adds an outer IP header reduces room available for the inner packet unless the path supports a larger unit. Oversize behavior can include source fragmentation where specified, path-MTU adaptation, segmentation, drop, or an error signal.

Do not subtract memorized constants blindly. IPv4 headers can contain options; IPv6 can contain extension headers; TCP can contain options; link formats can add tags; security and tunnel headers vary. Derive the active header chain from configuration and captures.

### Tunnels are nested layers

A tunnel encapsulates a complete unit inside another protocol. An inner IP packet may become payload of an outer IP packet. The outer header routes between tunnel endpoints; after decapsulation, the inner header governs onward delivery. The path then contains two internet-layer instances with different address scopes and often different MTUs, policies, and observability.

Treating a tunnel as “just a link” can be useful at one abstraction, but diagnosis must recover the real nesting. A packet can be reachable between outer endpoints while inner routing fails. An outer security association can authenticate tunnel peers while the inner application still lacks identity. An inner time-to-live or hop limit is not necessarily processed by transit routers that see only the outer header.

### Fragmentation, segmentation, and aggregation

Encapsulation is not always one-to-one. A transport can segment a byte stream into several PDUs. An internet layer can fragment a packet under specified conditions. A link or hardware function can aggregate or segment units. The receiver may reassemble before exposing an upper PDU.

This changes evidence. Seeing one application write does not imply one TCP segment, one IP packet, or one frame. Seeing a “large packet” in a host capture can reflect offload rather than an on-wire frame. Packet counts at two layers need not match. Correlate identifiers, sequence ranges, fragment fields, timestamps, and capture location.

IPv6 provides a useful concrete case. RFC 8200 defines an IPv6 header followed by zero or more extension headers and an upper-layer payload. The Next Header chain drives processing. Extension-header order and fragmentation rules matter; a parser that assumes a fixed transport offset is not a conformant general parser.

### Layering and end-to-end responsibility

Layering supports modularity and reuse, but some properties require endpoint knowledge. The end-to-end argument observes that complete correctness for functions such as application data integrity may require the endpoints, even when lower-layer mechanisms provide valuable detection or performance improvement.

This is not an order to put everything in applications. Link retransmission can be effective over a lossy local medium. Transport reliability can serve many applications. Encryption at several scopes can address different threats. The argument asks whether a lower layer possesses enough information to complete the function and whether the endpoints must still verify it.

### Middleboxes and cross-layer reality

Firewalls, NATs, load balancers, proxies, performance optimizers, and security gateways may inspect or transform several layers. RFC 3234 catalogues how middleboxes complicate fate sharing, configuration, failure, and diagnosis. Encryption can deliberately hide upper headers and payloads from intermediaries, changing which policy mechanisms remain possible.

Cross-layer information can improve performance—an application can choose payload size using path information, or a radio stack can expose changing capacity. It can also create brittle coupling. A safe optimization has a defined interface, fallback when information is absent or stale, versioning, and evidence that correctness does not depend on an undocumented lower-layer accident.

### Defensive decapsulation

Decapsulation processes attacker-controlled bytes at trust boundaries. A safe parser establishes the available byte count before reading a field, validates header and total lengths for overflow and containment, checks protocol identifiers, enforces nesting and recursion limits, handles duplicate or reordered optional headers according to specification, validates integrity at the right stage, and rejects ambiguity.

Parsing success is not authorization. After structural validation, policy decides whether the protocol, endpoint, state transition, resource use, and application operation are permitted. Resource limits matter: a tiny outer message can trigger expensive reassembly, decompression, certificate work, or nested parsing.

### Layer-aware diagnosis

Trace from the requirement downward and evidence upward:

1. Did the application produce and accept the intended message?
2. Did the transport create, deliver, retransmit, reset, or reject its PDU?
3. Did the internet layer route the packet with expected addresses and size?
4. Did each link create and deliver a valid frame to the next hop?
5. Did the physical service carry decodable symbols?

A capture proves only what its point and tooling can observe. Host capture, switch mirror, router trace, hardware counters, and destination capture can disagree legitimately because encapsulation changes, offloads, drops, sampling, and clocks differ.

The following executable teaching model computes nested lengths and reverses them. It uses representative fixed overheads—8 transport bytes, 20 internet bytes, and 18 link header/trailer bytes—but implements no real UDP, IPv4, or Ethernet fields.

<!-- bijux-verify: {"id":"encapsulation-length-trace","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"application_pdu=14\ntransport_pdu=22\ninternet_pdu=42\nlink_pdu=60\npayload_recovered=True\napplication_goodput_ratio=0.233\n","stderr":""}} -->
```python
payload = b"temperature=21"
layers = [
    ("transport", 8),
    ("internet", 20),
    ("link", 18),
]

sizes = {"application": len(payload)}
encoded = payload
for name, overhead in layers:
    header = bytes([overhead]) * overhead
    encoded = header + encoded
    sizes[name] = len(encoded)

decoded = encoded
for _, overhead in reversed(layers):
    decoded = decoded[overhead:]

print(f"application_pdu={sizes['application']}")
print(f"transport_pdu={sizes['transport']}")
print(f"internet_pdu={sizes['internet']}")
print(f"link_pdu={sizes['link']}")
print(f"payload_recovered={decoded == payload}")
print(f"application_goodput_ratio={len(payload) / len(encoded):.3f}")
```

Passing this example proves six outputs for a prefix-and-strip Python model. It does not encode, parse, checksum, transmit, route, fragment, encrypt, authenticate, or authorize any real PDU. It does not model padding, preambles, inter-frame gaps, options, offload, corruption, concurrency, or adversarial lengths.

## Definitions and Notation

Let layers be ordered from lower `0` to upper `n`. Let `S_i` be the SDU offered to layer `i`, and `P_i` its PDU. With header `H_i` and optional trailer `T_i`:

$P_i=H_i\parallel S_i\parallel T_i,\qquad S_i=P_{i+1}.$

Concatenation $\parallel$ describes representation, not timing. A decoder `D_i` should either produce a validated upper unit and metadata or a typed rejection:

$D_i(P_i)\in\{(S_i,m_i),\operatorname{reject}(reason)\}.$

Required preconditions include `|P_i|≥|H_i|+|T_i|` and consistency between declared and available lengths. In variable formats, the parser must establish each boundary before following the next.

Define the header chain $C(P)=(p_0,p_1,\ldots,p_k)$ as the ordered protocol instances a particular observation can parse. A tunnel can yield repeated types, such as $(\text{Ethernet},\text{IPv6}_{outer},\text{IPv6}_{inner},\text{TCP},\text{application})$.

**Endpoint** is scoped to a protocol: a tunnel endpoint, transport endpoint, and application principal need not coincide. **Next hop** is the adjacent forwarding target in a given layer context. **Protocol overhead** is bytes or processing attributable to a named protocol at a named boundary. **Goodput** counts useful application data over time and must not be inferred from efficiency alone.

## Mechanisms, Invariants, or Proof Structure

Review an encapsulation design through six obligations.

1. **Grammar:** field order, width, byte order, optionality, alignment, length, integrity coverage, and next-protocol identification are unambiguous.
2. **Composition:** upper units fit the lower service, including MTU, fragmentation, ordering, loss, and lifetime assumptions.
3. **Demultiplexing:** identifiers select exactly the intended handler under current registration and policy.
4. **State:** legal message sequences, duplicates, retransmissions, reassembly, timeout, and teardown are defined.
5. **Trust:** structural validation precedes allocation and use; authentication and authorization follow the correct representation.
6. **Evidence:** reference vectors, negative parses, captures, counters, conformance tests, state properties, resource tests, and operational traces support bounded claims.

A structural round-trip property is

`D_i(E_i(S,m))=(S,m')`

for legal `S` and metadata `m`, where `m'` contains the promised preserved interpretation. This property needs caveats: checksums may be generated, padding inserted, fields normalized, encryption randomized, or metadata consumed. State the equivalence relation instead of requiring byte equality blindly.

For a forwarding hop, a useful invariant is that removal of incoming link PDU `P_{L,a}` yields a valid network PDU `P_N`, and construction of outgoing `P_{L,b}` carries the permitted transformed network PDU `P_N'`. The proof must account for specified mutable fields, MTU behavior, policy, and errors. It does not imply end-to-end delivery.

## Alternatives and Trade-Offs

**Strict layering versus integrated implementation.** Strict boundaries improve modularity, substitution, and review. Shared buffers, offload, and fused processing can reduce copies and latency. An integrated implementation should preserve conceptual contracts and observability even when code modules do not mirror the diagram.

**Rich lower services versus simple datagrams.** Reliability, ordering, security, or reservation below can help many consumers. A narrower service supports more heterogeneous uses and preserves endpoint choice. Duplicated mechanisms can waste work, but mechanisms at different scopes may address different faults.

**Header clarity versus compact encoding.** Fixed, explicit fields simplify parsing and hardware. Variable-length or compressed headers reduce bytes but increase state, context, and error sensitivity. Evaluate bandwidth, processing, loss recovery, evolvability, and attack surface.

**Transparent middlebox versus explicit endpoint.** Transparent devices ease deployment but create hidden state and ambiguous failure. Explicit proxies and gateways can negotiate capabilities and expose identity while requiring application integration.

**Tunneling versus native integration.** Tunnels deploy overlays across an existing network and separate address domains. They add overhead, MTU complexity, nested policy, and another failure surface. Native support can be efficient but slower to deploy and harder to isolate organizationally.

**Deep inspection versus encrypted payloads.** Inspection can enforce policy and diagnose known protocols. End-to-end encryption protects content and reduces intermediary dependence. Designs must decide which metadata remains visible, where trust terminates, and how endpoints prove policy-relevant facts.

**Layered counters versus end-to-end outcomes.** Per-layer counters localize loss and errors. Only endpoint/application evidence establishes the intended outcome. Operate both and correlate them rather than choosing one.

## Failure Modes and Misconceptions

1. **Every network uses seven implementation layers.** OSI is a reference model; real suites and implementations combine and split functions.
2. **Peer layers communicate directly.** Their interaction is logical and depends on lower-layer services.
3. **Payload means application data.** An IP payload may be a complete transport PDU; payload is layer-relative.
4. **A router strips the packet to application bytes.** Ordinary forwarding replaces link encapsulation and processes the network header without terminating transport.
5. **The destination IP and destination MAC identify the same endpoint.** Across a routed link, the MAC can name a next hop while IP names a remote destination.
6. **One application write creates one frame.** segmentation, fragmentation, aggregation, buffering, and offload break that assumption.
7. **Header overhead is a universal constant.** Options, extensions, tags, security, tunnels, padding, and measurement boundary vary it.
8. **A checksum means authentic.** Many checksums detect accidental errors and provide no cryptographic sender authentication.
9. **Decapsulation success means authorized.** Syntax and integrity are distinct from policy and application semantics.
10. **A tunnel removes the inner network layer.** It adds an outer context and later reveals the inner one.
11. **Encryption removes layering.** It creates protected records or packets and changes visibility; lower encapsulation remains.
12. **A host capture is the wire.** Offload and capture placement can show pre-segmented or post-decapsulated representations.
13. **Cross-layer access is always bad.** Explicit, versioned information can help; hidden coupling without fallback is the durable failure.

## Worked Examples

### Example 1

**Question:** Is an HTTP request itself a TCP segment?

**Reasoning:** HTTP defines application messages. A byte-stream transport can split one request across segments or combine bytes from several writes.

**Conclusion:** The request is application-layer data carried by transport; message and segment boundaries need not coincide.

### Example 2

**Question:** Host A sends an IP packet through router R to host B. Which link destination does A use?

**Reasoning:** On A's local link, the frame normally targets R's next-hop link address while the IP header targets B.

**Conclusion:** Link addressing is hop-scoped; IP addressing supplies the routed destination context.

### Example 3

**Question:** A 1,000-byte application PDU gains 40 transport/internet bytes and 18 link bytes. What is efficiency at the stated link-PDU boundary?

**Reasoning:** Total is 1,058 bytes, so $\eta=1000/1058≈0.945$.

**Conclusion:** Application-byte efficiency is about 94.5% for that one unit and boundary, excluding all unlisted overhead and loss.

### Example 4

**Question:** A capture labels an Ethernet frame, IPv6 packet, TCP segment, and TLS record. Which is payload?

**Reasoning:** Each upper unit is payload of the immediately lower protocol. TLS data is TCP payload; the TCP segment is IPv6 payload; the IPv6 packet is Ethernet payload.

**Conclusion:** A trace should report the complete header chain rather than one unqualified payload.

### Example 5

**Question:** What changes when a router forwards an ordinary packet between two Ethernet links?

**Reasoning:** It validates/removes the incoming frame, processes specified IP fields and policy, chooses an outgoing interface/next hop, and creates a new frame with new link addresses and integrity data.

**Conclusion:** Link PDU lifetime is one hop; the processed IP unit continues toward its destination.

### Example 6

**Question:** Why can an inner packet of acceptable size fail after a tunnel is enabled?

**Reasoning:** The outer headers consume path MTU. If adaptation, segmentation, or fragmentation behavior is absent or blocked, the larger outer packet can be dropped.

**Conclusion:** Tunnel design must budget overhead and verify path-MTU signaling and failure behavior.

### Example 7

**Question:** May a parser allocate the declared payload length immediately after reading it?

**Reasoning:** The field may exceed available bytes, overflow arithmetic, violate protocol maximums, or trigger resource exhaustion.

**Conclusion:** Validate containment, limits, state, and policy before allocation or recursive parsing.

### Example 8

**Question:** Eight independent bit captures reconstruct a control byte. Is the byte coherent?

**Reasoning:** If bits cross or change independently without a protocol snapshot, the receiver can assemble a value never sent together.

**Conclusion:** Framing and protocol state must define atomicity or versioning; physical delivery of bits alone is insufficient.

### Example 9

**Question:** A firewall permits a valid TCP header. Has it authorized an application transaction?

**Reasoning:** Transport structure and connection state do not establish application principal, resource, method, or business policy. Encryption may hide those facts.

**Conclusion:** Enforcement claims must name visible fields, trust termination, layer, and residual endpoint authorization.

### Example 10

**Question:** A medical telemetry gateway successfully decapsulates sensor messages. Does that prove clinical correctness?

**Reasoning:** Structural success does not prove sensor identity, calibration, patient association, units, freshness, completeness, alarm timing, or safe response. Tunnels and retries may duplicate or delay valid messages.

**Conclusion:** Named clinical, biomedical, security, network, and safety authorities must review the full claim and deployed evidence. This chapter makes no certification or external-review claim.

## Cross-Program Connections

[Operating Systems](../../22-operating-systems/ROADMAP.md) owns socket, buffer, offload, and kernel-stack implementation. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns DMA, device queues, checksumming, and packet-processing hardware. [API and Service Engineering](../../28-api-and-service-engineering/ROADMAP.md) owns application protocol and service semantics above network carriage.

[Security Engineering](../../25-security-engineering/ROADMAP.md) owns threat models, cryptographic protection, parser hardening, authorization, and middlebox trust. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) reasons about message identity, ordering, duplication, loss, and partial failure above network PDUs.

[Platform Engineering](../../29-platform-engineering/ROADMAP.md) and [Cloud Engineering](../../30-cloud-and-infrastructure-engineering/ROADMAP.md) build overlays, gateways, load balancers, and policy layers. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) connects layered interface evidence to end-to-end outcomes, hazards, validation, and lifecycle ownership.

## References

- ISO/IEC, [*ISO/IEC 7498-1:1994 — Open Systems Interconnection Basic Reference Model: The Basic Model*](https://www.iso.org/standard/20269.html), official current record checked 2026-08-29. Reference vocabulary and layered standards framework; explicitly not an implementation specification.
- Robert Braden, ed., [*RFC 1122 — Requirements for Internet Hosts: Communication Layers*](https://www.rfc-editor.org/info/rfc1122/), Internet Standard STD 3, 1989, current RFC Editor record checked 2026-08-29. Internet application, transport, internet, and link model; PDU terminology and limits of strict layering.
- Brian Carpenter, ed., [*RFC 1958 — Architectural Principles of the Internet*](https://www.rfc-editor.org/info/rfc1958/), IAB Informational, 1996. Modularity, internet-layer independence, end-to-end responsibility, simplicity, and evolvability.
- Steve Deering and Bob Hinden, [*RFC 8200 — Internet Protocol, Version 6 (IPv6) Specification*](https://www.rfc-editor.org/info/rfc8200/), Internet Standard STD 86, 2017. Primary IPv6 packet, payload-length, Next Header, extension-header, and fragmentation rules.
- Wesley Eddy, ed., [*RFC 9293 — Transmission Control Protocol (TCP)*](https://www.rfc-editor.org/info/rfc9293/), Internet Standard STD 7, 2022. Current consolidated TCP segment format, processing, connection state, and interface requirements.
- Charles Hornig, [*RFC 894 — A Standard for the Transmission of IP Datagrams over Ethernet Networks*](https://www.rfc-editor.org/info/rfc894/), Internet Standard STD 41, 1984. Primary IP-over-Ethernet encapsulation specification.
- Brian Carpenter and Scott Brim, [*RFC 3234 — Middleboxes: Taxonomy and Issues*](https://www.rfc-editor.org/info/rfc3234/), IETF Informational, 2002. Layer-crossing intermediaries, hidden state, fate sharing, configuration, and diagnostic consequences.
- Jerome H. Saltzer, David P. Reed, and David D. Clark, [*End-to-End Arguments in System Design*](https://dl.acm.org/doi/10.1145/357401.357402), `ACM Transactions on Computer Systems` 2(4), 1984. Primary statement of endpoint knowledge and incomplete lower-layer functions.

## Exercises

### Exercise 1

For a 600-byte application PDU carried with 8 transport-header bytes, 40 internet-header bytes, 14 link-header bytes, and 4 link-trailer bytes, draw the nesting, compute every PDU length, and calculate efficiency at the link-PDU boundary. State at least five excluded overheads or transformations.

### Exercise 2

Trace one IP packet from host A through two routers to host B. Identify which source/destination identifiers and integrity fields are hop-scoped, which are normally end-to-end, which IP fields can change, and what evidence at four capture points would correlate the packet.

### Exercise 3

An outer IPv6 tunnel adds 40 bytes to inner packets on a path with a 1,500-byte MTU. Determine the largest inner packet that fits under the simplified assumptions. Then explain why deploying that constant alone is unsafe.

### Exercise 4

Design a defensive decoder for a nested length-prefixed protocol. State ordering of bounds checks, type dispatch, integrity validation, authentication, authorization, decompression, allocation, recursion limits, logging, and error responses.

### Exercise 5

An autonomous rail-control network uses Ethernet, IP, transport security, and application messages across redundant tunnels. Build an assurance plan that separates per-layer conformance, end-to-end command integrity, timing, duplication/order, failover, cybersecurity, physical process safety, and named human review.

## Answers to the Exercises

### Answer 1

Application length is 600 bytes. Transport PDU is `8+600=608`. Internet PDU is `40+608=648`. Link PDU is `14+648+4=666`. Efficiency at exactly that boundary is `600/666≈0.9009`, or about 90.1%.

The calculation excludes possible application framing, transport options, IP extension headers, VLAN or other link tags, link padding, preamble, start delimiter, inter-frame gap, physical encoding, security records, tunnels, acknowledgements, retransmissions, segmentation, fragmentation, and capture offload. Any five show why the published boundary and active header chain matter.

### Answer 2

At A, the frame source is A's outgoing interface and frame destination is router 1's next-hop interface; the IP source/destination normally identify A and B. Router 1 removes that frame, processes the IP packet, decrements Hop Limit or TTL and updates any required mutable integrity field, then frames toward router 2. Router 2 repeats this toward B. Each frame's addresses and frame integrity are hop-scoped. Transport ports, sequence information, and application bytes are normally endpoint-scoped, subject to NAT, proxies, fragmentation, security, or other specified transformations.

Capture at A egress, both router forwarding boundaries, and B ingress. Correlate IP version, source/destination, protocol/Next Header chain, stable identification or transport sequence ranges where available, payload length, immutable header fields, bounded timestamps, and payload digest only where lawful and visible. Account for TTL/Hop Limit, checksums, link addresses, fragmentation, offload, translation, sampling, and clock uncertainty. No single field is a universal correlation identity.

### Answer 3

Under only the stated arithmetic, the largest inner packet is `1500-40=1460` bytes. Deployment cannot rely on that constant alone because other outer extension, security, or link headers may apply; the stated MTU may differ by segment or direction; ECMP paths can differ; inner and outer fragmentation rules differ; path-MTU signals may be filtered; endpoints can cache stale values; offload can obscure captures; and nested tunnels can be added later.

Specify the exact inner/outer formats, effective MTU at every relevant boundary, discovery and cache behavior, maximum segment sizing, fragmentation policy, error signaling, black-hole detection, fallback, and monitoring. Test boundary sizes, route changes, failover, asymmetric paths, filtered errors, and nested encapsulation.

### Answer 4

Read only the fixed minimum prefix after proving it is available. Decode lengths with checked arithmetic; reject values below the header, above available bytes, above protocol maximums, or inconsistent with parent bounds. Validate the type before dispatch and require a registered, permitted handler. Establish integrity coverage and verify it before trusting covered content, while avoiding detailed unauthenticated error or timing oracles.

Apply authentication to the exact canonical representation and peer scope the protocol defines, then authorization to the principal, operation, object, state, and resource budget. Decompress only after validating algorithm and bounded compressed size, with strict output, ratio, time, memory, and nesting limits. Allocate incrementally within quotas rather than trusting declared size. Track recursion depth, total expanded bytes, object count, duplicate fields, state transitions, and timeout. Log typed reasons without secrets, rate-limit responses, and make failures release partial state. Fuzzing and reference vectors supplement—but do not replace—grammar, state, resource, and security review.

### Answer 5

Inventory every protocol instance and termination point: physical/link paths, VLAN or equivalent domains, IP routes, tunnel endpoints, transport-security peers, application principals, command identifiers, and actuator interfaces. Per-layer evidence includes conformance vectors, negative frames/packets, MTU and fragmentation behavior, routing and failover, checksum/integrity scope, tunnel replay and key behavior, parser hardening, constraints, captures, counters, and versioned configuration.

End-to-end evidence binds authenticated sender, vehicle/track context, command type, parameters, units, sequence, freshness, expiry, acknowledgement, execution feedback, and safe rejection. Model duplication, reordering, loss, stale replay, conflicting paths, partition, delayed failover, asymmetric recovery, clock loss, key rollover, power restart, common-cause link or tunnel failure, overload, and malicious inputs. Measure deadline distributions and worst-case recovery against physical braking and separation requirements; test independent safe-state mechanisms when communications cannot be trusted.

Named network, embedded/control, rail-signaling, rolling-stock, physical-safety, real-time, cryptography, cybersecurity, verification, operations, maintenance, human-factors, quality/configuration, and independent functional-safety authorities review their evidence. The responsible operator and authorized assessor own residual-risk acceptance under applicable standards. Passing PDU decoders, tunnel failover tests, or internal course review does not certify the railway system, and no external review is claimed.
