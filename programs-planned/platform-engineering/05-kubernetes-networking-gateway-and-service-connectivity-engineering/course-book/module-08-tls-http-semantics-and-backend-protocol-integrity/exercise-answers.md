# Worked answers — TLS, HTTP semantics, and backend protocol integrity

A complete answer identifies both client-to-Gateway and Gateway-to-backend connections. “TLS enabled” is not a sufficient trust description.

## 1. What does TLS termination at the Gateway make the Gateway responsible for?

The Gateway owns private-key access, certificate selection, SNI handling, chain presentation, supported TLS versions/ciphers, client-facing ALPN, HTTP authority handling, and creation of the separate backend connection. It also becomes the trusted source of forwarding metadata and may see plaintext application data. The release must prove correct hostname validation, wrong-host rejection, rotation, secret access, and backend protocol policy. Termination secures the frontend hop; it does not automatically secure or authenticate the backend hop.

## 2. Why is backend TLS incomplete without hostname/SAN verification?

Trusting a CA and encrypting the connection proves only that the peer presents some certificate under that trust hierarchy. Without checking the expected backend name against SANs, the Gateway may connect securely to the wrong service or a compromised certificate holder. The policy must bind the Service/port to an expected identity and trust anchor. The negative test is a valid certificate from the trusted CA for another name; the Gateway should reject it.

## 3. What does SNI influence?

SNI is sent in the ClientHello and commonly selects the listener’s certificate and virtual-server configuration before HTTP is available. It can influence routing in TLS passthrough designs. SNI does not itself prove the certificate is trusted, the hostname matches the SAN, or the later HTTP authority agrees. Test SNI/certificate selection, hostname verification, and Host/`:authority` mismatch separately. A shared Gateway may correctly reject a request with valid TLS but an unexpected HTTP authority.

## 4. Why should a Gateway replace incoming X-Forwarded-For?

An Internet client can supply any forwarding header. If the Gateway appends or trusts it, the application can be tricked into accepting an attacker-chosen client address. At the first trusted proxy boundary, discard or replace untrusted values with the transport peer the Gateway actually observed, then define how later trusted proxies append. The application must trust forwarded metadata only from approved immediate peers. A negative test sends a spoofed value and verifies that the backend receives the Gateway-generated value instead.

## 5. How can retries multiply work?

Several layers may retry independently: client, SDK, Gateway, mesh, application, and downstream service. Three attempts at each layer can turn one logical request into many backend effects, especially during failure. Retries also consume the same capacity needed for recovery. Assign one primary retry owner where possible, cap attempts with a shared deadline, expose attempt counts, and distinguish logical operations from transport attempts. Test commit-with-lost-response, timeout, and overload conditions.

## 6. When is retrying POST potentially safe?

Only when the operation has an end-to-end idempotency contract, the same idempotency key and request fingerprint are preserved, the body is replayable, the failure is retryable, and the remaining deadline permits another attempt. The authoritative service must store the logical outcome transactionally so a repeated request returns the same result rather than creating a second effect. A proxy cannot create safety merely by configuring `retries: 2`. Prove the lost-response-after-commit case and changed-input conflict.

## 7. What trade does response buffering create?

Buffering can isolate slow clients, support retries or transformations, and prevent backend connections from remaining open. It consumes memory/disk, delays streaming, adds latency, and can create large failure amplification under concurrent bodies. Disabling buffering preserves streaming but transfers backpressure and connection lifetime to the backend. Define maximum buffered bytes, spill policy, idle/total timeouts, cancellation cleanup, and behavior for slow readers. Measure memory and disk under the largest permitted response.

## 8. Why can a certificate rotate successfully in Kubernetes but remain stale in the proxy?

Updating the Secret or certificate resource changes desired state. The controller must observe the new version, deliver it to the data plane, and the listener must load it. A stale proxy process, failed watch, rejected configuration, or long-lived process state can keep serving the old certificate. Verify from an independent client by fingerprint/serial and correlate resource version, controller condition, load time, and listener response. Rotation evidence must include both overlap and eventual removal of the old key.

## 9. What is the difference between passthrough and re-encryption?

Passthrough forwards the client’s encrypted TLS stream to the backend; the Gateway does not terminate or inspect HTTP and routing is limited to pre-decryption information such as SNI. Re-encryption terminates client TLS at the Gateway and opens a second TLS connection to the backend, allowing L7 routing while protecting the backend hop. Re-encryption requires independent backend identity verification and two certificate lifecycles. Neither model is automatically superior; choose based on trust and routing requirements.

## 10. Why is an open TCP port not gRPC proof?

It proves only that a TCP connection was accepted. gRPC normally requires HTTP/2 framing, appropriate content type, method path, metadata, status trailers, and deadline/cancellation behavior; TLS deployments also need ALPN negotiation. A port can accept HTTP/1.1, plaintext, or an unrelated protocol. Use a protocol-aware client and verify HTTP/2 negotiation, a real RPC, error mapping, streaming where relevant, and behavior through the Gateway.

## 11. What does a 421 response communicate?

`421 Misdirected Request` indicates that the server or proxy is not willing or able to produce a response for the request’s authority on the current connection. At a shared Gateway, it can explicitly reject a Host/`:authority` that does not belong to the listener or routing context even when TLS to the socket succeeded. This prevents a valid connection to one name from being reused or abused for another authority. Test correct SNI with wrong HTTP authority as a separate negative case.

## 12. How should timeout values be related?

Begin with one end-to-end client or operation deadline, then allocate smaller child budgets for DNS, connect, TLS, request upload, backend attempt, response headers, streaming idle, and retry backoff. Downstream timeouts should not exceed the remaining upstream budget, and retry attempts must fit inside it. Include cancellation propagation and reserve time for returning an error. Test a slow backend and prove no layer continues uncontrolled work after the logical deadline.
