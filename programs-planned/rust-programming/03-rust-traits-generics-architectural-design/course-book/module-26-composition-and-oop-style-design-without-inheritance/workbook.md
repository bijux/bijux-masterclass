# Workbook — Module 26: Composition and OOP-Style Design Without Inheritance

[Chapter](index.md) · [Laboratory](../../labs/module-06-composed-renderer/README.md) · [Review Engine guide](../capstone.md) · [Solutions](solutions.md)

This workbook tests whether **Composition and OOP-Style Design Without Inheritance** has become a usable model rather than remembered vocabulary. Its governing question is: *How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?* Preserve your first prediction and record decisive facts in a **composition diagram**. A repair succeeds only when it keeps the difficult product requirement visible.

## Retrieval warm-up

Before compiling or running anything:

1. Restate the invariant from Module 25 — Trait Objects and Dynamic Polymorphism that today’s mechanism must preserve.
2. Rewrite the governing question in your own words: **How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?**
3. Draw the smallest **composition diagram** that could decide one positive and one negative case.
4. Name one shortcut that could make the visible example pass while deleting ownership, failure, ordering, capacity, safety, compatibility, or evidence required by the product.

## Part 1 — Predict

For each specimen, write a five-part diagnosis: expected outcome; decisive expression or signature; governing rule; smallest requirement-preserving repair; and one tempting change that would compile while weakening the design. Tie every answer to **Composition and OOP-Style Design Without Inheritance** rather than quoting a diagnostic without explaining its cause.

| # | Specimen | Your prediction |
|---:|---|---|
| 1 | [`01-private-invariant.rs`](../../compiler-labs/module-06/01-private-invariant.rs) | Pass or fail? What exact rule decides? |
| 2 | [`02-private-field-construction.rs`](../../compiler-labs/module-06/02-private-field-construction.rs) | Pass or fail? What exact rule decides? |
| 3 | [`03-generic-delegation.rs`](../../compiler-labs/module-06/03-generic-delegation.rs) | Pass or fail? What exact rule decides? |
| 4 | [`04-recursive-wrapper-sizing.rs`](../../compiler-labs/module-06/04-recursive-wrapper-sizing.rs) | Pass or fail? What exact rule decides? |
| 5 | [`05-closed-command-enum.rs`](../../compiler-labs/module-06/05-closed-command-enum.rs) | Pass or fail? What exact rule decides? |
| 6 | [`06-nonexhaustive-state-handling.rs`](../../compiler-labs/module-06/06-nonexhaustive-state-handling.rs) | Pass or fail? What exact rule decides? |
| 7 | [`07-unmet-composition-bound.rs`](../../compiler-labs/module-06/07-unmet-composition-bound.rs) | Pass or fail? What exact rule decides? |
| 8 | [`08-capability-intersection.rs`](../../compiler-labs/module-06/08-capability-intersection.rs) | Pass or fail? What exact rule decides? |

Run all specimens for this course from the course root with:

```bash
python3 ../tools/run_compiler_labs.py 03-rust-traits-generics-architectural-design
```

## Part 2 — Diagnose and repair

A ported design contains `BaseEntity`, `NamedEntity`, `StoredEntity`, and `RenderableStoredEntity` traits. Implementations provide dummy methods, and callers depend on broad bounds.

Repair by identifying domain invariants, consumer capabilities, closed states, and replaceable strategies. At least one hierarchy level must become an enum, one must disappear into an inherent method, and one must become composition.

## Part 3 — Focused exercises

1. Translate encapsulation, polymorphism, inheritance, and composition into Rust mechanisms.
2. Replace getter traits with domain operations.
3. Build a generic strategy and a dynamic strategy; state selection time.
4. Implement an adapter whose translation can fail.
5. Implement a decorator and test that it preserves ordering and errors.
6. Compare command enum with handler registry.
7. Replace an object-state pattern with an enum.
8. Replace a deep supertrait hierarchy with capability intersections.
9. Identify a wrapper that should not implement `Deref`.
10. Design the capstone's rule/factory/reporter composition boundaries.

### Replace the hierarchy

A design document proposes `BaseRenderer`, `HtmlRenderer`, `RedactingHtmlRenderer`, and `TimedRedactingHtmlRenderer`. Rebuild it using owned components:

- a core renderer;
- a redaction strategy;
- an output adapter;
- an optional timing decorator.

Draw the ownership graph and show where each responsibility can be replaced independently. Identify one combination the inheritance tree makes awkward but composition makes ordinary.

### Delegation discipline

Write a wrapper that delegates a trait while changing exactly one behavior. List which methods should forward, which should be redefined, and which default methods might accidentally bypass the wrapper's policy. Explain why delegation is a contract decision rather than boilerplate to generate blindly.

### State modeling

A document may be draft, reviewed, or published. Compare:

1. one struct with a `Status` enum;
2. a trait implemented by three state objects;
3. typestate parameters;
4. three unrelated concrete structs.

Choose based on whether state is runtime data, whether heterogeneous documents coexist, and whether illegal operations must be absent from the API. Do not use dynamic dispatch merely because the states have different names.

### Adapter versus decorator

For each case, choose and justify: convert a foreign logger into your `Reporter` port; add metrics around an existing reporter; translate domain errors into CLI exit codes; change a renderer's output format. State whether the wrapper changes interface, behavior, or both.

: composition map

Produce a component diagram for Review Engine. Every arrow must be labeled ownership, borrowing, static generic use, or dynamic trait-object use. Remove one trait that represents no actual substitution need.

### Interleaved reasoning pass

1. For **Model encapsulation, substitution, and delegation without class inheritance**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the composition diagram.
2. For **Apply composition, strategy, adapter, decorator, and command patterns selectively**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the composition diagram.
3. For **Separate domain state from interchangeable behavior**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the composition diagram.
4. For **Detect inheritance-shaped trait hierarchies and replace them with smaller capabilities**, construct one smallest positive case and one causal negative case. Mark the earliest phase or event that distinguishes them in the composition diagram.

5. Identify one guarantee from an earlier course that a careless implementation of **Composition and OOP-Style Design Without Inheritance** could regress.

For one case, write both a principled repair and a weaker repair that appears to work. The principled repair must preserve the requirement; the weaker repair must name the information, state, bound, or compatibility promise it silently discards.

## Part 4 — Independent laboratory

Build a report-rendering system with two base formats and two optional wrappers.

Requirements:

- the report domain has no formatting trait methods;
- base formats implement one narrow formatter contract;
- signature and line-number behavior use composition;
- one static composition path and one runtime-selected path are demonstrated;
- a closed enum alternative is implemented for comparison;
- tests prove wrappers preserve base errors and deterministic ordering;
- the design memo rejects an inheritance-shaped hierarchy.

The executable starter and reference implementation are in [module-06-composed-renderer](../../labs/module-06-composed-renderer/README.md). Implement from the contract first. Compare with the reference only after your tests pass or you have written a precise blocker.

### Laboratory acceptance trace

Before opening the reference implementation for **Composed Renderer**, record:

- the public behavior that demonstrates **Model encapsulation, substitution, and delegation without class inheritance**;
- one adversarial input, state transition, schedule, peer action, workload, or build condition appropriate to this module;
- the exact state after rejection or partial failure;
- ownership and cleanup;
- ordering and capacity;
- one shortcut deliberately excluded by the contract;
- one claim the tests cannot establish.

## Part 5 — Capstone transfer

Separate policy parsing, factory construction, rule execution, and reporting. The engine must not become a god object. Add a closure-rule adapter and one diagnostic decorator, then decide whether that decorator is generic or erased.

Document why rule types do not inherit from a common base struct and why shared data, if any, is composed in a helper value.

### Capstone invariant trace

For the Module 26 Review Engine increment, name the changed invariant and its owner before editing code. Follow it through input, validation, state transition, effect, output, failure, cleanup, and tests. Add storage, wire, scheduler, generated-code, compatibility, resource, or measurement consequences when this course makes them relevant. End by naming one earlier guarantee that remains unchanged.

## Part 6 — Reconstruct and defend

Pass when you can refactor an inheritance-shaped design into domain state plus capabilities, test a decorator's semantic transparency, and defend a closed enum against an open trait object under different requirements.

Oral prompt: **“Where does this design use composition, and which invariant would inheritance have obscured?”**
### Closed-book reconstruction

1. Which Rust mechanisms replace inheritance’s state reuse, behavior reuse, and substitution claims?
2. When is delegation preferable to a default trait method?
3. What law must a decorator preserve to remain transparent?
4. How do strategies differ from commands and adapters?
5. Which domain states belong in an enum rather than an object hierarchy?

### Independent transfer

Refactor an inheritance-shaped notification service into explicit domain state plus composed capabilities. Include one strategy, one adapter, and one decorator. For every layer, name the invariant it owns and one test that would expose accidental semantic change.

### Closed-book defense

In five minutes, answer “How do you obtain encapsulation, substitution, and reusable behavior through composition rather than inheritance?” using the **composition diagram**. Include one positive case, one causal negative case, one principled repair, one rejected shortcut, and one transfer outside Review Engine. A list of APIs without the deciding relationship is incomplete.
