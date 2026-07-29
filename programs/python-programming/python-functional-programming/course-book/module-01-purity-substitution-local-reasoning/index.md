# Module 01: Purity, Substitution, and Local Reasoning


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Purity Substitution Local Reasoning"]
  page["Module 01: Purity, Substitution, and Local Reasoning"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

This module teaches the semantic floor for the whole course:

- which functions are safe to reason about locally;
- which kinds of hidden state break substitution;
- how immutable values expose domain transitions;
- how to refactor toward explicit dataflow before abstractions get more powerful;
- which laws prove the first FuncPipe state remains stable.

If this module does not feel concrete, later topics like combinators, typed pipelines, and
effect management will feel ornamental instead of useful.

## Keep These Pages Nearby

Use these support surfaces while reading so the semantic floor stays attached to the
course promise and the capstone proof route:

- [First-Contact Map](../module-00-orientation/first-contact-map.md) for the shortest stable entry route
- [Module Promise Map](../guides/module-promise-map.md) for the plain-language contract of the module
- [Module Checkpoints](../guides/module-checkpoints.md) for the exit bar before Module 02
- [Capstone Map](../capstone/capstone-map.md) for the matching core packages and proof surfaces

Carry this question into the module:

> Which code can still be trusted as a local transform, and what immediately stops being substitutable once hidden state or effects enter?

## What You Should Learn Here

- How purity and substitution change the way you review Python code.
- How immutability and value semantics reduce hidden coupling.
- How small composable transforms make testing and refactoring cheaper.
- How to judge whether a rewrite preserves behavior instead of only reshaping syntax.

## Reading Route

Read the pages in this order:

- [FuncPipe Delta](capstone-delta.md) to see why Module 01 creates the first
  application reference state instead of comparing with a nonexistent Module 00
  snapshot
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
- [Exercises](exercises.md)
- [Exercise Answers](exercise-answers.md)

If you are reviewing instead of reading front-to-back:

- Open `Imperative vs Functional`, `Pure Functions and Contracts`, and `Isolating Side Effects` when you need the boundary between pure core and effectful shell.
- Open `Immutability and Value Semantics`, `Higher-Order Composition`, and `Local FP Refactors` when you need to improve real code without changing the behavior.
- Open `Typed Pipelines`, `Equational Reasoning`, and `Idempotent Transforms` when the code is already pure enough that you want stronger review tools.

## Exercises

The [Module 01 Exercises](exercises.md) require you to:

- trace one document through the actual reference-state functions;
- separate a mixed batch transformation from audit recording;
- build and review one typed unary composition;
- test the CSV-to-JSONL effect boundary;
- repair a false fixed-point claim.

Use [Exercise Answers](exercise-answers.md) only after you can state what your
evidence proves and does not prove.

## Capstone Checks

- Inspect the tracked source under
  `capstone/module-reference-states/module-01/src/funcpipe_rag/`.
- Trace `RawDoc -> CleanDoc -> ChunkWithoutEmbedding -> Chunk`.
- Locate the only file owner of CSV and JSONL effects.
- Match every law claim to a named test in `tests/test_laws.py` or
  `tests/learning/test_module_01_purity_foundations.py`.

Run the short learner proof from the course root:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/learning/test_module_01_purity_foundations.py
```

## Before Moving On

You should be able to explain why a function is pure, why that matters for substitution,
and where a thin effect wrapper belongs when purity is impossible. Use
[Refactoring Guide](refactoring-guide.md), complete the exercises, and compare the
tracked state with `capstone/_history/worktrees/module-01` after history refresh.

## Closing Criteria

- You can defend a purity judgment without appealing to taste or syntax alone.
- You can point to the exact place where an effect wrapper belongs when the transform itself cannot stay pure.
- You can compare two implementations and explain whether they are meaning-preserving under substitution.
- You can distinguish deterministic output, an idempotent transform, and a canonical
  completed value.
- You can explain why Module 01 keeps eager lists and explicit orchestration instead
  of importing concepts from later modules.

## Directory Glossary

Use [Glossary](glossary.md) when you want the recurring language in this module kept stable
while you move between lessons, exercises, and capstone checkpoints.
