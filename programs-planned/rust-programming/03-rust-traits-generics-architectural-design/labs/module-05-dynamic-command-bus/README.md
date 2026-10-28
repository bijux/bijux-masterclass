# Laboratory 25 — Dynamic Command Bus

This is the independent product for **Course 3, Module 25: Trait Objects and Dynamic Polymorphism**. Read the [module chapter](../../course-book/module-25-trait-objects-and-dynamic-polymorphism/index.md) and complete its [workbook](../../course-book/module-25-trait-objects-and-dynamic-polymorphism/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Build a command bus that owns heterogeneous command handlers behind a dyn-compatible interface.

Requirements:

- a stable command envelope and typed execution result;
- at least three concrete handlers;
- deterministic registration and dispatch;
- no downcasting in ordinary execution;
- a separate factory or constructor surface for handler-specific configuration;
- borrowed-handler support demonstrated through an explicit object lifetime;
- a comparison with a closed command enum.

## Design focus

The command bus exists because handler kinds are selected and stored at run time. Derive the erased contract from dispatch needs: stable command identity, one object-safe invocation method, and a concrete result envelope. Construction and handler-specific configuration belong outside the trait. Keep registration order deterministic and reject duplicate command names before dispatch.

Demonstrate both owned handlers and a borrowed handler whose object lifetime is explicit; do not add `'static` by reflex. Add negative examples for a generic trait method and an associated function without a receiver, then explain why each is not dyn-compatible. Ordinary execution must not downcast. Finish with an enum comparison that names the exact requirement under which a closed enum would be simpler and safer than the registry.

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

> When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Dynamic Command Bus**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
