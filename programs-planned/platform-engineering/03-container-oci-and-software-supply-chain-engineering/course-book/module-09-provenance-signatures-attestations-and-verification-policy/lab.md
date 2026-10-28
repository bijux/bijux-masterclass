# Laboratory — Verify the signer, then distrust the claim

## Goal

Create signed provenance for Atlas and prove that cryptographic validity is only the beginning of release verification.

## Safety boundary

The included private key is a public laboratory fixture. Never reuse it outside the course or interpret its signatures as real organizational authorization.

## Baseline

Generate provenance for the accepted API index, wrap it in DSSE, sign it, and verify the envelope and subject.

## Hypothesis

Only a statement with the exact subject, accepted signer fingerprint, approved builder/source/materials, and complete policy evidence will pass.

## Controlled action

1. modify payload after signing;
2. replace subject digest and re-sign with the fixture key;
3. keep subject but change builder ID to `developer-laptop` and re-sign;
4. verify with a different public key;
5. mark materials complete while adding undeclared network input;
6. verify the accepted controlled rebuild record.

## Oracle

Tampering fails cryptography. Re-signed wrong-subject and wrong-builder statements pass cryptographic checks but fail policy. Unsupported completeness claims fail. The accepted record passes within its declared evidence scope.

## Evidence

Submit envelope, signer fingerprint, provenance summary, every failure classification, and a statement of what the fixture key cannot prove.

## Interpretation

Separate authenticity, origin description, process assurance, and release authorization.

## Cleanup

Remove generated defect envelopes and preserve only checked fixtures/reports.

## Completion gate

You can explain why each rejected candidate failed even when a valid signature was present.

## Continue

- [Checkpoint](checkpoint.md)
- [Chapter](index.md)
