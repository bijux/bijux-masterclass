# Module Checkpoints

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
| [Module 02](../module-02-data-identity-content-addressing/index.md) | what makes state durable instead of path-shaped | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify` | you cannot distinguish workspace files, cache objects, remote-backed state, and lockfile records |
| [Module 03](../module-03-execution-environments-reproducible-inputs/index.md) | why execution environment belongs in the state model | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify` | your explanation of reproducibility still ignores toolchain and runtime context |
| [Module 04](../module-04-truthful-pipelines-declared-dependencies/index.md) | how `dvc.yaml` and `dvc.lock` tell different but compatible stories | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-repro` | you can read a stage but cannot say whether its edge is truly declared |
| [Module 05](../module-05-metrics-parameters-comparable-meaning/index.md) | which params and metrics are safe to compare and why | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify` | you treat any changed metric as meaningful without checking the declared control surface |
| [Module 06](../module-06-experiments-baselines-controlled-change/index.md) | how to vary runs without muddying baseline truth | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-experiment-review` | you can compare runs mechanically but cannot defend their comparability |
| [Module 07](../module-07-collaboration-ci-social-contracts/index.md) | what another maintainer should be able to rerun and review without oral context | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify` or `capstone-confirm` | your review story still depends on author memory |
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

