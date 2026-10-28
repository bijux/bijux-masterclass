# Address-domain inventory

Record address domains before assigning CIDRs.

| Domain | Typical owner | Stable for | Routable from | Translation expected | Policy meaning |
|---|---|---|---|---|---|
| loopback | Pod/host namespace | namespace lifetime | same namespace | no | local process boundary |
| Pod | CNI/IPAM | Pod sandbox lifetime | cluster according to CNI | ideally no application NAT | workload attachment, not durable principal |
| Node | cloud/host network | Node lifetime | infrastructure network | possible at edge/egress | infrastructure location |
| Service | Kubernetes Service allocator | Service lifetime | cluster data plane | destination translation | stable virtual service identity |
| Gateway/LB | Gateway/cloud implementation | infrastructure release | external or internal clients | proxy/NAT | edge boundary |
| external dependency | external owner | external contract | approved egress path | NAT/proxy/private endpoint | never inferred from DNS alone |

For every domain record IPv4 and IPv6 separately, owner, allocation source, overlap checks, route distribution, observability, exhaustion behavior, and recovery. A CIDR list without lifecycle ownership is incomplete.
