# Command Guide

Use this page when the main problem is command choice rather than concept choice. Deep
Dive Snakemake has three command layers so readers can stay at the smallest durable
surface instead of guessing where a target belongs.

Deep Dive Snakemake has three command layers: repository root, program directory, and
capstone directory. The layers exist so you do not have to guess where a command
belongs.

## How to use this page

Use this guide only after you know what job you are trying to do.

Read it in this order:

1. name the job
2. choose the smallest command layer that still answers it
3. run one command
4. inspect the matching evidence before escalating

If you are still choosing commands by which one sounds strongest, this page should slow
you down.

## Choose the layer before the command

```mermaid
flowchart TD
  need["Name the job"] --> layer["Pick the smallest command layer"]
  layer --> command["Run one command"]
  command --> evidence["Inspect the matching evidence"]
  evidence --> escalate{"Need stronger proof?"}
  escalate -- no --> stop["Stop"]
  escalate -- yes --> stronger["Escalate one step"]
  stronger --> command
```

## Start by treating command layers as teaching boundaries

The three command layers are not just convenience aliases.

They exist so learners can stay on the smallest honest surface:

- repository root when you need stable cross-program entry
- program directory when you need one-course focus
- capstone directory when you are already reading the workflow as a raw repository

Dropping to the capstone too early often makes the learning route larger than necessary.

## Choose the command layer

| If you need... | Use this layer | Why |
| --- | --- | --- |
| one stable entrypoint from the repository root | repository root | consistent commands across all programs |
| course-local commands while staying inside the program | `programs/reproducible-research/deep-dive-snakemake/` | a smaller surface than the repo root |
| the raw executable workflow repository | `capstone/` | direct access to the workflow itself |

## A simple rule

Prefer the highest layer that still answers the current question honestly:

- use repository root for cross-program consistency
- use the program directory when you want one-course focus
- use the capstone directory when you are already reading the workflow as a repository

Do not drop to the raw capstone just because it feels more "real." Smaller command
surfaces are often better for learning and review.

## One honest command decision

Suppose your real job is:

> I need one executed workflow story with saved evidence.

The honest command is `capstone-tour` from the highest layer that still feels natural for
your context.

It is not `proof`, because that command answers a broader stewardship question than the
job you just named.

## Start by job, not by directory

| If the job is... | Start here | Do not start with |
| --- | --- | --- |
| first-pass capstone reading | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm` |
| executed workflow review | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `make PROGRAM=reproducible-research/deep-dive-snakemake proof` |
| publish-boundary verification | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report` | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm` |
| execution-policy comparison | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-profile-audit` | random `make PROGRAM=reproducible-research/deep-dive-snakemake ...` exploration |
| strongest final confirmation | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm` | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` |

## Common good choices

| Situation | Good first command | Why |
| --- | --- | --- |
| You need a bounded first read. | `capstone-walkthrough` | it keeps repository orientation smaller than execution proof |
| You want one executed workflow story. | `capstone-tour` | it gives real evidence without jumping to the strongest route |
| You care about downstream trust. | `capstone-verify-report` | publish review is narrower than whole-repository confirmation |
| You suspect local and CI are diverging. | `capstone-profile-audit` | context drift should start at the policy surface |

## Repository root

Use root-level commands when you want one entrypoint that works across programs.

- `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough`
- `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour`
- `make PROGRAM=reproducible-research/deep-dive-snakemake proof`
- `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report`
- `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm`

## Program directory

Use `programs/reproducible-research/deep-dive-snakemake/` when you want the course-local
surface.

- `make capstone-walkthrough`
- `make capstone-tour`
- `make proof`
- `make capstone-profile-audit`
- `make capstone-confirm`

## Capstone directory

Use `capstone/` when you want the raw reference workflow.

- `make walkthrough`
- `make verify`
- `make tour`
- `make verify-report`
- `make profile-audit`
- `make confirm`

## Good stopping point

Stop when you can explain why the chosen command layer is proportionate to the current
question. If the layer still feels too large, step down one layer before opening more
targets.
