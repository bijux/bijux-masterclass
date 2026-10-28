# Lab — Module 06: Outbound HTTP, SSRF, and Webhook Integrity

> **Module 06:** Outbound HTTP, SSRF, and Webhook Integrity

## Objective

Evaluate the shared destination matrix, run controlled redirect and peer-change simulations, sign and verify exact webhook bytes, and prove replay rejection. Plant a hostname-suffix-only policy and a parse/reserialize signature implementation, capture both bypasses, then repair.

## Why this lab matters

This lab turns the module’s governing question—**How can outbound HTTP and webhook delivery avoid SSRF, rebinding, redirect abuse, tampering, and replay?**—into a falsifiable experiment. Evaluate the shared destination matrix, run controlled redirect and peer-change simulations, sign and verify exact webhook bytes, and prove replay rejection. Plant a hostname-suffix-only policy and a parse/reserialize signature implementation, capture both bypasses, then repair.

It advances the cumulative Analysis Runs Platform by requiring this result: **Implement destination policy, address classification, peer verification, exact-byte signatures, freshness, rotation, and replay defense**. The result is acceptable only if the inherited contract, security, durability, reliability, and performance guarantees remain intact.

## Setup conditions

The previous baseline is: **A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does the service call a user-chosen destination without becoming a network pivot or accepting forged delivery?*

## Hypothesis

The clean implementation should satisfy this claim: **parsed destination policy; all-address classification; mixed-answer rejection; connect-time peer model; redirect revalidation; exact-byte signatures; freshness and durable replay; receiver idempotency.** When the lab introduces this fault—**Remove or bypass the central control for Outbound HTTP, SSRF, and Webhook Integrity in a temporary branch**—at least one part of that oracle must fail before a downstream layer can report success. After repair, the same action sequence must restore the oracle without suppressing the fault, deleting evidence, or weakening an inherited guarantee.

## Controlled action and investigation

1. Implement and test: Reject forbidden schemes, ports, credentials, fragments, and address ranges.
2. Implement and test: Evaluate every resolved address and the connected peer.
3. Implement and test: Revalidate redirects and DNS changes.
4. Implement and test: Sign exact webhook bytes with key identity and timestamp.
5. Implement and test: Reject stale and replayed deliveries.

### Required planted defect

Remove or bypass the central control for **Outbound HTTP, SSRF, and Webhook Integrity** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

### Investigation notes

Before editing code, predict the first observable divergence caused by **Remove or bypass the central control for Outbound HTTP, SSRF, and Webhook Integrity in a temporary branch**. Record a timeline with five columns: action, authoritative state, external outcome, diagnostic evidence, and interpretation. After repair, explain which boundary owns the mechanism needed to achieve **Evaluate the shared destination matrix, run controlled redirect and peer-change simulations, sign and verify exact webhook bytes, and prove replay rejection. Plant a hostname-suffix-only policy and a parse/reserialize signature implementation, capture both bypasses, then repair**, and identify one attractive implementation that would pass the happy path while failing the oracle.

## Operational oracle

- parsed destination policy
- all-address classification
- mixed-answer rejection
- connect-time peer model
- redirect revalidation
- exact-byte signatures
- freshness and durable replay
- receiver idempotency

## Required evidence

- baseline transcript proving the previous checkpoint before **Outbound HTTP, SSRF, and Webhook Integrity** changes
- the exact source, fixture, contract, migration, or configuration diff that implements **Outbound HTTP, SSRF, and Webhook Integrity**
- focused result for: Reject forbidden schemes, ports, credentials, fragments, and address ranges.
- public, durable, security, or operational observation showing: Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **SSRF-safe delivery and webhook integrity**
- a limitation statement naming every live dependency required to support the strongest **Outbound HTTP, SSRF, and Webhook Integrity** claim but not exercised

## Interpretation and defense

1. Which state or effect is authoritative for **Outbound HTTP, SSRF, and Webhook Integrity**, and which observations are merely diagnostic?
2. Which retained artifact proves the causal link between **Remove or bypass the central control for Outbound HTTP, SSRF, and Webhook Integrity in a temporary branch** and the first violated part of the oracle?
3. What plausible shortcut would satisfy the clean path but fail under the controlled action?
4. How may the Python and TypeScript implementations differ internally while preserving the same external and durable result?
5. Which inherited guarantee would be lost if the mechanism were moved to a boundary that does not own the required state?

## Cleanup and reset

1. Restore the control changed for **Outbound HTTP, SSRF, and Webhook Integrity**.
2. Remove the temporary data, faults, credentials, permits, files, or delivery state created by the **Outbound HTTP, SSRF, and Webhook Integrity** experiment.
3. Rerun the focused regression and `make module-proof MODULE=06`.
4. Confirm the system again provides this result: Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.

## Completion gate

- parsed destination policy
- all-address classification
- mixed-answer rejection
- connect-time peer model
- redirect revalidation
- exact-byte signatures
- freshness and durable replay
- receiver idempotency

Retain the pre-repair failure, post-repair success, causal timeline, and cleanup evidence for **Outbound HTTP, SSRF, and Webhook Integrity**. A green command without the negative case and causal explanation does not satisfy this gate.
