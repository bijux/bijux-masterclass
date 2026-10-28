# Module 19 Investigations — Subtyping, Variance, PhantomData, and Drop Checking

[Chapter](../../course-book/module-19-subtyping-variance-phantomdata-and-drop-checking/index.md) · [Workbook](../../course-book/module-19-subtyping-variance-phantomdata-and-drop-checking/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?

Before invoking a compiler or runner, draw a **variance and substitution table** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **State lifetime subtype direction through substitutability and derive covariance, contravariance, and invariance operationally**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 19 — Subtyping, Variance, PhantomData, and Drop Checking, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
