# Module 06 Exercises: Review One Explicit RAG Flow

These six exercises use the Module 06 FuncPipe reference state. They form one
review sequence: classify dependencies, justify regrouping, make context
explicit, preserve outcome meanings, add inspectable policy, and prove a
refactor.

Before opening the answers, record:

1. the expected complete value;
2. the operation that must not run on the stopping route;
3. the Module 05 behavior that must remain true; and
4. one claim the focused evidence cannot support.

Work from:

```text
capstone/module-reference-states/module-06/
```

Use the focused commands below. Do not begin with the broad capstone suite.

## 1. Classify and compose the document flow

**Starting context:** inspect `Ok.map`, `Ok.and_then`, `Err.map`, and
`Err.and_then` in `src/funcpipe_rag/result/types.py`. Run:

```bash
PYTHONPATH=src pytest -q \
  tests/learning/test_module_06_explicit_context.py \
  -k result_chain_short_circuits_before_rag_cleaning
```

**Objective:** add a title prerequisite before the abstract prerequisite, then
project the successful `CleanDoc` to its normalized abstract.

**Constraints:**

- each prerequisite returns `Result[RawDoc, ErrInfo]`;
- `clean_doc` remains an ordinary pure function;
- record entry into both prerequisites and cleaning;
- a missing title stops before the abstract check;
- a missing abstract stops before cleaning; and
- use `map` only for the final plain projection.

**Expected evidence:** three input rows—missing title, missing abstract, and
valid—produce exact Results and exact call traces.

**Earlier contract preserved:** valid Module 05 values normalize identically,
and typed error provenance remains visible.

**Review question:** why would accumulating Validation be a better fit if the
product required both missing-field errors in one response?

## 2. Prove one legal regrouping

**Starting context:** run:

```bash
PYTHONPATH=src pytest -q \
  tests/learning/test_module_06_explicit_context.py \
  -k result_map_composition_preserves_rag_cleaning
```

Then inspect `tests/test_monad_laws.py`.

**Objective:** add a pure `word_count: str -> int` projection and compare:

```text
source.map(clean_doc).map(abstract).map(word_count)
```

with one `map` containing the same function order.

**Constraints:**

- generate mixed-case and whitespace-heavy abstracts;
- compare complete Result values;
- do not reverse or duplicate any function;
- keep observation out of the mapped functions; and
- name the exact law supporting the rewrite.

**Expected evidence:** both groupings agree across the generated input domain.

**Earlier contract preserved:** Module 01 substitution and Module 05 Result
values retain their meanings.

**Review question:** what RAG correctness or performance claims remain
unproven?

## 3. Make read-only policy and changing progress explicit

**Starting context:** run:

```bash
PYTHONPATH=src pytest -q \
  tests/learning/test_module_06_explicit_context.py \
  -k "reader_runs_same_rag_chunk_program or state_threads_rag_chunk_progress"
```

**Objective:** use one Reader program to chunk the same document with
`RagEnv(chunk_size=4, overlap=0)` and
`RagEnv(chunk_size=4, overlap=2)`. Then account for every emitted chunk with
State.

**Constraints:**

- construct the Reader once;
- supply each environment only at `.run`;
- give State a caller-created frozen `Progress`;
- return a new progress value for each chunk;
- assert exact chunk text order and final character total; and
- keep the initial progress unchanged.

**Expected evidence:** the two policies yield their predicted overlapping
sequences, and State reports progress for each sequence from the same initial
value.

**Earlier contract preserved:** Module 03 demand order and Module 05 immutable
values remain observable.

**Review question:** identify one simpler implementation using ordinary
arguments and a fold. Which version would you keep here, and why?

## 4. Preserve parse failure, invalid value, absence, and retrieval failure

**Starting context:** run:

```bash
PYTHONPATH=src pytest -q \
  tests/learning/test_module_06_explicit_context.py \
  -k "exception_bridge or layer_order"
```

**Objective:** extend chunk-size parsing with a pure positivity check, then add
an empty-query case to the retrieval model.

**Constraints:**

- catch only `ValueError` around `int(raw)`;
- return `CONFIG_PARSE` for non-numeric text;
- return `CHUNK_SIZE` for a parsed non-positive integer;
- let `RuntimeError` propagate;
- classify an empty query before choosing its container;
- preserve valid no-match as `Ok(NoneVal())`; and
- round-trip found, missing, failed, and empty-query cases through both
  transpose helpers.

**Expected evidence:** every case retains a distinct complete value and
unexpected failure remains an exception.

**Earlier contract preserved:** Module 05 `Option` absence and `Result` failure
remain different public meanings.

**Review question:** when would a dedicated retrieval sum type communicate the
four cases better than nested generic containers?

## 5. Add trace and policy without replacing the payload

**Starting context:** run:

```bash
PYTHONPATH=src pytest -q \
  tests/learning/test_module_06_explicit_context.py \
  -k "writer_preserves_rag_chunk or validation_toggle"
```

Also run `PYTHONPATH=src pytest -q tests/test_configurable.py`.

**Objective:** create strict and permissive normalization callables. Wrap the
selected callable with a Writer trace containing document ID, selected policy,
and final status.

**Constraints:**

- keep one normalization function;
- choose strictness during callable construction;
- invalid strict input must skip normalization;
- permissive input must normalize exactly once;
- Writer must preserve the complete Result payload;
- entries must appear in declared order; and
- do not print or call a logging backend.

**Expected evidence:** exact call traces, exact Result payloads, and exact
Writer entries for strict failure and permissive success.

**Earlier contract preserved:** the Module 01 normalizer and Module 05 typed
failure values do not change.

**Review question:** should rejected input produce trace data in your wrapper
order? State the policy before implementing it.

## 6. Defend the complete refactor

**Starting context:** run:

```bash
PYTHONPATH=src pytest -q \
  tests/learning/test_module_06_explicit_context.py \
  -k "refactored_config_boundary or explicit_flow_refactor"
```

**Objective:** expand parser characterization to whitespace and signed
integers, then extend the RAG equivalence property to valid overlap values.
Finish a context ledger for Result, Reader, State, Writer, and the policy
wrapper used in your solution.

**Constraints:**

- change no parsing policy during the parser rewrite;
- generate `chunk_size` before constrained overlap;
- compare complete embedded chunk lists;
- preserve normalization, offsets, order, and embeddings;
- prove an unrelated exception still raises; and
- recommend removing any context that does not improve ownership or review.

**Expected evidence:** old and new parsers agree on the expanded table; direct
and explicit flows agree over generated valid environments; the ledger states
why each remaining context earns its cost.

**Earlier contract preserved:** all observable FuncPipe behavior from Modules
01–05 remains equal over the exercised domain.

**Review question:** why does equivalence support safe change without proving
that the new design is better?

## Completion record

Before Module 07, write a short handoff containing:

- one dependent operation and its stopping case;
- one legal law-guided regrouping;
- one context you kept and one you rejected;
- the distinction between parse failure, invalid domain value, absence, and
  retrieval failure;
- one complete RAG preservation claim; and
- the focused command supporting each statement.
