# Reference — CIDR and Subnet Planning

An address plan is a long-lived allocation contract. It should be designed for routing, failure domains, growth, and future platform layers—not merely to fit today’s instances.

## Atlas reference allocation

Atlas uses `10.64.0.0/16` in the AWS reference lane.

| Purpose | Zone slot A | Zone slot B | Notes |
|---|---|---|---|
| Public edge | `10.64.0.0/24` | `10.64.1.0/24` | Load balancers, NAT gateways where used |
| Private workload | `10.64.16.0/20` | `10.64.32.0/20` | Host and later container workload capacity |
| Data | `10.64.64.0/24` | `10.64.65.0/24` | No default internet route |
| Reserved expansion | remaining ranges | remaining ranges | Future endpoints, Kubernetes, or service tiers |

The unused space is deliberate. Dense allocation can make a later non-overlapping expansion impossible.

## Begin with a registry

Do not select CIDRs independently in each project. The foundation should own a registry or IPAM process containing:

```text
network identity
CIDR
owner
purpose
region
account/project/subscription
routing domain
peering/transit relationships
allocation date
retirement state
```

The registry must include on-premises networks, VPN clients, partner routes, managed services, and future cluster pod/service ranges where relevant.

## Subnet size is not usable-host count alone

Providers reserve addresses and create their own network interfaces. Capacity consumers include:

- load-balancer nodes;
- NAT gateways and endpoints;
- instance and autoscaling interfaces;
- managed database interfaces;
- replacement overlap;
- future Kubernetes nodes and pods;
- incident and diagnostic hosts.

A subnet that fits steady state but not replacement or failure recovery is undersized.

## Stable zone identity

Availability-zone names can map differently across accounts. Use stable zone IDs in architecture records, then map them to account-local names at composition time. A semantic subnet key such as `private-a` should represent the same zone slot and role throughout its state history.

## Public and private are behavioral classifications

A public subnet normally has a route to an internet gateway and can host interfaces with public addressing. A private subnet lacks direct internet-gateway reachability but may still have outbound access through NAT, endpoints, transit, or proxies. A data subnet may intentionally have neither default internet nor general NAT route.

The name does not create the behavior. Record:

```text
subnet CIDR
route table
public-address setting
network policies
DNS behavior
egress path
intended workload class
```

## Overlap and containment

For every subnet, prove:

1. it is contained within the parent network;
2. it does not overlap any sibling;
3. it does not overlap connected networks;
4. its prefix permits expected capacity and replacement;
5. summarization does not accidentally route unintended ranges.

Atlas fixtures include both safe and overlapping plans so this is executable rather than a diagram-only claim.

## Route design

List each destination class and next hop:

| Source tier | Destination | Intended next hop |
|---|---|---|
| public | internet IPv4 | internet gateway |
| private | S3 | gateway endpoint when enabled |
| private | approved external dependency | NAT/proxy according to egress profile |
| data | internet | none |
| workload | internal VPC | local route plus security policy |

Longest-prefix selection decides routing. Security controls decide whether the routed packet is admitted. DNS decides which destination is attempted. Keep these evidence layers separate.

## IPv6

IPv6 does not use IPv4 NAT as the normal model. Egress-only gateways can allow outbound initiation while blocking unsolicited inbound connections, but route and security design still matter. Dual-stack workloads need independent IPv4 and IPv6 tests; enabling an IPv6 CIDR is not proof of equivalent policy.

## Future Kubernetes planning

Course 4 will introduce Kubernetes. Depending on the networking model, clusters may need node, pod, and service address space, plus load-balancer and endpoint interfaces. Reserving address space now avoids forcing a disruptive VPC migration later. The course does not choose those ranges prematurely; it records the requirement and ownership boundary.

## Review checklist

Reject an address plan when:

- ownership is absent;
- overlaps are unresolved;
- only steady-state capacity is considered;
- zone mapping is based solely on account-relative names;
- public/private classification relies on labels;
- data tiers have unexplained default routes;
- connected-network growth is ignored;
- cleanup or reuse of retired ranges has no quarantine policy.

A good address plan makes future routing decisions possible while keeping current flows explainable.
