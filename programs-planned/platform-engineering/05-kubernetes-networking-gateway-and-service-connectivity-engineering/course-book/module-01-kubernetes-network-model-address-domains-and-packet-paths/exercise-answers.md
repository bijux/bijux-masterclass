# Worked answers — Kubernetes network model, address domains, and packet paths

These answers model the level of reasoning expected in the checkpoint. A complete answer names the mechanism, the evidence that would distinguish competing causes, and the boundary of the claim.

## 1. Why is a ClusterIP not diagnosed like an address bound to a normal interface?

A ClusterIP is normally a virtual Service destination interpreted by the selected Service data plane, not an address assigned to a host interface. Depending on the cluster, forwarding can be implemented through nftables, iptables, IPVS, eBPF, a proxy, or cloud infrastructure. Therefore, absence from `ip addr` is expected and proves nothing about Service health. Diagnose the Service object, EndpointSlices, and the implementation’s programmed rules or maps. Then send a new connection and identify the chosen endpoint. The conclusion must name the actual Service implementation; commands for iptables are irrelevant if kube-proxy replacement or another data plane owns forwarding.

## 2. Draw the path for two containers in the same Pod and state which cluster components are not involved after sandbox creation.

The path is `container A socket → shared Pod network namespace → loopback or shared Pod interface → container B socket`. Both containers normally share one network namespace, so they also share loopback, interfaces, addresses, and routes. After the sandbox and local interfaces exist, this communication does not require cluster DNS, a Service, EndpointSlice selection, cross-Node routing, a Gateway, or ordinary CNI forwarding between Pods. A failure should first be tested with listening-socket evidence, bind address, protocol, local firewall state, and process lifecycle. CNI remains relevant to creating the sandbox, but not to each subsequent loopback packet.

## 3. A TCP handshake succeeds but a 2 MiB response stalls. Which hypothesis should be tested before blaming the application?

Test a path-MTU or fragmentation failure. The handshake uses small packets, so it can succeed even when encapsulation, encryption, or a lower-MTU underlay makes larger packets unusable. Send controlled payload sizes, inspect interface and tunnel MTUs, capture retransmissions, and check whether required ICMP “packet too big” or fragmentation-needed signals return. Also compare same-Node and cross-Node paths and test IPv4 and IPv6 separately. Application slowness remains possible, but a sharp size threshold and repeated retransmission with no application error strongly support an MTU hypothesis. Increasing timeouts would only hide the transport failure.

## 4. Why can a successful IPv4 test not be counted as dual-stack proof?

IPv4 and IPv6 have independent allocation, DNS, route, policy, listener, Service-family, endpoint-family, NAT, and egress paths. A client may receive both A and AAAA records but use only IPv4, or silently fall back from broken IPv6 through Happy Eyeballs behavior. Dual-stack proof therefore needs explicit IPv4 and IPv6 DNS queries and connections, family-specific policy and route evidence, and a negative or fault test for each family. A successful user request establishes only the family actually used. Record the selected address, source address, listener, endpoint family, and fallback timing rather than inferring family from object configuration.

## 5. What is the earliest useful distinction when a connection times out?

First distinguish name-resolution failure from failure after an address was selected. If no usable destination was produced, investigate resolver expansion, cache state, DNS transport, and authoritative records. If an address exists, determine whether the source selected a route and emitted a SYN or other first packet. This split prevents DNS, route, policy, and application causes from being mixed. The decisive evidence is the exact name queried, returned addresses and TTL, source route lookup, and packet observation at the source namespace. “Timeout” alone does not identify a layer; the earliest missing transition does.

## 6. Why is Pod IP a poor durable authorization identity?

Pod addresses are network-location data owned by CNI/IPAM at a point in time. Pods are replaceable, addresses may be reused, and a workload can move while retaining the same logical identity. Translation or proxies can also change the address observed by the application. Authorization based only on Pod IP can therefore grant a later workload the authority of an earlier one or fail when the same service reschedules. Use workload identity and application credentials for authority decisions. Pod addresses remain useful for routing, policy selection in bounded implementations, and incident correlation, but only with timestamps, ownership evidence, and awareness of reuse.

## 7. Explain why a Ready condition can coexist with cross-Node unreachability.

Readiness answers the probe defined by the workload, often from the kubelet or local Pod network. A local HTTP probe can succeed while remote Pod-prefix routes, overlay tunnels, cloud routes, policy on another Node, return paths, or MTU are broken. The endpoint controller may correctly publish the Pod because its readiness contract was satisfied. To diagnose, compare same-Node and cross-Node direct Pod tests, inspect route ownership on both Nodes, and capture the packet at source and destination vantage points. Readiness should not be changed to compensate for an unrelated cluster-route failure unless the application contract genuinely requires that remote path.

## 8. When does an overlay design need a smaller Pod MTU than the underlay?

When an outer tunnel or encryption header is added, the inner Pod packet plus encapsulation must fit within the underlay MTU. If the underlay supports 1500 bytes and the overlay adds, for example, dozens of bytes, a 1500-byte inner packet no longer fits. The Pod MTU should be at most the smallest end-to-end underlay MTU minus worst-case overhead for the relevant address family and tunnel. Verify the actual implementation because IPv6 and encryption can change overhead. Evidence should include interface MTUs, tunnel configuration, controlled packet-size tests, and ICMP behavior—not a value copied from another cluster.

## 9. What evidence distinguishes a missing forward route from a missing return route?

Observe the flow at several points. If the source namespace emits a packet but the destination Node or Pod never sees it, investigate the forward route, encapsulation, or forward policy. If the destination receives the request and emits a reply, but the source never sees the reply, the return route, NAT state, reverse-path filtering, or reverse policy is the likely boundary. Capture the exact five-tuple at source Pod, source Node, destination Node, and destination Pod, and record address translation at each hop. A destination-side application log proving receipt is especially strong evidence that the forward path worked.

## 10. Why should a packet-path document name translation points?

Translation changes the addresses used by routing, NetworkPolicy, connection tracking, observability, and application logs. Without naming DNAT, SNAT, proxy termination, or tunnel encapsulation, two teams can describe the same flow using different source and destination identities and reach incompatible conclusions. A useful path shows the address before and after each translation, who owns the translation state, and how the return packet is matched. It should also separate the transport peer from forwarded metadata and authenticated identity. The decisive evidence is a correlated capture or flow record on both sides of the translation boundary.

## 11. What does longest-prefix match contribute to Kubernetes incident analysis?

It prevents the false assumption that the default or broad cluster route necessarily handles a packet. A stale or incorrect more-specific route can override a valid `/16` or default route for one Pod prefix, Node, or external dependency. Use route lookup for the exact destination from the relevant namespace and inspect policy-routing tables where present. If one endpoint fails while others in the broader range succeed, a narrow route is a strong hypothesis. The result still needs return-path and data-plane evidence, because selecting the expected next hop does not prove the packet was delivered.

## 12. Which Course 1 skill remains essential in this module?

Linux evidence collection remains essential: network namespaces, interfaces, routes, sockets, process identity, packet capture, firewall state, and TLS behavior. Kubernetes adds desired-state APIs and controllers, but the final packet still traverses kernel and process mechanisms. A platform engineer must connect the Pod, Service, or Gateway object to the actual namespace and socket path rather than treating YAML as runtime truth. The strongest answer demonstrates one transition with both Kubernetes evidence and Linux evidence—for example, an EndpointSlice address plus a route lookup and capture showing whether traffic reaches that Pod.
