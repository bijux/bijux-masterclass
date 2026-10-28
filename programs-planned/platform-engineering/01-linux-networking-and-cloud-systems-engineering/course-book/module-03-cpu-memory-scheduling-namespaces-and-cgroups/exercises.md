# Exercises — Module 03: CPU, Memory, Scheduling, Namespaces, and cgroups

Complete these before opening the worked answers. Each response must name the mechanism, failure boundary, and decisive evidence where relevant.

## Exercise 1 — Load versus utilization

A four-core host has load average 8 and CPU utilization 30%. Give a plausible explanation.

## Exercise 2 — RSS sum

Why is summing process RSS an unreliable estimate of total unique memory consumption?

## Exercise 3 — Page cache

The host has little “free” memory but low memory pressure. Is this automatically a problem?

## Exercise 4 — memory.high and memory.max

Contrast `memory.high` with `memory.max` in cgroup v2.

## Exercise 5 — CPU quota surprise

Host CPU is available but Atlas is throttled. Explain how this can occur.

## Exercise 6 — PSI value

What question does pressure stall information answer better than a utilization gauge?

## Exercise 7 — Namespace limitation

A process is in a new PID namespace. Name two host powers it may still retain.

## Exercise 8 — pids.max

Why can a task-count limit protect the host even when CPU and memory limits exist?

## Exercise 9 — Descriptor exhaustion

What happens when a process reaches its file-descriptor limit, and which symptoms may appear?

## Exercise 10 — OOM evidence

How do you distinguish an OOM kill from a graceful application exit?

## Exercise 11 — Limit versus reservation

Why does `MemoryMax=512M` not guarantee the service can allocate 512 MiB?

## Exercise 12 — Resource checkpoint

What evidence proves a CPU limit was enforced rather than merely configured?
