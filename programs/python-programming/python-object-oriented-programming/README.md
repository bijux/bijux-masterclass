# Python Object-Oriented Programming

Python Object-Oriented Programming is the object-design course in the `python-programming`
family. It treats classes, state, interfaces, aggregates, and object collaboration as
engineering contracts rather than style preferences.

The course is intentionally opinionated. It teaches when classes clarify a system, when
they create avoidable coupling, and how to keep object-oriented Python explicit, testable,
and evolvable under production change.

## Who this course is for

- Python developers who already know class syntax and want stronger design judgment
- Engineers inheriting object-heavy codebases that are hard to change safely
- Library and application authors who need explicit contracts for state and collaboration
- Reviewers who want sharper criteria than "this feels object-oriented"

## Who this course is not for

- People looking for a beginner introduction to `class`, `self`, or inheritance syntax
- Readers who want a catalog of Gang of Four patterns without Python-specific trade-offs
- Teams trying to force every problem into a class hierarchy

## What you will be able to do

By the end of the course, you should be able to:

- explain the semantic contract of a Python object instead of treating it as a bag of fields
- separate values, entities, services, policies, and adapters without role confusion
- make invalid states and illegal transitions harder to construct
- design aggregates and projections that preserve invariants under change
- evolve persistence, public APIs, and serialized contracts without flattening the domain
- add time, concurrency, async, and verification pressure without losing ownership clarity
- review performance, observability, and security trade-offs without abandoning Pythonic design

## What this course covers

- Python's object model: identity, state, attribute lookup, equality, hashing, and copying
- Object responsibilities: composition, inheritance, MRO, mixins, protocols, semantic types, and layering
- State design: properties, dataclasses, validation, null-handling, and typestate
- Collaboration: aggregates, domain events, projections, adapters, and strategy objects
- Operational survival: resource ownership, unit of work, error contracts, compensation, compatibility, and refactoring
- Persistence: repositories, mapping, ORM/session boundaries, serialization, versioning, conflicts, and migration
- Runtime pressure: clocks, scheduling, queues, threads, async bridges, and safe retries
- Verification: behavioral tests, property checks, contract suites, and confidence ladders
- Extensibility: public APIs, facades, capability protocols, plugins, and governance
- Operational mastery: measurement, observability, trust boundaries, secure defaults, and capstone hardening

## Recommended background

- Comfortable Python fluency with functions, classes, exceptions, modules, and tests
- Some prior exposure to `dataclasses`, type hints, and basic testing workflow
- Willingness to evaluate design choices by failure modes, not only by aesthetics

## Course structure

- `course-book/` uses one stable shape: `guides/`, `reference/`, `module-00-orientation/`, and Modules `01` to `10`.
- `capstone/` contains a runnable monitoring-system reference implementation with
  aggregates, evaluation strategies, read models, and a runtime facade.
- `Makefile` exposes stable course-level entrypoints inside the monorepo.

## How to study this course well

1. Start with `course-book/guides/start-here.md`, `course-book/guides/module-promise-map.md`, and `course-book/guides/module-checkpoints.md` before browsing module chapters.
2. Use `course-book/guides/pressure-routes.md` when you are entering from a concrete engineering problem instead of reading front to back.
3. Work through Modules 01 to 10 in order when possible because the later modules assume earlier semantic and boundary decisions.
4. Treat each module as a design checkpoint: read the overview, then the chapter sequence, then the refactor chapter, then the module checkpoint.
5. Use Modules 01 to 05 as the semantic and survivability base, then Modules 06 to 10 as the persistence, runtime, governance, and operational mastery arc.
6. Keep the capstone open while reading so the abstractions stay grounded in one coherent domain, and use `course-book/guides/proof-ladder.md` before jumping to the strongest proof command.

## Quickstart

Preview the course book locally from the repository root:

```bash
make PROGRAM=python-programming/python-object-oriented-programming docs-serve
```

Run the course-level verification target:

```bash
make PROGRAM=python-programming/python-object-oriented-programming test
```

Run the capstone directly:

```bash
make -C programs/python-programming/python-object-oriented-programming/capstone confirm
```

Primary reading route:

- `course-book/guides/start-here.md`
- `course-book/guides/module-promise-map.md`
- `course-book/guides/module-checkpoints.md`
- `course-book/index.md`
- `course-book/module-00-orientation/index.md`
- `course-book/guides/capstone.md`

## How to know you are succeeding

- You can justify when not to introduce a class.
- You can explain why an invariant belongs in one object and not another.
- You can distinguish a projection from an authoritative domain object.
- You can add a feature to the capstone without breaking its lifecycle and boundary rules.

## Module map

- `00` Orientation and course map
- `01` Object model and data-model semantics
- `02` Design roles, inheritance trade-offs, construction boundaries, interfaces, and layering
- `03` State, validation, dataclasses, and typestate
- `04` Aggregates, events, projections, and collaboration
- `05` Resource ownership, failure handling, recovery contracts, and long-term evolution
- `06` Persistence, repositories, ORM/session boundaries, serialization, and schema evolution
- `07` Time, scheduling, concurrency, and async boundaries
- `08` Testing, verification, contracts, and confidence
- `09` Public APIs, extension points, plugins, and governance
- `10` Performance, observability, security, and capstone mastery

## Ten-module roadmap

1. Object model: identity, equality, copying, and the semantic contract of an object.
2. Design and layering: roles, composition, cooperative inheritance, construction boundaries, protocols, and boundary assignment.
3. State and typestate: validation, lifecycle transitions, and illegal-state prevention.
4. Aggregates and collaboration: cross-object invariants, events, projections, and policies.
5. Resources and evolution: cleanup, failure contracts, compensation, compatibility, and safe change.
6. Persistence and schema evolution: repositories, sessions, identity maps, codecs, versioning, and migration.
7. Time and concurrency: clocks, scheduling, retries, queues, threads, and async boundaries.
8. Testing and verification: behavioral proof, contracts, properties, and confidence ladders.
9. Public APIs and extension governance: facades, plugin seams, compatibility, and review controls.
10. Performance, observability, and security: operational review, trust boundaries, and capstone hardening.

## Capstone promise

The capstone is not decorative. It is the course's executable proof that the design
advice can survive contact with concrete code. As you move through the modules, the
monitoring-system capstone should answer three questions repeatedly:

- What object owns this invariant?
- Which behavior belongs in the domain, and which belongs in orchestration?
- What changes stay local, and what changes ripple across the system?

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE).
