# Module Dependency Map


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Functional Programming"]
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

This map exists to prevent a common failure mode: reading a later lesson without the
earlier concept that makes it necessary.

## What depends on what

- Module 01 is the semantic floor. Nothing later is persuasive without it.
- Module 02 depends on Module 01 because data-first APIs only help after purity and substitution are clear.
- Module 03 depends on Modules 01 and 02 because laziness only helps if dataflow remains inspectable.
- Modules 04 to 06 depend on that earlier floor because failure modelling and lawful chaining need stable dataflow and explicit boundaries.
- Modules 07 to 08 depend on Modules 01 to 06 because effect boundaries and async pressure are audits of whether the earlier functional story survives contact with reality.
- Modules 09 to 10 depend on everything before them because interop and sustainment are long-horizon reviews of the full design.

## How to use this map

- If a lesson feels abstract, move one step left and review its prerequisite.
- If a lesson feels repetitive, ask what new pressure it adds to the same pipeline model.
- If the capstone feels dense, match the confusion to the earliest module that explains the boundary.
