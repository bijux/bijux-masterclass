# Module 45 Investigations — Macro Diagnostics, Testing, and Public API Design

[Chapter](../../course-book/module-45-macro-diagnostics-testing-and-public-api-design/index.md) · [Workbook](../../course-book/module-45-macro-diagnostics-testing-and-public-api-design/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API?

Before invoking a compiler or runner, draw a **diagnostic contract** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Treat invocation grammar and generated Rust as two related public APIs**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 45 — Macro Diagnostics, Testing, and Public API Design, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
