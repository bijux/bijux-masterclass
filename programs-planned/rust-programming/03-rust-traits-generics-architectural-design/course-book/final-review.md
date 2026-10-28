# Course 3 Final Review — Traits, Generics, and Architectural Design

Begin every part from a blank page. You may use your code and the records you created, but do not follow the chapters line by line. The purpose is to expose whether the model can be reconstructed and transferred.

## Part 1 — Reconstruct the ten questions

For each question, supply a smallest working example, a causal negative example, the earliest decisive phase or event, a requirement-preserving repair, and one limit on the evidence you would use.

21. **Traits as Behavioral Contracts** — What behavior truly belongs in a shared contract, and which laws must every implementation preserve?
22. **Associated Types and Type Families** — When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?
23. **Coherence and Implementation Ownership** — Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?
24. **Static Polymorphism and Opaque Types** — When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?
25. **Trait Objects and Dynamic Polymorphism** — When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?
26. **Composition and OOP-Style Design Without Inheritance** — How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?
27. **Typestate and Capability-Oriented APIs** — Which illegal operations can be removed from the API by representing protocol state and authority in types?
28. **Boundary Traits and Adapters** — How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?
29. **Public API Evolution** — How can a public trait-based API evolve when downstream crates may both call it and implement it?
30. **Architectural Synthesis** — Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?

API names without the governing relationship do not answer this part.

## Part 2 — Independent construction

Build this product without copying a course domain:

> Build a plugin-capable inspection service with one static pipeline, one dynamic registry, a typestate builder, reusable contract tests, and a written compatibility policy.

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

Apply this change to Review Engine:

> Add a versioned rule capability to Review Engine while preserving source compatibility, deterministic rule order, and a clear static-versus-dynamic boundary.

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

Select one guarantee from Course 2 — Ownership, Lifetimes, and Memory and prove that the new construction does not regress it.

Trace one requirement from input to internal state, effect, output, and test. If Course 3 introduces a stronger mechanism, explain why the earlier simpler design is no longer sufficient rather than assuming that greater abstraction is automatically better.

## Part 5 — Diagnosis sprint

Choose three unfamiliar cases from the course: one valid, one rejected by an early decisive phase, and one that compiles or runs while violating the product contract. Freeze the prediction, use a **architecture decision record**, observe the result, and explain every mismatch between prediction and evidence.

## Part 6 — Oral defense

- **Module 21 — Traits as Behavioral Contracts:** answer “What behavior truly belongs in a shared contract, and which laws must every implementation preserve?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 22 — Associated Types and Type Families:** answer “When is a type chosen once by an implementation, when may callers choose it repeatedly, and how should that relationship appear in the API?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 23 — Coherence and Implementation Ownership:** answer “Which crate owns the right to create an implementation, and how can a public design preserve coherence without giving up adaptation?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 24 — Static Polymorphism and Opaque Types:** answer “When should concrete types remain visible to the compiler, and how can an API hide implementation details without erasing static guarantees?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 25 — Trait Objects and Dynamic Polymorphism:** answer “When is run-time heterogeneity real, what information does a trait object erase, and what must remain dispatchable?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 26 — Composition and OOP-Style Design Without Inheritance:** answer “How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 27 — Typestate and Capability-Oriented APIs:** answer “Which illegal operations can be removed from the API by representing protocol state and authority in types?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 28 — Boundary Traits and Adapters:** answer “How should a Rust program adapt external data, effects, closures, and foreign types without contaminating its core model?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 29 — Public API Evolution:** answer “How can a public trait-based API evolve when downstream crates may both call it and implement it?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 30 — Architectural Synthesis:** answer “Given a real source of variation, how do you choose among enums, generics, trait objects, closures, functions, and ordinary composition?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.

End with a fifteen-minute defense of Review Engine: product and non-goals, ownership and authority, main invariant, failure model, ordering and bounds, one difficult proof boundary, one rejected shortcut, evidence limits, and the handoff to the next course.

## Completion standard

Course 3 — Traits, Generics, and Architectural Design is complete when another competent Rust reader can reproduce the product behavior and causal explanation from your public contract, tests, and reasoning records. You must be able to say which claims are guaranteed by Rust, supplied by a library, chosen by the product, conditioned on a target or peer, or merely observed for one artifact and workload.

## Seven-day retention check

Without opening the course, redraw the ten-module chain and the core **architecture decision record**. Rebuild one small example in a new domain. Revisit only the relationships you cannot recover, then repeat the reconstruction rather than rereading the answer passively.
