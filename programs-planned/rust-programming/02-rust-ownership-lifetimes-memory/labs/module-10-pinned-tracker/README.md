# Laboratory 20 — Pinned Tracker

This is the independent product for **Course 2, Module 20: Pinning and Address-Sensitive Design**. Read the [module chapter](../../course-book/module-20-pinning-and-address-sensitive-design/index.md) and complete its [workbook](../../course-book/module-20-pinning-and-address-sensitive-design/workbook.md) before consulting the reference implementation.

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

> What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Pinned Tracker**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
