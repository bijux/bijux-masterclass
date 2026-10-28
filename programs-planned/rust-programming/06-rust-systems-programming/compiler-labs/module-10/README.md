# Module 60 Investigations — Integrated Systems Design, Testing, and Audit

[Chapter](../../course-book/module-60-integrated-systems-design-and-audit/index.md) · [Workbook](../../course-book/module-60-integrated-systems-design-and-audit/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How do you prove a systems product across binary formats, files, paths, processes, unsafe code, allocation, and FFI without letting one boundary invalidate another?

Before invoking a compiler or runner, draw a **whole-system boundary dossier** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Draw one boundary map from external bytes to final effects and back to foreign callers**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 60 — Integrated Systems Design, Testing, and Audit, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
