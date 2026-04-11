# Capstone Architecture Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Capstone"]
  page["Capstone Architecture Guide"]
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

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

Use this page when a module asks you to review the capstone's architecture instead of
only its syntax.

## What to inspect

1. Read [FuncPipe Capstone Guide](index.md).
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
