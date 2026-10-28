# Lab — Module 01: Processes, System Calls, Files, and Signals

## Goal

Prove the difference between graceful process termination and abrupt disappearance while preserving one claimed Atlas job.

## Safety boundary

Use only the dependency-light temporary Atlas runtime. Do not signal processes by a PID copied from an old run; identify the process from the current runtime file and verify its command first.

## Baseline

Run `make capstone-tour`. Then start the API, worker, and edge manually in a temporary directory using the commands in `capstone/README.md`. Submit one job and confirm it completes.

## Hypothesis

After `SIGTERM`, the worker stops taking new work, completes the current claim, exits zero, and leaves no orphan process. After `SIGKILL`, cleanup events may be absent and a processing claim must remain recoverable.

## Controlled action

Submit a job whose processing you can observe. Send `SIGTERM` to the verified worker and record process, event, claim, and result state. Repeat from a clean runtime, but send `SIGKILL` after a claim is visible. Start a replacement worker after the lease expires and observe recovery.

## Oracle

Graceful case: clean exit, no claim after the signal, and a completed or explicitly recoverable job. Abrupt case: signal termination, no graceful-stop event, and recovery from durable spool state without losing the job.

## Evidence

Process identity, signal command, wait status, relevant `/proc` fields, event lines, queued/processing/result directory listings, and replacement-worker recovery transcript.

## Interpretation

Explain whether the hypothesis was supported, falsified, or remained untested. Distinguish a mechanism result from a production claim and identify the first observation that changed your diagnosis.

## Cleanup

Terminate only verified current-run processes, wait for all children, and remove the temporary runtime after confirming no descriptor or process still references it.

## Completion gate

Explain why the abrupt case is a required correctness boundary even when the normal deployment uses graceful systemd shutdown.

Do not progress with an ambiguous cleanup state or an unexplained deviation from the expected oracle.
