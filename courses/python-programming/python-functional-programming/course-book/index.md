# Python Functional Programming

This course teaches functional programming in Python as a discipline of explicit dataflow,
controlled effects, and reviewable operational boundaries. The point is not to imitate a
different language. The point is to make Python systems easier to reason about, refactor,
test, and run in production.

## Why this course exists

Many Python functional-programming resources stop in one of two bad places:

- they stay at toy examples and never reach logging, retries, async work, or real boundaries
- they jump to abstractions quickly and leave learners unable to connect them to ordinary production code

This course exists to close that gap.

## Reading contract

This is not a reference to skim in arbitrary order. The learner path is deliberate:

1. Start with purity, substitution, and data-first APIs.
2. Learn streaming and typed failures before talking about infrastructure.
3. Learn effect boundaries before async coordination and framework interop.
4. Keep the capstone open so every abstraction stays attached to one evolving system.

If you skip that order, later chapters will still be readable, but the architecture will
feel stylistic instead of principled.

## What each module contributes

- `Module 00` establishes the study strategy, module rhythm, and capstone map.
- `Module 01` defines the semantic floor: purity, substitution, and local FP refactors.
- `Module 02` turns functions into configurable, data-first building blocks.
- `Module 03` introduces lazy iteration and streaming pipeline design.
- `Module 04` adds typed failures, folds, retries, and structured error reports.
- `Module 05` turns domain state into explicit algebraic models and validation contracts.
- `Module 06` layers monadic flows and explicit context without losing readability.
- `Module 07` isolates infrastructure behind ports, adapters, and capability boundaries.
- `Module 08` adds async plans, bounded concurrency, and backpressure discipline.
- `Module 09` shows how to interoperate with real libraries without giving up the core model.
- `Module 10` focuses on long-lived refactoring, performance, and governance.

## How to use FuncPipe while reading

The FuncPipe RAG capstone is the course’s executable proof:

- After Module 01, inspect which parts of the pipeline are still pure transforms.
- After Module 03, inspect where lazy iteration saves memory and where materialization is a boundary choice.
- After Module 07, inspect which interfaces are capabilities and which remain concrete adapters.
- After Module 08, inspect where async work is described as data and where it is actually driven.

The capstone should answer a standing question: "What does this idea look like in a real Python codebase?"

## Working locally

From the repository root:

```bash
make COURSE=python-programming/python-functional-programming install
make COURSE=python-programming/python-functional-programming test
make COURSE=python-programming/python-functional-programming docs-serve
```

## Common failure modes this course is trying to prevent

- treating FP as syntax instead of as a contract around state and effects
- mixing pure transforms with logging, I/O, or retries until nothing is locally understandable
- introducing laziness or async work without a clear boundary for when computation actually happens
- adding abstractions that make the codebase harder to debug than the imperative version
- bolting on "functional style" while leaving the production risks untouched
