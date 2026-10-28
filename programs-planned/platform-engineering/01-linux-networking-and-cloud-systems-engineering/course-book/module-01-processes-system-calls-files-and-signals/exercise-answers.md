# Worked Answers — Module 01: Processes, System Calls, Files, and Signals

These answers demonstrate reasoning. Equivalent answers are valid when they preserve the same mechanism and evidence boundary.

## Exercise 1 — Program, process, and PID

An executable file is stored program content. A process is a running execution context with memory, credentials, descriptors, signal state, and scheduling state. A PID is a namespace-scoped numeric identifier for one process at one time. A stale PID file can point to a later unrelated process after PID reuse. An operator who sends a signal using only the stale number can terminate the wrong workload. Strong identification combines supervisor ownership, cgroup, executable identity, and process start time.

## Exercise 2 — Unlinked but open

Removing the directory entry does not destroy the open file description held by a writer. The filesystem can reclaim blocks only after the last open reference closes. `du` walks reachable names, so it stops counting the file; `df` reports allocated blocks and remains full. Use `lsof +L1` or `/proc/<pid>/fd` to identify an unlinked descriptor and its owner. Repair by making the process reopen logs or by controlled restart, then verify the descriptor closes and space returns.

## Exercise 3 — SIGTERM versus SIGKILL

`SIGTERM` can be caught, blocked, or handled, so the process can stop admission, finish or release work, flush bounded state, and exit. `SIGKILL` is enforced by the kernel and cannot be handled. Therefore correctness must not depend exclusively on graceful cleanup. Durable claims, leases, atomic publication, and restart recovery must preserve or reconstruct state when the process disappears at any instruction boundary.

## Exercise 4 — Zombie diagnosis

The child has already exited; the kernel retains minimal termination information until its parent collects it with a wait operation. The zombie is not running and cannot process a signal. The parent owns the repair: it must reap children or delegate supervision to a component that does. Inspect PPID and the parent behavior. If the parent is broken, restart or fix the parent under controlled conditions. Repeated zombies indicate lifecycle ownership failure.

## Exercise 5 — Graceful worker contract

On `SIGTERM`, the worker should set a stop flag and refuse new claims. It should complete the already claimed bounded unit, atomically publish the result, remove the processing claim, record the transition, and exit zero. If work cannot finish within the grace period, the design needs checkpoint or lease recovery. The supervisor waits a declared duration and may then force termination. The oracle checks claim state and result publication, not only a final log line.

## Exercise 6 — Useful strace question

State a hypothesis such as: “The worker is blocked opening a spool file because directory traversal is denied.” Trace only file and process calls, capture timestamps, and expect an `openat` or `stat` failure with `EACCES`. If the trace instead shows repeated `nanosleep`, the hypothesis is false and the worker may simply be polling. The trace is decisive only for the system-call boundary; application reasons still require code and state evidence.

## Exercise 7 — PID reuse defense

Verify that the PID exists, its start time matches the recorded start identity, its executable or command belongs to Atlas, and its cgroup or supervisor unit is the expected one. Prefer asking the supervisor to stop the unit rather than signaling by PID. If a PID file remains necessary, record process start ticks from `/proc/<pid>/stat` and compare them. Abort on mismatch; never “best effort” kill an uncertain process.

## Exercise 8 — Exit result

Shells commonly encode termination by signal as 128 plus signal number, so 143 often means SIGTERM. That convention is not the full wait status and does not prove why the signal was sent or whether cleanup succeeded. Stronger evidence includes the supervisor result, kernel wait status, service journal, signal event, durable work state, and remaining descendants. A zero result also does not prove business correctness.

## Exercise 9 — Pipe backpressure

A pipe has bounded kernel buffering. Once full, a blocking write waits for the reader to consume bytes. The API may then stop serving requests or hold locks while blocked. The process appears alive and may use little CPU. Inspect descriptors, `strace` showing a blocked `write`, and the reader process. Logging architecture needs bounded buffering and failure policy; changing the destination from disk to pipe does not remove backpressure.

## Exercise 10 — Orphan helper

When the parent exits, the helper can be adopted by another reaper and continue. Its PPID changes, so scripts that kill only children of the original PID miss it. A service manager should own the complete cgroup or explicit process group and terminate all unit processes according to policy. The application should also avoid unmanaged background daemons. Verify unit cgroup membership, not only process ancestry.

## Exercise 11 — Descriptor inheritance

The listening descriptor was inherited across process creation and remained open in the child. The kernel keeps the socket alive while any descriptor refers to it. Set close-on-exec for descriptors that should not cross exec, close unnecessary descriptors in the child, and let the supervisor own socket activation explicitly when desired. `/proc/<child>/fd` and `ss -lntp` reveal the surviving owner.

## Exercise 12 — Checkpoint evidence

Retain the worker PID/start identity, signal timestamp, claim record before the signal, event showing no later claim, atomic result or recoverable queue state, processing directory after exit, and process exit status. This set connects request, ownership, durable effect, and lifecycle. A screenshot of `ps` after shutdown cannot prove that the in-flight job was preserved.
