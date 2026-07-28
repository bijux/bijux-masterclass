# Capstone Proof Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
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

Use this page when the question has moved from orientation to evidence. The goal is to
choose the smallest honest DVC proof route instead of escalating every question to full
repository confirmation.

## Choose the proof route by claim

| If you need to prove... | Start here | Escalate only if needed |
| --- | --- | --- |
| equal local reruns support team reproducibility only when identities, controls, runtime, clean reconstruction, and recovery also pass | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-workflow-evidence-audit` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-workflow-evidence-selftest` |
| current repository state still matches the declared contract | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify-report` |
| pointers identify bytes and storage layers can recover them after loss | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-data-identity-audit` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-data-identity-selftest` |
| stage declarations detect every real file, parameter, and output boundary | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-stage-contract-audit` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-stage-contract-selftest` |
| runtime changes are either declared or exposed as hidden influences | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-runtime-contract-audit` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-runtime-contract-selftest` |
| metric movement preserves population, controls, schema, unit, and evidence needed for comparison | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-metric-contract-audit` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-metric-contract-selftest` |
| a cache-cold reviewer can recover and explain the submitted state without private context | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-reviewer-handoff-audit` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-reviewer-handoff-selftest` |
| a changed run preserves baseline, intent, control, population, and metric boundaries before promotion | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-experiment-comparability-audit` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-experiment-comparability-selftest` |
| recovery survives local loss because remote-backed state still exists | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-recovery-review` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm` |
| candidate storage restores every protected current and historical revision before authority cutover | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-recovery-readiness-audit` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-recovery-readiness-selftest` |
| a candidate earns promotion only when immutable identity, exact inventory, integrity, claims, provenance, approval, and consumer scope agree | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-promotion-integrity-audit` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-promotion-integrity-selftest` |
| the publish boundary is safe for downstream trust | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-release-review` | [Capstone Review Worksheet](capstone-review-worksheet.md) |
| the whole repository still deserves trust as a stewarded specimen | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm` | none |

## Read evidence in this order

1. command output or saved bundle
2. `capstone/dvc.lock`
3. `capstone/publish/v1/`
4. the matching implementation file only if the boundary still feels unclear

## What a strong proof review can answer

- which layer is authoritative for the current claim
- whether the proof is about ordinary verification, recovery durability, or downstream trust
- which next change would require a stronger route than the one you just used
