<a id="top"></a>

# Completion Rubric


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Snakemake"]
  section["Completion Rubric"]
  page["Completion Rubric"]
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

Deep Dive Snakemake should finish with more than syntax familiarity.

Use this rubric to judge whether the learner can reason about workflow truth, dynamic
behavior, policy boundaries, and publish contracts without hand-waving.

---

## Completion Standard

You should be able to do all of the following:

* explain why a workflow reruns with evidence rather than intuition
* distinguish rule semantics from profile or executor policy
* describe what a checkpoint may discover and what it must never hide
* identify which outputs are internal versus safe for downstream trust
* explain which artifacts another reviewer should inspect before approving change

[Back to top](#top)

---

## Course Outcomes

| Area | Completion signal |
| --- | --- |
| file contracts | you can explain which paths are explicit contracts and why they matter |
| dynamic DAG behavior | you can describe the checkpoint boundary and its evidence surfaces clearly |
| operational policy | you can show which profile changes are safe and which would leak into semantics |
| publish boundaries | you can defend the public file API and the promoted evidence bundle |
| stewardship | you can review the workflow for drift, risk, and migration pressure |

[Back to top](#top)

---

## Capstone Evidence

Use these proof routes as the minimum capstone evidence:

1. `make -C capstone walkthrough`
2. `make -C capstone verify`
3. `make -C capstone verify-artifacts`
4. `make -C capstone confirm`

You are not done if you ran them mechanically but cannot explain what each one proved.

[Back to top](#top)

---

## Reviewer Questions

A reviewer should be able to ask:

* what this workflow claims to build
* what dynamic discovery is allowed to do here
* what is public for downstream trust
* what changed when moving between local and CI policy
* what would you inspect first before migration

If those answers stay vague, the learner is not done yet.

[Back to top](#top)
