# Skill map: how the program matures

The nine courses are cumulative. Each adds a new layer of responsibility without abandoning the earlier ones. A later mechanism is not permission to stop reasoning about values, ownership, failure, or boundaries.

## Course 1 — Rust Foundations

**Primary lens:** value, type, state, and failure.

**Working artifacts:** expression/type traces, ownership ledgers, state diagrams, error maps, and public-behavior tests.

**Course outcome:** read Rust as a typed language, make ownership visible, model valid states, handle failure explicitly, and finish a complete tested program.

**Capstone proof:** **Taskboard** is a persistent typed command-line task board that grows from pure functions into a library, binary, storage format, tests, and an independently designed feature.

**Handoff:** Course 2 keeps the same ownership model but studies it at the level of places, provenance, destruction, sharing, layout, and address sensitivity.

## Course 2 — Ownership, Lifetimes, and Memory

**Primary lens:** permission, provenance, liveness, cleanup, and representation.

**Working artifacts:** place-and-loan traces, lifetime relationship diagrams, cleanup state machines, liveness graphs, representation claim ledgers, and safety arguments.

**Course outcome:** design borrowed APIs, cleanup protocols, shared graphs, interior mutability, representation claims, variance, and pinning without folklore.

**Capstone proof:** **Memory Workspace** is an in-memory document workspace with generational handles, borrowed views, edit sessions, snapshots, observers, caches, and an explicit decision about whether pinning is justified.

**Handoff:** Course 3 turns memory-safe types into public contracts and architectural variation points.

## Course 3 — Traits, Generics, and Architectural Design

**Primary lens:** contract, law, variation, capability, dispatch, and evolution.

**Working artifacts:** law tables, implementation-ownership maps, variation maps, dispatch decisions, typestate graphs, compatibility impact tables, and contract tests.

**Course outcome:** define lawful contracts, choose static or dynamic polymorphism, compose behavior, encode protocols, and evolve public APIs.

**Capstone proof:** **Review Engine** is a policy evaluation engine with generic source and reporter boundaries, a dynamic rule registry, coherence-safe adapters, typestate construction, and a defended public extension surface.

**Handoff:** Course 4 uses those contracts as the joints of explicit dataflow and effect architecture.

## Course 4 — Functional Rust

**Primary lens:** capture, demand, item shape, cardinality, order, failure, accumulation, effect, and cost.

**Working artifacts:** capture ledgers, iterator stage maps, accumulator invariants, failure-policy matrices, structural-sharing diagrams, effect plans, law tests, and cost ledgers.

**Course outcome:** make callable capability, laziness, traversal, failure, accumulation, structural sharing, and effects explicit enough to reason about composition and cost.

**Capstone proof:** **LedgerFlow** is a deterministic ledger-event analyzer with structured diagnostics, failure-aware traversal, reduction invariants, persistent audit history, lazy queries, reports, and an effect shell.

**Handoff:** Course 5 asks when repeated dataflow and type relationships should become compile-time generation rather than ordinary Rust.

## Course 5 — Rust Metaprogramming

**Primary lens:** source of truth, input grammar, expansion, phase, name resolution, diagnostics, determinism, and compatibility.

**Working artifacts:** mechanism decisions, expansion ledgers, grammar tables, ASTs, semantic-validation tables, generated-surface maps, diagnostic contracts, and reproducibility records.

**Course outcome:** use generation only where one checked declaration should own several Rust surfaces or validated build data, while keeping the expanded program understandable as ordinary Rust.

**Capstone proof:** **CommandForge** is a compile-time validated command catalog combining a declarative catalog, custom derive, checked attribute, typed procedural DSL, and deterministic build generation while runtime commands remain ordinary Rust.

**Handoff:** Course 6 takes the same proof discipline across binary, operating-system, allocator, and foreign-language boundaries.

## Course 6 — Rust Systems Programming

**Primary lens:** external representation, resource state, trust boundary, unsafe obligation, platform contract, ABI, and compatibility.

**Working artifacts:** byte-layout tables, resource state machines, boundary ledgers, safety ledgers, allocation-state diagrams, ABI contracts, target-claim tables, and adversarial tests.

**Course outcome:** cross external boundaries without losing the guarantees built in the first five courses: define representations, track resources, isolate unsafe obligations, and expose safe interfaces.

**Capstone proof:** **FrameVault** is a versioned archive, transactional store, path policy, child-process capture system, aligned storage owner, C ABI, and opaque foreign-session API with an explicit safety dossier.

**Handoff:** Course 7 asks whether every ownership, cleanup, unsafe, and external-boundary claim remains valid when several execution agents may advance at once.

## Course 7 — Rust Concurrency and Parallelism

**Primary lens:** schedule, ownership transfer, synchronization, exclusion, visibility, liveness, failure, determinism, and resource bounds.

**Working artifacts:** thread ownership maps, join ledgers, protected-invariant tables, condition predicates, endpoint graphs, wait-for graphs, happens-before proofs, unsafe auto-trait dossiers, reduction laws, and deterministic reconciliation maps.

**Course outcome:** design concurrent and parallel Rust systems that are not merely data-race free, but have explicit capacity, shutdown, panic, cancellation, visibility, and output-order contracts.

**Capstone proof:** **BatchWeave** is a bounded concurrent batch engine with a fixed worker group, blocking queue, typed terminal outcomes, cooperative fail-fast cancellation, advisory atomic metrics, deterministic reconciliation, and a separately owned Rayon reporting stage.

**Handoff:** Course 8 will add asynchronous and networked systems. The same lifecycle questions remain, but tasks may suspend instead of occupying one thread and protocols must survive partial I/O, backpressure, cancellation, and distributed failure.

## Course 8 — Rust Async and Networked Services

**Primary lens:** suspension, wakeup, task ownership, framing, protocol state, capacity, cancellation, deadlines, commit ambiguity, retries, and shutdown.

**Working artifacts:** future-state ledgers, task trees, frame ledgers, connection state machines, capacity envelopes, cancellation tables, retry ledgers, service dossiers, and scripted-peer tests.

**Course outcome:** build bounded async and networked Rust services whose execution, wire behavior, overload, cancellation, retry, and operational claims can be explained independently of favorable scheduling or peer behavior.

**Capstone proof:** **JobWire** is a bounded TCP job protocol with explicit framing and negotiation, a single-authority broker, process-local idempotency, retry-safe clients, a small Hyper health surface, and phased graceful shutdown.

**Handoff:** Course 9 measures and hardens these systems for production: profiling, benchmarking, allocation, data movement, observability, reliability, security, packaging, CI, and release engineering.

## Course 9 — Rust Performance and Production Engineering

**Primary lens:** claim, workload, measurement boundary, cost, resource envelope, signal, threat, artifact, rollout, and recovery.

**Working artifacts:** performance charters, benchmark matrices, cost models, allocation and byte-journey ledgers, saturation reports, event schemas, SLO and retry policies, threat models, dependency inventories, release manifests, capacity plans, runbooks, and rollout records.

**Course outcome:** turn a correct Rust service into a measured, bounded, diagnosable, secure, reproducibly packaged, and operable product without confusing target observations with language guarantees.

**Capstone proof:** **MetricRail** is a bounded telemetry aggregator with representative benchmarks, causal profiles, borrowed parsing, explicit resource limits, structured tracing, typed overload, threat and dependency review, deterministic release metadata, and a production-readiness defense.

**Handoff:** Course 10 will integrate advanced type reasoning, compiler behavior, unsafe abstraction review, API evolution, performance evidence, and long-horizon architecture in one large systems capstone.

## Program-level outcome after Course 9

You should now be able to take an unfamiliar Rust problem from source text and external representation to a bounded concurrent or networked product:

1. define valid states and failure behavior;
2. choose ownership and borrowing boundaries;
3. derive lifetime, cleanup, and liveness relationships;
4. design narrow lawful contracts and variation points;
5. express transformations and effects as reviewable dataflow;
6. generate code only where one compile-time source of truth justifies it;
7. isolate operating-system, unsafe, allocator, and FFI obligations behind safe abstractions;
8. map thread ownership, joins, endpoints, and shutdown;
9. derive synchronization and atomic ordering from publication requirements;
10. separate data-race freedom from deadlock freedom, determinism, boundedness, fairness, and performance;
11. normalize nondeterministic execution into stable product output where the contract requires it;
12. state which claims are guaranteed, checked, target-conditioned, schedule-conditioned, or still external assumptions.

13. derive future state from suspension points and retained values;
14. own, cancel, drain, abort, and join asynchronous task trees;
15. turn arbitrary byte chunks into bounded protocol messages;
16. separate transport completion, protocol acceptance, application commit, and client observation;
17. define idempotency and retries for ambiguous remote outcomes;
18. state honest health, capacity, timeout, and shutdown guarantees.

19. define representative workloads and falsifiable performance contracts;
20. localize cost with profiles and scaling models before optimizing;
21. budget allocation, retention, byte movement, queueing, and tail behavior;
22. design bounded traces, metrics, health, SLOs, retries, and degraded modes;
23. threat-model runtime and build boundaries and minimize dependency and privilege surface;
24. produce traceable artifacts with explicit profiles, feature matrices, CI, installation, rollback, and rollout policy.

This is the readiness boundary for Course 10: advanced Rust mastery and integrated systems architecture.
