# Command Guide

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Capstone"]
  page["Command Guide"]
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

Read the first diagram as a timing map: this page is for command choice, not for reading
the whole capstone. Read the second diagram as the rule: choose the command layer that
matches the current job, run the smallest honest command, then escalate only if the
question changes.

Deep Dive DVC has three command layers: repository root, program directory, and capstone
directory. The layers exist so you do not have to guess where a command belongs.

## Choose the command layer

| If you need... | Use this layer | Why |
| --- | --- | --- |
| one stable entrypoint from the repository root | repository root | consistent commands across all programs |
| course-local commands while staying inside the program | `programs/reproducible-research/deep-dive-dvc/` | a smaller surface than the repo root |
| the raw executable reference repository | `capstone/` | direct access to the DVC project itself |

## Start by job, not by directory

| If the job is... | Start here | Do not start with |
| --- | --- | --- |
| first-pass capstone reading | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-walkthrough` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm` |
| current-state verification | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-tour` |
| experiment comparison | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-experiment-review` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm` |
| release-boundary review | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-release-review` | random `make PROGRAM=reproducible-research/deep-dive-dvc ...` exploration |
| strongest final confirmation | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm` | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-walkthrough` |

## Repository root

Use root-level commands when you want one entrypoint that works across programs.

- `make PROGRAM=reproducible-research/deep-dive-dvc capstone-walkthrough`
- `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify`
- `make PROGRAM=reproducible-research/deep-dive-dvc capstone-experiment-review`
- `make PROGRAM=reproducible-research/deep-dive-dvc capstone-release-review`
- `make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm`

## Program directory

Use `programs/reproducible-research/deep-dive-dvc/` when you want the course-local
surface.

- `make capstone-walkthrough`
- `make capstone-verify`
- `make capstone-experiment-review`
- `make capstone-release-review`
- `make capstone-confirm`

## Capstone directory

Use `capstone/` when you want the raw reference repository.

- `make walkthrough`
- `make verify`
- `make experiment-review`
- `make release-review`
- `make recovery-review`
- `make confirm`

## Good stopping point

Stop when you can explain why the chosen command layer is proportionate to the current
question. If the layer still feels too large, step down one layer before opening more
targets.
