# First-Contact Map
Use this page for your first honest session with the course. The goal is not to cover as
much ground as possible. The goal is to leave the first hour coherent enough that later
reading choices feel deliberate instead of random.

## First session route

```mermaid
flowchart TD
  promise["Read the program promise"] --> orient["Complete Module 00"]
  orient --> dryrun["Run one dry-run and one real build"]
  dryrun --> reflect["Write one plain-language explanation"]
  reflect --> decide["Choose whether to continue into Module 01 now"]
```

1. Read `../index.md` for the program promise.
2. Read `index.md` for the role of orientation.
3. Complete [Your first workflow](index.md#your-first-workflow).
4. Draw the three-node graph on paper: input, rule, output.
5. Read [Course Map](course-map.md) and choose a realistic study schedule.
6. Open [Module 01](../module-01-file-contracts-workflow-graph-truth/index.md).

Do not open the capstone yet. Its size is useful after the basic graph is familiar, but
at first contact it adds repository details that compete with the central idea.

## What you should know before Module 01

Before the first technical module, you should be able to answer:

- a target is a file you ask Snakemake to produce
- a rule connects declared input files to declared output files
- a dry-run reveals the planned graph without executing commands
- an up-to-date output does not run again merely because its rule appears in the file
- the capstone is evidence for concepts learned in smaller examples

## First-week rhythm

Repeat the same rhythm through the first modules:

1. begin by reproducing the smallest example
2. predict what the dry-run will report
3. change one input, output, or rule at a time
4. explain the observed behavior in terms of files and dependencies
5. complete the exercises before consulting their answers

## A strong first-session outcome

Your first session is successful if you can say all three of these without guessing:

- what target you requested
- why the first run had work to do
- why the second run did not

That may sound small. It is not small. It is the seed of every later topic in the
course.

## If the first workflow does not run

| Symptom | Inspect first |
| --- | --- |
| `snakemake: command not found` | complete [Platform Setup](../guides/platform-setup.md) and activate the course environment |
| `SyntaxError` or `IndentationError` | compare indentation and punctuation with the orientation `Snakefile` |
| missing `message.txt` | confirm your shell is in `artifacts/snakemake-first-workflow` |
| nothing needs to be done on the first run | remove `results/greeting.txt`, then dry-run again |
| output exists but contains unexpected text | run with `--printshellcmds` and inspect the exact command |

## When to leave this route

Move to [mid-course-map.md](mid-course-map.md) once Modules 01 to 03 feel stable and the
main question becomes scaling, publish trust, software boundaries, or operating contexts.
