<a id="top"></a>

# Publish Review Guide


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive Snakemake"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Publish Review Guide"]
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

Use this page when the question is not merely "did the workflow run?" but "what is the
stable published contract and how is it defended?"

---

## Recommended Route

1. Read `capstone/PUBLISH_REVIEW_GUIDE.md`.
2. Run `make -C capstone verify-report` or the course-level equivalent.
3. Compare the report bundle with [Capstone Review Worksheet](capstone-review-worksheet.md) and [Proof Matrix](proof-matrix.md).

[Back to top](#top)

---

## What A Good Review Can Answer

- which promoted files belong to the public contract
- which proofs are about publish trust rather than workflow execution generally
- which future change would require a versioned publish boundary change

[Back to top](#top)
