# 23. Computer Architecture

**Program code:** `CA`

**Purpose:** Develop command of processor, memory, interconnect, accelerator, and system architecture from instruction-set contracts through microarchitectural performance and energy trade-offs.

**Level-II professional outcome:** Ready to reason about hardware-software performance, contribute to architecture or low-level systems work, and diagnose how software maps onto modern processors and memory systems.

**Prerequisites:** digital logic basics; systems programming; algorithms; basic probability and performance analysis.

**Primary ownership:** digital implementation foundations; instruction-set architecture; datapaths and control; pipelining; caches and virtual memory hardware; out-of-order execution; multicore and coherence; interconnects; accelerators; architecture evaluation and security.

**Explicit exclusions:** operating-system policy and kernel implementation (Program 22); language compiler construction (Program 08); parallel programming techniques (Program 04).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Digital Foundations and Machine Representation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Boolean Logic and Combinational Circuits** | `001-boolean-logic-and-combinational-circuits.md` |
| 002 | **Sequential Logic and State** | `002-sequential-logic-and-state.md` |
| 003 | **Registers, Memories, and Clocking** | `003-registers-memories-and-clocking.md` |
| 004 | **Finite-State Control** | `004-finite-state-control.md` |
| 005 | **Integer Arithmetic Circuits** | `005-integer-arithmetic-circuits.md` |
| 006 | **Floating-Point Hardware** | `006-floating-point-hardware.md` |
| 007 | **Data Representation and Endianness** | `007-data-representation-and-endianness.md` |
| 008 | **Timing, Critical Paths, and Frequency** | `008-timing-critical-paths-and-frequency.md` |
| 009 | **Area, Power, Energy, and Thermal Constraints** | `009-area-power-energy-and-thermal-constraints.md` |
| 010 | **Reading a Simple Processor Block Diagram** | `010-reading-a-simple-processor-block-diagram.md` |

### Block 02 — Instruction-Set Architecture

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **ISA as a Hardware-Software Contract** | `011-isa-as-a-hardware-software-contract.md` |
| 012 | **Registers and Operand Models** | `012-registers-and-operand-models.md` |
| 013 | **Instruction Encoding** | `013-instruction-encoding.md` |
| 014 | **Addressing Modes** | `014-addressing-modes.md` |
| 015 | **Control-Flow Instructions** | `015-control-flow-instructions.md` |
| 016 | **Procedure Calls and Calling Conventions** | `016-procedure-calls-and-calling-conventions.md` |
| 017 | **Exceptions, Interrupts, and Privilege** | `017-exceptions-interrupts-and-privilege.md` |
| 018 | **Atomic Instructions** | `018-atomic-instructions.md` |
| 019 | **Vector and SIMD Extensions** | `019-vector-and-simd-extensions.md` |
| 020 | **Comparing RISC, CISC, and Domain-Specific ISAs** | `020-comparing-risc-cisc-and-domain-specific-isas.md` |

### Block 03 — Datapaths, Control, and Pipelining

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Single-Cycle Datapaths** | `021-single-cycle-datapaths.md` |
| 022 | **Multicycle Datapaths** | `022-multicycle-datapaths.md` |
| 023 | **Hardwired and Microprogrammed Control** | `023-hardwired-and-microprogrammed-control.md` |
| 024 | **Pipeline Stages** | `024-pipeline-stages.md` |
| 025 | **Structural Hazards** | `025-structural-hazards.md` |
| 026 | **Data Hazards and Forwarding** | `026-data-hazards-and-forwarding.md` |
| 027 | **Control Hazards** | `027-control-hazards.md` |
| 028 | **Pipeline Stalls and Flushes** | `028-pipeline-stalls-and-flushes.md` |
| 029 | **Precise Exceptions** | `029-precise-exceptions.md` |
| 030 | **Measuring Pipeline Throughput and Latency** | `030-measuring-pipeline-throughput-and-latency.md` |

### Block 04 — Memory Hierarchy

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Locality and the Memory Wall** | `031-locality-and-the-memory-wall.md` |
| 032 | **Direct-Mapped Caches** | `032-direct-mapped-caches.md` |
| 033 | **Set-Associative Caches** | `033-set-associative-caches.md` |
| 034 | **Cache Replacement and Write Policies** | `034-cache-replacement-and-write-policies.md` |
| 035 | **Multilevel Caches** | `035-multilevel-caches.md` |
| 036 | **Prefetching** | `036-prefetching.md` |
| 037 | **Main-Memory Organization** | `037-main-memory-organization.md` |
| 038 | **DRAM Timing and Controllers** | `038-dram-timing-and-controllers.md` |
| 039 | **TLBs and Hardware Page Walks** | `039-tlbs-and-hardware-page-walks.md` |
| 040 | **Analyzing Cache Misses from an Access Trace** | `040-analyzing-cache-misses-from-an-access-trace.md` |

### Block 05 — I/O, Storage, and System Integration

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Buses and Memory-Mapped I/O** | `041-buses-and-memory-mapped-i-o.md` |
| 042 | **Interrupts and Direct Memory Access** | `042-interrupts-and-direct-memory-access.md` |
| 043 | **PCI Express** | `043-pci-express.md` |
| 044 | **Storage Device Architecture** | `044-storage-device-architecture.md` |
| 045 | **Network Interface Architecture** | `045-network-interface-architecture.md` |
| 046 | **I/O Memory Management Units** | `046-i-o-memory-management-units.md` |
| 047 | **Timers and Platform Controllers** | `047-timers-and-platform-controllers.md` |
| 048 | **Firmware and Boot Interfaces** | `048-firmware-and-boot-interfaces.md` |
| 049 | **System-on-Chip Integration** | `049-system-on-chip-integration.md` |
| 050 | **Tracing Data from Device to Processor Memory** | `050-tracing-data-from-device-to-processor-memory.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Out-of-Order and Speculative Execution

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Instruction-Level Parallelism** | `051-instruction-level-parallelism.md` |
| 052 | **Register Renaming** | `052-register-renaming.md` |
| 053 | **Reservation Stations** | `053-reservation-stations.md` |
| 054 | **Reorder Buffers** | `054-reorder-buffers.md` |
| 055 | **Dynamic Scheduling** | `055-dynamic-scheduling.md` |
| 056 | **Branch Prediction** | `056-branch-prediction.md` |
| 057 | **Speculative Execution** | `057-speculative-execution.md` |
| 058 | **Load-Store Queues** | `058-load-store-queues.md` |
| 059 | **Memory Disambiguation** | `059-memory-disambiguation.md` |
| 060 | **Analyzing an Out-of-Order Pipeline Bottleneck** | `060-analyzing-an-out-of-order-pipeline-bottleneck.md` |

### Block 07 — Multicore, Coherence, and Consistency

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Shared-Memory Multiprocessors** | `061-shared-memory-multiprocessors.md` |
| 062 | **Cache-Coherence Problems** | `062-cache-coherence-problems.md` |
| 063 | **Snooping Protocols** | `063-snooping-protocols.md` |
| 064 | **Directory-Based Coherence** | `064-directory-based-coherence.md` |
| 065 | **MESI-Family Protocols** | `065-mesi-family-protocols.md` |
| 066 | **Memory Consistency Models** | `066-memory-consistency-models.md` |
| 067 | **Coherence Traffic and False Sharing** | `067-coherence-traffic-and-false-sharing.md` |
| 068 | **Multicore Interconnects** | `068-multicore-interconnects.md` |
| 069 | **Manycore Scalability** | `069-manycore-scalability.md` |
| 070 | **Relating Language Memory Models to Hardware Behavior** | `070-relating-language-memory-models-to-hardware-behavior.md` |

### Block 08 — Parallel and Specialized Architectures

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Vector Processors** | `071-vector-processors.md` |
| 072 | **SIMT GPU Architecture** | `072-simt-gpu-architecture.md` |
| 073 | **GPU Memory and Scheduling** | `073-gpu-memory-and-scheduling.md` |
| 074 | **Tensor and Matrix Accelerators** | `074-tensor-and-matrix-accelerators.md` |
| 075 | **Dataflow Architectures** | `075-dataflow-architectures.md` |
| 076 | **Reconfigurable Computing and FPGAs** | `076-reconfigurable-computing-and-fpgas.md` |
| 077 | **Near-Memory and In-Memory Computing** | `077-near-memory-and-in-memory-computing.md` |
| 078 | **Neuromorphic Architecture Concepts** | `078-neuromorphic-architecture-concepts.md` |
| 079 | **Domain-Specific Architecture Co-Design** | `079-domain-specific-architecture-co-design.md` |
| 080 | **Evaluating an Accelerator Against a General-Purpose Processor** | `080-evaluating-an-accelerator-against-a-general-purpose-processor.md` |

### Block 09 — Datacenter, Memory, and Interconnect Evolution

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **NUMA Systems** | `081-numa-systems.md` |
| 082 | **Chiplet Architectures** | `082-chiplet-architectures.md` |
| 083 | **On-Chip Networks** | `083-on-chip-networks.md` |
| 084 | **High-Speed Memory Technologies** | `084-high-speed-memory-technologies.md` |
| 085 | **Persistent-Memory Architecture** | `085-persistent-memory-architecture.md` |
| 086 | **CXL and Memory Disaggregation** | `086-cxl-and-memory-disaggregation.md` |
| 087 | **SmartNICs and Data-Processing Units** | `087-smartnics-and-data-processing-units.md` |
| 088 | **Rack-Scale and Warehouse-Scale Architecture** | `088-rack-scale-and-warehouse-scale-architecture.md` |
| 089 | **Energy-Proportional Computing** | `089-energy-proportional-computing.md` |
| 090 | **Mapping a Distributed Service onto Datacenter Hardware** | `090-mapping-a-distributed-service-onto-datacenter-hardware.md` |

### Block 10 — Architecture Evaluation, Security, and Reliability

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Benchmark Suites and Workload Selection** | `091-benchmark-suites-and-workload-selection.md` |
| 092 | **Cycles per Instruction and Performance Counters** | `092-cycles-per-instruction-and-performance-counters.md` |
| 093 | **Analytical and Simulation Models** | `093-analytical-and-simulation-models.md` |
| 094 | **Power and Energy Measurement** | `094-power-and-energy-measurement.md` |
| 095 | **Reliability, Faults, and Error Correction** | `095-reliability-faults-and-error-correction.md` |
| 096 | **Side Channels from Caches and Speculation** | `096-side-channels-from-caches-and-speculation.md` |
| 097 | **Transient-Execution Vulnerabilities** | `097-transient-execution-vulnerabilities.md` |
| 098 | **Hardware Trusted Execution Environments** | `098-hardware-trusted-execution-environments.md` |
| 099 | **Hardware Support for Memory Safety** | `099-hardware-support-for-memory-safety.md` |
| 100 | **Conducting a Quantitative Architecture Trade-Off Review** | `100-conducting-a-quantitative-architecture-trade-off-review.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
