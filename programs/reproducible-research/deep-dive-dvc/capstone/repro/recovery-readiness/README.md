# Recovery Readiness Specimen

This specimen models a remote migration with two promises that must survive:

- the current `main` dataset must be recoverable for ongoing work
- the published `release-2025-q1` dataset must remain recoverable for audit

The audit builds the Git and DVC history in an isolated workspace. It first records the
three-row release, tags it, then records a four-row mainline revision. The two revisions
have different DVC object identities, so restoring only the current workspace cannot
accidentally prove that release history survived.

## Contract surfaces

Read these files before running the audit:

1. `recovery-contract.json` names the protected revisions, expected contents, recovery
   objective, and cutover gate.
2. `data/observations.csv` is the published release dataset. The audit adds a later
   observation to create the mainline dataset.

The source directory is not a ready-made DVC repository. The audit copies it, creates the
history, and provisions isolated legacy and candidate remotes. This prevents a learner's
global Git configuration, cache, or remote from supplying hidden evidence.

## Decision under review

The candidate remote may replace the legacy remote only when a cache-empty reviewer can
restore every protected revision, match its content claim, and finish within the declared
recovery-time objective. Current-workspace success alone is not enough.
