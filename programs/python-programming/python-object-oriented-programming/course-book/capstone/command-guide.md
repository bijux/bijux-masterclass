# Command Guide


<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Object-Oriented Programming"]
  program --> pressure["A concrete question you need answered"]
  pressure --> guide["Command Guide"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Name the exact question you need answered"] --> skim["Skim only the sections that match that pressure"]
  skim --> crosscheck["Open the linked module, proof surface, or capstone route"]
  crosscheck --> next_move["Leave with one next decision, page, or command"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this guide is for a named pressure, not for wandering the whole course-book. Read the second diagram as the guide loop: arrive with a concrete question, use only the matching sections, then leave with one smaller and more honest next move.

This page exists so you do not have to reverse-engineer the executable surface.
Use it whenever you want to connect course claims to runnable evidence.

## Stable commands from the repository root

```bash
make PROGRAM=python-programming/python-object-oriented-programming docs-serve
make PROGRAM=python-programming/python-object-oriented-programming docs-build
make PROGRAM=python-programming/python-object-oriented-programming test
make PROGRAM=python-programming/python-object-oriented-programming demo
make PROGRAM=python-programming/python-object-oriented-programming inspect
make PROGRAM=python-programming/python-object-oriented-programming capstone-walkthrough
make PROGRAM=python-programming/python-object-oriented-programming capstone-tour
make PROGRAM=python-programming/python-object-oriented-programming capstone-verify-report
make PROGRAM=python-programming/python-object-oriented-programming capstone-confirm
make PROGRAM=python-programming/python-object-oriented-programming proof
```

## Stable commands from the capstone directory

```bash
make confirm
make demo
make inspect
make tour
make verify-report
make proof
```

## How to choose the right command

- Use `docs-serve` when you are reading and want the course-book locally.
- Use `test` when you want the raw executable suite without the review bundles.
- Use `demo` when you want the scenario printed directly in the terminal without the saved inspection bundle.
- Use `inspect` when you want a saved inspection bundle with scenario, rules, and history outputs.
- Use `capstone-walkthrough` from the repository root, or `tour` inside `capstone/`, when you want the saved walkthrough bundle for review or sharing.
- Use `capstone-tour` when you want the stronger tour route after the walkthrough is already clear.
- Use `capstone-verify-report` or `verify-report` when you want test output and saved state captured together.
- Use `capstone-confirm` or `confirm` when you want the strongest program-approved confirmation route.
- Use `proof` when you want the full course-sanctioned evidence route in one command.

## Route by review goal

| If you want to... | Start with | Escalate to |
| --- | --- | --- |
| understand the capstone story without reading internals first | `capstone-walkthrough` | `capstone-tour` |
| inspect saved review state | `inspect` | `capstone-verify-report` |
| run raw executable checks quickly | `test` | `capstone-confirm` |
| review architecture with durable evidence | `capstone-tour` | `capstone-verify-report` |
| run the strongest course-approved confirmation route | `capstone-confirm` | `proof` |

## Smallest honest command

- If the question is narrative, start with `capstone-walkthrough` and use `demo` only when you specifically want the terminal-only scenario route.
- If the question is behavioral, start with `test` or `inspect`.
- If the question is whole-capstone trust, start with `capstone-confirm` and escalate to `proof` only when you need the full public proof route.

## Honest rule

If a course claim matters, there should be a command or test route that helps you inspect
it. If you cannot name that route, use the capstone pages, local guide files, and module
maps to find the right surface before moving on.
