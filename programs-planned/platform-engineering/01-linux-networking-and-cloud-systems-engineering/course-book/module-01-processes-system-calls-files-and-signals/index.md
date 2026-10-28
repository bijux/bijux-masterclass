# Module 01 — Processes, System Calls, Files, and Signals

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.

> **Central question:** How does a Linux process actually acquire resources, communicate, fail, and terminate?

## Where this module fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary. The capstone increment is:

> **Run the Atlas API and worker as separate processes with explicit descriptors, exit behavior, signal handling, and observable process ownership.**

This result is required before the next module can build on it honestly.

## Learning outcomes

- Trace a program from executable image through process creation, system calls, descriptors, and exit status.
- Use `/proc`, `ps`, `lsof`, `strace`, and shell job control to explain observed behavior.
- Distinguish process identity, parentage, sessions, process groups, and terminal ownership.
- Design graceful `SIGTERM` handling without pretending `SIGKILL` can be handled.
- Recognize descriptor leaks, zombie processes, orphaned children, and ambiguous shutdown.
- Prove process behavior with transcripts and state observations rather than screenshots alone.

## Capstone increment

Run the Atlas API and worker as separate processes with explicit descriptors, exit behavior, signal handling, and observable process ownership.

## A process is more than a PID

A program is an executable representation stored somewhere. A process is a running instance with an address space, credentials, file-descriptor table, signal disposition, scheduling state, environment, current directory, and relationships to other processes. A PID is only one identifier in one PID namespace. Treating a process as “the PID in my shell” loses the state that matters during debugging.

When the shell runs a command, it prepares redirections, creates or reuses descriptors, establishes process-group and terminal relationships, and eventually asks the kernel to execute a program image. On Linux the exact sequence may involve `fork`, `clone`, `vfork`, `execve`, or library wrappers. The portable mental model is simpler: a new execution context inherits selected state, then an executable image replaces its program code and data.

Inspect Atlas while it runs:

```bash
ps -o pid,ppid,pgid,sid,stat,etime,cmd -C python3
cat /proc/<pid>/status
ls -l /proc/<pid>/fd
readlink /proc/<pid>/cwd
```

These views answer different questions. `ps` summarizes process and scheduling state. `/proc/<pid>/status` exposes credentials, threads, memory, capabilities, and signal masks. `/proc/<pid>/fd` shows which kernel objects the process can still reach. The current directory can keep a mount busy even when no file appears open.

## System calls are the observable kernel boundary

Application code does not directly read disks or send packets. It asks the kernel through system calls. Libraries may buffer, retry, combine, or transform those calls. A Python `open()` becomes one or more kernel operations; `print()` may write to a user-space buffer long before `write(2)` occurs.

`strace` is useful because it observes the system-call boundary:

```bash
strace -ff -e trace=%process,%file,%network -o /tmp/atlas.trace \
  python3 -m atlas_host.worker --config /tmp/atlas.json --once
```

Do not read a trace as a complete application explanation. It records requests and results at one boundary, not why the application chose them. It can alter timing and may expose sensitive paths or data. Use it to test a hypothesis such as “the worker is blocked in `openat` on the spool directory” or “the client never called `connect`.”

## File descriptors are capabilities held by a process

A descriptor is a small process-local integer referring to an open file description. That underlying kernel object may represent a regular file, socket, pipe, directory, terminal, event source, or device. Descriptors 0, 1, and 2 conventionally carry standard input, output, and error, but that is policy established by the parent process.

Descriptor inheritance is a common source of surprises. If the API opens a listening socket and then starts a child without close-on-exec behavior, the child may keep the socket alive after the API exits. A log file can remain writable through an inherited descriptor even after pathname permissions change. Deleting a file removes a directory entry; disk space is not reclaimed until all open references disappear.

Use evidence:

```bash
ls -l /proc/<pid>/fd
lsof -p <pid>
cat /proc/<pid>/limits
```

The capstone keeps API, worker, and edge processes separate so descriptor ownership remains visible. It does not daemonize itself or hide behind a framework supervisor.

## Process relationships explain cleanup and zombies

A parent can wait for a child and collect its termination status. If the child exits and the parent has not waited, the kernel retains a small zombie record. A zombie consumes little memory but signals broken process ownership. If a parent exits first, an orphan is adopted by a subreaper or PID 1 in the namespace.

A process group allows the shell or supervisor to signal a pipeline or job as one unit. A session groups process groups and usually has a controlling terminal. These relationships matter when a service launches helpers: terminating only the leader may leave descendants running. systemd later uses cgroups to supervise the whole unit rather than guessing from parent-child relationships alone.

## Signals are asynchronous notifications, not transactions

`SIGTERM` requests termination and can be handled. `SIGINT` usually represents interactive interruption. `SIGHUP` has historical terminal semantics and is often repurposed for reload. `SIGKILL` and `SIGSTOP` cannot be caught, blocked, or ignored.

A robust shutdown contract states:

1. which signal initiates graceful shutdown;
2. whether new work stops immediately;
3. how in-flight work is completed, rolled back, or made recoverable;
4. how long the supervisor waits;
5. what happens after the grace period;
6. which exit status represents clean termination.

The Atlas worker sets a stop event when it receives `SIGTERM`. It stops claiming new jobs but finishes the already claimed job before exiting. That is a bounded policy, not a universal rule. A long-running computation may instead checkpoint and return the claim to a durable queue.

Calling `kill -9` is not “a stronger graceful stop.” It removes the process before user-space cleanup. Use it only when you are intentionally testing the ungraceful failure boundary.

## Exit status and logs answer different questions

An exit status is a small result reported to the parent or supervisor. Zero conventionally indicates success. A process terminated by a signal is represented differently by shells and APIs. Structured logs can explain context, but the supervisor must not infer successful service completion from the presence of a final log line.

For Atlas, preserve:

```text
signal received
last claimed job
result publication
process exit status
remaining processing files
supervisor decision
```

The decisive oracle for graceful shutdown is not “the log says stopped.” It is that the process exited within the grace period, no new job was claimed after the stop request, and every prior claim reached a result, failure, or recoverable queued state.

## Worked investigation: a worker disappears

Suppose the API reports a job as `processing`, no worker process appears in `ps`, and a file remains under `spool/processing`.

A weak response is “restart the worker.” A systems investigation asks:

1. Does the recorded worker PID still exist, and could it have been reused?
2. Which process owned the processing file?
3. Was the process terminated normally, by signal, by the OOM killer, or by supervisor action?
4. Is the claim lease expired?
5. Can another worker recover it without duplicating an already published effect?

Use `/proc`, journal evidence, the processing filename, modification time, and result directory. The Atlas worker's lease recovery demonstrates one mechanism: an old processing file is moved back to queued state. The course does not call this distributed exactly-once processing. It is a host-local recovery rule whose safety depends on deterministic result publication and one host filesystem.

## Practical command map

| Question | First useful evidence |
|---|---|
| Is the process present? | `ps`, `/proc/<pid>/status` |
| Who launched or supervises it? | PPID, cgroup, service-manager status |
| What is it waiting on? | `strace`, `/proc/<pid>/wchan`, stack tools |
| Which files or sockets remain open? | `/proc/<pid>/fd`, `lsof` |
| Why did it exit? | parent wait status, journal, kernel log |
| Did shutdown preserve work? | spool/result state and timestamps |

Choose commands from the question. Do not begin with a memorized diagnostic ritual.

## Atlas implementation bridge

Read `capstone/atlas_host/api.py`, `worker.py`, and `events.py`. Identify every point at which user-space crosses into a kernel-managed object: listener creation, file open, rename, signal delivery, sleep/wakeup, and process exit. Run the tour and map event PIDs to `/proc` while the processes are alive.

The reference code deliberately stays in the foreground. A process manager must own daemonization, output capture, restart, and group cleanup. If you add a helper process, document descriptor inheritance and termination ownership before writing code.

## Design review prompts

- Which descriptor must remain open for each process to serve its responsibility?
- Which state survives an ungraceful kill?
- Can the parent distinguish clean completion from signal termination?
- Could a stale PID identify an unrelated process?
- Does graceful shutdown stop admission before completing or releasing existing work?

## Boundary case: fork, exec, threads, and subprocesses

A thread shares a process address space and descriptor table but has its own scheduling identity and stack. A subprocess has a separate process identity and can replace its executable image. This distinction changes failure containment: one crashing native thread normally terminates the process; one crashing helper process can be restarted or isolated if the parent owns its protocol.

Python's `subprocess` API is a wrapper over operating-system process creation. It can still leak descriptors, deadlock on full pipes, or inherit environment and credentials. Use explicit argument arrays rather than a shell when command parsing is unnecessary. If a shell is required, treat command construction as an injection boundary.

## Boundary case: signals and multithreaded programs

Signals are delivered according to process and thread masks. Python executes signal handlers in the main interpreter thread, which means a worker blocked in native code may not react immediately. A handler should perform minimal work—usually set an event or write to a self-pipe—and let the normal loop complete cleanup.

Do not call complex non-reentrant library functions from low-level signal handlers in systems languages. The safe pattern depends on runtime, but the design principle remains: convert asynchronous notification into an ordinary state transition.

## Investigation worksheet

For each Atlas process, complete:

```text
executable/release identity:
PID and start identity:
parent/supervisor:
process group and cgroup:
open listeners:
open durable-state descriptors:
stdout/stderr destination:
accepted termination signal:
grace period:
ungraceful recovery mechanism:
```

If any row is unknown, the process is not yet operationally owned.

## Field method: reconstructing a process from evidence

A useful process investigation moves from identity to resources to history. Start with the executable and arguments, then establish parentage, process group, session, controlling terminal, namespaces, cgroup, open descriptors, and current system-call state. No single command owns the truth. `ps` formats selected `/proc` fields; `lsof` adds descriptor interpretation; `/proc/<pid>/fd` shows links as the kernel exposes them; `strace` observes system calls from the attachment point onward. The evidence may change while you inspect it, so record timestamps and avoid treating two commands run seconds apart as one atomic snapshot.

Use this sequence for Atlas:

```bash
pid=$(cat /run/atlas/api.json | python3 -c 'import json,sys; print(json.load(sys.stdin)["pid"])')
ps -o pid,ppid,pgid,sid,stat,lstart,etime,args -p "$pid"
readlink -f "/proc/$pid/exe"
tr '\0' ' ' < "/proc/$pid/cmdline"; echo
cat "/proc/$pid/status"
cat "/proc/$pid/cgroup"
ls -l "/proc/$pid/fd"
```

Then explain each descriptor. A listening socket is an owned resource; a deleted-but-open log file still consumes storage; an inherited pipe can keep a reader from receiving end-of-file. Descriptor inheritance is controlled across `fork` and `exec` through close-on-exec policy. A child that unintentionally inherits a privileged socket can preserve access after the intended process exits.

PID values are reusable. A stale PID file can identify a different process after restart. The stronger identity is supervisor ownership plus start time, cgroup membership, executable identity, and—where needed—a pidfd. This is why Atlas writes PID evidence for teaching but delegates real lifecycle ownership to systemd in Module 02.

When a process disappears, preserve exit status, terminating signal, supervisor result, recent events, and any core-dump policy before restarting it. Restarting first may destroy the most decisive evidence. The operational habit developed here persists throughout the program: observe the owner and transition before modifying the system.


## Standards and reference discipline

| Claim or rule | Category | Decisive evidence |
|---|---|---|
| Process exit status is collected by a parent or supervisor; a PID alone is not a complete lifecycle record. | POSIX/Linux mechanism | `wait`, service-manager status, `/proc` |
| `SIGKILL` cannot be caught or handled by the target process. | POSIX signal semantics | ungraceful-stop lab and exit status |
| Open descriptors survive pathname rename or unlink until references close. | POSIX/Linux file semantics | `/proc/<pid>/fd`, `lsof +L1` |

A reference implementation may add behavior beyond a standard. A course policy may intentionally narrow legal behavior. Keep those claims separate when you write a runbook or defend a design.

## Failure patterns to recognize

### PID-file certainty

A stale PID file can identify a reused PID. Verify executable identity, start time, cgroup, and supervisor ownership.

### Logging as completion

A final log line can be buffered or emitted before durable effect. Use exit status and durable state as separate evidence.

### Killing only the parent

Descendants can survive when ownership is inferred only from PPID. Supervise a cgroup or explicit process group.


## Module synthesis

Return to the central question: **How does a Linux process actually acquire resources, communicate, fail, and terminate?**

A complete answer names the owner of the relevant state, the transition that changes it, the failure boundary, and the observation that would falsify the claim. The capstone is ready to progress only when the new mechanism works and the planted defect—**The worker acknowledges a job before durable completion and exits immediately on `SIGTERM`, losing the in-flight result.**—fails for the predicted reason.

## Continue

Module 02 assigns operating-system identity and supervision to these processes.

## Module route

1. [Complete the exercises](exercises.md) before viewing solutions.
2. [Compare with the worked answers](exercise-answers.md).
3. [Run the controlled lab](lab.md).
4. [Retain the checkpoint evidence](checkpoint.md).
