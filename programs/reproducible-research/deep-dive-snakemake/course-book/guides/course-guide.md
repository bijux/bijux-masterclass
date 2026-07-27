# Course Guide

Use this page when you need the big picture without losing the learner-first sequence.
Deep Dive Snakemake has several shelves and routes, but they do not serve the same job at
the same time. This guide exists to help you choose the smallest useful surface and stop
there.

## If you are learning this without the live class

Read this guide in four passes:

1. identify which job you are actually trying to do
2. choose the smallest course surface that serves that job
3. reject the heavier surface that only feels more complete
4. write down your next route before you open another shelf

If you skip step 2, the course can feel richer and more confusing at the same time.

## The rule that keeps the course coherent

Keep this rule in view:

> Learn the workflow idea in a small setting first. Use the capstone to corroborate that
> idea later in a larger repository.

If you reverse that order, the course becomes harder than it needs to be.

## What this guide is for

This guide is useful when you already know that you need orientation at course scale.
It is not the best page for first contact. If Snakemake itself is still new, start with
[Start Here](start-here.md) instead.

## The four durable surfaces

Deep Dive Snakemake has four durable surfaces. Treat them as different tools, not as one
large pile of pages.

### 1. Entry and orientation

Use these pages to start well, recover the reading order, and keep the first examples
small.

### 2. Modules

Use the modules for the actual teaching arc. This is where the course concepts are built
day by day.

### 3. Capstone

Use the capstone to see the same ideas survive a realistic repository shape and proof
route.

### 4. Reference

Use the reference pages when you are reviewing, repairing, diagnosing, or checking
readiness.

The modules are the course. The other shelves help you enter, corroborate, or inspect
them.

## A route-selection card you should be able to fill before browsing

Use a table like this:

| My current job is... | Smallest honest surface | Heavier surface to delay |
| --- | --- | --- |
| first contact | Start Here plus Module 00 | capstone repository |
| learning one day-sized concept | the current module | broad guide or reference browsing |
| corroborating a concept in a real repo | capstone map plus one bounded walkthrough | raw repository exploration |
| diagnosing or reviewing | reference shelf plus the specific module boundary | course-home prose |

If the heavier surface still feels more attractive, ask whether it is actually answering your current question.

## The recommended reading order

```mermaid
flowchart LR
  start["Start Here"] --> orient["Module 00"]
  orient --> early["Modules 01-03"]
  early --> middle["Modules 04-06"]
  middle --> late["Modules 07-10"]
  late --> capstone["Capstone and reference review"]
```

That order matters because later modules depend on earlier clarity:

- dynamic DAG work depends on truthful file contracts
- publish review depends on explicit internal boundaries
- architecture judgment depends on clearer ownership
- incident and governance work depend on proportionate proof habits

## Choose the right surface for the current job

Ask what job you are doing before you choose the next page.

| If your job is... | Start here | Do not start with |
| --- | --- | --- |
| first course entry | [Start Here](start-here.md) | the capstone repository |
| rebuilding the whole course picture | [Module 00](../module-00-orientation/index.md) | late-module incident or governance pages |
| finding the next page under pressure | [Pressure Routes](pressure-routes.md) | random browsing through `guides/` |
| checking whether a claim needs more evidence | [Proof Ladder](proof-ladder.md) | the strongest available command |
| translating module names into outcomes | [Module Promise Map](module-promise-map.md) | skim-reading every module index |
| deciding whether you are ready to continue | [Module Checkpoints](module-checkpoints.md) | the next module by default |
| entering the capstone honestly | [Capstone Map](../capstone/capstone-map.md) | raw repository files |
| diagnosing a review or boundary problem | [Reference Shelf](../reference/index.md) | course-home prose |

## The teaching arc in plain language

| Arc | Modules | What becomes possible |
| --- | --- | --- |
| workflow truth | Modules 01-02 | you can explain the DAG, discovery, and rerun behavior honestly |
| production and boundary control | Modules 03-05 | you can separate policy from meaning and software from orchestration |
| publication and repository design | Modules 06-08 | you can define what is public, what is internal, and what changes safely across contexts |
| incident and stewardship judgment | Modules 09-10 | you can investigate surprises and plan change without losing trust |

## What goes wrong when the wrong shelf answers the question

Use this card before you keep reading:

| If you are about to... | The likely hidden problem is... | Smaller route |
| --- | --- | --- |
| open the capstone before the module concept is stable | corroboration is replacing learning | stay in the current module example |
| browse reference to understand a lesson for the first time | diagnosis language is replacing the teaching arc | return to the module or Start Here |
| skim many module indexes to regain control | overview hunger is replacing sequence | use Module Promise Map or Course Map |
| choose the strongest proof surface immediately | evidence appetite is outrunning the question | use Proof Ladder and keep the smallest useful command |

If the smaller route feels too simple, that usually means it is the right route.

## What each surface should and should not do

| Surface | Use it for | Do not expect it to do |
| --- | --- | --- |
| orientation | getting started, pacing, and restoring sequence | teaching advanced judgment in full |
| modules | learning one day-sized concept deeply | proving everything about the capstone at once |
| capstone | repository-scale corroboration | acting as a beginner’s first exposure |
| reference | diagnosis, repair, and readiness checks | replacing the lesson sequence |

## A strong daily route

For most modules, this is the right rhythm:

1. reproduce the smallest example and make a prediction
2. read the lesson while keeping one concrete question in mind
3. work through the example without copying blindly
4. complete Exercises 1-5 before opening the answer page
5. complete Exercises 6-10 with a little more pressure or transfer
6. use [Module Checkpoints](module-checkpoints.md) to decide whether to continue

If your explanation is still weak, reduce the example before you widen into the capstone.

## Best defaults

Use these defaults unless a specific pressure gives you a better route:

1. enter with [Start Here](start-here.md)
2. anchor with [Module 00](../module-00-orientation/index.md)
3. read modules in order
4. keep [Learning Contract](learning-contract.md) and [Proof Ladder](proof-ladder.md)
   nearby
5. enter the capstone through [Capstone Map](../capstone/capstone-map.md)

## A warning about skipping

Later modules may sound more advanced and more immediately relevant. That does not make
them safer entry points.

If a later module is pulling you forward, ask which earlier skill it assumes:

- publish review assumes you already understand internal workflow truth
- operating-context review assumes you can separate policy from semantics
- incident response assumes you know which evidence routes deserve trust
- migration work assumes all of the above

Skipping is only safe when the earlier skill is already genuinely stable.

## A five-line route note you should be able to write from memory

If this guide has done its job, you should be able to write:

1. what job you are trying to do right now
2. which course surface is the smallest honest fit
3. which heavier surface you are intentionally delaying
4. why that heavier surface would be premature
5. what page you should open next

If you cannot do that, do not browse wider. Pick the smaller route again.

## Good stopping point

Stop reading this guide when you can answer these two questions:

1. Which surface should answer my next question?
2. Why would a heavier surface be premature right now?
