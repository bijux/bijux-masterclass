# Effect Boundaries

<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Data First Apis Expression Style"]
  page["Effect Boundaries"]
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

Module 01 already separates a pure RAG transformation from a CSV-to-JSONL shell.
It lets ordinary filesystem exceptions escape. Module 02 keeps that structural
separation and adds one new boundary promise: expected read, parse, and write
failures are returned as values.

The design goal is not “remove all effects.” A useful application must read and
write. The goal is to make effect ownership visible so the transformation can
still be tested and reasoned about with ordinary values.

## The boundary in one sentence

Keep path handling and filesystem access in thin adapters, pass replaceable
capabilities explicitly, and call the document-based core only after input has
become validated domain data.

In the completed Module 02 state, that rule has two related forms:

```text
injected path API
path -> Reader.read_docs -> Result[list[RawDoc]]
                          -> full_rag_api_docs -> Ok[(chunks, observations)]

concrete filesystem shell
input path -> FSReader -> full_rag_api -> write_chunks_jsonl -> Result[Observations]
```

The first form isolates the reader so tests can substitute it. The second proves
that the real CSV and JSONL adapters obey the same successful-value contract.

## Read the actual source in ownership order

All paths below are under
`capstone/module-reference-states/module-02/src/funcpipe_rag/`.

| Owner | Source | Responsibility |
| --- | --- | --- |
| domain values | `rag_types.py` | define documents, chunks, and `RagEnv` invariants |
| pure application | `api/core.py` | transform `RawDoc` values and calculate observations |
| capability contract | `api/config.py` | define `Reader` and group core/boundary dependencies |
| outcome value | `result.py` | define the minimal `Ok[T] | Err` boundary result |
| concrete adapters | `shells/rag_api_shell.py` | parse CSV, serialize JSONL, and translate expected I/O failures |
| CLI configuration | `shells/rag_main.py` | parse arguments and validate policy before execution |

This ownership line matters. `full_rag_api_docs` accepts documents, not paths. It
does not open files, catch filesystem exceptions, or decide where output belongs.

## A capability is narrower than an adapter

The core configuration module declares only what the path API needs:

```python
class Reader(Protocol):
    def read_docs(self, path: str) -> Result[list[RawDoc]]: ...
```

`FSReader` is one implementation. A test reader can return a fixed `Ok` or `Err`
without touching the filesystem. Both satisfy the same capability, so
`full_rag_api_path` does not need a branch for “test mode.”

```python
failure = Err("source unavailable")


class FailingReader:
    def read_docs(self, path: str):
        assert path == "missing.jsonl"
        return failure
```

When this reader is placed in `RagBoundaryDeps`, the returned value is exactly
`failure`. No cleaner, chunker, or embedder is needed to explain that result.

This is the Module 02 meaning of dependency injection: pass a small value that
implements a required operation. It does not require a framework or global
registry.

## Short-circuiting is part of the contract

The path API has one decision:

```python
docs_result = deps.reader.read_docs(path)
if isinstance(docs_result, Err):
    return docs_result
chunks, observations = full_rag_api_docs(
    docs_result.value,
    config,
    deps.core,
)
return Ok((chunks, observations))
```

An `Err` stops the composition. An `Ok` unwraps validated documents and crosses
into the pure API. `result_map` and `result_and_then` encode the same rule for
small compositions: their function argument is never called for `Err`.

The focused API proof makes the skipped call observable in
`test_reader_failure_short_circuits_the_pure_rag_core` and
`test_result_combinators_do_not_run_after_boundary_failure`.

## The real filesystem shell adds a writer

`shells/rag_api_shell.py` owns the complete effect sequence:

1. `FSReader.read_docs` opens and parses CSV into `RawDoc` values.
2. `full_rag_api` transforms those values and returns chunks plus observations.
3. `write_chunks_jsonl` serializes the chunks.
4. `run` returns `Ok(observations)` after a successful write.

Failure timing is observable:

| Condition | Core runs? | Output state | Outcome |
| --- | --- | --- | --- |
| missing input | no | output is not created | load `Err` |
| malformed CSV row | no | output is not created | load `Err` |
| header-only CSV | yes, with no documents | empty file | `Ok` with zero counts |
| valid CSV and output | yes | JSONL equals pure API chunks | `Ok` with observations |
| unavailable output parent | yes | output is not created | write `Err` |

The write failure occurs after core work because output feasibility is discovered
when the writer opens the target. The module makes that order explicit; it does
not claim transactional or atomic output.

## Expected failures and broken invariants are different

Module 02 uses `Err(str)` for expected edge failures. It does not convert every
exception into an ordinary result.

| Situation | Treatment in this state | Reason |
| --- | --- | --- |
| file missing, unreadable, or malformed | `Err("Load failed: ...")` | caller can reasonably handle it |
| output cannot be opened or written | `Err("Write failed: ...")` | caller can choose another destination |
| untyped chunk size is `True`, zero, or negative | configuration `Err` | reject boundary data before construction |
| unknown cleaning rule from CLI | configuration `Err` | reject policy before dependency lookup |
| internally produced impossible chunk offsets | exception | signals a violated program invariant |
| interruption or memory exhaustion | not normalized | not an ordinary domain outcome |

`RagEnv` is still allowed to defend its own invariant. The boundary parser must
check untyped values first so routine user error does not reach that constructor as
an exception.

Module 04 introduces richer failure modelling. Do not read a typed error taxonomy,
retry strategy, or recovery policy into this minimal `Result`.

## What the two proof styles establish

The injected-reader test proves control flow: reader failure is returned unchanged
and later work is skipped. It cannot prove that `open`, `csv.DictReader`, or
`json.dump` are wired correctly.

The real-filesystem tests prove adapter behavior using temporary paths:

- valid input matches `full_rag_api_docs` after JSON serialization;
- the source file remains unchanged;
- empty, malformed, missing, and unwritable routes have distinct outcomes;
- no output exists after a load failure.

Run both proof owners from the repository root:

```bash
make PROGRAM=python-programming/python-functional-programming \
  capstone-data-api-proof
make PROGRAM=python-programming/python-functional-programming \
  capstone-data-shell-proof
```

The first route executes
`test_module_02_data_first_apis.py`; the second executes
`test_module_02_filesystem_boundary.py`. A passing fake-boundary test is not a
substitute for the second route.

## Review the boundary without guessing

For any proposed change, trace these questions in order:

1. Does the function accept paths or already-validated domain values?
2. Which exact capability or adapter owns the effect?
3. Can an expected failure be returned before core work starts?
4. If core work has started, which effects may already have happened?
5. Which focused test observes the success value, failure value, and output state?
6. What stronger property is deliberately deferred?

A boundary is sealed when those answers are visible in signatures, source
ownership, and executable evidence—not merely asserted in prose.

## Limits of the Module 02 boundary

This state does not guarantee atomic replacement, cleanup of a partially written
file, bounded-memory CSV loading, retry policy, typed error categories, async
cancellation, or resource acquisition protocols. Those omissions are real design
boundaries, not hidden accomplishments.

Continue with [Configuration as Data](configuration-as-data.md) to see how the CLI
and other untyped callers validate policy before selecting dependencies.
