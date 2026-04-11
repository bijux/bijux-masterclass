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
| which files and state surfaces matter first | [Capstone File Guide](capstone-file-guide.md) | [Repository Layer Guide](repository-layer-guide.md) |
| what counts as current repository truth | [Command Guide](command-guide.md) | `make PROGRAM=reproducible-research/deep-dive-dvc capstone-verify` |
| what survives local loss and remote restore | [Recovery Review Guide](recovery-review-guide.md) | [Capstone Review Worksheet](capstone-review-worksheet.md) |
| what is safe for downstream trust | [Release Audit Checklist](release-audit-checklist.md) | [Release Review Guide](release-review-guide.md) |
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

## Directory glossary

Use [Glossary](glossary.md) when the route pages start sounding interchangeable and you
need the shelf language kept stable.
