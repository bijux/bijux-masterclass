# Checkpoint — Module 06: Outbound HTTP, SSRF, and Webhook Integrity

## Required result

Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.

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

## Defend the design

1. Answer the central question: **How does the service call a user-chosen destination without becoming a network pivot or accepting forged delivery?**
2. Demonstrate this capstone result: Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.
3. Show the planted defect, the first failing oracle, and the retained regression.
4. Explain why this invariant is shared across languages: the service validates URL policy, every resolved address, connected peer, redirects, exact signed bytes, freshness, and replay identity.
5. State exactly which database, network, process, telemetry backend, or operated exercise was not run in the current environment.

## Continue only when

Continue when the system again provides this module result—Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.—all focused checks pass, the **Outbound HTTP, SSRF, and Webhook Integrity** planted defect has failed for the predicted reason, and the record identifies every live claim not executed in the current environment.
