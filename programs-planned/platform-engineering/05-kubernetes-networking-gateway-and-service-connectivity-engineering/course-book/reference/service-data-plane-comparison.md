# Service data-plane comparison

| Design family | Typical mechanism | Strengths | Risks/evidence needs |
|---|---|---|---|
| userspace proxy | process accepts/forwards | simple model | extra hop, process capacity |
| iptables/nftables | kernel rules and connection tracking | mature, broad support | rule scale, update visibility, NAT state |
| IPVS | kernel virtual server | efficient load-balancing primitives | separate state model and debugging |
| eBPF | hook-based maps/programs | flexible, integrated policy/observability | implementation-specific hooks, map/program evidence |
| cloud/network appliance | external or managed forwarding | infrastructure integration | controller convergence, quotas, cloud failure boundary |

The Service and EndpointSlice APIs are portable. Programming details, source preservation, connection behavior, metrics, and update latency are implementation-specific.
