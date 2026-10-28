# Checkpoint — Module 06: Outbound HTTP, SSRF, and Webhook Integrity

## Required result

Implement destination policy, address classification, peer verification, exact-byte signatures, freshness, rotation, and replay defense.

## Demonstrate

- Reject forbidden schemes, ports, credentials, fragments, and address ranges.
- Evaluate every resolved address and the connected peer.
- Revalidate redirects and DNS changes.
- Sign exact webhook bytes with key identity and timestamp.
- Reject stale and replayed deliveries.

## Commands

```bash
make module-proof MODULE=06 TRACK=python
make module-proof MODULE=06 TRACK=typescript
make core-proof
```

## Evidence to retain

- baseline transcript proving the previous checkpoint before **Outbound HTTP, SSRF, and Webhook Integrity** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Outbound HTTP, SSRF, and Webhook Integrity**
- focused result for: Reject forbidden schemes, ports, credentials, fragments, and address ranges.
- public, durable, security, or operational observation showing: Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **SSRF-safe delivery and webhook integrity**
- a limitation statement naming every live dependency required to support the strongest **Outbound HTTP, SSRF, and Webhook Integrity** claim but not exercised

## Defend the design

1. Answer the central question: **How does the service call a user-chosen destination without becoming a network pivot or accepting forged delivery?**
2. Demonstrate this capstone result: Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.
3. Show the **Outbound HTTP, SSRF, and Webhook Integrity** defect, the first failing oracle, and the exact regression retained after repair.
4. Explain why this invariant is shared across languages: the service validates URL policy, every resolved address, connected peer, redirects, exact signed bytes, freshness, and replay identity.
5. State which environment-backed **Outbound HTTP, SSRF, and Webhook Integrity** route was not run and how that limits the claim.

## Continue only when

Continue when the system again provides this module result—Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.—all focused checks pass, the **Outbound HTTP, SSRF, and Webhook Integrity** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
