# Lab — Module 06: Outbound HTTP, SSRF, and Webhook Integrity

## Objective

Evaluate the shared destination matrix, run controlled redirect and peer-change simulations, sign and verify exact webhook bytes, and prove replay rejection. Plant a hostname-suffix-only policy and a parse/reserialize signature implementation, capture both bypasses, then repair.


## Setup conditions

The previous baseline is: **A shared hostile-input corpus exercises both language tracks and the artifact-storage boundary.** Run its checkpoint before changing code. Record the exact baseline command and predict how the planted defect will violate this module question: *How does the service call a user-chosen destination without becoming a network pivot or accepting forged delivery?*

## Failure action and investigation

1. Implement and test: Reject forbidden schemes, ports, credentials, fragments, and address ranges.
2. Implement and test: Evaluate every resolved address and the connected peer.
3. Implement and test: Revalidate redirects and DNS changes.
4. Implement and test: Sign exact webhook bytes with key identity and timestamp.
5. Implement and test: Reject stale and replayed deliveries.

### Required planted defect

Remove or bypass the central control for **Outbound HTTP, SSRF, and Webhook Integrity** in a temporary branch. Predict the first failing check before running it, then retain the minimized reproducer as a regression after repair.

## Operational oracle

The system satisfies the chapter’s central question: How does the service call a user-chosen destination without becoming a network pivot or accepting forged delivery? The result must be visible through public behavior or durable state, not inferred only from logs.

## Required evidence

- baseline transcript proving the previous checkpoint before **Outbound HTTP, SSRF, and Webhook Integrity** changes
- source, fixture, contract, migration, or configuration diff for this module
- focused result for: Reject forbidden schemes, ports, credentials, fragments, and address ranges.
- public, durable, security, or operational observation showing: Webhook registration and delivery resist SSRF, body alteration, stale messages, and duplicate replay.
- minimized planted-defect failure and repaired regression
- primary/comparison-track note for **SSRF-safe delivery and webhook integrity**
- a limitation statement naming every live database, network, process, telemetry backend, or operated exercise not run

## Cleanup and reset

1. Restore the control changed for **Outbound HTTP, SSRF, and Webhook Integrity**.
2. Remove synthetic data, faults, credentials, permits, files, or delivery state created by this lab.
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
