# Module 31 Investigations — Closures, Capture, and Callable Contracts

[Chapter](../../course-book/module-31-closures-capture-and-callable-contracts/index.md) · [Workbook](../../course-book/module-31-closures-capture-and-callable-contracts/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?

Before invoking a compiler or runner, draw a **closure capture map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Distinguish function items, function pointers, and anonymous closure types**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 31 — Closures, Capture, and Callable Contracts, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
