# Course 5 Final Review — Rust Metaprogramming

Begin every part from a blank page. You may use your code and the records you created, but do not follow the chapters line by line. The purpose is to expose whether the model can be reconstructed and transferred.

## Part 1 — Reconstruct the ten questions

For each question, supply a smallest working example, a causal negative example, the earliest decisive phase or event, a requirement-preserving repair, and one limit on the evidence you would use.

41. **Metaprogramming Boundaries and the Expansion Model** — Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?
42. **Declarative Macros: Matchers, Fragments, and Repetition** — How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?
43. **Recursive Macro Parsing and Token-Tree Techniques** — How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity?
44. **Hygiene, Scope, Paths, and Cross-Crate Macros** — Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?
45. **Macro Diagnostics, Testing, and Public API Design** — How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API?
46. **Procedural Macro Execution and TokenStream Engineering** — What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?
47. **Custom Derive Macros and Structural Generation** — How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking?
48. **Attribute Macros and Item Transformation** — How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?
49. **Function-Like Procedural Macros and Typed DSLs** — How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?
50. **Build Scripts, Generated Code, and Compile-Time Architecture** — How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?

API names without the governing relationship do not answer this part.

## Part 2 — Independent construction

Build this product without copying a course domain:

> Build a small generated command or protocol catalog using at least two distinct macro mechanisms. Every generated fact must have one authority, targeted invalid-input diagnostics, and expansion tests.

Before implementation, write:

```text
product promise and non-goals
owners and authorities
valid and invalid states
success transition
failure, cleanup, and retry state
order and capacity
external assumptions
public API
verification plan
three rejected designs
```

After implementation, preserve six traces: ordinary success, malformed input, rejected state, partial work before failure, cleanup, and one compatibility, platform, scheduler, workload, or peer edge relevant to this course.

## Part 3 — Capstone change

Apply this change to CommandForge:

> Add a new CommandForge field policy and command kind, tracing the change through grammar, semantic validation, expansion, runtime behavior, tests, and compatibility.

Do not introduce a second source of truth for validation, state, ordering, storage, protocol, scheduling, generation, measurement, or compatibility. Revise the authority map first when the change does not fit the current architecture.

Review the change through:

1. public behavior;
2. owner of the new invariant;
3. state after each failure point;
4. ownership and cleanup;
5. ordering and resource bounds;
6. compatibility or format consequences;
7. independent tests and their limits;
8. the simpler design you rejected.

## Part 4 — Cross-course preservation

Select one guarantee from Course 4 — Functional Rust and prove that the new construction does not regress it.

Trace one requirement from input to internal state, effect, output, and test. If Course 5 introduces a stronger mechanism, explain why the earlier simpler design is no longer sufficient rather than assuming that greater abstraction is automatically better.

## Part 5 — Diagnosis sprint

Choose three unfamiliar cases from the course: one valid, one rejected by an early decisive phase, and one that compiles or runs while violating the product contract. Freeze the prediction, use a **generation authority and reproducibility record**, observe the result, and explain every mismatch between prediction and evidence.

## Part 6 — Oral defense

- **Module 41 — Metaprogramming Boundaries and the Expansion Model:** answer “Which facts deserve generation, and what exactly happens between macro input and the Rust program that finally runs?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 42 — Declarative Macros: Matchers, Fragments, and Repetition:** answer “How do you design a `macro_rules!` invocation as a precise grammar while preserving ownership, evaluation order, and expression semantics?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 43 — Recursive Macro Parsing and Token-Tree Techniques:** answer “How can a declarative macro process a nontrivial token language with explicit parser state, guaranteed progress, and bounded complexity?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 44 — Hygiene, Scope, Paths, and Cross-Crate Macros:** answer “Whose names should generated code resolve, and how do you make exported macros survive nesting, imports, and dependency renaming?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 45 — Macro Diagnostics, Testing, and Public API Design:** answer “How do you prove that a macro accepts the intended language, rejects misuse for the intended reason, and remains an evolvable public API?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 46 — Procedural Macro Execution and TokenStream Engineering:** answer “What does the compiler actually give a procedural macro, what can the macro know, and how should tokens, spans, errors, and effects be handled?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 47 — Custom Derive Macros and Structural Generation:** answer “How do you inspect a Rust item, preserve its generics and constraints, and generate a lawful implementation without pretending to perform type checking?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 48 — Attribute Macros and Item Transformation:** answer “How do you validate and transform an attached item while preserving the parts of its public contract that the attribute does not own?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 49 — Function-Like Procedural Macros and Typed DSLs:** answer “How do you turn custom syntax into an AST, validate cross-entry semantics, normalize the model, and generate compact typed Rust?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 50 — Build Scripts, Generated Code, and Compile-Time Architecture:** answer “How do you integrate macros and build generation into a deterministic architecture with one source of truth and no overlapping authority?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.

End with a fifteen-minute defense of CommandForge: product and non-goals, ownership and authority, main invariant, failure model, ordering and bounds, one difficult proof boundary, one rejected shortcut, evidence limits, and the handoff to the next course.

## Completion standard

Course 5 — Rust Metaprogramming is complete when another competent Rust reader can reproduce the product behavior and causal explanation from your public contract, tests, and reasoning records. You must be able to say which claims are guaranteed by Rust, supplied by a library, chosen by the product, conditioned on a target or peer, or merely observed for one artifact and workload.

## Seven-day retention check

Without opening the course, redraw the ten-module chain and the core **generation authority and reproducibility record**. Rebuild one small example in a new domain. Revisit only the relationships you cannot recover, then repeat the reconstruction rather than rereading the answer passively.
