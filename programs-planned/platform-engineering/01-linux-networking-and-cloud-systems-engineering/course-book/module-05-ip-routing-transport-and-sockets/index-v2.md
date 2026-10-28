# Module 05 — IP, Routing, Transport, and Sockets

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.
> **Central question:** How does a byte leave one process and reach the intended process across interfaces, routes, and transport state?

---

## Where This Module Fits

Atlas begins this module with every guarantee established earlier in the course (identity, resources, and storage). Now, we must connect our services. The new responsibility is not a new tool; it is a stronger boundary around network communication.

The capstone increment for this module is:

> **Define Atlas listening addresses, route assumptions, port ownership, timeouts, and dual-stack behavior; prove them with socket and packet-path evidence.**

This result is required before the next module can build on it honestly. Before configuring cloud load balancers or service meshes, you must understand how a simple network socket works on a single host.

---

## Learning Outcomes

By the end of this module, you will be able to:

* **Read and understand** IP addresses, prefixes, interfaces, routes, and neighbor state for both IPv4 and IPv6.
* **Trace a TCP connection** through its lifecycle: SYN (handshake), established state, shutdown, and `TIME_WAIT`.
* **Distinguish** between TCP streams, UDP datagrams, Unix-domain sockets, and their unique failure models.
* **Choose** deliberately between loopback, wildcard, private, and public IP bindings.
* **Configure** connection, read, write, and idle timeouts as separate, precise controls.
* **Diagnose** listening, routing, reachability, and application failures systematically without guessing.

---

## 1. Start With Layers, But Debug the Actual Path

> **Concept Refresher: The Network Stack**
> Networking is traditionally taught using the OSI model (Layer 3 = IP, Layer 4 = TCP/UDP, Layer 7 = HTTP).

While layered models give us a good vocabulary, they are not magical elevators that seamlessly carry data. When you debug, you must look at the actual path:
An application opens a **socket** ➔ the kernel selects a **local address and route** ➔ **neighbor discovery** finds the physical hardware (MAC address) ➔ the **network interface** transmits the frame ➔ **routers** forward the packet ➔ the remote host's kernel passes the data to the destination **socket**.

At every point, if something breaks, you must ask: *Which table, route, policy, or process owns this specific decision?*

---

## 2. Addresses and Prefixes: Membership and Reachability

> **Concept Refresher: IPs and Bindings**
> * **Loopback (`127.0.0.1` or `::1`):** The "localhost" address. Traffic never leaves the machine.
> * **Wildcard (`0.0.0.0` or `::`):** Means "listen on ALL available network interfaces."
> * **Prefixes (e.g., `/24` or `/8`):** Defines the "subnet" or network portion of the address, used by routers to group devices. It is a routing tool, not a security boundary.
> 
> 

A common developer mistake is binding a private internal service to `0.0.0.0:18080` for "convenience." This exposes the port to the entire local network (and potentially the internet) unless a firewall blocks it.

Atlas binds its internal API exclusively to loopback (`127.0.0.1`). Only the edge service (which is meant to face the outside) binds to an external port. This is defense-in-depth.

---

## 3. Route Selection is Longest-Prefix Matching

> **Concept Refresher: The Routing Table**
> The kernel uses a routing table like a map to decide where to send a packet. When multiple routes match a destination, the kernel picks the **most specific match** (the "longest prefix"). A "default route" (`0.0.0.0/0`) is just the fallback used when no specific route exists.

Do not guess how a packet will route. Ask the kernel directly using the `ip` command:

```bash
ip address show                # List all IP addresses on the machine
ip route show table all        # Show all routing rules
ip route get 198.51.100.10     # Ask the kernel: "How would you reach this IP?"
ip -6 route get 2001:db8::10   # Same question, for IPv6

```

---

## 4. Neighbor Discovery Connects Network to Hardware

> **Concept Refresher: ARP and NDP**
> IP addresses exist only in software. To physically send data over a wire or Wi-Fi, your network card needs the destination's physical hardware address (MAC address).
> * **ARP (Address Resolution Protocol):** Used in IPv4 to map IPs to MACs.
> * **NDP (Neighbor Discovery Protocol):** The IPv6 equivalent.
> 
> 

If your host cannot resolve the MAC address of the next router or destination, the connection will fail. A "connection timed out" error might not be a broken application—it could be a failed ARP lookup. Use `ip neigh` to view the neighbor cache.

---

## 5. TCP is a State Machine AND a Byte Stream

> **Concept Refresher: TCP Characteristics**
> * **State Machine:** TCP connections go through phases (Listen, SYN-Sent, Established, FIN-Wait, Closed).
> * **Byte Stream:** TCP does *not* respect your application's message boundaries.
> 
> 

If your application calls `send()` twice with two separate JSON documents, the receiving application might get them both crammed together in a single `recv()` call, or chopped into three weirdly sized pieces. TCP only promises that the *bytes will arrive in order*. Your application (like HTTP) must figure out where one message ends and the next begins.

**The `TIME_WAIT` State:** When a server closes a connection, the socket goes into `TIME_WAIT` for a minute or two. This is **not a bug or a resource leak**. It is a safety mechanism to ensure delayed packets from the old connection don't accidentally get mixed into a new connection using the same ports.

**Gather TCP evidence:**

```bash
ss -lntp                     # Show all Listening, Numeric, TCP processes
ss -tan state established    # Show only active connections
ss -tan state time-wait      # Show connections safely waiting to fully close

```

---

## 6. UDP: Datagrams Without Guarantees

UDP (User Datagram Protocol) sends independent packets. It does not provide connection handshakes, retransmissions, ordering, or congestion control.

Developers sometimes treat UDP as just "faster TCP." This is dangerous. If you use UDP, your application code must handle lost packets, out-of-order packets, and retries. DNS uses UDP for small, fast queries, but falls back to TCP for large responses.

---

## 7. Unix-Domain Sockets

A Unix-domain socket looks like a file on your hard drive (e.g., `/var/run/app.sock`) but acts like a network connection. It is used exclusively for inter-process communication on the *same machine*.

Because it lives in the filesystem, you can use standard Linux file permissions (Owner/Group/Mode) to secure it, making it an excellent, fast alternative to TCP loopback.

---

## 8. Timeouts Belong to Different Phases

A generic configuration like `timeout=30` is a terrible practice because it hides multiple distinct boundaries. When a request fails, you need to know *what* timed out:

1. **DNS Resolution:** Could we turn the hostname into an IP?
2. **TCP Connect:** Did the TCP handshake complete?
3. **TLS Handshake:** Did the SSL/TLS certificate exchange succeed?
4. **Read/Write Idle:** Has the peer stopped sending data mid-stream?
5. **Total Operation:** Has this entire business transaction taken too long?

A "connect timeout" won't save you if the remote server accepts the connection but then silently refuses to send any data. You must configure distinct timeouts for distinct phases.

---

## 9. Worked Investigation: Port is Listening But Unreachable

**Scenario:** You run `ss -lntp` and see Atlas running on `127.0.0.1:18080`. However, a remote client laptop cannot connect to it.

**Investigation:** This is not a firewall bug. The socket is bound to loopback (`127.0.0.1`). By definition, loopback traffic can never leave the host.
To fix this securely, do not just change it to `0.0.0.0`. You must:

1. Bind it to the specific private internal IP (e.g., `10.0.0.5`).
2. Ensure host firewall policy only accepts traffic from known internal sources.

---

## 10. Dual-Stack Design is Explicit

> **Concept Refresher: Dual-Stack**
> A system is "Dual-Stack" if it runs both IPv4 and IPv6 simultaneously.

Do not test only IPv4 and declare "the network works." You must verify if the endpoint resolves an AAAA record, if the host has an IPv6 route, and if the application specifically listens on IPv6 (`::`). IPv6 is not just "IPv4 with longer addresses"; neighbor discovery and routing policies operate entirely differently.

---

## 11. Field Method: Diagnose from the Inside Out

When networking breaks, do not guess. Verify each layer outward, stopping as soon as the failure is located:

1. **Application:** Does the server process actually own the socket? (`ss -lntp`)
2. **Routing:** Does the host know how to route to the destination? (`ip route get <ip>`)
3. **Link:** Does neighbor discovery resolve the MAC address? (`ip neigh`)
4. **Transport:** Does the TCP handshake complete?
5. **Application Logic:** Does the application read and respond before its deadline?
6. **Intermediaries:** Is a proxy, firewall, or NAT device dropping the traffic?

*Warning: Using `ping` only proves ICMP reachability. It does NOT prove that a TCP listener is active, that a firewall allows port 443, or that an application is healthy.*

---

## Failure Patterns to Recognize

* **Wildcard Convenience:** Binding to `0.0.0.0` to make local testing easier, accidentally exposing an internal, unauthenticated database port to the entire internet.
* **Ping-Driven Diagnosis:** Assuming that because `ping` works, the web server must be reachable.
* **One Timeout to Rule Them All:** Using a single timeout variable, obscuring whether the network dropped the connection, or the application was just slow to process the data.

---

## Module Synthesis

Return to the central question: **How does a byte leave one process and reach the intended process across interfaces, routes, and transport state?**

A complete answer names the owner of the state, the kernel table that routes it, the failure boundary, and the specific command that proves it. The capstone is ready to progress only when the planted defect—*An administrative endpoint binds to `0.0.0.0` because the developer confused “reachable by the proxy” with “reachable by every interface.”*—fails for the exact reason you predicted.

### Module Route

1. Complete the exercises before viewing solutions.
2. Compare with the worked answers.
3. Run the controlled lab.
4. Retain the checkpoint evidence.
