# Module 57 — TLS and HTTPS: Certificates, Trust, Identity, SNI, and ALPN

**Progress: 57/100**

## The governing question

> Which facts does a successful TLS connection establish, which configuration establishes them, and how do you test identity failures without disabling the security property under study?

## Why this module comes now

The HTTP client and server contracts are complete over cleartext transport. TLS now adds confidentiality, integrity, and authenticated peer identity under a configured trust policy. It does not change the application route model, idempotency rules, or authorization. Keeping the layers separate lets the same ServiceWire application run behind HTTP/1.1, HTTPS, or HTTP/2 adapters.

TLS vocabulary is frequently blurred. “The certificate is valid” can mean chain validation, time validity, hostname matching, key usage, or merely that bytes parsed. This module requires each claim to name its evidence.

## Observable outcomes

By the end of the module, you can:

- distinguish encryption, integrity, chain trust, hostname verification, SNI, ALPN, and application authorization;
- load server keys and certificate chains under explicit ownership;
- configure a client with a dedicated trust anchor;
- verify the logical hostname even when connecting to a deterministic local address;
- inspect negotiated protocol and peer certificate information safely;
- classify certificate, identity, protocol, and socket failures;
- rotate TLS configuration without exposing private keys in logs;
- close TLS servers and sockets through the same lifecycle discipline as cleartext servers;
- explain why local fixtures are teaching credentials, not production credentials.

## The TLS assurance ladder

| Layer | Question |
|---|---|
| record protection | are bytes encrypted and integrity-protected after handshake? |
| chain trust | does the peer certificate chain to a configured trust anchor? |
| certificate validity | is it valid for the current time and intended usage? |
| hostname identity | does the certificate identify the requested logical host? |
| SNI | which name did the client present for server certificate selection? |
| ALPN | which application protocol was negotiated? |
| authorization | may this authenticated peer perform the operation? |

Success at one row does not imply success at later rows.

## Trust anchors and identity

A certificate chain is trusted when validation reaches a trust anchor configured by the client or platform. Hostname verification then checks whether the certificate's subject alternative names identify the requested service name.

A local teaching setup should use:

- one dedicated local CA certificate trusted only by tests;
- a server leaf certificate signed by that CA;
- SAN entries for `localhost` and `127.0.0.1` when both are tested;
- a server private key stored only in fixture scope;
- explicit `ca` and `servername` client options.

This exercises the real chain and identity mechanisms. `rejectUnauthorized: false` bypasses both and makes a success test meaningless.

## SNI preserves logical name at a shared endpoint

Server Name Indication carries a hostname during the handshake so a server can select credentials for several logical services on one address. A connector that dials a resolved IP should still supply the logical hostname as `servername` when appropriate.

SNI is visible before application data and is not a secret channel. It is a certificate-selection and identity mechanism.

A server may use an `SNICallback` to choose a secure context. If it does, the callback becomes part of startup and rotation policy:

- contexts must be built before publication;
- missing names need explicit fallback or rejection;
- private key errors must fail safely;
- rotation must not mix incompatible key/certificate pairs.

## ALPN chooses the application protocol

Application-Layer Protocol Negotiation allows peers to select protocols such as `h2` or `http/1.1` during TLS handshake. A successful TLS channel can still be unusable if the required application protocol was not negotiated.

The client should verify its requirement:

```ts
if (socket.alpnProtocol !== 'http/1.1') {
  socket.destroy(new Error('required ALPN protocol not negotiated'));
}
```

An empty negotiated value can be legal when neither side requires ALPN. Product policy decides.

Module 58 will use HTTP/2. This module makes negotiation explicit before multiplexing appears.

## HTTPS is HTTP over TLS, not a different application

`https.createServer()` supplies TLS transport and then Node's HTTP message layer. The route adapter should remain the same. Do not duplicate validation and domain code inside an HTTPS-specific handler.

A reusable server factory can accept either:

```ts
type TransportConfig =
  | { readonly kind: 'http' }
  | {
      readonly kind: 'https';
      readonly key: Buffer;
      readonly cert: Buffer;
      readonly ca?: readonly Buffer[];
    };
```

The transport adapter owns handshake and socket diagnostics. The application owns routes and jobs.

## Certificate parsing versus authorization

A server can request client certificates for mutual TLS. Successful client-certificate validation authenticates a certificate identity. Mapping that identity to application permissions is a separate authorization policy.

Course 6 uses server authentication only. If you add mutual TLS as transfer work, define:

- accepted issuer;
- SAN or subject mapping;
- revocation/rotation assumptions;
- authorization mapping;
- behavior when no certificate is supplied;
- audit fields that do not leak certificate material.

## Failure taxonomy

Useful TLS failures include:

```text
UNTRUSTED_ISSUER
CERTIFICATE_EXPIRED
HOSTNAME_MISMATCH
PROTOCOL_VERSION
CIPHER_OR_HANDSHAKE_FAILURE
ALPN_MISMATCH
PEER_CLOSED
DEADLINE
CANCELLED
```

Do not return raw internal errors to remote clients. On the client, preserve stable classification plus bounded cause. On the server, handshake failure may occur before HTTP exists, so there may be no request ID or problem response.

## Private-key handling

Private keys are high-sensitivity inputs.

- never include key bytes in errors or debug inspection;
- restrict fixture and production file permissions;
- avoid copying into general configuration dumps;
- validate key/certificate matching during startup;
- keep old context available until new context is complete if rotating;
- zeroization in JavaScript is limited because buffers and runtime copies can exist—state this honestly.

The course's fixture key exists only for local tests and must never be deployed.

## TLS deadlines and ownership

Handshake consumes the same overall client deadline. A socket can connect at TCP level but stall during TLS. The owner must abort and close on deadline or cancellation.

On the server, accepted raw connections that never complete handshake consume resources. Configure handshake and socket policies and include them in connection admission.

TLS close has an orderly protocol signal, but abrupt socket destruction remains possible. The product should distinguish complete HTTP response from transport teardown, as before.

## Worked case — deterministic local identity

A test server listens on `127.0.0.1`. The logical URL is `https://localhost:PORT`. The certificate SAN includes `DNS:localhost` and `IP:127.0.0.1`.

Client options:

```ts
const socket = tls.connect({
  host: '127.0.0.1',
  port,
  servername: 'localhost',
  ca: [caCertificate],
  ALPNProtocols: ['http/1.1'],
});
```

This preserves:

- deterministic address;
- logical hostname;
- SNI;
- chain trust;
- hostname verification;
- ALPN requirement.

A wrong-host test uses `servername: 'wrong.test'` and must fail. The repair is not to disable verification; it is to use the expected identity or issue the correct certificate.

## Certificate fixtures and time

Certificates have validity windows. Long-lived course archives can eventually contain expired fixtures. The verification route should classify an expired fixture clearly and document regeneration. A production system should automate renewal and deployment without relying on static repository keys.

For this course, fixture generation uses a long but finite local validity period and the release notes state the boundary. Tests still validate dates under the runtime's normal TLS behavior.

## TLS does not solve application replay

TLS protects one channel. It does not make a POST idempotent, preserve job records across restart, or authenticate an idempotency key as belonging to a user. Those remain application and later persistence concerns.

Similarly, HTTPS does not mean “safe input.” Every HTTP validation and bound from Modules 54–56 remains necessary.

## Common wrong models

### “Encrypted means authenticated”

Encryption without correct peer identity can protect a channel to the wrong party.

### “Trusted certificate means correct hostname”

Chain trust and name matching are separate checks.

### “SNI is the same as Host”

They can carry related names at different protocol layers and can differ under proxies or misconfiguration.

### “ALPN automatically gives HTTP/2”

Both peers must offer/select it, and the application must create the appropriate protocol stack.

### “Turn off verification for tests”

That removes the behavior the test should prove.

## Decision procedure

1. Define logical service name.
2. Define trust anchors.
3. Define accepted certificate identity.
4. Define SNI behavior.
5. Define required ALPN protocols.
6. Load key/certificate without logging secrets.
7. include handshake in deadline and admission.
8. classify pre-HTTP failures.
9. define rotation/startup rollback.
10. test trusted name, wrong name, untrusted CA, and ALPN mismatch.

## ServiceWire increment

Add HTTPS using the same finite application adapter. The runtime accepts paths to a local key, certificate, and optional CA chain. The client supplies trusted CA and server name. Startup validates files before publishing listeners.

## Case study — dial an IP, verify a hostname

A local integration test listens on `127.0.0.1`, but the certificate contains `DNS:localhost`. The client must keep two values:

```text
connect host: 127.0.0.1
server name:  localhost
```

The first chooses the network destination. The second drives SNI and certificate name verification. Replacing both with the IP changes the identity contract. Disabling verification makes the test stop testing TLS identity entirely.

The test trust store contains the course CA certificate. It does not add that CA globally. This keeps trust local to the client instance and avoids changing the machine’s security configuration.

### What a successful handshake establishes

Under the configured policy, a successful TLS connection establishes evidence that:

- a peer completed the cryptographic handshake;
- the peer presented a chain accepted by the configured trust anchors;
- the certificate is valid for the expected server name;
- the negotiated protocol and cipher satisfy the runtime and application policy;
- the connection traffic is protected against passive observation and undetected modification under the protocol assumptions.

It does not establish that:

- the application is authorized to perform a domain operation;
- the remote process is healthy;
- the HTTP response is semantically valid;
- the private key has never been compromised;
- DNS or routing selected the intended organizational service without further policy.

TLS supplies authenticated transport evidence, not complete application trust.

### SNI and ALPN are separate negotiations

SNI tells a multi-tenant server which logical name the client expects. ALPN negotiates the application protocol, such as `h2` or `http/1.1`. A certificate may verify while ALPN selects an unsupported protocol. Conversely, ALPN may negotiate `h2` while certificate verification fails. The client should check both under the same handshake deadline.

### Credential ownership and rotation

A server startup path owns key and certificate loading. It should validate that files can be read and that a test server can be constructed before publishing readiness. Private key bytes must not enter logs, error rendering, snapshots, or test diffs.

Rotation introduces a lifecycle question: replace credentials for new handshakes while existing connections continue under their established session, or restart listeners through a staged process. Node provides mechanisms for secure contexts, but the product must define the transition and rollback policy.

### Failure classification

| Failure | Phase | Typical client evidence |
|---|---|---|
| TCP refused | connect | OS error code |
| handshake deadline | handshake | timeout/cancellation |
| untrusted issuer | verification | certificate-chain failure |
| wrong hostname | verification | identity mismatch |
| ALPN mismatch | negotiation | unsupported application protocol |
| peer closes after TLS | application | HTTP or protocol failure |

Tests should induce each failure without using public services. Local certificates and ephemeral listeners make the results deterministic and keep secrets intentionally non-production.

## Ready to continue

You are ready for HTTP/2 when you can state exactly what a successful TLS handshake proves and can deliberately fail each omitted property.

## Primary Node.js references

- [TLS](https://nodejs.org/docs/latest-v24.x/api/tls.html)
- [HTTPS](https://nodejs.org/docs/latest-v24.x/api/https.html)
- [Crypto](https://nodejs.org/docs/latest-v24.x/api/crypto.html)

## Continue

- [Workbook](workbook.md)
- [Reasoned solutions](solutions.md)
- [Laboratory brief](../../labs/module-57-local-tls-identity-lab/README.md)
- [ServiceWire engineering guide](../capstone.md)
