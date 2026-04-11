<a id="top"></a>

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

[Back to top](#top)

## Readiness table

| Module | You are ready to move on when you can explain... | Quick proof or inspection route | Go back when... |
| --- | --- | --- | --- |
| [Module 01](../module-01-file-contracts-workflow-graph-truth/index.md) | why one target exists in the workflow plan and another does not | `snakemake -n` on the module example or [Capstone Walkthrough](../capstone/capstone-walkthrough.md) | Snakemake still feels like a command runner instead of a file-contract system |
| [Module 02](../module-02-dynamic-dags-discovery-integrity/index.md) | how discovery becomes a durable artifact instead of an ambient side effect | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | you can point to a checkpoint but not to the artifact that records what it discovered |
| [Module 03](../module-03-production-operations-policy-boundaries/index.md) | what belongs in a profile and what would change workflow meaning | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-profile-audit` | your explanation depends on one machine or one shell command |
| [Module 04](../module-04-scaling-workflows-interface-boundaries/index.md) | where a scaling change belongs: rule file, module, file API, or validation surface | [Boundary Map](../reference/boundary-map.md) plus `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | you are splitting files by discomfort rather than by ownership |
| [Module 05](../module-05-software-boundaries-reproducible-rules/index.md) | where workflow orchestration ends and helper software begins | `make PROGRAM=reproducible-research/deep-dive-snakemake proof` | you still treat scripts, packages, and environments as invisible implementation detail |
| [Module 06](../module-06-publishing-downstream-contracts/index.md) | what is public in `publish/v1/` and why it is smaller than the internal run state | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report` | you are still treating `results/` as the downstream contract |
| [Module 07](../module-07-workflow-architecture-file-apis/index.md) | which file owns workflow entry, rule families, file APIs, and helper code boundaries | [Capstone File Guide](../capstone/capstone-file-guide.md) | you can name folders but not explain their responsibilities |
| [Module 08](../module-08-operating-contexts-execution-policy/index.md) | which differences across local, CI, and SLURM are policy and which would be semantic drift | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-profile-audit` | you are treating context drift as harmless because the workflow still runs |
| [Module 09](../module-09-performance-observability-incident-response/index.md) | which evidence surface you would inspect before editing a slow or flaky workflow | [Incident Review Guide](../capstone/incident-review-guide.md) or `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | your first move is to change retries, threads, or grouping |
| [Module 10](../module-10-governance-migration-tool-boundaries/index.md) | how to improve or migrate the repository without losing proof and public trust | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm` | your migration plan is mostly taste, not preserved evidence |

[Back to top](#top)

## Common false positives

Do not call a module done just because:

- the examples looked familiar
- you can repeat the vocabulary
- the strongest route passed once
- you can follow the capstone without naming why the evidence matters

Those usually mean you have seen the surface, not learned the boundary.

[Back to top](#top)

## Best companion pages

- [Module Promise Map](module-promise-map.md) when you need the module contract restated
- [Proof Ladder](proof-ladder.md) when the proof route feels heavier than the claim
- [Capstone Map](../capstone/capstone-map.md) when the concept is clear but the repository route is not

[Back to top](#top)
