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

## Web and services: translate before invoking the framework

**Starting context:** read `boundaries/web/documents.py` and
`test_web_payload_translation_exposes_validation_as_a_value`.

**Objective:** add a payload whose `categories` value is not a string and trace
the resulting `ErrInfo` to an HTTP 422 decision in a shell.

**Constraints:**

- do not import FastAPI in the translator
- return a typed failure instead of raising for user input
- identify the failing document index and field
- do not perform RAG processing in the HTTP adapter

**Expected evidence:** valid payloads become immutable `RawDoc` values, invalid
payloads become `Err`, and the shell owns status-code mapping.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_09_interop.py \
  -k web_payload_translation_exposes_validation_as_a_value
```

Earlier contract preserved: Module 04 failures remain data and Module 07 keeps
framework behavior outside the domain core.

## Data and ML pipelines: validate topology before consuming data

**Starting context:** read `pipelines/configured.py` and
`test_configured_pipeline_rejects_invalid_order_before_consumption`.

**Objective:** try the orders `clean → embed` and `clean → chunk`, record their
distinct build failures, and then construct `clean → chunk → embed`.

**Constraints:**

- use the shipped names and parameter keys
- reject invalid topology while building, before iterating documents
- keep the valid pipeline lazy
- inject a fitted or external embedder only through `artifacts`

**Expected evidence:** invalid orders fail without a source pull; the valid order
returns an iterator of `Result[Chunk, ErrInfo]`.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_09_interop.py \
  -k configured_pipeline_rejects_invalid_order_before_consumption
```

Earlier contract preserved: Module 03 controls materialization and Module 06 keeps
configuration explicit rather than hidden in stage closures.

## CLI and config: make misspelled overrides fail closed

**Starting context:** read `pipelines/cli.py` and
`test_cli_override_rejects_a_misspelled_stage_without_mutation`.

**Objective:** apply `chunk.chunk_size=256`, then try the misspelled target
`chnuk.chunk_size=256` and explain why silent success is unsafe.

**Constraints:**

- parse text separately from applying it
- return a new frozen `PipelineConfig`
- reject a target that matches no configured step
- keep file and process I/O in the shell

**Expected evidence:** the original config stays at 512, the new config uses 256,
and the misspelling raises before a RAG run starts.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_09_interop.py \
  -k cli_override_rejects_a_misspelled_stage_without_mutation
```

Earlier contract preserved: configuration remains explicit data and invalid
configuration does not masquerade as a successful execution.

## Distributed dataflow: report capability without pretending to compile

**Starting context:** read `pipelines/distributed.py`,
`distributed-dataflow-review.md`, and
`test_distributed_status_does_not_confuse_installation_with_implementation`.

**Objective:** inspect both backend statuses and explain the difference between an
installed package, a shipped compiler, and a verified backend.

**Constraints:**

- do not install Dask or Beam
- do not claim a compiler exists because an import succeeds
- keep the local pipeline as the semantic oracle
- name the equivalence test required before enabling a compiler

**Expected evidence:** status reports are deterministic about the repository
contract even when local package installation varies.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_09_interop.py \
  -k distributed_status_does_not_confuse_installation_with_implementation
```

Earlier contract preserved: Module 08's ordering, failure, and backpressure
guarantees are requirements on a future backend, not assumptions.

## Functional facades: defer and translate client failure

**Starting context:** read `domain/facades.py` and
`test_facade_defers_client_failure_and_returns_it_as_data`.

**Objective:** make a deterministic fake embedder fail on its second item and
decide whether the facade should return partial success or one batch failure.

**Constraints:**

- constructing `IOPlan` must not call the embedder
- interpreting the plan must not leak the client exception
- preserve stable item keys on success
- state the batch atomicity policy in the test

**Expected evidence:** call count stays zero until `perform`, then the failure is
an `Err` with stage `facade.embed_batch`.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_09_interop.py \
  -k facade_defers_client_failure_and_returns_it_as_data
```

Earlier contract preserved: Module 07 effects remain descriptions and Module 04
keeps expected boundary failures in `Result`.

## Cross-process composition: reject code identity before reconstruction

**Starting context:** read `pipelines/specs.py` and
`test_pipeline_spec_is_hashed_and_allow_listed_before_execution`.

**Objective:** compare two specs that differ only in failure policy, then attempt
to reconstruct one with an empty allow-list.

**Constraints:**

- serialize function identifiers, never callables
- include operator type, identifier, and failure policy in the hash
- check the allow-list before invoking an operator
- keep rejection in `Result`

**Expected evidence:** policy changes alter the hash, disallowed identifiers return
`Err(code="DISALLOWED")`, and the registered callable is never invoked.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_09_interop.py \
  -k pipeline_spec_is_hashed_and_allow_listed_before_execution
```

Earlier contract preserved: Module 05 data modelling and Module 04 failure
policies survive serialization without turning transported data into executable
authority.

## Team adoption: review one boundary chain, not a style slogan

**Starting context:** read
`test_module_09_boundaries_converge_on_one_rag_pipeline`, then trace every call
into `boundaries/web`, `pipelines/cli.py`, and `pipelines/configured.py`.

**Objective:** review a payload-to-chunks run and assign ownership for validation,
override policy, pipeline topology, lazy execution, and embedding failure.

**Constraints:**

- each decision must have one named owner
- cite one executable assertion for every claimed contract
- distinguish a local unit proof from the broad capstone gate
- reject checklist items that only prescribe syntax

**Expected evidence:** one translated `RawDoc` enters the established pipeline,
the CLI-style override changes chunk size without mutation, and three embedded
chunks leave as `Ok`.

**Acceptance check:**

```bash
pytest -q tests/learning/test_module_09_interop.py \
  -k module_09_boundaries_converge_on_one_rag_pipeline
```

Earlier contract preserved: Module 09 adds adapters around one cumulative RAG
application; it does not create separate web, CLI, or dataframe applications.
