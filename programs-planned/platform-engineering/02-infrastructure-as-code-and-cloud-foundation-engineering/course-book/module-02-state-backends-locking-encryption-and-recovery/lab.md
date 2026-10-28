# Lab — Recover State Without Guessing

## Goal

Recover from an interrupted infrastructure operation without overwriting authoritative state, confusing history with truth, or using force-unlock as a substitute for diagnosis.

## Safety boundary

The required experiment uses the local state-backend model and immutable fixtures. It must not modify a real backend. The optional AWS path may use only a disposable sandbox bucket, a separate rehearsal key, versioning, and a bounded cost budget. Never rehearse recovery against an environment’s authoritative key.

## Baseline

Inspect:

```text
capstone/fixtures/state/backend-safe.json
capstone/fixtures/state/state-current.json
capstone/fixtures/state/state-next.json
capstone/fixtures/state/state-wrong-lineage.json
capstone/fixtures/plan/state-v1.json
capstone/fixtures/plan/state-v2.json
```

Create a short inventory of backend encryption, versioning, locking, lineage, serial, and recovery-key properties before inducing any failure.

## Hypothesis

A second writer must be rejected while the first owns the lock. An older serial is historical evidence, not automatically a valid recovery point. A different lineage must never be merged by assumption. Recovery should occur in an isolated rehearsal location, followed by refresh and explicit orphan classification. A state write failure after remote creation requires reconciliation, not blind re-application.

## Controlled action

1. Acquire the simulator lock as writer A.
2. Attempt to acquire it as writer B and retain the denial.
3. Simulate writer A creating a remote object and crashing before state commit.
4. Compare current, next, and wrong-lineage snapshots by digest, lineage, serial, and addresses.
5. Restore an older snapshot into an isolated rehearsal slot and compare it with the remote-object inventory.
6. Attempt to apply a plan bound to serial 1 after the state has advanced to serial 2.
7. Classify every unmatched object as import candidate, intentional unmanaged object, or deletion candidate. Do not perform the action automatically.
8. Write the incident decision required before force-unlock, including how you would establish that the original writer is no longer active.
9. Optional Level C: repeat the rehearsal with a disposable S3 backend key configured with versioning and native lockfile support. Retain only redacted identifiers and destroy the sandbox resources.

## Oracle

- writer B cannot enter the critical section while writer A owns it;
- force-unlock is unavailable without an explicit incident decision;
- wrong-lineage state is rejected;
- an older serial is classified as historical and restored only into the rehearsal slot;
- stale saved-plan context is rejected;
- no authoritative snapshot is overwritten during diagnosis;
- every remote/state mismatch receives one explicit disposition.

## Evidence

Retain:

```text
backend profile
lock acquisition and denial records
snapshot digest table
lineage and serial comparison
remote-versus-state reconciliation table
stale-plan rejection
force-unlock decision record
selected orphan-object disposition
```

Redact account identifiers, bucket names, KMS identifiers, and credentials from any optional cloud evidence.

## Interpretation

Explain why “restore the latest old file” is not a recovery algorithm. State may lag remote reality, a snapshot may belong to another lineage, and the crashed operation may have partially succeeded. The correct task is to reconstruct authority from independent evidence, then make one bounded repair.

## Cleanup

Release simulator locks, delete rehearsal slots, and run `make clean`. If the optional cloud exercise was used, delete rehearsal objects, backend bucket versions, lockfiles, and the sandbox bucket only after verifying no authoritative key was referenced.

## Completion gate

You pass only when you can describe the exact recovery sequence for “remote object created, state commit failed,” identify the evidence needed before force-unlock, and name the action you would explicitly avoid: blindly reapplying or overwriting state before reconciliation.
