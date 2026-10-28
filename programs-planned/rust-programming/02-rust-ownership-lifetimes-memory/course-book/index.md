# Course 2 — Ownership, Lifetimes, and Memory

## Provenance, Liveness, Representation, and Address Stability

Deepen ownership until borrowed APIs, cleanup protocols, shared graphs, interior mutation, representation claims, variance, and pinning can be designed from first principles rather than folklore.

## Why this course exists

Course 1 taught the visible ownership rules needed for ordinary programs. Real libraries expose borrowed views, return resources through guards, share immutable snapshots, cache behind shared references, and sometimes depend on representation or address stability. Those designs fail when lifetimes are treated as annotations to appease the compiler or smart pointers are selected by habit. This course refines the unit of reasoning from a whole value to places, loans, liveness edges, initialization states, and substitution capabilities.

## Before you begin

Course 1, including confident ownership tracing, borrowing, enums, `Option`/`Result`, collections, foundational traits and lifetimes, modules, and tests.

Keep a place/loan graph, lifetime relationship map, cleanup state machine, and liveness graph beside the code. The record changes shape as the course advances, but its purpose is constant: make the decisive relationship visible before syntax hides it.

## What you will be able to do

- Distinguish values from places and trace projections, move paths, partial moves, partial initialization, reborrowing, and later destruction obligations.
- Model loans over places and explain when fields, indices, slices, and method receivers can or cannot be borrowed disjointly.
- Translate lifetime syntax into provenance and outlives constraints, derive elision, and keep unrelated lifetimes independent.
- Design borrowed return types and reference-bearing structures whose relationships are neither under-specified nor unnecessarily coupled.
- Use higher-ranked callback bounds and scoped APIs when each call needs a fresh lifetime that must not escape.
- Derive destruction order and encode cleanup, rollback, commit, and failure atomicity through RAII guards and consuming transitions.
- Choose `Box`, dereference coercion, dynamically sized types, and `Cow` according to representation and ownership rather than as generic indirection tools.
- Design `Rc`/`Weak` ownership graphs by naming strong liveness roots, observer edges, cycle risks, identity, and teardown behavior.
- Use `Cell` and `RefCell` only when hidden mutation is justified; keep runtime borrow guards short and prevent reentrant borrow failure.
- Separate semantic validity, layout guarantees, target-conditioned observations, implementation details, and unsupported representation assumptions.
- Derive covariance, contravariance, and invariance from capability substitution rather than memorized container lists.
- Use `PhantomData` to communicate ownership, borrowing, variance, drop checking, and auto-trait relationships accurately.
- Recognize when an invariant is genuinely address-sensitive, construct and project pinned values safely, and reject ceremonial pinning.
- Choose runtime generations, static brands, ownership, indirection, or pinning according to the exact identity and validity problem.
- Defend a memory-oriented API with a provenance map, liveness graph, failure-state analysis, and evidence that matches the strength of each claim.

## What this course deliberately leaves for later

The course remains primarily safe Rust. It explains representation and address-sensitive contracts but reserves raw pointers, allocation APIs, FFI, and production unsafe abstraction construction for Course 6.

## Ten-day route

1. [Module 11: Places, Move Paths, and Advanced Borrowing](module-11-places-move-paths-and-advanced-borrowing/index.md) — Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?
2. [Module 12: Lifetime Relationships and Borrowed APIs](module-12-lifetime-relationships-and-borrowed-apis/index.md) — What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?
3. [Module 13: Scoped Access and Escape Prevention](module-13-scoped-access-and-escape-prevention/index.md) — Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?
4. [Module 14: RAII, Drop, Unwinding, and Failure Atomicity](module-14-raii-drop-unwinding-and-failure-atomicity/index.md) — Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?
5. [Module 15: Box, Deref, Dynamically Sized Types, and Cow](module-15-box-deref-dynamically-sized-types-and-cow/index.md) — When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?
6. [Module 16: Rc, Weak, and Ownership Graphs](module-16-rc-weak-and-ownership-graphs/index.md) — Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?
7. [Module 17: Interior Mutability and Runtime Borrows](module-17-interior-mutability-and-runtime-borrows/index.md) — Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?
8. [Module 18: Memory Representation, Validity, and Layout](module-18-memory-representation-validity-and-layout/index.md) — Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?
9. [Module 19: Subtyping, Variance, PhantomData, and Drop Checking](module-19-subtyping-variance-phantomdata-and-drop-checking/index.md) — When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?
10. [Module 20: Pinning and Address-Sensitive Design](module-20-pinning-and-address-sensitive-design/index.md) — What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?

## How the learning surfaces fit

The chapter is the authoritative explanation. The workbook exposes the model you actually hold through prediction, repair, construction, transfer, and defense. The independent lab removes accumulated capstone complexity so one mechanism remains visible. The capstone increment then asks that mechanism to coexist with every earlier decision.

The cumulative product is **Memory Workspace**: an in-memory document workspace with generational handles, borrowed views, revision-checked edits, snapshots, weak observers, caches, and explicit memory claims. Do not read the complete implementation before attempting the corresponding increment; the value of the capstone is the sequence of design decisions, not possession of the finished source.

Use the [compiler investigations](../compiler-labs/README.md), the [ten-day study plan](study-plan.md), the [Memory Workspace engineering guide](capstone.md), the [course reference](reference.md), and the [independent final review](final-review.md).

## Completion standard

The course is complete when you can satisfy the public behavior, explain the decisive rule without notes, repair a misleading implementation without weakening its requirement, and transfer the mechanism to the final independent product. A passing test suite without a causal model is incomplete; a persuasive explanation without working evidence is also incomplete.

## Course handoff

Course 3 turns the memory contracts established here into trait contracts, polymorphic boundaries, typestate protocols, and evolvable public architecture.

[Return to the program start](../../README.md) · [Open the sixty-module map](../../COURSE_MAP.md)
