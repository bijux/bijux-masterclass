# Module 57 Solutions — TLS Identity and HTTPS

## Prediction reasoning

A trusted chain with hostname mismatch is not acceptable for the requested logical identity. When connecting to an IP for `https://localhost`, use `localhost` as `servername`. Required `h2` not being negotiated makes the channel unsuitable for that product contract. A trusted server identity is not application authorization. Before HTTP exists, the server generally cannot send an HTTP problem response.

## Repair reasoning

Create test credentials with a dedicated CA. Configure the client `ca` option and expected `servername`. A failing identity test should fail visibly.

ALPN validation occurs after secure connection establishment. Destroy the socket if the selected protocol violates policy.

Private keys should be read into tightly scoped configuration and never interpolated into errors. Startup validates all TLS inputs before publishing any listener. If later startup fails, close already-started resources in reverse order.

The operation deadline begins before TCP/TLS establishment. Cancellation destroys the connecting TLS socket and removes listeners.

TLS identity can feed an authorization mapping, but the mapping is a separate application decision.

## Construction notes

Local tests need a certificate SAN that matches names used by clients. Modern hostname verification relies on SAN rather than a common-name-only certificate.

The echo server should cap bytes and close orderly. Tests should observe both secure connection and final close. Do not assert exact OpenSSL error prose; classify by stable local context or error code where available.

Peer certificate inspection can report subject alternative names or fingerprint under bounded formatting, but avoid dumping full certificate objects into routine logs.

## Laboratory evidence

Strong evidence includes:

- trusted localhost success;
- trusted IP success when SAN permits it;
- wrong `servername` failure;
- missing CA failure;
- required ALPN success;
- ALPN mismatch failure;
- handshake deadline;
- client cancellation;
- server shutdown with one connected TLS socket;
- no key bytes in errors.

## ServiceWire transfer

HTTPS wraps the existing application handler. HTTP and HTTPS endpoints can be started independently. The runtime reports bound endpoints only after both configured listeners succeed; otherwise it rolls back.

## Independent transfer

Mutual TLS verifies client chain and identity. Map a stable certificate identity to an administrative role under explicit policy. Handle expiration and rotation. Audit the mapped identity and certificate fingerprint, not private material. Authorization can still deny a successfully authenticated client.

## Defense summary

TLS creates a protected authenticated channel only under explicit trust and identity configuration. Every application contract survives above it. The strongest test is not “the request works” but a matrix that proves the intended failures remain failures.

## TLS proof solution

The trusted-localhost test dials the listener address while verifying `localhost` against the course CA. The wrong-host test uses the same network path and trust anchor but changes only expected identity. The untrusted-CA test keeps the name correct and removes trust. ALPN mismatch keeps certificate verification valid but requires a protocol the server does not offer. Each test isolates one omitted property.

A rotation design reads candidate files into bounded secret-bearing buffers, constructs and validates a secure context, then makes that context available for new handshakes. Existing connections keep their negotiated session. If staging fails, the previous context remains authoritative. The course fixture proves local trust, name, and ALPN behavior; it does not implement production secret storage, automated rotation, revocation policy, or certificate monitoring.

## Secret-handling solution

The loading interface returns opaque credential buffers to the server constructor and never implements custom inspection that reveals contents. Errors name the credential role and source path only when path disclosure is acceptable. Tests assert successful use or fingerprints, not snapshots of private bytes. Private keys are omitted from archives intended for general use unless they are explicitly disposable local teaching fixtures, as in this course; even then they are labeled non-production and never logged.
