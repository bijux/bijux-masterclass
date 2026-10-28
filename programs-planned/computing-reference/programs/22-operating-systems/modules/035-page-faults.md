---
module_id: OS-035
program: Operating Systems
level: 1
module_number: 35
title: Page Faults
status: complete
last_verified: 2026-09-04
---

# Page Faults

## One-Page Review

### Governing question

How should an operating system classify and resolve translation exceptions so recoverable memory events resume correctly while invalid, unsafe, or unserviceable accesses fail with precise evidence?

### Essential definitions

- A **page fault** is a synchronous architectural exception raised during address translation or access checking.
- The **fault address** is the virtual or architecture-defined address associated with the failed access.
- The **fault cause** encodes facts such as access type, privilege, translation presence, permissions, or reserved-entry conditions.
- A **recoverable fault** can be resolved by an authorized state transition and instruction retry.
- A **protection fault** occurs when translation exists or is otherwise known but access rights reject the operation.
- An **exception fixup** redirects a known faulting kernel instruction to a reviewed recovery path.
- A **recursive fault** occurs when handling one exception triggers another before the first context is safely resolved.

### Central model, mechanism, or theorem

Represent a fault event as `E=(address,pc,access,privilege,cause,context,generation)`. The handler snapshots architecture state, finds authoritative region `V`, and classifies the event. Resolution `R(E,V)` is one of `retry`, `signal`, `fixup`, `terminate`, `panic`, or `delegate`, with a concrete state change required before `retry`.

Retry is correct only if the handler establishes a translation and permissions that make the original operation valid, preserves any specified partial effects, and returns to the architecturally defined restart point. If the mapping changed while the handler waited, it reclassifies against the new generation instead of installing a stale result.

### Critical invariants

- Fault address, program counter, cause, access type, and privilege are captured before nested activity can overwrite them.
- Every retry follows a verified state change or a justified transient condition; unchanged invalid instructions cannot loop forever.
- Region and page-table state are revalidated after locks are dropped, allocation occurs, or I/O waits.
- User faults cannot trick privileged code into mapping unauthorized memory or disclosing kernel state.
- Kernel fault recovery applies only to registered operations and ranges with defined partial-progress semantics.
- Recursive, double, stack, machine, and handler-resource failures have bounded terminal behavior.
- Metrics distinguish demand, copy-on-write, permission, backing error, invalid address, fixup, and fatal outcomes.

### Common failures

Common mistakes are treating every fault as a missing page, trusting a stale fault address after nested faults, retrying without changing state, expanding a stack from any nearby invalid access, holding locks across fault-prone copies, translating kernel faults into user signals indiscriminately, catching `SIGSEGV` and continuing after an unresolved hardware fault, confusing `SIGBUS` and `SIGSEGV` policies across platforms, and using total fault counts as latency evidence.

### Compact example

A user store faults on a present read-only private mapping. The handler snapshots the address and write cause, locks and revalidates the region, recognizes copy-on-write, allocates and copies a private frame, verifies the mapping generation again, publishes a writable PTE, performs required invalidation, and retries. If the address was unmapped during allocation, it releases the frame and reports the current invalid-access outcome instead.

### Connections

[OS-031](031-address-translation.md), [OS-032](032-page-tables.md), [OS-033](033-translation-lookaside-buffers.md), and [OS-034](034-demand-paging.md) provide translation and population mechanics. [OS-036](../ROADMAP.md) and [OS-037](../ROADMAP.md) expand replacement and copy-on-write.

## Governing Question

A page fault is evidence from the architecture, not a complete diagnosis. An absent entry might represent valid lazy allocation, swapped data, a guard page, an invalid pointer, or an in-progress migration. A present-entry violation might request copy-on-write, enforce execute prevention, or reveal a bug.

The governing question is how to combine precise trap evidence with current operating-system policy. The handler must capture volatile state, select a legal transition, tolerate concurrency and waits, and choose a bounded terminal response when recovery is impossible.

## Why This Matters

Faults implement demand paging, stack growth, copy-on-write, access tracking, memory-mapped I/O, and user-space migration. They also enforce isolation when processes dereference invalid or unauthorized addresses.

Fault paths execute at difficult boundaries. They can interrupt kernel code, allocate under pressure, enter filesystems, block on I/O, contend on mapping locks, and fault again. A recovery bug can corrupt memory or turn a user input into a kernel crash.

Performance is bimodal. A minor mapping repair may be short; storage, reclaim, compaction, or delegated resolution may take orders of magnitude longer. Outcome-specific latency matters more than one aggregate count.

## Prerequisites and Retrieval

Review [OS-004](004-interrupts-and-exceptions.md), [OS-031](031-address-translation.md), [OS-032](032-page-tables.md), [OS-033](033-translation-lookaside-buffers.md), and [OS-034](034-demand-paging.md). Recall signals from [OS-028](028-signals-and-notifications.md).

Retrieve these distinctions:

- exception cause and operating-system resolution are separate layers;
- absent, nonresident, write-protected, execute-protected, reserved, and invalid states differ;
- synchronous fault delivery identifies the faulting execution context, unlike ordinary process-directed notification;
- retry, resume elsewhere, signal delivery, and termination have different saved-context semantics;
- hardware may report architecture-specific partial effects for split or misaligned accesses;
- user-mode and kernel-mode faults require different containment and recovery policies;
- fault count, fault service time, and application stall time are not interchangeable.

## Learning Objectives

After this module, you should be able to:

1. decode architecture fault address, program counter, access, privilege, and cause;
2. classify missing, demand, copy-on-write, protection, reserved, backing, stack, and fatal faults;
3. trace safe lock, allocation, I/O, revalidation, publication, invalidation, and retry;
4. design user fault signaling and bounded kernel exception-fixup paths;
5. reason about nested faults, partial accesses, userfault delegation, and handler liveness;
6. diagnose retry loops, stale completion, unsafe stack growth, and fault-time deadlocks;
7. build outcome-specific tests, metrics, and assurance evidence.

## Core Exposition

### Synchronous exception entry

The processor raises a page fault in response to a particular instruction fetch, load, store, or atomic access. Trap state identifies a saved execution point and architecture-specific cause. The handler begins in privileged context on a valid exception stack or equivalent facility.

Capture volatile fault registers early. On some architectures, a later nested fault overwrites the register holding the first address. Preserve the original event before calling code that can fault.

### Architecture evidence

Architectures differ. x86 page-fault error information distinguishes conditions such as nonpresent versus protection, read versus write, user versus supervisor, reserved-bit, instruction fetch, and optional protection features. RISC-V exposes separate instruction, load, and store or AMO page-fault causes plus a fault-value register under its rules.

Do not invent a portable numeric cause encoding. Normalize into an internal record while retaining raw values for diagnosis and architecture-specific decisions.

### Current mapping policy

Trap evidence is combined with the current address-space region: bounds, backing object, offset, allowed access, sharing, growth policy, generation, and page-table state. Another thread can change these between the fault and lock acquisition.

The fault address alone never authorizes allocation. A valid region and policy must explain why the access can be serviced.

### Classification

Useful classes include missing anonymous, missing file, swapped, copy-on-write, access-tracking, migration, userfault-delegated, stack-growth candidate, protection violation, malformed page table, backing error, and invalid address.

Classes are mutually exclusive at a decision point even when one resolution later transitions through another. Preserve cause and chosen class in metrics.

### Missing anonymous pages

A valid anonymous read can map a shared zero page; a write can allocate a private zeroed frame. Concurrent faults coordinate publication and loser cleanup. Allocation failure invokes memory policy rather than exposing uninitialized content.

Retry occurs only after a valid PTE is visible with sufficient permission. If the region disappears during allocation, the candidate is released and the event is reclassified.

### File-backed pages

A valid mapped-file fault checks page-cache state and can initiate or join retrieval. It validates object identity, offset, file size, mapping type, and final-page semantics. I/O errors and truncation can produce a bus-like process fault under platform policy.

Locks often cannot be held through storage I/O. The handler carries references and generation, then revalidates before installing the page.

### Copy-on-write

A write to a read-only private page can mean copy-on-write rather than a forbidden operation. The handler validates COW policy, allocates a private frame, copies stable content, and compare-publishes a writable entry.

Concurrent winners, pins, aliases, huge pages, and allocation failure complicate the transition. OS-037 develops the mechanism fully.

### Accessed and dirty emulation

Some systems deliberately fault to set accessed or dirty state in software or under an architecture extension. The handler verifies that the requested operation is otherwise authorized, updates tracking state, and retries.

Tracking faults can be frequent. Batching and sampling reduce overhead but change observation precision; neither may weaken actual permissions.

### Permission violations

A user write to a genuinely read-only region, instruction fetch from nonexecutable memory, or user access to supervisor memory is not repaired merely to make progress. The OS delivers the documented process exception or terminates according to policy.

Security-sensitive code does not silently upgrade access based on the attempted operation. Permission changes come from authorized mapping APIs or specific mechanisms such as COW.

### Reserved and malformed entries

An architecture can fault when reserved entry bits or illegal combinations appear. This often indicates kernel corruption, unsupported extensions, or erroneous table construction rather than an ordinary user mapping miss.

Containment depends on context, but continuing after guessing an encoding is unsafe. Preserve raw entry evidence and fail within a bounded policy.

### Stack growth

Some systems grow eligible user stacks on faults near a managed boundary. Growth must validate region identity, guard gaps, maximum stack size, address direction, resource limits, and the platform's access-context rules.

Do not convert an arbitrary wild pointer near another mapping into authorized memory. Guard pages remain intentionally inaccessible and distinguish overflow.

### Retrying the instruction

Fault-class exceptions generally preserve a restart point so the original instruction can execute again after resolution. The handler restores required register and privilege context and returns through the architecture's exception mechanism.

Retry must make progress. Count repeated faults at the same instruction, address, cause, and generation; bounded detection catches bad emulation or stale invalidation loops.

### Partial effects

Some wide, split, or misaligned memory operations can have architecture-specific partial effects before a later portion faults. The handler and higher-level code cannot assume every faulting operation was globally effect-free.

Atomic instruction contracts differ. Device memory is especially sensitive because reads and writes can have side effects. Align accesses and use architecture APIs rather than relying on transparent retry.

### Signals to user space

Unix-like systems commonly translate unresolvable user memory faults into synchronous signals such as `SIGSEGV` or `SIGBUS`, with platform-defined codes and address information. Default action usually terminates and may produce a core image.

A handler runs under async-signal constraints. Returning is safe only if the cause was repaired through a defined mechanism. Catching a segmentation signal, logging with unsafe routines, and continuing unchanged can immediately fault again or enter undefined language behavior.

### Language and runtime handling

Runtimes sometimes use protected pages for stack guards, safepoints, write barriers, or managed exceptions. They install platform-specific handlers, reserve alternate stacks, classify only owned address ranges, and chain or restore unrelated faults.

The design must coexist with sanitizers, debuggers, native libraries, signals, and multiple threads. A process-global handler is shared infrastructure, not a private callback.

### Kernel-mode faults

A kernel fault can arise from a bug, corrupted mapping, unsafe user pointer, deliberate probe, or expected access that has a registered recovery path. Arbitrarily invoking the full user fault path may deadlock or violate context rules.

Classify privilege, interrupt state, locks, fault-disable state, and address domain. Unrecoverable kernel faults trigger containment, diagnostics, or panic according to system policy.

### Exception tables and fixups

Kernel copy and probe routines can annotate instructions that may fault and associate them with fixup locations. On a matching fault, the handler redirects saved execution to code that returns a partial count or error.

Only registered sites qualify. Fixups must define which bytes transferred, how registers change, what locks are held, and whether retry is allowed. They cannot excuse arbitrary kernel pointer faults.

### No-fault regions

Some contexts cannot sleep, allocate, or recurse into complex memory management. Kernel APIs can disable faults or provide no-fault probes with bounded failure. Callers must handle inability to access rather than forcing population.

Pre-fault or pin data before entering constrained regions when the design allows, while respecting pin and resident-memory limits.

### Recursive and double faults

A fault handler can fault while reading metadata, growing its stack, logging, allocating, or copying. Dedicated exception stacks, early state capture, minimal low-level paths, and known-safe memory reduce recursion.

Architectures define escalation such as double-fault or critical-error behavior. Recovery options shrink rapidly. Use a bounded emergency path that avoids the failed dependencies.

### Lock ordering and deadlock

Fault handling can acquire region, page-table, page-cache, filesystem, reclaim, and allocator locks. A thread that faults while holding one of these in the wrong order can deadlock against itself or another handler.

Kernel interfaces state when user access or faulting is permitted. Review indirect faults from copying, instruction fetch, stack growth, and allocator metadata, not only explicit page accesses.

### User-space fault delegation

Linux `userfaultfd` can route supported missing, minor, and write-protect faults to a user-space monitor. The event identifies address and flags; the monitor supplies or continues a page through negotiated operations.

The monitor tracks mapping changes, fork, remove, unmap, and generations. A dead or overloaded monitor can stop faulting threads, so supervision, deadline, permission, and failure policy are part of correctness.

### Virtualization faults

Guest page faults can arise at guest first stage or host-controlled second stage. The hypervisor may inject a guest exception, populate host backing, emulate access, or terminate the VM. Evidence includes guest virtual and guest physical context under architecture rules.

Nested fault handling preserves VM identity and migration generation. A host error must not be misreported as a guest permission decision without policy.

### Device and machine errors

An access can fail because backing hardware reports poison or an uncorrectable error rather than because translation is missing. Operating systems may isolate a page, signal a process, recover mirrored data, or escalate.

Do not endlessly retry a permanent hardware fault. Preserve physical and machine-check evidence under security policy.

### Fault injection and testing

Inject allocation failure, cache miss, I/O error, truncation, concurrent unmap, COW races, userfault monitor death, recursive fault, and invalid entry. Validate both state and cleanup, not merely returned signal.

Architecture emulators help exercise rare causes but are evidence for the modeled implementation. Hardware tests, static review, and concurrency analysis remain necessary.

### Observability

Record raw cause, normalized class, user or kernel privilege, access type, outcome, retries, service latency, allocation, I/O, reclaim, lock wait, fixup site, signal code, recursion depth, and stale-generation rejection. Protect addresses and register state as sensitive data.

Aggregate by class and outcome. A total count can rise because healthy demand population increased, while one fatal or slow class worsened.

### Security and assurance

Treat fault addresses and timing as attacker-controlled inputs. Bound work, validate ranges and generations, preserve permission, zero memory, restrict diagnostics, and avoid exception-path side effects that amplify denial of service.

Assurance traces every cause to a permitted outcome and proves retry progress or bounded termination. No signal handler, emulator trace, or passing fault test alone certifies the memory subsystem.

## Definitions and Notation

Let fault event be `E=(a,p,o,u,c,x,g)`: address `a`, saved program counter `p`, operation `o`, privilege `u`, raw cause `c`, execution context `x`, and mapping generation `g`. Current region and page state are `V(a,t)` at classification time `t`.

Resolution function `R(E,V)` returns `retry`, `signal`, `fixup`, `terminate`, `panic`, or `delegate`. `retry` requires a state transition whose postcondition authorizes the original operation and preserves architecture-specified partial effects.

Let attempts for key `(p,a,o,c,g)` be `n`. A bounded retry policy defines maximum or progress evidence; unchanged state with increasing `n` cannot continue indefinitely.

## Mechanisms, Invariants, or Proof Structure

A reviewable page-fault handler follows ten obligations:

1. Capture raw address, PC, cause, operation, privilege, context, and architecture state early.
2. Normalize without discarding raw evidence or imposing another architecture's encoding.
3. Find and lock the current mapping, backing identity, permission, and generation.
4. Classify demand, cache, COW, tracking, migration, delegated, protection, malformed, and fatal states.
5. Bound allocation, I/O, reclaim, locks, retries, recursion, and external handling.
6. Revalidate after every unlocked operation or wait and reject stale completion.
7. Publish content, metadata, PTE, invalidation, accounting, and wakeup in safe order.
8. Retry only after progress; otherwise signal, fix up, terminate, or panic by policy.
9. Preserve partial-transfer, fork, exec, unmap, truncate, virtualization, and machine-error semantics.
10. Test and observe every class while labeling platform and evidence scope.

The executable classifier illustrates how x86-style core error bits separate present/protection, write/read, user/supervisor, reserved-bit, and instruction-fetch evidence.

<!-- bijux-verify: {"id":"toy-fault-decoder","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"code=0x17\npresent=protection\naccess=write\nprivilege=user\nreserved=clear\nfetch=instruction\n","stderr":""}} -->
```python
code = 0b10111
print(f"code={code:#x}")
print("present=" + ("protection" if code & 0b00001 else "nonpresent"))
print("access=" + ("write" if code & 0b00010 else "read"))
print("privilege=" + ("user" if code & 0b00100 else "supervisor"))
print("reserved=" + ("set" if code & 0b01000 else "clear"))
print("fetch=" + ("instruction" if code & 0b10000 else "data"))
```

The toy decodes five illustrative x86 bits only. It omits current architectural extensions, addresses, page tables, operating-system policy, side effects, and recovery.

## Alternatives and Trade-Offs

- Demand fault recovery saves eager work but moves latency and failure into access.
- Coarse address-space locking simplifies classification but serializes unrelated faults.
- Fine-grained fault and page locks improve concurrency but complicate stale-state validation.
- Kernel exception fixups contain expected probes but increase annotated control-flow complexity.
- User-space delegation enables migration policy but adds security and liveness dependencies.
- Automatic stack growth improves usability but weakens guard clarity if criteria are broad.
- Retry preserves transparent execution but is unsafe without progress and partial-effect analysis.
- Immediate termination contains invalid state but can reduce service availability.
- Rich crash evidence aids diagnosis but risks secrets and may fault recursively.

## Failure Modes and Misconceptions

1. **“Page fault means the page is absent.”** permission and malformed states also fault.
2. **“Hardware cause determines policy.”** the OS combines it with current mapping state.
3. **“Faulting instructions have no effects.”** split or misaligned operations can have architecture-specific partial effects.
4. **“Retry is always safe.”** state must change and side effects must be understood.
5. **“The fault address stays available.”** nested faults can overwrite volatile registers.
6. **“Any nearby fault may grow the stack.”** eligibility and limits must be strict.
7. **“Kernel faults become process signals.”** only user faults and defined paths use that containment.
8. **“A fixup catches all kernel mistakes.”** it applies only to registered sites and contracts.
9. **“Catching `SIGSEGV` makes invalid access recoverable.”** unresolved cause remains and handler constraints apply.
10. **“Minor faults are one mechanism.”** demand, COW, PTE install, and tracking can differ.
11. **“Userfault handlers are ordinary servers.”** their failure can suspend faulting execution.
12. **“One retry counter prevents livelock.”** key, generation, and genuine progress matter.
13. **“Total faults measure memory health.”** class, outcome, and latency are required.
14. **“A core dump is harmless evidence.”** it can contain secrets and large sensitive state.

## Worked Examples

### Example 1

A user read faults on a valid unpopulated anonymous region. The handler maps zero content read-only and retries. A later write takes the COW allocation path.

### Example 2

A file fault waits for I/O while another thread truncates the file. Generation and size revalidation reject stale PTE installation and return the platform's backing-error outcome.

### Example 3

Two threads write-fault one COW page. Both allocate; only one compare-publishes. The loser releases its frame and retries current state without corrupting reference counts.

### Example 4

A user fetch targets a writable nonexecutable region. The handler does not grant execute permission; it reports a protection fault according to process policy.

### Example 5

A kernel user-copy instruction faults after transferring 80 bytes. Its exception-table fixup returns the defined remaining count. Retrying the whole copy could duplicate external effects.

### Example 6

A fault handler logs through memory that itself is unmapped. The nested fault overwrites the raw address register. Early capture and a minimal emergency path preserve the original evidence.

### Example 7

A wild pointer lands just below a stack mapping. Broad automatic growth hides the bug. A guard gap, maximum, and architecture-specific access check reject it.

### Example 8

A userfault monitor receives an event after the client remaps that address. Its generation check discards the old page rather than populating the new object.

### Example 9

A guest access fails at second-stage translation because host backing was removed. The hypervisor repairs or terminates under host policy rather than injecting a false guest first-stage violation.

### Example 10

A dashboard reports fewer total faults after warmup but p99 latency rises from rare storage errors. Outcome-specific histograms reveal the regression.

## Cross-Program Connections

[Programming Languages: Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects native undefined behavior, signals, and user-memory access. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies exception delivery, MMUs, and precise state.

[Security Engineering](../../25-security-engineering/ROADMAP.md) frames permission faults, state disclosure, malicious addresses, and containment. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies fault taxonomies, liveness, diagnostics, and assurance.

Within this program, [OS-031](031-address-translation.md) through [OS-034](034-demand-paging.md) define normal mechanisms; [OS-036](../ROADMAP.md), [OS-037](../ROADMAP.md), and [OS-038](../ROADMAP.md) cover replacement, COW, and mapped files.

## References

- Linux kernel documentation, [Page Tables](https://docs.kernel.org/mm/page_tables.html), current page checked 2026-09-04. MMU faults, architecture entry, Linux handlers, demand, COW, shared mappings, and process signals.
- Linux kernel documentation, [Process Addresses](https://docs.kernel.org/mm/process_addrs.html), current page checked 2026-09-04. Region locking, fault traversal, page-table stability, concurrent changes, and file-fault invalidation.
- Linux kernel documentation, [Memory Management APIs](https://docs.kernel.org/core-api/mm-api.html), current page checked 2026-09-04. Fault callbacks, return values, PTE insertion, mapping constraints, allocation, and readahead.
- Linux kernel documentation, [Kernel-Level Exception Handling](https://docs.kernel.org/next/x86/exception-tables.html), current page checked 2026-09-04. x86 kernel faults, exception tables, instruction fixups, user-copy recovery, and control flow.
- RISC-V International, [Supervisor-Level ISA](https://docs.riscv.org/reference/isa/priv/supervisor.html), current specification checked 2026-09-04. Trap cause and value, instruction/load/store page faults, permission, canonicality, partial misaligned accesses, and retries.
- Intel, [Intel 64 and IA-32 Architectures Software Developer's Manuals](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), revision page checked 2026-09-04. Page-fault exception, fault address, error code, restart state, nested faults, paging, and protection.
- Arm, [Learn the architecture: Exception model](https://developer.arm.com/documentation/102412/latest/), current documentation checked 2026-09-04. Synchronous exceptions, syndrome, fault addresses, exception levels, vectors, return, and nested handling.
- Linux man-pages project, [sigaction(2)](https://man7.org/linux/man-pages/man2/sigaction.2.html), current page checked 2026-09-04. Synchronous signal information, fault addresses and codes, alternate stacks, reset, and handler constraints.
- Linux man-pages project, [userfaultfd(2)](https://man7.org/linux/man-pages/man2/userfaultfd.2.html), current page checked 2026-09-04. Missing, minor, and write-protect delegation, events, mapping changes, lifecycle, and liveness.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching RISC-V traps, page faults, lazy allocation, process termination, and user-kernel copying.

## Exercises

### Exercise 1

Design a page-fault classification table from raw cause, access, privilege, region, PTE, backing, and context. Define every terminal resolution.

### Exercise 2

Specify a concurrent COW fault path with stale-mapping revalidation, allocation failure, partial effects, invalidation, and bounded retry.

### Exercise 3

Design kernel exception fixups for a user-copy API. Cover annotated sites, partial transfer, no-fault contexts, nested faults, and diagnostics.

### Exercise 4

Construct fault tests and metrics that distinguish demand, file, COW, permission, invalid entry, storage error, userfault, and recursive outcomes.

### Exercise 5

Build an assurance review for a safety-relevant fault handler. Cover progress, recursion, resource bounds, signals, virtualization, evidence, and human review.

## Answers to the Exercises

### Answer 1

Capture raw architecture state first. Normalize instruction, load, store or atomic access; user or supervisor privilege; nonpresent, protection, reserved, canonical, alignment, and stage evidence. Under the current region lock, combine it with region bounds, access policy, generation, PTE state, backing object and offset, and fault-enabled context.

Valid missing anonymous or file state enters population; private write protection enters COW; approved tracking or migration state enters its handler; registered ranges may delegate. Unauthorized user access signals or terminates. Backing error uses the platform's bus or I/O outcome. Registered kernel sites fix up; unexpected kernel corruption or malformed tables enter containment or panic. Every retry names the state change, while every wait is bounded and followed by revalidation.

### Answer 2

Snapshot event and lock the region and leaf. Verify write access is allowed privately and the current read-only leaf has the expected generation. Take a stable reference to the old frame, then allocate outside any lock that forbids sleeping. Copy content under the required stability and reacquire current mapping state.

Compare object, region generation, old PTE, permission, pins, and huge-page state. If changed, release the candidate and reclassify. Otherwise update references, atomically publish the private writable leaf, invalidate stale translation as required, release the old reference, and retry. Concurrent losers free exactly once. Allocation failure leaves the old mapping intact. A repeated identical fault without state progress reaches bounded error handling.

### Answer 3

Annotate only instructions whose fault and recovery semantics are reviewed. The exception table maps each site to a fixup that knows register conventions and returns bytes transferred, bytes remaining, or a stable error. The low-level handler snapshots address and cause, confirms kernel privilege and registered PC, then redirects saved execution; it does not broadly catch kernel faults.

The API documents whether earlier bytes are visible and never retries them blindly. No-fault contexts use bounded probes and accept failure rather than entering allocation or I/O. Fixup code resides on known-present stacks and text, avoids unsafe logging, and has a recursive-fault terminal path. Tests cover faults before, during, and after transfer and verify lock and reference cleanup.

### Answer 4

Create controlled mappings for anonymous first touch, cached file without PTE, cold file retrieval, COW write, read-only write, nonexecute fetch where testable, invalid address, malformed-entry emulator test, injected storage error, registered userfault missing event, stale remap, and nested-handler failure. Separate base and huge pages and memory-pressure runs.

Record raw cause, normalized class, privilege, access, outcome, retries, service and application latency, allocation, I/O, reclaim, lock wait, invalidation, signal code, stale rejection, and cleanup. Preserve architecture, kernel, filesystem, device, mapping flags, page sizes, cache preparation, pressure, affinity, raw samples, and injected fault. Do not infer class or latency from total minor and major counters alone.

### Answer 5

Enumerate every architectural cause and context, including user, kernel, guest, host, nested, device, and machine-error boundaries. Prove early state capture, authorized classification, zeroing, permissions, generation revalidation, single publication, invalidation, bounded allocation and waits, retry progress, partial-effect handling, and terminal containment. Reserve reliable exception stacks and emergency diagnostics.

Inject allocation, I/O, stale mapping, duplicate fault, invalid PTE, target invalidation delay, recursion, userfault monitor failure, guest migration, and hardware-error simulations. Preserve architecture and platform revisions, traces, raw outcomes, and limitations. Named CPU, kernel-memory, filesystem, runtime, virtualization, security, real-time, safety, and independent-verification reviewers assess residual risk. Neither a caught signal nor a passing emulator test is certification.
