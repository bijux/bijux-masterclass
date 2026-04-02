<a id="top"></a>

# Deep Dive DVC: Capstone Map


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive DVC"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Deep Dive DVC: Capstone Map"]
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

The capstone is the executable cross-check for this program, but it should not be the
first teaching surface for every concept. This page gives you one clear route through
the repository so you know when to enter it, what to inspect, and which command proves
the idea you are studying.

---

## Recommended Entry Rule

Use the capstone lightly in Modules 01-03, heavily in Modules 04-09, and as a review
specimen in Module 10.

If a concept still feels abstract, return to the smaller module exercise first. The
capstone should confirm understanding, not replace first-contact learning.

---

## Enter By Question Type

Use the question, not your anxiety level, to choose the route:

| Question type | Start here | Escalate only if needed |
| --- | --- | --- |
| what does this repository promise | `capstone-tour` | `capstone-verify` |
| does the current state still match the declared contract | `capstone-verify` | `capstone-verify-report` |
| how should I compare experiment candidates | `capstone-experiment-review` | `capstone-confirm` |
| what survives cache loss and remote restore | `capstone-recovery-review` | `capstone-confirm` |
| what is safe for downstream trust | `capstone-release-review` | `capstone-confirm` |

---

## Module-to-Capstone Route

| Module | Course page | Learner goal | Capstone surfaces | First capstone command |
| --- | --- | --- | --- | --- |
| 01 Why Reproducibility Fails | [Module 01](../module-01-reproducibility-failures-real-teams/index.md) | see why rerunnable scripts are weaker than explicit state contracts | `README.md`, `TOUR.md`, `data/raw/service_incidents.csv` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-tour` |
| 02 Data Identity and Content Addressing | [Module 02](../module-02-data-identity-content-addressing/index.md) | separate location from durable data identity | `data/raw/`, `.dvc/cache`, `.dvc-remote/`, `dvc.lock` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify` |
| 03 Execution Environments as Inputs | [Module 03](../module-03-execution-environments-reproducible-inputs/index.md) | inspect the runtime boundary instead of treating it as luck | `Makefile`, `pyproject.toml`, `src/incident_escalation_capstone/` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify` |
| 04 Pipelines as Truthful DAGs | [Module 04](../module-04-truthful-pipelines-declared-dependencies/index.md) | inspect declared stage edges and recorded execution state | `dvc.yaml`, `dvc.lock`, `state/data_profile.json` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-repro` |
| 05 Metrics, Parameters, and Meaning | [Module 05](../module-05-metrics-parameters-comparable-meaning/index.md) | inspect declared controls and semantic comparison surfaces | `params.yaml`, `metrics/metrics.json`, `publish/v1/metrics.json` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify-report` |
| 06 Experiments Without Chaos | [Module 06](../module-06-experiments-baselines-controlled-change/index.md) | vary the control surface without mutating the baseline contract | `params.yaml`, `metrics/`, `publish/v1/`, experiment comparison bundle | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-experiment-review` |
| 07 Collaboration, CI, and Social Contracts | [Module 07](../module-07-collaboration-ci-social-contracts/index.md) | inspect verification gates and reproducibility checks another person can run | `Makefile`, `tests/`, `TOUR.md` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify-report` |
| 08 Production, Scale, and Incident Survival | [Module 08](../module-08-recovery-scale-incident-survival/index.md) | rehearse cache loss and remote-backed restoration | `.dvc-remote/`, `publish/v1/`, recovery targets, recovery review bundle | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-recovery-review` |
| 09 Promotion, Registry Boundaries, Release Contracts, and Auditability | [Module 09](../module-09-promotion-registry-boundaries-auditability/index.md) | inspect the promoted interface and the evidence that defends it | `publish/v1/`, `publish/v1/manifest.json`, `publish/v1/params.yaml`, `dvc.lock`, release review bundle | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-release-review` |
| 10 Migration, Governance, Anti-Patterns, and DVC Tool Boundaries | [Module 10](../module-10-migration-governance-dvc-boundaries/index.md) | review the full repository as a long-lived stewardship specimen | `README.md`, `dvc.yaml`, `dvc.lock`, `Makefile`, `publish/v1/` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm` |

[Back to top](#top)

---

## First Capstone Tour

If you want one sane first walkthrough, use this order:

1. Run `make PROGRAM=reproducible-research/deep-dive-dvc capstone-tour` to generate the learner-first executed reading bundle.
2. Read `capstone/README.md` to understand the contract the repository is trying to keep.
3. Read `capstone/dvc.yaml` and then `capstone/dvc.lock` to compare declared versus recorded state.
4. Read `capstone/params.yaml` and `capstone/metrics/metrics.json` to see what comparisons are allowed to mean.
5. Read `capstone/publish/v1/` and `capstone/TOUR.md` to inspect the promoted contract and proof bundle.
6. Run `make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm` when you want the strongest executable proof instead of a prose tour.

This order keeps state identity and contract meaning ahead of mechanics.

[Back to top](#top)

---

## Keep These Pages Open Together

When you move from the course into the repository, keep these pages open as a set:

1. [Capstone Guide](readme-capstone.md)
2. [Capstone File Guide](capstone-file-guide.md)
3. [Repository Layer Guide](repository-layer-guide.md)
4. [Verification Route Guide](../reference/verification-route-guide.md)

That combination keeps the learner from confusing file ownership, repository layers, and
proof commands.

[Back to top](#top)

---

## Fast Routes by Goal

| Goal | Start here | Then inspect |
| --- | --- | --- |
| Why is this repository more than a data sync folder? | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-tour` | `README.md`, `dvc.yaml`, `dvc.lock` |
| What exactly is tracked as state? | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify` | `params.yaml`, `metrics/`, `publish/v1/` |
| How should I compare experiment candidates? | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-experiment-review` | `params.yaml`, `metrics.json`, `exp-show.txt` |
| How would I inspect the truthful pipeline? | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-repro` | `dvc.yaml`, `dvc.lock`, `state/` |
| Which outputs are safe for downstream trust? | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-release-review` | `publish/v1/manifest.json`, `publish/v1/report.md` |
| How does recovery survive local loss? | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-recovery-review` | `.dvc-remote/`, `publish/v1/`, `Makefile` |
| What would I review before migration? | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm` | `README.md`, `dvc.yaml`, `dvc.lock`, `Makefile` |

[Back to top](#top)

---

## Capstone Discipline

Use the capstone well:

* read the module first, then verify in the capstone
* prefer commands and files over vague summaries
* inspect one contract question at a time
* treat the proof bundle as review evidence, not decoration

If the repository starts to feel larger than the concept you are studying, step back to
the module and return once the smaller exercise has made the idea legible again.

[Back to top](#top)
