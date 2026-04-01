# FuncPipe Capstone Guide

The FuncPipe RAG capstone is the course’s executable proof. It is not a separate side
project and not a graduation appendix. It is the codebase the course keeps pointing to
when it talks about purity, lazy pipelines, effect boundaries, and async plans.

## What this capstone is proving

The capstone demonstrates a Python codebase where:

- pure transforms remain separate from effectful boundaries
- iterator pipelines and materialization points are explicit
- Result-like flows, retries, and structured policies are inspectable in code
- infrastructure is organized behind protocols and adapters
- async coordination is described explicitly instead of being smeared through the core

## How to use it while reading

- After Module 01, inspect the smallest pure transforms and their tests.
- After Module 03, inspect where lazy dataflow stays lazy and where the system chooses to materialize.
- After Module 07, inspect capability boundaries and the difference between protocols and adapters.
- After Module 08, inspect async plan helpers and the shells that actually drive them.

Use the capstone to answer: "What would this module look like in a real Python repository?"

## Best entrypoints

- Repository guide: [`capstone/README.md`](https://github.com/bijux/deep-dive-series/blob/master/courses/python-programming/python-functional-programming/capstone/README.md)
- Core packages: [`capstone/src/funcpipe_rag/`](https://github.com/bijux/deep-dive-series/tree/master/courses/python-programming/python-functional-programming/capstone/src/funcpipe_rag)
- Test surface: [`capstone/tests/`](https://github.com/bijux/deep-dive-series/tree/master/courses/python-programming/python-functional-programming/capstone/tests)

## Core commands

```bash
make COURSE=python-programming/python-functional-programming install
make COURSE=python-programming/python-functional-programming test
make COURSE=python-programming/python-functional-programming capstone-tour
make -C capstone test
```

## What to inspect during review

- Which code is still pure and which code crosses an effect boundary?
- Which dataflow is lazy, and where is materialization deliberate?
- Which abstractions simplify reasoning, and which ones only rename complexity?
- Which claims are backed by tests instead of by commentary?
