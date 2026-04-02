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
make PROGRAM=python-programming/python-functional-programming demo
make PROGRAM=python-programming/python-functional-programming inspect
make PROGRAM=python-programming/python-functional-programming docs-serve
make PROGRAM=python-programming/python-functional-programming docs-build
make PROGRAM=python-programming/python-functional-programming capstone-tour
make PROGRAM=python-programming/python-functional-programming capstone-verify-report
make PROGRAM=python-programming/python-functional-programming capstone-confirm
make PROGRAM=python-programming/python-functional-programming proof
make PROGRAM=python-programming/python-functional-programming history-refresh
make PROGRAM=python-programming/python-functional-programming history-clean
```

## Stable commands from the capstone directory

```bash
make install
make test
make demo
make inspect
make tour
make verify-report
make confirm
make proof
make history-refresh
make history-clean
```

## How to choose the right command

- Use `docs-serve` when you are reading the course-book locally.
- Use `install` before your first capstone run or when the environment changed.
- Use `test` when you want executable confidence in the codebase.
- Use `demo` when you want the learner-facing walkthrough route with the shared catalog verb.
- Use `inspect` when you want the quickest inventory of packages, tests, and proof guides.
- Use `capstone-tour` or `tour` when you want the learner-facing proof bundle.
- Use `capstone-verify-report` or `verify-report` when you want a durable review bundle with executed test output.
- Use `capstone-confirm` or `confirm` when you want the strictest public confirmation route for this capstone.
- Use `proof` when you want the sanctioned end-to-end evidence route in one command.
- Use `history-refresh` when you want fresh module tags plus `_history/worktrees/module-XX` for module-by-module comparison.
- Use `history-clean` when you want to remove the generated history surface, the local module tags, and the generated history branch before rebuilding from scratch.

## Honest rule

If a course claim matters, there should be a command or evidence bundle that helps you
inspect it. If you cannot name that route, use the capstone guides and module maps to
find the right surface before moving on.
