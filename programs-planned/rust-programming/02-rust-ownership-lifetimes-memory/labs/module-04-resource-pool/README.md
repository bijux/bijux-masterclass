# Laboratory 14 — RAII Resource Pool

This is the independent product for **Course 2, Module 14: RAII, Drop, Unwinding, and Failure Atomicity**. Read the [module chapter](../../course-book/module-14-raii-drop-unwinding-and-failure-atomicity/index.md) and complete its [workbook](../../course-book/module-14-raii-drop-unwinding-and-failure-atomicity/workbook.md) before consulting the reference implementation.

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

## Working route

Use the common [laboratory method](../../../START_HERE.md#laboratory-method). Work from `starter/`, add the first adversarial test before the design-changing repair, and complete the workbook’s transfer problem before reading the reference implementation.

```bash
cd starter
cargo test
cargo fmt -- --check
cargo clippy -- -D warnings
```

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

> Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **RAII Resource Pool**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
