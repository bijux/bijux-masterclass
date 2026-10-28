# Laboratory 14 — RAII Resource Pool

**Course 2 · Module 14: RAII, Drop, Unwinding, and Failure Atomicity**

[Chapter](../../course-book/module-14-raii-drop-unwinding-and-failure-atomicity/index.md) · [Workbook](../../course-book/module-14-raii-drop-unwinding-and-failure-atomicity/workbook.md) · [Memory Workspace guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **RAII, Drop, Unwinding, and Failure Atomicity**: Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic? The product must make **Derive local, field, tuple, temporary, and scope destruction order from documented rules** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **destruction trace** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a generic single-threaded resource pool whose checked-out item is owned by a lease guard and automatically returned unless an explicit consuming transition says otherwise.

```text
labs/module-04-resource-pool/
├── starter/
└── solution/
```

### Required API

```rust
pub struct Pool<T> { /* private */ }
pub struct Lease<'a, T> { /* private */ }

impl<T> Pool<T> {
    pub fn new(items: Vec<T>) -> Self;
    pub fn available(&self) -> usize;
    pub fn checkout(&mut self) -> Option<Lease<'_, T>>;
}

impl<T> Lease<'_, T> {
    pub fn get(&self) -> &T;
    pub fn get_mut(&mut self) -> &mut T;
    pub fn discard(self);
    pub fn replace(self, replacement: T) -> T;
}
```

`replace` returns the checked-out item and puts the replacement into the pool. Ordinary drop returns the checked-out item. `discard` permanently removes it.

### Design constraints

- no cloning requirement on `T`;
- no direct call to `Drop::drop`;
- no `unsafe`, raw pointers, reference counting, or interior mutability;
- no destructor panic under any represented state;
- the item is acted on at most once;
- method signatures make double return impossible;
- tests include ordinary return, mutation, discard, replace, early return, and panic unwinding.

### Limitation analysis

Because `Lease` borrows the pool mutably, only one lease can exist and the pool cannot be inspected directly while the lease is active. This is intentional in Module 14. Later modules can compare a `RefCell`-backed or shared-ownership topology, but do not weaken this lab to anticipate them.

### Acceptance

```bash
cargo test -p rust-olm-lab-04-resource-pool --all-targets
cargo clippy -p rust-olm-lab-04-resource-pool --all-targets -- -D warnings
```

## Design record

Before implementation, complete this record for **RAII Resource Pool**:

| Question | Required answer |
|---|---|
| Module decision | How does **RAII, Drop, Unwinding, and Failure Atomicity** answer its governing question in this product? |
| Authority | Which type or component decides the main rule? |
| Valid states | Which states may be observed through the public API? |
| Rejection | What exact input or transition is refused, and what remains unchanged? |
| Ownership | Who owns every resource before, during, and after the decisive operation? |
| Order and bounds | Which sequence, capacity, lifetime, or compatibility limit is promised? |
| Evidence | Which test, compiler case, model, trace, or review could falsify the claim? |

Use the **destruction trace** to answer the table. Then add at least three adversarial cases: one at the smallest boundary, one at the largest accepted or rejected boundary, and one that leaves partial work before failure. For each, state the final observable state before running the test.

## Working route

1. Read the product contract and run the starter’s baseline checks for **RAII Resource Pool**.
2. Draw the smallest **destruction trace** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to Memory Workspace so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 14 — RAII Resource Pool**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **RAII Resource Pool**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Derive local, field, tuple, temporary, and scope destruction order from documented rules.
- Design RAII guards whose ownership encodes exactly one cleanup or release obligation.
- Use Option::take, mem::replace, staged candidates, and consuming transitions while preserving valid states.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 14 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **destruction trace**. Defend why your design is simpler than one plausible alternative under the new requirements.
