# Module 5 Investigations — Structs, Enums, Methods, and Pattern Matching

[Chapter](../../course-book/module-05-structs-enums-methods-and-pattern-matching/index.md) · [Workbook](../../course-book/module-05-structs-enums-methods-and-pattern-matching/workbook.md) · [Course investigation method](../README.md)

> **Prediction question:** How can the type system make valid states representable and contradictory states difficult or impossible to construct?

Before invoking a compiler or runner, draw a **state model** and classify the expected result. The prediction must identify the earliest decisive phase or event and show why the result follows from **Choose structs, tuple structs, newtypes, enums, and associated data from domain shape rather than language familiarity**. Diagnostic wording may vary; the causal relationship may not.

After observing Module 5 — Structs, Enums, Methods, and Pattern Matching, preserve two repairs. The first is the smallest change that keeps the product requirement. The second is a tempting change that compiles, runs, or quiets the tool by erasing information, weakening a bound, changing ownership, hiding a failure, or narrowing the public contract. Explain precisely why the second repair is unacceptable here.

Finish by creating a new specimen that changes one relationship while keeping every incidental detail stable. Predict whether that variation changes parsing, name resolution, type checking, trait solving, borrow checking, build execution, runtime behavior, schedule behavior, or only architectural quality.
