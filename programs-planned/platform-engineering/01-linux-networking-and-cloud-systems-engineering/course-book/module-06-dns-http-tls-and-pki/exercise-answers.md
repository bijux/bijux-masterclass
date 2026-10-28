# Worked Answers — Module 06: DNS, HTTP, TLS, and PKI

These answers demonstrate reasoning. Equivalent answers are valid when they preserve the same mechanism and evidence boundary.

## Exercise 1 — Resolver versus DNS

The system name-service switch may consult `/etc/hosts`, DNS, mDNS, or other sources and apply search domains. `dig` sends DNS queries directly to a selected resolver. The difference reveals which naming layer supplied the address. Applications often follow system resolution, so diagnose with both rather than declaring one wrong.

## Exercise 2 — TTL planning

Resolvers that cached the old record may reuse it for the remainder of the original 86400-second TTL. Changing the authoritative TTL does not invalidate those entries. Existing connections can persist even longer. Lower the TTL at least one old-TTL interval before migration, then observe resolver and connection behavior.

## Exercise 3 — HTTP over TLS

It can prove negotiated transport parameters and authenticated peer identity when chain and name validation succeed. It does not prove the HTTP Host is accepted, the route exists, the user is authorized, or the backend is healthy. Protocol layers must be tested separately.

## Exercise 4 — SAN matching

Current hostname verification relies on the Subject Alternative Name extension. The course requires explicit DNS and IP SAN entries for the names used. Depending on legacy common-name fallback creates client inconsistency and weakens the naming contract. Reissue the certificate with correct SANs.

## Exercise 5 — IP SAN

No. An IP literal is matched against an IP Address SAN, not a DNS SAN that happens to contain digits and dots. The fixture contains an IP SAN for 127.0.0.1. Alternatively connect using a verified DNS name that resolves to loopback.

## Exercise 6 — SNI and Host

SNI in the TLS handshake can select a certificate for `atlas.test`, while the later HTTP Host field names another virtual host or is absent/invalid. The edge evaluates both layers. Capture the SNI name, served certificate, and Host field separately.

## Exercise 7 — Private CA risk

A trusted CA can authenticate any name permitted by local validation policy. Its fixture private key is shipped with the course, so any holder could mint certificates. Passing it directly to the lab client confines trust to the experiment. System-wide installation would create a broad persistent trust vulnerability.

## Exercise 8 — Rotation oracle

Connect from a client path with SNI and verification, then inspect the served leaf fingerprint, SANs, issuer, and dates. Checking the file on disk or a successful reload command is insufficient when another process, listener, or instance may still serve the old certificate.

## Exercise 9 — TLS version policy

The server may also permit obsolete versions or weak configuration, present an invalid certificate, mishandle keys, or skip client validation. Secure use combines protocol version, algorithms, certificate validation, key management, and endpoint policy. RFC 9325 provides broader operational guidance.

## Exercise 10 — Negative DNS caching

A resolver may have cached a prior NXDOMAIN or negative response according to the zone's negative caching rules. Query authoritative data and the recursive resolver separately, then wait for or flush the relevant cache under controlled policy. Repeated application retries do not force authoritative refresh.

## Exercise 11 — Debug `-k`

Network reachability, TCP, TLS encryption, and some HTTP behavior may work, but peer authentication is broken. The failure likely concerns trust chain, hostname, validity, or certificate policy. `-k` is useful to localize the layer; it must not remain in the repair.

## Exercise 12 — End-to-end evidence

Record name resolution, selected address and route, listener/edge process, TLS version and served chain, successful hostname and trust validation, HTTP Host, readiness status/body, and backend readiness evidence. This chain distinguishes naming, transport, trust, edge routing, and application readiness.
