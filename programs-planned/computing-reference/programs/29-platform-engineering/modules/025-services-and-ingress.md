---
module_id: PLAT-025
program: Platform Engineering
level: 1
module_number: 25
title: Services and Ingress
status: complete
last_verified: 2026-09-02
---

# Services and Ingress

## One-Page Review

### Governing question

How should a platform connect changing workload endpoints to stable names and controlled internal or external traffic while preserving protocol, ownership, topology, identity, encryption, policy, and failure evidence?

### Essential definitions

- A **Service** is a Kubernetes resource that provides stable discovery and, for most types, virtual-IP forwarding to a changing set of network endpoints.
- An **EndpointSlice** groups backend addresses by address family, protocol, port, and Service, with conditions and topology used by data-plane consumers.
- A **selector** is a label query through which the control plane derives endpoints for a Service; a selector match is not an authentication or authorization decision.
- A **headless Service** has `clusterIP: None`, supplies endpoint discovery without platform virtual-IP load balancing, and shifts selection behavior to clients.
- **ClusterIP**, **NodePort**, and **LoadBalancer** are Service exposure types; later types normally build on earlier forwarding behavior.
- **Ingress** is the stable but frozen Kubernetes HTTP/HTTPS routing API implemented by an Ingress controller and selected through an IngressClass.
- **Gateway API** is a role-oriented family including GatewayClass, Gateway, Route, and ReferenceGrant resources with typed routing and status.
- A **listener** is an address/port/protocol/TLS attachment point on a Gateway; a **route** attaches matching and forwarding rules to an accepted parent.
- **traffic policy** states strict local-versus-cluster routing behavior; **traffic distribution** expresses a preference such as same-zone routing where supported.
- A **ReferenceGrant** is target-namespace consent for specified cross-namespace Gateway API references; it mitigates confused-deputy behavior.

### Central model, mechanism, or theorem

Model a connectivity contract as $N=(C,E,D,R,B,T,A,P,O,L,X)$: consumer and protocol contract $C$, endpoint derivation $E$, discovery $D$, routing/data plane $R$, boundary/exposure $B$, topology policy $T$, authentication/authorization/encryption $A$, network policy $P$, observability $O$, lifecycle $L$, and exceptions $X$. A request is usable only if name/address resolution, route attachment, endpoint eligibility, data-plane programming, transport, policy, and application handling all succeed. A Service selector, ready endpoint, accepted route, or TLS handshake proves only its own layer.

### Critical invariants

- Service selectors uniquely target intended workload labels and every selected port has one unambiguous protocol and target-port contract.
- Endpoint readiness, serving, and terminating are interpreted separately; terminating endpoints do not silently count as normal future capacity.
- DNS names and Service virtual IPs are discovery identities, not workload authentication or tenant authorization.
- Exposure type is chosen from consumer reachability and protocol; public reachability always has explicit owner, allowed sources, identity, encryption, rate, and abuse controls.
- Headless discovery is used only when clients can handle multiple changing addresses, connection balancing, stale DNS, and endpoint failure.
- Ingress always names its class and uses portable path/TLS behavior unless an implementation-specific contract is declared and tested.
- Gateway, listener, route, backend, certificate, and namespace owners are distinct; cross-namespace references require target-side consent.
- TLS termination and every subsequent plaintext or encrypted hop are documented; certificate identity, hostnames, rotation, and failure are observed.
- NetworkPolicy ingress and egress are independently enforced by a supported implementation and do not substitute for service routing or application authorization.
- Changes preserve drain, connection lifetime, DNS/cache behavior, dual-stack reachability, rollback, and current route/endpoint status evidence.

### Common failures

Using broad selectors; targeting the wrong named port; assuming `Running` pods are endpoints; publishing not-ready endpoints accidentally; treating ClusterIP as a security boundary; using NodePort without perimeter ownership; expecting LoadBalancer type to standardize provider features; using client-IP affinity as identity; choosing headless discovery for naive clients; omitting IngressClass; relying on implementation-specific annotations silently; terminating TLS while exposing an unprotected backend hop; permitting cross-namespace references without consent; allowing all egress; and declaring success from route acceptance without a request test.

### Compact example

An external payments API uses an organization-owned Gateway listener on `payments.example.com:443`, an application-owned HTTPRoute, and a same-namespace ClusterIP Service with a named `https-app` target port. The listener terminates a rotated certificate; the backend hop uses authenticated TLS under a documented policy. The Service selector includes stable application and traffic-track labels. EndpointSlice status shows four normal ready endpoints across three zones, two terminating/serving endpoints retained only for drain semantics, and one unready endpoint. NetworkPolicy allows gateway identity to backend port and restricts backend egress. Route parent status, endpoint status, certificate expiry, data-plane config, synthetic transactions, and user outcomes are observed separately.

### Connections

Retrieve workload readiness, rollout, placement, disruption, and drain from [PLAT-024](024-pods-workloads-and-controllers.md), declarative ownership/status from [PLAT-023](023-kubernetes-declarative-resources.md), runtime and network authority from [PLAT-022](022-runtime-isolation-and-resource-controls.md), image protocol identity from [PLAT-021](021-container-images-as-platform-artifacts.md), and API routing/error contracts from the API and Service Engineering program.

## Governing Question

Which consumers may reach which protocol at which stable identity, how are eligible endpoints selected, where are routing and security decisions enforced, and what evidence locates failure across control plane, data plane, network, and application?

Kubernetes networking separates durable intent from distributed implementation. A Service and its EndpointSlices exist in the API. DNS publishes names. kube-proxy or another data plane programs forwarding. A cloud controller may provision a load balancer. An Ingress or Gateway controller configures protocol-aware edge infrastructure. Network policy constrains connections. The application still authenticates and serves requests.

Each layer can be healthy while the journey fails. Design and diagnosis must preserve the chain rather than treating “the Service is up” as an end-to-end claim.

## Why This Matters

Pod IPs and pod lifetimes change. Clients need stable discovery, and operators need traffic to follow ready replacements during rollout and failure. Services provide that indirection. External exposure adds shared addresses, DNS, certificates, firewalls, routing, providers, and multiple organizational owners.

A small selector mistake can send production traffic to canaries or administrative pods. A readiness error can remove every backend. A local traffic policy can blackhole traffic on nodes without endpoints. A certificate can be correct at the edge while traffic is plaintext across an untrusted network. A NetworkPolicy can permit a path but no route, or a route can exist while policy denies it.

The platform should offer explicit connectivity products—internal service, headless membership discovery, provider load balancer, HTTP route, private gateway, public gateway—rather than exposing every low-level field without an ownership model.

## Prerequisites and Retrieval

Retrieve IP addressing, TCP/UDP/SCTP, DNS, HTTP, TLS, certificates, proxies, load balancing, NAT, routing, firewalls, identity, selectors, pod readiness, EndpointSlices, eventual consistency, and distributed failure.

You should understand client connection pools, keepalive, retries, timeouts, idempotency, health checks, source addresses, IPv4/IPv6, SNI, host/path matching, certificate rotation, and namespace/RBAC boundaries.

## Learning Objectives

After completing this module, you should be able to:

1. define Service selectors, ports, endpoints, discovery, IP-family, and traffic-policy contracts;
2. choose ClusterIP, headless, NodePort, LoadBalancer, ExternalName, Ingress, or Gateway API from consumer and protocol needs;
3. interpret EndpointSlice address types, ports, readiness, serving, terminating, ownership, and topology;
4. design DNS, client balancing, session affinity, source-IP, and connection-drain behavior;
5. configure portable Ingress behavior and explain why the frozen API is not a complete edge platform;
6. separate GatewayClass, Gateway, listener, Route, backend, certificate, and ReferenceGrant ownership;
7. combine routing with TLS, workload identity, NetworkPolicy, rate/abuse controls, and application authorization; and
8. verify control-plane acceptance, data-plane realization, end-to-end traffic, lifecycle, and provider cleanup.

## Core Exposition

### Begin with the consumer and protocol

List consumers: same pod, same namespace, other namespaces, other clusters, corporate networks, partners, browsers, public internet, or provider services. State protocol and connection behavior: TCP, UDP, SCTP, HTTP, HTTPS, gRPC, TLS passthrough, long-lived stream, WebSocket, or custom framing.

Define identity and authorization separately from location. A DNS name and port locate a service. A certificate, workload identity, token, or application credential authenticates a peer. RBAC controls Kubernetes API operations, not ordinary data-plane requests.

Record latency, availability, source-IP, locality, session, timeout, retry, maximum request/connection, bandwidth, and observability requirements. These determine whether a virtual IP, client discovery, L4 balancer, or L7 gateway fits.

### Derive endpoints safely

A Service selector matches pod labels in its namespace. The EndpointSlice controller derives endpoint addresses and named ports for matching pods. Keep selector identity labels stable and disjoint from management or transient status labels. Include a traffic-track label when stable and canary backends need separate Services.

Port fields have distinct roles: `port` is the Service port; `targetPort` is the backend port number or name; `nodePort` is the node-facing allocated/static port for relevant types. Name every multi-port Service port and use consistent app-container port names. A renamed target port can yield missing or incorrect endpoints during mixed revisions.

Services without selectors allow manually or externally managed EndpointSlices. This is a platform-owned integration path: validate addresses, ports, address family, managed-by label, ownership, readiness, lifecycle, and protection against API-server or control-plane endpoint misuse.

### Read EndpointSlices as data-plane inputs

EndpointSlices partition endpoints by address type, protocol, port set, and Service. They scale updates and supply node/zone topology. Consumers must watch all slices for the Service and tolerate replacement, duplication during transitions, and eventual propagation.

`serving` reflects whether the endpoint serves; `terminating` marks deletion; `ready` is generally serving and not terminating, with special behavior for publish-not-ready Services. A terminating endpoint can remain serving during drain, but normal proxies usually avoid it while non-terminating ready endpoints exist.

The following synthetic inventory distinguishes these conditions and address families.

<!-- bijux-verify: {"id":"service-endpoint-eligibility","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"endpoints=7\nserving=6\nnormal_ready=4\nterminating=2\nipv4=5\nipv6=2\nzones=3\n","stderr":""}} -->
```python
endpoints = [
    {"address": "10.0.0.1", "family": "IPv4", "zone": "a", "serving": True, "terminating": False},
    {"address": "10.0.1.1", "family": "IPv4", "zone": "b", "serving": True, "terminating": False},
    {"address": "10.0.0.2", "family": "IPv4", "zone": "a", "serving": False, "terminating": False},
    {"address": "2001:db8::1", "family": "IPv6", "zone": "a", "serving": True, "terminating": False},
    {"address": "2001:db8::2", "family": "IPv6", "zone": "b", "serving": True, "terminating": True},
    {"address": "10.0.2.1", "family": "IPv4", "zone": "c", "serving": True, "terminating": True},
    {"address": "10.0.2.2", "family": "IPv4", "zone": "c", "serving": True, "terminating": False},
]
print(f"endpoints={len(endpoints)}")
print(f"serving={sum(endpoint['serving'] for endpoint in endpoints)}")
print(f"normal_ready={sum(endpoint['serving'] and not endpoint['terminating'] for endpoint in endpoints)}")
print(f"terminating={sum(endpoint['terminating'] for endpoint in endpoints)}")
print(f"ipv4={sum(endpoint['family'] == 'IPv4' for endpoint in endpoints)}")
print(f"ipv6={sum(endpoint['family'] == 'IPv6' for endpoint in endpoints)}")
print(f"zones={len({endpoint['zone'] for endpoint in endpoints})}")
```

The fixture does not model EndpointSlice ownership, port compatibility, publish-not-ready behavior, data-plane propagation, reachability, or application correctness.

### Use ClusterIP as internal stable forwarding

ClusterIP is the default Service type. The control plane allocates one or more virtual IPs and the service proxy/data plane routes to endpoints. The virtual IP is not normally bound to one network interface. Exact implementation—iptables, IPVS, nftables, eBPF, user-space proxy, or provider system—is cluster specific.

ClusterIP is reachability, not isolation. Other pods may reach it unless NetworkPolicy, network segmentation, identity, or application authorization denies them. Namespace-qualified DNS improves naming but does not protect a tenant.

Use named ports and stable service DNS names rather than embedding cluster IPs. Cluster IP fields have mutability constraints and can differ across clusters. Clients must use timeouts, retries appropriate to operation idempotency, and connection re-resolution behavior.

### Choose headless discovery deliberately

A headless Service has no virtual IP or platform proxy. DNS returns endpoint addresses for selector-backed ready endpoints; named ports can produce SRV records. StatefulSets commonly use headless Services for stable pod identities.

The client now owns address selection, balancing, failover, DNS caching, connection pool refresh, and partial failure. Some clients use only the first answer indefinitely. Long TTL or library caching can retain dead endpoints. Headless does not bypass NetworkPolicy or remove the need for identity.

Publish-not-ready addresses supports bootstrap or membership discovery but exposes endpoints before readiness. Use only when the protocol itself manages readiness and cannot bootstrap otherwise. Separate discovery eligibility from user traffic eligibility.

### Understand Service exposure types

**NodePort** exposes a port on node addresses and builds on ClusterIP. It is a low-level integration surface for external load balancers or controlled environments. Every eligible node address, firewall, source policy, and port allocation becomes part of the boundary.

**LoadBalancer** asks an implementation/provider to provision external or internal load-balancing infrastructure, normally building on NodePort/ClusterIP behavior with implementation options. Provider annotations, address allocation, health checks, source ranges, dual stack, lifecycle, cost, and status differ. Model a supported provider profile rather than calling the type portable infrastructure.

**ExternalName** publishes a DNS CNAME-like alias to an external name without proxying. HTTP Host and TLS server-name expectations can differ from the alias, producing failures or unsafe workarounds. It supplies no health, port, identity, or policy verification.

`externalIPs` relies on externally routed addresses and does not allocate them; current Kubernetes guidance deprecates this surface. Prefer owned load-balancer or Gateway integrations.

### Define traffic policy and locality

`externalTrafficPolicy` and `internalTrafficPolicy` express strict cluster-versus-local routing behavior where supported. Local policy can preserve source IP or avoid cross-node hops but can drop traffic on nodes without local ready endpoints and create uneven load.

Traffic distribution expresses preferences such as same-zone/same-node routing under current API and data-plane support. Preference is not guarantee. Topology hints and endpoint zone data depend on complete node labels, balanced capacity, and implementation.

Optimize locality only after protecting availability. Observe requests and errors by client zone, backend zone, node, and endpoint. A zonal outage can require cross-zone traffic; a strict local policy may turn survivable remote capacity into a blackhole.

Session affinity based on client IP is coarse and breaks under NAT, proxies, address changes, scaling, and failure. It is not authentication and does not replace application sessions in shared storage or signed tokens.

### Plan dual-stack behavior

Dual-stack clusters can assign IPv4 and IPv6 Service addresses using `ipFamilyPolicy` and ordered `ipFamilies`. `PreferDualStack` can fall back; `RequireDualStack` fails if unsupported. Providers, CNIs, DNS, load balancers, policies, clients, probes, certificates, and observability must support both paths.

Test A and AAAA resolution and actual connectivity independently. A client may prefer IPv6 and fail slowly before IPv4 fallback. EndpointSlices separate address types. Do not declare dual-stack from two allocated addresses without end-to-end reachability evidence.

### Keep Ingress portable within its limits

Ingress maps HTTP/HTTPS hosts and paths to Service backends. It requires an Ingress controller; creating the object alone creates no data plane. Name `ingressClassName` explicitly so the intended controller claims it. Avoid multiple defaults.

Use `Exact` or `Prefix` path types for portable matching. `ImplementationSpecific` delegates semantics to the controller and must be documented/tested. Host/path precedence, rewrite, regex, timeout, body size, authentication, canary weights, and health behavior often rely on implementation-specific annotations.

Ingress TLS commonly terminates at the controller using a Secret with certificate/key. The API does not standardize the entire certificate lifecycle or backend encryption. Verify SNI/host match, issuer, renewal, Secret access, reload, expiry, cipher/protocol profile, client-to-edge and edge-to-backend hops.

The Ingress API is frozen. It remains supported, but new platform routes should consider Gateway API when its implementations and conformance meet requirements.

### Use Gateway API for role-oriented routing

Gateway API separates infrastructure and application roles. A cluster infrastructure owner selects/installs an implementation and offers GatewayClasses. A gateway owner creates Gateways with addresses and listeners. Application owners attach HTTPRoute or other route types subject to listener policy. Backend owners control Services and cross-namespace consent.

A Route `parentRef` requests attachment. The Gateway listener restricts which namespaces/routes may attach. Route status is reported per parent with conditions such as Accepted and ResolvedRefs. An accepted spec may still lack a programmed or reachable data plane; inspect Gateway/listener/route/backend status together.

HTTPRoute matches hostnames, paths, headers, methods where supported, and applies standardized filters/backends/timeouts according to conformance. Conflicting routes are resolved by specified rules, not manifest order. Multiple owners can share one Gateway without sharing write access to one monolithic object.

Choose only supported Gateway API version/channel and implementation features. Core/extended/implementation-specific support and conformance reports matter. Do not assume every controller implements every filter or protocol.

### Protect cross-namespace references

Cross-namespace routing can become a confused deputy: a route owner might direct privileged gateway traffic to a backend or certificate it does not own. Gateway API requires target-side `ReferenceGrant` for covered cross-namespace references, except route-to-Gateway attachment uses listener policy.

The grant resides in the target namespace and permits specified source group/kind/namespace to reference target kind, optionally name under API rules. Keep grants narrow, inventory their consumers, and revoke when relationships end. Status must not reveal existence of an ungranted target.

ReferenceGrant permits reference; it does not authorize end-user traffic, bypass NetworkPolicy, or prove backend readiness. RBAC and admission constrain who can create grants.

### Separate routing from network policy

NetworkPolicy selects pods and controls allowed ingress and egress connections when the CNI implements it. A pod becomes isolated independently per direction when selected by a policy declaring that direction; allowed rules from applicable policies combine additively.

For a pod-to-pod connection, source egress and destination ingress must both allow it. A Service or Gateway route does not automatically open policy, and policy allowance does not create discovery or routing. Default-deny plus explicit DNS, gateway, dependency, and telemetry paths is a common posture.

NetworkPolicy is generally L3/L4 and has implementation-dependent behavior around NAT, nodes, load balancers, host networking, and unsupported features. Application authentication and authorization remain necessary. Verify effective enforcement with allowed and denied probes from representative identities.

### Design end-to-end TLS and identity

Draw every hop: client to external load balancer, gateway, service data plane, pod, sidecar, and external dependency. For each, state source/destination identity, encryption, certificate authority, SNI, trust roots, client authentication, termination, re-encryption, and plaintext exposure.

Central edge termination simplifies certificate management but gives the gateway plaintext and can leave backend traffic unencrypted. Passthrough preserves end-to-end TLS but reduces L7 routing/observability. Re-encryption creates two authenticated TLS sessions. Choose by threat and protocol, not “TLS enabled.”

Automate issuance and rotation with bounded validity, overlap, rollback, revocation response, and expiry alerting. Never place private keys in route annotations or broad shared namespaces.

### Coordinate readiness, draining, and connections

Pod readiness drives EndpointSlice serving/ready for selector-derived endpoints. When deletion begins, endpoints become terminating and normal readiness excludes them. Data planes and clients update eventually; existing connections can persist.

Termination must stop new application work, drain within grace, and coordinate upstream idle/request timeouts. Removing an endpoint cannot recall requests already sent. Long-lived streams need explicit maximum age, reconnect, and drain signaling.

Load-balancer health checks may target nodes, Service ports, or pod endpoints independently of Kubernetes readiness. Align them without creating a correlated dependency. Observe time from pod readiness/deletion to EndpointSlice, proxy, gateway, DNS/provider, and client behavior.

### Govern public exposure

Public exposure requires hostname/address ownership, DNS, certificate, source policy, DDoS/abuse protection, rate and size limits, authentication, authorization, logging/privacy, vulnerability response, cost, support, and incident authority. A `LoadBalancer` or Route object is only part of that product.

Offer public/private gateway classes and load-balancer profiles with approved providers and policy. Prevent arbitrary annotations from requesting insecure schemes, broad security groups, unsupported protocols, or uncontrolled cost. Bind routes to application owners and inventory every public listener/backend.

### Observe and diagnose by layer

For a failed request, check name resolution; selected address family; listener/address/TLS; route attachment and match; backend reference; Service port; EndpointSlices; endpoint condition/topology; data-plane programming; NetworkPolicy; pod readiness; application logs/traces; and dependency outcome.

Observe DNS success/latency/answers, Service and EndpointSlice propagation, endpoints by ready/serving/terminating/family/zone, connection/error distribution, source preservation, proxy sync, provider status, Gateway listener/route conditions, certificate expiry/handshake, policy denies, HTTP response class, latency, retries, and synthetic tasks.

Status such as LoadBalancer ingress address, Ingress admitted, Gateway Programmed, or Route Accepted is necessary control-plane evidence, not an end-to-end guarantee.

### Test lifecycle and failure

Test selector zero-match/overmatch, named-port mismatch, all-unready backends, termination drain, rolling mixed revisions, node/zone loss, local-policy empty node, stale DNS and connection pools, dual-stack partial failure, provider provisioning/deletion, route conflict, class/controller absence, certificate rotation/expiry, ReferenceGrant removal, network-policy default deny, and controller restart.

Verify cleanup of external addresses, DNS, firewall rules, certificates, health checks, and provider resources after resource deletion. Finalizers and provider controllers can wedge; never remove them without understanding leaked infrastructure and traffic risk.

## Definitions and Notation

Let connectivity contract $N=(C,E,D,R,B,T,A,P,O,L,X)$ have the components defined in the review. Let Service-selected pod set at time $t$ be $S_t=\{p\mid \operatorname{labels}(p)\models q\}$ for selector $q$. Selection alone does not imply readiness or authorization.

For endpoint $e$, let $s(e)$ be serving and $\tau(e)$ terminating. Under normal semantics, ready eligibility is $r(e)=s(e)\land\neg\tau(e)$, subject to special publication configuration and consumer behavior.

Let request path be ordered hops $H=(h_0,\ldots,h_k)$. End-to-end success requires every required resolution, policy, transport, route, and application predicate along $H$; one layer's success is not sufficient.

For topology domains $z$, let request volume $x_z$ and healthy endpoint capacity $c_z$. Same-zone preference is safe only with fallback and overload policy when $x_z>c_z$ or $c_z=0$; the preference itself does not create capacity.

## Mechanisms, Invariants, or Proof Structure

The path is consumer/protocol $\rightarrow$ stable discovery $\rightarrow$ Service/route intent $\rightarrow$ selector or managed endpoints $\rightarrow$ EndpointSlices $\rightarrow$ controller/data-plane programming $\rightarrow$ network policy $\rightarrow$ TLS/identity $\rightarrow$ pod/application $\rightarrow$ response evidence $\rightarrow$ drain, update, or cleanup.

Ingress and Gateway controllers reconcile API resources into implementation-specific proxies, load balancers, DNS, certificates, or routes. Service and EndpointSlice consumers program internal forwarding. These are eventually consistent control loops with independent status and failure.

Invariants are exact selection/ports, condition-aware endpoints, separate discovery and identity, owned exposure, capable headless clients, explicit Ingress class, role-separated Gateway references, documented TLS hops, bidirectional network policy, and lifecycle evidence.

No networking resource proves user success or complete security. End-to-end claims require data-plane, application, identity, policy, dependency, and user evidence.

## Alternatives and Trade-Offs

**Virtual IP versus headless discovery:** VIPs centralize endpoint selection and simplify clients. Headless discovery exposes identity/locality but makes clients handle churn and balancing.

**Cluster versus local traffic policy:** cluster routing maximizes endpoint pool; local routing preserves locality/source properties but can blackhole or imbalance.

**NodePort versus LoadBalancer:** NodePort is primitive and portable at API level but expands node perimeter. LoadBalancer automates provider infrastructure with provider-specific behavior and cost.

**Ingress versus Gateway API:** Ingress is mature and widely implemented but frozen and annotation-heavy. Gateway API provides typed roles and extensibility but requires CRDs, compatible versions, and verified implementation conformance.

**Central versus application-owned gateway:** central ownership standardizes security/cost and shared addresses; dedicated gateways isolate failure and customization at greater cost. Gateway API can split infrastructure and route ownership.

**TLS termination versus passthrough/re-encryption:** termination enables L7 policy and observability; passthrough preserves backend TLS context; re-encryption balances control with two trust relationships.

**Strict default-deny versus permissive migration:** default deny limits lateral movement but requires dependency/DNS inventory. Stage observability and explicit rules without leaving permanent allow-all exceptions.

**Locality versus resilience:** same-zone routing lowers latency/cost, while cross-zone fallback absorbs imbalance/failure. Define both preference and overload behavior.

## Failure Modes and Misconceptions

- **“A Service is a load balancer appliance.”** It is API intent realized by cluster/provider data planes with implementation-specific mechanics.
- **“Selected means healthy.”** Endpoint readiness derives from conditions and publication policy.
- **“ClusterIP is private.”** Reachability scope is not authorization or confidentiality.
- **“LoadBalancer is portable.”** Provider annotations, health, addresses, source behavior, dual stack, and lifecycle differ.
- **“Headless is faster.”** It shifts balancing, caching, retry, and failure handling to clients.
- **“Ingress creates ingress.”** An accepted controller/class implementation must realize it.
- **“TLS on Ingress is end-to-end.”** Backend hops can remain plaintext and unauthenticated.
- **“Accepted Route is reachable.”** Parent, references, programming, endpoints, policy, and application can still fail.
- **“ReferenceGrant grants traffic.”** It grants an object reference, not end-user authorization.
- **“NetworkPolicy is a firewall order.”** Applicable allows combine additively and isolation is per direction.
- **“Session affinity is identity.”** Client IP can represent proxies or many users and changes over time.
- **“Removing an endpoint drains every request.”** Propagation and existing connections require explicit lifecycle design.

## Worked Examples

### Example 1

A selector `app=api` also matches a debug pod. The platform requires `app`, `component`, and stable traffic-track labels, validates template/Service agreement, and removes debug from production endpoints.

### Example 2

A mixed rollout renames container port `http` to `web` while Service `targetPort` remains `http`. New pods produce no matching endpoint port. Compatibility keeps the old name until all consumers migrate.

### Example 3

A headless database Service publishes member addresses. The database client refreshes DNS, validates member TLS identity, handles multiple answers, and never interprets DNS order as leader order.

### Example 4

`internalTrafficPolicy: Local` causes failures on nodes without local endpoints. The team changes to cluster routing until every node has intentional local capacity.

### Example 5

A LoadBalancer is healthy at node checks but every pod is unready. Layered diagnostics distinguish provider health from empty ready EndpointSlices.

### Example 6

An Ingress `ImplementationSpecific` regex behaves differently after controller migration. The platform moves portable routes to Prefix/Exact and versions the remaining controller-specific contract.

### Example 7

An HTTPRoute in `shop` references a Service in `payments`. The payments owner creates a narrow ReferenceGrant; deletion immediately invalidates the reference without revealing other targets.

### Example 8

Edge TLS is valid, but gateway-to-backend traffic crosses an untrusted network in plaintext. Re-encryption with backend identity and restricted NetworkPolicy closes the undocumented hop.

### Example 9

IPv4 succeeds and IPv6 times out. Dual-stack status was green because addresses existed. Independent AAAA, route, policy, endpoint, and transaction tests locate a provider IPv6 path failure.

### Example 10

During drain, long-lived streams stay on a terminating/serving endpoint until a maximum age, receive reconnect guidance, and finish before grace; normal new traffic uses non-terminating endpoints.

## Cross-Program Connections

Networking contributes addressing, DNS, routing, NAT, transport, load balancing, and failure domains. Security contributes identity, TLS, authorization, confused-deputy prevention, network policy, DDoS, and key lifecycle. Distributed systems contributes discovery, eventual propagation, retries, connection pools, and locality.

API engineering contributes HTTP routing, host/path matching, timeouts, errors, versions, and compatibility. Reliability contributes health, drain, failover, observability, synthetic traffic, and incident isolation. Performance contributes connection distribution, cross-zone cost, queues, and capacity.

Platform product engineering contributes supported exposure classes, shared-gateway ownership, provider profiles, and consumer diagnostics. Finance contributes public-address, gateway, load-balancer, egress, and cross-zone cost.

## References

- Kubernetes Project, [*Service*](https://kubernetes.io/docs/concepts/services-networking/service/), current documentation retrieved September 2, 2026. Selectors, ports, ClusterIP, NodePort, LoadBalancer, ExternalName, headless discovery, traffic policy/distribution, affinity, and exposure.
- Kubernetes Project, [*EndpointSlices*](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/), current documentation retrieved September 2, 2026. Slice grouping, address types, ports, ready/serving/terminating, topology, ownership, and custom management.
- Kubernetes Project, [*DNS for Services and Pods*](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/), current documentation retrieved September 2, 2026. Service and headless A/AAAA records, SRV named-port records, pod DNS, search paths, and identity limits.
- Kubernetes Project, [*IPv4/IPv6 Dual-Stack*](https://kubernetes.io/docs/concepts/services-networking/dual-stack/), current documentation retrieved September 2, 2026. IP family policy/order, Service allocation, headless behavior, and provider prerequisites.
- Kubernetes Project, [*Ingress*](https://kubernetes.io/docs/concepts/services-networking/ingress/), current documentation retrieved September 2, 2026. Frozen API status, controller/class, host/path rules, path types, TLS, default backends, and implementation differences.
- Kubernetes Project, [*Network Policies*](https://kubernetes.io/docs/concepts/services-networking/network-policies/), current documentation retrieved September 2, 2026. Independent ingress/egress isolation, additive allow rules, selectors, CIDRs, ports, and implementation limits.
- Gateway API, [*HTTPRoute*](https://gateway-api.sigs.k8s.io/reference/api-types/httproute/), current Standard-channel documentation retrieved September 2, 2026. Parents, hostnames, matches, filters, backend references, attachment, merging, and per-parent status.
- Gateway API, [*HTTP Routing*](https://gateway-api.sigs.k8s.io/guides/user-guides/http-routing/), current guide retrieved September 2, 2026. Gateway/listener/HTTPRoute composition, host/path/header matching, multiple routes, and backends.
- Gateway API, [*ReferenceGrant*](https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/), current Standard-channel documentation retrieved September 2, 2026. Target-side cross-namespace consent, from/to structure, runtime revocation, status confidentiality, and confused-deputy mitigation.
- Gateway API, [*Security Model*](https://gateway-api.sigs.k8s.io/docs/concepts/security/), current documentation retrieved September 2, 2026. Infrastructure, gateway, route, and backend roles; listener attachment; namespace trust; certificate and backend references.
- Gateway API, [*API Specification*](https://gateway-api.sigs.k8s.io/reference/spec/), current specification retrieved September 2, 2026. Resource schemas, conditions, conformance levels, route matching, conflict precedence, policy, and reference rules.
- Kubernetes Project, [*Virtual IPs and Service Proxies*](https://kubernetes.io/docs/reference/networking/virtual-ips/), current documentation retrieved September 2, 2026. Virtual-IP implementation, proxy modes, session affinity, traffic policies, health checks, and data-plane behavior.

## Exercises

### Exercise 1

Design connectivity contracts for an internal API, headless database membership, node-local telemetry receiver, private partner endpoint, and public web API. Choose discovery/exposure, identity, TLS, policy, topology, and evidence.

### Exercise 2

Audit a Service whose selector matches stable and canary pods, has numeric targetPort drift, `publishNotReadyAddresses: true`, client-IP affinity, Local traffic policy, and a single-stack LoadBalancer in a dual-stack requirement.

### Exercise 3

Design a shared Gateway API platform for infrastructure, gateway, route, backend, and certificate owners across namespaces. Include attachment, ReferenceGrant, TLS, route conflict, policy, status, and deletion.

### Exercise 4

Diagnose intermittent 503s during rollout when route status is Accepted, certificate valid, Service exists, EndpointSlices show terminating endpoints, and NetworkPolicy recently changed.

### Exercise 5

Transfer the connectivity model to a regional emergency-dispatch radio/data network. Address stable identity, changing responders, protocol, local routing, degraded operation, encryption, authorization, cross-agency consent, failure, and human authority.

## Answers to the Exercises

### Answer 1

The internal API uses ClusterIP and namespace-qualified DNS, workload TLS identity, default-deny ingress/egress with explicit callers/dependencies, cluster routing, and endpoint plus task evidence. Database membership uses headless DNS only because clients understand multiple addresses, stable member TLS identity, refresh, leadership, and failure; user traffic uses a separate ready Service. Node-local telemetry can use a DaemonSet plus internal Local-policy Service only if each client node has an endpoint and loss behavior is defined. The partner endpoint uses a private LoadBalancer or private Gateway listener with owned address/DNS, mutual authentication, source controls, re-encrypted backend, rate limits, and provider lifecycle. The public API uses a public Gateway/HTTPRoute, certificate automation, WAF/abuse controls, application authorization, cross-zone fallback, restricted backend NetworkPolicy, and synthetic/user evidence. Every class records owner, provider/controller version, dual-stack requirement, route/endpoint status, certificate, cleanup, and cost.

### Answer 2

Split stable and canary selectors into separate Services or deliberately weighted routes; do not let a broad selector set an accidental percentage. Restore a named target port that exists across all live revisions, stage rename compatibility, and validate EndpointSlice ports. Remove `publishNotReadyAddresses` unless the application protocol explicitly owns bootstrap and can distinguish discovery from user traffic. Client-IP affinity is not identity and can pin NATed populations to one backend; replace state dependence or document bounded affinity. Local policy must prove a ready endpoint on every receiving node or provide cluster fallback; otherwise it blackholes. A single-stack provider address contradicts a hard dual-stack contract even if the cluster allocates both families. Verify provider support and both paths or declare supported single stack. Re-test selector, readiness, drain, family, source identity, policy, distribution, and end-to-end tasks before promotion.

### Answer 3

Infrastructure owners install a conformant controller and approved GatewayClasses. Gateway owners create public/private Gateways, listeners, addresses, certificate references, allowed-route namespaces, security profiles, and capacity. Application namespaces own HTTPRoutes with explicit parentRefs, host/path matches, timeouts, filters, and same-namespace Services. Backend owners issue narrow ReferenceGrants for any cross-namespace Service reference; certificate namespace owners separately grant Secret reference where required. Listener attachment and ReferenceGrant form two target-side handshakes. Admission enforces hostname ownership, non-overlapping route intent where required, supported filters, TLS, no plaintext public listener, and quotas. NetworkPolicy permits gateway data-plane identities to backends; application auth remains. Observe Gateway/listener Accepted/Programmed, Route per-parent Accepted/ResolvedRefs, reference changes, certificate expiry, endpoint health, data-plane config, and synthetic requests. Deletion drains routes/listeners, revokes grants, cleans provider/DNS/cert resources, and preserves audit.

### Answer 4

Accepted means the parent accepted route configuration, not that every request succeeds. Correlate 503 time with route revision, gateway data-plane programming, Service port, EndpointSlice changes, pod deletion/readiness, zones, and NetworkPolicy rollout. Count non-terminating serving endpoints separately from terminating/serving drain endpoints. Check whether all normal endpoints briefly disappeared, whether the data plane falls back to terminating endpoints, and whether grace/connection timeouts align. Validate the new policy from actual gateway source identity/IP after NAT on the chosen CNI; ingress and gateway egress both must allow the backend path. Inspect gateway upstream error reason, connection reuse to draining pods, readiness probes, rollout surge/unavailable, and application logs. Repair selector/readiness/rollout capacity or policy specifically, preserve drain, and verify with sustained revision-specific synthetic traffic. Do not rotate the valid certificate or recreate the accepted route without evidence.

### Answer 5

Use a stable incident/channel identity distinct from changing vehicle, handset, responder, and relay addresses. Discovery maps that identity to currently authorized, reachable endpoints with role, region, protocol, capability, and readiness. Prefer local relays during normal operation for latency and spectrum efficiency, with explicit regional fallback when local capacity fails; disconnected operation needs cached signed assignments and later reconciliation. Encrypt each radio/data hop appropriate to device capability and authenticate agency/device/person separately; channel location never authorizes dispatch data. Cross-agency routing requires target-agency consent analogous to a grant, scoped by incident, protocol, resources, and time. Observe route programming, endpoint readiness, coverage, congestion, key expiry, failed authorization, delivery acknowledgement, and human confirmation separately. Test relay loss, partition, duplicate messages, stale membership, key rotation, overloaded fallback, and safe drain. Authorized dispatchers and incident commanders retain prioritization and emergency override under audit; automated routing never decides substantive emergency response authority.
