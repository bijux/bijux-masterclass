# Skill Map — How Responsibility Grows

Each course adds a new design responsibility while retaining the earlier ones. The tables below are useful both for placement and for deciding which earlier model to revisit when a later design becomes unclear.

## Program-level progression

| Course | Primary responsibility | You finish able to… |
|---:|---|---|
| 1 | Values, Ownership, Errors, and Complete Programs | How do Rust’s types, ownership rules, state models, and error boundaries combine into a complete program you can explain end to end? |
| 2 | Provenance, Resource Protocols, and Address-Sensitive Design | How do places, loans, lifetimes, destruction, shared liveness, representation, and address stability determine whether a memory design is valid? |
| 3 | Behavioral Contracts, Variation, and Evolvable APIs | How should a Rust architecture represent shared behavior, type relationships, runtime variation, protocol states, and downstream extension without importing an inheritance model? |
| 4 | Closures, Iterators, Fallible Dataflow, and Effect Isolation | How can Rust make capture, traversal, cardinality, ordering, failure, accumulation, structural sharing, effects, and cost visible in one dataflow? |
| 5 | Declarative Macros, Procedural Macros, DSLs, and Build-Time Authority | Which facts deserve one compile-time source of truth, which generation mechanism is the least powerful adequate choice, and how can expanded code remain diagnosable ordinary Rust? |
| 6 | Bytes, Operating-System Boundaries, Unsafe Abstractions, and FFI | What does each external boundary promise, which facts can Rust verify, which facts require a manual proof, and how does a safe interface contain those obligations? |
| 7 | Threads, Coordination, Atomics, and Deterministic Work Distribution | Which facts remain true across every legal thread schedule, and what ownership, synchronization, progress, failure, and normalization arguments make those facts reviewable? |
| 8 | Futures, Tokio, Protocols, and Resilient Service Lifecycles | How do suspension, wakeup, task ownership, framing, protocol state, capacity, cancellation, retry, and shutdown remain explicit when peers and timing are only partly observable? |
| 9 | Measurement, Efficiency, Observability, Security, and Delivery | Which measurements, resource bounds, signals, security controls, artifact records, and operating policies make a Rust system defensible under representative load? |
| 10 | Compiler Reasoning, Type Architecture, Soundness, and Long-Lived Systems | How do you design and evolve a Rust system whose type relationships, unsafe boundaries, compiler behavior, compatibility promises, verification evidence, and operating limits survive independent change? |

## Course 1 — Rust Foundations

**Entry:** You should already understand variables, conditions, loops, functions, and collections in at least one programming language. No systems-programming or memory-management background is assumed.

**Primary role:** Course 1 makes ordinary Rust legible. It teaches you to read expressions as typed values, track ownership deliberately, model states with data types, treat failures as part of the interface, and finish a small program whose behavior is protected at several boundaries.

**Scope boundary:** The course stays in safe Rust and mostly in the standard library. It introduces the ownership, trait, iterator, lifetime, module, and testing vocabulary required by later courses, but it does not yet pursue advanced lifetime algebra, smart-pointer architecture, unsafe code, concurrency, async runtimes, or macro construction.

**Reasoning record:** type trace, ownership ledger, state-transition table, error map, and public-boundary map.

### Course 1 module outcomes

| Module | You should be able to… |
|---:|---|
| 1 | Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”. |
| 2 | Treat if and loop constructs as typed expressions and prove branch agreement and loop result behavior. |
| 3 | Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger. |
| 4 | Model shared and mutable references as permissions constrained by aliasing and validity. |
| 5 | Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity. |
| 6 | Use Vec, slices, and HashMap with explicit length, capacity, invalidation, lookup, and ordering assumptions. |
| 7 | Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values. |
| 8 | Write generic functions and types whose bounds correspond to operations actually performed. |
| 9 | Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type. |
| 10 | Trace a behavioral change through grammar, types, domain rules, persistence, rendering, tests, and documentation. |

**Exit construction:** Build a small persistent inventory program from a behavioral contract. It must use typed states, contextual errors, deterministic storage, a library/binary split, and tests that protect both successful and failing behavior.

**Next handoff:** Course 2 returns to ownership at a deeper level: places, loans, lifetimes, destruction, shared liveness, representation, variance, and pinning.

## Course 2 — Ownership, Lifetimes, and Memory

**Entry:** You should be able to build and test a complete safe-Rust program, explain moves and ordinary borrows, use structs and enums, propagate errors, and organize a library and binary.

**Primary role:** Course 2 turns the ownership rules from Course 1 into a design language for memory. You learn to derive borrow relationships, reason about cleanup and unwinding, choose smart pointers by liveness topology, use interior mutability without hiding reentrancy hazards, and distinguish semantic guarantees from layout observations.

**Scope boundary:** The course remains centered on safe public APIs. It explains the memory obligations behind smart pointers, interior mutability, layout, variance, and pinning, but manual allocation, raw-pointer implementation, FFI, threads, and async execution remain later responsibilities.

**Reasoning record:** place and move-path map, loan graph, lifetime relation, destruction trace, liveness graph, representation table, and pinning contract.

### Course 2 module outcomes

| Module | You should be able to… |
|---:|---|
| 11 | Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations. |
| 12 | Translate lifetime syntax into constraints among borrows rather than durations attached to values. |
| 13 | Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation. |
| 14 | Derive local, field, tuple, temporary, and scope destruction order from documented rules. |
| 15 | Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership. |
| 16 | Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts. |
| 17 | Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs. |
| 18 | Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation. |
| 19 | State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally. |
| 20 | Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants. |

**Exit construction:** Build a revisioned record store with borrowed queries, generational identity, a staged mutation protocol, shared immutable snapshots, and a written liveness and cleanup analysis.

**Next handoff:** Course 3 asks how several types can promise lawful behavior and how those contracts shape an architecture that can vary and evolve.

## Course 3 — Traits, Generics, and Architectural Design

**Entry:** You should be comfortable with ownership and borrowing, trait basics, generic functions, lifetime annotations, smart-pointer liveness, and private invariant-bearing types.

**Primary role:** Course 3 turns traits and generics into architectural tools rather than syntax exercises. It teaches contracts and laws, associated type families, coherence, static and dynamic dispatch, composition, typestate, adapters, and compatibility-aware public APIs.

**Scope boundary:** The course focuses on behavioral and architectural variation. It deliberately postpones iterator-centered functional architecture, macro generation, unsafe systems boundaries, and concurrent execution.

**Reasoning record:** trait-law table, associated-type relationship map, coherence ownership map, dispatch map, typestate transition graph, adapter boundary, and compatibility matrix.

### Course 3 module outcomes

| Module | You should be able to… |
|---:|---|
| 21 | Define a trait whose methods express a coherent behavioral contract. |
| 22 | Choose between generic parameters and associated types from relationship cardinality. |
| 23 | Predict whether an implementation satisfies coherence and orphan rules. |
| 24 | Design generic functions and types with the weakest sufficient bounds. |
| 25 | Derive whether a trait is dyn-compatible and repair it without erasing its meaning. |
| 26 | Model encapsulation, substitution, and delegation without class inheritance. |
| 27 | Encode a finite protocol with marker states and consuming transitions. |
| 28 | Design extension traits, closure adapters, and conversion boundaries with precise contracts. |
| 29 | Classify public trait changes by downstream source-compatibility risk. |
| 30 | Map axes of variation before selecting polymorphism mechanisms. |

**Exit construction:** Build a plugin-capable inspection service with one static pipeline, one dynamic registry, a typestate builder, reusable contract tests, and a written compatibility policy.

**Next handoff:** Course 4 keeps these contracts but asks how values, failure, demand, and effects compose through closures, iterators, reductions, and persistent transformations.

## Course 4 — Functional Rust

**Entry:** You should be able to design trait boundaries, use static and dynamic dispatch, understand ownership through collections, and model state explicitly.

**Primary role:** Course 4 develops a functional style that remains honest about ownership and mutation. You learn to derive closure capabilities, read iterator pipelines as state machines, choose reductions and short-circuiting deliberately, compose fallible traversal, implement custom iteration, and isolate effects around a deterministic core.

**Scope boundary:** The course uses ordinary functions, closures, iterators, and immutable public models. It does not treat mutation as forbidden, and it postpones macro construction, parallel iteration, async streams, and benchmark-driven optimization.

**Reasoning record:** capture map, iterator stage table, cardinality and order trace, failure-policy matrix, accumulator invariant, structural-sharing graph, effect boundary, and qualitative cost model.

### Course 4 module outcomes

| Module | You should be able to… |
|---:|---|
| 31 | Distinguish function items, function pointers, and anonymous closure types. |
| 32 | Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers. |
| 33 | Derive the item type and cardinality effect of common iterator adapters. |
| 34 | Design a fold accumulator with a precise prefix invariant. |
| 35 | Compose optional and fallible transformations while preserving ownership and error meaning. |
| 36 | Implement a correct custom `Iterator` by defining state and exhaustion behavior. |
| 37 | Define recursive algebraic data with the appropriate indirection. |
| 38 | Separate deterministic domain decisions from filesystem, time, environment, and terminal effects. |
| 39 | Design domain combinators that preserve type and error meaning. |
| 40 | Produce a transformation map that identifies source, shape, ownership, failure, state, and effect boundaries. |

**Exit construction:** Build a deterministic route-analysis engine whose parser, fallible transformation, reductions, persistent history, borrowed queries, and effect shell can be tested independently.

**Next handoff:** Course 5 moves repetition and cross-surface consistency to compile time, but only when one declaration genuinely deserves authority over several generated Rust surfaces.

## Course 5 — Rust Metaprogramming

**Entry:** You should be able to design traits and public APIs, reason about ordinary Rust expansion targets, write tests at several boundaries, and separate deterministic core logic from effects.

**Primary role:** Course 5 treats metaprogramming as language and authority design. It covers declarative grammar, recursive token processing, hygiene, diagnostics, procedural-macro phases, derives, attributes, typed DSLs, and deterministic build generation.

**Scope boundary:** The course generates ordinary Rust but does not make macros the default abstraction. It avoids using generation for runtime policy, postpones low-level unsafe implementation, and treats third-party procedural-macro crates as compiler-phase dependencies with explicit version and reproducibility implications.

**Reasoning record:** authority map, accepted grammar, token and repetition trace, hygiene/path map, expansion ledger, diagnostic contract, phase map, generated-surface inventory, and reproducibility record.

### Course 5 module outcomes

| Module | You should be able to… |
|---:|---|
| 41 | Separate runtime abstraction from compile-time generation. |
| 42 | Read a matcher as a grammar rather than as textual substitution. |
| 43 | Model recursive macro rules as parser states and transitions. |
| 44 | Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros. |
| 45 | Treat invocation grammar and generated Rust as two related public APIs. |
| 46 | Explain when and how a procedural macro executes. |
| 47 | Parse `DeriveInput` and distinguish structs, enums, and unions. |
| 48 | Parse attribute arguments independently from the attached item. |
| 49 | Design a bounded custom grammar with explicit compatibility space. |
| 50 | Explain the Cargo build-script lifecycle and communication protocol. |

**Exit construction:** Build a small generated command or protocol catalog using at least two distinct macro mechanisms. Every generated fact must have one authority, targeted invalid-input diagnostics, and expansion tests.

**Next handoff:** Course 6 leaves the compiler boundary and crosses external byte, file, process, allocator, ABI, callback, and foreign-resource boundaries.

## Course 6 — Rust Systems Programming

**Entry:** You should be able to model ownership and cleanup, design public traits and errors, isolate effects, understand generated code, and maintain deterministic formats and tests.

**Primary role:** Course 6 connects Rust to hostile bytes, filesystems, native paths, child processes, raw storage, allocators, C callers, callbacks, and foreign resources. Unsafe Rust appears only after the safe product contract and proof boundary are explicit.

**Scope boundary:** The course covers single-threaded systems boundaries and narrow unsafe abstractions. Threads, atomics, async I/O, networking, and production measurement are deferred so each external contract remains visible.

**Reasoning record:** binary-layout table, cursor/range proof, resource-state machine, durability timeline, path threat model, process contract, safety dossier, allocator layout record, ABI table, and foreign-liveness graph.

### Course 6 module outcomes

| Module | You should be able to… |
|---:|---|
| 51 | Define a binary format as a versioned contract rather than a sequence of convenient writes. |
| 52 | Distinguish read, write, flush, data synchronization, metadata synchronization, and directory-entry durability. |
| 53 | Distinguish portable logical names, `Path`, `PathBuf`, `OsStr`, and display text. |
| 54 | Construct commands from a program plus arguments, not an interpolated shell line. |
| 55 | Name the operations Rust requires an unsafe context to perform. |
| 56 | Distinguish raw pointers from references and explain why conversion does not transfer ownership. |
| 57 | Construct and validate `Layout` values without unchecked size arithmetic. |
| 58 | Distinguish ABI compatibility from semantic validity and ownership. |
| 59 | Separate raw bindings, checked unsafe shims, and safe domain wrappers. |
| 60 | Draw one boundary map from external bytes to final effects and back to foreign callers. |

**Exit construction:** Build a checked packet archive with transactional output, one justified unsafe storage abstraction or a written rejection of it, and a stateless C validation boundary.

**Next handoff:** Course 7 introduces legal schedules: values and resources now move among threads, synchronization carries visibility, and termination becomes a first-class product property.

## Course 7 — Rust Concurrency and Parallelism

**Entry:** You should be able to audit ownership, unsafe boundaries, cleanup, representation, and system calls, and to distinguish semantic state from observational or platform-dependent facts.

**Primary role:** Course 7 moves from single-threaded resource correctness to schedule-independent product reasoning. It covers thread transfer, scoped lifetimes, locks and invariants, condition predicates, message passing, liveness, atomics, one narrow lock-free proof, and deterministic parallel reduction.

**Scope boundary:** The course uses operating-system threads and Rayon. Async runtimes, sockets, network protocols, and async cancellation remain Course 8 topics. Lock-free code is taught as a proof exercise, not as a default replacement for locks and channels.

**Reasoning record:** thread ownership map, protected-invariant table, wait-for graph, predicate/wakeup record, channel topology, shutdown tree, happens-before graph, atomic state machine, work-partition map, and deterministic reconciliation table.

### Course 7 module outcomes

| Module | You should be able to… |
|---:|---|
| 61 | distinguish concurrency, parallelism, scheduling, interleaving, data races, and broader race conditions. |
| 62 | explain the real meaning of a `T: 'static` bound and why owned values can satisfy it. |
| 63 | name the state invariant protected by each `Mutex` or `RwLock` rather than treating the primitive as a generic thread-safety wrapper. |
| 64 | write every condition-variable wait as a predicate loop over mutex-protected state. |
| 65 | model channel operations as ownership transfer rather than shared access. |
| 66 | distinguish deadlock, starvation, livelock, priority inversion, and slow work. |
| 67 | separate atomicity of one location from visibility of other memory. |
| 68 | distinguish obstruction-free, lock-free, and wait-free progress claims from ordinary nonblocking API behavior. |
| 69 | distinguish task parallelism, data parallelism, and a long-lived message-driven worker service. |
| 70 | construct one architecture diagram connecting coordinator, queue, workers, result channel, metrics, report pool, and CLI boundaries. |

**Exit construction:** Build a bounded concurrent verifier with a fixed worker group, explicit failure policy, cancellation, panic containment, complete join accounting, and deterministic final reconstruction.

**Next handoff:** Course 8 replaces blocking thread stacks with suspended futures and adds network peers, byte-stream framing, protocol state, deadlines, retries, and graceful service shutdown.

## Course 8 — Rust Async and Networked Services

**Entry:** You should be able to reason about thread ownership, synchronization, backpressure, liveness, atomics, deterministic reconciliation, system I/O, and bounded resources.

**Primary role:** Course 8 begins with the `Future::poll` contract and then builds Tokio task trees, bounded codecs, connection lifecycles, versioned protocols, admission control, cancellation-safe operations, a small Hyper surface, and idempotent retry policy.

**Scope boundary:** The course builds a process-local network service. It does not attempt distributed consensus, TLS implementation, database transactions, service meshes, or framework-driven web development. Those concerns are discussed only where they affect the stated protocol and lifecycle guarantees.

**Reasoning record:** future state table, wake-source map, task tree, buffer/frame ledger, connection state machine, protocol transition table, capacity ledger, cancellation trace, retry/commit matrix, and shutdown timeline.

### Course 8 module outcomes

| Module | You should be able to… |
|---:|---|
| 71 | explain why a future is inert until polled. |
| 72 | distinguish a runtime, worker thread, task, future, reactor, and blocking pool. |
| 73 | distinguish readiness from transfer completion. |
| 74 | distinguish bind, listen, accept, connect, resolve, read, write, half-close, and full close. |
| 75 | separate framing, text decoding, syntax parsing, semantic validation, state legality, and application execution. |
| 76 | find every accumulation point in an async service. |
| 77 | derive cancellation behavior from future-owned state and external side effects. |
| 78 | distinguish accepted transport, HTTP connection future, request future, body stream, and application service. |
| 79 | classify failures by phase, scope, retryability, and commit ambiguity. |
| 80 | construct a complete async service dossier. |

**Exit construction:** Build a bounded async command service with a length-delimited protocol, tracked task tree, explicit admission, honest health semantics, cancellation-safe shutdown, and deterministic timeout tests.

**Next handoff:** Course 9 asks whether the service’s performance, memory, reliability, observability, security, artifact, and operational claims are supported by representative evidence.

## Course 9 — Rust Performance and Production Engineering

**Entry:** You should be able to build bounded synchronous and asynchronous systems, state protocol and shutdown guarantees, separate live metrics from authoritative state, and preserve deterministic behavior under concurrency.

**Primary role:** Course 9 converts production claims into falsifiable contracts. It covers benchmark design, profiling, allocation and data movement, saturation and queueing, observability, reliability policy, threat modeling, supply-chain review, Cargo profiles, packaging, rollout, and incident learning.

**Scope boundary:** The course teaches measurement and operational reasoning, not folklore optimization. It does not promise universal performance rankings, complete security proof, or production readiness from one green pipeline. Every conclusion is scoped to a workload, artifact, environment, and time.

**Reasoning record:** performance claim, workload description, benchmark boundary, cost model, allocation ledger, byte journey, saturation curve, signal dictionary, SLO/error-budget policy, threat model, dependency dossier, release manifest, and rollout decision.

### Course 9 module outcomes

| Module | You should be able to… |
|---:|---|
| 81 | turn an imprecise performance complaint into a falsifiable contract with workload, metric, percentile, resource budget, and correctness oracle. |
| 82 | choose sampling, instrumentation, counters, and targeted tracing based on the question being asked. |
| 83 | distinguish object size, heap allocation, capacity, live bytes, retained bytes, peak bytes, and allocation count. |
| 84 | trace bytes across kernel, transport, framing, parsing, domain, storage, and response layers. |
| 85 | separate service time, wait time, queue depth, concurrency, throughput, and utilization. |
| 86 | separate events, spans, metrics, profiles, and domain audit records by the questions they can answer. |
| 87 | write a service-level indicator and objective whose population, success condition, window, and exclusions are unambiguous. |
| 88 | identify assets, actors, trust boundaries, entry points, privileges, and abuse cases for a Rust service. |
| 89 | explain how Cargo profile settings affect optimization, debug information, overflow checks, assertions, code generation, link-time optimization, panic behavior, and strip policy. |
| 90 | write a production-readiness review that connects user behavior to capacity, dependencies, failure modes, observability, security, and recovery. |

**Exit construction:** Take a bounded service and produce a complete production dossier: benchmark protocol, profile, memory and byte accounting, load curve, observability map, reliability policy, threat model, release manifest, and go/no-go decision.

**Next handoff:** Course 10 synthesizes the entire program: advanced type relationships, compiler representations, unsafe review, verification strategy, compatibility, and long-lived architectural change.

## Course 10 — Advanced Rust Mastery

**Entry:** You should have completed the preceding nine courses or equivalent work. You should be able to explain ownership, memory, traits, functional dataflow, macros, unsafe systems boundaries, concurrency, async protocols, and production evidence without relying on API-name recall alone.

**Primary role:** Course 10 is the synthesis course. It teaches compiler-phase reasoning, advanced trait solving, GATs and HRTBs, const-generic witnesses, opaque and erased types, whole-abstraction unsafe review, source-to-artifact analysis, verification strategy, API and data evolution, and architectural restraint.

**Scope boundary:** The course selects stable mechanisms that serve real product requirements. It does not reward obscure syntax, nightly-feature collecting, unsafe code retained for display, or lower-level compiler output used where source-level reasoning is already decisive.

**Reasoning record:** compiler-phase record, trait-goal graph, lifetime family, witness proof, open/closed variation map, unsafe state-and-operation dossier, source-to-artifact observation, verification claim matrix, compatibility matrix, migration plan, and architecture decision record.

### Course 10 module outcomes

| Module | You should be able to… |
|---:|---|
| 91 | separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases. |
| 92 | rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints. |
| 93 | distinguish one associated type from a lifetime-indexed family of associated types. |
| 94 | use const parameters when a numeric fact changes representation, layout, or legal composition. |
| 95 | distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type. |
| 96 | write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation. |
| 97 | explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication. |
| 98 | classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims. |
| 99 | analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data. |
| 100 | construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy. |

**Exit construction:** Build a versioned embedded journal whose borrowed read API, runtime validators, bounded transaction representation, compatibility policy, unsafe-or-safe storage decision, and verification matrix are derived from an invariant ownership map.

**Next handoff:** The program ends with independent transfer: you should be able to enter an unfamiliar Rust system, identify its authorities and proof boundaries, make a cross-cutting change, and state what remains uncertain.
