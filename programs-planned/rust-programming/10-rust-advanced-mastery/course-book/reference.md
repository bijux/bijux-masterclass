# Advanced Rust Reference Desk

This page is for retrieval after you have completed the derivations. It compresses the ten module records, decision rules, and boundaries. Do not use it as a substitute for the authoritative chapters.

## Claim categories

| Category | Typical evidence | What remains outside it |
|---|---|---|
| language legality | compiler acceptance or causal rejection | product suitability and runtime data |
| lifetime/type API | positive and compile-fail fixtures | implementation soundness beyond the interface |
| runtime invariant | constructors, transition tests, model comparison | unexecuted states and external failures |
| unsafe soundness | written proof, adversarial tests, Miri evidence | universal proof of unvisited paths |
| compatibility | downstream fixtures, MSRV/features, golden bytes | unknown third-party assumptions |
| artifact behavior | pinned build, symbols, layout, benchmark | portability to another toolchain or target |
| architecture | invariant map, alternatives, evidence matrix | future requirements and residual risk |

## Module 91 — Reading Rust Through the Compiler: HIR, MIR, Borrow Checking, and Codegen

**Question:** When difficult Rust code surprises you, which compiler representation and which proof obligation actually decide the result?

**Primary record:** compiler evidence ledger.

**Use when:** separate parsing, name resolution, type checking, trait solving, borrow checking, monomorphization, optimization, and linking as distinct explanatory phases.

**Do not infer:** successful compilation or one tool observation does not establish the complete product, compatibility, safety, or performance claim.

**Fast review:**

- Why is this method selected? → resolved receiver, autoderef/autoref, and trait candidates
- Why does this borrow conflict? → place projections, access kinds, and loan liveness across control flow
- When is a value destroyed? → initialization state and normal/unwind exit edges
- Did abstraction add runtime cost? → equivalent artifact, symbols, assembly, and profile evidence

## Module 92 — Advanced Trait Solving: Goals, Projections, and Type Equality

**Question:** How do you design and debug APIs when the compiler must prove nested trait goals and normalize associated types before ordinary operations become legal?

**Primary record:** trait-goal graph.

**Use when:** rewrite a complex generic error as a small set of trait goals, projection goals, and equality constraints.

**Do not infer:** successful compilation or one tool observation does not establish the complete product, compatibility, safety, or performance claim.

**Fast review:**

- Who chooses a related type? → associated type when the implementation owns one relationship
- Where should equality be required? → the composition site connecting two components
- Why is selection ambiguous? → missing input evidence, competing impls, or unconstrained parameter
- Should errors be erased? → the boundary that owns stable recovery policy

## Module 93 — GATs, Higher-Ranked Bounds, and Lending Interfaces

**Question:** How can an API return views tied to each borrow of `self` without pretending that every yielded value has one fixed lifetime?

**Primary record:** lifetime quantifier map.

**Use when:** distinguish one associated type from a lifetime-indexed family of associated types.

**Do not infer:** successful compilation or one tool observation does not establish the complete product, compatibility, safety, or performance claim.

**Fast review:**

- Does each borrow create a distinct view type? → a lifetime-indexed associated family
- May the consumer retain the value? → owned output or explicit conversion
- Must a callback accept every temporary lifetime? → a higher-ranked `for<'a>` bound
- Must the component be dynamically erased? → move erasure after conversion to an owned stable type

## Module 94 — Const Generics, Witness Types, and Compile-Time Invariants

**Question:** Which numeric and state facts belong in types, which remain runtime data, and how do you avoid turning a library into an unusable type-level calculator?

**Primary record:** compile-time/runtime invariant table.

**Use when:** use const parameters when a numeric fact changes representation, layout, or legal composition.

**Do not infer:** successful compilation or one tool observation does not establish the complete product, compatibility, safety, or performance claim.

**Fast review:**

- Does the value alter representation or legal composition? → const generic or witness type
- Is the value loaded from data and frequently variable? → runtime validation and private checked state
- Is a slot initialized? → runtime length and transition invariant
- Do callers need the proof in their types? → public witness with private construction

## Module 95 — Opaque and Erased Types: impl Trait, dyn Trait, Any, and Plugin Boundaries

**Question:** When should an API hide one concrete type, erase many concrete types behind a contract, or preserve explicit variants—and what information is lost at each boundary?

**Primary record:** variation and erasure map.

**Use when:** distinguish opaque return types from trait objects and explain why different branches of `impl Trait` must share one hidden concrete type.

**Do not infer:** successful compilation or one tool observation does not establish the complete product, compatibility, safety, or performance claim.

**Fast review:**

- Is there one hidden concrete return type? → `impl Trait`
- Is runtime open extension required? → `dyn Trait` with deliberate ownership
- Is the variant set centrally governed? → enum
- Is only type identity available? → `Any` with explicit downcast policy

## Module 96 — Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits

**Question:** What exact proof makes a safe API implemented with unsafe code sound across every constructor, method, failure path, destructor, and thread-safety claim?

**Primary record:** unsafe abstraction safety dossier.

**Use when:** write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation.

**Do not infer:** successful compilation or one tool observation does not establish the complete product, compatibility, safety, or performance claim.

**Fast review:**

- Can safe Rust express the required representation? → prefer the safe design unless measured/product evidence justifies unsafe
- Which slots contain live values? → one explicit initialized-state invariant
- Can user code run while invariants are broken? → reorder transitions or install a cleanup guard
- May the type cross threads? → derive or explicitly prevent auto traits; manually assert only with a full race proof

## Module 97 — From Source to Machine Code: Monomorphization, Dispatch, Layout, and Code Size

**Question:** How do type-level architecture and compiler decisions become concrete symbols, call paths, layouts, and artifact size—and which observations are stable enough to guide design?

**Primary record:** source-to-artifact observation record.

**Use when:** explain when generic functions are monomorphized and why source-level abstraction does not determine final code duplication.

**Do not infer:** successful compilation or one tool observation does not establish the complete product, compatibility, safety, or performance claim.

**Fast review:**

- Does variation need open runtime extension? → trait object if the product requires it
- Is code duplication material? → symbol and section evidence for representative instantiations
- Does layout require a guarantee? → documented repr for FFI/unsafe contract
- Did optimization move or remove cost? → equivalent semantics plus profile and assembly evidence

## Module 98 — Verification Beyond Examples: Compile-Fail, Property, Model, Fuzz, Miri, and Concurrency Exploration

**Question:** Which verification technique can falsify which kind of Rust claim, and how do you combine them without pretending that test volume equals proof?

**Primary record:** claim-to-evidence verification matrix.

**Use when:** classify claims as type-level, functional, algebraic, state-machine, memory-safety, concurrency, compatibility, or performance claims.

**Do not infer:** successful compilation or one tool observation does not establish the complete product, compatibility, safety, or performance claim.

**Fast review:**

- Is misuse supposed to be unrepresentable? → compile-fail evidence and visibility review
- Is behavior algebraic over many values? → property or differential tests
- Is the component a finite transition system? → model exploration after every step
- Does the claim concern unsafe execution? → written proof plus adversarial tests and Miri where available

## Module 99 — Long-Lived APIs: SemVer, MSRV, Features, Migrations, and Workspace Stewardship

**Question:** How do you evolve a Rust library, data format, feature graph, and workspace without silently breaking downstream source, behavior, tools, or stored data?

**Primary record:** compatibility and migration matrix.

**Use when:** analyze a proposed change from the perspectives of downstream callers, downstream implementors, type inference, pattern matching, and stored data.

**Do not infer:** successful compilation or one tool observation does not establish the complete product, compatibility, safety, or performance claim.

**Fast review:**

- Who can break? → analyze callers, implementors, inference, matches, data, and tools separately
- Is a feature additive? → it adds capability under feature unification
- Is MSRV a real promise? → execute supported feature/workspace checks on the declared minimum
- How does stored data evolve? → versioned read/write policy and failure-atomic migration

## Module 100 — Architectural Synthesis: Building and Defending a Long-Lived Rust System

**Question:** Can you turn ten courses of mechanisms into one restrained architecture whose guarantees, unsafe core, verification evidence, compatibility policy, and operating limits can survive independent review?

**Primary record:** architecture defense dossier.

**Use when:** construct an invariant map connecting product claims to types, runtime validation, synchronization, unsafe proofs, tests, and operational policy.

**Do not infer:** successful compilation or one tool observation does not establish the complete product, compatibility, safety, or performance claim.

**Fast review:**

- Which component owns each invariant? → one primary type, transition, codec, or policy owner
- Does an advanced mechanism earn its proof cost? → retain only when it removes a material invalid state or boundary ambiguity
- What is public? → stable behavior and deliberate extension points
- What evidence supports release? → claim-specific verification and explicit residual risk

## Final retrieval checklist

Before approving an advanced Rust design, ask:

1. What requirement cannot be expressed more simply?
2. Who owns each type, value, policy, version, and extension choice?
3. Which phase or runtime event establishes the claim?
4. Which unsafe or external assumptions remain?
5. What happens after every failure and panic?
6. Which downstream code or data becomes a compatibility stakeholder?
7. Which evidence can falsify the claim?
8. What evidence is artifact-specific or time-limited?
9. Which advanced mechanism was deliberately rejected?
10. What residual risk should the next maintainer see immediately?
