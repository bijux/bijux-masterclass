# Lab — Module 02: Identity, Permissions, Capabilities, and Service Supervision

## Goal

Prove positive and negative filesystem authority for each Atlas service identity and verify the systemd execution policy.

## Safety boundary

Use a disposable VM for real users and installed units. The dependency-light route uses temporary directories and your current identity; it cannot prove kernel enforcement for separate users.

## Baseline

Run `systemd-analyze verify capstone/systemd/*.service capstone/systemd/*.timer`. Review `sysusers.d` and `tmpfiles.d` before creating any account.

## Hypothesis

The API can write only its declared runtime/log/state paths, cannot alter `/opt/atlas` or TLS keys, and starts without root or unnecessary capabilities.

## Controlled action

In a VM, install the fixture users and directories, copy the release read-only, start the units, and perform controlled write attempts as each service user. Inspect effective unit properties and `/proc/<pid>/status`.

## Oracle

Required writes succeed; code, unit, and private-key writes fail; effective UID/GID and capability sets match policy; no service has a login shell; the units stop cleanly.

## Evidence

`namei -l`, `stat`, service-user write transcripts, unit properties, `/proc` credential fields, and systemd verification output.

## Interpretation

Explain whether the hypothesis was supported, falsified, or remained untested. Distinguish a mechanism result from a production claim and identify the first observation that changed your diagnosis.

## Cleanup

Stop and disable units, remove only course-created users and paths if the VM is not restored from snapshot, and verify no process remains.

## Completion gate

Defend every shared group and writable path. “It was required to make the lab work” is not sufficient.

Do not progress with an ambiguous cleanup state or an unexplained deviation from the expected oracle.
