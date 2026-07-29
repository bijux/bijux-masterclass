# Module 07 Exercises

Work from `capstone/module-reference-states/module-07/`. That directory is the
completed Module 07 application state. Module 06 is the before-state, while
Modules 08 and 09 and the live capstone must retain every boundary contract
proved here.

For each exercise, name the domain-owned contract, the shell action that
interprets it, and the concrete infrastructure detail that must remain outside
the pure RAG core.

## Ports and adapters: substitute storage without changing behavior

**Starting context:** read `StorageRead`, `FileStorage`, and `InMemoryStorage`,
then run `test_storage_adapters_preserve_rag_read_behavior`.

**Objective:** add a third document to both fixtures and make the shared
domain-facing function filter one requested category before returning document
identifiers.

**Constraints:**

- keep the function parameter typed as `StorageRead`;
- do not branch on the adapter class;
- compare complete observable results from both adapters;
- do not move CSV parsing into the domain-facing function.

**Expected evidence:** both adapters return the same ordered identifiers for the
requested category.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-07
PYTHONPATH=src pytest -q tests/learning/test_module_07_effect_boundaries.py \
  -k storage_adapters_preserve_rag_read_behavior
```

Earlier contract preserved: the Module 06 RAG computation still consumes
`RawDoc` values and typed failures; only the source of those values changes.

## Effect interfaces: prove description before execution

**Starting context:** read `IOPlan`, `io_delay`, `io_map`, and `perform`, then
run `test_io_plan_defers_rag_read_until_the_shell_performs_it`.

**Objective:** add a second mapped transformation that counts the identifiers,
while retaining a single storage read at interpretation time.

**Constraints:**

- build the complete description before calling `perform`;
- record the boundary call in an event trace;
- keep `perform` in the test shell;
- do not materialize the storage iterator before `io_delay`.

**Expected evidence:** construction records no events, interpretation returns
`Ok(2)`, and the trace contains exactly one read.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-07
PYTHONPATH=src pytest -q tests/learning/test_module_07_effect_boundaries.py \
  -k io_plan_defers_rag_read_until_the_shell_performs_it
```

Earlier contract preserved: Module 06 transformations remain ordinary pure
functions; Module 07 describes only the boundary call that supplies their data.

## Capability protocols: request the least authority

**Starting context:** read `StorageRead`, `StorageWrite`, and `Storage`, then run
`test_read_capability_grants_no_write_authority`.

**Objective:** add a function that counts readable documents and prove it accepts
the read-only adapter without adding a write method.

**Constraints:**

- annotate the dependency as `StorageRead`;
- leave `ReadOnlyDocs` structurally typed;
- do not inherit from the protocol;
- run strict mypy over the learning test after the behavioral check.

**Expected evidence:** the count succeeds, the adapter has no write capability,
and static checking accepts the narrow assignment.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-07
PYTHONPATH=src pytest -q tests/learning/test_module_07_effect_boundaries.py \
  -k read_capability_grants_no_write_authority
MYPYPATH=src mypy --strict --follow-imports=silent \
  tests/learning/test_module_07_effect_boundaries.py
```

Earlier contract preserved: explicit dependencies from Module 06 remain visible;
the protocol narrows what the dependency may do instead of hiding it in an
environment object with unrestricted access.

## Resource safety: close a partial read

**Starting context:** read `FileStorage.read_docs` and
`test_partial_storage_read_closes_the_owned_file`.

**Objective:** consume two rows from a three-row stream, stop, and prove the
owned file closes without requesting the third row.

**Constraints:**

- record when `open` is entered;
- assert construction is lazy;
- close the iterator explicitly;
- do not force the stream to a list.

**Expected evidence:** one open event occurs on first demand, the file remains
open during partial traversal, and explicit close releases it before exhaustion.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-07
PYTHONPATH=src pytest -q tests/learning/test_module_07_effect_boundaries.py \
  -k partial_storage_read_closes_the_owned_file
```

Earlier contract preserved: Module 03 streaming remains demand-driven; Module
07 adds deterministic cleanup without replacing the iterator model.

## Functional logging: separate trace construction from emission

**Starting context:** read `trace_stage`, `trace_value`, `run_writer`, and
`CollectingLogger`, then run
`test_structured_logs_remain_data_until_the_shell_emits_them`.

**Objective:** add a third `TRACE` entry containing the first document
identifier and prove its position before draining all entries to the logger.

**Constraints:**

- keep the primary document list unchanged;
- construct only `LogEntry` values in the Writer program;
- assert the logger is empty before the shell loop;
- preserve entry order.

**Expected evidence:** the Writer returns the original identifiers and three
ordered entries; the collecting logger receives them only during shell
interpretation.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-07
PYTHONPATH=src pytest -q tests/learning/test_module_07_effect_boundaries.py \
  -k structured_logs_remain_data_until_the_shell_emits_them
```

Earlier contract preserved: Module 06 Writer composition still carries the same
primary value; Module 07 gives its accumulated data a domain-owned log shape.
