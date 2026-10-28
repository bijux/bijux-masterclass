# Lab — Prove the Packet Path

## Goal

Prove that the Atlas network admits the declared flows, rejects unsafe shortcuts, and makes the availability and cost consequences of its egress design explicit.

## Safety boundary

The required path uses deterministic CIDR, route, and flow fixtures. It creates no VPC, NAT gateway, endpoint, DNS zone, or flow log. The optional AWS path must use a disposable sandbox, a bounded spend limit, and an explicit destroy checklist because NAT gateways, endpoints, and logs can incur cost.

## Baseline

Inspect:

```text
capstone/fixtures/network/network-plan-safe.json
capstone/fixtures/network/flow-cases.json
```

Build an address and route inventory containing each subnet role, CIDR, availability-zone slot, route table, default route, and intended source/destination flow.

## Hypothesis

Every subnet requires an explicit routing role. Private placement is not equivalent to no egress. Source security-group relationships are more precise than opening a backend to an entire VPC CIDR. A single NAT used by multiple zones creates a cross-zone dependency. An endpoints-only profile is safe only when every required dependency has a reachable endpoint or another declared path.

## Controlled action

1. Run the CIDR overlap and containment checks on `network-plan-safe.json`.
2. Evaluate all flow cases and identify the route and policy decision for each permitted or denied packet.
3. Evaluate `network-plan-overlap.json` and retain the exact overlap rejection.
4. Evaluate `network-plan-data-internet.json` and explain why direct internet routing from the data tier violates the design.
5. Replace broad VPC-CIDR backend access with a source security-group relationship.
6. Compare `nat-per-zone`, `single-nat`, and `endpoints-only` profiles for availability, cost, and dependency coverage.
7. For `endpoints-only`, list every Atlas dependency that loses connectivity and the evidence required before declaring the profile viable.
8. Model one zone failure under a single-NAT design and identify the surviving and failed paths.
9. Optional Level C: apply the sandbox network, test reachability through SSM or equivalent controlled access, inspect flow logs, and destroy every cost-bearing resource.

## Oracle

- baseline CIDRs are contained and non-overlapping;
- every subnet has one explicit route-table association;
- public default routes exist only in intended public tiers;
- workload interfaces receive no public address;
- backend admission is source-identity based rather than VPC-wide;
- each egress profile has an honest availability and cost claim;
- every failed flow can be traced to a specific route, security, DNS, or endpoint decision.

## Evidence

Retain the address plan, route matrix, flow decision table, security-group relationship, egress-profile comparison, zone-failure analysis, and at least one negative reachability proof.

## Interpretation

Explain why “private subnet” is an incomplete statement. A subnet’s behavior emerges from routes, address assignment, network policy, DNS, endpoints, NAT, gateways, and destination behavior. Also distinguish a routing failure from a security-policy denial and a DNS failure; they require different evidence.

## Cleanup

Remove generated local plans and run `make clean`. If the optional cloud path was used, destroy endpoints, NAT gateways, route tables, flow-log destinations, test instances, and elastic IPs. Confirm that no cost-bearing resource remains.

## Completion gate

You pass only when you can draw one successful and one failed packet path hop by hop, name the exact decision at each hop, and defend the selected egress profile with both availability and cost evidence.
