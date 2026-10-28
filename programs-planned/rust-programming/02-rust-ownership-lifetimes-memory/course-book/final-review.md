# Course 2 Final Review — Ownership, Lifetimes, and Memory

Begin every part from a blank page. You may use your code and the records you created, but do not follow the chapters line by line. The purpose is to expose whether the model can be reconstructed and transferred.

## Part 1 — Reconstruct the ten questions

For each question, supply a smallest working example, a causal negative example, the earliest decisive phase or event, a requirement-preserving repair, and one limit on the evidence you would use.

11. **Places, Move Paths, and Advanced Borrowing** — Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?
12. **Lifetime Relationships and Borrowed APIs** — What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?
13. **Scoped Access and Escape Prevention** — Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?
14. **RAII, Drop, Unwinding, and Failure Atomicity** — Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?
15. **Box, Deref, Dynamically Sized Types, and Cow** — When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?
16. **Rc, Weak, and Ownership Graphs** — Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?
17. **Interior Mutability and Runtime Borrows** — Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?
18. **Memory Representation, Validity, and Layout** — Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?
19. **Subtyping, Variance, PhantomData, and Drop Checking** — When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?
20. **Pinning and Address-Sensitive Design** — What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?

API names without the governing relationship do not answer this part.

## Part 2 — Independent construction

Build this product without copying a course domain:

> Build a revisioned record store with borrowed queries, generational identity, a staged mutation protocol, shared immutable snapshots, and a written liveness and cleanup analysis.

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

Apply this change to Memory Workspace:

> Add document labels and snapshot comparison to Memory Workspace while preserving stale-handle rejection, bounded retention, and borrowed-view provenance.

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

Select one guarantee from Course 1 — Rust Foundations and prove that the new construction does not regress it.

Trace one requirement from input to internal state, effect, output, and test. If Course 2 introduces a stronger mechanism, explain why the earlier simpler design is no longer sufficient rather than assuming that greater abstraction is automatically better.

## Part 5 — Diagnosis sprint

Choose three unfamiliar cases from the course: one valid, one rejected by an early decisive phase, and one that compiles or runs while violating the product contract. Freeze the prediction, use a **pinning contract**, observe the result, and explain every mismatch between prediction and evidence.

## Part 6 — Oral defense

- **Module 11 — Places, Move Paths, and Advanced Borrowing:** answer “Which places, projections, move paths, and loans are active at each program point, and how can access be decomposed safely?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 12 — Lifetime Relationships and Borrowed APIs:** answer “What provenance and outlives relationships must hold for every returned or stored reference, and which relationships should remain independent?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 13 — Scoped Access and Escape Prevention:** answer “Who chooses a lifetime, and how can an API expose temporary access while making escape unrepresentable?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 14 — RAII, Drop, Unwinding, and Failure Atomicity:** answer “Which value owns each cleanup obligation, when does destruction run, and what state remains after early return, error, or panic?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 15 — Box, Deref, Dynamically Sized Types, and Cow:** answer “When is indirection required by representation or ownership, what metadata travels with a pointer, and when should an API borrow-or-own conditionally?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 16 — Rc, Weak, and Ownership Graphs:** answer “Which edges keep allocations alive, which only observe, and how does the graph dismantle when roots disappear?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 17 — Interior Mutability and Runtime Borrows:** answer “Which logically hidden mutation justifies runtime enforcement, and how can guard scope and reentrancy remain controlled?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 18 — Memory Representation, Validity, and Layout:** answer “Is a claim a language guarantee, a standard-library contract, a target-conditioned fact, a current observation, or an unsupported assumption?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 19 — Subtyping, Variance, PhantomData, and Drop Checking:** answer “When may a longer-lived capability substitute for a shorter requirement, and what semantic relationships must marker types communicate?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 20 — Pinning and Address-Sensitive Design:** answer “What invariant becomes invalid after mechanical movement, who promises not to move the value, and can the design avoid address sensitivity entirely?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.

End with a fifteen-minute defense of Memory Workspace: product and non-goals, ownership and authority, main invariant, failure model, ordering and bounds, one difficult proof boundary, one rejected shortcut, evidence limits, and the handoff to the next course.

## Completion standard

Course 2 — Ownership, Lifetimes, and Memory is complete when another competent Rust reader can reproduce the product behavior and causal explanation from your public contract, tests, and reasoning records. You must be able to say which claims are guaranteed by Rust, supplied by a library, chosen by the product, conditioned on a target or peer, or merely observed for one artifact and workload.

## Seven-day retention check

Without opening the course, redraw the ten-module chain and the core **pinning contract**. Rebuild one small example in a new domain. Revisit only the relationships you cannot recover, then repeat the reconstruction rather than rereading the answer passively.
