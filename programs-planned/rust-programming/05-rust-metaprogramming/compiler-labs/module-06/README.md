# Module 46 Investigations — Procedural Macro Execution and TokenStream Engineering

[Chapter](../../course-book/module-46-procedural-macro-execution-and-tokenstream-engineering/index.md) · [Workbook](../../course-book/module-46-procedural-macro-execution-and-tokenstream-engineering/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?

Before invoking a compiler or runner, draw a **token-stream phase map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Explain when and how a procedural macro executes**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 46 — Procedural Macro Execution and TokenStream Engineering, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
