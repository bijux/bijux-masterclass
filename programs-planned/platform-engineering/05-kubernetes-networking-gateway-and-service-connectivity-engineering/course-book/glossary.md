# Glossary

**Address domain** — A set of addresses with one ownership and routing meaning, such as Pod, Node, Service, public, or external dependency addresses.

**ALPN** — TLS extension used to negotiate an application protocol such as HTTP/2.

**BackendTLSPolicy** — Gateway API policy for authenticating TLS connections from a Gateway implementation to a backend, subject to implementation support.

**CNI** — Container Network Interface specification defining how a runtime invokes network plugins and exchanges results.

**ClusterIP** — Stable virtual Service destination interpreted by the Service data plane; normally not an address bound to a host interface.

**Connected peer** — The address to which the socket actually connected, distinguished from a hostname or earlier DNS answer.

**Control plane** — Components that store desired state and produce configuration decisions.

**Data plane** — Components and programmed state that handle packets or connections.

**EndpointSlice** — Kubernetes API object representing scalable backend endpoint membership and conditions for a Service.

**Egress** — Traffic leaving a workload or trust boundary toward another service or network.

**Encapsulation** — Wrapping an inner packet inside an outer packet, usually adding MTU overhead.

**Gateway** — Gateway API resource requesting listeners and infrastructure behavior from a GatewayClass implementation.

**GatewayClass** — Cluster-scoped Gateway API resource identifying a controller and class of Gateway infrastructure.

**Headless Service** — Service with no ClusterIP, commonly publishing endpoint addresses directly through DNS.

**HTTP authority** — The logical target host and optional port carried by HTTP, such as `Host` or `:authority`.

**IPAM** — IP address management: allocation, ownership, release, recovery, and garbage collection of addresses.

**Listener** — Gateway port/protocol/hostname attachment point that can accept compatible Routes.

**MTU** — Maximum transmission unit supported by a link or interface before fragmentation or rejection.

**NAT** — Network address translation, which changes source or destination addresses and creates state that affects identity and capacity.

**Negative caching** — Retaining a DNS failure such as NXDOMAIN for a bounded time.

**NetworkPolicy** — Kubernetes L3/L4 allow-list API whose effect depends on a supporting implementation.

**North-south traffic** — Traffic entering or leaving the cluster/application boundary.

**East-west traffic** — Traffic among workloads or services inside the platform boundary.

**Overlay** — Network that transports inner Pod packets across an underlay, often using encapsulation.

**Packet-path ledger** — Table of expected packet identity, owner, transformation, observation, and negative control at every boundary.

**Path MTU** — Smallest MTU along an end-to-end path.

**Programmed generation** — Version of desired endpoint or route state actually installed in a data plane.

**ReferenceGrant** — Gateway API resource in a target namespace that authorizes specific cross-namespace references.

**Route** — Gateway API object such as HTTPRoute that attaches application routing rules to compatible listeners.

**SNI** — TLS Server Name Indication sent before HTTP to select and authenticate a logical server name.

**Service data plane** — Implementation that maps a Service destination to eligible endpoints using kernel, proxy, eBPF, cloud, or other mechanisms.

**Session affinity** — Bounded preference to select the same backend for a client key; not durable identity or authorization.

**Source preservation** — Retaining the original network source address through forwarding; separate from authenticated identity.

**Traffic distribution** — Preference for selecting endpoints based on topology while retaining fallback, depending on feature support.

**Traffic policy** — Hard endpoint eligibility rule such as local-only behavior for internal or external Service traffic.

**Underlay** — Network that carries Node or outer tunnel traffic.

**Wildcard hostname** — Hostname pattern with specification-defined matching; not an arbitrary regular expression.

**Workload identity** — Cryptographically or administratively established identity of a workload, separate from an ephemeral IP address.
