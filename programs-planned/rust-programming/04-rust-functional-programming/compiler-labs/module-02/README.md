# Module 32 Investigations — The Iterator Model

[Chapter](../../course-book/module-32-the-iterator-model/index.md) · [Workbook](../../course-book/module-32-the-iterator-model/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** What state does an iterator own, when does work happen, and what is consumed by each call to next?

Before invoking a compiler or runner, draw a **iterator state trace** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Explain the distinct roles of `IntoIterator`, `Iterator`, adapters, and consumers**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 32 — The Iterator Model, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
