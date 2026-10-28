# Module 28 Investigations — Boundary Traits and Adapters

[Chapter](../../course-book/module-28-boundary-traits-and-adapters/index.md) · [Workbook](../../course-book/module-28-boundary-traits-and-adapters/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?

Before invoking a compiler or runner, draw a **adapter boundary map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Design extension traits, closure adapters, and conversion boundaries with precise contracts**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 28 — Boundary Traits and Adapters, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
