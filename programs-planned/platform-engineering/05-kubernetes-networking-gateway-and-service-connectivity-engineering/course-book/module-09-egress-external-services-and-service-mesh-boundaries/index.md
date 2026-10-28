# Module 9 — Egress, external services, and service-mesh boundaries

Ingress begins with a listener the platform owns. Egress begins with a dependency often owned elsewhere: an identity provider, queue, object store, package registry, payment service, or managed database. The name can resolve to changing addresses, redirects can change authority, NAT can exhaust state, and a proxy or mesh can change both protocol and trust.

The engineering question is:

> How do we bind a logical dependency to an approved connected peer and path without turning broad outbound access into the platform’s permanent escape hatch?

## Learning outcomes

By the end of this module, you can:

- create an owned inventory of external dependencies and their failure semantics;
- compare direct NAT, forward proxies, egress gateways, and private endpoints;
- explain why a hostname is not a stable network identity;
- validate DNS answers, redirects, and connected peers against SSRF and policy risks;
- evaluate selectorless Services and ExternalName without treating them as universal egress controls;
- reason about NAT capacity, source identity, and connection reuse;
- decide whether a service mesh solves a named gap or merely adds control planes;
- produce an egress contract suitable for Course 6 storage and data-resilience work.

## Begin with dependency ownership

For every external dependency, record:

- logical name and business purpose;
- owner and support route;
- protocol and ports;
- authentication mechanism;
- expected DNS names and certificate identities;
- allowed address classes or private endpoints;
- redirect policy;
- data classification;
- retry and timeout policy;
- availability and degradation behavior;
- source-address requirements;
- audit and telemetry requirements;
- whether the dependency is needed at build time, startup, or runtime.

Runtime Atlas Pods should not need package-registry or source-repository egress merely because the build system did. Course 3 already produced immutable images; build dependencies should not leak into runtime policy.

## Common egress architectures

### Direct Node or cloud NAT

Pods connect through Node or cloud NAT to public destinations. This is simple but often exposes broad destination reachability and creates shared translation state.

Questions include:

- Which source address is presented externally?
- How many translated ports are available?
- How are connections distributed across NAT gateways or Nodes?
- What happens when a gateway or zone fails?
- Can policy identify destinations before translation?
- Which logs connect a Pod identity to a translated flow?

### Forward proxy

Applications or transparent infrastructure send requests through a proxy. A proxy can enforce hostname, protocol, authentication, logging, and policy, but it becomes an application-aware dependency.

It must correctly handle:

- CONNECT or protocol-specific tunneling;
- destination and redirect policy;
- credential forwarding;
- TLS interception boundaries, if any;
- streaming and large bodies;
- timeouts and retries;
- high availability and backpressure.

### Egress gateway

An egress gateway centralizes selected outbound flows and may provide stable source addresses or policy. It introduces a shared data-plane dependency, routing complexity, and capacity planning.

A stable source IP proves only the path’s egress identity. It does not authenticate the destination, authorize application actions, or guarantee that traffic could not bypass the gateway.

### Private service endpoint

A cloud private endpoint or private service connection can keep traffic on provider-controlled networks and avoid public Internet paths. It changes:

- DNS answers;
- subnet routes;
- security-group/firewall behavior;
- source and destination addresses;
- regional/zone availability;
- endpoint ownership and cost;
- certificate names.

Prove the actual connected peer and route. A private DNS name alone does not establish that packets stayed on the intended private path.

## A hostname is not a connected peer

A hostname can resolve to multiple addresses, change over time, return private or public addresses, or be influenced by split-horizon DNS. Between validation and connection, DNS can change. The server can redirect the client to another authority.

A robust outbound policy performs a sequence such as:

1. parse the URL according to one strict parser;
2. reject user information, unsupported scheme, invalid port, and forbidden syntax;
3. normalize the hostname;
4. resolve it using the intended resolver path;
5. classify every answer by address family and network class;
6. reject loopback, link-local, metadata, private, reserved, or tenant-forbidden ranges unless explicitly owned;
7. connect using an approved resolved address;
8. verify the connected peer where the runtime permits;
9. perform TLS hostname verification for the logical dependency;
10. revalidate every redirect from the beginning;
11. avoid forwarding credentials to a different authority unless explicitly approved.

This is Course 3’s SSRF discipline applied to platform egress. NetworkPolicy alone generally cannot express full hostname and redirect semantics.

## Redirects are new authorization decisions

An HTTP 3xx response can change scheme, hostname, port, and path. A client that validated only the original URL can be redirected to:

- a metadata service;
- a loopback listener;
- a private tenant network;
- a different public provider;
- a credential-harvesting endpoint.

For every redirect:

- enforce maximum hop count;
- parse and classify the new destination;
- resolve and validate again;
- decide whether method/body may be replayed;
- strip authorization and cookies when authority changes unless policy allows them;
- preserve the original deadline;
- record the chain for audit.

A redirect is not merely another response; it requests a new connection and trust decision.

## NAT is finite state

NAT can exhaust translated ports or connection-tracking capacity before link bandwidth is saturated. Risk increases with:

- many short-lived connections;
- poor connection reuse;
- one shared egress address;
- long `TIME_WAIT` periods;
- retries during dependency failure;
- uneven destination distribution;
- zone-local gateways with imbalanced workloads.

Monitor active translations, allocation failures, connection churn, per-destination demand, and gateway saturation. Capacity planning belongs to the network path, not only the application.

## Source identity and allowlists

Some external services allow requests by source IP. A stable egress address can satisfy that narrow integration requirement, but it has limitations:

- many workloads share the same address;
- compromise of any allowed workload may gain the network path;
- failover can change the source;
- IPv4 and IPv6 may use different egress identities;
- source IP does not provide request-level identity;
- bypass routes can undermine the claim.

Prefer workload or application authentication when available. Treat source allowlisting as one layer, not the sole authority boundary.

## Failure semantics and truthful degradation

Every dependency needs an explicit failure contract. When it is unavailable, Atlas must decide whether to:

- reject the initiating request;
- accept work durably and retry later;
- return partial data with a precise warning;
- use bounded stale data;
- disable one optional capability;
- fail closed because continuing would violate security or correctness.

The network layer cannot invent this decision. It can surface connect timeout, TLS failure, refused connection, reset, DNS failure, or policy denial. The owning application or workflow decides what those outcomes mean.

Avoid long opaque retries at several layers. If the client, Gateway, service mesh, application, and SDK each retry three times, one logical operation can produce dozens of attempts. Assign one retry owner where possible, preserve an end-to-end deadline, and expose attempts separately from logical operations.

A circuit breaker or egress proxy can bound repeated connection attempts, but it must not return a successful-looking empty result when the dependency is required. Degradation is truthful only when clients can distinguish fresh, stale, partial, unavailable, and rejected outcomes.

## Egress identity and tenant isolation

Shared egress infrastructure can collapse many workloads and tenants behind one source address or proxy identity. The external service may then see only the gateway, not the originating workload. If the proxy adds workload identity metadata, the receiver must know which proxy is authorized to assert it and how that metadata is protected.

For multi-tenant paths, prove:

- policy keys include tenant and workload identity where required;
- one tenant cannot reuse another tenant’s proxy credentials;
- connection pools do not mix authentication context unsafely;
- logs retain accountable origin without exposing secrets;
- quotas and failures are attributed to the correct tenant;
- stable source IP allowlists do not accidentally grant every platform workload equal authority.

Network source aggregation is an architectural side effect, not an authorization strategy.

## Selectorless Service and ExternalName

A selectorless Service with managed EndpointSlices can present an external endpoint behind a Kubernetes Service identity. It is useful when a platform controller owns endpoint publication and health.

It does not automatically solve:

- DNS change tracking;
- TLS identity;
- external health;
- tenant authorization;
- redirect validation;
- source egress policy.

An `ExternalName` Service creates DNS indirection. It does not proxy, authenticate, or rewrite HTTP authority. HTTPS and Host-based protocols may fail or validate the wrong name.

Choose these tools only when their ownership model matches the dependency.

## FQDN-aware policy is implementation-specific

Some CNI or mesh implementations allow egress policy based on DNS names. This can be useful, but it creates a coupled resolver/policy system.

Review:

- which DNS queries the policy engine observes;
- how long addresses remain allowed;
- TTL and negative-cache handling;
- CNAME chains;
- wildcard semantics;
- shared/CDN addresses;
- DNS rebinding defenses;
- direct-IP bypass;
- behavior when the policy engine misses a query;
- IPv4/IPv6 parity.

Do not describe this as ordinary Kubernetes NetworkPolicy. Name the implementation and conformance evidence.

## Service mesh: capability before product

A service mesh can provide workload identity, mutual TLS, traffic policy, telemetry, retries, and service discovery through sidecars, node proxies, ambient components, or other designs. It also adds:

- another control plane;
- certificate and identity lifecycle;
- proxy resource overhead;
- new failure and upgrade modes;
- protocol compatibility constraints;
- interaction with Gateway, CNI, NetworkPolicy, and application retries;
- additional incident surfaces.

The decision should begin with a measured gap:

```text
required capability
→ why application/Gateway/CNI controls are insufficient
→ expected benefit
→ operational cost
→ failure model
→ migration and rollback
→ evidence plan
```

A mesh cannot make an unsafe non-idempotent retry safe. It cannot repair unclear service ownership, missing authorization, or an invalid data-consistency model. Course 5 rejects a mesh in the Atlas baseline because no current requirement justifies the additional planes.

## Multi-cluster is a separate architecture

Connecting two clusters is not “publish one DNS record.” It introduces:

- overlapping address spaces;
- service-name collisions;
- cross-cluster identity and authorization;
- routing or tunneling;
- failure-domain and partition semantics;
- consistency of discovery;
- certificate and trust-domain design;
- traffic locality and cost;
- independent upgrade and incident ownership.

Course 9 of the Platform Engineering program owns fleet and multi-cluster operations. Course 5 records the boundary rather than adding a superficial multi-cluster example.

## Egress observability

A useful outbound record connects the logical dependency to the network evidence without using unbounded or sensitive metric labels. Capture:

- dependency identifier and owner;
- source workload/tenant in an access-controlled event;
- resolver path and answer class;
- connected address class, not necessarily the raw address in metrics;
- proxy or gateway path;
- TLS peer name and verification result;
- attempt number and remaining deadline;
- response category;
- bytes and duration;
- redirect count;
- policy decision.

Metrics can aggregate by dependency, outcome, address family, and egress class. Detailed addresses and redirect chains belong in protected logs or traces with retention controls. An egress incident is difficult to reconstruct when the application logs only “request failed” and the NAT logs only a translated five-tuple.

## Worked investigation — allowed hostname redirects into metadata

Atlas allows egress to `updates.vendor.example`. The hostname resolves to a public address and passes policy. The server responds with a redirect to a link-local metadata address. The client follows it and forwards an authorization header.

The original hostname allow was not sufficient because the redirect created a new authority and connected peer.

The repair:

- revalidates every redirect;
- rejects link-local and metadata address ranges;
- strips credentials on authority change;
- preserves one deadline and hop budget;
- records the redirect chain;
- adds a negative regression fixture;
- verifies that direct-IP and encoded-address variants are also rejected.

## Capstone implementation

Module 9 uses:

- `capstone/atlas_net/egress.py` for URL, address, redirect, and peer policy;
- `capstone/shared/vectors/egress.json` for approved and rejected cases;
- `capstone/architecture/deferred-responsibilities.yaml` for Course 6 storage boundaries;
- `capstone/scripts/egress_policy_lab.py` for redirect and peer-validation evidence;
- `course-book/reference/mesh-decision-record.md` for capability-driven mesh review.

The deterministic resolver and peer model prove the Atlas policy logic. They do not prove a cloud NAT, private endpoint, or mesh data plane.

## Course 6 storage boundary

Course 6 will add databases, CSI, persistent volumes, snapshots, backup, and restore. Course 5 hands over the network requirements without claiming data durability:

- storage and database service names;
- ports and protocols;
- address families;
- zone and topology assumptions;
- NetworkPolicy dependencies;
- private endpoint or egress requirements;
- TLS and identity expectations;
- failure semantics when the path is unavailable.

A successful TCP connection to storage proves only connectivity. It does not prove write durability, replication, fencing, backup, or recovery.

## Name authorization must survive resolution changes

Allowing a hostname is not the same as authorizing every address it can return. Answers can change through ordinary rotation, split-horizon configuration, compromise, wildcard services, or rebinding. Redirects can move the client to a different host after the first destination was approved.

A robust outbound sequence is:

1. parse and normalize the URL;
2. enforce scheme, port, user-info, and fragment policy;
3. resolve through an approved resolver path;
4. classify every answer;
5. reject mixed or forbidden answer sets according to policy;
6. connect to one approved address;
7. verify the connected peer address and TLS identity;
8. re-evaluate every redirect;
9. apply deadline, size, and retry budgets;
10. record the logical dependency and actual peer.

NetworkPolicy alone may not express this complete contract. If the chosen implementation adds FQDN-aware policy, state that as an implementation requirement and test its cache and failure semantics.

## NAT is a finite stateful dependency

Source NAT consumes translation state and ephemeral ports. Capacity depends on destination tuples, connection lifetime, keep-alive, retry storms, idle timeout, public-address count, and provider behavior. An approximate starting point is:

```text
concurrent translated connections
≤ usable source-port capacity across available NAT addresses
```

The real limit can be lower because of per-destination quotas or uneven hashing. Monitor active mappings, allocation failures, port utilization, connection churn, and retransmissions. A dependency outage that triggers aggressive retries can exhaust NAT and make unrelated egress fail.

The recovery plan must distinguish destination failure from NAT failure. Longer application timeouts do not create more translation capacity.

## Private endpoints move rather than remove ownership

A private service endpoint changes DNS, routes, source identity, policy, and billing. It may avoid public internet transit, but it still needs account ownership, private-zone authority, route-table attachment, security controls, TLS identity, regional behavior, quota evidence, and rollback.

A private DNS answer with no valid route is a discovery success and a connectivity failure. A public fallback can silently violate the intended trust boundary.

## Proxies are application-visible intermediaries

A forward proxy may authenticate workloads, authorize destinations, tunnel TLS, terminate connections, or inspect protocol metadata. It also becomes a capacity, privacy, certificate, and availability dependency.

Define the client protocol, workload identity, destination policy, logging, bypass prevention, fail-open or fail-closed behavior, retry ownership, and outage response. A proxy must not become an unreviewed universal escape path around NetworkPolicy or application authorization.

## Service mesh adoption needs a named capability gap

A mesh can provide consistent service identity, mTLS, telemetry, and traffic policy, but adds control-plane and data-plane components, certificate rotation, resource cost, failure modes, upgrade choreography, and debugging layers.

Adopt it only after naming the unmet requirement and comparing simpler mechanisms. The decision record should cover direct libraries, Gateway or node-proxy options, workload identity, L7 policy needs, cross-cluster behavior, operator skill, latency, incident burden, rollback, and removal. “Standardize traffic” is not a sufficiently specific requirement.

## Transition

Modules 1–9 constructed Atlas connectivity from Pod attachment to external dependency. Module 10 turns the design into an operational release: layered diagnosis, conformance claims, upgrades, game days, categorical evidence, and the exact Course 6 handoff.
