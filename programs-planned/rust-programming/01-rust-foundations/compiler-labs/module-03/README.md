# Module 3 Investigations — Ownership, Moves, Copying, and Destruction

[Chapter](../../course-book/module-03-ownership-moves-copying-and-destruction/index.md) · [Workbook](../../course-book/module-03-ownership-moves-copying-and-destruction/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** Who owns each resource after every assignment, call, return, destructure, and scope exit?

Before invoking a compiler or runner, draw a **ownership ledger** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Trace ownership through bindings, calls, returns, aggregates, and scopes using a move-path ledger**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 3 — Ownership, Moves, Copying, and Destruction, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
