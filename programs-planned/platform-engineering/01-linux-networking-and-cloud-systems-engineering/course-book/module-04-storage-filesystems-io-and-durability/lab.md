# Lab — Module 04: Storage, Filesystems, I/O, and Durability

## Goal

Prove atomic result publication, failure cleanup, and an independent restore.

## Safety boundary

Use a temporary filesystem tree. Do not fill a shared filesystem. For a live `tmpfs` or loop-device exercise, use a disposable VM and a strict size bound.

## Baseline

Run the atomic-store and spool tests. Record filesystem type, mount, free blocks, and free inodes for the lab path.

## Hypothesis

A failed publication leaves the old final result intact and no temporary file; a completed backup is not accepted until restored and verified.

## Controlled action

Publish an initial result, inject a write failure using a bounded file-size or mock fixture, and verify cleanup. Create a backup of the completed spool, restore to a separate path, and verify bytes, modes, and job status.

## Oracle

Readers observe only complete old or new results; failed staging leaves no final partial object; restore reproduces expected state without reading the live directory.

## Evidence

Mount identity, hashes, modes, failure errno, temporary-file listing, backup artifact digest, restore transcript, and observed restore time.

## Interpretation

Explain whether the hypothesis was supported, falsified, or remained untested. Distinguish a mechanism result from a production claim and identify the first observation that changed your diagnosis.

## Cleanup

Unmount only lab-created mounts, remove temporary trees after descriptor checks, and verify free-space/inode counters return.

## Completion gate

Write the strongest durability claim supported by your environment and name the next untested failure boundary.

Do not progress with an ambiguous cleanup state or an unexplained deviation from the expected oracle.
