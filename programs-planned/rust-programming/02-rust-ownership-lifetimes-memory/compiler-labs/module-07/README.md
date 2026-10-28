# Module 17 Investigations — Interior Mutability and Runtime Borrows

[Chapter](../../course-book/module-17-interior-mutability-and-runtime-borrows/index.md) · [Workbook](../../course-book/module-17-interior-mutability-and-runtime-borrows/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?

Before invoking a compiler or runner, draw a **runtime-borrow trace** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Explain UnsafeCell as the primitive behind interior mutability while remaining within safe APIs**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 17 — Interior Mutability and Runtime Borrows, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
