# Python Functional Programming

Python Functional Programming is the functional-design course in the
`python-programming` family. It teaches purity, explicit effects, streaming,
error-typed flows, and async coordination as engineering tools for building systems
that remain understandable under growth and change.

This course exists to answer one practical question clearly:

> How do you write Python systems that stay testable, composable, and operationally
> predictable without pretending the real world has no effects?

## Who this course is for

- Python developers who already ship services, pipelines, or tooling and want stronger design discipline
- Engineers who need functional techniques without turning the codebase into theory theater
- Reviewers who want concrete criteria for purity, effect boundaries, and data-first design
- Maintainers who want refactors, async work, and production debugging to become safer instead of riskier

## Who this course is not for

- Readers looking for a syntax-level introduction to `lambda`, `map`, or list comprehensions
- People treating functional programming as a catalog of clever tricks
- Teams that want "FP style" while keeping hidden globals, shared mutation, and effect-heavy cores

## What you will be able to do

By the end of the course, you should be able to:

- separate pure transforms from effectful boundaries in ordinary Python systems
- model pipelines as explicit dataflow instead of hidden state transitions
- use iterators, Result-like containers, and async plans without losing debuggability
- structure code so retries, logging, backpressure, and integration boundaries remain reviewable
- evolve a production codebase toward functional discipline without demanding a total rewrite

## Reading contract

This is not a browse-at-random reference. The reading path matters:

1. Learn purity and substitution before laziness and error composition.
2. Learn laziness and typed failures before effect boundaries and async work.
3. Learn effect boundaries before framework interop and long-term sustainment.
4. Keep the capstone open while reading so the abstractions remain attached to one codebase.

If you skip that order, later modules will still be readable, but the trade-offs will
feel ornamental instead of necessary.

If you want the shortest stable entry route, start with `course-book/guides/start-here.md`.

## What this course covers

- purity, substitution, and local reasoning
- closures, expression-oriented style, and data-first APIs
- iterators, streaming, laziness, and bounded traversal
- Result and Option style error handling, aggregation, and retries
- algebraic data modelling, validation, and serialization boundaries
- monadic flows, explicit context, and layered effect descriptions
- ports, adapters, capability protocols, and async backpressure
- ecosystem interop, refactoring, and governance for long-lived systems

## How the capstone fits

[`capstone/`](https://github.com/bijux/bijux-masterclass/tree/master/programs/python-programming/python-functional-programming/capstone)
is the executable proof for the course. It houses the FuncPipe RAG codebase that the
modules keep referring to. It is not an optional side project. It is the place where
the course’s claims become inspectable in code, tests, and command-line entrypoints.

Use it to answer questions like:

- Where does purity end and orchestration begin?
- Which abstractions remain stable under refactoring?
- Which async or effectful behaviors are described as data instead of hidden control flow?

## Working locally

From the repository root:

```bash
make PROGRAM=python-programming/python-functional-programming install
make PROGRAM=python-programming/python-functional-programming test
make PROGRAM=python-programming/python-functional-programming capstone-test
make PROGRAM=python-programming/python-functional-programming docs-serve
make PROGRAM=python-programming/python-functional-programming history-refresh
```

At the course level, `test` is the strongest published proof route and delegates to the
capstone's `confirm` target. Use `capstone-test` when you only want the pytest suite.

Primary reading route:

- `course-book/guides/index.md`
- `course-book/guides/start-here.md`
- `course-book/index.md`
- `course-book/module-00-orientation/index.md`
- `course-book/guides/history-guide.md`
- `course-book/guides/capstone.md`

## Course shape

- `course-book/` contains the published learning material.
- `course-book/guides/` contains the durable learner and capstone guides.
- `capstone/` contains the runnable FuncPipe RAG implementation, tests, and helper tooling.
- `capstone/module-reference-states/` contains the tracked end-of-module source states for Modules 01 to 09.
- `capstone/_history/` is generated locally from module tags and worktrees and is meant for study-time comparison, not as the tracked source of truth.
- `Makefile` exposes stable course-level entrypoints from the monorepo root.

## Module map

- `00` Orientation
- `01` Purity and substitution
- `02` Closures, expression style, and FP-friendly APIs
- `03` Iterators, laziness, and streaming dataflow
- `04` Recursion, folds, memoization, and streaming failures
- `05` Algebraic data modelling
- `06` Monadic flows as composable pipelines
- `07` Effect boundaries and resource safety
- `08` Async FuncPipe and backpressure
- `09` FP across libraries and frameworks
- `10` Refactoring, performance, and sustainment

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE).
