# Deep Dive Snakemake

Deep Dive Snakemake is a full self-learning course for readers who want to move from
their first honest workflow to long-lived workflow stewardship. It starts with one small
local rule and ends with migration, governance, and tool-boundary judgment. The teaching
goal is not feature coverage. The teaching goal is to help you build workflows that are
legible, reviewable, and trustworthy under change.

If you are new, start here with confidence. If you already maintain a pipeline, start
here with discipline. Either way, the course is designed to take you from beginner to
advanced by building one durable idea on top of another.

## What this course teaches

By the end of the course, you should be able to:

- explain a workflow as a file-contract system instead of as shell-command folklore
- diagnose why a rule reruns, why discovery changed the graph, and why a boundary failed
- separate workflow meaning from profiles, executors, storage policy, and runtime noise
- publish results as deliberate downstream contracts instead of accidental output piles
- review architecture, incident, and migration decisions with proportionate proof

## What makes this course different

This course is intentionally cumulative.

It does not assume that:

- a successful local run proves the workflow is trustworthy
- advanced means "more features"
- the capstone repository is the best first lesson
- learners should reverse-engineer the study method from scattered pages

Instead, it teaches a stable progression:

1. understand one small workflow truthfully
2. add dynamic behavior without losing reviewability
3. add production pressure without letting policy change meaning
4. add scaling, publication, architecture, and operating-context judgment
5. finish with incident response, governance, and migration discipline

## Who this course is for

Use this course if you are:

- completely new to Snakemake and want a real foundation instead of disconnected syntax
- repairing a workflow that runs but is difficult to trust or review
- inheriting a pipeline repository and trying to understand what is public, what is
  policy, and what is internal scaffolding
- teaching or supervising workflow work and need a shared language for proof,
  boundaries, and stewardship

## What not to expect

This course is not:

- a quick syntax cheat sheet
- a cluster-administration course
- a container ideology course
- a bag of advanced tricks detached from workflow truth

It does cover those adjacent areas where they matter, but only in service of trustworthy
workflow engineering.

## Start with the right lane

| If you are here because... | Start with | Stay there until you can say... |
| --- | --- | --- |
| Snakemake is still new | [Start Here](guides/start-here.md), [Module 00](module-00-orientation/index.md), [Module 01](module-01-file-contracts-workflow-graph-truth/index.md) | "I can explain why one target ran, why another did not, and why the second run stayed quiet." |
| you need to repair an existing workflow | [Pressure Routes](guides/pressure-routes.md), [Module 03](module-03-production-operations-policy-boundaries/index.md), [Module 04](module-04-scaling-workflows-interface-boundaries/index.md) | "I know whether the problem is graph truth, policy drift, interface sprawl, or incident evidence." |
| you steward a long-lived repository | [Course Guide](guides/course-guide.md), [Module 06](module-06-publishing-downstream-contracts/index.md), [Module 07](module-07-workflow-architecture-file-apis/index.md) | "I can name what is public, what is policy, what owns the next change, and what proof is proportionate." |

## The teaching arc

The course contains one orientation module and ten core modules. Each module is designed
as a full learning day with ten exercises.

| Module | Main question | Why it matters |
| --- | --- | --- |
| [Module 00](module-00-orientation/index.md) | how should I enter and study this course | it gives you the first workflow, the study rhythm, and the capstone timing |
| [Module 01](module-01-file-contracts-workflow-graph-truth/index.md) | what does the workflow actually claim to build | all later judgment depends on truthful file contracts |
| [Module 02](module-02-dynamic-dags-discovery-integrity/index.md) | how can the DAG change without becoming magical | dynamic discovery is where many workflows lose reviewability |
| [Module 03](module-03-production-operations-policy-boundaries/index.md) | what may change across runs without changing meaning | production pressure is dangerous when policy and semantics blur |
| [Module 04](module-04-scaling-workflows-interface-boundaries/index.md) | how do larger rule sets stay legible | growth without boundaries creates accidental sprawl |
| [Module 05](module-05-software-boundaries-reproducible-rules/index.md) | where should workflow logic stop and software begin | hidden helper behavior can make a workflow unreadable |
| [Module 06](module-06-publishing-downstream-contracts/index.md) | what exactly is public downstream | outputs are not trustworthy just because files exist |
| [Module 07](module-07-workflow-architecture-file-apis/index.md) | how should the repository be shaped | architecture is part of reproducibility, not decoration |
| [Module 08](module-08-operating-contexts-execution-policy/index.md) | how do local, CI, and scheduler contexts stay comparable | context drift must not quietly change workflow meaning |
| [Module 09](module-09-performance-observability-incident-response/index.md) | how do you investigate surprises before editing | incident work needs evidence before tuning |
| [Module 10](module-10-governance-migration-tool-boundaries/index.md) | how do you steward change over time | long-lived trust requires governance and honest tool boundaries |

## How the course should feel

A healthy learning pass through this course should feel like this:

- smaller examples first
- clear predictions before commands
- stronger evidence only when the claim needs it
- capstone entry after the idea is legible locally
- later modules feeling harder because they combine earlier truths, not because they hide
  them

If the course feels like random browsing, pause and return to the entry guides instead of
opening more material.

## The support pages that matter most

Keep these nearby while you study:

| Need | Best page |
| --- | --- |
| smallest safe entry | [Start Here](guides/start-here.md) |
| big-picture route without overload | [Course Guide](guides/course-guide.md) |
| stable study habit | [Learning Contract](guides/learning-contract.md) |
| module title translated into judgment | [Module Promise Map](guides/module-promise-map.md) |
| honest readiness bar | [Module Checkpoints](guides/module-checkpoints.md) |
| proportionate proof choice | [Proof Ladder](guides/proof-ladder.md) |
| module-to-capstone routing | [Capstone Map](capstone/capstone-map.md) |
| review and repair support | [Reference Shelf](reference/index.md) |

## How the capstone fits

The capstone is the repository-sized corroboration surface for the course. It is not your
first lesson.

Use it in this order:

1. learn the concept in the module and local exercises
2. choose the smallest honest proof route
3. enter the capstone through a guided route
4. widen only when the current claim genuinely needs a larger surface

If the capstone is clearer than the module, the module is what needs another pass.

## Practice contract

Each module asks you to do more than read:

- Exercises 1-5 make the local model legible.
- Exercises 6-10 make the model transferable under review, change, or pressure.
- The answer page is for comparison after an attempt, not as a script to follow.
- The checkpoint page decides whether the next module will build on understanding or on
  recognition.

## Success signal

This home page has done its job when you know:

- exactly where to start
- why the course begins small
- which page should answer the next question
- why the capstone is corroboration rather than first contact
- why advanced stewardship depends on beginner-level file-contract truth
