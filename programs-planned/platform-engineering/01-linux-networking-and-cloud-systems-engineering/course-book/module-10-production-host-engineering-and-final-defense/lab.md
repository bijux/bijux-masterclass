# Lab — Module 10: Production Host Engineering and Final Defense

## Goal

Release Atlas Host Runtime 1.0, run a bounded multi-fault game day, restore the system, and export the exact Course 2 handoff.

## Safety boundary

Run the full game day only in a disposable VM. Establish console access, snapshot, abort criteria, and cleanup owner before injecting faults.

## Baseline

Verify manifest, units, PKI, capstone tour, backup/restore, listener policy, resource envelope, and handoff files. Record the strongest evidence class available.

## Hypothesis

Each injected fault causes the predicted first oracle, is diagnosed without weakening another boundary, and leaves no residual state after recovery.

## Controlled action

Stage worker termination, storage writability loss, backend loss, certificate failure, and name-resolution failure. Repair each, rerun focused proof, then rebuild handoff and course manifests.

## Oracle

Readiness and routing react truthfully, durable jobs remain complete or recoverable, verified TLS returns, baseline tour passes, and post-clean manifests verify exactly.

## Evidence

Game-day timeline, hypothesis/result table, commands, raw evidence paths, repair diffs, restore time, final tour, handoff manifest, and unexecuted Class D claims.

## Interpretation

Explain whether the hypothesis was supported, falsified, or remained untested. Distinguish a mechanism result from a production claim and identify the first observation that changed your diagnosis.

## Cleanup

Restore snapshot or reverse every change, terminate all lab processes, remove temporary routes/mounts/certs, clean generated reports, and verify manifests after cleanup.

## Completion gate

Defend one end-to-end request, one ungraceful failure, one recovery, and every Course 2 infrastructure requirement.

Do not progress with an ambiguous cleanup state or an unexplained deviation from the expected oracle.
