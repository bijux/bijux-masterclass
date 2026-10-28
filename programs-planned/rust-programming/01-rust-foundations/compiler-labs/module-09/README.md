# Module 9 Investigations — Crates, Modules, Public APIs, Tests, and Documentation

[Chapter](../../course-book/module-09-crates-modules-public-apis-tests-and-documentation/index.md) · [Workbook](../../course-book/module-09-crates-modules-public-apis-tests-and-documentation/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?

Before invoking a compiler or runner, draw a **module and API map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Distinguish package, crate, target, and module while organizing code by responsibility rather than one file per type**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 9 — Crates, Modules, Public APIs, Tests, and Documentation, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
