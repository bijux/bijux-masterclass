<a id="top"></a>

# Capstone Walkthrough


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive Snakemake"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Capstone Walkthrough"]
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

Use this page when you want the capstone as a guided first-contact repository tour rather
than as a fully executed proof bundle.

---

## Recommended Route

1. Read `capstone/docs/WALKTHROUGH_GUIDE.md`.
2. Run `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough`.
3. Read the copied `Snakefile`, rule files, `list-rules.txt`, and `dryrun.txt` in that order.
4. Use [Capstone Review Worksheet](capstone-review-worksheet.md) to write down what is visible before execution.

[Back to top](#top)

---

## What The Walkthrough Should Teach

- what the workflow claims to build before it runs
- where dynamic discovery is declared rather than hidden
- which files are public contracts and which files are only review aids
- which next command should deepen the review once first contact is clear

[Back to top](#top)
