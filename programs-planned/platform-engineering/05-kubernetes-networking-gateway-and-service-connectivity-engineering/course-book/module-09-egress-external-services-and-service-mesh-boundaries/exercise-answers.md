# Worked answers — Egress, external services, and service-mesh boundaries

Outbound policy must connect a logical dependency to the actual peer, path, authority, and failure contract.

## 1. Why is a hostname not a stable network identity?

DNS answers can change, contain several addresses, differ by resolver view, include CNAME chains, or be affected by rebinding and cache timing. A hostname expresses logical naming, not the exact peer connected at one moment. Egress policy should parse and normalize the name, resolve through the intended path, classify every address, connect only to approved results, verify the connected peer and TLS hostname, and repeat the process for redirects. Record both logical dependency and connected address class.

## 2. What capacity can exhaust in NAT before bandwidth?

Translated source ports and connection-tracking entries can exhaust while link bandwidth remains available. Many short connections, poor keep-alive, retries, long `TIME_WAIT`, one shared public address, and concentrated destinations increase pressure. Monitor active translations, allocation failures, per-destination connection churn, and gateway saturation. Capacity planning should model ports/connections and failure-zone distribution, not only Mbps. A stable source IP is a finite shared resource.

## 3. What does an ExternalName Service not provide?

It provides DNS indirection to another name. It does not proxy traffic, validate destination addresses, manage health, preserve or rewrite HTTP authority, authenticate TLS, enforce redirects, or create application authorization. HTTPS may fail if the client uses the Service name for SNI/Host while the external server expects its own name. Use it only when the client protocol and ownership model are compatible and prove the actual TLS/HTTP behavior.

## 4. When can a selectorless Service be useful?

It can expose endpoints not represented by selected Pods—such as a platform-managed external or migrated service—through a Kubernetes Service identity. A trusted controller or owner must publish and retire EndpointSlices, validate addresses/ports, and represent health. Because that publisher can redirect traffic, it is an authority boundary. It is useful when the platform genuinely owns that mapping, not as a generic workaround for any external URL.

## 5. Why must redirects be revalidated?

A redirect creates a new destination and trust decision. It can change scheme, hostname, port, path, and address class, potentially reaching metadata, loopback, private networks, or another tenant. Reapply URL parsing, DNS/address classification, peer verification, TLS hostname checks, hop limits, and deadline. Strip credentials when authority changes unless explicitly approved. The regression test should include a public allowed origin redirecting to a forbidden private or link-local peer.

## 6. What is the security risk of forwarding credentials across redirect authority?

Authorization headers, cookies, or signed request material intended for one origin can be disclosed to another server. An attacker controlling the original or redirected response can harvest credentials. The client or proxy should remove sensitive credentials on authority change unless policy explicitly binds both authorities, and should never copy bearer tokens blindly. Evidence includes a redirect test to a controlled different authority verifying that credentials are absent.

## 7. What does stable egress IP prove?

It proves that traffic following that path can appear externally from a predictable network source, useful for partner allowlists and attribution. It does not prove which internal workload sent the request, that the destination is authentic, that bypass paths are impossible, or that application authorization succeeded. Many tenants may share the IP. Pair it with workload/application identity, route enforcement, bypass tests, and failover evidence for IPv4 and IPv6.

## 8. Why is FQDN policy implementation-specific?

Standard NetworkPolicy is primarily selector/CIDR/port based. FQDN-aware policy requires integration with DNS observation, TTLs, CNAMEs, wildcard rules, address updates, and enforcement state. Implementations differ in how they learn queries, retain addresses, prevent direct-IP bypass, handle rebinding, and support IPv6. Therefore, name the CNI/mesh version and test behavior under DNS changes and cache expiry rather than presenting it as portable Kubernetes semantics.

## 9. What should a private-endpoint design prove?

Prove that DNS resolves to the intended private address, route selection uses the private path, firewall/security-group policy permits only approved sources, the connected peer is the intended service, TLS names still validate, and public fallback/bypass is absent or deliberate. Include zone/region availability, endpoint ownership, quotas, and failure behavior. A private DNS zone alone does not prove packets stayed private.

## 10. What can a service mesh not repair about retries?

It cannot make a non-idempotent application effect safe, decide the authoritative idempotency key, or undo duplicated commits. Mesh retries can actually amplify work when combined with application and client retries. The service contract must define retryability, idempotency, deadline, and result replay. A mesh can enforce bounded transport attempts and telemetry, but correctness remains owned by the application/workflow. Test commit-with-lost-response through the complete retry stack.

## 11. Why should runtime Pods not need package-registry egress?

Course 3 produced immutable, self-contained OCI releases. Source and package retrieval belong to the build pipeline, where dependencies are pinned and verified. Allowing runtime Pods to fetch packages expands supply-chain attack surface, undermines reproducibility, and adds an unnecessary availability dependency. A negative egress test should show package registries are unreachable from the runtime namespace while the application still starts and operates using the released image.

## 12. How should egress dependency failure be represented?

Represent it according to the owning application contract: reject the initiating request, accept work durably and retry, return explicit partial/stale data, disable an optional feature, or fail closed. Do not convert a required dependency failure into a successful empty response. Network evidence should distinguish DNS, connect, TLS, policy, timeout, and remote status, while the application exposes a stable domain outcome. Preserve one deadline and bounded retry owner.
