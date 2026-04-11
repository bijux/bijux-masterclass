# Proof Matrix


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Snakemake"]
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

This page maps the course's main claims to the commands and files that prove them.

Use it when you care about a concept but want the fastest evidence route.

---

## Core Workflow Claims

| Claim | Command | File surfaces |
| --- | --- | --- |
| the capstone has a bounded first-pass reading route | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `course-book/capstone/index.md`, `artifacts/walkthrough/reproducible-research/deep-dive-snakemake/` |
| the workflow exposes its public rule surface clearly | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `capstone/Snakefile`, `artifacts/walkthrough/reproducible-research/deep-dive-snakemake/list-rules.txt` |
| dynamic discovery becomes explicit evidence instead of a hidden side effect | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `capstone/results/discovered_samples.json`, `capstone/publish/v1/discovered_samples.json` |
| profiles change execution policy without changing workflow meaning | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-profile-audit` | `capstone/profiles/`, `capstone/Makefile` |
| promoted outputs are smaller than the full internal repository state | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | [`capstone-review-worksheet.md`](../capstone/capstone-review-worksheet.md), `capstone/publish/v1/`, `capstone/results/` |

---

## Operational Claims

| Claim | Command | File surfaces |
| --- | --- | --- |
| the workflow validates configuration before execution | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-validate-config` | `capstone/config/config.yaml`, `capstone/config/schema.yaml` |
| the workflow can explain its plan before a run | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `artifacts/walkthrough/reproducible-research/deep-dive-snakemake/dryrun.txt`, `capstone/workflow/rules/` |
| the publish bundle can defend itself after execution | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-artifacts` | `capstone/publish/v1/manifest.json`, `capstone/publish/v1/provenance.json` |
| the publish boundary is reviewable as a durable contract | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report` | [`capstone-review-worksheet.md`](../capstone/capstone-review-worksheet.md), `artifacts/proof/reproducible-research/deep-dive-snakemake/verify/` |
| the repository can prove itself through one stronger end-to-end route | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm` | `capstone/Makefile`, `capstone/tests/` |
| workflow incidents can be reviewed with narrower evidence than a full rewrite | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-selftest` or `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `capstone/tests/selftest.sh`, `capstone/logs/`, `artifacts/tour/reproducible-research/deep-dive-snakemake/` |
| the executed workflow tour is reviewable as evidence | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `artifacts/tour/reproducible-research/deep-dive-snakemake/`, [`capstone-proof-guide.md`](../capstone/capstone-proof-guide.md) |

---

## Review Questions

| Question | Best first command | Best first file |
| --- | --- | --- |
| where should a first-time reader start in the capstone | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `course-book/capstone/index.md` |
| what does this workflow claim it will build | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-wf-dryrun` | `capstone/Snakefile` |
| what exactly is public for downstream trust | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-artifacts` | [`capstone-review-worksheet.md`](../capstone/capstone-review-worksheet.md) |
| which surface explains dynamic discovery honestly | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `capstone/workflow/rules/preprocess.smk` |
| what would I inspect before migration | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm` | `course-book/capstone/index.md` |

---

## Companion Pages

The most useful companion pages for this matrix are:

* [`capstone/command-guide.md`](../capstone/command-guide.md)
* [`topic-boundaries.md`](../reference/topic-boundaries.md)
* [`practice-map.md`](../reference/practice-map.md)
* [`capstone-file-guide.md`](../capstone/capstone-file-guide.md)
* [`capstone-review-worksheet.md`](../capstone/capstone-review-worksheet.md)
* [`capstone-proof-guide.md`](../capstone/capstone-proof-guide.md)
