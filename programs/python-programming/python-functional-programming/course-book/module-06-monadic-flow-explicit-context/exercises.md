# Module 06 Exercises

These exercises change or inspect the Module 06 FuncPipe RAG reference state.
Work in the declared core order because each prompt assumes the preceding flow
rules are already understood.

Before opening an answer:

1. write the expected value or trace;
2. name the failure or absence branch;
3. run the named learning test;
4. state which Module 05 behavior must remain true; and
5. record what the evidence cannot establish.

Each exercise supplies a focused acceptance command. Use the broad capstone
suite only after the complete module slice is ready.

## and_then and bind: preserve the first failure

**Starting context:** run
`test_result_chain_short_circuits_before_rag_cleaning` and inspect
`Ok.and_then` and `Err.and_then` in `result/types.py`.

**Objective:** add a title prerequisite before the abstract prerequisite and
prove that a missing title prevents both the abstract check and cleaning.

**Constraints:**

- return an `ErrInfo` value rather than raising;
- record entry into each prerequisite and the cleaning stage;
- keep the checks in declared order;
- do not inspect `.value` outside the successful branch.

**Expected evidence:** a document with no title records only the title check and
returns `TITLE_REQUIRED`; a valid document still normalizes through
`clean_doc`.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k result_chain_short_circuits_before_rag_cleaning
```

Earlier contract preserved: Module 05 typed failure provenance remains visible,
and valid documents retain the same normalized value.

## Lifting plain functions: keep independent inputs independent

**Starting context:** run
`test_liftA2_combines_independent_rag_config_fields` and inspect `liftA2` in
`result/types.py`.

**Objective:** add independently validated `sample_size` and build a frozen
configuration value without making its validation depend on chunk size.

**Constraints:**

- keep each field parser independent;
- preserve left-to-right fail-fast order for `Result`;
- do not catch constructor exceptions inside the pure combiner;
- explain when accumulating `Validation` would be the better choice.

**Expected evidence:** all valid inputs produce the expected configuration;
when the leftmost and rightmost inputs fail, the declared leftmost error is
preserved.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k liftA2_combines_independent_rag_config_fields
```

Earlier contract preserved: Module 05 still distinguishes typed failure values
from successful immutable configuration values.

## Law-guided design: justify a regrouping

**Starting context:** run
`test_result_map_composition_preserves_rag_cleaning` and read the functor
composition law.

**Objective:** add a pure projection from normalized abstract text to word count
and prove that separate and composed map groupings agree.

**Constraints:**

- keep every mapped function pure;
- generate mixed-case and whitespace-heavy abstracts;
- compare complete `Result` values;
- state which product claim the law does not prove.

**Expected evidence:** the generated examples produce the same typed word-count
result for both legal groupings.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k result_map_composition_preserves_rag_cleaning
```

Earlier contract preserved: Module 01 substitution and Module 05 typed values
remain valid inside the Module 06 composition machinery.

## Reader pattern: vary overlap at the call site

**Starting context:** run
`test_reader_runs_same_rag_chunk_program_with_explicit_env` and inspect `asks`
in `fp/effects/reader.py`.

**Objective:** run the same chunking Reader with overlap `0` and overlap `2`,
then explain the changed chunk boundaries.

**Constraints:**

- construct the Reader once;
- pass both `RagEnv` values only to `.run`;
- preserve document identity and text;
- assert exact chunk text order.

**Expected evidence:** the no-overlap and overlap runs produce their exact
declared sequences from one unchanged program.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k reader_runs_same_rag_chunk_program_with_explicit_env
```

Earlier contract preserved: Module 03 chunk order and bounded traversal remain
determined by immutable configuration.

## Explicit state threading: add skipped-chunk progress

**Starting context:** run
`test_state_threads_rag_chunk_progress_without_global_mutation` and inspect
`State.and_then`.

**Objective:** extend the frozen progress value with `skipped` and add a state
operation that records an empty chunk without increasing processed characters.

**Constraints:**

- accept the initial state from the caller;
- return a new frozen progress value;
- preserve operation order;
- leave the original initial value unchanged.

**Expected evidence:** the final state distinguishes processed and skipped
chunks while the result value and starting state remain explicit.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k state_threads_rag_chunk_progress_without_global_mutation
```

Earlier contract preserved: Module 01 immutability and Module 03 chunk ordering
remain observable after local progress is introduced.

## Error-typed flows: narrow the expected exception set

**Starting context:** run
`test_exception_bridge_types_expected_config_failure_only` and inspect
`try_result`.

**Objective:** accept decimal chunk sizes but classify a negative value as a
typed domain error after parsing.

**Constraints:**

- bridge only `ValueError` from `int`;
- perform the positivity check as a pure `Result` step;
- let `RuntimeError` propagate;
- retain distinct parse and range error codes.

**Expected evidence:** numeric positive input succeeds, non-numeric input
returns `CONFIG_PARSE`, negative input returns `CHUNK_SIZE`, and unexpected
runtime failure is raised.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k exception_bridge_types_expected_config_failure_only
```

Earlier contract preserved: Module 05 typed failures retain provenance while
unexpected defects remain exceptions.

## Layered containers: choose the dominant outcome

**Starting context:** run
`test_layer_order_distinguishes_missing_document_from_retrieval_failure` and
inspect both transpose helpers.

**Objective:** add a fourth case for an empty query and decide whether it is
absence or a typed input failure before transposing.

**Constraints:**

- state the public meaning before choosing the container;
- keep retrieval failure distinct from no match;
- round-trip every declared case;
- do not use `None`.

**Expected evidence:** each case retains its meaning after two transposes, and
the chosen empty-query contract is explicit in the type and assertion.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k layer_order_distinguishes_missing_document_from_retrieval_failure
```

Earlier contract preserved: Module 05 `Option` absence and `Result` failure
remain separate observable states.

## Writer pattern: preserve payload while extending the trace

**Starting context:** run
`test_writer_preserves_rag_chunk_while_accumulating_trace` and inspect
`Writer.and_then`.

**Objective:** append the chunk’s document ID, span, and embedding readiness as
three ordered entries without changing the chunk.

**Constraints:**

- use the Module 06 string-entry Writer API;
- retain the exact original chunk value;
- append entries in observation order;
- do not call `print` or a logger.

**Expected evidence:** `run_writer` returns the original chunk and an exact
three-entry tuple.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k writer_preserves_rag_chunk_while_accumulating_trace
```

Earlier contract preserved: Module 05 immutable RAG values are unchanged while
Module 06 adds inspectable trace data.

## Refactoring try/except: preserve the boundary contract

**Starting context:** run
`test_refactored_config_boundary_matches_characterized_behavior` and compare
the two local parsers.

**Objective:** characterize leading whitespace and signed integer input before
removing the legacy parser.

**Constraints:**

- compare complete typed results;
- retain exact error code and message behavior;
- keep the expected exception class narrow;
- run the unexpected-exception test from the preceding core.

**Expected evidence:** legacy and refactored parsers agree on the expanded input
table, and an unrelated runtime defect still raises.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k "refactored_config_boundary or exception_bridge"
```

Earlier contract preserved: public Module 05 success and failure values remain
stable while Module 06 changes internal control flow.

## Configurable pipelines: assemble policy once

**Starting context:** run
`test_validation_toggle_changes_policy_without_duplicating_rag_pipeline` and
inspect `toggle_validation`.

**Objective:** add a minimum-title validation toggle while retaining one
normalization function.

**Constraints:**

- select policy when constructing the callable;
- do not add a flag argument to `normalize`;
- prove disabled mode is the original pipeline;
- record whether normalization executes.

**Expected evidence:** enabled invalid input short-circuits before normalization;
disabled input follows the unchanged base pipeline exactly once.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k validation_toggle_changes_policy_without_duplicating_rag_pipeline
```

Earlier contract preserved: the pure RAG normalizer retains its Module 01
input-output behavior while Module 06 changes assembly policy.
