# Progress Through the One Hundred Modules

Mark a module only after you have completed its chapter, frozen the workbook predictions, repaired the causal failures, built the independent lab, applied the capstone increment, and reconstructed the model without following the text.

The optional local progress command reads the same module tree:

```bash
make progress
python3 tools/progress.py done 1
```

## Course 1 — Rust Foundations

- [ ] **01. Compilation, Expressions, and Types**
- [ ] **02. Control Flow, Functions, and Invariants**
- [ ] **03. Ownership, Moves, Copying, and Destruction**
- [ ] **04. Borrowing, References, Slices, and Strings**
- [ ] **05. Structs, Enums, Methods, and Pattern Matching**
- [ ] **06. Collections, Iterators, and Closures**
- [ ] **07. Errors, Parsing, Files, and Persistence**
- [ ] **08. Generics, Traits, Conversions, and Lifetime Basics**
- [ ] **09. Crates, Modules, Public APIs, Tests, and Documentation**
- [ ] **10. Integration and Independent Change**

- [ ] **Course 1 capstone:** reconstruct and defend Taskboard without following the engineering guide line by line.
- [ ] **Course 1 transfer:** Add one cross-layer Taskboard feature—such as due dates or labels—without weakening deterministic storage, typed transitions, or failure atomicity.

## Course 2 — Ownership, Lifetimes, and Memory

- [ ] **11. Places, Move Paths, and Advanced Borrowing**
- [ ] **12. Lifetime Relationships and Borrowed APIs**
- [ ] **13. Scoped Access and Escape Prevention**
- [ ] **14. RAII, Drop, Unwinding, and Failure Atomicity**
- [ ] **15. Box, Deref, Dynamically Sized Types, and Cow**
- [ ] **16. Rc, Weak, and Ownership Graphs**
- [ ] **17. Interior Mutability and Runtime Borrows**
- [ ] **18. Memory Representation, Validity, and Layout**
- [ ] **19. Subtyping, Variance, PhantomData, and Drop Checking**
- [ ] **20. Pinning and Address-Sensitive Design**

- [ ] **Course 2 capstone:** reconstruct and defend Memory Workspace without following the engineering guide line by line.
- [ ] **Course 2 transfer:** Add document labels and snapshot comparison to Memory Workspace while preserving stale-handle rejection, bounded retention, and borrowed-view provenance.

## Course 3 — Traits, Generics, and Architectural Design

- [ ] **21. Traits as Behavioral Contracts**
- [ ] **22. Associated Types and Type Families**
- [ ] **23. Coherence and Implementation Ownership**
- [ ] **24. Static Polymorphism and Opaque Types**
- [ ] **25. Trait Objects and Dynamic Polymorphism**
- [ ] **26. Composition and OOP-Style Design Without Inheritance**
- [ ] **27. Typestate and Capability-Oriented APIs**
- [ ] **28. Boundary Traits and Adapters**
- [ ] **29. Public API Evolution**
- [ ] **30. Architectural Synthesis**

- [ ] **Course 3 capstone:** reconstruct and defend Review Engine without following the engineering guide line by line.
- [ ] **Course 3 transfer:** Add a versioned rule capability to Review Engine while preserving source compatibility, deterministic rule order, and a clear static-versus-dynamic boundary.

## Course 4 — Functional Rust

- [ ] **31. Closures, Capture, and Callable Contracts**
- [ ] **32. The Iterator Model**
- [ ] **33. Iterator Algebra and Pipeline Shape**
- [ ] **34. Folds, Scans, and Short-Circuiting**
- [ ] **35. Option, Result, and Fallible Traversal**
- [ ] **36. Custom Iterators and Collection Protocols**
- [ ] **37. Recursive Data and Structural Sharing**
- [ ] **38. Functional Core and Effect Isolation**
- [ ] **39. Combinator Laws and Cost Models**
- [ ] **40. Functional Architecture Synthesis**

- [ ] **Course 4 capstone:** reconstruct and defend LedgerFlow without following the engineering guide line by line.
- [ ] **Course 4 transfer:** Add balance checkpoints to LedgerFlow without introducing a second source of truth for event order or reducer semantics.

## Course 5 — Rust Metaprogramming

- [ ] **41. Metaprogramming Boundaries and the Expansion Model**
- [ ] **42. Declarative Macros: Matchers, Fragments, and Repetition**
- [ ] **43. Recursive Macro Parsing and Token-Tree Techniques**
- [ ] **44. Hygiene, Scope, Paths, and Cross-Crate Macros**
- [ ] **45. Macro Diagnostics, Testing, and Public API Design**
- [ ] **46. Procedural Macro Execution and TokenStream Engineering**
- [ ] **47. Custom Derive Macros and Structural Generation**
- [ ] **48. Attribute Macros and Item Transformation**
- [ ] **49. Function-Like Procedural Macros and Typed DSLs**
- [ ] **50. Build Scripts, Generated Code, and Compile-Time Architecture**

- [ ] **Course 5 capstone:** reconstruct and defend CommandForge without following the engineering guide line by line.
- [ ] **Course 5 transfer:** Add a new CommandForge field policy and command kind, tracing the change through grammar, semantic validation, expansion, runtime behavior, tests, and compatibility.

## Course 6 — Rust Systems Programming

- [ ] **51. Binary Data Contracts: Bytes, Endianness, and Checked Parsing**
- [ ] **52. Files, Durability, and Transactional Replacement**
- [ ] **53. Paths, Names, and Platform Boundaries**
- [ ] **54. Processes, Environments, and Standard Streams**
- [ ] **55. Unsafe Rust as a Proof Boundary**
- [ ] **56. Raw Pointers, Provenance, and Uninitialized Memory**
- [ ] **57. Manual Allocation and Owning Unsafe Abstractions**
- [ ] **58. C FFI: ABI, Strings, Pointers, and Error Boundaries**
- [ ] **59. Foreign Resources, Callbacks, and Wrapper Architecture**
- [ ] **60. Integrated Systems Design, Testing, and Audit**

- [ ] **Course 6 capstone:** reconstruct and defend FrameVault without following the engineering guide line by line.
- [ ] **Course 6 transfer:** Add a bounded archive index to FrameVault while preserving format compatibility, path policy, failure atomicity, allocator safety, and C ABI ownership.

## Course 7 — Rust Concurrency and Parallelism

- [ ] **61. Threads, Schedules, Send, Sync, and Race Freedom**
- [ ] **62. Structured Threads: Scopes, Joins, and Panic Boundaries**
- [ ] **63. Shared State: Locks and Protected Invariants**
- [ ] **64. Coordination: Condvars, Barriers, and Phase Protocols**
- [ ] **65. Message Passing, Backpressure, and Shutdown**
- [ ] **66. Liveness: Deadlock, Cancellation, and Recovery**
- [ ] **67. Atomics, Happens-Before, and Memory Ordering**
- [ ] **68. Lock-Free Protocols, Reclamation, and Unsafe Send/Sync**
- [ ] **69. Rayon, Work Stealing, and Deterministic Parallelism**
- [ ] **70. Integrated Concurrent Architecture, Testing, and Audit**

- [ ] **Course 7 capstone:** reconstruct and defend BatchWeave without following the engineering guide line by line.
- [ ] **Course 7 transfer:** Add bounded retry to BatchWeave while preserving one terminal outcome per source job, fail-fast semantics, queue bounds, and deterministic final reporting.

## Course 8 — Rust Async and Networked Services

- [ ] **71. Futures, Polling, Wakers, and Async State Machines**
- [ ] **72. Tokio Runtimes, Tasks, and Structured Async Lifecycles**
- [ ] **73. Async I/O, Buffers, Streams, and Framing**
- [ ] **74. TCP, UDP, DNS, and Connection Lifecycles**
- [ ] **75. Protocol State Machines, Versioning, and Defensive Parsing**
- [ ] **76. Backpressure, Admission Control, and Fair Work Distribution**
- [ ] **77. Cancellation Safety, Deadlines, and Graceful Shutdown**
- [ ] **78. HTTP Services with Hyper: Requests, Bodies, and Connections**
- [ ] **79. Network Failure, Idempotency, Retries, and Deterministic Testing**
- [ ] **80. Integrated Async Service Architecture, Testing, and Audit**

- [ ] **Course 8 capstone:** reconstruct and defend JobWire without following the engineering guide line by line.
- [ ] **Course 8 transfer:** Add one streaming JobWire operation with an explicit per-stream capacity and cancellation contract while preserving protocol versioning and service shutdown.

## Course 9 — Rust Performance and Production Engineering

- [ ] **81. Performance Contracts, Workloads, and Benchmark Design**
- [ ] **82. CPU Profiling, Cost Models, and Hot-Path Optimization**
- [ ] **83. Allocation, Memory Footprint, and Ownership Cost**
- [ ] **84. Data Movement, Buffering, and Zero-Copy Boundaries**
- [ ] **85. Runtime Efficiency: Contention, Queueing, Batching, and Async Load**
- [ ] **86. Observability: Structured Tracing, Metrics, and Diagnostic Context**
- [ ] **87. Reliability Under Load: SLOs, Load Shedding, Retries, and Degradation**
- [ ] **88. Security and Supply-Chain Engineering**
- [ ] **89. Cargo Profiles, Binary Size, Packaging, CI, and Reproducible Releases**
- [ ] **90. Production Readiness, Capacity Planning, Rollouts, and Incident Learning**

- [ ] **Course 9 capstone:** reconstruct and defend MetricRail without following the engineering guide line by line.
- [ ] **Course 9 transfer:** Add one high-cardinality MetricRail query while preserving bounded memory, deterministic output, observability cardinality, overload behavior, and artifact traceability.

## Course 10 — Advanced Rust Mastery

- [ ] **91. Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen**
- [ ] **92. Advanced Trait Solving: Goals, Projections, and Type Equality**
- [ ] **93. GATs, Higher-Ranked Bounds, and Lending Interfaces**
- [ ] **94. Const Generics, Witness Types, and Compile-Time Invariants**
- [ ] **95. Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries**
- [ ] **96. Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits**
- [ ] **97. From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size**
- [ ] **98. Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration**
- [ ] **99. Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship**
- [ ] **100. Architectural Synthesis: Building and Defending a Long-Lived Rust System**

- [ ] **Course 10 capstone:** reconstruct and defend AxiomStore without following the engineering guide line by line.
- [ ] **Course 10 transfer:** Implement the AXIOM02 format extension without creating a parallel validation or persistence architecture, and defend every compatibility and unsafe consequence.

## Program completion

- [ ] Reconstruct the ten-course progression from memory.
- [ ] Explain one invariant and one rejected shortcut from every capstone.
- [ ] Make an unseen cross-cutting change in a Rust system and preserve ownership, errors, cleanup, determinism, bounds, compatibility, and verification claims.
- [ ] State what remains dependent on a compiler version, target, operating system, foreign caller, workload, or human review.
