# Capstone Test Guide


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Functional Programming"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Capstone Test Guide"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the exact question you need answered"] --> skim["Skim only the sections that match that pressure"]
  skim --> crosscheck["Open the linked module, proof surface, or capstone route"]
  crosscheck --> next_move["Leave with one next decision, page, or command"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for proof-first reading, not for
surveying the whole suite. Read the second diagram as the guide loop: arrive with one
claim to check, read only the matching proof group, then leave with one smaller and more
honest next move.

Use this page when a module tells you to inspect capstone proof and you want a stable
reading route through the test suite.

## Choose the first proof group

| If your current claim is about... | Start here | Then compare with... |
| --- | --- | --- |
| purity, substitution, or lazy dataflow | `tests/unit/fp/`, `tests/unit/result/`, and `tests/unit/streaming/` | [Proof Matrix](../guides/proof-matrix.md) |
| failure modelling, validation, or lawful composition | `tests/unit/fp/laws/`, `tests/unit/policies/`, and `tests/unit/rag/` | [Capstone Review Worksheet](capstone-review-worksheet.md) |
| effect boundaries, adapters, or async pressure | `tests/unit/domain/`, `tests/unit/boundaries/`, and `tests/unit/infra/adapters/` | [Capstone Architecture Guide](capstone-architecture-guide.md) |
| interop, orchestration, or sustainment | `tests/unit/interop/`, `tests/unit/pipelines/`, and the saved proof bundle | [Capstone Proof Guide](capstone-proof-guide.md) |

## Best route

1. Read [Capstone Proof Guide](capstone-proof-guide.md).
2. Start with the one test group that matches the current claim.
3. Run `make PROGRAM=python-programming/python-functional-programming test` only if reading is not enough.
4. Compare the tests you read with [Proof Matrix](../guides/proof-matrix.md) and [Capstone Review Worksheet](capstone-review-worksheet.md).

## Best module-to-test bridge

- Modules 01 to 03:
  start with `tests/unit/fp/`, `tests/unit/result/`, and `tests/unit/streaming/`
- Modules 04 to 06:
  start with `tests/unit/fp/laws/`, `tests/unit/policies/`, and `tests/unit/rag/`
- Modules 07 to 08:
  start with `tests/unit/domain/`, `tests/unit/boundaries/`, and `tests/unit/infra/adapters/`
- Modules 09 to 10:
  start with `tests/unit/interop/`, `tests/unit/pipelines/`, and the capstone proof bundle

## What this page should prevent

- treating every test folder as equally relevant to every module
- reading implementation code before you know what the proof surface promises
- using a large test suite as a vague reassurance instead of as a review map

## Stop here when

- you know the first proof group worth opening
- you know whether reading is enough or you need to run the suite
- you can name which claim the test group is supposed to justify
