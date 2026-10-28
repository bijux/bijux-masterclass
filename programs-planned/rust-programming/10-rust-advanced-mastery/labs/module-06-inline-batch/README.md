# Laboratory 6 — Inline Batch

[Course 10](../../README.md) · [Common laboratory method](../../../START_HERE.md#laboratory-method)

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

### Completion standard

You can point to every live `T`, name its owner at every transition, and explain exactly why each unsafe read, drop, or slice construction is valid. If any panic point creates a live value outside the recorded prefix, the abstraction is not ready.
