# Worked Answers — Network Foundation

## 1. Subnet classification

Reachability comes from route-table association, address assignment, gateways, and security policy. Names/tags are metadata. A subnet named private with an internet-gateway route and public addresses is public in behavior.

Prove the classification by walking a packet in both directions and recording route, address, gateway, and filtering decisions rather than trusting the subnet label.

## 2. Zone IDs

AWS account-specific zone letters can map to different physical zones. Zone IDs provide stable cross-account identity needed for aligned placement and failure-domain reasoning.

A multi-account placement plan should record both the stable zone ID and the account-local name used by each provider call.

## 3. Reserved space

Future endpoints, load balancers, scaling, data tiers, peering/transit, and Kubernetes pod/service ranges need room. Tight allocation makes later non-overlapping expansion and migration difficult.

The address plan should reserve explicit ranges and document the authority allowed to allocate them, rather than merely leaving accidental gaps.

## 4. Egress profiles

`single-nat` is cheaper but one-zone and may create cross-zone traffic. `nat-per-zone` improves zonal independence at higher fixed cost. `endpoints-only` removes general internet egress but requires complete service-endpoint and immutable-image planning.

## 5. Endpoint effects

It can avoid NAT/data-transfer paths and add an endpoint policy/private DNS path. IAM and resource policies still apply, and an overly broad endpoint policy can expand authority.

Verify the actual route table, DNS answer, endpoint policy, principal policy, and bucket policy; the mere existence of an endpoint proves none of those decisions.

## 6. IPv6 egress

IPv6 does not require address translation. Use routes and an egress-only internet gateway for outbound-only behavior. Security groups, DNS AAAA, listener support, and application testing still matter.

A dual-stack release therefore needs separate IPv4 and IPv6 reachability and negative-ingress evidence instead of assuming one family validates the other.

## 7. Security-group references

They authorize traffic from interfaces belonging to a named source group rather than a broad, mutable CIDR. This better represents the intended ALB-to-workload relationship.

The proof should show that removing the source-group membership removes reachability while unrelated interfaces in the same CIDR remain unauthorized.

## 8. NACL risk

They are stateless and subnet-scoped. Both directions and ephemeral return ports must be permitted. Rule order and subnet-wide impact can cause confusing asymmetric failures.

When diagnosing a failure, evaluate the full request and return path and compare NACL counters with security-group and route evidence before changing rules.

## 9. DNS evidence

Query name/type, client/resolver identity, answer/NXDOMAIN, TTL, authoritative chain, private-zone associations, address family, and the subsequent connection target.

Retain timestamps and repeat after TTL expiry so that a cached answer is not mistaken for current authoritative configuration.

## 10. Centralization trade-offs

It adds transit/inspection dependencies, route propagation, cross-account authority, cost, and a shared failure domain. Adopt it when ownership and policy need justify those costs.

The decision record should compare those costs with the concrete controls or shared services that centralization enables and define how the shared path fails safely.

## 11. Flow-log limits

They show summarized flow metadata and accept/reject status for observed interfaces. They do not capture payloads, prove application success, or always provide immediate packet-by-packet truth.

Correlate them with route tables, security-group rules, DNS evidence, packet captures where permitted, and application traces before concluding why a request failed.

## 12. “Private” diagnosis

It is publicly reachable by design: public address plus IGW route plus open security group. Remove public addressing, associate the intended private table, close SSH, use a controlled management path, and verify negative reachability.
