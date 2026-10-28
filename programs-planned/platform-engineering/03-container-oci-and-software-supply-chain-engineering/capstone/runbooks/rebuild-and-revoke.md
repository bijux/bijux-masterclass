# Runbook — rebuild and revoke a compromised image subject

## Trigger

Use this runbook when an image subject contains prohibited content, comes from an unauthorized source/builder, has a critical exploitable defect, or can no longer be trusted independently of its signing key.

## Immediate containment

1. Freeze promotion and new deployment of the digest and every tag currently resolving to it.
2. Preserve release, registry, build, provenance, signature, deployment, and runtime evidence.
3. Enumerate active environments, nodes, mirrors, caches, and consumers using the subject.
4. Decide whether running workloads require immediate termination or controlled replacement based on exploitability and service risk.
5. Do not delete the only evidence before the subject and exposure set are recorded.

## Recovery

Repair the earliest faulty input or authority boundary. Build a **new subject** under controlled inputs; never mutate existing blobs or claim that retagging repairs them. Re-run graph, platform, runtime, inventory, provenance, signature, and target-policy gates. Promote the replacement by digest, roll it out, and verify effective runtime identity.

## Revocation record

Record revoked digest, reason, scope, discovery tags, first/last known use, affected evidence, replacement digest, owner, decision time, and retention/legal-hold policy. A registry deletion is not the revocation record and may not erase mirrors/backups/caches.

## Closure

Close only after active use is zero or explicitly accepted, replacement evidence passes, rollback no longer selects the revoked subject, tags are corrected/audited, and the original control gap has a regression test or policy gate.
