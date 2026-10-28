# Skill map: how the program matures

The six courses are cumulative. Each adds a new layer of responsibility without abandoning the earlier ones.

## Course 1 — Rust Foundations

**Primary lens:** value, type, state, and failure.

**Working artifacts:** expression/type traces, ownership ledgers, state diagrams, error maps, and public-behavior tests.

**Course outcome:** Learn to read Rust as a typed language, make ownership visible, model valid states, handle failure explicitly, and finish a complete tested program.

**Capstone proof:** **Taskboard** is a persistent typed command-line task board that grows from one pure function into a library, binary, storage format, tests, and an independently designed feature.

**Handoff:** Course 2 keeps the same ownership model but studies it at the level of places, provenance, destruction, sharing, layout, and address sensitivity.

## Course 2 — Ownership, Lifetimes, and Memory

**Primary lens:** permission, provenance, liveness, cleanup, and representation.

**Working artifacts:** place-and-loan traces, lifetime relationship diagrams, cleanup state machines, liveness graphs, representation claim ledgers, and safety arguments.

**Course outcome:** Deepen ownership until you can design borrowed APIs, cleanup protocols, shared graphs, interior mutability, representation claims, variance, and pinning without folklore.

**Capstone proof:** **Memory Workspace** is an in-memory document workspace with generational handles, borrowed views, edit sessions, snapshots, observers, caches, and an explicit decision about whether pinning is justified.

**Handoff:** Course 3 turns these memory-safe types into public contracts and architectural variation points.

## Course 3 — Traits, Generics, and Architectural Design

**Primary lens:** contract, law, variation, capability, dispatch, and evolution.

**Working artifacts:** law tables, implementation-ownership maps, variation maps, dispatch decisions, typestate graphs, compatibility impact tables, and contract tests.

**Course outcome:** Turn type-level knowledge into architecture: define lawful contracts, choose static or dynamic polymorphism, compose behavior, encode protocols, and evolve public APIs.

**Capstone proof:** **Review Engine** is a policy evaluation engine with generic source and reporter boundaries, a dynamic rule registry, coherence-safe adapters, typestate construction, and a defended public extension surface.

**Handoff:** Course 4 uses those contracts as the joints of explicit dataflow and effect architecture.

## Course 4 — Functional Rust

**Primary lens:** capture, demand, item shape, cardinality, order, failure, accumulation, effect, and cost.

**Working artifacts:** capture ledgers, iterator stage maps, accumulator invariants, failure-policy matrices, structural-sharing diagrams, effect plans, law tests, and cost ledgers.

**Course outcome:** Make callable capability, laziness, traversal, failure, accumulation, structural sharing, and effects explicit enough to reason about composition and cost.

**Capstone proof:** **LedgerFlow** is a deterministic ledger-event analyzer with structured diagnostics, failure-aware traversal, reduction invariants, persistent audit history, lazy queries, reports, and an effect shell.

**Handoff:** Course 5 asks when repeated dataflow and type relationships should become compile-time generation rather than ordinary Rust.

## Course 5 — Rust Metaprogramming

**Primary lens:** source of truth, input grammar, expansion, phase, name resolution, diagnostics, determinism, and compatibility.

**Working artifacts:** mechanism decisions, expansion ledgers, grammar tables, ASTs, semantic-validation tables, generated-surface maps, diagnostic contracts, and reproducibility records.

**Course outcome:** Use generation only where one checked declaration must own several Rust surfaces or validated build data, and keep the expanded program understandable as ordinary Rust.

**Capstone proof:** **CommandForge** is a compile-time validated command catalog combining a declarative catalog, custom derive, checked attribute, typed procedural DSL, and deterministic build generation while runtime commands remain ordinary Rust.

**Handoff:** Course 6 takes the same proof discipline across binary, operating-system, allocator, and foreign-language boundaries.

## Course 6 — Rust Systems Programming

**Primary lens:** external representation, resource state, trust boundary, unsafe obligation, platform contract, ABI, and compatibility.

**Working artifacts:** byte-layout tables, resource state machines, boundary ledgers, safety ledgers, allocation-state diagrams, ABI contracts, target-claim tables, and adversarial tests.

**Course outcome:** Cross external boundaries without losing the guarantees built in the first five courses: define representations, track resources, isolate unsafe obligations, and expose safe interfaces.

**Capstone proof:** **FrameVault** is a versioned archive, transactional store, path policy, child-process capture system, aligned storage owner, C ABI, and opaque foreign-session API with an explicit safety dossier.

**Handoff:** Course 7 will add concurrency and parallelism, where ownership and boundary reasoning must remain valid across simultaneous execution.

## Program-level outcome

After Course 6, you should be able to take an unfamiliar Rust problem from external representation to tested public interface:

1. define valid states and failure behavior;
2. choose ownership and borrowing boundaries;
3. derive lifetime, cleanup, and liveness relationships;
4. design narrow lawful contracts and variation points;
5. express transformations and effects as reviewable dataflow;
6. generate code only where one compile-time source of truth justifies it;
7. isolate operating-system, unsafe, allocator, and FFI obligations behind safe abstractions;
8. state which claims are guaranteed, checked, target-conditioned, or still external assumptions.

This is the readiness boundary for Course 7: concurrency and parallelism.
