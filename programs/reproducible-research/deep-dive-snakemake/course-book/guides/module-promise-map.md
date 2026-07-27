# Module Promise Map

Use this page when a module title sounds right but still too compressed. A strong module
title should tell you what kind of judgment you will leave with, not just which topic
bucket the chapter belongs to.

## How to use this page

Use this map before you start a module or when a module feels broader than its title.

Read it in this order:

1. identify the module you are entering
2. read the promise as a change in judgment, not just as a topic label
3. check the boundary the module is really about
4. note the first corroboration route, but do not jump there until the lesson itself is clear

This page exists to keep module names from becoming vague headings that learners have to
interpret alone.

## How to read this map

Each row answers four practical questions:

1. what the module is trying to change in your mental model
2. what boundary that promise is really about
3. what you should be able to do afterward
4. what capstone route first corroborates the lesson

If a module drifts away from that contract, the drift should be visible here.

## Start by asking what the module should change in your head

Beginners often read a module title as if it only announces subject matter:

- this module is about dynamic DAGs
- this one is about publishing
- this one is about governance

That is too flat.

The better question is:

> what judgment should I be able to make after this module that I could not make before?

That is why every row in this map names a promise, a boundary, and a leave-able-to-do
outcome.

## Module contracts

| Module | The promise | The boundary | You should leave able to... | First corroboration route |
| --- | --- | --- | --- | --- |
| [01 File Contracts](../module-01-file-contracts-workflow-graph-truth/index.md) | make Snakemake legible as a file-contract system instead of command folklore | rules, targets, rerun causes, publish discipline | explain why a job appears in the DAG before any execution happens | [Capstone Walkthrough](../capstone/capstone-walkthrough.md) |
| [02 Dynamic DAGs](../module-02-dynamic-dags-discovery-integrity/index.md) | show how discovery can change the DAG without becoming magic | checkpoints, discovered-set artifacts, wildcard limits, publish integrity | point to the artifact that records what discovery found | [Capstone Walkthrough](../capstone/capstone-walkthrough.md) |
| [03 Production Operations](../module-03-production-operations-policy-boundaries/index.md) | separate workflow meaning from operational policy | profiles, retries, staging, clean-room proof, governance | explain what may vary across runs without changing workflow semantics | [Capstone Architecture Guide](../capstone/capstone-architecture-guide.md) |
| [04 Scaling Workflows](../module-04-scaling-workflows-interface-boundaries/index.md) | grow the repository without hiding the visible workflow graph | includes, modules, file APIs, validation, CI review surfaces | decide where a scaling change belongs before splitting files | [Capstone File Guide](../capstone/capstone-file-guide.md) |
| [05 Software Boundaries](../module-05-software-boundaries-reproducible-rules/index.md) | teach the line between workflow orchestration and the software it drives | scripts, packages, environments, provenance, runtime contracts | explain where rule logic ends and helper software begins | [Capstone Proof Guide](../capstone/capstone-proof-guide.md) |
| [06 Publishing](../module-06-publishing-downstream-contracts/index.md) | make publish surfaces explicit downstream contracts instead of convenience folders | `results/` versus `publish/v1/`, manifests, reports, provenance | explain which outputs a downstream consumer is allowed to trust | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) |
| [07 Workflow Architecture](../module-07-workflow-architecture-file-apis/index.md) | teach repository architecture as part of reproducibility and reviewability | entrypoints, rule families, file APIs, helper boundaries, repository layers | point to the owning layer for a structural workflow change | [Capstone File Guide](../capstone/capstone-file-guide.md) |
| [08 Operating Contexts](../module-08-operating-contexts-execution-policy/index.md) | keep executor and profile differences reviewable without semantic drift | local, CI, and scheduler policy; retries; storage and staging assumptions | explain what changed across contexts and why the workflow promise stayed stable | [Capstone Architecture Guide](../capstone/capstone-architecture-guide.md) |
| [09 Incident Response](../module-09-performance-observability-incident-response/index.md) | make workflow incidents diagnosable before edits begin | logs, benchmarks, summaries, provenance, triage routes | choose the next evidence surface before touching the workflow | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) |
| [10 Governance](../module-10-governance-migration-tool-boundaries/index.md) | teach stewardship, migration order, and honest tool boundaries | review method, migration sequencing, governance rules, handoff decisions | improve the repository while preserving trust in current outputs and proof routes | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) |

## What this page prevents

This map exists to prevent four common course failures:

- a module promises judgment but only delivers syntax
- a module promises operations but never reaches executable proof
- a module promises architecture but leaves ownership blurry
- a module promises stewardship but never turns into review behavior

If you notice one of those failures while reading, come back here and name the missing
piece directly.

## The beginner mistake to catch early

The most common beginner mistake is mistaking recognition of a module topic for command of
the module promise.

For example:

- knowing that Module 06 is about publishing is not the same as being able to define the downstream contract
- knowing that Module 08 is about contexts is not the same as being able to separate policy drift from semantic drift

This page is here to keep that difference visible.

## Best companion pages

- [Module Checkpoints](module-checkpoints.md) when you need the exit bar after the promise
- [Proof Ladder](proof-ladder.md) when the corroboration route feels too heavy
- [Capstone Map](../capstone/capstone-map.md) when the promise is clear but the repository route is not
