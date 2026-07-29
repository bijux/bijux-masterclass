# Module 02: Data-First APIs and Expression Style


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Data First Apis Expression Style"]
  page["Module 02: Data-First APIs and Expression Style"]
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

Read the first diagram as a placement map: this page sits between the course promise, the lesson pages listed below, and the capstone surfaces that pressure-test the module. Read the second diagram as the study route for this page, so the diagrams point you toward the `Lesson map`, `Exercises`, and `Closing criteria` instead of acting like decoration.

## Keep These Pages Open

Use these support surfaces while reading so data-first design stays connected to explicit
configuration and composition pressure:

- [First-Contact Map](../module-00-orientation/first-contact-map.md) for the foundation route through the first three modules
- [Module Promise Map](../guides/module-promise-map.md) for the module contract in one place
- [Practice Map](../reference/practice-map.md) for the read-inspect-prove rhythm
- [Capstone Map](../capstone/capstone-map.md) for the configured pipeline surfaces in FuncPipe

Carry this question into the module:

> What should become explicit data so the pipeline composes honestly instead of hiding choices inside control flow?

This module turns purity from a local refactoring habit into a reusable design style.
The focus is on configuration, expression-oriented code, and APIs that compose without
leaking globals or control flags.

Start with [FuncPipe Delta](capstone-delta.md). It maps the Module 01 application to
the new configured API, names the behavior that must remain equal, and provides the
smallest executable proof route.

## Learning outcomes

- how closures and partial application create configurable pure behavior
- how expression-oriented Python keeps dataflow visible
- how to design APIs that stay small, explicit, and testable
- how to represent configuration and rules as data instead of ambient behavior
- how to return expected filesystem failure without moving effects into the core

## Lesson map

- [Closures and Partials](closures-and-partials.md)
- [Expression-Oriented Python](expression-oriented-python.md)
- [Expression Review and Trade-Offs](expression-review-and-tradeoffs.md)
- [Introducing Laziness](introducing-laziness.md)
- [FP-Friendly APIs](fp-friendly-apis.md)
- [Effect Boundaries](effect-boundaries.md)
- [Configuration as Data](configuration-as-data.md)
- [Configuration Review and Validation](configuration-review-and-validation.md)
- [Callbacks to Combinators](callbacks-to-combinators.md)
- [Tiny Function DSLs](tiny-function-dsls.md)
- [Debugging Compositions](debugging-compositions.md)
- [Imperative to FP Refactor](imperative-to-fp-refactor.md)
- [FuncPipe Delta](capstone-delta.md)
- [Exercises](exercises.md)
- [Exercise Answers](exercise-answers.md)
- [Refactoring Guide](refactoring-guide.md)

## Exercises

Use [Module 02 Exercises](exercises.md) to classify API ownership, add an ordered
cleaning policy, compare rule representations, prove boundary short-circuiting, and
add neutral observation. Each exercise states the Module 01 behavior that must
remain valid. Consult [Exercise Answers](exercise-answers.md) only after writing your
prediction and evidence.

## Capstone checkpoints

- Inspect `api/config.py` and `api/core.py` in the completed Module 02 state; classify
  policy, capabilities, inputs, and observation.
- Compare `iter_rag_core` with `full_rag_api_docs`; identify cardinality and the
  first materialization point in each shape.
- Inspect `shells/rag_api_shell.py` and `shells/rag_main.py`; explain why the CLI
  delegates policy validation and why load failure precedes core execution.
- Read both learning proof files:
  `test_module_02_data_first_apis.py` and
  `test_module_02_filesystem_boundary.py`.
- Run `capstone-data-api-proof` and `capstone-data-shell-proof` from the repository
  root with `PROGRAM=python-programming/python-functional-programming`.

## Before moving on

You should be able to explain how data-first APIs stay configurable without turning into
dependency soup, where laziness starts to become a design obligation rather than an
implementation trick, and which expected failures belong to the filesystem shell.
Use [Refactoring Guide](refactoring-guide.md) and compare against
`capstone/module-reference-states/module-02` before moving forward.

## Closing criteria

- You can explain why a data-first API composes more predictably than one driven by ambient flags.
- You can identify where laziness starts to influence interface design instead of remaining an internal optimization.
- You can review a configuration path and explain how overrides stay explicit and testable.
- You can distinguish an injected-reader short-circuit proof from a real CSV/JSONL
  adapter proof.

## Directory glossary

Use [Glossary](glossary.md) when you want the recurring language in this module kept stable while you move between lessons, exercises, and capstone checkpoints.
