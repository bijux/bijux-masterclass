# Orientation — inherit the workload before designing the network

Course 5 does not begin with a blank cluster or a vendor installation guide. It begins with a workload whose identity, lifecycle, resource, and supply-chain contracts were already established in Course 4.

That distinction matters. Networking is often taught as a sequence of objects—create a Service, install an ingress controller, add a NetworkPolicy—but those objects are meaningful only in relation to a workload contract. A network cannot make a process ready, cannot decide whether a retry is safe, and cannot turn a mutable image tag into a trustworthy release. It can only transport, select, translate, filter, and expose traffic according to the information it is given.

The inherited Atlas system contains:

- namespace `atlas-system`;
- a three-replica Atlas API Deployment;
- a one-replica worker Deployment;
- immutable image digests;
- API port `8080` named `http`;
- explicit startup, readiness, liveness, and shutdown behavior;
- intended placement across two failure domains, without an unsupported availability claim;
- a public authority requirement, `atlas.example.invalid`;
- a design target for default-deny traffic policy;
- open risks around endpoint propagation, DNS, Gateway implementation, address families, and storage connectivity.

Run the predecessor proof before reading further:

```bash
make predecessor-proof
```

The command verifies the exact bytes of `capstone/predecessor/handoff/`. If it fails, the course boundary is already broken: repair the handoff rather than silently adapting Course 5 to a different workload.

## The three paths you must be able to draw

Before applying any manifest, draw these paths from memory.

### 1. Direct workload path

```text
Atlas API Pod
    ↓
Pod network attachment
    ↓
Node route or overlay/underlay path
    ↓
worker Pod
```

This path raises questions about Pod addresses, CNI attachment, Node routing, MTU, policy, and return traffic. It does not involve Service selection unless the caller deliberately uses a Service address.

### 2. Service path

```text
client Pod
    ↓
DNS answer or known Service address
    ↓
Service virtual destination
    ↓
programmed Service data plane
    ↓
eligible EndpointSlice endpoint
    ↓
Ready Atlas API Pod
```

Here the Service object, EndpointSlices, readiness, and node-local forwarding state are separate proof objects. A correct selector does not prove endpoint publication; a correct EndpointSlice does not prove that every Node has installed the same forwarding generation.

### 3. Public path

```text
external client
    ↓
public DNS and route
    ↓
TLS listener
    ↓
Gateway and HTTPRoute attachment
    ↓
Atlas API Service
    ↓
EndpointSlice and Service data plane
    ↓
Ready Atlas API Pod
```

This path adds certificate identity, SNI, HTTP authority, trusted forwarding metadata, Gateway status, backend protocol, cloud or local load-balancer behavior, and external source translation.

For every arrow, record four things:

1. **Owner** — which process, controller, kernel component, or external service is allowed to create the transition?
2. **Input state** — which object or configuration drives it?
3. **Observed evidence** — what can you inspect when it works or fails?
4. **Negative control** — what test proves that an unintended path is denied?

A packet-path diagram without owners is decoration. A manifest without observed state is intent. A successful request without a negative control proves very little about policy.

## Evidence levels

Run:

```bash
make doctor
```

The required dependency-light lane uses Python, Go, and OpenSSL. It can prove semantic rules, execute real loopback DNS and TCP/TLS exchanges, and exercise process failure. Optional tools may provide stronger evidence:

- `kubectl`, kind, and a CNI implementation for cluster behavior;
- `dig`, `ss`, `ip`, and `tcpdump` for native observation;
- a Gateway controller for attachment and data-plane behavior;
- a real cloud environment for load balancers, routes, NAT, private endpoints, and managed DNS.

Record absent tools as `not-executed`. Do not replace missing evidence with a screenshot from documentation, a synthetic JSON result, or a statement that the configuration “should work.”

The evidence ladder used throughout the course is:

```text
document and design evidence
        ↓
deterministic semantic evidence
        ↓
real local sockets, DNS, and TLS
        ↓
disposable Kubernetes cluster evidence
        ↓
real cloud/network environment evidence
        ↓
operated evidence under representative traffic and failure
```

Each level answers different questions. The semantic policy evaluator can prove that the Atlas rule model is internally consistent; it cannot prove that an installed CNI enforces NetworkPolicy. A kind cluster can prove one local implementation; it cannot certify a managed cloud load balancer or multi-zone route design.

## Safety boundary

Networking labs can alter routes, filters, DNS behavior, certificates, and listeners. The default lane changes only local files and loopback processes. The optional cluster lane must use a disposable environment.

Before any privileged experiment, define:

- the exact namespace or network namespace in scope;
- the expected process and interface inventory;
- a rollback command tested before the fault;
- a second management path if the experiment can remove connectivity;
- a capture filter and retention rule for packet data;
- an abort condition.

Do not apply default-deny policy, host firewall rules, or Gateway changes to a shared cluster as an exploratory step.

## Initial diagnostic

Answer these without consulting later chapters:

- Why can a Ready Pod still be unreachable from another Node?
- Why does a ClusterIP usually not appear in `ip addr`?
- Which controller publishes Service endpoints, and which component forwards packets to them?
- When does a NetworkPolicy begin isolating a Pod?
- What does an `Accepted=True` HTTPRoute fail to prove?
- Why must an edge proxy replace rather than trust a client-supplied forwarding header?
- Why can a successful IPv4 request not establish dual-stack correctness?
- Why can an open TCP connection still fail to prove HTTP/2 or gRPC compatibility?

The point is not to score yourself. The answers reveal which layer you instinctively blame. This course replaces layer preference with transition-based diagnosis.

## Orientation deliverable

Create a one-page ledger containing:

- the three paths above;
- every address domain involved;
- expected translation points;
- the authority that owns each transition;
- evidence currently available;
- evidence still missing;
- the strongest claim you are willing to make before Module 1.

Proceed only when the Course 4 handoff remains byte-identical and another learner can use your ledger to say where CNI, Service, DNS, NetworkPolicy, Gateway, TLS, and egress evidence will attach.
