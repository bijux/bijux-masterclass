---
module_id: CA-048
program: Computer Architecture
level: 1
module_number: 48
title: Firmware and Boot Interfaces
status: complete
last_verified: 2026-09-04
---

# Firmware and Boot Interfaces

## One-Page Review

### Governing question

How can reset firmware discover and initialize a changing platform, select and authenticate the intended software, describe hardware without ambiguity, and transfer memory, privilege, services, evidence, and recovery authority to the next stage exactly once?

### Essential definitions

- **reset vector** is the architecturally defined first instruction address or entry mechanism after reset.
- **boot stage** is one component in a sequence that establishes enough state to authenticate, load, and invoke its successor.
- **firmware interface** is a versioned contract of calls, tables, registers, data structures, and lifecycle rules between platform software layers.
- **platform initialization** configures clocks, memory, interconnects, security, and devices needed for later stages.
- **boot services** are firmware facilities available before an explicit handoff boundary.
- **runtime services** are the narrowly retained firmware facilities callable after operating-system ownership begins.
- **machine description** records discoverable hardware topology, addresses, interrupts, clocks, and reserved resources.
- **UEFI** defines an OS-loader/platform-firmware environment with protocols, tables, boot services, and runtime services.
- **ACPI** defines tables and methods used to enumerate/configure hardware and coordinate power and platform behavior.
- **Devicetree** describes a hardware instance as a hierarchical data structure passed to later software.
- **SBI** is a RISC-V supervisor-to-higher-privilege firmware interface.
- **verified boot** permits execution only after policy-authorized cryptographic verification.
- **measured boot** records measurements for later attestation without itself deciding whether to execute.
- **rollback protection** rejects authenticated but policy-obsolete software.

### Central model, mechanism, or theorem

Model a handoff from stage `S_i` to `S_(i+1)` as a typed record `H_i=(entry, ABI, memory map, machine description, services, security state, evidence, version)`. Before branching, `S_i` authenticates or authorizes the successor, validates every bounded pointer/range and overlap, completes required cache/device writes, freezes mutable handoff data, and publishes `H_i`. After the branch, only the contract-designated owner may mutate each resource. Boot-service exit, privilege lowering, page-table activation, and ownership transfer are state transitions, not ordinary calls that can be retried casually.

### Critical invariants

- The reset path begins in a documented privilege, endianness, execution, cache, and interrupt state.
- Each stage verifies the exact bytes and metadata it will execute before granting authority.
- Every image, table, stack, log, and reserved range fits in owned memory without arithmetic overflow or overlap.
- Machine-description identities, address cells, interrupt parents, clocks, and reserved regions are internally consistent.
- The final memory map is captured at the protocol-defined handoff point and remains valid through transition.
- Calls use the exact ABI, calling convention, register preservation, alignment, and concurrency rules.
- Boot-only services are never called after their termination boundary.
- Runtime mappings preserve required physical/virtual identity and memory attributes.
- Measured-boot logs correspond to extended measurements, and rollback state changes atomically.
- Failure selects a bounded recovery path without executing unauthenticated fallback or exposing old secrets.

### Common failures

Common failures include assuming reset state, training memory with the wrong board parameters, trusting table checksums as authenticity, parsing attacker-controlled lengths without checked arithmetic, treating compatible strings as complete device identity, losing reserved-memory exclusions, modifying the UEFI map between its final retrieval and `ExitBootServices`, retaining stale firmware pointers, calling runtime services with wrong mappings, conflating measured and verified boot, authenticating an old vulnerable image without rollback policy, extending a measurement over different bytes than execution, accepting unsigned recovery media, and resetting before durable failure evidence is committed.

### Compact example

An invented loader owns physical `[0x80000000,0x80020000)`, proposes a 96 KiB kernel at `0x80200000`, a 32 KiB Devicetree at `0x80218000`, and a reserved region `[0x8021f000,0x80223000)`. Half-open range arithmetic shows the kernel ends at `0x80218000` and does not overlap the Devicetree, but the Devicetree ends at `0x80220000` and overlaps the reserved region by 4 KiB; the handoff must be rejected or relocated.

### Connections

Firmware and boot interfaces connect reset/clock/power controllers, memory systems, privilege modes, ABIs, executable formats, device discovery, interrupt and IOMMU configuration, operating-system loaders, cryptographic roots of trust, attestation, updates, recovery, virtualization, and postmortem observability.

## Governing Question

Boot is a cross-layer protocol executed while the platform is least observable and most mutable. Each stage inherits partial state, establishes new invariants, and hands authority onward.

The central difficulty is not merely loading bytes. It is proving which bytes, addresses, descriptions, services, mappings, and security state the successor may rely on—and when the predecessor stops owning them.

## Why This Matters

A processor with no valid boot contract cannot reach a general operating system reliably. A boot interface that works on one revision can corrupt memory or hang on another when topology or reserved regions change.

Firmware executes with broad privilege before normal isolation and logging exist. A parser, update, rollback, or recovery mistake therefore becomes a platform-wide security boundary failure.

Stable interfaces let firmware and operating systems evolve independently. Their versioning and lifecycle rules are as architecturally significant as instruction encodings.

## Prerequisites and Retrieval

Before studying this module, be able to:

- trace reset, exception level, address translation, caches, and interrupts;
- use half-open address ranges and checked integer arithmetic;
- distinguish physical, virtual, bus, and device-visible addresses;
- explain hashes, signatures, keys, counters, and authenticated metadata;
- read an ABI, executable header, and structured hardware description.

Retrieve processor reset state and boot-hart selection; ROM and immutable-root contents; stage graph and entry ABIs; DRAM-controller/training parameters; cache/coherency state; image formats and load constraints; UEFI/PI revision and protocols; ACPI revision/tables; Devicetree version/bindings/overlays; SBI version/extensions; memory-map descriptor format/key; reserved/secure/runtime regions; interrupt-controller and timer discovery; console; entropy source; root keys/revocations; verification and measurement algorithms; anti-rollback storage; update atomicity; recovery policy; crash/reset logs; virtualization ownership; firmware, board, OS, and errata revisions.

## Learning Objectives

After completing this module, you should be able to:

1. reconstruct the reset-to-operating-system stage graph and trust boundaries;
2. specify entry state and ABI requirements for each handoff;
3. validate image ranges, entry points, memory maps, and machine descriptions;
4. distinguish UEFI boot/runtime services, ACPI tables, Devicetree, and SBI roles;
5. perform a race-safe boot-service exit and ownership transfer;
6. design verified, measured, rollback-protected, and recoverable boot flows;
7. preserve cache, MMU, interrupt, and multicore consistency at handoff;
8. contain parser, service, update, and recovery failures;
9. verify interface conformance with reference models and fault injection;
10. collect reproducible evidence across firmware and OS revisions.

## Core Exposition

### Start from architectural reset state

Document the initial instruction address, privilege mode, active hart/core, endianness, interrupt masks, address translation, cache/coherency, vector state, and implementation-defined registers. Code must establish any unstated property before relying on it.

Reset state is not a normal process environment: RAM, stack, global data, clocks, and secondary cores may be unavailable.

### Build a stage graph

Name immutable ROM, first mutable stage, platform initialization, payload selector, OS loader, hypervisor, kernel, and recovery stages. Record who authenticates whom and which storage/memory each may change.

A graph exposes alternate recovery and update paths that a simple linear diagram hides.

### Establish temporary execution resources

Early code may use registers, on-chip SRAM, cache-as-RAM, or a small trusted memory. Bounds and replacement/coherency behavior must be explicit.

Do not place stack or authentication workspace in DRAM before training establishes it.

### Initialize clocks and memory

Select safe clocks, release controller resets, configure memory PHY/controller, train channels, discover usable capacity, and test enough memory for the next stage.

Board topology, timing parameters, voltage, temperature, repair/ECC state, and firmware version are part of the evidence.

### Bring up interconnect coherence

Configure coherent agents and shareability before multiple processors or DMA observe common state. Clean/invalidate caches as the architecture requires when ownership or cacheability changes.

A successful single-core load does not prove coherent multicore handoff.

### Load an image defensively

Parse headers with bounded offsets, checked addition/multiplication, alignment, file-size versus memory-size constraints, and segment-overlap policy. Reject entry points outside executable authorized regions.

Copy/decompress into owned memory, then perform required data-cache clean and instruction-cache invalidation before execution.

### Authenticate bytes and metadata

Verify signatures from an authorized key chain over the canonical image and security-relevant metadata: version, target, load policy, dependencies, and configuration.

Validate algorithm/key policy and revocation, not merely mathematical signature correctness.

### Enforce rollback policy

Compare signed version/security counter against monotonic trusted state. Update the counter only under an atomic policy that preserves at least one bootable authorized image across power failure.

Recovery must not become an unrestricted path to an older vulnerable version.

### Measure the executed configuration

Hash the exact authorized bytes and material configuration into a protected measurement chain and append corresponding event-log records. Define ordering and event encoding.

Measurement supports later claims; it does not automatically block execution.

### Validate the machine description

Treat UEFI tables, ACPI, Devicetree, and vendor data as structured inputs. Check signatures/magic, versions, total lengths, offsets, alignment, checksums where specified, duplicate identities, recursion/depth, references, and address ranges.

A valid checksum detects some corruption but is not cryptographic authenticity.

### Interpret Devicetree precisely

Walk nodes and properties using parent-defined address/size cells. Translate `reg` through bus `ranges`; resolve phandles, interrupt parents, clocks, resets, IOMMUs, and reserved memory according to bindings.

The `compatible` list selects a driver/binding; it does not replace validation of required properties.

### Interpret ACPI precisely

Locate the root pointer and table set, validate signatures/lengths/checksums/revisions, then use standardized tables and namespace methods according to their contracts.

Firmware-described addresses and resources still require overlap, ownership, and policy validation.

### Use UEFI protocols by lifecycle

UEFI exposes handles and protocols for discovery plus boot services for allocation, events, images, and I/O. Callers must honor task-priority, event, buffer, and ownership rules.

Protocol presence and revision are capabilities to inspect, not permission to assume every optional behavior.

### Separate boot and runtime services

Boot services exist until successful `ExitBootServices`. Runtime services are the smaller post-handoff set and require prescribed memory mappings and serialization/environment rules.

Never retain boot-service pointers or protocol objects as if they remain valid afterward.

### Capture the final UEFI memory map

Obtain the map plus map key with sufficient buffer, cease operations that can change it, and invoke `ExitBootServices` with the matching key. If the call reports a changed map, reacquire and retry the whole bounded sequence.

The last map defines firmware, conventional, reserved, ACPI, MMIO, and runtime ownership for the handoff.

### Build page tables from ownership

Map loader, kernel, stack, machine description, runtime regions, MMIO, and reserved holes with correct cacheability and permissions. Avoid identity assumptions unless the interface requires them.

Activate translation only with an entry address, stack, and exception path valid in the new address space.

### Define the entry ABI

Specify entry PC, register arguments, stack alignment, preserved registers, exception level, MMU/cache state, interrupt state, machine-description pointer, hart ID, and calling convention.

Clear or initialize unspecified registers if information leakage or nondeterminism matters.

### Transfer privilege deliberately

Configure delegation, protection regions, page tables, vectors, timers, interrupt controllers, and higher-privilege firmware before lowering privilege. Retain only the minimum service authority needed later.

The successor must not be able to rewrite immutable verification or rollback state.

### Use SBI as a versioned service boundary

RISC-V supervisor software discovers SBI base/version and individual extensions before calls. It handles standardized error returns and extension-specific concurrency and state rules.

SBI abstracts selected higher-privilege services; it is not a complete hardware description or universal device API.

### Bring up secondary processors

Keep secondary cores parked in a defined coherent state, publish per-core stacks/entry/context, order visibility, then release or request start. Each core validates identity and acknowledges arrival.

Timeout and partial arrival policies prevent one failed core from hanging boot invisibly.

### Transfer interrupt and timer ownership

Initialize controllers masked, install valid handlers/stacks, clear stale pending state according to device semantics, set routing/priority, then enable delivery. Establish monotonic time and event facilities before scheduling depends on them.

Firmware-reserved interrupts and timer services must be excluded from OS ownership explicitly.

### Preserve reserved memory

Reserve firmware runtime code/data, secure-world memory, measurement logs, crash buffers, device carveouts, IOMMU structures, and hardware holes before general allocation.

Reconcile overlaps conservatively; never silently convert an unknown reserved range into RAM.

### Handle firmware runtime calls

Map runtime regions with described attributes, convert pointers only under the prescribed transition, serialize calls as required, and defend the kernel from faulty firmware with timeouts/platform policy where possible.

Runtime firmware remains privileged code in the trusted computing base.

### Support virtualization

Define whether firmware calls are trapped, emulated, forwarded, or unavailable to guests. Give each guest synthetic machine descriptions and memory maps consistent with assigned resources.

Host physical tables must not leak unassigned devices, addresses, keys, or topology.

### Design atomic updates

Authenticate the update package, write inactive storage, verify readback, atomically select the candidate, record trial state, and commit only after a defined health signal. Power loss at every write boundary must leave a recovery route.

Wear limits and shared metadata require explicit transactional design.

### Bound recovery authority

Recovery images and media follow their own authenticated policy, least-privilege device access, rollback constraints, and audit trail. User-presence or enterprise policy may authorize exceptional operations.

Recovery convenience must not dissolve the normal trust chain.

### Preserve failure evidence

Record reset cause, failing stage/error, verified image identity, rollback counter, measurement-log status, and update slot in retained storage before destructive reset when feasible.

Treat logs as bounded, integrity-sensitive, and potentially confidential.

### Minimize parsers and drivers

Complex filesystems, networks, option ROMs, decompression, configuration languages, and device drivers enlarge pre-OS attack surface. Keep early formats and privileges narrow.

Sandbox or defer untrusted extensibility where the platform permits.

### Make errors typed and fail closed

Differentiate absent capability, unsupported version, malformed input, authentication failure, rollback, resource exhaustion, timeout, hardware fault, and policy denial. Choose recovery based on type without treating corruption as absence.

Avoid fallback from secure interface failure to an unauthenticated legacy path.

### Verify handoff refinement

Create a reference model for memory ownership, table parsing, image ranges, stage state, and service availability. Every implementation handoff must refine one legal model transition.

Assert no stale owner, executable unauthenticated byte, writable protected region, post-exit boot call, or dangling machine-description reference.

### Test hostile descriptions and images

Fuzz lengths, offsets, recursion, strings, duplicate handles/phandles, overlapping segments, decompression bombs, invalid entry points, changed memory-map keys, missing extensions, and malformed runtime descriptors.

Use sanitizers/emulation first, then fault-injected boards and update power-cut testing.

### Gather layered evidence

Combine deterministic range models, parser/unit tests, UEFI/ACPI/Devicetree/SBI conformance, emulated boots, hardware traces, secure-boot negative tests, update interruption, multicore stress, and OS regression.

Bind results to platform, firmware configuration, keys/policy, boot media, OS, and specification revisions.

## Definitions and Notation

- `S_i`: boot stage `i`.
- `H_i`: immutable handoff record from `S_i` to its successor.
- `R=[base,end)`: half-open physical range with checked `end=base+size`.
- `owner(R,t)`: unique component authorized to mutate range/resource `R` at transition state `t`.
- `image=(bytes,metadata,target,version,entry)`: candidate executable plus authorization context.
- `authorized(image,policy)`: signature, key, target, version, revocation, and dependency policy pass.
- `measured(x)`: canonical bytes/configuration `x` extended and represented consistently in the event log.
- `map_key`: token identifying the exact UEFI memory-map generation used for boot-service exit.
- `MD`: validated machine-description graph.
- `service_available(s,t)`: service `s` may be called in lifecycle state `t`.
- `handoff_ok`: authorization, bounds, ownership, visibility, ABI, and lifecycle predicates all hold.

Half-open ranges simplify adjacency: `[a,b)` and `[b,c)` do not overlap. Every addition is checked in the address width before comparison.

## Mechanisms, Invariants, or Proof Structure

1. **Reset obligation:** each assumed initial processor/platform property is architecturally guaranteed or established.
2. **Stage obligation:** the complete normal, update, and recovery graph has authenticated successors and bounded authority.
3. **Image obligation:** parsing, load ranges, entry, bytes, metadata, keys, revocation, and rollback policy agree.
4. **Memory obligation:** every range is checked, non-overlapping as required, attributed, and uniquely owned.
5. **Description obligation:** machine-description structure, references, resources, topology, and reserved ranges validate.
6. **Visibility obligation:** writes, cache maintenance, barriers, and instruction synchronization precede use.
7. **ABI obligation:** registers, stack, entry, privilege, translation, interrupts, and calling convention match.
8. **Lifecycle obligation:** services and pointers are used only in states where their contracts remain valid.
9. **Exit obligation:** the final memory-map generation matches successful boot-service termination.
10. **Privilege obligation:** delegated and retained firmware authority is minimal and protected from successors.
11. **Multicore obligation:** secondary release observes initialized per-core state exactly once or fails visibly.
12. **Evidence obligation:** measurements/logs, reset causes, image IDs, and update state correspond to actual actions.
13. **Update obligation:** every interrupted update state retains an authenticated boot or recovery path.
14. **Recovery obligation:** fallback is authenticated, rollback-aware, bounded, and auditable.
15. **Progress obligation:** finite retries/timeouts lead to handoff, contained recovery, or diagnosable halt.

Prove each transition by establishing `handoff_ok` before the branch and a single ownership cut: predecessor writes finish before publication, successor reads begin after acquire/synchronization, and post-cut mutation follows only the new contract. Compose the transitions only if security state and reserved resources remain monotonic across the whole stage graph.

## Alternatives and Trade-Offs

1. **Fixed layout versus discoverable tables:** fixed layouts simplify tiny systems; tables support platform variation.
2. **Devicetree versus ACPI:** Devicetree describes instantiated hardware explicitly; ACPI adds standardized tables and executable namespace methods.
3. **Direct register access versus firmware calls:** direct access lowers mediation; calls preserve platform policy/abstraction.
4. **Rich firmware versus minimal firmware:** rich pre-OS services improve compatibility; minimal firmware shrinks privileged attack surface.
5. **Single image versus staged chain:** one image reduces interfaces; stages separate immutable roots, updates, and policy.
6. **Copy versus execute in place:** copying permits placement/protection; XIP saves RAM/time but constrains storage/cache behavior.
7. **Eager versus deferred device initialization:** eager supports boot I/O; deferred keeps firmware simpler and leaves ownership to OS.
8. **Verified versus measured boot:** verification enforces local policy; measurement supports attestation and diagnosis.
9. **A/B slots versus recovery image:** A/B supports transactional trials; a recovery image costs less storage but may limit repair.
10. **Runtime services versus OS-native drivers:** runtime services preserve platform features; native drivers reduce firmware dependency.
11. **Identity versus relocated runtime mappings:** identity is simpler; relocation fits OS layout but requires exact pointer conversion.
12. **Static secondary release versus firmware-mediated start:** static mechanisms are direct; mediation can preserve platform sequencing.
13. **Strict halt versus degraded boot:** halt protects invariants; degraded boot can preserve availability with narrower capabilities.
14. **Detailed logs versus minimal disclosure:** rich logs aid diagnosis; early logs can expose secrets/topology.
15. **Compatibility fallback versus fail-closed:** fallback broadens bootability; it can silently bypass the intended trust policy.

## Failure Modes and Misconceptions

1. “Reset provides a C environment.” Stack, RAM, globals, caches, and secondary-core state must be established.
2. “The reset state is identical across implementations.” Architectural guarantees and implementation options differ.
3. “Successful DRAM training proves all memory.” It proves a configuration under limited conditions, not exhaustive reliability.
4. “A parsed executable is safe to load.” Bounds, overlap, permissions, target, authenticity, and entry need validation.
5. “A valid signature authorizes execution.” Key policy, revocation, version, target, and dependencies also matter.
6. “Verified boot and measured boot are synonyms.” One gates execution; the other records evidence.
7. “Signed old firmware is safe.” Rollback protection is a separate policy/state mechanism.
8. “A checksum authenticates ACPI.” It is an integrity-format check, not a trust proof.
9. “Devicetree is just a list of addresses.” Hierarchy, cells, translations, references, bindings, and reserved memory matter.
10. “A compatible string proves a device exists.” Firmware input and hardware reality can disagree.
11. “Firmware tables may be trusted because firmware supplied them.” Trust and parser safety remain explicit decisions.
12. “Physical addresses are universal.” Bus translations, IOMMUs, aliases, and secure ownership can differ.
13. “Adjacent ranges overlap.” Half-open ranges sharing an endpoint are disjoint.
14. “Checking `base < limit` prevents overflow.” Compute end with checked arithmetic first.
15. “UEFI protocols survive OS handoff.” Boot protocols/services end at successful exit.
16. “Any memory-map key can exit boot services.” It must identify the current map generation.
17. “Retrying exit needs only the old map.” Reacquire the map/key after mutation.
18. “Runtime services work under arbitrary mappings.” Required descriptors, attributes, and transition rules apply.
19. “The entry ABI is obvious from architecture.” Each platform/boot protocol specifies registers and state.
20. “Cache maintenance is optional after copying code.” Noncoherent paths can execute stale instructions.
21. “Releasing cores after writing entry is ordered automatically.” Publication and synchronization are required.
22. “SBI describes all RISC-V hardware.” It exposes selected supervisor services; machine description remains separate.
23. “Recovery may skip verification because normal boot failed.” That turns failure into policy bypass.
24. “A/B storage makes updates atomic automatically.” Selection, trial, health, counter, and metadata writes must be transactional.
25. “Measurement logs cannot lie if registers are protected.” Log entries must correspond exactly to extended events.
26. “A boot that reaches the kernel is correct.” Ownership, security, topology, runtime, update, and failure invariants need evidence.

## Worked Examples

### Example 1

ROM authenticates a board-specific first stage before DRAM exists, so it verifies into bounded SRAM and grants only the registers/storage needed to initialize memory.

### Example 2

An ELF segment's `offset+filesz` wraps the file-width integer. Checked addition rejects it before a small-looking bounds comparison can pass.

### Example 3

A Devicetree child `reg` uses the parent's two address cells and one size cell, then a bus `ranges` property translates it into the processor physical map.

### Example 4

An ACPI table has correct signature and checksum but a length extending outside its owned region; structural bounds reject it.

### Example 5

The loader obtains a UEFI map, an allocation changes it, and `ExitBootServices` rejects the stale key. The loader reacquires the map and retries without intervening allocations.

### Example 6

Firmware marks two code pages and one variable page runtime. The OS preserves their attributes and performs the specified virtual-address transition before later calls.

### Example 7

A RISC-V kernel queries the SBI base and timer extension, handles “not supported,” and selects a platform alternative instead of issuing an assumed legacy call.

### Example 8

An A/B update boots the candidate as a trial; watchdog reset before health confirmation leaves the prior authenticated slot selected and records the failure.

### Example 9

Secondary cores observe per-core stack and entry only after a release barrier, acknowledge arrival, and time out into a documented reduced-core configuration.

### Example 10

This deterministic range audit finds overlap among a kernel, machine description, and reserved region using checked half-open intervals.

<!-- bijux-verify: {"id":"boot-handoff-range-audit","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"kernel=[0x80200000,0x80218000) valid=yes\ndevicetree=[0x80218000,0x80220000) valid=yes\nreserved=[0x8021f000,0x80223000) valid=yes\nkernel_devicetree_overlap=no\ndevicetree_reserved_overlap=yes overlap_bytes=4096\nhandoff=reject\n"}} -->
```python
address_limit = 1 << 32
ranges = {
    "kernel": (0x80200000, 96 * 1024),
    "devicetree": (0x80218000, 32 * 1024),
    "reserved": (0x8021f000, 16 * 1024),
}

def checked(name):
    base, size = ranges[name]
    end = base + size
    valid = 0 <= base < address_limit and 0 <= size and end <= address_limit
    print(f"{name}=[0x{base:08x},0x{end:08x}) valid={'yes' if valid else 'no'}")
    return base, end, valid

kernel = checked("kernel")
devicetree = checked("devicetree")
reserved = checked("reserved")

def overlap(left, right):
    start = max(left[0], right[0])
    end = min(left[1], right[1])
    return max(0, end - start)

kd = overlap(kernel, devicetree)
dr = overlap(devicetree, reserved)
print(f"kernel_devicetree_overlap={'yes' if kd else 'no'}")
print(f"devicetree_reserved_overlap={'yes' if dr else 'no'} overlap_bytes={dr}")
print("handoff=reject" if dr or not all(x[2] for x in (kernel, devicetree, reserved)) else "handoff=accept")
```

## Cross-Program Connections

- **Operating Systems:** loaders transfer memory maps, machine descriptions, privilege, timers, interrupts, and firmware services to kernels.
- **Computer Security:** roots of trust, signatures, revocation, rollback, measurement, recovery, and secret erasure begin before the OS.
- **Distributed Systems:** boot stages form a local protocol with version negotiation, durable state, retries, idempotence, and failure recovery.
- **Programming Languages:** binary/table parsers need memory safety, checked arithmetic, type validation, and bounded recursion.
- **Storage Systems:** updates require crash-consistent slot data, metadata, counters, selection, and health commits.
- **Virtualization:** hypervisors synthesize tables/services and mediate privileged firmware interfaces for guests.
- **Systems Engineering:** end-to-end assurance composes silicon, board, firmware, policy, keys, boot media, and OS evidence.

## References

1. UEFI Forum, [Specifications: UEFI 2.11, ACPI 6.6, and PI releases](https://uefi.org/specifications), accessed 2026-09-04.
2. UEFI Forum, [Unified Extensible Firmware Interface Specification 2.11](https://uefi.org/sites/default/files/resources/UEFI_Spec_Final_2.11.pdf), accessed 2026-09-04.
3. UEFI Forum, [Advanced Configuration and Power Interface Specification 6.6](https://uefi.org/sites/default/files/resources/ACPI_Spec_6.6.pdf), accessed 2026-09-04.
4. Devicetree.org, [Devicetree Specification releases](https://www.devicetree.org/specifications/), accessed 2026-09-04.
5. RISC-V International, [RISC-V Supervisor Binary Interface specification repository](https://github.com/riscv-non-isa/riscv-sbi-doc), accessed 2026-09-04.
6. Trusted Firmware-A, [Firmware design](https://trustedfirmware-a.readthedocs.io/en/latest/design/firmware-design.html), accessed 2026-09-04.
7. Linux kernel documentation, [Booting AArch64 Linux](https://docs.kernel.org/arch/arm64/booting.html), accessed 2026-09-04.
8. Linux kernel documentation, [The EFI boot stub](https://www.kernel.org/doc/html/latest/admin-guide/efi-stub.html), accessed 2026-09-04.

## Exercises

### Exercise 1

Specify a reset-to-kernel stage graph for a four-core platform with ROM, mutable platform firmware, UEFI loader, recovery image, secure monitor, and hypervisor. State trust, memory, privilege, authentication, and secondary-core ownership at each edge.

### Exercise 2

Design a validator for an image with three segments plus a Devicetree and measurement log. Include checked arithmetic, alignment, overlap, entry, permissions, reserved memory, canonical measurement, and cache-maintenance rules.

### Exercise 3

Give a race-safe UEFI handoff algorithm from final memory-map acquisition through page-table activation and successful boot-service exit. Explain retry behavior and forbidden operations.

### Exercise 4

Design an A/B firmware update protocol with signature verification, rollback protection, trial boot, health confirmation, watchdog failure, power loss at every metadata write, and authenticated recovery.

### Exercise 5

Create a verification plan for Devicetree/ACPI/SBI handoff on physical and virtual platforms. Include malformed input, multicore ordering, missing capabilities, runtime services, evidence capture, and limitations.

## Answers to the Exercises

### Answer 1

ROM owns reset core and immutable keys, authenticates bounded firmware into SRAM, and keeps other cores parked. Platform firmware initializes coherent DRAM/controllers, authenticates the UEFI payload/recovery policy, installs secure monitor, and transfers only nonsecure ranges. UEFI authenticates loader; loader validates machine description/map and authenticates hypervisor/kernel.

Publish per-core stacks/entries before monitor-mediated release. Secure monitor retains only delegated calls and secure memory; hypervisor takes nonsecure memory, interrupts, IOMMU, cores, and guest descriptions. Every failure edge reaches authenticated rollback-aware recovery or a diagnosable halt.

### Answer 2

For each file offset, load base, file size, memory size, alignment, and entry computation, use width-bounded addition and require file range, owned destination, `filesz<=memsz`, permitted alignment, no forbidden overlap, and executable entry membership. Compare half-open segment, Devicetree, log, stack, firmware, secure, MMIO, and reserved ranges.

Hash canonical authenticated bytes/metadata, copy/decompress, zero memory tails, assign least permissions, clean data cache, invalidate instruction cache, and synchronize before entry. Reject unknown mandatory fields and make the exact accepted layout part of evidence.

### Answer 3

Allocate every buffer and construct page tables first. Retrieve the UEFI map/key into an oversized stable buffer, then perform no map-changing boot-service operation. Call `ExitBootServices` with that key. On the specified stale-key failure, reacquire map/key and retry the bounded pair; do not reuse the old map.

After success, never call boot services or protocol pointers. Preserve runtime/reserved descriptors and attributes, finish cache/TLB synchronization, activate entry-valid page tables/stack/vector, and branch under the documented ABI.

### Answer 4

Verify package signature, target, dependencies, revocation, and version before writing inactive slot. Write data plus manifest, verify readback, then crash-consistently mark candidate/trial while retaining old confirmed slot. Boot candidate with bounded attempts; commit selection and monotonic counter only after authenticated health evidence.

Watchdog/power loss decrements or invalidates trial without harming confirmed slot. Every metadata state has deterministic selection; recovery is separately authenticated and cannot install below rollback policy except through explicit protected authorization.

### Answer 5

Use schema/binding/table validators plus fuzzing for lengths, cells, references, recursion, duplicates, checksums, overlap, unknown revisions, missing SBI extensions, malformed return codes, and runtime descriptors. Reference-model ownership and ABI state across emulation, hypervisor synthesis, real boards, secondary-core release, cache/MMU changes, exit retries, and runtime calls.

Capture exact blobs, hashes, logs, calls/results, firmware/OS/board revisions, and reset causes. Negative tests inject stale map keys, unavailable services, corrupt tables, core timeout, power cuts, and firmware hangs. Internal tests do not establish silicon, cryptographic-module, or external secure-boot certification.
