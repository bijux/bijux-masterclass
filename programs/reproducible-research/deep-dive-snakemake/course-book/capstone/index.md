# Capstone Guide

This capstone is the executable reference workflow for Deep Dive Snakemake. It is where
the course’s largest claims become runnable and reviewable:

- rules act as explicit file contracts
- dynamic discovery leaves durable evidence instead of ambient side effects
- profiles change operating policy without redefining workflow meaning
- published outputs are smaller and clearer than the internal run state

It is not the right place for first exposure to a concept. It is the right place for
corroboration once the local idea is already clear.

## Use this capstone when

- the module idea is already legible and you want executable corroboration
- you need one repository that keeps workflow truth, publish trust, and policy surfaces visible together
- you are reviewing whether a small workflow behaves like a serious one under pressure

## Do not use this capstone when

- you still need the first explanation of the concept itself
- you want to browse the whole repository before naming the question
- the strongest route feels safer than choosing a smaller proof surface

## Choose the entry route by question

| If the question is... | Start here | Escalate only if needed |
| --- | --- | --- |
| what does this repository promise | [Capstone Walkthrough](capstone-walkthrough.md) | [Capstone File Guide](capstone-file-guide.md) |
| which files and commands are publicly important | [Command Guide](command-guide.md) | [Capstone Proof Guide](capstone-proof-guide.md) |
| what is safe for downstream trust | [Publish Review Guide](publish-review-guide.md) | [Capstone Review Worksheet](capstone-review-worksheet.md) |
| what differs across local, CI, and scheduler policy | [Profile Audit Guide](profile-audit-guide.md) | [Capstone Review Worksheet](capstone-review-worksheet.md) |
| how should I review the repository as a steward | [Capstone Review Worksheet](capstone-review-worksheet.md) | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm` |

## First honest pass

1. Run `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough`.
2. Read [Capstone Walkthrough](capstone-walkthrough.md).
3. Read [Capstone File Guide](capstone-file-guide.md).
4. Read the copied `Snakefile`, key rule files, and `FILE_API.md`.
5. Stop before widening into stronger proof routes.

That is enough to see the repository contract, the visible workflow shape, and the public
publish boundary without turning the capstone into directory tourism.

## Core commands

From repository root:

```sh
make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough
make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour
make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report
make PROGRAM=reproducible-research/deep-dive-snakemake capstone-profile-audit
make PROGRAM=reproducible-research/deep-dive-snakemake capstone-confirm
```

Those commands cover first pass, executed review, publish trust, policy review, and the
strongest confirmation path.

## What to keep asking while you read

- which files are public contracts and which are internal coordination state
- where discovery becomes a durable artifact instead of runtime folklore
- which settings belong to policy rather than workflow meaning
- which saved evidence would matter most to another maintainer

## Directory glossary

Use [Glossary](glossary.md) when the route pages start sounding interchangeable and you
need the shelf language kept stable.
