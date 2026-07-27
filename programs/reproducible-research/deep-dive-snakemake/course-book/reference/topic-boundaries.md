# Topic Boundaries

Use this page when you want to understand what Deep Dive Snakemake is promising to teach
deeply, what it treats as support, and what it deliberately hands off to other courses or
other tools. A good boundary page prevents two common failures:

- expecting this course to teach every adjacent topic equally
- assuming a topic is unimportant simply because it is not the course center

This course is selective on purpose. The selectivity exists to protect learning quality.

## The main promise of the course

Deep Dive Snakemake is a course about trustworthy workflow engineering. Its central
question is:

> How do you make a Snakemake workflow legible, reviewable, and governable from first
> run through long-term stewardship?

Everything in the course is chosen because it helps answer that question.

## Core topics the course must teach deeply

If these topics stay fuzzy, the course has failed no matter how many commands ran
successfully.

| Core topic | Why it is core | Main modules | What successful learning looks like |
| --- | --- | --- | --- |
| file-contract truth | Snakemake only stays honest when rule inputs, outputs, and targets mean what they claim | 01, 02 | you can read a target, predict the graph, and spot hidden assumptions |
| dynamic DAG discipline | checkpoints are where workflows often drift from explicit contracts into runtime folklore | 02 | you can explain changing graphs as staged evidence, not magic |
| policy versus semantics | profiles and operating contexts should change execution policy, not analytical meaning | 03, 08 | you can compare contexts without confusing cost with truth |
| repository and ownership boundaries | larger workflows need smaller, durable responsibilities across modules and file APIs | 04, 07 | you can route a change to the right layer without guesswork |
| helper-code and runtime boundaries | wrappers, scripts, packages, and execution surfaces must support the workflow contract instead of hiding it | 05, 08 | you can decide what belongs in workflow code and what belongs outside it |
| publish and downstream contracts | results only become trustworthy when downstream users can inspect a stable public interface | 06 | you can define what is public, what is internal, and what evidence travels with the result |
| incident response and stewardship | a workflow has to stay reviewable under pressure and over time, not only on a calm local run | 09, 10 | you can classify a failure, choose the right evidence, and govern the next change |

## Supporting topics that strengthen the core

These topics matter because they make the core judgments easier to teach, test, and
review. They are important, but they are not the center of the course argument.

| Supporting topic | Why it matters here | Where it appears |
| --- | --- | --- |
| dry-runs, summaries, and DAG views | they make workflow intent visible before execution | Modules 01, 02, 03, 09 |
| rule modularity | it helps keep larger repositories inspectable | Modules 04, 07 |
| resource declarations | they expose operating assumptions and prevent invisible executor folklore | Modules 03, 08 |
| manifests, checksums, and integrity reports | they turn publication into a reviewable contract | Module 06 |
| benchmarks and incident evidence | they let maintainers reason from saved proof instead of memory | Module 09 |
| containers and execution surfaces | they clarify runtime boundaries when environment drift matters | Modules 05, 08 |

Study these topics as tools that strengthen a core judgment. Do not let them replace the
core judgment.

## Deliberate outer boundaries

These topics are real and valuable, but they are not the main subject of this course.

| Boundary topic | Why it is outside the center | Honest handoff |
| --- | --- | --- |
| biological analysis depth | the course uses biology as pressure, not as the main teaching surface | learn domain interpretation in the relevant science course, not here |
| general Python software architecture | helper code matters only where it affects workflow truth | use Module 05 to judge boundaries, then study broader Python design elsewhere |
| cluster administration and scheduler operations | scheduler policy matters, but workflow semantics come first | use Modules 03 and 08 for workflow-facing policy; learn administration separately |
| container ecosystem debates | containers matter as execution boundaries, not as an ideology course | use them to stabilize runtime surfaces when needed |
| general data-versioning platforms | Snakemake has neighbors and limits | Module 10 teaches when to hand off to adjacent tools |
| every Snakemake feature in equal depth | not every feature matters equally to correctness and stewardship | the course prioritizes the features that most affect reviewability |

An honest course does not pretend to be infinite. It teaches the most important ideas
deeply and hands off the rest clearly.

## Topics learners often overweight

These topics are easy to romanticize and easy to teach badly:

- wrappers treated as a substitute for understanding file contracts
- checkpoints treated as sophistication rather than explicit staged discovery
- executor flags treated as if they define analytical meaning
- results directories treated as published interfaces
- modularization treated as virtue even when ownership gets blurrier

The course does cover these, but only in ways that sharpen workflow judgment.

## Misreadings this page is meant to prevent

### "The course forgot adjacent topics."

It did not forget them. It scoped them deliberately. If a topic only matters because it
supports workflow trust, the course covers that slice and stops there.

### "If the workflow runs locally once, the advanced material is optional."

It is not optional. Later modules exist because real workflow truth appears under scale,
policy drift, publication pressure, incident response, and migration.

### "Advanced means more features."

Not here. Advanced means better judgment under change, pressure, and complexity.

### "Snakemake should own every orchestration concern forever."

Module 10 exists to prevent that mistake. Tool boundaries are part of stewardship.

## How to use this page for study decisions

When you are unsure where to spend effort, ask these questions:

1. Is this topic core, supporting, or outside the course center?
2. If it is core, which module owns it?
3. If it is supporting, which core judgment does it strengthen?
4. If it is outside the center, what is the honest handoff instead of stretching this
   course into a different one?

## Companion pages

- [Module Dependency Map](module-dependency-map.md)
- [Practice Map](practice-map.md)
- [Completion Rubric](completion-rubric.md)
- [Capstone Map](../capstone/capstone-map.md)
