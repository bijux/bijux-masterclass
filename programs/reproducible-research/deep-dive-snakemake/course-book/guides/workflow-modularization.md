# Workflow Modularization

Use this page when a workflow is growing and the real question is not "can we split it?"
but "which split keeps the workflow more legible than it is today?"

## Start with the decision, not the tool

Before you split anything, answer two questions:

1. what ownership boundary is currently hard to review
2. what would a new file make clearer that is currently blurry

If you cannot answer those, the split is probably about discomfort, not design.

## Choose the smallest boundary that clarifies the workflow

| If the real need is... | Prefer this level | What it should own | What it must not hide |
| --- | --- | --- | --- |
| one small workflow with obvious rule relationships | a single `Snakefile` | the visible graph and top-level intent | architecture complexity for its own sake |
| grouping coherent rule families in one repository | `include:` files under `workflow/rules/` | rules that share one clear contract or stage | cross-cutting defaults that only make sense after oral explanation |
| reusing a workflow bundle with an explicit interface | `workflow/modules/` | a named boundary with declared inputs and outputs | the real DAG shape or the consumer-facing file contract |
| moving non-trivial implementation out of rule bodies | `workflow/scripts/` or `src/` | computation and reusable program logic | silent workflow semantics that disappear from the rule surface |
| changing run context without changing meaning | `profiles/` | execution policy, resources, retries, and executor settings | analytical meaning or published output contracts |

## Fast decision rules

- stay in one `Snakefile` while the graph is still easier to review than the split
- use `include:` when the new file mirrors a rule family a reviewer can name in one sentence
- use `workflow/modules/` only when the module has a stable interface and a consumer can explain it
- move logic into `workflow/scripts/` or `src/` when the code is real software, not just shell glue
- keep `profiles/` for operating policy only; if a profile change alters workflow meaning, the boundary is wrong

## Warning signs

Modularization is going badly when:

- files are split because one file felt long, but ownership is now less clear
- a "common" module is imported everywhere and confidently understood nowhere
- path conventions or wildcard assumptions live only in helper code
- profile files quietly change the published meaning of the workflow
- the top-level `Snakefile` becomes an include dispatcher with no readable contract left

## Good companion surfaces

- [Module 04](../module-04-scaling-workflows-interface-boundaries/index.md) for the full teaching arc
- [Module 07](../module-07-workflow-architecture-file-apis/index.md) for repository architecture and file APIs
- [Capstone Map](../capstone/capstone-map.md) for the route from module idea to repository evidence

## Good stopping point

Stop when you can say three things clearly:

- what the new boundary owns
- what stayed visible at the rule surface
- why the repository is easier to review after the split than before it
