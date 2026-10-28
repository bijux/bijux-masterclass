# Case 3 — Ready snapshot, broken restore

## Incident

A `VolumeSnapshot` reports `readyToUse=true`. The restored database starts but fails integrity checks and cannot complete log recovery.

## Evidence

- Snapshot creation occurred while a multi-volume database checkpoint was in progress.
- Only the data volume was selected; the separate log volume was omitted.
- No application generation or log position was recorded.
- The restore test had previously checked only that the PVC became Bound.

## Failure

The snapshot system produced a valid storage copy of an incomplete recovery set. Storage readiness was misrepresented as application consistency.

## Correct response

Classify the snapshot as crash-consistent and unusable for the intended recovery. Define the complete member set, coordinate an application checkpoint, use group snapshot capability where supported, and record the logical generation. Restore all members into new claims and run database and business-level validation.

## Lesson

The final oracle belongs to the application. Snapshot API status closes a control-plane transition; it does not prove a service can recover.
