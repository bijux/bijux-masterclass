# Worked Answers — Module 05: IP, Routing, Transport, and Sockets

These answers demonstrate reasoning. Equivalent answers are valid when they preserve the same mechanism and evidence boundary.

## Exercise 1 — Wildcard listener

`127.0.0.1` is IPv4 loopback only. `0.0.0.0` is the IPv4 wildcard for all local IPv4 addresses. `::1` is IPv6 loopback. `::` is the IPv6 wildcard and may or may not accept IPv4-mapped connections depending on socket configuration. Verify actual listeners and firewall policy; do not infer exposure from source code alone.

## Exercise 2 — Route get

It asks the kernel to resolve the specific destination through policy rules and route tables and reports selected source address, interface, and next hop. A more specific route or policy rule can override the default. Use the actual destination and, where relevant, source or mark context.

## Exercise 3 — TCP framing

TCP exposes an ordered byte stream, not records. Segmentation, buffering, congestion, and receiver timing determine read boundaries. The application protocol must define framing through length, delimiter, or structured protocol rules and loop until complete. One `send` does not create one peer `recv`.

## Exercise 4 — UDP trade-off

It needs identifiers, acknowledgements, retransmission timers, duplicate suppression, ordering or sequence handling, congestion behavior, fragmentation policy, and failure limits. At that point the design may resemble a transport protocol. Choose UDP because the application needs datagram semantics or an established UDP-based protocol, not because it seems faster.

## Exercise 5 — TIME_WAIT

TIME_WAIT is a normal TCP state that protects a recently closed connection tuple from delayed segments and supports reliable close. High counts may reflect connection churn. Investigate connection reuse, active closer, ephemeral port range, NAT state, and workload. A leak is an unintended resource retention, not every visible protocol state.

## Exercise 6 — Timeout phases

A connect timeout succeeded and is irrelevant after establishment. The client needs a response-header or read/idle deadline and usually an absolute operation deadline. The server may also need request and handler deadlines. Record which phase consumed time; one generic timeout obscures diagnosis.

## Exercise 7 — Loopback edge

It prevents packets from remote interfaces reaching the API listener and makes the proxy the intended network entry. It reduces exposure and simplifies trusted-proxy policy. Firewall rules still matter, and separate-host proxies require a private interface design. Loopback is an architectural choice, not universally correct.

## Exercise 8 — IPv6 evidence

Verify an AAAA or intended address, host IPv6 assignment, route, listener, firewall policy, TLS SAN/name, and successful client request over IPv6. A wildcard source line or provider checkbox is insufficient. Record whether IPv4 fallback masked an IPv6 failure.

## Exercise 9 — Listen backlog

It does not increase application processing capacity, repair slow handlers, remove file-descriptor limits, or bypass upstream SYN queue limits. It only influences queued connection handling within kernel constraints. Measure accept rate, connection states, drops, and application latency before changing it.

## Exercise 10 — NAT identity

Many users can share one translated address, and addresses can change or be spoofed through untrusted forwarding metadata. NAT conveys reachability, not user identity. Use authenticated application identity and authorization policy. Source address remains useful for network operations and abuse signals within its limits.

## Exercise 11 — Unix socket alternative

When both processes share one host, a Unix socket can avoid IP exposure and use filesystem permissions or peer credentials. It still needs path ownership, cleanup, backlog, timeout, and proxy support. TCP loopback may be preferable for portability, metrics, or future separation. Choose based on explicit constraints.

## Exercise 12 — Failure localization

Refused usually means the destination host actively rejected because no listener owns the tuple or policy returned a reset. First verify DNS/address, then `ip route get` from the client, then `ss -lntp` and firewall state on the destination. Packet capture can show SYN/RST. It differs from timeout, where packets may be dropped or the route fails silently.
