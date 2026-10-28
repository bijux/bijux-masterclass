# Module 44 Investigations — Hygiene, Scope, Paths, and Cross-Crate Macros

[Chapter](../../course-book/module-44-hygiene-scope-paths-and-cross-crate-macros/index.md) · [Workbook](../../course-book/module-44-hygiene-scope-paths-and-cross-crate-macros/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?

Before invoking a compiler or runner, draw a **hygiene and path map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Distinguish textual scope, path-based scope, and expansion-site lookup for declarative macros**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 44 — Hygiene, Scope, Paths, and Cross-Crate Macros, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
