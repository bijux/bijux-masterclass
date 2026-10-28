# Checkpoint — Network Foundation

## Required evidence

Retain:

- non-overlapping address plan and allocation owner;
- stable zone-ID to account-local name mapping;
- subnet role, public-address, and route-table matrix;
- successful and failed packet walks;
- security-group source/destination model;
- DNS authority and resolver path;
- `single-nat`, `nat-per-zone`, and `endpoints-only` trade-off record;
- zone-failure analysis;
- negative reachability evidence;
- flow-log interpretation limits;
- cost-bearing network cleanup proof when the AWS lane is used.

## Decision defense

Draw one allowed and one denied flow from source through DNS, route selection, gateways/endpoints, security decisions, and destination behavior. Identify the precise decision that admits or drops each packet. Explain why “private subnet” is insufficient as a behavioral claim.

## Progression gate

You pass only when every default route, public address, and egress mechanism has an explicit owner and purpose, and the chosen egress profile is defended with both availability and cost evidence.
