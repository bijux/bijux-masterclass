# Worked answers — Services, EndpointSlices, and service data planes

A Service incident should always separate stable identity, backend publication, and forwarding state.

## 1. Why are Service, EndpointSlice, and node data-plane state three separate proof objects?

The Service expresses stable identity, ports, selectors, address families, and traffic policy. EndpointSlices express current backend membership and conditions. The node or proxy data plane implements forwarding from the Service destination to an eligible endpoint. Each can be correct while another is stale or invalid. A release therefore records all three and correlates their generations. Testing only the Service YAML cannot show whether endpoints exist; testing only EndpointSlices cannot show whether every Node programmed them.

## 2. What does a correct selector fail to prove?

It proves only which Pod labels the Service intends to select. It does not prove selected Pods are Ready, expose the named target port, appear in current EndpointSlices, match the intended address family, or have been programmed into the data plane. It also does not prove the application listens on the resulting address/port. The decisive evidence combines Pod labels and readiness, EndpointSlice addresses/conditions/ports, data-plane generation, and a direct endpoint plus Service-path test.

## 3. Why can existing connections outlive endpoint removal?

Endpoint removal controls future selection after convergence. Existing TCP connections, NAT mappings, IPVS state, eBPF connection state, or proxy connection pools may already bind the flow to the old backend. HTTP/2 can carry many requests on one long-lived connection. Test both new connections and connections created before readiness withdrawal, and record endpoint-change and data-plane-programming timestamps. If the goal is to terminate established streams, that requires an explicit draining or connection-close mechanism beyond removing the endpoint.

## 4. When is a headless Service appropriate?

Use it when clients or protocols need direct endpoint identity and are prepared to handle discovery, caching, changes, balancing, and failure themselves—for example some clustered or stateful peer protocols. A headless Service returns endpoint addresses rather than an ordinary virtual ClusterIP. It is inappropriate when clients expect one stable load-balanced destination without understanding endpoint churn. The design must explain TLS identity for individual endpoints, record ordering/failover behavior, and prove that client caches respect lifecycle changes.

## 5. Why is “no iptables rule” insufficient evidence of a broken Service?

The cluster may use kube-proxy in nftables or IPVS mode, an eBPF replacement, a user-space proxy, or external infrastructure. The absence of one implementation’s artifact proves only that the implementation might be different. First identify the Service data-plane owner and version, then inspect its rules, maps, virtual services, or status. Pair that with a new connection test and EndpointSlice generation. Tool output without implementation identification is not a diagnostic conclusion.

## 6. What failure can a named targetPort prevent compared with a numeric targetPort?

A named target port decouples the Service contract from a hard-coded backend number and lets selected Pods map the same semantic port name to their actual container port. This can prevent a rollout where the container port changes but the Service still sends traffic to the old number. It does not prevent missing, duplicate, or inconsistently named ports, nor does it prove protocol. Release evidence should show the name resolved consistently in EndpointSlices and that the process speaks the expected protocol.

## 7. Why can ClientIP affinity overload one backend behind NAT?

Many distinct users can appear to the Service data plane under one translated source address. If affinity keys on that address, all those users may be mapped to one backend until timeout or backend removal. This creates a hotspot despite an apparently balanced client population. Measure source-address distribution at the affinity decision point, backend load, and behavior after NAT or proxy changes. Affinity is bounded routing preference, not user identity or durable session ownership.

## 8. What must be measured during readiness withdrawal?

Record the time the workload becomes unready, the Pod condition update, EndpointSlice condition change, per-node or proxy data-plane programming, selection of new connections, behavior of existing connections, and process exit. Include at least one long-lived connection and new requests during the transition. This timeline shows whether traffic stopped too late, capacity was removed too early, or one data-plane instance lagged. A single final successful request does not prove graceful withdrawal.

## 9. Why should a selectorless Service be reviewed as an authority boundary?

Without a selector, endpoint membership is not derived from Pods. Whoever publishes EndpointSlices can direct Service traffic to arbitrary approved or unapproved addresses. That actor therefore holds routing authority. Review who can mutate slices, how addresses/ports are validated, how health and stale endpoints are managed, and whether cross-tenant or private-network targets are possible. NetworkPolicy and application authorization still apply; a valid selectorless Service does not automatically make an external endpoint trustworthy.

## 10. How does a LoadBalancer Service differ from Gateway API?

A LoadBalancer Service requests external reachability for one Service, commonly at L4, through provider or controller infrastructure. Gateway API separates infrastructure class, shared listeners, application routes, cross-namespace consent, protocol-specific matching, and status. A LoadBalancer Service can be the backend exposure mechanism for a Gateway implementation, but it does not itself express HTTP hostname/path ownership. Choose based on required protocol and team boundaries, not on which YAML is newer.

## 11. What does externalTrafficPolicy Local trade?

It can preserve the original network source and avoid cross-Node forwarding, but only Nodes with eligible local endpoints can serve traffic. This reduces the healthy Node population, can create uneven capacity, and depends on external health checks converging with local endpoint state. Prove source preservation, behavior on a Node without endpoints, readiness-withdrawal timing, zone failure, and load distribution. The correct answer is a trade-off, not an unqualified optimization.

## 12. Why should Service release evidence record data-plane generation?

Kubernetes API objects can be current while one Node or proxy still forwards using an older endpoint set. Recording the desired EndpointSlice generation and the generation installed by each data-plane instance makes convergence measurable. It lets an incident distinguish selector/publication correctness from stale forwarding. The evidence should be paired with a negative test showing that a removed endpoint is no longer selected for new connections, while documenting established-connection behavior separately.
