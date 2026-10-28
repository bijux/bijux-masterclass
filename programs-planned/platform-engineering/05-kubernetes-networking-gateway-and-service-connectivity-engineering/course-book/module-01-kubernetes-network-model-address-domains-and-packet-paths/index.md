# Module 1 — Kubernetes network model, address domains, and packet paths

A Kubernetes networking incident rarely begins with a precise statement. It begins with “the Pod is unreachable,” “the Service is broken,” or “the ingress times out.” Those sentences compress several independent transitions into one symptom.

The first durable skill in this course is to expand the symptom into a packet path before selecting a tool.

> Which address belongs to which domain, which component owns each transition, and where is the earliest point at which desired and observed behavior diverge?

## Learning outcomes

By the end of this module, you can:

- distinguish loopback, Pod, Node, Service, edge, and external address domains;
- draw direct, cross-Node, Service, and public packet paths in both directions;
- separate control-plane declarations from data-plane packet handling;
- use longest-prefix routing, return-path analysis, and MTU budgets to explain failures;
- treat IPv4 and IPv6 as separate paths requiring separate evidence;
- identify where NAT changes address evidence without creating authenticated identity;
- build a transition ledger that guides diagnosis rather than merely documenting architecture.

## The network model is a set of responsibilities

Kubernetes does not require one universal packet implementation. A cluster may use routed Pod prefixes, an overlay tunnel, cloud-native interfaces, eBPF forwarding, kube-proxy rules, a user-space proxy, or a combination. The durable model is therefore expressed as responsibilities rather than a particular command output.

A functioning cluster normally needs these properties:

1. Every Pod network namespace receives the intended interfaces, addresses, routes, and DNS configuration.
2. Pod addresses are unique within the address domain in which the cluster expects them to be routable.
3. Pods can reach the destinations required by the workload contract.
4. Nodes and network devices know how to forward traffic to remote Pod addresses, directly or through encapsulation.
5. Return traffic can find a valid reverse path.
6. Service destinations can be translated or forwarded to eligible endpoints by the selected data plane.
7. Policy enforcement occurs at known observation points.
8. packet size, fragmentation, and encapsulation behavior remain valid end to end.

Notice what is absent: Kubernetes does not promise that Pod addresses are durable identity, publicly reachable, or bound to physical interfaces. It does not promise that a ClusterIP appears as a host address. It does not guarantee symmetric routing merely because the forward path exists.

## Address domains

Treat every address as belonging to an ownership domain. The same numeric shape—an IPv4 address, for example—does not imply the same semantics.

| Domain | Typical owner | Meaning | Common diagnostic mistake |
|---|---|---|---|
| Loopback | network namespace | local to one namespace | expecting another Pod to reach `127.0.0.1` |
| Pod | CNI/IPAM and cluster routing | endpoint address for one sandbox or interface | treating it as durable identity |
| Node | host/cloud network | address used to reach a machine | confusing Node reachability with Pod reachability |
| Service | Kubernetes Service data plane | virtual destination mapped to eligible endpoints | searching for it on a normal interface |
| Edge/public | Gateway/load balancer/DNS owners | externally reachable authority | assuming source address is preserved |
| External dependency | another platform or provider | address outside workload ownership | allowing an entire CIDR because one hostname resolved there |

An address-domain inventory should include prefix, owner, allocation method, routing scope, translation points, reuse rules, and evidence source. Course 5 stores the Atlas inventory in `capstone/architecture/address-domains.yaml`.

### Loopback

Containers in the same Pod normally share one network namespace, so they share loopback and the Pod interfaces. Once the sandbox exists, communication over `127.0.0.1` does not traverse the CNI data path, Service plane, cluster DNS, or NetworkPolicy path in the usual way. This is why sidecars can communicate locally even while cross-Pod networking is broken.

### Pod addresses

A Pod address identifies a network attachment at a point in time. Pods are replaceable, addresses may be reused, and the same workload identity can appear at a different address after rescheduling. Use Pod addresses for routing and diagnostics, not durable domain authorization.

### Node addresses

Node addresses belong to the host or cloud network. An overlay often uses Node addresses as outer tunnel endpoints while carrying Pod-addressed packets inside. A routed design may advertise Pod prefixes through Node or fabric routes. In both cases, Node reachability is a prerequisite, not proof, of Pod reachability.

### Service addresses

A ClusterIP is a stable virtual destination interpreted by the Service data plane. It is normally not a conventional host address. Depending on the implementation, packet handling may occur through nftables, iptables, IPVS, eBPF, a proxy, or cloud infrastructure. “I cannot find the ClusterIP in `ip addr`” is therefore expected, not diagnostic evidence.

### Edge and external addresses

Public DNS, cloud load balancers, Gateway listeners, NAT, proxies, and external dependencies introduce addresses outside the Pod/Node/Service domains. They may translate source or destination addresses, terminate TLS, or add metadata. Every translation must be recorded because downstream logs may otherwise be mistaken for original network identity.

## Canonical packet paths

A path must be drawn in both directions. Many incidents are failures of the return path, not the request path.

### Same Pod

```text
container A socket
→ shared network namespace
→ loopback or Pod interface
→ container B socket
```

After sandbox creation, no Service, DNS, or cross-Node routing is required. If this path fails, investigate listening sockets, address binding, protocol, process state, and local firewall behavior before blaming the cluster network.

### Same Node, different Pods

```text
source Pod
→ source veth/interface
→ host-side attachment or datapath
→ destination attachment
→ destination Pod
```

The path may cross a bridge, routed interface, eBPF program, or other local data plane. Check source route selection, neighbor state, policy hooks, and destination listening state.

### Different Nodes

```text
source Pod
→ source Node datapath
→ underlay route or overlay encapsulation
→ destination Node datapath
→ destination Pod
```

This path introduces Node reachability, Pod-prefix ownership, tunnel endpoints, encapsulation overhead, cloud route or security controls, and reverse-path behavior. A Pod can be Ready because its local probe succeeds while this path is broken.

### Service destination

```text
client
→ Service virtual destination
→ Service data-plane lookup
→ eligible endpoint selection
→ endpoint packet path
→ backend Pod
```

Three states must agree:

1. the Service definition;
2. EndpointSlice membership and conditions;
3. programmed data-plane state on the traffic-handling node or device.

A correct Service selector proves only selector intent. It does not prove readiness, endpoint publication, or forwarding convergence.

### Public Gateway destination

```text
client resolver and route
→ external listener or load balancer
→ TLS and Gateway listener
→ Route match and backend reference
→ Service data plane
→ eligible Pod
```

The path adds certificate identity, HTTP authority, route attachment, cross-namespace authorization, forwarding-header trust, backend protocol, and possibly cloud translation. A public `200` proves that one request traversed one path; it does not prove negative policy, dual stack, failover, or every endpoint.

## Route selection and the return path

IP routing chooses the most specific matching route, then applies metric and policy rules. Kubernetes incident analysis benefits from this ordinary Linux rule.

Suppose a Pod has:

```text
10.42.0.0/16  via cni0
10.42.7.0/24  via tunl0
0.0.0.0/0     via 10.0.0.1
```

Traffic to `10.42.7.18` follows the `/24`, not the broader `/16` or default route. A stale narrow route can therefore override a valid broad route.

Do not stop after proving the source route. At the destination, ask how the reply returns to the source address actually observed. NAT, asymmetric fabric paths, reverse-path filtering, or missing Pod-prefix routes can make the SYN arrive while the SYN-ACK disappears.

Useful evidence includes:

- route lookup for the exact destination from the relevant namespace;
- interface and neighbor state;
- captures at source Pod, source Node, destination Node, and destination Pod;
- the source address visible at each point;
- counters on the enforcing or forwarding component.

## MTU is an end-to-end budget

A successful TCP handshake uses small packets. Larger payloads may fail when encapsulation reduces the available packet size and Path MTU Discovery is blocked or misconfigured.

A simple budget is:

```text
Pod MTU ≤ smallest underlay MTU − encapsulation overhead
```

The exact overhead depends on IPv4 versus IPv6 and the tunnel or encryption method. Symptoms include:

- small requests succeed while large responses stall;
- one Node pair fails because its underlay MTU differs;
- IPv4 succeeds and IPv6 fails, or the reverse;
- retransmissions occur without application errors;
- lowering MSS appears to “fix” the path.

Before changing application timeouts, test with controlled packet sizes and inspect interface MTUs, tunnel configuration, ICMP behavior, and captures. The course model in `capstone/atlas_net/mtu.py` calculates bounded budgets; it does not replace measurement in a real path.

## Dual stack is a matrix, not a checkbox

A dual-stack Service or Pod does not create one combined path. It creates at least two address-family paths, each with separate allocation, routing, DNS, policy, translation, and observation.

A useful matrix includes:

```text
client family × DNS answer family × listener family × Service family
× endpoint family × policy family × egress family
```

Happy Eyeballs behavior can hide an IPv6 outage by rapidly falling back to IPv4. A successful user request may therefore coexist with a completely broken IPv6 path. Test each family explicitly and record which family was selected.

## NAT changes evidence, not authority

NAT rewrites source or destination addresses and creates state. It can preserve reachability while obscuring the original source. It can also introduce port exhaustion and return-path dependency.

Network source identity must be kept separate from:

- a forwarding header supplied by a trusted proxy;
- a workload identity established cryptographically;
- an authenticated application principal;
- a tenant or domain authorization decision.

A Pod IP or preserved client IP can be useful evidence. It is not a durable authorization credential.

## A transition ledger for diagnosis

For each path, build a table like this:

| Transition | Desired state | Owner | Observed evidence | Negative control |
|---|---|---|---|---|
| Pod attachment | address and routes installed | runtime + CNI | namespace interfaces, CNI state | attachment absent after DEL |
| cross-Node route | remote Pod prefix reachable | CNI/fabric/cloud | route lookup and capture | unrelated prefix denied |
| Service membership | Ready endpoints published | endpoint controller | EndpointSlice | unready Pod excluded |
| Service forwarding | current generation installed | proxy/eBPF/cloud plane | rules/maps/metrics | removed endpoint not selected |
| DNS | name maps to intended Service | CoreDNS and resolver | exact query and answer | unknown name returns bounded failure |
| policy | intended flow allowed, others denied | policy controller/data plane | policy verdicts and negative probes | unauthorized namespace denied |
| Gateway | Route attached to listener | Gateway controller | conditions and observed generation | unauthorized Route rejected |
| TLS | client authenticates expected name | certificate and listener owners | chain, SAN, SNI, handshake | wrong hostname rejected |

The diagnostic rule is simple:

> Find the earliest transition for which desired state is correct but observed state or the expected negative control is absent.

This avoids beginning every incident with whichever tool or layer is most familiar.

## Worked investigation — three Ready Pods, one unreachable

The Atlas API has three Ready Pods. Requests through the Service sometimes fail. EndpointSlices contain all three addresses. The Service rules appear current.

A per-endpoint test shows that the failing Pod is reachable from its own Node but not from another Node. The destination Node capture sees no encapsulated traffic for that Pod prefix. Route inspection on the source Node shows a more-specific stale route pointing to a removed tunnel endpoint.

The earliest failed transition is cross-Node forwarding. Readiness was truthful for the local probe. Endpoint publication was correct. The Service data plane selected a valid endpoint. The fault was a stale route below the Service layer.

The repair is not to remove the Pod from readiness or recreate the Service. It is to reconcile the route owner, verify the reverse path, and test that stale routes are removed after Node or attachment lifecycle changes.

## Capstone increment

Module 1 uses:

- `capstone/architecture/address-domains.yaml`;
- `capstone/architecture/packet-paths.yaml`;
- `capstone/atlas_net/routing.py`;
- `capstone/atlas_net/mtu.py`;
- `capstone/scripts/packet_path_lab.py`.

The lab produces a transition ledger and route/MTU evidence. The model is deliberately implementation-neutral. Later modules attach concrete CNI, Service, DNS, policy, and Gateway owners to these transitions.

## Stateful forwarding changes the meaning of time

Packet-path diagrams often look stateless: a packet enters one interface, a route is selected, policy is checked, and the packet leaves another interface. Real service paths usually contain state. Connection tracking, proxy connection pools, NAT mappings, neighbor caches, DNS caches, and load-balancer backend tables all remember earlier observations.

This matters during change. Suppose an endpoint is removed at 12:00:00. New connections created after all data planes converge should no longer select it. A TCP connection created at 11:59:55 may continue because the connection-tracking entry already binds that flow to the old destination. A packet capture that sees traffic to the removed address is therefore incomplete evidence until you identify whether the flow is new or established.

A useful incident record includes four clocks:

1. when desired state changed;
2. when the controller published new observed state;
3. when each data-plane instance programmed the change;
4. when each client connection was created.

Without those clocks, endpoint withdrawal, DNS expiration, policy propagation, and certificate rotation can all look random.

### Conntrack is not a routing table

Routing decides where a packet would go under current route policy. Connection tracking can preserve an earlier translation for an established flow. When diagnosing a Service, compare a new five-tuple with an existing one. Reusing the same keep-alive connection can hide a repaired backend-selection path; opening only new connections can hide disruption to long-lived streams.

The same distinction appears at L7. A Gateway may keep an upstream HTTP/2 connection after Route or endpoint state changes. The Kubernetes object can be current while an older pooled connection remains in use. Release tests need both connection classes.

## Asymmetric paths require separate forward and reverse proofs

A forward path and return path can use different Nodes, interfaces, NAT states, or policy domains. Asymmetry is not automatically wrong, but every stateful enforcement point must tolerate it.

Common asymmetry sources include:

- external load balancers selecting one Node while the backend replies through another path;
- `externalTrafficPolicy` changing whether source NAT occurs;
- policy routing selecting a different table for the reply source;
- cloud routes advertising Pod prefixes through several Nodes;
- multi-homed Nodes choosing a source address the peer cannot route;
- IPv4 and IPv6 following different gateways;
- direct-server-return or eBPF load-balancing designs.

The diagnostic question is not merely “can the source reach the destination?” It is:

```text
Which source address leaves each hop?
Which component owns the reverse route for that source?
Which stateful device expects the reply to traverse it?
```

A SYN visible at the destination and no SYN-ACK visible at the source narrows the search. Capture the reply at the destination namespace, destination Node, source Node, and source namespace. The first point where it disappears identifies a much smaller set of owners.

## Build evidence by vantage point

A strong packet-path dossier records observations at several layers rather than collecting many commands from one place.

| Vantage point | Useful question | Evidence limit |
|---|---|---|
| Kubernetes API | What was declared and observed by controllers? | does not prove packet handling |
| source process | Which name, address, protocol, and timeout did the caller use? | does not prove kernel path |
| source namespace | Which route and source address were selected? | does not prove remote delivery |
| source Node | Was policy, NAT, encapsulation, or Service translation applied? | does not prove destination acceptance |
| destination Node | Did the outer and inner packet arrive? | does not prove application read |
| destination namespace | Did the transport reach the socket? | does not prove application correctness |
| application | Was the request accepted and answered? | one success does not prove negative controls or failover |

The minimum useful observation is the earliest fact that contradicts the expected transition ledger. More commands are not automatically better evidence. A packet capture without the expected path, timestamp, address family, and connection identity can create more ambiguity than it removes.

## Separate reachability, identity, and authority

A route can make a destination reachable. TLS can authenticate a peer name. A workload-identity system can authenticate a service account. Application authorization can decide whether the caller may perform an operation. These are different properties.

Network engineers often overclaim from address evidence. A packet arriving from a Pod CIDR does not prove which workload sent it if addresses are reusable or spoofing controls are unclear. A request entering through the expected Gateway does not prove the original user unless the forwarding metadata is produced by a trusted hop and validated by the application. NetworkPolicy can reduce reachable peers; it does not make every remaining request authorized.

Throughout the course, write these as separate ledger entries:

```text
Reachability: packet can traverse the intended path.
Peer identity: the intended peer is authenticated.
Request authority: the authenticated principal may perform the action.
```

Keeping them separate prevents a connectivity repair from silently weakening security.

## Transition

Module 1 established the path model. Module 2 studies the first cluster-owned transition on most Pod paths: creation, verification, recovery, and deletion of the Pod network attachment through CNI and IPAM.
