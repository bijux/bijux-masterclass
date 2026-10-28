# Module 11 Investigations — Places, Move Paths, and Advanced Borrowing

[Chapter](../../course-book/module-11-places-move-paths-and-advanced-borrowing/index.md) · [Workbook](../../course-book/module-11-places-move-paths-and-advanced-borrowing/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?

Before invoking a compiler or runner, draw a **place and move-path map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Distinguish values from places and trace projections, move paths, partial initialization, and later destruction obligations**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 11 — Places, Move Paths, and Advanced Borrowing, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
