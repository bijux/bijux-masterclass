# Module 03 — CPU, Memory, Scheduling, Namespaces, and cgroups

> **Program stage:** Course 1 of 10 — Understand and operate the substrate.
> **Central question:** How does the kernel share finite host resources, and how can one workload be bounded without making false isolation claims?

---

## Where This Module Fits

Atlas begins this module with every security guarantee established in Course 1. Now, we add a new responsibility: **Resource Containment**. An application can be perfectly secure and correct in isolation, but still take down a host by consuming an unbounded share of CPU or Memory.

The capstone increment for this module is:

> **Publish and exercise a resource envelope for Atlas using cgroup v2 and systemd resource controls, with explicit throttling and memory-failure behavior.**

This result is required before the next module can build on it honestly.

---

## Learning Outcomes

By the end of this module, you will be able to:

* **Distinguish** between CPU time, load average, utilization, run-queue pressure, and throttling.
* **Explain** virtual memory, resident memory, page cache, swap, overcommit, and Out-Of-Memory (OOM) selection.
* **Read** cgroup v2 hierarchies, controller rules, and kernel pressure evidence.
* **Use** namespaces and cgroups accurately, understanding why they are mechanisms—not complete security boundaries.
* **Choose** CPU, memory, task, and file-descriptor limits based on actual workload evidence.
* **Demonstrate** bounded failure and recovery using safe stress fixtures.

---

## 1. The Myth of Infinite Capacity

A host has finite CPU time, memory, tasks (PIDs), file descriptors, I/O bandwidth, and kernel structures. Resource engineering begins by explicitly naming which quantity is constrained and deciding exactly what should happen when that boundary is hit.

For Atlas, we define separate "resource envelopes" for the API, worker, and edge services. A real limit cannot be guessed; it must come from measuring the workload and intentionally leaving headroom for the kernel, the service manager, logging, and recovery operations.

---

## 2. CPU: Utilization, Load, and Throttling

> **Concept Refresher: CPU Metrics**
> * **CPU Utilization (%):** How much time the CPU spent actively doing work over a given interval.
> * **Load Average:** A measure of the system's *run queue*. It counts processes that are currently using the CPU, waiting for the CPU, or stuck waiting for uninterruptible I/O (like a slow disk). A load of 4.0 means 4 processes are in this state.
> * **CPU Quota vs. Weight:** A *quota* is a hard ceiling (e.g., "you get exactly 1 CPU core's worth of time per second"). A *weight* is a relative share (e.g., "if there is contention, Service A gets twice as much CPU time as Service B").
> 
> 

CPU observations are notoriously easy to misread. For example, a task blocked on a slow disk can drive the Load Average sky-high, even though actual CPU utilization remains at 5%.

Conversely, a CPU *Quota* can cause your application to be heavily throttled, resulting in massive latency spikes, even while the host's overall CPU utilization appears low.

**How to gather CPU evidence:**

```bash
cat /proc/loadavg                 # Check run queue pressure
cat /proc/stat                    # Check host-wide CPU time
ps -eo pid,psr,stat,ni,pcpu,comm  # Check process-level CPU usage
cat /sys/fs/cgroup/<group>/cpu.stat # Look for 'nr_throttled' to prove quota limits

```

---

## 3. Memory: Virtual vs. Resident and the OOM Killer

> **Concept Refresher: Memory Types**
> * **Virtual Memory (VSZ):** The theoretical address space a process has *asked* for. (A process can ask for 10GB but only actually use 100MB).
> * **Resident Set Size (RSS):** The physical RAM the process is actually occupying right now.
> * **Page Cache:** The kernel uses unused RAM to cache recently read/written files. "Low free memory" is often completely fine because the kernel will instantly dump this cache if an application needs real RAM.
> * **OOM Killer:** The Out-Of-Memory Killer. When the system physically runs out of memory, the kernel plays executioner, calculating a "badness score" for processes and forcefully killing them (`SIGKILL`) to save the OS.
> 
> 

"Memory pressure" happens when useful applications compete for RAM, the kernel struggles to reclaim cache, system latency rises, and allocations start to fail.

A service killed by the OOM killer did *not* exit cleanly. It was violently terminated.

**How to gather Memory evidence:**

```bash
cat /proc/meminfo                        # Overall system memory
cat /proc/<pid>/smaps_rollup             # Deep dive into a specific process's memory
cat /proc/pressure/memory                # Pressure Stall Information (PSI)
cat /sys/fs/cgroup/<group>/memory.current # Real memory used by a cgroup
cat /sys/fs/cgroup/<group>/memory.events  # Logs of OOM kills or limit hits

```

---

## 4. cgroups: The Kernel's Limiters

> **Concept Refresher: cgroups (Control Groups)**
> If namespaces dictate what a process can *see*, cgroups dictate what a process can *use*. cgroups are a kernel feature that limits, accounts for, and isolates the resource usage (CPU, memory, disk I/O, network) of a collection of processes.

cgroup v2 organizes processes into a single unified hierarchy. **A child process can never escape a limit imposed by its parent's cgroup.** systemd automatically creates and owns cgroups for the units it manages.

Important cgroup v2 controls exposed via systemd:

* `MemoryMax=`: A hard memory boundary (triggers OOM kill inside the cgroup if breached).
* `MemoryHigh=`: A pressure boundary (triggers aggressive memory reclaim, slowing the app down before it hits the max).
* `CPUQuota=`: A hard bandwidth ceiling over a specific period.
* `TasksMax=`: Prevents fork-bombs by limiting the total number of threads/processes.

*Note: A limit is a ceiling, not a reservation. Setting `MemoryMax=512M` does not guarantee 512MB will actually be available on the host.*

---

## 5. Namespaces: Views, Not Security Boundaries

> **Concept Refresher: Namespaces**
> Namespaces are a kernel feature that wraps a global system resource in an abstraction, making it appear to the processes within the namespace that they have their own isolated instance of the global resource.
> * *Examples:* PID namespace (process thinks it is PID 1), Network namespace (process thinks it has its own private network interfaces).
> 
> 

Namespaces are foundational for containers (like Docker), but **a namespace alone does not create a secure container.** Processes still share the exact same kernel. To make a boundary truly secure, namespaces must be combined with capabilities, cgroups, `seccomp` filters, and strict filesystem mounts.

---

## 6. What Happens When We Hit the Wall? (Failure Semantics)

A useful resource policy specifies exactly what happens at the boundary:

* **CPU Quota hit:** Requests become slower (throttled). The service stays alive, but latency spikes.
* **Memory High hit:** The system violently reclaims cache. The application slows down heavily.
* **Memory Max hit:** The process attempts to allocate memory, the kernel refuses, and the OOM killer terminates a process within the cgroup.
* **Tasks Max hit:** The application tries to create a new thread or spawn a child process, and it fails.
* **File Descriptor limit hit:** `open()` or `accept()` system calls fail with `EMFILE`. The app can no longer read files or accept network connections.

A supervisor (like systemd) restarting a service cannot magically fix a deterministic memory limit that gets exceeded on every single request. The application must be designed to handle these failures gracefully.

---

## 7. Worked Investigation: Green Host, Slow API

**Scenario:** Host CPU utilization is only 45%, but the Atlas API's latency has doubled.

**Investigation:** You check the API unit's `/sys/.../cpu.stat` and see `nr_throttled` increasing rapidly. The host has 8 spare CPU cores, yet the API is struggling. Why?
Because the systemd unit was configured with `CPUQuota=50%`. This limits the entire API cgroup to *half of one CPU core*, regardless of how idle the rest of the machine is.

The correct response is not to blindly delete the quota. You must determine: Was this quota intentional? Did the workload increase? You must record the workload, throttling counters, and latency together before changing the boundary.

---

## 8. Bounded Stress, Not Destructive Stress

When testing limits in a lab, use a **bounded stress fixture**—a script that allocates a specific, known amount of memory and sleeps briefly.

**Never use an unbounded fork bomb, a script that completely fills a disk, or an infinite memory allocator as an educational shortcut.** The skill we are learning is *controlled failure and recovery*, not surprise destruction.

---

## 9. Field Method: Interpret Pressure Before Choosing Limits

Resource limits are policy, not diagnosis. Before setting limits, you must understand your workload. Build your resource envelope by answering:

```text
Steady API requests per second:
Maximum concurrent connections:
Maximum request bytes:
Worker concurrency:
Largest in-flight job:
Expected page-cache use:
Startup burst CPU/RAM:

```

Once you know this, choose `MemoryHigh` as an early-warning pressure signal, `MemoryMax` as a hard containment boundary to protect the rest of the host, and `TasksMax` to prevent thread explosions. Include interpreter overhead and file buffers, and always add a measured safety margin.

---

## 10. Failure Patterns to Recognize

* **Host Average Hides Unit Throttling:** A specific cgroup can be heavily throttled and dropping traffic while the host-wide CPU dashboard shows a healthy 30% utilization.
* **RSS Arithmetic Errors:** Simply adding up the Resident Set Size (RSS) of all processes will drastically over-calculate memory usage, because processes often share the exact same memory pages (like shared C libraries).
* **Limits Without Failure Design:** Adding a memory ceiling without programming the application to handle failures gracefully simply converts a slow system into a system that constantly crashes opaquely.

---

## Module Synthesis

Return to the central question: **How does the kernel share finite host resources, and how can one workload be bounded without making false isolation claims?**

A complete answer names the resource, the kernel mechanism that limits it (cgroups), the behavior when the limit is breached, and the specific `/sys` or `/proc` file that proves it happened. The capstone is ready to progress only when your new envelope works, and the planted defect—*The worker has no memory ceiling, and readiness remains green while host memory pressure causes unrelated services to stall*—fails for the exact reason you predicted.

### Module Route

1. Complete the exercises before viewing solutions.
2. Compare with the worked answers.
3. Run the controlled lab.
4. Retain the checkpoint evidence.