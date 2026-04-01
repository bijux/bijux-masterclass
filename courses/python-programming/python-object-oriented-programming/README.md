# Python Object-Oriented Programming

Python Object-Oriented Programming is the object-design course in the `python-programming`
family. It treats classes, state, interfaces, aggregates, and object collaboration as
engineering contracts rather than style preferences.

The course is intentionally opinionated. It teaches when classes clarify a system, when
they create avoidable coupling, and how to keep object-oriented Python explicit, testable,
and evolvable under production change.

## What this course covers

- Python's object model: identity, state, attribute lookup, equality, hashing, and copying
- Object responsibilities: composition, inheritance, protocols, semantic types, and layering
- State design: properties, dataclasses, validation, null-handling, and typestate
- Collaboration: aggregates, domain events, projections, adapters, and strategy objects
- Operational survival: resource ownership, unit of work, compatibility, and refactoring

## Course structure

- `course-book/` contains the published course material.
- `capstone/` contains a runnable monitoring-system reference implementation.
- `Makefile` exposes stable course-level entrypoints inside the monorepo.

## Quickstart

Preview the course book locally from the repository root:

```bash
make COURSE=python-programming/python-object-oriented-programming docs-serve
```

Run the course-level verification target:

```bash
make COURSE=python-programming/python-object-oriented-programming test
```

Run the capstone directly:

```bash
make -C courses/python-programming/python-object-oriented-programming/capstone confirm
```

## Module map

- `00` Orientation and course map
- `01` Object model and data-model semantics
- `02` Design roles, interfaces, and layering
- `03` State, validation, dataclasses, and typestate
- `04` Aggregates, events, projections, and collaboration
- `05` Resource ownership, failure handling, and long-term evolution

## License

MIT — see [LICENSE](LICENSE).
