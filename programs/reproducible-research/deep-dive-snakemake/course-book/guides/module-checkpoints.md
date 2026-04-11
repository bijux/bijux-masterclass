<a id="top"></a>

# Module Checkpoints


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive Snakemake"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Module Checkpoints"]
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

This page is the missing study contract at the end of each module. It gives a human bar
for readiness instead of assuming that reading the prose once means the concept is
stable.

Use it when you are about to move on and want to know whether you are ready, what you are
still fuzzy on, and which proof route should settle the question.

---

## How To Use The Checkpoints

For each module:

1. read the module overview and main lessons
2. answer the checkpoint questions without looking at the text
3. run the smallest honest proof route
4. only advance when the concept feels explainable, not merely recognizable

[Back to top](#top)

---

## Checkpoint Table

| Module | You are ready when you can explain | You should be able to do | Useful proof route |
| --- | --- | --- | --- |
| 01 | why rules and targets form a file-driven DAG | explain a dry-run without hand-waving | `capstone-walkthrough` |
| 02 | why dynamic discovery needs one durable discovered-set artifact and one honest publish trail | describe what discovery is allowed to change and what must stay stable | `make verify` |
| 03 | why profiles, failure handling, and proof routes are policy surfaces rather than workflow meaning | distinguish execution context from workflow semantics and choose the right production proof route | `capstone-profile-audit` |
| 04 | how repository growth stays legible through named boundaries and review gates | name which file or interface boundary should absorb one scaling change | `capstone-tour` |
| 05 | why software ownership, runtime contracts, and provenance must stay reviewable together | explain where rule logic ends, where software begins, and what evidence supports a rebuild | `proof` |
| 06 | what makes a versioned publish bundle trustworthy downstream | explain which files are public, which changes are compatible, and what evidence defends the bundle | `capstone-verify-report` |
| 07 | how repository architecture protects workflow meaning | review ownership without guessing where the contract lives | `proof` |
| 08 | what may change across local, CI, and cluster contexts | explain which differences are policy and which would be semantic drift | `capstone-profile-audit` |
| 09 | how to move from workflow symptom to evidence-backed diagnosis | choose the right observability or incident surface first | `proof` |
| 10 | when Snakemake should stop owning a concern | review a workflow as a long-lived product with migration judgment | `capstone-confirm` |

[Back to top](#top)

---

## Failure Signals

Do not advance yet if any of these are still true:

* you recognize the term but cannot explain the invariant it protects
* you know the strongest proof command but not the smallest honest one
* you can follow the capstone mechanically but cannot name the owning boundary
* you can repeat the repair pattern but cannot say what failure it prevents

These are not small study gaps. They are signals that the next module will feel more
arbitrary than it should.

[Back to top](#top)

---

## Best Companion Pages

Use these with the checkpoints:

* [`module-promise-map.md`](module-promise-map.md) to see what each title promised
* [`proof-ladder.md`](proof-ladder.md) to keep proof proportional to the question
* [`practice-map.md`](../reference/practice-map.md) to match module work with proof loops
* [`capstone-review-worksheet.md`](../capstone/capstone-review-worksheet.md) when you want to record what the evidence actually showed

[Back to top](#top)
