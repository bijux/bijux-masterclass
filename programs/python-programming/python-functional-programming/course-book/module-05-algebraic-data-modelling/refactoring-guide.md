# Module 05 Refactoring Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  module["Module 05"] --> guide["Refactoring Guide"]
  guide --> worktree["_history/worktrees/module-05"]
  worktree --> next["Module 06"]
```

```mermaid
flowchart TD
  shape["Inspect the domain shapes"] --> smart["Check smart constructors and validation"]
  smart --> match["Review pattern matching and serialization"]
  match --> laws["Read the algebraic law tests"]
  laws --> move["Move on only when the model is explicit"]
```
<!-- page-maps:end -->

This guide closes Module 05. The learner standard here is explicit modelling. The code
should tell you what states exist, what data is valid, and how transport concerns stay
outside the core model.

## Stable comparison route

1. run `make PROGRAM=python-programming/python-functional-programming history-refresh`
2. open `capstone/_history/worktrees/module-05/src/funcpipe_rag/`
3. compare `fp/`, `core/rag_types.py`, and `boundaries/serde.py`
4. read the law and validation tests under `capstone/_history/worktrees/module-05/tests/`

## What to refactor toward

- product and sum types that reveal domain meaning without extra commentary
- smart constructors that keep invariants close to the model
- validation that can accumulate multiple problems when that helps the caller
- serialization layers that adapt the model without rewriting it

## Exit standard

Before Module 06, you should be able to justify your chosen data shape and explain how a
reviewer can tell transport format from domain meaning.
