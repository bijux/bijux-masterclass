# Course 2 — Ownership, Lifetimes, and Memory

## Provenance, Resource Protocols, and Address-Sensitive Design

## The promise

Course 2 turns the ownership rules from Course 1 into a design language for memory. You learn to derive borrow relationships, reason about cleanup and unwinding, choose smart pointers by liveness topology, use interior mutability without hiding reentrancy hazards, and distinguish semantic guarantees from layout observations.

> **Governing question:** How do places, loans, lifetimes, destruction, shared liveness, representation, and address stability determine whether a memory design is valid?

Course 1 established complete safe-Rust programs: typed state, explicit ownership, recoverable failure, deterministic persistence, tests, and a library/binary boundary. Course 2 keeps those guarantees and makes the underlying memory relationships explicit—places, loans, lifetimes, cleanup, shared liveness, representation, and address stability.

## Before Day 1

You should be able to build and test a complete safe-Rust program, explain moves and ordinary borrows, use structs and enums, propagate errors, and organize a library and binary.

From a blank page, sketch one earlier product or a comparable program. Mark an owner, a valid and invalid state, a failure path, cleanup, and a public promise. Repair any relationship you cannot explain before adding this course’s mechanisms.

## Outcomes

- Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations.
- Translate lifetime syntax into constraints among borrows rather than durations attached to values.
- Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation.
- Derive local, field, tuple, temporary, and scope destruction order from documented rules.
- Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership.
- Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts.
- Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs.
- Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation.
- State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally.
- Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants.
- Integrate all ten mechanisms in Memory Workspace without creating competing authorities.
- Complete and defend an unseen change using a pinning contract.

## The ten-day line

| Day | Module | Governing question | Capability that must become visible | Laboratory |
|---:|---|---|---|---|
| 1 | [11 — Places, Move Paths, and Advanced Borrowing](./module-11-places-move-paths-and-advanced-borrowing/index.md) | Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely? | **Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations.** | [Borrow Surgery](../labs/module-01-borrow-surgery/README.md) |
| 2 | [12 — Lifetime Relationships and Borrowed APIs](./module-12-lifetime-relationships-and-borrowed-apis/index.md) | What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent? | **Translate lifetime syntax into constraints among borrows rather than durations attached to values.** | [Zero-Copy Records](../labs/module-02-zero-copy-records/README.md) |
| 3 | [13 — Scoped Access and Escape Prevention](./module-13-scoped-access-and-escape-prevention/index.md) | Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable? | **Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation.** | [Scoped Visitors](../labs/module-03-scoped-visitors/README.md) |
| 4 | [14 — RAII, Drop, Unwinding, and Failure Atomicity](./module-14-raii-drop-unwinding-and-failure-atomicity/index.md) | Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic? | **Derive local, field, tuple, temporary, and scope destruction order from documented rules.** | [RAII Resource Pool](../labs/module-04-resource-pool/README.md) |
| 5 | [15 — Box, Deref, Dynamically Sized Types, and Cow](./module-15-box-deref-dynamically-sized-types-and-cow/index.md) | When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally? | **Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership.** | [Boxed Expression Tree](../labs/module-05-boxed-expressions/README.md) |
| 6 | [16 — Rc, Weak, and Ownership Graphs](./module-16-rc-weak-and-ownership-graphs/index.md) | Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear? | **Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts.** | [Shared Ownership Graph](../labs/module-06-rc-weak-graph/README.md) |
| 7 | [17 — Interior Mutability and Runtime Borrows](./module-17-interior-mutability-and-runtime-borrows/index.md) | Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled? | **Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs.** | [Revisioned Interior Cache](../labs/module-07-interior-cache/README.md) |
| 8 | [18 — Memory Representation, Validity, and Layout](./module-18-memory-representation-validity-and-layout/index.md) | Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption? | **Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation.** | [Layout Observatory](../labs/module-08-layout-observatory/README.md) |
| 9 | [19 — Subtyping, Variance, PhantomData, and Drop Checking](./module-19-subtyping-variance-phantomdata-and-drop-checking/index.md) | When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate? | **State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally.** | [Variance Branding](../labs/module-09-variance-branding/README.md) |
| 10 | [20 — Pinning and Address-Sensitive Design](./module-20-pinning-and-address-sensitive-design/index.md) | What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely? | **Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants.** | [Pinned Tracker](../labs/module-10-pinned-tracker/README.md) |

The table is a dependency chain, not a menu. A later module may use an earlier mechanism but may not silently weaken its ownership, failure, ordering, capacity, safety, compatibility, or evidence contract.

## Decision rules

| Decision | Rule used throughout this course |
|---|---|
| Borrow relation | Name the owner and prove every returned reference originates from data that remains alive. |
| Cleanup protocol | Assign every resource acquisition exactly one cleanup owner and trace unwind paths. |
| Shared liveness | Use strong edges for ownership and weak edges for observation or back-links. |
| Interior mutability | Use runtime loans only when the call graph and reentrancy policy are explicit. |
| Pinning | Use pinning only when the pointee has a genuine address-sensitive invariant after pinning. |

Use these rules during prediction and review. When a rule does not decide the case, write the missing product requirement instead of selecting an API by habit.

## The reasoning record

The ten module-specific records culminate in a **pinning contract**. Draw places, loans, outlives relations, destruction, and liveness before selecting a pointer type. Keep the record small enough to inspect but complete enough to expose the first unsupported assumption.

## Scope and handoff

The course remains centered on safe public APIs. It explains the memory obligations behind smart pointers, interior mutability, layout, variance, and pinning, but manual allocation, raw-pointer implementation, FFI, threads, and async execution remain later responsibilities.

Course 3 asks how several types can promise lawful behavior and how those contracts shape an architecture that can vary and evolve.

## Capstone — Memory Workspace

Memory Workspace is a single-threaded document workspace with generational handles, borrowed views, staged edits, snapshots, weak observers, caches, and explicit memory accounting. Every feature exists to make an ownership or lifetime relationship observable.

Open the [engineering guide](capstone.md) before Day 1 so the final architecture is visible. Implement only the current increment. The independent laboratory remains separate so that the mechanism can be learned without hiding behind accumulated capstone code.

## Completion

The course is complete when you can build and defend:

> Build a revisioned record store with borrowed queries, generational identity, a staged mutation protocol, shared immutable snapshots, and a written liveness and cleanup analysis.

and then change the capstone under this constraint:

> Add document labels and snapshot comparison to Memory Workspace while preserving stale-handle rejection, bounded retention, and borrowed-view provenance.

A passing test suite is necessary. It is not sufficient unless you can explain why the tests are capable of falsifying the claim and which target-, scheduler-, workload-, peer-, or policy-dependent facts remain outside them.

## Continue

- [Ten-day plan](study-plan.md)
- [Module 11 — Places, Move Paths, and Advanced Borrowing](./module-11-places-move-paths-and-advanced-borrowing/index.md)
- [Memory Workspace engineering guide](capstone.md)
- [Course reference](reference.md)
- [Final review](final-review.md)
- [Compiler and design investigations](../compiler-labs/README.md)
- [Independent laboratories](../labs/)
