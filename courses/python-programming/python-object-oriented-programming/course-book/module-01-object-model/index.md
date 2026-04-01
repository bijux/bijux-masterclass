# Module 01: Object Model

This module builds the semantic floor for the rest of the course. Before talking
about architecture, inheritance, or aggregates, you need a precise mental model of
what Python objects are and how they behave.

## Why this module matters

Most long-lived OOP mistakes are already visible at the object-model level:

- confusing identity with value
- mutating state that was assumed to be isolated
- relying on accidental attribute lookup behavior
- treating equality and hashing as convenience instead of container contracts
- choosing classes where plain values or functions would be clearer

If these semantics are fuzzy, later architecture decisions become style debates
instead of engineering decisions.

## Main questions

- What is identity, and when should it matter?
- What makes state safe or dangerous to share?
- How do equality and hashing interact with containers?
- Where does attribute lookup really happen?
- When is a class the wrong abstraction entirely?

## Reading path

1. Start with object identity and attribute layout.
2. Move into construction, representation, and equality contracts.
3. Then study aliasing, copying, and the broader data model.
4. Finish with the "when classes are the wrong tool" chapter and the module refactor.

## Common failure modes

- using mutable objects as keys without respecting hash semantics
- leaking shared state through default values, aliasing, or shallow copying
- exposing too much representation detail in the public surface of an object
- assuming attribute access is a simple field lookup when descriptors and class state are involved

## Capstone connection

The capstone's `MetricName`, `Severity`, `MetricSample`, and `ThresholdRule` types only
work because their value semantics are explicit. The `MonitoringPolicy` aggregate also
depends on a precise boundary between identity-bearing entities and value-oriented rule
definitions. Read this module as the semantic justification for those choices.

## Outcome

You should finish this module able to inspect a class or instance and explain its
data-model contract without appealing to folklore or implementation accidents.
