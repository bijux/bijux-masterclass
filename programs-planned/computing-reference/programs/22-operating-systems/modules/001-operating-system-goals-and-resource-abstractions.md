---
module_id: OS-001
program: Operating Systems
level: 1
module_number: 1
title: Operating-System Goals and Resource Abstractions
status: complete
last_verified: 2026-08-28
---

# Operating-System Goals and Resource Abstractions

## One-Page Review

### Governing question

How can one machine safely and efficiently support many programs while presenting each with usable abstractions instead of raw hardware?

### Essential definitions

- An **operating system** is the software layer that provides execution services and governs shared hardware and software resources.
- A **kernel** is the privileged core that enforces mechanisms and boundaries; it is not necessarily the entire operating system.
- A **resource** is a finite or controlled capability such as processor time, memory, storage, a device, or a communication endpoint.
- An **abstraction** presents a stable interface and semantics while hiding selected implementation detail.
- **Multiplexing** shares a resource across clients in time, space, or both.
- **Protection** constrains which subjects may perform which operations on which objects.
- **Policy** chooses among allowed actions; **mechanism** makes those actions possible and enforceable.

### Central model, mechanism, or theorem

For each resource, identify:

`physical resource → kernel mechanism → named abstraction → allocation policy → observable guarantee`.

A processor becomes execution contexts scheduled over time; physical memory supports protected address spaces; storage blocks support files and durable namespaces; network devices support sockets and protocol endpoints. Abstractions are contracts, not claims that physical limits disappear.

### Critical invariants

- One client cannot access another's resource without an authorized sharing path.
- Every allocated resource has an owner, lifetime, accounting rule, and reclamation path.
- Virtual names resolve within a declared namespace and authority.
- Multiplexing preserves progress and isolation assumptions stated by policy.
- Failure of one component is contained only within explicitly engineered boundaries.
- Resource accounting measures the resource actually constrained.

### Common failures

Common errors include equating the OS with a GUI, treating abstraction as cost-free, confusing concurrency with simultaneous execution, assuming fairness means equal allocation, using a PID or descriptor as globally stable identity, believing a process owns physical memory directly, and calling a container a hardware virtual machine.

### Compact example

Two processes may both use descriptor `3`, yet each descriptor table can map that integer to a different kernel object. The small number is a process-local name, not the resource itself. Sharing occurs only when creation, inheritance, or transfer rules arrange a common underlying reference.

### Connections

[OS-002](../ROADMAP.md) develops privilege and protection rings. Hardware support connects to [Computer Architecture](../../23-computer-architecture/ROADMAP.md); user-space interfaces connect to [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md); isolation connects to [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

Without an operating system, each program would need device-specific control, physical-memory discipline, and its own conventions for sharing and protection. With no enforcement boundary, one faulty program could overwrite another or monopolize a device. The OS turns hardware into a managed environment: programs request services through interfaces while privileged mechanisms retain authority over resources.

The goal is not merely convenience. Operating systems balance protection, utilization, responsiveness, throughput, fairness, predictability, portability, recoverability, observability, and evolvability. These goals conflict. A policy optimized for aggregate throughput can harm interactive latency; aggressive caching uses memory to reduce I/O but can increase reclaim latency.

## Why This Matters

Systems bugs often come from confusing a name with an object or a promise with a mechanism. A process identifier can be reused. A virtual address is not a physical address. A successful buffered write is not necessarily stable storage. A thread can share an address space while retaining its own execution state. Debugging improves when every observation is traced through the relevant abstraction and owner.

OSTEP organizes operating systems around virtualization, concurrency, and persistence ([official version 1.10 site](https://pages.cs.wisc.edu/~remzi/OSTEP/)). This chapter adds protection and resource governance as cross-cutting obligations. Later chapters explain how concrete kernels implement each one.

## Prerequisites and Retrieval

You should understand programs, functions, memory, processors, persistent storage, and basic concurrency. Recall that an interface specifies observable operations, an implementation realizes them, an invariant must survive every allowed transition, and finite resources require an admission or allocation policy.

## Learning Objectives

After completing this module, you should be able to:

- distinguish operating system, kernel, runtime, firmware, and application;
- identify physical resources and the abstractions built over them;
- explain time and space multiplexing;
- separate mechanism, policy, and interface;
- analyze ownership, naming, lifetime, accounting, and reclamation;
- compare isolation, sharing, efficiency, fairness, and predictability goals;
- identify abstraction leaks and failure boundaries;
- construct evidence for a resource-management claim without overgeneralizing it.

## Core Exposition

The OS occupies a boundary between programs and machine resources, but the boundary varies by design. Firmware initializes hardware and may remain available through runtime services. A hypervisor can allocate hardware among guest kernels. Language runtimes manage memory and concurrency above the kernel. User-space servers may implement substantial OS services. “Kernel” therefore names an authority boundary, while “operating system” includes the larger execution environment and interfaces.

An abstraction deliberately omits detail. A **process** packages an execution context, address-space view, credentials, resource references, and lifecycle state. A **virtual address space** gives each process a protected naming scheme for memory. A **file** provides a byte or record-oriented persistent object independent of raw device sectors. A **socket** names a communication endpoint independent of direct device programming. None creates infinite resources: allocation can fail, operations can block, and physical limits remain observable through performance and quotas.

Multiplexing occurs over time and space. A processor can run one context, then another; a storage device interleaves requests. Memory can be partitioned among address spaces. A filesystem divides capacity among files while sharing metadata and caches. Statistical multiplexing exploits clients not peaking simultaneously, but overload still requires queueing, rejection, degradation, or reclamation.

Protection requires subjects, objects, operations, and authority. Isolation is not the same as secrecy: separate address spaces prevent ordinary direct access, but timing, shared caches, files, or permitted IPC can still convey information. Saltzer and Schroeder's [protection principles](https://doi.org/10.1109/PROC.1975.9939) emphasize least privilege, complete mediation, and small understandable mechanisms; applying them requires a threat model and verified implementation.

Mechanism and policy should be distinguished even when one implementation couples them. A timer interrupt and context-switch mechanism permit preemption; a scheduler policy chooses the next runnable context. Page tables permit mappings and protection; memory policy chooses placement and reclamation. Descriptor tables provide process-local references; creation and transfer policy determines sharing.

Resource management has a recurring lifecycle:

1. discover or create the resource;
2. authenticate the requester and authorize an operation;
3. admit and allocate under policy;
4. name the resource in a namespace;
5. use, share, wait, or revoke;
6. account for consumption and failures;
7. release or reclaim every reference;
8. preserve or recover state when persistence is promised.

An unowned transition is a common defect. If a process exits, the kernel reclaims volatile resources, but persistent files remain by design. If the parent never collects child exit state, a zombie record can remain. If a descriptor is inherited unexpectedly, an object can outlive the process thought to own it. Lifetime follows references and policy, not human intuition.

## Definitions and Notation

Let resource capacity be `C`, clients be `p₁...pₙ`, and allocation to client `i` be `aᵢ≥0`. A feasible allocation satisfies `Σaᵢ≤C`. A policy may add reservations, priorities, deadlines, or weights. Feasibility alone proves neither fairness nor useful progress.

- **Virtualization:** constructs a logical resource interface over physical or lower-level resources.
- **Concurrency:** multiple activities have overlapping lifetimes; they need not execute simultaneously.
- **Parallelism:** activities execute simultaneously on distinct execution resources.
- **Namespace:** context that maps names to objects.
- **Handle:** a reference interpreted by an authority, often scoped to a process or table.
- **Isolation:** limits interference or observation across a boundary.
- **Accounting:** attributes resource consumption to an owner or group.
- **Reclamation:** recovers a resource when ownership ends or pressure policy requires it.

## Mechanisms, Invariants, or Proof Structure

For a proposed abstraction, review five obligations:

1. **Safety:** forbidden access or corruption cannot occur under assumptions.
2. **Liveness:** entitled work can eventually progress under the stated load and policy.
3. **Accounting:** use is charged to the correct principal.
4. **Recovery:** failures leave a defined state and reclamation path.
5. **Performance:** overhead and contention meet a measured objective.

The following executable model illustrates local names resolving to kernel-owned objects. It checks namespace separation and intentional sharing; it is not a kernel implementation.

<!-- bijux-verify: {"id":"process-local-resource-names","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"p1: terminal\np2: log-file\nshared: event-channel event-channel\nisolated: denied\n","stderr":""}} -->
```python
tables = {
    "p1": {3: "terminal", 4: "event-channel"},
    "p2": {3: "log-file", 8: "event-channel"},
}

def resolve(process, descriptor):
    try:
        return tables[process][descriptor]
    except KeyError:
        return "denied"

print("p1:", resolve("p1", 3))
print("p2:", resolve("p2", 3))
print("shared:", resolve("p1", 4), resolve("p2", 8))
print("isolated:", resolve("p2", 4))
```

Passing these examples does not prove complete mediation, safe concurrency, reference counting, or resistance to forged identifiers. Those require mechanisms and adversarial evidence at the real authority boundary.

## Alternatives and Trade-Offs

**Rich versus minimal interfaces.** Rich interfaces can reduce application work. Small composable interfaces reduce trusted complexity and often age better, but composition can add crossings and coordination.

**Efficiency versus isolation.** Sharing pages, caches, and kernel paths saves resources; it also creates contention and side channels. Copying improves separation but costs time and space.

**Fairness versus throughput.** Equal shares may waste capacity or ignore priorities. Work-conserving weighted policies can improve utilization while requiring explicit starvation bounds.

**Transparency versus control.** Automatic caching and migration simplify programs. Explicit controls help specialized workloads but expose mechanism and reduce portability.

**General-purpose versus specialized systems.** A general OS supports diverse workloads and hardware. Embedded, real-time, unikernel, or library-OS designs can narrow goals for predictability, size, or control.

## Failure Modes and Misconceptions

1. The kernel is the whole operating system. False: system services, libraries, and tools can be part of the OS environment.
2. Virtual means unlimited. False: logical resources still consume finite capacity.
3. Concurrency means parallel execution. False: lifetimes can overlap on one processor.
4. A resource name is globally meaningful. False: names are interpreted in namespaces and can be reused.
5. Isolation forbids all communication. False: authorized sharing and IPC are deliberate paths.
6. Equal allocation is always fair. False: work, weights, deadlines, and entitlements differ.
7. Abstractions eliminate hardware behavior. False: page faults, caches, and device latency leak through cost.
8. Cleanup is solely an application duty. False: the OS reclaims some resources but persistence and external effects outlive processes.
9. Protection is only access-control configuration. False: mediation, privilege, implementation, and side channels matter.
10. High utilization proves good service. False: latency, progress, isolation, and recoverability can fail at full utilization.

## Worked Examples

### Example 1

**Question:** Is a shell an operating system?

**Reasoning:** It is a user interface and program launcher using OS services. It does not normally own privileged CPU, memory, and device enforcement.

**Conclusion:** An OS environment can include a shell without making the shell its kernel.

### Example 2

**Question:** How is one CPU virtualized?

**Reasoning:** Execution contexts retain state while policy selects which runs; timer and transition mechanisms recover control. Each process experiences progress over time.

**Conclusion:** Time multiplexing creates the execution abstraction without creating more physical CPU time.

### Example 3

**Question:** Why can two processes use the same virtual address?

**Reasoning:** Each address is resolved through its address-space context to potentially different physical memory and permissions.

**Conclusion:** A virtual address is a scoped name, not a machine-wide physical location.

### Example 4

**Question:** What does a file abstract?

**Reasoning:** It supplies naming, contents, metadata, permissions, and operations above blocks and devices. Persistence after a crash depends on filesystem and synchronization semantics.

**Conclusion:** The interface hides layout but not every failure or durability boundary.

### Example 5

**Question:** Is descriptor `3` the same object in every process?

**Reasoning:** Descriptor numbers index process-local tables. Different entries may reference different objects; distinct numbers may intentionally share one object.

**Conclusion:** Resolve names through their owning namespace.

### Example 6

**Question:** Does a 50% CPU limit mean every second contains 500 ms of execution?

**Reasoning:** Enforcement may occur over windows or quotas, and runnable competition matters. Bursts and throttling can coexist with a long-run share.

**Conclusion:** Resource guarantees require time windows and policy semantics.

### Example 7

**Question:** Why can memory allocation succeed before physical memory is used?

**Reasoning:** Virtual mappings, demand allocation, overcommit, and lazy initialization may defer physical commitment.

**Conclusion:** Allocation APIs and physical-resource commitment are different transitions.

### Example 8

**Question:** Does process exit remove its files?

**Reasoning:** The kernel reclaims process-owned volatile state and closes references, but named persistent objects follow filesystem lifetime rules.

**Conclusion:** Reclamation depends on resource class and remaining references.

### Example 9

**Question:** Is a container a separate kernel?

**Reasoning:** Common OS containers isolate namespaces and resource accounting while sharing a host kernel. A virtual machine normally runs a guest kernel over virtual hardware.

**Conclusion:** Similar packaging can rest on different authority and failure boundaries.

### Example 10

**Question:** What evidence supports “the scheduler is fair”?

**Reasoning:** Define eligible clients, weights, observation interval, tolerated deviation, blocking, and overload. Measure delivered service and starvation under adversarial mixes.

**Conclusion:** Fairness is a quantified policy property, not a visual impression of activity.

## Cross-Program Connections

- **Computer Architecture:** privilege, interrupts, address translation, and atomic operations supply enforcement mechanisms.
- **Systems Programming:** applications encounter OS abstractions through APIs, errors, blocking, and resource lifetimes.
- **Security Engineering:** protection and least privilege govern authority over kernel objects.
- **Distributed Systems:** a single kernel's shared-memory and failure assumptions do not extend automatically across machines.
- **Cloud Platform Engineering:** virtual machines and containers compose OS resource and isolation mechanisms into tenant services.

## References

- Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau. [*Operating Systems: Three Easy Pieces*, version 1.10](https://pages.cs.wisc.edu/~remzi/OSTEP/). University of Wisconsin–Madison. Version record checked 2026-08-28.
- Abraham Silberschatz, Peter B. Galvin, and Greg Gagne. [*Operating System Concepts*, 10th ed.](https://uat.store.wiley.com/en-us/operating-system-concepts-10th-edition-p-9781119320913) Wiley, 2018, ISBN 9781119320913. Publisher record checked 2026-08-28.
- Russ Cox, Frans Kaashoek, and Robert Morris. [*xv6: a Simple, Unix-Like Teaching Operating System*](https://pdos.csail.mit.edu/6.S081/2020/xv6/book-riscv-rev1.pdf). MIT PDOS, RISC-V revision 1, 2020.
- Jerome H. Saltzer and Michael D. Schroeder. [“The Protection of Information in Computer Systems.”](https://doi.org/10.1109/PROC.1975.9939) *Proceedings of the IEEE* 63(9), 1975, pp. 1278–1308.
- Dennis M. Ritchie and Ken Thompson. [“The UNIX Time-Sharing System.”](https://doi.org/10.1145/361011.361061) *Communications of the ACM* 17(7), 1974, pp. 365–375.

## Exercises

### Exercise 1

For CPU, memory, storage, and networking, identify one physical resource, kernel mechanism, abstraction, policy choice, and observable guarantee.

### Exercise 2

Given capacity `C=12` CPU quanta and clients with weights `1,2,3`, derive proportional allocations. Explain rounding, idle clients, and why the calculation alone does not prove fairness.

### Exercise 3

Extend the descriptor-table model to represent explicit inheritance from a parent to a child. State safety and lifetime invariants and adversarial cases.

### Exercise 4

Compare a process, OS container, and virtual machine by kernel ownership, naming, resource accounting, isolation, failure scope, and overhead.

### Exercise 5

Design a resource contract for a multi-tenant image-processing host. Include admission, CPU and memory policy, storage lifetime, device access, observability, overload, reclamation, and falsifying evidence.

## Answers to the Exercises

### Answer 1

CPU: processor core, preemption/context switching, execution context, weighted scheduling, bounded service share. Memory: DRAM, translation/protection, virtual address space, placement/reclaim, inaccessible foreign mappings. Storage: block device, filesystem and cache, file, allocation/durability policy, named bytes preserved under stated synchronization and failures. Networking: interface queues, protocol stack and descriptor tables, socket, queueing/filtering policy, scoped delivery and error semantics. Each guarantee must name assumptions; the abstraction name alone proves none.

### Answer 2

Total weight is `6`, so ideal allocations are `12·(1/6)=2`, `12·(2/6)=4`, and `12·(3/6)=6` quanta. Nondivisible capacity needs a deterministic remainder rule or repeated scheduling whose long-run error is bounded. An idle client may donate unused capacity under a work-conserving policy, but reservation semantics could retain it. The arithmetic proves proportional targets only; fairness also requires eligibility, accounting accuracy, finite observation windows, bounded deviation, and evidence that no runnable client starves.

### Answer 3

On creation, copy only entries marked inheritable into the child's new table; inherited entries reference the same underlying objects while descriptor numbers remain table-local. Safety requires no unmarked capability to appear and resolution only within the caller's table. Lifetime requires an object remain live while any authorized reference exists and be reclaimed after the last reference under object policy. Test closed-on-create entries, number collisions, parent close after inheritance, child close before parent, forged descriptor numbers, repeated creation, and concurrent close/use. A Python map can model references but cannot prove kernel atomicity or authorization.

### Answer 4

A process uses one host kernel and receives an address space, credentials, handles, and lifecycle state. A typical OS container still shares the host kernel but adds namespace views and group accounting around one or more processes; a kernel flaw can cross tenants. A virtual machine presents virtual hardware and normally runs a guest kernel, adding a hypervisor boundary, more state, and different failure/management costs. None is absolutely isolated: devices, caches, hypervisor or host code, configuration, and shared services remain attack and contention surfaces.

### Answer 5

Admit a job only when authenticated tenant, declared input size, memory reservation, storage quota, and supported decoder pass validation. Allocate weighted CPU with a starvation bound, enforce a hard memory limit with explicit job failure rather than host-wide pressure, expose only required accelerator queues, and store inputs/results under tenant-scoped names with retention and deletion rules. Account CPU time, peak memory, I/O bytes, device time, queue delay, failures, and throttling. On overload, queue to a bounded limit then reject; on process exit or timeout, reclaim volatile resources and transition durable job state to retryable or failed. Falsify the contract with malicious images, burst load, memory exhaustion, device reset, process kill, stale references, quota races, and attempts to read another tenant's objects. Record tail latency, starvation, leakage, and cleanup—not merely throughput.
