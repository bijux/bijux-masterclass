# Local Functional Refactors

A functional refactor does not require converting an entire application. The safest
route is usually local:

1. identify one mixed responsibility;
2. extract a value transformation;
3. make its inputs explicit;
4. preserve behavior with focused evidence;
5. leave effects in the existing owner until another change earns a new boundary.

FuncPipe's Module 01 snapshot preserves its monolithic predecessor in `full_rag.py`
so you can inspect this route without inventing intermediate repositories.

## Begin with observable behavior

The legacy `impure_chunks` loop does three important things:

- normalizes each abstract;
- partitions normalized text by `env.chunk_size`;
- records document ID, text, start, and end.

Before changing shape, state what must remain equal:

```text
(doc_id, text, start, end)
```

The pure pipeline adds an immutable `Chunk` representation and deterministic
embedding, so comparing whole values with legacy dictionaries would be dishonest.
The property test compares the shared structural contract instead.

## Extract normalization

Inside a long loop, normalization is easy to duplicate:

```python
text = " ".join(doc.abstract.strip().lower().split())
```

Give the transition a domain name:

```python
def clean_doc(doc: RawDoc | CleanDoc) -> CleanDoc:
    abstract = " ".join(doc.abstract.strip().lower().split())
    return CleanDoc(
        doc_id=doc.doc_id,
        title=doc.title,
        abstract=abstract,
        categories=doc.categories,
    )
```

This extraction earns several things at once:

- the returned type says normalization occurred;
- unchanged fields are visible;
- fixed-point behavior can be tested directly;
- no caller-owned object is modified.

It does **not** make file loading pure. Extraction narrows one responsibility; it
does not erase effects elsewhere.

## Extract chunk construction

The chunk loop depends on two explicit values: a cleaned document and valid
configuration.

```python
def chunk_doc(
    doc: CleanDoc,
    env: RagEnv,
) -> list[ChunkWithoutEmbedding]:
    text = doc.abstract
    return [
        ChunkWithoutEmbedding(
            doc_id=doc.doc_id,
            text=text[offset : offset + env.chunk_size],
            start=offset,
            end=offset + len(text[offset : offset + env.chunk_size]),
        )
        for offset in range(0, len(text), env.chunk_size)
    ]
```

The comprehension is not inherently safer than a loop. The improvement is that:

- the accumulator is local and returned fresh;
- `env` makes policy visible;
- each output contains offsets that can be checked against the input;
- a valid `RagEnv` prevents a zero step.

A clearer local implementation could bind the slice once rather than repeat it. Such
a change should preserve the reconstruction and offset properties; it need not wait
for a larger architectural rewrite.

## Extract deterministic embedding

Real embedding services introduce I/O, model versions, retries, and nondeterminism.
Those concerns would obscure Module 01's goal. The snapshot uses SHA-256-derived
values so `embed_chunk` remains local:

```python
first = ChunkWithoutEmbedding("a", "same text", 0, 9)
second = ChunkWithoutEmbedding("b", "same text", 100, 109)

assert embed_chunk(first).embedding == embed_chunk(second).embedding
```

The test double proves dataflow and substitution. It does not prove semantic
retrieval quality.

## Make orchestration readable

Once stages exist, the application can name intermediate values:

```python
def docs_to_embedded(docs: list[RawDoc], env: RagEnv) -> list[Chunk]:
    cleaned = [clean_doc(doc) for doc in docs]
    chunked = [chunk for doc in cleaned for chunk in chunk_doc(doc, env)]
    embedded = [embed_chunk(chunk) for chunk in chunked]
    return embedded
```

This explicit version is preferable to a premature generic pipeline because one
document expands into many chunks and `env` participates in the middle stage.

`full_rag` adds the collection-level invariant:

```python
def full_rag(docs: list[RawDoc], env: RagEnv) -> list[Chunk]:
    return structural_dedup_chunks(docs_to_embedded(docs, env))
```

The final call makes output canonical. It is a semantic operation, not a formatting
pass.

## Keep effects at the existing edge

`rag_shell` still owns:

```text
open CSV -> parse rows -> call full_rag -> open JSONL -> serialize chunks
```

A local refactor of normalization or chunking should not also redesign file adapters,
error models, and logging. That would make equivalence harder to establish. Later
modules change those boundaries when the course has introduced the required concepts.

## Proof at the right level

The Module 01 tests demonstrate different obligations.

### Stage behavior

```python
cleaned = clean_doc(doc)
assert clean_doc(cleaned) == cleaned

chunks = chunk_doc(cleaned, env)
assert "".join(chunk.text for chunk in chunks) == cleaned.abstract
```

### Input preservation

```python
before = list(docs)
_ = docs_to_embedded(docs, env)
assert docs == before
```

### Legacy equivalence

`test_refactor_preserves_chunk_structure` compares only:

```text
doc_id, text, start, end
```

### Canonical completion

```python
result = full_rag(docs, env)
assert structural_dedup_chunks(result) == result
```

Do not use one coarse end-to-end assertion as evidence for all four claims. A failure
should tell a learner which contract changed.

## Failure routes

### Refactor changes normalization order

Lower-casing before or after whitespace collapse happens to agree here. Other
operations may not commute. Preserve the exact output property rather than assuming
all "cleaning" sequences are interchangeable.

### Refactor loses the final short chunk

Changing a `range` boundary can make chunk counts look plausible while dropping text.
The reconstruction property catches this directly.

### Refactor replaces the domain type with dictionaries

Dictionaries may reproduce output content while discarding the type transition and
frozen-value contract. Structural equality alone is not the whole Module 01 design.

### Refactor introduces a clever abstraction

If an abstraction requires closures, partial application, lazy flattening, or typed
failure behavior not yet taught, it belongs in a later state. Preserve the learning
sequence as well as runtime output.

## A disciplined review route

For a proposed local refactor:

1. name the smallest changed responsibility;
2. list the preserved fields and behavior;
3. identify any change to evaluation order or materialization;
4. identify any newly hidden input or effect;
5. run the narrow stage test;
6. run the legacy-equivalence or canonicalization property when applicable;
7. inspect the diff for unrelated boundary changes.

Use:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/learning/test_module_01_purity_foundations.py \
  capstone/module-reference-states/module-01/tests/test_laws.py
```

## Learner work

Refactor a deliberately repeated slice expression in a local copy of `chunk_doc`:

- bind `chunk_text` once per offset;
- keep the public signature and output type;
- preserve empty-input behavior;
- preserve reconstruction and offsets;
- do not change embedding, deduplication, or shell code.

Write a focused example for a final short chunk and a property for full text
reconstruction. Explain what the tests prove and what they do not prove. Then compare
your implementation with the tracked reference state; do not edit downstream states
for this exercise.

Continue with [Small Combinator Library](small-combinator-library.md), where repeated
sequencing behavior—not domain transformations—is considered for reuse.
