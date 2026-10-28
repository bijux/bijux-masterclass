# Capstone architecture

Atlas Connectivity Plane 1.0 uses a deliberately small set of components so that ownership remains visible.

```text
public DNS
  → Gateway address
  → TLS listener
  → HTTPRoute
  → atlas-api Service
  → ready EndpointSlice
  → API Pod

worker/API Pod
  → cluster DNS
  → internal Service or direct owned dependency
  → governed egress for external services
```

## Ownership rules

- Course 4 owns workload image, process, readiness, shutdown, labels, and ports.
- The CNI/IPAM implementation owns Pod attachment and address state.
- Kubernetes controllers own Service and EndpointSlice intent.
- The installed service data plane owns virtual-address forwarding.
- CoreDNS and resolver configuration own name-to-address behavior.
- NetworkPolicy objects and the installed CNI own L3/L4 admission.
- GatewayClass/Gateway owners manage edge infrastructure and listeners.
- Route owners manage application routing within permitted boundaries.
- The target namespace owns cross-namespace permission through ReferenceGrant.
- The certificate system owns issuance and rotation; the Gateway owns listener use.
- External dependency owners remain outside the cluster; Atlas owns its egress contract.

## Deliberate exclusions

The capstone does not implement a production CNI, cloud load balancer, DNS operator, certificate authority, or service mesh. It models and verifies the contracts required to evaluate those systems. Course 6 will own persistent storage; Course 8 will deepen platform security and tenancy; Course 9 will operate fleet-scale reliability and capacity.
