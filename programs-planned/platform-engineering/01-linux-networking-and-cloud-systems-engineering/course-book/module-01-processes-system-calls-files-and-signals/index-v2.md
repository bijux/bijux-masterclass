# Module 01 — Processes, System Calls, Files, and Signals

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.
> **Central question:** How does a Linux process actually acquire resources, communicate, fail, and terminate?

---

## Where This Module Fits

Atlas begins this module with every guarantee established earlier in the course. The new responsibility is not a new tool; it is a stronger boundary. Before we can orchestrate systems safely, we must understand the fundamental building blocks of how they run.

The capstone increment for this module is:

> **Run the Atlas API and worker as separate processes with explicit descriptors, exit behavior, signal handling, and observable process ownership.**

This result is required before the next module can build on it honestly.

---

## Learning Outcomes

By the end of this module, you will be able to:

* **Trace a program** from its executable image through process creation, system calls, file descriptors, and exit status.
* **Diagnose behavior** using `/proc`, `ps`, `lsof`, `strace`, and shell job control.
* **Distinguish** between process identity, parentage, sessions, process groups, and terminal ownership.
* **Design graceful shutdown** using `SIGTERM` handling, recognizing that `SIGKILL` cannot be handled.
* **Identify system leaks**, including descriptor leaks, zombie processes, orphaned children, and ambiguous shutdowns.
* **Prove process behavior** with verifiable transcripts and state observations rather than just screenshots.

---

## 1. A Process is More Than a PID

> **Concept Refresher: Program vs. Process**
> * **Program:** A passive set of instructions stored on disk (an executable file).
> * **Process:** An active, running instance of a program. It has its own memory (address space), credentials, current working directory, and a unique Process ID (PID).
> 
> 

Treating a process merely as “the PID in my shell” loses the state that matters most during debugging. A process includes a file-descriptor table, signal disposition, scheduling state, and relationships to other processes.

When your shell runs a command, it prepares redirections, establishes process-group relationships, and asks the OS kernel to execute a program. On Linux, this involves a sequence of system calls (like `fork` or `clone` to copy the current process, followed by `execve` to replace the copy with your new program).

**Observe Atlas in action:**

```bash
# Summarize process and scheduling state
ps -o pid,ppid,pgid,sid,stat,etime,cmd -C python3

# Expose credentials, threads, memory, and capabilities
cat /proc/<pid>/status

# Show which kernel objects the process can still reach
ls -l /proc/<pid>/fd

# See the current working directory
readlink /proc/<pid>/cwd

```

---

## 2. System Calls Are the Observable Kernel Boundary

> **Concept Refresher: User Space vs. Kernel Space**
> Modern operating systems are split in two. **User space** is where your normal applications (like Python scripts) run. **Kernel space** is the core of the OS with full hardware access. When an app needs to read a file, send network data, or allocate memory, it must politely ask the kernel to do it via a **System Call (syscall)**.

Application code does not directly read disks or send packets. A Python `open()` becomes one or more kernel operations; `print()` writes to a user-space buffer long before the actual `write(2)` syscall occurs.

`strace` is an invaluable tool because it observes this exact boundary:

```bash
strace -ff -e trace=%process,%file,%network -o /tmp/atlas.trace \
  python3 -m atlas_host.worker --config /tmp/atlas.json --once

```

**Warning:** Do not read a trace as a complete explanation of your application's logic. It only records the requests made to the kernel and the kernel's responses. Use it to test specific hypotheses, such as *“the worker is blocked on opening the spool directory”* or *“the client never attempted to connect.”*

---

## 3. File Descriptors Are Capabilities

> **Concept Refresher: File Descriptors (FDs)**
> In Linux, "everything is a file"—including regular files, network sockets, pipes, and hardware devices. A **File Descriptor** is simply a small integer the kernel uses to keep track of these open resources for a process.
> * `0` = Standard Input (stdin)
> * `1` = Standard Output (stdout)
> * `2` = Standard Error (stderr)
> 
> 

Descriptor inheritance is a common source of bugs. If an API opens a listening socket and then starts a child process without "close-on-exec" behavior, the child may accidentally keep that socket alive even after the API exits.

Furthermore, deleting a file on Linux only removes the directory entry. The actual disk space is not reclaimed until **all open file descriptors** pointing to it are closed.

**Gather evidence of open descriptors:**

```bash
ls -l /proc/<pid>/fd
lsof -p <pid>
cat /proc/<pid>/limits

```

---

## 4. Process Relationships Explain Cleanup and Zombies

> **Concept Refresher: The Process Lifecycle**
> * **Parent/Child:** Processes create other processes. The creator is the parent (PPID); the created is the child.
> * **Zombie:** A child process that has finished executing, but its parent hasn't yet "waited" to collect its exit status. It consumes almost no memory but clutters the process table.
> * **Orphan:** A child process whose parent died before it did. Linux safely hands orphans over to `PID 1` (the init system) to be managed.
> 
> 

A **process group** allows the shell to signal a pipeline as one unit. These relationships matter heavily when a service launches helpers. If you only terminate the leader, its descendants might keep running in the background. Modern systems (like `systemd`) use `cgroups` to supervise entire trees of processes rather than guessing based on parent-child links.

---

## 5. Signals Are Asynchronous Notifications

> **Concept Refresher: Common Signals**
> * `SIGTERM` (15): "Please stop gracefully." (Can be caught and handled).
> * `SIGINT` (2): Interruption, usually triggered by pressing `Ctrl+C`.
> * `SIGKILL` (9): "Stop immediately." (Cannot be caught, blocked, or ignored. Handled directly by the kernel).
> 
> 

A robust software shutdown contract states:

1. Which signal initiates graceful shutdown.
2. Whether new work is rejected immediately.
3. How in-flight work is completed, rolled back, or queued.
4. How long the supervisor waits before giving up.
5. What happens after the grace period expires.

For Atlas, the worker sets a stop event when it receives `SIGTERM`. It finishes its current job, refuses new ones, and exits.

Calling `kill -9` (`SIGKILL`) is **not** a stronger graceful stop—it violently removes the process, bypassing user-space cleanup. Only use it when intentionally testing ungraceful failure boundaries.

---

## 6. Exit Status and Logs Answer Different Questions

An exit status (like `0` for success) is a small integer reported back to the parent. A process terminated by a signal is represented differently by shells and APIs.

**Logs are not enough:** Structured logs explain context, but a supervisor must *never* infer successful completion just because it saw a final log line saying "shutting down." The decisive oracle for a graceful shutdown is:

* The process actually exited within the grace period.
* No new jobs were claimed.
* Every prior claim reached a definitive state (success, failure, or cleanly re-queued).

---

## 7. Worked Investigation: A Worker Disappears

**Scenario:** The API reports a job as `processing`, but no worker process is visible in `ps`, and a file is stuck in `spool/processing`.

A weak engineer says, *"Just restart the worker."* A systems engineer investigates by asking:

1. Does the recorded worker PID still exist, or was it reused by another app?
2. Which process actually owned the processing file?
3. Was the process killed normally, by a signal, by the Out-Of-Memory (OOM) killer, or by a supervisor?
4. Is the job's claim lease expired?
5. Can a new worker safely recover it without duplicating work?

You would use `/proc`, the system journal, and file modification times to find the truth before mutating the system.

---

## 8. Practical Command Map

When debugging, choose your command based on the specific question you are trying to answer. Avoid blindly running a memorized list of commands.

| Question | First Useful Evidence |
| --- | --- |
| **Is the process present?** | `ps`, `/proc/<pid>/status` |
| **Who launched or supervises it?** | PPID, cgroup, service-manager status |
| **What is it waiting on?** | `strace`, `/proc/<pid>/wchan`, stack tools |
| **Which files/sockets remain open?** | `/proc/<pid>/fd`, `lsof` |
| **Why did it exit?** | parent wait status, journal, kernel log |
| **Did shutdown preserve work?** | spool/result state and timestamps |

---

## 9. Atlas Implementation Bridge & Design Prompts

Read `capstone/atlas_host/api.py`, `worker.py`, and `events.py`. Identify exactly where user-space crosses into kernel-space: listener creation, file open, rename, signal delivery, sleep/wakeup, and process exit.

**Ask yourself these design questions:**

* Which descriptors *must* remain open for the process to function?
* What data survives an ungraceful kill?
* Could a stale PID in a log accidentally identify a completely unrelated new process?
* Does our graceful shutdown stop accepting new work *before* releasing existing work?

### Boundary Cases

* **Threads vs. Subprocesses:** A thread shares the descriptor table and memory space with its parent. A subprocess gets its own identity. A crashing thread kills the whole process; a crashing subprocess can be isolated.
* **Signals in Multithreaded Apps:** In Python, signal handlers execute in the main interpreter thread. A worker blocked in native code won't react instantly. Signal handlers should do *minimal* work (like flipping a boolean flag) and let the main loop handle the actual cleanup safely.

---

## 10. Investigation Worksheet

For every Atlas process you run, you must be able to fill out this worksheet. If any row is unknown, the process is not yet operationally owned.

```text
Executable/release identity:
PID and start identity:
Parent/supervisor:
Process group and cgroup:
Open listeners:
Open durable-state descriptors:
Stdout/stderr destination:
Accepted termination signal:
Grace period:
Ungraceful recovery mechanism:

```

---

## 11. Field Method: Reconstructing a Process

A useful investigation moves logically from **identity ➔ resources ➔ history**.

Use this exact sequence to investigate Atlas:

```bash
# 1. Safely extract the PID from the JSON state file
pid=$(cat /run/atlas/api.json | python3 -c 'import json,sys; print(json.load(sys.stdin)["pid"])')

# 2. Check process state, start time, and arguments
ps -o pid,ppid,pgid,sid,stat,lstart,etime,args -p "$pid"

# 3. Verify the exact executable on disk
readlink -f "/proc/$pid/exe"

# 4. View the full command line arguments
tr '\0' ' ' < "/proc/$pid/cmdline"; echo

# 5. Check capabilities, memory, and limits
cat "/proc/$pid/status"
cat "/proc/$pid/cgroup"

# 6. Audit all open resources
ls -l "/proc/$pid/fd"

```

When a process disappears unexpectedly, **preserve the exit status, signal, and logs before restarting it.** Restarting it immediately destroys the crime scene.

---

## 12. Failure Patterns to Recognize

* **PID-file Certainty:** A stale PID file can point to a reused PID. Always verify the executable identity, start time, and cgroup to ensure it's the program you think it is.
* **Logging as Completion:** A final log line can be buffered or emitted *before* data is safely written to disk. Use exit status and file timestamps as proof.
* **Killing Only the Parent:** Descendants can survive if you only kill the parent process. Always supervise via a `cgroup` or process group.

---

## Module Synthesis

Return to the central question: **How does a Linux process actually acquire resources, communicate, fail, and terminate?**

A complete engineering answer names the owner of the state, the kernel transition that changes it, the failure boundary, and the observation that proves it. You are ready to move on *only* when the planted capstone defect fails for the exact reason you predicted.

### Module Route

1. Complete the exercises before viewing solutions.
2. Compare with the worked answers.
3. Run the controlled lab.
4. Retain the checkpoint evidence.