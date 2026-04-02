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

## What you will be able to do

By the end of the course, you should be able to:

- explain what happens at import time, class-definition time, instance time, and call time
- inspect runtime behavior without accidentally executing the wrong thing
- preserve signatures, provenance, and reviewability when wrapping callables
- choose honestly between plain code, decorators, descriptors, class decorators, and metaclasses
- review meta-heavy code for hidden state, global hooks, and unjustified runtime power

## Recommended background

- comfortable Python fluency with classes, functions, modules, exceptions, and tests
- some exposure to `dataclasses`, `typing`, and `inspect`
- willingness to evaluate dynamic behavior by debugging cost instead of cleverness

## Course shape

- `course-book/` follows one stable shape: `guides/`, `reference/`, `module-00-orientation/`, and Modules `01` to `10`
- `capstone/` contains the executable incident-plugin runtime used to prove the course claims
- `Makefile` exposes stable program-level commands from the monorepo root

## Reading contract

This is not a browse-at-random course. The sequence matters:

1. Learn runtime observation before wrapper design.
2. Learn wrapper design before descriptor ownership.
3. Learn descriptor ownership before metaclasses.
4. Learn the mechanism ladder before governance and red lines.
5. Keep the capstone open while reading so every hook stays attached to one runnable codebase.

If you skip that order, later modules can still feel readable, but the design trade-offs
become much harder to judge honestly.

## Learner route

1. Start with `course-book/guides/start-here.md`.
2. Read `course-book/guides/course-guide.md` and `course-book/guides/learning-contract.md`.
3. Keep `course-book/guides/module-promise-map.md` open so each module stays attached to one clear promise.
4. Use `course-book/guides/module-checkpoints.md` to decide whether you are ready to move on.
5. Use `course-book/guides/design-question-map.md` when your engineering question is clearer than the mechanism name.
6. Use `course-book/guides/outcomes-and-proof-map.md` when you want the course promises tied directly to evidence.
7. Use `course-book/module-00-orientation/mid-course-map.md` when you are leaving the observation modules and entering wrappers, descriptors, and class customization.
8. Use `course-book/module-00-orientation/return-map.md` when you are resuming the course after a break and need to re-enter from the right boundary.
9. Use `course-book/guides/proof-ladder.md` when you need the smallest honest proof route.
10. Move through Modules `00` to `10` in order, then close with the mastery review inside Module `10`.
11. Keep `course-book/capstone/index.md` and `course-book/capstone/capstone-map.md` open while reading.

## What this course covers

- Python's runtime object model for functions, classes, modules, methods, and instances
- safe observation with builtins and `inspect`
- signature preservation, provenance, and wrapper discipline
- decorator design, policy boundaries, and typing-aware runtime behavior
- class decorators, properties, descriptors, and per-attribute ownership
- metaclass design, class-creation timing, and declaration-time enforcement
- governance boundaries for dynamic execution, monkey-patching, import hooks, and review policy

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

## How the capstone fits

[`capstone/`](https://github.com/bijux/bijux-masterclass/tree/master/programs/python-programming/python-meta-programming/capstone)
is the executable proof for the course. It is a plugin runtime for incident-delivery
adapters that keeps four mechanisms visible in one inspectable system:

- descriptor-backed configuration fields
- action decorators with preserved metadata
- metaclass-driven registration and generated constructor signatures
- introspection-driven manifest export that does not execute business actions

Use it to answer questions like:

- Which behavior belongs to attribute access instead of wrappers?
- Which work happens at class-definition time instead of runtime invocation?
- Which exported facts can be inspected without executing user behavior?

## Working locally

From the repository root:

```bash
make PROGRAM=python-programming/python-meta-programming docs-serve
make PROGRAM=python-programming/python-meta-programming docs-build
make PROGRAM=python-programming/python-meta-programming test
```

Primary reading route:

- `course-book/guides/index.md`
- `course-book/guides/start-here.md`
- `course-book/index.md`
- `course-book/module-00-orientation/index.md`
- `course-book/guides/capstone.md`
- `course-book/guides/capstone-architecture-guide.md`
- `course-book/guides/capstone-walkthrough.md`
- `course-book/reference/topic-boundaries.md`
- `course-book/reference/anti-pattern-atlas.md`

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE).
