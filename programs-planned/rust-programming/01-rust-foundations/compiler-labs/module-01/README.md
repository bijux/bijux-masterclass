# Module 1 Investigations — Compilation, Expressions, and Types

[Chapter](../../course-book/module-01-compilation-expressions-and-types/index.md) · [Workbook](../../course-book/module-01-compilation-expressions-and-types/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How does Rust turn source text into a typed program, and what type and value does every expression produce?

Before invoking a compiler or runner, draw a **type trace** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Distinguish package, crate, target, module, compiler, Cargo, profile, and artifact without collapsing them into “the project”**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 1 — Compilation, Expressions, and Types, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
