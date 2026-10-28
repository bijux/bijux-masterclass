# Module 7 Investigations — Errors, Parsing, Files, and Persistence

[Chapter](../../course-book/module-07-errors-parsing-files-and-persistence/index.md) · [Workbook](../../course-book/module-07-errors-parsing-files-and-persistence/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** Which failures are part of the product contract, where are they detected, and what state is visible after failure?

Before invoking a compiler or runner, draw a **error map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Distinguish absence, recoverable failure, invariant violation, process failure, and ordinary values**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 7 — Errors, Parsing, Files, and Persistence, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
