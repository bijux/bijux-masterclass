# Laboratory 22 — Associated Families

This is the independent product for **Course 3, Module 22: Associated Types and Type Families**. Read the [module chapter](../../course-book/module-22-associated-types-and-type-families/index.md) and complete its [workbook](../../course-book/module-22-associated-types-and-type-families/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Implement a tabular source abstraction with two layers:

- `LendingRows`, whose `Row<'a>` borrows from the source's current buffer;
- `OwnedRows`, an adapter that materializes durable `OwnedRow` values.

The lab must demonstrate why ordinary `Iterator` cannot express the lending relationship and must include a compile-fail example preventing a borrowed row from surviving the next mutable advance.

The solution must not expose the GAT to callers that only need owned rows.

## Design focus

The source reuses an internal text buffer, so each borrowed row is valid only until the next mutable advance. Model that relationship directly: `Row<'a>` must be tied to the borrow used for one call, not to an invented long-lived lifetime. The owned adapter should copy only at the boundary where durable storage is requested. Callers that need ordinary owned iteration should not have to understand the lending protocol or name its GAT.

Test empty input, multiple rows, repeated advancement, and conversion to owned rows. Add a negative example showing that a borrowed row cannot survive another mutable call. Compare the design with three weaker alternatives: returning `String` for every row, exposing internal buffer indices, and claiming ordinary `Iterator<Item = &str>` can borrow from mutable iterator state. Explain exactly what information each alternative loses or misrepresents.

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

> When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Associated Families**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
