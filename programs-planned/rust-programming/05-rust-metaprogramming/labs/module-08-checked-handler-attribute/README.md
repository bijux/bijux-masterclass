# Laboratory 48 — Checked Handler Attribute

**Course 5 · Module 48: Attribute Macros and Item Transformation**

[Chapter](../../course-book/module-48-attribute-macros-and-item-transformation/index.md) · [Workbook](../../course-book/module-48-attribute-macros-and-item-transformation/workbook.md) · [CommandForge guide](../../course-book/capstone.md) · [Program method](../../../START_HERE.md#laboratory-method)

## Why this laboratory exists

The laboratory isolates one decision from **Attribute Macros and Item Transformation**: How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own? The product must make **Parse attribute arguments independently from the attached item** visible through its public behavior, failure state, and tests rather than through explanatory comments alone.

Work from `starter/` with a **attribute preservation table** beside the code. Preserve the first failing case and your original design before reading `solution/`; the reference is a comparison surface, not a sequence of missing lines.

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

1. Read the product contract and run the starter’s baseline checks for **Checked Handler Attribute**.
2. Draw the smallest **attribute preservation table** capable of deciding the governing question.
3. Add a causal negative or adversarial test that fails for the intended relationship.
4. Implement one invariant at a time; after each failure, record state, ownership, cleanup, order, and capacity.
5. Complete the transfer task in a domain unrelated to CommandForge so that syntax cannot substitute for understanding.
6. Compare with `solution/` by contract, proof boundary, and rejected shortcuts before comparing implementation shape.

## Completion check

The laboratory is complete when the required behavior and failure paths pass and you can answer this question without the chapter:

For **Laboratory 48 — Checked Handler Attribute**, answer the learning-target question from the completed product. Point to the public boundary that carries the rule, the adversarial case that would falsify it, and one fact the test suite does not establish.

Demonstrate the same mechanism once in the workbook’s unrelated transfer domain. Name one shortcut that would compile or pass the happy path while weakening the product contract.

## Reference comparison

Open [`solution/`](solution/) only after your implementation works or you have written a precise blocker. For **Checked Handler Attribute**, compare accepted and rejected inputs, state after failure, ownership or authority, deterministic behavior, public surface, and justified cost before comparing syntax.

## Completion standard

The laboratory is complete when the implementation and tests demonstrate:

- Parse attribute arguments independently from the attached item.
- Validate supported item kinds and function signatures.
- Preserve visibility, attributes, generics, ABI, safety, asyncness, and body when the macro does not own them.

Also preserve one ordinary success trace, one causal rejection or partial-failure trace, cleanup, deterministic behavior where promised, and one explicit limit on what the tests establish. A happy-path implementation or an explanation that merely names the API is incomplete.

## Independent transfer

Rebuild the decisive relationship from Module 48 in a different product. Change the domain types, names, public behavior, and failure mode while retaining the same **attribute preservation table**. Defend why your design is simpler than one plausible alternative under the new requirements.
