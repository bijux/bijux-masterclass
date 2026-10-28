---
module_id: CA-037
program: Computer Architecture
level: 1
module_number: 37
title: Main-Memory Organization
status: complete
last_verified: 2026-09-04
---

# Main-Memory Organization

## One-Page Review

### Governing question

How should memory controllers, channels, modules, ranks, devices, bank groups, banks, rows, columns, bursts and protection bits be composed and addressed so that advertised capacity is real, parallelism is usable, data lanes are complete, failures are contained and software-visible memory behaves coherently?

### Essential definitions

- A **memory channel** is an independently controlled command/address/data interface or logical controller path.
- A **module** is a replaceable package, such as a DIMM, carrying memory devices and support components.
- A **rank** is a set of devices selected together to supply the channel's data width for an access.
- A **device** is one memory component with a specified density and data width such as `x8`.
- A **bank** is a semi-independent storage array with one active row buffer in the elementary DRAM model.
- A **bank group** organizes banks with additional timing/resource relationships in applicable DRAM generations.
- A **row** is a wordline-sized collection activated into a bank's row buffer.
- A **column** selects data within the active row for a burst transfer.
- A **burst** transfers multiple data beats after one column command.
- **data rate** counts transfers per second per data pin and is not the command clock frequency.
- **rank interleaving** alternates requests across ranks to expose timing slack and capacity.
- **address mapping** assigns physical-address fields or functions to channel, rank, bank-group, bank, row, column and byte positions.
- **ECC** adds check symbols/data paths to detect or correct specified error patterns; its guarantee depends on code, lane mapping and failure model.
- **refresh** periodically restores volatile DRAM charge and temporarily consumes array command opportunity.
- **memory scrubbing** reads, checks and possibly rewrites memory to prevent latent errors from accumulating.

### Central model, mechanism, or theorem

Capacity is a product of independently verified geometry. For `C` channels, `R` ranks/channel, `D` data devices/rank, `B` banks/device, `W` rows/bank, `K` columns/row and device width `x` bits/column, usable data bytes are `C*R*D*B*W*K*x/8` after reconciling burst/column conventions. Peak data bandwidth is `channels*transfers/s*channel_data_bits/8`, but sustained useful bandwidth subtracts refresh, command gaps, turnarounds, ECC/retry and access-pattern conflicts. Address mapping must be bijective over installed usable locations and preserve exact byte/lane identity.

### Critical invariants

- Installed device density, width and count multiply to the claimed rank/channel/system capacity without double-counting burst beats.
- Every accepted physical byte maps to one intended channel/rank/device/bank/row/column/lane and reconstructs uniquely.
- All data and check lanes of a rank correspond to the same logical transfer, beat and address.
- Requests outside populated or enabled capacity never alias installed memory.
- Rank/chip-select, bank and row commands cannot select incompatible devices or stale configuration.
- Writes preserve unselected bytes/check symbols through masks, read-modify-write or code-specific handling.
- Refresh and power-state transitions preserve retained data under documented operating limits.
- ECC correction/detection claims match symbol placement, chip/lane failure modes and reporting behavior.
- Controller queues and interleaving cannot reorder operations beyond the architectural/coherence contract.
- Capacity/bandwidth/RAS measurements bind exact topology, rate, mapping, firmware and population.

### Common failures

Common failures include multiplying megatransfers by two again because DDR has two edges, treating an `x8` device as eight bytes wide, counting ECC capacity as usable application data, confusing ranks with channels, assuming every bank serves simultaneously through one shared data bus, interpreting a row-buffer hit as a cache hit, mapping low address bits entirely to one bank, crossing device lanes between ranks, ignoring partial-population holes, calculating capacity from marketing module labels instead of discovered geometry, assuming SECDED corrects every multi-bit/chip failure, scrubbing without ownership/order rules, and claiming peak bandwidth as sustained application bandwidth.

### Compact example

Two channels with two ranks each, eight `x8` data devices per rank, 32 banks/device, 65,536 rows/bank and 1,024 column locations/row yield 64 GiB usable data under the stated column-width convention. One extra `x8` ECC device per rank produces 72 GiB physically installed device capacity for 64 GiB usable, or 12.5% check capacity relative to usable data. A 64-bit channel at 4.8 GT/s has 38.4 GB/s pin-rate peak; two channels have 76.8 GB/s before protocol and workload losses.

### Connections

Main-memory organization connects binary capacity arithmetic, DRAM circuits, address hashing, cache-line placement, controllers, coherence, virtual-memory NUMA policy, ECC/RAS, board topology, firmware discovery, power management and performance counter interpretation.

## Governing Question

Main memory looks like a byte array to software, but the implementation is a hierarchy of controllers, links, ranks, narrow devices and two-dimensional arrays. Address mapping and coordinated devices transform those structures into a uniform line transfer.

Organization determines capacity, available bank/rank/channel parallelism, row locality, wiring, failure domains and upgrade rules. A correct design must make all levels agree on identity and topology before optimization begins.

## Why This Matters

An incorrect capacity formula can overstate memory by a burst factor or expose aliases. An incorrect lane mapping can combine bytes from different beats or make ECC check the wrong symbols. These are functional defects, not small performance errors.

Organization also shapes latency and bandwidth. Sequential address placement can concentrate traffic on one channel or preserve row locality; hashing can spread load while complicating diagnosis and locality prediction.

Reliability depends on physical placement. The same abstract ECC bits provide different chip-failure coverage depending on how symbols span devices and lanes.

## Prerequisites and Retrieval

Before studying this module, be able to:

- manipulate powers of two and convert bits, bytes, GiB and transfers/s;
- explain cache-line and physical-address decomposition;
- distinguish latency, throughput and capacity;
- describe row activation and burst transfer at a conceptual level;
- explain basic error detection/correction and memory ordering.

Retrieve controller/channel count and topology; module type and electrical population rules; ranks/channel; devices/rank, density, width and organization; bank-group/bank/row/column geometry; burst length, prefetch architecture and data-beat convention; channel data/check width; data rate and clocks; address map/hash and reserved holes; rank/bank/device decode; byte/bit lane wiring and swizzling; write masks; ECC codeword/symbol/lane placement; spare rows/ranks/devices; refresh modes and temperature policy; power states; training/calibration; firmware discovery tables; interleaving/NUMA domains; hotplug/repair behavior; error injection/reporting; counters; controller/PHY/module/firmware/OS revisions; environmental limits and errata.

## Learning Objectives

After completing this module, you should be able to:

1. distinguish channels, modules, ranks, devices, banks, rows, columns and bursts;
2. derive data and raw capacity from device geometry;
3. compute pin-rate peak bandwidth without DDR double-counting;
4. map a physical address through an explicit hierarchy and reconstruct it;
5. compare row-, bank-, rank- and channel-interleaving choices;
6. explain how narrow devices jointly form data/ECC channel width;
7. identify partial-population, mirroring, sparing and reserved-capacity effects;
8. separate ECC capability from physical failure coverage and recovery policy;
9. verify topology, address/lane mapping, refresh and integrity invariants;
10. validate organization using documentation, simulation, firmware and hardware evidence.

## Core Exposition

### Begin with the software abstraction

Software issues byte-addressed loads/stores to physical addresses after translation. The memory system may interleave and hash those addresses, but it must implement the same coherent bytes and attributes.

Define populated ranges, holes, aliases, reserved firmware regions and NUMA ownership before deriving array fields.

### Distinguish controller and channel

A controller schedules memory commands and may operate one or more channels/subchannels. A channel has its own relevant buses/links and can provide parallel data opportunity relative to another channel.

Do not infer channel count from controller count or module sockets. Retrieve the actual topology and population-dependent modes.

### Understand modules

A module carries devices, identification data and sometimes registers, buffers, power-management or error-protection components. Module capacity is a consequence of its devices/ranks, not a substitute for understanding them.

Population affects electrical loading, supported data rates and interleaving. Empty sockets and disabled ranks do not provide capacity.

### Understand ranks

Devices in one rank are selected together and contribute different data/check lanes to a transfer. Two ranks can share a channel's data wires but have distinct chip-select and stored capacity.

Ranks do not normally double instantaneous channel pin width. Rank switching can hide some timing constraints but adds turnarounds and loading.

### Understand device width

An `x8` device contributes eight data bits per transfer beat, not eight bytes. Eight `x8` data devices form a 64-bit data interface when selected together.

Device density combines array geometry and width. Confirm vendor convention before multiplying columns by burst length or internal prefetch width.

### Understand banks and bank groups

Banks provide independent row state and some parallel command opportunity, but share rank/channel resources. Bank groups introduce timing distinctions among same/different-group command sequences where specified.

Bank count is not equal to simultaneous full-bandwidth transfers. Command/data buses and timing constrain service.

### Understand rows

An activate operation selects one row into a bank's row buffer. Accesses to columns of that active row can avoid another activate; a different row requires closure/precharge and activation under applicable policy.

Row size in one device differs from the rank-wide bytes visible across all devices. State the granularity.

### Understand columns and bursts

A column command initiates a burst of beats from the active row. Documentation may specify column addresses in units affected by device width, burst length and internal prefetch architecture.

Derive capacity from the device's official density/organization and use column arithmetic only after reconciling conventions.

### Derive device capacity

Under a simplified explicit geometry, device bits equal banks times rows per bank times column locations per row times bits per location. Convert bits to bytes once.

Cross-check against stated device density. A mismatch often reveals burst or bank-group double-counting.

### Derive rank capacity

Multiply one device's capacity by the number of data devices contributing unique data lanes. Check devices may add physical bits but not ordinary usable bytes.

Stacked packages or multi-die devices require the vendor's logical organization; package count alone may not expose die/rank structure.

### Derive system capacity

Sum enabled ranks across channels, then subtract or separately report mirroring, sparing, firmware reservations, encryption metadata or disabled regions.

Report raw installed, usable physical-address and OS-available capacity separately. GiB and GB differ by powers of two versus ten.

### Form channel data width

Lane wiring maps each device's DQ bits to positions in the channel word on every beat. Byte enables and burst order must agree with controller logic and board swizzling.

Training can discover timing relationships but does not excuse an incorrect logical lane map.

### Add ECC lanes

A common organization adds check devices/lanes beside data devices. ECC encoding groups data/check symbols into codewords; coverage depends on code and how symbols cross chips.

State correction/detection strength precisely. “ECC memory” alone does not prove chipkill, retry, poison, patrol scrub or end-to-end coverage.

### Calculate ECC overhead

For 64 data bits plus 8 check bits per beat, physical lane capacity is 72/64 or 1.125 times usable data, a 12.5% overhead relative to usable data and 11.11% of raw bits.

Include spare devices/rows and mirrored data separately; they serve different reliability mechanisms.

### Compute peak bandwidth

Pin-rate peak per channel equals transfers/s times data bits/transfer divided by eight. If a specification already states GT/s or MT/s, do not multiply by DDR edges again.

Aggregate independent channels only when mapping, controllers and workload can use them concurrently.

### Explain sustained bandwidth

Useful bytes are below pin peak because commands, refresh, row changes, bus turnarounds, reads/writes, conflicts, ECC/retry and finite request parallelism consume opportunities.

Measure at the interface relevant to the claim and distinguish payload from check/protocol traffic.

### Design address mapping

Map byte/beat/column, bank, bank group, rank, channel and row using selected bit fields or XOR hashes. Low-bit interleaving can distribute consecutive cache lines; row-friendly mapping may preserve larger sequential runs.

The mapping must cover every populated location exactly once, reject holes and remain consistent in controller, firmware, diagnostics and performance analysis.

### Reconstruct addresses

For direct field mappings, concatenate decoded fields and verify round trips. For XOR/hash mappings, implement and test the inverse or prove uniqueness over the configured domain.

Round-trip tests at every boundary catch dropped bits, overlap and off-by-one capacity errors.

### Interleave channels

Channel interleaving places nearby regions across channels to raise bandwidth and balance queues. Coarse mapping can preserve locality or isolation but concentrate a hot region.

Record granularity and hash. Software page placement and cache-line size influence whether applications exploit it.

### Interleave ranks

Rank interleaving uses otherwise idle rank resources and may hide refresh or row timing, while all ranks still contend for the channel data bus.

Switching rank direction can add delay. Power-down policy and thermal limits change availability.

### Interleave banks

Bank selection from moderately low address bits lets consecutive requests occupy multiple banks. Mapping everything sequential into one row maximizes row locality but limits bank parallelism.

Choose using measured access patterns and controller scheduling. Hashing can reduce pathological strides.

### Preserve row locality

Keeping nearby accesses in the same row reduces activates when requests arrive together and policy keeps the row open. It can also create hot-bank concentration.

Row-buffer locality is a DRAM scheduling condition, not cache residency. Report hit/conflict/empty categories with exact definitions.

### Handle partial population

Asymmetric ranks/channels may create flex regions: part interleaved, remainder mapped to one channel. Firmware and OS must expose the actual topology.

Test boundaries between symmetric and remainder regions. Never apply a uniform hash beyond populated capacity.

### Handle NUMA organization

Sockets/controllers define non-uniform latency and bandwidth domains. Physical pages should be placed near requesters when policy and workload permit.

Remote access still uses coherent system interconnects. Channel bandwidth numbers alone omit those paths.

### Integrate caches and coherence

Cache-line addresses become memory requests after coherent ownership and writeback. Memory mapping must preserve all line bytes and not split unsupported atomic/coherence units incorrectly.

Home-node or directory hashes may differ from DRAM channel mapping. Document both.

### Handle writes and masks

Narrow writes may be combined, masked on the bus or require read-modify-write for ECC/codeword granularity. Preserve untouched bytes and check symbols.

Posted write acknowledgment, controller buffering and durable completion are distinct. Volatile DRAM acceptance is not persistence.

### Refresh volatile arrays

Rows must be refreshed within documented temperature/device limits. Refresh can be all-bank, per-bank or fine-grained depending on technology.

Controller scheduling must meet retention while bounding request delay. Self-refresh and power transitions require entry/exit correctness.

### Scrub memory deliberately

Patrol scrubbing finds/corrects latent errors before another fault makes them uncorrectable. It consumes bandwidth and interacts with caches/coherence when writing corrected data.

Scrub address coverage, rate, exclusions, error escalation and hotplug/power behavior require verification.

### Support repair and sparing

Devices may remap defective rows internally; systems may spare ranks/lanes/pages or mirror memory. These change available capacity and failure containment.

Record activation conditions and persistent error logs. A repair must not silently remap the wrong physical identity.

### Train the physical interface

High-rate interfaces calibrate delays, voltage references and lane timing. Training results apply to exact population, rate, voltage and temperature conditions.

Failures should fall back safely or disable affected capacity rather than expose unreliable memory.

### Discover topology in firmware

Firmware reads module information, configures controllers, trains links and publishes usable ranges/topology/error data to the OS. Discovery should match physical population.

Cross-check firmware tables against controller registers and diagnostics; stale inventory creates capacity or placement errors.

### Handle hotplug and lifecycle

Adding/removing memory requires quiescing, migrating or invalidating pages and updating mappings without live aliases. Not all hardware supports dynamic topology.

Reset, sleep and power loss have distinct retention contracts. Volatile memory contents cannot be assumed across unsupported transitions.

### Threat-model address mapping

Predictable bank/row placement can enable contention or disturbance attacks; secret hashes may complicate diagnostics without eliminating physical effects.

Use isolation, monitoring, refresh/repair and platform mitigations based on a stated threat model and actual device behavior.

### Verify organization

Unit-test capacity products and address round trips. Exercise first/last bytes, every field transition, holes, asymmetric population, lane masks, ECC injection, refresh and power states.

Compare controller models with firmware discovery and physical schematics. Use traffic generators and hardware counters for channel/rank/bank distribution.

### Gather layered evidence

Start with datasheets/specifications and executable arithmetic; then use memory-controller simulation, RTL assertions, board/lane review and firmware tests. Validate RAS through controlled error injection where authorized.

Measure bandwidth/latency patterns and applications across placements. Bind device stepping, module population, controller/PHY RTL, firmware, OS, temperature and errata.

## Definitions and Notation

- `C`: enabled memory channels.
- `R`: enabled data ranks per channel under a uniform example.
- `D`: data devices per rank.
- `E`: check/ECC devices per rank.
- `G`: bank groups per device/rank organization as specified.
- `B`: banks per device, or `G` times banks/group when applicable.
- `W`: rows per bank.
- `K`: column locations per row under an explicit device convention.
- `x`: device data bits contributed per column/beat (`x8`, for example).
- `F`: transfers per second per data pin.
- `Q`: channel usable data bits per transfer.
- `capacity_data=C*R*D*B*W*K*x/8` bytes in the simplified uniform model.
- `bandwidth_peak=C*F*Q/8` bytes/s for independent equally rated channels.
- `row_hit`: request whose target row is already active in its bank under the controller definition.
- `raw_capacity`: all installed data/check/spare bits, stated by inclusion policy.

Symbols deliberately separate data devices from ECC devices and device width from channel width. Real standards may encode columns, bursts and internal prefetch differently; reconcile the simplified equation with authoritative device density before use.

## Mechanisms, Invariants, or Proof Structure

1. **Population obligation:** configured channels/ranks/devices match electrically present enabled hardware.
2. **Capacity obligation:** device geometry cross-checks density and system usable/raw totals without unit duplication.
3. **Range obligation:** only populated, nonreserved physical ranges are exposed.
4. **Decode obligation:** every exposed byte maps to exactly one installed location and round-trips.
5. **Lane obligation:** all data/check lanes align to the same rank, beat, address and codeword.
6. **Mask obligation:** partial writes preserve every unselected data/check symbol.
7. **Command obligation:** rank/bank/row/column selection and power state make each command legal.
8. **Ordering obligation:** scheduling/interleaving preserves coherence, atomics, fences and device rules.
9. **Refresh obligation:** every retained row meets the specified refresh window under supported conditions.
10. **Integrity obligation:** detection/correction/poison behavior matches the code and physical failure mapping.
11. **Repair obligation:** sparing/remap/mirroring preserves unique physical identity and reports capacity changes.
12. **Lifecycle obligation:** training, reset, sleep, hotplug and power transitions expose only trustworthy state.
13. **Progress obligation:** refresh, scrub and RAS work cannot permanently starve demand under stated fairness.
14. **Discovery obligation:** firmware/OS topology and ranges match controller decode.
15. **Evidence obligation:** capacity, bandwidth and reliability claims bind topology, units, versions and environment.

The proof begins with bijective address decode over populated ranges and a lane/codeword mapping for each transfer. State-machine invariants then cover commands, refresh, writes, errors and lifecycle. Coherent ordering composes at the controller interface. Reliability and performance require fault-injection and workload evidence beyond arithmetic.

## Alternatives and Trade-Offs

1. **More channels versus wider channels:** more channels expose independent queues; wider channels move more bits per transfer.
2. **More ranks versus fewer:** ranks add capacity/interleaving; they increase loading, turnaround and power complexity.
3. **x4 versus x8 devices:** narrower devices change device count and ECC symbol/failure mapping.
4. **More banks versus simpler control:** banks expose parallelism; shared buses and timing limit realized throughput.
5. **Fine versus coarse channel interleaving:** fine mapping balances streams; coarse mapping aids isolation/locality.
6. **Simple fields versus XOR hashing:** fields are diagnosable; hashes reduce stride hotspots but complicate inversion.
7. **Open-row versus close-row orientation:** open rows exploit locality; close/adaptive policies reduce conflicts.
8. **Symmetric versus asymmetric population:** symmetry maximizes uniform interleaving; asymmetry preserves upgrade flexibility/capacity.
9. **ECC versus no ECC:** ECC consumes lanes/capacity/latency but detects/corrects defined faults.
10. **SECDED versus stronger codes:** stronger coverage handles broader faults at more check/data-path cost.
11. **Sparing versus mirroring:** sparing replaces failed resources; mirroring tolerates broader failures at large capacity cost.
12. **Frequent versus sparse scrubbing:** frequent scrub lowers latent-error exposure; it spends bandwidth/energy.
13. **All-bank versus per-bank refresh:** all-bank is simpler; per-bank can preserve more service opportunity.
14. **Maximum rate versus conservative rate:** peak rate raises bandwidth; reduced rate may support heavier population/margin.
15. **Hardware transparency versus software topology:** transparency simplifies software; explicit NUMA enables placement control.

## Failure Modes and Misconceptions

1. “A channel is a DIMM socket.” Topology and subchannels/controllers differ.
2. “Two ranks double channel width.” They usually share the same data wires at different selections.
3. “x8 means eight bytes.” It means eight bits per device transfer.
4. “Burst length multiplies official density.” Density already incorporates the device organization convention.
5. “Bank groups are extra capacity beyond banks.” Banks are partitioned into groups; do not multiply twice.
6. “Every bank transfers concurrently.” Shared command/data resources constrain them.
7. “Row-buffer hits are cache hits.” They are active-row scheduling outcomes after cache misses.
8. “GT/s needs another DDR factor of two.” Transfers/s already counts edges.
9. “Peak pin rate is application bandwidth.” Protocol, refresh, turns and workload reduce useful bytes.
10. “Two channels always double throughput.” Mapping and request parallelism must exercise both.
11. “ECC device bytes are usable memory.” They normally store check information.
12. “12.5% ECC overhead means 12.5% of raw.” It is 12.5% relative to 64-bit usable in a 72-bit example, 11.11% of raw.
13. “SECDED corrects any two-bit error.” It normally corrects one and detects (not corrects) two within its codeword assumptions.
14. “ECC protects every chip failure.” Symbol-to-device mapping and code strength determine coverage.
15. “Partial writes never affect ECC.” Check symbols must reflect merged complete codeword data.
16. “Unused address bits may be ignored.” Dropped bits create aliases or inaccessible capacity.
17. “One mapping applies to asymmetric capacity.” Remainder regions may use different decode.
18. “XOR hashing is automatically bijective.” Overlap/dropped source bits can break uniqueness.
19. “More row hits always improve system speed.” Queue fairness and dependent request latency also matter.
20. “Refresh only changes bandwidth.” It can create latency tails and retention failures if late.
21. “Self-refresh preserves memory under all power loss.” It requires specified retained power/conditions.
22. “Scrubbing is an ordinary DMA read.” Correction writes, coherence and error policy matter.
23. “Training proves all future conditions.” Margin changes with population, rate, voltage and temperature.
24. “Firmware-reported capacity proves wiring.” Cross-check decode, inventory and boundary tests.
25. “NUMA distance is only latency.” Bandwidth and interconnect contention vary too.
26. “No errors in a short test proves reliability.” Coverage, time, temperature and injected faults matter.

## Worked Examples

### Example 1

Eight `x8` data devices selected as one rank provide `8*8=64` data bits per transfer beat; a ninth `x8` device can carry eight check bits.

### Example 2

A 16-Gib `x8` device stores 2 GiB. Eight data devices form a 16-GiB rank; four such ranks form 64 GiB usable data.

### Example 3

At 4.8 GT/s and 64 data bits, one channel's pin-rate peak is `4.8e9*64/8=38.4e9` bytes/s.

### Example 4

A system exposes 64 GiB usable but installs 72 GiB across data/check devices. ECC overhead is 8/64=12.5% relative to usable.

### Example 5

Mapping cache-line bit 0 to channel alternates sequential 64-byte lines across two channels; a stride of 128 bytes may still concentrate depending on higher hashes.

### Example 6

Two requests target different banks but share one channel data bus. Activates may overlap, but their data bursts serialize on that bus.

### Example 7

An asymmetric second channel has half the capacity. The common region interleaves; the remainder must decode only to the larger channel.

### Example 8

A byte write changes part of an ECC codeword. The controller merges or masks data and regenerates check symbols rather than preserving obsolete ECC.

### Example 9

Patrol scrub finds a correctable error and rewrites corrected data; repeated errors at the page trigger platform retirement policy rather than silent reuse.

### Example 10

This deterministic geometry model cross-checks capacity, ECC physical overhead and aggregate pin-rate peak.

<!-- bijux-verify: {"id":"memory-organization-model","mode":"run","language":"python","toolchain":"python3","expect":{"exit_code":0,"stdout":"channels=2 ranks=4 banks=128 devices=32 data_capacity_gib=64.00\necc_devices=4 raw_capacity_gib=72.00 usable_capacity_gib=64.00 ecc_overhead_pct=12.50\nper_channel_peak_gbps=38.40 aggregate_peak_gbps=76.80\n"}} -->
```python
channels = 2
ranks_per_channel = 2
data_devices_per_rank = 8
ecc_devices_per_rank = 1
banks_per_device = 32
rows_per_bank = 65_536
columns_per_row = 1_024
device_bits_per_column = 8

ranks = channels * ranks_per_channel
device_bytes = banks_per_device * rows_per_bank * columns_per_row * device_bits_per_column // 8
data_devices = ranks * data_devices_per_rank
ecc_devices = ranks * ecc_devices_per_rank
data_capacity = data_devices * device_bytes
raw_capacity = (data_devices + ecc_devices) * device_bytes
gib = 1024 ** 3

transfers_per_second = 4.8e9
channel_data_bits = 64
per_channel_peak = transfers_per_second * channel_data_bits / 8
aggregate_peak = channels * per_channel_peak

print(f"channels={channels} ranks={ranks} banks={ranks * banks_per_device} devices={data_devices} data_capacity_gib={data_capacity / gib:.2f}")
print(f"ecc_devices={ecc_devices} raw_capacity_gib={raw_capacity / gib:.2f} usable_capacity_gib={data_capacity / gib:.2f} ecc_overhead_pct={100 * (raw_capacity - data_capacity) / data_capacity:.2f}")
print(f"per_channel_peak_gbps={per_channel_peak / 1e9:.2f} aggregate_peak_gbps={aggregate_peak / 1e9:.2f}")
```

The geometry and rate are invented. The column convention is explicit but simplified; real device density must be reconciled with authoritative organization/burst definitions. Pin-rate peak excludes every protocol, refresh, turnaround, queueing and workload loss.

## Cross-Program Connections

- **Digital Design:** PHY lanes, timing training, command decode and ECC datapaths realize the organization.
- **Data Structures:** multidimensional arrays and bijective mappings organize physical locations.
- **Operating Systems:** NUMA placement, hotplug, page retirement and firmware tables expose topology.
- **Distributed Systems:** ownership and failure domains extend from caches across sockets/controllers.
- **Reliability Engineering:** ECC, scrubbing, sparing, mirroring and telemetry manage faults.
- **Security Engineering:** address mapping, row interaction and shared banks create attack surfaces.
- **Performance Engineering:** channel/bank balance, row locality, bandwidth and latency tails quantify use.
- **Formal Methods:** decode bijection, lane alignment and lifecycle invariants prevent aliases/data loss.

## References

1. gem5, [Memory System](https://www.gem5.org/documentation/general_docs/memory_system/), current memory-system modeling, ports and controller context; retrieved 2026-09-04.
2. gem5, [gem5 Standard Library Memory Components](https://www.gem5.org/documentation/general_docs/memory_system/gem5_memory_system/), current channel/component configuration and simulation context; retrieved 2026-09-04.
3. SAFARI Research Group, [Ramulator 2.0](https://github.com/CMU-SAFARI/ramulator2), current modular DRAM simulator/controller framework and reproducibility context; retrieved 2026-09-04.
4. Linux kernel, [EDAC Documentation](https://docs.kernel.org/edac/index.html), current error-detection/correction reporting and memory-controller RAS software context; retrieved 2026-09-04.
5. Micron Technology, [DDR5 SDRAM](https://www.micron.com/products/memory/dram-components/ddr5-sdram), current device/product organization and density context; retrieved 2026-09-04.
6. Sarah L. Harris and David Money Harris, [Digital Design and Computer Architecture: RISC-V Edition Resources](https://pages.hmc.edu/harris/ddca/ddcarv.html), main-memory organization and hierarchy teaching resources; retrieved 2026-09-04.

## Exercises

### Exercise 1

Derive usable/raw capacity and channel width for a specified set of channels, ranks, x4 devices and ECC lanes, cross-checking device density.

### Exercise 2

Design and invert an address mapping for two channels, two ranks, bank groups and banks; test field and capacity boundaries.

### Exercise 3

Compare channel/bank interleaving strategies for sequential, power-of-two stride and random traces, including row locality and queue balance.

### Exercise 4

Extend the executable model with asymmetric population, mirrored memory, reserved ranges and decimal-versus-binary reporting.

### Exercise 5

Write a verification plan for memory organization from schematic/device geometry through controller RTL, firmware discovery, ECC injection and OS-visible topology.

## Answers to the Exercises

### Answer 1

Compute one device's bits from authoritative density, then multiply only unique data devices for usable rank capacity. Multiply ranks/channels actually enabled. Add check/spare devices only to a separately labeled raw physical total. Channel data width is selected data devices times device width; check width is separate.

Cross-check the product using bank/row/column geometry after reconciling burst convention. Report bits/bytes, GB/GiB and ECC overhead denominator. Explain any mirroring, sparing or firmware reservation before claiming OS-usable capacity.

### Answer 2

Allocate byte/beat/column bits, then channel, bank-group, bank, rank and row fields or documented hashes. Implement `decode(address)` and `encode(fields)`; exhaust small configurations and boundary-sample real sizes to prove `encode(decode(a))=a` over populated ranges and rejection of holes.

Test first/last byte, every single field transition, highest row, asymmetric remainder and overflow. For XOR mappings, retain enough independent source bits for inversion and prove no two exposed addresses map to one location.

### Answer 3

Feed identical traces to each mapping and record per-channel/rank/bank request counts, active-row hits/conflicts/empty cases, command/data utilization, queueing and completion latency. Fine channel/bank interleaving often balances sequential lines; unfortunate power-of-two strides can concentrate without hashing; row-oriented mapping may help bursts but reduce parallelism.

Use the same scheduler/timing and report both locality and balance. No mapping dominates every trace, and peak bank count is not achieved bandwidth.

### Answer 4

Represent each channel as explicit populated ranks rather than a uniform multiplier. Build exposed interleaved regions only where peers have matching capacity and map remainders to valid channels. Subtract reserved ranges, apply mirroring as reduced unique capacity and add ECC/spares only to raw installed bits.

Print raw, usable physical-address and post-reservation capacity in bytes, decimal GB and binary GiB. Assert regions neither overlap nor leave unintended aliases and their sum matches the component model.

### Answer 5

Cross-check schematics, module/device identity, density/width/ranks, lanes/swizzles, clocks and supported population. Verify RTL capacity constants, bijective address decode, command/rank selection, masks/ECC codewords, refresh/power/training, errors/retries and order. Exercise first/last/boundary addresses and asymmetric/failed resources.

Compare firmware inventory/ranges/NUMA tables with controller registers and OS topology. Inject correctable/uncorrectable/lane faults under authorization; test scrub, poison, logging and retirement. Measure mapping balance and bandwidth/latency, binding device stepping, modules, controller/PHY RTL, firmware, OS, temperature and errata. Internal evidence is not independent RAS or platform certification.
