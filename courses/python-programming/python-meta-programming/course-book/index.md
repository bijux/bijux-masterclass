# Python Metaprogramming

This course teaches Python metaprogramming as a discipline of runtime honesty. It is not
about collecting more magic. It is about understanding what the interpreter is doing when
objects inspect, transform, and register other objects.

## Why this course exists

Many metaprogramming resources fail in one of two ways:

- they celebrate power without explaining the invariants that make it safe
- they jump straight to advanced hooks and leave readers unable to compare them to simpler alternatives

This course exists to close that gap.

## Reading contract

This is not a reference to skim in arbitrary order. The learner path is deliberate:

1. Start with the object model and introspection before decorators.
2. Learn decorators before descriptors and descriptors before metaclasses.
3. Reach the responsibility module only after you understand the mechanics it is trying to constrain.
4. Keep the capstone open so every mechanism remains attached to one executable system.

If you skip that order, later modules will still be readable, but the design trade-offs
will feel like folklore instead of engineering.

## What each module contributes

- [Module 00](module-00.md) defines the study strategy, the power ladder, and the capstone map.
- [Module 01](module-01.md) establishes the object model that all later runtime hooks depend on.
- [Module 02](module-02.md) teaches safe introspection without breaking semantics.
- [Module 03](module-03.md) turns `inspect` into a verification and diagnostic tool.
- [Module 04](module-04.md) introduces decorators as controlled callable transformation.
- [Module 05](module-05.md) develops decorator patterns with stronger production and typing discipline.
- [Module 06](module-06.md) bridges class decorators, `@property`, and the move toward attribute control.
- [Module 07](module-07.md) explains the descriptor protocol as the real attribute engine.
- [Module 08](module-08.md) extends descriptors toward framework-grade patterns.
- [Module 09](module-09.md) introduces metaclasses as a last-resort class-creation hook.
- [Module 10](module-10.md) turns responsibility, security, and debuggability into hard boundaries.
- [Capstone](capstone.md) provides the executable runtime that keeps the course honest.

## How to use the capstone while reading

- After Module 04, inspect how wrappers preserve or damage signatures and metadata.
- After Module 07, inspect where descriptor behavior lives and how state is stored.
- After Module 09, inspect what the metaclass owns that other mechanisms do not.
- After Module 10, inspect which parts of the runtime would be hardest to debug if the implementation became less explicit.

The capstone should answer the question: "What does this runtime hook look like in a real Python system?"

## Common failure modes this course is trying to prevent

- reaching for metaclasses before understanding decorators or descriptors
- treating introspection as harmless when it can trigger work or hide fragility
- wrapping callables in ways that destroy signatures, tracebacks, or tooling visibility
- making class creation more magical than the problem demands
- using dynamic power without clear responsibility boundaries
