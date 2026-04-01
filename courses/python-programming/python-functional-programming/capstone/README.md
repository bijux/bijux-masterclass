# FuncPipe RAG Capstone

This directory contains the runnable project that accompanies the Python Functional Programming course book.

The course root stays stable:

- `course-book/` holds the narrative modules and reference material.
- `capstone/` holds the executable FuncPipe RAG implementation, tests, snapshots, and helper scripts.

From the repository root, use the course wrapper targets:

```bash
make COURSE=python-programming/python-functional-programming install
make COURSE=python-programming/python-functional-programming test
```

From this directory, you can also invoke the project targets directly:

```bash
make install
make test
```

Build the learner-facing proof bundle:

```bash
make tour
```

## How to study this capstone

Use this repository as evidence, not just as a runnable project:

- inspect pure transformation helpers before infrastructure packages
- inspect tests alongside implementation so claims stay attached to proof
- inspect adapters and shells when the course starts talking about effect boundaries
- inspect async effect packages only after the sync boundaries are already clear

The capstone should make the course’s abstractions easier to trust, not easier to hand-wave.
