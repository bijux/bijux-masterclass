# Module 96 Workbook — Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits

[Chapter](index.md) · [AxiomStore guide](../capstone.md) · [Solutions](solutions.md)

This workbook turns the chapter’s **soundness dossier** into evidence. Write predictions before compiling or running anything. Preserve the stated product requirement during repair; a green build obtained by deleting the difficult relationship is not a solution.

## Part 1 — Predict

For each case, submit: expected category (`compile-pass`, `compile-fail`, `run-pass`, `run-fail`, or `manual-review`), first decisive phase or event, governing relationship, and the strongest conclusion the outcome would justify.

Your prediction sheet must make the soundness dossier visible. For one case, change exactly one assumption and explain why the decisive phase or outcome moves.

### Prediction 1 — Publish before initialize

`push` increments `len` and then writes into `MaybeUninit<T>`. A panic is injected between the steps. Predict the later drop behavior.

### Prediction 2 — Pop ordering

`pop` reads the final slot with `assume_init_read` and decrements `len` afterward. What happens if code between those operations panics?

### Prediction 3 — Slice formation

An implementation forms `&[T]` over all `N` slots while only `len` are initialized. Predict soundness.

### Prediction 4 — Forget behavior

A caller `mem::forget`s the batch. Must the safety proof rely on `Drop` running?

## Part 2 — Diagnose and repair

Each repair must leave a more precise soundness dossier. Reject fixes that merely erase the type, lifetime, state, compatibility, or artifact fact that the exercise is designed to expose.

### Repair 1 — Safety comment cites capacity

A comment says a slot is initialized because its index is below `N`.

Required direction: Capacity proves allocated slot existence, not initialization. Cite `index < len` and the transition that wrote the value before publishing `len`.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the soundness dossier changes.

### Repair 2 — Manual Send/Sync impl

The type manually implements both auto traits to make it usable in more contexts.

Required direction: Remove the impls unless a complete race/aliasing proof requires and supports them. Let fields and `T` determine auto traits.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the soundness dossier changes.

### Repair 3 — Only happy-path drop test

Tests fill the batch and drop it but never exercise pop, clear, partial occupancy, zero capacity, or panic ordering.

Required direction: Add state-transition and destructor-counting coverage plus Miri for executed unsafe paths when available.

Submit the corrected boundary plus one causal negative case. In the explanation, show exactly how the soundness dossier changes.

## Part 3 — Focused exercises

### Exercise 1 — Invariant state machine

Enumerate all legal `len`/slot states and transitions.

Completion standard: Every unsafe operation cites a reachable state and exact initialized range.

### Exercise 2 — Exact-drop harness

Use a counter type through push, pop, clear, and partial drop.

Completion standard: Every constructed value is dropped exactly once unless deliberately leaked.

### Exercise 3 — Zero/ZST audit

Test zero capacity and zero-sized values.

Completion standard: No proof relies on nonzero allocation size or unique addresses for ZSTs.

### Exercise 4 — Safe oracle comparison

Implement the same API with `Vec<T>` and compare operation sequences.

Completion standard: The unsafe version has identical public semantics for the explored domain.

### Cross-course transfer

Choose one artifact from Courses 1–9 and reassess it through **Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits**. Reconstruct its current invariant owner, then decide whether the soundness dossier reveals a genuine defect. A justified no-change decision is valid when the advanced mechanism would add proof or compatibility cost without removing a real invalid state.


### Applied case study — auditing panic in partially initialized storage

An `InlineBatch<T, N>` owns `[MaybeUninit<T>; N]` and an initialized-prefix length. A new `extend_with` method repeatedly invokes a closure to construct values. The closure may panic after producing several elements. A proposed implementation increments `len` before writing each value so `Drop` “knows what to clean.” Another writes first and increments afterward. A third uses a temporary guard.

Construct the complete state-transition table for one iteration. For every intermediate point, state which slots contain live `T`, which owner is responsible for them, and what `Drop` must do after panic. Explain why increment-before-write can drop uninitialized memory and why write-before-increment can leak a just-written value if an operation capable of panicking is inserted between the two steps.

Audit the abstraction beyond this method. Cover zero capacity, `pop`, `clear`, `as_slice`, movement of the batch, drop order, auto traits, and whether `T: Unpin` is relevant. Finish with an evidence map that separates code review, destructor counters, bounded transition exploration, Miri, and compile-fail API checks. State one soundness claim that none of those forms proves alone.

## Part 4 — Independent laboratory

Build [Audited Inline Batch](../../labs/module-06-inline-batch/README.md) from its `starter/` package.

Build a fixed-capacity inline batch over `MaybeUninit`, accompanied by a safe oracle and a written proof for initialization, slicing, pop, drop, panic, zero capacity, and auto traits.

Before implementation, freeze Audited Inline Batch’s public behavior and the soundness dossier. After implementation, complete its transfer task in a domain with different ownership, version, capacity, extension, or failure policy; renaming types does not demonstrate transfer.

## Part 5 — Capstone transfer

Keep AxiomStore’s `InlineBatch` private. Produce the full soundness dossier and ensure every unsafe operation has a local `SAFETY:` comment that cites facts established by surrounding safe code.

Update AxiomStore’s soundness dossier before code. Record the changed invariant owner, new failure paths, compatibility effect, and falsifying evidence. Then run the full capstone route because this module can invalidate guarantees outside its local file.

### Evidence quality review

Before leaving the module, select the unsafe operation whose local comment initially seemed sufficient. Trace it backward to the safe constructor and forward through movement, failure, and destruction. Record one soundness claim not covered by the tests you wrote, and state whether manual review, Miri, a model, or removal of the optimization is the appropriate next response.

## Part 6 — Reconstruct and defend

Review the abstraction from safe constructor through every method and destructor. Explain why local pointer plausibility, a passing test suite, or a clean Miri run is insufficient alone.

Finish without notes by reconstructing the soundness dossier. Name the requirement, the simpler design, the decisive rejected construction, the state after failure, and the evidence that could falsify your claim. End by stating one condition under which this mechanism should be removed.

The defense is complete only when another reader can reproduce the reasoning behind Audited Inline Batch and the AxiomStore increment without seeing your final implementation.
