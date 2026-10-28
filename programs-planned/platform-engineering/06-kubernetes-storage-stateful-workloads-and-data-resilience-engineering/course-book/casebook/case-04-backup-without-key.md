# Case 4 — Backup without a usable key

## Incident

Backups have completed for months and object checksums are valid. During a cluster-loss drill, the recovery team cannot decrypt them because the KMS key was retired with the original environment.

## Evidence

- Backup objects exist in a separate bucket.
- The manifest records an old key identifier.
- Key deletion followed infrastructure teardown policy.
- Recovery principals were never tested outside the primary account.

## Failure

The data copy survived, but the recovery plane did not. Backup retention and key retention were governed independently.

## Correct response

Record key identity and historical decrypt requirements in every backup manifest. Place recovery keys or wrapping authority in an independent, audited boundary. Add a pre-retirement check that rejects key deletion while retained backups depend on it. Execute a drill that obtains the key through the real recovery process.

## Lesson

Encryption is part of recoverability. A backup is not restorable unless bytes, catalogue, software, credentials, and keys all remain available at the chosen disaster tier.
