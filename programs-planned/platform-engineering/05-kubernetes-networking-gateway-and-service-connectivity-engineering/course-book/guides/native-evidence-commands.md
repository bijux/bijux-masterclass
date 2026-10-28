# Guide — native network evidence commands

Commands are useful only when tied to a hypothesis and observation point. The examples below are templates; replace names, namespaces, addresses, and interfaces with the actual flow.

## Routes and addresses

```bash
ip -brief address
ip -4 route
ip -6 route
ip route get 10.244.2.17 from 10.244.1.8
ip -6 route get fd00:10:244:2::17 from fd00:10:244:1::8
ip neigh show
```

Run them in the correct network namespace. A host route table is not a Pod route table.

## Sockets

```bash
ss -lntup
ss -tn state established
lsof -nP -iTCP:8080 -sTCP:LISTEN
```

Record bind address, family, port, process, and namespace. `0.0.0.0` and `::` behavior can differ by system configuration.

## DNS

```bash
dig +noall +answer +authority atlas-api.atlas-system.svc.cluster.local A
dig +noall +answer +authority atlas-api.atlas-system.svc.cluster.local AAAA
dig +search atlas-api
dig +tcp atlas-api.atlas-system.svc.cluster.local
```

Preserve query type, response code, TTL, server, and timing. A short-form command that omits these fields is weaker evidence.

## TLS and HTTP

```bash
openssl s_client \
  -connect 127.0.0.1:18443 \
  -servername atlas.example.invalid \
  -CAfile capstone/pki/ca.crt \
  -verify_hostname atlas.example.invalid

curl --resolve atlas.example.invalid:18443:127.0.0.1 \
  --cacert capstone/pki/ca.crt \
  https://atlas.example.invalid:18443/api/whoami
```

Do not use `-k` or disable verification in evidence meant to establish identity.

## Kubernetes objects

```bash
kubectl get pod,service,endpointslice -n atlas-system -o wide
kubectl describe service atlas-api -n atlas-system
kubectl get networkpolicy -A -o yaml
kubectl get gateway,httproute -A -o yaml
kubectl get events -A --sort-by=.lastTimestamp
```

Status and events are control-plane evidence. Pair them with a protocol probe.

## Packet capture

```bash
tcpdump -ni any 'host 10.244.2.17 and tcp port 8080'
tcpdump -ni eth0 -vv 'icmp or icmp6'
```

Use the smallest filter that still captures the hypothesis. Record interface, namespace, clock, snap length, and whether checksum offload can affect interpretation.
