# Reference Answers — Module 06: Outbound HTTP, SSRF, and Webhook Integrity

Read after attempting all twelve Outbound HTTP, SSRF, and Webhook Integrity exercises. Compare the owner, invariant, counterexample, and oracle rather than copying wording.

## 1. Why is `https://` alone insufficient SSRF defense?

**Answer.** TLS protects the connection to the selected peer; it does not make a private or metadata destination safe.

**Capstone check.** Run the HTTPS/private-address cases in `capstone/shared/vectors/ssrf.json`; a TLS URL resolving to a forbidden peer must still fail.

## 2. Why reject mixed public and private DNS answers?

**Answer.** Selection may differ across retries or layers, enabling a hostname to pass validation yet connect to a forbidden peer.

**Capstone check.** Use the mixed-answer DNS case in `capstone/shared/vectors/ssrf.json`; one forbidden answer rejects the destination rather than relying on resolver order.

## 3. What does peer verification prove?

**Answer.** That the connected socket address remains one of the addresses approved for this request; it narrows DNS rebinding and resolver divergence.

**Capstone check.** Exercise the approved-address/connected-peer mismatch vector and retain the peer comparison as the delivery oracle.

## 4. How should redirects be handled?

**Answer.** Disable by default or follow a small bounded count while fully revalidating each target and stripping sensitive headers across origins.

**Capstone check.** Run a redirect chain that crosses into a forbidden destination; each hop must be re-parsed, re-resolved, and re-authorized.

## 5. Why sign exact bytes?

**Answer.** Any parse/reserialize step can change order, whitespace, numbers, or Unicode; authentication must cover what crossed the wire.

**Capstone check.** Change one byte of the serialized webhook body in `capstone/shared/vectors/webhook.json`; signature verification must fail before JSON interpretation.

## 6. What belongs in webhook signed metadata?

**Answer.** A version, timestamp, durable delivery identifier, key identifier, and body digest or exact body according to the profile.

**Capstone check.** Verify the course webhook profile binds version, timestamp, delivery ID, key ID, and exact body bytes in one deterministic vector.

## 7. Why use both freshness and replay state?

**Answer.** Freshness bounds time but permits repeated use within the window; replay state enforces one accepted delivery ID.

**Capstone check.** Replay the same delivery ID inside the freshness window; timestamp validation passes but durable replay state must reject the second effect.

## 8. What if the receiver commits business state and crashes before replay state?

**Answer.** They must be one transaction or the business operation must be idempotent with the same delivery ID; otherwise retry can duplicate effects.

**Capstone check.** Use one transaction or an idempotent business key tied to delivery ID; the receiver test must survive a crash between effect and acknowledgment.

## 9. Why revalidate at delivery instead of registration only?

**Answer.** DNS, redirects, ownership, and policy can change between registration and later delivery.

**Capstone check.** Change DNS or destination policy after registration and before dispatch; the delivery-time SSRF check must reject the now-forbidden peer.

## 10. What does egress firewalling add?

**Answer.** A deployment-level backstop that can block destinations even if application policy contains a defect.

**Capstone check.** Record egress filtering as a deployment backstop in the checkpoint; application vectors still must pass because network policy is not a substitute for URL validation.

## 11. Trace SSRF-safe delivery and webhook integrity in the primary implementation

The relevant entry points are `capstone/tracks/python-fastapi/src/api_security/ssrf.py` and `capstone/tracks/typescript-fastify/src/security/ssrf.ts`. The required invariant is that the service validates URL policy, every resolved address, connected peer, redirects, exact signed bytes, freshness, and replay identity.

## 12. Compare SSRF-safe delivery and webhook integrity across Python and TypeScript

Both tracks must preserve this invariant: the service validates URL policy, every resolved address, connected peer, redirects, exact signed bytes, freshness, and replay identity. The intentional difference is that resolver/client APIs differ; no implementation may re-resolve outside the validated connection path.
