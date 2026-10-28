# Module 4 — DNS and service discovery

A DNS lookup is not one question sent to one server. It is a resolver algorithm operating on a name, search list, `ndots` threshold, cache state, DNS policy, network path, and one or more authoritative or forwarding servers. A deployment can publish the correct Service record while clients continue to receive NXDOMAIN from a negative cache. A name can resolve perfectly while the selected Service has no usable endpoint.

The engineering question is:

> Which component transformed the name, which cache or authority answered it, and what does the answer prove about the service path that follows?

## Learning outcomes

By the end of this module, you can:

- trace a Kubernetes DNS lookup from application input to the final DNS query;
- explain namespace-relative names, search paths, `ndots`, and absolute names;
- distinguish ClusterIP, headless, SRV, Pod, and external discovery behavior;
- reason about positive and negative TTLs across several cache layers;
- evaluate Pod `dnsPolicy`, `dnsConfig`, and NodeLocal DNS choices;
- diagnose UDP/TCP transport and NetworkPolicy failures;
- design dual-stack and split-horizon tests that identify the exact answer source;
- state what DNS correctness does—and does not—prove.

## The discovery chain

For a typical in-cluster lookup, the path is:

```text
application name
→ language/runtime resolver behavior
→ libc or local resolver configuration
→ search-list and ndots expansion
→ Pod DNS nameserver
→ optional Node-local cache
→ CoreDNS or another cluster DNS service
→ Kubernetes API-derived record or upstream resolver
→ response and TTL
→ one or more client-side caches
```

Each arrow has its own state and failure modes. “CoreDNS is healthy” proves only that a process or Service met a selected health criterion. It does not prove the client asked the expected name, reached the expected resolver, received a fresh answer, or used the result correctly.

## Names are interpreted in a namespace context

A normal Service has a fully qualified name of the form:

```text
service.namespace.svc.cluster-domain
```

The cluster domain is configurable; do not hard-code `cluster.local` in portable application logic.

Inside the same namespace, a client may use the short name:

```text
atlas-api
```

From another namespace, the same token is normally expanded using that caller’s search list and can refer to a different Service or fail. The two clients are not asking the same logical question merely because their source code contains the same string.

Use a fully qualified name when cross-namespace intent must be explicit. A trailing dot marks an absolute DNS name and prevents search-list expansion.

## `ndots` changes the query sequence

Resolver configuration commonly includes a search list and an `options ndots:N` value. A name with fewer than `N` dots is often tried against search suffixes before being tried as absolute. A name with enough dots may be tried as absolute first.

For example, a client calling `api.partner.example` under a high `ndots` value may generate several cluster-suffixed queries before the external query. This affects:

- query volume and latency;
- negative-cache entries;
- information leakage to internal or external DNS;
- which name appears in captures;
- outage behavior when one search candidate exists unexpectedly.

Diagnose the names actually transmitted on the wire or reported by resolver tracing, not only the string passed by the application.

## Service records

### ClusterIP Service

A normal Service usually has A and/or AAAA records pointing to its Service address. The DNS answer establishes the Service destination; endpoint selection remains the responsibility of the Service data plane.

A correct A record does not prove:

- EndpointSlices exist;
- any endpoint is Ready;
- every Node has current forwarding state;
- NetworkPolicy permits the flow;
- the backend is listening.

### Headless Service

For a headless Service, DNS commonly publishes endpoint addresses rather than a virtual ClusterIP. Clients now receive membership information directly and own more of the balancing and caching behavior.

The answer can change as Pods are created, become ready, terminate, or move. A client that caches indefinitely defeats the intended discovery model.

### SRV records

SRV records can publish service names, protocols, ports, and targets for named Service ports. They are useful when clients understand SRV semantics. They do not provide application-level health or leader election.

### Pod records

Pod DNS behavior depends on hostname, subdomain, Service relationships, and cluster configuration. Treat Pod names as specific platform contracts, not universal assumptions.

## DNS answer order is not an ownership protocol

Multiple A or AAAA records may be returned in an order influenced by the DNS server, resolver, client library, or caching layer. That order is not a leader-election, primary-selection, or durable affinity contract.

If the application needs one authoritative writer, ordered workflow step, or stable instance identity, model that explicitly. Do not infer it from the first DNS answer.

## Positive and negative caches

A DNS result can be cached in several places:

- the application or language runtime;
- libc or a local daemon;
- NodeLocal DNS;
- CoreDNS cache plugins;
- upstream recursive resolvers;
- external provider infrastructure.

Positive answers remain until their TTL expires or a cache-specific policy removes them. Negative responses such as NXDOMAIN can also be cached, usually according to SOA-derived negative TTL behavior or local configuration.

This creates a classic rollout failure:

```text
1. client asks for atlas-api before the Service exists;
2. resolver returns NXDOMAIN;
3. Service and record are created;
4. authoritative DNS is now correct;
5. client continues to use cached NXDOMAIN until expiry.
```

Restarting CoreDNS does not clear an application cache. Recreating the Service does not invalidate a Node-local negative entry. Diagnosis must identify the cache that produced the observed answer and its remaining lifetime.

## Authoritative freshness and client freshness are different

To prove DNS change propagation, record at least:

- exact query name and type;
- client namespace and resolver configuration;
- responder address;
- response code and answer;
- TTL or negative-cache lifetime;
- timestamp;
- whether the query bypassed or used each cache layer;
- address family selected by the client.

A direct query to CoreDNS can prove authoritative cluster state while the application remains stale. Both observations can be true.

## Pod DNS policy

`dnsPolicy` determines how a Pod’s resolver configuration is derived. Common choices include cluster-oriented behavior, inheriting Node settings, explicit configuration, and host-network-aware cluster behavior.

Inspect the effective `/etc/resolv.conf` inside the Pod. The manifest is desired state; the file is what the process actually uses.

`dnsConfig` can add nameservers, searches, or options, but broad or inconsistent overrides make incidents harder. Record why every override exists and whether the application’s resolver honors it.

## NodeLocal DNS

NodeLocal DNS can reduce latency and connection pressure by providing a Node-local cache and forwarding path. It also adds:

- a Node-local address that egress policy may need to allow;
- per-Node cache state and failure domains;
- another configuration and upgrade surface;
- potentially different packet paths for UDP and TCP;
- a need to distinguish Node cache health from CoreDNS health.

A failure affecting one Node can therefore produce DNS errors for only the Pods scheduled there. The Course 5 casebook includes exactly this shape.

## DNS transport is part of the network contract

DNS commonly uses UDP, but TCP is required for responses that are truncated or exceed UDP constraints and for other valid behaviors. Default-deny egress that allows only UDP/53 is incomplete.

The path may fail because of:

- resolver address unreachable;
- UDP allowed but TCP denied;
- MTU or fragmentation behavior;
- Node-local listener absent;
- CoreDNS Service with no usable endpoints;
- CoreDNS unable to reach upstream resolvers;
- policy allowing CoreDNS but denying its upstream egress;
- route or firewall asymmetry.

Test both transports and record where the query stops.

## Dual-stack discovery

A dual-stack proof must separate:

- A query and IPv4 connection;
- AAAA query and IPv6 connection;
- answer ordering;
- resolver filtering or synthesis;
- client address-selection behavior;
- fallback timing;
- IPv4 and IPv6 policy;
- endpoint-family availability.

A successful client call may have fallen back to IPv4. Use explicit family tests and packet evidence rather than assuming that an AAAA record was used.

## ExternalName and external discovery

An `ExternalName` Service returns a CNAME-like DNS relationship to another name. It does not proxy traffic, verify the destination, preserve an HTTP Host header, or guarantee TLS identity compatibility.

A client connecting to `internal-name.namespace.svc` but receiving a CNAME to `vendor.example` may still send the internal HTTP authority or validate the wrong TLS name, depending on the client. Treat this as an application/protocol compatibility decision, not a transparent network alias.

For external dependencies, Course 9 will compare direct DNS, private endpoints, proxies, selectorless Services, and egress gateways. DNS is one part of that design, not the complete security boundary.

## API-based discovery

Some controllers, operators, and infrastructure components watch EndpointSlices or other Kubernetes APIs instead of relying on DNS. This can provide richer conditions and topology metadata.

It also introduces:

- Kubernetes API credentials and authorization;
- watch resumption and resource-version handling;
- cache consistency;
- larger implementation responsibility;
- direct coupling to Kubernetes APIs.

Ordinary application clients should not adopt API-based discovery merely because it seems “more current.” Use it when the consumer genuinely needs information DNS cannot express and owns the operational cost.

## Worked investigation — CoreDNS is healthy, the client still sees NXDOMAIN

A new Atlas Service is created at 10:00. CoreDNS logs show the record at 10:01. A client Pod continues failing until 10:05.

Evidence shows:

- the application attempted the short name from a different namespace;
- the resolver first queried `atlas-api.client.svc...`, which did not exist;
- that NXDOMAIN was cached in a Node-local resolver;
- the correct cross-namespace name was never queried;
- restarting CoreDNS changed nothing.

The failure was not delayed Service publication. It was name interpretation plus negative caching. The repair uses the fully qualified Service name and keeps negative-cache evidence in the runbook.

## Capstone implementation

Module 4 uses:

- `capstone/atlas_net/dns.py` for search expansion, positive/negative cache, and query behavior;
- `capstone/atlas_net/network_lab.py` for a real UDP DNS exchange;
- `capstone/manifests/observability/coredns-fragment.yaml` as a bounded configuration fragment;
- `capstone/scripts/dns_cache_lab.py` for cache timing and failure evidence.

The local DNS server is a teaching fixture, not an implementation of the full DNS protocol or CoreDNS. Its purpose is to make query identity, response code, cache state, and TTL visible.

## Release evidence

A credible discovery release includes:

- cluster domain and resolver configuration;
- Service and record types consumed;
- exact names used by each workload;
- positive and negative TTL behavior;
- UDP and TCP tests;
- dual-stack query and connection evidence;
- NetworkPolicy dependencies;
- NodeLocal DNS ownership if present;
- upstream resolver and private-zone ownership;
- an explicit statement that DNS success does not prove backend availability.

## DNS transport is part of availability

A resolver normally begins with UDP, but large responses, DNSSEC data, truncation, or policy can require TCP. EDNS changes advertised buffer sizes and failure behavior. A NetworkPolicy that permits only UDP/53 can therefore make ordinary names work while larger answers time out.

Record the actual transport path:

```text
application resolver
→ Pod resolver configuration
→ optional node-local cache
→ CoreDNS Service
→ selected CoreDNS endpoint
→ upstream or authoritative server
```

Each hop can cache, retry, truncate, forward, or change the source identity seen by the next hop. A healthy CoreDNS Pod proves neither that the Service reaches it nor that its upstream path succeeds.

## CoreDNS behavior is a plugin chain

CoreDNS evaluates configured plugins in order. The Kubernetes plugin can synthesize cluster records, cache can retain positive and negative answers, forward can query upstream resolvers, rewrite can change names or answers, and fallthrough can transfer a query to a later plugin. Configuration order therefore changes semantics.

For every cluster DNS profile, capture:

- the Corefile or equivalent configuration;
- plugin order and zones;
- cache policy and denial TTL;
- upstream resolvers and timeout behavior;
- loop detection and health endpoints;
- autoscaling and disruption behavior;
- Service and EndpointSlice state;
- NetworkPolicy rules for client-to-DNS and DNS-to-upstream traffic.

Restarting CoreDNS to “clear DNS” is a poor first response. It discards evidence, may leave client caches unchanged, and can amplify an upstream outage.

## Search expansion has measurable cost

A name without a trailing dot may be tried against each search suffix before it is queried as absolute, depending on `ndots`. For a search list with several entries, one application lookup can create many DNS queries and timeouts.

This matters when an external name contains fewer dots than the threshold. The resolver may ask cluster DNS for several nonexistent expanded names before trying the intended absolute name. Negative caching can reduce repeated load, but an outage or slow upstream can make the expansion path dominate application latency.

The diagnostic record should show the name as supplied by the application, resolver options, generated query sequence, response codes, TTLs, and timing. Testing only `dig` with a fully qualified name can bypass the application’s actual resolver algorithm.

## Discovery data has consistency semantics

DNS is an eventually refreshed view. A client can continue using an address until its cache expires, and some language runtimes or connection pools retain results longer than DNS TTL alone suggests. A headless Service can expose endpoint churn directly to clients, while a ClusterIP lets the Service data plane absorb much of that churn behind one stable destination.

When a record changes, test:

- a client with a cached positive answer;
- a client with a cached negative answer;
- a fresh client;
- an existing connection created from the old answer;
- a new connection after TTL expiry;
- behavior when one address family changes before the other.

This separates DNS convergence from transport connection lifetime.

## Private and split-horizon names need one authority model

Cloud private zones, cluster zones, corporate zones, and public DNS may provide different answers for the same logical name. This is useful only when the intended client population and route domain are explicit.

A private answer that points to an unreachable address is not a DNS success. A public fallback that bypasses a private service endpoint can become a security or cost defect. Course 5’s egress profile binds logical dependencies to permitted resolution and connected-peer behavior rather than treating any syntactically valid DNS answer as authorized.

## Transition

Module 4 establishes discovery. Module 5 constrains which discovered paths are reachable, using NetworkPolicy’s additive L3/L4 model without confusing address-based segmentation with workload or application authorization.
