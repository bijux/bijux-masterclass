# Start Here

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Make"]
  section["Guides"]
  page["Start Here"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Start with a terminal, not with the capstone.

## If Make is completely new

1. Complete the first Makefile in [Module 00](../module-00-orientation/index.md).
2. Confirm that `make --version` reports GNU Make 4 or newer.
3. Create a directory dedicated to course experiments.
4. Begin [Module 01](../module-01-build-graph-foundations-truth/index.md).

Keep each module’s files in a separate practice directory. Breaking a practice build is
part of learning; isolating it makes experimentation safe.

Before leaving orientation, check that you can answer these without guessing:

- Which path is the target in the file-building example?
- Which path is its prerequisite?
- Why does the second run do no work?
- Which single edit makes the target stale again?

If any answer is unclear, rerun the three commands with `make --trace`. Ten minutes spent
reading that evidence now prevents hours of memorizing syntax without a graph model.

## If you already use Make

Do not skip Module 01 merely because targets and recipes look familiar. First answer:

- Can you predict exactly which targets rebuild after changing a header?
- Can you explain the answer with `make --trace`?
- Can you run the same successful build twice and show that the second run does no work?

If any answer is uncertain, begin with Module 01. Familiar syntax and a reliable mental
model are different achievements.

## If you inherited a failing build

Use the focused routes below, but return to the full sequence after the immediate problem
is understood.

| Symptom | Read first | Command to gather evidence |
| --- | --- | --- |
| target never rebuilds | Module 01 | `make --trace TARGET` |
| target always rebuilds | Modules 01 and 03 | `make -q TARGET; echo $?` |
| `make -j` fails | Module 02 | compare `make -j1` with `make -j8` |
| variable has a surprising value | Module 04 | `make --warn-undefined-variables` |
| generated files are incomplete | Module 06 | inspect producer rules and failed-run leftovers |
| release contents vary | Modules 08 and 09 | compare sorted manifests and checksums |

## What to save from each day

Create a small learning record containing:

- the final Makefile or repository change
- the command used to verify it
- one prediction that was wrong
- one sentence explaining the corrected model

Do not save generated build directories unless an exercise explicitly asks for failure
evidence.

## When to read answers

Attempt an exercise first. If you are blocked for more than 20 minutes:

1. write down the exact behavior you expected
2. capture the command and output you observed
3. read only the matching answer
4. close the answer and reproduce the repair yourself

An answer is a teaching aid, not proof that you can perform the skill.

## Your next page

Read [Module 00](../module-00-orientation/index.md) for setup and study rhythm, then
continue directly to [Module 01](../module-01-build-graph-foundations-truth/index.md).
Use the [course guide](course-guide.md) only when you need a route through an existing
problem.
