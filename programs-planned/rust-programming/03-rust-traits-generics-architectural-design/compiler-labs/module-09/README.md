# Module 29 Investigations — Public API Evolution

[Chapter](../../course-book/module-29-public-api-evolution/index.md) · [Workbook](../../course-book/module-29-public-api-evolution/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How can a public trait-based API evolve when downstream crates may both call it and implement it?

Before invoking a compiler or runner, draw a **compatibility matrix** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Classify public trait changes by downstream source-compatibility risk**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 29 — Public API Evolution, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
