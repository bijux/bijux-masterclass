# Reasoned Solutions — Module 96: Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits

[Workbook](workbook.md) · [Chapter](index.md) · [Laboratory](../../labs/module-06-inline-batch/README.md) · [AxiomStore guide](../capstone.md)

Use these notes only after preserving your prediction and repair for **Module 96: Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits**. Compare the reasoning against this question: *What exact proof makes a safe API implemented with unsafe code sound across every constructor, method, failure path, destructor, and thread-safety claim?* Do not compare line count first. A different implementation is valid when it preserves the same public contract and can defend its ownership, failure, ordering, capacity, safety, compatibility, and evidence consequences.

## Part 1 — Prediction

### Prediction 1 — Publish before initialize

Drop trusts `len` and may call `assume_init_drop` on an uninitialized slot. Publication must occur after successful initialization.

### Prediction 2 — Pop ordering

The moved value may still be included in the published initialized prefix and later dropped twice. Decrement first, then move out.

### Prediction 3 — Slice formation

Creating references to uninitialized `T` is invalid even if the caller never reads the extra elements. The slice must cover exactly the initialized prefix.

### Prediction 4 — Forget behavior

No. Leaking may lose cleanup but cannot be required to preserve validity or prevent undefined behavior.

## Part 2 — Diagnose and repair

Judge every repair against the soundness dossier: the decisive relationship must become clearer, not disappear behind cloning, erasure, broad bounds, visibility, unchecked construction, or deleted validation.

### Repair 1 — Safety comment cites capacity

**Causal defect.** A comment says a slot is initialized because its index is below `N`.

**Principled repair.** Capacity proves allocated slot existence, not initialization. Cite `index < len` and the transition that wrote the value before publishing `len`.

The negative case should reintroduce **Safety comment cites capacity** while preserving the surrounding requirement. The soundness dossier must identify the first phase at which the original assumption becomes invalid.

### Repair 2 — Manual Send/Sync impl

**Causal defect.** The type manually implements both auto traits to make it usable in more contexts.

**Principled repair.** Remove the impls unless a complete race/aliasing proof requires and supports them. Let fields and `T` determine auto traits.

The negative case should reintroduce **Manual Send/Sync impl** while preserving the surrounding requirement. The soundness dossier must identify the first phase at which the original assumption becomes invalid.

### Repair 3 — Only happy-path drop test

**Causal defect.** Tests fill the batch and drop it but never exercise pop, clear, partial occupancy, zero capacity, or panic ordering.

**Principled repair.** Add state-transition and destructor-counting coverage plus Miri for executed unsafe paths when available.

The negative case should reintroduce **Only happy-path drop test** while preserving the surrounding requirement. The soundness dossier must identify the first phase at which the original assumption becomes invalid.

## Part 3 — Focused exercises

### Exercise 1 — Invariant state machine

The construction should answer: Enumerate all legal `len`/slot states and transitions.

The decisive acceptance criterion is: Every unsafe operation cites a reachable state and exact initialized range.

For **Invariant state machine**, apply the soundness dossier to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 2 — Exact-drop harness

The construction should answer: Use a counter type through push, pop, clear, and partial drop.

The decisive acceptance criterion is: Every constructed value is dropped exactly once unless deliberately leaked.

For **Exact-drop harness**, apply the soundness dossier to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 3 — Zero/ZST audit

The construction should answer: Test zero capacity and zero-sized values.

The decisive acceptance criterion is: No proof relies on nonzero allocation size or unique addresses for ZSTs.

For **Zero/ZST audit**, apply the soundness dossier to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Exercise 4 — Safe oracle comparison

The construction should answer: Implement the same API with `Vec<T>` and compare operation sequences.

The decisive acceptance criterion is: The unsafe version has identical public semantics for the explored domain.

For **Safe oracle comparison**, apply the soundness dossier to the exact construction above and to its closest simpler alternative. The answer is complete only when the stated acceptance criterion survives a counterexample aimed at that design choice.

### Cross-course transfer

Full credit may conclude that **Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits** should not be retrofitted into the earlier artifact. The comparison must identify the current owner, the proof benefit, maintenance cost, and a concrete failure that would change.

### Applied case study — auditing panic in partially initialized storage

At the start of an iteration, exactly `0..len` contains live values and the batch owns them. The closure should run before any slot state changes. If it panics, the existing prefix remains unchanged. After it returns a `T`, that value is temporarily owned by the local variable. Writing it into `slots[len]` transfers ownership to the storage; immediately afterward `len` must be advanced without invoking user code or another operation that can panic. The invariant is restored when `0..new_len` is initialized.

Incrementing first makes `Drop` treat an unwritten slot as live after panic, which is undefined behavior. Writing first and then performing arbitrary fallible or panicking work before incrementing leaves a live value outside the recorded prefix, causing a leak on unwind. A small internal guard can be useful only if construction requires a longer multi-step transition; otherwise the shortest non-panicking write-then-increment sequence is easier to audit.

For `N = 0`, `push` always returns the value and slices are empty. `pop` decrements before `assume_init_read`, transferring exactly one live value. `clear` repeats that transition. Slice construction is sound only for the initialized prefix and for the borrow duration. Moving the batch moves the backing array and its initialized values normally; no address-sensitive invariant exists, so `Unpin` is irrelevant. Auto traits should be inherited from the fields rather than asserted manually.

Destructor counters test exactly-once behavior on executed paths. Bounded transition exploration checks state-machine combinations. Miri can detect executed undefined behavior. Compile-fail tests protect the safe API surface. Review connects every unsafe operation to the invariant. None alone proves soundness for every `T`, capacity, panic point, target, and future code change.

## Part 4 — Independent laboratory

A complete [Audited Inline Batch](../../labs/module-06-inline-batch/README.md) satisfies its public contract and makes the soundness dossier inspectable. The reference implementation is not canonical; compare accepted input, rejected input, state after failure, ownership/lifetime surface, deterministic behavior, and extension authority in that order.

Build a fixed-capacity inline batch over `MaybeUninit`, accompanied by a safe oracle and a written proof for initialization, slicing, pop, drop, panic, zero capacity, and auto traits.

The transfer variant for Audited Inline Batch must alter at least two substantive dimensions and preserve an independent oracle; a domain-name substitution is not evidence of mastery.

## Part 5 — Capstone transfer

Keep AxiomStore’s `InlineBatch` private. Produce the full soundness dossier and ensure every unsafe operation has a local `SAFETY:` comment that cites facts established by surrounding safe code.

A strong capstone change keeps the responsibility described by the soundness dossier local. Reject any design that spreads the mechanism across unrelated AxiomStore modules without a named requirement.

## Part 6 — Reconstruct and defend

Review the abstraction from safe constructor through every method and destructor. Explain why local pointer plausibility, a passing test suite, or a clean Miri run is insufficient alone.

The defense passes when it reconstructs the soundness dossier from the requirement, shows a causal rejected construction, compares a simpler alternative, maps evidence, and names residual risk. Terminology without that chain is not mastery.

## Deep reasoning and transfer

### Decisive model

> What exact proof makes a safe API implemented with unsafe code sound across every constructor, method, failure path, destructor, and thread-safety claim?

Build a **unsafe state-and-operation dossier**. Mark the owner or authority, valid and invalid states, first decisive phase or event, state after failure, and visible consequence. The model is too weak when it records only the API call and not the relationship that makes the call legal or useful.

### Outcome checks

1. **Write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
2. **Separate Rust validity from application invariants and explain which violations can create undefined behavior.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
3. **Trace pointer provenance, allocation identity, alignment, initialization, aliasing, and lifetime as independent obligations.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
4. **Audit normal return, recoverable error, panic, partial initialization, move, and drop paths for exactly-once cleanup.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.
5. **Derive whether `Send` and `Sync` should be inherited, prevented, or manually asserted for an unsafe abstraction.** Give one satisfying example, one example that fails for that exact cause, and the earliest decisive observation.

### Repair discipline

The weak repair for this module is any change that makes the current example pass by deleting the first outcome: **Write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation.** A principled repair preserves that requirement, narrows the unsupported assumption, and makes the deciding fact observable in the unsafe state-and-operation dossier.

### Reference implementation comparison

For [Inline Batch](../../labs/module-06-inline-batch/README.md), compare contract, state transitions, adversarial cases, cleanup, and public behavior before syntax. Identify the earliest operation that could violate the contract and the type, check, protocol, or review procedure that prevents it. Then state when a simpler design would be preferable.

### Capstone transfer

In AxiomStore, Module 96 is complete only when the new behavior fits the existing authority map. Trace the changed fact from input through validation, state transition, effect, output, and tests. Two components deciding the same fact indicate a second source of truth rather than successful integration.

### Oral defense

Answer these without notes:

1. In **Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits**, which relationship decides this question: “What exact proof makes a safe API implemented with unsafe code sound across every constructor, method, failure path, destructor, and thread-safety claim?”
2. What is the smallest causal negative case?
3. Which repair preserves the requirement?
4. Which tempting repair deletes it?
5. What can the chosen evidence falsify, and what remains unproved?
6. How would the design change in a product unrelated to AxiomStore?
