# Module Promise Map

Use this page when a module title sounds right but still too compressed. Good module
titles should not behave like vague topic buckets. They should tell you what judgment you
will leave with, what boundary the module is really about, and what proof route first
corroborates the lesson.

## How to use this page

Before you open a module, ask one better question than "what topic is this about?":

> What judgment should I be able to make after this module that I could not make before?

That is what this map is designed to answer.

## How to read each row

Each row tells you:

1. what change in judgment the module is trying to produce
2. which boundary the module is really about
3. what you should leave able to do
4. what capstone route first corroborates the lesson

If a module feels diffuse, return here and check whether you are losing the promise, the
boundary, or the outcome.

## Module promises

| Module | The promise | The boundary underneath it | You should leave able to... | First corroboration route |
| --- | --- | --- | --- | --- |
| [Module 01 File Contracts](../module-01-file-contracts-workflow-graph-truth/index.md) | make Snakemake legible as a file-contract system instead of as command folklore | rules, targets, rerun causes, and atomic outputs | explain why one job appears in the plan before anything runs | [Capstone Walkthrough](../capstone/capstone-walkthrough.md) |
| [Module 02 Dynamic DAGs](../module-02-dynamic-dags-discovery-integrity/index.md) | show how discovery can change the DAG without becoming magical | checkpoints, discovered-set artifacts, wildcard limits, and integrity checks | point to the artifact that records what discovery found | [Capstone Walkthrough](../capstone/capstone-walkthrough.md) |
| [Module 03 Production Operations](../module-03-production-operations-policy-boundaries/index.md) | separate workflow meaning from operational policy | profiles, retries, staging, clean-room proof, and failure discipline | explain what may vary across runs without changing workflow semantics | [Capstone Architecture Guide](../capstone/capstone-architecture-guide.md) |
| [Module 04 Scaling Workflows](../module-04-scaling-workflows-interface-boundaries/index.md) | teach how a growing repository stays legible instead of merely fragmented | includes, modules, file APIs, validation surfaces, and ownership seams | decide where a scaling change belongs before splitting files | [Capstone File Guide](../capstone/capstone-file-guide.md) |
| [Module 05 Software Boundaries](../module-05-software-boundaries-reproducible-rules/index.md) | make the line between workflow orchestration and the software it drives reviewable | scripts, packages, environments, provenance, and runtime contracts | explain where workflow logic ends and helper software begins | [Capstone Proof Guide](../capstone/capstone-proof-guide.md) |
| [Module 06 Publishing](../module-06-publishing-downstream-contracts/index.md) | turn outputs into explicit downstream contracts instead of convenience folders | internal results, publish bundles, manifests, reports, and compatibility rules | define what a downstream consumer is allowed to trust | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) |
| [Module 07 Workflow Architecture](../module-07-workflow-architecture-file-apis/index.md) | teach repository architecture as part of reproducibility and reviewability | entrypoints, rule families, file APIs, helper boundaries, and repository layers | point to the owning layer for a structural workflow change | [Capstone File Guide](../capstone/capstone-file-guide.md) |
| [Module 08 Operating Contexts](../module-08-operating-contexts-execution-policy/index.md) | keep executor and profile differences reviewable without semantic drift | local, CI, and scheduler policy; retries; staging; storage assumptions | explain what changed across contexts and why the workflow promise stayed stable | [Capstone Architecture Guide](../capstone/capstone-architecture-guide.md) |
| [Module 09 Incident Response](../module-09-performance-observability-incident-response/index.md) | make performance and trust incidents diagnosable before edits begin | isolated baseline, tuning, validation-bypass, and repeated-work evidence | classify reference, acceptance, rejection, and regression from generated proof | [Capstone Proof Guide](../capstone/capstone-proof-guide.md) |
| [Module 10 Governance](../module-10-governance-migration-tool-boundaries/index.md) | teach stewardship, migration order, and honest tool boundaries | current truth, migration proof, governance rules, and handoff decisions | improve or migrate the repository without losing trust | [Capstone Review Worksheet](../capstone/capstone-review-worksheet.md) |

## What this page is trying to prevent

This map exists to prevent common course failures:

- a module promises judgment but is remembered only as a topic label
- a module promises architecture but leaves ownership blurry
- a module promises publication but never sharpens downstream trust
- a module promises governance but stays in abstract process language

If you notice one of those failures while studying, use the promise row to name the gap.

## The beginner mistake to catch early

Recognizing the subject is not the same as gaining the module’s judgment.

For example:

- knowing that Module 06 is "about publishing" is not the same as being able to define
  the downstream contract
- knowing that Module 08 is "about contexts" is not the same as being able to separate
  policy drift from semantic drift

The course works only when that difference stays visible.

## Companion pages

- [Module Checkpoints](module-checkpoints.md) when you need the exit bar after the promise
- [Proof Ladder](proof-ladder.md) when the corroboration route feels too heavy
- [Capstone Map](../capstone/capstone-map.md) when the promise is clear but the repository
  route is not
