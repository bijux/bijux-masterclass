# Module 06 — DNS, HTTP, TLS, and PKI

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.

> **Central question:** How does a client turn a name into an authenticated application connection, and where can that chain fail?

## Where this module fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary. The capstone increment is:

> **Serve Atlas through an HTTPS edge with a local trust chain, correct names, certificate verification, rotation evidence, and protocol-aware health checks.**

This result is required before the next module can build on it honestly.

## Learning outcomes

- Explain recursive resolution, authoritative data, caching, TTLs, and negative answers.
- Separate HTTP semantics from a particular transport version.
- Trace TLS negotiation, certificate path validation, hostname verification, SNI, and ALPN.
- Create and inspect a local CA and leaf certificate without normalizing insecure trust bypasses.
- Distinguish encryption, server authentication, client authentication, and application authorization.
- Diagnose name, trust, expiry, and protocol mismatch failures from evidence.

## Capstone increment

Serve Atlas through an HTTPS edge with a local trust chain, correct names, certificate verification, rotation evidence, and protocol-aware health checks.

## A name is an input to a chain of decisions

A client usually begins with a name, not an address. The operating system's name-service switch, local hosts file, configured recursive resolver, caches, search domains, and application library all influence the result. DNS itself is a distributed database: authoritative servers publish data; recursive resolvers perform and cache lookups on behalf of clients.

Do not reduce name resolution to “ask DNS.” Record:

```bash
getent ahosts atlas.example.invalid
dig atlas.example.invalid A
dig atlas.example.invalid AAAA
dig +trace atlas.example.invalid
resolvectl query atlas.example.invalid 2>/dev/null || true
```

`getent` follows the host's configured name-service policy and may include `/etc/hosts`; `dig` asks DNS directly. Their disagreement is evidence, not a contradiction.

## TTL is a cache lifetime, not a propagation guarantee

A positive TTL tells caches how long they may reuse a record. Negative responses can also be cached. Changing a record does not force every existing cache entry to disappear. A client may also cache resolved addresses independently or maintain existing connections after DNS changes.

For planned changes, reason about the previous TTL, change time, resolver behavior, connection lifetime, and rollback. Setting a low TTL one minute before a migration does not erase a record cached yesterday with a one-day TTL.

## HTTP semantics remain above the transport

HTTP defines methods, status codes, fields, representations, and cache semantics independently of whether a connection uses HTTP/1.1, HTTP/2, or HTTP/3. A reverse proxy can translate transport versions while preserving HTTP semantics.

Course 1 uses HTTP/1.1 in the teaching servers because its message framing is inspectable with ordinary tools. That does not make HTTP/1.1 the recommended endpoint version. The important host-level questions are listener ownership, connection reuse, header trust, body bounds, timeouts, and authenticated transport.

## TLS creates a protected channel only when validation succeeds

A typical TLS client and server negotiate a protocol version and cryptographic parameters, establish keys, authenticate at least the server through a certificate, and protect application bytes. TLS does not authorize an Atlas operation. It authenticates the peer name according to a trust policy and protects transport against relevant attackers.

Server certificate validation includes:

1. building a chain to a trusted anchor;
2. checking validity times and constraints;
3. verifying signatures and permitted use;
4. matching the requested host name to a subject alternative name;
5. applying local algorithm and policy restrictions.

Disabling verification removes the very property that distinguishes an authenticated TLS connection from an encrypted connection to an attacker.

## Names belong in subject alternative names

Modern hostname verification uses the certificate's Subject Alternative Name extension. The Atlas fixture certificate includes `atlas.test`, `localhost`, `127.0.0.1`, and `::1` because the local labs connect through those names and addresses. A production certificate should contain only the names required by its endpoint policy.

The certificate's common name is not a substitute for correct SANs. An IP address must be represented as an IP SAN, not a DNS SAN containing characters that look like an address.

Inspect the fixture:

```bash
openssl x509 -in capstone/pki/atlas.crt -noout \
  -subject -issuer -dates -ext subjectAltName
openssl verify -CAfile capstone/pki/ca.crt capstone/pki/atlas.crt
```

## SNI and ALPN influence the handshake

Server Name Indication carries the intended server name during the TLS handshake so one listener can select the correct certificate and configuration. Application-Layer Protocol Negotiation allows peers to select protocols such as HTTP/1.1 or HTTP/2.

A certificate can be valid for a name while the server selects the wrong virtual host because SNI or Host policy differs. Debug both layers:

```bash
openssl s_client -connect 127.0.0.1:18443 \
  -servername atlas.test \
  -CAfile capstone/pki/ca.crt \
  -verify_return_error
```

Then send an HTTP request with the intended `Host` field. TLS name and HTTP host usually align, but they are evaluated by different protocol layers.

## A private CA is a trust decision

The course creates a local fixture CA so the learner can see issuance and validation. Installing a CA into a system trust store grants it authority to authenticate any name allowed by local policy. Do not install a course CA on a shared host. Pass the CA file directly to the lab client.

Private keys are fixture material and are clearly marked. Production keys require protected generation, storage, access, rotation, and incident handling. Certificate automation is addressed later in the platform program.

## Rotation requires overlap and observation

A robust certificate rotation does not replace a file and hope. It prepares a new key/certificate, verifies name and chain, installs it atomically, reloads or restarts the edge, confirms the served certificate from a client path, and retains rollback material for a bounded period.

Clients may pin a private trust anchor, public CA, or intermediate. Rotating the leaf is different from rotating the issuer. A reload that succeeds syntactically can still serve the old certificate on another listener or instance.

## Worked investigation: curl works only with `-k`

`curl -k https://atlas.test` succeeds, while verified curl fails. `-k` is diagnostic evidence that the application may be reachable; it is not a repair.

Investigate in order:

1. Which address did `atlas.test` resolve to?
2. Which certificate did that address serve with SNI `atlas.test`?
3. Is the issuer trusted by the client?
4. Is the current time within the validity interval?
5. Does SAN contain the exact DNS name?
6. Does the chain include required intermediates?

Repair trust or naming. Retain one failing `openssl s_client -verify_return_error` transcript and the passing transcript after repair.

## DNS and TLS failure matrix

| Symptom | Likely layer | Decisive observation |
|---|---|---|
| name not found | name-service or DNS | `getent`, resolver query, authoritative record |
| connection timeout | route/firewall/listener | route and socket evidence |
| certificate unknown | trust chain | served chain and trust-anchor set |
| hostname mismatch | certificate naming | requested name and SAN |
| HTTP 421/host rejection | HTTP virtual host | Host field and edge policy |
| TLS alert before HTTP | handshake/policy | `openssl s_client` trace and server log |

A single browser error often collapses several of these categories. Reconstruct the chain.

## Atlas implementation bridge

The course PKI is generated from `create_pki.sh`. The tour passes the fixture CA explicitly to the client and verifies `atlas.test`. Inspect the served certificate with SNI and compare the TLS name to the HTTP Host policy.

Do not import the course CA into a system-wide trust store. Production certificate automation, public DNS control, revocation, and issuer rotation remain later platform responsibilities.

## Design review prompts

- Which name does the client verify?
- Which trust anchor authorizes the leaf?
- Does the edge present the same certificate on every listener?
- What happens during overlap rotation?
- Which error occurs before any HTTP request exists?

## Boundary case: trust store diversity

Browsers, operating systems, Java runtimes, containers, and language libraries can use different trust stores. A certificate that verifies with `openssl` may fail in another client because the intermediate chain, hostname policy, time source, or root set differs. Record the actual client and trust source used by the proof.

Private PKI also needs name constraints, issuance policy, revocation or short lifetimes, audit, and protected CA keys. The course fixture intentionally proves only the basic chain and hostname mechanics.

## Boundary case: clock correctness

Certificate validity and many authentication systems depend on time. A host with a badly skewed clock can reject valid certificates or accept not-yet-valid assumptions. Verify synchronization source and offset when TLS failures appear across many unrelated names.

## Name-to-request worksheet

```text
input name:
name-service source:
resolved addresses and TTL:
selected address/route:
SNI name:
served certificate fingerprint:
trust anchor:
verified SAN:
negotiated protocol:
HTTP Host and response:
```

This worksheet prevents a browser's combined error message from collapsing six independent layers.

## Field method: separate name, route, cryptographic identity, and HTTP authority

An HTTPS request crosses four distinct naming decisions. DNS maps a name to one or more addresses. Routing selects a path to an address. TLS SNI and hostname verification select and authenticate a certificate identity. HTTP authority selects an application virtual host. These values often match, but they are not interchangeable.

Investigate them separately:

```bash
dig +noall +answer atlas.test
ip route get 127.0.0.1
openssl s_client -connect 127.0.0.1:18443 \
  -servername atlas.test -verify_return_error \
  -CAfile capstone/pki/ca.crt </dev/null
curl --cacert capstone/pki/ca.crt \
  --resolve atlas.test:18443:127.0.0.1 \
  https://atlas.test:18443/health/live
```

A DNS answer can be correct while the wrong certificate is served. A certificate chain can validate while the requested name is absent. TLS can succeed while the HTTP Host value is rejected. `curl -k` removes peer verification and therefore changes the security claim; it is useful only as a bounded comparison during diagnosis.

Certificate rotation is a compatibility window. Publish new trust before presenting a new chain, verify all client populations, then retire old trust after the declared overlap. Track not only leaf expiry but intermediate and root validity, key usage, extended key usage, name constraints, revocation strategy, and time synchronization. A host with a badly skewed clock can reject an otherwise valid certificate.

The fixture CA and private keys in this course are intentionally local, visibly labelled, and unsafe for any external environment. Their purpose is to make path building and hostname verification observable. A production design should minimize certificate names, protect private keys through a managed or hardware-backed boundary where appropriate, and automate renewal without allowing an unverified fallback.

HTTP semantics remain independent of the selected transport version. A reverse proxy may accept HTTP/2 from clients and speak HTTP/1.1 to Atlas. Preserve method, status, authority, content framing, and retry semantics across the translation instead of assuming protocol-version symmetry.


## Standards and reference discipline

| Claim or rule | Category | Decisive evidence |
|---|---|---|
| HTTP semantics are independent of HTTP/1.1, HTTP/2, or HTTP/3 transport mapping. | RFC 9110 | message and intermediary behavior |
| TLS peer authentication requires certificate-chain and name verification. | RFC 8446 / RFC 9325 | `openssl verify`, verified client connection |
| DNS cache lifetime and connection lifetime are separate. | DNS protocol and application policy | resolver observation plus active connections |

A reference implementation may add behavior beyond a standard. A course policy may intentionally narrow legal behavior. Keep those claims separate when you write a runbook or defend a design.

## Failure patterns to recognize

### Verification bypass

Using `-k` or an unverified TLS context hides the trust failure rather than repairing it.

### TTL mythology

Lowering a DNS TTL after caches already stored a longer value does not invalidate those entries.

### Certificate equals authorization

A valid server certificate authenticates the endpoint name; it does not authorize an application action.


## Module synthesis

Return to the central question: **How does a client turn a name into an authenticated application connection, and where can that chain fail?**

A complete answer names the owner of the relevant state, the transition that changes it, the failure boundary, and the observation that would falsify the claim. The capstone is ready to progress only when the new mechanism works and the planted defect—**The client disables certificate verification to “fix” a hostname mismatch, converting a naming error into loss of peer authentication.**—fails for the predicted reason.

## Continue

Module 07 places explicit traffic boundaries and intermediaries around the HTTPS endpoint.

## Module route

1. [Complete the exercises](exercises.md) before viewing solutions.
2. [Compare with the worked answers](exercise-answers.md).
3. [Run the controlled lab](lab.md).
4. [Retain the checkpoint evidence](checkpoint.md).
