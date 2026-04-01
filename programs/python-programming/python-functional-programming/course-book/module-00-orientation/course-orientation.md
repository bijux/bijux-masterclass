# Functional Programming Course Orientation

Python Functional Programming is a course about **discipline**, not ornament. It teaches
how to use functional ideas to make Python systems more predictable under refactoring,
testing, concurrency, and operational change.

## The question this course owns

Keep one question in view while reading:

> Which part of this system is pure dataflow, which part is effectful coordination, and
> can another engineer tell the difference by reading the code?

If the answer is vague, the system will get harder to reason about as it grows.

## Where this course fits

Inside the `python-programming` family:

- object-oriented programming teaches long-lived state and collaboration boundaries
- metaprogramming teaches runtime machinery and reflective control
- functional programming teaches explicit dataflow, controlled effects, and composition

This course owns the third of those. It is the course for turning "works for now" Python
into code that remains explainable when the pipeline, service, or workflow becomes bigger.

## What this course is trying to change in the learner

By the end of the course, these should stop feeling like optional cleanups:

- passing configuration as explicit data
- isolating I/O and mutation to thin boundaries
- choosing iterators instead of materializing everything
- representing expected failures as data instead of tangled control flow
- treating async coordination as a design problem instead of hidden runtime magic

Those are not stylistic preferences. They are maintainability boundaries.

## How to read the course

Read the modules in order. Each one adds a constraint the next one relies on:

1. **Purity and substitution** before abstractions.
2. **Data-first APIs and laziness** before typed failure handling.
3. **Typed failures and explicit context** before infrastructure boundaries.
4. **Infrastructure boundaries** before async backpressure and ecosystem interop.
5. **Interop and refactoring** only after the semantic floor is solid.

## What the capstone proves

[`capstone/`](https://github.com/bijux/bijux-masterclass/tree/master/programs/python-programming/python-functional-programming/capstone)
is the course’s executable proof. It contains the FuncPipe RAG codebase that the modules
keep referring to. Use it to inspect:

- pure transformation boundaries
- lazy and eager edges
- capability protocols and adapters
- Result-like flows and retry policies
- async plans and bounded orchestration

If a course claim cannot be connected to the capstone, treat the claim skeptically.

## Questions to keep asking while you read

- Which values could be substituted safely, and which steps still hide control flow?
- Where does data stop and orchestration begin?
- Which abstraction is simplifying the code, and which one is only renaming complexity?
- Which operational guarantees survive tests, retries, and asynchronous execution?
