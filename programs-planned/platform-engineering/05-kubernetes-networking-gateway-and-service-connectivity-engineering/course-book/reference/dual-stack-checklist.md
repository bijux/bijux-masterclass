# Dual-stack checklist

Verify IPv4 and IPv6 independently for:

- Pod addresses and routes;
- Node reachability;
- Service ClusterIPs and `ipFamilyPolicy`;
- EndpointSlice address types;
- DNS A and AAAA answers;
- application listeners;
- NetworkPolicy peers and `ipBlock` ranges;
- Gateway/listener addresses;
- external load balancer behavior;
- egress/private connectivity;
- MTU and ICMP behavior;
- telemetry labels and dashboards.

Disable client fallback during tests. A successful request after IPv6 timeout and IPv4 fallback is a degraded result, not dual-stack success.
