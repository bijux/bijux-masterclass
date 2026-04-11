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
| what is safe for downstream trust | [Capstone Review Worksheet](capstone-review-worksheet.md) | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report` |
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

## Shelf vocabulary

Use this section when the route pages start sounding interchangeable. The capstone shelf
is not a second course book. It is a bounded set of entry routes into one executable
repository, and the terms here keep those routes distinct.

### Route terms

| Term | Meaning here | Why it matters |
| --- | --- | --- |
| walkthrough | the bounded first pass through the repository | keeps first contact human-scale |
| proof route | the smallest executed or saved route that can honestly test a workflow claim | keeps evidence proportional to the question |
| publish boundary | the downstream-facing output surface another person is allowed to trust | separates public deliverables from internal run state |
| profile audit | the route that compares local, CI, and scheduler policy surfaces | keeps execution policy from masquerading as workflow meaning |
| stewardship review | the stronger route used when another maintainer needs to judge the whole repository | prevents first-pass reading from escalating into full review too early |
| capstone entry | one bounded way into the executable repository | prevents directory tourism |
| public file surface | the smaller set of files another reader should inspect first | keeps the repository reviewable under pressure |
| saved evidence bundle | an exported artifact set that lets a reviewer inspect the workflow later | keeps trust tied to durable evidence instead of terminal scrollback |

### Page names in plain language

| Page | What it helps you do |
| --- | --- |
| [Capstone Walkthrough](capstone-walkthrough.md) | take a bounded first pass through the repository |
| [Command Guide](command-guide.md) | choose the right command layer and first command |
| [Capstone File Guide](capstone-file-guide.md) | know which repository files matter first and why |
| [Capstone Proof Guide](capstone-proof-guide.md) | choose the shortest honest proof route |
| [Capstone Review Worksheet](capstone-review-worksheet.md) | review the downstream trust surface and stewardship route |
| [Profile Audit Guide](profile-audit-guide.md) | review local, CI, and scheduler policy drift |
| [Capstone Review Worksheet](capstone-review-worksheet.md) | review the repository as a steward, not only as a learner |
| [Capstone Extension Guide](capstone-extension-guide.md) | evolve the repository without weakening its teaching or review value |
| [Capstone Review Worksheet](capstone-review-worksheet.md) | narrow a failure review to the evidence that matters |

## Reading rule

If two capstone pages sound interchangeable, do not open both. Name the current job:
entry, command choice, file surface, publish review, policy review, or stewardship. Then
open the one page that owns that job.
