# Python Metaprogramming

Python Metaprogramming is the runtime-mechanics course in the `python-programming`
family. It treats introspection, decorators, descriptors, and metaclasses as engineering
tools with explicit contracts, clear limits, and real operational costs.

This course exists to answer one hard question clearly:

> What is Python actually doing at runtime when code starts inspecting, wrapping, or
> rewriting other code and objects?

## Who this course is for

- Python developers who already write solid application code and now need stronger runtime judgment
- Library and framework authors who must preserve signatures, debugging, and tooling behavior
- Reviewers inheriting meta-heavy codebases that feel magical and brittle
- Engineers who want to know when decorators, descriptors, or metaclasses are justified and when they are not

## Who this course is not for

- Readers looking for clever tricks without runtime semantics
- Teams treating metaprogramming as a shortcut around clear design
- People who want to start with metaclasses before understanding simpler tools

## What you will be able to do

By the end of the course, you should be able to:

- explain how Python resolves attributes, wraps callables, and creates classes
- preserve signatures, metadata, and debuggability when using decorators
- design descriptors and metaclasses with explicit invariants instead of folklore
- choose the lowest-power runtime hook that solves the problem honestly
- identify when metaprogramming has crossed the line from useful abstraction into liability

## Reading contract

This is not a browse-at-random reference. The reading path matters:

1. Learn the object model and safe introspection before transformation.
2. Learn decorators before descriptors and descriptors before metaclasses.
3. Learn the power tools before the responsibility rules that limit them.
4. Keep the capstone open while reading so every mechanism stays attached to one executable system.

If you skip that order, later material will still be readable, but the trade-offs will
feel arbitrary instead of principled.

## What this course covers

- object identity, callability, and introspection
- `inspect` as a diagnostic and verification tool
- decorators as controlled callable transformation
- descriptors as the real attribute engine
- metaclasses as class-creation hooks of last resort
- responsibility boundaries around dynamic execution, global hooks, and framework-grade magic

## How the capstone fits

[`capstone/`](https://github.com/bijux/deep-dive-series/tree/master/courses/python-programming/python-meta-programming/capstone)
is the executable proof for the course. It is a plugin runtime for incident-delivery
adapters that brings together:

- descriptor-backed configuration fields
- decorator-based action instrumentation
- metaclass-driven plugin registration
- introspection-driven manifest export

Use it to answer questions like:

- Which work happens at class-definition time versus instance time?
- Which wrappers preserve runtime identity and which ones damage it?
- Which registry or manifest behavior depends on introspection staying honest?

## Working locally

From the repository root:

```bash
make COURSE=python-programming/python-meta-programming docs-serve
make COURSE=python-programming/python-meta-programming docs-build
make COURSE=python-programming/python-meta-programming test
```

## Course shape

- `course-book/` contains the published learning material.
- `capstone/` contains the runnable plugin-runtime implementation and tests.
- `Makefile` exposes stable course-level entrypoints from the monorepo root.

## Module map

- `00` Orientation
- `01` Everything Is an Object
- `02` Basic Introspection
- `03` The `inspect` Module
- `04` Decorators
- `05` Decorator Patterns and Typing
- `06` Class Decorators and the Property Bridge
- `07` Descriptors
- `08` Descriptors for Framework-Grade Patterns
- `09` Metaclasses
- `10` Responsibility and Runtime Boundaries
- `11` Outro

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/deep-dive-series/blob/master/LICENSE).
