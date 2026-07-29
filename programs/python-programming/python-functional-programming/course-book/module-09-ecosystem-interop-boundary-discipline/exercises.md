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

## Helper libraries: require semantic parity

**Starting context:** read `interop/toolz_compat.py` and
`test_optional_helper_facade_preserves_plain_python_semantics`.

**Objective:** decide whether optional composition helpers earn their dependency
cost for a normalize-filter-project pipeline.

**Constraints:**

- import only through `funcpipe_rag.interop.toolz_compat`
- keep the result identical whether `toolz` is installed or absent
- keep the iterator lazy until the final `list`
- state what readability gain would justify enabling the dependency

**Expected evidence:** mixed-case padded strings normalize, empty strings are
removed, and the final projection preserves encounter order.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_09_interop.py \
  -k optional_helper_facade_preserves_plain_python_semantics
```

Earlier contract preserved: optional packages do not change the domain value or
failure model established in Modules 04 through 06.

## Data processing: separate record normalization from dataframe choice

**Starting context:** read `interop/dataframes.py` and
`test_record_adapter_normalizes_without_mutating_boundary_input`.

**Objective:** add a second record with missing `abstract` data and decide whether
the boundary should normalize it to an empty string or reject it.

**Constraints:**

- do not require pandas, Polars, or Dask
- do not mutate the input dictionaries
- preserve unrelated fields
- state where strict schema validation belongs

**Expected evidence:** normalization is idempotent, input rows remain unchanged,
and the chosen missing-value policy is visible in an assertion.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_09_interop.py \
  -k record_adapter_normalizes_without_mutating_boundary_input
```

Earlier contract preserved: Module 01 value semantics and Module 05 validation
remain independent of the optional tabular implementation.
