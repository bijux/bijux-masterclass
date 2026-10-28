---
module_id: DBE-026
program: Database Engineering
level: 1
module_number: 26
title: Buffer Pools
status: complete
last_verified: 2026-08-30
---

# Buffer Pools

## One-Page Review

### Governing question

How does a database safely map persistent page identities to reusable memory frames so concurrent operators can share cached pages without reading stale identities, evicting active data, exposing incomplete I/O, or losing dirty changes?

### Essential definitions

A **buffer pool** is engine-managed memory containing fixed-size **frames** that can hold database pages. A **page table** maps a complete page identity—such as database/tablespace, relation generation, fork/file, and block—to its resident frame. A **hit** finds a valid resident page; a **miss** needs allocation and usually storage I/O. A **pin** or reference prevents frame reuse while a caller may access it. A **content latch** protects short page-memory reads or mutations; it is distinct from a transaction lock. A **dirty frame** differs from its durable page and must obey WAL/flush rules before reuse. **Single-flight** miss handling lets concurrent requests for the same absent page share one load.

### Central model, mechanism, or theorem

At any instant, each valid resident page identity maps to at most one frame, and a frame represents at most one published identity. A caller must pin a matching frame before using it, then take the required content latch. On a miss, the manager reserves a free/eligible frame, installs a transient loading state, performs and validates I/O, then atomically publishes validity and wakes waiters. A frame is reusable only when no pins, latches, I/O, or correctness-critical ownership remain and any dirty image has been safely written under recovery rules.

### Critical invariants

- Page identity includes every component needed to distinguish database, relation generation, fork/file, and block.
- Page-table entry, frame tag, generation/state, and bytes agree before a hit is returned.
- Every user holds a pin for the entire interval in which the frame might otherwise be recycled.
- Page content is read or mutated under the engine's required latch; pinning alone does not serialize bytes.
- One absent-page load is shared or races are resolved without publishing duplicate valid frames.
- I/O completion validates length, identity, format, checksum/authentication, and cancellation before `valid` publication.
- Dirty pages are never discarded; required WAL/log is durable before the corresponding page write.
- Errors remove or invalidate loading mappings, release reservations, and wake every waiter with a defined outcome.

### Common failures

Failures include using an incomplete page key; touching a frame after unpin; holding a latch without a pin; confusing transaction locks with buffer latches; treating “in page table” as “valid”; issuing duplicate reads for one miss; publishing before checksum and identity validation; evicting a pinned or I/O-active frame; dropping a dirty page; measuring hit ratio without workload or latency; sizing only page bytes while ignoring descriptors/hash/latches; allocating nearly all host RAM and triggering OS pressure; warming synthetic pages that displace the real working set; and querying detailed cache views so aggressively that observation perturbs production.

### Compact example

A three-frame teaching pool loads A into frame 0; a second fetch of A hits the same frame and raises its pin count to two. After releasing both pins, B and C occupy frames 1 and 2. B is dirty; C remains pinned. Attempting to reuse frame 2 for D is rejected because C is pinned. Reusing clean, unpinned frame 0 succeeds: A's mapping is removed only as frame 0 is retagged and D is loaded/validated. Final mappings are B→1, C→2, D→0; B remains dirty and therefore protected from silent reuse.

### Connections

[DBE-021](021-pages-blocks-and-database-files.md) defines persistent page identity and [DBE-025](025-database-page-free-space-management.md) supplies insertion candidates. [DBE-027](../ROADMAP.md) selects victims; [DBE-028](../ROADMAP.md) governs dirty writeback.

## Governing Question

Storage pages are persistent units; query operators need memory. Reading the same page from storage for every tuple access would be catastrophically expensive, while allowing every operator to retain arbitrary page copies would waste memory and break coherence. The buffer manager centralizes residency: a bounded collection of frames, metadata, lookup, synchronization, I/O, and lifecycle rules.

The difficult part is not copying `P` bytes. It is proving that those bytes belong to the requested page and remain in the same frame while a caller uses them; coordinating simultaneous hits, misses, writers, eviction, and I/O; and preserving recovery order for dirty pages. A fast cache with a stale-tag race is a corruption mechanism.

## Why This Matters

Buffer pools determine the latency difference between nanosecond-scale memory access and storage I/O, the effective reach of indexes and scans, checkpoint/writeback pressure, and the memory available to execution, locks, plans, connections, the operating system, and other services. They are shared contention surfaces: page-table partitions, descriptor state, free lists, victim selection, I/O queues, and hot page latches can dominate workload latency.

Metrics are frequently misread. A 99% hit rate can hide a disastrous 1% of synchronous remote reads, while a lower hit rate with effective prefetch and fast sequential I/O can perform well. Free frames near zero may be normal because cache memory is intended for use. Dirty frames, pins, pending I/O, waits-for-free, churn, page classes, and latency distributions give the missing context.

Buffer sizing is system design. More frames extend cache reach, but descriptors and hash tables add overhead; large dirty inventories increase checkpoint work; process/OS memory pressure can cause swapping or reclaim; NUMA placement changes latency; and buffered I/O can duplicate pages in the OS cache. The correct size comes from measured working sets and failure headroom, not a universal percentage.

## Prerequisites and Retrieval

Retrieve database pages and checksums, relation generations/forks, hash tables, finite-state machines, reference counts, latches and memory ordering, asynchronous I/O, WAL, dirty pages, cache locality, virtual memory, NUMA, and transaction locks.

Distinguish persistent page from memory frame; page table from database table; pin from content latch from transaction lock; resident from loading from valid; hit from logical read from physical device read; dirty from durable; free frame from clean evictable frame; database buffer pool from OS page cache; memory allocation from resident working set; and point-in-time per-frame consistency from a cache-wide snapshot.

## Learning Objectives

After this module, you should be able to:

1. define the complete frame/page-table state model;
2. trace hit and miss paths including single-flight I/O;
3. explain pin, latch, transaction-lock, and I/O ownership separately;
4. validate page identity and bytes before publication;
5. derive frame counts and metadata overhead from memory/page sizes;
6. classify clean, dirty, loading, pinned, and evictable states;
7. reason about shared, partitioned, local, and OS-backed cache designs;
8. interpret cache metrics without relying on hit ratio alone;
9. diagnose stalls, churn, duplicate reads, and memory pressure; and
10. test buffer lifecycle, concurrency, I/O failure, and recovery boundaries.

## Core Exposition

A frame is a memory region large enough for one engine page plus separately stored descriptor state. The descriptor can contain page tag, state flags, pin/reference count, dirty bit, usage/replacement metadata, I/O ownership/wait state, content latch, checksum/LSN context, and links or shard identifiers. Page bytes and descriptor must be treated as one lifecycle even when allocated separately.

A page tag must identify persistent bytes unambiguously. Relation name and block number are insufficient: databases, tablespaces, forks, indexes, temporary objects, and generations after truncate/rewrite can share numbers over time. PostgreSQL's cache inspection, for example, exposes database, tablespace, filenode, fork, and block components. Exact engine tags vary.

The page table is commonly a hash structure from tag to frame descriptor. It supports fast hit detection but is itself concurrent mutable state. Sharding/partitioning reduces one global lock, at the cost of cross-partition operations and load imbalance. The mapping must not outlive frame retagging or appear only after another thread has already published a duplicate page.

Frame state is richer than occupied/free. A useful abstract machine includes free, reserved, loading, valid-clean, valid-dirty, writeback, eviction/retagging, and error. Pins, latches, and I/O references refine these states. Not every implementation names them this way, but every transition must prevent consumers from seeing incompatible tag/byte pairs.

On a hit, lookup finds a candidate descriptor. The caller atomically pins it or otherwise obtains a stable reference, then rechecks that its tag/state still match; otherwise it releases and retries. This “pin then revalidate” pattern closes a race where eviction retags the frame between lookup and pin. After a valid pin, the caller acquires a content latch appropriate to its operation.

A pin protects frame identity/lifetime, not tuple bytes. A shared/read latch permits compatible readers; an exclusive/write latch permits mutation. A transaction lock or MVCC rule protects logical isolation over longer intervals and may survive after the page latch is released. Holding page latches for user/network waits or long computation destroys concurrency and risks deadlocks.

PostgreSQL's official buffer implementation notes explicitly separate reference-count pins from buffer content locks: an unpinned frame can be reclaimed, and a pin is required before locking/access. That is one concrete protocol, not a guarantee that all engines expose identical APIs or lock modes.

On a miss, the manager must prevent duplicate authoritative loads. Under single-flight behavior, one requester installs or claims a loading entry while later requesters attach as waiters. The owner obtains a free or eligible victim frame, preserves dirty/recovery obligations if needed, assigns a transient tag/state, submits I/O, and eventually publishes success or failure.

Publishing a loading frame as a hit is unsafe. Storage can return a short read, wrong block after address/identity bugs, torn/corrupt bytes, unsupported page version, authentication failure, cancellation, timeout, or I/O error. The manager validates the full page under engine rules before changing state to valid. Waiters must observe the state transition with correct memory synchronization.

On load failure, the mapping cannot remain a normal resident hit. The owner marks error/removes the transient entry under the lookup protocol, releases the frame reservation, and wakes every waiter. Depending on error class, waiters retry, receive the same error, or enter corruption/recovery handling. Resource cleanup must work under cancellation and exceptions.

Multiple copies can exist below or above the database pool: filesystem page cache, block-device/controller cache, remote-storage cache, replica cache, and CPU caches. They do not replace database pins, page latches, WAL ordering, or transaction visibility. Buffered I/O may duplicate memory; direct I/O changes alignment and prefetch responsibilities but not the buffer manager's coherence contract.

A logical read is a request for a database page. A buffer hit satisfies it from a resident valid frame. A miss may cause one or several physical/storage operations due to readahead, merging, compression, encryption, redundancy, filesystem/device granularity, or remote protocols. SQL Server official documentation similarly distinguishes logical reads from physical reads that populate the buffer cache.

Prefetch/read-ahead reserves frames and starts loads before demand reaches them, overlapping I/O and computation. A prefetched page that is never used consumed bandwidth and cache space. Demand must join an in-flight prefetch instead of launching a duplicate read. Prefetch correctness is identical to demand load; only timing and replacement treatment differ.

Newly allocated pages can be created in frames without reading old storage content, but allocation, initialization, WAL, checksum, and publication rules still apply. A zeroed memory frame is not automatically a valid new page. Page identity must be durably allocated and the page initialized under the access method.

Modification requires an exclusive content protocol, WAL/undo creation where applicable, page LSN/version and checksum handling, and dirty publication before releasing appropriate protection. Marking dirty means memory differs from durable storage; it does not mean the transaction is committed or the page has been written. Many transactions can modify one dirty frame before one later write.

A dirty frame is not an eligible silent victim. It can become reusable only after the engine schedules and successfully completes a permitted page write, respecting write-ahead order and any doublewrite/full-page/checksum/encryption mechanisms. DBE-028 treats writeback; DBE-029 treats corruption.

Pins are resource obligations. A leaked pin gradually removes frames from the evictable population and can stall the database despite abundant configured memory. Long pins can be legitimate for an active scan but must be observable and bounded by ownership. Pin underflow/double release is as dangerous as leakage because it can make an active frame appear reusable.

When all frames are pinned, dirty awaiting flush, loading, or otherwise ineligible, a miss must wait, help progress, fail under policy, or acquire emergency capacity. It must not evict an active frame. Metrics such as waits for free buffers, pin age, writeback backlog, pending reads, and latch waits distinguish the cause.

Replacement metadata estimates future reuse; DBE-027 covers LRU/clock/scan-resistant policies. At this boundary, a victim selector may only propose. The buffer manager atomically verifies the frame remains unpinned, correctly tagged, not I/O-owned, and clean or safely flushed before recycling. Selection and authorization are separate.

Cache capacity is not simply `memory/page_size`. If budget `M` includes `F` frames of `P` bytes and descriptor/lookup overhead approximately `d` per frame plus fixed `K`, then `F<=floor((M-K)/(P+d))`. Alignment, allocator fragmentation, NUMA metadata, hash load factor, compression dual images, and huge-page rounding alter actual use.

Page size changes both payload and metadata ratios. Smaller pages give finer cache granularity but require more descriptors/hash entries/latches and I/O operations for the same bytes. Larger pages amortize metadata and improve sequential transfer but amplify random reads/writes and evict more unrelated content. Page size is an engine-format choice, not merely buffer tuning.

Shared pools maximize cross-session reuse but create synchronization/NUMA contention. Per-process/local pools simplify ownership but duplicate hot pages and complicate coherence. Multiple pool instances/shards reduce latch contention while risking uneven residency. Separate pools/rings for scans, temporary pages, compressed images, or page classes can protect hot workloads but partition capacity.

Warmup can load recorded/hot pages after restart and reduce cold latency, but the recorded workload may be obsolete; indiscriminate warmup competes with recovery and user I/O. Persist only identities, never treat cached bytes as durable truth unless the product explicitly implements persistent memory with recovery semantics.

Large scans can pollute a general cache by replacing frequently reused pages with one-touch pages. Scan rings, admission control, bypass, midpoint insertion, and page-class policies mitigate this; these are replacement/admission choices for DBE-027. Operators should measure “read ahead evicted without access” or equivalent evidence rather than assume every filled frame is valuable.

Security matters because cached frames hold plaintext row/index contents, sometimes after storage decryption. Core dumps, debugger access, crash artifacts, swap, hibernation, and memory scraping can expose them. MySQL documents an option affecting inclusion of buffer-pool pages in core files. Protection requires least privilege, dump policy, encryption/keys, swap/core controls, and evidence handling.

Inspection views are observations, not necessarily atomic snapshots. PostgreSQL documents that `pg_buffercache` avoids buffer-manager locks and provides self-consistent information per buffer but not a consistent state across all buffers. MySQL warns detailed `INNODB_BUFFER_PAGE` inspection can affect performance. Use low-impact aggregate metrics in routine monitoring and detailed views in controlled diagnosis.

Core metrics include logical requests, hits/misses, miss latency by storage/page class, in-flight and duplicate/coalesced reads, free/valid/dirty/loading/writeback frames, pinned count and age, free-buffer waits, latch contention/hold time, page-table lookup contention, eviction outcomes, dirty-victim rejections, prefetch usefulness, churn, working-set reuse distance, NUMA distribution, memory/descriptor overhead, OS reclaim/swap, and checkpoint backlog.

Hit rate must declare denominator and interval. `hits/(hits+misses)` can be distorted by repeated accesses to one hot catalog page, while rare misses dominate latency. Compare service time contribution, tail latency, page classes, working-set changes, and storage utilization. Reset/restart effects and counter wrap/sampling windows matter.

Testing should cover repeated hits, simultaneous same-page misses, different-page hash collisions, every frame state, pin/latch races, victim retagging, dirty rejection, I/O success/short/error/cancel, wrong identity/version/checksum, waiter wakeup, relation truncate/rewrite, all-pinned exhaustion, prefetch-demand join, memory pressure, resize, NUMA/shards, crash during load/write, and recovery. Model checking and race instrumentation complement deterministic unit tests.

The executable model below demonstrates a single-threaded subset: unique page-table mapping, hit pin increments, release, dirty protection, pinned-victim rejection, clean reuse, and accounting. Victim choice is explicit so it does not smuggle DBE-027's policy into this module. It is not concurrent, asynchronous, durable, or vendor-compatible.

<!-- bijux-verify: {"id":"buffer-frame-lifecycle","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"a_frames=(0, 0)\nafter_load=((0, 'A', 0, False, True), (1, 'B', 0, True, True), (2, 'C', 1, False, True))\nblocked=('D', 2, 'pinned')\nd_frame=0\nfinal=((0, 'D', 0, False, True), (1, 'B', 0, True, True), (2, 'C', 0, False, True))\npage_table=(('B', 1), ('C', 2), ('D', 0))\nstats=(2, 5, 4, 1)\ninvariants=True\n","stderr":""}} -->
```python
from dataclasses import dataclass


@dataclass
class Frame:
    key: str | None = None
    pins: int = 0
    dirty: bool = False
    valid: bool = False


class BufferPool:
    def __init__(self, count: int) -> None:
        self.frames = [Frame() for _ in range(count)]
        self.page_table: dict[str, int] = {}
        self.hits = self.misses = self.reads = self.blocked = 0

    def fetch(self, key: str, victim: int | None = None) -> int:
        if key in self.page_table:
            self.hits += 1
            index = self.page_table[key]
            frame = self.frames[index]
            assert frame.valid and frame.key == key
            frame.pins += 1
            return index
        self.misses += 1
        index = next((i for i, frame in enumerate(self.frames) if not frame.valid), None)
        if index is None:
            assert victim is not None
            index = victim
            old = self.frames[index]
            if old.pins:
                self.blocked += 1
                raise RuntimeError("pinned")
            if old.dirty:
                self.blocked += 1
                raise RuntimeError("dirty")
            assert old.key is not None
            del self.page_table[old.key]
        frame = self.frames[index]
        frame.key, frame.pins, frame.dirty, frame.valid = key, 1, False, False
        self.reads += 1
        frame.valid = True  # stands for successful full read and validation
        self.page_table[key] = index
        return index

    def release(self, index: int) -> None:
        assert self.frames[index].pins > 0
        self.frames[index].pins -= 1

    def mark_dirty(self, index: int) -> None:
        frame = self.frames[index]
        assert frame.valid and frame.pins > 0
        frame.dirty = True

    def snapshot(self) -> tuple:
        return tuple(
            (index, frame.key, frame.pins, frame.dirty, frame.valid)
            for index, frame in enumerate(self.frames)
        )

    def valid(self) -> bool:
        return (
            len(self.page_table) == len(set(self.page_table))
            and all(
                frame.valid and frame.key == key
                for key, index in self.page_table.items()
                for frame in (self.frames[index],)
            )
            and len({index for index in self.page_table.values()}) == len(self.page_table)
            and all(frame.pins >= 0 for frame in self.frames)
        )


pool = BufferPool(3)
a_first = pool.fetch("A")
a_second = pool.fetch("A")
pool.release(a_first)
pool.release(a_second)
b = pool.fetch("B")
pool.release(b)
c = pool.fetch("C")
b_again = pool.fetch("B")
pool.mark_dirty(b_again)
pool.release(b_again)
after_load = pool.snapshot()
try:
    pool.fetch("D", victim=c)
except RuntimeError as error:
    blocked = ("D", c, str(error))
pool.release(c)
d = pool.fetch("D", victim=a_first)
pool.release(d)

print(f"a_frames={(a_first, a_second)}")
print(f"after_load={after_load}")
print(f"blocked={blocked}")
print(f"d_frame={d}")
print(f"final={pool.snapshot()}")
print(f"page_table={tuple(sorted(pool.page_table.items()))}")
print(f"stats={(pool.hits, pool.misses, pool.reads, pool.blocked)}")
print(f"invariants={pool.valid()}")
```

The model makes a load valid immediately only as a labeled stand-in for completed validation. Real code needs a transient lookup entry, waiter ownership, memory ordering, I/O cancellation, tag recheck, content latches, WAL, and writeback.

## Definitions and Notation

Let `F` be frame count, `P` bytes per page, `d` approximate per-frame descriptor/lookup overhead, `K` fixed pool overhead, and `M` memory budget. A simple upper bound is `F<=floor((M-K)/(P+d))`. Let `R` be logical page requests, `H` valid resident hits, and `X=R-H` misses; reported hit rate is `H/R` for `R>0`, but it is not a latency or device-read model.

For page tag `t`, page table `T(t)=f` implies frame `f` is reserved/published for `t`; a hit is usable only after a successful pin and tag/state recheck. A frame is **eligible for reuse** only if its pin count is zero, no incompatible latch/I/O/reference exists, and it is clean or its dirty write is durably complete under engine rules.

## Mechanisms, Invariants, or Proof Structure

A correct buffer fetch follows these obligations:

1. Construct the complete current-generation page tag and validate requested block ownership/range.
2. Lookup under the page-table concurrency protocol.
3. On a candidate hit, acquire a pin/reference and recheck tag plus valid state; retry if retagged.
4. Acquire only the content latch needed, validate/read or mutate bytes, then release latch while retaining pin as required.
5. On miss, install/join one loading state and reserve an eligible free/victim frame without losing dirty data.
6. Submit bounded I/O; validate full length, identity, type/version, checksum/authentication, and cancellation.
7. Atomically publish valid state and wake waiters, or publish/remove error and release every resource.
8. On mutation, produce recovery information, update page metadata, mark dirty, and respect WAL-before-page ordering.
9. Unpin exactly once per acquired pin; victim selection must revalidate all eligibility predicates atomically.
10. Audit page-table/frame bijection, pins, latches, waiters, I/O, dirty/writeback, errors, memory, and workload latency.

Uniqueness is a safety property: if two independently mutable valid frames represent one page, writers can diverge and later writes race to storage. Single-flight or race resolution must produce one published frame. Pin safety is temporal: if the pin remains positive from final tag validation through last access, a correct reuser cannot satisfy zero-pin eligibility during that interval.

## Alternatives and Trade-Offs

One shared pool maximizes reuse but increases page-table/latch/NUMA contention. Sharded pools distribute synchronization but can strand capacity and duplicate policy state. Local pools simplify ownership but duplicate pages. OS-cache reliance reduces database memory management but cannot express database pins, transaction-aware dirty order, or page-class admission.

Buffered I/O benefits from OS readahead and portability but can double-cache. Direct I/O reduces duplication and gives the engine more control, while requiring alignment, explicit prefetch, and capable asynchronous I/O. Memory mapping simplifies address translation but page faults/writeback are harder to schedule under database recovery and failure handling.

Large pools improve reuse until memory pressure, dirty backlog, startup/resize cost, descriptor overhead, or diminishing working-set benefit dominates. Persistent warmup reduces cold start but consumes startup I/O and can load obsolete pages. Detailed per-frame telemetry aids diagnosis but costs CPU/latches/memory and can expose sensitive contents/identities.

## Failure Modes and Misconceptions

- “A hash-table hit is safe.” Pin and revalidate tag/state before access.
- “A pin protects bytes.” It protects lifetime; content latches protect short physical access.
- “A transaction lock pins the page.” Logical locks and physical residency have different lifetimes.
- “Loading means resident.” Bytes are unavailable until complete validation and publication.
- “Two reads of one miss are harmless.” Duplicate published frames can diverge under writes.
- “Dirty means committed.” It means memory differs from durable page, independent of visibility/commit.
- “An unpinned dirty frame is free.” It requires safe writeback before reuse.
- “High hit rate proves health.” Miss latency, dirty waits, churn, pins, and page class can dominate.
- “Use all RAM for the pool.” The OS, engine metadata, execution, connections, and failure headroom need memory.
- “Cache views are snapshots.” Some are sampled, lock-light, expensive, or inconsistent across frames.

## Worked Examples

### Example 1

The first A request misses, reserves frame 0, reads/validates A, publishes its mapping, and returns with one pin. A second request hits frame 0 and raises pins to two. Both callers can share identity while their content-latch intervals remain separately governed.

### Example 2

After both A callers release, its pin count is zero but the clean valid page remains cached. Unpinned does not mean free; it means eligible for replacement subject to policy and atomic revalidation.

### Example 3

B is fetched, pinned for modification, and marked dirty before release. Its pin becomes zero, yet it cannot be silently reused. A later victim attempt must schedule WAL-compliant writeback or choose a clean frame.

### Example 4

C remains pinned while a request explicitly proposes its frame for D. The manager rejects reuse. Evicting anyway would let C's caller read D bytes through a stale frame reference.

### Example 5

Clean unpinned A is reused for D. A's page-table entry is removed as the frame enters retag/loading state; D is published only after the modeled read validates. Final page-table values are unique frames 1,2,0 for B,C,D.

### Example 6

Two threads miss on E simultaneously. A correct manager lets one own the load and makes the other wait on that descriptor. If the read succeeds both pin the same valid frame; if checksum fails both receive defined failure and no valid E mapping remains.

### Example 7

A four-gigabyte budget, 8192-byte pages, 128-byte descriptors, and 16 MiB fixed overhead gives at most `floor((4294967296-16777216)/(8192+128))=514092` model frames. Allocator/hash/alignment/NUMA overhead can lower the observed count.

### Example 8

One million requests yield 990000 hits and 10000 misses: 99% hit rate. If hits average 2 microseconds and misses 8 milliseconds, misses contribute about 80 seconds versus 1.98 seconds for hits before concurrency. The small miss fraction dominates service time.

### Example 9

A sequential scan prefetches 64 pages, but a limit stops after two. Sixty-two unused frames and I/O operations can evict useful pages. Admission/ring policy and “prefetched then evicted unused” metrics reveal the waste.

### Example 10

Free-buffer waits spike while free frames are zero. Evidence shows 40% pinned by a leaked error path and 35% dirty behind stalled storage. Increasing pool size delays failure; fixing balanced pin release and writeback/storage progress addresses the two causes.

## Cross-Program Connections

- [Data Structures Engineering](../../17-data-structures-engineering/ROADMAP.md) supplies hash tables, finite-state machines, reference counts, and cache structures.
- [Operating Systems](../../22-operating-systems/ROADMAP.md) supplies page cache, virtual memory, direct/asynchronous I/O, NUMA, and writeback.
- [Programming Languages — Concurrent and Parallel Programming](../../04-programming-languages-concurrent-and-parallel-programming/ROADMAP.md) supplies atomic publication, latches, reference lifetimes, waiters, and race reasoning.
- [Computer Architecture](../../23-computer-architecture/ROADMAP.md) supplies cache hierarchy, memory ordering, coherence, bandwidth, and NUMA locality.
- [Systems Engineering](../../26-systems-engineering/ROADMAP.md) supplies capacity, observability, pressure handling, and fault diagnosis.

## References

1. PostgreSQL Global Development Group, [Buffer Manager README](https://github.com/postgres/postgres/blob/master/src/backend/storage/buffer/README), pin/reference and content-lock access rules plus buffer strategy notes.
2. PostgreSQL Global Development Group, [Resource Consumption](https://www.postgresql.org/docs/18/runtime-config-resource.html), PostgreSQL 18 shared-buffer and OS-cache configuration guidance.
3. PostgreSQL Global Development Group, [`pg_buffercache`](https://www.postgresql.org/docs/18/pgbuffercache.html), PostgreSQL 18 buffer identity, dirty/usage/pin fields and observation-consistency caveats.
4. Oracle, [InnoDB Buffer Pool](https://dev.mysql.com/doc/refman/8.4/en/innodb-buffer-pool.html), MySQL 8.4 residency, dirty, pending I/O, read-ahead, eviction, and monitoring documentation.
5. Oracle, [InnoDB Buffer Pool Information Schema Tables](https://dev.mysql.com/doc/refman/8.4/en/innodb-information-schema-buffer-pool-tables.html), MySQL 8.4 per-page/pool inspection documentation.
6. Microsoft, [Read Data Pages in the Database Engine](https://learn.microsoft.com/en-us/sql/relational-databases/reading-pages?view=sql-server-ver17), logical/physical reads, buffer cache, and read-ahead documentation.
7. Microsoft, [`sys.dm_os_buffer_descriptors`](https://learn.microsoft.com/en-us/sql/relational-databases/system-dynamic-management-objects/sys-dm-os-buffer-descriptors-transact-sql?view=sql-server-ver17), SQL Server resident-page descriptor documentation.
8. Raghu Ramakrishnan and Johannes Gehrke, *Database Management Systems*, 3rd ed., McGraw-Hill, 2003, buffer-management foundations.
9. Hector Garcia-Molina, Jeffrey D. Ullman, and Jennifer Widom, *Database Systems: The Complete Book*, 2nd ed., Pearson, 2008, secondary-storage and buffer-manager foundations.

## Exercises

### Exercise 1

Trace a two-frame pool through `fetch A`, `fetch A`, release one A pin, `fetch B`, mark B dirty, release B, and request C with A proposed as victim. Give mappings, pins, dirty states, hit/miss/read counts, and whether reuse is legal at each point.

### Exercise 2

For 8 GiB budget, 16 KiB pages, 192-byte descriptor overhead, and 64 MiB fixed overhead, compute the model frame upper bound and raw page bytes. Explain at least four reasons actual resident/process memory differs.

### Exercise 3

Design a same-page single-flight miss protocol including page-table races, owner/waiters, I/O validation, cancellation, error publication, and retry. State the linearization points.

### Exercise 4

Diagnose 99.7% hit rate with worsening p99 latency, free-buffer waits, increasing dirty frames, low storage throughput, and long pin ages. Give competing hypotheses, evidence, and safe actions.

### Exercise 5

Design a production buffer-pool resize and warmup experiment. Cover memory headroom, OS cache/NUMA, workload phases, cache state, metrics, dirty/checkpoint effects, security, rollback, and evidence limitations.

## Answers to the Exercises

### Answer 1

First A is a miss/read into frame 0 with pin 1; second A is a hit on frame 0 with pin 2. Releasing one leaves A pinned once, so it is not reusable. B misses/reads into free frame 1; marking dirty while pinned is legal, and release leaves B `(pins=0,dirty=true)`. C misses, but proposed A still has pin 1, so reuse is illegal and C waits/fails or another eligible frame must be found; B is also ineligible for silent reuse because dirty. Counts at that point are one hit, three misses (including C request), two completed reads, assuming rejected victim occurs before C I/O. Page table remains A→0,B→1.

### Answer 2

`M=8589934592`, `K=67108864`, and `P+d=16384+192=16576`, so the upper bound is `floor(8522825728/16576)=514166` frames. Raw page bytes are `514166*16384=8424095744` bytes (about 7.846 GiB). Actual memory differs because descriptor/hash/shard/latch structures are only approximated; allocator/alignment/huge-page rounding adds overhead; compressed and uncompressed images may coexist; memory can be committed but not resident; NUMA placement, core/dump policy, other engine components, OS cache, fragmentation, and dynamic resize also intervene.

### Answer 3

Under the appropriate page-table shard protocol, lookup either pins an existing valid frame or atomically installs one loading entry; that successful install is miss-ownership linearization. Losers attach waiter references and sleep without holding content/table latches. The owner reserves an eligible frame, reads, checks full length/tag/page type/version/checksum/authentication and cancellation, then under descriptor/table synchronization publishes valid state; that publication is successful-fetch linearization and wakes waiters, which pin/recheck the same frame. On failure, it publishes a terminal error or removes the loading entry while retaining an error result long enough to wake all current waiters; cleanup releases I/O/frame references exactly once. Retry occurs only after observing that transition and redoing lookup, preventing duplicate publication.

### Answer 4

The hit rate can coexist with a small set of very slow misses, dirty-victim stalls, storage errors/throttling, checkpoint backlog, or leaked/legitimately long pins. Break down miss/read/write latency and bytes by storage/page class; pending reads/writes, dirty age/count, WAL flush position, checkpoint progress, queue depth, errors, free-list waits, victim rejection reasons, pin owners/ages, latch waits, workload/plan changes, OS pressure/swap, and replica/backup contention. Restore storage/writeback progress and contain errors; locate balanced pin ownership and cancel only safe offending work; throttle dirty producers or scans under documented controls. Do not evict pinned/dirty frames, disable durability, or merely enlarge memory before proving the cause.

### Answer 5

Establish baseline working-set/reuse, logical/physical reads, miss tails, free/dirty/loading/pinned frames, writeback/checkpoints/WAL, OS available memory/reclaim/swap/PSI, NUMA distribution, process overhead, and workload phases. Change size incrementally within tested engine limits, leaving OS, execution, connection, maintenance, and failure headroom; observe resize duration and shard/chunk balance. Test cold start, natural warmup, and governed recorded warmup separately, labeling OS-cache state and preventing synthetic loads from evicting production-hot pages. Check dump/core exposure of cached plaintext and least-privilege telemetry. Define thresholds and rollback to the prior setting, but account for cache-state hysteresis. Repeat representative peak, scan, checkpoint, failover/restart, and storage-degradation tests; report confidence intervals and avoid treating one hit-rate improvement as universal throughput or durability evidence.
