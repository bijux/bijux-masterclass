# Sixty-module course map

The sequence is cumulative. Revisited ideas return at a higher level: use becomes memory reasoning; memory reasoning becomes architecture; architecture becomes dataflow; dataflow becomes compile-time authority; compile-time authority meets external systems boundaries.

## Course 1 — Rust Foundations

**Values, Ownership, and Complete Programs**

Learn to read Rust as a typed language, make ownership visible, model valid states, handle failure explicitly, and finish a complete tested program.

1. [Compilation, Expressions, and Types](01-rust-foundations/course-book/module-01-compilation-expressions-and-types/index.md) — How does Rust turn source text into a typed program, and what type and value does every expression produce?
2. [Control Flow, Functions, and Invariants](01-rust-foundations/course-book/module-02-control-flow-functions-and-invariants/index.md) — How can control flow make every path, boundary, and loop invariant visible enough to test and review?
3. [Ownership, Moves, Copying, and Destruction](01-rust-foundations/course-book/module-03-ownership-moves-copying-and-destruction/index.md) — Who owns each resource after every assignment, call, return, destructure, and scope exit?
4. [Borrowing, References, Slices, and Strings](01-rust-foundations/course-book/module-04-borrowing-references-slices-and-strings/index.md) — Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?
5. [Structs, Enums, Methods, and Pattern Matching](01-rust-foundations/course-book/module-05-structs-enums-methods-and-pattern-matching/index.md) — How can the type system make valid states representable and contradictory states difficult or impossible to construct?
6. [Collections, Iterators, and Closures](01-rust-foundations/course-book/module-06-collections-iterators-and-closures/index.md) — Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?
7. [Errors, Parsing, Files, and Persistence](01-rust-foundations/course-book/module-07-errors-parsing-files-and-persistence/index.md) — Which failures are part of the product contract, where are they detected, and what state is visible after failure?
8. [Generics, Traits, Conversions, and Lifetime Basics](01-rust-foundations/course-book/module-08-generics-traits-conversions-and-lifetime-basics/index.md) — What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?
9. [Crates, Modules, Public APIs, Tests, and Documentation](01-rust-foundations/course-book/module-09-crates-modules-public-apis-tests-and-documentation/index.md) — Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?
10. [Integration and Independent Change](01-rust-foundations/course-book/module-10-integration-and-independent-change/index.md) — Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?

Capstone: [Taskboard](01-rust-foundations/course-book/capstone.md)

Next-stage handoff: Course 2 keeps the same ownership model but studies it at the level of places, provenance, destruction, sharing, layout, and address sensitivity.

## Course 2 — Ownership, Lifetimes, and Memory

**Resource Topology and Safe Memory Design**

Deepen ownership until you can design borrowed APIs, cleanup protocols, shared graphs, interior mutability, representation claims, variance, and pinning without folklore.

11. [Places, Move Paths, and Advanced Borrowing](02-rust-ownership-lifetimes-memory/course-book/module-11-places-move-paths-and-advanced-borrowing/index.md) — Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?
12. [Lifetime Relationships and Borrowed APIs](02-rust-ownership-lifetimes-memory/course-book/module-12-lifetime-relationships-and-borrowed-apis/index.md) — What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?
13. [Scoped Access and Escape Prevention](02-rust-ownership-lifetimes-memory/course-book/module-13-scoped-access-and-escape-prevention/index.md) — Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?
14. [RAII, Drop, Unwinding, and Failure Atomicity](02-rust-ownership-lifetimes-memory/course-book/module-14-raii-drop-unwinding-and-failure-atomicity/index.md) — Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?
15. [Box, Deref, Dynamically Sized Types, and Cow](02-rust-ownership-lifetimes-memory/course-book/module-15-box-deref-dynamically-sized-types-and-cow/index.md) — When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?
16. [Rc, Weak, and Ownership Graphs](02-rust-ownership-lifetimes-memory/course-book/module-16-rc-weak-and-ownership-graphs/index.md) — Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?
17. [Interior Mutability and Runtime Borrows](02-rust-ownership-lifetimes-memory/course-book/module-17-interior-mutability-and-runtime-borrows/index.md) — Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?
18. [Memory Representation, Validity, and Layout](02-rust-ownership-lifetimes-memory/course-book/module-18-memory-representation-validity-and-layout/index.md) — Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?
19. [Subtyping, Variance, PhantomData, and Drop Checking](02-rust-ownership-lifetimes-memory/course-book/module-19-subtyping-variance-phantomdata-and-drop-checking/index.md) — When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?
20. [Pinning and Address-Sensitive Design](02-rust-ownership-lifetimes-memory/course-book/module-20-pinning-and-address-sensitive-design/index.md) — What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?

Capstone: [Memory Workspace](02-rust-ownership-lifetimes-memory/course-book/capstone.md)

Next-stage handoff: Course 3 turns these memory-safe types into public contracts and architectural variation points.

## Course 3 — Traits, Generics, and Architectural Design

**Contracts, Polymorphism, and Evolvable APIs**

Turn type-level knowledge into architecture: define lawful contracts, choose static or dynamic polymorphism, compose behavior, encode protocols, and evolve public APIs.

21. [Traits as Behavioral Contracts](03-rust-traits-generics-architectural-design/course-book/module-21-traits-as-behavioral-contracts/index.md) — What behavior truly belongs in a shared contract, and which laws must every implementation preserve?
22. [Associated Types and Type Families](03-rust-traits-generics-architectural-design/course-book/module-22-associated-types-and-type-families/index.md) — When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?
23. [Coherence and Implementation Ownership](03-rust-traits-generics-architectural-design/course-book/module-23-coherence-and-implementation-ownership/index.md) — Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?
24. [Static Polymorphism and Opaque Types](03-rust-traits-generics-architectural-design/course-book/module-24-static-polymorphism-and-opaque-types/index.md) — When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?
25. [Trait Objects and Dynamic Polymorphism](03-rust-traits-generics-architectural-design/course-book/module-25-trait-objects-and-dynamic-polymorphism/index.md) — When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?
26. [Composition and OOP-Style Design Without Inheritance](03-rust-traits-generics-architectural-design/course-book/module-26-composition-and-oop-style-design-without-inheritance/index.md) — How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?
27. [Typestate and Capability-Oriented APIs](03-rust-traits-generics-architectural-design/course-book/module-27-typestate-and-capability-oriented-apis/index.md) — Which illegal operations can be removed from the API by representing protocol state and authority in types?
28. [Boundary Traits and Adapters](03-rust-traits-generics-architectural-design/course-book/module-28-boundary-traits-and-adapters/index.md) — How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?
29. [Public API Evolution](03-rust-traits-generics-architectural-design/course-book/module-29-public-api-evolution/index.md) — How can a public trait-based API evolve when downstream crates may both call it and implement it?
30. [Architectural Synthesis](03-rust-traits-generics-architectural-design/course-book/module-30-architectural-synthesis/index.md) — Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?

Capstone: [Review Engine](03-rust-traits-generics-architectural-design/course-book/capstone.md)

Next-stage handoff: Course 4 uses those contracts as the joints of explicit dataflow and effect architecture.

## Course 4 — Functional Rust

**Closures, Iterators, and Explicit Dataflow**

Make callable capability, laziness, traversal, failure, accumulation, structural sharing, and effects explicit enough to reason about composition and cost.

31. [Closures, Capture, and Callable Contracts](04-rust-functional-programming/course-book/module-31-closures-capture-and-callable-contracts/index.md) — What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?
32. [The Iterator Model](04-rust-functional-programming/course-book/module-32-the-iterator-model/index.md) — What state does an iterator own, when does work happen, and what is consumed by each call to next?
33. [Iterator Algebra and Pipeline Shape](04-rust-functional-programming/course-book/module-33-iterator-algebra-and-pipeline-shape/index.md) — How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?
34. [Folds, Scans, and Short-Circuiting](04-rust-functional-programming/course-book/module-34-folds-scans-and-short-circuiting/index.md) — What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?
35. [Option, Result, and Fallible Traversal](04-rust-functional-programming/course-book/module-35-option-result-and-fallible-traversal/index.md) — Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?
36. [Custom Iterators and Collection Protocols](04-rust-functional-programming/course-book/module-36-custom-iterators-and-collection-protocols/index.md) — What laws must a custom traversal obey, and who owns the collection when iteration begins?
37. [Recursive Data and Structural Sharing](04-rust-functional-programming/course-book/module-37-recursive-data-and-structural-sharing/index.md) — How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?
38. [Functional Core and Effect Isolation](04-rust-functional-programming/course-book/module-38-functional-core-and-effect-isolation/index.md) — Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?
39. [Combinator Laws and Cost Models](04-rust-functional-programming/course-book/module-39-combinator-laws-and-cost-models/index.md) — What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?
40. [Functional Architecture Synthesis](04-rust-functional-programming/course-book/module-40-functional-architecture-synthesis/index.md) — How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?

Capstone: [LedgerFlow](04-rust-functional-programming/course-book/capstone.md)

Next-stage handoff: Course 5 asks when repeated dataflow and type relationships should become compile-time generation rather than ordinary Rust.

## Course 5 — Rust Metaprogramming

**Macros, Derives, and Compile-Time Systems**

Use generation only where one checked declaration must own several Rust surfaces or validated build data, and keep the expanded program understandable as ordinary Rust.

41. [Metaprogramming Boundaries and the Expansion Model](05-rust-metaprogramming/course-book/module-41-metaprogramming-boundaries-and-expansion-model/index.md) — Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?
42. [Declarative Macros: Matchers, Fragments, and Repetition](05-rust-metaprogramming/course-book/module-42-declarative-macros-matchers-fragments-and-repetition/index.md) — How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?
43. [Recursive Macro Parsing and Token-Tree Techniques](05-rust-metaprogramming/course-book/module-43-recursive-macro-parsing-and-token-tree-techniques/index.md) — How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity?
44. [Hygiene, Scope, Paths, and Cross-Crate Macros](05-rust-metaprogramming/course-book/module-44-hygiene-scope-paths-and-cross-crate-macros/index.md) — Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?
45. [Macro Diagnostics, Testing, and Public API Design](05-rust-metaprogramming/course-book/module-45-macro-diagnostics-testing-and-public-api-design/index.md) — How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API?
46. [Procedural Macro Execution and TokenStream Engineering](05-rust-metaprogramming/course-book/module-46-procedural-macro-execution-and-tokenstream-engineering/index.md) — What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?
47. [Custom Derive Macros and Structural Generation](05-rust-metaprogramming/course-book/module-47-custom-derive-macros-and-structural-generation/index.md) — How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking?
48. [Attribute Macros and Item Transformation](05-rust-metaprogramming/course-book/module-48-attribute-macros-and-item-transformation/index.md) — How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?
49. [Function-Like Procedural Macros and Typed DSLs](05-rust-metaprogramming/course-book/module-49-function-like-procedural-macros-and-typed-dsls/index.md) — How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?
50. [Build Scripts, Generated Code, and Compile-Time Architecture](05-rust-metaprogramming/course-book/module-50-build-scripts-generated-code-and-compile-time-architecture/index.md) — How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?

Capstone: [CommandForge](05-rust-metaprogramming/course-book/capstone.md)

Next-stage handoff: Course 6 takes the same proof discipline across binary, operating-system, allocator, and foreign-language boundaries.

## Course 6 — Rust Systems Programming

**Bytes, Operating-System Boundaries, Unsafe Abstractions, and FFI**

Cross external boundaries without losing the guarantees built in the first five courses: define representations, track resources, isolate unsafe obligations, and expose safe interfaces.

51. [Binary Data Contracts: Bytes, Endianness, and Checked Parsing](06-rust-systems-programming/course-book/module-51-binary-data-contracts/index.md) — How do you turn untrusted bytes into typed values without confusing representation, validation, allocation, and meaning?
52. [Files, Durability, and Transactional Replacement](06-rust-systems-programming/course-book/module-52-files-durability-and-transactional-replacement/index.md) — What has actually been promised after a file operation succeeds: bytes written, buffers flushed, data synchronized, a name replaced, or a recoverable durable state?
53. [Paths, Names, and Platform Boundaries](06-rust-systems-programming/course-book/module-53-paths-names-and-platform-boundaries/index.md) — How do you manipulate host paths without pretending that every operating-system name is UTF-8, every component is harmless, or every lookup remains stable?
54. [Processes, Environments, and Standard Streams](06-rust-systems-programming/course-book/module-54-processes-environments-and-standard-streams/index.md) — How do you launch another program without turning arguments into shell syntax, leaking ambient state, deadlocking on pipes, or misreporting its result?
55. [Unsafe Rust as a Proof Boundary](06-rust-systems-programming/course-book/module-55-unsafe-rust-and-safety-proofs/index.md) — What additional obligation begins when the compiler can no longer prove a memory-safety condition, and how do you make that obligation small, local, and reviewable?
56. [Raw Pointers, Provenance, and Uninitialized Memory](06-rust-systems-programming/course-book/module-56-raw-pointers-provenance-and-uninitialized-memory/index.md) — How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?
57. [Manual Allocation and Owning Unsafe Abstractions](06-rust-systems-programming/course-book/module-57-manual-allocation-and-owning-unsafe-abstractions/index.md) — How do you turn a raw allocation into one safe owner whose length, layout, initialization, destruction, and failure behavior remain correct for every state?
58. [C FFI: ABI, Strings, Pointers, and Error Boundaries](06-rust-systems-programming/course-book/module-58-c-ffi-abi-strings-and-error-boundaries/index.md) — How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?
59. [Foreign Resources, Callbacks, and Wrapper Architecture](06-rust-systems-programming/course-book/module-59-foreign-resources-callbacks-and-wrapper-architecture/index.md) — How do you wrap a foreign handle so ownership, borrowing, destruction, callbacks, reentrancy, and error channels become ordinary Rust obligations?
60. [Integrated Systems Design, Testing, and Audit](06-rust-systems-programming/course-book/module-60-integrated-systems-design-and-audit/index.md) — How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?

Capstone: [FrameVault](06-rust-systems-programming/course-book/capstone.md)

Next-stage handoff: Course 7 will add concurrency and parallelism, where ownership and boundary reasoning must remain valid across simultaneous execution.
