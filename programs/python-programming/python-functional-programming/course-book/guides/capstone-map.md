# Capstone Map


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Functional Programming"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Capstone Map"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the exact question you need answered"] --> skim["Skim only the sections that match that pressure"]
  skim --> crosscheck["Open the linked module, proof surface, or capstone route"]
  crosscheck --> next_move["Leave with one next decision, page, or command"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

This map turns the capstone into a deliberate study surface instead of a single guide
page. Use it whenever you want to decide where to go next for concrete evidence.

## Capstone route

- Start with [FuncPipe Capstone Guide](capstone.md) for the overall role and purpose.
- Read [Capstone File Guide](capstone-file-guide.md) when you need a code-reading route.
- Read the capstone's local [`PACKAGE_GUIDE.md`](https://github.com/bijux/bijux-masterclass/blob/master/programs/python-programming/python-functional-programming/capstone/PACKAGE_GUIDE.md) when you are already inside the repository and want the same route locally.
- Read [Capstone Test Guide](capstone-test-guide.md) when you want the test suite to function as a review map.
- Read [Capstone Review Worksheet](capstone-review-worksheet.md) when you want an explicit review lens.
- Read [Capstone Architecture Guide](capstone-architecture-guide.md) when you are reviewing package boundaries.
- Read [Capstone Walkthrough](capstone-walkthrough.md) when you want the learner-facing tour story.
- Read the capstone's local [`WALKTHROUGH_GUIDE.md`](https://github.com/bijux/bijux-masterclass/blob/master/programs/python-programming/python-functional-programming/capstone/WALKTHROUGH_GUIDE.md) when you want the repository itself to provide the first-pass reading order.
- Read [Capstone Proof Guide](capstone-proof-guide.md) when you want the verification route.
- Use `make PROGRAM=python-programming/python-functional-programming inspect` when you need the shortest inspection route before choosing a deeper guide.
- Use `make PROGRAM=python-programming/python-functional-programming capstone-verify-report` when you need a saved review bundle instead of only console output.
- Use `make PROGRAM=python-programming/python-functional-programming capstone-confirm` when you need the strongest published confirmation route.
- Read [Capstone Extension Guide](capstone-extension-guide.md) when you want to decide where a new change belongs.

## Module-to-capstone bridge

- Modules 01 to 03 map most directly to `fp/`, `result/`, `streaming/`, and the pipeline core.
- Modules 04 to 06 map most directly to failure containers, algebraic modelling, and configured flows.
- Modules 07 to 08 map most directly to `domain/`, `boundaries/`, `infra/`, and async effect packages.
- Modules 09 to 10 map most directly to `interop/`, review guides, and proof surfaces.

## Module-to-file, test, and proof route

| Module | Best first source surface | Best first test or review surface | Best first command |
| --- | --- | --- | --- |
| Module 01: Purity and substitution | `capstone/src/funcpipe_rag/fp/core.py`, `capstone/src/funcpipe_rag/fp/combinators.py` | `capstone/tests/unit/fp/test_core_chunk_roundtrip.py`, `capstone/tests/unit/fp/test_core_state_machine.py` | `make PROGRAM=python-programming/python-functional-programming capstone-test` |
| Module 02: Data-first APIs and expression style | `capstone/src/funcpipe_rag/pipelines/specs.py`, `capstone/src/funcpipe_rag/pipelines/configured.py` | `capstone/tests/unit/pipelines/test_specs_roundtrip.py`, `capstone/tests/unit/pipelines/test_configured_pipeline.py` | `make PROGRAM=python-programming/python-functional-programming capstone-test` |
| Module 03: Iterators and lazy dataflow | `capstone/src/funcpipe_rag/streaming/`, `capstone/src/funcpipe_rag/tree/` | `capstone/tests/unit/streaming/test_streaming.py`, `capstone/tests/unit/tree/test_tree_folds.py` | `make PROGRAM=python-programming/python-functional-programming capstone-test` |
| Module 04: Resilience and streaming failures | `capstone/src/funcpipe_rag/result/`, `capstone/src/funcpipe_rag/policies/retries.py`, `capstone/src/funcpipe_rag/policies/breakers.py` | `capstone/tests/unit/result/test_result_folds.py`, `capstone/tests/unit/policies/test_retries.py`, `capstone/tests/unit/policies/test_breakers.py` | `make PROGRAM=python-programming/python-functional-programming capstone-verify-report` |
| Module 05: Algebraic data modelling | `capstone/src/funcpipe_rag/fp/validation.py`, `capstone/src/funcpipe_rag/rag/domain/` | `capstone/tests/unit/fp/test_pattern_matching.py`, `capstone/tests/unit/rag/test_stages.py` | `make PROGRAM=python-programming/python-functional-programming capstone-test` |
| Module 06: Monadic flow and explicit context | `capstone/src/funcpipe_rag/fp/effects/`, `capstone/src/funcpipe_rag/result/types.py` | `capstone/tests/unit/fp/test_configurable.py`, `capstone/tests/unit/fp/test_layering.py`, `capstone/tests/unit/result/test_option_result.py` | `make PROGRAM=python-programming/python-functional-programming capstone-verify-report` |
| Module 07: Effect boundaries and resource safety | `capstone/src/funcpipe_rag/boundaries/`, `capstone/src/funcpipe_rag/domain/effects/`, `capstone/src/funcpipe_rag/domain/capabilities.py` | `capstone/tests/unit/domain/test_io_plan_laws.py`, `capstone/tests/unit/domain/test_session.py`, `capstone/tests/unit/domain/test_idempotent.py` | `make PROGRAM=python-programming/python-functional-programming capstone-tour` |
| Module 08: Async FuncPipe and backpressure | `capstone/src/funcpipe_rag/domain/effects/async_/`, `capstone/src/funcpipe_rag/infra/adapters/async_runtime.py` | `capstone/tests/unit/domain/test_async_backpressure.py`, `capstone/tests/unit/domain/test_async_law_properties.py`, `capstone/tests/unit/domain/test_async_resilience.py` | `make PROGRAM=python-programming/python-functional-programming capstone-verify-report` |
| Module 09: Ecosystem interop | `capstone/src/funcpipe_rag/boundaries/shells/cli.py`, `capstone/src/funcpipe_rag/pipelines/cli.py`, `capstone/src/funcpipe_rag/interop/` | `capstone/tests/unit/pipelines/test_cli_overrides.py`, `capstone/tests/unit/interop/test_stdlib_fp.py`, `capstone/tests/unit/interop/test_toolz_compat.py` | `make PROGRAM=python-programming/python-functional-programming capstone-tour` |
| Module 10: Refactoring and sustainment | `capstone/README.md`, `capstone/ARCHITECTURE.md`, `capstone/PROOF_GUIDE.md`, `capstone/pyproject.toml` | `capstone/TOUR.md`, `capstone/WALKTHROUGH_GUIDE.md`, `capstone/PROOF_GUIDE.md` | `make PROGRAM=python-programming/python-functional-programming test` |

Use this table when a module page tells you to inspect the capstone and you want the
smallest stable route from concept to source, proof, and command.
