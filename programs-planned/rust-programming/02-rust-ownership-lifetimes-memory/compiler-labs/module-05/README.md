# Module 15 Investigations — Box, Deref, Dynamically Sized Types, and Cow

[Chapter](../../course-book/module-15-box-deref-dynamically-sized-types-and-cow/index.md) · [Workbook](../../course-book/module-15-box-deref-dynamically-sized-types-and-cow/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?

Before invoking a compiler or runner, draw a **indirection model** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Use Box for exclusive heap-owned indirection and recursive finite-size representation without equating Box with shared ownership**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 15 — Box, Deref, Dynamically Sized Types, and Cow, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
