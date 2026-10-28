---
module_id: OS-073
program: Operating Systems
level: 2
module_number: 73
title: Network Buffers
status: complete
last_verified: 2026-09-04
---

# Network Buffers

## One-Page Review

### Governing question

How should an operating system represent, share, transform, queue, charge, map, recycle, and destroy network packet buffers so that high-rate paths avoid unnecessary copies without permitting stale metadata, out-of-bounds access, double release, unbounded memory, or mutation through shared storage?

### Essential definitions

- A **socket buffer (SKB)** is Linux's packet metadata object; its bytes can reside in a linear head, page fragments, and a fragment list rather than inside the metadata structure itself.
- **Headroom** is unused space before current packet data in the linear allocation; **tailroom** is unused space after the linear tail and before the allocation end.
- **Linear length** is the byte count directly addressable between data and tail; **nonlinear length** is data in page fragments or fragment lists.
- A **clone** allocates distinct SKB metadata while sharing packet data; a **copy** allocates private packet data as well.
- **Copy-on-write (COW)** makes a required portion private and writable only when sharing or insufficient space makes copying necessary.
- **`truesize`** is an accounting estimate of memory consumed on behalf of an SKB, not merely its payload length.
- A **page pool** supplies and recycles DMA-compatible receive memory while tracking pages that remain in flight.
- **Netmem** abstracts packet memory that may not be CPU-readable or backed by an ordinary `struct page`.
- A **destructor** performs owner-specific release or accounting when the SKB's lifetime ends.
- **Zero-copy notification** tells an application when referenced send memory can be reused under the interface; it does not prove peer receipt.

### Central model, mechanism, or theorem

Represent a buffer as

$$
B=(m,H,F,L,D,O,R,A,C,G),
$$

where $m$ is mutable SKB metadata, $H$ the linear head allocation, $F$ nonlinear fragments, $L$ validated geometry, $D$ DMA state, $O$ mutable ownership, $R$ reference graph, $A$ accounting owner and charge, $C$ checksum and protocol metadata, and $G$ aggregation or segmentation state. Metadata reference count and shared-data reference count are distinct. One SKB can die while clones retain $H$ and $F$; one fragment can outlive every original receive descriptor.

The governing rule is that transformation requires both geometric validity and write authority. Pushing a header needs headroom and a writable head. Modifying payload needs private writable backing. Passing to DMA requires mapped, stable bytes. Recycling requires no remaining consumer and correct synchronization. Final release uncharges and invokes each backing store's completion exactly once.

### Critical invariants

- Current data, tail, end, total length, nonlinear length, header offsets, fragment extents, and fragment-list lengths describe one internally consistent packet.
- Every read or write is bounded against the actual linear or nonlinear representation before dereference.
- A clone can mutate its private metadata but cannot mutate shared packet bytes without establishing writable ownership.
- Header and payload sharing are tracked independently where the representation permits header-only clones.
- Socket, cgroup, protocol, allocator, page-pool, user-page, DMA, and device charges or references are acquired before exposure and released exactly once.
- DMA ownership and CPU readability follow the backing provider's contract; not every netmem instance is an ordinary readable page.
- Offload, checksum, VLAN, tunnel, timestamp, route, security, and queue metadata are updated or cleared whenever bytes or ownership change.
- Queue membership contributes exactly one owned reference and removal has one disposition: transfer, consume, drop, or requeue.
- `truesize` and resource limits represent memory pressure conservatively enough to prevent tiny payloads from hiding large allocations.
- Pool, device, socket, namespace, and user-memory teardown waits for all buffer and completion references to resolve.

### Common failures

Common mistakes are assuming every packet is linear, using total length as contiguous length, pushing a header without headroom, modifying a clone's shared data, checking the SKB reference count but not the data reference count, retaining stale header offsets after pull or encapsulation, charging only payload bytes, orphaning an SKB without understanding its destructor, recycling a page still held by a clone, invoking page APIs on unreadable netmem, freeing pinned user pages before zero-copy notification, double unmapping shared fragments, leaving checksum state valid after payload mutation, using one control buffer across layers without ownership, and destroying a page pool when socket queues still contain its pages.

### Compact example

A packet has 384 linear bytes and fragments of 700 and 900 bytes. Its total length is 1,984 bytes, nonlinear length 1,600 bytes, and head length 384 bytes. A clone raises the shared-data reference count to two. Although the clone has its own metadata, it must copy or COW before modifying shared bytes. If it only changes queue mapping, no payload copy is needed because that field lives in private metadata.

### Connections

[OS-031](031-address-translation.md), [OS-038](038-memory-mapped-files.md), [OS-037](037-copy-on-write.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-055](055-numa-memory-placement.md), [OS-063](063-direct-memory-access.md), [OS-067](067-zero-copy-and-kernel-bypass.md), [OS-071](071-socket-layer-architecture.md), and [OS-072](072-packet-reception-and-transmission.md) connect network buffers to memory, COW, accounting, locality, DMA, socket state, and packet paths.

## Governing Question

Network buffers sit between incompatible needs. Devices want aligned DMA memory and rings. Parsers want contiguous headers. Protocols want cheap header insertion and removal. Forwarding wants clones. Sockets need memory accounting. Zero-copy wants externally owned pages. High packet rates punish allocation and copying, while hostile packets punish every unchecked shortcut.

The governing question is how one representation can carry packet bytes and the truth about those bytes across all these owners. The answer is not one flat array. It is a metadata object plus a reference graph and a set of transformations whose preconditions are explicit.

## Why This Matters

At millions of packets per second, one allocation, reference-count cache miss, linearization, or whole-packet copy per packet can dominate CPU and memory bandwidth. Page recycling, fragments, cloning, batching, GRO, GSO, and zero-copy are major performance tools.

Those tools create long and branching lifetimes. A received page can be cloned for forwarding and capture, queued to a socket, redirected, and later recycled. A user send buffer can remain pinned after `sendmsg` returns. A device can still DMA a fragment after upper layers consider a request cancelled.

Buffer bugs are high impact: out-of-bounds parsing, cross-tenant data exposure, use-after-free, double unmap, kernel-memory exhaustion, corrupt checksums, or stale security metadata. Geometry, authority, accounting, and evidence must travel together.

## Prerequisites and Retrieval

Review [OS-007](007-kernel-data-structures.md), [OS-008](008-kernel-memory-allocation.md), [OS-024](024-atomic-operations.md), [OS-031](031-address-translation.md), [OS-038](038-memory-mapped-files.md), [OS-037](037-copy-on-write.md), [OS-040](040-diagnosing-memory-pressure-and-thrashing.md), [OS-051](051-per-cpu-state.md), [OS-052](052-smp-kernel-synchronization.md), [OS-053](053-scalable-locking.md), [OS-055](055-numa-memory-placement.md), [OS-063](063-direct-memory-access.md), [OS-067](067-zero-copy-and-kernel-bypass.md), [OS-071](071-socket-layer-architecture.md), and [OS-072](072-packet-reception-and-transmission.md).

Retrieve these distinctions:

- SKB metadata, head allocation, page fragment, fragment list, extension, and owner-specific context are different objects;
- `head`, `data`, `tail`, and `end` are positions in the linear allocation, while total length can include nonlinear bytes;
- SKB reference count, shared head-data reference count, fragment page reference, socket reference, and DMA ownership are separate lifetimes;
- cloning metadata, copying all data, copying only a header, expanding headroom, linearizing, and pulling data are different transformations;
- allocated bytes, payload bytes, SKB `truesize`, charged bytes, pinned bytes, and device-mapped bytes differ;
- readable CPU memory, page-backed memory, DMA-addressable memory, device memory, and user-pinned memory are not interchangeable;
- receive recycling, ordinary page freeing, user completion, transmit completion, and pool destruction have different terminal evidence;
- checksum state, segmentation state, header offsets, protocol, route, mark, priority, and timestamp require independent validity;
- queue membership, list linkage, tree linkage, device ownership, and socket ownership cannot overlap arbitrarily;
- drop, consume, clone, redirect, transmit, orphan, purge, and free each imply different accounting and evidence.

## Learning Objectives

After this module, you should be able to:

1. draw SKB linear and nonlinear geometry and recompute total, head, data, tailroom, fragment, and aggregate lengths;
2. distinguish metadata references from shared-data and backing-page references across clone, copy, COW, pull, trim, and linearization;
3. preserve header offsets, checksum, segmentation, VLAN, tunnel, route, security, timestamp, and queue metadata through transformations;
4. trace page-pool, netmem, DMA, socket-owned, user-pinned, and device-owned buffer lifetimes;
5. design bounded allocation, `truesize`, socket and cgroup charging, per-CPU caches, pressure reclaim, and emergency reserves;
6. reason about zero-copy completion, destructor callbacks, orphaning, queue purging, teardown, and device reset;
7. validate buffer code with adversarial geometry, sharing, failure injection, reference tracking, and workload-scoped measurement.

## Core Exposition

### Metadata and bytes are separate

An SKB is primarily metadata. It points into a head allocation and describes optional external fragments and another SKB list. The metadata can be copied cheaply while bytes remain shared.

This separation enables high-rate transformations but forbids using object identity as data ownership. Always ask which allocation contains the target byte and who may modify it.

### Linear head geometry

The linear allocation is described conceptually by ordered positions

$$
head\le data\le tail\le end.
$$

Bytes from `data` to `tail` are current linear packet content. Space before `data` is headroom; space after `tail` is tailroom. The allocation can also contain shared-info metadata near its end under implementation rules.

### Headroom

Headroom permits prepending link, network, transport, or tunnel headers without allocating a new buffer. A push moves `data` backward and increases packet length.

Before pushing, require sufficient headroom and a writable header area. Headroom in a shared clone is capacity, not authority.

### Tailroom

Tailroom permits appending payload, padding, authentication tags, or trailers in the linear area. A put operation advances `tail` and total length.

Check both physical tailroom and protocol maximum. Padding exposed to a device or user must be initialized so stale kernel bytes cannot leak.

### Total and nonlinear length

Total `len` includes linear and nonlinear bytes. `data_len` records the nonlinear portion. Therefore

$$
headlen=len-data\_len.
$$

Code that directly dereferences `len` bytes from `data` is wrong when `data_len>0`. Use fragment-aware accessors or first make the required range linear.

### Page fragments

Fragments describe ranges within referenced pages or other supported packet memory. Each has an offset and size bounded by its backing object.

The same page can contribute several fragments or be shared across SKBs. Reference and DMA rules apply to the backing memory, not just the small descriptor.

### Fragment lists

A fragment list chains other SKBs as nonlinear data. It can represent aggregation, segmentation relationships, or large packets without flattening all bytes.

Traversal needs cycle-free ownership, bounded total length, and correct accounting. Freeing the parent releases child references according to the representation.

### Shared information

Metadata associated with the head allocation stores fragment descriptors, fragment-list links, GSO state, transmit flags, and the shared-data reference count.

Because clones share this region, mutation requires the relevant exclusivity. A private `struct sk_buff` does not imply private shared-info state.

### SKB references

Taking an SKB reference retains that metadata object. Queue insertion commonly transfers or takes such a reference depending on the API contract.

Dropping the final SKB reference begins its destructor and data release. It does not necessarily free every backing byte immediately if other shared-data or page references remain.

### Cloning

Cloning allocates new SKB metadata and shares the head data and fragments. Each clone can carry different routing, queue, timestamp, or list metadata where fields are private.

Cloning is ideal for multicast, forwarding plus local delivery, capture, and retransmission when bytes remain immutable. It is unsafe to edit shared headers or payload without COW.

### Shared-data references

The head data reference count tracks users of the shared linear allocation. Some designs partition the count to represent payload-only references used by transport retransmission.

Check the correct predicate for the region to modify. Whole-head sharing and header writability are related but not identical.

### Headerless and payload clones

A transport can retain a payload reference while allowing another SKB to prepend headers. Header-release metadata records which portion a clone may treat as writable after ensuring space.

Only the intended producer should create this arrangement for a source SKB. Repeated or arbitrary header release can make writability reasoning unsound.

### Full copy

A full copy allocates private metadata and packet data. It simplifies later mutation and decouples lifetime at the cost of allocation and memory bandwidth.

Copy when an external owner cannot satisfy downstream lifetime, when policy requires isolation, or when widespread modifications make COW savings unlikely.

### Copy-on-write

COW checks sharing and required headroom. If the requested region is already private and large enough, no copy is needed; otherwise allocate and copy the required data.

Failure leaves the caller with the documented original state. Callers must handle allocation failure rather than modifying shared data anyway.

### Expanding the head

Encapsulation may need more headroom than the current allocation. Head expansion creates a new linear area while preserving packet bytes, offsets, fragments, metadata, and ownership.

Rebase every pointer or stored offset according to its contract. Never retain a raw pointer into the old head across possible reallocation.

### Pulling data

Pull advances `data` over consumed linear bytes and reduces visible length. A fragment-aware pull can move bytes from nonlinear storage into a new linear prefix when required.

Validate the requested amount against total length and ensure parsers do not use header pointers invalidated by movement or reallocation.

### Trimming and appending

Trim shortens a packet, releasing or resizing fragments and fragment-list children beyond the new end. Append grows only after capacity and writeability checks.

Update checksum and segmentation state when covered bytes change. Ensure discarded user or device-backed fragments receive the right completion.

### Linearization

Linearization copies nonlinear bytes into one contiguous allocation. It simplifies parsers and devices without scatter-gather support.

It can be expensive or fail under memory pressure. Prefer helpers that copy only the required header prefix when the rest can remain fragmented.

### Fragment-aware access

Safe accessors copy or map a bounded range across the linear head, page fragments, and fragment lists. They validate offset plus length without overflow.

Do not assume high-memory or device memory has a permanent kernel virtual address. Provider-specific mapping and readability rules remain authoritative.

### Header offsets

SKBs store MAC, network, transport, and inner-header locations as offsets or pointers under defined conventions. Push, pull, encapsulation, decapsulation, copy, and head expansion can change them.

Reset or rebase offsets at every structural transition. An offset within allocation but pointing at the wrong header is still unsafe parser state.

### The control buffer

The SKB control buffer offers private scratch space to a layer while that layer owns the packet. Different subsystems reuse the same bytes.

Ownership is temporal. A layer must initialize its fields and must not expect them to survive transfer through another user unless an explicit contract reserves them.

### Extensions

Optional SKB extensions carry additional metadata without enlarging every base object. They have their own allocation, cloning, COW, and release rules.

Feature combinations must not retain a stale extension after bytes or policy invalidate it. Allocation failure needs a safe semantic fallback.

### Protocol and packet type

Protocol fields identify the next parser and packet-type fields distinguish host, broadcast, multicast, other-host, or related classes. They are derived from device and link processing.

Clear or recalculate them when synthesizing or redirecting packets. Metadata from one namespace or device must not be trusted on another without validation.

### Device and queue mapping

An SKB can point to ingress or egress device context and record a queue mapping. Redirect, forwarding, bonding, tunneling, and device removal can change that association.

Device references and queue indices must remain valid for their use window. Revalidate feature and queue metadata after changing egress.

### Route and destination references

Cached route state accelerates repeated processing and can be stored with reference or no-reference encodings under strict lifetime rules.

Do not retain a no-reference route past its protected epoch. Clear cached routes after transformations that change namespace, marks, addresses, or policy inputs.

### Marks, priority, and security metadata

Marks and priority guide routing, policy, filtering, qdiscs, and sockets. Security or connection-tracking associations can also accompany the packet.

Cloning copies relevant metadata, but crossing a trust boundary can require clearing or recomputing it. A user-controlled mark is not automatically kernel-trusted policy.

### Checksum metadata

Checksum state says whether data needs verification, was verified for certain layers, has a complete checksum contribution, or is prepared for partial transmit completion.

Any mutation within a covered region invalidates or incrementally updates the state. Copying bytes without checksum metadata—or metadata without equivalent bytes—breaks the packet contract.

### Segmentation metadata

GSO type, size, segment count, and header offsets describe how one internal packet becomes several outputs. GRO can create related aggregate representations.

Cloning preserves these fields only while bytes remain equivalent. Trim, tunnel edits, and device feature changes can require recomputation or software segmentation.

### Timestamps

An SKB can carry receive time, transmit scheduling time, software timestamp, or hardware timestamp correlation state. These events and clocks differ.

Clones used for several consumers need clear timestamp ownership. Do not overwrite an ingress timestamp with an unrelated enqueue time without storing both at separate observation points.

### Socket ownership

An SKB owned by a socket can hold a socket reference or charge memory through a destructor callback. Ownership supports accounting and wakeup, not permission for arbitrary protocol mutation.

Orphaning calls the owner destructor and detaches accounting while the buffer continues to exist. Use it only when a new owner or global limit governs the remaining memory.

### `truesize`

Payload length understates memory when a tiny packet occupies a full page, head allocation, SKB object, fragments, or pinned user memory. `truesize` supplies a more conservative charge.

It remains an accounting model, not an exact allocator invoice. Maintain proportionality well enough that an attacker cannot queue huge backing allocations under tiny charges.

### Socket and cgroup charging

Receive and send queues charge buffers against socket limits, protocol pressure, applicable cgroups, and host memory policy. Charge before queue visibility.

Uncharge exactly once on dequeue and consumption, drop, orphan, or transfer according to the API. Descriptor passing or namespace changes do not erase the original memory automatically.

### Allocation context

Process context can sleep for memory; softirq and other atomic contexts cannot. Allocation flags express reclaim and blocking constraints.

Design reserves and pools for the actual caller context. Retrying a sleeping allocation in an atomic path is not a recovery strategy.

### Emergency memory

Networking can be needed to reclaim memory or write dirty state. Special emergency pages and `pfmemalloc` metadata allow narrow progress through trusted paths.

Do not deliver reserve-backed packets broadly. Restrict them to protocols and sockets able to participate safely in memory recovery.

### Per-CPU caches

Per-CPU SKB and page caches reduce shared allocator contention and improve locality. They multiply idle reserves and complicate CPU offline and imbalance.

Bound cache sizes, drain them on lifecycle transitions, and observe per-CPU misses and remote frees rather than only global allocation totals.

### Page pools

A page pool binds allocation and recycling policy to receive queues or compatible consumers. It can pre-map pages, maintain a fast cache and ring, and synchronize returned ranges for devices.

The preferred single-consumer context provides lockless fast access. Cross-CPU or extra references can route return through slower paths.

### Page-pool fragments

Splitting a page reduces memory waste for small buffers but adds fragment reference accounting and cache-line updates. Device synchronization can depend on the final fragment return.

Configure offset and maximum DMA length conservatively. An incorrect small sync range can expose stale CPU writes to the device.

### Recycling through SKBs

An SKB marked with page-pool recycle information returns backing to the pool on final release when eligibility remains valid. Clones delay that release.

Do not directly return the page from the driver after transferring it to the SKB. The final data owner is the only safe recycler.

### Pool shutdown

Stopping the receive queue prevents new allocations and descriptor publication, but pages can remain in XDP redirects, SKBs, sockets, qdiscs, or device transmit.

Track in-flight count and wait or defer final pool destruction. Timeout may diagnose a leak; it does not authorize freeing live pages.

### Netmem abstraction

Netmem lets drivers handle backing that may be a page, DMA-buf, or another provider. Some instances are not CPU-readable and cannot be passed to ordinary page or DMA helpers.

Use netmem and page-pool abstractions for address, reference, mapping, and synchronization. Test unreadable backing explicitly rather than assuming `page_address` exists.

### Header-data split

A device can place CPU-parsed headers in ordinary memory and payload in separate or device memory. This reduces host-memory bandwidth for payload consumers able to use the backing directly.

Parsers must stay within the readable header. Copy or provider-aware access is required if deeper headers extend into unreadable payload.

### Receive DMA lifetime

The device owns a posted receive buffer until completion or reset containment. The CPU synchronizes before reading and the pool synchronizes before reposting where required.

Persistent mapping avoids repeated map cost but not direction and cache ownership. Buffer reuse before final protocol release corrupts later readers.

### Transmit DMA lifetime

An SKB's head and fragments remain stable from descriptor publication through validated device completion. Each mapped segment retains its exact unmap parameters.

If mapping fragment $k$ fails, unwind segments $0$ through $k-1$ and leave upper-layer ownership unambiguous. Do not free shared pages while another clone transmits.

### User-page zero-copy

`MSG_ZEROCOPY` can pin or reference user pages instead of copying large sends. This exchanges per-byte copy cost for pinning, accounting, completion notification, and longer shared lifetime.

The application must not modify pages until the error-queue notification covers the send identifier. Small writes can be slower because fixed overhead dominates.

### Notification ranges

Zero-copy completions can coalesce identifier ranges and may arrive out of order in exceptional paths. Identifiers count eligible calls under their interface rather than payload bytes.

Use wrap-safe tracking and drain the error queue. Close and fallback copying must still resolve every outstanding user buffer.

### Deferred copy

Some paths copy user-backed fragments later to bound notification latency or satisfy a consumer that cannot retain the external backing. The original send may still have avoided its initial copy.

Instrumentation must distinguish initial zero-copy acceptance, later copy, and final notification. “Zero copy” is a path property, not a permanent packet label.

### Splice and file-backed pages

Splice-like paths can reference page-cache or pipe buffers in an SKB. These pages have filesystem, pipe, and writeback lifetimes beyond networking.

Before mutation or an incompatible consumer, copy or orphan fragments under the correct helper. Network teardown cannot free a filesystem-owned page.

### Clones in retransmission

Reliable transports can retain payload while sending header variants and retransmissions. Header-only cloning avoids duplicating large data.

ACK processing, loss recovery, retransmission, and final socket close race over references. Sequence state determines logical validity; reference count determines memory safety.

### Multicast and taps

One ingress SKB can be cloned for protocol delivery, bridge forwarding, packet taps, or multicast outputs. Slow observers extend shared-data lifetime and memory pressure.

Apply per-consumer bounds and copy where isolation requires. A diagnostic tap must not silently become an unbounded retention mechanism.

### Queues

SKB queues provide linked ownership with synchronized and unsynchronized variants. The caller must know whether it holds the list lock or single-owner context.

One SKB cannot occupy two ordinary list positions using the same links. Remove before requeue, and preserve one reference per membership contract.

### Purging

Purging removes every queued SKB and drops its reference, often recording a drop reason. The caller supplies required synchronization.

Purge during shutdown only after producers are stopped. Otherwise new buffers can arrive after the apparently final sweep.

### Drop reasons

Reasoned freeing attributes why a buffer left the path: policy, malformed data, memory, queue capacity, checksum, route, device, or teardown.

Reason labels improve diagnosis but must not expose secrets or create unbounded cardinality. One buffer should not be counted as several independent drops at successive cleanup layers.

### Destructors

An SKB destructor may uncharge a socket, release a user-page completion context, return provider memory, or perform other owner-specific cleanup.

Set the destructor only with its required state and clear or invoke it during ownership transfer as documented. A stale destructor can uncharge or free the wrong owner.

### Queueing under pressure

Buffers accumulate in driver rings, NAPI backlog, GRO state, protocol queues, sockets, qdiscs, retransmission, and device rings. Each layer needs a byte and object bound.

Backpressure as early as semantics permit. Increasing every limit multiplies worst-case memory and latency without increasing the slow consumer's rate.

### NUMA placement

Allocate buffer heads, pages, metadata, rings, and processing on a node near the device and consumer when possible. Remote recycling and clone release can dirty shared reference-count cache lines.

Steering changes actual locality. Observe allocation node, processing CPU, device node, and final-free CPU under the same workload.

### Security boundaries

Initialize padding and newly exposed head or tail bytes before copyout or DMA. Clear stale metadata on reused objects. Validate all offsets and lengths before parser access.

Pinned and device memory expands attack surface. Enforce per-user and per-cgroup limits, IOMMU boundaries, provider authorization, and teardown revocation.

### Observability

Measure SKB allocations and failures, head sizes, fragment counts, nonlinear ratios, clones, COW, copies, linearization, `truesize`, socket charges, queue bytes, page-pool fast and slow paths, recycling, NUMA mismatch, pinned pages, zero-copy notifications, DMA maps, drops, and lifetime.

Sampling must avoid turning every packet into an allocation. Aggregate per CPU with known reset and merge behavior, and preserve request or flow correlation only when needed.

### Testing

Fuzz every geometry boundary: zero length, head-only, fragment-only, maximum fragments, nested fragment lists, short headers, overflowing sums, cloned heads, shared payloads, insufficient headroom, trim across fragments, and failed linearization.

Inject allocation, COW, mapping, notification, queue, and teardown failures. Use reference, leak, DMA, lock, bounds, and memory-accounting diagnostics. Test device reset and pool shutdown with clones in every downstream queue.

## Definitions and Notation

Let:

- $a_h$ be linear allocation size;
- $h$ be headroom;
- $\ell_h$ be linear packet length;
- $t$ be tailroom;
- $F=(f_1,\ldots,f_k)$ be fragment lengths;
- $\ell_f=\sum_i f_i$ be nonlinear fragment length, including validated fragment-list contribution;
- $\ell=\ell_h+\ell_f$ be total packet length;
- $r_m$ be references to one SKB metadata object;
- $r_d$ be references to shared head data;
- $r_i$ be references to fragment backing $i$;
- $T$ be `truesize` accounting charge;
- $Q_j$ be charged bytes in queue or owner $j$;
- $K_j$ be its limit;
- $O(x,t)$ be the mutable owner of backing $x$ at time $t$.

Linear geometry requires

$$
a_h=h+\ell_h+t,
$$

subject to implementation-reserved metadata outside the usable expression. Total length requires

$$
\ell=\ell_h+\sum_{i=1}^{k}f_i.
$$

Safe contiguous access of range $[o,o+n)$ without copying requires

$$
0\le o,\quad 0\le n,\quad o+n\le \ell_h
$$

using checked arithmetic. Fragment-aware access instead proves coverage across the complete representation.

A clone creates new metadata but shares data:

$$
r_m^{clone}=1,\qquad r_d\leftarrow r_d+1.
$$

Mutation of shared bytes requires

$$
r_d=1\ \land\ writable(range)=true,
$$

or a successful COW transition that establishes those conditions.

Every accounted queue remains bounded:

$$
0\le Q_j\le K_j,
$$

and every backing has one mutable owner:

$$
\forall x,t:\ |O(x,t)|=1.
$$

These equations are an abstract geometry and ownership model, not the complete in-memory ABI of any kernel version.

## Mechanisms, Invariants, or Proof Structure

### Obligation 1: validate geometry globally

Linear positions, total and nonlinear lengths, fragments, fragment lists, header offsets, and allocation capacity form one checked, overflow-free representation.

Counterexample: total length is valid but `data_len` exceeds it, making computed head length wrap into a huge contiguous range.

### Obligation 2: prove write authority

Every mutation establishes private writable backing for the modified region and sufficient head or tail capacity.

Counterexample: a forwarding clone decrements TTL in shared bytes and silently alters the locally delivered packet.

### Obligation 3: preserve metadata equivalence

Checksum, segmentation, offsets, route, device, namespace, security, timestamp and queue metadata are copied, cleared or recalculated with the bytes.

Counterexample: payload changes but partial-checksum offsets still describe the old transport header.

### Obligation 4: separate reference domains

Metadata, shared head, each fragment, socket, pool, provider, DMA and user-completion contexts acquire and release their own references exactly once.

Counterexample: the final SKB reference frees a page that another clone still references through shared data.

### Obligation 5: charge before queueing

Realistic memory cost is charged to the socket, cgroup, protocol or queue owner before remote or local producers can make the buffer visible.

Counterexample: one-byte datagrams backed by full pages bypass a payload-only limit and exhaust host memory.

### Obligation 6: honor provider capabilities

Page, netmem, DMA-buf, user page, page-cache page and device memory are accessed, mapped, synchronized and released through their owning APIs.

Counterexample: a driver calls an ordinary page mapping helper on unreadable device-backed netmem.

### Obligation 7: recycle only on final return

Receive backing returns to its pool only after all SKB, XDP, socket, qdisc, device and external references end and DMA sync is correct.

Counterexample: the receive driver recycles a page immediately after building an SKB that remains queued to a socket.

### Obligation 8: resolve zero-copy ownership

User buffers remain pinned, charged and immutable to the application until copied fallback or completion notification establishes reuse.

Counterexample: `sendmsg` success is treated as reuse permission and the application overwrites bytes before transmission.

### Obligation 9: make queue membership unique

Each list or tree insertion has one linkage owner, one reference rule and one removal disposition under the correct lock or single-consumer context.

Counterexample: one SKB is inserted into two lists using the same link fields, corrupting both queues.

### Obligation 10: make destruction owner-specific

Destructors, uncharge, DMA unmap, page release, pool recycle, user notification and extension cleanup run in a defined order once.

Counterexample: orphaning invokes a socket destructor, then final free invokes the stale pointer again and underflows accounting.

### Obligation 11: quiesce producers before teardown

Device, protocol, socket, timer, workqueue, XDP, tap and user producers stop before queues are purged and pools or providers are destroyed.

Counterexample: page-pool shutdown reaches zero momentarily, then a delayed redirect completion returns another page into freed pool state.

### Obligation 12: scope evidence to backing and path

Tests identify allocation, provider, memory node, DMA model, device, offloads, clone graph, queues, load, failure, observer and terminal condition.

Counterexample: copied loopback sends are presented as evidence for pinned-page zero-copy notification or NIC DMA lifetime.

## Alternatives and Trade-Offs

- **Linear buffers versus fragments:** linear data simplifies parsing and devices; fragments avoid copying large payloads.
- **Clone versus full copy:** clones save bandwidth and allocation; copies isolate mutation and lifetime.
- **Whole-buffer COW versus header COW:** whole copying is simple; header-only privatization retains large shared payloads.
- **Reserved headroom versus later expansion:** reservation speeds encapsulation; excess headroom wastes memory on every packet.
- **Large heads versus page fragments:** large heads improve locality for small packets; page fragments scale large payloads and scatter-gather.
- **Page allocation versus page-pool recycle:** general allocation is flexible; recycling amortizes mapping and preserves queue locality.
- **Full pages versus split fragments:** full pages simplify references; splitting reduces waste but adds shared-page coordination.
- **Page-backed versus netmem abstraction:** pages integrate broadly; netmem permits device memory and future providers with stricter access rules.
- **Copy send versus user-page zero-copy:** copies permit immediate reuse; zero-copy benefits large transfers while pinning and notifying.
- **Exact allocation charge versus `truesize` approximation:** exact accounting is costly; conservative approximation must resist amplification.
- **Socket ownership versus orphaning:** socket charge provides accountability; orphaning permits later paths only with replacement governance.
- **Per-CPU caches versus global pools:** per-CPU state reduces contention; global capacity shares memory and avoids multiplied reserves.
- **Eager linearization versus fragment-aware access:** linearization simplifies all later users; bounded access copies only what a parser needs.
- **Cached route metadata versus fresh lookup:** caching saves work; stale policy or namespace inputs require invalidation.
- **Detailed per-buffer tracing versus sampling:** full traces explain reference graphs; sampling preserves hot-path performance and privacy.

## Failure Modes and Misconceptions

- **“The SKB contains the packet bytes.”** It describes bytes held in one or more backing objects.
- **“`len` bytes are contiguous at `data`.”** only head length is linear when nonlinear data exists.
- **“Headroom is writable.”** sharing can remove write authority even when capacity exists.
- **“A clone is a deep copy.”** it has private metadata and shared packet data.
- **“One reference count governs everything.”** metadata, shared data, fragments, sockets, DMA and providers differ.
- **“Private metadata means private headers.”** header bytes can still be shared.
- **“COW cannot fail.”** allocation under pressure can fail and must preserve safe state.
- **“Linearization is free metadata work.”** it copies bytes and can allocate or fail.
- **“Pulling data preserves old pointers.”** movement or reallocation invalidates stored header addresses.
- **“Checksum state survives any mutation.”** covered byte or header changes require update or invalidation.
- **“GSO metadata is only a performance hint.”** it is required to create correct output packets.
- **“Payload bytes equal memory cost.”** heads, pages, metadata, pins, and fragments amplify charge.
- **“Orphaning frees an SKB.”** it detaches an owner and invokes its destructor while the buffer remains.
- **“A destructor always frees data.”** it performs owner-specific cleanup; shared data can remain.
- **“A page pool owns every page immediately on put.”** other references or return context can change the path.
- **“Stopping RX makes pool destruction immediate.”** downstream queues and clones can retain pages.
- **“Netmem is always a `struct page`.”** providers can expose different and unreadable backing.
- **“DMA-mapped means CPU-readable.”** provider and ownership rules still apply.
- **“Zero-copy send allows immediate mutation.”** user pages remain shared until notification or fallback completion.
- **“Completion IDs count bytes.”** the interface can count eligible calls and coalesce ranges.
- **“One SKB can join several lists.”** ordinary linkage supports one membership at a time.
- **“Purging once ends producers.”** producers must be quiesced before the final purge.
- **“Padding need not be initialized.”** it can leak stale data through DMA or copyout.
- **“Large buffer limits fix slow consumers.”** they enlarge memory and queueing without raising consumption rate.
- **“Loopback proves zero-copy hardware behavior.”** loopback can trigger deferred copies and bypass device DMA.

## Worked Examples

### Example 1

A linear allocation has 128 bytes of headroom, 384 bytes between data and tail, and 1,536 bytes of tailroom. Two fragments contain 700 and 900 bytes.

The linear allocation is 2,048 bytes, nonlinear length is 1,600, and total packet length is 1,984. A parser needing 512 contiguous bytes cannot dereference them directly: only 384 are linear.

### Example 2

The following toy recomputes geometry and one clone's COW decision. It models no SKB implementation, allocation, page, or reference atomicity.

<!-- bijux-verify: {"id":"network-buffer-geometry","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"allocation=2048 headroom=128 linear=384 tailroom=1536\nfragments=2 nonlinear=1600 total=1984\nclone_metadata_refs=1 shared_data_refs=2\nmodify_queue_mapping_copy=False\nmodify_payload_copy=True\n","stderr":""}} -->
```python
headroom = 128
linear = 384
tailroom = 1536
fragments = [700, 900]
allocation = headroom + linear + tailroom
nonlinear = sum(fragments)
total = linear + nonlinear
shared_data_refs = 2

print(
    f"allocation={allocation} headroom={headroom} "
    f"linear={linear} tailroom={tailroom}"
)
print(
    f"fragments={len(fragments)} nonlinear={nonlinear} total={total}"
)
print(f"clone_metadata_refs=1 shared_data_refs={shared_data_refs}")
print("modify_queue_mapping_copy=False")
print(f"modify_payload_copy={shared_data_refs > 1}")
```

Queue mapping is private metadata in this model, while payload bytes are shared. Actual writability uses kernel helpers and region-specific rules.

### Example 3

A router clones one SKB for local delivery and forwarding. Forwarding must decrement the IPv4 TTL. It first makes the header private, adjusts TTL, and updates the header checksum. The local clone retains the original TTL and checksum.

Changing bytes before COW would mutate both logical packets. Copying the full 64 KiB payload would be correct but unnecessarily expensive when only the header changes.

### Example 4

A parser needs a 60-byte TCP header, but only 40 bytes are linear and the rest begins in a fragment. A fragment-aware pull helper makes the required 60-byte prefix linear after verifying total length.

The parser reacquires header locations after the helper because allocation may move. It does not retain a pointer into the old head across the call.

### Example 5

An attacker sends one-byte datagrams that each occupy a 2 KiB head allocation plus SKB metadata. Charging one payload byte would permit millions of allocations under a small byte limit.

The receive path charges a conservative `truesize` before socket queue insertion. At the limit it drops or backpressures according to protocol semantics and records the correct stage.

### Example 6

A page-pool page is split into two receive fragments. One becomes an SKB queued to a socket; the other is dropped in NAPI. Dropping the second fragment does not make the whole page recyclable because the socket retains the first.

Final return of the last fragment performs the provider's synchronization and recycle action. Pool shutdown includes the outstanding socket-held fragment in its in-flight count.

### Example 7

A netmem-backed receive payload is not CPU-readable, while its split header is readable. The driver parses no payload and builds the representation using netmem helpers.

A later consumer that requires payload inspection must use a supported copy or mapping path. Converting the backing blindly to `struct page` would violate the provider contract.

### Example 8

An application sends four large buffers with zero-copy identifiers 40 through 43. A notification covers 40 through 42, while 43 remains outstanding. The allocator can reuse the first three ranges but not the fourth.

If the path copied identifier 41 internally, its notification still resolves user ownership under the interface. The application does not infer peer acknowledgement from any of these events.

### Example 9

A transmit SKB has a linear head and five shared fragments. Mapping fragment three fails. The driver unmaps the head and fragments zero through two using the original parameters, never published the incomplete descriptor set, and returns a resource result without consuming caller ownership.

It does not unmap fragments three through four because they were never mapped, and it does not free the shared pages because clones may retain them.

### Example 10

Device removal stops receive publication and NAPI, but the page pool reports 37 pages in flight. Diagnostics find 30 in socket queues, five in a packet tap, and two on a transmit redirect.

The driver waits for or forcibly resolves those owning subsystems through supported teardown. It does not destroy the pool at timeout and turn later frees into use-after-free.

## Cross-Program Connections

- **Data structures engineering:** intrusive lists, reference graphs, fragments, rings, COW, caches, checked iterators, and cycle handling define buffer mechanics.
- **Computer architecture:** cache lines, NUMA, DMA coherence, IOMMUs, TLBs, atomics, memory ordering, and device memory shape ownership cost.
- **Network engineering:** headers, MTU, fragmentation, checksum, tunneling, segmentation, retransmission, multicast, and queueing define transformations.
- **Security engineering:** untrusted geometry, stale metadata, padding leaks, pinned memory, device access, accounting amplification, and destructor bugs define attack surfaces.
- **Performance engineering:** allocation, copy volume, fragment count, COW rate, linearization, recycling, cache misses, queue bytes, and notification delay define evidence.
- **API and service engineering:** buffer ownership, streaming, framing, backpressure, cancellation, and completion meaning propagate to user APIs.
- **Distributed systems:** retransmission, duplication, multicast, flow control, loss, and delayed completion extend buffer lifetimes across protocol state.
- **Platform engineering:** cgroup limits, device and NUMA placement, offload policy, observability, safe teardown, and incident evidence govern deployments.
- **Storage engineering:** scatter-gather, DMA mapping, descriptor ownership, page pinning, completion, and reset share the same resource invariants.
- **Formal methods:** separation logic, ownership types, reference-state machines, checked arithmetic, and temporal teardown properties clarify proofs.

## References

1. Linux Kernel Documentation, [`struct sk_buff`](https://docs.kernel.org/networking/skbuff.html), linear geometry, fragments, shared info, cloning, data references, checksum and segmentation metadata; retrieved 2026-09-04.
2. Linux Kernel Documentation, [Linux Networking and Network Devices APIs](https://docs.kernel.org/networking/kapi.html), SKB allocation, queues, references, clone, copy, COW, orphan, purge, fragment access, ownership and destruction; retrieved 2026-09-04.
3. Linux Kernel Documentation, [Page Pool API](https://docs.kernel.org/networking/page_pool.html), DMA mapping, synchronization, page and fragment allocation, recycling, in-flight lifetime, NUMA and statistics; retrieved 2026-09-04.
4. Linux Kernel Documentation, [Netmem Support for Network Drivers](https://docs.kernel.org/networking/netmem.html), abstract packet memory, unreadable backing, page-pool integration, provider references and DMA restrictions; retrieved 2026-09-04.
5. Linux Kernel Documentation, [`MSG_ZEROCOPY`](https://docs.kernel.org/networking/msg_zerocopy.html), user-page sharing, accounting, completion notifications, fallback copying, ordering and test caveats; retrieved 2026-09-04.
6. Linux Kernel Documentation, [Checksum Offloads](https://docs.kernel.org/networking/checksum-offloads.html), checksum states, partial offsets, receive verification, encapsulation and fallback; retrieved 2026-09-04.
7. Linux Kernel Documentation, [Segmentation Offloads](https://docs.kernel.org/networking/segmentation-offloads.html), GSO, GRO, TSO, USO, fragments, headers and tunnel metadata; retrieved 2026-09-04.
8. Linux Kernel Documentation, [AF_XDP](https://docs.kernel.org/networking/af_xdp.html), UMEM ownership, fill, completion, RX and TX rings, copy and zero-copy modes, and multi-buffer representation; retrieved 2026-09-04.
9. Linux Kernel Documentation, [XDP RX Metadata](https://docs.kernel.org/networking/xdp-rx-metadata.html), metadata headroom, device timestamps, hashes, VLAN tags, XDP pass and AF_XDP contracts; retrieved 2026-09-04.
10. Linux Kernel Documentation, [Device Memory TCP](https://docs.kernel.org/networking/devmem.html), device-backed receive payloads, header-data split, DMA-buf lifecycle, user access and zero-copy ownership; retrieved 2026-09-04.

## Exercises

### Exercise 1

Given a buffer with 192 bytes headroom, 320 linear bytes, 1,536 tailroom bytes, fragments of 1,000, 2,000, and 500 bytes, and shared-data count three, compute its geometry and design safe operations to prepend a 64-byte header and modify 100 payload bytes beginning at total offset 400.

### Exercise 2

Trace references and charges when a page-pool receive page becomes an SKB, is cloned for a packet tap and local socket, then the original is redirected for transmit. State when the page can recycle and how device reset changes the proof.

### Exercise 3

Design a safe ancillary function that reads, removes, and replaces a variable-length tunneled header in a possibly nonlinear, cloned SKB. Cover bounds, linear access, COW, headroom, offsets, checksums, GSO and failure.

### Exercise 4

Design memory accounting and backpressure for a service receiving tiny datagrams and sending large `MSG_ZEROCOPY` responses. Include `truesize`, socket and cgroup limits, page pins, notifications, errors, close, and emergency progress.

### Exercise 5

Create a validation campaign for network-buffer geometry and lifetime across pages, netmem, page pools, clones, fragments, DMA, queues, zero-copy, pressure, CPU hotplug, device reset, and pool destruction.

## Answers to the Exercises

### Answer 1

The linear allocation is $192+320+1536=2048$ bytes. Nonlinear length is $1000+2000+500=3500$ bytes, and total packet length is $320+3500=3820$ bytes. Only offsets zero through 319 are directly contiguous in the linear data. The existing 192-byte headroom is large enough for a 64-byte header, but shared-data count three means capacity does not imply writability.

First call the supported header-COW helper requesting at least 64 bytes headroom. On success, reacquire all header locations because the head allocation may have moved, push 64 bytes, initialize every new byte, set the new protocol header offsets, increase total and linear length, and update or invalidate checksum and segmentation metadata. On failure, leave the original SKB unmodified and propagate allocation failure.

The requested payload range starts at original total offset 400, beyond the original 320-byte linear head and 80 bytes into fragment one. It spans 100 bytes within that fragment. A header-only COW does not make shared payload private. Use a fragment-aware COW or full-copy operation that establishes private writable backing for this range, or create a new transformed packet according to the protocol. Validate offset plus length with checked arithmetic, update checksums and any authenticated or segmentation metadata, and preserve the other clones' bytes.

### Answer 2

The page pool begins with allocator ownership, then publishes the mapped page to the receive ring and device. Completion plus DMA synchronization transfers it to the driver. Building an SKB transfers backing ownership into the SKB representation and marks it for pool recycling; the driver must no longer recycle directly.

Cloning for the packet tap and local socket creates private metadata objects while increasing the shared-data reference domain. Queueing adds the references and memory charges specified by each tap and socket path. Redirecting the original for transmit transfers that SKB to the egress queue and later device DMA. Dropping the original metadata after transmit completion cannot recycle the page while tap or socket clones remain.

Each consumer releases its metadata and charge once. The last shared-data or fragment reference performs the page-pool return with required synchronization. Only then can the pool cache or ring reuse it. If the final return occurs on another CPU or with an extra page reference, the slower provider path may apply.

During reset, stop new publication and establish that the receive device and redirect destination can no longer DMA. Resolve every old-generation transmit descriptor before releasing its SKB. The page remains in flight until device ownership and every clone end. Masking interrupts or timing out does not prove this. Pool destruction waits for the tracked in-flight count after all producers and callbacks are quiesced.

### Answer 3

Parse outer fixed fields with a bounded fragment-aware copy, not direct total-length dereference. Validate minimum header, declared variable length, alignment, option structure, total packet coverage, and every offset addition without overflow. Determine the full range to remove and replacement length before mutation. Reject unsupported nesting, checksum, or GSO forms explicitly.

Make the needed header prefix linear and then request COW for every byte that will change plus sufficient replacement headroom. Either operation can allocate and move the head, so retain offsets rather than raw pointers and reacquire addresses afterward. Do not modify the original until all fallible preparation required for transactional behavior succeeds, or maintain a cleanup path with a valid documented intermediate state.

Pull the old header, push or append the replacement according to layout, initialize new bytes, and reset MAC, outer and inner network and transport offsets. Recalculate packet length, protocol, encapsulation, route and device-dependent metadata. Invalidate or incrementally update checksums only with a proved formula. Recompute GSO type, header length and feature eligibility, or segment in software before transformation if the new tunnel form cannot remain GSO.

On allocation or validation failure, return an error with original ownership intact and no stale pointer. Test cloned heads, headers crossing fragments, zero and maximum options, insufficient total data, overflow, failed COW, failed expansion, checksum offload, nested tunnels and final devices lacking the new offload.

### Answer 4

For receive, charge a conservative SKB `truesize` that reflects head allocation, metadata and fragments rather than the tiny datagram payload. Enforce per-socket receive bytes and objects, per-cgroup memory, protocol pressure and host-wide limits before queue insertion. Apply early filtering and bounded application admission. At capacity, use protocol-appropriate drop or backpressure and attribute the stage.

For response, enable zero-copy only for sizes and paths where measured copy savings exceed pin and notification overhead. Before acceptance, charge socket send memory, user locked or pinned pages, cgroup memory and outstanding completion identifiers. Bound calls, bytes, pages and elapsed lifetime. Small responses use copying so their buffers can be reused immediately.

After successful zero-copy send, mark the application range immutable and in flight. Drain error-queue notifications, handle coalesced and out-of-order identifier ranges with wrap-safe tracking, and free or reuse only covered buffers. Treat fallback copied completion as ownership resolution, not failure. ENOBUFS and pin-limit errors enter normal backpressure rather than busy retry.

On timeout or close, preserve page ownership until the kernel resolves every send through notification, fallback or teardown. A send return and descriptor close are not sufficient evidence. Reserve narrowly scoped memory and workers for protocol acknowledgements, error-queue draining, close and reclaim. Monitor real allocations, `truesize`, queue bytes, pins, notification age, errors, drops and cgroup pressure.

### Answer 5

Generate head-only, fragment-only and mixed buffers; zero and maximum lengths; every headroom and tailroom boundary; maximum fragment arrays; fragment lists; short headers crossing each boundary; and sums near integer overflow. Verify `len`, `data_len`, head length, fragment totals and checked copy against an independent byte oracle. Fuzz push, put, pull, trim, expand and linearize with allocation failure at every point.

Create metadata references, ordinary clones, headerless payload clones and page fragments in controlled graphs. Modify metadata, headers and payload through supported COW helpers and prove other clones remain unchanged. Track all metadata, head-data, page, socket, pool, extension, route, user-completion and destructor references. Purge queues under their required locks and race producers only where the API permits.

Exercise ordinary pages, split page-pool fragments, extra references, remote-CPU returns, unreadable netmem, DMA-buf providers, user-pinned pages, file-backed fragments and emergency pages. Inject DMA mapping failure at each segment, noncoherent synchronization boundaries, transmit timeout, late completion, AF_XDP and XDP redirect, zero-copy fallback, notification reordering, close, socket orphaning, CPU hotplug, device reset, removal and page-pool shutdown.

Under memory pressure, send tiny-payload/large-allocation attacks, large fragments, slow packet taps, stalled sockets and notification starvation. Assert bounded charge, no underflow, no leak, no use-after-free, no double unmap, no stale destructor, and continued control-path progress. Use bounds, address, leak, lock, DMA and reference diagnostics plus provider statistics.

Measure allocation and failure, copy bytes, clone and COW rate, linearization, fragment count, `truesize`, queue charge, page recycling, NUMA mismatch, pin duration, completion delay, CPU, cache misses and throughput. Record kernel, provider, driver, device, DMA model, offloads, topology, workload, fault and instrumentation. Software or loopback paths do not prove physical DMA, unreadable device memory, or NIC completion; passing finite tests does not prove every reference interleaving. State those limits.
