# Python Meta-Programming

Python Meta-Programming is the runtime-judgment course in the `python-programming`
family. It teaches introspection, decorators, descriptors, and metaclasses as tools
that must earn their complexity through observability, testability, and clear ownership.

## Core question

The course exists to answer one question without folklore:

> What is Python actually doing at runtime, and is this the lowest-power mechanism that solves the problem honestly?

## Audience

This course is for:

- experienced Python developers who already understand ordinary object design
- library and framework authors who need signatures, metadata, and registration behavior to stay visible
- reviewers inheriting dynamic codebases that feel magical but underexplained

This course is not for:

- trick collecting
- first-contact Python learners
- designs that still have a simpler explicit solution available

## Course shape

- `course-book/` now follows one stable shape: `guides/`, `reference/`, `module-00-orientation/`, and Modules `01` to `10`
- `capstone/` contains the executable incident-plugin runtime used to prove the course claims
- `Makefile` exposes stable program-level commands from the monorepo root

## Learner route

1. Start with `course-book/guides/start-here.md`.
2. Read `course-book/guides/course-guide.md` and `course-book/guides/learning-contract.md`.
3. Move through Modules `00` to `10` in order, then close with the mastery review inside Module `10`.
4. Keep `course-book/guides/capstone-map.md` and `capstone/README.md` open while reading.

## What the capstone proves

The capstone is a plugin runtime for incident-delivery adapters. It keeps four mechanisms
visible in one small system:

- descriptor-backed configuration fields
- action decorators with preserved metadata
- metaclass-driven registration and generated constructor signatures
- introspection-driven manifest export that does not execute business actions

## Working locally

From the repository root:

```bash
make PROGRAM=python-programming/python-meta-programming docs-serve
make PROGRAM=python-programming/python-meta-programming docs-build
make PROGRAM=python-programming/python-meta-programming test
```

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE).
