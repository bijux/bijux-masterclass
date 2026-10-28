# Laboratory 48 — Checked Handler Attribute

This is the independent product for **Course 5, Module 48: Attribute Macros and Item Transformation**. Read the [module chapter](../../course-book/module-48-attribute-macros-and-item-transformation/index.md) and complete its [workbook](../../course-book/module-48-attribute-macros-and-item-transformation/workbook.md) before consulting the reference implementation.

## Learning target

The laboratory asks one focused version of the module’s governing question:

> How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?

By the end, the answer must be visible in the public API, failure behavior, adversarial tests, and design explanation—not merely in comments.

## Product

Implement an attribute that validates a handler and emits typed companion metadata:

```rust
#[checked_handler(name = "echo", about = "Return the supplied text")]
pub fn echo(input: &str) -> Result<String, String> {
    Ok(input.to_owned())
}
```

The original function must remain intact. The attribute owns metadata and a narrow syntactic contract; it does not own the function’s domain behavior.

## Required behavior

- Accept exactly `name` and `about` string keys.
- Reject unknown keys, duplicate keys, missing keys, and empty values.
- Require a public, non-async, non-const, safe free function with one `&str` parameter and an explicit `Result` return shape.
- Preserve visibility, ordinary attributes, signature, and body.
- Emit a deterministic companion constant containing name, description, and a typed function pointer.
- Point errors at the offending argument or function component.

## Adversarial cases

Test a private function, method, async function, wrong arity, owned `String` parameter, missing return type, duplicate metadata, and a valid function with documentation and `inline` attributes. Verify that the function runs exactly once through the generated pointer.

## Build sequence

Write a preservation ledger before code. Parse attribute arguments and the item separately, validate, then quote the original item plus metadata. Never reconstruct a simplified function from selected fields.

## Transfer

Add an optional `hidden` flag that changes catalog visibility metadata without changing function visibility or runtime behavior.

## Preservation proof

The attribute owns a narrow handler contract and companion metadata. Test that the original function remains callable under the same name, visibility, parameter type, and return type. Preserve unrelated attributes unless the contract explicitly consumes them.

Negative cases should include a private function, a method with a receiver, an asynchronous function, the wrong number of parameters, an unsupported metadata key, and duplicate metadata. Each rejection should point to the item or argument that violates the documented contract.

Review generated identifiers for collision risk. If the macro derives helper names from the function name, state the naming scheme and keep helpers private where possible. The attribute must not silently become a registration system; global catalog order and command-name uniqueness belong to a separate mechanism.

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

> How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Checked Handler Attribute**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.
