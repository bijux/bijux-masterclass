# Command Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  root["Repository root"] --> course["Course Makefile"]
  course --> capstone["Capstone Makefile"]
  capstone --> inspect["Demo, proof, and inspection commands"]
```

```mermaid
flowchart LR
  choose["Choose what you want to learn"] --> docs["Build or serve docs"]
  choose --> tests["Run confirmation tests"]
  choose --> demo["Run the learner walkthrough"]
  choose --> inspect["Inspect the capstone state"]
```
<!-- page-maps:end -->

This page exists so the learner does not have to reverse-engineer the executable surface.
Use it whenever you want to connect course claims to runnable evidence.

## Stable commands from the repository root

```bash
make PROGRAM=python-programming/python-object-oriented-programming docs-serve
make PROGRAM=python-programming/python-object-oriented-programming docs-build
make PROGRAM=python-programming/python-object-oriented-programming test
```

## Stable commands from the capstone directory

```bash
make confirm
make demo
```

## How to choose the right command

- Use `docs-serve` when you are reading and want the course-book locally.
- Use `test` or `confirm` when you want executable confidence in the capstone.
- Use `demo` when you want a human-readable walkthrough of the monitoring scenario.

## Honest rule

If a course claim matters, there should be a command or test route that helps you inspect
it. If you cannot name that route, use the capstone pages and module maps to find the
right surface before moving on.
