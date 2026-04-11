# Deep Dive Snakemake Capstone Guide

This capstone is the executable reference workflow for Deep Dive Snakemake. It keeps rule
contracts, dynamic discovery, operating policy, and publish trust visible in one place so
the workflow can be reviewed as a real repository rather than as terminal folklore.

Use this guide once the local module idea is already clear. The capstone should
corroborate one workflow claim at a time, not become the first explanation of Snakemake.

## What this capstone proves

- rules can act as explicit file contracts
- dynamic discovery can leave durable evidence instead of ambient side effects
- profiles can change operating policy without redefining workflow meaning
- published outputs can stay smaller and clearer than internal run state

## Choose the right capstone route

| If your question is... | Best page |
| --- | --- |
| Which capstone surface matches the current module? | [Capstone Map](capstone-map.md) |
| Which files and commands are publicly important? | [Command Guide](command-guide.md) and [Capstone File Guide](capstone-file-guide.md) |
| Where do workflow, policy, and publish ownership live? | [Capstone Architecture Guide](capstone-architecture-guide.md) |
| Which proof route is honest for this claim? | [Capstone Proof Guide](capstone-proof-guide.md) |
| How should I review the repository as a steward? | [Capstone Review Worksheet](capstone-review-worksheet.md) |
| Where should a new change land? | [Capstone Extension Guide](capstone-extension-guide.md) |

## Start by module range

| Module range | Best capstone focus |
| --- | --- |
| Modules 01-02 | file contracts, dynamic discovery, and deterministic workflow shape |
| Modules 03-04 | policy surfaces, execution boundaries, and repository interfaces |
| Modules 05-08 | publish contracts, software boundaries, and operating-context drift |
| Modules 09-10 | incident evidence, migration pressure, and stewardship review |

## Core commands

| If you need... | From the repository root | From the capstone directory |
| --- | --- | --- |
| the first bounded pass | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough` | `make walkthrough` |
| executed workflow review | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour` | `make tour` |
| publish-trust review | `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-verify-report` | `make verify-report` |

## Guide set

- [Capstone Map](capstone-map.md)
- [Capstone Walkthrough](capstone-walkthrough.md)
- [Command Guide](command-guide.md)
- [Capstone File Guide](capstone-file-guide.md)
- [Capstone Architecture Guide](capstone-architecture-guide.md)
- [Capstone Proof Guide](capstone-proof-guide.md)
- [Capstone Review Worksheet](capstone-review-worksheet.md)
- [Capstone Extension Guide](capstone-extension-guide.md)
- [Glossary](glossary.md)

## Review questions

- Which files are public contracts and which are only internal coordination state?
- Where does discovery become a durable artifact instead of runtime folklore?
- Which settings belong to operating policy rather than workflow meaning?
- Which saved evidence bundle would matter most to another maintainer?

## Stop here when

- you know which boundary the current workflow question belongs to
- you know whether the next move is walkthrough, proof, or stewardship review
- you know the smallest command or bundle that can answer honestly
