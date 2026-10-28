# Exercises — State and Recovery

## 1. Backend bootstrap

Why can OpenTofu not create the remote backend it is already configured to use?

## 2. State-only information

What information does state hold that configuration usually cannot reconstruct safely?

## 3. Force-unlock evidence

A lock is 40 minutes old. What evidence is required before force-unlock?

## 4. Unsafe rollback

Explain why S3 versioning does not make arbitrary state rollback safe.

## 5. Encryption layers

Compare S3 KMS encryption with OpenTofu native state encryption.

## 6. Sensitive output

Why can a `sensitive` output still be dangerous in state?

## 7. State boundary

Give a reason to split state and a reason not to split it further.

## 8. Workspace limits

Why are workspaces insufficient as the only production/dev isolation control?

## 9. Remote-state access

What security concern exists with `terraform_remote_state`?

## 10. Orphan after partial apply

An EC2 instance exists after a failed apply but is absent from state. What are the safe options?

## 11. Lineage and serial

How do lineage and serial differ?

## 12. Recovery rehearsal

Design a state recovery rehearsal that cannot overwrite the authoritative state.
