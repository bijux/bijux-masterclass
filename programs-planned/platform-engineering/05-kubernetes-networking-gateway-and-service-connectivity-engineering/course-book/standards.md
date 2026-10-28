# Standards and version profile

This course distinguishes four kinds of claim:

1. **Normative specification** — a published contract such as the Kubernetes API, CNI specification, Gateway API, HTTP, or TLS.
2. **Reference implementation behavior** — what a selected CNI, DNS server, service data plane, or Gateway controller actually implements.
3. **Atlas platform policy** — choices made for the cumulative capstone, such as default deny, frontend TLS termination, or the decision not to add a service mesh.
4. **Executed evidence** — what was actually run in the release environment.

Confusing these categories is a major source of false confidence. A valid NetworkPolicy object does not prove enforcement. A conformant Gateway API implementation does not prove that a cloud address was provisioned. A local TLS exchange does not prove managed-load-balancer behavior.

## Pinned conceptual baseline

| Area | Course baseline | Role |
|---|---|---|
| Kubernetes | 1.36.2 | Service, EndpointSlice, DNS, policy, traffic distribution, and API behavior |
| CNI specification | 1.1.0 | runtime/plugin lifecycle, result, cleanup, garbage collection, and status contract |
| Gateway API | 1.6.1 Standard channel | role-oriented listeners, routes, references, status, and conformance |
| kind | 0.32.0 with Kubernetes 1.36.1 node image | optional disposable local-cluster lane |
| Cilium | 1.20.0 | optional CNI, policy, kube-proxy replacement, Gateway, and Hubble lane |
| CoreDNS | 1.14.6 | DNS implementation reference |
| Envoy Gateway | 1.8.3 | comparative Gateway implementation reference |
| HTTP | RFC 9110 family | request semantics, authority, retries, intermediaries, and caching |
| TLS | TLS 1.2 and TLS 1.3 deployment profile | peer authentication and transport protection |

Patch-level differences are recorded rather than hidden. The optional kind lane defaults to Kubernetes 1.36.1 while the conceptual course baseline is Kubernetes 1.36.2. Evidence from that lane must therefore name the actual cluster version.

## Primary source map

| Subject | Primary source |
|---|---|
| Kubernetes networking model | [Cluster networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/) |
| Services and virtual IPs | [Services, Load Balancing, and Networking](https://kubernetes.io/docs/concepts/services-networking/) |
| EndpointSlices | [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/) |
| DNS | [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) |
| NetworkPolicy | [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) |
| Service traffic distribution | [Service traffic distribution](https://kubernetes.io/docs/concepts/services-networking/service/#traffic-distribution) |
| CNI | [CNI specification 1.1.0](https://www.cni.dev/docs/spec/) |
| Gateway API | [Gateway API documentation](https://gateway-api.sigs.k8s.io/) |
| Gateway API conformance | [Conformance profiles](https://gateway-api.sigs.k8s.io/concepts/conformance/) |
| Cilium | [Cilium 1.20 documentation](https://docs.cilium.io/en/stable/) |
| CoreDNS | [CoreDNS manual](https://coredns.io/manual/toc/) |
| Envoy Gateway | [Envoy Gateway documentation](https://gateway.envoyproxy.io/) |
| HTTP semantics | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) |
| TLS 1.3 | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) |

The course book explains the required concepts without requiring these sources to be open during study. The links are provided for normative review and implementation-specific follow-up.

## Normative versus implementation claims

The CNI specification defines the contract between a runtime and plugins. It does not prescribe a particular route, tunnel, policy engine, IPAM database, or Service implementation.

Kubernetes defines Service, EndpointSlice, NetworkPolicy, and related API semantics. The selected data-plane implementation determines where translation and enforcement occur, which diagnostic surfaces exist, and how quickly state converges.

Gateway API defines resources, attachment, references, status, release channels, and conformance profiles. A controller supports a specific set of resources and features. The course records the exact features Atlas consumes rather than claiming universal Gateway API support.

CoreDNS, Cilium, Envoy Gateway, kube-proxy, cloud load balancers, and managed DNS are implementations. Their versions, configuration, and runtime evidence must be recorded before making operational claims.

## Atlas Connectivity Plane profile

Atlas Connectivity Plane 1.0 makes these deliberate decisions:

- Gateway API is the primary north-south routing contract.
- HTTPS terminates at the shared Gateway in the accepted baseline.
- The Gateway-to-backend hop is documented as plaintext HTTP; it is not described as end-to-end TLS.
- `PreferDualStack` is a desired Service policy, while IPv4 and IPv6 require independent proof.
- default deny is accepted only with explicit DNS, Gateway, and approved-client flows;
- forwarding identity is replaced at the trusted Gateway boundary rather than appended to untrusted headers;
- egress policy validates the connected peer and every redirect, not only the originally requested hostname;
- non-idempotent retries require an idempotency contract and a replayable body;
- a service mesh is rejected until a named requirement and measured gap justify the additional control and data planes;
- persistent-storage and CSI semantics are transferred to Course 6 rather than implied by network reachability.

These are Atlas design choices, not universal standards requirements.

## Evidence rule

A release may state only the strongest evidence actually executed:

```text
document
→ semantic model
→ local sockets and TLS
→ disposable Kubernetes cluster
→ real cloud/network environment
→ operated evidence over time
```

Higher lanes do not erase the lower ones. A live cluster can still contain an incorrect architecture; a correct semantic model can still fail on a real implementation. Production confidence requires both sound contracts and environment evidence.
