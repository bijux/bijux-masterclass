# Module 02 FuncPipe Delta: Move Policy into Values

Module 01 established a deterministic value transformation:

```text
RawDoc -> CleanDoc -> ChunkWithoutEmbedding -> Chunk -> deduplicated Chunk
```

Its CSV-to-JSONL shell deliberately allowed filesystem exceptions to escape.
Module 02 preserves the successful transformation while adding immutable policy,
expression-oriented composition, and `Result`-bearing boundaries.

## Why the Module 01 shape is no longer enough

The first state has one built-in cleaning order and one directly threaded pipeline.
That is sufficient to prove purity, but awkward for callers that need to:

- choose cleaning rules and chunk size without rewriting orchestration;
- inspect filtering policy before running it;
- substitute a deterministic reader, cleaner, embedder, or observation tap;
- handle expected input and output failures without catching exceptions around the
  pure core.

The new concept is **data-first API design**. Stable policy becomes frozen data,
small functions interpret that data, and concrete effects remain in the shell.

## Source delta

| Responsibility | Module 02 source | Capability added |
| --- | --- | --- |
| run policy | `api/config.py`, `api/clean_cfg.py` | frozen configuration can be captured, compared, and validated |
| expression flow | `fp.py`, `api/core.py` | `pipe`, `fmap`, `ffilter`, and `flatmap` expose stage order |
| predicate policy | `core/rules_pred.py` | filtering rules are inspectable data interpreted by `eval_pred` |
| function rules | `core/rules_dsl.py` | closures bind policy into `RawDoc -> bool` functions |
| guarded text rules | `core/rules_lint.py` | an AST whitelist limits the accepted expression language |
| boundary outcomes | `result.py`, `shells/` | expected read, parse, configuration, and write failures become `Err` |
| stable API return | `api/types.py`, `api/core.py` | callers receive chunks together with observations |

The API layer still delegates cleaning, chunking, embedding, and canonical
deduplication to the domain stages introduced in Module 01.

## Executable laws

Two focused proof files divide the claims by ownership.

`test_module_02_data_first_apis.py` proves 15 cases:

- expression composition matches direct threading;
- iterator combinators are lazy and retain stage order;
- cleaning order is immutable, observable policy;
- configurators capture policy without capturing input;
- predicate and function rule forms preserve their respective semantics;
- untyped configuration rejects booleans, nonpositive sizes, and unknown rules
  before constructing `RagConfig`;
- taps observe values without changing them;
- injected reader failure short-circuits the pure core;
- default Module 02 chunks equal the Module 01 value pipeline.

`test_module_02_filesystem_boundary.py` proves six concrete adapter cases:

- valid CSV produces the same chunks and observations as `full_rag_api_docs`;
- a header-only CSV produces a successful empty JSONL file;
- malformed CSV and a missing input return load `Err` values before output exists;
- an unavailable output parent returns a write `Err`;
- the CLI rejects an unknown cleaning rule before execution.

Run the published routes from the repository root:

```bash
make PROGRAM=python-programming/python-functional-programming \
  capstone-data-api-proof
make PROGRAM=python-programming/python-functional-programming \
  capstone-data-shell-proof
```

## Boundary decision order

`boundary_rag_config` owns validation of untyped policy:

1. reject values that are not integers and reject `bool` explicitly;
2. reject zero and negative chunk sizes;
3. require cleaning rules to be a list or tuple of strings;
4. reject rule names absent from the cleaning registry;
5. only then construct `RagEnv`, `CleanConfig`, and `RagConfig`.

Python makes the first distinction essential:

```python
isinstance(True, int)  # True
```

The CLI boundary delegates to this same parser. It must not construct a
`CleanConfig` independently, because doing so would allow an unknown name to reach
dependency construction and fail later as an exception.

## Preserved meaning

With default policy:

- whitespace normalization and lower-casing match Module 01;
- chunk text, document IDs, offsets, ordering, and embeddings match;
- canonical deduplication remains deterministic and idempotent;
- pure stages perform no file or process I/O;
- the successful filesystem route serializes exactly the chunks returned by the
  pure API.

The new `Result` contract changes only how expected boundary failure is represented.
It does not turn filesystem failure into a domain value inside the core.

## Completed reference state

`capstone/module-reference-states/module-02` is the completed application state for
this module. Compare its source with Module 01:

```bash
diff -qr \
  programs/python-programming/python-functional-programming/capstone/module-reference-states/module-01/src \
  programs/python-programming/python-functional-programming/capstone/module-reference-states/module-02/src
```

The focused filesystem test belongs to the introduction state because it proves the
adapter at the point where its contract appears. The configuration and CLI
corrections are carried through Modules 03–09 and the live Module 10 capstone so
later states cannot silently weaken the public boundary law.

## Move-forward boundary

Module 02 proves synchronous configuration, expression flow, policy as data, and
explicit boundary outcomes. It does not yet prove bounded consumption of large
sources, a typed domain-error taxonomy, retry or resource policy, asynchronous
backpressure, or safe execution of arbitrary rule languages.

Move to Module 03 when you can point from each claim above to its source and focused
test, explain why the CLI shares the configuration parser, and show that the
default API still returns Module 01 values.
