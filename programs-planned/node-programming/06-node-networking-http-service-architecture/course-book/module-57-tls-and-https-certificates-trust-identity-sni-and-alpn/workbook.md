# Module 57 Workbook — TLS Identity and HTTPS

## 1. Predict

1. The chain validates, but hostname verification fails. Is the peer acceptable?
2. A client connects to an IP while the logical URL uses a hostname. Which value belongs in `servername`?
3. TLS succeeds with no ALPN protocol, but the product requires `h2`. Is the connection usable?
4. A trusted local CA signs a server certificate. Does that authorize the server to submit jobs?
5. An HTTPS handshake fails before HTTP headers. Can the server return a problem JSON body?

## 2. Diagnose and repair

- Replace `rejectUnauthorized: false` with a local trust anchor.
- Preserve hostname verification while dialing a deterministic IP.
- Add required ALPN validation.
- Prevent private-key material from entering diagnostics.
- Include handshake time in one deadline.
- Roll back startup when certificate loading fails.
- Separate TLS identity from application authorization.

## 3. Focused construction

1. Generate or load a dedicated local CA and server certificate.
2. Start a TLS echo server.
3. Connect with trusted CA and expected hostname.
4. Test wrong hostname.
5. Test untrusted issuer.
6. Negotiate `http/1.1`.
7. Require a missing protocol and fail.
8. Close server and sockets completely.
9. Inspect bounded peer certificate metadata.
10. Document fixture limitations.

## 4. Independent laboratory

Build the [Local TLS Identity Lab](../../labs/module-57-local-tls-identity-lab/README.md).

## 5. ServiceWire transfer

Add HTTPS and trusted client configuration. Reuse the same route/application boundary. Expose negotiated protocol only in bounded diagnostics.

## 6. Independent transfer

Design mutual TLS for an internal administrative endpoint. Separate certificate trust, identity mapping, role authorization, rotation, and audit evidence.

## 7. Closed-book defense

1. What are the distinct TLS assurance layers?
2. What does SNI do?
3. What does ALPN do?
4. Why is a local CA better than disabling verification?
5. Which HTTP/application checks remain after TLS succeeds?

## 8. TLS proof table

For each test—trusted localhost, wrong hostname, untrusted CA, expired certificate, and ALPN mismatch—record:

- network destination;
- expected server name;
- trust anchors;
- expected handshake phase;
- observed error class;
- cleanup evidence.

The table should make it impossible to “fix” a failed test by setting `rejectUnauthorized: false`.

## 9. Rotation design

Describe how a long-running service could stage new credentials. Separate file read, secure-context construction, readiness of new handshakes, existing connections, rollback, and secret disposal. State which parts are implemented by the course fixture and which remain operational policy.

## 10. Secret-handling review

List every place key or certificate bytes could accidentally appear: thrown errors, debug inspection, structured logs, test snapshots, process arguments, environment variables, generated archives, and crash dumps. Define a safe loading interface and a rendering policy. Explain why certificates may be public while private keys still require non-rendering and lifecycle discipline.
