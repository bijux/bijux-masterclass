---
module_id: OS-003
program: Operating Systems
level: 1
module_number: 3
title: System Calls and User-Kernel Transitions
status: complete
last_verified: 2026-09-04
---

# System Calls and User-Kernel Transitions

## One-Page Review

### Governing question

How can an unprivileged thread request operating-system work while preserving a controlled boundary, precise interface semantics, and a safe return to user execution?

### Essential definitions

- A **system call** is a request through a kernel-defined application binary interface (ABI) for an operating-system service.
- A **wrapper** is a user-space library function that prepares the ABI call and translates its raw result into a language or library convention.
- A **system-call ABI** specifies service identifiers, argument locations, register preservation, result and error encoding, and architecture-specific entry behavior.
- An **entry instruction** deliberately causes a synchronous architectural transition to a configured kernel entry point; examples include `SYSCALL`, `SVC`, and `ECALL` on particular architectures.
- A **trap frame** is kernel-managed saved state sufficient to inspect the request, switch execution contexts when necessary, and resume or redirect user execution.
- **Copy-in** and **copy-out** are mediated transfers between user memory and kernel-owned state; they are not ordinary trusted pointer dereferences.
- A **partial result** reports work completed before a boundary such as interruption, end of available data, or resource exhaustion.

### Central model, mechanism, or theorem

A call is a protocol across a protection boundary:

`U(request, user_state) -> K(entry, saved_state, normalized_request) -> U(result, next_state)`.

Correctness requires a legal entry, protected saved state, ABI-correct decoding, complete mediation of caller-controlled values, explicit ownership during blocking and cancellation, and a validated return. Crossing into privileged execution provides a mechanism; it does not authorize the request or guarantee that it completes atomically.

### Critical invariants

- User execution can enter privileged service code only through configured entry paths.
- Entry code treats the service number, scalar arguments, handles, pointers, lengths, and indirect data as untrusted.
- Saved user state and the active kernel stack cannot be modified by the caller during service execution.
- Each acquired reference, lock, allocation, credential snapshot, and partial effect has an owner and an unwind rule.
- Blocking, signals, cancellation, restart, and preemption preserve the public interface contract.
- Copy-in and copy-out validate ranges, overflow, permissions, direction, lifetime, and fault behavior.
- Return values and restored execution state disclose no unintended privileged data or authority.

### Common failures

Common mistakes are equating a library function with a kernel entry, treating the syscall number as authorization, dereferencing a user pointer after a stale check, assuming one call equals one indivisible action, retrying a partial operation as though no work occurred, promising fixed transition cost, confusing a vDSO fast path with a system call, and restoring caller-controlled return state without validation.

### Compact example

A wrapper places a `read` service identifier, file descriptor, buffer address, and count in ABI-defined locations, then executes the entry instruction. Kernel entry saves user state and dispatches only after validating the identifier. The service resolves the descriptor, checks access, transfers at most the requested bytes through a user-memory helper, and returns a byte count or encoded error. The wrapper may translate the raw negative kernel result into `-1` plus `errno`. A short positive count is success, not an error and not proof that the request was fulfilled completely.

### Connections

[OS-001](001-operating-system-goals-and-resource-abstractions.md) defines resource mediation, and [OS-002](002-privilege-levels-and-protection-rings.md) defines the privilege boundary. [OS-004](../ROADMAP.md) distinguishes interrupt and exception causes; [OS-006](../ROADMAP.md) develops processes and execution contexts. ABI mechanics connect to [Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md), while boundary assurance connects to [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

Applications need files, clocks, memory mappings, network endpoints, processes, and devices, yet direct access to the mechanisms behind those resources would defeat isolation. A system call is the operating system's deliberately narrow way to accept such requests. It combines an application-visible contract, an architecture-specific transition, and a kernel dispatch path.

Calling it a “kernel function call” hides the important work. The caller and callee operate at different privilege, trust, and often addressability assumptions. Entry must preserve state, establish a safe stack and execution context, decode an ABI, and reject malformed requests. The service may block, be interrupted, produce a partial result, or race with revocation. Return crosses the boundary again.

The governing engineering question is therefore not merely how to execute one privileged routine. It is how to preserve the request's semantics and the protection boundary across every entry, wait, error, restart, copy, and return path.

## Why This Matters

The system-call surface is one of the most exercised interfaces in a general-purpose system. Small errors multiply: a missing range check can expose kernel memory, a stale pointer can create a double-fetch vulnerability, an incorrect restart can duplicate an external effect, and an ABI mismatch can silently corrupt arguments. Even a correct service can become unsafe if entry or return restores the wrong state.

The interface also shapes performance and portability. Applications usually call language runtimes or C library wrappers, not raw architecture instructions. A wrapper can choose among kernel services, use a user-space fast path, adapt structure versions, or translate errors. A source-level API can therefore remain stable while architectures use different registers and kernels evolve internal implementations.

Finally, system calls teach a general boundary pattern. Device ioctls, hypercalls, remote procedures, enclave calls, and privileged service IPC all require explicit marshalling, validation, authority, lifecycle, and error semantics. The mechanisms differ; the disciplined questions transfer.

## Prerequisites and Retrieval

Recall from [OS-002](002-privilege-levels-and-protection-rings.md) that privilege is processor-enforced authority and that a controlled transition transfers execution to trusted code rather than promoting an application's instruction stream. You should understand registers, stacks, virtual memory, processes, file descriptors, interrupts, and basic concurrency.

Retrieve these distinctions before proceeding:

- an API is a source-level programming contract, while an ABI fixes binary calling details;
- synchronous means caused at a defined instruction boundary, not necessarily fast or nonblocking;
- a pointer is an address supplied by a caller, not proof of mapped, stable, authorized storage;
- an error code describes an outcome, not necessarily absence of effects;
- a thread can sleep in the kernel while its process and other threads continue;
- mechanism determines how control crosses; policy determines whether a requested operation is allowed.

## Learning Objectives

After completing this module, you should be able to:

- distinguish an application API, library wrapper, vDSO routine, system-call ABI, and kernel implementation;
- trace a request from user registers through architecture entry, dispatch, service execution, and return;
- state which user and kernel state must be protected across a transition;
- explain why scalar validation, handle resolution, authorization, and user-memory access are separate checks;
- reason about short results, encoded errors, blocking, signals, restart, cancellation, and partial effects;
- identify time-of-check/time-of-use and double-fetch hazards at user-memory boundaries;
- decompose transition latency without assuming each component is fixed or independent;
- compare direct entry, batching, shared queues, and user-space fast paths by their changed invariants;
- design boundary and adversarial tests for a syscall-like interface;
- identify where architecture, kernel, security, and safety claims require accountable human review.

## Core Exposition

### Three contracts, not one call

The expression `read(fd, buffer, count)` can name three related but distinct interfaces. At source level, a language or POSIX-like API defines types, results, and observable behavior. In user space, a library wrapper performs calling-convention work and may add policy or compatibility logic. At the kernel boundary, a syscall ABI assigns a service number, argument registers or stack locations, and a raw result convention.

The names need not match one-to-one. A wrapper can invoke a newer kernel service, combine services, or avoid entry altogether. Conversely, a raw syscall may lack a stable high-level wrapper. Programs that bypass their platform's supported wrapper inherit architecture, ABI, compatibility, and error-handling details.

A vDSO illustrates the distinction. The kernel can map callable code and selected data into a process so some queries complete in user space. Because no privileged entry occurs on the successful fast path, “calling an operating-system-provided clock function” does not prove a system call happened. A fallback may still enter the kernel when the fast path cannot satisfy the request.

### Preparing the user-side ABI

Before entry, a wrapper places the syscall identifier and arguments where the ABI requires. This may include extending integer values, splitting wide arguments, aligning pairs, or passing a pointer to a structure. The wrapper must respect registers designated as clobbered or preserved by that ABI.

An ABI is architecture- and operating-system-specific. The same source function can use different instruction encodings, syscall numbers, register assignments, stack rules, and error conventions. Even within one architecture, a 32-bit compatibility process and a native 64-bit process may require distinct tables and structure layouts.

The wrapper does not make pointer data trustworthy. It can detect convenient user-space mistakes, but the kernel cannot rely on those checks: the caller may issue the instruction directly, another thread may change memory, and malicious code can ignore the library.

### Architectural entry and trusted state

An entry instruction causes a synchronous exception or architecturally defined privilege-changing operation. Depending on the architecture, hardware records some return state in registers or memory, changes privilege, masks or controls selected events, and chooses a configured target. Early assembly code then saves remaining state and establishes invariants required by ordinary kernel code.

The exact sequence must be learned from the relevant architecture and kernel implementation. On one target, hardware may switch stacks; on another, entry software must do so. Some registers retain caller values; others are overwritten. Speculation controls, address-space transitions, interrupt state, and per-CPU data access add implementation-specific obligations.

The durable requirement is that the handler reach a well-defined trusted context before treating general kernel code as callable. The kernel must protect the entry target, saved user state, kernel stack, dispatch tables, and per-thread metadata from user modification. Nested exceptions and non-maskable events must not corrupt a partially constructed frame.

### Dispatch is classification, not authorization

Dispatch validates the service identifier against the active ABI and selects a handler. An unknown identifier produces a defined failure such as `ENOSYS` on Linux. A valid identifier means only that an implementation exists. It does not establish that this caller may use the referenced file, process, namespace, device, or memory.

The handler interprets scalar arguments with exact widths and signedness, checks ranges and arithmetic overflow, resolves handles to live kernel objects, checks credentials or capabilities, and accounts resource limits. These decisions may depend on a credential snapshot, namespace, security module, object state, or revocation that changes concurrently.

Every indirect structure adds an ABI. Size fields, version fields, flags, reserved bits, alignment, optional tails, and nested pointers require explicit rules. Copying a structure into kernel memory can stabilize it for validation; repeatedly reading fields from mutable user memory can produce a combination the caller never presented at one instant.

### User-memory mediation

User pointers inhabit a lower-trust address space. A preliminary numerical range test is not enough. Pages can be absent, protected, remapped, reclaimed, or concurrently modified. Arithmetic on address plus length can wrap. The access direction matters: a readable range need not be writable, and a valid input range need not be an authorized output destination.

Kernels therefore use architecture-aware helpers for copying, probing, pinning, or faulting user memory. The correct technique depends on lifetime. Small request metadata is often copied once and validated from a stable kernel buffer. Long-lived asynchronous I/O may pin pages or create managed mappings, with quotas and revocation rules. Copy-out must define what happens if some output was produced but the destination faults.

A classic double-fetch defect occurs when privileged code validates one read from user memory and acts on a later read that can differ. Defenses include a single bounded copy, immutable snapshots, locks in a shared protocol, sequence counters with retry, or deliberately idempotent validation. The chosen defense must match concurrency and fault semantics.

### Blocking, scheduling, and ownership

A synchronous call can block. If a pipe has no data, a read may place the calling thread on a wait queue and let the scheduler run another thread. The kernel stack, trap frame, object references, and accounting state must remain owned and valid while the thread sleeps. Locks that cannot be held across sleep must be released without losing the condition being awaited.

Wakeup is not proof that the condition remains true. Another thread may consume the resource first, so wait paths commonly recheck a predicate in a loop under the relevant synchronization. Cancellation, timeout, object closure, process exit, and signal delivery create additional wake reasons.

Blocking also means syscall latency is not simply transition overhead. Waiting for storage, a peer, a scheduler, or memory can dominate. Optimizing entry instructions while ignoring queueing and service work often targets the smallest term.

### Results, errors, interruption, and restart

Kernel ABIs and library APIs can encode errors differently. On Linux architectures without a separate error indicator, a raw negative value conventionally represents a kernel error number; a libc wrapper commonly returns `-1` and stores the positive code in thread-local `errno`. Portable code follows the documented API rather than assuming raw encoding.

Short positive results are fundamental. A read requesting 4,096 bytes may return 300 because only 300 were available, an end boundary was reached, or an event arrived after progress. Retrying from the beginning without accounting for those 300 bytes duplicates consumption or output. Zero also has operation-specific meaning, such as end-of-file for a read.

Signals complicate the contract. If interruption occurs before progress, an interface may expose `EINTR` or the system may restart under defined conditions. If progress occurred, a partial result may be returned instead. Kernel-internal restart markers, library behavior, signal dispositions, and interface standards determine the outcome. “Retry every interrupted call” is unsafe when the operation may have externally visible effects or a timeout must be recomputed.

### Returning to user execution

The kernel first makes the service outcome conform to the raw ABI, releases or transfers owned resources, and selects the next user state. Scheduler decisions may return to another thread before the caller eventually resumes. Signal delivery, tracing, or rescheduling may alter the path without changing the requirement for a valid boundary.

Return code restores architecture-defined state using a protected frame. It must reject or sanitize forbidden privilege bits, invalid addresses, noncanonical state, debug controls, and other values that could grant authority or fault unsafely. Registers that might disclose kernel data require initialization or clearing under the ABI and implementation threat model.

The wrapper then translates the result into its source-level contract. A clean architectural return proves neither service success nor complete work; it only means execution crossed back through an accepted return path.

### Cost and alternatives to repeated crossings

A useful latency decomposition is

`T_call = T_wrapper + T_entry + T_dispatch + T_validate + T_service + T_wait + T_copy + T_return`.

This is an accounting model, not a promise that terms are independent or paid once. Page faults can occur during copy, service work can sleep and restart, scheduler delay can overlap device work, and cache or mitigation effects can persist after return. Measurements must name architecture, kernel, mitigations, workload, contention, clock, and statistic.

Batching amortizes entry and dispatch across several operations but creates larger validation and partial-completion contracts. Shared submission queues reduce crossings but require ownership, memory-ordering, descriptor validation, backpressure, revocation, and completion protocols. User-space fast paths reduce entries for safely readable state but need kernel-controlled publication and fallback. Each optimization moves work and invariants; none removes the protection boundary by wish.

## Definitions and Notation

Let `U` denote permitted user states and `K` permitted kernel states. Let `n` be a syscall identifier, `a` its scalar arguments, `m` referenced user memory, `c` caller authority, and `o` the resolved kernel objects. Let `E` be configured legal entries and `D` the ABI-specific dispatch map.

For entry event `e`, a simplified transition is

`(u, e, n, a, m) -> (k_entry, save(u), n, a, m)` only if `u ∈ U` and `e ∈ E`.

Dispatch requires `n ∈ domain(D)`. Service execution additionally requires

`well_formed(a, snapshot(m)) ∧ live(o) ∧ authorized(c, o, operation) ∧ within_limits(c, request)`.

These predicates are separate: a mapped address can contain malformed data; a well-formed request can name a stale object; a live object can be unauthorized; an authorized operation can exceed a quota.

Let `p` be committed progress and `r` a raw result. A partial-success contract has `0 < p ≤ requested` and returns `r = p`; retry begins after `p`, not from the original boundary. An error result describes the documented state at failure and must not be generalized to “no effect” without an interface guarantee.

For return transformation `R`, require `R(k, frame, result) ∈ U`, restored control state is authorized, kernel-only data is not exposed, and all resources not deliberately transferred have a defined owner. These expressions organize review; they are not formal semantics for a real architecture or kernel.

## Mechanisms, Invariants, or Proof Structure

Review a system-call path as six linked obligations.

**ABI integrity.** The caller and kernel agree on identifier, argument width, signedness, placement, structure layout, clobbers, and result encoding. Native and compatibility ABIs dispatch through the correct definitions.

**Entry integrity.** Only configured instructions and causes reach protected targets. Saved state, kernel stacks, per-thread identity, address-space state, and event nesting are valid before general kernel code runs.

**Mediation integrity.** Dispatch bounds-checks the identifier. The handler separately validates scalars, snapshots mutable metadata, resolves live objects, authorizes the operation, enforces quotas, and uses user-memory helpers.

**Lifecycle integrity.** References, locks, buffers, wait registrations, credentials, accounting charges, and partial effects have explicit ownership across success, failure, sleep, wakeup, cancellation, and thread exit.

**Result integrity.** Short counts, zero, errors, timeouts, interruption, and restart match the public contract. A retry cannot silently duplicate committed effects.

**Return integrity.** Outgoing state is suitable for user execution, privileged data is absent, and the chosen return path tolerates tracing, signals, preemption, and architecture-specific restrictions.

The executable model below demonstrates dispatch, bounded transfer, raw error encoding, and wrapper translation. It intentionally models data as immutable Python values so its success cannot support claims about real page faults, races, privilege changes, or kernel entry.

<!-- bijux-verify: {"id":"toy-system-call-boundary","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"call=read\nentry=user_to_kernel\ncopied=5\ndata=hello\nreturn=kernel_to_user\nbad_fd_result=-9\nuser_errno=9\n","stderr":""}} -->
```python
FILES = {3: b"hello kernel"}


def kernel_read(fd, count):
    if fd not in FILES:
        return -9, b""  # Toy encoding for EBADF.
    if count < 0 or count > 64:
        return -22, b""  # Toy encoding for EINVAL.
    data = FILES[fd][:count]
    return len(data), data


def user_read(fd, count):
    raw, data = kernel_read(fd, count)
    if raw < 0:
        return -1, b"", -raw
    return raw, data, 0


print("call=read")
print("entry=user_to_kernel")
copied, data, error = user_read(3, 5)
print(f"copied={copied}")
print(f"data={data.decode()}")
print("return=kernel_to_user")
raw_bad, _ = kernel_read(99, 5)
print(f"bad_fd_result={raw_bad}")
_, _, error = user_read(99, 5)
print(f"user_errno={error}")
```

Passing proves only the listed outcomes for this deterministic model. It does not execute an entry instruction, cross privilege, access user virtual memory, schedule a thread, deliver a signal, enforce credentials, or reproduce any Linux ABI.

## Alternatives and Trade-Offs

**Individual calls versus batching.** Individual calls have simple attribution and failure boundaries. Batches amortize crossings and improve locality, but must report which entries completed, what order was observed, how cancellation works, and whether later entries execute after a failure.

**Copied requests versus shared queues.** Copying gives the kernel a stable snapshot and straightforward ownership at transfer cost. Shared queues can reduce copies and entries, but mutable descriptors, ring indexes, memory ordering, pinning, backpressure, and teardown become part of the security and correctness contract.

**Blocking versus nonblocking interfaces.** Blocking calls are direct to program and can integrate naturally with threads. Nonblocking calls expose readiness and progress explicitly, enabling event loops but increasing state-machine complexity. Asynchronous submission separates acceptance from completion and needs durable request identities and cancellation semantics.

**Generic versus specialized interfaces.** A generic control call can reduce syscall-table growth but often creates a broad, versioned command and structure grammar. Specialized calls can have clearer types and audit boundaries while increasing interface count. Stability, discoverability, extensibility, and attack surface all matter.

**Wrapper portability versus raw control.** Library wrappers adapt ABIs and error conventions and are normally the portable choice. Raw calls can expose a new kernel facility before library support, but bind code to exact syscall numbers, layouts, and architecture conventions.

**Kernel entry versus a user-space fast path.** Kernel entry provides current mediation and can observe protected state. A vDSO or shared read-only mapping can make frequent queries cheaper, provided publication is race-safe, data exposure is acceptable, and a correct fallback exists.

**Stronger isolation versus transition cost.** Address-space switching, speculation mitigations, register clearing, and validation can add measurable overhead. Relaxing them changes a security assumption. Decisions require the deployed threat model and representative measurement rather than a universal nanosecond claim.

## Failure Modes and Misconceptions

1. **“The C function is the syscall.”** The wrapper, source API, raw ABI, and kernel handler can differ.
2. **“A valid syscall number is permission.”** It only identifies a dispatch target; object authorization remains necessary.
3. **“Entry gives the application kernel mode.”** Control transfers to kernel code with saved application state.
4. **“A checked pointer stays checked.”** Mappings and contents can change between check and use.
5. **“An error means nothing happened.”** Interfaces may permit partial or externally visible effects before failure.
6. **“A short read should be retried from byte zero.”** Progress must be preserved or data can be duplicated or lost.
7. **“Every `EINTR` is safely retryable.”** Restart depends on operation semantics, progress, timeouts, signal policy, and runtime behavior.
8. **“System calls do not block because entry is synchronous.”** Synchronous causation does not constrain service duration.
9. **“A wakeup means the resource is available.”** Predicates generally require synchronized rechecking.
10. **“vDSO code runs in the kernel.”** Its successful fast path executes in user mode over kernel-published state.
11. **“One benchmark gives syscall cost.”** Architecture, kernel, mitigations, caches, contention, service, and statistic change the result.
12. **“More generic arguments improve compatibility.”** Untyped commands and extensible structures can enlarge ambiguity and validation burden.
13. **“Copying once solves every lifetime issue.”** It stabilizes metadata but not necessarily referenced objects, pinned pages, authority, or cancellation.
14. **“A safe entry guarantees a safe return.”** Restore state, register disclosure, signal paths, and alternate return instructions need independent review.

## Worked Examples

### Example 1

**Question:** A program calls `gettimeofday` through libc, yet tracing reports no system call. Is one tool necessarily wrong?

**Reasoning:** The wrapper may use a vDSO routine mapped into user space and read kernel-published timekeeping data without privileged entry. Tracing may observe only actual entries. A fallback can still use a syscall.

**Conclusion:** An operating-system API invocation is not synonymous with a privilege transition.

### Example 2

**Question:** Why must a kernel reject an unknown service identifier before indexing its dispatch table?

**Reasoning:** The identifier is caller-controlled. Using it unchecked can select memory outside the table and redirect privileged control. A defined bounds check converts unsupported identifiers into a documented error.

**Conclusion:** Dispatch-table bounds are part of entry mediation, not merely friendly error handling.

### Example 3

**Question:** A request contains `{length: 8, operation: READ}` in user memory. The kernel validates it, then fetches the fields again. What can fail?

**Reasoning:** Another thread can change either field between fetches. The handler may validate one request and execute a different or impossible combination.

**Conclusion:** Copy mutable metadata once into kernel-owned storage or use an explicit concurrency protocol.

### Example 4

**Question:** A `read` asks for 1,024 bytes and returns 120. Should the wrapper report failure?

**Reasoning:** A positive short count is a successful transfer of 120 bytes. Streams, terminals, end boundaries, or interruption after progress can produce it. The application decides whether to request the remaining 904.

**Conclusion:** Result semantics include progress; success is not equivalent to satisfying the maximum request.

### Example 5

**Question:** A thread sleeps inside a pipe read. Which state must survive?

**Reasoning:** Its saved user context, kernel stack, pipe reference, wait registration, credentials relevant to the operation, and partial progress need valid ownership. Wakeup must recheck the pipe predicate while handling closure, signal, and cancellation.

**Conclusion:** Blocking extends the boundary protocol across scheduling and object lifetime.

### Example 6

**Question:** Can a library safely retry every call that returns `EINTR`?

**Reasoning:** Some interfaces have no committed effect before the error, some return partial progress instead, and some operations can change external state before interruption. Relative timeouts may also need adjustment.

**Conclusion:** Retry policy is operation-specific and must use the documented progress and restart contract.

### Example 7

**Question:** Why maintain a separate compatibility syscall table for a 32-bit process on a 64-bit kernel?

**Reasoning:** Pointer widths, integer widths, alignment, syscall numbers, structure layouts, and result conventions may differ. Decoding with native assumptions can misread arguments or leak padding.

**Conclusion:** Compatibility is an explicit ABI boundary, not automatic widening.

### Example 8

**Question:** A batch submits ten writes and the sixth fails. What must the interface define?

**Reasoning:** Callers need to know which writes committed, whether order is guaranteed, whether entries seven through ten ran, how per-entry errors appear, and whether resubmission duplicates effects.

**Conclusion:** Batching saves crossings by creating a richer partial-completion protocol.

### Example 9

**Question:** A benchmark reports a 90-nanosecond “syscall.” May that value size a storage-service deadline?

**Reasoning:** The measurement may cover a minimal cached call on one CPU and kernel. Real storage calls include validation, copying, queueing, device work, scheduling, and tail latency under contention.

**Conclusion:** Decompose and measure the deployed path at representative percentiles; do not transfer a microbenchmark constant.

### Example 10

**Question:** A medical device process can issue only two permitted ioctls. Does that establish actuator safety?

**Reasoning:** The ioctl grammars, indirect buffers, driver state machine, concurrency, DMA, firmware, timing, failure recovery, authentication, and physical interlocks can still enable unsafe outcomes. Allowlisting numbers is only one control.

**Conclusion:** A named safety authority and security reviewer must assess the complete command path, evidence, assumptions, and residual risk; this module makes no certification claim.

## Cross-Program Connections

[Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) owns practical wrapper use, `errno`, robust I/O loops, and FFI boundaries. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) owns instruction-level exception entry, privilege state, register conventions, and return mechanisms. This module composes those mechanisms into an operating-system service boundary.

[Security Engineering](../../25-security-engineering/ROADMAP.md) develops complete mediation, confused deputies, memory-safety failures, syscall filtering, and assurance. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) develops races, wait predicates, cancellation, and memory ordering. [Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects versioned interface design and adapter boundaries.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) adds hazard analysis, traceability, independent review, and lifecycle evidence for high-consequence boundaries. The successor [OS-004](../ROADMAP.md) separates synchronous exceptions from external interrupts, while later modules develop scheduling, virtual memory, filesystems, and device paths invoked through these calls.

## References

- Linux man-pages project, [`syscall(2)`](https://man7.org/linux/man-pages/man2/syscall.2.html), current page checked 2026-09-04. Documents the Linux indirect wrapper, architecture calling conventions, raw results, and `errno` translation.
- Linux man-pages project, [`syscalls(2)`](https://man7.org/linux/man-pages/man2/syscalls.2.html), current page checked 2026-09-04. Distinguishes system calls from library wrappers and catalogs the Linux interface.
- Linux man-pages project, [`vdso(7)`](https://man7.org/linux/man-pages/man7/vdso.7.html), current page checked 2026-09-04. Documents kernel-provided user-space fast paths and architecture-specific symbol/version concerns.
- Linux man-pages project, [`signal(7)`](https://man7.org/linux/man-pages/man7/signal.7.html), current page checked 2026-09-04. Documents signal delivery, interrupted calls, and restart behavior on Linux.
- Linux man-pages project, [`seccomp(2)`](https://man7.org/linux/man-pages/man2/seccomp.2.html), current page checked 2026-09-04. Documents Linux syscall filtering and its explicit limitations.
- Linux Kernel documentation, [Entry/exit handling for exceptions, interrupts, system calls and KVM](https://docs.kernel.org/core-api/entry.html), current page checked 2026-09-04. Describes generic kernel entry-state sequencing and context tracking.
- Linux Kernel documentation, [Kernel entries on x86-64](https://docs.kernel.org/arch/x86/entry_64.html), current page checked 2026-09-04. Describes x86-64 entry mechanisms, calling constraints, and return concerns.
- Intel Corporation, [*Intel® 64 and IA-32 Architectures Software Developer's Manuals*](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html), current index checked 2026-09-04. Primary x86 system-call and exception architecture specification.
- Arm Limited, [*AArch64 Exception Model*](https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/Learn%20the%20Architecture/Exception%20model.pdf), 2019. Official overview of exception levels, synchronous exceptions, `SVC`, entry, and return.
- RISC-V International, [*RISC-V Ratified Specifications Library*](https://docs.riscv.org/reference/home/index.html), current library checked 2026-09-04. Primary index for `ECALL`, trap delegation, status, and return specifications.
- The Open Group, [`read()` and `pread()`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/read.html), POSIX.1-2024. Normative source for short reads, blocking, interruption, results, and errors.
- The Open Group, [`write()` and `pwrite()`](https://pubs.opengroup.org/onlinepubs/9799919799/functions/write.html), POSIX.1-2024. Normative source for partial writes, atomicity scope, interruption, and errors.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Teaching implementation of RISC-V trap entry, syscall dispatch, argument validation, and return.

## Exercises

### Exercise 1

Trace a `read(fd, buffer, 4096)` from a C call through wrapper, ABI preparation, entry, dispatch, descriptor resolution, authorization, user-memory transfer, result encoding, return, and wrapper translation. Identify which values remain untrusted at each point.

### Exercise 2

Design a versioned syscall argument structure that contains an operation, flags, byte count, timeout, and data pointer. State width, signedness, reserved-field, overflow, forward-compatibility, copy-in, and output rules.

### Exercise 3

A call transferred 600 of 1,000 bytes before a signal arrived. Compare returning 600, returning `EINTR`, and automatically restarting. Explain which choices preserve observable progress and what the caller must do.

### Exercise 4

Replace one-call-per-operation submission with a shared ring. Construct the minimum correctness and security argument for descriptor publication, memory ordering, validation, ownership, backpressure, partial completion, cancellation, revocation, and process death.

### Exercise 5

An autonomous vehicle controller exposes a small syscall-like interface from an untrusted planner to a privileged actuator service. Design an assurance review separating automated tests, implementation inspection, timing evidence, operational controls, physical safeguards, and named human judgment.

## Answers to the Exercises

### Answer 1

The source call reaches a libc wrapper, which must treat `fd`, `buffer`, and `4096` as caller values and place the syscall identifier and arguments according to the active ABI. The entry instruction transfers to a protected target and saves user state; caller registers remain untrusted inputs. Dispatch bounds-checks the identifier before selecting `read`.

The handler resolves `fd` in the caller's descriptor table, takes a stable object reference, checks that the object supports reading and that current authority and state permit it, and bounds arithmetic for the count. `buffer` remains an untrusted user address. A user-memory helper verifies the output direction and handles faults during copy. Blocking preserves the object, wait, frame, and progress ownership. The kernel returns a short nonnegative count or a raw encoded error, restores validated user state, and the wrapper translates the raw convention into its API result and possibly `errno`. Neither wrapper entry nor a valid descriptor alone authorizes arbitrary data access.

### Answer 2

Use fixed-width integer fields with an explicit `size` and `version`; define byte order within the native ABI, alignment, and zeroed reserved fields. Give `operation` a closed known set, reject unknown mandatory flags, and define whether unknown optional flags are ignored. Make byte count unsigned but reject values above the service and signed-result maxima. Define the timeout clock, absolute or relative interpretation, infinity representation, and overflow behavior. Define pointer width through the ABI rather than a language type.

The kernel first copies the declared fixed header with a maximum size, validates `size` before any tail access, zero-initializes its destination, then copies only a supported bounded extent. It uses one snapshot for validation and action. Output fields have explicit valid-on-success and valid-on-error rules; padding is cleared before copy-out. New versions append fields without reinterpreting old bytes, while incompatible semantics receive a new operation or interface. Compatibility ABIs translate layouts deliberately.

### Answer 3

Returning 600 preserves the fact that 600 bytes moved and lets the caller resume at offset 600. Returning only `EINTR` would hide progress unless the interface separately guarantees that no bytes moved, so it is unsuitable for the stated event. Automatic restart from the original buffer and count could duplicate the 600 bytes; restarting only the remainder requires kernel bookkeeping and must remain consistent with object semantics and signal policy.

The caller treats a positive 600 as success, advances its buffer and logical position, reduces the remaining count to 400, and decides whether completion is required. For an operation with non-idempotent external effects, it must never infer “no effect” from interruption without a documented guarantee. Timeouts should be recomputed against the specified clock rather than reset blindly.

### Answer 4

The producer owns a slot until it publishes a fully initialized descriptor with release ordering; the consumer observes publication with acquire ordering and owns it until completion. Monotonic indexes and bounded arithmetic prevent wrap confusion. Descriptors constrain opcodes, lengths, addresses, object handles, and reserved fields. User memory is pinned or registered with quotas and cannot be reused until completion or confirmed cancellation.

Backpressure prevents overwriting unconsumed slots. Completion records include stable request identities, status, and committed progress. Cancellation races define whether the operation was never accepted, canceled before effect, or completed. Revocation blocks new submissions, drains or aborts accepted work, removes mappings only after device and kernel access stop, and reports final ownership. Process death triggers the same teardown without trusting the producer. Tests cover malformed descriptors, reordered publication, index wrap, queue saturation, duplicated identifiers, completion loss, cancel/complete races, unmap during use, and consumer reset.

### Answer 5

Begin with the actuator hazards, allowed command vocabulary, state transitions, timing bounds, safe state, planner assumptions, and all routes into the privileged service. Automated checks can fuzz identifiers, lengths, flags, structures, pointers, sequencing, resource exhaustion, cancellation, and forbidden commands; verify ABI schemas and policy configurations; and exercise restart and process-death paths. Implementation review traces entry, snapshots, authorization, concurrency, scheduling, drivers, DMA, firmware, return, and error cleanup against the exact deployed architecture.

Timing evidence covers worst credible contention, deadline misses, stale commands, clock faults, and overload behavior rather than only average entry latency. Operational controls cover boot integrity, identity, updates, configuration drift, monitoring, incident response, and degraded modes. Independent physical interlocks, command bounds, watchdogs, and safe-state behavior require hazard-based tests. A named safety authority, domain engineer, security reviewer, and acceptance owner must review traceability, independence, test representativeness, unresolved findings, and residual risk under applicable obligations. A restricted syscall list or passing toy model cannot provide that judgment, and this chapter claims no external certification.
