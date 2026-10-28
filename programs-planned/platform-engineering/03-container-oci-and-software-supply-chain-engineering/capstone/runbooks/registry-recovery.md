# Runbook — registry integrity or availability failure

## Trigger

Use when the registry is unavailable, returns digest-mismatched bytes, loses manifests/blobs/referrers, shows unauthorized tag mutation, or cannot satisfy retention/rollback obligations.

## Triage

Separate availability from integrity. For availability, determine which approved subjects are already present in runtime/node caches and which new deployments are blocked. For integrity, stop pulls/promotions immediately and compare registry responses with release records and independent retained digests.

Preserve registry audit/auth logs, storage/object versions, replication state, tag history, garbage-collection records, and client pull errors. Do not rebuild images merely to restore availability; rebuilding creates new subjects.

## Recovery paths

- Restore missing immutable objects from a verified mirror/backup and recheck every descriptor edge.
- Recreate mutable tags from release records only after immutable graph verification.
- Restore/refill subject-bound evidence and verify its subjects/signatures.
- Use an approved mirror by digest when policy explicitly supports it.
- Re-authorize promotion only after authentication, retention, replication, and recovery controls are healthy.

## Closure

Demonstrate pull-by-digest for active and rollback subjects, referrer discovery, tag audit, authentication/authorization, retention/GC safety, and recovery from a clean client. Record RPO/RTO and any evidence that remains environment-specific.
