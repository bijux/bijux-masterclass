# Module 04 — Storage, Filesystems, I/O, and Durability

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.

> **Central question:** When an application says that data was written, which bytes are actually durable and on which failure boundary?

## Where this module fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary. The capstone increment is:

> **Separate Atlas runtime, configuration, logs, queue state, and results; publish files atomically; and prove disk-full and restart behavior.**

This result is required before the next module can build on it honestly.

## Learning outcomes

- Distinguish files, directory entries, inodes, file descriptors, mounts, filesystems, and block devices.
- Explain page cache, writeback, sync, fsync, rename, and directory durability.
- Classify data as immutable code, configuration, ephemeral runtime state, logs, or durable application state.
- Design atomic publication that does not cross filesystem boundaries.
- Handle `ENOSPC`, inode exhaustion, partial writes, and interrupted cleanup explicitly.
- Perform and verify a small backup-and-restore exercise rather than equating backup creation with recoverability.

## Capstone increment

Separate Atlas runtime, configuration, logs, queue state, and results; publish files atomically; and prove disk-full and restart behavior.

## Names are not bytes

A pathname is resolved through directory entries and mount points to a filesystem object. A regular file's metadata is represented by an inode-like structure; directory entries associate names with objects. An open descriptor can continue to reference an object after its name is removed.

This distinction explains several operational surprises:

- deleting a large log does not free space while a process keeps it open;
- renaming a file changes directory entries, not its open descriptors;
- changing permissions on a pathname does not revoke already open access;
- mounting a filesystem over a non-empty directory hides the previous entries without deleting them.

Use `df` for filesystem block capacity, `df -i` for inode capacity, `du` for reachable directory content, and `lsof +L1` for unlinked open files. They answer different questions.

## The storage stack has multiple acknowledgement layers

An application write can be copied into a language buffer, a kernel page, a filesystem journal, a device cache, and eventually persistent media. “`write()` returned” usually means the kernel accepted bytes, not that a power loss cannot lose them.

`fsync` asks the system to make a file's data and required metadata durable according to the storage stack. After atomically replacing a pathname, synchronizing the parent directory may be required to make the directory-entry change durable. Filesystems and devices differ, so state the boundary rather than claiming universal power-loss behavior.

Atlas atomic publication follows:

```text
create temporary file in destination directory
→ write complete bytes
→ flush user-space buffer
→ fsync temporary file
→ set final mode
→ replace destination atomically
→ fsync parent directory
```

Creating the temporary file on another filesystem breaks atomic rename. Copying into place can expose partial content.

## Atomicity and durability are different

`rename` or `os.replace` can provide atomic visibility within one filesystem: readers see either the old or new name target. It does not alone prove that the new entry survives a crash. Conversely, synchronizing a file that readers can observe while it is being written provides durability without atomic publication.

The Atlas spool requires both properties for queue and result records. The exact guarantee is bounded to the destination filesystem and host storage configuration.

## Classify paths before choosing storage

Atlas separates:

- **immutable code** under `/opt/atlas`, replaced as a release;
- **configuration** under `/etc/atlas`, delivered by an authority outside the service;
- **runtime state** under `/run/atlas`, allowed to disappear at boot;
- **durable state** under `/var/lib/atlas`, expected to survive service and host restart;
- **logs** under `/var/log/atlas`, locally buffered but ideally exported;
- **backups** under an independent failure boundary.

A path does not become durable because it begins with `/var`. The mount, block device, snapshot policy, and restore process establish the actual boundary.

## Filesystems, mounts, and namespaces

A filesystem implements naming, metadata, allocation, and persistence semantics over some backing. ext4, XFS, tmpfs, network filesystems, and object-backed FUSE filesystems do not provide identical behavior.

Mount options can affect execution, device access, set-ID behavior, access times, write ordering, and error handling. Mount namespaces allow different process groups to see different trees. A bind mount re-exposes an existing subtree; it does not copy data.

Before relying on a feature, record:

```bash
findmnt -T /var/lib/atlas -o TARGET,SOURCE,FSTYPE,OPTIONS
stat -f /var/lib/atlas
lsblk -o NAME,TYPE,FSTYPE,SIZE,MOUNTPOINTS
```

## Disk-full and inode-full are normal failure cases

Writes may fail after some bytes were accepted. An application must check return values and close/fsync errors. A filesystem can have free blocks but no free inodes. Reserved blocks, quotas, thin provisioning, snapshots, or remote capacity can make reported space differ from the effective application boundary.

Atlas readiness creates, synchronizes, and removes a small file in the spool path. That proves a narrow current write operation, not future capacity. Capacity monitoring and alerting appear later in the program.

When `ENOSPC` occurs during publication, the temporary file must be removed and the old final object must remain intact. A failed log write should not silently turn a business operation into success.

## Backups are unproven until restore

A backup command can complete while omitting open data, ACLs, extended attributes, encryption keys, database consistency, or required configuration. A snapshot may be crash-consistent but not application-consistent.

Course 1 uses a small filesystem backup fixture. The lab restores into a separate path, verifies expected files and hashes, and starts a read-only inspection against the restored state. It does not overwrite the live state during the first test.

Define:

- what is backed up;
- which state is excluded;
- consistency point;
- encryption and access;
- retention;
- failure domain;
- restore procedure;
- restore verification;
- recovery point and recovery time observed in the exercise.

## Worked investigation: disk space did not return

Atlas logs filled a filesystem. An operator deleted `events.jsonl`, but `df` remains full. `du` no longer shows the bytes. `lsof +L1` shows that the API still holds the unlinked file open.

The correct repair is to rotate using a method the application supports or restart/reopen the writer under controlled conditions. Recreating a path with the same name does not redirect the old descriptor. The incident evidence should include the deleted inode, owning PID, descriptor, recovered space, and any log interval lost.

## Durability statement for the capstone

Atlas Host Runtime 1.0 claims that a completed result is published atomically and synchronized through the local filesystem interface before the processing claim is removed. It does not claim protection from corrupted media, a lying device cache, filesystem bugs, whole-volume loss, or zone loss. Those require storage and backup architecture defined in the outgoing handoff.

## Atlas implementation bridge

Read `atomic_store.py` and the spool transition tests. The implementation creates its temporary file in the destination directory, synchronizes bytes, replaces the name, and synchronizes the directory. The tests prove visible behavior; a VM crash experiment is needed for stronger storage-stack evidence.

Use the backup fixture only after documenting its omissions. Restore to a new path and compare data, modes, and hashes before attempting an in-place recovery.

## Design review prompts

- Which files may disappear at reboot?
- Which operation relies on same-filesystem rename?
- What happens if the final directory fsync fails?
- How is an unlinked open log detected?
- Which failure domain contains both live state and backup?

## Boundary case: concurrent readers and writers

Atomic replacement gives new path lookups an all-old or all-new result, but readers that already opened the old file continue reading it. This is usually desirable for configuration and result publication. If the application needs all readers to switch simultaneously, it requires a higher-level coordination protocol.

Multiple writers need ownership. Two workers writing the same final name can race even if each write is atomic. Atlas assigns one claimed job to one worker and uses deterministic result identity; a later distributed course adds fencing and stronger coordination.

## Boundary case: filesystem errors after close

Buffered or network filesystems can report errors during flush, `fsync`, or close rather than the initial write. Code must check those operations. A context manager that raises on close is part of the transaction outcome. Logging and then suppressing the error creates false success.

## Storage worksheet

```text
data class:
owner:
path/API:
backing filesystem or service:
atomicity requirement:
durability boundary:
maximum acceptable loss:
backup boundary:
restore oracle:
cleanup behavior after partial failure:
```

Use this worksheet before choosing a cloud disk, object store, or database in Course 2.

## Field method: write the durability protocol before writing code

A storage operation should be described as a sequence of state transitions and crash points. For an atomic Atlas result publication, the sequence is:

1. create a temporary file in the destination directory;
2. write the complete bytes;
3. flush language and userspace buffers;
4. synchronize the file according to the required durability boundary;
5. apply final mode and ownership policy;
6. rename within the same filesystem;
7. synchronize the parent directory when the claim includes recovery after a sudden crash;
8. remove or reconcile obsolete source state.

At each boundary, ask what a crash leaves behind. Before rename, the old visible result remains and a temporary file may require cleanup. After rename but before directory synchronization, visibility is established for running processes, but persistence of the directory entry across sudden power loss depends on filesystem and storage semantics. After publishing a result but before deleting the processing record, recovery may observe both. That is not automatically corruption, but the recovery algorithm must define which state wins and avoid duplicate effects.

`fsync` is not a universal remote durability primitive. A guest filesystem, virtual block device, host cache, storage controller, network volume, or managed service may acknowledge at a different boundary. State the failure boundary you tested: process crash, kernel crash, VM termination, host power loss, zone loss, or provider service failure.

Disk capacity also has multiple exhaustion modes. Byte blocks, inodes, project quotas, file-descriptor limits, and thin-provisioned backing storage can fail independently. Readiness should not perform an expensive write on every request, but the system must surface low-space and write failure before silently losing work. The Atlas readiness fixture checks a local write mechanism; later reliability courses add sustained monitoring and alert policy.

A backup is an input to recovery, not evidence of recovery. The module requires a restore into an empty destination, ownership and mode verification, application-level reading of restored results, and a recorded recovery time. If the restore depends on knowledge held only by the person who created the backup, the procedure is not yet operational.


## Standards and reference discipline

| Claim or rule | Category | Decisive evidence |
|---|---|---|
| Atomic pathname replacement and crash durability are different properties. | Filesystem semantics | reader observation plus fsync/restore experiment |
| A temporary file must be on the destination filesystem for atomic rename. | POSIX/Linux rename boundary | device ID and controlled cross-filesystem failure |
| Backup success is not restore success. | Atlas operational requirement | independent restore and hash verification |

A reference implementation may add behavior beyond a standard. A course policy may intentionally narrow legal behavior. Keep those claims separate when you write a runbook or defend a design.

## Failure patterns to recognize

### Cross-filesystem staging

A temporary file under `/tmp` may be on another filesystem, turning rename into failure or copy semantics.

### Deleting open logs

Removing a pathname does not close the writer descriptor or necessarily release blocks.

### Snapshot equals backup

A snapshot in the same account, region, key boundary, or failure domain may not satisfy recovery requirements.


## Module synthesis

Return to the central question: **When an application says that data was written, which bytes are actually durable and on which failure boundary?**

A complete answer names the owner of the relevant state, the transition that changes it, the failure boundary, and the observation that would falsify the claim. The capstone is ready to progress only when the new mechanism works and the planted defect—**A result is renamed into place but the parent directory is never synchronized, so the program overstates its crash-durability guarantee.**—fails for the predicted reason.

## Continue

Module 05 exposes the service through intentionally chosen interfaces and routes.

## Module route

1. [Complete the exercises](exercises.md) before viewing solutions.
2. [Compare with the worked answers](exercise-answers.md).
3. [Run the controlled lab](lab.md).
4. [Retain the checkpoint evidence](checkpoint.md).
