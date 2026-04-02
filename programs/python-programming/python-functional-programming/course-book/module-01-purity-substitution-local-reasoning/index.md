# Module 01: Purity, Substitution, and Local Reasoning


<!-- page-maps:start -->
## Module Position

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Functional Programming"]
  program --> module["Module 01: Purity, Substitution, and Local Reasoning"]
  module --> lessons["Lesson pages and worked examples"]
  module --> checkpoints["Exercises and closing criteria"]
  module --> capstone["Related capstone evidence"]
```

```mermaid
flowchart TD
  purpose["Start with the module purpose and main questions"] --> lesson_map["Use the lesson map to choose reading order"]
  lesson_map --> study["Read the lessons and examples with one review question in mind"]
  study --> proof["Test the idea with exercises and capstone checkpoints"]
  proof --> close["Move on only when the closing criteria feel concrete"]
```
<!-- page-maps:end -->

Read the first diagram as a placement map: this page sits between the course promise, the lesson pages listed below, and the capstone surfaces that pressure-test the module. Read the second diagram as the study route for this page, so the diagrams point you toward the `Lesson map`, `Exercises`, and `Closing criteria` instead of acting like decoration.

## Keep These Pages Open

Use these support surfaces while reading so the semantic floor stays attached to the
course promise and the capstone proof route:

- [First-Contact Map](../module-00-orientation/first-contact-map.md) for the shortest stable entry route
- [Module Promise Map](../guides/module-promise-map.md) for the plain-language contract of the module
- [Module Checkpoints](../guides/module-checkpoints.md) for the exit bar before Module 02
- [Capstone Map](../guides/capstone-map.md) for the matching core packages and proof surfaces

Carry this question into the module:

> Which code can still be trusted as a local transform, and what immediately stops being substitutable once hidden state or effects enter?

This module establishes the semantic floor for the whole course. If the learner cannot
separate pure transforms from hidden state here, every later abstraction will feel
ornamental instead of necessary.

## Learning outcomes

- how purity and substitution change the way you review Python code
- how immutability and value semantics reduce hidden coupling
- how small composable transforms make testing and refactoring cheaper
- how to judge whether a rewrite preserves behavior instead of only reshaping syntax

## Lesson map

- [Imperative vs Functional](imperative-vs-functional.md)
- [Pure Functions and Contracts](pure-functions-and-contracts.md)
- [Immutability and Value Semantics](immutability-and-value-semantics.md)
- [Higher-Order Composition](higher-order-composition.md)
- [Local FP Refactors](local-fp-refactors.md)
- [Small Combinator Library](small-combinator-library.md)
- [Combinator Laws and Trade-Offs](combinator-laws-and-tradeoffs.md)
- [Typed Pipelines](typed-pipelines.md)
- [Typed Pipeline Review](typed-pipeline-review.md)
- [Isolating Side Effects](isolating-side-effects.md)
- [Equational Reasoning](equational-reasoning.md)
- [Idempotent Transforms](idempotent-transforms.md)
- [Refactoring Guide](refactoring-guide.md)

## Exercises

- Take one helper from the capstone and classify it as pure, effectful, or mixed, then justify the classification in terms of substitution.
- Rewrite one small imperative branch as a value-preserving transform and state what behavioral evidence would prove the refactor safe.
- Pick one input transformation and explain whether repeated application is idempotent, conditional, or unsafe.

## Capstone checkpoints

- Identify which helpers in FuncPipe stay pure across refactors.
- Trace where configuration is explicit instead of ambient.
- Check whether tests prove behavior or only exercise examples.

## Before moving on

You should be able to explain why a function is pure, why that matters for substitution,
and where a thin effect wrapper belongs when purity is impossible. Use
[Refactoring Guide](refactoring-guide.md) and compare against
`capstone/_history/worktrees/module-01` before moving forward.

## Closing criteria

- You can defend a purity judgment without appealing to taste or syntax alone.
- You can point to the exact place where an effect wrapper belongs when the transform itself cannot stay pure.
- You can compare two implementations and explain whether they are meaning-preserving under substitution.
