# Module 96 — Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits

**96/100** · Course 10 · Module 96 of 100

[Course 10 overview](../index.md) · [Workbook](workbook.md) · [Solutions](solutions.md) · [AxiomStore guide](../capstone.md)

## The question

> What exact proof makes a safe API implemented with unsafe code sound across every constructor, method, failure path, destructor, and thread-safety claim?

## Why this comes now

Course 6 introduced unsafe Rust at external and allocation boundaries. Course 10 returns to unsafe code from the reviewer’s perspective. The central skill is not writing a clever pointer operation; it is auditing the complete safe abstraction that makes the operation reachable. Soundness depends on validity, provenance, alignment, initialization, aliasing, lifetime, panic behavior, drop behavior, and auto-trait exposure working together. A local `SAFETY:` comment is useful only when it names facts established elsewhere and those facts remain true on every path.

Course 6 taught how to write narrow unsafe mechanisms. This module changes perspective: you are now the reviewer responsible for the complete safe abstraction and every state from construction through destruction.

Course 6 taught how to write small unsafe boundaries. Course 10 raises the standard: review the entire safe abstraction, including constructors, failure paths, drop, forgetting, and auto traits. A locally plausible pointer operation is irrelevant if a safe method can invalidate its preconditions before the next call.

## What you will be able to do

After completing this module, you will be able to:

- write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation
- separate Rust validity from application invariants and explain which violations can create undefined behavior
- trace pointer provenance, allocation identity, alignment, initialization, aliasing, and lifetime as independent obligations
- audit normal return, recoverable error, panic, partial initialization, move, and drop paths for exactly-once cleanup
- derive whether `Send` and `Sync` should be inherited, prevented, or manually asserted for an unsafe abstraction
- minimize unsafe reachability by placing a small mechanism behind a safe state machine and adversarial tests

## Core model

### The governing model

The governing artifact is a **soundness dossier**. It starts with the safe public promise, defines representation states, maps every safe operation to state transitions, lists each unsafe operation’s local preconditions, and closes the proof over panic, partial initialization, drop, leak, move, `Send`, and `Sync` behavior.

### 1. The unit of review is the safe abstraction

An unsafe block may be locally plausible while the public type remains unsound. Review begins at every safe constructor and method that can reach the block. Ask what values callers can create, what aliases they can retain, whether panics interrupt transitions, and what `Drop` will observe. A soundness argument is a graph from safe inputs to unsafe preconditions, not a sentence attached to one dereference.

**Widen the review unit.** Starting from one `assume_init_read`, list every safe method that can change whether the slot is initialized.

### 2. Validity is stricter than application meaning

Rust references must be aligned, non-null, point to initialized values of the correct type, and obey aliasing and lifetime requirements. A `bool` must contain a valid boolean representation; an enum discriminant must be valid. By contrast, “record key is unique” is an application invariant. Violating uniqueness is a product defect; constructing an invalid reference can be undefined behavior. Keep these categories separate so safety comments do not rely on merely desirable business rules.

**Separate validity from domain rules.** Explain why a valid but forbidden key is not undefined behavior, while reading an uninitialized `String` is.

### 3. Provenance and allocation identity travel with pointers

A numeric address alone is not a complete argument that a pointer may access an object. Pointer arithmetic must remain within the relevant allocation or permitted one-past boundary, preserve alignment for the accessed type, and use a pointer derived from the allocation being accessed. Avoid integer round trips in safe abstraction internals unless the platform and API contract explicitly justify them. Store indices or offsets when identity can remain with the owning pointer.

**Track provenance.** For a pointer derived from an array of `MaybeUninit<T>`, state the allocation, alignment, range, and lifetime facts needed to form a slice.

### 4. Initialization is a state machine

`MaybeUninit<T>` permits storage that does not yet contain a valid `T`. The abstraction must know exactly which slots are initialized before creating references, moving values out, or dropping them. A length field often witnesses an initialized prefix, but push must increment only after a successful write and pop must decrement before exposing an uninitialized slot to cleanup. Panic paths must not cause uninitialized memory to be dropped or initialized values to leak unintentionally.

**Order publication.** In `push`, compare incrementing `len` before and after writing `value`. Which order survives panic or unwinding?

### 5. Panic safety is part of soundness when invariants are temporarily broken

Many unsafe implementations temporarily create states that safe methods must not observe. If user code can run during that window—through `Clone`, comparison, formatting, allocation failure handlers, or callbacks—a panic may strand the invariant. Prefer operations that cannot invoke user code while the representation is inconsistent. Otherwise install a guard that restores or safely disposes of the partial state during unwinding.

**Audit destruction.** Trace pop, clear, drop, and `mem::forget`. Which guarantee is cleanup, and which is memory safety even when cleanup never runs?

### 6. Drop and forgetting require different claims

`Drop` must destroy every initialized owned value exactly once and deallocate with the original layout. But safe code may leak a value with `mem::forget`, reference cycles, or process termination. Soundness cannot require that every destructor always runs unless an unsafe caller contract supplies that guarantee. Pinning’s drop guarantee and foreign resource protocols need especially careful language about what safe code can and cannot bypass.

**Review auto traits.** Determine whether fields make the abstraction automatically `Send` or `Sync`; do not write manual impls unless the proof includes races and aliasing.

### 7. Auto traits are public soundness claims

Raw pointers and `UnsafeCell` can change automatic `Send` and `Sync` behavior. Manually implementing either trait asserts that all cross-thread uses allowed by the safe API are race free and uphold aliasing. The proof must cover the stored `T`, endpoint roles, destruction, and concurrent method calls. Add a negative marker such as `PhantomData<Rc<()>>` when thread transfer would violate the protocol; do not rely on accidental field choices to prevent it.

**Construct a failed proof.** Write one seemingly reasonable safety comment that omits a necessary fact, then repair the invariant rather than the prose alone.

### 8. Audit evidence must include failed constructions

Positive tests show intended behavior. Add drop counters, panic injection, zero capacity, full capacity, repeated clear, partial clone failure where applicable, and compile-fail cases for prohibited aliasing or thread transfer. Use Miri when available to find undefined behavior in executed paths, but do not treat a clean run as a proof of unexecuted states. The written invariant remains authoritative.

**Reader check.** Explain this idea using the concrete boundary in Audited Inline Batch and name one fact that remains outside the mechanism. Then change one assumption and predict whether the result becomes a type error, a runtime rejection, a compatibility problem, or only a measured implementation observation.

### A decision table

| Design question | Principled evidence or mechanism | Weak substitute to reject |
|---|---|---|
| Can safe Rust express the required representation? | prefer the safe design unless measured/product evidence justifies unsafe | unsafe chosen as a mark of expertise |
| Which slots contain live values? | one explicit initialized-state invariant | reading memory based on capacity or stale flags |
| Can user code run while invariants are broken? | reorder transitions or install a cleanup guard | assuming panic never occurs |
| May the type cross threads? | derive or explicitly prevent auto traits; manually assert only with a full race proof | accidental Send/Sync from field selection |

### A rigorous working procedure

1. Freeze the safe API and state exactly what callers may assume.
2. Enumerate representation states, including empty, partially initialized, full, moved-from slots, and dropping.
3. For every safe method, write precondition, mutation order, postcondition, and panic point.
4. For every unsafe operation, cite concrete facts already established by surrounding safe code.
5. Audit drop, `forget`, zero capacity, zero-sized `T`, movement, and auto traits separately.
6. Compare against a safe oracle and run targeted dynamic tools where available; record what those tools still do not prove.

### Failure patterns and principled repairs

Unsafe-abstraction failures are rarely repaired by adding a comment beside the final pointer operation. The repair is to restore a complete invariant chain: valid construction, every safe mutation, panic and partial-initialization paths, destruction, auto-trait behavior, and the exact local fact that justifies each unsafe operation.

### Reviewing only the unsafe line

Trace every safe constructor, method, alias, panic path, move, and destructor that reaches it.

### Using an application invariant as a validity proof

State alignment, initialization, provenance, aliasing, and lifetime independently of business rules.

### Incrementing initialized length before writing

Write the value first and publish the new length only after initialization succeeds.

### Assuming Drop always executes

Do not make soundness depend on destructor execution that safe code can bypass by leaking.

### What the compiler cannot decide for you

Unsafe Rust allows the implementation to assert obligations the compiler cannot verify. It does not relax the public promise. A clean Miri run covers only executed paths under its model; a safety comment is review evidence, not a proof by itself; and `Drop` cannot be required for soundness because values may be forgotten.

If the dossier cannot fit on a few reviewable pages, shrink the abstraction or return to safe storage. The goal is not to demonstrate unsafe expertise but to make the safe surface boring.

## Use the idea in a complete program

Treat `InlineBatch<T, N>` as a state machine. Before reading an unsafe line, write the initialized-prefix invariant and the exact transition order for push, pop, clear, and drop. Then test zero capacity and a destructor-counting type.

```rust
use std::mem::MaybeUninit;

struct InlineBatch<T, const N: usize> {
    slots: [MaybeUninit<T>; N],
    len: usize,
}

impl<T, const N: usize> InlineBatch<T, N> {
    fn new() -> Self {
        Self {
            slots: [const { MaybeUninit::uninit() }; N],
            len: 0,
        }
    }

    fn push(&mut self, value: T) -> Result<(), T> {
        if self.len == N {
            return Err(value);
        }
        self.slots[self.len].write(value);
        self.len += 1;
        Ok(())
    }
}

impl<T, const N: usize> Drop for InlineBatch<T, N> {
    fn drop(&mut self) {
        for slot in &mut self.slots[..self.len] {
            // SAFETY: the initialized-prefix invariant states that exactly
            // slots 0..len contain live T values, each owned by this batch.
            unsafe { slot.assume_init_drop() };
        }
    }
}
```

### Trace the example

For `push`, mark the slot as uninitialized, write the value, then publish the new length. For `pop`, reduce the published initialized prefix before moving the value out. For `as_slice`, prove allocation identity, alignment, contiguity, initialized range, aliasing, and returned lifetime separately.

Introduce a panic-capable wrapper around `T` and identify which operations can actually panic. Verify that a panic cannot make `len` claim an uninitialized slot or make drop visit a moved value. Finally, explain why leaking the entire batch may leak values but must not create undefined behavior.

### Use it in AxiomStore

AxiomStore’s only production unsafe code is an internal `InlineBatch<T, N>` used to stage a bounded transaction without heap allocation. The public transaction API is safe. The dossier defines the initialized-prefix invariant, state transitions, drop order, panic surface, `N = 0`, movement, and auto-trait behavior. A safe `Vec<T>` oracle and drop-counting model tests are retained beside the implementation so the optimization never becomes its own specification.

AxiomStore’s unsafe dossier is stored beside `InlineBatch` and contains:

```text
safe API promise
representation fields
state invariant
constructor proof
push transition
pop transition
slice-formation proof
clear/drop proof
panic and partial-progress analysis
forget/leak analysis
auto-trait analysis
dynamic-tool coverage
residual risk
```

No other capstone module may reach raw slots. If a later feature needs a new unsafe operation, the dossier and reference oracle change before the code does.

## Practice sequence

1. **Safety-comment audit.** Take four unsafe blocks and classify each required fact as validity, provenance, initialization, aliasing, or lifetime.
2. **Transition-order repair.** Implement both wrong and correct push ordering in a model; show the state exposed by a panic between steps.
3. **Exact-drop test.** Use counters to cover push, pop, clear, ordinary drop, and partial occupancy.
4. **Zero and ZST review.** Test `N = 0` and a zero-sized type without assuming nonzero addresses or storage bytes.
5. **Auto-trait review.** Compare `T`, `Rc<T>`, and `Cell<T>` instantiations and explain what the fields imply.

Complete the [workbook](workbook.md) and [Audited Inline Batch](../../labs/module-06-inline-batch/README.md). The negative investigations must identify which soundness fact is absent, not merely that the code contains `unsafe`.

## Ready to continue

Continue only when you can review a safe abstraction from constructor through destruction, write a local justification that cites established facts, and explain why leak behavior and auto traits are part of the public soundness story. You should be willing to reject the unsafe design when a safe implementation meets the requirement.

## Primary Rust references

- The Rust Reference: behavior considered undefined
- The standard library documentation for MaybeUninit, ptr, and mem
- The Rustonomicon: uninitialized memory, drop checking, and Send/Sync

Read `MaybeUninit`, pointer, and Rustonomicon material with the current validity/provenance model in mind. Mark any compiler-model or Miri statement as tool- and version-scoped rather than timeless ABI law.

## Continue

1. Complete the [workbook](workbook.md) without consulting answers.
2. Build [Audited Inline Batch](../../labs/module-06-inline-batch/README.md).
3. Apply Module 96 in the [AxiomStore engineering guide](../capstone.md).
4. Review the [solutions](solutions.md) only after preserving your own predictions and design record.
