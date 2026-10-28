# Rust Advanced Mastery

## Compiler Reasoning, Type Architecture, and Long-Lived Systems

Course 10 is the final ten-day course and covers Modules 91–100. It is not a miscellaneous “advanced topics” appendix. It is the synthesis course: every mechanism is judged by the proof it provides, the authority it assigns, the compatibility burden it creates, the evidence that supports it, and the simpler design it displaces.

The first nine courses established a complete progression:

```text
values and control
        ↓
resources and memory
        ↓
contracts and architecture
        ↓
dataflow and effects
        ↓
compile-time authority
        ↓
systems boundaries
        ↓
concurrent execution
        ↓
async services and protocols
        ↓
measured production systems
        ↓
compiler-shaped reasoning and long-lived design
```

The cumulative capstone, **AxiomStore**, is a versioned embedded record engine. It uses advanced Rust selectively: a GAT-based private codec lends record views, const generics bound local representation, trait objects host runtime validators, one reviewed `MaybeUninit` abstraction owns an inline transaction batch, and versioned migrations preserve stored data. The course’s central discipline is restraint. You must justify every advanced mechanism against a simpler alternative.

## What you will be able to do

After completing Course 10, you will be able to:

- separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases
- translate source constructs into a control-flow and place-oriented model suitable for borrow, move, and drop reasoning
- rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints
- distinguish proving that a trait is implemented from normalizing an associated type selected by that implementation
- distinguish one associated type from a lifetime-indexed family of associated types
- design a lending cursor whose returned view cannot outlive the borrow that produced it
- use const parameters when a numeric fact changes representation, layout, or legal composition
- construct witness types only through checked functions and preserve their proof through private fields
- distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type
- derive dyn-compatibility requirements from the operations available through erased receivers
- write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation
- separate Rust validity from application invariants and explain which violations can create undefined behavior
- explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication
- compare static dispatch, enum dispatch, and trait-object dispatch through behavior, extension model, call shape, and measured artifact cost
- classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims
- select compile-fail tests, examples, properties, model exploration, fuzzing, Miri, schedule exploration, or benchmarks according to the claim
- analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data
- define and test an MSRV policy without confusing the manifest declaration with actual verification
- construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy
- choose static, dynamic, enum, const-generic, borrowing, owned, generated, concurrent, async, and unsafe mechanisms only where their proof benefit exceeds complexity

- read a difficult Rust failure through the earliest compiler phase capable of deciding it;
- construct trait-goal, lifetime-quantifier, variation, unsafe-safety, verification, and compatibility records;
- audit an unsafe abstraction from safe constructors through panic and destruction rather than reviewing isolated pointer lines;
- scope code-generation and layout conclusions to an exact artifact;
- evolve a public library and persistent format with explicit downstream and migration evidence;
- defend a complete architecture while naming residual risk and mechanisms deliberately rejected.

## Prerequisite diagnosis

Begin only when you can complete the following without tutorials:

1. build and test a multi-crate Rust workspace;
2. explain moves, reborrowing, variance, pinning, trait objects, associated types, and typestate;
3. audit a small unsafe block through validity, alignment, initialization, aliasing, lifetime, and cleanup;
4. design bounded concurrent and async lifecycles;
5. distinguish a language guarantee, library contract, platform observation, product invariant, and measured artifact claim;
6. create a performance experiment with an oracle and traceable build identity;
7. evolve a versioned protocol or file format without silently reinterpreting old data.

If one area is weak, return to the named earlier capstone and repair it before beginning. Course 10 assumes fluency because its work is integration and review, not first exposure.

## The ten modules

91. [Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen](module-91-reading-rust-through-the-compiler-hir-mir-borrow-checking-and-codegen/index.md) — When difficult Rust code surprises you, which compiler representation and which proof obligation actually decide the result?
92. [Advanced Trait Solving: Goals, Projections, and Type Equality](module-92-advanced-trait-solving-goals-projections-and-type-equality/index.md) — How do you design and debug APIs when the compiler must prove nested trait goals and normalize associated types before ordinary operations become legal?
93. [GATs, Higher-Ranked Bounds, and Lending Interfaces](module-93-gats-higher-ranked-bounds-and-lending-interfaces/index.md) — How can an API return views tied to each borrow of `self` without pretending that every yielded value has one fixed lifetime?
94. [Const Generics, Witness Types, and Compile-Time Invariants](module-94-const-generics-witness-types-and-compile-time-invariants/index.md) — Which numeric and state facts belong in types, which remain runtime data, and how do you avoid turning a library into an unusable type-level calculator?
95. [Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries](module-95-opaque-and-erased-types-impl-trait-dyn-trait-any-and-plugin-boundaries/index.md) — When should an API hide one concrete type, erase many concrete types behind a contract, or preserve explicit variants—and what information is lost at each boundary?
96. [Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits](module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/index.md) — What exact proof makes a safe API implemented with unsafe code sound across every constructor, method, failure path, destructor, and thread-safety claim?
97. [From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size](module-97-from-source-to-machine-code-monomorphization-dispatch-layout-and-code-size/index.md) — How do type-level architecture and compiler decisions become concrete symbols, call paths, layouts, and artifact size—and which observations are stable enough to guide design?
98. [Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration](module-98-verification-beyond-examples-compile-fail-property-model-fuzz-miri-and-concurrency-exploration/index.md) — Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof?
99. [Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship](module-99-long-lived-apis-semver-msrv-features-migrations-and-workspace-stewardship/index.md) — How do you evolve a Rust library, data format, feature graph, and workspace without silently breaking downstream source, behavior, tools, or stored data?
100. [Architectural Synthesis: Building and Defending a Long-Lived Rust System](module-100-architectural-synthesis-building-and-defending-a-long-lived-rust-system/index.md) — Can you turn ten courses of mechanisms into one restrained architecture whose guarantees, unsafe core, verification evidence, compatibility policy, and operating limits can survive independent review?

## One continuous AxiomStore story

AxiomStore starts as a deliberately plain owned record engine. Each day changes one proof boundary:

| Day | AxiomStore increment | New responsibility |
|---:|---|---|
| 1 | compiler evidence notebook | source, control flow, drops, and artifact observations are separated |
| 2 | codec and validation goal graph | associated families and equality constraints become explicit |
| 3 | borrowed record views | each snapshot borrow selects its own view family |
| 4 | bounded local representation | capacity and checked witnesses acquire clear ownership |
| 5 | runtime validator registry | static codecs and erased policy occupy different boundaries |
| 6 | inline transaction batch | one small unsafe state machine receives a complete dossier |
| 7 | dispatch and code-size observatory | source architecture is connected to one pinned artifact |
| 8 | verification matrix | every invariant receives the strongest suitable evidence |
| 9 | compatibility and migration policy | source, features, MSRV, and stored bytes evolve deliberately |
| 10 | AXIOM02 extension and defense | the whole architecture absorbs an unseen cross-cutting change |

## How to study

Follow one dense day per module:

```text
authoritative chapter
    → frozen predictions
    → causal repairs
    → focused construction
    → independent laboratory
    → AxiomStore increment
    → reasoned solutions
    → closed-book defense
```

Do not start by opening unstable compiler dumps or adding advanced syntax. Start with the product claim and the module’s reasoning artifact. Use tools only when their representation can answer the question. Every day ends with one page recording the selected mechanism, simpler rejected alternative, proof owner, verification evidence, compatibility effect, and remaining risk.

## Course surfaces

- [Ten-day study plan](study-plan.md)
- [AxiomStore engineering guide](capstone.md)
- [Advanced Rust reference desk](reference.md)
- [Final independent review](final-review.md)
- [Compiler investigations](../compiler-labs/README.md)
- [Independent laboratories](../labs/)

## Completion standard

Course 10 is complete when you can implement the AXIOM02 extension without step-by-step instructions and defend AxiomStore before an independent reviewer. Passing tests is necessary but insufficient. You must show:

- a coherent invariant ownership map;
- causal negative evidence for type-level boundaries;
- a complete unsafe safety dossier;
- model, property, fixture, and process evidence appropriate to each claim;
- a compatibility matrix covering current and legacy bytes;
- artifact-scoped code-generation observations;
- a restrained public API;
- explicit residual risk.
