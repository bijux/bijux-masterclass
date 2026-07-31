# Module 09 Capstone Delta

Module 08 ends with a local FuncPipe RAG system whose asynchronous work, failure
values, effect descriptions, and backpressure rules are explicit. Module 09 does
not replace that architecture. It tests whether the same contracts survive contact
with ordinary Python tools and process boundaries.

## The pressure

The application now needs library helpers, tabular inputs, HTTP and CLI shells,
configurable assembly, optional distributed backends, effectful clients, and a
portable pipeline description. Importing a framework directly into the domain
would make those tools the owners of the application.

## The completed change

| Core | New Module 09 surface | Behavior that remains true |
| --- | --- | --- |
| Standard library tools | `interop/stdlib_fp.py`, `rag/stdlib_fp.py` | RAG stages remain lazy and deterministic |
| Helper libraries | `interop/toolz_compat.py`, `interop/returns_compat.py` | the core stays importable without optional packages |
| Data processing | `interop/dataframes.py` | normalization returns new records |
| Web and services | `boundaries/web/` | HTTP remains an adapter, not domain ownership |
| Data and ML pipelines | `pipelines/configured.py` | invalid stage order fails before consumption |
| CLI and config | `pipelines/cli.py`, `boundaries/shells/` | overrides are pure data before the shell performs I/O |
| Distributed dataflow | `pipelines/distributed.py` | unavailable backends fail honestly; local proof remains authoritative |
| Functional facades | `domain/facades.py` | effects remain descriptions until interpreted |
| Cross-process composition | `pipelines/specs.py` | only allow-listed function identifiers become executable |
| Team adoption | the module review route | contracts are defended by executable evidence, not style slogans |

Module 09 is represented by
`capstone/module-reference-states/module-09`. Module 10's live
`capstone/src/funcpipe_rag` endpoint must preserve these public behaviors while
adding sustainment work.

## Comparison route

From the repository root:

```bash
make PROGRAM=python-programming/python-functional-programming history-refresh
git diff --no-index \
  programs/python-programming/python-functional-programming/capstone/_history/worktrees/module-08 \
  programs/python-programming/python-functional-programming/capstone/_history/worktrees/module-09
```

Start with the newly owned directories rather than reading the whole diff:

```text
src/funcpipe_rag/interop/
src/funcpipe_rag/pipelines/
src/funcpipe_rag/boundaries/web/
src/funcpipe_rag/domain/facades.py
tests/learning/test_module_09_interop.py
```

The history diff also changes module markers in inherited files. Those markers
identify the snapshot; they are not new application behavior.

## Proof route

The focused learning tests are deliberately readable:

```bash
PYTHONPATH=programs/python-programming/python-functional-programming/capstone/module-reference-states/module-09/src \
  programs/python-programming/python-functional-programming/capstone/../../../../artifacts/venv/python-programming/python-functional-programming/capstone/bin/pytest \
  -q programs/python-programming/python-functional-programming/capstone/module-reference-states/module-09/tests/learning/test_module_09_interop.py
```

Each exercise points to one test name. Read the test before implementation, make
the smallest defensible change, and then run that test. The full Module 09 snapshot
and live capstone suites remain the broader regression evidence.
