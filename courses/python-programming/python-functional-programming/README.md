# Python Functional Programming — Correctness-First Course & FuncPipe RAG Build

[![License](https://img.shields.io/github/license/bijux/python-functional-programming?style=flat-square)](https://github.com/bijux/python-functional-programming/blob/main/LICENSE)
[![Docs](https://img.shields.io/badge/docs-live-blue?style=flat-square)](https://bijux.github.io/python-functional-programming/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square)](https://www.python.org/)

**A production-minded deep dive into functional programming in Python**, grounded in a real running project (FuncPipe RAG).

- **Live docs:** https://bijux.github.io/python-functional-programming/  
- **Author hub:** https://bijux.github.io/

---

## What This Project Is

- A 10-module course (Modules 01–10) that teaches FP the way you ship code: purity, explicit effects, streaming, async backpressure, algebraic data modelling, and interop with the Python ecosystem.
- A working codebase at the **end of Module 09**: config-as-data pipelines, lazy iterators, Result/Option error handling, retries/breakers, structured logs, monadic helpers (Reader/State/Writer), async plans with bounded concurrency, and config-driven pipeline specs.
- An evolving FuncPipe RAG builder you can refactor as you learn; earlier states are tagged (`module-01`, `module-02`, …) and exported under `history/`.

---

## Quickstart

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
make install            # installs dev + docs extras

# Run tests
make test

# Preview docs locally (Material theme, live reload)
make docs-serve
```

Prefer manual docs setup? `pip install -r requirements-docs.txt && mkdocs serve`.

---

## How to Navigate

- **Course book:** `course-book/` (rendered by MkDocs). Start with Module 00 for orientation, then proceed through Modules 01–10 in order.
- **Code:** `src/funcpipe_rag/` and `tests/` evolve alongside the modules; each module’s themes map to concrete code.
- **Standards:** `course-book/reference/` contains the FP standards and review checklist used throughout.
- **Snapshots:** `history/` holds module-tag exports for comparison or rollback.

The MkDocs landing page embeds this README, so repo and docs stay in sync.

---

## Module Roadmap (High Level)

| Module | Focus | What You Build |
| --- | --- | --- |
| 01 | Purity & substitution | Pure call graphs, refactors proven with Hypothesis |
| 02 | Closures & expression style | Data-first APIs, partial application, config-as-data |
| 03 | Iterators & laziness | Streaming pipelines, fan-in/out, observability taps |
| 04 | Recursion & resilience | Memoization, Result/Option for per-record failures, error aggregation |
| 05 | Algebraic data modelling | ADTs, applicative validation, monoids, Pydantic edges, serialization contracts |
| 06 | Monadic flows | `bind`/`and_then`, Reader/State/Writer patterns, configurable pipelines |
| 07 | Effect boundaries | Ports/adapters, idempotent effect design, resource safety, structured logs |
| 08 | Async & backpressure | Async generators, bounded queues, retry/timeout policies as data, rate limiting |
| 09 | Ecosystem interop | Stdlib/toolz/returns facades, dataframe-friendly FP, config-driven pipeline specs |
| 10 | Refactoring & sustainment | Performance budgets, property-based regression, governance for FP systems |

---

## FuncPipe RAG Snapshot (Module 09 State)

- **Interop:** `src/funcpipe_rag/interop/stdlib_fp.py`, plus optional `toolz`/`returns` facades.
- **Pipelines:** `src/funcpipe_rag/pipelines/` for config-driven, stateless pipeline specs and canonical hashing.
- **Boundaries & CLI:** `funcpipe_rag.boundaries.shells` exposes CLI entrypoints for JSONL data, with allow-listed reconstruction of specs.
- **Error handling & retries:** Result/Option streams, circuit breakers, structured reports, and retry policies as data.
- **Async layer:** `AsyncPlan`/`AsyncGen` with bounded concurrency, backpressure, rate limiting, and deterministic fake-time hooks for tests.
- **Standards:** `course-book/reference/fp-standards.md` and `course-book/reference/review-checklist.md` guide implementation and reviews.

---

## Repository Layout

```
course-book/   # MkDocs content (Modules 00–10, reference)
src/           # FuncPipe RAG source (end-of-Module-09 state)
tests/         # Property and regression tests
history/       # Tagged snapshots per module (exports)
all-cores/     # Concatenated module markdown helpers
Makefile       # install/test/docs workflows
mkdocs.yml     # Docs configuration (Material)
requirements-docs.txt  # Lightweight docs stack
```

---

## Contributing and Learning Flow

- Treat every claim as a contract: add or extend tests when you change behavior.
- Keep effects at the edges; prefer pure helpers and explicit data for configuration.
- Use `make docs-serve` while editing modules to keep narrative and code aligned.
- When in doubt, add a small property test before refactoring.
