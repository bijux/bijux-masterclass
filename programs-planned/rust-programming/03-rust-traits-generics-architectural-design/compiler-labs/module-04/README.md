# Module 24 Investigations — Static Polymorphism and Opaque Types

[Chapter](../../course-book/module-24-static-polymorphism-and-opaque-types/index.md) · [Workbook](../../course-book/module-24-static-polymorphism-and-opaque-types/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?

Before invoking a compiler or runner, draw a **static-dispatch map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Design generic functions and types with the weakest sufficient bounds**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 24 — Static Polymorphism and Opaque Types, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
