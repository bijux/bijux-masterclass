# Orientation

This course teaches functional programming in Python as a discipline for making dataflow,
effects, and operational risk easier to reason about. The goal is not to imitate another
language. The goal is to make real Python systems clearer under testing, refactoring,
integration, and growth.

## What this course is not

- It is not a syntax-first introduction to `lambda`, `map`, or list comprehensions.
- It is not a tour of abstractions detached from production code.
- It is not an excuse to rename imperative complexity with functional vocabulary.

## What this course is

- A design guide for separating pure transforms from effectful boundaries
- A pipeline guide for lazy dataflow, typed failures, and explicit coordination
- A systems guide for ports, adapters, async pressure control, and long-lived refactoring
- A review guide for judging whether an abstraction improves or hides the code

## Recommended prerequisites

- Comfortable Python fluency: functions, modules, exceptions, iterators, and tests
- Prior exposure to type hints, `dataclasses`, and pytest
- Willingness to treat purity, effects, and failure handling as design contracts

## Readiness check

You are ready for this course if you can already do most of the following without looking
up syntax:

- write and test a small pure helper function
- explain why shared mutable state creates non-local bugs
- trace data through a generator or iterator pipeline
- describe the difference between domain logic and I/O orchestration
- use type hints to communicate function inputs and outputs

If some of those still feel shaky, continue more slowly and keep the capstone open while
you read. The course assumes engineering curiosity, not perfection.

## Orientation path

- Read the full [Course Orientation](course-orientation.md).
- Read [How to Study This Course](how-to-study-this-course.md).
- Keep the [FuncPipe Capstone Guide](../capstone.md) open from the beginning.

## Capstone roadmap

The FuncPipe RAG capstone matures with the course:

- Modules 01 to 03 establish purity, configuration, and lazy pipeline shape.
- Modules 04 to 06 introduce typed failures, algebraic modelling, and lawful composition.
- Modules 07 to 08 move effects and async coordination behind explicit boundaries.
- Modules 09 to 10 focus on interop, review standards, and long-lived sustainment.
