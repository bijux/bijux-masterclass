# Worked answers — Traffic locality, source identity, and dual stack

The answers treat endpoint-selection policy as an availability and capacity decision, not merely a latency option.

## 1. Why must locality be applied after endpoint eligibility?

Locality should choose among endpoints that already satisfy readiness, serving/termination, protocol, port, and address-family requirements. If locality is applied first, the system can select an unready or incompatible local endpoint even though a healthy remote endpoint exists. The proof should show the filtered eligible set before topology preference and include a case where the local endpoint is unready. Soft preference should fall back; hard-local policy may intentionally fail.

## 2. What does internalTrafficPolicy Local do on a Node with no local endpoint?

It restricts internal Service selection to eligible endpoints on that Node. With none available, the Node has no backend for that Service, even if remote endpoints are healthy. This is a deliberate availability trade, not a transient selector bug. Test from client Pods on Nodes with and without local endpoints. Use it for Node-local semantics only when placement and capacity guarantee the required local population or when failure is the desired behavior.

## 3. Why can externalTrafficPolicy Local preserve source IP but reduce availability?

Local policy avoids cross-Node forwarding and often avoids source NAT, so the backend may see the original network source. But only Nodes with local eligible endpoints can serve external traffic. Health-check lag, uneven placement, rollout, or zone loss can shrink capacity or send traffic to Nodes with no backend. Prove source address, external health-check behavior, endpoint withdrawal, and failure-domain capacity. Source preservation is valuable evidence but not worth an unstated outage mode.

## 4. What is the difference between topology preference and topology requirement?

A preference ranks eligible endpoints—such as same-zone first—but permits fallback when local capacity is absent. A requirement removes non-local endpoints from consideration and can produce failure despite healthy remote capacity. The decision must say which behavior is intended. Test one domain with no local endpoint: a preference should fall back according to its contract; a requirement should fail predictably. Latency results alone cannot justify converting a preference into a hard eligibility rule.

## 5. Why can ClientIP affinity hotspot a backend?

The affinity key is the source address observed at the Service data plane. NAT or a proxy can collapse many users into one source, causing them all to prefer the same endpoint. Long affinity timeouts and uneven client populations worsen the hotspot. Measure observed source-key distribution and backend utilization, not just logical user count. Session affinity is neither durable session state nor authenticated identity and should not be required for correctness.

## 6. What does RequireDualStack promise that PreferDualStack does not?

`RequireDualStack` makes allocation of both supported address families a requirement; if the cluster cannot provide both, Service creation or update should not silently release a single-stack result. `PreferDualStack` requests both but permits a supported single-family outcome. Neither proves end-to-end paths. Use Require only when failing configuration is safer than silently degrading, and still test DNS, routes, policy, listeners, and endpoints for each family.

## 7. How can Happy Eyeballs hide an IPv6 outage?

The client can race or quickly fall back to IPv4 after an IPv6 attempt fails. Users see success, possibly with added latency, while IPv6 is completely broken. Aggregate success metrics then conceal the family-specific outage. Force IPv4 and IPv6 separately, record which address was attempted, and measure fallback delay. Family-specific SLO populations are necessary if dual stack is part of the platform promise.

## 8. Why is a forwarded client IP trustworthy only at a bounded proxy hop?

Any direct client can send forwarding headers. The application may trust them only when the immediate transport peer is an approved proxy that replaces untrusted values and writes the address it actually observed. If several proxies exist, their order and trust must be explicit. The forwarded IP remains network evidence, not authenticated user identity. Prove a direct client cannot spoof it and that an untrusted peer’s value is discarded.

## 9. What evidence proves topology-aware fallback?

Show the eligible endpoint set, topology metadata/hints, initial local selection, a fault removing local capacity, and subsequent selection of a permitted remote endpoint without violating readiness or family rules. Measure convergence time, failed/rejected requests during transition, and cross-zone traffic. Object fields alone do not prove data-plane support. The claim must name the implementation and version that honored the preference.

## 10. When is Local internal traffic policy a natural fit?

It fits a genuinely Node-local capability such as an agent, cache, or daemon where remote fallback would violate semantics, and where the platform ensures one healthy local endpoint on every client Node. It can also be useful for traffic that must remain on the Node for performance or security reasons with an accepted failure mode. It is not a generic optimization for ordinary replicated APIs. The design must prove placement, health, capacity, and behavior on new or drained Nodes.

## 11. What must a dual-stack NetworkPolicy inventory contain?

List IPv4 and IPv6 source/destination classes, DNS resolver addresses, Service and endpoint families, external egress/NAT paths, policy selectors or CIDRs, Gateway/listener families, and negative tests for each family. Ensure a broad IPv4 allow is not mistaken for IPv6 coverage and that IPv4-mapped IPv6 forms are handled consistently where relevant. The evidence should show actual policy verdicts and connections for both families.

## 12. Why should locality benchmarks include rejected or failed requests?

A hard-local or overloaded topology can lower latency for admitted successes while rejecting or timing out a larger fraction of offered traffic. Excluding those outcomes makes the policy appear faster by removing its failures from the denominator. Report offered, admitted, completed, rejected, failed, and missing requests per topology domain and family. A locality change is acceptable only when it meets both performance and availability/correctness objectives under normal and faulted placement.
