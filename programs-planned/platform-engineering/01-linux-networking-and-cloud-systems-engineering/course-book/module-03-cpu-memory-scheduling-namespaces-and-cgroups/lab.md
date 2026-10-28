# Lab — Module 03: CPU, Memory, Scheduling, Namespaces, and cgroups

## Goal

Exercise CPU and memory boundaries and distinguish configured limits from observed enforcement.

## Safety boundary

Run only in a disposable Linux VM. The fixture is bounded, but resource policy mistakes can still make a small VM unresponsive. Keep console access and a snapshot.

## Baseline

Record host CPU count, memory, pressure, unit cgroup path, `cpu.stat`, `memory.current`, `memory.events`, and Atlas readiness without pressure.

## Hypothesis

A CPU quota increases throttling without necessarily changing liveness; a hard memory boundary contains allocation failure within the unit and leaves the rest of the host responsive.

## Controlled action

Run `ALLOW_RESOURCE_LAB=1 capstone/scripts/resource_lab.sh`. In a full VM lab, add a temporary transient unit with a smaller CPU quota and another with a bounded memory allocation near `MemoryMax`.

## Oracle

Effective controls are visible in the cgroup, throttling or memory events change as predicted, the experiment exits within its bound, and unrelated Atlas components remain observable.

## Evidence

Before/after cgroup controls and counters, PSI, process exit status, elapsed time, readiness, and host console responsiveness.

## Interpretation

Explain whether the hypothesis was supported, falsified, or remained untested. Distinguish a mechanism result from a production claim and identify the first observation that changed your diagnosis.

## Cleanup

Remove transient units, verify cgroups disappear or become empty, and confirm pressure returns to baseline.

## Completion gate

State which observation proves enforcement and which only proves configuration.

Do not progress with an ambiguous cleanup state or an unexplained deviation from the expected oracle.
