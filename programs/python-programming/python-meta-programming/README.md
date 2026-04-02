# Python Metaprogramming

Python Metaprogramming is the runtime-judgment course in the `python-programming`
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

## Module map

| Module | Title | Main focus |
| --- | --- | --- |
| `00` | Orientation and Study Practice | establish the power ladder, reading order, and capstone role |
| `01` | Runtime Objects and the Python Object Model | explain what Python objects really are at runtime |
| `02` | Safe Runtime Observation and Inspection | inspect values and code without accidental execution |
| `03` | Signatures, Provenance, and Runtime Evidence | turn observation into reliable runtime facts |
| `04` | Function Wrappers and Transparent Decorators | begin transformation without lying about behavior or metadata |
| `05` | Decorator Design, Policies, and Typing | carry runtime policy without obscuring signatures and intent |
| `06` | Class Customization Before Metaclasses | use lower-power class tools before escalating to metaclasses |
| `07` | Descriptors, Lookup, and Attribute Control | understand how attribute access is actually resolved |
| `08` | Descriptor Systems, Validation, and Framework Design | turn descriptor mechanics into disciplined runtime architecture |
| `09` | Metaclass Design and Class Creation | justify the highest-power class hook narrowly and visibly |
| `10` | Runtime Governance and Mastery Review | convert mechanism knowledge into review standards and exit criteria |

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
