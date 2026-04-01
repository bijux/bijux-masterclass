# Orientation

Python gives you enough flexibility to model almost anything. That flexibility is
useful only if you can explain what your objects mean, what they are allowed to do,
and where the boundaries of responsibility actually live.

This course is a structured deep dive into those boundaries.

## What this course is not

- It is not a beginner introduction to `class`, `self`, or inheritance syntax.
- It is not a catalog of patterns detached from Python's actual runtime model.
- It is not a defense of using classes everywhere.

## What this course is

- A semantics-first guide to Python objects and the data model
- A design guide for responsibilities, collaboration, and layering
- A state-modeling guide for validation, typestate, and lifecycle transitions
- A systems guide for aggregates, events, projections, and operational evolution

## Recommended prerequisites

- Comfortable Python fluency: functions, classes, exceptions, modules, and tests
- Prior exposure to `dataclasses`, type hints, and common container behavior
- Willingness to treat design choices as contracts that must survive change

## Readiness check

You are ready for this course if you can already do most of the following without
looking up syntax:

- define a class with a meaningful constructor and instance methods
- explain the difference between a class attribute and an instance attribute
- write a small pytest test for object behavior
- use `dataclass` for a simple value type
- explain why mutating shared state can produce non-local bugs

If some of those feel shaky, you can still continue, but you will need to slow down
and verify the runtime behavior of the examples rather than relying on intuition.

## Key terms used throughout the course

- **value object**: an object defined primarily by its content rather than identity
- **entity**: an object whose continuity and lifecycle matter over time
- **aggregate**: a consistency boundary that centralizes cross-object invariants
- **projection**: a downstream read model derived from authoritative events or state
- **policy**: a replaceable object that captures a decision rule
- **adapter**: an object that translates between the domain and an external system
- **typestate**: a modeling approach where legal operations depend on lifecycle state

## Start here

- Read the full [Course Map](course-map.md).
- Then continue into [Module 01](../module-01-object-model/index.md).

## Capstone roadmap

The monitoring-system capstone matures with the course:

- Module 01 gives you the object semantics needed to trust its value types and entity boundaries.
- Module 02 explains why the code splits into domain objects, policies, runtime orchestration, and adapters.
- Module 03 explains its lifecycle states, validation boundaries, and null-avoidance choices.
- Module 04 explains its aggregate root, domain events, projections, and collaboration surfaces.
- Module 05 explains its unit of work, cleanup obligations, and compatibility pressure under change.
