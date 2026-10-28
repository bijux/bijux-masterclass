# Worked Answers — Module 07: Firewalls, NAT, Proxies, and Load Balancing

These answers demonstrate reasoning. Equivalent answers are valid when they preserve the same mechanism and evidence boundary.

## Exercise 1 — Firewall versus authentication

Source addresses can represent shared networks, NAT gateways, compromised hosts, or spoofable forwarding data. The firewall narrows network reachability but does not identify the application principal. Atlas still requires application authentication and authorization in later programs. Treat network source as context, not user identity.

## Exercise 2 — Established traffic

Return packets for connections the host initiated or accepted are recognized by connection tracking. Accepting them avoids writing reverse rules for every ephemeral port. The policy must still handle invalid state and understand related protocols. Connection tracking is resource state and can itself be exhausted.

## Exercise 3 — ICMP policy

IPv4 path MTU discovery can fail when fragmentation-needed messages are blocked, causing black-hole connections. IPv6 relies on ICMPv6 for neighbor discovery and router functions, so blanket blocking can break basic connectivity. Permit required types with appropriate rate controls.

## Exercise 4 — NAT scope

The backend may see one translated source address and port mappings rather than original stable client identities. Translation state can expire and addresses can be reused. Preserve user identity at the application layer and use trusted proxy mechanisms only where the architecture controls them.

## Exercise 5 — Forwarded spoof

It removes all incoming forwarding and real-IP fields, then writes a canonical value from the direct TCP peer. The API is reachable only through the trusted edge in the deployment model. Tests inject a spoofed field and verify it is not preserved.

## Exercise 6 — Safe retry

GET is intended to be safe and can often be retried within a deadline. POST /jobs can create an effect, and Course 1 has no end-to-end idempotency key proving duplicate suppression. Retrying after an ambiguous response could submit twice. Later API courses define stronger idempotency.

## Exercise 7 — Health depth

TCP connect proves a listener accepted the transport handshake. Liveness proves the application handler executes. Readiness tests selected prerequisites for routing, such as writable state and worker freshness. None proves every business operation, and deeper checks can add load or dependency coupling.

## Exercise 8 — Drain sequence

Mark it not ready or remove it from new selection, wait for bounded in-flight work and long-lived connections according to policy, stop the service gracefully, then force termination only after the deadline. Verify no new requests arrive and account for work that exceeds the drain window.

## Exercise 9 — Forward versus reverse proxy

A forward proxy represents clients reaching external destinations; a reverse proxy represents servers accepting client traffic. Both terminate one connection and create another, can inspect data, and become policy and availability dependencies. Configuration must define identity propagation, TLS, timeouts, and failure behavior.

## Exercise 10 — L4 versus L7

If routing depends on HTTP host, path, method, headers, or application-aware health, an L4 balancer sees only transport metadata. An L7 proxy can make those decisions but owns HTTP semantics and often TLS. Choose the lowest layer that satisfies the requirement.

## Exercise 11 — Firewall rollout

It checks syntax, not reachability, interaction with existing rules, correct interface names, or management-source accuracy. Use a console or rollback timer, inspect the combined ruleset, test from allowed and denied sources, and preserve a recovery path. Load only in a disposable lab for this course.

## Exercise 12 — 503 proof

Record one incoming request, the number and identity of backend attempts, elapsed deadline, final 503, and absence of repeated background retries. For unsafe methods, confirm only one attempt. Correlate edge and backend logs. A 503 alone does not reveal whether the proxy attempted one or one hundred connections.
