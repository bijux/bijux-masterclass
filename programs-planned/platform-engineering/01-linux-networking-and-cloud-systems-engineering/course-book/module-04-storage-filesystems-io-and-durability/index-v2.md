# Module 04 — Storage, Filesystems, I/O, and Durability

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.  
> **Central question:** When an application says that data was written, which bytes are actually durable and on which failure boundary?

---

## Where This Module Fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary around data persistence.

The capstone increment for this module is:

> **Separate Atlas runtime, configuration, logs, queue state, and results; publish files atomically; and prove disk-full and restart behavior.**

This result is required before the next module can build on it honestly. Before we trust a database or a cloud storage bucket, we must understand how basic files actually work.

---

## Learning Outcomes

By the end of this module, you will be able to:

* **Distinguish** between files, directory entries, inodes, file descriptors, mounts, filesystems, and block devices.
* **Explain** page cache, writeback, `sync`, `fsync`, atomic `rename`, and directory durability.
* **Classify** data into immutable code, configuration, ephemeral runtime state, logs, or durable state.
* **Design** atomic file publications that do not accidentally cross filesystem boundaries.
* **Handle** `ENOSPC` (No space left on device), inode exhaustion, and interrupted cleanups explicitly in code.
* **Perform** and verify a true backup-and-restore exercise, proving that creating a backup is not the same as being able to recover.

---

## 1. Names Are Not Bytes

> **Concept Refresher: Inodes vs. File Names**
> In Linux, a "file" and its "name" are two different things.
> * **Inode:** The actual underlying object on the disk that holds the file's metadata (permissions, size) and points to the actual data blocks.
> * **Directory Entry (Name):** A human-readable label (like `events.log`) that points to an inode.
> * **File Descriptor:** An open connection to an inode used by a running process.
> 
> 

This separation explains several operational surprises:

* **The Phantom Large File:** Deleting a massive log file does not immediately free disk space *if a process still has it open*. The directory entry (the name) is deleted, but the inode and data blocks remain until the final file descriptor is closed.
* **Renaming:** Renaming a file only changes the directory entry. It does not break open file descriptors.
* **Mount Hiding:** Mounting a new filesystem over a non-empty directory hides the old files; it does not delete them.

**How to gather storage evidence:**

```bash
df -h         # Check total block capacity (Gigabytes)
df -i         # Check total inode capacity (Number of files)
du -sh *      # Measure reachable files in a directory
lsof +L1      # Find "deleted" files that are still held open by a process

```

---

## 2. The Storage Stack Has Multiple Acknowledgement Layers

> **Concept Refresher: The Journey of a Byte**
> When your Python app calls `file.write("hello")`, the data is NOT immediately on the physical hard drive. It travels through layers:
> 1. Language Buffer (e.g., Python's internal memory)
> 2. Kernel Page Cache (RAM)
> 3. Filesystem Journal
> 4. Device Cache (Hard Drive's onboard RAM)
> 5. Persistent Media (Magnetic platters or Flash memory)
> 
> 

When `write()` returns success, it usually just means the *kernel accepted the bytes into RAM*. A power loss at this exact moment will lose the data.

To guarantee data is physically written, applications must use **`fsync`**. `fsync` forces the kernel and the storage device to flush the data all the way down to the persistent media.

**The Atlas Atomic Publication Protocol:**
To safely update a file without anyone ever reading a half-written version, follow this exact sequence:

1. Create a temporary file in the *same destination directory*.
2. Write all bytes to the temporary file.
3. Flush the user-space buffer.
4. `fsync` the temporary file (ensures bytes are durable).
5. Set final file permissions (mode).
6. Atomically replace the old file with the temporary file (`rename`).
7. `fsync` the parent directory (ensures the rename itself survives a crash).

*Warning: Creating the temporary file in `/tmp` and moving it to `/var/lib` breaks atomic rename if they are on different filesystems. The OS will silently fall back to copying the file chunk-by-chunk, exposing partial content.*

---

## 3. Atomicity and Durability Are Different

* **Atomicity:** Readers see either the old file or the new file. They *never* see a mix of both. (Achieved via `rename`).
* **Durability:** The file survives someone pulling the power plug out of the wall. (Achieved via `fsync`).

An atomic `rename` does not prove the new file survives a crash. Conversely, `fsync`ing a file while you are writing it provides durability, but a concurrent reader might read half the file before you finish (lacking atomicity). Atlas requires *both* for queue state.

---

## 4. Classify Paths Before Choosing Storage

A path does not become durable just because it begins with `/var`. You must deliberately map data types to the correct Linux directories:

| Path | Data Classification | Lifecycle |
| --- | --- | --- |
| `/opt/atlas` | **Immutable Code** | Replaced entirely during a release. Read-only for the app. |
| `/etc/atlas` | **Configuration** | Authored by deployment tools. Read-only for the app. |
| `/run/atlas` | **Runtime State** | Ephemeral (PIDs, sockets). Allowed to disappear on reboot. |
| `/var/lib/atlas` | **Durable State** | The actual database/queue. Expected to survive host reboots. |
| `/var/log/atlas` | **Logs** | Locally buffered evidence, meant to be exported and rotated. |

---

## 5. Filesystems, Mounts, and Namespaces

Not all filesystems behave identically. `ext4`, `XFS`, network drives (NFS), and memory-backed filesystems (`tmpfs`) have vastly different crash semantics.

Before relying on a storage feature, prove what you are actually writing to:

```bash
findmnt -T /var/lib/atlas -o TARGET,SOURCE,FSTYPE,OPTIONS
lsblk -o NAME,TYPE,FSTYPE,SIZE,MOUNTPOINTS
stat -f /var/lib/atlas

```

---

## 6. Disk-Full and Inode-Full Are Normal Failure Cases

> **Concept Refresher: Inode Exhaustion**
> You can have 500 GB of free space left on your disk, but if you create millions of tiny 1-byte files, you will run out of *inodes*. Once inodes are exhausted, the OS will return `ENOSPC` (No space left on device) even though you have gigabytes of space left.

An application must check return values and close/fsync errors. When `ENOSPC` occurs during a file publication, your code must cleanly remove the temporary file and leave the old, final object intact. A failed log write should not silently cause a financial transaction to look like a success.

---

## 7. Backups Are Unproven Until Restore

Creating a backup file is not the goal; **restoring a system** is the goal. A backup command can complete successfully while omitting open data, extended attributes, or database consistency.

For the capstone, define:

* What is backed up?
* What state is intentionally excluded?
* Restore procedure (always to a new, empty path first).
* Restore verification (checking file hashes and modes).
* Recovery Point Objective (RPO) and Recovery Time Objective (RTO) observed in the exercise.

---

## 8. Worked Investigation: Disk Space Did Not Return

**Scenario:** The server's disk filled up. An operator hastily ran `rm /var/log/atlas/events.jsonl`. However, running `df -h` shows the disk is still 100% full.

**Investigation:** The operator deleted the *name*, but the API process still has the file descriptor open, so the kernel refuses to delete the *bytes*.
Running `lsof +L1` reveals the unlinked file is still held open by the API.

**Fix:** Recreating a file with the same name doesn't fix it. The correct repair is to trigger the application's native log rotation, or safely restart the service so it closes its file descriptors and releases the bytes.

---

## 9. Storage Worksheet

Before choosing a cloud disk, object store, or database, complete this worksheet for your application's data:

```text
Data class:
Owner:
Path/API:
Backing filesystem or service:
Atomicity requirement:
Durability boundary (when is it safe to say "done"?):
Maximum acceptable loss (RPO):
Backup boundary:
Restore oracle (how do we know the restore worked?):
Cleanup behavior after partial failure:

```

---

## 10. Field Method: Write the Protocol Before the Code

At every boundary in your code, ask: *What does a crash leave behind right now?*

* **Before rename:** The old result remains, and a temporary file exists (requires cleanup on reboot).
* **After rename, before directory fsync:** The new file is visible to running processes, but if the power cuts, the filesystem might revert the directory entry to the old file.
* **After publish, before deleting the old claim:** Recovery might observe both the published result and the processing claim. Your recovery algorithm must know which one wins to avoid duplicate work.

`fsync` is not a magic wand. A virtual block device, host cache, or network volume might acknowledge a write at a different physical boundary than a local SSD. Always state the failure boundary you actually tested (e.g., process crash, VM termination, or host power loss).

---

## Failure Patterns to Recognize

* **Cross-Filesystem Staging:** Creating a temporary file in `/tmp` (which is often a RAM disk `tmpfs`) and moving it to `/var/lib` breaks atomic rename and forces a slow, non-atomic data copy.
* **Deleting Open Logs:** Assuming `rm` frees disk space without checking if the file is held open.
* **Snapshot Equals Backup:** Assuming an AWS EBS snapshot is a true backup. If the AWS account is compromised, or the region fails, the snapshot may be lost alongside the primary volume.

---

## Module Synthesis

Return to the central question: **When an application says that data was written, which bytes are actually durable and on which failure boundary?**

A complete answer names the owner of the relevant state, the transition that changes it, the failure boundary, and the observation that would falsify the claim. The capstone is ready to progress only when the new mechanism works and the planted defect—*A result is renamed into place but the parent directory is never synchronized, so the program overstates its crash-durability guarantee*—fails for the predicted reason.

### Module Route

1. Complete the exercises before viewing solutions.
2. Compare with the worked answers.
3. Run the controlled lab.
4. Retain the checkpoint evidence.