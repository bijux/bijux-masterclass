# Laboratory — Rotate a secret without leaking it

## Goal

Exercise an encrypted/reference-based secret change through controller retrieval, Kubernetes projection, workload adoption, overlap, and revocation.

## Safety boundary

Use synthetic credentials and the local secret authority. Never place a real secret in the course repository or evidence directory.

## Baseline

Version A is active and the workload proves it can authenticate.

## Hypothesis

Version B should not permit revocation of A until the workload has demonstrably adopted B; plaintext must never appear in Git or reports.

## Controlled action

Create version B, reconcile the reference, simulate workload reload, test both versions during overlap, revoke A, and scan all repository and report files for plaintext.

## Oracle

Promotion is accepted only after B is used successfully and A fails after revocation. The plaintext scanner finds no leak.

## Required evidence

Save non-secret version IDs, controller status, workload adoption event, overlap tests, revocation result, policy outcome, and scanner report.

## Interpretation

A synchronized Secret without workload adoption is incomplete. A successful rotation that leaks plaintext is a failed release.

## Cleanup

Destroy synthetic secret material, retain only identifiers and proof output, then rerun the repository scanner.

## Completion gate

The learner can locate decryption authority, plaintext lifetime, workload adoption, and revocation evidence.
