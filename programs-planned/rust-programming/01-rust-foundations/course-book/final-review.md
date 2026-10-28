# Course 1 Final Review — Rust Foundations

Begin every part from a blank page. You may use your code and the records you created, but do not follow the chapters line by line. The purpose is to expose whether the model can be reconstructed and transferred.

## Part 1 — Reconstruct the ten questions

For each question, supply a smallest working example, a causal negative example, the earliest decisive phase or event, a requirement-preserving repair, and one limit on the evidence you would use.

1. **Compilation, Expressions, and Types** — How does Rust turn source text into a typed program, and what type and value does every expression produce?
2. **Control Flow, Functions, and Invariants** — How can control flow make every path, boundary, and loop invariant visible enough to test and review?
3. **Ownership, Moves, Copying, and Destruction** — Who owns each resource after every assignment, call, return, destructure, and scope exit?
4. **Borrowing, References, Slices, and Strings** — Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?
5. **Structs, Enums, Methods, and Pattern Matching** — How can the type system make valid states representable and contradictory states difficult or impossible to construct?
6. **Collections, Iterators, and Closures** — Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?
7. **Errors, Parsing, Files, and Persistence** — Which failures are part of the product contract, where are they detected, and what state is visible after failure?
8. **Generics, Traits, Conversions, and Lifetime Basics** — What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?
9. **Crates, Modules, Public APIs, Tests, and Documentation** — Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?
10. **Integration and Independent Change** — Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?

API names without the governing relationship do not answer this part.

## Part 2 — Independent construction

Build this product without copying a course domain:

> Build a small persistent inventory program from a behavioral contract. It must use typed states, contextual errors, deterministic storage, a library/binary split, and tests that protect both successful and failing behavior.

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

Apply this change to Taskboard:

> Add one cross-layer Taskboard feature—such as due dates or labels—without weakening deterministic storage, typed transitions, or failure atomicity.

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

For Course 1, show that the independent product is understandable to a programmer who knows basic programming but has never seen Rust.

Trace one requirement from input to internal state, effect, output, and test. If Course 1 introduces a stronger mechanism, explain why the earlier simpler design is no longer sufficient rather than assuming that greater abstraction is automatically better.

## Part 5 — Diagnosis sprint

Choose three unfamiliar cases from the course: one valid, one rejected by an early decisive phase, and one that compiles or runs while violating the product contract. Freeze the prediction, use a **whole-program invariant map**, observe the result, and explain every mismatch between prediction and evidence.

## Part 6 — Oral defense

- **Module 1 — Compilation, Expressions, and Types:** answer “How does Rust turn source text into a typed program, and what type and value does every expression produce?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 2 — Control Flow, Functions, and Invariants:** answer “How can control flow make every path, boundary, and loop invariant visible enough to test and review?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 3 — Ownership, Moves, Copying, and Destruction:** answer “Who owns each resource after every assignment, call, return, destructure, and scope exit?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 4 — Borrowing, References, Slices, and Strings:** answer “Which temporary permissions does an operation require, and how narrowly can those permissions be scoped?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 5 — Structs, Enums, Methods, and Pattern Matching:** answer “How can the type system make valid states representable and contradictory states difficult or impossible to construct?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 6 — Collections, Iterators, and Closures:** answer “Does an algorithm borrow, mutate, or consume a collection, and what complexity and invalidation consequences follow?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 7 — Errors, Parsing, Files, and Persistence:** answer “Which failures are part of the product contract, where are they detected, and what state is visible after failure?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 8 — Generics, Traits, Conversions, and Lifetime Basics:** answer “What behavior is genuinely shared, what constraints make it valid, and what borrow relationship must a signature expose?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 9 — Crates, Modules, Public APIs, Tests, and Documentation:** answer “Which surfaces are product contracts, which are implementation details, and what independent evidence protects each boundary?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 10 — Integration and Independent Change:** answer “Can you make and defend a cross-layer change without tutorial imitation or accidental contract regression?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.

End with a fifteen-minute defense of Taskboard: product and non-goals, ownership and authority, main invariant, failure model, ordering and bounds, one difficult proof boundary, one rejected shortcut, evidence limits, and the handoff to the next course.

## Completion standard

Course 1 — Rust Foundations is complete when another competent Rust reader can reproduce the product behavior and causal explanation from your public contract, tests, and reasoning records. You must be able to say which claims are guaranteed by Rust, supplied by a library, chosen by the product, conditioned on a target or peer, or merely observed for one artifact and workload.

## Seven-day retention check

Without opening the course, redraw the ten-module chain and the core **whole-program invariant map**. Rebuild one small example in a new domain. Revisit only the relationships you cannot recover, then repeat the reconstruction rather than rereading the answer passively.
