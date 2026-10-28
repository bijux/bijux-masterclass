# Module 05 — IP, Routing, Transport, and Sockets

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.

> **Central question:** How does a byte leave one process and reach the intended process across interfaces, routes, and transport state?

## Where this module fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary. The capstone increment is:

> **Define Atlas listening addresses, route assumptions, port ownership, timeouts, and dual-stack behavior; prove them with socket and packet-path evidence.**

This result is required before the next module can build on it honestly.

## Learning outcomes

- Read addresses, prefixes, interfaces, routes, and neighbor state for IPv4 and IPv6.
- Trace a TCP connection through SYN, established state, shutdown, and TIME_WAIT.
- Distinguish TCP streams, UDP datagrams, Unix-domain sockets, and their failure models.
- Choose loopback, wildcard, private, and public bindings deliberately.
- Use connect, read, write, and idle timeouts as separate controls.
- Diagnose listening, routing, reachability, and application failures without guessing.

## Capstone increment

Define Atlas listening addresses, route assumptions, port ownership, timeouts, and dual-stack behavior; prove them with socket and packet-path evidence.

## Start with layers, but debug the actual path

Layer models are useful vocabularies, not packet elevators. On a typical host, an application uses a socket; the kernel selects a local address and route; neighbor discovery resolves a next-hop link address where needed; a network interface transmits frames; routers forward packets; and the remote host demultiplexes transport state to a socket.

At each point ask: which namespace, table, interface, route, policy, and process owns the decision?

## Addresses and prefixes describe membership and reachability

An IPv4 or IPv6 address is assigned to an interface within a namespace. A prefix length describes the network portion used for route matching, not a security boundary. `127.0.0.0/8` is loopback in IPv4. `::1` is IPv6 loopback. RFC 1918 IPv4 and unique-local IPv6 ranges are not internet-routable by ordinary policy, but “private” does not mean trusted.

A wildcard listener such as `0.0.0.0:18080` accepts connections addressed to any local IPv4 interface unless another policy blocks them. `127.0.0.1:18080` accepts only loopback traffic in that network namespace. On some systems an IPv6 wildcard socket may also accept IPv4-mapped connections depending on socket options.

Atlas binds the internal API to loopback. The edge binds the externally intended port. That is defense in depth with firewall policy, not a replacement for it.

## Route selection is longest-prefix matching plus policy

A routing table maps destination prefixes to next hops, interfaces, and attributes. The kernel generally chooses the most specific matching route, then applies metrics and policy rules. A default route is simply a low-specificity route used when no more specific entry matches.

Inspect:

```bash
ip address show
ip route show table all
ip rule show
ip route get 198.51.100.10
ip -6 route get 2001:db8::10
```

`ip route get` is especially useful because it asks the kernel how it would route one destination, including selected source address.

## Neighbor discovery connects network and link layers

IPv4 commonly uses ARP to map a local next-hop IP address to a link-layer address. IPv6 uses Neighbor Discovery over ICMPv6. If the destination is not on-link, the host resolves the next hop, usually a router, rather than the final destination.

A failed neighbor entry, wrong prefix, or missing route can all appear as “connection timed out.” Use `ip neigh`, packet capture, and route evidence before blaming the application.

## TCP is a state machine and a byte stream

TCP provides a reliable ordered byte stream between endpoint pairs. It does not preserve application message boundaries. `send` of one JSON document and another can be received as one read, several reads, or any segmentation consistent with the byte stream. HTTP defines its own framing above TCP.

A server creates a socket, binds an address, listens with a backlog, and accepts established connections. The listen backlog is not an infinite request queue. It interacts with handshake queues, kernel limits, and application accept rate.

TCP shutdown is directional. A peer can close its sending direction while still receiving. Abrupt reset differs from orderly FIN. `TIME_WAIT` protects the connection tuple from delayed segments after an active close; it is not automatically a leak.

Inspect:

```bash
ss -lntp
ss -tan state established
ss -tan state time-wait
```

## UDP preserves datagrams but not delivery

UDP sends independent datagrams. It does not provide connection establishment, retransmission, ordering, duplicate suppression, or congestion-aware reliable delivery. Application protocols must define what they need.

DNS often uses UDP for ordinary queries and TCP when required by response size or protocol behavior. Treating UDP as “faster TCP” produces broken retry and amplification assumptions.

## Unix-domain sockets are still sockets

A Unix-domain socket addresses a filesystem or abstract-namespace endpoint on one host. It can carry stream or datagram semantics and may support peer-credential inspection. Filesystem socket paths have ownership and mode policy; removing the pathname does not necessarily terminate existing connections.

Atlas uses TCP loopback because later proxy and cloud mappings need explicit address and port behavior. A Unix socket would be a defensible alternative for one-host deployments if proxy support and permission policy were defined.

## Timeouts belong to different phases

A single “timeout=30” hides multiple boundaries:

- DNS resolution deadline;
- TCP connect deadline;
- TLS handshake deadline;
- request-write deadline;
- response-header deadline;
- body-read or idle deadline;
- whole-operation deadline.

A connect timeout does not stop a peer that accepts and never responds. An idle timeout is not the same as an absolute operation deadline. Course 4 of API Engineering explores these at the service level; here the focus is their socket and intermediary foundation.

## Worked investigation: port is listening but unreachable

`ss -lntp` shows Atlas on `127.0.0.1:18080`. A remote client cannot connect. That is expected, not a firewall bug: the socket is not bound to the host's remote interface address.

If the edge should reach it on the same host, loopback is correct. If a separate proxy VM must reach it, the architecture must choose a private interface binding and firewall source policy. Changing to `0.0.0.0` without the second decision creates accidental exposure.

A disciplined path:

1. Resolve the client name to an address.
2. Determine the client route and source address.
3. Verify packets reach the destination interface.
4. Verify host policy accepts them.
5. Verify a listener owns the destination tuple.
6. Verify the application accepts and responds.

## Dual-stack design is explicit

Do not test only IPv4 and claim “networking works.” Record whether the endpoint has A and AAAA records, whether the host has usable IPv6 routes, whether the service listens on IPv6, and how clients fall back between address families.

IPv6 is not “IPv4 with longer addresses.” Neighbor discovery, link-local addressing, extension headers, and policy details differ. The capstone considers both families but its dependency-light tour uses loopback to remain portable.

## Network evidence for Atlas

The module checkpoint retains:

- listener table with owning PIDs;
- address and route tables;
- one successful loopback connection;
- one intentionally failed binding or route case;
- timeout classification;
- the final network plan naming public, private, loopback, management, and egress paths.

## Atlas implementation bridge

The API listens only on loopback; the edge owns external exposure. During the tour, inspect `ss -lntp` and use `ip route get` for the client path. The dependency-light tour uses ephemeral ports, while the deployment profile uses fixed ports.

Run the network-namespace lab only with explicit opt-in inside a disposable VM. It creates two namespaces and a veth pair, proves a route, and removes them through a trap.

## Design review prompts

- Which listener should be reachable from another host?
- What source address does the selected route use?
- Which timeout covers a peer that accepts and never responds?
- Is IPv6 behavior tested or assumed?
- Which evidence separates firewall rejection from missing listener?

## Boundary case: local success, remote failure

A local request can bypass routing, firewall, NAT, and external TLS layers. `curl localhost` proves the application on one network namespace, not the public path. Conversely, a public request can succeed through a load balancer while direct host diagnostics fail because direct access is intentionally blocked.

Build a path matrix: same-process, same-host, same-subnet, cross-zone, internet, and management. Each row has different routes and policy.

## Boundary case: source address selection

A multihomed host can have several valid source addresses. Route selection, policy rules, and application binding influence which is used. Remote access controls may fail because the selected source is not the one assumed in the design. `ip route get` reveals the kernel's choice for a destination; binding a client socket can alter it.

## Connection worksheet

```text
client namespace and identity:
resolved destination addresses:
selected source address:
route and next hop:
firewall/NAT transitions:
listener tuple and owning process:
transport deadlines:
application protocol and framing:
expected close behavior:
```

Use the worksheet for both successful and failed cases; the difference localizes the fault.

## Field method: diagnose the path from the nearest owned layer outward

Network diagnosis becomes faster when each observation answers one layer and you stop as soon as the failure is located. For a client reaching Atlas:

1. Does the server process own a listening socket on the expected address family, address, and port?
2. Does the host route the client's source and the return path through the intended interface?
3. Does neighbor discovery or the next hop resolve?
4. Does a TCP handshake complete?
5. Does the application read and respond before its deadline?
6. Does a proxy, firewall, NAT device, or load balancer transform the path?

Use `ss -lntp` for listener ownership, `ip -br address` for interface state, `ip route get <destination>` for route choice, and `tcpdump` only with a bounded filter and explicit privacy boundary. `curl` proves an application exchange but cannot by itself identify where a failed handshake was dropped.

TCP is a byte stream. One `send` does not imply one `recv`, and message framing belongs to the application protocol. A successful `connect` proves that the handshake completed, not that the remote application is ready or authorized. Half-close, resets, retransmissions, keepalives, and idle timeouts affect different phases. TIME_WAIT is a correctness mechanism that prevents delayed segments from contaminating a new connection; treating every TIME_WAIT socket as a leak leads to unsafe tuning.

Backlogs are also layered. The kernel has queues for incomplete and completed handshakes; the server runtime has an accept loop; the application may have worker or request queues. Raising one backlog can only move pressure to the next queue. Later performance modules quantify this, but Course 1 requires you to name the queue whose growth you are observing.

Dual-stack behavior must be tested, not inferred from one wildcard bind. Depending on platform and socket options, an IPv6 wildcard listener may or may not accept IPv4-mapped connections. Atlas declares loopback listeners and tests both families where available. Administrative listeners remain loopback-only unless an explicit management network and authorization model justify exposure.


## Standards and reference discipline

| Claim or rule | Category | Decisive evidence |
|---|---|---|
| TCP is an ordered byte stream and does not preserve application message boundaries. | RFC 9293 | socket experiment with segmented reads |
| Route selection uses destination-prefix and policy information, not application intent. | Linux/IP model | `ip route get` |
| Loopback and wildcard bindings create materially different exposure. | socket API and host policy | `ss -lntp` plus remote/loopback tests |

A reference implementation may add behavior beyond a standard. A course policy may intentionally narrow legal behavior. Keep those claims separate when you write a runbook or defend a design.

## Failure patterns to recognize

### Wildcard convenience

Binding every interface to make local testing easier can expose an internal endpoint.

### Ping-driven diagnosis

ICMP reachability does not prove a TCP listener, firewall policy, TLS handshake, or application response.

### One timeout

A single timeout value obscures which phase consumed the budget and which retry is safe.


## Module synthesis

Return to the central question: **How does a byte leave one process and reach the intended process across interfaces, routes, and transport state?**

A complete answer names the owner of the relevant state, the transition that changes it, the failure boundary, and the observation that would falsify the claim. The capstone is ready to progress only when the new mechanism works and the planted defect—**An administrative endpoint binds to `0.0.0.0` because the developer confused “reachable by the proxy” with “reachable by every interface.”**—fails for the predicted reason.

## Continue

Module 06 gives those addresses stable names and authenticated transport.

## Module route

1. [Complete the exercises](exercises.md) before viewing solutions.
2. [Compare with the worked answers](exercise-answers.md).
3. [Run the controlled lab](lab.md).
4. [Retain the checkpoint evidence](checkpoint.md).
