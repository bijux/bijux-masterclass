# Guide — diagnose Kubernetes DNS without guessing

DNS incidents are often “fixed” by restarting CoreDNS or the application. That can clear a cache and erase the evidence. Use the following sequence instead.

## 1. Record the exact name the application used

A short name, partially qualified name, and fully qualified name can generate different candidate queries. Capture `/etc/resolv.conf`, `search`, `options ndots`, and the application runtime.

## 2. Reproduce the candidate sequence

Query A and AAAA explicitly. Use an absolute trailing-dot name to bypass search expansion. Query over UDP and TCP when relevant. Record response code, TTL, and authoritative or negative-cache information.

## 3. Identify the cache layers

Possible caches include:

- application or language runtime;
- libc or local resolver;
- node-local DNS cache;
- CoreDNS cache;
- upstream recursive resolver;
- authoritative service.

A cache hit at one layer can persist after another layer changes.

## 4. Compare DNS intent with Service state

For a normal Service, compare A/AAAA records with ClusterIPs. For a headless Service, compare answers with EndpointSlice addresses and readiness publication rules. For SRV, verify port name, target, and port.

## 5. Prove DNS transport

Under default deny, verify both UDP and TCP 53 to the actual DNS endpoints. A successful query before policy is not evidence after policy.

## 6. Stop once DNS has answered its question

If the correct address is returned, move to route, policy, transport, TLS, and application evidence. DNS does not prove reachability or peer identity.

## Failure signatures

| Observation | Likely next investigation |
|---|---|
| NXDOMAIN before Service creation, persists after | negative cache and TTL |
| one family answers, other times out | dual-stack resolver or transport path |
| FQDN works, short name fails | search path or namespace |
| UDP fails, TCP works | MTU, fragmentation, or policy path |
| DNS works, connect fails | route, policy, Service, or listener |
