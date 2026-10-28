# Course 2 — Ownership, Lifetimes, and Memory

## Provenance, Resource Protocols, and Address-Sensitive Design

Course 2 turns the ownership rules from Course 1 into a design language for memory. You learn to derive borrow relationships, reason about cleanup and unwinding, choose smart pointers by liveness topology, use interior mutability without hiding reentrancy hazards, and distinguish semantic guarantees from layout observations.

> **Governing question:** How do places, loans, lifetimes, destruction, shared liveness, representation, and address stability determine whether a memory design is valid?

## Entry point

You should be able to build and test a complete safe-Rust program, explain moves and ordinary borrows, use structs and enums, propagate errors, and organize a library and binary.

The immediate prerequisite is [Course 1: Rust Foundations](../01-rust-foundations/course-book/index.md). Entering mid-program is reasonable only when you can complete the previous course’s final review and one independent construction without following its solution.

## Ten-day route

| Day | Module | Capability added | Independent laboratory |
|---:|---|---|---|
| 1 | [11 — Places, Move Paths, and Advanced Borrowing](course-book/module-11-places-move-paths-and-advanced-borrowing/index.md) | Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations | [Borrow Surgery](labs/module-01-borrow-surgery/README.md) |
| 2 | [12 — Lifetime Relationships and Borrowed APIs](course-book/module-12-lifetime-relationships-and-borrowed-apis/index.md) | Translate lifetime syntax into constraints among borrows rather than durations attached to values | [Zero-Copy Records](labs/module-02-zero-copy-records/README.md) |
| 3 | [13 — Scoped Access and Escape Prevention](course-book/module-13-scoped-access-and-escape-prevention/index.md) | Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation | [Scoped Visitors](labs/module-03-scoped-visitors/README.md) |
| 4 | [14 — RAII, Drop, Unwinding, and Failure Atomicity](course-book/module-14-raii-drop-unwinding-and-failure-atomicity/index.md) | Derive local, field, tuple, temporary, and scope destruction order from documented rules | [RAII Resource Pool](labs/module-04-resource-pool/README.md) |
| 5 | [15 — Box, Deref, Dynamically Sized Types, and Cow](course-book/module-15-box-deref-dynamically-sized-types-and-cow/index.md) | Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership | [Boxed Expression Tree](labs/module-05-boxed-expressions/README.md) |
| 6 | [16 — Rc, Weak, and Ownership Graphs](course-book/module-16-rc-weak-and-ownership-graphs/index.md) | Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts | [Shared Ownership Graph](labs/module-06-rc-weak-graph/README.md) |
| 7 | [17 — Interior Mutability and Runtime Borrows](course-book/module-17-interior-mutability-and-runtime-borrows/index.md) | Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs | [Revisioned Interior Cache](labs/module-07-interior-cache/README.md) |
| 8 | [18 — Memory Representation, Validity, and Layout](course-book/module-18-memory-representation-validity-and-layout/index.md) | Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation | [Layout Observatory](labs/module-08-layout-observatory/README.md) |
| 9 | [19 — Subtyping, Variance, PhantomData, and Drop Checking](course-book/module-19-subtyping-variance-phantomdata-and-drop-checking/index.md) | State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally | [Variance Branding](labs/module-09-variance-branding/README.md) |
| 10 | [20 — Pinning and Address-Sensitive Design](course-book/module-20-pinning-and-address-sensitive-design/index.md) | Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants | [Pinned Tracker](labs/module-10-pinned-tracker/README.md) |

The route is cumulative. Day 1 establishes this course’s vocabulary and Day 10 requires an architectural change that preserves all earlier guarantees.

## Working method

Draw places, loans, outlives relations, destruction, and liveness before selecting a pointer type. Use the module-specific reasoning record named in each chapter. Freeze predictions before compiling, preserve causal diagnostics, and compare the lab reference only after recording your own design.

## Capstone — Memory Workspace

Memory Workspace is a single-threaded document workspace with generational handles, borrowed views, staged edits, snapshots, weak observers, caches, and explicit memory accounting. Every feature exists to make an ownership or lifetime relationship observable.

The [engineering guide](course-book/capstone.md) supplies the ten integration steps. The executable [capstone directory](capstone/README.md) contains the product and tests. Each increment must name the changed invariant, the component that owns it, state after failure, and the earlier guarantee that must remain unchanged.

## Scope

The course remains centered on safe public APIs. It explains the memory obligations behind smart pointers, interior mutability, layout, variance, and pinning, but manual allocation, raw-pointer implementation, FFI, threads, and async execution remain later responsibilities.

Course 3 asks how several types can promise lawful behavior and how those contracts shape an architecture that can vary and evolve.

## Exit standard

Complete this independent construction:

> Build a revisioned record store with borrowed queries, generational identity, a staged mutation protocol, shared immutable snapshots, and a written liveness and cleanup analysis.

Then complete this capstone extension:

> Add document labels and snapshot comparison to Memory Workspace while preserving stale-handle rejection, bounded retention, and borrowed-view provenance.

The next step is [Course 3: Traits, Generics, and Architectural Design](../03-rust-traits-generics-architectural-design/course-book/index.md).

## Reading and execution routes

- [Course book](course-book/index.md)
- [Ten-day study plan](course-book/study-plan.md)
- [Course reference](course-book/reference.md)
- [Final review](course-book/final-review.md)
- [Compiler and design investigations](compiler-labs/README.md)
- [Laboratories](labs/)

```bash
make static-proof
make compiler-labs
make check
make test
make starters
make docs
make proof
```

Static inspection and compilation answer different questions. The strongest completion route uses the pinned toolchain, executes tests and investigations, renders the book, and preserves the resulting evidence with the code under review.
