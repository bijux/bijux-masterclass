# Capstone Architecture Guide


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Functional Programming"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Capstone Architecture Guide"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the exact question you need answered"] --> skim["Skim only the sections that match that pressure"]
  skim --> crosscheck["Open the linked module, proof surface, or capstone route"]
  crosscheck --> next_move["Leave with one next decision, page, or command"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

Use this page when a module asks you to review the capstone's architecture instead of
only its syntax.

## What to inspect

1. Read `capstone/docs/ARCHITECTURE.md`.
2. Compare it with [FuncPipe Capstone Guide](index.md) and [Capstone File Guide](capstone-file-guide.md).
3. Inspect `tests/`, then `src/funcpipe_rag/fp/`, `rag/`, `pipelines/`, `domain/`, and `boundaries/` in that order.

## What the architecture should prove

- the pure functional core is still visibly separate from concrete effects
- failures and composition rules are carried by explicit packages instead of hidden branching
- policies and pipelines encode orchestration without swallowing the domain model
- adapters and interop surfaces remain visible edges instead of slowly owning the core

## Best use inside the course

- Use it after Module 03 to confirm that purity and dataflow still have a concrete home.
- Revisit it after Modules 06 to 08 to confirm that composition and async pressure did not blur the boundaries.
- Revisit it again in Module 10 when reviewing interop, evidence, and sustainment.
