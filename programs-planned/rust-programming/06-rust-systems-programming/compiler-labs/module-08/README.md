# Module 58 Investigations — C FFI: ABI, Strings, Pointers, and Error Boundaries

[Chapter](../../course-book/module-58-c-ffi-abi-strings-and-error-boundaries/index.md) · [Workbook](../../course-book/module-58-c-ffi-abi-strings-and-error-boundaries/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How do you cross a C ABI while keeping representation, ownership, nullability, string encoding, failure, and unwinding contracts explicit on both sides?

Before invoking a compiler or runner, draw a **ABI table** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Distinguish ABI compatibility from semantic validity and ownership**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 58 — C FFI: ABI, Strings, Pointers, and Error Boundaries, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
