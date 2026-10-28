# Network investigation command map

Commands are useful only when they answer a previously stated question. This field guide maps common questions to evidence sources and records the limits of each observation. It is deliberately organized by transition rather than by favorite tool.

## 1. Resolve the logical destination

Questions:

- Which name did the application actually query?
- Which search suffixes and `ndots` rules expanded it?
- Which A, AAAA, CNAME, or SRV answers were returned?
- Was the answer positive, negative, cached, or truncated?

Typical evidence:

```bash
cat /etc/resolv.conf
getent ahosts atlas-api.atlas-system.svc
getent hosts atlas-api.atlas-system.svc.cluster.local

dig atlas-api.atlas-system.svc.cluster.local A

dig atlas-api.atlas-system.svc.cluster.local AAAA

dig +tcp atlas-api.atlas-system.svc.cluster.local A
```

Inside Kubernetes, also inspect the Service, EndpointSlices, CoreDNS Service/endpoints, and CoreDNS configuration. `dig` with an absolute name does not reproduce an application lookup that used search expansion. A successful answer does not prove the returned address is reachable.

## 2. Identify the source namespace and socket

Questions:

- Which process opened the socket?
- Which namespace contains the interface and route?
- Which local address and port were selected?
- Is the application listening on loopback, Pod IP, wildcard, IPv4, or IPv6?

Typical evidence:

```bash
ss -lntup
ss -nto
lsof -nP -i
cat /proc/<pid>/net/tcp
```

Where privileges and tooling permit:

```bash
nsenter -t <pid> -n ip addr
nsenter -t <pid> -n ip route get <destination>
nsenter -t <pid> -n ss -nto
```

A listening socket proves local readiness to accept a connection on that address. It does not prove Service selection, NetworkPolicy, remote routing, or application-level readiness.

## 3. Prove route and source-address selection

Questions:

- Which route wins for this exact destination?
- Which interface and source address will the kernel use?
- Is policy routing involved?
- Does the return source have a valid route back?

Typical evidence:

```bash
ip -4 route get 10.244.2.19
ip -6 route get fd00:10:244::19
ip rule show
ip route show table all
ip -6 route show table all
ip neigh show
ip -6 neigh show
```

Run the lookup in the relevant network namespace. A host route lookup can differ from a Pod route lookup. Record the exact destination and family rather than dumping routes without a question.

## 4. Observe CNI attachment state

Questions:

- Which plugin chain was invoked?
- Which interface, address, route, and DNS data were returned?
- Does the attachment identity still correspond to a live sandbox?
- Is leaked IPAM or host-side state present?

Evidence depends on the implementation, but normally includes:

- runtime sandbox identity and network namespace;
- CNI configuration list and plugin versions;
- plugin logs for `ADD`, `CHECK`, `DEL`, `GC`, and `STATUS` where supported;
- host and Pod interfaces;
- IPAM allocation records;
- routes, tunnels, eBPF maps, or bridge state owned by the implementation.

Do not delete host interfaces or allocator records until the owner and generation are established. Manual cleanup can turn one leaked record into duplicate address ownership.

## 5. Join Service intent to endpoint state

Questions:

- Which Service port and selector are declared?
- Which EndpointSlices belong to the Service?
- Which endpoints are ready, serving, or terminating?
- Are ports, protocols, and address families consistent?

Typical evidence:

```bash
kubectl get service atlas-api -n atlas-system -o yaml
kubectl get endpointslice -n atlas-system \
  -l kubernetes.io/service-name=atlas-api -o yaml
kubectl get pod -n atlas-system -l app.kubernetes.io/name=atlas-api \
  -o wide
```

Construct a join table rather than reading the objects separately:

```text
Pod UID | Pod IP | Node | Ready | terminating | slice | port | generation
```

Correct objects still do not prove that every Node or proxy has programmed the latest backend set.

## 6. Inspect the Service data plane

First identify the implementation. Possible evidence surfaces include:

- kube-proxy mode and logs;
- nftables or iptables rules;
- IPVS virtual services and real servers;
- eBPF maps and flow records;
- user-space proxy configuration;
- cloud load-balancer backend state.

Do not run an iptables-specific checklist before confirming that iptables owns the Service path. Record the desired endpoint generation and the generation or timestamp programmed on each affected Node.

For an incident involving a removed endpoint, separate:

- a new connection created after convergence;
- an established connection created before withdrawal;
- an HTTP request reusing an existing keep-alive or HTTP/2 connection.

## 7. Evaluate NetworkPolicy

Questions:

- Does any policy select the source for egress?
- Does any policy select the destination for ingress?
- Which union of rules allows each direction?
- Which labels are acting as security attributes?
- Does the installed implementation enforce the relevant traffic class?

Typical evidence:

```bash
kubectl get networkpolicy -A -o yaml
kubectl get namespace --show-labels
kubectl get pod -A --show-labels -o wide
```

Then execute a positive and negative connection test using fresh connections. A YAML review alone cannot prove enforcement. A successful connection can be an existing tracked flow, host traffic outside the intended policy path, or a workload not selected for isolation.

## 8. Inspect Gateway API attachment

Questions:

- Which GatewayClass/controller owns the Gateway?
- Is the Gateway accepted and programmed for the current generation?
- Which listener accepts the Route kind and namespace?
- Do hostnames intersect?
- Are cross-namespace references granted by the target namespace?
- Are backend references resolved?

Typical evidence:

```bash
kubectl get gatewayclass -o yaml
kubectl get gateway -A -o yaml
kubectl get httproute -A -o yaml
kubectl get referencegrant -A -o yaml
```

For each condition, record type, status, reason, message, observed generation, parent, and reporting controller. `Programmed=True` does not prove DNS, firewall, TLS, or application behavior.

## 9. Verify TLS and HTTP authority

Questions:

- Which name is the client authenticating?
- Which certificate is selected by SNI?
- Does the chain reach the intended trust anchor?
- Is the HTTP authority accepted by the Gateway?
- Is backend TLS verified independently?

Typical evidence:

```bash
openssl s_client \
  -connect <address>:443 \
  -servername atlas.example.invalid \
  -verify_hostname atlas.example.invalid \
  -CAfile atlas-ca.crt

curl --resolve atlas.example.invalid:443:<address> \
  --cacert atlas-ca.crt \
  https://atlas.example.invalid/api/health
```

A request made with TLS verification disabled cannot support an identity claim. Pinning DNS with `--resolve` is useful because it keeps hostname verification while testing a chosen socket address.

## 10. Capture packets with a defined oracle

Before using `tcpdump`, state:

- expected source and destination addresses;
- ports and protocol;
- interface or namespace;
- whether you expect inner or outer encapsulated packets;
- connection start time;
- size and time bound;
- payload sensitivity.

Example bounded capture:

```bash
timeout 20 tcpdump -ni any \
  'host 10.244.2.19 and tcp port 8080' \
  -c 200 -w incident.pcap
```

A packet missing from `any` on one Node does not prove it never existed elsewhere. Capture at the source namespace, source Node, destination Node, and destination namespace as needed. Keep capture artifacts under controlled retention because they can contain credentials, identifiers, and payload data.

## 11. Test egress as a resolved-peer transaction

Questions:

- Which URL and redirect chain were accepted?
- Which addresses did the approved resolver return?
- Which address did the socket actually connect to?
- Which TLS identity was verified?
- Did NAT, proxy, or private endpoint state become the bottleneck?

Evidence should include normalized URL, resolver answers, address classification, connected peer, certificate identity, deadline, retry count, and response size. Revalidate every redirect. A hostname allowlist without connected-peer verification is vulnerable to resolution changes.

## 12. Preserve evidence before restarting

Restarts can repair stale caches, agents, proxies, and controllers, but they also destroy process state and make the original cause harder to establish. Before restart, collect:

- object generations and conditions;
- process and agent versions;
- endpoint and policy generations;
- route, neighbor, tunnel, map, or rule state;
- logs around the first failure;
- bounded flow or packet evidence;
- a timestamped hypothesis;
- the expected state change caused by the restart.

After restart, rerun the same oracle. “Restart fixed it” is not a root cause; it is evidence that some restart-owned state influenced the path.
