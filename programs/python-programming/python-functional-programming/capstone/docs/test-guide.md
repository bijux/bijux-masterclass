# FuncPipe Test Guide


<!-- page-maps:start -->
## Guide Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  guide["Capstone docs"]
  section["Docs"]
  page["FuncPipe Test Guide"]
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

Use this guide when you want the test suite to function as a review map instead of a
large undifferentiated tree.

## Test groups

| Group | Paths | What it proves |
| --- | --- | --- |
| Algebra and laws | `tests/unit/fp/laws/`, `tests/unit/result/`, `tests/unit/tree/` | the reusable functional containers and laws behave as the course claims |
| Functional toolkit | `tests/unit/fp/`, `tests/unit/streaming/` | pure helpers, stream combinators, and local reasoning rules stay stable |
| Domain and async behavior | `tests/unit/domain/` | retries, transactions, async scheduling, and effect descriptions remain explicit |
| Pipeline and policy surfaces | `tests/unit/pipelines/`, `tests/unit/policies/` | configured pipelines and runtime policies stay reviewable instead of hidden |
| Application model | `tests/unit/rag/`, `tests/unit/rag/domain/` | RAG-specific assembly, stages, and domain values preserve their contracts |
| Edges and interop | `tests/unit/boundaries/`, `tests/unit/infra/adapters/`, `tests/unit/interop/` | adapters, serialization, storage, and compatibility helpers stay at the edge |

## Suggested reading order

1. `tests/unit/fp/laws/`
2. `tests/unit/fp/`, `tests/unit/result/`, and `tests/unit/streaming/`
3. `tests/unit/rag/` and `tests/unit/rag/domain/`
4. `tests/unit/pipelines/` and `tests/unit/policies/`
5. `tests/unit/domain/`
6. `tests/unit/boundaries/`, `tests/unit/infra/adapters/`, and `tests/unit/interop/`

That order keeps semantic floor before orchestration and keeps the outer edges last.

## Question to test map

| If the question is about... | Read this test group first | Then open |
| --- | --- | --- |
| algebraic laws, mapping, chaining, folds, or reusable result behavior | `tests/unit/fp/laws/`, `tests/unit/result/`, `tests/unit/tree/` | `src/funcpipe_rag/fp/`, `result/`, `tree/` |
| pure helper behavior, iterator composition, or stream laziness | `tests/unit/fp/`, `tests/unit/streaming/` | `src/funcpipe_rag/fp/`, `streaming/` |
| domain values, stage composition, or RAG-specific rules | `tests/unit/rag/`, `tests/unit/rag/domain/` | `src/funcpipe_rag/core/`, `rag/`, `rag/domain/` |
| configured pipelines, retries, breakers, or runtime policy | `tests/unit/pipelines/`, `tests/unit/policies/` | `src/funcpipe_rag/pipelines/`, `policies/` |
| resource plans, async behavior, capabilities, or effect descriptions | `tests/unit/domain/` | `src/funcpipe_rag/domain/`, `domain/effects/`, `boundaries/` |
| adapters, serialization, storage, or infrastructure edges | `tests/unit/boundaries/`, `tests/unit/infra/adapters/` | `src/funcpipe_rag/boundaries/`, `infra/` |
| stdlib or external-library compatibility | `tests/unit/interop/` | `src/funcpipe_rag/interop/` |

## Failure-first reading order

1. State the behavior that should fail first.
2. Open the matching test group from the table above.
3. Name the owning package before you open implementation files.
4. Escalate into `make inspect`, `make verify-report`, or `make tour` only when the tests need more context.

## Review questions

- Which tests here prove laws or invariants rather than only a happy path?
- Which package should stay unchanged if this test still passes?
- Which proof route should you run after reading this group: `make test`, `make tour`, or `make proof`?
- Which future change would require a new test group instead of another test in the current folder?

## Best companion files

- `PACKAGE_GUIDE.md`
- `PUBLIC_SURFACE_MAP.md`
- `PROOF_GUIDE.md`
- `ARCHITECTURE.md`
