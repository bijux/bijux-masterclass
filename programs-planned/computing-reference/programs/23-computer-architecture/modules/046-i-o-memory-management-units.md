---
module_id: CA-046
program: Computer Architecture
level: 1
module_number: 46
title: I/O Memory Management Units
status: complete
last_verified: 2026-09-04
---

# I/O Memory Management Units

## One-Page Review

### Governing question

How can an I/O memory management unit translate and authorize device-originated memory requests at high rate while preserving requester/process/domain identity, permissions, invalidation order, page-table coherence, fault attribution, interrupt/DMA isolation and safe device assignment through reset and failure?

### Essential definitions

- An **I/O memory management unit** (`IOMMU`) translates and protects device memory transactions.
- An **I/O virtual address** (`IOVA`) is a device-visible address interpreted in an IOMMU translation domain.
- A **translation domain** binds page tables, address width, permissions and lifecycle to a set of requesters.
- A **requester ID** identifies the function/agent originating a transaction at the IOMMU boundary.
- A **stream ID** is an architecture/interconnect-specific requester identity used by a system MMU.
- A **process address space ID** (`PASID`) or substream ID selects a process/subdomain within a requester.
- An **IOTLB** caches IOVA-to-physical translations and permissions.
- A **device TLB** can cache translations in a device through address-translation services (`ATS`) or analogous mechanisms.
- A **context/device table** maps requester identity to a translation domain/root/configuration.
- An **IOMMU page walk** reads translation structures to resolve an IOVA miss.
- **translation invalidation** makes cached mappings/contexts unusable at the required IOMMU/device observers.
- **queued invalidation** submits invalidation commands and receives completion after required ordering.
- A **translation fault** reports an unmapped, permission-denied, malformed or otherwise invalid request.
- **interrupt remapping** validates/routes device interrupt messages using requester/context policy.
- **device assignment** gives a guest/userspace owner controlled access to a function plus DMA/interrupt resources.

### Central model, mechanism, or theorem

For every device request `q=(requester,PASID,IOVA,operation,length,attributes,ID)`, the IOMMU first selects an authorized context/domain, translates each covered page, checks read/write/execute/privilege and physical output bounds, then forwards only permitted byte ranges with requester/order attributes intact. Cached results are valid only for matching domain generations. Unmap/reassign follows revoke order: stop or fence new device work, update mappings, invalidate IOMMU and device translation caches, wait for completion and in-flight quiescence, then reuse/free pages or change ownership.

### Critical invariants

- Every transaction carries authentic requester and substream/process identity through context lookup.
- A requester can use only its assigned domain and cannot forge another domain through address or PASID aliasing.
- Translation covers every byte/page of a request; overflow or partially unmapped ranges fault without unauthorized access.
- IOTLB/device-TLB hits match domain generation, page size, IOVA tag, operation and permissions.
- Page-table walks validate entry type, alignment, reserved bits, permissions, output width and memory attributes.
- Mapping publication and invalidation are ordered so neither old nor partially initialized mappings authorize access.
- Invalidation completion covers every required IOMMU cache, walker and device translation cache before page reuse.
- Fault records identify requester/PASID/address/operation/cause without granting access or overflowing silently.
- Reset/hot-unplug/timeout cannot leave requester DMA active against reassigned memory.
- Finite command, walk, fault and completion queues retain progress under stated fairness and backpressure.

### Common failures

Common failures include indexing domains by bus/device/function while dropping segment, trusting device-supplied PASID without enable/bounds, mapping only the first page of a multi-page request, rounding mappings outward into adjacent memory, granting write for a read-only buffer, updating page tables without cache invalidation, acknowledging unmap before device ATS invalidation, freeing memory while DMA remains outstanding, reusing domain IDs without generation control, assuming CPU TLB flush affects IOTLBs, letting fault queues overflow without containment, reporting faults after losing requester identity, assigning multifunction devices whose peer traffic bypasses isolation, and resetting a function without fencing late requests.

### Compact example

An invented 4 KiB mapping gives domain A IOVA `0x10000000` read-only to physical `0x80000000` and IOVA `0x10001000` read/write to `0x90000000`; domain B maps the first IOVA to `0xa0000000`. A domain-A read at offset `0x123` becomes `0x80000123`; a write to that read-only page faults; an unmapped third page faults; domain-B read translates to `0xa0000123`. With two-cycle IOTLB lookup, 98% hits and three serial 80-cycle walk accesses per miss, an invented expectation is 6.80 cycles.

### Connections

IOMMUs connect virtual memory/TLBs, DMA, PCIe requester identity, device drivers, hypervisors, interrupt remapping, page pinning, shared virtual memory, ATS/PASID, confidential computing, fault handling, zero-copy and formal revocation/isolation proofs.

## Governing Question

CPU page tables protect CPU accesses, but devices initiate transactions independently. An IOMMU inserts a translation/protection boundary between device and memory, enabling remapping, scatter-gather, isolation and assignment.

The difficult operation is revocation. A mapping can be cached in IOMMU and device, while requests are in flight and page memory is about to be reused. Safe completion must cover all those states.

## Why This Matters

Without IOMMU isolation, a faulty or compromised device can read or overwrite arbitrary physical memory. With an incorrectly configured IOMMU, the same failure hides behind apparently valid APIs.

Translation adds walks, caches and invalidation traffic to high-rate DMA. PASID/shared virtual memory can improve programmability while multiplying identity and fault complexity.

Device assignment security depends on topology, reset, interrupt remapping and peer-to-peer routes, not only page-table permission bits.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace CPU TLB/page-table translation and invalidation;
- reason about DMA descriptors, mapping direction and ownership;
- identify PCIe functions/requester IDs and interrupts;
- apply page-range and permission arithmetic;
- explain virtualization domains and device reset/quiescence.

Retrieve IOMMU architecture/version/mode; requester/stream/segment identity and aliases; context/device/PASID table formats; domain IDs and generations; page sizes/levels/PTE format; IOVA/physical widths; read/write/execute/privilege/atomic attributes; IOTLB/walk-cache geometry; coherency of translation tables; invalidation commands/scopes/completion; ATS, PASID, page-request interface and device TLB; interrupt remapping; fault queue/records/stall/retry; bypass/identity domains; peer routing/ACS; reserved memory; nested translation; assignment/reset groups; firmware tables; kernel/hypervisor/device firmware revisions, mitigations and errata.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish CPU virtual, IOVA and physical addresses;
2. bind requester/PASID identity to domains and page-table roots;
3. walk and validate IOMMU translations across page sizes;
4. check entire request ranges and access permissions;
5. integrate IOTLB, walk caches and device ATS translations;
6. specify safe map, unmap, invalidation and page-reuse ordering;
7. handle translation faults, stalls/retries and queue overflow;
8. assess device assignment, interrupt remapping and peer isolation;
9. verify translation refinement, revocation and conditional progress;
10. evaluate translation overhead using counters and workloads.

## Core Exposition

### Distinguish address spaces

CPU virtual addresses belong to a process/CPU translation context. IOVAs belong to device domains; physical addresses name memory/interconnect resources.

Numerical equality does not make their authority or lifecycle equal.

### Identify the requester

The interconnect supplies a requester/stream ID derived from the originating function/port. Include segment/hierarchy bits required to avoid collisions.

Identity must be trustworthy at the IOMMU boundary and preserved through bridges.

### Select a domain

Context/device tables map requester to translation mode/root/domain ID and allowed PASIDs. A disabled/unknown entry faults or follows explicit secure default.

Never use permissive bypass as an error fallback.

### Select a process context

PASID/substream enables multiple address spaces from one device. Validate capability, enable state, width and binding before table lookup.

Device-provided PASID is an input to authorize, not proof of ownership.

### Decode the IOVA

Split page offset and page-table indices for the selected mode/page size. Check address width, canonicality and addition overflow across request length.

Multi-page requests need every covered page translated and authorized.

### Walk translation tables

Start at the domain/context root, compute each entry address and retrieve it through the defined coherent memory path. Validate nonleaf/leaf encodings and physical table alignment.

Fault malformed/reserved/output-overflow entries instead of masking them.

### Form large-page results

A higher-level leaf maps a larger aligned range and substitutes lower IOVA bits. Required low physical fields must satisfy alignment.

Cache page size in the IOTLB so matching and offsets remain exact.

### Check permissions

Read, write, execute/privilege, atomic and snoop/memory attributes can differ. A write never succeeds from a read-only mapping because the same address previously read.

Permissions are cached and therefore part of invalidation scope.

### Check the whole transfer

A DMA burst crossing a page can have different mappings/permissions. Split at boundaries or validate all pages before any non-idempotent effect.

For writes, partial success semantics must be explicit if later page faults.

### Use IOTLBs

IOTLB entries cache requester/domain/PASID, IOVA page, physical page, size, permissions/attributes and generation. Hits reduce page walks.

Shared structures require partition/QoS and side-channel analysis.

### Cache walk intermediates

Walk caches remember context/nonleaf entries. They can stay stale even when final IOTLB entries are absent.

Invalidation and domain reuse must cover them or version their results.

### Merge page walks

Compatible same-domain/page misses can share a walk and attach dependents. Different operations may need different permissions.

Never merge across requester/PASID/domain generation merely because IOVA matches.

### Publish a mapping

Allocate/pin physical pages, write complete page-table entries with required coherence/order, then expose descriptor/IOVA to the device. Invalidate stale negative/old translations if architecture requires.

The device cannot own the buffer before mapping is valid.

### Unmap safely

Stop new descriptors/requests, establish device queue fence/quiescence as required, remove/restrict PTEs, issue correct invalidations, wait completion, drain in-flight accesses, then unpin/reuse.

Reversing the final steps creates DMA use-after-free.

### Invalidate by scope

Commands may target address, PASID, domain, requester/context or global caches. Select enough scope for page-size and cached-intermediate behavior.

Do not assume invalidating one IOVA leaf evicts every combined/nested/device translation automatically.

### Wait for completion

Queued invalidation completion means prior requested cache effects/order are globally effective at documented observers. Submission alone is not completion.

Retain command IDs and handle error/timeout without freeing memory early.

### Coordinate ATS

ATS lets devices request/cache translations. It can reduce repeated translation latency but moves stale state into device TLBs.

Unmap/reassign must invalidate device caches and await protocol completion where required.

### Handle page requests

Devices may request that missing pages be made resident/mapped, enabling shared virtual memory. Requests carry identity and can stall transactions.

OS resolves, denies or faults them with bounded resources and tenant policy.

### Support shared virtual memory

Device PASID can refer to a process address space, reducing explicit buffer remapping. Process lifetime, migration, faults and invalidation now synchronize CPU and device.

Device access still obeys IOMMU permissions and page residency.

### Support nested translation

Virtualization can translate guest IOVA through guest and host stages. Combined caches carry both context generations and permissions.

Guest/hypervisor invalidations target relevant staged/combined entries.

### Remap interrupts

MSI writes include destination/vector data; interrupt remapping verifies requester and selects permitted host/guest target. DMA mapping alone does not protect interrupts.

Configure remapping/handlers before enabling device messages.

### Consider peer-to-peer paths

Peer transactions may route between endpoints without reaching the same remapping point. Topology and access-control capabilities determine mediation.

Assignment groups must reflect routes/reset/resource sharing, not just functions individually.

### Form isolation groups

Devices inseparable by requester alias, bridge routing, peer paths or reset may belong to one assignment group. Assign the whole group to one trust domain.

Software grouping is a platform claim requiring topology/firmware validation.

### Configure bypass cautiously

Identity/bypass domains reduce translation cost for trusted agents but expose physical memory. Limit ranges/permissions and avoid global fallback.

Firmware-reserved devices need explicit ownership transfer before OS reconfiguration.

### Protect reserved memory

Exclude firmware, IOMMU tables, interrupt tables, hypervisor and other tenants from device mappings. Protect translation tables from device write access.

Memory encryption/private pages may require shared/bounce regions and attribute transitions.

### Pin and account pages

DMA mappings retain physical pages against reuse/migration unless supported shared-fault mechanisms coordinate it. Account pinned memory to the owner.

Long-lived unbounded pins can exhaust memory and break reclaim.

### Handle coherence

Translation-table reads and updates need the architecture's coherent/cache maintenance path. Translated DMA data can be coherent or noncoherent separately.

IOMMU translation does not make device data coherent automatically.

### Preserve memory attributes

Output transactions carry shareability, cacheability/snoop, privilege and other attributes derived from context/PTE/request policy.

Wrong attributes can create stale data or bypass isolation even with correct addresses.

### Record faults

Fault entries should capture requester/stream, PASID, IOVA, operation, cause, stage and transaction context sufficient for diagnosis/recovery.

Sanitize exposure to guests while retaining host evidence.

### Handle fault queue overflow

A bounded fault queue can fill under malicious traffic. Backpressure, rate limit, mask/stall/disable requester and surface overflow explicitly.

Never silently drop faults while continuing unauthorized accesses.

### Stall or abort faults

Some models abort immediately; others stall and allow software repair/retry. Stall consumes device/IOMMU resources and needs timeout/cancel.

Retry must bind the same request generation and recheck permissions.

### Isolate faulting devices

Repeated faults may disable a PASID/function/domain, stop queues or reset the device. Containment scope follows trust and shared-resource topology.

Capture evidence before reset and reconcile in-flight DMA.

### Handle reset

Reset function/device/IOMMU in coordinated order. Block new requests, invalidate contexts/caches, drain/quarantine late traffic and restore only trusted mappings.

Requester IDs reused after hotplug need generations/quiescence.

### Handle hotplug

Removal stops new config/DMA but outstanding transactions can remain. OS tears down assignment only after platform containment and invalidation.

Insertion starts from deny-by-default context until configured.

### Assign devices to guests

Validate isolation group/reset, bind to guest domain, map guest memory least privilege, configure interrupt remapping and expose controlled configuration.

On detach/migration, quiesce, invalidate device/IOMMU translations and interrupts before memory/resource reuse.

### Protect confidential guests

Private/encrypted pages may reject device access; guest shares explicit bounce/mapped pages with integrity/confidentiality trade-offs.

IOMMU tables and assignment metadata belong to the trusted hypervisor/platform boundary.

### Bound walk resources

Walkers consume slots, PTE memory requests, response buffers and invalidation coordination. Reserve progress for invalidations/faults.

Untrusted miss storms must not starve CPUs, other devices or revocation.

### Prioritize invalidation

Revocation commands may need priority over new translations so an active device cannot indefinitely delay unmap. Avoid cycles where completion waits on queues filled by the revoked requester.

Use separate resources/credits or proven arbitration.

### Measure translation overhead

Count IOTLB/device-TLB hits/misses, walks, PTE cache levels, ATS/page requests, invalidations, stalls/faults and queue latency by requester/PASID/page size.

Connect them to DMA throughput/tails and memory traffic.

### Use large I/O pages

Large pages expand IOTLB reach and reduce walks but require alignment/contiguity and enlarge permission/revocation granularity.

Measure fragmentation and mapping lifetime alongside performance.

### Verify translation

Compare every forwarded/faulted request to a reference domain/page-table model. Guard physical memory and inject boundary/permission faults.

Assert full-range authorization, exact output bytes/attributes and no stale-generation hit.

### Verify invalidation

Race mapping changes with IOTLB/walk/ATS hits and in-flight DMA. Page reuse starts only after all defined completion/quiescence predicates.

Use formal epochs/scoreboards and OS/device stress.

### Gather layered evidence

Start with executable translation examples, then reference walkers/formal tests, kernel/hypervisor assignment, ATS/fault injection and hardware counters/analyzers.

Bind IOMMU architecture, firmware tables, interconnect, device firmware, kernel/hypervisor and errata.

## Definitions and Notation

- `RID`: requester/stream identity at IOMMU boundary.
- `PASID`: process/substream address-space selector when enabled.
- `D`: domain containing translation root, ID/generation and policy.
- `IOVA`: device-visible input address.
- `PA`: translated physical output address.
- `p`: base-page offset bits; page bytes are `2^p`.
- `map_D(vpn)=(ppn,permissions,attributes,generation)`.
- `q=(RID,PASID,IOVA,operation,length,attributes,ID)`.
- `pages(q)`: every input page touched by `[IOVA,IOVA+length)` after checked arithmetic.
- `authorized(q)`: every page maps and permits operation/attributes.
- `IOTLB_hit`: full domain/context/page/permission/generation match.
- `invalidation_complete(s)`: every cache/device/walker in scope `s` rejects prior state.
- `quiescent(RID)`: no old device transaction can reach memory under revoked mapping.
- `translation_expectation=A+(1-H)*P` for stated serial lookup/miss model.

Requester, stream, domain and PASID encodings are architecture-specific. The abstract terms require mapping to exact specification tables and platform topology.

## Mechanisms, Invariants, or Proof Structure

1. **Identity obligation:** authentic requester/segment/PASID selects exactly one authorized context/domain.
2. **Range obligation:** checked arithmetic covers every request byte/page without wrap.
3. **Walk obligation:** indices, PTE addresses, types, alignment and output width are exact.
4. **Permission obligation:** every page permits operation, privilege and attributes before forwarding.
5. **Cache obligation:** IOTLB/walk/device entries match domain generation and page-size identity.
6. **Publication obligation:** complete tables/mappings become visible before device IOVA ownership.
7. **Revocation obligation:** PTE restriction precedes complete invalidation/quiescence and memory reuse.
8. **ATS obligation:** device translations participate in invalidation/completion.
9. **Ordering obligation:** translation/data/atomic/coherence attributes refine platform rules.
10. **Fault obligation:** unauthorized/malformed requests do not access memory and produce attributable bounded records.
11. **Interrupt obligation:** device messages are remapped to permitted targets.
12. **Lifecycle obligation:** reset/hotplug/assignment/domain-ID reuse cannot authorize stale traffic.
13. **Resource obligation:** walk/fault/command/completion queues remain bounded with containment.
14. **Progress obligation:** invalidation, faults and permitted DMA progress under stated fairness.
15. **Evidence obligation:** isolation/performance claims bind architecture, topology, revisions and workloads.

Refine each forwarded transaction to the reference domain mapping and each fault to denied access with no physical effect. Prove cached equivalence using generation/invalidation invariants, then prove page reuse only after invalidation completion plus requester quiescence. Assignment composes DMA and interrupt isolation with topology/reset assumptions.

## Alternatives and Trade-Offs

1. **Bypass versus translation:** bypass minimizes latency; translation provides remapping/isolation.
2. **Shared versus per-device domains:** sharing eases buffers/peer access; per-device domains narrow authority.
3. **Small versus large pages:** small pages give granularity; large pages improve reach/walk traffic.
4. **Eager versus lazy mappings:** eager avoids runtime faults; lazy/on-demand reduces pinning but adds stalls.
5. **Explicit DMA maps versus shared virtual memory:** explicit maps make lifetime clear; SVM improves programmability.
6. **IOMMU-only versus device ATS caching:** central caches simplify revocation; ATS reduces translation round trips.
7. **Abort versus stall faults:** abort bounds resources; stall permits demand paging/recovery.
8. **Address versus domain invalidation:** address scope reduces disruption; domain scope is simpler/safer for broad change.
9. **Synchronous versus queued invalidation:** synchronous is direct; queued batches work and needs completion tracking.
10. **Identity versus translated trusted devices:** identity keeps physical addressing; translated limits ranges/remaps.
11. **Direct assignment versus mediated devices:** direct gives performance; mediation centralizes validation/migration.
12. **Per-function versus group assignment:** per-function is flexible; groups reflect inseparable topology/reset.
13. **Coherent versus noncoherent table/data paths:** coherence simplifies visibility; noncoherence needs explicit maintenance.
14. **Deep versus shallow walk/fault queues:** deep absorbs bursts; shallow bounds denial-of-service state.
15. **Maximum throughput versus revocation priority:** throughput favors new requests; security/lifecycle requires prompt invalidation.

## Failure Modes and Misconceptions

1. “IOMMU translates CPU virtual pointers automatically.” DMA APIs create IOVA mappings; SVM is explicit.
2. “IOVA equals physical address if numbers match.” Domain semantics/permissions still differ.
3. “Requester ID is globally just BDF.” Segment/interconnect aliases and topology matter.
4. “PASID from device is trusted.” It must be enabled, bounded and bound to requester/domain.
5. “One translated start address authorizes the whole burst.” Every covered page/byte needs permission.
6. “Round mappings outward for convenience.” That grants adjacent memory.
7. “Read permission implies write.” Permissions are operation-specific.
8. “IOTLB tags need only IOVA.” Domain/PASID/page size/generation/permission matter.
9. “Changing the PTE revokes cached access.” Invalidation and completion are required.
10. “Submitting invalidation means complete.” Wait for the documented completion.
11. “IOMMU invalidation always flushes device ATS.” Device translations require included protocol scope.
12. “CPU TLB shootdown revokes DMA.” CPU and I/O translation caches differ.
13. “Unmap may free pages immediately.” Old DMA/in-flight translations must quiesce.
14. “Domain ID reuse is harmless after root change.” Stale caches need generation/invalidation.
15. “Translation implies cache coherence.” Data coherency is a separate attribute/protocol.
16. “An IOMMU fault can be dropped safely.” It must contain access and report/record overflow.
17. “Stalled faults consume no resources.” Request/device/walker state remains occupied.
18. “Retry uses current permissions automatically.” It must bind/revalidate exact transaction context.
19. “Interrupt remapping is part of DMA translation automatically.” It is a related distinct protection.
20. “Peer-to-peer always crosses the root IOMMU.” Routing/ACS/topology can differ.
21. “Every function can be assigned independently.” Shared requester/reset/peer paths form groups.
22. “Function reset stops all late DMA instantly.” Quiescence/containment is still required.
23. “Bypass is safe for firmware devices forever.” Ownership/lifecycle changes require reconfiguration.
24. “Huge I/O pages only improve performance.” They expand authority/revocation/contiguity granularity.
25. “High IOTLB hit rate proves low overhead.” Walk tails, invalidations and data path may dominate.
26. “Successful VM assignment proves isolation.” Malicious DMA/MSI/peer/reset/fault cases require proof/tests.

## Worked Examples

### Example 1

Domain A and B map identical IOVA to different physical pages; requester context selects the correct result rather than a global IOVA cache hit.

### Example 2

A 6 KiB DMA write begins 2 KiB before a page end, so it touches three pages; all three need writable mappings.

### Example 3

An IOTLB entry for read-only mapping hits on read but faults write without performing a new walk.

### Example 4

Software writes a mapping, orders page-table visibility and publishes descriptor/IOVA only afterward.

### Example 5

Unmap stops queue, clears PTE, invalidates IOMMU plus ATS device TLB, waits completion/drains DMA, then frees page.

### Example 6

A late ATS translation response bears an old domain epoch and is discarded after revocation.

### Example 7

Fault queue reaches threshold under hostile PASID misses; IOMMU stalls/disables requester and records overflow rather than forwarding.

### Example 8

A guest-assigned VF receives only its IOVA domain and remapped MSI vectors; sibling function shares reset group and remains co-assigned.

### Example 9

An SVM device page request causes OS to fault/map a page, invalidate/update translations and resume the exact stalled generation.

### Example 10

This deterministic domain translator audits context-separated mappings, permissions, faults and elementary IOTLB expectation.

<!-- bijux-verify: {"id":"iommu-domain-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"domain=A iova=0x10000123 operation=read result=0x80000123\ndomain=A iova=0x10000123 operation=write result=fault_permission\ndomain=A iova=0x10002123 operation=read result=fault_unmapped\ndomain=B iova=0x10000123 operation=read result=0xa0000123\niotlb_hit_pct=98.00 walk_accesses=3 expected_cycles=6.80\n"}} -->
```python
page_bytes = 4096
domains = {
    "A": {
        0x10000000: (0x80000000, "r"),
        0x10001000: (0x90000000, "rw"),
    },
    "B": {
        0x10000000: (0xa0000000, "rw"),
    },
}

def translate(domain, iova, operation):
    page = iova - iova % page_bytes
    offset = iova % page_bytes
    entry = domains[domain].get(page)
    if entry is None:
        return "fault_unmapped"
    physical_page, permissions = entry
    if operation == "write" and "w" not in permissions:
        return "fault_permission"
    return f"0x{physical_page + offset:08x}"

for domain, iova, operation in [
    ("A", 0x10000123, "read"),
    ("A", 0x10000123, "write"),
    ("A", 0x10002123, "read"),
    ("B", 0x10000123, "read"),
]:
    print(f"domain={domain} iova=0x{iova:08x} operation={operation} result={translate(domain, iova, operation)}")

iotlb_hit = 0.98
iotlb_lookup = 2
walk_accesses = 3
pte_access_cycles = 80
expected_cycles = iotlb_lookup + (1 - iotlb_hit) * walk_accesses * pte_access_cycles
print(f"iotlb_hit_pct={100 * iotlb_hit:.2f} walk_accesses={walk_accesses} expected_cycles={expected_cycles:.2f}")
```

The mappings and timing are invented. The model translates one-page accesses without page-table encoding, caches, concurrency, ATS, nested translation or queueing; the timing is a serial expectation, not implementation evidence.

## Cross-Program Connections

- **Operating Systems:** DMA mapping, page pinning, VFIO/IOMMUFD and fault handling manage domains.
- **Virtualization:** nested translation, assignment and interrupt remapping isolate guests.
- **Security Engineering:** requester authenticity, least privilege and revocation contain devices.
- **Concurrent Systems:** map/unmap, invalidation and in-flight DMA require happens-before/progress.
- **Memory Architecture:** page walks, TLBs, coherence and huge pages recur in I/O form.
- **PCIe:** requester IDs, ATS/PASID, peer routes and MSI carry device transactions.
- **Performance Engineering:** hit/walk/invalidation/fault counters explain translation overhead.
- **Formal Methods:** domain refinement, generations and quiescence prove isolation/revocation.

## References

1. RISC-V International, [RISC-V IOMMU Repository](https://github.com/riscv-non-isa/riscv-iommu), current IOMMU architecture specification sources and releases; retrieved 2026-09-04.
2. Linux kernel, [VFIO Device Assignment](https://docs.kernel.org/driver-api/vfio.html), current IOMMU groups, device assignment and userspace API context; retrieved 2026-09-04.
3. Linux kernel, [Dynamic DMA Mapping Guide](https://docs.kernel.org/core-api/dma-api-howto.html), current DMA addresses, mappings, directions and synchronization guidance; retrieved 2026-09-04.
4. Intel, [Virtualization Technology for Directed I/O Architecture Specification](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-virtualization-technology-for-directed-io-architecture-specification.html), current VT-d translation, remapping and invalidation architecture; retrieved 2026-09-04.
5. Arm, [System Memory Management Unit Architecture Specification](https://developer.arm.com/documentation/ihi0070/latest), current SMMUv3 stream/substream translation, fault and invalidation architecture; retrieved 2026-09-04.

## Exercises

### Exercise 1

Trace context lookup and a multi-page read/write through requester/PASID, IOTLB and page-table state, including one permission fault.

### Exercise 2

Design map/unmap/reuse ordering for a device with ATS and outstanding DMA, including invalidation timeout.

### Exercise 3

Specify a bounded fault queue and stall/retry protocol robust to hostile requesters and domain teardown.

### Exercise 4

Extend the executable model with page sizes, multi-page ranges, IOTLB generations and queued invalidation.

### Exercise 5

Write a verification/evaluation plan for securely assigning a PASID/ATS-capable PCIe device to guests.

## Answers to the Exercises

### Answer 1

Authenticate requester including segment/stream aliases, validate PASID binding and select root/domain generation. Split checked `[IOVA,IOVA+length)` by page, query generation-tagged IOTLB, walk misses and validate every PTE/permission/output. Forward only authorized subranges under specified partial semantics.

Record translated PA/attributes or fault with requester/PASID/IOVA/operation. A read-only cached entry still faults write; identical IOVA in another domain resolves independently.

### Answer 2

Stop new submissions, fence/quiesce device queue as required, remove PTE authorization, publish update, enqueue address/domain invalidation covering IOMMU/walk caches and ATS device TLB, await completion and drain old in-flight transactions. Only then unpin/free/reassign memory and recycle domain IDs.

On timeout, quarantine/reset requester and retain pages/mappings as uncertain until platform proves containment. Old-epoch responses cannot refill.

### Answer 3

Each record retains requester/PASID/domain generation, IOVA, operation, cause, stage and transaction ID. Reserve entries/credits before stalling; apply per-requester quotas/rate limits and expose overflow. Software may resolve then issue generation-matched resume, or abort/disable.

Domain teardown cancels/stops stalled requests before root reuse. Assert no faulting request reaches memory, no silent record loss, bounded occupancy and progress for other domains under fairness.

### Answer 4

Represent mappings by `(domain,generation,page_size,IOVA_base)->(PA_base,permissions)`. Split the entire request, choose most-specific/legal nonambiguous entry, validate alignment and all pages. IOTLB entries carry generation; queued invalidation marks old generation unusable and completion waits until every matching entry/walk is gone.

Add in-flight counts so page reuse requires invalidation completion plus zero old transactions. Test overflow, boundaries, mixed permissions and domain-ID reuse.

### Answer 5

Verify topology/requester aliases/groups/reset, PASID binding, device/context tables, page walks/large pages, full-range permissions, IOTLB/walk/ATS caching, map/unmap generations, queued completion, IOTLB/device invalidation, IOVA/physical guards, MSI remapping, peer routing, faults/overflow/retry, reset/hotplug and migration with formal scoreboards, hostile DMA and fault injection.

Measure hit/walk/ATS/page-request/invalidation/fault traffic, latency tails, DMA throughput/CPU/memory interference and tenant fairness across page sizes/working sets. Bind IOMMU architecture, firmware topology, interconnect/device firmware, hypervisor/kernel and errata; internal evidence is not external isolation, architecture or silicon certification.
