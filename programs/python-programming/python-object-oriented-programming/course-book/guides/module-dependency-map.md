# Module Dependency Map


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Object-Oriented Programming"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Module Dependency Map"]
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

This map exists to prevent a common failure mode: reading an advanced chapter without
the earlier concept that gives it meaning.

## What depends on what

- Module 01 is the semantic floor. Nothing later makes sense without it.
- Module 02 depends on Module 01 because object roles only matter after object semantics are clear.
- Module 03 depends on Modules 01 and 02 because lifecycle and typestate need stable ownership.
- Module 04 depends on Modules 01 to 03 because collaboration only works if single-object contracts are already explicit.
- Modules 05 to 07 depend on Module 04 because persistence and runtime pressure should preserve the earlier domain boundaries.
- Modules 08 to 10 depend on all earlier modules because verification, API governance, and operational mastery are audits of the whole design.

## How to use this map

- If a module feels abstract, move one step left and review its prerequisite.
- If a module feels repetitive, ask which new pressure it is adding to the same design.
- If the capstone feels confusing, match the confusion to the earliest module that explains that boundary.

## Honest interpretation

The course is not linear because learning should be rigid. It is linear because later
trade-offs become cheap slogans when the earlier ownership model is missing.
