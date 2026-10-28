---
module_id: OS-011
program: Operating Systems
level: 1
module_number: 11
title: Processes and Address Spaces
status: complete
last_verified: 2026-09-04
---

# Processes and Address Spaces

## One-Page Review

### Governing question

How does an operating system represent an executing protection domain whose threads share selected resources while memory mappings, identities, credentials, files, and lifecycle change concurrently?

### Essential definitions

- A **process** is a kernel-managed resource and protection context containing one or more execution threads plus references to an address space, files, credentials, namespaces, signals, accounting, and parentage.
- An **address space** is the set of virtual-address mappings and translation state visible to participating threads; it is not the same as the physical memory currently resident.
- A **virtual memory area (VMA)** is a contiguous virtual interval with common permissions, backing, and policy metadata.
- A **page table** translates virtual pages into physical frames or special nonpresent states and carries access-control and status bits interpreted by hardware and the kernel.
- **Copy-on-write (COW)** shares read-only physical backing until an attempted write creates a logically private copy.
- A **process identifier (PID)** is a namespace-scoped, reusable name; a stable process handle binds operations to one process lifetime.
- A **zombie** is a terminated process whose minimal exit identity and status remain until its parent or designated reaper collects them.

### Central model, mechanism, or theorem

Model a process as a graph of references rather than one monolithic object:

`process = threads + mm + files + credentials + signals + namespaces + limits + parentage`.

Creation decides which components are copied, shared, or newly constructed. Address translation is valid only when a virtual address lies in an authorized mapping and the current page-table state permits the access. Termination stops execution and releases most resources, while identity and exit status may persist for reaping. Correct lifecycle reasoning follows every shared reference independently.

### Critical invariants

- Each thread executes with a well-defined current address space, credentials, namespace view, register state, and kernel stack.
- VMAs in one address space have valid ordered ranges and permissions; mapping mutations and page-table changes follow their synchronization protocols.
- A successful translation cannot grant read, write, or execute authority beyond the mapping and architecture protection contract.
- Copy-on-write preserves identical initial contents while ensuring a writer's later changes are private unless the mapping is explicitly shared.
- Process creation either returns a valid child to both lifecycle domains or unwinds every partially acquired resource without publication.
- PID lookup validates namespace and lifetime; PID reuse never redirects a supposedly stable process operation.
- Exit, notification, reparenting, reaping, and final reference release occur once, even with multiple threads and concurrent observers.

### Common failures

Common mistakes are equating a process with a program file, assuming every thread has a separate address space, treating virtual size as resident memory, inferring physical contiguity from virtual contiguity, believing fork immediately copies every page, forgetting that shared mappings remain shared, using a PID after lookup without lifetime protection, assuming `exec` creates a new PID, changing mapping metadata without coordinating faults, granting write and execute together unnecessarily, reading `/proc` as an atomic snapshot, and confusing exit with complete disappearance.

### Compact example

A server process has four threads sharing one address space and file table. It creates a worker child using copy-on-write address-space state. Initially both page tables reference the same read-only anonymous frame with two owners. When the child writes, the fault path allocates a new frame, copies contents, installs a writable child mapping, and drops the old frame's child reference. The parent still reads the original. The child then executes another program: its PID persists, but mappings and many execution attributes are replaced. On exit, most resources are released; its exit status remains until the parent reaps it through a lifetime-safe handle or validated identity.

### Connections

[OS-002](002-privilege-levels-and-protection-rings.md) establishes protection, [OS-003](003-system-calls-and-user-kernel-transitions.md) establishes process entry, and [OS-007](007-kernel-data-structures.md) establishes identity and lifetime. [OS-012](../ROADMAP.md) develops creation and loading; [OS-019](../ROADMAP.md) develops virtual memory. Address translation connects to [Computer Architecture](../../23-computer-architecture/ROADMAP.md), and isolation connects to [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

“A process is a running program” is useful only as a first approximation. One executable file can back many processes. A process can replace its program without changing PID. Several threads can execute concurrently inside one address space. Distinct processes can share pages, files, memory objects, namespaces, and kernel resources while remaining different protection and lifecycle subjects.

The kernel must answer, under concurrency: which thread is executing, which address space translates its user addresses, which credentials authorize an operation, which files and namespaces it sees, who can signal or inspect it, which resources it owns, and whether it is live, exiting, or already reaped. These answers can change at fork, clone, exec, mapping operations, credential transitions, namespace creation, and exit.

The governing question is how to model these components and transitions without collapsing identity, memory, execution, authority, and lifetime into one vague object. The address space is central, but it is one referenced resource among several.

## Why This Matters

Process abstractions create isolation and multiplex hardware. Virtual addresses let different processes use the same numerical address without naming the same physical frame. Page permissions prevent ordinary code from writing executable text or kernel memory. Scheduling interleaves threads while preserving register and stack state. File and namespace tables give each process a controlled view of external resources.

The abstraction also creates subtle shared state. After fork, parent and child may share physical pages through copy-on-write, open file descriptions behind duplicated descriptors, and inherited synchronization state. Within a multithreaded process, one thread can unmap memory another is using. A stale PID can identify a later process. A debugger or `/proc` reader can observe a moving target.

Security depends on precise boundaries. Address-space randomization is weakened by pointer disclosure. Writable-executable mappings expand code-injection paths. Credentials and namespaces determine whose PID, UID, mount, or network view applies. Core dumps, process inspection, shared memory, and inherited descriptors can cross trust boundaries unless governed deliberately.

## Prerequisites and Retrieval

Recall from [OS-001](001-operating-system-goals-and-resource-abstractions.md) that an OS names, protects, multiplexes, and accounts for resources. Recall from [OS-002](002-privilege-levels-and-protection-rings.md) that user access is constrained by privilege and translation. Recall from [OS-007](007-kernel-data-structures.md) that an indexed pointer needs lifetime acquisition. Recall from [OS-008](008-kernel-memory-allocation.md) that virtual, physical, and device addresses differ.

Retrieve these distinctions:

- program bytes on storage are not an executing process;
- a process is not a thread, though a single-threaded process has one thread;
- a VMA describes a range policy, while page-table entries describe current translations at finer granularity;
- mapped virtual bytes can be nonresident, shared, swapped, file-backed, or represented by huge pages;
- copying a descriptor table entry does not necessarily copy the underlying open file description;
- termination and reaping are different lifecycle events;
- numeric identity and object lifetime are separate.

## Learning Objectives

After completing this module, you should be able to:

- model a process as threads plus independently referenced resource domains;
- distinguish program image, process, thread, address space, VMA, page table, and physical frame;
- explain virtual translation, protection checks, page faults, and TLB consequences at a high level;
- reason about anonymous, file-backed, private, shared, stack, heap, and special mappings;
- simulate copy-on-write and identify its concurrency and failure obligations;
- explain configurable sharing during clone-like creation and replacement during exec;
- distinguish PID, thread-group identity, process groups, sessions, namespaces, and stable handles;
- order multithreaded exit, notification, zombie retention, reparenting, and reaping;
- interpret process memory observations without equating virtual, resident, proportional, or private size;
- identify security or safety claims requiring accountable human review.

## Core Exposition

### A process is a reference graph

Separate execution state from resource state. Each thread needs registers, scheduling state, signal mask, kernel stack, and a link to shared or selected process resources. Threads commonly share one address space, file descriptor table, filesystem context, signal dispositions, and credentials according to the OS threading model. Kernel implementations may represent each schedulable task similarly and group tasks through shared references.

Creation primitives expose or internally choose sharing. A fork-like operation creates a new process identity and logically copied resource view, using reference sharing and copy-on-write for efficiency. A clone-like primitive can request that selected components—such as virtual memory or file tables—be shared. Not every flag combination makes a coherent process model, so kernels enforce constraints.

The graph explains lifetime. Closing one descriptor drops a reference to an open file description; other descriptors or processes can retain it. One thread exiting does not destroy a shared address space while peers remain. Final release occurs when the last authorized reference and asynchronous user ends.

### Address spaces and VMAs

An address space is an ordered collection of virtual ranges plus page tables and policy. Typical regions include executable and library segments, anonymous heap, thread stacks, file mappings, shared-memory mappings, runtime data, and kernel-provided helper pages. These locations are conventions and loader choices subject to architecture and randomization, not a universal fixed diagram.

A VMA describes a half-open interval `[start, end)` with common access permissions, mapping type, backing file and offset or anonymous policy, and flags. Adjacent areas may merge when all relevant properties agree; changing protection or unmapping a subrange may split one area. Gaps are invalid unless a special growth rule applies.

Linux currently represents one userspace address space with `mm_struct` and its VMAs with `vm_area_struct` objects indexed by a Maple Tree. That is an implementation example, not the process abstraction itself. VMA metadata locking, reverse mappings, and page-table locking solve different concurrency problems and must not be substituted casually.

### Translation and protection

The CPU splits a virtual address into page-table indexes and an offset. Starting from the current address-space root, hardware or software walks entries to find a leaf mapping. The leaf identifies a physical frame or large-page mapping and carries present, user, readable, writable, executable, accessed, dirty, and architecture-specific state.

A translation lookaside buffer caches recent translations. Changing a page table is not complete merely when memory contains a new entry; CPUs that might use the old translation need the architecture's synchronization and invalidation protocol. Address-space switches update or tag the translation context so one process does not use another's entries.

Protection is checked at multiple layers. The VMA expresses intended mapping policy, page-table entries enforce current hardware access, and the syscall path checks credentials and object rights. A bug that installs a writable page under a read-only VMA can violate the higher-level contract even if the page-table operation is mechanically valid.

### Page faults and demand population

An access can fault because no valid translation exists, permission is insufficient, a page is absent, a copy-on-write mapping is read-only, or architecture state needs handling. The fault handler identifies the address space and stabilized VMA, checks the requested access, and either resolves the mapping or reports an exception such as a process signal.

Demand paging defers physical allocation or file reading until access. A large mapping can reserve virtual range without occupying equivalent resident memory. File-backed pages may already exist in the page cache and be shared among address spaces. Anonymous zero pages can be represented economically until written.

Fault handling races with unmap, protection change, truncation, migration, reclaim, and process exit. Stabilizing VMA metadata does not automatically stabilize every page-table entry or physical page. The implementation needs its documented lock, reference, retry, and invalidation protocol.

### Mapping types and permissions

Anonymous mappings have no ordinary file content backing and commonly hold heaps, stacks, and runtime state. File-backed mappings relate virtual pages to file offsets. Private mappings use copy-on-write for modifications; shared mappings can propagate writes to other mappings and, under their contract, backing storage.

Read, write, and execute permissions should follow least privilege. Loaders can map code readable-executable and mutable data readable-writable, avoiding writable-executable pages except under tightly governed mechanisms. Changing permission is a synchronization and security event, not only a bit flip.

Fixed-address mappings can replace or collide with existing layout depending on API flags. They require exact range and overflow validation. Guard regions around stacks or sensitive mappings turn some overflows into faults. Mapping device memory, huge pages, locked pages, or persistent memory introduces separate alignment, accounting, coherency, and lifetime rules.

### Copy-on-write

At fork, logically private writable pages can initially remain physically shared. Parent and child mappings are made nonwritable under a COW protocol, and the physical page holds sufficient references. A read returns identical content. A write faults, allocates a private frame when sharing still exists, copies content, installs the writer's writable mapping, and releases its claim on the old frame.

If the page is no longer shared, an implementation may restore write permission without copying, subject to synchronization. Two simultaneous writers can each need private copies. Allocation failure, signals, concurrent unmap, page migration, and pinning complicate the slow path.

COW saves time and memory when the child soon calls exec or few pages are modified. It can defer substantial latency and allocation pressure into later writes. Forking a process with many mappings also costs page-table and metadata work even when data frames are shared.

### Program replacement

An exec-like operation replaces the calling process's program image. The kernel validates the executable, arguments, environment, interpreter, credentials, limits, and file metadata; builds new mappings and initial stack; applies security transitions; and commits the new address space and register entry state. Failure before commitment returns to the old program.

On success, the PID remains, but old mappings are discarded and caught signal dispositions, thread population, alternate stacks, and other documented attributes change. File descriptors without close-on-exec remain, which is both a useful inheritance mechanism and a frequent authority leak.

Multithreaded exec requires other threads to cease because their instruction pointers and stacks belong to the old image. Observers must not assume that a stable PID implies a stable executable, address map, credentials, or command name across time.

### Process identities and groups

A PID names a process within a PID namespace and can be reused after lifecycle completion. Linux distinguishes thread IDs and a thread-group ID representing the POSIX process view. Processes also participate in parent-child relations, process groups for job control, and sessions associated with terminals.

Namespaces can make the same process visible under different PID numbers at different hierarchy levels. A numeric PID from one namespace cannot be interpreted without that scope. Credentials include several user and group IDs with different authorization roles; namespaces can map their numerical appearance.

For race-free operations, use a stable process handle where the platform provides one. Linux pidfds refer to a particular process lifetime and can support signaling, waiting, and polling without a PID-reuse window. Obtaining a handle still requires permission checks, and it does not freeze the process's mappings or credentials.

### Files, signals, and other shared domains

A descriptor table maps small integers to open file descriptions. Fork usually copies the table logically while entries reference the same underlying open descriptions, so file offsets and status can remain shared. Clone-like creation can share the table itself, making later descriptor installation and closure immediately visible across participants.

Signal dispositions, pending signals, masks, and delivery targets have process-wide and thread-specific aspects. A signal can interrupt a syscall, wake a thread, terminate the process, or trigger a user handler on a selected stack. Process lifecycle must coordinate handler state with exec and exit.

Filesystem root and working directory, namespaces, resource limits, cgroup membership, security labels, timers, IPC state, and accounting complete the resource graph. Saying “the child inherits the process” is too imprecise; each domain has copy, share, reset, or recompute rules.

### Concurrency within an address space

Threads can fault, map, unmap, protect, pin, inspect, and access the same address space concurrently. Application synchronization must prevent one thread from using a range another removes. The kernel still protects its own metadata from corruption, but it cannot infer application object lifetime from a virtual address.

Linux documents address-space-wide, VMA-granular, reverse-mapping, and page-table locks with specific ordering and scope. A lock stabilizing a VMA object may not freeze the bytes, backing folio, or every page-table entry. Page-table walkers must also account for hardware-updated accessed and dirty state.

Long-held global address-space locks harm scalability and can deadlock with filesystem or fault paths. Fine-grained and optimistic mechanisms improve concurrency but require revalidation after retry. The correct protocol depends on whether code reads metadata, installs mappings, zaps entries, migrates pages, or frees page-table levels.

### Exit, zombies, and reaping

Process exit first coordinates thread-group termination according to the API. It prevents new operations, closes or releases files and mappings, handles robust synchronization state, updates accounting, notifies a parent or reaper, and makes the task unschedulable. Asynchronous kernel references can delay final object reclamation.

A zombie retains minimal identity and exit information so a parent can collect status. It owns neither a running thread nor a normal address space. Reaping removes that lifecycle record and permits identifier reuse under kernel policy. If a parent exits, children are reparented to an appropriate reaper.

Waiting is an ownership and notification protocol, not just polling a PID. Concurrent waiters, stopped or continued state, signals, namespace init behavior, and child selection affect results. A PID reused after reap must never satisfy an operation intended for the former child; pidfds or equivalent stable handles close that race.

### Observing process memory

Memory maps show virtual intervals and permissions at an observation instant. Resident-set size counts resident pages under tool-specific semantics; it is not total allocation, private ownership, or future pressure. Shared pages complicate attribution. Proportional measures divide shared cost but are accounting conventions.

`/proc` observations race with the target's mapping and lifecycle changes and may be permission-filtered. A mapping can disappear between reading its line and inspecting its pages. Names such as heap or stack are annotations, not complete ownership proofs. Deleted files can remain mapped.

For diagnosis, record the process lifetime handle, namespace, timestamp, kernel and tool version, and which metric is used. Correlate maps with fault, reclaim, page-table, and allocation evidence before claiming a leak or physical footprint.

### Security and failure boundaries

ASLR varies layout to make address prediction harder; information leaks and shared offsets can weaken it. Nonexecutable data, read-only code, guard pages, control-flow protections, and strict user-kernel copy rules complement isolation. No single mapping flag establishes process security.

Process inspection, cross-process memory access, core dumps, tracing, and debugging are powerful capabilities. Permission checks must consider credentials, namespaces, dumpability, security policy, and target lifecycle. Memory contents include secrets even when maps alone appear innocuous.

Resource limits and accounting must bound address space, resident memory, locked or pinned pages, process count, descriptors, and other amplification. A process can reserve large virtual ranges cheaply but later fault physical memory; admission and runtime pressure policies need both views.

## Definitions and Notation

Represent an address space as an ordered set of VMAs `V = {v_1, ..., v_n}`, where `v_i = [s_i, e_i)` and `s_i < e_i`. For a nonoverlapping map sorted by start,

`e_i ≤ s_(i+1)` for every adjacent pair.

An access `(a, op)` is eligible at the VMA layer only if exactly one `v_i` contains `a` and `op` belongs to its permissions. Successful hardware access additionally requires a valid page-table translation and protection state; eligibility does not imply residency.

Let virtual address `a` under page size `P` have virtual page number `vpn = floor(a / P)` and offset `o = a mod P`. A present leaf maps `vpn` to physical frame `pfn`, producing physical address `pfn × P + o`, subject to privilege and permission checks. Huge mappings change the level and offset width but preserve the translation idea.

For a COW frame `f`, let `refs(f)` count valid mapping ownership under its protocol. After fork, parent and child can map `f` read-only with `refs(f) = 2`. A child write either proves exclusive ownership and upgrades safely or creates `g` with copied content, installs `g` for the child, decrements `refs(f)`, and sets `refs(g) = 1`.

Let process lifetime identity be `(namespace, pid, generation)`. A numeric `(namespace, pid)` lookup is insufficient after reuse unless the operation acquires the currently matched process lifetime before it can exit and be replaced.

## Mechanisms, Invariants, or Proof Structure

Review a process and address-space design through eight obligations.

**Identity integrity.** PIDs, thread IDs, groups, sessions, namespaces, parentage, handles, and generations identify intended live subjects without reuse ambiguity.

**Mapping integrity.** VMA intervals, permissions, backing, offsets, gaps, merging, splitting, and accounting form a valid address-space representation.

**Translation integrity.** Page-table construction, permission, atomicity, locking, invalidation, and lifetime agree with hardware walkers and concurrent faults.

**Sharing integrity.** Each resource domain states copy, reference-share, direct-share, reset, and ownership rules across fork, clone, and exec.

**COW integrity.** Shared content remains stable to readers, writers receive private state, references balance, and concurrent fault and unmap paths revalidate.

**Authority integrity.** Credentials, namespaces, mapping permissions, process-inspection rights, descriptors, and security transitions grant only intended access.

**Lifecycle integrity.** Creation, publication, thread exit, process exit, notification, zombie retention, reparenting, reaping, and final release occur in legal order exactly once.

**Evidence integrity.** Maps, resident metrics, traces, tests, and experiments state snapshot races, sharing conventions, kernel version, workload, and the properties observed.

The executable model below demonstrates a single-page copy-on-write split between parent and child address spaces.

<!-- bijux-verify: {"id":"toy-copy-on-write","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"before=parent:7:A child:7:A refs:2\nafter=parent:7:A child:8:B refs-old:1 refs-new:1\nprivate=yes\n","stderr":""}} -->
```python
frames = {7: {"value": "A", "refs": 1}}
parent = {"page0": 7}

child = dict(parent)
frames[7]["refs"] += 1
print(
    "before="
    + f"parent:{parent['page0']}:{frames[parent['page0']]['value']} "
    + f"child:{child['page0']}:{frames[child['page0']]['value']} "
    + f"refs:{frames[7]['refs']}"
)

old_frame = child["page0"]
if frames[old_frame]["refs"] > 1:
    frames[old_frame]["refs"] -= 1
    frames[8] = {"value": frames[old_frame]["value"], "refs": 1}
    child["page0"] = 8
frames[child["page0"]]["value"] = "B"

print(
    "after="
    + f"parent:{parent['page0']}:{frames[parent['page0']]['value']} "
    + f"child:{child['page0']}:{frames[child['page0']]['value']} "
    + f"refs-old:{frames[7]['refs']} refs-new:{frames[8]['refs']}"
)
print("private=" + ("yes" if frames[parent["page0"]]["value"] == "A" else "no"))
```

Passing proves only this sequential dictionary model's reference counts and private values. It does not model page tables, TLBs, concurrent faults, allocation failure, shared mappings, huge pages, files, signals, security, or a real fork implementation.

## Alternatives and Trade-Offs

**Separate processes versus shared-memory threads.** Processes provide stronger default memory separation and independent failure domains. Threads share data cheaply but require application synchronization and coordinated lifecycle.

**Eager copy versus copy-on-write.** Eager copy pays predictable creation cost and gives immediate independence. COW saves work when pages remain unchanged but defers faults, allocation, copying, and failure into later writes.

**Private versus shared mappings.** Private mappings isolate modifications and support COW. Shared mappings enable efficient communication and persistence but require synchronization, durability, and trust policy.

**Large versus base pages.** Large pages reduce translation depth and TLB pressure. They increase allocation, fragmentation, fault, copy, and placement granularity.

**Numeric PIDs versus stable handles.** PIDs are compact, conventional, and namespace-visible but reusable. Stable handles close reuse races at the cost of descriptors, permissions, and lifecycle management.

**Coarse versus fine address-space locks.** Coarse locks simplify invariants but serialize faults and map changes. Fine locks scale readers and disjoint ranges while increasing ordering, retry, and reclamation complexity.

**Detailed introspection versus isolation.** Rich maps, memory reads, and tracing improve diagnosis. They expose secrets and layout, perturb targets, and require strict authority and retention controls.

## Failure Modes and Misconceptions

1. **“A process is a program.”** Program files are inputs; a process is a changing execution and resource context.
2. **“One process means one thread.”** A process can contain several schedulable contexts sharing an address space.
3. **“Each thread owns separate memory.”** Threads commonly share mappings, while stacks are conventional regions within that shared space.
4. **“Virtual size equals RAM use.”** Mappings can be unpopulated, swapped, file-backed, or shared.
5. **“Adjacent virtual pages are adjacent physical frames.”** Page tables can map arbitrary eligible frames.
6. **“Fork copies every byte immediately.”** Modern implementations commonly share private pages through COW.
7. **“All inherited state is private after fork.”** Open descriptions and shared mappings can remain shared.
8. **“Exec creates a new process.”** It normally preserves process identity while replacing the program image and documented attributes.
9. **“A read-only VMA freezes its metadata and pages.”** Faults, migration, reclaim, and kernel operations can change lower-level state under protocol.
10. **“A PID uniquely identifies a lifetime.”** It is reusable and namespace-scoped.
11. **“Exit frees everything immediately.”** Zombies, observers, references, and asynchronous cleanup can remain.
12. **“Reaping kills the child.”** The child has already terminated; reaping collects retained status and identity.
13. **“A `/proc` map is an atomic truth.”** It is a permissioned observation racing with a live target.
14. **“ASLR alone isolates processes.”** Translation permissions, credentials, least privilege, leak resistance, and lifecycle remain essential.

## Worked Examples

### Example 1

**Question:** Two processes both use virtual address `0x400000`. Must they access the same bytes?

**Reasoning:** Their page-table roots can translate the same virtual number to different frames with different permissions.

**Conclusion:** Virtual addresses have meaning only within an address-space identity and mapping lifetime.

### Example 2

**Question:** A process maps 100 GiB anonymously but touches one page. Did it consume 100 GiB of physical memory?

**Reasoning:** The map reserves virtual range; demand allocation populates only accessed pages subject to policy.

**Conclusion:** Report virtual reservation and resident backing separately.

### Example 3

**Question:** Parent and child share a COW page. The parent writes first. Does the child's value change?

**Reasoning:** A private mapping's write fault gives the parent a private writable frame or exclusive upgrade; the child retains the old content.

**Conclusion:** COW shares storage temporarily without changing logical private semantics.

### Example 4

**Question:** One thread unmaps a buffer while another computes with its pointer. Will the kernel preserve the application object?

**Reasoning:** Kernel metadata remains internally consistent, but the second access can fault because application lifetime was unsynchronized.

**Conclusion:** Shared-address-space object lifetime is an application concurrency obligation.

### Example 5

**Question:** A file descriptor exists in both parent and child after fork. Are their file offsets independent?

**Reasoning:** Descriptor entries can reference the same open file description, which carries shared offset and status.

**Conclusion:** Copying a handle table is not necessarily copying the referenced resource.

### Example 6

**Question:** Monitoring observes the same PID before and after an executable name changes. Is it a new process?

**Reasoning:** A successful exec preserves PID while replacing mappings and program state.

**Conclusion:** Stable numeric identity does not imply a stable program image.

### Example 7

**Question:** A controller reads a PID, delays, then sends a signal. What race exists?

**Reasoning:** The original target may exit and be reaped; the PID can be assigned to another process.

**Conclusion:** Use a stable process handle or atomically acquire lifetime under the platform's protocol.

### Example 8

**Question:** A child has exited but still appears in a process listing. Is it executing?

**Reasoning:** A zombie retains exit status and minimal identity for its reaper but has no running address space.

**Conclusion:** Visibility and schedulability are different lifecycle properties.

### Example 9

**Question:** A debugger reads a VMA line and then accesses the range. Can it assume the mapping still exists?

**Reasoning:** The target can concurrently unmap, exec, or exit unless the inspection mechanism stabilizes it.

**Conclusion:** Treat process introspection as a raced snapshot unless the API supplies stronger synchronization.

### Example 10

**Question:** Two safety-control processes use separate address spaces and pass isolation tests. Is interference impossible?

**Reasoning:** They still share CPUs, caches, memory bandwidth, kernel paths, devices, power, and administrative controls.

**Conclusion:** Named real-time, security, safety, and platform reviewers must assess shared-resource interference and residual risk; this module claims no certification.

## Cross-Program Connections

[Computer Architecture](../../23-computer-architecture/ROADMAP.md) develops MMUs, page tables, TLBs, caches, protection bits, and address translation. This module connects those mechanisms to process identity and lifecycle. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops thread sharing, races, synchronization, and reclamation.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects mapping permissions, process inspection, credentials, namespaces, ASLR, descriptor inheritance, and isolation. [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) explains executable layout, linking, runtimes, stacks, heaps, and threads from the language side.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames resource limits, fault containment, shared-resource interference, and assurance. Successors [OS-012](../ROADMAP.md), [OS-013](../ROADMAP.md), [OS-019](../ROADMAP.md), and [OS-020](../ROADMAP.md) deepen loading, threads, virtual memory, and page tables.

## References

- Linux Kernel documentation, [Process Addresses](https://docs.kernel.org/mm/process_addrs.html), current page checked 2026-09-04. VMAs, address-space representation, locking, reverse mappings, page-table operations, atomicity, and freeing.
- Linux Kernel documentation, [Page Tables](https://docs.kernel.org/mm/page_tables.html), current page checked 2026-09-04. Hierarchical translation, page frames, entries, faults, architecture folding, and per-process roots.
- Linux man-pages project, [fork(2)](https://man7.org/linux/man-pages/man2/fork.2.html), current page checked 2026-09-04. Child identity, inherited resources, copy-on-write, limits, and failure behavior.
- Linux man-pages project, [clone(2)](https://man7.org/linux/man-pages/man2/clone.2.html), current page checked 2026-09-04. Configurable sharing of virtual memory, files, signals, namespaces, thread groups, and process handles.
- Linux man-pages project, [execve(2)](https://man7.org/linux/man-pages/man2/execve.2.html), current page checked 2026-09-04. Program-image replacement, interpreter loading, attribute preservation and reset, credentials, descriptors, and failure.
- Linux man-pages project, [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html), current page checked 2026-09-04. Anonymous and file mappings, private and shared semantics, permissions, placement, alignment, and errors.
- Linux man-pages project, [mprotect(2)](https://man7.org/linux/man-pages/man2/mprotect.2.html), current page checked 2026-09-04. Page-aligned permission changes, architecture behavior, mapping splits, protection keys, and errors.
- Linux man-pages project, [proc_pid_maps(5)](https://man7.org/linux/man-pages/man5/proc_pid_maps.5.html), current page checked 2026-09-04. Process mapping intervals, permissions, offsets, devices, inodes, pathnames, and access control.
- Linux man-pages project, [credentials(7)](https://man7.org/linux/man-pages/man7/credentials.7.html), current page checked 2026-09-04. PIDs, parentage, process groups, sessions, user and group identities, and authorization roles.
- Linux man-pages project, [pid_namespaces(7)](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html), current page checked 2026-09-04. Namespace-scoped identities, hierarchy, init and reaping roles, visibility, and procfs behavior.
- Linux man-pages project, [pidfd_open(2)](https://man7.org/linux/man-pages/man2/pidfd_open.2.html), current page checked 2026-09-04. Stable process file descriptors, polling, signaling relationships, thread constraints, and PID-reuse avoidance.
- Linux man-pages project, [wait(2)](https://man7.org/linux/man-pages/man2/wait.2.html), current page checked 2026-09-04. Child state observation, exit status, zombies, selection, signals, and reaping behavior.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Compact implementations of process state, page tables, address spaces, fork, copy-on-write lab context, exec, exit, wait, sleep, and wakeup.

## Exercises

### Exercise 1

Model a web-server process as threads and referenced resource domains. For address space, descriptors, open descriptions, credentials, signal dispositions, namespaces, working directory, and limits, state what fork, thread creation, exec, thread exit, and process exit copy, share, reset, or release.

### Exercise 2

For four private pages shared after fork, trace reference counts when parent writes pages 0 and 2, child writes pages 1 and 2 concurrently under a correct fault protocol, parent exits, child execs, and the old address spaces are released.

### Exercise 3

Design synchronization for an address-space range manager supporting lookup, fault, map, unmap, protection change, page migration, and full teardown. Separate VMA stability, page-table entry access, physical-page lifetime, and TLB invalidation.

### Exercise 4

Design a process-monitoring interface that remains correct across PID namespaces, PID reuse, exec, multithreaded exit, zombies, and permission changes. State handle, snapshot, consistency, and privacy semantics.

### Exercise 5

Construct an assurance review for two safety-critical processes isolated by address spaces on one multicore system. Cover translation, shared kernel paths, caches, memory bandwidth, scheduler, devices, denial of service, observation, fault injection, and human judgment.

## Answers to the Exercises

### Answer 1

Represent each thread with registers, kernel stack, scheduling state, signal mask, and references to process resources. Fork creates a new PID and thread, logically copies the address-space view through COW, copies descriptor entries while retaining references to the same open descriptions, inherits credentials, dispositions, namespaces, directory, and limits under each API's rules. Thread creation shares the address space and usually the process-level descriptor, signal-disposition, credential, and namespace domains while creating thread execution state.

Exec replaces mappings and execution entry, terminates peer threads, resets documented signal and runtime attributes, applies credential transitions, and closes close-on-exec descriptors; PID and many process relations persist. One thread's exit releases its execution state and references but not shared domains still used by peers. Final process exit closes descriptors, tears down mappings after users cease, releases resource-domain references, publishes exit status, and leaves a zombie record until reaped. Each component needs exact platform semantics rather than a blanket “copy process” rule.

### Answer 2

After fork, each of four frames has two mapping references and both page tables make private writable intent read-only at the leaf. Parent writes pages 0 and 2: each fault allocates and copies a new parent frame, changes only the parent PTE to writable, and reduces the corresponding original to one child reference. Child writes page 1 similarly, leaving a child copy and one parent reference to the original.

Concurrent writes to page 2 begin from a state where the child alone references the original because the parent already copied. Under the fault lock and revalidation, the child can safely upgrade its mapping without copying if no other relevant owner remains; it must not rely on a stale pre-lock count. Parent exit drops its private frames for pages 0 and 2 and its original references for pages 1 and 3. Child exec installs a new image transactionally, then unmaps old pages 0 through 3, dropping every child reference. Each frame is reclaimed only at its final reference after page-table and TLB safety.

### Answer 3

Use an ordered address-space index whose read protocol stabilizes the VMA during lookup and fault. Map, unmap, permission change, split, and merge require address-space or range write exclusion and follow an order compatible with reverse mappings. Fault installs a PTE only after revalidating that the VMA still covers the address with the required permission. Page-table writes use the leaf or higher-level lock and atomic access rules for the architecture.

Migration stabilizes the physical page through its reference and reverse-mapping protocol, marks or replaces translations, copies data, updates eligible PTEs, and releases the old frame only after walkers cannot use it. Unmap first removes or invalidates leaf access, updates reverse mappings and references, performs required TLB invalidation, and only then reclaims backing. Full teardown blocks new faults and reverse-map access, zaps leaves, invalidates translations, detaches VMAs, and frees page-table levels after every walker is excluded. Lock order and retry points must be documented and tested.

### Answer 4

Resolve a namespace-scoped PID to a stable lifetime handle and retain the namespace identity used for interpretation. Expose immutable lifetime identity, current thread-group and parent relations, exec generation, state, and selected resource metrics. Numeric PID remains a display field, never the durable key. Poll or event notification distinguishes exit from reaping; zombie status remains readable according to permissions until collection.

Define each read as either individually current or part of an explicitly requested snapshot generation. A snapshot may pause the target, use kernel stabilization, or report fields with per-field timestamps and inconsistency markers; do not imply atomicity accidentally. Exec increments image generation and invalidates cached map interpretation. Multithreaded exit reports per-thread and group state. Recheck credentials, namespace authority, dumpability, and security policy on sensitive operations; minimize maps and memory data, redact addresses, audit access, bound retention, and return a stable gone result after final lifetime release.

### Answer 5

State spatial-isolation properties for user mappings, kernel mappings, page-table roots, permissions, TLB tags, invalidation, DMA domains, and process-inspection authority. Test cross-process read, write, execute, stale translation, COW, fork, exec, crash, and teardown under concurrency. Review the kernel's shared code, allocator, page cache, files, IPC, signals, namespaces, and administrative paths for unintended communication or common-mode failure.

Measure worst credible interference from scheduler preemption, interrupts, cache and TLB contention, memory bandwidth, NUMA, reclaim, thermal control, and shared devices. Enforce CPU, memory, descriptor, process, and I/O budgets with safe overload behavior. Fault-inject malformed mappings, memory exhaustion, stuck exits, device DMA, and monitor loss. Use hardware isolation where required, verify boot and configuration, and make evidence representative of deployed load. A named architecture owner, kernel specialist, real-time analyst, security reviewer, safety authority, independent verifier, and acceptance owner must assess assumptions and residual risk. This chapter and COW toy claim no external certification.
