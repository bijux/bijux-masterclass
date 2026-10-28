# Module 43 Investigations — Recursive Macro Parsing and Token-Tree Techniques

[Chapter](../../course-book/module-43-recursive-macro-parsing-and-token-tree-techniques/index.md) · [Workbook](../../course-book/module-43-recursive-macro-parsing-and-token-tree-techniques/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity?

Before invoking a compiler or runner, draw a **recursive grammar state** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Model recursive macro rules as parser states and transitions**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 43 — Recursive Macro Parsing and Token-Tree Techniques, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
