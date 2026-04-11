# Capstone Extension Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Capstone"]
  page["Capstone Extension Guide"]
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

Use this guide when changing the DVC capstone after the course is already in use.

The goal is not to forbid growth. The goal is to keep new work from weakening the state,
promotion, and recovery contracts the course depends on.

---

## Boundaries That Must Stay Legible

These boundaries should remain explicit:

* source data versus derived state
* declared pipeline contract versus recorded execution state
* internal repository state versus `publish/v1/`
* local cache convenience versus remote-backed durability

---

## Safe Kinds Of Change

These changes are usually safe when reviewed carefully:

* adding a new internal stage whose dependencies and outputs are fully declared
* enriching the publish bundle without breaking existing promoted files
* extending params or metrics when comparability rules are updated with them
* strengthening verification or recovery evidence

---

## Risky Kinds Of Change

These changes need stronger review:

* changing the meaning of an existing promoted artifact
* adding parameters that silently invalidate historical comparisons
* moving recovery guarantees from the remote to local cache assumptions
* changing stage behavior without making the new dependency surface legible in `dvc.yaml`

---

## Minimum Proof After A Change

After any meaningful capstone change, rerun:

1. `make PROGRAM=reproducible-research/deep-dive-dvc capstone-walkthrough`
2. `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify`
3. `make PROGRAM=reproducible-research/deep-dive-dvc capstone-recovery-drill`
4. `make PROGRAM=reproducible-research/deep-dive-dvc capstone-tour`

If any of those results become harder to explain, the repository likely got worse even if
it still runs.

---

## Best Companion Pages

Use these pages with this guide:

* [`capstone-file-guide.md`](capstone-file-guide.md)
* [`capstone-review-worksheet.md`](capstone-review-worksheet.md)
* [`proof-matrix.md`](../guides/proof-matrix.md)
* [`completion-rubric.md`](../reference/completion-rubric.md)
