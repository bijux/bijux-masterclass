# Module 02 FuncPipe Delta: Move Policy into Values

Module 01 established a deterministic RAG transformation: normalize documents,
split them into chunks, derive local embeddings, and remove structural duplicates.
Its laws describe the values produced. Module 02 preserves those values while making
policy, composition, observation, and boundary failure explicit.

## Previous capability

The Module 01 core can be reasoned about by substitution:

```text
RawDoc -> CleanDoc -> list[ChunkWithoutEmbedding] -> list[Chunk] -> list[Chunk]
```

The application works, but changing chunk size, cleaning order, filtering, tracing,
or input source requires changing orchestration code or passing loosely related
arguments through it.

## New design pressure

One RAG transformation must support different callers:

- a caller chooses cleaning rules and chunk size;
- a review route inspects filtering policy without executing it;
- a test substitutes a deterministic cleaner, embedder, reader, or observation tap;
- a file boundary reports failure as data instead of terminating the pure core;
- composition remains readable enough to compare with the Module 01 baseline.

The concept introduced now is **data-first API design**: represent stable policy as
immutable values, bind it into small functions, and keep effectful capabilities at
the edge.

## Source changes

| Responsibility | Module 02 surface | Behavior gained |
| --- | --- | --- |
| immutable run policy | `api/config.py`, `api/clean_cfg.py`, `app_config.py` | configuration can be compared, passed, and captured |
| expression flow | `fp.py`, `api/core.py` | `fmap`, `ffilter`, `flatmap`, and `pipe` expose stage order |
| inspectable predicates | `core/rules_pred.py` | filtering policy is frozen data interpreted by `eval_pred` |
| composable function rules | `core/rules_dsl.py` | closures bind domain policy into `RawDoc -> bool` |
| guarded text rules | `core/rules_lint.py` | a small AST whitelist rejects unsupported expressions |
| explicit boundary failure | `result.py`, `shells/` | readers and writers return `Ok` or `Err` |
| stable API result | `api/types.py`, `api/core.py` | callers receive chunks plus complete observations |

The module adds an API layer around the same domain stages. It does not replace
cleaning, chunking, embedding, or canonical deduplication.

## Proof and laws

The cumulative learning proof establishes:

- expression-oriented composition matches direct function calls;
- configurators create independent runs from immutable captured policy;
- cleaning rule order is observable and deterministic;
- predicate data remains inspectable and short-circuits when interpreted;
- function rules compose without accessing I/O;
- boundary parsing accepts valid untyped data and rejects invalid types as `Err`;
- injected taps observe completed stages without changing returned chunks;
- reader failure passes through without running the RAG core;
- default Module 02 output equals the Module 01 value pipeline.

From the program root:

```bash
PYTHONPATH=capstone/module-reference-states/module-02/src \
  python -m pytest -q \
  capstone/module-reference-states/module-02/tests/learning/test_module_02_data_first_apis.py
```

## Preserved behavior

With default policy:

- whitespace normalization and lower-casing match Module 01;
- chunk text, document IDs, offsets, ordering, and embeddings match;
- canonical deduplication remains deterministic and idempotent;
- pure stages still perform no file or process I/O;
- changing API shape does not change RAG meaning.

Module 02 introduces some lazy intermediate iterators so expression stages compose,
but bounded streaming is not yet the module's main contract. Module 03 makes demand
and materialization first-class.

## Reference state

`capstone/module-reference-states/module-02` is the completed application state for
this module. Compare it with Module 01:

```bash
diff -qr \
  capstone/module-reference-states/module-01/src \
  capstone/module-reference-states/module-02/src
```

Use the table above to read that structural delta; do not treat the new API, rules,
and shell directories as unrelated examples.

## Boundary rule

Untyped input must be validated before constructing domain values. In Python,
`bool` is a subclass of `int`, so an integer boundary must explicitly reject
booleans:

```python
isinstance(True, int)  # True
```

This is an API-design lesson, not a trivia question. If `True` reaches `RagEnv`, it
silently becomes a chunk size of one.

## Downstream states

Modules 03 through 09 and the live Module 10 capstone inherit Module 02's
configuration and boundary contract. A correction to that public behavior or its
learning proof must be carried through every downstream state and checked with the
history routes.

## Move-forward boundary

Module 02 proves synchronous configuration, expression flow, data predicates, and
explicit boundary outcomes. It does not yet prove:

- bounded consumption of large or infinite sources;
- typed domain error taxonomies;
- retry and resource policies;
- asynchronous backpressure;
- production-safe execution of arbitrary rule languages.

Move to Module 03 when you can distinguish a value, a policy value, a transform, a
capability, and an effectful boundary in the FuncPipe call graph—and can point to a
test proving that the new API preserves Module 01 values.
