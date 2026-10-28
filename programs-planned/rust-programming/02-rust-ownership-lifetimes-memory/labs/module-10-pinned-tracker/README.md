# Laboratory 20 — Pinned Tracker

**Course 2 · Module 20: Pinning and Address-Sensitive Design**

[Chapter](../../course-book/module-20-pinning-and-address-sensitive-design/index.md) · [Workbook](../../course-book/module-20-pinning-and-address-sensitive-design/workbook.md) · [Memory Workspace guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Pinning and Address-Sensitive Design**: What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely? The product must make **Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **pinning contract** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build an address-sensitive tracker that can be initialized only after pinning and can then report whether every observation occurs at its initialized address. The implementation remains entirely safe Rust.

```text
labs/module-10-pinned-tracker/
├── starter/
└── solution/
```

### Required type

The tracker contains:

- an owned label;
- `Cell<Option<NonNull<PinnedTracker>>>` storing its initialized address;
- an observation counter;
- `PhantomPinned`.

No raw pointer is dereferenced. `NonNull` is used only as a copyable address token obtained safely from a reference.

### Required API

- constructor returns an unpinned, uninitialized value;
- `initialize(self: Pin<&Self>)` records the address once;
- `observe(self: Pin<&Self>)` verifies the current address and increments a counter;
- accessors use `Pin<&Self>` after initialization;
- safe heap and stack pin examples;
- no unchecked pin constructors;
- compile-fail evidence that unrestricted mutable access/move-out is unavailable after pinning;
- no panicking destructor.

### Interpretation

The address token simulates an external registration without performing FFI. The type demonstrates the safe-facing pin contract; it is not a self-referential pointer implementation.

### Acceptance

```bash
cargo test -p rust-olm-lab-10-pinned-tracker --all-targets
cargo clippy -p rust-olm-lab-10-pinned-tracker --all-targets -- -D warnings
```

## Design record

Before implementation, complete this record for **Pinned Tracker**:

| Question | Required answer |
|---|---|
| Module decision | How does **Pinning and Address-Sensitive Design** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **pinning contract** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **Pinned Tracker**.
2. Draw the smallest **pinning contract** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Memory Workspace so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 20 — Pinned Tracker**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Pinned Tracker**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants.
- Explain Pin<P> as a contract on the pointee mediated by a pointer, not as a magical immovable allocation.
- Use Unpin and PhantomPinned correctly and construct pinned values without exposing moves after invariant activation.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 20 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **pinning contract**. Defend why your design is simpler than one plausible alternative under the new requirements.
