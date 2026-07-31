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

## Static capabilities: make time an explicit dependency

**Starting context:** read `Clock`, `Logger`, `MonotonicTestClock`, and
`CollectingLogger`, then run
`test_clock_and_logger_capabilities_make_time_explicit`.

**Objective:** record three chunk identifiers and prove each timestamp increases
by exactly one microsecond.

**Constraints:**

- accept only `Clock` and `Logger` capabilities;
- use the deterministic clock adapter;
- assert the complete structured log trace;
- do not call the system clock directly.

**Expected evidence:** three ordered entries carry deterministic, strictly
increasing timestamps.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-07
PYTHONPATH=src pytest -q tests/learning/test_module_07_effect_boundaries.py \
  -k clock_and_logger_capabilities_make_time_explicit
```

Earlier contract preserved: explicit context remains visible as in Module 06;
capability protocols make each permitted effect narrower and statically named.

## Composing effects: preserve the primary read result

**Starting context:** read `logged_read` in `domain/composition.py`, then run
`test_logged_read_composes_capabilities_without_eager_effects`.

**Objective:** wrap two separate paths, perform both plans, and prove each
result and log entry retains the requested path in order.

**Constraints:**

- construct both plans before performing either;
- keep storage and logger as separate capabilities;
- assert the logger remains empty during construction;
- consume each returned iterator only after interpretation.

**Expected evidence:** two typed read results and two ordered path-specific log
entries appear only after the two `perform` calls.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-07
PYTHONPATH=src pytest -q tests/learning/test_module_07_effect_boundaries.py \
  -k logged_read_composes_capabilities_without_eager_effects
```

Earlier contract preserved: Module 03 laziness and Module 06 compositional
reasoning survive the addition of an observational boundary effect.

## Idempotent effects: distinguish attempts from writes

**Starting context:** read `content_key`, `AtomicWriteCap`, and
`idempotent_write`, then run
`test_idempotent_chunk_write_replays_without_duplicate_output`.

**Objective:** replay two logically identical chunk lists whose metadata differs
and explain why the current key still permits only one actual write.

**Constraints:**

- keep chunk text identical;
- change only metadata or embedding values;
- record both attempts and actual writes;
- retain the atomic write-if-absent operation.

**Expected evidence:** both plans return success, two attempts occur, and one
actual write occurs because Module 07 defines content identity from text.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-07
PYTHONPATH=src pytest -q tests/learning/test_module_07_effect_boundaries.py \
  -k idempotent_chunk_write_replays_without_duplicate_output
```

Earlier contract preserved: pure chunk values remain immutable; Module 07
derives a stable boundary key without adding mutation to the RAG core.

## Sessions and transactions: select one terminal action

**Starting context:** read `Session`, `TxProtocol`, and `with_tx`, then run
`test_transaction_bracket_commits_success_and_rolls_back_failure`.

**Objective:** add a commit-failure branch and prove that its error replaces the
successful body result without invoking rollback.

**Constraints:**

- keep the session explicit;
- record begin, body, commit, and rollback calls;
- return typed nested results from the capability;
- interpret only the complete bracket.

**Expected evidence:** body success followed by commit failure returns the commit
error and records `begin`, `write`, `commit` with no rollback.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-07
PYTHONPATH=src pytest -q tests/learning/test_module_07_effect_boundaries.py \
  -k transaction_bracket_commits_success_and_rolls_back_failure
```

Earlier contract preserved: Module 05 typed failures retain their provenance;
the transaction bracket determines cleanup without converting them to
exceptions.

## Incremental migration: preserve ordered read identity

**Starting context:** run
`test_incremental_io_plan_migration_preserves_read_result`, then compare the
direct storage read with the delayed plan in that test.

**Objective:** migrate the projection from document IDs to `(doc_id, categories)`
pairs while keeping the direct and interpreted results equivalent.

**Constraints:**

- change only the projected observable;
- preserve generated inputs and their order;
- keep the boundary call inside `io_delay`;
- compare the complete typed result, not only its length.

**Expected evidence:** the generated examples show the migrated plan neither
changes, drops, nor reorders an observed pair.

**Acceptance check:**

```bash
cd capstone/module-reference-states/module-07
PYTHONPATH=src pytest -q tests/learning/test_module_07_effect_boundaries.py \
  -k incremental_io_plan_migration_preserves_read_result
```

Earlier contract preserved: Module 03 iteration order and Module 05 typed
results remain observable while Module 07 moves effect timing to the shell.
