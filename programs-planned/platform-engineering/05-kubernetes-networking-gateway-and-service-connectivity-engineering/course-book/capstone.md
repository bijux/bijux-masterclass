# Capstone — Atlas Connectivity Plane 1.0

The capstone continues the exact Atlas workload released by Course 4. It does not create a new demonstration application.

## Inherited guarantees

The API and worker images are immutable digest-addressed releases. They run as UID/GID `65532`, do not require privilege escalation, use read-only root filesystems, expose named ports, implement startup/readiness/liveness semantics, and honor a 30-second shutdown contract. Course 5 must preserve those guarantees while adding connectivity.

## Target architecture

```text
external client
  │
  ├─ public DNS: atlas.example.invalid
  │
  ▼
HTTPS Gateway listener
  │  replaces untrusted forwarding headers
  │  attaches only approved HTTPRoutes
  ▼
atlas-api Service :8080
  │  selects only eligible EndpointSlice endpoints
  ▼
Ready atlas-api Pods
  │
  ├─ cluster DNS over UDP and TCP
  ├─ approved worker/internal paths
  └─ explicit external egress contracts
```

## Capstone contracts

The release contains six connected contracts:

1. **address and route contract** — Pod, Node, Service, public, and external domains do not overlap accidentally; forward and reverse paths are owned;
2. **discovery contract** — Service names, record types, search behavior, TTLs, and negative answers are explicit;
3. **membership contract** — readiness, EndpointSlice conditions, traffic policy, and data-plane generation govern backend eligibility;
4. **segmentation contract** — required ingress and egress flows survive default deny while planted unauthorized flows fail;
5. **edge trust contract** — Gateway attachment, hostname/path matching, TLS, forwarded identity, and retry behavior are bounded;
6. **external dependency contract** — URL, hostname, resolved addresses, connected peer, redirects, TLS, and resource limits are validated.

## Executable evidence

`capstone/atlas_net/` implements deterministic models for the contracts. `capstone/network_lab.py` starts real loopback backend processes, a Service proxy, a UDP DNS server, and a TLS Gateway. The lab proves actual socket, HTTP, DNS, certificate, readiness, and header behavior without claiming Kubernetes conformance.

`capstone/manifests/` contains the Kubernetes production-intent release and explicit example-only frontier resources. `capstone/kind/` and `capstone/cilium/` define the guarded native lane. `capstone/planted-defects/` and `capstone/releases/` make the release gate proof-sensitive.

## Final defense

The final defense must demonstrate:

- a correct same-Node and cross-Node packet path;
- idempotent CNI attachment cleanup;
- Service convergence after readiness withdrawal;
- positive and negative DNS cache behavior;
- default-deny policy without broad exceptions;
- Gateway attachment and negative route cases;
- public TLS hostname verification and honest backend trust claims;
- egress connected-peer validation;
- one rejected mesh proposal based on insufficient value;
- a complete Course 6 handoff.

The capstone is accepted only when correctness and evidence gates pass. A faster or more permissive path is not an improvement if it weakens identity, policy, TLS, readiness, or failure semantics.
