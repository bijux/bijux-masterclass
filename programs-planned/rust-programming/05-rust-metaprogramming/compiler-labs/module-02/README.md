# Module 42 Investigations — Declarative Macros: Matchers, Fragments, and Repetition

[Chapter](../../course-book/module-42-declarative-macros-matchers-fragments-and-repetition/index.md) · [Workbook](../../course-book/module-42-declarative-macros-matchers-fragments-and-repetition/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?

Before invoking a compiler or runner, draw a **matcher and fragment trace** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Read a matcher as a grammar rather than as textual substitution**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 42 — Declarative Macros: Matchers, Fragments, and Repetition, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
