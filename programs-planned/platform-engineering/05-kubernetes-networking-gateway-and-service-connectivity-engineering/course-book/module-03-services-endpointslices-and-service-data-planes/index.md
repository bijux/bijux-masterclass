# Module 3 — Services, EndpointSlices, and Service data planes

A Kubernetes Service creates a stable destination for a changing backend population. It does not itself proxy packets, prove that Pods are Ready, or guarantee that every Node has programmed the latest endpoint set.

The engineering question is:

> How do Service identity, endpoint membership, endpoint eligibility, and forwarding state converge—and how do we identify which of those contracts failed?

## Learning outcomes

By the end of this module, you can:

- distinguish a Service object from EndpointSlices and data-plane state;
- explain how readiness and termination affect endpoint eligibility;
- compare common Service implementations without assuming one tool output;
- reason about ClusterIP, headless, selectorless, NodePort, and LoadBalancer Services;
- evaluate traffic policy, session affinity, and locality as availability decisions;
- diagnose stale endpoint programming and connection-lifetime effects;
- define release evidence that records both desired endpoint state and programmed generation.

## A Service has identity; EndpointSlices have membership

A Service defines a stable name, virtual address or discovery contract, ports, and selection intent. For a selector-based Service, controllers observe Pods and publish EndpointSlices representing backend addresses, ports, and conditions.

That produces at least three independent states:

1. **Service definition** — stable identity, selector, port mapping, traffic policy, address families.
2. **EndpointSlice state** — current backend membership and conditions.
3. **Data-plane state** — rules, maps, proxies, or cloud configuration that actually handle traffic.

A release proof must inspect all three. If only the Service YAML is correct, the system may still have zero endpoints. If EndpointSlices are correct, one Node may still be forwarding according to an older generation.

## Membership is not eligibility

A Pod may match the Service selector but not be eligible for normal traffic. Readiness, deletion, and endpoint conditions influence publication and selection.

Course 4 defined the Atlas readiness contract. Course 5 preserves it: the network must not reinterpret “process exists” as “endpoint may receive ordinary traffic.”

Important endpoint concepts include:

- **ready** — usable for normal traffic under the intended policy;
- **serving** — still capable of serving, particularly during termination scenarios;
- **terminating** — endpoint is being removed;
- topology metadata and hints used by locality-aware data planes.

Controllers and implementations evolve, so record the exact API version and observed conditions. During graceful shutdown, measure the timeline:

```text
Pod deletion requested
→ readiness becomes false
→ EndpointSlice condition changes
→ data plane stops selecting endpoint for new traffic
→ existing connections drain or terminate
→ process exits
```

If the process exits before endpoint withdrawal converges, clients can be sent to a dead backend. If endpoint withdrawal occurs too early, capacity can drop before the Pod drains useful work.

## Port mapping is part of the contract

A Service port maps a stable client-facing port to a backend `targetPort`. Named target ports reduce accidental coupling to a numeric container port and allow different workloads to expose the same semantic port name.

A correct mapping must agree across:

- Service `port` and protocol;
- `targetPort` name or number;
- container port declaration where used for readability/tooling;
- EndpointSlice port name and protocol;
- application listening socket;
- Gateway backend protocol expectations.

A named port cannot prove that the application speaks HTTP, HTTP/2, or gRPC. It prevents some mismatches; protocol integrity still needs runtime evidence.

## Service virtual destination implementations

The same Service API can be implemented through different data planes.

### iptables or nftables rule programming

Rules translate or steer the virtual destination to endpoints. Diagnosis requires inspecting the correct table, chain, family, and rule generation. Absence from iptables is not evidence of failure if the cluster uses nftables or eBPF.

### IPVS

IPVS represents virtual services and real servers in kernel state. It has different observability and connection behavior from rule-based NAT.

### eBPF service data plane

eBPF implementations may replace kube-proxy and store Service/endpoint state in maps. Their diagnostics, update behavior, and source-translation rules are implementation-specific.

### user-space or cloud implementation

A proxy process or cloud load balancer may handle part of the path. The Kubernetes objects remain desired state; the external system’s observed configuration becomes another proof object.

The course deliberately avoids teaching “look for this exact iptables chain” as the Service mental model. First identify the implementation and its ownership boundary.

## EndpointSlice scale and generations

EndpointSlices partition endpoint data so large backend sets do not require one enormous object. Multiple slices can represent one Service. Consumers must combine all relevant slices, handle additions/removals, and avoid assuming object order.

A useful data-plane record includes the generation or resource versions of endpoint state it has consumed. Without that, “rules look correct” cannot establish whether they reflect the latest membership.

The Atlas semantic model assigns a programmed generation to Service data-plane state. The lab can therefore create the important incident shape:

```text
EndpointSlice generation N+1 is correct
Node A programs N+1
Node B remains on N
```

That is a convergence failure, not a selector failure.

## Existing connections and endpoint removal

Removing an endpoint from desired state normally prevents new selections after convergence. Existing TCP connections may continue because connection tracking or proxy state already binds them to a backend. Whether they drain, reset, or outlive endpoint removal depends on protocol, implementation, and process shutdown.

Do not test endpoint withdrawal by issuing only new short connections. Include:

- a long-lived connection established before readiness changes;
- new connections during withdrawal;
- endpoint and data-plane generation timestamps;
- backend process exit time;
- error behavior observed by clients.

## Headless Services

A headless Service (`clusterIP: None`) does not provide the ordinary virtual ClusterIP. DNS commonly returns endpoint addresses directly. This is useful when clients need per-instance identity or perform their own discovery and balancing.

It transfers responsibility to clients:

- handling multiple addresses;
- caching and refresh;
- endpoint changes;
- ordering and failure;
- TLS identity where addresses represent instances.

A headless Service is not “a faster ClusterIP.” It is a different ownership model.

## Selectorless Services

A Service without a selector can be paired with manually or externally managed EndpointSlices. This can bridge Kubernetes clients to endpoints owned elsewhere.

Because endpoint publication is no longer derived from Pods, the endpoint publisher becomes an authority boundary. Review:

- who may create or update the slices;
- whether addresses and ports are validated;
- how health and lifecycle are represented;
- how stale endpoints are removed;
- whether the Kubernetes API proxy is allowed to forward to them;
- how tenant boundaries are preserved.

Selectorless Services are useful, but they should not become a generic escape hatch for external dependencies.

## NodePort and LoadBalancer

A NodePort exposes a port on Nodes according to the implementation. A LoadBalancer Service requests external infrastructure, usually in addition to a NodePort or equivalent backend path.

These resources answer “how can external traffic reach a Service?” They do not provide the complete L7 ownership and route model of Gateway API. Course 7 will place Gateway listeners and HTTP routes above Service backends.

Cloud load balancers introduce additional observed state:

- provisioned addresses;
- health-check behavior;
- source translation;
- backend registration;
- zone policy;
- controller conditions;
- provider quotas and reconciliation delay.

## Traffic policy and locality

`internalTrafficPolicy` and `externalTrafficPolicy` can restrict endpoint selection to local endpoints. Hard-local behavior can preserve source addresses or avoid cross-Node traffic, but it creates a defined failure mode: a Node with no eligible local endpoint may drop traffic even when remote endpoints are healthy.

Topology-aware distribution and preference features are softer: they prefer nearby endpoints while retaining fallback under the supported semantics. Course 6 studies these in detail.

The decision must include capacity and failure domains. Locality that lowers median latency can increase tail failure during uneven placement or zone loss.

## Session affinity is bounded stickiness

`ClientIP` affinity attempts to keep a client source mapped to one backend for a bounded period. It is not durable session ownership, tenant identity, or failover state.

NAT can collapse many users behind one source address, creating a hotspot. Backend removal or timeout changes the mapping. Stateful applications still need explicit session and consistency design.

## Worked investigation — EndpointSlice is correct, one Node is stale

Atlas has three Ready API endpoints. Clients on Nodes A and C succeed; clients on Node B intermittently reach a terminated Pod address.

Investigation shows:

- Service definition and selector are correct;
- current EndpointSlices no longer contain the terminated address;
- Node A and C data-plane generations match the latest endpoint state;
- Node B’s service map still contains the removed endpoint;
- a controller/agent error on Node B prevented reconciliation.

The earliest failed transition is data-plane programming on Node B. Recreating the Service would obscure the fault. The correct repair restores the Node’s Service agent, verifies convergence to the current generation, and proves the removed endpoint is no longer selected.

## Capstone implementation

Module 3 uses:

- `capstone/atlas_net/services.py` for Service, endpoint, generation, and selection behavior;
- `capstone/atlas_net/locality.py` for hard and preferred locality;
- `capstone/manifests/base/10-api-service.yaml`;
- `capstone/manifests/labs/headless-service.yaml`;
- `capstone/manifests/labs/selectorless-service.yaml`;
- `capstone/scripts/service_convergence_lab.py`.

The loopback laboratory runs real backend processes and removes one backend from eligibility. It proves the local harness’s convergence behavior, not a particular kube-proxy or eBPF implementation.

## Release evidence

A credible Service release records:

- Service identity, families, ports, selectors, and policies;
- current EndpointSlices and endpoint conditions;
- data-plane implementation and generation;
- readiness-withdrawal timeline;
- new and established connection behavior;
- positive and negative reachability tests;
- locality and source-translation behavior;
- unresolved environment-specific claims.

## A Service creates stable naming, not stable backend state

The Service object gives clients a stable identity and port contract while endpoint membership changes. That separation is the feature. It also means the virtual destination has no useful meaning without a current mapping to eligible backends.

The Service CIDR is an address domain owned by the cluster’s Service data plane. It must not overlap Pod, Node, VPN, or external routed prefixes. Overlap can produce routes that capture Service traffic before the intended translation hook, or cause external routers to believe they own a virtual address that exists only inside the cluster.

A Service release should record:

- cluster IP families and allocation policy;
- port names, numbers, and protocols;
- selector or explicit endpoint ownership;
- endpoint eligibility rules;
- internal and external traffic policy;
- session affinity where used;
- data-plane implementation and version;
- health-check and source-translation behavior;
- convergence and rollback evidence.

## Endpoint conditions must be read as a timeline

EndpointSlice conditions are not independent labels. During normal operation and termination they describe a transition. An endpoint may be terminating while still serving an existing connection, or not ready for ordinary new traffic while the process performs bounded drain work.

The exact interpretation depends on the consumer and Kubernetes version, so tests should observe the installed implementation rather than assuming that every proxy uses every condition identically. The durable invariant is that the release defines which traffic population may reach a terminating endpoint and for how long.

Build a timeline with:

```text
T0 deletion or readiness change requested
T1 Pod condition updated
T2 EndpointSlice observed generation changes
T3 each node/proxy acknowledges the new generation
T4 new connections stop selecting the endpoint
T5 established connections finish or are terminated
T6 process exits
```

If T6 precedes T4, clients can receive new connections to a dead process. If T2 never occurs, the problem belongs to endpoint publication. If T2 occurs but one Node remains on an earlier generation, the problem belongs to the data-plane reconciler.

## Selection algorithms operate on flows, not abstract requests

A Service implementation usually selects a backend when it creates or observes a new flow. The lifetime of that decision depends on transport and proxy behavior:

- UDP has no connection handshake, but implementations may keep affinity or tracking state;
- TCP selection commonly persists for the connection lifetime;
- HTTP/1.1 keep-alive carries several requests over one TCP connection;
- HTTP/2 and gRPC multiplex many streams over one long-lived connection;
- a Gateway can pool backend connections independently of client connections.

This is why “send 1,000 HTTP requests” may exercise only a few backend selections. To test distribution or endpoint withdrawal, control connection reuse and record both request and transport identities.

Session affinity adds another state layer. `ClientIP` affinity is based on the source address visible to the Service data plane, which may be a NAT address shared by many users. It cannot substitute for user session ownership or tenant routing.

## External traffic adds health-check and source-address contracts

A LoadBalancer Service usually causes a controller to configure provider infrastructure, but the external device has its own backend registration and health model. `externalTrafficPolicy: Local` can preserve the client source address and avoid an extra cross-Node hop, while making Nodes without local eligible endpoints unable to serve traffic.

The release must align:

- load-balancer backend registration;
- health-check target and semantics;
- Pod placement and readiness;
- Node eligibility;
- source NAT behavior;
- return routing;
- zone policy;
- draining during endpoint and Node removal.

A health check that only proves a Node port accepts TCP can keep a Node registered after the last local application endpoint disappears. Conversely, a health check tied too closely to one Pod can remove useful Node capacity during a local rollout. Measure the whole chain.

## Data-plane replacement is a migration, not a toggle

Moving from one Service implementation to another—such as kube-proxy rules to eBPF replacement—changes live forwarding state. A safe migration needs to prove:

1. old and new agents do not fight over the same hook or leave conflicting state;
2. existing connections behave as declared;
3. Service, NodePort, health-check, source-address, and locality semantics remain compatible;
4. IPv4 and IPv6 both work;
5. rollback removes new state and restores old behavior;
6. observability and incident commands are updated;
7. policy enforcement ordering remains understood.

The API objects can remain unchanged while the packet path changes substantially. Treat the data-plane generation and implementation identity as release evidence.

## Transition

Module 3 establishes stable Service identity and dynamic endpoint selection. Module 4 examines how clients discover that identity, how resolver behavior changes the query, and why DNS correctness and Service availability are separate claims.
