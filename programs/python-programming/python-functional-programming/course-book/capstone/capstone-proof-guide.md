# Capstone Proof Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Capstone"]
  page["Capstone Proof Guide"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

Use this page when a lesson makes a design claim and you want the most direct evidence in
the capstone.

## Proof route

Do not execute this section as a top-to-bottom command list. Choose one escalation
path for the claim you actually need to prove.

1. Read [FuncPipe Capstone Guide](index.md).
2. Run `make PROGRAM=python-programming/python-functional-programming inspect` when you need the fastest inventory of package, test, and guide ownership.
3. Read tests in this order when you need the shortest honest proof:
   `tests/unit/fp/`, `tests/unit/result/`, `tests/unit/rag/`, `tests/unit/pipelines/`,
   `tests/unit/policies/`, `tests/unit/domain/`, `tests/unit/boundaries/`,
   `tests/unit/infra/`, then `tests/unit/interop/`.
4. Run `make PROGRAM=python-programming/python-functional-programming capstone-test`
   when you want the pytest suite without the wider walkthrough or bundle routes.
5. Choose exactly one artifact route when another person needs saved evidence:
   `capstone-verify-report` for a review bundle, `capstone-tour` for a guided bundle,
   or `proof` for both inspection and tour surfaces.
6. Run `make PROGRAM=python-programming/python-functional-programming test` or
   `capstone-confirm` only for the strictest lint, type, build, review, and proof
   confirmation.
7. Use [Capstone Review Worksheet](capstone-review-worksheet.md) to decide whether the
    evidence is strong enough.

Every route from `capstone-test` upward executes the full pytest suite once per
invocation. Composite routes reuse one saved test report across their bundles.
Running several routes separately repeats the same suite and is not a stronger
proof unless the source or configuration changed between runs.

## Test-reading route by pressure

| If you need to prove... | Open these tests first | Then cross-check with |
| --- | --- | --- |
| pure transforms and lawful composition | `tests/unit/fp/` and `tests/unit/result/` | `src/funcpipe_rag/fp/` and `src/funcpipe_rag/result/` |
| retrieval modelling, validation, and domain choices | `tests/unit/rag/` and `tests/unit/policies/` | `src/funcpipe_rag/rag/` and `src/funcpipe_rag/policies/` |
| pipeline assembly and effect boundaries | `tests/unit/pipelines/`, `tests/unit/domain/`, and `tests/unit/boundaries/` | `src/funcpipe_rag/pipelines/`, `src/funcpipe_rag/domain/`, and `src/funcpipe_rag/boundaries/` |
| adapter and interoperability seams | `tests/unit/infra/` and `tests/unit/interop/` | `src/funcpipe_rag/infra/` and `src/funcpipe_rag/interop/` |

## What you should be able to answer after proof review

- Which package owns the checked behavior?
- Which test or artifact confirmed it?
- Which future change would require stronger or different proof?
