# Worked Answers — Module 04: Storage, Filesystems, I/O, and Durability

These answers demonstrate reasoning. Equivalent answers are valid when they preserve the same mechanism and evidence boundary.

## Exercise 1 — Rename and fsync

Rename can make pathname visibility atomic, but the new directory entry may remain only in volatile cache. Synchronizing the file protects its content; synchronizing the parent directory protects the namespace update according to the filesystem/storage contract. The exact power-loss guarantee remains bounded by the stack. State both atomic visibility and durability separately.

## Exercise 2 — Cross-filesystem temp

The directories may be on different filesystems. Rename across filesystems fails with `EXDEV`; a fallback copy exposes partial content and different durability. Create the temporary file in the destination directory, write and sync it, then replace the final name on the same filesystem.

## Exercise 3 — Deleted log

`lsof +L1` or `/proc/<pid>/fd` identifies unlinked open files. `findmnt` reveals mount layering, and inspecting the underlying mount after unmounting in a safe environment can reveal hidden entries. `df` versus `du` is a symptom, not the diagnosis. Do not unmount a live production path to investigate.

## Exercise 4 — Partial ENOSPC

It must treat the object as incomplete, stop using it as a final result, close and remove the temporary file where safe, preserve the previous final object, and report failure. Code must handle short writes and close/fsync errors. Retrying blindly can consume remaining space or expose mixed content.

## Exercise 5 — Inode exhaustion

The filesystem may have exhausted inode or metadata capacity, hit a quota, or have reserved space unavailable to the process. `df -i`, quota tools, filesystem-specific metrics, and the exact errno distinguish causes. A spool with millions of tiny files can exhaust inodes before bytes.

## Exercise 6 — Mount hides data

The mount changes pathname resolution so the new filesystem root is visible at that path; entries on the underlying filesystem remain but are hidden. They can still consume space. Inspect `findmnt` and design mount points empty before attachment. Accessing hidden data requires a safe alternate view or unmount, not casual production manipulation.

## Exercise 7 — Backup proof

Restore into an independent location, verify expected files, hashes, owners, modes, ACLs/xattrs if required, and application readability. Record consistency point, excluded state, key availability, observed recovery time, and failure domain. A successful archive creation proves only that the command produced an artifact.

## Exercise 8 — Root disk

Path convention does not control the underlying disk lifecycle. If `/var/lib` is on the root volume and deletion-on-termination is enabled, replacement loses it. The storage plan must map the path to persistent storage or backup/restore with a declared boundary. Test termination or replacement in the actual provider.

## Exercise 9 — Directory ownership

Creation requires write and execute permission on the containing directory and traversal through every parent. Use `namei -l`, inspect mount read-only state and ACLs, and test as the effective service identity. File ownership of an existing result does not grant directory-entry creation.

## Exercise 10 — Symlink risk

An attacker controlling a writable directory can replace an expected path with a symlink to another location, causing deletion or permission changes outside the intended tree. Use directory file descriptors, no-follow flags, ownership checks, and fixed roots. Avoid privileged recursive cleanup of paths assembled from untrusted names.

## Exercise 11 — Atomic completion order

If the claim were removed first and the process died before result publication, the job could disappear from every state. Publishing atomically first ensures either the processing claim remains recoverable or the result exists. Removing the claim after durable result publication completes the state transition. Cross-file atomicity remains bounded and should be reconciled after crash.

## Exercise 12 — Honest durability claim

A completed result is written to a temporary file on the destination filesystem, synchronized, atomically installed at its final name, and followed by parent-directory synchronization before the processing claim is removed. This is local-filesystem evidence. It does not claim protection against media loss, filesystem or device bugs, whole-volume loss, or zone failure; backup and cloud storage requirements address those boundaries.
