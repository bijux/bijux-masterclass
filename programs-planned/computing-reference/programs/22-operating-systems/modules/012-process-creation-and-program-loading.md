---
module_id: OS-012
program: Operating Systems
level: 1
module_number: 12
title: Process Creation and Program Loading
status: complete
last_verified: 2026-09-04
---

# Process Creation and Program Loading

## One-Page Review

### Governing question

How can an operating system create a new process or replace a process image while validating untrusted executable input, preserving only intended authority, and making failure atomic?

### Essential definitions

- **Process creation** allocates a new process lifetime and chooses which parent resources are copied, shared, reset, or newly created.
- **Program loading** validates an executable representation and constructs virtual mappings, entry state, stack, and metadata from it.
- **Exec** replaces the calling process's program image without creating a new PID on success.
- A **program header** describes a runtime segment's file bytes, memory size, virtual placement, permissions, and alignment; section headers primarily serve linking and analysis.
- **BSS or zero-fill tail** is the memory portion of a loadable segment beyond its file bytes that must begin as zero.
- An **interpreter** is another executable selected by a script rule, binary-format rule, or an ELF `PT_INTERP` request to complete execution.
- An **auxiliary vector** is a typed set of kernel-provided startup values passed to the new program and dynamic loader.

### Central model, mechanism, or theorem

Treat spawn and exec as transactions with an explicit commit point:

`inspect → authorize → plan → allocate → populate → secure → commit → enter`.

Before commit, the old process image remains runnable or the unpublished child can be destroyed completely. At commit, identity, mappings, credentials, descriptors, signal state, and register entry must change according to one coherent contract. After commit, failure cannot safely “return to the old program”; it must terminate or follow a narrowly specified fatal path.

### Critical invariants

- Executable offsets, sizes, virtual addresses, alignments, arithmetic, and segment overlaps are validated before they drive mapping or copying.
- Every mapped byte is sourced from the authorized file, intentionally zero-filled, initialized stack data, or a documented kernel mapping—never stale allocator content.
- Final page permissions implement the format and policy without unintended writable-executable aliases.
- The executable and interpreter objects used after authorization are the same objects whose contents and metadata are loaded, closing path replacement races.
- Creation and exec apply documented copy, share, close, reset, and credential-transition rules to every process resource domain.
- Entry registers, stack pointer, arguments, environment, auxiliary vector, thread-local state, and architecture state satisfy the target ABI.
- Failure before commit releases all provisional resources; success publishes one valid child or one complete replacement image exactly once.

### Common failures

Common mistakes are treating fork and exec as one operation, assuming exec changes PID, parsing section headers to decide runtime mappings, trusting file offsets and counts before overflow checks, copying fewer bytes than a segment exposes, forgetting zero-fill, allowing writable and executable aliases, resolving an authorized path again later, leaking descriptors across exec, assuming signatures alone authorize privilege, performing unsafe work between fork and exec in a multithreaded child, and claiming rollback remains possible after the old image is destroyed.

### Compact example

A supervisor opens an executable beneath a trusted directory, validates the file object and policy, creates a child with a stable handle, applies file actions, resource limits, namespaces, and a no-new-privileges rule, then executes by descriptor. The loader validates architecture and program headers, maps file-backed text read-execute, maps data read-write, zeroes each segment tail, builds a bounded initial stack containing argument and environment strings plus the auxiliary vector, selects the authorized dynamic interpreter, applies credential rules, closes close-on-exec descriptors, and commits. If validation or allocation fails before commit, the supervisor receives an error and no partially visible new image exists.

### Connections

[OS-011](011-processes-and-address-spaces.md) defines process resource graphs and mappings. [OS-013](../ROADMAP.md) develops threads, [OS-020](../ROADMAP.md) develops page tables, and [OS-036](../ROADMAP.md) develops memory-mapped files. Executable format connects to [Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md); privilege transitions connect to [Security Engineering](../../25-security-engineering/ROADMAP.md).

## Governing Question

Creating execution has two distinct forms. Fork-like creation produces a new process lifetime whose state derives from a parent. Exec-like replacement keeps a process lifetime while substituting a new program image. Shells commonly compose them, making `fork + exec` look like one action, but their failure, identity, sharing, and security semantics differ.

An executable file is untrusted structured input. Its headers contain counts, offsets, sizes, addresses, permissions, alignments, interpreter names, and architecture metadata. A malformed value can overflow arithmetic, overlap mappings, expose uninitialized memory, or redirect control. The path to the file can change between authorization and use. Interpreters and dynamic libraries add further objects and policy.

The governing question is how to build and commit one valid execution context while preserving the old image or destroying an unpublished child on precommit failure. The design must also prevent inherited authority, credential escalation, concurrency, and observability from creating hidden state.

## Why This Matters

Process creation sits on login, service startup, shells, containers, build systems, server workers, and recovery. Its costs influence architecture: copy-on-write makes fork efficient when exec follows, while large multithreaded processes still pay metadata and coordination costs. Spawn interfaces can combine creation, file actions, and program replacement more directly.

Loading is a security boundary. Set-user-ID and file capability rules can change credentials. Environment variables can influence dynamic linking unless secure-execution policy suppresses them. Inherited descriptors can grant files, sockets, namespaces, or privileged service channels. Executable mappings define whether attacker-controlled data can become instructions.

Failure atomicity matters operationally. Returning an exec error is meaningful only while the old image is intact. If failure occurs after destructive commit, continuing arbitrary old code is impossible. A correct loader moves fallible validation and allocation before commitment, minimizes the postcommit path, and has a defined fatal response for exceptional late failure.

## Prerequisites and Retrieval

Recall from [OS-003](003-system-calls-and-user-kernel-transitions.md) that syscall arguments are untrusted and must be copied and validated. Recall from [OS-008](008-kernel-memory-allocation.md) that allocation can fail and partial construction must unwind. Recall from [OS-011](011-processes-and-address-spaces.md) that a process is threads plus independently referenced resource domains and that COW is logical copying with shared backing.

Retrieve these distinctions:

- fork creates a new lifetime; exec replaces an image in the current lifetime;
- executable program headers describe runtime segments, while section headers are not the loader's primary map plan;
- file size and memory size differ when a segment has a zero-filled tail;
- a pathname lookup result is an object reference at one time, not a permanent binding to those bytes;
- entry address validity requires an executable mapped segment and architecture rules, not merely an in-range integer;
- descriptor inheritance is separate from memory-map replacement;
- dynamic linking runs program-like code before the application's conventional entry function.

## Learning Objectives

After completing this module, you should be able to:

- distinguish fork, clone, spawn, exec, and interpreter dispatch by identity and sharing semantics;
- design a failure-atomic process-creation transaction;
- validate an ELF-like executable's header table, ranges, sizes, alignment, entry, and permissions;
- explain file-backed segment mapping, zero-fill, relocation, interpreter selection, and auxiliary vectors;
- construct the initial argument, environment, and metadata stack under ABI and size constraints;
- reason about descriptor, signal, credential, namespace, and thread changes across exec;
- close time-of-check/time-of-use races using stable executable objects and policies;
- explain why multithreaded fork children have restricted safe behavior before exec;
- test malformed binaries, partial allocation, privilege transitions, and postcommit failure paths;
- identify loader-security or safety claims requiring accountable human review.

## Core Exposition

### Separate creation from replacement

A fork-like operation creates a child process identity, execution context, and references derived from the caller. The child starts from a defined point with a return value distinguishing it from the parent. Address-space pages can be shared copy-on-write; descriptors can point to shared open file descriptions; credentials and namespaces are inherited under precise rules.

A clone-like interface makes selected sharing explicit and can create either process-like or thread-like execution. Sharing virtual memory, file tables, signal handlers, parent relationships, or namespaces changes which invariants the new task joins. The kernel validates flag combinations because arbitrary sharing can make identity and signal semantics incoherent.

Exec does not create a child. It replaces mappings, architecture entry state, arguments, environment, and documented process attributes. PID, parentage, and many resource relations remain. A successful exec never returns to the caller; a precommit failure returns an error to the old image.

### Creation as a transaction

Reserve identity and accounting, allocate a task object and kernel stack, copy or share resource-domain references, construct scheduling and signal state, create or reference an address space, initialize architecture registers, link parentage, and only then make the child runnable and externally observable. Exact order varies, but publication must be last relative to required initialization.

Each stage owns resources acquired so far. If address-space duplication fails, release copied file references, credentials, task storage, PID reservation, and accounting without exposing a half-child. If publication succeeds, parent and child each own their documented references and must exit independently.

Resource limits and policy can reject process creation before memory exhaustion. User-triggered process trees require counts, memory and page-table costs, descriptors, namespaces, scheduler capacity, and audit attribution. Retrying creation under a hard limit without changing state cannot create progress.

### Fork in a multithreaded process

Only the calling thread appears in the child after a traditional fork, while memory contains snapshots of locks and runtime state that other threads may have held. The absent owner cannot unlock them. Between fork and exec, calling allocation, logging, locale, or general library code can deadlock or observe inconsistent runtime state.

Standards restrict the child to async-signal-safe operations before exec in relevant multithreaded use. At-fork handlers can arrange locks around creation, but they are difficult to compose across libraries and do not solve every runtime invariant. A spawn implementation can avoid exposing a general post-fork child path and is often preferable.

The parent also needs error reporting. If a child fails setup or exec and merely exits, the parent must distinguish that from successful exec followed by immediate program exit. A close-on-exec status pipe is a common pattern: the child writes a structured pre-exec error, while successful exec closes the descriptor atomically.

### Resolve and hold the executable safely

Path resolution traverses directories under a namespace, root, mount view, credentials, symlink policy, and race conditions. Authorization followed by a second path lookup can execute a substituted object. Open a stable file object with the required resolution constraints, validate that object, and execute by descriptor when the platform supports it.

The object can still change if writable aliases are allowed, so execution protocols deny or coordinate writes as required. Network or mutable filesystems add integrity and availability considerations. Content signatures, measured storage, immutable deployment, and mount policy can strengthen provenance, but the kernel still validates format and permission.

Script and miscellaneous-format dispatch select an interpreter. The interpreter path or bound object becomes part of the trust decision. Credential derivation, argument rewriting, namespace resolution, and recursive interpreter limits must be defined. A convenient extension mechanism can become a privilege-confusion path.

### Parse executable headers defensively

Validate magic, class, byte order, version, machine, file type, header sizes, table offset, entry count, and entry size before iterating. For every expression such as `offset + count × entry_size`, use checked arithmetic and confirm the resulting range lies within the file. Reject ambiguous truncation rather than reading a partial structure.

For each loadable segment, require `file_size ≤ memory_size`. Validate `file_offset + file_size` within the file and `virtual_address + memory_size` within the user address domain without wrap. Enforce required congruence between file offset and virtual address modulo segment alignment. Validate page-rounded ranges and overlaps after rounding, not only raw byte intervals.

Reject conflicting mappings or define exactly how shared boundary pages are populated. Enforce architecture rules, canonical addresses, null-page policy, stack collisions, interpreter placement, and resource limits. Validate that the entry point lies in an executable segment of the resulting plan.

### Program headers and memory image

ELF program headers tell the loader which portions of a file participate in execution. A `PT_LOAD` segment describes file offset and size, virtual address, memory size, flags, and alignment. The loader maps file bytes into the specified virtual range and zero-initializes the memory tail beyond file size.

Text is commonly readable and executable; writable data is commonly nonexecutable. A segment can begin or end within a page, so loader and pager must ensure bytes outside the authorized file and segment do not leak. Shared file-cache pages and private COW mappings need permissions consistent with process semantics.

Section names such as `.text`, `.data`, and `.bss` help linkers and tools, but a runtime loader follows segments. Several sections can occupy one segment; stripped executables can omit information irrelevant to runtime. Teaching a loader to map by section invites divergence from the execution ABI.

### Address randomization and placement

Position-independent executables and shared objects can be placed at randomized bases. The loader chooses ranges that satisfy alignment, architecture limits, nonoverlap, stack and heap layout, and policy. Entropy is constrained by address width, fixed mappings, alignment, information leaks, and compatibility.

Randomization changes addresses, not program semantics. Relative locations and relocation metadata let code refer to symbols at runtime. The kernel typically selects the main image, interpreter, stack, and special mapping placements; the dynamic loader maps dependencies under its own rules and kernel APIs.

Fixed-address and non-position-independent images restrict placement. Never “repair” a malformed overlap by silently moving an ABI-fixed segment. The load plan must match the executable contract or fail.

### Dynamic interpreter and linking

A dynamically linked ELF image names an interpreter in `PT_INTERP`. The kernel validates and maps the main executable enough to transfer control to that interpreter and passes metadata describing both. The dynamic loader maps required shared objects, performs relocations, applies symbol resolution and versioning, establishes thread-local storage, enforces secure-execution restrictions, and eventually transfers control toward the program entry sequence.

Library search depends on encoded paths, environment, caches, defaults, namespaces, and secure mode. Empty, relative, writable, or attacker-controlled search locations can redirect dependency loading. Privileged execution suppresses or ignores dangerous environment influence according to platform policy.

Lazy symbol binding defers some relocation until first call, reducing startup work but keeping mutation machinery active later. Immediate binding moves cost and failure earlier. Read-only-after-relocation protections can make relocation targets nonwritable after setup. These are loader and build-policy choices, not consequences of ELF alone.

### Initial stack and auxiliary vector

The new stack contains argument count, pointers to argument strings, environment pointers and strings, auxiliary vector entries, alignment padding, and architecture-defined data. The kernel or loader may also supply random bytes, platform strings, executable identity, page size, program-header location, entry address, interpreter base, and secure-execution indication.

Validate total argument and environment bytes, pointer counts, terminators, stack growth, alignment, and address arithmetic. Copy user inputs into stable kernel memory before destroying the old address space because the original pointers cease to be meaningful afterward. Every byte exposed to user space must be initialized.

The auxiliary vector is typed. Consumers should query by defined key rather than assume order or presence. It can contain sensitive address and randomness information, so process-inspection permissions matter. Values describe the committed image and must agree with actual mappings.

### Descriptors and inherited authority

Exec replaces mappings but normally retains file descriptors unless marked close-on-exec. A leaked descriptor can provide a privileged file, listening socket, namespace, secret pipe, device, or directory capability to an untrusted new program. Set close-on-exec atomically when creating or duplicating descriptors; setting it in a later call races with concurrent fork and exec.

Spawn file actions deliberately close, duplicate, and open descriptors in a defined order. Descriptor numbers can be reused during actions, so ordering and temporary handles matter. Standard input, output, and error should be explicitly established rather than assumed.

Other inherited resources include working directory, root, umask, limits, scheduling attributes, cgroup membership, namespace membership, controlling terminal, and signal mask. Build a resource-domain table that states retain, reset, transform, or reject for each launch policy.

### Credentials and security transitions

Executable metadata can request effective identity changes through set-user-ID, set-group-ID, or file capabilities, subject to filesystem, tracing, no-new-privileges, namespace, and security-module rules. The new credentials, dumpability, secure-execution mode, environment handling, and process attributes must form one coherent transition.

`no_new_privs` is inherited and prevents exec from granting privilege through these file mechanisms on Linux. It is a monotonic control, not a complete sandbox. Existing descriptors, capabilities, namespaces, seccomp rules, and kernel attack surface remain.

Credential decisions must use the authorized executable object, not merely its original pathname. Interpreter chains complicate which file contributes credentials. Audit should record stable file identity, old and new credentials, policy result, interpreter, and failure without exposing secrets.

### Commit point and late failure

Build provisional address-space structures, validate executable and interpreter, copy inputs, calculate credentials, allocate stack and tables, and map required pages before commit where possible. The exact kernel commit point is implementation-specific, but after the old executable image is irreversibly removed, returning through its syscall instruction is not viable.

At commit, stop or eliminate peer threads, switch the address-space and credential references, apply descriptor closures and signal resets, install register state, publish the new image identity, and release the old resources in an order safe for observers. Tracers and audit hooks need consistent transition events.

Minimize fallible work afterward. If an exceptional postcommit failure prevents entry, terminate the process with a defined status or signal and release the new image. Do not pretend transactional rollback exists without preserved executable code, stack, mappings, credentials, and side effects.

### Testing and evidence

Generate malformed executables: truncated headers, extreme counts, wrapping offsets, file size greater than memory size, overlapping page-rounded segments, bad alignment, noncanonical addresses, invalid interpreter, entry outside executable memory, and writable-executable requests. Assert rejection before publication and without leaks.

Fault-inject each allocation, file read, mapping, page-table, credential, descriptor-action, and interpreter step. Exercise fork and spawn under process and memory limits, multithreaded runtimes, concurrent descriptor creation, namespace changes, tracing, and signal delivery. Verify the status channel distinguishes pre-exec failure from program exit.

Measure creation latency, copied page-table metadata, COW faults, resident growth, dynamic relocation, dependency I/O, and high-percentile startup under pressure. Record binaries, build IDs, loader, libraries, environment policy, kernel, filesystem, cache state, CPU, and instrumentation overhead. A successful run does not prove parser safety across all files.

## Definitions and Notation

Let file length be `F`. A program-header table at offset `h` with `n` entries of size `q` is structurally bounded only if checked arithmetic establishes

`0 ≤ h ≤ F` and `n × q ≤ F - h`.

For loadable segment `i`, define file interval `[o_i, o_i + f_i)` and memory interval `[v_i, v_i + m_i)`, where `f_i ≤ m_i`. Both additions must be nonwrapping and the file interval must lie within `[0, F)`. Bytes corresponding to `[v_i + f_i, v_i + m_i)` are initialized to zero.

If alignment `a_i > 1`, a common ELF load congruence is

`v_i mod a_i = o_i mod a_i`.

The loader also reasons about page-rounded intervals under page size `P`: `floor(v_i/P) × P` through `ceil((v_i+m_i)/P) × P`. Permissions and overlap must be valid at this actual mapping granularity.

Let `O` be the old image, `N` a validated provisional image, and `C` the commit transition. Before `C`, failure preserves `O` and discards `N`; after `C`, execution enters `N` or takes the specified fatal path. A rollback claim requires explicit preservation and reversal of every state changed by `C`.

## Mechanisms, Invariants, or Proof Structure

Review creation and loading through eight obligations.

**Input integrity.** Paths, file objects, headers, counts, ranges, interpreters, arguments, environment, and metadata are bounded, stable, and validated before use.

**Image integrity.** Segment mappings, file bytes, zero-fill, permissions, entry point, stack, auxiliary vector, special mappings, and ABI state agree.

**Authority integrity.** Executable identity, descriptor inheritance, credentials, capabilities, namespaces, environment, security policy, and interpreter trust grant only intended authority.

**Sharing integrity.** Fork and clone specify copy, COW, reference-share, direct-share, reset, or creation for every resource domain.

**Transaction integrity.** Precommit failure preserves the old image or destroys an unpublished child; commit publishes one coherent state; postcommit failure follows a defined fatal path.

**Concurrency integrity.** Peer threads, at-fork state, signals, descriptor creation, tracing, file mutation, and address-space observers cannot see or create an invalid hybrid.

**Lifecycle integrity.** Parent, child, executable, interpreter, mappings, descriptors, credentials, old image, and provisional image references transfer and release exactly once.

**Evidence integrity.** Parser tests, fault injection, security tests, timing measurements, provenance, and deployment review state the formats, policies, hardware, and failures covered.

The executable model below validates essential properties of a small load plan and reports its file-backed and zero-filled bytes.

<!-- bijux-verify: {"id":"toy-load-plan","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"valid=yes\ntext-file=3000 text-zero=2000\ndata-file=1200 data-zero=2896\nentry=0x400080 executable=yes\nwx-segments=0\n","stderr":""}} -->
```python
page_size = 4096
file_size = 12000
segments = [
    {"name": "text", "offset": 0, "file": 3000, "memory": 5000,
     "virtual": 0x400000, "align": page_size, "permissions": "r-x"},
    {"name": "data", "offset": 8192, "file": 1200, "memory": 4096,
     "virtual": 0x402000, "align": page_size, "permissions": "rw-"},
]
entry = 0x400080

valid = True
for segment in segments:
    valid = valid and segment["file"] <= segment["memory"]
    valid = valid and segment["offset"] + segment["file"] <= file_size
    valid = valid and segment["virtual"] % segment["align"] == segment["offset"] % segment["align"]
print("valid=" + ("yes" if valid else "no"))
for segment in segments:
    zero = segment["memory"] - segment["file"]
    print(f"{segment['name']}-file={segment['file']} {segment['name']}-zero={zero}")
executable = any(
    segment["virtual"] <= entry < segment["virtual"] + segment["memory"]
    and "x" in segment["permissions"]
    for segment in segments
)
print(f"entry={entry:#x} executable=" + ("yes" if executable else "no"))
write_execute = sum(
    "w" in segment["permissions"] and "x" in segment["permissions"]
    for segment in segments
)
print(f"wx-segments={write_execute}")
```

Passing proves arithmetic for two hard-coded segments only. It does not parse ELF, check integer-width overflow, page-rounded overlap, architecture ABI, relocations, files, credentials, concurrency, or a real executable loader.

## Alternatives and Trade-Offs

**Fork plus exec versus spawn.** Fork plus exec is expressive and composes with Unix process state. Spawn can avoid unsafe general child execution and reduce address-space duplication but exposes a narrower setup language.

**Path execution versus descriptor execution.** Paths are convenient and policy-friendly but can be replaced between checks. Descriptor execution binds to an opened object while adding descriptor, procfs, and close-on-exec considerations.

**Static versus dynamic linking.** Static images reduce runtime dependency lookup and loader complexity but duplicate code and complicate updates. Dynamic linking shares libraries and supports modular updates while adding search, relocation, ABI, and startup policy.

**Eager versus lazy relocation.** Eager binding moves work and failure to startup and can harden relocation data sooner. Lazy binding reduces initial work but creates later latency and mutation paths.

**Fixed versus randomized placement.** Fixed placement simplifies some low-level systems and debugging. Randomization raises prediction cost but needs position-independent code, entropy, and leak resistance.

**Inherited versus closed descriptors.** Inheritance enables pipelines and supervisors. Default closure minimizes ambient authority; atomic close-on-exec and explicit allowlists make intent clearer.

**Kernel versus user-space format handling.** Kernel handling integrates credentials and direct entry. A trusted user-space interpreter can support more formats but expands dispatch, path, privilege, and compatibility behavior.

## Failure Modes and Misconceptions

1. **“Fork runs a new program.”** It creates a new process initially continuing the existing image.
2. **“Exec creates a new PID.”** It replaces the current image while preserving process identity.
3. **“Fork copies all physical memory.”** COW commonly shares private pages until writes.
4. **“Section headers define runtime mappings.”** Program headers are the primary ELF loading description.
5. **“Memory size equals file size.”** Zero-filled tails such as BSS make memory larger.
6. **“Header fields are safe after magic matches.”** Every count, offset, size, address, and alignment needs checked validation.
7. **“Authorization by pathname binds later use.”** A second lookup can resolve a different object.
8. **“Executable permission means trusted code.”** Integrity, provenance, policy, interpreter, and credentials remain separate.
9. **“Exec closes all descriptors.”** Only those governed by close-on-exec or explicit actions close automatically.
10. **“No-new-privileges is a sandbox.”** It blocks particular exec privilege gains but leaves existing authority and attack surface.
11. **“The dynamic loader is after program startup.”** It commonly runs before the application's conventional entry.
12. **“The child may call any library before exec.”** Multithreaded parent state can leave locks permanently held in the child.
13. **“Any exec failure returns normally.”** After destructive commit, the old return context may no longer exist.
14. **“One successful binary proves loader safety.”** Malformed structure and rare failure paths require systematic tests.

## Worked Examples

### Example 1

**Question:** A shell calls fork and the child calls exec. When does the new PID appear?

**Reasoning:** Fork creates and publishes the child identity; exec later changes the child's image without changing that PID.

**Conclusion:** Creation and program replacement are distinct lifecycle events.

### Example 2

**Question:** A segment declares 8 KiB in memory but 3 KiB in the file. What fills the rest?

**Reasoning:** The loader maps authorized file bytes and initializes the 5 KiB tail to zero under the format contract.

**Conclusion:** Leaving the tail as allocator contents is an information leak and semantic failure.

### Example 3

**Question:** `offset + count × size` wraps to a small value that lies inside the file. Is the table valid?

**Reasoning:** Machine arithmetic wrap invalidates the mathematical range even if the wrapped endpoint passes a naive bound.

**Conclusion:** Use checked multiplication and subtraction-based bounds before reading entries.

### Example 4

**Question:** Two raw segments do not overlap, but their page-rounded intervals share a page with conflicting permissions. Can both be mapped directly?

**Reasoning:** Page tables enforce permissions at page granularity, and population can expose bytes across the raw boundary.

**Conclusion:** Validate and construct the actual rounded mapping plan, including boundary-page contents and permissions.

### Example 5

**Question:** A supervisor validates `/trusted/tool`, then calls exec on the pathname. What race remains?

**Reasoning:** The directory entry can be replaced between validation and the second lookup.

**Conclusion:** Retain the validated file object and execute by stable descriptor or enforce equivalent immutability.

### Example 6

**Question:** A child of a multithreaded parent calls a logging function before exec and hangs. Why?

**Reasoning:** Another parent thread may have held the logger's mutex at fork; that owner does not exist in the child.

**Conclusion:** Restrict the child path to permitted safe operations or use a spawn mechanism.

### Example 7

**Question:** An untrusted program inherits a listening socket despite changing executable and credentials. What failed?

**Reasoning:** Address-space replacement does not close descriptors lacking close-on-exec, so ambient authority crossed the boundary.

**Conclusion:** Launch from an explicit descriptor allowlist with atomic close-on-exec defaults.

### Example 8

**Question:** A dynamic executable's own entry point is valid. Can the kernel ignore `PT_INTERP` failure?

**Reasoning:** The process image contract requires the named interpreter to perform dynamic linking before application entry.

**Conclusion:** Missing or invalid required interpreter makes the execution fail.

### Example 9

**Question:** The loader has destroyed the old mappings, then cannot allocate the final stack page. Can it return `ENOMEM` to old code?

**Reasoning:** The old instruction and stack context no longer exist unless a real rollback image was preserved.

**Conclusion:** Move fallible work before commit and define termination for exceptional postcommit failure.

### Example 10

**Question:** A signed control binary and loader pass format tests. Does that certify safe actuator startup?

**Reasoning:** Configuration, inherited authority, timing, libraries, hardware, update policy, and system hazards remain.

**Conclusion:** Named platform, security, real-time, safety, and acceptance reviewers must assess full evidence; this module claims no certification.

## Cross-Program Connections

[Compilers and Language Implementation](../../08-compilers-and-language-implementation/ROADMAP.md) develops object formats, linking, relocation, calling conventions, runtimes, and entry sequences. This module adds kernel validation, mapping, credentials, and process lifecycle. [Programming Languages: Systems Programming](../../05-programming-languages-systems-programming/ROADMAP.md) connects launch APIs, descriptors, errors, and unsafe post-fork behavior.

[Security Engineering](../../25-security-engineering/ROADMAP.md) connects provenance, path races, privilege transitions, capabilities, descriptor leakage, ASLR, writable-executable memory, and sandbox composition. [Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) explains multithreaded fork hazards and publication.

[Systems Engineering](../../26-systems-engineering/ROADMAP.md) frames startup dependencies, rollback boundaries, recovery, resource admission, and assurance. Successors [OS-013](../ROADMAP.md), [OS-019](../ROADMAP.md), [OS-035](../ROADMAP.md), and [OS-084](../ROADMAP.md) deepen threads, virtual memory, executable files, and containers.

## References

- Linux man-pages project, [fork(2)](https://man7.org/linux/man-pages/man2/fork.2.html), current page checked 2026-09-04. Child creation, COW, resource inheritance, limits, errors, and multithreaded child restrictions.
- Linux man-pages project, [clone(2)](https://man7.org/linux/man-pages/man2/clone.2.html), current page checked 2026-09-04. Configurable sharing, identities, pidfds, namespaces, stacks, signal behavior, and flag constraints.
- Linux man-pages project, [execve(2)](https://man7.org/linux/man-pages/man2/execve.2.html), current page checked 2026-09-04. Image replacement, scripts, ELF interpreters, arguments, environment, credentials, preserved and reset attributes, and errors.
- Linux man-pages project, [execveat(2)](https://man7.org/linux/man-pages/man2/execveat.2.html), current page checked 2026-09-04. Directory-relative and descriptor-based execution, empty paths, close-on-exec interactions, and errors.
- Linux man-pages project, [posix_spawn(3)](https://man7.org/linux/man-pages/man3/posix_spawn.3.html), current page checked 2026-09-04. Spawn attributes, file actions, child housekeeping, fork-like implementation choices, exec, and error reporting.
- System V gABI, [Program Loading and Dynamic Linking](https://gabi.xinuos.com/elf/07-loading-intro.html), current page checked 2026-09-04. ELF process images, program headers, loadable segments, interpreters, dynamic sections, and initialization.
- Linux man-pages project, [ld.so(8)](https://man7.org/linux/man-pages/man8/ld.so.8.html), current page checked 2026-09-04. Dynamic dependency search, environment controls, secure-execution mode, tokens, caches, preload, audit, and diagnostics.
- Linux man-pages project, [getauxval(3)](https://man7.org/linux/man-pages/man3/getauxval.3.html), current page checked 2026-09-04. Auxiliary-vector keys for hardware, program headers, entry, interpreter base, page size, security, and random data.
- Linux man-pages project, [capabilities(7)](https://man7.org/linux/man-pages/man7/capabilities.7.html), current page checked 2026-09-04. Capability sets, file capabilities, exec transformations, namespaces, and privilege decomposition.
- Linux man-pages project, [PR_SET_NO_NEW_PRIVS(2const)](https://man7.org/linux/man-pages/man2/PR_SET_NO_NEW_PRIVS.2const.html), current page checked 2026-09-04. Monotonic inheritance and prevention of exec-based privilege gains.
- Linux Kernel documentation, [Kernel Support for miscellaneous Binary Formats](https://docs.kernel.org/admin-guide/binfmt-misc.html), current page checked 2026-09-04. Magic and extension dispatch, interpreters, argument and credential flags, bound files, and namespace concerns.
- Linux man-pages project, [proc_pid_auxv(5)](https://man7.org/linux/man-pages/man5/proc_pid_auxv.5.html), current page checked 2026-09-04. Process auxiliary-vector exposure and permission control.
- Russ Cox, Frans Kaashoek, and Robert Morris, [*xv6: a simple, Unix-like teaching operating system*](https://pdos.csail.mit.edu/6.1810/2025/xv6/book-riscv-rev5.pdf), MIT, 2025 edition. Compact implementations of fork, page-table copying, exec validation and mapping, argument stack construction, commit, exit, and wait.

## Exercises

### Exercise 1

Design a failure-atomic process-creation sequence. Enumerate task storage, PID, credentials, files, address space, parentage, scheduling, audit, and publication, with an injected failure and unwind at every acquisition.

### Exercise 2

Write a validation specification for an ELF-like header table and load segments. Cover checked arithmetic, file bounds, memory size, address domain, page rounding, alignment, overlap, permissions, interpreter, and entry point.

### Exercise 3

Design a secure supervisor launch using descriptor-based execution. Cover path resolution, file integrity, status reporting, descriptor actions, arguments, environment, credentials, capabilities, namespaces, limits, signals, and audit.

### Exercise 4

Compare fork-plus-exec, clone-like creation, and spawn for a large multithreaded service launching short helpers. Include correctness, post-fork safety, page tables, COW, descriptor races, setup expressiveness, performance, and error semantics.

### Exercise 5

Construct an assurance review for loading a safety-critical control image. Separate format validation, cryptographic provenance, mapping permissions, dynamic dependencies, timing, rollback, fault injection, operational policy, and human judgment.

## Answers to the Exercises

### Answer 1

Reserve accounting and a namespace-scoped PID generation; allocate the task and kernel stack; acquire credentials and namespace references; copy or share filesystem, file-table, signal, limit, and cgroup domains; construct the child address-space metadata and COW page tables; initialize architecture registers, signal state, parent links, and audit identity; then insert into visible indexes and scheduler state. Define publication as the first point at which lookup or execution can succeed.

After each acquisition, inject failure. Unwind in reverse, never using full exit logic on state it assumes initialized. Before visibility, detach parent links, release page tables and mapping references, resource-domain references, stack and task storage, PID reservation, and charges. Test concurrent parent exit and signal without allowing a half-child to appear. After publication, normal child lifecycle owns all resources; parent and child receive their specified return values exactly once.

### Answer 2

Validate fixed header bytes before decoding variable tables. Check magic, class, endian, version, machine, type, header sizes, table count, and entry size. Establish `n × q ≤ F - h` with checked arithmetic. For each segment, establish `f_i ≤ m_i`, `o_i + f_i ≤ F`, nonwrapping `v_i + m_i`, canonical user addresses, resource bounds, and required `v_i mod a_i = o_i mod a_i` for valid alignment.

Compute page-rounded mapping intervals with checked floor and ceiling operations. Reject unauthorized overlap, null or kernel ranges, stack and interpreter collisions, and conflicting permissions; define boundary-page population so no file or allocator bytes leak. Require no writable-executable alias under policy. Validate the interpreter field's form, termination, recursion, identity, architecture, and authorization. Require entry inside an executable mapped interval with ABI alignment. Only after the full plan passes may allocation and mapping begin.

### Answer 3

Resolve beneath a trusted directory with explicit symlink, mount, and namespace policy; open the executable immutably or under write-denial; verify type, ownership, integrity signature or digest, and deployment identity on that file object. Create a close-on-exec status pipe and a child or spawn transaction. Default every unrelated descriptor to close-on-exec, then apply an explicit ordered allowlist for standard streams and service handles.

Build bounded arguments and a minimal allowlisted environment. Set working directory, root and namespaces, user and group IDs, capability sets, no-new-privileges, security policy, resource and process limits, affinity and scheduling, signal mask and dispositions, and cgroup placement in the reviewed order. Execute the validated descriptor. A successful exec closes the status channel; precommit failure sends a bounded structured error. The parent holds a stable process handle, audits executable identity and final policy, applies a startup deadline, and kills and reaps failed launches without PID races.

### Answer 4

Fork-plus-exec supports arbitrary child setup but, in a multithreaded service, only the caller survives with copied lock state; the child must use a narrow async-signal-safe path. It duplicates address-space metadata and page tables and creates later COW faults even if exec follows immediately. Concurrent descriptor creation needs atomic close-on-exec, and a status channel must distinguish exec failure.

Clone-like creation can share selected resources or use vfork-like parent suspension to avoid duplication, but unsafe memory sharing lets the child corrupt the parent and forbids ordinary stack or runtime behavior. Flag combinations and lifetime are complex. Spawn gives the implementation freedom to use efficient creation while exposing declarative attributes and file actions, reducing unsafe child code. It is preferred when its setup language suffices. Benchmark startup, page-table work, faults, resident growth, and tail latency under actual thread count and memory pressure; preserve equivalent descriptor, credential, signal, namespace, error, and audit semantics across comparisons.

### Answer 5

Specify accepted architecture and executable profile; formally or independently review every parser bound, integer width, segment, page rounding, zero-fill, entry, stack, interpreter, and permission rule. Verify image and dependency provenance through protected keys, reproducible build identity, revocation, immutable storage, and measured deployment. Prefer static or tightly pinned dependencies when the hazard analysis requires a closed image; otherwise inventory and authenticate the dynamic loader and every library.

Measure cold and warm load time, page faults, relocation, verification, storage failures, memory pressure, and deadline margins on deployed hardware. Fault-inject malformed images, missing dependencies, exhausted memory, corrupted signatures, descriptor leakage, power loss, and postcommit failure. Define atomic update, fallback image, safe-state behavior, audit, monitoring, and recovery drills. A named loader or kernel expert, build-provenance owner, security reviewer, real-time analyst, safety authority, independent verifier, and acceptance owner must assess coverage and residual risk. This chapter and two-segment model claim no external certification.
