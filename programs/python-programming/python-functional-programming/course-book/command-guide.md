# Command Guide


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  root["Repository root"] --> course["Course Makefile"]
  course --> capstone["Capstone Makefile"]
  capstone --> proof["Tour, tests, and proof commands"]
```

```mermaid
flowchart LR
  choose["Choose what you want to learn"] --> docs["Build or serve docs"]
  choose --> install["Install capstone dependencies"]
  choose --> tests["Run the capstone tests"]
  choose --> tour["Build the learner tour"]
  choose --> proof["Run the proof route"]
```
<!-- page-maps:end -->

This page exists so the learner does not have to reverse-engineer the executable surface.
Use it whenever you want to connect a course claim to runnable evidence.

## Stable commands from the repository root

```bash
make PROGRAM=python-programming/python-functional-programming install
make PROGRAM=python-programming/python-functional-programming test
make PROGRAM=python-programming/python-functional-programming docs-serve
make PROGRAM=python-programming/python-functional-programming docs-build
make PROGRAM=python-programming/python-functional-programming capstone-tour
make PROGRAM=python-programming/python-functional-programming proof
```

## Stable commands from the capstone directory

```bash
make install
make test
make tour
make proof
```

## How to choose the right command

- Use `docs-serve` when you are reading the course-book locally.
- Use `install` before your first capstone run or when the environment changed.
- Use `test` when you want executable confidence in the codebase.
- Use `capstone-tour` or `tour` when you want the learner-facing proof bundle.
- Use `proof` when you want the sanctioned end-to-end evidence route in one command.

## Honest rule

If a course claim matters, there should be a command or evidence bundle that helps you
inspect it. If you cannot name that route, use the capstone guides and module maps to
find the right surface before moving on.
