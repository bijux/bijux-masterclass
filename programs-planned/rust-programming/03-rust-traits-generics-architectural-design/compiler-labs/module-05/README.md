# Module 25 Investigations — Trait Objects and Dynamic Polymorphism

[Chapter](../../course-book/module-25-trait-objects-and-dynamic-polymorphism/index.md) · [Workbook](../../course-book/module-25-trait-objects-and-dynamic-polymorphism/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?

Before invoking a compiler or runner, draw a **dynamic-dispatch map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Derive whether a trait is dyn-compatible and repair it without erasing its meaning**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 25 — Trait Objects and Dynamic Polymorphism, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
