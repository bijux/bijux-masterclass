# Python Metaprogramming

Python Metaprogramming is a teaching-first masterclass in the `python-programming`
family. Its primary product is the course website: sequenced lessons, runnable labs,
worked examples, decision-focused exercises, and reasoned answers for independent study.
It teaches introspection, decorators, descriptors, and metaclasses as tools that must
earn their complexity through observability, testability, and clear ownership.

The incident-plugin capstone is the integration project. It lets learners transfer
course ideas into one realistic runtime, but it does not replace the lessons or define
the whole learning experience.

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

- `course-book/guides/` contains learner routes, question maps, checkpoints, and proof ladders.
- `course-book/module-00-orientation/` plus Modules `01` to `10` contain the core teaching arc.
- `labs/` contains small executable learning surfaces that isolate the concept currently
  being taught.
- `tests/` proves the claims made by those course labs.
- `course-book/reference/` contains durable maps, glossaries, and review standards.
- `course-book/capstone/` contains integration-project routes, architecture walkthroughs,
  and review checklists.
- `capstone/` contains the executable incident-plugin runtime used for transfer and
  integration proof.
- `Makefile` exposes stable program-level commands from the monorepo root

## Reading contract

This is not a browse-at-random course. The sequence matters:

1. Learn runtime observation before wrapper design.
2. Learn wrapper design before descriptor ownership.
3. Learn descriptor ownership before metaclasses.
4. Learn the mechanism ladder before governance and red lines.
5. Run the focused lesson or lab before transferring the mechanism into the capstone.
6. Use the capstone after the concept is clear enough to explain what the larger system adds.

If you skip that order, later modules can still feel readable, but the design trade-offs
become much harder to judge honestly.

## Learner route

1. Start with `course-book/guides/start-here.md`.
2. Read `course-book/guides/course-guide.md` and `course-book/guides/learning-contract.md`.
3. Keep `course-book/guides/module-promise-map.md` open so each module stays attached to one clear promise.
4. Use `course-book/guides/module-checkpoints.md` to decide whether you are ready to move on.
5. Use `course-book/guides/pressure-routes.md` when your engineering question is clearer than the mechanism name.
6. Use `course-book/guides/proof-matrix.md` when you want the course promises tied directly to evidence.
7. Use `course-book/module-00-orientation/mid-course-map.md` when you are leaving the observation modules and entering wrappers, descriptors, and class customization.
8. Use `course-book/module-00-orientation/mid-course-map.md` when you are resuming the course after a break and need to re-enter from the right boundary.
9. Use `course-book/guides/proof-ladder.md` when you need the smallest honest proof route.
10. Move through Modules `00` to `10` in order, then close with the mastery review inside Module `10`.
11. Use `course-book/capstone/index.md` and `course-book/capstone/capstone-map.md` after
    each module to locate its smallest integration proof.

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
is the integration project for the course. It is a plugin runtime for incident-delivery
adapters that keeps four mechanisms visible in one inspectable system:

- descriptor-backed configuration fields
- action decorators with preserved metadata
- metaclass-driven registration and generated constructor signatures
- introspection-driven manifest export that does not execute business actions

Use it to answer questions like:

- Which behavior belongs to attribute access instead of wrappers?
- Which work happens at class-definition time instead of runtime invocation?
- Which exported facts can be inspected without executing user behavior?

Those questions are transfer work. Learn each mechanism first from the core lesson,
runnable example, worked example, and exercises. Then use the capstone to check whether
your explanation survives contact with a system where several mechanisms interact.

## Working locally

From the repository root:

```bash
make PROGRAM=python-programming/python-meta-programming docs-serve
make PROGRAM=python-programming/python-meta-programming docs-build
make -C programs/python-programming/python-meta-programming lab
make -C programs/python-programming/python-meta-programming lab-test
make -C programs/python-programming/python-meta-programming observation-lab
make -C programs/python-programming/python-meta-programming observation-debug-view
make -C programs/python-programming/python-meta-programming observation-lab-test
make -C programs/python-programming/python-meta-programming evidence-lab
make -C programs/python-programming/python-meta-programming evidence-lab-test
make -C programs/python-programming/python-meta-programming evidence-repr
make -C programs/python-programming/python-meta-programming evidence-repr-test
make -C programs/python-programming/python-meta-programming capstone-bind-action
make PROGRAM=python-programming/python-meta-programming test
make PROGRAM=python-programming/python-meta-programming capstone-walkthrough
make PROGRAM=python-programming/python-meta-programming capstone-tour
make PROGRAM=python-programming/python-meta-programming capstone-verify-report
make PROGRAM=python-programming/python-meta-programming capstone-confirm
```

Use `lab` for the Module 01 runtime-object evidence. Use `observation-lab` and
`observation-debug-view` for Module 02's observation boundaries and worked example.
Use `evidence-lab` and `evidence-repr` for Module 03's classified evidence packet and
signature-guided representation. The matching focused targets verify each teaching
contract. `capstone-bind-action` is the Module 03 transfer: it validates a real action
call without constructing or invoking the plugin. `lab-test` verifies all course labs.
Use `capstone-walkthrough` when you are ready for the broader integration project,
`capstone-tour` when you want the same saved bundle in the proof ladder,
`capstone-verify-report` when you need durable integration evidence, and
`capstone-confirm` for the strictest capstone confirmation pass.

Primary reading route:

- `course-book/guides/index.md`
- `course-book/guides/start-here.md`
- `course-book/index.md`
- `course-book/module-00-orientation/index.md`
- `course-book/module-01-runtime-objects-object-model/index.md`
- `labs/runtime_objects/evidence.py`
- `course-book/module-01-runtime-objects-object-model/exercises.md`
- `course-book/module-01-runtime-objects-object-model/exercise-answers.md`
- `course-book/module-02-runtime-observation-inspection/index.md`
- `labs/runtime_observation/evidence.py`
- `labs/runtime_observation/debug_view.py`
- `course-book/module-02-runtime-observation-inspection/exercises.md`
- `course-book/module-02-runtime-observation-inspection/exercise-answers.md`
- `course-book/module-03-signatures-provenance-runtime-evidence/index.md`
- `labs/runtime_evidence/evidence.py`
- `labs/runtime_evidence/safe_repr.py`
- `course-book/module-03-signatures-provenance-runtime-evidence/exercises.md`
- `course-book/module-03-signatures-provenance-runtime-evidence/exercise-answers.md`
- `course-book/capstone/index.md`
- `course-book/capstone/capstone-map.md`
- `course-book/capstone/capstone-architecture-guide.md`
- `course-book/capstone/capstone-walkthrough.md`
- `course-book/reference/topic-boundaries.md`
- `course-book/reference/anti-pattern-atlas.md`

## License

MIT — see the repository root [LICENSE](https://github.com/bijux/bijux-masterclass/blob/master/LICENSE).
