# Module 22 Investigations — Associated Types and Type Families

[Chapter](../../course-book/module-22-associated-types-and-type-families/index.md) · [Workbook](../../course-book/module-22-associated-types-and-type-families/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?

Before invoking a compiler or runner, draw a **associated-type relationship map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Choose between generic parameters and associated types from relationship cardinality**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 22 — Associated Types and Type Families, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
