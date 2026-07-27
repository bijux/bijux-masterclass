# Module 00: Orientation and Study Practice

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["Orientation"]
  page["Module 00: Orientation and Study Practice"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Read the orientation promise"] --> map["Choose the right map or guide"]
  map --> capstone["Keep one capstone surface nearby"]
  capstone --> proof["Use proof only when the ownership claim stays weak"]
  proof --> module["Enter Module 01 with one clear question"]
```
<!-- page-maps:end -->

Python gives you enough flexibility to model almost anything. That flexibility becomes
useful only when you can answer three questions clearly:

- what does this object mean?
- what is it allowed to decide?
- where should that decision boundary stop?

This course is organized to make those questions habitual. The topics grow from syntax
and semantics into persistence, runtime coordination, verification, public API
discipline, and operational review, but the ownership question stays central.

Keep one question visible while reading the whole course:

> Which object should own this decision, and what makes that ownership boundary the
> least surprising place for it to live?

That question is the thread connecting all ten modules.

## Why this orientation matters

Many learners struggle with advanced object-oriented material not because the concepts
are impossible, but because they start with the wrong expectation.

This course is not mainly about:

- Python syntax review
- inheritance tricks
- pattern names without context

It is about using Python’s object model deliberately so later architectural and
operational choices still make sense under change.

That means you should approach the course like a guided design review, not like a syntax
catalog.

## What this course is not

- it is not a first introduction to `class`, `self`, or inheritance syntax
- it is not a defense of classes for every problem
- it is not a pattern glossary detached from Python’s runtime behavior
- it is not a collection of isolated refactoring tips

These exclusions matter because they stop you from reading later pages as if they were
only style opinions.

## What this course is

This course is six things at once, in a deliberate order:

- a semantics-first guide to Python objects and the data model
- a design guide to responsibility, collaboration, and layering
- a lifecycle guide to validation, typestate, and state transitions
- a systems guide to aggregates, repositories, events, projections, and runtime
  boundaries
- a verification and governance guide to public APIs, extension seams, and long-lived
  change
- an operational hardening guide to performance, observability, security, and production
  review

Reading the course with that full arc in mind helps later modules feel like progression
instead of topic jumps.

## Readiness check

You are ready for the course if most of these already feel routine:

- defining a class with a meaningful constructor and instance methods
- explaining the difference between class attributes and instance attributes
- writing a small `pytest` test for object behavior
- using `dataclass` for a simple value type
- explaining why mutating shared state can create non-local bugs

If some of those are still shaky, do not stop. Slow down and treat examples as things to
run and inspect rather than as things to understand only by intuition.

## How to use this orientation module

Do not skim this page and jump straight into Module 01 with no plan.

Instead:

1. read the full [Course Map](course-map.md)
2. read [Module Promise Map](../guides/module-promise-map.md) so the ten-module contract
   stays visible
3. read [Module Checkpoints](../guides/module-checkpoints.md) so you know what each
   module is supposed to change in your judgment
4. choose which orientation map you are most likely to revisit first and why

This keeps the course reader-first. You should know how to navigate before the design
pressure increases.

## Orientation map set

Use these pages deliberately:

- [Course Map](course-map.md): when you need the whole arc in one view
- [First-Contact Map](first-contact-map.md): when the course still feels too large
- [Mid-Course Map](mid-course-map.md): when the topics start overlapping
- [Mastery Map](mastery-map.md): when you want the course to function like one system
  again

These pages are not filler. They are re-entry points for different learner states.

## Capstone roadmap

The monitoring-system capstone matures with the course.

- Module 01 establishes the value, entity, and object-meaning discipline needed to trust
  its core types.
- Module 02 explains the split between domain, policy, runtime orchestration, adapters,
  and the composition root.
- Module 03 explains lifecycle states, validation boundaries, and typestate discipline.
- Module 04 explains aggregates, events, projections, and cross-object collaboration
  surfaces.
- Module 05 explains failure handling, cleanup duties, and safe evolution pressure.
- Module 06 explains repositories, codecs, sessions, and schema change without
  flattening the model.
- Module 07 explains clocks, queues, schedulers, and async boundaries without leaking
  them into aggregates.
- Module 08 turns testing into contract-driven proof instead of loose example coverage.
- Module 09 explains how a stable facade and governed extension seams could be published
  safely.
- Module 10 reviews the whole design for performance, observability, trust boundaries,
  and operational readiness.

This roadmap matters because every later module assumes you still understand what the
capstone was supposed to preserve from the earlier ones.

## Common ways learners get lost

- treating the course as if modules can be learned independently with no retained
  ownership story
- focusing on syntax familiarity and ignoring semantic meaning
- reading the capstone as finished code instead of as a pressure-tested teaching artifact
- skipping the checkpoint and promise guides, then losing the thread of what each module
  is adding

If one of these sounds familiar, use the orientation maps actively instead of passively.

## What to do before Module 01

Before you continue, make sure you can answer all of these:

- what kind of reader am I today: foundation, diagnosis, or review?
- which guide will I use when I get lost?
- which capstone surface will I keep nearby first?
- what ownership question am I carrying into Module 01?

If those answers are blank, stay in orientation a little longer.

## Exercises

- write the core ownership question of the course in your own words, then name one
  design mistake it should prevent
- identify the prerequisite that feels least automatic for you, then name the first
  module where that weakness would create review confusion
- open [Course Map](course-map.md),
  [Module Promise Map](../guides/module-promise-map.md), and
  [Module Checkpoints](../guides/module-checkpoints.md), then decide which one you will
  revisit after Module 01 and why

## Closing criteria

- you can explain what this course means by object-oriented design discipline rather than
  syntax familiarity
- you know which orientation guide to revisit when you need a full map, a promise map,
  or a checkpoint bar
- you can describe how the capstone grows from semantic example to operational review
  surface across Modules 01 to 10

## Stable vocabulary

Use [Reference Glossary](../reference/glossary.md) when you want the recurring language
in this course kept stable while you move between orientation, guides, modules, and
capstone proof.
