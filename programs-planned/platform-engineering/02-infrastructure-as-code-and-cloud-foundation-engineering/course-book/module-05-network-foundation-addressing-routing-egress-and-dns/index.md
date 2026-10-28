# Module 5 — Network Foundation: Addressing, Routing, Egress, and DNS

A subnet is not public because it is named `public`. It is public when its route table and address assignment permit an interface to use an internet gateway, and when security policy permits the flow. A private subnet can still have outbound internet through NAT, private service access through endpoints, or no egress at all.

This module turns Course 1 packet-path reasoning into a reproducible VPC design. The goal is not to memorize AWS diagrams. It is to own each route, address, DNS decision, and cost-bearing egress path.

## Learning outcomes

You will be able to:

- design a non-overlapping address plan with future Kubernetes needs in mind;
- distinguish Availability Zone names from stable Zone IDs;
- prove subnet role from route-table association and address behavior;
- design IPv4 and IPv6 paths deliberately;
- compare NAT, VPC endpoints, public addresses, proxies, and no-egress profiles;
- distinguish security groups, network ACLs, routes, and application authorization;
- design DNS resolver and private-zone ownership;
- instrument flows without treating logs as packet capture;
- reason about centralized versus account-local networking;
- verify negative reachability as well as successful connectivity.

## Start with flows, not resources

Write the required flows first:

| Source | Destination | Protocol | Purpose | Owner |
|---|---|---|---|---|
| Internet | ALB listener | TCP/443 | public Atlas API | edge |
| ALB | Atlas instance | TCP/18080 | approved backend path | edge/workload |
| Atlas | S3 backup endpoint | HTTPS | backup write | workload/data |
| Atlas | IMDS | link-local HTTP + token | temporary credentials/metadata | platform |
| Operator | SSM control channel | HTTPS outbound | managed access | operations |
| Atlas | arbitrary internet | none by default/profled | package/API egress | explicitly approved |

Each flow becomes route, DNS, security-group, endpoint, identity, and evidence decisions.

## Address planning is long-lived

Atlas uses `10.64.0.0/16`. It reserves blocks rather than packing subnets tightly:

```text
10.64.0.0/24    public edge slot 0
10.64.1.0/24    public edge slot 1
10.64.16.0/20   private workload slot 0
10.64.32.0/20   private workload slot 1
10.64.64.0/20   reserved data slot 0
10.64.80.0/20   reserved data slot 1
```

Future Kubernetes clusters may need pod and service address space, interface endpoints, load-balancer nodes, and burst headroom. Renumbering after peering, allowlists, DNS, and certificates depend on addresses is expensive.

Use an organization-wide IPAM process. The course’s CIDR checker proves non-overlap within Atlas; it cannot prove the range is unused elsewhere in the organization.

## Zone names are account-relative

`eu-central-1a` can map to a different physical zone in another AWS account. Zone IDs are stable identifiers across accounts. When multi-account topology needs aligned zones, record Zone IDs rather than assuming the same letter means the same location.

The module input uses stable logical slot keys (`zone-0`, `zone-1`) and records observed zone ID/name mappings in evidence.

## Route tables define reachability intent

Every subnet is associated with a route table, explicitly or through the VPC’s main table. Atlas explicitly associates every subnet so a future main-table change cannot alter a subnet silently.

Public edge table:

```text
10.64.0.0/16 → local
0.0.0.0/0    → internet gateway
::/0         → internet gateway (only when IPv6 profile enabled)
```

Private workload table, NAT profile:

```text
10.64.0.0/16 → local
0.0.0.0/0    → NAT gateway for the selected availability profile
::/0         → egress-only internet gateway (when IPv6 enabled)
```

Private endpoint-only profile has no default internet route. It uses S3 gateway endpoints and interface endpoints for SSM-related services. That profile requires immutable images and careful dependency inventory.

## NAT is an availability and cost decision

A public NAT gateway permits private IPv4 instances to initiate internet connections. A single NAT gateway is cheaper but creates one zonal dependency and cross-zone data charges when used from another zone. A NAT gateway per active zone improves zonal independence but costs more.

AWS introduced a regional NAT Gateway option in 2026. Provider support and exact semantics must be verified before adopting it; the course’s pinned AWS provider reference uses the established zonal NAT resource profile.

Atlas profiles:

- `single-nat` — development cost profile, explicitly not zone tolerant;
- `nat-per-zone` — stronger egress availability for active zones;
- `endpoints-only` — no general internet egress; requires declared endpoints and image discipline;
- `none` — no external egress.

The profile is visible in the root stack and policy evidence.

## VPC endpoints reduce some public paths, not all risk

Gateway endpoints for S3/DynamoDB and interface endpoints for many services can keep traffic on provider networks and reduce NAT cost. Endpoint policies and private DNS become part of authorization and name resolution.

An endpoint does not automatically grant service permission; IAM and resource policy still apply. Conversely, an overly broad endpoint policy can weaken a previously narrow path.

## IPv6 changes the egress model

IPv6 addresses are globally routable. A private workload does not need NAT for address translation. Use route policy and an egress-only internet gateway to allow outbound-only IPv6. Security groups remain necessary.

Dual-stack correctness requires:

- IPv6 CIDR allocation;
- subnet IPv6 ranges;
- DNS AAAA decisions;
- listener support;
- route tables;
- security-group rules;
- client tests over both families.

Do not publish AAAA records until the complete path works and is monitored.

## Security groups and network ACLs have different roles

Security groups are stateful and attach to network interfaces/resources. Atlas expresses flows by referencing security groups where possible:

```text
ALB security group → workload security group : TCP/18080
```

This is stronger than allowing the whole VPC CIDR.

Network ACLs are stateless subnet-level rules. They require return-path port ranges and are easy to misuse. Atlas leaves default NACL behavior in the baseline and uses explicit security groups. NACL changes are introduced only for a specific threat or compliance requirement with packet-level tests.

Neither mechanism performs application authorization.

## DNS is part of the network foundation

Atlas distinguishes:

- public hosted zone and API record;
- private service names;
- VPC DNS resolver behavior;
- split-horizon names;
- endpoint private DNS;
- TTL and failover behavior;
- ownership of delegated zones.

A private hosted zone associated with the wrong VPC produces resolution failures that look like network or service failure. DNS evidence includes query name, resolver, answer, TTL, address family, and authoritative path.

## Centralized networking is not automatically mature

A central network account can own transit gateways, inspection, shared egress, DNS resolver endpoints, and connectivity. It also creates cross-account dependencies, route-propagation complexity, cost, and a larger failure domain.

Course 2 uses account-local VPCs. Course 10 may later expose governed network capabilities. Centralization should be driven by real shared ownership and policy, not by a diagram copied from a large enterprise.

## Flow logs are summarized evidence

VPC Flow Logs can record accepted/rejected flow metadata at selected interfaces/subnets/VPCs. They do not contain payloads and may be delayed or aggregated. Use them with route tables, security groups, DNS evidence, and active probes.

Logging every field and flow indefinitely creates cost and sensitive metadata. Choose destinations, retention, and access deliberately.

## Worked incident: “private” instance is reachable

An instance sits in a subnet named `private-a`. It receives a public IPv4 address. The subnet’s route table points `0.0.0.0/0` to the internet gateway. Its security group allows TCP/22 from anywhere.

The name provides no control. The packet path is public.

The repair is not only renaming. Remove public addressing, associate the intended private route table, restrict management to SSM or a controlled path, and run a negative external reachability test.

## Atlas network module

The module creates:

- VPC with DNS support;
- explicitly associated public/private route tables;
- public and private subnets keyed by zone slot;
- internet gateway;
- selected egress profile;
- S3 gateway endpoint;
- optional interface endpoints;
- flow-log destination and role integration;
- outputs grouped by subnet role and slot.

Policy rejects:

- overlapping CIDRs;
- default internet route in an endpoint-only private table;
- workload public IP;
- SSH ingress from the internet;
- one NAT advertised as zone tolerant;
- missing explicit route-table association;
- unbounded egress without an approved profile.

## Packet walk: private Atlas host reaches S3

Atlas in `private-b` needs to write a backup object. The foundation provides an
S3 gateway endpoint associated with the private route table.

A packet decision can be reasoned as:

1. DNS resolves the S3 service name according to the AWS endpoint behavior.
2. The destination IP matches the service prefix list route installed by the
   gateway endpoint.
3. Longest-prefix selection chooses the endpoint route over `0.0.0.0/0` to
   `nat-b`.
4. The endpoint policy, bucket policy, IAM role, and KMS key policy still must
   permit the operation.
5. Flow logs may show the network flow but not prove the object write or policy
   decision.

If the endpoint is missing, the same call may egress through NAT and still
succeed. Therefore a successful upload does not prove the intended path. The
lab asserts the selected route and, in a real account, correlates route-table,
flow, and S3 access evidence.

## Failure analysis: one NAT for two zones

A single NAT gateway in `public-a` serves `private-a` and `private-b`.

Advantages:

- lower fixed cost;
- fewer addresses and resources;
- simple sandbox cleanup.

Costs and risks:

- `private-b` egress crosses zones;
- zone A or NAT failure removes egress for both private tiers;
- cross-zone data processing can add cost;
- route dependencies are less local;
- maintenance affects all private workloads.

Per-zone NAT improves locality and zone-failure containment but doubles fixed
resources in a two-zone design. Course 2 uses `nat_mode = none` for the cheapest
dependency-light/default stack and makes NAT an explicit reviewed choice in the
AWS lane. Production guidance records `per-az` as a target only when the service
requires that availability and the organization accepts the cost.

## Split-horizon DNS and ownership

Internal Atlas service names may resolve to private addresses while the public
name resolves to the ALB. This can reduce hairpin/public routing, but it creates
two namespaces with potentially different answers and failure modes.

Define:

- which zone is authoritative for each name;
- which networks associate with the private zone;
- how resolver forwarding works from other networks;
- whether certificates cover public, private, or both names;
- how debugging distinguishes cache, resolver, route, and target failure;
- who may publish records.

“DNS issue” is not a diagnosis. Evidence should identify query name/type,
resolver used, answer/authority, TTL, and the subsequent network path.

## IPv6 is not an automatic dual-stack checkbox

Giving subnets IPv6 changes addressing, security rules, egress, logging,
application binding, DNS records, and client behavior. IPv6 addresses are
globally routable by design; private behavior comes from routing and filtering,
not RFC1918 addressing.

A dual-stack migration needs:

- application listeners on both families;
- AAAA and A publication strategy;
- egress-only internet gateway or proxy design;
- security-group and NACL parity;
- monitoring and log parsing for IPv6;
- Happy Eyeballs/client testing;
- rollback if one family fails.

Course 2 reserves IPv6 address space in the architecture but does not claim a
dual-stack release without those proofs.

## Atlas capstone increment

Module 5 adds HCL, a Python route evaluator, CIDR tests, cost/availability profile fixtures, DNS records, and negative-reachability evidence templates.

## Completion standard

You are ready for Module 6 when you can draw every Atlas packet path from source interface to destination, name the route and policy decision at each hop, identify the DNS authority, and state which path produces recurring cost.
