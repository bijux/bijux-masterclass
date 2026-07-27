# Module Checkpoints


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Guides"]
  page["Module Checkpoints"]
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

Use this page when you are about to move on and want an honest readiness bar. Reading a
module once is not the same thing as being ready for the next one. These checkpoints are
meant to tell you whether the next module will build on stable understanding or on vague
recognition.

## How to use this page

For each module:

1. answer the checkpoint question without looking at the text
2. run the listed proof or inspection route
3. stop if you still cannot explain the result in plain language

If you need to reread, reread the narrowest lesson that matches the gap instead of the
whole module.

## Readiness table

| Module | You are ready to move on when you can explain... | Quick proof or inspection route | Go back when... |
| --- | --- | --- | --- |
| [Module 01](../module-01-reproducibility-failures-real-teams/index.md) | why rerunning commands is weaker than explicit state contracts | [Capstone Guide](../capstone/index.md) or `make PROGRAM=reproducible-research/deep-dive-dvc capstone-tour` | you are still treating "it runs again" as the whole reproducibility story |
| [Module 02](../module-02-data-identity-content-addressing/index.md) | why paths locate content while pointers identify it, and why identity can survive after recoverability is lost | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-data-identity-audit` | you cannot identify which layer supplied restored bytes or explain the pointer-only failure |
| [Module 03](../module-03-execution-environments-reproducible-inputs/index.md) | why declared runtime drift triggers a rebuild while hidden process state can preserve stale meaning | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-runtime-contract-audit` | you treat empty status or forced execution as proof that the runtime contract is complete |
| [Module 04](../module-04-truthful-pipelines-declared-dependencies/index.md) | why declared file and parameter changes become stale while hidden influences and undeclared output loss remain invisible | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-stage-contract-audit` | you cannot connect each status receipt to the semantic value or missing artifact it leaves behind |
| [Module 05](../module-05-metrics-parameters-comparable-meaning/index.md) | why the same numeric movement can be accepted or rejected when population, controls, schema, units, or evidence change | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-metric-contract-audit` | you treat arithmetic, matching keys, or row counts as proof that two metric claims are comparable |
| [Module 06](../module-06-experiments-baselines-controlled-change/index.md) | how to vary runs without muddying baseline truth | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-experiment-review` | you can compare runs mechanically but cannot defend their comparability |
| [Module 07](../module-07-collaboration-ci-social-contracts/index.md) | why discovery, object availability, Git completeness, recorded execution, review authority, and result meaning must all survive a cache-cold handoff | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-reviewer-handoff-audit` | you treat successful pull or reproduction as proof that the submitted handoff was complete and reviewable |
| [Module 08](../module-08-recovery-scale-incident-survival/index.md) | what survives local loss and what only looked durable | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-recovery-review` | you still blur local convenience with remote-backed recovery guarantees |
| [Module 09](../module-09-promotion-registry-boundaries-auditability/index.md) | what is safe for downstream trust and why it is smaller than the whole repository | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-release-review` | the promoted bundle still feels like a raw dump of internal state |
| [Module 10](../module-10-migration-governance-dvc-boundaries/index.md) | how to improve or migrate the repository without losing proof and trust | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm` | your migration plan is mostly taste instead of preserved evidence |

## Common false positives

Do not call a module done just because:

- the commands looked familiar
- you can repeat the vocabulary
- the strongest route passed once
- you can follow the capstone without naming why the evidence matters

Those usually mean you have seen the surface, not learned the boundary.

## Best companion pages

- [Module Promise Map](module-promise-map.md) when you need the module contract restated
- [Proof Ladder](proof-ladder.md) when the proof route feels heavier than the claim
- [Capstone Map](../capstone/capstone-map.md) when the concept is clear but the repository route is not
