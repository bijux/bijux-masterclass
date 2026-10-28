# Module 37 Investigations — Recursive Data and Structural Sharing

[Chapter](../../course-book/module-37-recursive-data-and-structural-sharing/index.md) · [Workbook](../../course-book/module-37-recursive-data-and-structural-sharing/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?

Before invoking a compiler or runner, draw a **structural-sharing graph** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Define recursive algebraic data with the appropriate indirection**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 37 — Recursive Data and Structural Sharing, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
