# Imperative vs Functional

Module 01 begins with a review question, not a syntax preference:

> How much of this function can you understand from its arguments and return value?

Imperative Python often describes **how state changes**. Functional Python emphasizes
**how values are transformed**. Both styles can be clear. The important difference
is whether hidden state forces a reviewer to search outside the expression at hand.

## What you need

You should already be comfortable with functions, loops, comprehensions, type
annotations, and dataclasses. This lesson introduces no third-party framework.

Keep the Module 01 reference state open:

```text
capstone/module-reference-states/module-01/src/funcpipe_rag/
```

The corresponding short proof is:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/learning/test_module_01_purity_foundations.py
```

Run that command from the `python-functional-programming` directory.

## One behavior, two descriptions

Suppose a RAG ingestion step must normalize an abstract.

```python
def normalize_in_place(rows: list[dict[str, str]]) -> None:
    for row in rows:
        row["abstract"] = " ".join(row["abstract"].strip().lower().split())
```

The call returns `None`. Its useful result is a mutation of objects owned by the
caller. To review a later expression involving `rows`, you must know whether this
function has already run and who else holds references to the same dictionaries.

Now make the transformation explicit:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class RawDoc:
    doc_id: str
    abstract: str


@dataclass(frozen=True)
class CleanDoc:
    doc_id: str
    abstract: str


def clean_doc(doc: RawDoc) -> CleanDoc:
    return CleanDoc(
        doc_id=doc.doc_id,
        abstract=" ".join(doc.abstract.strip().lower().split()),
    )
```

For a fixed `RawDoc`, the result is fixed. The input remains available for comparison,
and the type transition records that normalization occurred.

```python
raw = RawDoc("doc-a", "  Pure   Values ")

assert clean_doc(raw) == CleanDoc("doc-a", "pure values")
assert raw.abstract == "  Pure   Values "
```

That is the practical value of local reasoning: the function body and explicit input
are enough to predict the returned value.

## Substitution is the test

A deterministic function is not automatically pure. Purity requires both:

- the returned value depends only on explicit inputs; and
- evaluation produces no observable effect.

If `clean_doc(raw)` is pure, replacing the call with its value preserves program
meaning:

```python
cleaned = clean_doc(raw)
```

can become:

```python
cleaned = CleanDoc("doc-a", "pure values")
```

for that specific `raw`. This is **referential transparency**.

The following function is deterministic in what it returns but is not pure:

```python
audit: list[str] = []


def clean_and_record(doc: RawDoc) -> CleanDoc:
    audit.append(doc.doc_id)
    return clean_doc(doc)
```

Replacing the call with the returned `CleanDoc` removes an audit entry. Program
meaning changes, so substitution is unsafe.

## The first FuncPipe state

Module 01 establishes this pure dataflow:

```text
RawDoc
  -> clean_doc
CleanDoc
  -> chunk_doc with RagEnv
list[ChunkWithoutEmbedding]
  -> embed_chunk
list[Chunk]
  -> structural_dedup_chunks
canonical list[Chunk]
```

The code is split by responsibility:

| File | Review responsibility |
| --- | --- |
| `rag_types.py` | frozen domain values and valid chunk configuration |
| `pipeline_stages.py` | deterministic value transformations |
| `full_rag.py` | stage ordering and legacy comparison |
| `rag_shell.py` | CSV input and JSONL output |
| `tests/test_laws.py` | property-based laws over many generated values |
| `tests/learning/test_module_01_purity_foundations.py` | short learner-facing proof |

`full_rag.py` deliberately keeps `impure_chunks` beside `docs_to_embedded`. Compare
their ownership:

```python
def impure_chunks(docs: list[RawDoc], env: RagEnv) -> list[LegacyChunkMetadata]:
    result: list[LegacyChunkMetadata] = []
    for doc in docs:
        # normalize, split, construct dictionaries, and mutate result here
        ...
    return result
```

The pure orchestration names the same transformations:

```python
def docs_to_embedded(docs: list[RawDoc], env: RagEnv) -> list[Chunk]:
    cleaned = [clean_doc(doc) for doc in docs]
    chunked = [chunk for doc in cleaned for chunk in chunk_doc(doc, env)]
    embedded = [embed_chunk(chunk) for chunk in chunked]
    return embedded
```

The second form does not win because comprehensions are inherently functional. It
wins because each named stage has a smaller contract and can be substituted or tested
without reconstructing the whole loop.

## Trace one document

Given:

```python
doc = RawDoc(
    doc_id="paper-1",
    title="Local Reasoning",
    abstract="  Pure   Python  ",
    categories="cs.PL",
)
env = RagEnv(chunk_size=5)
```

the observable value transitions are:

| Expression | Relevant result |
| --- | --- |
| `clean_doc(doc)` | abstract `"pure python"` |
| `chunk_doc(clean_doc(doc), env)` | texts `["pure ", "pytho", "n"]` |
| `embed_chunk(first_chunk)` | a deterministic 16-number tuple |
| `full_rag([doc], env)` | canonical chunks ordered by document ID and offset |

The SHA-256-based embedding is not a semantic embedding model. It is a deterministic
local stand-in that lets the course teach dataflow without network access or model
variability.

## Where effects belong

File access cannot be pure: reading depends on external state, and writing changes
external state. FuncPipe gives those operations to `rag_shell`:

```text
read CSV -> full_rag(docs, env) -> write JSONL
  effect          pure core          effect
```

Do not call the whole program pure. Say precisely that `full_rag` is pure for valid
domain inputs and `rag_shell` is the effectful owner.

## Failure route: hidden configuration

This version looks convenient:

```python
CHUNK_SIZE = 512


def chunk_doc(doc: CleanDoc) -> list[ChunkWithoutEmbedding]:
    ...
```

Its output depends on a global that is absent from the signature. A test that changes
`CHUNK_SIZE` can affect later tests. The reference state instead requires
`RagEnv(chunk_size=...)`, so configuration participates in equality and substitution.

Python adds a boundary trap: `bool` is a subclass of `int`. Module 01's `RagEnv`
rejects `True` even though `isinstance(True, int)` is true. A chunk size is an exact
positive integer domain value, not merely something accepted by numeric operators.

## Review checklist

For any helper, ask:

1. Are all value-determining inputs visible in the parameters?
2. Does the function mutate an input or reachable shared object?
3. Does it read time, randomness, environment, files, or process state?
4. Does it write, log, cache, or otherwise change observable state?
5. Can the call be replaced by its returned value without changing behavior?
6. Does a focused test prove the claim, including the important failure route?

Do not classify by surface syntax. A comprehension can call an impure function; a
loop can build and return a fresh value without touching shared state.

## Learner work

Open `pipeline_stages.py` in the Module 01 reference state. For `clean_doc`,
`chunk_doc`, and `embed_chunk`, write down:

- explicit inputs;
- returned value;
- invariant preserved;
- one hidden dependency that would break substitution;
- the named test that demonstrates the current contract.

Then inspect `rag_shell.py` and mark the exact lines where the program crosses into
and out of the pure core. Your evidence is a short call graph plus the passing Module
01 learning proof—not a rewritten pipeline.

Continue with [Pure Functions & Contracts](pure-functions-and-contracts.md), where
these judgments become reviewable input, output, and invariant contracts.
