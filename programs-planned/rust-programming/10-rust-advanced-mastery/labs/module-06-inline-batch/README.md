# Laboratory 96 — Inline Batch

**Course 10 · Module 96: Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits**

[Chapter](../../course-book/module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/index.md) · [Workbook](../../course-book/module-96-auditing-unsafe-abstractions-validity-provenance-drop-panic-and-auto-traits/workbook.md) · [AxiomStore guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits**: What exact proof makes a safe API implemented with unsafe code sound across every constructor, method, failure path, destructor, and thread-safety claim? The product must make **Write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **unsafe state-and-operation dossier** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Product

Build a fixed-capacity owner of up to `N` values without a heap allocation. The internal representation is `[MaybeUninit<T>; N]` plus an initialized-prefix length. The public API is safe; all unsafe operations are private and justified by one state invariant.

Begin with the starter’s `Vec`-backed `SafeBatch` as the behavioral oracle. Do not delete it until the inline implementation matches it across push, pop, mutation, clear, drop, zero capacity, and full-capacity failure.

### State invariant

At every observable boundary:

```text
slots[0..len]      contain exactly len live T values
slots[len..N]      are logically uninitialized
0 <= len <= N
InlineBatch owns every live value in the initialized prefix
```

Write a transition table for `push`, `pop`, `clear`, and `drop`. For each line, record the old state, operation that changes initialization, new owner of the value, updated length, and unwind behavior.

### Required API

Provide `new`, `len`, `is_empty`, `is_full`, `push`, `pop`, `as_slice`, `as_mut_slice`, `clear`, `Default`, and `Drop`. A rejected `push` must return the original value. `pop` must transfer ownership exactly once. `clear` and final destruction must drop exactly the initialized prefix.

Every unsafe block needs an adjacent `SAFETY:` explanation tied to the invariant. Do not assert `Send`, `Sync`, or `Unpin` manually; derive auto-trait behavior from the fields unless a separate proof requires otherwise.

### Adversarial evidence

Use a drop-counted type to test:

- ordinary destruction;
- pop followed by destruction;
- clear followed by destruction;
- full insertion failure;
- zero capacity;
- mutation through `as_mut_slice`;
- a panic while producing a sequence of candidate values.

Run the completed solution under Miri when the tool is available, but document why a passing Miri run is evidence for executed paths rather than a universal proof.

### Transfer

Add `try_extend` with a stated failure policy. Decide whether partial insertion is allowed or whether the method must stage values and commit atomically. Make the choice visible in the type and error behavior; do not leave a partially changed batch after claiming all-or-nothing semantics.

### Using the reference

Compare your implementation with `solution/` only after the safe oracle and destructor tests pass. Review unsafe operations one by one. A shorter implementation is not better if it makes the initialization state implicit.

### Mechanism-specific completion standard

You can point to every live `T`, name its owner at every transition, and explain exactly why each unsafe read, drop, or slice construction is valid. If any panic point creates a live value outside the recorded prefix, the abstraction is not ready.

## Design record

Before implementation, complete this record for **Inline Batch**:

| Question | Required answer |
|---|---|
| Module decision | How does **Auditing Unsafe Abstractions: Validity, Provenance, Drop, Panic, and Auto Traits** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **unsafe state-and-operation dossier** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Inline Batch**.
2. Draw the smallest **unsafe state-and-operation dossier** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to AxiomStore so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Whole-laboratory completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Write a safety dossier that names representation states, public preconditions, internal invariants, and proof obligations for every unsafe operation.
- Separate Rust validity from application invariants and explain which violations can create undefined behavior.
- Trace pointer provenance, allocation identity, alignment, initialization, aliasing, and lifetime as independent obligations.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 96 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **unsafe state-and-operation dossier**. Defend why your design is simpler than one plausible alternative under the new requirements.
