# Checkpoint — Provenance and verification policy

## Required evidence

- exact-subject provenance statement;
- DSSE envelope and signature verification;
- signer trust policy;
- wrong-subject and wrong-builder rejections;
- materials-completeness evaluation;
- controlled rebuild comparison;
- key rotation/revocation plan.

## Decision defense

Defend the authorized builder identity and explain why the public course fixture key provides no production assurance.

## Progression gate

Proceed when all evidence objects are bound to exact digests and policy distinguishes “cryptographically valid” from “authorized for release.” Module 10 will promote, revoke, roll back, and hand the release to Kubernetes.

## Continue

- [Next stage](../module-10-release-promotion-revocation-and-kubernetes-handoff/index.md)
- [Course index](../index.md)
