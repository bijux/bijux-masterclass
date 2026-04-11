# FuncPipe Package Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  guide["Capstone docs"]
  section["Docs"]
  page["FuncPipe Package Guide"]
  proof["Proof route"]

  family --> program --> guide --> section --> page
  page -.checks against.-> proof
```

```mermaid
flowchart LR
  orient["Read the guide boundary"] --> inspect["Inspect the named files, targets, or artifacts"]
  inspect --> run["Run the confirm, demo, selftest, or proof command"]
  run --> compare["Compare output with the stated contract"]
  compare --> review["Return to the course claim with evidence"]
```
<!-- page-maps:end -->

Use this guide when you want a stable code-reading route through the capstone. The point
is not to read files alphabetically. The point is to understand which package owns which
kind of reasoning pressure.

## Recommended reading order

1. `tests/unit/fp/`, `tests/unit/result/`, and `tests/unit/streaming/`
2. `src/funcpipe_rag/fp/`, `result/`, `tree/`, and `streaming/`
3. `src/funcpipe_rag/core/`, `rag/`, and `rag/domain/`
4. `src/funcpipe_rag/pipelines/` and `policies/`
5. `src/funcpipe_rag/domain/`, `boundaries/`, and `infra/`
6. `src/funcpipe_rag/interop/`

That order keeps proof before abstraction and keeps the pure core visible before you hit
effects and integrations.

## Package groups

| Group | Paths | Owns | First matching tests |
| --- | --- | --- | --- |
| Functional core | `src/funcpipe_rag/fp/`, `result/`, `tree/`, `streaming/` | reusable algebra, containers, folds, and lazy stream behavior | `tests/unit/fp/`, `tests/unit/result/`, `tests/unit/tree/`, `tests/unit/streaming/` |
| RAG model | `src/funcpipe_rag/core/`, `rag/`, `rag/domain/` | chunk shapes, stage composition, RAG assembly, and domain values | `tests/unit/rag/`, `tests/unit/rag/domain/` |
| Orchestration and policy | `src/funcpipe_rag/pipelines/`, `policies/` | configured pipelines, policies, and runtime choices that stay explicit | `tests/unit/pipelines/`, `tests/unit/policies/` |
| Effect boundaries | `src/funcpipe_rag/domain/`, `domain/effects/`, `boundaries/`, `infra/` | capabilities, adapters, effect descriptions, shells, and concrete runtime edges | `tests/unit/domain/`, `tests/unit/boundaries/`, `tests/unit/infra/adapters/` |
| Interop | `src/funcpipe_rag/interop/` | bridges to stdlib and external library styles | `tests/unit/interop/` |

## Start with the question you have

| If you are asking... | Open these source packages first | Then open these proofs |
| --- | --- | --- |
| Where do the pure helpers and composition primitives live? | `src/funcpipe_rag/fp/`, `result/`, `tree/`, `streaming/` | `tests/unit/fp/`, `tests/unit/result/`, `tests/unit/tree/`, `tests/unit/streaming/` |
| Where does the RAG-specific domain model live? | `src/funcpipe_rag/core/`, `rag/`, `rag/domain/` | `tests/unit/rag/`, `tests/unit/rag/domain/` |
| Where do configured pipelines and policy choices live? | `src/funcpipe_rag/pipelines/`, `policies/` | `tests/unit/pipelines/`, `tests/unit/policies/` |
| Where do effect descriptions and execution boundaries begin? | `src/funcpipe_rag/domain/`, `domain/effects/`, `boundaries/`, `infra/` | `tests/unit/domain/` |
| Where do library bridges and compatibility layers live? | `src/funcpipe_rag/interop/` | `tests/unit/interop/` |

## Short routes by course pressure

### Purity, substitution, and local reasoning

1. `src/funcpipe_rag/fp/core.py`
2. `src/funcpipe_rag/core/rag_types.py`
3. `tests/unit/fp/test_core_chunk_roundtrip.py`
4. `tests/unit/fp/test_core_state_machine.py`

### Data-first APIs and explicit configuration

1. `src/funcpipe_rag/rag/rag_api.py`
2. `src/funcpipe_rag/rag/config.py`
3. `src/funcpipe_rag/pipelines/configured.py`
4. `tests/unit/rag/test_api.py`
5. `tests/unit/pipelines/test_configured_pipeline.py`

### Iterators, laziness, and streaming pressure

1. `src/funcpipe_rag/rag/chunking.py`
2. `src/funcpipe_rag/rag/streaming_rag.py`
3. `src/funcpipe_rag/streaming/fanout.py`
4. `src/funcpipe_rag/streaming/time.py`
5. `tests/unit/streaming/test_streaming.py`

### Failure handling, validation, and explicit context

1. `src/funcpipe_rag/result/`
2. `src/funcpipe_rag/fp/validation.py`
3. `src/funcpipe_rag/fp/effects/`
4. `tests/unit/result/`
5. `tests/unit/fp/test_configurable.py`
6. `tests/unit/result/test_option_result.py`

### Ports, adapters, resource safety, and async work

1. `src/funcpipe_rag/domain/capabilities.py`
2. `src/funcpipe_rag/domain/effects/`
3. `src/funcpipe_rag/boundaries/`
4. `src/funcpipe_rag/infra/adapters/`
5. `tests/unit/domain/`

### Interop and long-lived project review

1. `src/funcpipe_rag/interop/`
2. `src/funcpipe_rag/pipelines/cli.py`
3. `src/funcpipe_rag/boundaries/shells/cli.py`
4. `tests/unit/interop/`
5. `tests/unit/pipelines/test_cli_overrides.py`

## Review questions by group

- Functional core:
  Which helpers stay pure, lawful, and lazily composable?
- RAG model:
  Which values and stage boundaries define the application-specific semantics?
- Orchestration and policy:
  Which choices are configurable policy rather than hidden control flow?
- Effect boundaries:
  Which package describes effects and which one actually executes them?
- Interop:
  Which compatibility helper can disappear without corrupting the core model?

## What this guide prevents

- starting in adapters and mistaking them for the center of the design
- reading the pipeline shell before you know what the pure stages promise
- treating every package as equally effectful or equally important
- changing an interop layer without knowing which proofs should stay unchanged

## Best companion files

- `ARCHITECTURE.md`
- `TEST_GUIDE.md`
- `PUBLIC_SURFACE_MAP.md`
- `PROOF_GUIDE.md`
