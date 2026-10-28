---
module_id: CONPAR-002
program: Programming Languages: Concurrent & Parallel Programming
level: 1
module_number: 2
title: Processes, Threads, Tasks, and Fibers
status: complete
last_verified: 2026-08-29
---

# Processes, Threads, Tasks, and Fibers

## One-Page Review

### Governing question

Which boundary owns resources, which context executes instructions, which unit expresses work, and which scheduler decides where that work runs?

### Essential definitions

- A **process** is an operating-system execution and protection domain with a virtual address space and resource/security context; exact contents and sharing rules are OS-specific.
- A **kernel thread** is an OS-scheduled execution context, commonly with registers, stack, scheduling state, and thread-specific attributes, that shares its process resources with peer threads.
- A **platform thread** is a language-runtime thread represented by or closely bound to an OS thread for its lifetime.
- A **task** is a logical unit of work with code, data environment, lifecycle, dependencies, and possibly a result. A task is scheduled *onto* an execution context and is not inherently a thread.
- A **fiber** is a user-space, normally cooperatively scheduled execution context, often stackful, that runs on a hosting thread. Terminology varies across runtimes.
- A **virtual thread**, **goroutine**, or other runtime-managed lightweight context is a language-specific abstraction multiplexed over fewer OS threads; it should be described by its specification rather than assumed to be a generic fiber.
- A **scheduler** selects an eligible execution context or task and maps it to a worker or processor subject to dependencies and resource policy.
- **Preemption** allows a scheduler to interrupt an executing context at permitted boundaries. **Cooperative suspension** requires the context to yield, await, or block through an integrated runtime point.
- **Blocking** prevents a context from progressing until a condition occurs. Whether it also immobilizes its carrier depends on the runtime and operation.
- **Isolation** limits unintended observation and interference; a separate process often supplies a stronger default fault/address-space boundary than peer threads, but never guarantees complete security or availability.

### Central model, mechanism, or theorem

Let $P$ be processes, $K$ kernel threads, $R$ runtime-managed contexts, and $T$ logical tasks. At time $\tau$, partial mappings describe ownership and placement:

$$
owner_K:K\to P,\qquad carrier_\tau:R\rightharpoonup K,\qquad work_\tau:T\rightharpoonup R.
$$

Several tasks may successively use one runtime context; many runtime contexts may be multiplexed over fewer kernel threads; and kernel threads are scheduled on processors. Therefore

$$
|T|,\ |R|,\ |K|,\ \text{and processor count}
$$

are independent quantities. A correctness argument must use actual sharing, suspension, cancellation, and lifecycle rules—not names such as “task” or “thread.”

### Critical invariants

Every unit of work has an owner that observes success, failure, cancellation, and cleanup. Shared process memory requires synchronization regardless of whether access comes from platform threads, virtual threads, fibers, or migrated tasks. Per-thread state is not safely per-task when tasks migrate or share carriers. Potentially blocking operations must state whether they suspend only the logical context or pin/block the worker. Admission and queues are bounded. Process isolation, task structure, and scheduler placement are separate claims.

### Common failures

Frequent mistakes are creating one thread per tiny task; calling every asynchronous handle a thread; assuming processes share nothing; treating a task as already running; storing request context in worker-thread locals; blocking an event-loop or fiber carrier with unsupported I/O; assuming lightweight contexts make CPU work faster; cancelling a future while its external effect continues; leaking detached children; using process boundaries as the only security control; and benchmarking worker counts without queue, memory, correctness, or tail-latency evidence.

### Compact example

Suppose tasks A, B, and C have resumable segments. A runs first on worker 0, suspends, then resumes on worker 1; B uses worker 1 while A waits; C later uses worker 0. There are three task identities, two worker-thread identities, and possibly one or two simultaneously available processors. Thread-local state follows workers, not A. Task-local state must follow A across suspension.

### Connections

[CONPAR-001](001-concurrency-parallelism-and-asynchrony.md) separates logical overlap, physical parallelism, and delayed completion. [CONPAR-003 through CONPAR-010](../ROADMAP.md) develop schedules, safety, liveness, races, ownership, and model choice. Kernel process/thread machinery belongs to [Operating Systems](../../22-operating-systems/ROADMAP.md); remote failure and node boundaries belong to [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md).

## Governing Question

When a program says “start this concurrently,” what exactly is created, which resources does it share, who may schedule it, and what must wait for its completion?

Process, thread, task, and fiber are not four sizes of the same thing. A process primarily establishes an OS-managed resource and protection domain. A thread primarily supplies an execution context within such a domain. A task primarily represents work and its dependencies. A fiber primarily supplies a runtime-managed resumable context. Real runtimes compose them: tasks run on virtual threads, virtual threads mount on platform threads, platform threads map to kernel threads, and those threads run inside processes on processors.

Terminology is not fully portable. Java specifies platform and virtual `Thread` instances. Go specifies goroutines as independent concurrent threads of control in one address space but deliberately abstracts runtime mapping. OpenMP tasks are code plus a data environment that an implementation assigns to team threads. Windows exposes a named fiber API; other libraries call comparable mechanisms green threads, user-level threads, coroutines, or continuations with materially different stack and scheduling semantics. The safe approach is to state the mechanism's properties.

## Why This Matters

Choosing the wrong abstraction can break correctness before performance. Moving request context into a thread-local works while one request occupies one platform thread, then leaks context when tasks share workers or migrate. Calling a blocking native operation from a cooperative runtime can immobilize a carrier and starve thousands of logical contexts. Sharing an unsynchronized map among fibers is still a race if another carrier runs peers in parallel. Cancelling a task handle may not cancel the database change it initiated.

Resource costs differ. Processes carry address spaces, kernel bookkeeping, handles, credentials, and IPC boundaries. Kernel/platform threads carry scheduled contexts and stacks. Runtime-managed contexts can use smaller or growable stacks and cheaper switching, but their queues, captured state, timers, and task-local data still consume memory. Tasks can be extremely small descriptions, yet millions of queued tasks can exhaust the heap before any execute.

Isolation differs too. Peer threads ordinarily share their process address space and many resources, so an invalid write or fatal process failure can affect all. Separate processes usually require explicit shared memory or IPC and can be restarted independently. Yet processes can share files, credentials, namespaces, inherited descriptors, kernel limits, and a host; they are not automatically mutually untrusted sandboxes.

Operational diagnosis depends on the mapping. A thread dump that shows ten carrier threads may correspond to a million virtual threads. A process monitor may show one hot process while one runtime worker monopolizes CPU. A trace that records only task IDs cannot reveal carrier pinning. Production observability needs stable process, kernel-thread, logical-context, task, parent, and request relationships where the runtime exposes them.

## Prerequisites and Retrieval

Retrieve CONPAR-001's definitions of concurrency, parallelism, asynchrony, schedule, dependency, and ownership. Understand stacks, function calls, virtual memory at a conceptual level, queues, identity, partial functions, and resource limits.

Remember that “running” is a state, not an identity. A task may be created, queued, eligible, running, suspended, cancelled, failed, or complete. A thread may be runnable but not executing on a processor. A fiber may retain a stack while suspended. A process can contain no application thread currently on-CPU and still own live resources.

No OS scheduler implementation, memory-model formalism, or specific async framework is assumed. Later modules own joins, synchronization, event loops, cooperative scheduling, cancellation, structured concurrency, thread pools, and task graphs.

## Learning Objectives

By the end of this module, you should be able to:

1. distinguish resource/protection domains, execution contexts, logical work, and user-space resumable contexts;
2. trace a task through runtime context, carrier thread, kernel scheduler, and processor;
3. identify which state is private, shared, inherited, copied, or explicitly communicated for each mechanism;
4. explain platform-thread, virtual-thread, goroutine, task, coroutine, and fiber terminology without false equivalence;
5. predict when blocking suspends only logical work and when it pins or blocks a worker;
6. reject thread-local assumptions for work that can migrate;
7. compare process isolation with in-process communication and switching costs;
8. design lifecycle, admission, cancellation, cleanup, and observability contracts; and
9. select mechanisms from workload and failure boundaries rather than syntax or advertised scale.

## Core Exposition

A **process** is best treated as an OS-owned resource and protection boundary, not merely “a running program.” It commonly has a virtual address space, open-resource table, credentials, signal or exception dispositions, accounting identity, environment, and one or more threads. Exact details vary by OS and creation API. Several processes can execute the same program image, and one process can replace its program image without retaining all of its prior threads.

Process separation changes communication. Ordinary pointers do not directly designate objects in another process address space. Programs use pipes, sockets, shared-memory mappings, files, kernel objects, or higher-level IPC. This explicit boundary aids containment and independent restart but adds serialization, copying or shared-memory synchronization, system calls, protocol versioning, partial failure, and operational complexity.

A **thread** carries instruction execution within a process. Peer threads generally share executable code, heap, global variables, and process resources, while each has register state, a stack, scheduling state, and thread-specific data. The precise signal masks, identifiers, priorities, and inherited attributes are platform rules. Shared address space makes communication cheap but lets races, aliasing, memory corruption, and process termination cross thread boundaries.

“Thread” can name a language abstraction or a kernel entity. In Java, a platform thread wraps an OS thread for its lifetime. POSIX `pthread_create` creates a thread in the calling process under POSIX-defined sharing and lifecycle rules. Linux's NPTL implements POSIX threads on kernel scheduling primitives. Some older or specialized runtimes use many-to-one or many-to-many user/kernel mappings. Never infer the mapping only from an API type name.

A **task** is work, not necessarily an execution context. It can be a function plus arguments, a node in a dependency graph, a future-producing operation, or an OpenMP explicit task with a data environment. Creating a task normally makes it eligible or queued; a scheduler later assigns it to a worker. It may execute immediately on the creating thread, on another thread, in pieces around suspension points, or not at all if cancelled before start.

Task identity supports result and lifecycle structure. A task can have a parent, children, deadline, cancellation state, dependencies, priority, and completion handle. Those features do not imply stack ownership or isolation. Two tasks on one worker can share every process global. One task can run on several workers at different times when untied or resumable. A thread can execute many tasks sequentially.

A **fiber** traditionally gives a user-space scheduler a resumable, usually stackful context. Switching fibers saves one context and restores another without asking the kernel scheduler to switch threads. Cooperative suspension occurs at yield, await, or runtime-integrated blocking points. A fiber that never yields can monopolize its hosting thread. A blocking system or foreign call unknown to the runtime can block that thread and every fiber awaiting it.

Stackful contexts preserve ordinary call stacks across suspension, making blocking-style code convenient. They need stack storage, growth/overflow policy, unwinding, debugging, and foreign-call integration. Stackless coroutines compile suspension points into state machines and store only live state, but suspension usually must be explicit in compatible functions. The terms overlap in libraries; the properties matter more than the label.

Java **virtual threads** are lightweight `java.lang.Thread` instances scheduled by the Java runtime onto carrier platform threads. At supported blocking I/O, a virtual thread can unmount so the carrier runs another. Native or foreign operations can pin it, hindering scalability. Oracle explicitly distinguishes throughput scale from per-operation speed: virtual threads are not faster CPU threads.

Go **goroutines** are language-level concurrent control flows in one address space. The Go specification defines starting and termination behavior while leaving much scheduling implementation freedom. Implementations multiplex goroutines over OS threads, grow stacks, and integrate many blocking operations. A goroutine is not a process and does not isolate heap mutations. It should not be called an OS thread merely because the specification uses “thread of control.”

OpenMP makes the task/thread distinction explicit. Encountering a task construct generates an explicit task with a data environment. The encountering thread may execute it immediately or defer it; a team thread may later run it. Dependencies constrain eligibility, and scheduling points permit switching. A conforming program cannot rely on an unspecified convenient scheduling order.

Runtime-managed contexts improve the cost of *waiting concurrency* by multiplexing. They do not create processor capacity. If 100,000 virtual threads all become CPU-ready, available carrier threads and processors remain the bottleneck. Fairness, queueing, memory, garbage collection, and downstream limits determine behavior. CPU-bound work still needs bounded parallelism matched to resources.

Blocking must be classified at the actual boundary. A kernel thread blocked in a system call is unavailable until wakeup. A virtual thread or coroutine awaiting runtime-integrated nonblocking I/O may release its carrier. A monitor, native call, foreign library, filesystem path, DNS resolver, or lock may behave differently. Documentation and measurement must confirm the path; `async` syntax or a lightweight identity is insufficient evidence.

Thread-local storage attaches data to a platform or kernel thread. It works for state whose ownership truly is that thread, such as runtime bookkeeping. It is unsafe for request or task context when logical work can migrate or a worker processes unrelated tasks sequentially. Use task-local/context propagation with defined child inheritance and cleanup, or pass values explicitly. Even task-local state can become hidden coupling and memory retention.

Process-local globals are also shared by all in-process contexts. Moving from platform threads to fibers does not remove synchronization obligations. Cooperative single-thread execution can prevent simultaneous access only while the runtime remains on one worker and callbacks never interleave at invariant-breaking suspension points. Scaling to multiple carriers or yielding mid-operation exposes the same shared-state design.

Creation and termination must have owners. A process needs reaping/restart and IPC cleanup. A thread needs join or deliberate detachment and resource reclamation. A task needs completion observation and child policy. A fiber needs a scheduler owner, cancellation/unwinding behavior, and stack cleanup. “Fire and forget” is a lifecycle decision with failure and shutdown consequences, not absence of responsibility.

Cancellation is usually a request, not instantaneous erasure. Work might not have started, might be suspended, might hold a lock, or might already have committed an external effect. The mechanism must define cancellation points, cleanup handlers, child propagation, result state, deadline ownership, and idempotency/reconciliation for irreversible operations. Killing a process is stronger but can still leave durable external effects.

The deterministic model below separates three logical task identities from two worker identities. Task A resumes on a different worker, illustrating why worker-local state cannot represent task identity.

<!-- bijux-verify: {"id":"task-worker-mapping","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"task_count=3\nworker_count=2\nsegments=5\nA_workers=0,1\nA_migrated=True\n","stderr":""}} -->
```python
schedule = [
    ("A", 0),
    ("B", 1),
    ("C", 0),
    ("A", 1),
    ("B", 1),
]

tasks = sorted({task for task, worker in schedule})
workers = sorted({worker for task, worker in schedule})
a_workers = sorted({worker for task, worker in schedule if task == "A"})

print(f"task_count={len(tasks)}")
print(f"worker_count={len(workers)}")
print(f"segments={len(schedule)}")
print("A_workers=" + ",".join(str(worker) for worker in a_workers))
print(f"A_migrated={len(a_workers) > 1}")
```

Execution proves only the arithmetic and identities of this encoded schedule. It does not create threads, demonstrate real migration, measure scheduler cost, establish fairness, model memory visibility or cancellation, validate an actual runtime, or justify a production concurrency design.

Mechanism choice follows the boundary. Use processes when address-space/fault separation, privilege separation, independent deployment, or incompatible runtimes justify IPC cost. Use platform/kernel threads for bounded parallel CPU execution or blocking integration where their resource cost is acceptable. Use tasks to expose work/dependencies independently of workers. Use virtual threads, goroutines, fibers, or coroutines for large waiting populations only after confirming blocking integration, context propagation, admission, and diagnostics.

## Definitions and Notation

Let $P$ be processes, $K$ kernel threads, $R$ runtime-managed contexts, $T$ tasks, and $U$ processors. Ownership functions are

$$
owner_K:K\to P,\qquad owner_R:R\to P,\qquad owner_T:T\to P.
$$

At time $\tau$, placement is partial:

$$
carrier_\tau:R\rightharpoonup K,\qquad
work_\tau:T\rightharpoonup R,\qquad
cpu_\tau:K\rightharpoonup U.
$$

Undefined means queued, suspended, blocked, completed, or otherwise not placed; the lifecycle state resolves which. Multiplexing permits many $R$ over fewer $K$ across time. Physical parallelism at $\tau$ is bounded by distinct processors in the range of $cpu_\tau$, not by $|T|$ or $|R|$.

Let $Addr(p)$ be a process address-space domain and $Resources(p)$ its governed resource set. Threads $k_1,k_2$ with the same owner normally access shared $Addr(p)$, subject to language/OS permissions and memory semantics. Cross-process access requires a named IPC or shared-memory relation; different $p$ alone does not prove absence of shared resources.

A task lifecycle can be modeled

$$
created\to queued\to running\leftrightarrow suspended\to
\{completed,failed,cancelled\}.
$$

Actual runtimes may merge or add states. Every terminal outcome must be observable by the owner, and every transition must preserve resource and cleanup invariants.

## Mechanisms, Invariants, or Proof Structure

**Cardinality independence.** A queue can contain 10,000 tasks while four workers exist; one task can execute inline with no new worker; one virtual context can migrate between carriers; one kernel thread can execute many tasks. Therefore no equality among $|T|,|R|,|K|,|U|$ follows without a runtime contract.

**Sharing follows ownership, not scheduling style.** If two execution contexts belong to one process and access one reachable mutable location, they require synchronization under possible overlap. Cooperative scheduling removes some preemption points but does not establish ownership or protect invariants across explicit suspension.

**Task-local continuity.** Suppose task $t$ runs first where $work_{\tau_1}(t)=r_1$ and later where $work_{\tau_2}(t)=r_2$, with different carriers. State indexed by carrier $k$ can change between segments; state indexed by $t$ follows logical identity. Thus worker-thread locals cannot implement migrating task context without runtime propagation.

**Blocking amplification.** If $n$ logical contexts share $m$ carriers and $b$ carriers are blocked or pinned, at most $m-b$ carriers remain for runnable contexts. Lightweight logical count does not prevent starvation when $b=m$.

**Isolation qualification.** Separate address spaces prevent ordinary direct pointer access, but shared memory, inherited descriptors, common credentials, files, quotas, kernel bugs, and external services remain channels. Process isolation is one control in a threat/failure model, not a proof of independence.

**Lifecycle closure.** For every created unit, exactly one ownership policy accounts for its terminal state and resource reclamation. Detachment transfers responsibility to a durable supervisor; it does not delete the obligation.

**Cancellation safety.** Cancellation before an external commit and cancellation after it are different states. Correct cleanup must not assume rollback. The protocol records whether work was prevented, interrupted, completed, or left uncertain and reconciles ambiguous effects.

**Performance evidence.** Compare mechanisms with the same correctness oracle and workload, recording runnable/waiting mix, stacks and heap, queue depth, carrier utilization, context switches, pinning/blocking, throughput, tail latency, cancellations, and overload. A count of created contexts is not scalability evidence.

## Alternatives and Trade-Offs

**Processes versus in-process contexts.** Processes improve address-space, fault, privilege, and deployment separation. IPC, startup, memory, serialization, coordination, and cross-process diagnosis cost more. Threads/tasks communicate cheaply but share failure and memory hazards.

**Platform threads versus virtual/lightweight contexts.** Platform threads integrate naturally with OS blocking and native tools but are finite and relatively costly. Lightweight contexts scale waiting populations when runtime suspension works, while adding scheduler, pinning, task-local, dump, and memory-retention concerns.

**Tasks versus dedicated threads.** Tasks expose logical work and let a scheduler bound/reuse workers. Dedicated threads provide stable thread affinity and thread-local semantics but can waste stacks and scheduler capacity. Affinity-sensitive native/UI work may require the latter.

**Stackful fibers versus stackless coroutines.** Stackful suspension preserves ordinary call structure and supports legacy blocking style when integrated. Stackless state machines make suspension visible and store selected state compactly, but require compatible call chains. Debugger and cancellation quality can outweigh syntax.

**Preemptive versus cooperative scheduling.** Preemption improves responsiveness against non-yielding work but permits interruption across many points and requires synchronization. Cooperation makes suspension points visible but lets one task monopolize a worker and exposes invariants across awaits.

**Thread-local versus explicit/task-local context.** Thread-local access is efficient for true worker state. Explicit values are easiest to reason about. Task-local context follows logical work but can propagate unexpectedly, hide dependencies, and retain large graphs.

## Failure Modes and Misconceptions

- **“A process is a program.”** Several processes can run one image; a process can replace its image.
- **“Processes share nothing.”** Files, memory mappings, credentials, namespaces, quotas, and external systems can be shared.
- **“A thread is a CPU.”** A runnable thread awaits scheduler placement and can migrate between processors.
- **“A task is a lightweight thread.”** A task may have no stack and may execute inline, migrate, or never start.
- **“Fiber, coroutine, goroutine, and virtual thread are synonyms.”** Their stack, scheduling, blocking, and specification contracts differ.
- **“Cooperative means race-free.”** Suspension can interleave invariants, and multiple carriers can run simultaneously.
- **“Blocking a lightweight thread is always cheap.”** Unsupported blocking or pinning consumes the carrier.
- **“Thread-local means request-local.”** Worker reuse and task migration violate that assumption.
- **“Millions of contexts imply millions of parallel operations.”** processors and downstream capacity remain bounded.
- **“Cancellation stops the effect.”** It may only change a handle while external work continues or has committed.
- **“A separate process is a sandbox.”** Security requires explicit privilege, namespace, syscall, IPC, secret, and resource controls.
- **“More workers prove more throughput.”** Coordination, memory, queues, contention, and correctness determine results.

## Worked Examples

### Example 1

**Question:** Two services run the same executable. Are they one process?

**Reasoning:** Each launch can create a distinct process identity, address space, resource table, and lifecycle even with identical code bytes. They may still share files, sockets, credentials, or mapped memory.

**Conclusion:** Program image equality does not merge process identity or eliminate shared-resource analysis.

### Example 2

**Question:** Four threads increment one heap counter. What do they share?

**Reasoning:** Their stacks and register states are distinct, but the heap location belongs to the common process. Read-modify-write is not automatically atomic. Thread creation supplies execution contexts, not synchronization.

**Conclusion:** Shared address space makes communication available and correctness obligations immediate.

### Example 3

**Question:** A pool has two threads and accepts 100 tasks. How many can execute simultaneously?

**Reasoning:** At most two task segments run on those workers at one instant, and fewer if workers block. The other tasks are queued or terminal. Task count expresses outstanding work, not processor parallelism.

**Conclusion:** Worker and task cardinalities must be measured separately.

### Example 4

**Question:** Task A suspends on I/O and resumes on another worker. Where should its trace ID live?

**Reasoning:** A raw thread-local remains on the first worker and may be seen by unrelated work; the second worker lacks it. Pass the trace context explicitly or use runtime task-context propagation with cleanup and child rules.

**Conclusion:** Logical context follows task identity, not incidental carrier identity.

### Example 5

**Question:** Why can one fiber freeze every fiber on its thread?

**Reasoning:** Cooperative scheduling needs a yield or integrated await. A long CPU loop or unknown blocking call never returns control to the user scheduler. Peers remain runnable but cannot be selected.

**Conclusion:** Cheap switching is irrelevant when the current context does not reach a scheduling point.

### Example 6

**Question:** Does a Java virtual thread make a CPU-intensive hash faster?

**Reasoning:** It still executes on a carrier and processor. Virtualization improves the number of mostly waiting flows; it neither creates cores nor accelerates the hash. Many CPU-ready virtual threads add queueing.

**Conclusion:** Lightweight concurrency targets scale, not per-operation CPU speed.

### Example 7

**Question:** May an OpenMP task assume the creating thread will execute it next?

**Reasoning:** The implementation may execute immediately or defer it to a team thread, subject to dependencies and scheduling points. Code depending on a particular unspecified order is nonconforming and can also misuse thread-local state.

**Conclusion:** Task correctness must survive every permitted assignment and order.

### Example 8

**Question:** Is `fork` from a multithreaded POSIX process equivalent to cloning all threads?

**Reasoning:** POSIX specifies a new process containing a replica of the calling thread, not every peer thread; inherited synchronization state and the restricted operations safe before `exec` make this a hazardous boundary. Use the exact platform spawn/fork/exec contract.

**Conclusion:** Process creation from multithreaded state has semantics that a “copy the process” slogan hides.

### Example 9

**Question:** A medical-device controller moves its telemetry parser into another process. Is the system now safe?

**Reasoning:** The boundary can contain some crashes and memory faults, but safety still depends on authenticated IPC, resource limits, deadlines, stale/replayed data, unit semantics, restart state, command authority, device fail-safe behavior, and system hazards. Review requires named clinicians, biomedical/device engineers, safety and security engineers, human-factors/accessibility specialists, regulators, operators, vendors, affected users, and independent clinical/technical assurance. No external review is claimed.

**Conclusion:** Process separation is a mechanism and evidence item, not a medical safety case.

### Example 10

**Question:** When should a blocking request server choose processes, platform threads, or virtual contexts?

**Reasoning:** Privilege/fault separation may justify worker processes. A bounded number of blocking native calls may fit platform threads. A large population waiting in runtime-integrated I/O may fit virtual contexts. CPU work, downstream caps, context propagation, cancellation, diagnostics, and measurements can require a hybrid.

**Conclusion:** Choose from isolation and workload properties, not one universal hierarchy.

## Cross-Program Connections

[Operating Systems](../../22-operating-systems/ROADMAP.md) owns process creation, kernel scheduling, protection, virtual memory, and thread implementation. [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns native calls, resource lifetime, ABI, and unsafe memory consequences.

[Network Engineering](../../24-network-engineering/ROADMAP.md) supplies sockets and backpressure constraints that concurrency cannot remove. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) adds node, message, partial-failure, and remote-lifecycle boundaries beyond processes.

[Security Engineering](../../25-security-engineering/ROADMAP.md) evaluates process privilege, sandboxing, IPC authentication, denial of service, and context leakage. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) supplies workload isolation, quotas, observability, and runtime standards.

[Testing & Quality Engineering](../../13-software-engineering-testing-and-quality-engineering/ROADMAP.md) explores scheduler, cancellation, migration, blocking, and overload cases. [Software Reliability Engineering](../../14-software-engineering-software-delivery-and-reliability-engineering/ROADMAP.md) governs supervision, shutdown, incident evidence, and tail latency.

## References

- IEEE and The Open Group, [*POSIX.1-2024 System Interfaces*, `2 General Information and pthread/process interfaces](https://pubs.opengroup.org/onlinepubs/9799919799/functions/V2_chap02.html), Issue 8, 2024. Normative process, thread, scheduling, signal, fork, exec, and synchronization rules; checked 2026-08-29.
- Michael Kerrisk and Linux man-pages contributors, [*NPTL(7): Native POSIX Threads Library*](https://man7.org/linux/man-pages/man7/nptl.7.html), Linux man-pages 6.16, 2025. Linux POSIX-thread implementation characteristics and limits; checked 2026-08-29.
- Oracle, [*Java SE 26: Virtual Threads*](https://docs.oracle.com/en/java/javase/26/core/virtual-threads.html), 2026. Official platform/virtual thread, carrier, mounting, blocking, pinning, scale, and observability guidance; checked 2026-08-29.
- Go Project, [*The Go Programming Language Specification*, Go statements](https://go.dev/ref/spec#Go_statements), language version 1.27, 2026. Normative goroutine initiation, parameter evaluation, independent execution, and termination; checked 2026-08-29.
- OpenMP Architecture Review Board, [*OpenMP API Specification 5.2*, Tasking Terminology and `12](https://www.openmp.org/spec-html/5.2/openmpch12.html), 2021. Explicit tasks, data environments, dependencies, scheduling points, thread assignment, and synchronization.
- Atul Adya, Jon Howell, Marvin Theimer, William J. Bolosky, and John R. Douceur, [“Cooperative Task Management without Manual Stack Management”](https://www.usenix.org/conference/2002-usenix-annual-technical-conference/cooperative-task-management-without-manual-stack), *USENIX ATC 2002*. Stack management and cooperative event/task programming.
- Thomas E. Anderson, Brian N. Bershad, Edward D. Lazowska, and Henry M. Levy, [“Scheduler Activations”](https://doi.org/10.1145/146941.146944), *ACM Transactions on Computer Systems* 10(1), 1992, pp. 53–79. Kernel/user-level thread scheduling interface and many-to-many motivation.
- Andrew S. Tanenbaum and Herbert Bos, [*Modern Operating Systems*, 5th ed.](https://www.pearson.com/en-us/subject-catalog/p/modern-operating-systems/P200000011812), Pearson, 2022. Processes, threads, scheduling, IPC, and protection foundations.

## Exercises

### Exercise 1

For process, kernel/platform thread, task, and fiber, identify owned resources, private execution state, shared state, scheduler, blocking behavior, creation/termination owner, and one claim that the mechanism does not establish.

### Exercise 2

Given 200 tasks, 50 runtime contexts, 8 carrier threads, and 4 processors, state tight instantaneous upper bounds on task segments running, kernel threads on-CPU, and CPU-parallel segments. Then analyze the case where all eight carriers are pinned.

### Exercise 3

A request task starts on worker 1, suspends, resumes on worker 4, spawns two children, and is cancelled after one child commits a database write. Design context propagation, ownership, cancellation, cleanup, and reconciliation; diagnose every incorrect thread-local assumption.

### Exercise 4

Compare a four-process/one-thread-per-process server, one process with 32 platform threads, and one process with virtual contexts on eight carriers for 10,000 mostly waiting requests plus bounded CPU validation. Define an experiment and correctness oracle rather than choosing from labels.

### Exercise 5

Design a high-integrity medical-device gateway that uses process isolation, threads, and tasks. State trust/fault boundaries, IPC, task lifecycle, blocking/admission policy, shutdown/restart behavior, hazards, evidence, and named human review required before use.

## Answers to the Exercises

### Answer 1

A process owns an OS resource/protection context such as address space, handles, credentials, and accounting; it contains threads and is scheduled indirectly through them. Its boundary does not prove sandboxing or independence from shared resources. A kernel/platform thread owns register state, stack, scheduler state, and thread-specific data while sharing process memory/resources; the OS schedules it, and blocking generally makes that thread unavailable. It does not create synchronization or a CPU.

A task owns logical work, dependencies, result/lifecycle, and perhaps captured data; a runtime schedules it on workers, where it can queue, execute inline, suspend, migrate, or be cancelled. It does not inherently own a stack, thread, or isolation boundary. A fiber owns a resumable user-space context, commonly a stack, and a runtime scheduler cooperatively runs it on a host thread. Unknown blocking can immobilize the host; fiber identity does not make shared memory safe.

### Answer 2

At most eight task/runtime segments can occupy eight carrier threads at once, assuming one segment per carrier. At most four kernel threads can be on four processors simultaneously, so at most four task segments are physically CPU-parallel. The 200 tasks and 50 runtime contexts enlarge eligible/queued populations but not those instantaneous bounds.

If all eight carriers are pinned or blocked, zero carriers remain for other runnable runtime contexts, even though four processors may be idle or execute unrelated processes. The runtime could create compensation carriers only if its documented policy permits it; correctness and capacity planning cannot assume that. Measure pinning reason, duration, queues, carrier creation, CPU use, and tail latency.

### Answer 3

Represent request ID, trace span, authenticated principal, deadline, locale, and policy snapshot as explicit immutable context or runtime task-local data with specified child inheritance. Never use worker-1 local storage: after migration worker 4 lacks it, while worker 1 may leak it to another task. Worker-4 locals likewise cannot identify the request. Children receive derived spans, the remaining deadline, and least authority.

The parent owns both children and observes terminal outcomes. Cancellation stops new work, signals both children, and awaits bounded cleanup. The committed write cannot be erased by cancelling its handle. Record an idempotency key and commit result, then run a domain reconciliation or compensating workflow if policy permits; the other child must report prevented, cancelled, completed, or uncertain. Release locks, permits, connections, buffers, and context bindings exactly once. Audit parent/child/task/worker transitions without making worker identity the business key.

### Answer 4

Use identical validated requests and response oracle: status, canonical payload, durable effects, exactly-once/idempotency policy, deadlines, cancellation, cleanup, and overload behavior. Workloads vary connection count, wait/CPU ratio, native blocking, downstream capacity, burstiness, request sizes, failures, cancellations, and steady-state duration. Pin process/thread/runtime versions and hardware.

Measure throughput; queue, median and tail latency; CPU; RSS/stack/heap; context switches; GC; worker/carrier utilization; blocked/pinned time; IPC; downstream concurrency; errors; cancellations; and recovery. Four processes may isolate faults/privileges and use four cores but add IPC/memory. Thirty-two platform threads tolerate blocking but bound in-flight execution and consume thread resources. Virtual contexts can represent 10,000 waits compactly when operations unmount, yet eight carriers bound CPU execution and pinning can collapse capacity. A hybrid may win; only correct results under measured load support a decision.

### Answer 5

Place network-facing parsing in a least-privilege process separated from the device-control process. Authenticate and version IPC messages; use bounded queues, explicit schemas, sequence numbers, freshness/deadline, replay protection, checksums/signatures as required, unit-bearing values, and fail-closed decoding. Device authority exists only in the control process. Separate safety-monitor and audit paths where the hazard analysis requires independent behavior; process boundaries share no unreviewed mutable memory.

Within each process, use bounded threads for blocking/native device operations and tasks for owned request workflows. Every task has parent, deadline, cancellation result, idempotency key, resource permit, and terminal audit. CPU work is bounded; unsupported blocking never runs on an event/fiber carrier. Shutdown stops admission, drives devices to a defined safe state, resolves or records uncertain commands, drains within a deadline, persists restart state, and terminates. Restart authenticates device/session state and never blindly replays an unacknowledged command.

Hazards include malformed or replayed telemetry, stale state, unit/decimal confusion, lost/duplicate/reordered commands, resource exhaustion, deadlock, thread/task context leakage, clock failure, process crash loops, IPC partition, compromised process, device disagreement, unsafe cancellation, and incomplete shutdown. Verification includes fault injection, scheduler exploration, load/overload, race and memory tools, IPC fuzzing, timing bounds, recovery, accessibility/localization, hardware-in-loop under governed safety controls, and independent trace review.

Named review includes clinicians and device users, biomedical/device and integration engineers, functional-safety and cybersecurity engineers, human-factors/accessibility/localization specialists, quality/regulatory and legal/privacy staff, vendor representatives, site operations/training, incident responders, and independent clinical/technical assurance. Process isolation and automated tests do not establish device safety, clinical correctness, regulatory acceptance, or deployment authorization; no external review is claimed.
