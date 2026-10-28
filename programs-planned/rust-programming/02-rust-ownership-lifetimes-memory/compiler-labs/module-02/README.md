# Module 12 Investigations — Lifetime Relationships and Borrowed APIs

[Chapter](../../course-book/module-12-lifetime-relationships-and-borrowed-apis/index.md) · [Workbook](../../course-book/module-12-lifetime-relationships-and-borrowed-apis/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?

Before invoking a compiler or runner, draw a **lifetime constraint graph** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Translate lifetime syntax into constraints among borrows rather than durations attached to values**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 12 — Lifetime Relationships and Borrowed APIs, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
