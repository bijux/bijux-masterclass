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
