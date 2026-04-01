# Python Object-Oriented Programming

This course teaches object-oriented Python as a discipline of explicit semantics,
clear responsibilities, and long-lived system boundaries. The focus is not on class
syntax in isolation. The focus is on how object models behave under mutation,
inheritance, refactoring, and operational change.

## Why this course exists

Many Python OOP resources stop at surface mechanics: classes, inheritance, and a few
design patterns. That is not enough to build systems that remain readable and correct
after a year of feature growth.

This course is organized around harder questions:

- What is the semantic contract of an object in Python?
- When should identity matter more than value equality?
- Where do invariants live when multiple objects collaborate?
- How do you keep object-heavy systems from becoming tangled or brittle?
- How do you evolve APIs, storage, and behaviors without breaking callers?

## Reading contract

This is not a browse-at-random reference. The course is designed as a sequence:

1. Learn the object model before discussing architecture.
2. Learn role assignment before discussing state transitions.
3. Learn state transitions before discussing aggregates and cross-object invariants.
4. Learn collaboration boundaries before discussing resources and long-term evolution.

If you skip that order, later chapters will still be readable, but the design trade-offs
will feel arbitrary instead of principled.

## Working model

The course uses a monitoring-system domain as the running example. That domain is
small enough to reason about and rich enough to force real design choices around
state, interfaces, aggregates, events, and failure handling.

## How to use the running example

- Read each module overview first to understand the design pressure for that stage.
- Keep the capstone open while reading the later modules so every abstraction stays attached to one domain.
- Use the refactor chapters as checkpoints rather than optional appendices.
- Re-run the capstone tests after modules that materially change how you think about boundaries.

## What you will build

By the end of the course, you should be able to:

- model value objects and entities without confusing their contracts
- choose composition, inheritance, protocols, or plain functions deliberately
- design state transitions so illegal states are difficult to construct
- enforce cross-object invariants through aggregate roots and disciplined APIs
- keep operational concerns like resources, logging, retries, and compatibility explicit

## What each module contributes

- [Orientation](module-00-orientation/index.md) establishes the learner contract, prerequisites, and course map.
- [Module 01](module-01-object-model/index.md) defines the semantic floor: identity, state, equality, attribute lookup, and copying.
- [Module 02](module-02-design-and-layering/index.md) assigns responsibilities across values, entities, services, policies, and adapters.
- [Module 03](module-03-state-and-typestate/index.md) turns state transitions, validation, and typestate into explicit design work.
- [Module 04](module-04-aggregates-and-collaboration/index.md) moves from single-object correctness to coherent collaboration boundaries.
- [Module 05](module-05-resources-and-evolution/index.md) focuses on survivability: cleanup, failure handling, compatibility, and change.
- [Capstone](capstone.md) provides the executable slice that keeps the prose honest.

## Common failure modes this course is trying to prevent

- treating classes as containers instead of contracts
- using inheritance because it feels reusable rather than because it preserves substitutability
- hiding invalid states behind `None`, ad hoc flags, or informal conventions
- scattering invariants across multiple objects with no clear owner
- mixing domain rules, orchestration, persistence, and integrations in the same class
- introducing "small" changes that silently widen public API or lifecycle obligations

## Reading order

- Start with [Orientation](module-00-orientation/index.md).
- Work through Modules 01 to 05 in order.
- Use the [Capstone](capstone.md) to connect the prose to runnable code.

## Expected learner rhythm

- Read one module overview before touching its chapters.
- Read chapter prose in order unless you are deliberately reviewing.
- Pause at each refactor chapter and explain the design shift in your own words.
- Use the capstone as a design mirror, not only as a code sample.
