# Module 49 Investigations — Function-Like Procedural Macros and Typed DSLs

[Chapter](../../course-book/module-49-function-like-procedural-macros-and-typed-dsls/index.md) · [Workbook](../../course-book/module-49-function-like-procedural-macros-and-typed-dsls/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?

Before invoking a compiler or runner, draw a **DSL syntax-to-model map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Design a bounded custom grammar with explicit compatibility space**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 49 — Function-Like Procedural Macros and Typed DSLs, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
