# Proof Matrix


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Guides"]
  page["Proof Matrix"]
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

This page maps the course's main design claims to the capstone surface that proves them.
Use it whenever a module makes an important claim and you want the shortest honest route
to evidence instead of browsing the repository at random.

At the course level, `make PROGRAM=python-programming/python-functional-programming test`
now delegates to the capstone's `confirm` target so the default proof route matches the
strongest published confirmation surface. Use `capstone-test` when you only need the raw
pytest suite.

## Core design claims

| Claim | Best first route | Best first surface |
| --- | --- | --- |
| purity is a local reasoning contract, not just a style preference | `make PROGRAM=python-programming/python-functional-programming test` | `tests/unit/fp/`, `tests/unit/result/`, `src/funcpipe_rag/fp/` |
| laziness and streaming stay deliberate under pressure | `make PROGRAM=python-programming/python-functional-programming test` | `tests/unit/streaming/`, `src/funcpipe_rag/streaming/` |
| failure modelling is visible as data instead of hidden control flow | `make PROGRAM=python-programming/python-functional-programming test` | `tests/unit/result/`, `tests/unit/policies/`, `src/funcpipe_rag/result/` |
| configured pipelines preserve explicit composition boundaries | `make PROGRAM=python-programming/python-functional-programming test` | `tests/unit/pipelines/`, `src/funcpipe_rag/pipelines/` |
| effect boundaries stay visible instead of leaking into the core | inspect [`capstone-architecture-guide.md`](../capstone/capstone-architecture-guide.md) | `src/funcpipe_rag/domain/`, `src/funcpipe_rag/boundaries/`, `src/funcpipe_rag/infra/` |
| async coordination remains bounded and reviewable | `make PROGRAM=python-programming/python-functional-programming test` | `tests/unit/domain/`, `src/funcpipe_rag/domain/effects/async_/` |

## Course contract to proof surface

| Course outcome | Best first route | Best first surface |
| --- | --- | --- |
| separate pure transforms from effectful coordination in ordinary Python systems | `make PROGRAM=python-programming/python-functional-programming capstone-test` | `tests/unit/fp/`, `src/funcpipe_rag/fp/`, `src/funcpipe_rag/boundaries/` |
| design pipelines that stay configurable, lazy, and testable under growth | `make PROGRAM=python-programming/python-functional-programming capstone-test` | `tests/unit/pipelines/`, `tests/unit/streaming/`, `src/funcpipe_rag/pipelines/` |
| model expected failures and domain states as data instead of tangled control flow | `make PROGRAM=python-programming/python-functional-programming capstone-test` | `tests/unit/result/`, `src/funcpipe_rag/result/`, `src/funcpipe_rag/fp/validation.py` |
| move infrastructure behind explicit protocols, adapters, and async coordination layers | `make PROGRAM=python-programming/python-functional-programming capstone-tour` | `src/funcpipe_rag/domain/`, `src/funcpipe_rag/infra/`, `src/funcpipe_rag/domain/effects/async_/` |
| sustain a long-lived codebase with evidence, review standards, and migration discipline | `make PROGRAM=python-programming/python-functional-programming proof` | guided bundles under `artifacts/`, review guides, and capstone proof surfaces |

## Capstone review claims

| Review question | Best first route | Best first surface |
| --- | --- | --- |
| where should I start reading the capstone | inspect [`capstone-file-guide.md`](../capstone/capstone-file-guide.md) | `tests/`, then `src/funcpipe_rag/fp/`, `rag/`, and `pipelines/` |
| which package owns the idea from the module I just read | inspect [`capstone/capstone-map.md`](../capstone/capstone-map.md) | the matching package group in `src/funcpipe_rag/` |
| what is the strongest guided proof route | `make PROGRAM=python-programming/python-functional-programming proof` | [`capstone-proof-guide.md`](../capstone/capstone-proof-guide.md), `artifacts/tour/python-programming/python-functional-programming/` |
| what lets a human reviewer inspect the repository quickly | `make PROGRAM=python-programming/python-functional-programming capstone-tour` | [`capstone-walkthrough.md`](../capstone/capstone-walkthrough.md), `package-tree.txt`, `test-tree.txt` |
| which review questions should I carry into a change | inspect [`capstone-review-worksheet.md`](../capstone/capstone-review-worksheet.md) | the matching code and test folders |
| which earlier module state should I compare against | `make PROGRAM=python-programming/python-functional-programming history-refresh` | `capstone/_history/worktrees/module-XX/`, `_history/manifests/module-XX.json`, `capstone/module-reference-states/` |

## Module-to-proof bridge

| Module range | Main module question | Best proof surfaces |
| --- | --- | --- |
| Modules 01 to 03 | what stays pure and lazy | `tests/unit/fp/`, `tests/unit/result/`, `tests/unit/streaming/`, `src/funcpipe_rag/fp/`, `streaming/` |
| Modules 04 to 06 | how failures, laws, and explicit context stay reviewable | `tests/unit/fp/laws/`, `tests/unit/policies/`, `src/funcpipe_rag/result/`, `fp/effects/`, `policies/` |
| Modules 07 to 08 | where effects and async pressure enter | `tests/unit/domain/`, `tests/unit/infra/adapters/`, `src/funcpipe_rag/domain/`, `boundaries/`, `infra/` |
| Modules 09 to 10 | how interop, review, and sustainment stay honest | `tests/unit/interop/`, [`capstone-walkthrough.md`](../capstone/capstone-walkthrough.md), [`capstone-architecture-guide.md`](../capstone/capstone-architecture-guide.md), `course-book/capstone/capstone-review-worksheet.md` |

## Best companions

- [`capstone/command-guide.md`](../capstone/command-guide.md)
- [`capstone-proof-guide.md`](../capstone/capstone-proof-guide.md)
- [`capstone-review-worksheet.md`](../capstone/capstone-review-worksheet.md)
- [`capstone-architecture-guide.md`](../capstone/capstone-architecture-guide.md)
- [`capstone-file-guide.md`](../capstone/capstone-file-guide.md)
