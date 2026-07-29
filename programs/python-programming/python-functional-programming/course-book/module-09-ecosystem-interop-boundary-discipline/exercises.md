# Module 09 Exercises

These exercises modify or review the Module 09 FuncPipe RAG reference state. Work
from `capstone/_history/worktrees/module-09` after running the history refresh, or
use the tracked source at `capstone/module-reference-states/module-09`.

For every exercise, preserve the Module 08 contracts: deterministic stages,
explicit failures, bounded consumption, and effects interpreted only at a boundary.

## Standard library tools: prove laziness before preferring a helper

**Starting context:** read `interop/stdlib_fp.py`, `rag/stdlib_fp.py`, and
`test_stdlib_interop_defers_source_consumption`.

**Objective:** explain why `merge_streams` can join document sources without
materializing them, then add a third source to the test.

**Constraints:**

- do not convert an input iterable to `list`
- do not add a dependency
- observe source pulls rather than inspecting iterator internals
- keep source order stable

**Expected evidence:** before the first `next`, the source-pull log is empty; each
`next` adds exactly the pull needed for that value.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_09_interop.py \
  -k stdlib_interop_defers_source_consumption
```

Earlier contract preserved: Module 03's lazy traversal remains true at the Module
09 interop boundary.
