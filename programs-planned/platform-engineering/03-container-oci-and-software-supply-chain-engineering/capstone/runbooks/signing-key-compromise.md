# Runbook — signing-key or signing-identity compromise

## Trigger

Use when private key material, keyless workload identity, certificate issuance policy, builder identity, or signing workflow may have been used without authorization.

## Containment

1. Stop new promotions relying on the identity.
2. Revoke/disable the key, workload, workflow, or issuer path according to the trust system.
3. Preserve signatures, certificates, transparency entries, provenance, workflow logs, and authorization policy.
4. Enumerate every subject signed during the exposure window.

Do not automatically classify every signed image as malicious. Signature compromise invalidates the authority evidence; image content/origin may still be independently recoverable.

## Re-evaluation

For each active/rollback subject, verify immutable content, source revision/review, builder provenance, materials, controlled build evidence, runtime/inventory/vulnerability policy, and deployment history. Classify as independently trusted, replacement required, or unresolved. Issue new attestations only from a restored authorized identity and only when the signer can legitimately attest to the claim.

## Recovery

Establish new key/identity, narrow policy, test rotation overlap and revocation, rebuild or re-attest according to the recovered evidence, promote replacement records, and update Course 4 admission data.

## Closure

No policy trusts the compromised identity; all affected subjects have owned disposition; active releases have valid current authority; incident evidence is retained; regression tests reject the compromised path.
