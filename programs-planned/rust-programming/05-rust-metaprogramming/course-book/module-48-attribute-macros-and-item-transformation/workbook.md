# Workbook — Module 48: Attribute Macros and Item Transformation

[Chapter](index.md) · [Laboratory](../../labs/module-08-checked-handler-attribute/README.md) · [CommandForge guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Attribute Macros and Item Transformation** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?* Preserve your first prediction and record decisive facts in a **attribute preservation table**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 47 — Custom Derive Macros and Structural Generation that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?**
3. Draw the smallest **attribute preservation table** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen about **attribute ownership and item preservation**, record the expected outcome, the first decisive source shape, the earliest phase that knows the fact, the smallest repair preserving the requirement, and one tempting change that would obtain a pass by weakening this module’s public contract.

| # | Specimen | Your committed prediction |
|---:|---|---|
| 1 | [`main.rs`](../../compiler-labs/module-08/case-01/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 2 | [`main.rs`](../../compiler-labs/module-08/case-02/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 3 | [`main.rs`](../../compiler-labs/module-08/case-03/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 4 | [`main.rs`](../../compiler-labs/module-08/case-04/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 5 | [`main.rs`](../../compiler-labs/module-08/case-05/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 6 | [`main.rs`](../../compiler-labs/module-08/case-06/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 7 | [`main.rs`](../../compiler-labs/module-08/case-07/src/main.rs) | Pass or fail? Name the exact phase and rule. |
| 8 | [`main.rs`](../../compiler-labs/module-08/case-08/src/main.rs) | Pass or fail? Name the exact phase and rule. |

Run this course’s cases from the program root with:

```bash
python3 tools/run_compiler_labs.py 05-rust-metaprogramming
```

Do not accept “the macro failed” as an explanation. Distinguish matcher failure, parser failure, semantic validation, expansion, name resolution, type checking, build-script validation, and runtime behavior.

## Part 2 — Diagnose and repair

An attribute macro parses a function by searching its token string for `fn`, emits a wrapper with the same name, drops documentation and `cfg` attributes, changes an asynchronous function into a synchronous one, and accepts arbitrary key-value options while ignoring unknown keys.

### Repair sequence

1. Parse the attribute arguments with a closed grammar and reject unknown, duplicate, or malformed keys.
2. Parse the attached item into the exact supported Rust item type. Reject other items and unsupported qualifiers with errors at their source spans.
3. State preservation obligations before generation: original attributes, visibility, signature, generics, ABI, unsafety, asyncness, and body are preserved unless the attribute explicitly owns a transformation.
4. Emit the original function unchanged and generate companion metadata or a deliberately named wrapper. Avoid duplicate evaluation and name collisions.
5. Test public/private functions, generic signatures, unsupported async or unsafe functions, malformed metadata, and interaction with ordinary attributes.

### Required proof

Produce three artifacts:

- a attribute ownership and item preservation record that names the authority and the generated or checked surface;
- the smallest invocation, item, or build input that reproduces the original defect;
- a positive or negative test that would fail if the superficial repair replaced the principled one.

Your repair is incomplete if it merely changes token spelling. Explain how the accepted language, generated surface, evaluation semantics, names, errors, and compatibility obligations changed.

## Part 3 — Focused exercises

### Exercise 1 — Preservation ledger

For an attribute attached to a handler function, list which item properties are preserved, validated, transformed, or rejected.

### Exercise 2 — Attribute grammar

Design `#[command_handler(about = "...", hidden)]`. Specify unknown keys, duplicate keys, value types, and defaults.

### Exercise 3 — Signature validation

Validate `fn(Args) -> Result<String, CommandError>` without claiming to know type aliases or path resolution. What can the macro honestly check?

### Exercise 4 — Name collision

How should the macro derive a companion metadata constant name, and what collision remains possible?

### Exercise 5 — Wrapper semantics

A wrapper logs before and after calling the original function. Which semantics must it preserve under early return or panic?

### Exercise 6 — Attribute ordering

Two attributes transform the same function. Why can source order matter?

For every answer that proposes a macro, add a one-sentence rejection criterion: what simpler condition would make ordinary Rust preferable?

### Interleaved reasoning pass

1. For **Parse attribute arguments independently from the attached item**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the attribute preservation table.
2. For **Validate supported item kinds and function signatures**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the attribute preservation table.
3. For **Preserve visibility, attributes, generics, ABI, safety, asyncness, and body when the macro does not own them**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the attribute preservation table.
4. For **Decide whether to preserve, augment, wrap, or replace an item**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the attribute preservation table.

5. Identify one guarantee from an earlier course that a careless implementation of **Attribute Macros and Item Transformation** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

### Product: Checked Handler Attribute

Open [`labs/module-08-checked-handler-attribute/README.md`](../../labs/module-08-checked-handler-attribute/README.md) only after completing the prediction table. The starter is intentionally a valid baseline, not a half-written answer.

Before implementation, complete this module-specific design record:

| Decision | Your answer |
|---|---|
| attribute argument grammar | |
| supported attached item kind | |
| signature contract | |
| preserved visibility and attributes | |
| preserved original function | |
| generated companion items | |
| name-collision policy | |
| diagnostic spans | |

Build the smallest valid **attribute ownership and item preservation** surface first. Add one accepted case, one rejection owned by this mechanism, and one case that expands successfully before ordinary Rust rejects a later obligation. Compare with the reference only after those three phase boundaries are protected by tests.

### Laboratory acceptance trace

Before opening the reference implementation for **Checked Handler Attribute**, record:

- the public behavior that demonstrates **Parse attribute arguments independently from the attached item**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Implement `#[command_handler]` as a validating augmentation: preserve the handler, validate one owned argument and explicit `Result`, and generate a typed `HandlerDescriptor`. Reject unsupported qualifiers with spanned diagnostics.

The capstone increment must leave a visible design record: one diagram or table, one positive test, one negative test, and one statement of what this mechanism deliberately does **not** own.

### Capstone invariant trace

For the Module 48 CommandForge increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Answer without the chapter:

1. What exactly does the attribute own?
2. Which attached-item properties must be preserved?
3. How can generated typed assignments delegate semantic checking to Rust?
4. Why can attribute ordering affect behavior?

Then perform a ten-minute reconstruction: recreate the smallest useful example for this module from an empty file, including one rejected input. If reconstruction requires copying the chapter, return to the mental model before continuing.

### Completion standard

Use the chapter’s readiness statement as the threshold:

Continue when you can state:

- which transformation mode the attribute uses;
- which item kinds and signatures it supports;
- which original surfaces are preserved or rejected;
- which generated names and visibility are introduced;
- which checks are syntactic versus semantic;
- how configuration attributes affect companions;
- how direct calls differ from catalog-mediated calls;
- what evidence proves the original behavior remains intact.

Do not continue if the macro reconstructs a function from selected fields and silently drops attributes, generics, ABI, or visibility.

Before advancing, defend these module-specific points:

- why replacing the item gives the macro greater responsibility than derive
- which item properties the attribute may change
- what information remains unavailable before type checking
- how generated companion names avoid collisions

### Closed-book defense

In five minutes, answer “How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?” using the **attribute preservation table**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside CommandForge. A list of APIs without the deciding relationship is incomplete.
