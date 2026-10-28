# 22. Operating Systems

**Program code:** `OS`

**Purpose:** Develop deep command of the abstractions, mechanisms, policies, and implementation trade-offs that mediate hardware resources and application execution.

**Level-II professional outcome:** Ready to work on kernels, runtimes, containers, low-level infrastructure, performance diagnosis, and operating-system-adjacent systems software.

**Prerequisites:** systems programming; computer architecture foundations; concurrency basics; data structures.

**Primary ownership:** kernel architecture; processes and threads; scheduling; synchronization; virtual memory; filesystems; I/O and devices; network stack internals; virtualization and isolation; OS security, observability, and reliability.

**Explicit exclusions:** user-space systems programming practice (Program 05); processor microarchitecture (Program 23); network protocol engineering above OS stack (Program 24).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Kernel Structure and Execution Boundaries

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **Operating-System Goals and Resource Abstractions** | `001-operating-system-goals-and-resource-abstractions.md` |
| 002 | **Privilege Levels and Protection Rings** | `002-privilege-levels-and-protection-rings.md` |
| 003 | **System Calls and User-Kernel Transitions** | `003-system-calls-and-user-kernel-transitions.md` |
| 004 | **Interrupts and Exceptions** | `004-interrupts-and-exceptions.md` |
| 005 | **Kernel Architectures: Monolithic, Microkernel, and Hybrid** | `005-kernel-architectures-monolithic-microkernel-and-hybrid.md` |
| 006 | **Boot Process and Kernel Initialization** | `006-boot-process-and-kernel-initialization.md` |
| 007 | **Kernel Data Structures** | `007-kernel-data-structures.md` |
| 008 | **Kernel Memory Allocation** | `008-kernel-memory-allocation.md` |
| 009 | **Kernel Modules and Drivers** | `009-kernel-modules-and-drivers.md` |
| 010 | **Tracing a Request Across User and Kernel Space** | `010-tracing-a-request-across-user-and-kernel-space.md` |

### Block 02 — Processes, Threads, and Scheduling

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Processes and Address Spaces** | `011-processes-and-address-spaces.md` |
| 012 | **Process Creation and Program Loading** | `012-process-creation-and-program-loading.md` |
| 013 | **Threads and Execution Contexts** | `013-threads-and-execution-contexts.md` |
| 014 | **Context Switching** | `014-context-switching.md` |
| 015 | **Process States and Wait Queues** | `015-process-states-and-wait-queues.md` |
| 016 | **Scheduling Objectives** | `016-scheduling-objectives.md` |
| 017 | **Round-Robin and Priority Scheduling** | `017-round-robin-and-priority-scheduling.md` |
| 018 | **Multilevel Feedback Queues** | `018-multilevel-feedback-queues.md` |
| 019 | **Fair Scheduling** | `019-fair-scheduling.md` |
| 020 | **Measuring Scheduler Latency and Throughput** | `020-measuring-scheduler-latency-and-throughput.md` |

### Block 03 — Synchronization and Interprocess Communication

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **Critical Sections in the Kernel** | `021-critical-sections-in-the-kernel.md` |
| 022 | **Spinlocks and Interrupt Context** | `022-spinlocks-and-interrupt-context.md` |
| 023 | **Mutexes, Semaphores, and Condition Variables** | `023-mutexes-semaphores-and-condition-variables.md` |
| 024 | **Atomic Operations** | `024-atomic-operations.md` |
| 025 | **Deadlock Conditions and Avoidance** | `025-deadlock-conditions-and-avoidance.md` |
| 026 | **Pipes and Byte Streams** | `026-pipes-and-byte-streams.md` |
| 027 | **Shared Memory** | `027-shared-memory.md` |
| 028 | **Signals and Notifications** | `028-signals-and-notifications.md` |
| 029 | **Local Sockets and Message Queues** | `029-local-sockets-and-message-queues.md` |
| 030 | **Designing an IPC Mechanism from Semantics and Cost** | `030-designing-an-ipc-mechanism-from-semantics-and-cost.md` |

### Block 04 — Virtual Memory

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Address Translation** | `031-address-translation.md` |
| 032 | **Page Tables** | `032-page-tables.md` |
| 033 | **Translation Lookaside Buffers** | `033-translation-lookaside-buffers.md` |
| 034 | **Demand Paging** | `034-demand-paging.md` |
| 035 | **Page Faults** | `035-page-faults.md` |
| 036 | **Virtual-Memory Page Replacement** | `036-virtual-memory-page-replacement.md` |
| 037 | **Copy-on-Write** | `037-copy-on-write.md` |
| 038 | **Memory-Mapped Files** | `038-memory-mapped-files.md` |
| 039 | **Shared Pages and Page Cache** | `039-shared-pages-and-page-cache.md` |
| 040 | **Diagnosing Memory Pressure and Thrashing** | `040-diagnosing-memory-pressure-and-thrashing.md` |

### Block 05 — Filesystems and Persistent Storage

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Files, Directories, and Namespaces** | `041-files-directories-and-namespaces.md` |
| 042 | **Inodes and Metadata** | `042-inodes-and-metadata.md` |
| 043 | **File Allocation** | `043-file-allocation.md` |
| 044 | **Filesystem Free-Space Management** | `044-filesystem-free-space-management.md` |
| 045 | **Buffer Cache and Page Cache** | `045-buffer-cache-and-page-cache.md` |
| 046 | **Journaling** | `046-journaling.md` |
| 047 | **Crash Consistency** | `047-crash-consistency.md` |
| 048 | **Filesystem Permissions** | `048-filesystem-permissions.md` |
| 049 | **Virtual Filesystem Layers** | `049-virtual-filesystem-layers.md` |
| 050 | **Tracing File Creation to Stable Storage** | `050-tracing-file-creation-to-stable-storage.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Multiprocessor and NUMA Operating Systems

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Per-CPU State** | `051-per-cpu-state.md` |
| 052 | **SMP Kernel Synchronization** | `052-smp-kernel-synchronization.md` |
| 053 | **Scalable Locking** | `053-scalable-locking.md` |
| 054 | **Kernel Read-Copy-Update** | `054-kernel-read-copy-update.md` |
| 055 | **NUMA Memory Placement** | `055-numa-memory-placement.md` |
| 056 | **Processor Affinity** | `056-processor-affinity.md` |
| 057 | **Load Balancing Across Cores** | `057-load-balancing-across-cores.md` |
| 058 | **Timer and Interrupt Scalability** | `058-timer-and-interrupt-scalability.md` |
| 059 | **TLB Shootdowns** | `059-tlb-shootdowns.md` |
| 060 | **Diagnosing Multiprocessor Kernel Contention** | `060-diagnosing-multiprocessor-kernel-contention.md` |

### Block 07 — Devices, I/O, and Storage Stacks

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Device Discovery and Driver Models** | `061-device-discovery-and-driver-models.md` |
| 062 | **Memory-Mapped and Port-Mapped I/O** | `062-memory-mapped-and-port-mapped-i-o.md` |
| 063 | **Direct Memory Access** | `063-direct-memory-access.md` |
| 064 | **Block and Character Devices** | `064-block-and-character-devices.md` |
| 065 | **I/O Schedulers** | `065-i-o-schedulers.md` |
| 066 | **Asynchronous I/O** | `066-asynchronous-i-o.md` |
| 067 | **Zero-Copy and Kernel Bypass** | `067-zero-copy-and-kernel-bypass.md` |
| 068 | **Storage Queues and NVMe** | `068-storage-queues-and-nvme.md` |
| 069 | **Operating-System Support for Persistent Memory** | `069-operating-system-support-for-persistent-memory.md` |
| 070 | **Designing an I/O Path for Latency or Throughput** | `070-designing-an-i-o-path-for-latency-or-throughput.md` |

### Block 08 — Networking Inside the Operating System

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Socket Layer Architecture** | `071-socket-layer-architecture.md` |
| 072 | **Packet Reception and Transmission** | `072-packet-reception-and-transmission.md` |
| 073 | **Network Buffers** | `073-network-buffers.md` |
| 074 | **Protocol Processing** | `074-protocol-processing.md` |
| 075 | **Routing and Neighbor Tables** | `075-routing-and-neighbor-tables.md` |
| 076 | **Connection State Management** | `076-connection-state-management.md` |
| 077 | **Congestion-Control Hooks** | `077-congestion-control-hooks.md` |
| 078 | **Packet Filtering** | `078-packet-filtering.md` |
| 079 | **Offload and Receive-Side Scaling** | `079-offload-and-receive-side-scaling.md` |
| 080 | **Profiling the Kernel Network Path** | `080-profiling-the-kernel-network-path.md` |

### Block 09 — Virtualization, Containers, and Isolation

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **Trap-and-Emulate Virtualization** | `081-trap-and-emulate-virtualization.md` |
| 082 | **Hardware-Assisted Virtualization** | `082-hardware-assisted-virtualization.md` |
| 083 | **Hypervisor Architectures** | `083-hypervisor-architectures.md` |
| 084 | **Virtual Memory for Guests** | `084-virtual-memory-for-guests.md` |
| 085 | **Virtual Devices and Virtio** | `085-virtual-devices-and-virtio.md` |
| 086 | **Namespaces** | `086-namespaces.md` |
| 087 | **Control Groups** | `087-control-groups.md` |
| 088 | **Container Filesystems** | `088-container-filesystems.md` |
| 089 | **System-Call Filtering and Sandboxing** | `089-system-call-filtering-and-sandboxing.md` |
| 090 | **Comparing Virtual Machines, Containers, and Process Isolation** | `090-comparing-virtual-machines-containers-and-process-isolation.md` |

### Block 10 — Security, Reliability, and Specialized Systems

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Kernel Attack Surfaces** | `091-kernel-attack-surfaces.md` |
| 092 | **Capabilities and Mandatory Access Control** | `092-capabilities-and-mandatory-access-control.md` |
| 093 | **Secure Boot and Measured Boot** | `093-secure-boot-and-measured-boot.md` |
| 094 | **Kernel Memory-Safety Strategies** | `094-kernel-memory-safety-strategies.md` |
| 095 | **Kernel Observability and eBPF** | `095-kernel-observability-and-ebpf.md` |
| 096 | **Crash Dumps and Kernel Debugging** | `096-crash-dumps-and-kernel-debugging.md` |
| 097 | **Real-Time Scheduling** | `097-real-time-scheduling.md` |
| 098 | **Energy-Aware Operating Systems** | `098-energy-aware-operating-systems.md` |
| 099 | **Distributed and Network Operating-System Concepts** | `099-distributed-and-network-operating-system-concepts.md` |
| 100 | **Reviewing an Operating System for Isolation, Performance, and Recoverability** | `100-reviewing-an-operating-system-for-isolation-performance-and-recoverability.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
