# Module 16 Investigations — Rc, Weak, and Ownership Graphs

[Chapter](../../course-book/module-16-rc-weak-and-ownership-graphs/index.md) · [Workbook](../../course-book/module-16-rc-weak-and-ownership-graphs/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?

Before invoking a compiler or runner, draw a **liveness graph** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Draw strong and weak ownership graphs and derive allocation liveness from roots and reference counts**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 16 — Rc, Weak, and Ownership Graphs, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
