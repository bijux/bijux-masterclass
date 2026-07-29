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
