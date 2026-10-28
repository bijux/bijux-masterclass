# Module 56 Investigations — Raw Pointers, Provenance, and Uninitialized Memory

[Chapter](../../course-book/module-56-raw-pointers-provenance-and-uninitialized-memory/index.md) · [Workbook](../../course-book/module-56-raw-pointers-provenance-and-uninitialized-memory/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How do you manipulate addresses and storage without accidentally creating an invalid reference, leaving uninitialized values live, or performing pointer arithmetic outside its allocation?

Before invoking a compiler or runner, draw a **initialization and provenance map** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Distinguish raw pointers from references and explain why conversion does not transfer ownership**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 56 — Raw Pointers, Provenance, and Uninitialized Memory, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
