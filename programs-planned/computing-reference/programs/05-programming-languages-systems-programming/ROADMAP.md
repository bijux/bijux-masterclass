# 05. Programming Languages: Systems Programming

**Program code:** `SYSP`

**Purpose:** Develop command of low-level software construction where memory, representation, operating-system interfaces, latency, portability, and failure behavior are explicit.

**Level-II professional outcome:** Ready to build and maintain command-line tools, daemons, networking components, storage utilities, runtime components, and performance-sensitive libraries in C, C++, or Rust.

**Prerequisites:** Programming Languages & Semantics Level I; Computer Architecture Level I or equivalent; basic operating-system concepts.

**Primary ownership:** C and Rust systems programming; memory and resource management; Unix/POSIX interfaces; binary representation; process and file APIs; sockets and evented I/O; FFI; debugging and profiling; portable low-level libraries; systems hardening.

**Explicit exclusions:** kernel design and implementation (Program 22); compiler implementation (Program 08); network protocol architecture (Program 24); parallel programming theory (Program 04).

## Level I — Undergraduate Core

Modules 001–050 establish the complete foundational model and canonical mechanisms.

### Block 01 — Machine-Oriented Program Construction

| Module | Canonical chapter | Future file |
|---:|---|---|
| 001 | **From Source Text to Process Image** | `001-from-source-text-to-process-image.md` |
| 002 | **Integer Representation, Overflow, and Conversion** | `002-integer-representation-overflow-and-conversion.md` |
| 003 | **Floating-Point Representation and Exceptional Values** | `003-floating-point-representation-and-exceptional-values.md` |
| 004 | **Pointers, Addresses, and Object Lifetimes** | `004-pointers-addresses-and-object-lifetimes.md` |
| 005 | **Arrays, Pointer Arithmetic, and Bounds** | `005-arrays-pointer-arithmetic-and-bounds.md` |
| 006 | **Structures, Unions, Padding, and Alignment** | `006-structures-unions-padding-and-alignment.md` |
| 007 | **Bitwise Operations and Bit Fields** | `007-bitwise-operations-and-bit-fields.md` |
| 008 | **Endianness and Portable Binary Representation** | `008-endianness-and-portable-binary-representation.md` |
| 009 | **Undefined, Unspecified, and Implementation-Defined Behavior** | `009-undefined-unspecified-and-implementation-defined-behavior.md` |
| 010 | **Reading Generated Assembly to Validate Assumptions** | `010-reading-generated-assembly-to-validate-assumptions.md` |

### Block 02 — Memory and Resource Management

| Module | Canonical chapter | Future file |
|---:|---|---|
| 011 | **Stack Frames and Automatic Storage** | `011-stack-frames-and-automatic-storage.md` |
| 012 | **Heap Allocation and Allocator Interfaces** | `012-heap-allocation-and-allocator-interfaces.md` |
| 013 | **Ownership Conventions in C** | `013-ownership-conventions-in-c.md` |
| 014 | **RAII and Deterministic Resource Management** | `014-raii-and-deterministic-resource-management.md` |
| 015 | **Rust Ownership and Move Semantics** | `015-rust-ownership-and-move-semantics.md` |
| 016 | **Borrowing, Lifetimes, and Alias Control** | `016-borrowing-lifetimes-and-alias-control.md` |
| 017 | **Reference Counting and Shared Ownership** | `017-reference-counting-and-shared-ownership.md` |
| 018 | **Arenas, Pools, and Region Allocation** | `018-arenas-pools-and-region-allocation.md` |
| 019 | **Memory-Mapped Regions** | `019-memory-mapped-regions.md` |
| 020 | **Diagnosing Leaks, Use-After-Free, and Corruption** | `020-diagnosing-leaks-use-after-free-and-corruption.md` |

### Block 03 — Files, Processes, and Unix Interfaces

| Module | Canonical chapter | Future file |
|---:|---|---|
| 021 | **File Descriptors and the Unix I/O Model** | `021-file-descriptors-and-the-unix-i-o-model.md` |
| 022 | **Open, Read, Write, Seek, and Close** | `022-open-read-write-seek-and-close.md` |
| 023 | **Directories, Metadata, and Filesystem Traversal** | `023-directories-metadata-and-filesystem-traversal.md` |
| 024 | **Processes, Fork, Exec, and Exit** | `024-processes-fork-exec-and-exit.md` |
| 025 | **Environment Variables and Process Context** | `025-environment-variables-and-process-context.md` |
| 026 | **Signals and Asynchronous Process Events** | `026-signals-and-asynchronous-process-events.md` |
| 027 | **Pipes and Shell-Style Composition** | `027-pipes-and-shell-style-composition.md` |
| 028 | **Interprocess Communication with Local Sockets** | `028-interprocess-communication-with-local-sockets.md` |
| 029 | **Permissions, Users, Groups, and Privilege** | `029-permissions-users-groups-and-privilege.md` |
| 030 | **Building a Robust Unix Command-Line Utility** | `030-building-a-robust-unix-command-line-utility.md` |

### Block 04 — Libraries, Interfaces, and Build Boundaries

| Module | Canonical chapter | Future file |
|---:|---|---|
| 031 | **Header Files and Translation Units** | `031-header-files-and-translation-units.md` |
| 032 | **Static Libraries and Archive Linking** | `032-static-libraries-and-archive-linking.md` |
| 033 | **Shared Libraries and Dynamic Linking** | `033-shared-libraries-and-dynamic-linking.md` |
| 034 | **Application Binary Interfaces** | `034-application-binary-interfaces.md` |
| 035 | **Symbol Visibility and Versioning** | `035-symbol-visibility-and-versioning.md` |
| 036 | **Foreign-Function Interfaces** | `036-foreign-function-interfaces.md` |
| 037 | **Calling C Safely from Higher-Level Languages** | `037-calling-c-safely-from-higher-level-languages.md` |
| 038 | **Build Graphs and Incremental Compilation** | `038-build-graphs-and-incremental-compilation.md` |
| 039 | **Feature Detection and Conditional Compilation** | `039-feature-detection-and-conditional-compilation.md` |
| 040 | **Designing a Stable Systems-Library Interface** | `040-designing-a-stable-systems-library-interface.md` |

### Block 05 — Diagnostics and Defensive Systems Code

| Module | Canonical chapter | Future file |
|---:|---|---|
| 041 | **Assertions, Contracts, and Defensive Checks** | `041-assertions-contracts-and-defensive-checks.md` |
| 042 | **Error Codes, Errno, and Result Types** | `042-error-codes-errno-and-result-types.md` |
| 043 | **Logging Without Distorting Timing** | `043-logging-without-distorting-timing.md` |
| 044 | **Core Dumps and Postmortem Debugging** | `044-core-dumps-and-postmortem-debugging.md` |
| 045 | **Interactive Debugging with GDB or LLDB** | `045-interactive-debugging-with-gdb-or-lldb.md` |
| 046 | **Memory Sanitizers** | `046-memory-sanitizers.md` |
| 047 | **Undefined-Behavior and Thread Sanitizers** | `047-undefined-behavior-and-thread-sanitizers.md` |
| 048 | **System-Call Tracing** | `048-system-call-tracing.md` |
| 049 | **CPU and Allocation Profiling** | `049-cpu-and-allocation-profiling.md` |
| 050 | **Hardening a Small Native Program** | `050-hardening-a-small-native-program.md` |

## Level II — Graduate and Professional Depth

Modules 051–100 add internals, difficult cases, production constraints, advanced theory, and independent technical judgment.

### Block 06 — Sockets and Event-Driven I/O

| Module | Canonical chapter | Future file |
|---:|---|---|
| 051 | **Socket Creation, Binding, Listening, and Accepting** | `051-socket-creation-binding-listening-and-accepting.md` |
| 052 | **Stream Framing over TCP** | `052-stream-framing-over-tcp.md` |
| 053 | **Datagram Programming over UDP** | `053-datagram-programming-over-udp.md` |
| 054 | **Blocking, Nonblocking, and Timed I/O** | `054-blocking-nonblocking-and-timed-i-o.md` |
| 055 | **I/O Multiplexing with Select and Poll** | `055-i-o-multiplexing-with-select-and-poll.md` |
| 056 | **Scalable Readiness APIs: epoll and kqueue** | `056-scalable-readiness-apis-epoll-and-kqueue.md` |
| 057 | **Asynchronous I/O Interfaces** | `057-asynchronous-i-o-interfaces.md` |
| 058 | **Connection State Machines** | `058-connection-state-machines.md` |
| 059 | **Backpressure and Bounded Buffers** | `059-backpressure-and-bounded-buffers.md` |
| 060 | **Engineering a Production-Grade Network Daemon** | `060-engineering-a-production-grade-network-daemon.md` |

### Block 07 — Storage and Binary Data Engineering

| Module | Canonical chapter | Future file |
|---:|---|---|
| 061 | **Designing Binary File Formats** | `061-designing-binary-file-formats.md` |
| 062 | **Checksums and Corruption Detection** | `062-checksums-and-corruption-detection.md` |
| 063 | **Buffered and Direct I/O** | `063-buffered-and-direct-i-o.md` |
| 064 | **Memory Mapping and Page-Fault Behavior** | `064-memory-mapping-and-page-fault-behavior.md` |
| 065 | **Append-Only Logs** | `065-append-only-logs.md` |
| 066 | **Crash-Consistent File Updates** | `066-crash-consistent-file-updates.md` |
| 067 | **Write-Ahead Logging in User Space** | `067-write-ahead-logging-in-user-space.md` |
| 068 | **Compression and Framing** | `068-compression-and-framing.md` |
| 069 | **Zero-Copy Data Paths** | `069-zero-copy-data-paths.md` |
| 070 | **Building a Recoverable On-Disk Data Component** | `070-building-a-recoverable-on-disk-data-component.md` |

### Block 08 — Advanced Rust and Safe Systems Interfaces

| Module | Canonical chapter | Future file |
|---:|---|---|
| 071 | **Unsafe Rust and Its Proof Obligations** | `071-unsafe-rust-and-its-proof-obligations.md` |
| 072 | **Raw Pointers and Provenance** | `072-raw-pointers-and-provenance.md` |
| 073 | **Pinning and Self-Referential Structures** | `073-pinning-and-self-referential-structures.md` |
| 074 | **Interior Mutability** | `074-interior-mutability.md` |
| 075 | **Send, Sync, and Thread-Safety Contracts** | `075-send-sync-and-thread-safety-contracts.md` |
| 076 | **Custom Smart Pointers** | `076-custom-smart-pointers.md` |
| 077 | **Procedural Boundaries Around Unsafe Code** | `077-procedural-boundaries-around-unsafe-code.md` |
| 078 | **FFI Ownership Across Rust and C** | `078-ffi-ownership-across-rust-and-c.md` |
| 079 | **No-Std and Constrained Environments** | `079-no-std-and-constrained-environments.md` |
| 080 | **Auditing a Safe Abstraction over Unsafe Mechanisms** | `080-auditing-a-safe-abstraction-over-unsafe-mechanisms.md` |

### Block 09 — Portability, Isolation, and Security

| Module | Canonical chapter | Future file |
|---:|---|---|
| 081 | **POSIX Portability and Platform Divergence** | `081-posix-portability-and-platform-divergence.md` |
| 082 | **Windows Systems Interfaces and Handle Semantics** | `082-windows-systems-interfaces-and-handle-semantics.md` |
| 083 | **Cross-Compilation and Target Triples** | `083-cross-compilation-and-target-triples.md` |
| 084 | **Containers, Namespaces, and Process Isolation Interfaces** | `084-containers-namespaces-and-process-isolation-interfaces.md` |
| 085 | **Sandboxing with Seccomp and Capability Restrictions** | `085-sandboxing-with-seccomp-and-capability-restrictions.md` |
| 086 | **Privilege Separation** | `086-privilege-separation.md` |
| 087 | **Secure Temporary Files and Race-Free Filesystem Use** | `087-secure-temporary-files-and-race-free-filesystem-use.md` |
| 088 | **Memory-Safety Mitigations and Control-Flow Protection** | `088-memory-safety-mitigations-and-control-flow-protection.md` |
| 089 | **Fuzzing Native Parsers and Protocol Handlers** | `089-fuzzing-native-parsers-and-protocol-handlers.md` |
| 090 | **Designing a Portable and Least-Privilege Systems Tool** | `090-designing-a-portable-and-least-privilege-systems-tool.md` |

### Block 10 — Production Systems Components

| Module | Canonical chapter | Future file |
|---:|---|---|
| 091 | **Daemon Lifecycle and Service Supervision** | `091-daemon-lifecycle-and-service-supervision.md` |
| 092 | **Configuration Reloading Without Process Restart** | `092-configuration-reloading-without-process-restart.md` |
| 093 | **Graceful Shutdown and Draining** | `093-graceful-shutdown-and-draining.md` |
| 094 | **Resource Limits and Overload Behavior** | `094-resource-limits-and-overload-behavior.md` |
| 095 | **Native Plugin Systems** | `095-native-plugin-systems.md` |
| 096 | **Lock Files, PID Files, and Single-Instance Coordination** | `096-lock-files-pid-files-and-single-instance-coordination.md` |
| 097 | **High-Resolution Timing and Clock Selection** | `097-high-resolution-timing-and-clock-selection.md` |
| 098 | **Low-Latency Logging and Telemetry** | `098-low-latency-logging-and-telemetry.md` |
| 099 | **Packaging, Debug Symbols, and Reproducible Native Builds** | `099-packaging-debug-symbols-and-reproducible-native-builds.md` |
| 100 | **Reviewing a Systems Component for Safety, Failure, and Operability** | `100-reviewing-a-systems-component-for-safety-failure-and-operability.md` |

## Completion standard

This program is complete only when all 100 future module files satisfy `MODULE_CONTENT_CONTRACT.md`. The roadmap itself is not course completion.
