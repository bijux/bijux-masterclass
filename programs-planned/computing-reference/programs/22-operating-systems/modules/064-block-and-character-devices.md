---
module_id: OS-064
program: Operating Systems
level: 2
module_number: 64
title: Block and Character Devices
status: complete
last_verified: 2026-09-04
---

# Block and Character Devices

## One-Page Review

### Governing question

How should an operating system expose devices through file-like interfaces while preserving the different semantics of character streams and controls versus addressable block storage, and while keeping naming, queuing, completion, caching, concurrency, errors, and removal correct?

### Essential definitions

- A **character device** exposes driver-defined operations, commonly a byte stream, message stream, control endpoint, or event source, through a file descriptor.
- A **block device** exposes addressable fixed-size logical blocks and participates in a storage stack that can split, merge, queue, cache, schedule, and complete I/O.
- A **device number** combines a major number selecting a driver or class with a minor number selecting an instance; it is routing metadata, not stable hardware identity.
- A **device node** is a filesystem special file whose type and device number route operations to a registered device.
- A **file operation** is an entry point such as open, read, write, poll, ioctl, mmap, flush, or release associated with an open file description.
- A **bio** describes a block I/O operation, target range, operation flags, memory vectors, status, and asynchronous completion.
- A **request** is a block-layer dispatch unit that can combine or transform bios for a hardware queue.
- **blk-mq** is Linux's multi-queue block I/O mechanism, connecting software submission queues to hardware dispatch queues and tagged requests.
- A **queue limit** states alignment, block-size, segment, boundary, operation, and transfer constraints that upper layers must respect.
- **quiescence** prevents new I/O and drains or resolves every operation that can reach device state before teardown.

### Central model, mechanism, or theorem

A device file is a capability to a live kernel object, not a direct reference to hardware. Opening resolves namespace and policy into an open-file context. Each operation must validate that context against interface semantics and lifecycle state, and final close releases per-open state independently of physical device removal.

For a block request $R=(o,s,n,v,f,c)$, correctness requires a supported operation $o$, aligned sector or byte range $(s,n)$ within capacity, a memory-vector set $v$ satisfying queue limits, flags $f$ whose durability and ordering meanings the stack preserves, and exactly one terminal completion $c$. For a character operation, the driver defines whether position, record boundaries, blocking, partial transfer, readiness, and control commands are meaningful; these cannot be inferred from the word “character.”

### Critical invariants

- Namespace lookup, device number, kernel object, physical identity, and open-file lifetime remain distinct.
- Registration publishes an interface only after operations can safely observe initialized state; removal stops new opens before revoking backing state.
- Every successful open has exactly one matching release of its per-open resources, even after disconnect.
- User buffers are accessed only through approved copy, iterator, pinning, or mapping APIs with partial-transfer and fault semantics preserved.
- Character drivers define offset, blocking, readiness, record, ioctl, and mmap behavior as a stable ABI.
- Block drivers advertise truthful capacity, logical and physical sizes, segment limits, supported operations, cache behavior, and topology.
- A submitted bio or request is immutable where the API requires and reaches exactly one terminal completion with accurate status.
- Flush, FUA, discard, zeroing, integrity, and zone operations are never silently reported as stronger than the device guarantees.
- Removal, reset, and timeout synchronize callbacks, queues, mappings, DMA, and open handles before final memory release.

### Common failures

Common mistakes are treating `/dev` names as identity, registering before state is ready, freeing state while files remain open, assuming character means unseekable or byte-at-a-time, holding a spinlock across `copy_to_user()`, inventing an unversioned ioctl ABI, returning readiness that immediately blocks, exposing unsafe device memory through mmap, reporting block capacity in the wrong unit, ignoring queue limits, modifying a submitted bio, completing twice, losing error precision, claiming flush or discard support falsely, accepting I/O during removal, and assuming device-node deletion closes existing file descriptors.

### Compact example

A block device advertises a four-sector maximum transfer and an eight-sector boundary. A request beginning at sector 14 for ten sectors cannot cross sector 16 and is split into `14+2`, `16+4`, and `20+4`. The arithmetic demonstrates constraint propagation only; a real block layer also checks logical-block alignment, segments, operation flags, capacity, DMA mapping, queue state, and completion.

### Connections

[OS-041](041-files-directories-and-namespaces.md), [OS-045](045-buffer-cache-and-page-cache.md), [OS-049](049-virtual-filesystem-layers.md), [OS-061](061-device-discovery-and-driver-models.md), [OS-063](063-direct-memory-access.md), and [OS-065](../ROADMAP.md) connect device interfaces to naming, caching, VFS dispatch, hardware lifecycle, DMA, and scheduling.

## Governing Question

Unix-like systems make devices accessible through file descriptors, but the abstraction is deliberately incomplete. A terminal, random-number source, accelerator control endpoint, disk, partition, and virtual volume can all appear beneath `/dev` while obeying radically different contracts.

The governing question is how to preserve the convenience of open, read, write, poll, ioctl, mmap, and close without erasing the semantics needed for safe device control and storage. Correct design begins with an explicit ABI and lifecycle, then chooses character, block, or a subsystem-specific interface because its semantics fit.

## Why This Matters

Device files cross the kernel trust boundary. They translate untrusted lengths, offsets, pointers, flags, and commands into privileged memory access and hardware operations. Their ABI can outlive the driver implementation for decades.

Block devices sit beneath filesystems, databases, swap, volume managers, encryption, and virtual machines. A false durability claim or incorrect completion can corrupt state far above the driver. Queue limits are correctness information, not optional performance hints.

Character devices are simpler only in the sense that they bypass the generic block stack. The driver must define buffering, concurrency, readiness, cancellation, and record semantics itself. A compact implementation can still carry a permanent and security-sensitive userspace contract.

## Prerequisites and Retrieval

Review [OS-003](003-system-calls-and-user-kernel-transitions.md), [OS-007](007-kernel-data-structures.md), [OS-009](009-kernel-modules-and-drivers.md), [OS-026](026-pipes-and-byte-streams.md), [OS-031](031-address-translation.md), [OS-041](041-files-directories-and-namespaces.md), [OS-045](045-buffer-cache-and-page-cache.md), [OS-049](049-virtual-filesystem-layers.md), [OS-054](054-kernel-read-copy-update.md), [OS-061](061-device-discovery-and-driver-models.md), [OS-062](062-memory-mapped-and-port-mapped-i-o.md), and [OS-063](063-direct-memory-access.md).

Retrieve these distinctions:

- pathname, device node, device number, kernel device object, driver binding, and hardware identity are separate layers;
- an inode represents a special file while a file object represents one open description and its position and private state;
- removal of namespace reachability does not invalidate already open descriptions automatically;
- user copying can sleep and partially succeed, so locking and return conventions matter;
- a block logical address, byte offset, page vector, bio, request, DMA segment, and hardware command are different representations;
- submission transfers ownership and completion returns it under the subsystem contract;
- data transfer completion, cache persistence, and durable media commitment are different events;
- character, block, network, input, graphics, and other subsystem interfaces encode distinct policies.

## Learning Objectives

After this module, you should be able to:

1. distinguish character and block semantics from device nodes, numbers, classes, names, and physical topology;
2. design character open, read, write, seek, poll, ioctl, mmap, flush, and release behavior as a stable ABI;
3. trace block I/O from a bio through splitting, merging, request allocation, blk-mq dispatch, DMA, and completion;
4. specify capacity, block sizes, alignment, segment, boundary, cache, discard, integrity, and zoning constraints truthfully;
5. preserve partial-transfer, blocking, readiness, cancellation, error, and durability semantics across layers;
6. coordinate references, queues, callbacks, open handles, reset, suspend, and hot-unplug during teardown;
7. verify device interfaces with ABI tests, fault injection, model devices, stress, tracing, and retained evidence.

## Core Exposition

### Start from semantics

Choose an interface by the operations users need. A byte or message stream, event queue, control plane, or small device-specific endpoint can suit a character device. Randomly addressable storage intended for filesystems or stacking belongs in the block layer.

Do not use a character device merely because it is easier to register. Reimplementing storage alignment, caching, scheduling, writeback, statistics, partitioning, and stacking behind ad hoc reads and writes creates an incompatible shadow block layer.

### The file abstraction

Opening a device node resolves the pathname to an inode and its encoded device type and number. The VFS dispatches to registered operations and creates an open file description with flags, position, credentials context, and driver-private state.

File descriptors can be duplicated or inherited while sharing the open description. A driver must decide which state belongs to the device, which belongs to one open description, and which belongs to one operation.

### Device numbers

Major and minor numbers route opens to registered device ranges. Dynamic allocation avoids local conflicts; stable public assignments require coordination. The character and block number spaces are distinct.

Numbers are not serial numbers or persistent identity. Userspace policy can create meaningful symlinks from topology and attributes, while the kernel number can change across boots.

### Device nodes and classes

Registration of a kernel interface and creation of a filesystem node are separate events. Device classes and userspace device managers commonly coordinate sysfs attributes, events, permissions, and `/dev` nodes.

Deleting a node prevents future pathname opens but does not close existing descriptors. Conversely, a stale node can exist when no matching device is registered and its open must fail safely.

### Publish-after-ready

Initialize locks, queues, buffers, device state, callbacks, identifiers, and power before making a cdev, disk, or class interface reachable. Any registration call that can trigger userspace observation is a publication boundary.

On failure, reverse every published layer. During removal, reverse reachability first: block new opens and submissions, mark disconnected, then drain work before freeing storage.

### Character device registration

Linux character drivers allocate or reserve a device-number range, initialize a `cdev` with file operations and owner, and add it to the system. Combined device helpers can couple a cdev with a device-model object.

After `cdev_add()`, operations can run immediately. Therefore the containing object and operation table must already be valid, and their lifetime must extend past every open file.

### Misc devices

The miscellaneous-device framework can allocate a minor and simplify registration for suitable small character interfaces. It does not define the ABI, concurrency, or teardown policy.

Use the subsystem that best represents the function. A misc device should not replace established input, TTY, media, graphics, watchdog, hardware-monitoring, or other frameworks merely to reduce code.

### Open

Open validates instance state, access mode, exclusivity, credentials, and resource availability, then takes references and constructs per-open context. It can start hardware only when the ABI promises that behavior.

Serialize open against disconnect. If removal wins, fail without publishing a context. If open wins, removal must retain the backing object and make later operations observe a defined disconnected result.

### Per-open state

Use per-open state for cursors, subscriptions, partial records, authorization snapshots where appropriate, outstanding asynchronous requests, and references. Store it in the file's private field under clear ownership.

Do not put one client's cursor or mode in global device state unless sharing is the documented ABI. Duplicated file descriptors intentionally share an open description and therefore its file position and private state.

### Release and flush

Release runs when the final reference to the open file description closes, not necessarily for every `close()` system call. It frees per-open resources and drops the device reference.

Flush has different invocation semantics and is not a substitute for release. Define whether close waits for output, reports delayed errors, cancels operations, or merely drops the caller's handle.

### Character reads

Define whether reads return a byte stream, one record, multiple records, snapshots, or events. State minimum sizes, truncation policy, EOF meaning, blocking, interruption, and behavior after disconnect.

Return the number of bytes actually transferred. If some bytes succeeded before a later fault or interruption, partial progress commonly takes precedence over an error; follow the specific ABI and iterator helpers.

### Character writes

Define atomicity, buffering, framing, backpressure, partial acceptance, validation, and when hardware consumes data. A successful copy into a kernel queue is not necessarily device completion or durable output.

Validate lengths and arithmetic before allocation or copy. Never let an untrusted count overflow a command size, ring index, or device field.

### User memory access

User pointers cannot be dereferenced directly. Use `copy_to_user()`, `copy_from_user()`, iterators, or subsystem helpers and interpret their return convention correctly.

User access can fault and sleep. Do not hold a spinlock, disable interrupts, or retain an inconsistent device transaction across a potentially faulting copy. Stage data in a kernel buffer or use a suitable pinning model.

### File position and seeking

A character device can support meaningful offsets, reject seeking, or implement a domain-specific position. “Character” does not force one answer.

Use VFS helpers for fixed-size or no-seek behavior. Validate negative, overflowing, and sparse offsets, and serialize position-sensitive operations where shared descriptions require it.

### Blocking and nonblocking operation

Blocking reads and writes sleep on a condition while holding references but not spinlocks. Recheck the condition in a loop after wakeup because signals, spurious wakes, competing readers, and disconnect can change state.

With nonblocking mode, return the defined would-block error when no progress is possible. If some progress occurred, return that progress under the ABI rather than hiding it.

### Wait queues

Update the state that makes an operation ready under its lock, then wake waiters with the ordering required by the wait-queue pattern. The waiter prepares to sleep and rechecks the predicate to avoid lost wakeups.

Disconnect and error transitions also wake waiters. No blocked operation should wait forever for hardware that has been removed.

### Poll readiness

Poll registers the appropriate wait queues and returns a level description of operations that would make progress without blocking now. Readable, writable, priority, hangup, and error conditions have distinct meanings.

Returning readable with no data creates busy loops; failing to report hangup can strand event loops. Readiness can change immediately after poll, so the subsequent operation must still handle races.

### Ioctl interfaces

Ioctl supports commands that do not fit read, write, or standard subsystem operations. It is flexible and therefore easy to make permanently brittle.

Use standard encoding macros, fixed-width UAPI types, explicit padding, reserved zero fields, size checks, version or capability discovery, compatible 32-bit handling, and defined unknown-command errors. Never embed kernel pointers or architecture-sized layout accidentally.

### Prefer established operations

Use read/write for data, poll for readiness, mmap for mappings, sysfs for simple device attributes, and netlink or a subsystem API for structured control when appropriate. Do not place every function behind ioctl.

An ABI should describe semantics rather than mirror internal structs or hardware registers. This permits implementation and device revisions without breaking applications.

### Memory mapping

A character device may map buffers or device apertures into userspace only under an explicit protection and lifetime model. Validate offset, length, alignment, permissions, cache attributes, and whether pages may be inherited or dumped.

VMA open, close, and fault callbacks can outlive the original file operation. Removal must revoke or fault future access safely; closing the file does not necessarily destroy mappings.

### Asynchronous notification

Character devices can integrate poll, signals, eventfd, or asynchronous-I/O mechanisms. Each notification is a hint to inspect authoritative state, not permission to assume one operation completed.

Coalescing and races are normal. Use counters, sequence numbers, or queues so notifications do not lose semantic events.

### Concurrency model

List all callers: process-context operations, interrupt handlers, workers, timers, power callbacks, reset, and removal. Assign locks and ownership by invariant, not by callback name.

Avoid a single lock held across user copies, hardware waits, or callbacks into other subsystems. Preserve lock order and make per-open versus device-wide serialization explicit.

### Character error model

Distinguish invalid request, permission denial, would-block, interruption, timeout, disconnected device, protocol error, data loss, and permanent failure. Preserve partial byte counts when the ABI requires.

Sticky errors can be stored per open or device, but define when they are consumed. Do not translate every hardware failure into a generic I/O error if a stable more precise result exists.

### Block address space

A block device exports a finite capacity in logical sectors or blocks. Linux commonly expresses block-layer positions in 512-byte sectors even when the device's logical block size differs.

Convert units explicitly and check multiplication, addition, alignment, and end-of-device bounds. Capacity publication must match the ranges the driver can actually complete.

### Logical and physical block sizes

The logical block size is the minimum addressable unit exposed to upper layers. The physical block size and minimum or optimal I/O sizes describe underlying media or topology.

Misreporting these values causes invalid requests, read-modify-write amplification, or alignment loss in filesystems and partitions. Hints must be truthful and stable for the device lifetime.

### The bio

A bio describes an operation and memory vectors directed at a block device. It carries sector, size, operation and flags, status, and an asynchronous end-I/O callback.

After submission, the caller must not touch it until completion transfers ownership back under the API. Biovecs remain immutable while iterators represent splitting and partial progress.

### Bio vectors

Bio vectors identify pages, offsets, and lengths rather than requiring one kernel virtual mapping. Iterator helpers present the correct subrange after splitting or cloning.

Drivers use the supported iterator for the representation they receive. “All segments” helpers have restrictions and can be wrong for a cloned or split bio.

### Stacking

Virtual block drivers remap, clone, split, aggregate, encrypt, replicate, or transform bios before forwarding them. Each layer preserves operation flags, completion, accounting, limits, and errors.

Queue limits compose conservatively. A stacked device cannot advertise a transfer or durability capability stronger than every possible lower path supports.

### Requests

The block layer can merge bios into a request that fits one device command. The request is a dispatch and completion object, not a stable copy of userspace input.

Use accessors for operation, position, bytes, segments, and flags rather than depending on internal layout. Map request data for DMA only after the request is owned by the driver.

### blk-mq architecture

blk-mq uses per-CPU or software-context submission queues and one or more hardware dispatch queues. Tags identify outstanding requests and enable parallel hardware queues.

The queue callback either accepts a request, reports a defined resource condition, or completes it as required. Returning success transfers responsibility for exactly one eventual completion.

### Queue limits

Set maximum sectors, segments, segment size, boundary masks, DMA alignment, logical and physical sizes, discard limits, and other capabilities before publishing the disk.

The block layer uses limits to split and merge, but drivers still validate hardware descriptor conversions. Limits can change only through supported synchronization with no incompatible in-flight requests.

### Request splitting and merging

Splitting turns a larger logical operation into children that each satisfy limits. Merging combines compatible adjacent work to reduce overhead.

Both transformations must preserve operation flags, ordering, integrity, accounting, and final completion. A parent completes only after all children terminate, with a defined error aggregation rule.

### Dispatch and backpressure

Hardware queues have finite tags, descriptors, credits, and controller slots. Temporary shortage returns the block-layer resource status that arranges retry; it is not a successful submission.

Stop and restart hardware queues through supported mechanisms. Avoid private busy loops or accepting a request that cannot be tracked to completion.

### DMA mapping

Map request segments through the DMA API with direction derived from the block operation. The mapped scatter list can differ from the bio or request vectors.

Check mapping failure, program returned DMA addresses and lengths, and unmap with exact original parameters after completion or contained abort. OS-063 supplies the full ownership proof.

### Completion

Complete every accepted request exactly once with the most accurate block status. Completion returns tags, unblocks upper layers, releases DMA ownership, and can run callbacks in constrained contexts.

Synchronize normal interrupt completion with timeout, reset, and removal using request states or atomic ownership. Double completion is memory corruption; missing completion is permanent resource loss.

### Partial completion

Modern drivers usually complete requests at a defined granularity through supported helpers. If hardware reports partial success, preserve the successfully transferred extent and accurate residual or error semantics expected by the subsystem.

Never advance internal vectors by modifying immutable bio data. Use iterators and completion APIs so stacked layers see a consistent result.

### Read and write semantics

Reads return data associated with the addressed logical range or an error. Writes can complete at several layers: accepted by the driver, received by the device, stored in volatile cache, or committed to nonvolatile media.

The block stack's flags and cache model communicate which level is required. A driver must not report completion early if doing so violates the advertised contract.

### Flush and FUA

A cache flush orders and drains prior writes according to the storage contract. Force Unit Access requests particular writes reach nonvolatile storage without remaining only in a volatile cache.

Advertise and translate these capabilities accurately through every stacked layer. A no-op flush on a volatile write-back cache creates silent durability failure.

### Discard and write zeroes

Discard communicates that logical ranges are no longer needed; it does not universally promise reads return zeros. Write-zeroes requests promise zero-read semantics under their operation contract and may be optimized internally.

Publish granularity, alignment, maximum ranges, segment count, and zeroing behavior. Treat these operations as untrusted range requests and check capacity arithmetic.

### Data integrity

Integrity metadata can protect data and address information across memory, transport, controller, and media. The block integrity framework associates metadata payloads and profiles with bios and queues.

Stacked devices must transform or propagate metadata consistently. Silently dropping integrity information while reporting success defeats the end-to-end claim.

### Zoned devices

Zoned storage restricts writes in sequential zones and exposes operations such as zone append, reset, open, and close. Queue limits describe zone size, write granularity, and open or active limits.

A conventional block abstraction remains, but arbitrary overwrite assumptions no longer hold. Filesystems or translation layers must obey the zone state machine.

### Partitions

Partitions provide subranges of a disk with translated addresses and identity. The core can scan partition tables and create child block devices.

Drivers expose the whole-device capacity and geometry honestly; they do not trust on-media partition metadata as privileged instructions. Removal invalidates partitions before the containing disk disappears.

### Page cache and direct I/O

Buffered filesystem I/O interacts with the page cache and writeback before becoming bios. Direct I/O bypasses parts of that path but still obeys alignment, pinning, block, DMA, and completion rules.

The device driver sees block requests rather than a universal distinction between application APIs. Cache coherence between buffered, mapped, and direct access is enforced by upper layers and invalidation protocols.

### Device-mapper and virtual disks

Logical volumes, encryption, snapshots, thin provisioning, loop devices, network block devices, and virtual-machine disks present block semantics without one local physical disk.

They still owe truthful limits, error propagation, ordering, flush semantics, teardown, and exactly-once completion. Network uncertainty or backing-file recursion adds failure modes rather than weakening the interface contract.

### Block versus character selection

Use block when the central abstraction is an addressable storage range consumed by filesystems or block stackers. Use character when operations are stream-, message-, event-, control-, or device-specific.

Many physical devices expose several interfaces: a block data path plus a character management endpoint, or a subsystem node plus sysfs attributes. Keep authority and ABI boundaries clear rather than forcing everything through one node.

### Security

Check access through normal filesystem permissions plus capability or policy checks for privileged operations. Do not rely on an obscure node name.

Validate user sizes, offsets, flags, ioctl layouts, mapped ranges, device-returned lengths, and all arithmetic. Clear data before exposing newly allocated buffers and prevent stale device content from crossing tenants.

### Removal with open handles

Removal first stops new opens and block submissions, marks the object disconnected, and unpublishes nodes or disks. Existing character files retain memory references but operations return defined errors or drain buffered data.

Freeze or quiesce block queues, fail or finish outstanding requests, stop DMA and interrupts, synchronize workers and mappings, and release hardware resources. Final object memory waits for open, VMA, request, and callback references.

### Suspend and reset

Suspend coordinates upper-layer freezing, queue quiescence, cache flush where required, outstanding I/O, wake policy, and power. Resume restores hardware and queue state before accepting work.

Reset serializes with dispatch and completion, marks affected requests, reinitializes queues, and prevents old completions from terminating reused tags. Character operations observe the same generation or recovery state.

### Observability

For character devices record opens, active contexts, queue depth, wait reasons, partial transfers, readiness transitions, commands, timeouts, disconnects, and ABI versions without leaking payloads.

For block devices record operations, bytes, latency distributions, queue and tag, merges, splits, retries, mapped segments, status, timeouts, resets, flushes, discards, limits, and outstanding requests. Correlate submission and completion by stable generation-aware identifiers.

### Verification

Test character ABIs with invalid pointers, every size boundary, short copies, signals, nonblocking mode, poll races, duplicated descriptors, 32-bit compatibility, mmap lifetime, concurrent opens, reset, and removal.

Test block drivers with a model device, fault injection, malformed completions, mapping failures, every queue limit, mixed operations, flush and FUA, power loss, timeout, reset, stacked devices, filesystem stress, integrity checks, and hot-unplug. Preserve exact configurations and negative results.

## Definitions and Notation

Let a device publication be $D=(t,r,k,l)$, where $t$ is character or block type, $r$ is routing identity, $k$ is the referenced kernel object, and $l$ is lifecycle generation. Let an open context be $F=(k,m,p,x)$ for access mode $m$, position $p$, and private state $x$.

A character operation is $C=(o,b,n,p,f)$ with operation $o$, user buffer or argument $b$, requested extent $n$, position $p$, and flags $f$. Its result is a byte count or stable error under the ABI; a positive partial count must not be conflated with total requested success.

A block operation is $R=(o,s,n,V,f,g)$ with operation, starting sector, byte or sector extent, memory vectors, flags, and generation. It is admissible only when

$$
0 \le s, \qquad s+n \le \text{capacity}, \qquad R \models Q,
$$

where $Q$ is the complete queue-limit and operation contract. Accepted work transitions `allocated -> prepared -> queued -> dispatched -> in-flight -> completing -> terminal`; exactly one path owns each transition.

## Mechanisms, Invariants, or Proof Structure

A reviewable device interface discharges these obligations:

1. **Semantic fit:** justify character, block, or subsystem selection from the user-visible contract.
2. **Identity:** separate name, device number, class, topology, physical identity, and generation.
3. **Publication:** initialize all reachable state before registration and remove reachability before teardown.
4. **Open lifetime:** pair every successful open reference and per-open allocation with final release.
5. **ABI:** define position, partial I/O, blocking, readiness, commands, mappings, errors, and compatibility.
6. **Bounds:** validate every user range, capacity calculation, conversion, queue limit, and hardware field.
7. **Ownership:** transfer character queue, bio, request, DMA, tag, and buffer ownership explicitly.
8. **Ordering:** preserve data, descriptor, flush, FUA, integrity, and completion relations through every layer.
9. **Progress:** bound waits and retries, apply backpressure, and guarantee one terminal result.
10. **Concurrency:** serialize operation, interrupt, timeout, reset, power, and removal state transitions.
11. **Revocation:** stop new access and drain callbacks, mappings, DMA, requests, and open users before free.
12. **Evidence:** test ABI, limits, faults, stacking, durability, architecture, lifecycle, and adversarial inputs.

The proofs remain separate. A device node proves namespace reachability, not hardware presence. An open reference proves object lifetime, not operational readiness. Queue acceptance proves ownership transfer, not device completion. A completed write proves only the durability level promised by flags and cache configuration.

## Alternatives and Trade-Offs

- **Character versus block:** character permits domain-specific behavior; block supplies storage composition, caching, queues, limits, and filesystems.
- **Subsystem framework versus raw cdev:** a framework adds policy and interoperability; a raw cdev offers flexibility and a larger ABI burden.
- **Static versus dynamic numbers:** static allocation aids legacy compatibility; dynamic allocation avoids conflicts and pairs with discovery-based naming.
- **Stream versus records:** streams allow arbitrary partial reads; records preserve message boundaries and need truncation rules.
- **Blocking versus nonblocking:** blocking simplifies sequential clients; nonblocking integrates event loops and requires precise readiness.
- **Read/write versus ioctl:** standard data operations compose well; ioctl fits controls but is easy to freeze into a brittle ABI.
- **Copy versus mmap:** copying simplifies ownership and revocation; mmap can reduce copies while extending lifetime and fault complexity.
- **One device lock versus per-open and queue locks:** one lock simplifies invariants; finer ownership improves concurrency and expands ordering analysis.
- **Bio forwarding versus request-based dispatch:** bio forwarding suits simple stacking; blk-mq requests fit hardware queues, tags, merging, and scheduling.
- **Single versus multiple hardware queues:** one queue simplifies reset; multiple queues scale and require affinity and cross-queue lifecycle control.
- **Immediate versus batched completion:** immediate completion lowers latency; batching reduces overhead and can delay error visibility.
- **Write-through versus write-back cache:** write-through simplifies durability; write-back improves throughput and requires truthful flush and FUA.
- **Fail versus requeue on shortage:** failure bounds latency; requeue absorbs transient resource pressure but needs fairness and progress.
- **Physical versus virtual block device:** physical drivers face hardware protocols; virtual drivers inherit stacking, recursion, and lower-layer uncertainty.

## Failure Modes and Misconceptions

- **“Everything under `/dev` has file semantics.”** Each device ABI defines which operations and guarantees exist.
- **“The node name identifies hardware.”** Names and numbers are routing and policy artifacts.
- **“Removing the node closes users.”** Existing files and mappings can outlive namespace removal.
- **“`release` runs for every close call.”** It follows the final open-file-description reference.
- **“Character means byte-at-a-time and unseekable.”** The driver defines records, position, and transfer units.
- **“A successful copy means hardware completed.”** It may mean only that a kernel queue accepted bytes.
- **“Poll readiness promises the next call succeeds.”** State can race; readiness is level information at one instant.
- **“Ioctl structs can mirror kernel structs.”** UAPI layout must be stable across versions and word sizes.
- **“Closing a file revokes every mmap.”** VMAs have independent references and callbacks.
- **“A block sector always equals the physical block.”** Address units and device granularities differ.
- **“Queue limits are tuning hints.”** They prevent unrepresentable and unsafe requests.
- **“Submitted bios remain caller-owned.”** Submission transfers access until end-I/O.
- **“One bio becomes one command.”** splitting, merging, stacking, and scheduling transform work.
- **“An interrupt means success.”** Status and request identity must be validated.
- **“Write completion means durable media.”** Volatile caches require flush or FUA semantics.
- **“Discard means reads return zero.”** Only an explicit zeroing guarantee supports that claim.
- **“Timeout ends the request.”** Hardware and DMA may remain active until recovery contains them.
- **“Unregister permits immediate free.”** Open files, requests, VMAs, and callbacks can retain state.

## Worked Examples

### Example 1

A sensor cdev allocates per-open subscription state. Reads return whole timestamped records, reject undersized buffers without consuming a record, and wake with disconnected status after hot-unplug.

### Example 2

A command endpoint supports nonblocking writes. It returns the accepted byte count when queue capacity remains, returns would-block with zero progress, and reports device completion separately through pollable result records.

### Example 3

An ioctl uses fixed-width fields, explicit padding required to be zero, a structure size, flags, and reserved space. The compatibility path converts pointers explicitly and rejects unknown flags.

### Example 4

A device VMA remains after the original file closes. Its object reference keeps metadata alive, while disconnect marks future faults invalid and revokes the hardware mapping before registers are released.

### Example 5

A filesystem submits a bio spanning pages. A stacked encryption target clones and remaps it, the block layer splits it at a queue boundary, and the driver converts resulting request segments into DMA descriptors.

### Example 6

A four-queue NVMe-like device maps software contexts to hardware queues. Tags identify requests; timeout and interrupt paths atomically arbitrate completion so each tag is returned once.

### Example 7

A virtual disk reports a 4 KiB logical block size and a 128 KiB optimal size inherited from its lower stripe. Misaligned 512-byte writes are rejected or handled above rather than silently truncated.

### Example 8

A write-back device completes ordinary writes from volatile cache. A database issues a flush between log and metadata epochs; the driver reports completion only after the device confirms the required persistence order.

### Example 9

During hot-unplug, a block driver freezes new submission, fails queued but undispatched requests, contains DMA for in-flight commands, synchronizes interrupts, completes every request once, and keeps disk metadata alive for remaining opens.

### Example 10

The following pure calculation splits a ten-sector request by a four-sector maximum and an eight-sector boundary. It does not create bios, apply all queue limits, perform DMA, dispatch hardware, or prove completion.

<!-- bijux-verify: {"id":"block-request-splitting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"request=14+10\nsegment=14+2\nsegment=16+4\nsegment=20+4\ntotal=10\n","stderr":""}} -->
```python
def split_request(start, count, maximum, boundary):
    result = []
    cursor = start
    remaining = count
    while remaining:
        to_boundary = boundary - (cursor % boundary)
        length = min(remaining, maximum, to_boundary)
        result.append((cursor, length))
        cursor += length
        remaining -= length
    return result

segments = split_request(start=14, count=10, maximum=4, boundary=8)
print("request=14+10")
for sector, length in segments:
    print(f"segment={sector}+{length}")
print(f"total={sum(length for _, length in segments)}")
```

## Cross-Program Connections

[Database Engineering](../../18-database-engineering/ROADMAP.md) connects block geometry, caches, persistence, integrity, storage layout, write-ahead logging, and failure. [Security Engineering](../../25-security-engineering/ROADMAP.md) connects device-node permissions, ioctl validation, DMA isolation, stale data, revocation, and least privilege.

[Software Engineering Patterns](../../11-software-engineering-patterns/ROADMAP.md) connects adapters, stable interfaces, ownership, state machines, queues, and resource acquisition. [Systems Engineering](../../26-systems-engineering/ROADMAP.md) contributes interface contracts, hazard analysis, fault containment, traceability, and assurance. Within this program, [OS-063](063-direct-memory-access.md) develops DMA and [OS-065](../ROADMAP.md) develops I/O scheduling.

## References

- Linux kernel documentation, [Multi-Queue Block IO Queueing Mechanism](https://docs.kernel.org/block/blk-mq.html), current page checked 2026-09-04. Bios, requests, software and hardware queues, tags, dispatch, completion and resource states.
- Linux kernel documentation, [The Linux Kernel API](https://docs.kernel.org/core-api/kernel-api.html), current page checked 2026-09-04. Character-number allocation, cdev publication, bios, submission, polling and block helpers.
- Linux kernel documentation, [Immutable Biovecs and Biovec Iterators](https://docs.kernel.org/block/biovecs.html), current page checked 2026-09-04. Bio vector immutability, iterators, splitting, partial completion and helper constraints.
- Linux kernel documentation, [Data Integrity](https://docs.kernel.org/block/data-integrity.html), current page checked 2026-09-04. Integrity payloads, profiles, block-layer propagation and stacking.
- Linux kernel documentation, [Overview of the Linux Virtual File System](https://docs.kernel.org/filesystems/vfs.html), current page checked 2026-09-04. Inodes, files, file operations, open descriptions, read, write, seek, mmap and lifecycle.
- Linux kernel documentation, [Locking](https://docs.kernel.org/filesystems/locking.html), current page checked 2026-09-04. File-operation and VMA callback contexts and locking rules.
- Linux kernel documentation, [Ioctl Based Interfaces](https://docs.kernel.org/driver-api/ioctl.html), current page checked 2026-09-04. Command encoding, UAPI data types, compatibility, extensibility and error conventions.
- Linux kernel documentation, [Linux Allocated Devices](https://docs.kernel.org/admin-guide/devices.html), current page checked 2026-09-04. Character and block major/minor registries, device-node conventions and public allocation policy.
- Linux kernel documentation, [Miscellaneous Devices](https://docs.kernel.org/driver-api/misc_devices.html), current page checked 2026-09-04. Misc-device registration, dynamic minors, open routing and deregistration.
- Linux kernel documentation, [Device Drivers Infrastructure](https://docs.kernel.org/driver-api/infrastructure.html), current page checked 2026-09-04. Device objects, class publication, references, attributes, lifecycle and userspace visibility.

## Exercises

### Exercise 1

Design a record-oriented character device for timestamped measurements. Specify registration, open state, blocking and nonblocking reads, poll, ioctl configuration, errors, duplicated descriptors, reset and hot-unplug.

### Exercise 2

Design a blk-mq driver for a device with four hardware queues, 128 tags each, 4 KiB logical blocks, a 1 MiB maximum transfer, 64 segments, a volatile write cache, discard and integrity metadata.

### Exercise 3

Trace one 3 MiB filesystem write through bios, a snapshot layer, an encryption layer, queue-limit splitting, requests, DMA mapping, device cache, flush and final completion.

### Exercise 4

Model removal while character files and VMAs remain open and block requests are queued, DMA-active, timed out, and completing on other CPUs.

### Exercise 5

Build a verification and assurance plan for one driver that exposes a block data interface and a character management interface.

## Answers to the Exercises

### Answer 1

Allocate a dynamic device range, initialize device locks, bounded record queue, wait queue, configuration, sequence counter, disconnected state, references and file operations, then publish the cdev and class device last. Open checks lifecycle and access policy under the device lock, takes a reference, and allocates a per-open subscription containing the next sequence, filters, overflow state and authorization. Duplicated descriptors share that open context by design.

Read requires space for one complete record; an undersized buffer returns a documented error without consumption. With no matching record, nonblocking mode returns would-block, while blocking mode sleeps on a predicate that includes data, overflow, error and disconnect. Copy outside the spinlock from a stable staged record, then atomically advance the cursor. Poll registers the same wait queue and reports readable, error, or hangup from the same predicates. Versioned fixed-width ioctls update per-open filters after validation. Reset increments a device generation and reports a discontinuity. Hot-unplug unpublishes, marks disconnected, wakes all waiters, stops production and retains state until opens and VMAs release.

### Answer 2

Negotiate DMA and initialize a blk-mq tag set with four hardware queues and queue depth 128, while allowing reserved tags for recovery if needed. Allocate the disk, set capacity in the block layer's expected sector unit, and publish limits before adding it: 4096-byte logical and physical sizes as truthful, 1 MiB maximum transfer, 64 maximum segments plus actual segment size and boundary limits, discard granularity and maximums, integrity profile, and write-back cache with real flush and FUA support.

The queue callback validates the operation, starts the request, maps its segments for DMA, and either returns a resource status before acceptance or programs a free hardware command and accepts exactly one completion obligation. Interrupt completion validates tag and generation, stops DMA ownership, unmaps, maps hardware status to precise block status, and ends the request once. Timeout arbitrates ownership with completion and begins bounded recovery. Flush orders prior writes to nonvolatile media; discard never promises zero reads unless supported. Teardown freezes and quiesces queues, resolves every tag, synchronizes callbacks, deletes the disk, frees the tag set, and releases device state.

### Answer 3

The filesystem and page cache form bios describing the 3 MiB logical range, memory vectors, write operation, and durability flags. The snapshot target first preserves old extents or redirects new data according to its copy-on-write invariant. The encryption layer clones or transforms bios while preserving logical ordering, errors and integrity context. Each layer constrains limits by the lower path. The block layer splits the write into requests no larger than 1 MiB and further at segment, boundary, alignment, snapshot, or encryption-unit constraints.

The driver maps request segments for DMA, publishes descriptors before doorbells, and accepts completion ownership. The device may acknowledge data into volatile cache; ordinary request completion then satisfies only that advertised level. When the filesystem submits the required flush, every stacking layer forwards or implements the barrier, and the physical driver completes it only after the device confirms prior writes meet the persistence contract. Child errors aggregate into the parent result without reporting unwritten ranges as successful. Only after all children and the flush terminate can the filesystem treat the requested persistence point as complete.

### Answer 4

Removal first atomically marks the shared device disconnected, deletes or disables new character and block reachability, wakes character waiters, and freezes block submission. Existing character files retain the object but new operations return disconnected or drain already committed records under the ABI. VMAs hold separate references; fault callbacks reject new device access, and existing device mappings are revoked or invalidated before hardware resources disappear.

Queued but undispatched block work completes with a removal status. DMA-active work is contained through device stop, bus mastering control and IOMMU revocation before unmap. Timeout and interrupt paths use an atomic request state and generation so only one owns final completion; both synchronize before tags or memory are reused. Cancel timers and workers, mask and synchronize interrupts, finish all request callbacks, revoke mappings, release hardware resources, and drop the registration reference. Final memory release waits for all files, VMAs, requests, callbacks and diagnostic references. If active DMA cannot be proven contained, quarantine its backing memory rather than free it.

### Answer 5

Specify the common hardware lifecycle, reference graph, reset generation, privilege model and lock order, then define two separate ABIs. For block, record capacity units, logical and physical sizes, limits, operations, cache and durability semantics, integrity, DMA, timeout and completion. For character management, record command encodings, fixed-width layouts, compatibility, permissions, blocking, poll, mmap, partial results and disconnect behavior. Prove management reset and firmware operations serialize with block submission and cannot expose a half-configured device.

Test every registration failure and publication race, concurrent open and I/O, invalid pointers and sizes, all ioctl bits, 32-bit compatibility, duplicated files, mmap-after-close, queue limits, mapping failure, tag exhaustion, split and merged I/O, flush, FUA, discard, integrity, corrupted completions, timeout, reset, suspend and hot-unplug. Run filesystems and destructive block tests only on isolated media. Enable DMA and lock debugging, inject faults, and trace generation-aware submission and completion. Preserve source, kernel, firmware, hardware, topology, queue configuration, seeds, traces, power-loss method, negative results and limitations; passing functional I/O alone does not prove ABI stability or durability.
