---
module_id: CA-044
program: Computer Architecture
level: 1
module_number: 44
title: Storage Device Architecture
status: complete
last_verified: 2026-09-04
---

# Storage Device Architecture

## One-Page Review

### Governing question

How do block-storage devices translate queued logical reads, writes, flushes, discards and management commands into media operations while preserving address identity, atomicity/order/durability contracts, finite-cache ownership, error reporting, recovery, endurance and predictable performance across workload patterns?

### Essential definitions

- A **logical block address** (`LBA`) identifies a host-visible block or logical sector in a namespace/device.
- A **logical block** is the minimum host-addressable unit; it may differ from filesystem, physical sector, NAND page and erase-block sizes.
- A **request queue** holds commands awaiting device/controller service; multiqueue paths distribute submission/completion work.
- **queue depth** is outstanding command count under a stated queue/device scope.
- A **volatile write cache** acknowledges data retained in power-dependent memory before nonvolatile media completion.
- **flush** requests completion of prior relevant writes to a specified nonvolatile boundary under protocol rules.
- **force unit access** (`FUA`) requests nonvolatile completion for a particular write under supported semantics.
- A **discard/deallocate/trim** operation tells a device that selected logical blocks no longer contain required data.
- A **flash translation layer** (`FTL`) maps host LBAs to physical NAND locations and manages out-of-place writes.
- A **NAND page** is a program/read unit; an **erase block** groups many pages and is erased before reuse.
- **garbage collection** relocates valid pages and erases blocks to recover free space.
- **overprovisioning** is physical media capacity not exposed as ordinary user LBAs, used for mapping, spare space and management.
- **write amplification factor** (`WAF`) is media bytes written divided by host bytes written over a defined interval.
- **wear leveling** distributes erase/program wear across physical blocks.
- **uncorrectable bit error rate** (`UBER`) and endurance metrics have exact vendor/specification definitions and conditions.
- A **zoned device** constrains writes within zones, often requiring sequential advancement of a write pointer.

### Central model, mechanism, or theorem

A storage controller refines each accepted command `q=(opcode,namespace,LBA,length,data,attributes,ID,order)` into one terminal completion while retaining ownership of command/data/status. Logical reads return the newest completed/ordered bytes; writes become visible and durable only at the protocol's documented points. An SSD FTL maps each updated logical page to a fresh physical page, atomically updates metadata and later reclaims stale pages without losing the sole current copy. Performance and endurance depend on queueing, locality, transfer size, caching and amplification, not interface peak alone.

### Critical invariants

- Every command range is checked for namespace identity, LBA bounds, length arithmetic, alignment and permissions.
- Each accepted command produces exactly one matching terminal completion or remains explicitly outstanding.
- Read data corresponds to the newest logically visible write under ordering and cache rules.
- Acknowledged writes remain owned in protected volatile/nonvolatile state consistent with advertised power-loss guarantees.
- Flush/FUA completion corresponds exactly to the documented persistence boundary and ordering scope.
- FTL metadata never points to an incomplete/corrupt new page or loses the last valid old page during update/recovery.
- Garbage collection copies only validated current pages and does not resurrect stale versions.
- Discard cannot expose another tenant's stale data or be assumed to return a fixed value unless specified.
- Error, timeout, reset and surprise removal reconcile partial/in-flight work without silent success or unsafe replay.
- Capacity, throughput, latency, WAF and endurance claims bind exact units, workload, queue depth, firmware and state.

### Common failures

Common failures include calling a 512-byte logical sector the physical write unit, assuming a completed write is durable, issuing flush without establishing prior write order, treating discard as secure erase or guaranteed zero-read, calculating WAF from commands rather than bytes, using raw NAND capacity as user capacity, dividing interface peak by request size without queue/overhead/media limits, treating deep queues as lower latency, ignoring tail latency from garbage collection, retrying uncertain writes to non-idempotent targets, assuming RAID or ECC replaces backups, trusting SMART counters without unit/firmware definitions, comparing fresh empty SSDs with steady-state full devices, and estimating endurance without workload WAF and spare-area assumptions.

### Compact example

An invented SSD exposes 1,000 GB from 1,070 GB raw NAND, giving 7% spare capacity relative to user capacity. If 100 GiB host writes cause 160 GiB media writes, WAF is 1.60. At 500,000 4 KiB random IOPS, payload is 2.048 GB/s (decimal). A rough idealized host-endurance estimate with 3,000 P/E cycles and constant WAF is `1070*3000/1.6/1000=2006.25 TB` host writes; real endurance depends on reserved uses, workload, retention, failures and vendor warranty definitions.

### Connections

Storage device architecture connects block APIs, PCIe/NVMe, DMA/interrupt queues, scheduling, filesystems, FTL algorithms, ECC, persistence models, crash consistency, security erasure, telemetry, reliability, workload benchmarking and distributed durability.

## Governing Question

Software sees a namespace of numbered logical blocks. A device may implement those blocks with magnetic sectors, NAND pages/erase blocks, controller DRAM, mapping tables, ECC and background maintenance.

The interface intentionally hides physical placement, but it cannot hide completion, ordering, error and durability contracts. Correct systems distinguish “accepted,” “visible to reads,” “completed,” and “survives specified power loss.”

## Why This Matters

Persistent data depends on a chain from filesystem/barriers through driver/transport/controller cache to media. A mistaken flush or power-loss assumption can pass normal tests and fail only after a crash.

Flash permits no in-place overwrite without erase, so write workload and free-space state cause amplification and latency tails. Deep queues improve throughput while increasing delay and uncertainty during reset.

Device firmware is a storage computer. Its translation, ECC, garbage collection and recovery require the same explicit invariants as host software.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace DMA submission/completion queues and interrupts;
- distinguish visibility, ordering and durability;
- compute IOPS, throughput, latency and unit conversions;
- explain checksums/ECC and crash-consistent metadata at a basic level;
- reason about logical-to-physical mapping and garbage collection.

Retrieve interface/command-set/specification version; model/firmware; namespace/LBA formats, capacity and metadata/protection; queue count/depth, IDs and ordering; maximum transfer/scatter/boundary/alignment; volatile cache and power-loss protection; write-cache enable; flush/FUA/write-zeroes/discard/secure-erase semantics; atomic/write-unit guarantees; error/status/retry/reset/abort; SMART/health/endurance units; media geometry and ECC where exposed; FTL mapping/page/erase-block/spare area; GC/wear-level/background policy; zoned constraints; encryption/sanitize; multipath/reservation behavior; OS driver/filesystem/mount settings; benchmark workload, fill/precondition, queue depth and temperature; errata.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish logical blocks from media program/erase units;
2. trace submission, DMA, controller execution and completion;
3. explain volatile-cache, flush and FUA persistence boundaries;
4. model FTL mapping, out-of-place update and garbage collection;
5. calculate throughput, WAF, overprovisioning and qualified endurance estimates;
6. compare HDD, SSD and zoned-device scheduling constraints;
7. handle discard, errors, timeouts, reset and uncertain writes safely;
8. interpret health/ECC telemetry without overstating guarantees;
9. verify command/data/metadata refinement and crash recovery;
10. benchmark storage with reproducible steady-state workloads.

## Core Exposition

### Begin with the host abstraction

A namespace/device exposes LBAs and one or more logical block formats. A command names start LBA and count/length under protocol limits.

Validate arithmetic before DMA or media work. `start+count` overflow must not wrap into another range.

### Distinguish block sizes

Filesystem block, virtual-memory page, logical sector, physical sector, SSD page and erase block are different granularities. Alignment and amplification cross these boundaries.

Report each by bytes and source rather than calling all of them “block size.”

### Understand HDD media

Magnetic disks position heads over tracks; seek and rotational delay dominate small random access, while sequential transfers exploit locality. Caches and command reordering hide some mechanics.

Modern devices may expose logical geometry unrelated to exact physical sectors/tracks.

### Understand SSD media

NAND reads/programs pages but erases larger blocks. Programs typically move bits in constrained directions and pages have finite program/erase endurance.

Controllers parallelize across channels/dies/planes while managing ECC, bad blocks and mapping.

### Understand controller caches

Read caches may satisfy repeated LBAs; write caches absorb/batch writes and reorder media placement. Cache capacity/backpressure affects completion.

If volatile cache acknowledges writes, power loss can lose them unless protected or flushed under exact semantics.

### Trace command submission

Host fills a command/descriptor and data mappings, orders visibility, rings a doorbell or calls a transport. Controller fetches/validates before execution.

Submission acceptance is not device completion or durability.

### Trace completion

Device writes read data or status/completion through DMA, orders it, then interrupts or updates a polled queue. Host matches queue/command ID and synchronizes before consuming.

Unknown, duplicate or stale completions are contained.

### Validate command ranges

Check namespace, opcode, starting LBA, nonzero/allowed count, maximum transfer, metadata, alignment, DMA mappings and permissions. Split only at supported boundaries.

Never widen a write into adjacent LBAs without read-preserve or explicit authorization.

### Preserve request identity

Queue ID plus command ID/tag identifies outstanding work. Do not recycle until terminal completion/abort certainty.

Reset/timeouts require generations so late completions cannot attach to new requests.

### Understand queue depth

Multiple outstanding commands expose device/media parallelism and cover latency. At saturation, deeper queues generally add waiting and tails rather than useful throughput.

Report depth per queue and aggregate, plus workload concurrency.

### Use multiqueue paths

Per-core/hardware queues reduce lock contention and improve locality. Device controllers arbitrate across submission queues and completion processing.

Fairness/QoS prevent one stream from monopolizing media or tags.

### Understand read path

Reads may hit controller cache or trigger FTL lookup/media read/ECC decode, then DMA data and completion. Correctable retries add latency.

Return error/poison rather than silently fabricated data when correction fails.

### Understand write path

Writes DMA host data, buffer it, update media and metadata under ordering/persistence rules, then complete at the documented point.

The newest logical copy may temporarily reside in protected controller state, journal/log or new physical page.

### Distinguish visibility and durability

A completed write may be visible to subsequent reads but remain in volatile cache. Durability means surviving the specified failures at a documented boundary.

Power-loss protection scope may cover data, metadata, both or neither.

### Use flush correctly

Flush orders/drains prior relevant cached writes to the specified nonvolatile domain. Host must ensure earlier commands are ordered before the flush.

Flush completion does not certify application-level crash consistency if filesystem ordering is wrong.

### Use FUA correctly

FUA requests a particular write reach the required nonvolatile boundary before completion, when supported. It may interact with prior/other writes differently than a broad flush.

Drivers/filesystems map higher-level barriers to actual device capabilities.

### Handle write-cache settings

Cache enable/disable and volatile/protected status can change after reset, firmware update or path failover. Discover and monitor effective state.

Do not assume a model name implies power-loss protection.

### Define atomic write guarantees

Devices may guarantee atomicity only for aligned sizes/units and specific commands/settings. Larger writes can tear across power loss or error.

Filesystems/databases must use supported units plus checksummed/journaled recovery.

### Implement FTL lookup

An FTL maps each logical page to the current physical page and tracks reverse validity. Tables may be cached in controller DRAM and persisted through logs/checkpoints.

Mapping metadata needs crash recovery and integrity protection.

### Perform out-of-place updates

Program new data into a free physical page, validate it, atomically publish mapping/version, then mark old page stale. Keep at least one recoverable current copy through transition.

Power failure at any point must recover old or new consistent data, not neither/mixed metadata.

### Garbage-collect blocks

Select a victim erase block, copy its still-current valid pages elsewhere, persist mapping changes, then erase/reuse. Stale pages need not move.

Poor victims or low free space increase copied bytes and latency.

### Compute write amplification

`WAF=media_written_bytes/host_written_bytes` over the same interval. Include GC, metadata and other applicable internal writes if telemetry defines them.

State units/counter wrap/reset and avoid command-count ratios.

### Use overprovisioning

Spare capacity gives FTL room for out-of-place writes, GC, bad-block replacement and metadata. Define denominator: `(raw-user)/user` differs from spare fraction of raw.

User-created unallocated/discarded space can help only under workload/device behavior.

### Wear-level media

Dynamic wear leveling spreads new writes; static wear leveling may move cold data to free less-worn blocks. Movement itself adds writes.

Track erase distributions, retired blocks and remaining spare capacity rather than only average cycles.

### Use ECC and retries

Media stores redundant symbols and may retry reads with adjusted sensing. Correction strength and raw error rates evolve with wear/retention/temperature.

Telemetry should distinguish corrected events, retries and uncorrectable data with exact scope.

### Manage bad blocks

Manufacturing/runtime bad blocks are mapped out using spare resources. Growing defects reduce margin and may trigger warning/failure thresholds.

Never expose stale data when remapping or lose mapping metadata.

### Handle discard

Discard tells the device selected LBAs need not preserve data. The device may delay reclamation and subsequent reads can return defined, deterministic or indeterminate results by capability.

Discard is not secure erase and can leak timing/allocation information.

### Handle write zeroes

Write-zeroes may avoid transferring full zero payload and allocate/deallocate internally. Its readback/durability semantics follow the command capability.

Do not substitute discard when deterministic zeros are required.

### Sanitize securely

Sanitize/secure erase mechanisms have specific scope, crypto/media/block behavior and completion/status. Verify capability and threat model.

Filesystem deletion/discard alone does not prove irrecoverability.

### Understand zoned storage

Zones have states and write pointers; sequential-write-required zones accept writes at the current pointer. Reset reclaims a zone.

Host-managed placement reduces hidden FTL work but moves policy/recovery complexity upward.

### Handle zone append

Append lets device choose actual LBA at write pointer and reports it. Concurrent appenders must use returned locations, not assumed addresses.

Completion and recovery persist mapping between logical record and reported LBA.

### Schedule HDD requests

Reordering reduces seeks and merges adjacent work, subject to deadlines/fairness/barriers. Flash lacks mechanical seek but still benefits from parallelism/locality.

Scheduler policy must respect flush/FUA and tenant QoS.

### Schedule SSD requests

Controllers distribute work across channels/dies/planes and may prioritize reads over background writes. Write bursts can fill buffers and trigger GC.

Tail latency emerges from shared internal resources not visible in LBA interface.

### Handle thermal throttling

Sustained workloads heat controllers/media; firmware reduces speed to protect operation. Short benchmarks may measure only boost/cold state.

Record temperature, power state and duration.

### Handle power states

Low-power entry saves energy but adds wake latency and may affect volatile state. Host/device coordinate outstanding commands and latency tolerance.

Power loss differs from managed shutdown/sleep.

### Recover after power loss

Firmware scans/checks journals, checkpoints and metadata to reconstruct mappings. Recovery must reject torn/corrupt records and preserve newest durable versions.

Measure recovery time and verify data against acknowledged durability semantics.

### Handle reset and abort

Abort may not stop media work immediately; reset invalidates queues and can leave commands uncertain. Driver quiesces, records state and recreates queues/mappings.

Only idempotent commands with known partial state are safely retried automatically.

### Handle timeouts

Timeout means completion was not observed. Controller might be busy in recovery/GC or command may have committed.

Escalate abort/reset/path recovery while preserving uncertainty and command IDs.

### Handle multipath

Multiple paths can address the same namespace. Reservations, access state and failover prevent simultaneous unsafe writers and stale path assumptions.

Path failure does not necessarily mean media failure or command nonexecution.

### Interpret health telemetry

Temperature, media errors, percentage used, bytes written and spare thresholds use device-specific units and reset/saturation rules. Save raw and decoded forms.

Telemetry predicts risk imperfectly and does not replace end-to-end checks/backups.

### Protect data end to end

Transport CRC, media ECC and application checksums cover different paths/failure modes. Metadata/versioning detects misdirection and stale blocks.

Encryption protects confidentiality but not automatically freshness or recoverability.

### Compute IOPS and throughput

Payload throughput is IOPS times average payload bytes if operations transfer that payload. Small random requests can be IOPS-limited; large sequential work bandwidth-limited.

Report reads/writes/mix, block size, queue depth, alignment and units.

### Understand latency distributions

Report average and percentiles, with coordinated-omission-aware load generation. Queue wait, service, GC/retry and host completion all matter.

Steady-state tails often differ sharply from fresh-device results.

### Precondition benchmarks

Define secure erase/format/fill, sequential/random preconditioning, working-set size and duration until stable metrics. Preserve device wear and thermal context.

Comparing one fresh and one used device is invalid.

### Verify command behavior

Use guard LBAs, known patterns, checksums, power-fault injection under controlled conditions and reference queue scoreboards. Test every boundary/error/status.

Assert request/completion conservation and no out-of-range DMA/LBA access.

### Verify FTL recovery

Model logical-to-physical versions, inject failure between each data/metadata step and reboot/recover. Check each durable write and allowed nondurable outcome.

Stress low spare space, GC, bad blocks, ECC and metadata corruption.

### Gather layered evidence

Start with arithmetic/queue models, then emulation, OS block tests, device analyzers/telemetry, power-cut testing and application crash-consistency tests.

Bind command-set, model/firmware, capacity state, OS/driver/filesystem, workload, temperature and errata.

## Definitions and Notation

- `LBA`: host-visible logical block index.
- `L`: logical block bytes; range bytes are `count*L` after checked arithmetic.
- `Q`: queue depth under a stated queue scope.
- `IOPS`: completed operations/second under named endpoint.
- `throughput=IOPS*payload_bytes` when payload is uniform.
- `H`: host bytes written in an interval.
- `M`: media/internal bytes written under a telemetry definition.
- `WAF=M/H` for `H>0`.
- `R`: raw physical capacity; `U`: user-exposed capacity.
- `OP_user=(R-U)/U`; spare fraction of raw is `(R-U)/R`.
- `E`: rated/assumed average P/E cycles in an idealized calculation.
- `host_endurance_ideal=R*E/WAF`, excluding reserved/retention/failure/warranty effects.
- `durable(q,f)`: command `q` survives failure class `f` after the documented boundary.
- `residue=total-completed` at one explicitly named completion endpoint.

Decimal GB/TB and binary GiB/TiB must not be mixed silently. Vendor endurance and health metrics override simplified formulas for real products.

## Mechanisms, Invariants, or Proof Structure

1. **Range obligation:** namespace/LBA/count arithmetic identifies only authorized logical blocks.
2. **Command obligation:** opcode, format, alignment, metadata, flags and queue ID are valid before execution.
3. **Ownership obligation:** command/data/completion buffers have one authorized mutator/consumer at each state.
4. **Completion obligation:** each accepted ID receives exactly one terminal status with valid data/residue.
5. **Visibility obligation:** reads observe newest ordered logically visible bytes.
6. **Durability obligation:** flush/FUA/cache completion matches the documented failure boundary.
7. **Mapping obligation:** each valid LBA version maps to one validated current physical representation.
8. **Update obligation:** out-of-place data and metadata transitions retain old or new recoverable state.
9. **GC obligation:** only current valid pages move and stale pages never resurrect.
10. **Integrity obligation:** ECC/checksums/versioning prevent corrupt/misdirected data from becoming valid silently.
11. **Security obligation:** discard/reuse/sanitize/multipath cannot expose another tenant's stale data.
12. **Recovery obligation:** timeout/abort/reset/power loss reports allowed outcomes and blocks unsafe replay/free.
13. **Resource obligation:** queues/tags/cache/free blocks/spares remain within capacity with backpressure.
14. **Progress obligation:** foreground commands and required maintenance progress under stated fairness/resources.
15. **Evidence obligation:** capacity/performance/endurance claims bind units, workload, state, firmware and endpoint.

Refine command queues to an abstract logical block map plus completion/order/persistence states. Prove FTL update/recovery maintains at least one valid newest allowed version, then prove GC preserves the mapping. Resource/progress proofs include free-space and response reservations. Performance/endurance remain workload evidence after safety.

## Alternatives and Trade-Offs

1. **HDD versus SSD:** HDD offers mechanical sequential economics; SSD offers parallel low-latency reads with endurance/FTL costs.
2. **SATA/SAS versus NVMe-like queues:** legacy paths are mature; multiqueue protocols expose parallelism/lower overhead.
3. **Write-through versus volatile cache:** write-through simplifies durability; caching improves latency/combining.
4. **Flush versus per-write FUA:** flush batches prior writes; FUA targets individual durability semantics.
5. **Large versus small queue depth:** large exposes throughput; small lowers queueing/tail uncertainty.
6. **Large versus small I/O:** large amortizes command cost; small improves granularity/latency.
7. **Page versus block FTL mapping:** page mapping is flexible; block/coarser mapping saves metadata.
8. **More versus less overprovisioning:** more lowers GC/WAF/tails; less exposes more user capacity.
9. **Aggressive versus lazy GC:** aggressive builds reserve early; lazy preserves foreground resources until pressure.
10. **Dynamic versus static wear leveling:** dynamic minimizes movement; static balances cold-data wear.
11. **Host-managed versus device-managed placement:** host-managed zones expose policy; FTL hides media complexity.
12. **Discard versus no discard:** discard aids reclamation; leaks allocation timing and has semantic variation.
13. **Inline versus end-to-end integrity:** inline ECC is efficient; end-to-end checks detect misdirection/stale paths.
14. **Immediate versus batched completions:** immediate lowers latency; batching reduces CPU/interrupt overhead.
15. **Peak throughput versus endurance/tails:** aggressive writes maximize short-run speed; can raise heat/WAF/wear.

## Failure Modes and Misconceptions

1. “One LBA equals one NAND page.” Logical/media granularities differ.
2. “Physical sector size reveals all media geometry.” Controllers abstract internal organization.
3. “Command accepted means completed.” Queue acceptance only transfers ownership.
4. “Write completion always means durable.” Volatile caches may acknowledge earlier.
5. “Flush orders writes not submitted before it.” Host/driver ordering must establish scope.
6. “FUA and flush are identical.” One targets a command; the other may drain prior scope.
7. “Power-loss protection covers everything.” Data/metadata/cache scope must be verified.
8. “Atomic sector means any multi-sector write is atomic.” Alignment/size/command limits apply.
9. “SSD overwrites pages in place.” NAND commonly uses out-of-place updates.
10. “Old page may be invalidated before new mapping is safe.” That risks losing the only copy.
11. “GC copies every page.” Only current valid pages should move.
12. “WAF is device writes divided by host commands.” It is a byte ratio under defined counters.
13. “7% overprovision means 7% of raw.” Denominator changes the percentage.
14. “Discard guarantees zeros.” Read-after-discard behavior is capability-specific.
15. “Discard securely erases.” It only deallocates logically.
16. “ECC eliminates data loss.” Coverage, wear, metadata and firmware faults remain.
17. “SMART units are universal.” Definitions/scales depend on device/firmware.
18. “Peak interface rate equals storage bandwidth.” Media/controller/queue/packet limits intervene.
19. “More queue depth reduces latency.” It often adds waiting after saturation.
20. “Average latency describes storage.” GC/retry/thermal/reset produce important tails.
21. “A fresh empty SSD is representative.” Steady-state full behavior differs.
22. “Timeout means write did not happen.” Completion can be lost after partial/full commit.
23. “Reset makes retry safe.” Old work may have committed or complete late.
24. “RAID replaces backup.” Correlated/software/operator failures remain.
25. “Encryption proves integrity and erasure.” Threat model/key lifecycle/authentication matter.
26. “One sequential benchmark validates architecture.” Mix, depth, size, fullness and temperature change behavior.

## Worked Examples

### Example 1

A 4 KiB filesystem write to a 512-byte-LBA namespace spans eight LBAs but may update one 16 KiB NAND page plus metadata internally.

### Example 2

A volatile-cache write completes quickly; a following ordered flush completes only after prior relevant data/metadata reaches its promised nonvolatile boundary.

### Example 3

An FTL programs new page P9, verifies it, commits LBA-to-P9 mapping/version, then marks old P2 stale.

### Example 4

GC chooses a block with 20 valid and 236 stale pages, moves the 20 current versions, commits mappings and erases once.

### Example 5

100 GiB host and 160 GiB media writes produce WAF 1.60; command count would be irrelevant if sizes differ.

### Example 6

1,070 GB raw and 1,000 GB user capacity produce 7% user-relative overprovision but about 6.54% spare fraction of raw.

### Example 7

After discard, firmware may reclaim pages later; software cannot use readback contents as a security or zero guarantee without capability.

### Example 8

A zoned append reports the actual LBA selected at the write pointer; recovery uses that returned address.

### Example 9

A timed-out database log write has uncertain commit; retrying blindly could duplicate a record, so recovery consults durable sequence/checksum state.

### Example 10

This deterministic model audits capacity/spare ratios, WAF, payload throughput and an explicitly idealized endurance estimate.

<!-- bijux-verify: {"id":"storage-capacity-endurance-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"user_capacity_gb=1000 raw_capacity_gb=1070 overprovision_user_pct=7.00 spare_raw_pct=6.54\nhost_write_gib=100 media_write_gib=160 waf=1.60\nrandom_iops=500000 payload_kib=4 payload_gbps=2.048\npe_cycles=3000 idealized_host_endurance_tb=2006.25\n"}} -->
```python
user_capacity_gb = 1000
raw_capacity_gb = 1070
overprovision_user = (raw_capacity_gb - user_capacity_gb) / user_capacity_gb
spare_raw = (raw_capacity_gb - user_capacity_gb) / raw_capacity_gb

host_write_gib = 100
media_write_gib = 160
waf = media_write_gib / host_write_gib

random_iops = 500_000
payload_kib = 4
payload_gbps = random_iops * payload_kib * 1024 / 1e9

pe_cycles = 3000
idealized_host_endurance_tb = raw_capacity_gb * pe_cycles / waf / 1000

print(f"user_capacity_gb={user_capacity_gb} raw_capacity_gb={raw_capacity_gb} overprovision_user_pct={100 * overprovision_user:.2f} spare_raw_pct={100 * spare_raw:.2f}")
print(f"host_write_gib={host_write_gib} media_write_gib={media_write_gib} waf={waf:.2f}")
print(f"random_iops={random_iops} payload_kib={payload_kib} payload_gbps={payload_gbps:.3f}")
print(f"pe_cycles={pe_cycles} idealized_host_endurance_tb={idealized_host_endurance_tb:.2f}")
```

The capacities, workload, WAF and P/E cycles are invented. The endurance formula ignores reserved metadata, bad blocks, retention, workload variation, failure distributions, warranty conventions and firmware behavior and must not predict a real product.

## Cross-Program Connections

- **Operating Systems:** block multiqueue, I/O schedulers, DMA and filesystems map application intent to commands.
- **Data Structures:** queues, rings, maps, logs and free-block structures implement controllers/FTLs.
- **Databases:** WAL, flush ordering, torn-write detection and idempotence rely on durability semantics.
- **Distributed Systems:** device durability is one layer beneath replication and consensus persistence.
- **Security Engineering:** IOMMU, encryption, sanitize and stale-data reuse define storage isolation.
- **Reliability Engineering:** ECC, wear, bad blocks, telemetry and recovery manage media failure.
- **Performance Engineering:** queue depth, block size, WAF, preconditioning and tails determine observed service.
- **Formal Methods:** mapping refinement and crash invariants prove old-or-new recoverability.

## References

1. NVM Express, [NVMe Specifications](https://nvmexpress.org/specifications/), current base, command-set and transport specification access; retrieved 2026-09-04.
2. Linux kernel, [Block Documentation](https://docs.kernel.org/block/index.html), current block-layer, queue, integrity and zoned-device documentation index; retrieved 2026-09-04.
3. Linux kernel, [Multi-Queue Block IO Queueing Mechanism](https://docs.kernel.org/block/blk-mq.html), current software/hardware queue and tag architecture; retrieved 2026-09-04.
4. Linux kernel, [FIEMAP](https://docs.kernel.org/filesystems/fiemap.html), current logical-to-extent reporting and filesystem interface context; retrieved 2026-09-04.
5. QEMU, [NVMe Emulation](https://www.qemu.org/docs/master/system/devices/nvme.html), current NVMe controller/namespace feature emulation documentation; retrieved 2026-09-04.
6. linux-nvme, [nvme-cli Repository](https://github.com/linux-nvme/nvme-cli), current NVMe identification, management, telemetry and testing tooling; retrieved 2026-09-04.
7. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), storage hierarchy/performance teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Trace host submission through DMA, controller cache, FTL, NAND and completion for read, volatile write, FUA write and ordered flush.

### Exercise 2

Design a crash-consistent page-mapped FTL update and garbage-collection protocol with versioned metadata/checksums.

### Exercise 3

Compute WAF, user/raw spare ratios, bandwidth and qualified endurance estimates from counters with mixed block sizes and wraps.

### Exercise 4

Extend the executable model with queue depth, variable sizes, GC copied bytes, thermal throttling and latency percentiles.

### Exercise 5

Write a verification/evaluation plan for an NVMe-like SSD including power-loss, reset, discard/sanitize, telemetry and steady-state workloads.

## Answers to the Exercises

### Answer 1

For every command retain queue/ID, LBA range, DMA buffers, order and completion endpoint. A read maps LBA, retrieves/decodes media/cache data and DMA-completes. Volatile write may complete after protected controller ownership only if advertised; FUA waits for its required nonvolatile point. Flush follows ordered prior writes and drains their promised scope.

Separate accepted, visible, completed and durable times. Completion data/status is ordered before interrupt/poll observation and uncertain timeout/reset remains explicit.

### Answer 2

Program data with LBA/version/checksum into a free page, verify it, append/checkpoint an integrity-protected mapping update, atomically make the new version current, then mark old stale. Recovery selects the highest fully committed valid mapping and retains old data if new metadata/data tore.

GC copies only pages whose reverse map/version is still current, commits each new mapping before invalidating old, then records block state and erases. Reserve free pages/metadata log space so recovery/GC cannot deadlock.

### Answer 3

Convert every counter to bytes using its documented unit and account for wrap/reset. Sum host payload and media data/metadata writes over identical interval; divide for WAF. Report `(R-U)/U` and `(R-U)/R` separately. Throughput uses completed payload/time, not command count alone.

An ideal host-write estimate `R*E/WAF` must label decimal/binary units and exclusions. Real claims use vendor rated endurance/warranty plus observed workload WAF, wear distribution, spare/retired blocks, retention, temperature and firmware.

### Answer 4

Generate timestamped requests with size/mix and bounded queue. Service through a payload limit plus periodic GC that adds copied media bytes/delay; throttle bandwidth above a temperature threshold. Track host/media bytes, queue/service/total latency and completed IOPS/throughput.

Use a deterministic seed/trace, validate no-GC single-depth cases analytically and report mean/percentiles with stated convention. The model remains synthetic unless calibrated.

### Answer 5

Verify namespace/LBA bounds, queues/tags/DMA, completions, ordering, volatile-cache/FUA/flush, atomic units, FTL mapping/GC, ECC/integrity, discard/write-zeroes/zones, IOMMU/security, timeout/abort/reset/multipath and recovery using scoreboards, guard ranges, emulation, error and controlled power-cut injection.

Benchmark preconditioned steady-state read/write mixes across size, depth, locality, fullness, duration and temperature. Report payload/bus/media bytes, WAF, IOPS/bandwidth, latency tails, CPU, thermal/power, health/error/wear and recovery. Bind specification, model/firmware, OS/driver/filesystem/settings/workload and errata; internal evidence is not external durability, endurance or device certification.
