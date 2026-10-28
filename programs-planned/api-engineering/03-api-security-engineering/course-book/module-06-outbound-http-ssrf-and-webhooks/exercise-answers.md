# Worked Answers — Module 06: Outbound HTTP, SSRF, and Webhook Integrity

Use these solutions to audit your reasoning for **Outbound HTTP, SSRF, and Webhook Integrity**. Each answer identifies the decisive rule and the evidence boundary; compare that reasoning with your own counterexample rather than memorizing the wording.

## 1. Why is `https://` alone insufficient SSRF defense?

TLS protects the connection to the selected peer; it does not make a private or metadata destination safe.

**Capstone check.** Run the HTTPS/private-address cases in `capstone/shared/vectors/ssrf.json`; a TLS URL resolving to a forbidden peer must still fail.

The chapter’s decisive distinction is this: Redirects restart the policy. Do not automatically follow a 302 from a public host to a private address. Parse, resolve, validate, connect, and count each hop under a small maximum. Revalidate on every retry because DNS and configuration may change after registration.

## 2. Why reject mixed public and private DNS answers?

Selection may differ across retries or layers, enabling a hostname to pass validation yet connect to a forbidden peer.

**Capstone check.** Use the mixed-answer DNS case in `capstone/shared/vectors/ssrf.json`; one forbidden answer rejects the destination rather than relying on resolver order.

In the cumulative capstone, the rule becomes concrete: Resolve the hostname and inspect every answer. Reject loopback, unspecified, private, link-local, multicast, documentation, carrier-grade NAT, metadata-service, and organization-reserved ranges according to the deployment policy. Handle IPv4-mapped IPv6 and alternative textual forms. A mixed public/private answer is rejected rather than selecting the convenient public address.

## 3. What does peer verification prove?

That the connected socket address remains one of the addresses approved for this request; it narrows DNS rebinding and resolver divergence.

**Capstone check.** Exercise the approved-address/connected-peer mismatch vector and retain the peer comparison as the delivery oracle.

A useful way to reason about the boundary is: Model URL evaluation as a pure DestinationPolicy over parsed URL and injected resolver results. The real transport receives the validated address set and must expose the connected peer for verification. Use HMAC-SHA256 over a versioned signing string containing timestamp, delivery ID, key ID, and SHA-256 of exact body bytes; compare with hmac.compare digest.

## 4. How should redirects be handled?

Disable by default or follow a small bounded count while fully revalidating each target and stripping sensitive headers across origins.

**Capstone check.** Run a redirect chain that crosses into a forbidden destination; each hop must be re-parsed, re-resolved, and re-authorized.

The implementation consequence is: Evaluate the shared destination matrix, run controlled redirect and peer-change simulations, sign and verify exact webhook bytes, and prove replay rejection. Plant a hostname-suffix-only policy and a parse/reserialize signature implementation, capture both bypasses, then repair.

## 5. Why sign exact bytes?

Any parse/reserialize step can change order, whitespace, numbers, or Unicode; authentication must cover what crossed the wire.

**Capstone check.** Change one byte of the serialized webhook body in `capstone/shared/vectors/webhook.json`; signature verification must fail before JSON interpretation.

The important nuance is: Do not parse and reserialize JSON before verification. Property order, whitespace, Unicode escapes, and numeric representations can change while the data appears equivalent. The signature covers transport bytes. If a standard HTTP message-signature profile is adopted later, its covered components and canonicalization rules must replace—not be mixed with—the course-specific profile.

## 6. What belongs in webhook signed metadata?

A version, timestamp, durable delivery identifier, key identifier, and body digest or exact body according to the profile.

**Capstone check.** Verify the course webhook profile binds version, timestamp, delivery ID, key ID, and exact body bytes in one deterministic vector.

Under concurrency or failure, the distinction becomes: Webhook integrity protects the receiver from forged or replayed delivery, not from a malicious destination. Sign the exact bytes transmitted, plus a stable delivery identifier, timestamp, and key identifier under an explicit course profile. The receiver verifies with constant-time comparison, enforces freshness, stores the delivery ID durably before applying the effect, and returns the same logical result for a duplicate.

## 7. Why use both freshness and replay state?

Freshness bounds time but permits repeated use within the window; replay state enforces one accepted delivery ID.

**Capstone check.** Replay the same delivery ID inside the freshness window; timestamp validation passes but durable replay state must reject the second effect.

The design remains honest only if: Rotation again requires overlap. The sender signs with the active key; the receiver can verify the active and retiring keys for a bounded window identified by key ID. Retiring a key before all in-flight retries expire creates an avoidable outage. Keeping every historical key forever expands compromise impact.

## 8. What if the receiver commits business state and crashes before replay state?

They must be one transaction or the business operation must be idempotent with the same delivery ID; otherwise retry can duplicate effects.

**Capstone check.** Use one transaction or an idempotent business key tied to delivery ID; the receiver test must survive a crash between effect and acknowledgment.

The consumer-facing consequence is: Start with a strict URL policy: allowed scheme, explicit or default port, no user information, no fragment, normalized host syntax, and a bounded path/query length. A host allowlist may be appropriate for a training topology, but suffix matching alone is insufficient: trusted.example.attacker.test and Unicode lookalikes demonstrate why parse results, not text fragments, matter.

## 9. Why revalidate at delivery instead of registration only?

DNS, redirects, ownership, and policy can change between registration and later delivery.

**Capstone check.** Change DNS or destination policy after registration and before dispatch; the delivery-time SSRF check must reject the now-forbidden peer.

The operational consequence is: A webhook URL is not harmless configuration. It asks the service to resolve a name, connect from a privileged network location, follow protocol behavior, and transmit signed data. The security decision spans registration and every delivery attempt.

## 10. What does egress firewalling add?

A deployment-level backstop that can block destinations even if application policy contains a defect.

**Capstone check.** Record egress filtering as a deployment backstop in the checkpoint; application vectors still must pass because network policy is not a substitute for URL validation.

The strongest engineering interpretation is: DNS rebinding exists when policy checks one resolution and the HTTP client performs another. The connection path must use the validated address set while preserving the intended TLS server name and Host authority, then verify the connected peer belongs to that set. If the client library cannot provide that guarantee, the honest production control belongs in a constrained egress proxy or network policy; application validation alone should not be described as complete.

## 11. Trace SSRF-safe delivery and webhook integrity in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/ssrf.py` and `capstone/tracks/typescript-fastify/src/security/ssrf.ts`. The required invariant is that the service validates URL policy, every resolved address, connected peer, redirects, exact signed bytes, freshness, and replay identity.

The defect-oriented view is: Webhook integrity protects the receiver from forged or replayed delivery, not from a malicious destination. Sign the exact bytes transmitted, plus a stable delivery identifier, timestamp, and key identifier under an explicit course profile. The receiver verifies with constant-time comparison, enforces freshness, stores the delivery ID durably before applying the effect, and returns the same logical result for a duplicate.

## 12. Compare SSRF-safe delivery and webhook integrity across Python and TypeScript

Both tracks must preserve this invariant: the service validates URL policy, every resolved address, connected peer, redirects, exact signed bytes, freshness, and replay identity. The intentional difference is that resolver/client APIs differ; no implementation may re-resolve outside the validated connection path.

Across the Python and TypeScript tracks, the invariant is: DNS rebinding exists when policy checks one resolution and the HTTP client performs another. The connection path must use the validated address set while preserving the intended TLS server name and Host authority, then verify the connected peer belongs to that set. If the client library cannot provide that guarantee, the honest production control belongs in a constrained egress proxy or network policy; application validation alone should not be described as complete.
