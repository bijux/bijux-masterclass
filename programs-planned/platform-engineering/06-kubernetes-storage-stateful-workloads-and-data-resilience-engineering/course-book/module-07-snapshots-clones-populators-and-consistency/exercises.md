# Exercises — Snapshots, Clones, Populators, and Consistency

Work from the chapter and executable artifacts, but write your own reasoning before reading the solutions. Each answer should name the authoritative state, the unsafe shortcut, and the evidence that would decide the case.

## 1. Distinguish crash and application consistency

What does a crash-consistent snapshot capture, and when is application quiescence required?

## 2. Design a group snapshot protocol

Atlas database uses separate data and WAL volumes. Describe a safe group snapshot sequence.

## 3. Interpret `readyToUse` correctly

A VolumeSnapshot reports ready. List what is proven and what remains unknown.

## 4. Choose clone, snapshot restore, or populator

A developer needs a sanitized 50 GiB test database. Compare three creation paths.

## 5. Protect snapshot deletion

Explain the difference between deleting a VolumeSnapshot object and deleting the underlying snapshot content.

## 6. Handle quiesce failure safely

The application freezes writes, but group snapshot creation times out. What should the controller do?

## 7. Evaluate snapshot chains

How can long copy-on-write snapshot chains affect the source even when snapshots are “read-only”?

## 8. Preserve historical truth

Should an old snapshot be rewritten or relabelled after discovering it was only crash-consistent?

## 9. Secure snapshot access

Why can read-only snapshot permission still expose the entire production database?

## 10. Design a restore test

What makes a snapshot restore test decisive rather than ceremonial?

## 11. Explain why snapshots are not backups

Give four reasons a storage snapshot may fail as the only recovery copy.

## 12. Decide if VolumeGroupSnapshot is required

When can independent per-volume snapshots be sufficient, and when is group coordination necessary?
