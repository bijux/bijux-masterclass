# Module Checkpoints

Use this page when you are about to move on and want an honest readiness bar. Reading a
module once is not the same as being ready for the next one. These checkpoints exist to
tell you whether the next module will build on stable understanding or on vague
recognition.

## If you are learning this without the live class

Use this page in four passes:

1. answer the checkpoint from memory before reopening the module
2. run or inspect one proportionate proof route
3. explain the result in your own words
4. stop immediately if the explanation still sounds memorized, vague, or borrowed from the course text

If you skip step 1, checkpoints turn into rereading with extra ceremony.

## What readiness means in this course

Readiness is stricter than familiarity.

You are ready when you can:

- explain the boundary in plain language
- inspect one proportionate proof route
- interpret the result without leaning on course wording
- say what misunderstanding would send you back

If one of those is missing, the next module will often feel harder for the wrong reason.

## The readiness packet you should keep for each module

For each module, keep one tiny packet:

- one boundary statement
- one proof route
- one interpretation in your own words
- one known misunderstanding that would send you back

If your packet cannot fit on a few lines, you probably still understand the surface less clearly than you think.

## How to use this page honestly

For each module:

1. answer the checkpoint from memory
2. run or inspect the listed proof route
3. explain the result in your own words
4. stop if the explanation still sounds memorized or vague

If you need to reread, reread the narrowest lesson that matches the gap instead of the
whole module.

## A checkpoint card you should be able to fill quickly

Use a table like this after each module:

| Part | Short honest answer |
| --- | --- |
| boundary | what this module taught me to separate or protect |
| proof route | the smallest route that tests that boundary |
| interpretation | what the route means when it passes or fails |
| go-back trigger | what confusion would send me back one lesson |

If one cell stays blank, that module is not ready to support the next one.

## Checkpoints by module

| Module | You are ready to move on when you can explain... | Quick proof or inspection route | Go back when... |
| --- | --- | --- | --- |
| [Module 01](../module-01-file-contracts-workflow-graph-truth/index.md) | why one target exists in the workflow plan and another does not | `snakemake -n` on the module example or [Capstone Walkthrough](../capstone/capstone-walkthrough.md) | Snakemake still feels like a command runner instead of a file-contract system |
| [Module 02](../module-02-dynamic-dags-discovery-integrity/index.md) | how discovery becomes a durable artifact instead of an ambient side effect | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | you can point to a checkpoint but not to the artifact that records what it discovered |
| [Module 03](../module-03-production-operations-policy-boundaries/index.md) | how declared resources become a scheduler request without changing workflow meaning | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-scheduler-policy-audit` | your explanation depends on one machine, one shell, or an unrecorded cluster command |
| [Module 04](../module-04-scaling-workflows-interface-boundaries/index.md) | where a scaling change belongs: rule file, module, file API, or validation surface | [Boundary Review Prompts](../reference/boundary-review-prompts.md) plus `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | you are splitting files by discomfort rather than by ownership |
| [Module 05](../module-05-software-boundaries-reproducible-rules/index.md) | where workflow orchestration ends and helper software begins | `make PROGRAM=reproducible-research/deep-dive-snakemake proof` | scripts, packages, and environments still feel like invisible implementation detail |
| [Module 06](../module-06-publishing-downstream-contracts/index.md) | what is public in `publish/v1/` and why it is smaller than internal run state | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report` | you are still treating `results/` as the downstream contract |
| [Module 07](../module-07-workflow-architecture-file-apis/index.md) | which file owns workflow entry, rule families, file APIs, and helper boundaries | [Capstone File Guide](../capstone/capstone-file-guide.md) | you can name folders but not explain their responsibilities |
| [Module 08](../module-08-operating-contexts-execution-policy/index.md) | which differences across local, CI, and scheduler policy preserve one semantic plan | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-context-invariance-audit` | you are treating context drift as harmless because the workflow still runs |
| [Module 09](../module-09-performance-observability-incident-response/index.md) | which work changed and which artifact and evidence contracts survived | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-performance-diagnostics-audit` | you accept one timing comparison or equal bytes as sufficient performance proof |
| [Module 10](../module-10-governance-migration-tool-boundaries/index.md) | how to improve or migrate the repository without losing proof and public trust | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm` | your migration plan is driven more by taste than by preserved evidence |

## Common false positives

Do not call a module done just because:

- the examples looked familiar
- you can repeat the vocabulary
- the strongest route passed once
- you can follow the capstone without saying why the evidence matters

Those usually mean you have seen the surface, not learned the boundary.

## What goes wrong when a learner treats familiarity as readiness

Use this card before you move on:

| If you are saying... | The likely hidden problem is... | Better honesty test |
| --- | --- | --- |
| "that module looked familiar" | recognition without explanation | answer the checkpoint from memory |
| "the strongest route passed" | maximal evidence is masking weak interpretation | pick one proportionate proof route and explain it |
| "I can follow the capstone" | repository navigation is replacing boundary understanding | state the module boundary in plain language |
| "I think I get it" | no go-back trigger has been named | write the misunderstanding that would send you back |

If the better honesty test feels narrower than your current proof, that is a feature, not a limitation.

## What honest use looks like

Suppose you think you are done with Module 06 because the publish lesson felt familiar.

Strong checkpoint use would be:

1. ask yourself what is public in `publish/v1/`
2. run the verification route
3. explain why `results/` is larger than the true trust surface
4. stop if your answer collapses back into "that is just where the files ended up"

That is the level of honesty these checkpoints are trying to force.

## A five-line readiness note you should be able to write from memory

If this page has done its job, you should be able to write after any module:

1. what boundary the module taught you to see
2. which proof route checks that boundary
3. what the proof means when it succeeds
4. what misunderstanding would send you back
5. why the next module would be premature if those stay vague

If you cannot do that, the module is not finished enough to support the next one.

## Companion pages

- [Module Promise Map](module-promise-map.md) when you need the module contract restated
- [Proof Ladder](proof-ladder.md) when the proof route feels heavier than the claim
- [Capstone Map](../capstone/capstone-map.md) when the concept is clear but the repository
  route is not
