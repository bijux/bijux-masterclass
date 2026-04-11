# Python Object-Oriented Programming Capstone Guide

The capstone is a monitoring-policy system for a team that needs to register rules,
activate them deliberately, evaluate incoming metric samples, emit incidents, and keep
downstream read models in sync without turning the domain model into procedural glue.

Use this guide to keep the capstone question-first. The repeated study goal is simple:
if this behavior changed tomorrow, which object or boundary should absorb that change,
and why?

## What this capstone proves

- value objects can keep domain facts explicit and stable
- an aggregate can own lifecycle transitions and incident decisions directly
- strategies can carry evaluation variability without bloating the aggregate
- events and projections can keep derived views downstream of authoritative state
- runtime orchestration can stay outside the domain while still coordinating real work

## Choose the right capstone route

| If your question is... | Best page |
| --- | --- |
| Which capstone surface matches the current module? | [Capstone Map](capstone-map.md) |
| Which files should I read first? | [Capstone File Guide](capstone-file-guide.md) |
| Where do ownership boundaries and packages live? | [Capstone Architecture Guide](capstone-architecture-guide.md) |
| Which proof route is honest for this claim? | [Capstone Proof Guide](capstone-proof-guide.md) |
| How should I review the design as a steward? | [Capstone Review Worksheet](capstone-review-worksheet.md) |
| Where should a new change land? | [Capstone Extension Guide](capstone-extension-guide.md) |

## Start by module range

| Module range | Best capstone focus |
| --- | --- |
| Modules 01-03 | value semantics, lifecycle rules, and aggregate state transitions |
| Modules 04-07 | policies, events, repositories, runtime coordination, and boundary ownership |
| Modules 08-10 | tests, bundles, public routes, and extension seams |

## Core commands

| If you need... | From the repository root | From the capstone directory |
| --- | --- | --- |
| the learner-facing walkthrough | `make PROGRAM=python-programming/python-object-oriented-programming capstone-walkthrough` | `make walkthrough` |
| executable verification | `make PROGRAM=python-programming/python-object-oriented-programming test` | `make confirm` |
| saved proof bundles | `make PROGRAM=python-programming/python-object-oriented-programming proof` | `make proof` |

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

- Which object owns each invariant?
- Which objects are authoritative, and which are only derived views?
- Where would a new rule mode, sink, or projection belong without weakening ownership?

## Stop here when

- you know which object or boundary the current chapter is really about
- you know which file or bundle makes that ownership visible
- you know the smallest command that proves it
