---
module_id: LSDS-011
program: Large-Scale Data Systems Engineering
level: 1
module_number: 11
title: Distributed Block Storage
status: complete
last_verified: 2026-09-03
---

# Distributed Block Storage

## One-Page Review

### Governing question

How should a large-scale storage system divide logical data into independently named byte extents, locate and validate their physical copies, and expose parallel access without confusing namespace, placement, durability, and device allocation?

### Essential definitions

- A **logical block** or **chunk** is a bounded byte extent identified independently of the file pathname and physical device sectors that contain it.
- A **block handle** is the stable or generation-qualified identity used to refer to that logical extent.
- **Namespace metadata** maps a logical file/object and byte range to ordered block handles and records attributes or policy.
- **Placement metadata or computation** maps a block/object identity and layout epoch to candidate storage targets.
- A **storage node** serves block bytes and local integrity metadata from one or more devices.
- A **block replica** is one encoded copy in a named failure domain; it is not another logical block.
- A **partial block** is the valid tail extent shorter than the configured maximum block size.
- A **block report/inventory** is a storage node's evidence about block replicas it currently holds; authority still depends on system metadata and generation rules.
- **Scrubbing** reads and verifies stored data to detect latent corruption before repair options disappear.

### Central model, mechanism, or theorem

Represent a logical file version as ordered extents `F=[(h_i, o_i, l_i)]`, where handle `h_i` covers logical offset `o_i` for length `l_i`. A block placement record is relative to layout epoch `e`: `P_e(h_i)={target replicas or fragments}`. A read is acceptable only when the namespace version, handle generation, placement epoch, byte range, and integrity evidence are mutually compatible.

For file length `L` and maximum block size `B`, dense fixed-boundary layout uses `ceil(L/B)` blocks; block `i` covers `[iB, min((i+1)B,L))`. Larger `B` reduces block-count metadata and favors streaming throughput, while increasing repair units, straggler exposure, and over-read for small ranges.

### Critical invariants

- Pathnames and directories never substitute for stable data-block identity.
- Logical offsets map to a complete, ordered, nonoverlapping block extent set for the selected file version.
- Physical sector/filesystem allocation is hidden beneath the distributed block contract.
- Placement and membership are evaluated under an explicit epoch or map version.
- Acknowledged bytes meet the declared persistence and replica/fragment policy.
- Checksums and length/generation metadata bind the exact bytes being served.
- Lost, stale, corrupt, orphan, and under-protected replicas are distinct states.
- Capacity, read/write throughput, metadata, repair, and failure-domain placement are measured separately.

### Common failures

Frequent failures are equating a logical block with a disk sector, storing pathname-to-host lists as permanent truth, trusting a block report as authorization, counting stale replicas toward durability, ignoring partial tails, choosing block size from capacity alone, treating checksums as replication, deleting apparent orphans before reconciliation, colocating replicas behind one failure domain, and benchmarking only sequential throughput.

### Compact example

A 275-MiB file under a 128-MiB maximum block size has extents of 128, 128, and 19 MiB. A 20-MiB read beginning at logical offset 120 MiB requires 8 MiB from block 0 and 12 MiB from block 1. With three full replicas, raw payload storage is three times the file length before metadata, checksums, temporary copies, local-filesystem overhead, and repair.

### Connections

[LSDS-003](003-range-hash-and-consistent-partitioning.md) supplies placement functions and epochs. [LSDS-004](004-data-locality.md) supplies topology-aware access. [LSDS-009](009-cluster-failure-assumptions.md) supplies failure domains. [LSDS-012](../ROADMAP.md) deepens metadata servers and namespace; [LSDS-013](../ROADMAP.md) develops replication and erasure coding; [LSDS-014](../ROADMAP.md) develops read/write pipelines.

## Governing Question

A local filesystem maps names through inodes and allocation structures onto sectors of attached devices. A large-scale distributed filesystem must also split data across machines, keep access parallel, survive component loss, detect corruption, rebalance membership, and let clients find bytes without routing every data packet through one metadata server.

The term **block** is overloaded. A physical disk exposes sectors or logical block addresses. A local filesystem allocates pages/extents. A distributed filesystem uses much larger logical blocks or chunks—often megabytes—to amortize metadata and enable streaming. An object store may name variable-sized objects instead of file blocks. A virtual block device may present fixed sectors while internally storing objects. Sound reasoning always names the layer.

The governing question is how to define a logical extent contract independent of volatile physical placement. Namespace metadata says which block handles constitute a file version. Placement says where valid copies should be. Storage nodes say what they currently possess. Integrity says whether bytes match. Reconciliation turns these views into safe actions. Keeping them distinct enables direct parallel I/O and controlled repair.

## Why This Matters

Large analytical files cannot depend on one server or disk. Dividing them into blocks spreads capacity and bandwidth: many workers can read different extents concurrently, and storage can repair or rebalance smaller units than whole datasets. Compute schedulers can place tasks near block replicas.

Block size shapes the entire system. Tiny blocks create many metadata entries, files, checksums, RPCs, seeks, and tasks. Huge blocks reduce overhead but concentrate slow-device risk, lengthen repair, reduce useful parallelism for small files, and make small random reads fetch from large storage units unless indexes and range access are effective.

Correctness depends on identities and generations. A file can be deleted and recreated under the same pathname. A block can be rewritten, recovered, or moved. A delayed storage node can report an old replica after the namespace advanced. If readers or repairers match only path and block number, they can return or replicate stale bytes.

Durability depends on failure domains and detection. Three replicas on three devices in one host do not survive host loss. Three replicas can all contain the same silent corruption if the source or write path was wrong. Checksums detect some byte corruption but do not create an independent good copy. Scrubbing and repair compete with production I/O.

## Prerequisites and Retrieval

Recall partition identity and placement from [LSDS-002](002-horizontal-partitioning.md) and [LSDS-003](003-range-hash-and-consistent-partitioning.md). Recall locality tiers from [LSDS-004](004-data-locality.md), serialized byte contracts from [LSDS-008](008-serialization-across-workers.md), failure domains from [LSDS-009](009-cluster-failure-assumptions.md), and work/movement/state accounting from [LSDS-010](010-reasoning-about-work-movement-and-state-at-scale.md).

You should understand byte offsets, integer division, ranges, files, checksums, hashes, replication, epochs, leases, snapshots, caching, throughput, latency, IOPS, and failure domains. Retrieve the invariant that replicas add physical copies without changing logical partition count.

## Learning Objectives

After completing this module, you should be able to:

- distinguish device sectors, local extents, distributed blocks, objects, and virtual block devices;
- map a logical file byte range to block handles and intra-block ranges;
- explain the separation among namespace, placement, storage-node inventory, and bytes;
- compare metadata lookup placement with computed placement and indirection;
- reason about block size using metadata, streaming, random-read, repair, and skew costs;
- specify block identity, generation, length, checksum, policy, and placement epoch;
- distinguish acknowledged, complete, valid, available, replicated, and durable states;
- describe direct client-to-storage data access after metadata resolution;
- diagnose missing, stale, corrupt, orphan, under-protected, and misplaced replicas;
- account for payload, replica, checksum, temporary, and repair bytes;
- design safe inventory reconciliation and scrubbing evidence; and
- specify consequence-appropriate review for stored data.

## Core Exposition

### Storage layers and overloaded blocks

A physical device reads and writes sectors through a controller. A local filesystem groups sectors into allocation units and extents, tracks free space, journaling, and directories. A distributed storage node can store each logical block as a local file, object, or region while exposing a network API. Clients should not depend on that local representation.

A distributed block is usually much larger than a sector. Its purpose is not atomic device I/O; it is a manageable data, placement, checksum, scheduling, replication, and recovery unit. A block may contain many filesystem extents and be transferred in smaller packets or checksum chunks.

Object storage names byte strings directly. A distributed filesystem commonly layers file names and offsets over block/object handles. Ceph's RADOS exposes named objects to clients and maps them through placement groups to object storage daemons. HDFS exposes file blocks stored and served by DataNodes. GFS used large chunks with handles managed by a master and bytes served by chunkservers.

Virtual block storage exposes sector-like random read/write to a guest while implementing those sectors through distributed objects, logs, or replicas. Do not import filesystem append, rename, or immutable-block assumptions into a virtual disk without checking its contract.

### File-to-block extent mapping

For dense fixed-boundary layout with maximum block size `B`, file byte offset `x` maps to block index `floor(x/B)` and intra-block offset `x mod B`. The final block has length `L mod B` unless `L` is an exact multiple, in which case it is full. Empty files need no data blocks under the simple model.

A range `[a,a+n)` intersects block `i` over `[max(a,iB), min(a+n,(i+1)B,L))` when the lower endpoint is smaller. The client requests only those intersections if the storage API supports range reads. Metadata supplies actual block handles; arithmetic block numbers are not durable identity.

Sparse files, copy-on-write snapshots, deduplication, compression, variable extents, and append can break the simple one-to-one logical/physical picture. A hole can read as zeros without stored payload. Snapshot versions can share immutable blocks. Compression changes physical length. The namespace/layout metadata must describe these cases.

Block ordering is part of the file version. Missing or overlapping logical extents are corruption unless the format explicitly represents holes or overlays. Store exact logical length; otherwise tail padding can become visible data.

### Block identity and generation

A useful block identity contains a namespace or pool, opaque handle, and generation/version. It can also bind tenant, file version, layout policy, and creation epoch. The handle should remain stable while physical replicas move.

Path plus ordinal is insufficient. A pathname can be renamed or reused, snapshots share historical contents, and concurrent appends create new tails. A repair instruction delayed across deletion/recreation must not write old bytes into a new object with the same human-readable name.

Content-addressed blocks derive identity from a digest of canonical bytes, providing strong deduplication and corruption checks when designed correctly. They complicate mutable data, tenant confidentiality, key rotation, garbage collection, and collision handling. Location-addressed opaque handles decouple identity from content but need separate checksums.

Generation stamps or epochs fence stale writers and replicas. Readers ask for the exact generation authorized by namespace metadata. Storage nodes reject stale mutation tokens; reconciliation classifies older generations instead of counting them as current durability.

### Namespace, placement, and data paths

Namespace maps file/object names to attributes, access policy, logical length, block handles, snapshots, and perhaps layout policy. Placement maps handles to targets. The data path transfers block bytes between clients and storage nodes, often without proxying payload through the namespace service.

This separation scales aggregate bandwidth. A client requests metadata, receives authorized handles/locations or a computable map, selects a suitable replica using locality and health, then reads directly. On writes, metadata grants identity and policy; storage nodes accept data under tokens/generations and report durable completion; metadata commits the new file version.

Metadata is still on the correctness path even when it is not on every byte path. It establishes current namespace, authorization, generation, and completion. A cached location can become stale; the client retries through current metadata/map rules without interpreting any responding node as authoritative.

Module 012 develops namespace server internals, and Module 014 develops pipeline sequencing. Here the core invariant is that metadata resolution and byte service are distinct protocols with compatible identities.

### Explicit and computed placement

An explicit placement map stores block-to-node locations in metadata. Lookup is direct and can represent exceptions, but per-block placement state grows with block count and changes during failure/rebalance. Storage-node block reports help reconstruct or verify actual inventory.

Computed placement uses a deterministic function over object/block identity and a versioned cluster/topology map. Clients or storage nodes calculate candidate targets without a central per-object location list. Ceph's CRUSH maps objects through placement groups to OSDs, reducing per-object placement metadata and encoding failure-domain rules.

Indirection groups many objects or blocks under a placement unit. Placement groups amortize peering and placement metadata, but their count affects balance, recovery fan-out, memory, and control traffic. An especially large object can still skew capacity because placement functions do not know future object size automatically.

Computed does not mean timeless. Membership, weights, failure domains, and policy change, producing a new map epoch. Requests carry or discover map version; nodes redirect stale clients safely. Rebalance compares old and new assignments and moves only the required data while preserving availability.

### Choosing block size

Block count is approximately `L/B`; namespace memory, reports, checksums, open files, RPCs, and scheduling metadata commonly scale with count. Larger blocks amortize this overhead and enable long sequential transfers at device/network throughput.

Smaller blocks expose more placement and task parallelism and reduce a full-block repair unit. They can better isolate corruption or hot ranges. They also multiply metadata and tiny operations, and a workload with many small files may not fill even one block per file.

Large blocks can create tails: one slow disk or corrupt replica holds a longer extent; repairing one full block moves more data; a hot block limits distribution unless caching/striping adds copies. Small range reads are not necessarily forced to transfer the entire logical block, but checksumming, compression, object layout, or storage APIs can create read amplification.

Choose from actual file and request-size distributions, sequential/random mix, target task granularity, metadata capacity, network/device throughput, checksum unit, repair bandwidth/objective, placement balance, and failure rate. A universal default is not a proof for a workload.

### Logical completeness and commit

Creating a block handle does not make a valid block. States can include allocated, writing, finalized, committed, under-protected, corrupt, deleting, and tombstoned. File visibility should reference a complete compatible set under the selected commit semantics.

An acknowledgement must declare its durability level: accepted in memory, local journal, local device, replica quorum, all configured replicas, or durable metadata commit. A client timeout creates ambiguity; idempotency and generation-qualified tokens prevent duplicate or divergent blocks.

Append/mutation requires serialization. GFS used leases to choose a primary replica for mutation ordering. Other systems use single-writer rules, consensus metadata, copy-on-write immutable blocks, or primary OSDs. The exact mechanism belongs in later modules; the foundational rule is one authoritative mutation order per block generation.

Close/commit records exact block lengths and a complete file version. A crash can leave uncommitted block candidates. Reconciliation must not expose them merely because bytes exist on storage nodes.

### Integrity metadata

Checksums can cover sectors, chunks within a block, full blocks, or trees. Smaller checksum chunks localize corruption and support range verification at metadata overhead. A full-block digest binds identity strongly but may require reading the whole block to compute or verify.

Bind checksum algorithm/version, byte range, logical length, block handle/generation, and encrypted/compressed representation as appropriate. A checksum without its scope is ambiguous. Checksums stored beside data on the same failed device do not provide independent durability, though they still detect many bit changes.

On read, verify returned bytes against trusted integrity metadata before use. A mismatch marks that replica suspect/corrupt, retries another valid source, and schedules controlled repair. Do not overwrite other replicas from an unverified source.

End-to-end validation can include application-format checks beyond storage checksums. A block can be byte-perfect yet contain invalid records produced upstream. Storage integrity and dataset semantic validity are different evidence.

### Inventory and reconciliation

Storage nodes inventory local replicas and send registrations, heartbeats, block reports, or incremental changes. Metadata compares observed `(handle,generation,length,checksum,target)` with expected policy. Reports describe current observation, not authority to attach arbitrary bytes to a namespace.

Classify discrepancies. A **missing** expected replica is absent/unreachable. **Under-protected** means too few valid failure-domain copies. **Misplaced** has enough copies but violates topology policy. **Stale** has an old generation. **Corrupt** fails integrity. **Orphan** is observed but not referenced by authoritative live/snapshot metadata. **Over-replicated** exceeds desired valid copies.

Reconciliation order protects data. Confirm authoritative metadata and snapshot/tombstone horizons, find valid sources, restore required protection, then remove stale/excess/orphan data after grace and audit rules. Immediate deletion on one inconsistent view can destroy the last recoverable copy.

Reports are large at scale. Full inventories establish a baseline; incremental reports reduce steady traffic. Report IDs, epochs, sequence/completeness, and retries prevent omission or duplicate processing from being misread.

### Placement, balance, and locality

Placement must spread protection across declared failure domains while balancing bytes, IOPS, throughput, and recovery load. Equal block counts do not imply equal bytes because tail/variable objects differ. Equal bytes do not imply equal demand because hot data dominates reads.

Weighted targets reflect usable capacity or class. Draining/removing devices produces a new placement plan and migration. Rebalance consumes source reads, target writes, and network, so throttle against production objectives without leaving protection low indefinitely.

Locality-aware compute prefers a block's host or rack when queue delay and resource compatibility allow. A location list is a set of choices, not an instruction to overload the nearest replica. Cache and replica selection can spread hot reads.

Computed placement reduces metadata lookups, while explicit load-aware routing can react to current hotspots. Hybrid clients compute candidates then select using health/locality/load. Selection must stay within the authorized current replica set.

### Durability, availability, and repair

Durability means correct bytes remain recoverable under stated faults; availability means operations complete within an objective. A block can be durable on an offline device but unavailable now. A readable replica can make data available while current protection is below durability policy.

Replication and erasure coding create independent recovery information; Module 013 develops their math. The block layer records desired policy, valid current fragments/replicas, failure domains, and repair priority. Do not count a corrupt, stale, unreachable, or same-domain copy blindly.

Repair selects a verified source or sufficient valid fragments, reconstructs into a new authorized target/generation, verifies result, registers it, and only then removes obsolete data. Concurrent membership and mutation changes require epochs and idempotent operations.

Repair bandwidth can dominate after correlated loss. Prioritize blocks by remaining protection, demand, consequence, and repair cost. Backfill/rebalance must not starve foreground traffic or take so long that another failure causes data loss.

### Scrubbing and latent corruption

Normal reads sample hot data but may never touch cold blocks. Latent sector, firmware, memory, or software corruption can remain until another replica fails. Scrubbing deliberately reads bytes and verifies checksums/metadata, optionally comparing replicas.

Scrub frequency trades detection window against I/O. Set it from latent-error risk, protection, repair time, data consequence, media, and workload. Schedule/jitter scans and throttle them; synchronized full scans can saturate the cluster.

Record last verified time per replica/block, algorithm, result, source, and remediation. A “healthy node” with stale scrub age is weaker evidence than recently verified bytes. Scrub itself can expose software bugs, so canary and observe changes.

### Capacity and performance accounting

Raw device capacity is not usable logical capacity. Subtract replication/erasure overhead, checksums/metadata, filesystem reserve, journals/WAL, temporary writes, snapshots, garbage-collection lag, rebalance headroom, failed/draining devices, and operational free-space margin.

For full replication factor `r`, payload bytes alone amplify by `r`; actual physical amplification includes more. Deduplication/compression can reduce physical bytes, but repair and version retention still need headroom. Quote decimal versus binary units explicitly.

Throughput is limited by clients, metadata, storage-node CPU/memory/network, devices, racks, checksum/encoding, and replica acknowledgements. Aggregate bandwidth can hide one hot node. Measure IOPS, request/byte sizes, queueing, p50/p95/p99/max latency, local/remote reads, cache hits, repairs, scrub, and foreground/background interference.

Small files are a metadata and request problem even when their total bytes are modest. Packing/container formats can amortize blocks and seeks, but complicate random update, deletion, and recovery. Later module 019 treats this pathology in depth.

### Security and multitenancy

Authorize namespace operations and data-plane block access. A block handle should not be a bearer secret. Use scoped short-lived capabilities/tokens or authenticated requests binding operation, tenant, handle, generation, range, and expiry.

Encrypt data in transit and at rest under the threat model; preserve integrity and key lifecycle. Device retirement requires secure erasure or cryptographic key destruction with audit. Deduplication across tenants can leak equality or usage patterns.

Quotas and isolation cover logical bytes, physical policy overhead, IOPS, bandwidth, metadata, snapshots, and repair impact. One tenant's hot blocks, tiny objects, or deletion burst must not exhaust shared metadata or recovery capacity.

### Observability and evidence

Retain namespace file version and extent map, block/generation/length/checksum, desired policy, placement/map epoch, actual valid locations, failure domains, last verification, access state, and lifecycle/tombstone. Avoid exposing sensitive handles in broad metrics.

Metrics include logical/physical/usable bytes, blocks/files, full/partial distribution, replicas/fragments by state, under-protected bytes, corrupt/missing/orphan counts, report lag, read/write bytes/ops/latency, checksum failures, scrub age/rate, repair backlog/rate, rebalance movement, and device/rack skew.

Tie a read failure to exact client, file version, block generation, requested range, selected replica, map epoch, checksum result, retry, and outcome. Tie a durability claim to current valid failure-domain evidence, not only desired replication configuration.

## Definitions and Notation

Let a file version have length `L>=0` and ordered extent list `F=[(h_i,o_i,l_i)]`. For a dense nonsparse file, extents cover `[0,L)` exactly, do not overlap, and appear in increasing `o_i`. Each `h_i` is generation-qualified.

For fixed maximum block size `B>0`, block count `n=ceil(L/B)` for `L>0` and zero for `L=0`. Block `i` covers `[iB,min((i+1)B,L))` and length `l_i=min(B,L-iB)`.

A requested range `[a,a+m)` is valid when `0<=a<=L`, `m>=0`, and `a+m<=L`. Its intersection with block `i` is `[max(a,iB),min(a+m,iB+l_i))` when nonempty. The storage request uses intra-block offset `max(a,iB)-iB` and intersection length.

Let layout epoch `e` define topology/membership/policy map and `P_e(h)` the ordered or unordered set of authorized storage targets for handle `h`. Actual observations `O(h)` must be reconciled against `P_e`, generation, length, integrity, and namespace liveness.

With full replication factor `r`, ideal payload physical bytes equal `rL` and payload amplification is `r` for `L>0`. Actual capacity adds metadata, checksum, journal, temporary, snapshot, reserve, and repair terms and may subtract compression/deduplication.

Let `V(h)` be currently valid compatible replicas across failure domains and desired policy `D(h)`. “Available” depends on an accessible valid member; “protected” requires `V(h)` to satisfy `D(h)` under the topology model. They are not equivalent predicates.

## Mechanisms, Invariants, or Proof Structure

To design or audit a distributed block layer:

1. Name the abstraction layer, workload, and byte-range semantics.
2. Define block handles, generations, file versions, logical offsets, and tail behavior.
3. Separate namespace mapping, placement/map epoch, node inventory, and data transfer.
4. Define acknowledgement, mutation order, completion, and visibility evidence.
5. Bind length and integrity metadata to exact bytes and generation.
6. Map desired/actual copies across real failure domains.
7. Reconcile missing, stale, corrupt, orphan, excess, and misplaced replicas safely.
8. Account logical, physical, temporary, repair, and reserved capacity plus foreground/background I/O.
9. Test range mapping, failures, stale epochs, corruption, reports, repair, and cleanup.
10. Review data consequence, security, retention, and recovery requirements.

The following fixture calculates fixed-size block extents, replication payload, a cross-boundary range, and a simple full-replica repair size. It does not model a production protocol, metadata, compression, or erasure coding.

<!-- bijux-verify: {"id":"block-extent-accounting","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"file_bytes=288358400 block_size=134217728 block_count=3\nblock_lengths=(134217728, 134217728, 19922944)\nreplicated_bytes=865075200 storage_amplification=3.00\nrange_fragments=((0, 125829120, 8388608), (1, 0, 12582912))\nrepair_bytes_one_full_replica=134217728\n","stderr":""}} -->
```python
MIB = 1024 * 1024
file_bytes = 275 * MIB
block_size = 128 * MIB
replication = 3

block_count = (file_bytes + block_size - 1) // block_size
block_lengths = tuple(
    min(block_size, file_bytes - index * block_size)
    for index in range(block_count)
)


def range_fragments(offset, length):
    end = offset + length
    fragments = []
    for index, size in enumerate(block_lengths):
        block_start = index * block_size
        block_end = block_start + size
        left = max(offset, block_start)
        right = min(end, block_end)
        if left < right:
            fragments.append((index, left - block_start, right - left))
    return tuple(fragments)


replicated_bytes = file_bytes * replication
print(
    f"file_bytes={file_bytes} block_size={block_size} "
    f"block_count={block_count}"
)
print(f"block_lengths={block_lengths}")
print(
    f"replicated_bytes={replicated_bytes} "
    f"storage_amplification={replicated_bytes / file_bytes:.2f}"
)
print(f"range_fragments={range_fragments(120 * MIB, 20 * MIB)}")
print(f"repair_bytes_one_full_replica={block_lengths[1]}")
```

The fixture uses binary MiB. The tail is 19 MiB, not another 128-MiB allocation in the logical model. The cross-boundary read consumes exactly 20 MiB from two handles. Real physical capacity can allocate more due to local extents, checksums, replication metadata, journals, snapshots, and reserve.

Correctness proof checks ordered extent coverage, handle/generation uniqueness, authoritative commit, and exact range reconstruction. Durability proof checks valid independent recovery information under named faults. Performance claims need workload distributions and foreground/background contention. None follows from the block-count calculation alone.

## Alternatives and Trade-Offs

Central explicit placement simplifies exceptional mapping and direct inventory queries but grows per-block metadata and update load. Computed placement scales location derivation and moves intelligence to clients/nodes, but requires synchronized topology maps, deterministic rules, and careful remapping. Indirection through groups amortizes control state while changing balance/recovery granularity.

Fixed-size block boundaries simplify offsets, parallel scanning, and predictable maximum repair units. Variable extents reduce tail waste and can follow content boundaries, compression, or write patterns, but require richer metadata and fragmentation control. Content-defined chunks aid deduplication and incremental change while adding hashing and boundary variability.

Immutable blocks plus copy-on-write simplify snapshots, caching, integrity, and concurrent readers. Mutable blocks support in-place workloads but need ordering, leases/locks, journaling, and replica consistency. Append-only semantics lie between them and suit many analytical logs.

Large blocks reduce metadata and favor sequential throughput; small blocks improve parallelism and repair granularity. Packing small files reduces metadata at the cost of independent deletion/update and may amplify reads. No block size is universally optimal.

Replication enables direct reads and simple repair at high capacity cost. Erasure coding reduces steady capacity but adds fragment fan-out, compute, and degraded-read/repair complexity. Module 013 develops the choice.

Checksums per small sub-block localize corruption and range verification but add metadata. Whole-block content digests strengthen identity but cost full scans and complicate mutation. Layered checksums can serve both.

Locality-biased reads reduce network while risking hotspot concentration. Load-aware remote reads spend network to reduce queueing. Hedged reads can cut tails but amplify I/O. Use deadlines, cancellation, and evidence rather than duplicating every read.

## Failure Modes and Misconceptions

1. **A distributed block is a disk sector.** It is a larger logical storage-system unit.
2. **A pathname identifies immutable bytes.** Names can be renamed, deleted, recreated, or versioned.
3. **Block ordinal is a durable handle.** Metadata must supply generation-qualified identity.
4. **Location is part of block identity.** Placement changes while logical identity can remain.
5. **Computed placement never changes.** Membership/policy maps have epochs.
6. **A node report is namespace authority.** It is observed inventory to reconcile.
7. **An observed replica counts toward durability.** It may be stale, corrupt, or same-domain.
8. **Three devices mean three failure domains.** They can share host, rack, power, or controller.
9. **Checksums create redundancy.** They detect changes but do not supply replacement bytes.
10. **Replication proves semantic correctness.** It can preserve identical bad input faithfully.
11. **All full-size blocks consume exactly `B` physical bytes.** Encoding and allocation differ.
12. **The tail block is always full.** Logical length bounds its valid bytes.
13. **Range reads always transfer a full block.** API/layout determine transfer amplification.
14. **Larger blocks only reduce metadata.** They alter parallelism, tails, and repair.
15. **Smaller blocks only improve repair.** They multiply control and request overhead.
16. **Equal block counts balance capacity.** Variable/tail sizes differ.
17. **Equal bytes balance performance.** Hotness and device capability differ.
18. **Allocated means committed.** Candidates can remain incomplete after failure.
19. **Timeout means a write failed.** The durable effect may have occurred without acknowledgement.
20. **Deleting every orphan immediately saves space safely.** Metadata lag/snapshots can make classification transient.
21. **Rebalance is free background work.** It competes for disk, network, and CPU.
22. **Local disk implies durable cluster state.** Host/device loss defines durability.
23. **Scrubbing hot data is enough.** Cold replicas can hide latent corruption.
24. **Aggregate free space prevents write failure.** One target/domain can fill or throttle.
25. **Storage validity proves appropriate use.** Domain semantics and retention need separate review.

## Worked Examples

### Example 1

**Question:** How many 64-MiB blocks hold a 130-MiB dense file?

**Reasoning:** Ceiling division gives three; their logical lengths are 64, 64, and 2 MiB.

**Conclusion:** Tail length follows file length, not maximum block size.

### Example 2

**Question:** Can a reader derive the durable handle as `path + block_index`?

**Reasoning:** Not safely across rename, deletion/recreation, snapshots, or generation changes.

**Conclusion:** Resolve ordered generation-qualified handles from metadata.

### Example 3

**Question:** Why may a client read block bytes without proxying through the metadata server?

**Reasoning:** Metadata grants current identity, authorization, and locations/map; storage nodes serve the data plane directly.

**Conclusion:** Separate control authority from bulk-byte bandwidth.

### Example 4

**Question:** A block report lists an old generation and two current replicas. Is replication three?

**Reasoning:** No. The stale generation cannot satisfy current recovery policy.

**Conclusion:** Count only compatible validated replicas.

### Example 5

**Question:** A checksum fails on one replica. Copy it to restore count?

**Reasoning:** No. Read another verified source, reconstruct, verify, then register the replacement.

**Conclusion:** Repair begins from trusted bytes.

### Example 6

**Question:** Why can one huge object defeat balanced placement groups?

**Reasoning:** The hash balances identities, not unknown byte sizes; its target devices receive disproportionate capacity.

**Conclusion:** Observe byte and demand skew, not only object counts.

### Example 7

**Question:** Does an acknowledged local-disk write satisfy a three-rack durability policy?

**Reasoning:** No. The acknowledgement contract has reached only one failure domain.

**Conclusion:** Name persistence and protection level in every acknowledgement.

### Example 8

**Question:** Why delay orphan deletion after coordinator recovery?

**Reasoning:** Namespace state, reports, snapshots, and tombstones may still be reconciling; the apparent orphan may be the last valid candidate.

**Conclusion:** Use epochs, grace, and authoritative reconciliation.

### Example 9

**Question:** A rebalancer saturates disks while foreground latency rises. Add clients?

**Reasoning:** Clients cannot create device capacity. Throttle/prioritize repair using protection risk and objectives, or add genuine capacity.

**Conclusion:** Background storage work belongs in capacity accounting.

### Example 10

**Question:** Can three verified replicas approve retention of child-protection evidence?

**Reasoning:** No. Lawful basis, access, sealing, chain of custody, correction, disclosure, retention/deletion, jurisdiction, trauma-informed handling, and safety consequences require named safeguarding, legal, records, privacy/security, evidence-governance, accessibility, operations, and independent child-safety review. No external approval is claimed here.

**Conclusion:** Byte durability cannot decide lawful or safe retention.

## Cross-Program Connections

[Operating Systems](../../22-operating-systems/ROADMAP.md) supplies devices, filesystems, allocation, caching, checksums, and I/O scheduling. [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies storage media, controllers, DMA, buses, and memory hierarchy. [Network Engineering](../../24-network-engineering/ROADMAP.md) supplies topology, transfer, congestion, and failure paths.

[Database Engineering](../../18-database-engineering/ROADMAP.md) owns pages, records, logs, buffer management, and transactions above/beside block layers. [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies extent maps, trees, hashing, bitmaps, and sketches. [Distributed Systems Engineering](../../27-distributed-systems-engineering/ROADMAP.md) owns leases, replication protocols, consensus, failure detection, and consistency.

[Data Engineering](../../19-data-engineering/ROADMAP.md) consumes files/objects for pipelines and manages layout/compaction. [Data Architecture Engineering](../../20-data-architecture-engineering/ROADMAP.md) owns lifecycle, authoritative data, retention, residency, and recovery policy. [Platform Engineering](../../29-platform-engineering/ROADMAP.md) owns storage service provisioning, quotas, isolation, monitoring, and operations.

GFS demonstrates large chunks, master metadata, direct chunkserver I/O, leases, checksums, replication, and garbage collection. HDFS documents NameNode namespace/block metadata, DataNode byte storage, block reports, replication, checksums, and rack-aware design. Ceph/RADOS demonstrates objects, direct OSD access, placement groups, CRUSH-computed topology placement, epochs, peering, and recovery. Colossus illustrates evolution toward distributed metadata, direct file servers, background custodians, and storage tiers.

## References

- Sanjay Ghemawat, Howard Gobioff, and Shun-Tak Leung, [*The Google File System*](https://research.google/pubs/the-google-file-system/), SOSP, 2003. Primary chunk, master/chunkserver, lease, checksum, replication, mutation, and garbage-collection design.
- Apache Hadoop Project, [*HDFS Architecture*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html), checked 2026-09-03. Official current NameNode, DataNode, block, replication, checksum, write, and rack-awareness documentation.
- Apache Hadoop Project, [*DataNode API*](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-hdfs/build/source/hadoop-hdfs-project/hadoop-hdfs/target/api/org/apache/hadoop/hdfs/server/datanode/DataNode.html), checked 2026-09-03. Official current block-to-byte-stream and inventory-report role.
- Sage A. Weil et al., [*Ceph: A Scalable, High-Performance Distributed File System*](https://www.usenix.org/event/osdi06/tech/full_papers/weil/weil.pdf), OSDI, 2006. Primary object, OSD, placement-group, CRUSH, metadata/data separation, and recovery design.
- Ceph Foundation, [*Ceph Architecture*](https://docs.ceph.com/en/latest/architecture/), checked 2026-09-03. Official current RADOS, client, monitor, OSD, pool, placement, replication, and recovery overview.
- Ceph Foundation, [*CRUSH Maps*](https://docs.ceph.com/en/latest/rados/operations/crush-map/), checked 2026-09-03. Official current topology hierarchy, device weight, placement policy, and failure-domain rules.
- Ceph Foundation, [*Placement Groups*](https://docs.ceph.com/en/latest/rados/operations/placement-groups/), checked 2026-09-03. Official current object-to-PG mapping, balance, overhead, and recovery behavior.
- Dean Hildebrand and Denis Serenyi, [*A Peek Behind Colossus, Google's File System*](https://cloud.google.com/blog/products/storage-data-transfer/a-peek-behind-colossus-googles-file-system), Google Cloud, 2021. Official Colossus client, curator, metadata, data-server, custodian, and tier overview.
- Larry Greenfield and Seth Pollen, [*How Colossus Optimizes Data Placement for Performance*](https://cloud.google.com/blog/products/storage-data-transfer/how-colossus-optimizes-data-placement-for-performance/), Google Cloud, 2025. Official current Colossus placement, workload, storage-tier, and scale context.
- Brad Calder et al., [*Windows Azure Storage: A Highly Available Cloud Storage Service with Strong Consistency*](https://azure.microsoft.com/en-us/blog/sosp-paper-windows-azure-storage-a-highly-available-cloud-storage-service-with-strong-consistency/), SOSP, 2011. Primary storage-stamp, front-end, partition, stream, replication, and consistency architecture summary.

## Exercises

### Exercise 1

Map a 410-MiB dense file into 128-MiB blocks. Give block count and lengths, then map a 30-MiB range starting at offset 250 MiB.

### Exercise 2

Design a block identity and metadata record that remains safe across rename, snapshot, deletion/recreation, replica movement, stale reports, and retry.

### Exercise 3

A cluster reports three replicas: two current copies on separate devices in one host and one stale copy in another rack. Evaluate availability and a policy requiring three current replicas across racks.

### Exercise 4

A 10-PiB logical store uses three full replicas and reserves 15% of raw capacity for repair/rebalance/free-space headroom. Estimate minimum raw payload-plus-headroom capacity under a clearly stated convention, then list omitted overheads.

### Exercise 5

A research archive stores irreplaceable human-subject data as distributed blocks. Specify identity, integrity, placement, inventory, scrub, repair, security, retention, evidence, and named review requirements.

## Answers to the Exercises

### Answer 1

Ceiling division yields four blocks with logical lengths 128, 128, 128, and 26 MiB. Range `[250,280)` takes 6 MiB from block 1 at intra-block offset 122 MiB and 24 MiB from block 2 at offset zero. Metadata supplies the actual handles/generations; these indices only calculate extent geometry.

### Answer 2

Use namespace/pool ID, opaque block handle, generation, owning file version or immutable-reference set, logical offset/length, committed state, checksum algorithm/value/scope, layout policy, creation/map epoch, encryption/key reference, and lifecycle/tombstone identity. Namespace entries map current/snapshot file versions to handles; placement records or computation are epoch-qualified and separate. Storage-node reports contain handle, generation, length, checksum evidence, node/device/domain, and report epoch/sequence. Idempotency tokens fence retries, and tombstone/grace state prevents delayed reports from attaching or deleting data across pathname reuse.

### Answer 3

At least one current copy is readable while the host is available, so present availability may exist. There are only two current replicas and both share a host, giving one current host failure domain; the stale rack copy cannot reconstruct the current generation. The three-current-across-racks policy is unsatisfied. Prioritize repair from a verified current source into authorized distinct racks, verify/register replacements, and do not delete the stale copy until reconciliation and recovery policy permit.

### Answer 4

Three full replicas require 30 PiB of raw payload. If the convention is that payload may occupy at most 85% of installed raw capacity, installed capacity is `30/0.85≈35.294 PiB`. If “add 15% on top” were intended, it would instead be 34.5 PiB; the policy must say which. Omitted costs include checksums, metadata, journals/WAL, filesystem/device reserve, encoding/alignment, temporary writes, snapshots/versions, garbage-collection lag, failed/draining devices, hot-tier caches, encryption metadata, scrubbing/repair I/O, capacity skew, and unit/vendor provisioning effects.

### Answer 5

Use immutable archive/object version and generation-qualified block handles; exact extent maps, lengths, format/schema/provenance, checksums and independent fixity manifests; replicas/fragments across justified failure domains and administrative threats; complete signed/authorized inventory with report epochs; scheduled scrubbing based on media/risk; verified-source repair with generation fencing and post-repair validation; and disaster restore drills. Encrypt in transit/at rest with governed keys, least privilege, tamper-evident audit, residency, secure device retirement, and protected metadata. Retention, consent withdrawal, legal holds, controlled access, de-identification limits, and deletion proofs must coexist with snapshot/backup/repair lifecycles. Named review includes principal investigators and data stewards, research ethics/IRB authority, participant/community representation, privacy/legal/records, cybersecurity/key management, archival/storage specialists, disaster recovery, accessibility, and independent research-integrity assurance. Local block validation does not constitute external ethical or archival approval.
