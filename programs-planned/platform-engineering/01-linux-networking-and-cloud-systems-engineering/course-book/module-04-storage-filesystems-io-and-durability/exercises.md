# Exercises — Module 04: Storage, Filesystems, I/O, and Durability

Complete these before opening the worked answers. Each response must name the mechanism, failure boundary, and decisive evidence where relevant.

## Exercise 1 — Rename and fsync

Why can atomic rename still leave a crash-durability gap?

## Exercise 2 — Cross-filesystem temp

Why is creating a temporary file under `/tmp` risky before moving it into `/var/lib/atlas`?

## Exercise 3 — Deleted log

Which commands distinguish an unlinked-open file from hidden data under a mount?

## Exercise 4 — Partial ENOSPC

A write returns after writing only part of a buffer before `ENOSPC`. What must the application do?

## Exercise 5 — Inode exhaustion

How can file creation fail when `df -h` reports free capacity?

## Exercise 6 — Mount hides data

Why can mounting a filesystem over a non-empty directory make files “disappear” without deletion?

## Exercise 7 — Backup proof

A tar command exits zero. Which additional evidence is required before calling the backup recoverable?

## Exercise 8 — Root disk

Why is `/var/lib/atlas` not automatically durable across cloud instance replacement?

## Exercise 9 — Directory ownership

The worker owns files but cannot create a new result. What path evidence is needed?

## Exercise 10 — Symlink risk

Why can a privileged cleanup routine following symlinks be dangerous?

## Exercise 11 — Atomic completion order

Why does Atlas publish the result before removing the processing claim?

## Exercise 12 — Honest durability claim

Write a bounded durability statement for Atlas Course 1.
