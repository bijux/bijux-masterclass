# Exercises — Module 01: Processes, System Calls, Files, and Signals

Complete these before opening the worked answers. Each response must name the mechanism, failure boundary, and decisive evidence where relevant.

## Exercise 1 — Program, process, and PID

Explain why an executable file, a process, and a PID are not interchangeable. Give one operational error caused by treating them as the same thing.

## Exercise 2 — Unlinked but open

A 20 GiB log is removed, but `df` reports no recovered space while `du` no longer finds it. Explain the most likely mechanism and the evidence you would collect.

## Exercise 3 — SIGTERM versus SIGKILL

Why can a service promise cleanup on `SIGTERM` but not on `SIGKILL`? What must the durability design assume?

## Exercise 4 — Zombie diagnosis

A process table contains a long-lived entry in state `Z`. What is retained, who owns the repair, and why does killing the zombie not solve it?

## Exercise 5 — Graceful worker contract

Design a shutdown sequence for the Atlas worker after it has claimed a job but before publishing the result.

## Exercise 6 — Useful strace question

Rewrite “run strace and see what happens” as a falsifiable investigation for a worker that appears hung.

## Exercise 7 — PID reuse defense

A cleanup script reads a PID from a file and sends `kill`. Add the minimum evidence needed before signaling.

## Exercise 8 — Exit result

A shell reports status 143. What can you infer, what can you not infer, and which raw evidence would be stronger?

## Exercise 9 — Pipe backpressure

An API writes logs to a pipe whose reader stops consuming. Why can this stall the API even though no disk is involved?

## Exercise 10 — Orphan helper

The API launches a helper and exits; the helper continues running. Explain why parent-child relationships alone are insufficient supervision.

## Exercise 11 — Descriptor inheritance

A child keeps the API port bound after the API process exits. What likely happened and how is it prevented?

## Exercise 12 — Checkpoint evidence

List the smallest evidence set that proves the Atlas worker handled a graceful stop without losing a claimed job.
