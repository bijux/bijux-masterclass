# Rust Programming Course Map

The ninety modules form one sequence. The number identifies the intellectual position, not merely the folder. Each course assumes the prior capstones and reasoning records.

```text
values → resources → contracts → dataflow → generation
       → systems boundaries → concurrency → async services
       → performance and production operation
```

## Course responsibilities

| Course | Modules | Governing question | Capstone |
|---:|---:|---|---|
| 1 | 1–10 | How do values, types, ownership, failure, and program structure form a complete safe Rust program? | **Taskboard** |
| 2 | 11–20 | How do permissions, provenance, cleanup, sharing, representation, variance, and address sensitivity shape memory-safe APIs? | **Memory Workspace** |
| 3 | 21–30 | How do types promise lawful behavior, vary statically or dynamically, compose, encode protocols, and evolve? | **Review Engine** |
| 4 | 31–40 | How do capture, lazy traversal, fallibility, accumulation, structural sharing, effects, and cost form explicit dataflow? | **LedgerFlow** |
| 5 | 41–50 | Which compile-time declaration should own generated syntax, diagnostics, metadata, and build data? | **CommandForge** |
| 6 | 51–60 | How do bytes, filesystems, processes, allocation, unsafe code, C ABIs, callbacks, and foreign resources cross safe boundaries? | **FrameVault** |
| 7 | 61–70 | Which facts remain true across legal thread schedules, synchronization, cancellation, failure, and parallel work distribution? | **BatchWeave** |
| 8 | 71–80 | How do futures, tasks, framing, protocols, backpressure, deadlines, retries, and shutdown behave with remote peers? | **JobWire** |
| 9 | 81–90 | How do measurement, performance, memory, observability, reliability, security, release engineering, and operation make the product defensible? | **MetricRail** |

## The ninety modules

Read the sequence vertically. Each module names one governing question and one place where the cumulative capstone must become more mature. The course boundary changes the dominant lens, but earlier ownership, error, cleanup, and boundedness contracts remain active.

## Course 1 — Rust Foundations

1. [Compilation, Expressions, and Types](01-rust-foundations/course-book/module-01-compilation-expressions-and-types/index.md)
2. [Control Flow, Functions, and Invariants](01-rust-foundations/course-book/module-02-control-flow-functions-and-invariants/index.md)
3. [Ownership, Moves, Copying, and Destruction](01-rust-foundations/course-book/module-03-ownership-moves-copying-and-destruction/index.md)
4. [Borrowing, References, Slices, and Strings](01-rust-foundations/course-book/module-04-borrowing-references-slices-and-strings/index.md)
5. [Structs, Enums, Methods, and Pattern Matching](01-rust-foundations/course-book/module-05-structs-enums-methods-and-pattern-matching/index.md)
6. [Collections, Iterators, and Closures](01-rust-foundations/course-book/module-06-collections-iterators-and-closures/index.md)
7. [Errors, Parsing, Files, and Persistence](01-rust-foundations/course-book/module-07-errors-parsing-files-and-persistence/index.md)
8. [Generics, Traits, Conversions, and Lifetime Basics](01-rust-foundations/course-book/module-08-generics-traits-conversions-and-lifetime-basics/index.md)
9. [Crates, Modules, Public APIs, Tests, and Documentation](01-rust-foundations/course-book/module-09-crates-modules-public-apis-tests-and-documentation/index.md)
10. [Integration and Independent Change](01-rust-foundations/course-book/module-10-integration-and-independent-change/index.md)

Continue through the **Taskboard** engineering guide before the course final review.

## Course 2 — Ownership, Lifetimes, and Memory

11. [Places, Move Paths, and Advanced Borrowing](02-rust-ownership-lifetimes-memory/course-book/module-11-places-move-paths-and-advanced-borrowing/index.md)
12. [Lifetime Relationships and Borrowed APIs](02-rust-ownership-lifetimes-memory/course-book/module-12-lifetime-relationships-and-borrowed-apis/index.md)
13. [Scoped Access and Escape Prevention](02-rust-ownership-lifetimes-memory/course-book/module-13-scoped-access-and-escape-prevention/index.md)
14. [RAII, Drop, Unwinding, and Failure Atomicity](02-rust-ownership-lifetimes-memory/course-book/module-14-raii-drop-unwinding-and-failure-atomicity/index.md)
15. [Box, Deref, Dynamically Sized Types, and Cow](02-rust-ownership-lifetimes-memory/course-book/module-15-box-deref-dynamically-sized-types-and-cow/index.md)
16. [Rc, Weak, and Ownership Graphs](02-rust-ownership-lifetimes-memory/course-book/module-16-rc-weak-and-ownership-graphs/index.md)
17. [Interior Mutability and Runtime Borrows](02-rust-ownership-lifetimes-memory/course-book/module-17-interior-mutability-and-runtime-borrows/index.md)
18. [Memory Representation, Validity, and Layout](02-rust-ownership-lifetimes-memory/course-book/module-18-memory-representation-validity-and-layout/index.md)
19. [Subtyping, Variance, PhantomData, and Drop Checking](02-rust-ownership-lifetimes-memory/course-book/module-19-subtyping-variance-phantomdata-and-drop-checking/index.md)
20. [Pinning and Address-Sensitive Design](02-rust-ownership-lifetimes-memory/course-book/module-20-pinning-and-address-sensitive-design/index.md)

Continue through the **Memory Workspace** engineering guide before the course final review.

## Course 3 — Traits, Generics, and Architectural Design

21. [Traits as Behavioral Contracts](03-rust-traits-generics-architectural-design/course-book/module-21-traits-as-behavioral-contracts/index.md)
22. [Associated Types and Type Families](03-rust-traits-generics-architectural-design/course-book/module-22-associated-types-and-type-families/index.md)
23. [Coherence and Implementation Ownership](03-rust-traits-generics-architectural-design/course-book/module-23-coherence-and-implementation-ownership/index.md)
24. [Static Polymorphism and Opaque Types](03-rust-traits-generics-architectural-design/course-book/module-24-static-polymorphism-and-opaque-types/index.md)
25. [Trait Objects and Dynamic Polymorphism](03-rust-traits-generics-architectural-design/course-book/module-25-trait-objects-and-dynamic-polymorphism/index.md)
26. [Composition and OOP-Style Design Without Inheritance](03-rust-traits-generics-architectural-design/course-book/module-26-composition-and-oop-style-design-without-inheritance/index.md)
27. [Typestate and Capability-Oriented APIs](03-rust-traits-generics-architectural-design/course-book/module-27-typestate-and-capability-oriented-apis/index.md)
28. [Boundary Traits and Adapters](03-rust-traits-generics-architectural-design/course-book/module-28-boundary-traits-and-adapters/index.md)
29. [Public API Evolution](03-rust-traits-generics-architectural-design/course-book/module-29-public-api-evolution/index.md)
30. [Architectural Synthesis](03-rust-traits-generics-architectural-design/course-book/module-30-architectural-synthesis/index.md)

Continue through the **Review Engine** engineering guide before the course final review.

## Course 4 — Functional Rust

31. [Closures, Capture, and Callable Contracts](04-rust-functional-programming/course-book/module-31-closures-capture-and-callable-contracts/index.md)
32. [The Iterator Model](04-rust-functional-programming/course-book/module-32-the-iterator-model/index.md)
33. [Iterator Algebra and Pipeline Shape](04-rust-functional-programming/course-book/module-33-iterator-algebra-and-pipeline-shape/index.md)
34. [Folds, Scans, and Short-Circuiting](04-rust-functional-programming/course-book/module-34-folds-scans-and-short-circuiting/index.md)
35. [Option, Result, and Fallible Traversal](04-rust-functional-programming/course-book/module-35-option-result-and-fallible-traversal/index.md)
36. [Custom Iterators and Collection Protocols](04-rust-functional-programming/course-book/module-36-custom-iterators-and-collection-protocols/index.md)
37. [Recursive Data and Structural Sharing](04-rust-functional-programming/course-book/module-37-recursive-data-and-structural-sharing/index.md)
38. [Functional Core and Effect Isolation](04-rust-functional-programming/course-book/module-38-functional-core-and-effect-isolation/index.md)
39. [Combinator Laws and Cost Models](04-rust-functional-programming/course-book/module-39-combinator-laws-and-cost-models/index.md)
40. [Functional Architecture Synthesis](04-rust-functional-programming/course-book/module-40-functional-architecture-synthesis/index.md)

Continue through the **LedgerFlow** engineering guide before the course final review.

## Course 5 — Rust Metaprogramming

41. [Metaprogramming Boundaries and the Expansion Model](05-rust-metaprogramming/course-book/module-41-metaprogramming-boundaries-and-expansion-model/index.md)
42. [Declarative Macros: Matchers, Fragments, and Repetition](05-rust-metaprogramming/course-book/module-42-declarative-macros-matchers-fragments-and-repetition/index.md)
43. [Recursive Macro Parsing and Token-Tree Techniques](05-rust-metaprogramming/course-book/module-43-recursive-macro-parsing-and-token-tree-techniques/index.md)
44. [Hygiene, Scope, Paths, and Cross-Crate Macros](05-rust-metaprogramming/course-book/module-44-hygiene-scope-paths-and-cross-crate-macros/index.md)
45. [Macro Diagnostics, Testing, and Public API Design](05-rust-metaprogramming/course-book/module-45-macro-diagnostics-testing-and-public-api-design/index.md)
46. [Procedural Macro Execution and TokenStream Engineering](05-rust-metaprogramming/course-book/module-46-procedural-macro-execution-and-tokenstream-engineering/index.md)
47. [Custom Derive Macros and Structural Generation](05-rust-metaprogramming/course-book/module-47-custom-derive-macros-and-structural-generation/index.md)
48. [Attribute Macros and Item Transformation](05-rust-metaprogramming/course-book/module-48-attribute-macros-and-item-transformation/index.md)
49. [Function-Like Procedural Macros and Typed DSLs](05-rust-metaprogramming/course-book/module-49-function-like-procedural-macros-and-typed-dsls/index.md)
50. [Build Scripts, Generated Code, and Compile-Time Architecture](05-rust-metaprogramming/course-book/module-50-build-scripts-generated-code-and-compile-time-architecture/index.md)

Continue through the **CommandForge** engineering guide before the course final review.

## Course 6 — Rust Systems Programming

51. [Binary Data Contracts: Bytes, Endianness, and Checked Parsing](06-rust-systems-programming/course-book/module-51-binary-data-contracts/index.md)
52. [Files, Durability, and Transactional Replacement](06-rust-systems-programming/course-book/module-52-files-durability-and-transactional-replacement/index.md)
53. [Paths, Names, and Platform Boundaries](06-rust-systems-programming/course-book/module-53-paths-names-and-platform-boundaries/index.md)
54. [Processes, Environments, and Standard Streams](06-rust-systems-programming/course-book/module-54-processes-environments-and-standard-streams/index.md)
55. [Unsafe Rust as a Proof Boundary](06-rust-systems-programming/course-book/module-55-unsafe-rust-and-safety-proofs/index.md)
56. [Raw Pointers, Provenance, and Uninitialized Memory](06-rust-systems-programming/course-book/module-56-raw-pointers-provenance-and-uninitialized-memory/index.md)
57. [Manual Allocation and Owning Unsafe Abstractions](06-rust-systems-programming/course-book/module-57-manual-allocation-and-owning-unsafe-abstractions/index.md)
58. [C FFI: ABI, Strings, Pointers, and Error Boundaries](06-rust-systems-programming/course-book/module-58-c-ffi-abi-strings-and-error-boundaries/index.md)
59. [Foreign Resources, Callbacks, and Wrapper Architecture](06-rust-systems-programming/course-book/module-59-foreign-resources-callbacks-and-wrapper-architecture/index.md)
60. [Integrated Systems Design, Testing, and Audit](06-rust-systems-programming/course-book/module-60-integrated-systems-design-and-audit/index.md)

Continue through the **FrameVault** engineering guide before the course final review.

## Course 7 — Rust Concurrency and Parallelism

61. [Module 61: Threads, Schedules, Send, Sync, and Race Freedom](07-rust-concurrency-parallelism/course-book/module-61-threads-schedules-send-sync-and-race-freedom/index.md)
62. [Module 62: Structured Threads: Scopes, Joins, and Panic Boundaries](07-rust-concurrency-parallelism/course-book/module-62-structured-threads-scopes-joins-and-panic-boundaries/index.md)
63. [Module 63: Shared State: Locks and Protected Invariants](07-rust-concurrency-parallelism/course-book/module-63-shared-state-locks-and-protected-invariants/index.md)
64. [Module 64: Coordination: Condvars, Barriers, and Phase Protocols](07-rust-concurrency-parallelism/course-book/module-64-coordination-condvars-barriers-and-phase-protocols/index.md)
65. [Module 65: Message Passing, Backpressure, and Shutdown](07-rust-concurrency-parallelism/course-book/module-65-message-passing-backpressure-and-shutdown/index.md)
66. [Module 66: Liveness: Deadlock, Cancellation, and Recovery](07-rust-concurrency-parallelism/course-book/module-66-liveness-deadlock-cancellation-and-recovery/index.md)
67. [Module 67: Atomics, Happens-Before, and Memory Ordering](07-rust-concurrency-parallelism/course-book/module-67-atomics-happens-before-and-memory-ordering/index.md)
68. [Module 68: Lock-Free Protocols, Reclamation, and Unsafe Send/Sync](07-rust-concurrency-parallelism/course-book/module-68-lock-free-protocols-reclamation-and-unsafe-send-sync/index.md)
69. [Module 69: Rayon, Work Stealing, and Deterministic Parallelism](07-rust-concurrency-parallelism/course-book/module-69-rayon-work-stealing-and-deterministic-parallelism/index.md)
70. [Module 70: Integrated Concurrent Architecture, Testing, and Audit](07-rust-concurrency-parallelism/course-book/module-70-integrated-concurrent-architecture-testing-and-audit/index.md)

Continue through the **BatchWeave** engineering guide before the course final review.

## Course 8 — Rust Async and Networked Services

71. [Module 71: Futures, Polling, Wakers, and Async State Machines](08-rust-async-networked-services/course-book/module-71-futures-polling-wakers-and-async-state-machines/index.md)
72. [Module 72: Tokio Runtimes, Tasks, and Structured Async Lifecycles](08-rust-async-networked-services/course-book/module-72-tokio-runtimes-tasks-and-structured-async-lifecycles/index.md)
73. [Module 73: Async I/O, Buffers, Streams, and Framing](08-rust-async-networked-services/course-book/module-73-async-io-buffers-streams-and-framing/index.md)
74. [Module 74: TCP, UDP, DNS, and Connection Lifecycles](08-rust-async-networked-services/course-book/module-74-tcp-udp-dns-and-connection-lifecycles/index.md)
75. [Module 75: Protocol State Machines, Versioning, and Defensive Parsing](08-rust-async-networked-services/course-book/module-75-protocol-state-machines-versioning-and-defensive-parsing/index.md)
76. [Module 76: Backpressure, Admission Control, and Fair Work Distribution](08-rust-async-networked-services/course-book/module-76-backpressure-admission-control-and-fair-work-distribution/index.md)
77. [Module 77: Cancellation Safety, Deadlines, and Graceful Shutdown](08-rust-async-networked-services/course-book/module-77-cancellation-safety-deadlines-and-graceful-shutdown/index.md)
78. [Module 78: HTTP Services with Hyper: Requests, Bodies, and Connections](08-rust-async-networked-services/course-book/module-78-http-services-with-hyper-requests-bodies-and-connections/index.md)
79. [Module 79: Network Failure, Idempotency, Retries, and Deterministic Testing](08-rust-async-networked-services/course-book/module-79-network-failure-idempotency-retries-and-deterministic-testing/index.md)
80. [Module 80: Integrated Async Service Architecture, Testing, and Audit](08-rust-async-networked-services/course-book/module-80-integrated-async-service-architecture-testing-and-audit/index.md)

Continue through the **JobWire** engineering guide before the course final review.

## Course 9 — Rust Performance and Production Engineering

81. [Performance Contracts, Workloads, and Benchmark Design](09-rust-performance-production-engineering/course-book/module-81-performance-contracts-workloads-and-benchmark-design/index.md)
82. [CPU Profiling, Cost Models, and Hot-Path Optimization](09-rust-performance-production-engineering/course-book/module-82-cpu-profiling-cost-models-and-hot-path-optimization/index.md)
83. [Allocation, Memory Footprint, and Ownership Cost](09-rust-performance-production-engineering/course-book/module-83-allocation-memory-footprint-and-ownership-cost/index.md)
84. [Data Movement, Buffering, and Zero-Copy Boundaries](09-rust-performance-production-engineering/course-book/module-84-data-movement-buffering-and-zero-copy-boundaries/index.md)
85. [Runtime Efficiency: Contention, Queueing, Batching, and Async Load](09-rust-performance-production-engineering/course-book/module-85-runtime-efficiency-contention-queueing-batching-and-async-load/index.md)
86. [Observability: Structured Tracing, Metrics, and Diagnostic Context](09-rust-performance-production-engineering/course-book/module-86-observability-structured-tracing-metrics-and-diagnostic-context/index.md)
87. [Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation](09-rust-performance-production-engineering/course-book/module-87-reliability-under-load-slos-load-shedding-retries-and-degradation/index.md)
88. [Security and Supply-Chain Engineering](09-rust-performance-production-engineering/course-book/module-88-security-and-supply-chain-engineering/index.md)
89. [Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases](09-rust-performance-production-engineering/course-book/module-89-cargo-profiles-binary-size-packaging-ci-and-reproducible-releases/index.md)
90. [Production Readiness, Capacity Planning, Rollouts, and Incident Learning](09-rust-performance-production-engineering/course-book/module-90-production-readiness-capacity-planning-rollouts-and-incident-learning/index.md)

Continue through the **MetricRail** engineering guide before the course final review.

## How to read dependencies

A later course may use an earlier mechanism without reteaching it. When a chapter uses an unfamiliar mechanism, follow the linked prerequisite rather than searching randomly. The progression revisits ideas at higher responsibility:

- ownership begins as move and borrow behavior, then becomes liveness, architecture, async state, and retained-memory cost;
- errors begin as `Result`, then become protocol, FFI, concurrency, retry, and service-objective policy;
- performance begins as algorithmic awareness, then becomes profiling, saturation, artifact configuration, and capacity planning;
- testing begins as behavior checks, then expands to compiler cases, schedule control, hostile input, load, security, release, and rollback exercises.
