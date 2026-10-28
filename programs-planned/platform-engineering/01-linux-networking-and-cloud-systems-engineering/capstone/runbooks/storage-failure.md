# Runbook — Atlas Storage Failure

## Trigger

Readiness reports unwritable state, queue transitions fail, free blocks/inodes are exhausted, or result integrity differs.

## Preserve

Record mount identity/options, filesystem usage, inode usage, kernel/storage errors, queue directory inventory, and the last successful transition. Avoid running cleanup that destroys evidence.

## Diagnose

Distinguish permission, read-only remount, full blocks, full inodes, quota, underlying device error, and application path error. Identify whether a result already exists for any processing record before requeueing.

## Recover

Restore writable capacity or mount health, reconcile each queue item, verify atomic publication with a fixture, and perform an application-level read of restored data.

## Prohibited shortcuts

Do not make the release directory writable, delete unknown queue files, or call a backup successful without an empty-destination restore.
