# Module 20 Investigations — Pinning and Address-Sensitive Design

[Chapter](../../course-book/module-20-pinning-and-address-sensitive-design/index.md) · [Workbook](../../course-book/module-20-pinning-and-address-sensitive-design/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?

Before invoking a compiler or runner, draw a **pinning contract** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Distinguish ownership movement from mechanical relocation and identify genuine address-sensitive invariants**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 20 — Pinning and Address-Sensitive Design, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
