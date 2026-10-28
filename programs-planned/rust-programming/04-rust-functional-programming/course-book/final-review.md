# Course 4 Final Review — Functional Rust

Begin every part from a blank page. You may use your code and the records you created, but do not follow the chapters line by line. The purpose is to expose whether the model can be reconstructed and transferred.

## Part 1 — Reconstruct the ten questions

For each question, supply a smallest working example, a causal negative example, the earliest decisive phase or event, a requirement-preserving repair, and one limit on the evidence you would use.

31. **Closures, Capture, and Callable Contracts** — What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?
32. **The Iterator Model** — What state does an iterator own, when does work happen, and what is consumed by each call to next?
33. **Iterator Algebra and Pipeline Shape** — How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?
34. **Folds, Scans, and Short-Circuiting** — What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?
35. **Option, Result, and Fallible Traversal** — Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?
36. **Custom Iterators and Collection Protocols** — What laws must a custom traversal obey, and who owns the collection when iteration begins?
37. **Recursive Data and Structural Sharing** — How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?
38. **Functional Core and Effect Isolation** — Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?
39. **Combinator Laws and Cost Models** — What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?
40. **Functional Architecture Synthesis** — How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?

API names without the governing relationship do not answer this part.

## Part 2 — Independent construction

Build this product without copying a course domain:

> Build a deterministic route-analysis engine whose parser, fallible transformation, reductions, persistent history, borrowed queries, and effect shell can be tested independently.

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

Apply this change to LedgerFlow:

> Add balance checkpoints to LedgerFlow without introducing a second source of truth for event order or reducer semantics.

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

Select one guarantee from Course 3 — Traits, Generics, and Architectural Design and prove that the new construction does not regress it.

Trace one requirement from input to internal state, effect, output, and test. If Course 4 introduces a stronger mechanism, explain why the earlier simpler design is no longer sufficient rather than assuming that greater abstraction is automatically better.

## Part 5 — Diagnosis sprint

Choose three unfamiliar cases from the course: one valid, one rejected by an early decisive phase, and one that compiles or runs while violating the product contract. Freeze the prediction, use a **whole-pipeline architecture map**, observe the result, and explain every mismatch between prediction and evidence.

## Part 6 — Oral defense

- **Module 31 — Closures, Capture, and Callable Contracts:** answer “What does a closure capture, which callable traits does it implement, and what invocation contract should an API require?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 32 — The Iterator Model:** answer “What state does an iterator own, when does work happen, and what is consumed by each call to next?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 33 — Iterator Algebra and Pipeline Shape:** answer “How do adapters change item type, cardinality, order, ownership, and stopping behavior across a pipeline?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 34 — Folds, Scans, and Short-Circuiting:** answer “What invariant does an accumulator maintain, and when should a traversal continue, emit intermediate state, or stop early?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 35 — Option, Result, and Fallible Traversal:** answer “Should a fallible traversal skip, fail fast, recover, accumulate diagnostics, or continue with an explicit default?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 36 — Custom Iterators and Collection Protocols:** answer “What laws must a custom traversal obey, and who owns the collection when iteration begins?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 37 — Recursive Data and Structural Sharing:** answer “How can recursive values be transformed without hiding ownership, rebuilding cost, or structural sharing?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 38 — Functional Core and Effect Isolation:** answer “Which decisions can remain pure, which effects must occur at the boundary, and what data should cross between them?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 39 — Combinator Laws and Cost Models:** answer “What semantic laws should a combinator preserve, and what can honestly be claimed about evaluation and cost?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.
- **Module 40 — Functional Architecture Synthesis:** answer “How do closure, iterator, error, reduction, structural-sharing, and effect decisions compose into a readable whole system?” using one positive trace, one causal negative trace, one principled repair, one rejected shortcut, and one case where a simpler mechanism is sufficient.

End with a fifteen-minute defense of LedgerFlow: product and non-goals, ownership and authority, main invariant, failure model, ordering and bounds, one difficult proof boundary, one rejected shortcut, evidence limits, and the handoff to the next course.

## Completion standard

Course 4 — Functional Rust is complete when another competent Rust reader can reproduce the product behavior and causal explanation from your public contract, tests, and reasoning records. You must be able to say which claims are guaranteed by Rust, supplied by a library, chosen by the product, conditioned on a target or peer, or merely observed for one artifact and workload.

## Seven-day retention check

Without opening the course, redraw the ten-module chain and the core **whole-pipeline architecture map**. Rebuild one small example in a new domain. Revisit only the relationships you cannot recover, then repeat the reconstruction rather than rereading the answer passively.
