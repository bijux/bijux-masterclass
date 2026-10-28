# Course 2 study plan — Ownership, Lifetimes, and Memory

This plan turns ten chapters into ten days of deliberate practice. A day is complete only when the model, independent laboratory, and Memory Workspace increment agree. If the lab passes while the explanation remains vague, repair the model before moving on.

## Daily rhythm

| Time | Work | Required output |
|---|---|---|
| 08:30–09:00 | closed-book reconstruction | one page of the previous mechanism from memory |
| 09:00–11:00 | authoritative chapter and typed examples | annotated model and changed-assumption predictions |
| 11:15–12:30 | compiler or boundary specimens | frozen predictions and causal comparison |
| 13:30–15:00 | repair and focused construction | smallest principled repair plus rejected shortcut |
| 15:15–17:30 | independent laboratory | working behavior, adversarial tests, design record |
| 18:30–20:00 | Memory Workspace increment | integrated change and regression evidence |
| 20:00–20:30 | explanation and retrieval | invariant, decisive rule, failure state, transfer case |

Take real breaks. Dense work is not continuous screen time. The weekend between Days 5 and 6 is for repair, reconstruction, and rest rather than new material.

## Day 1 — Places, Move Paths, and Advanced Borrowing

**Governing question:** Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?

### Morning: derive the model

Read [Module 11](module-11-places-move-paths-and-advanced-borrowing/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-11-places-move-paths-and-advanced-borrowing/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 11 — Borrow Surgery](../labs/module-01-borrow-surgery/README.md). Implement the package in `labs/module-01-borrow-surgery/starter` without reading the solution.

### Evening: integrate the course product

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Represent workspace slots with generational handles and keep mutable access narrower than the whole workspace. Stale identity and current ownership are separate concerns. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 2 — Lifetime Relationships and Borrowed APIs

**Governing question:** What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?

### Morning: derive the model

Read [Module 12](module-12-lifetime-relationships-and-borrowed-apis/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-12-lifetime-relationships-and-borrowed-apis/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 12 — Zero-Copy Records](../labs/module-02-zero-copy-records/README.md). Implement `labs/module-02-zero-copy-records/starter`.

### Evening: integrate the course product

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Expose document views and search excerpts that borrow from workspace-owned text. Derive every output lifetime from the owner that actually supplies the bytes. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Translate lifetime syntax into constraints among borrows rather than durations attached to values;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 3 — Scoped Access and Escape Prevention

**Governing question:** Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?

### Morning: derive the model

Read [Module 13](module-13-scoped-access-and-escape-prevention/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-13-scoped-access-and-escape-prevention/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 13 — Scoped Visitors](../labs/module-03-scoped-visitors/README.md). Build `ScopedText`, a safe text-processing component that owns one reusable scratch buffer and exposes transformed records only inside callback scope.

### Evening: integrate the course product

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Normalize temporary queries through a scoped callback so borrowed results cannot escape. The API should permit useful work while making invalid retention unexpressible. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish caller-chosen named lifetimes from fresh lifetimes generated independently for each callback invocation;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 4 — RAII, Drop, Unwinding, and Failure Atomicity

**Governing question:** Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?

### Morning: derive the model

Read [Module 14](module-14-raii-drop-unwinding-and-failure-atomicity/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-14-raii-drop-unwinding-and-failure-atomicity/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 14 — RAII Resource Pool](../labs/module-04-resource-pool/README.md). Build a generic single-threaded resource pool whose checked-out item is owned by a lease guard and automatically returned unless an explicit consuming transition says otherwise.

### Evening: integrate the course product

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Add staged edit sessions whose owned candidate state can be committed or abandoned. A failed commit must preserve the documented state without relying on fallible destructors. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Derive local, field, tuple, temporary, and scope destruction order from documented rules;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 5 — Box, Deref, Dynamically Sized Types, and Cow

**Governing question:** When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?

### Morning: derive the model

Read [Module 15](module-15-box-deref-dynamically-sized-types-and-cow/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-15-box-deref-dynamically-sized-types-and-cow/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 15 — Boxed Expression Tree](../labs/module-05-boxed-expressions/README.md). Build a typed arithmetic expression tree with minimal recursive indirection.

### Evening: integrate the course product

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Introduce immutable snapshots and conditional query ownership. Use `Box` or `Cow` only where the product needs indirection or conditional allocation. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 6 — Rc, Weak, and Ownership Graphs

**Governing question:** Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?

### Morning: derive the model

Read [Module 16](module-16-rc-weak-and-ownership-graphs/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-16-rc-weak-and-ownership-graphs/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 16 — Shared Ownership Graph](../labs/module-06-rc-weak-graph/README.md). Build an immutable/shared project tree with strong child ownership, weak parent backlinks, and weak external observers.

### Evening: integrate the course product

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Store snapshots with strong ownership, expose weak observers, and define eviction. Draw the liveness graph and prove that observers do not keep snapshots alive. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 7 — Interior Mutability and Runtime Borrows

**Governing question:** Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?

### Morning: derive the model

Read [Module 17](module-17-interior-mutability-and-runtime-borrows/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-17-interior-mutability-and-runtime-borrows/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 17 — Revisioned Interior Cache](../labs/module-07-interior-cache/README.md). Build `IndexedText`, an editable string with a lazily computed line-start index.

### Evening: integrate the course product

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Add a revision-aware line cache with short `RefCell` guard scopes and explicit hit/miss behavior. No callback may run while a mutable runtime borrow is held. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 8 — Memory Representation, Validity, and Layout

**Governing question:** Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?

### Morning: derive the model

Read [Module 18](module-18-memory-representation-validity-and-layout/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-18-memory-representation-validity-and-layout/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 18 — Layout Observatory](../labs/module-08-layout-observatory/README.md). Build a safe executable/library that records layout observations while refusing to present them as universal guarantees.

### Evening: integrate the course product

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Produce a memory report with formulas, target observations, and explicit exclusions. Do not present `size_of` observations as a complete allocation or ABI account. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Separate semantic value, validity invariant, abstract layout guarantee, ABI promise, and measured observation;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 9 — Subtyping, Variance, PhantomData, and Drop Checking

**Governing question:** When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?

### Morning: derive the model

Read [Module 19](module-19-subtyping-variance-phantomdata-and-drop-checking/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-19-subtyping-variance-phantomdata-and-drop-checking/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 19 — Variance Branding](../labs/module-09-variance-branding/README.md). Build a scoped arena whose IDs cannot be mixed across arena instances created by separate brand scopes.

### Evening: integrate the course product

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Review runtime generational handles against a branded alternative. Explain which invalid combinations each technique prevents and which stale-state problem remains runtime data. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?”—without reading the chapter;
- demonstrate this outcome on a fresh example: State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;

## Day 10 — Pinning and Address-Sensitive Design

**Governing question:** What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?

### Morning: derive the model

Read [Module 20](module-20-pinning-and-address-sensitive-design/index.md). Reconstruct the central example in a new file, then change one assumption that affects this module’s decisive relationship. Write the prediction before compiling and record the earliest phase that can establish the result.

### Midday: predict and repair

Complete the [workbook](module-20-pinning-and-address-sensitive-design/workbook.md). Preserve the product requirement during every repair. Keep the smallest counterexample that exposed a wrong model; it becomes part of the final explanation rather than disposable scratch work.

### Afternoon: isolate the mechanism

Build [Laboratory 20 — Pinned Tracker](../labs/module-10-pinned-tracker/README.md). Build an address-sensitive tracker that can be initialized only after pinning and can then report whether every observation occurs at its initialized address. The implementation remains entirely safe Rust.

### Evening: integrate the course product

The course capstone is **Memory Workspace**, an in-memory document workspace with handles, snapshots, edit sessions, and caches. Conduct an address-sensitivity review and reject pinning unless an invariant truly depends on stable location. Defend the simpler architecture when handles and indirection suffice. The exact implementation task is in the workbook; the full product contract is in the capstone guide.

### End-of-day proof

Do not advance merely because the code passes. Close the chapter and produce the following without notes:

- answer the module question—“What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?”—without reading the chapter;
- demonstrate this outcome on a fresh example: Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants;
- repair the debugging case while preserving its product requirement;
- complete the laboratory transfer variant and explain the decisive design choice;


## Mid-course reconstruction

After Day 5, rebuild the five-module dependency chain without notes. Select the two compiler specimens that changed your model most, rerun them, and explain why the wrong prediction was plausible. Repair every incomplete lab before opening Day 6; later mechanisms assume that the earlier contract is stable.

## Final consolidation

After Day 10, use the [course reference](reference.md) to compress the material, not to relearn it. Complete the [final review](final-review.md) from an empty directory. Then defend Memory Workspace by tracing one successful operation and one adversarial failure through every layer touched by the course.
