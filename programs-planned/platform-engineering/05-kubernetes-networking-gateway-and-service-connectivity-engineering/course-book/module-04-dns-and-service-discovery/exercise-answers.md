# Worked answers — DNS and service discovery

These answers trace the resolver path and keep DNS correctness separate from endpoint and application correctness.

## 1. Why can `atlas-api` resolve differently from two namespaces?

A short name is interpreted through each Pod’s resolver search list. In namespace `client-a`, `atlas-api` may be tried as `atlas-api.client-a.svc.<cluster-domain>`; in `client-b`, the first candidate is different. One namespace may contain a Service with that name while the other does not. `ndots`, local resolver behavior, and caches can further change query order. The decisive evidence is the effective `/etc/resolv.conf` and exact DNS queries from each Pod. Use a fully qualified Service name when cross-namespace intent must be explicit.

## 2. What does `ndots` change?

`ndots` influences whether a name is tried as absolute before or after search-suffix expansion. Under a high threshold, a name that already looks external can generate several cluster-local candidates first, increasing latency, query volume, and negative-cache entries. It can also expose unexpected internal names or create different behavior when one suffix happens to exist. Prove the effect by recording the exact transmitted query sequence and response times, not merely the name string given to the application.

## 3. Why can DNS be correct while a Service is unavailable?

A normal Service DNS record commonly points to the ClusterIP independently of backend readiness. DNS can return the correct address while EndpointSlices contain no eligible endpoints, a Node’s data plane is stale, NetworkPolicy denies traffic, or the application is not listening. Conversely, a headless Service may publish addresses that later become unusable. A complete test follows the answer into Service membership, forwarding, transport, and protocol evidence. DNS proves discovery state, not service health.

## 4. Why is DNS answer order not a leader election contract?

DNS servers, caches, resolvers, and client libraries may reorder multiple answers. TTL expiry or endpoint churn can also change the set. No durable ownership or consensus is established by “the first address.” A client that treats the first answer as a primary can select different instances across processes or requests. If one writer or leader is required, use an explicit coordination or service protocol. DNS can publish candidates; it does not assign authoritative roles.

## 5. How does negative caching create a post-deployment outage?

A client can query a name before the Service or record exists, receive NXDOMAIN, and cache that negative response. After authoritative DNS becomes correct, the client or Node-local cache continues returning NXDOMAIN until the negative TTL expires. Restarting or fixing CoreDNS may not change that client state. Evidence should identify the cache that answered, remaining TTL, original query name, and authoritative answer obtained through a bypass query. The repair addresses naming/order and cache lifetime rather than repeatedly recreating the Service.

## 6. What risk does NodeLocal DNS introduce?

It adds a per-Node cache and forwarding hop. This can reduce latency and connection-tracking pressure, but a broken or stale Node-local instance can affect only Pods on one Node. Egress policy must allow the actual Node-local address and both UDP/TCP behavior, and operations must distinguish Node cache health from CoreDNS health. Test the same lookup from Pods on several Nodes and compare resolver configuration, cache state, and upstream reachability.

## 7. Why can ExternalName break HTTPS?

ExternalName creates DNS indirection; it does not change the logical authority used by the client. A client may connect to the external address while sending the internal Service name in SNI or HTTP Host, causing certificate or virtual-host mismatch. Other clients may follow the CNAME and use different name behavior. Prove the exact SNI, certificate SAN validation, and HTTP authority. If the external service expects its own name, use an explicit application/configuration contract rather than assuming DNS aliasing is transparent.

## 8. What must a dual-stack DNS proof include?

It must include explicit A and AAAA queries, response TTLs and order, the client’s address-selection behavior, separate IPv4 and IPv6 connection attempts, route and NetworkPolicy evidence for each family, and the endpoint family actually reached. Also inject a one-family failure to see whether fallback works and how much delay it adds. A successful normal request is insufficient because the client may have silently selected or fallen back to only one family.

## 9. When is API-based EndpointSlice discovery justified?

It is justified when a controller or infrastructure component needs richer membership, conditions, topology, or generation data that DNS cannot express and is prepared to own Kubernetes API credentials, watches, cache consistency, and resumption. Ordinary applications should prefer the simpler Service/DNS contract unless they truly need those semantics. The decision should compare operational cost and authorization surface. A successful watch does not remove the need for endpoint health and connection behavior.

## 10. Why should a cluster domain not be hard-coded?

The cluster DNS suffix is configurable and can differ across environments or fleets. Hard-coding `cluster.local` makes the application depend on one installation detail and complicates migration or testing. Prefer short names within a namespace, configuration-derived fully qualified names, or platform-provided discovery. The evidence is an application test under a non-default cluster domain or a static check proving that the domain comes from configuration rather than source code.

## 11. What distinguishes authoritative DNS freshness from client freshness?

Authoritative freshness describes the current record and TTL at the source of truth, such as CoreDNS backed by current Kubernetes state. Client freshness describes what a specific application or cache is still using. A client can be stale even when the authority is current, and a direct authoritative query can bypass the cache that causes the outage. Record responder address, cache path, TTL, query timestamp, and whether the result was served from cache. Both observations can be true simultaneously.

## 12. What evidence should accompany a DNS latency claim?

State the exact name and type, resolver path, cache state, query transport, number of search-expanded queries, response code, answer count, TTL, client location, address family, and sample distribution. Separate cache hits from misses and positive answers from expected/ unexpected negative answers. A single `dig` timing from an operator machine is not representative of Pod resolver behavior. The claim should identify whether latency belongs to application lookup, NodeLocal cache, CoreDNS, upstream recursion, or connection after resolution.
