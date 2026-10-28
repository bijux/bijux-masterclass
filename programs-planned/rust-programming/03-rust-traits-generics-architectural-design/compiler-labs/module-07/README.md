# Module 27 Investigations — Typestate and Capability-Oriented APIs

[Chapter](../../course-book/module-27-typestate-and-capability-oriented-apis/index.md) · [Workbook](../../course-book/module-27-typestate-and-capability-oriented-apis/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** Which illegal operations can be removed from the API by representing protocol state and authority in types?

Before invoking a compiler or runner, draw a **typestate transition graph** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Encode a finite protocol with marker states and consuming transitions**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 27 — Typestate and Capability-Oriented APIs, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
