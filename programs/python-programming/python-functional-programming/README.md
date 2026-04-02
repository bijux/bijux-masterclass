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
When Modules 01 to 03 feel stable and you need the cleanest bridge into failures,
effects, and async pressure, use `course-book/module-00-orientation/mid-course-map.md`.
When you are returning after a break and need the right re-entry boundary, use
`course-book/module-00-orientation/return-map.md`.

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
make PROGRAM=python-programming/python-functional-programming history-verify
```

At the course level, `test` is the strongest published proof route and delegates to the
capstone's `confirm` target. Use `capstone-test` when you only want the pytest suite.

Primary reading route:

- `course-book/guides/index.md`
- `course-book/guides/start-here.md`
- `course-book/index.md`
- `course-book/module-00-orientation/index.md`
- `course-book/guides/history-guide.md`
- `course-book/capstone/index.md`

## Course shape

- `course-book/guides/` contains the durable learner routes, reading contracts, checkpoints, and proof maps.
- `course-book/capstone/` contains the repository entry pages, architecture routes, file guides, and review worksheets.
- `course-book/reference/` contains durable maps, glossary pages, and review standards.
- `course-book/module-00-orientation/` plus Modules `01` to `10` contain the core teaching arc.
- `capstone/` contains the runnable FuncPipe RAG implementation, tests, and helper tooling.
- `capstone/module-reference-states/` contains the tracked end-of-module snapshot sources for Modules 01 to 09.
- `capstone/_history/` is generated locally from module tags, verified worktrees, and per-module manifests, and is meant for study-time comparison, not as the tracked source of truth.
- `Makefile` exposes stable course-level entrypoints from the monorepo root.

## Module map

| Module | Title | Main focus |
| --- | --- | --- |
| `00` | Orientation and Study Practice | establish the reading order, proof surfaces, and capstone role |
| `01` | Purity, Substitution, and Local Reasoning | make state and effects explicit before composition grows |
| `02` | Data-First APIs and Expression Style | turn helpers into configurable, data-driven pipeline pieces |
| `03` | Iterators, Laziness, and Streaming Dataflow | build lazy pipelines that materialize deliberately |
| `04` | Streaming Resilience and Failure Handling | make retries, folds, cleanup, and typed failures explicit |
| `05` | Algebraic Data Modelling and Validation | encode domain states and validation as explicit value shapes |
| `06` | Monadic Flow and Explicit Context | compose dependent work without hiding context or failure |
| `07` | Effect Boundaries and Resource Safety | move I/O, adapters, and resource lifecycles behind contracts |
| `08` | Async Pipelines, Backpressure, and Fairness | add bounded async coordination and deterministic async proof |
| `09` | Ecosystem Interop and Boundary Discipline | work with libraries and frameworks without losing the core design |
| `10` | Refactoring, Performance, and Sustainment | keep the system governable under growth, review, and change |

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE).
