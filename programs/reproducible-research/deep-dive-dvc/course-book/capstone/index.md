# DVC Capstone Guide

This capstone is the executable reference repository for Deep Dive DVC. It is where the
course’s largest claims become inspectable:

- state identity is explicit instead of path-shaped
- declared pipeline contracts and recorded execution state can be compared directly
- promoted outputs are smaller and clearer than the whole repository
- recovery is tested against a remote-backed durability story instead of assumption

It is not the right place for first exposure to a concept. It is the right place for
corroboration once the local idea is already clear.

## Use this capstone when

- the module idea is already legible and you want executable corroboration
- you need one repository that keeps state authority, promotion, and recovery visible together
- you are reviewing whether a small DVC project behaves like a serious long-lived repository

## Do not use this capstone when

- you still need the first explanation of the concept itself
- you want to browse the whole repository before naming the trust question
- the strongest route feels safer than choosing a smaller proof surface

## Choose the entry route by question

| If the question is... | Start here | Escalate only if needed |
| --- | --- | --- |
| what this repository promises | [Capstone Map](capstone-map.md) | [Command Guide](command-guide.md) |
| which files and state surfaces matter first | [Capstone File Guide](capstone-file-guide.md) | [Command Guide](command-guide.md) |
| what counts as current repository truth | [Command Guide](command-guide.md) | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify` |
| what survives local loss and remote restore | [Recovery Review Guide](recovery-review-guide.md) | [Capstone Review Worksheet](capstone-review-worksheet.md) |
| what is safe for downstream trust | [Release Review Guide](release-review-guide.md) | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-release-review` |
| how should I review the repository as a steward | [Capstone Review Worksheet](capstone-review-worksheet.md) | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm` |

## First honest pass

1. Run `make PROGRAM=reproducible-research/deep-dive-dvc capstone-walkthrough`.
2. Read [Capstone File Guide](capstone-file-guide.md).
3. Read `dvc.yaml`, `dvc.lock`, and `params.yaml` in that order.
4. Read one route page that matches your question: experiment, recovery, or release.
5. Stop before widening into stronger proof routes.

That is enough to see the repository contract, the declared and recorded state story, and
the promoted boundary without turning the capstone into directory tourism.

## Core commands

From repository root:

```sh
make PROGRAM=reproducible-research/deep-dive-dvc capstone-walkthrough
make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify
make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify-report
make PROGRAM=reproducible-research/deep-dive-dvc capstone-experiment-review
make PROGRAM=reproducible-research/deep-dive-dvc capstone-recovery-review
make PROGRAM=reproducible-research/deep-dive-dvc capstone-release-review
make PROGRAM=reproducible-research/deep-dive-dvc capstone-confirm
```

Those commands cover first pass, current-state verification, saved evidence, experiment
comparison, recovery review, release review, and the strongest confirmation path.

## What to keep asking while you read

- which layer is authoritative for this question
- which file records the difference between declaration and execution
- which promoted files another person is allowed to trust downstream
- which guarantees depend on the DVC remote rather than local convenience

## Shelf vocabulary

Use this section when the capstone route pages start to blur together. The capstone
shelf is not a second course book. It is a small set of routes into one executable DVC
repository, and the terms here keep those routes distinct.

### Route terms

| Term | Meaning here | Why it matters |
| --- | --- | --- |
| walkthrough | the bounded first pass through the repository without executing proof routes | keeps first contact human-scale |
| verify | the ordinary executable check that current repository state still matches the contract | separates current-state truth from broader stewardship review |
| verify report | the saved verification bundle for later inspection | helps you review promotion and enforcement without rerunning live |
| experiment review | the focused comparison route for changed runs against the baseline | keeps experiment discussion from mutating the baseline story |
| recovery review | the bundle that shows what survives local loss and remote restore | keeps durability claims distinct from release claims |
| release review | the bundle that audits what downstream users may trust | keeps promoted state distinct from internal repository state |
| confirm | the strongest overall repository confirmation pass | for final confidence after narrower routes already make sense |
| authoritative layer | the file or state surface that should win when surfaces disagree | keeps review attached to state ownership |
| promoted contract | the smaller downstream-facing bundle that another consumer is allowed to trust | prevents the whole repository from masquerading as a release |

### Page names in plain language

| Page | What it helps you do |
| --- | --- |
| [DVC Capstone Guide](index.md) | enter the repository with the right expectations |
| [Capstone Map](capstone-map.md) | choose the right route by module or question |
| [Command Guide](command-guide.md) | pick the right command layer and first command |
| [Capstone File Guide](capstone-file-guide.md) | know which repository files to open first and why |
| [Experiment Review Guide](experiment-review-guide.md) | compare changed runs without muddying the baseline story |
| [Recovery Review Guide](recovery-review-guide.md) | review restore guarantees and what they depend on |
| [Release Review Guide](release-review-guide.md) | make one downstream-trust judgment |
| [Capstone Review Worksheet](capstone-review-worksheet.md) | review the repository as a steward, not just a reader |

## Reading rule

If two pages sound interchangeable, do not open both. Name the job first: entry,
command choice, state authority, file ownership, experiment review, recovery review,
release review, or stewardship. Then open the one page that owns that job.
