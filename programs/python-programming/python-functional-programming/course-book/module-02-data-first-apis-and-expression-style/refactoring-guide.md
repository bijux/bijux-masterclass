# Module 02 Refactoring Guide


<!-- page-maps:start -->
## Concept Position

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Functional Programming"]
  program --> module["Module 02: Data-First APIs and Expression Style"]
  module --> concept["Module 02 Refactoring Guide"]
  concept --> capstone["Capstone pressure point"]
```

```mermaid
flowchart TD
  problem["Start with the design or failure question"] --> example["Study the worked example and trade-offs"]
  example --> boundary["Name the boundary this page is trying to protect"]
  boundary --> proof["Carry that question into code review or the capstone"]
```
<!-- page-maps:end -->

Read the first diagram as a placement map: this page is one concept inside its parent module, not a detached essay, and the capstone is the pressure test for whether the idea holds. Read the second diagram as the working rhythm for the page: name the problem, study the example, identify the boundary, then carry one review question forward.

This guide closes Module 02. The goal is to make configuration and composition explicit
enough that changing behavior does not require hidden globals or callback archaeology.

## Stable comparison route

1. run `make PROGRAM=python-programming/python-functional-programming history-refresh`
2. open `capstone/_history/worktrees/module-02/src/funcpipe_rag/api/`
3. compare `config.py`, `core.py`, and `types.py`
4. read `capstone/_history/worktrees/module-02/tests/test_rag_api.py` and `test_fp.py`

## What to refactor toward

- function signatures that accept data directly instead of fishing values out of globals
- closures and partial application only when they make configuration clearer
- composition helpers that expose intermediate values without mutating flow
- tests that show the public API contract, not only the internal helper sequence

## Exit standard

Before Module 03, you should be able to show where configuration enters, how it flows,
and why the API stays inspectable under change.
