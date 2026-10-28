# Laboratory 7 — Local TLS Identity Lab

**Module 57**

## Product

Build a local TLS echo endpoint using a dedicated course CA and server certificate. The client connects to a deterministic local address while verifying the logical name. It can require ALPN and reports bounded peer identity evidence.

## Governing question

> How can tests prove chain trust, hostname identity, SNI, ALPN, deadlines, and lifecycle without bypassing certificate verification?

## Public surface

- `startTlsEchoServer(fixtures, options)` returns bound endpoint and close handle.
- `connectTls(options)` verifies CA, server name, and ALPN.
- Fixture loader never logs private-key bytes.
- Tests exercise both required success and required failure.

## Required invariants

- No test uses `rejectUnauthorized: false`.
- Wrong hostname remains a failure.
- Untrusted issuer remains a failure.
- Required ALPN mismatch closes the socket.
- Handshake shares one operation deadline.
- Server and connected sockets close completely.

The laboratory is complete only when the tests distinguish these invariants from a smaller implementation that happens to pass the normal path.

## Implementation sequence

1. Load CA, key, and certificate.
2. Start bounded echo server.
3. Connect using CA and `servername`.
4. Add wrong-name and untrusted tests.
5. Add ALPN negotiation and mismatch.
6. Add deadline/cancellation.
7. Add socket registry and shutdown.

Keep the sequence causal. A later feature should not hide an earlier failure. For example, do not add retry before a single attempt has one clear terminal owner, and do not add shutdown before the normal resource lifecycle is observable.

## Adversarial cases

- wrong hostname
- missing CA
- certificate not valid for IP
- unsupported ALPN
- client cancellation during handshake
- oversized echo payload
- server close with active socket
- key loading failure

For each case, write the predicted state transition and the exact terminal evidence before running the test. Prefer injected clocks, deterministic fake peers, explicit counters, and local ephemeral ports to arbitrary sleeps.

## Prohibited shortcuts

- disabling verification
- trusting every self-signed certificate globally
- using selected IP as identity unintentionally
- logging key buffers
- starting listener before credentials validate

A shortcut is prohibited because it removes the mechanism under study. It is not a style preference.

## Completion evidence

1. success matrix
2. failure matrix
3. negotiated protocol assertion
4. no private bytes in diagnostics
5. active-socket cleanup

Also include a small ownership table naming every socket, timer, listener, queue, request, response, or subscription created by the product and its cleanup transition.

## Independent transfer

Design mutual TLS for an internal administration route, including certificate-to-role mapping and rotation assumptions.

The transfer is not complete when only type names change. Reconstruct the protocol, state, capacity, time, and terminal ledgers for the new domain.

## Using the starter

The starter compiles and exposes the domain vocabulary, configuration validation, and one baseline test. It does not implement the difficult mechanism. Extend it without weakening strict TypeScript settings.

Run:

```bash
npm run typecheck
npm test
```

## Comparing with the reference

Open `reference/` only after your normal and adversarial tests pass. Compare:

1. state representation;
2. bound enforcement point;
3. cleanup ownership;
4. failure classification;
5. test evidence.

Adopt a reference difference only when it proves an invariant your design misses or makes the same contract materially easier to inspect.
