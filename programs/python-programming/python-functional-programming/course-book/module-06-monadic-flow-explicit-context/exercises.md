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
