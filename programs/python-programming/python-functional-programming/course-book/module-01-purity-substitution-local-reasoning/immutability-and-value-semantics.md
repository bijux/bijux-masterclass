# Immutability and Value Semantics

Purity is difficult to maintain when two parts of a program share a mutable object.
Even a function that never assigns to a global can observe changes made through
another reference.

Module 01 uses frozen dataclasses so RAG records behave as values: equality depends
on field content, and a field cannot be rebound after construction.

## The aliasing problem

```python
metadata = {"category": "cs.PL"}
first = metadata
second = metadata

first["category"] = "math.NT"
assert second["category"] == "math.NT"
```

There are two names but one dictionary. Understanding `second` requires tracking
assignments through every alias.

Compare a frozen value:

```python
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Paper:
    doc_id: str
    category: str


original = Paper("paper-1", "cs.PL")
reclassified = replace(original, category="math.NT")

assert original.category == "cs.PL"
assert reclassified.category == "math.NT"
```

The relationship is explicit: a change is represented by a new value.

## What `frozen=True` guarantees

The Module 01 types in `rag_types.py` are:

- `RawDoc`
- `CleanDoc`
- `ChunkWithoutEmbedding`
- `Chunk`
- `RagEnv`

Each is declared with `@dataclass(frozen=True)`. This provides:

- structural equality from fields;
- a generated hash when all fields are hashable;
- a runtime error when code tries to rebind a field;
- a useful signal to type checkers and reviewers.

The learning proof demonstrates the runtime boundary:

```python
from dataclasses import FrozenInstanceError

doc = RawDoc("doc-a", "title", "abstract", "cs.PL")

with pytest.raises(FrozenInstanceError):
    doc.abstract = "changed"
```

Freezing does not make Python values universally or deeply immutable.

## Shallow versus deep immutability

This dataclass is frozen but contains a mutable list:

```python
@dataclass(frozen=True)
class MisleadingBatch:
    doc_ids: list[str]


batch = MisleadingBatch(["doc-a"])
batch.doc_ids.append("doc-b")  # allowed
```

The field cannot be rebound, but the referenced list can change.

Module 01's record fields are immutable scalars or tuples:

```python
@dataclass(frozen=True, eq=True)
class Chunk(ChunkWithoutEmbedding):
    embedding: tuple[float, ...]
```

This makes an individual `Chunk` safe to hash. The pipeline still returns
`list[Chunk]`. That list is a mutable **container of immutable values**.

```python
chunks = chunk_doc(cleaned, env)
chunks.append(other_chunk)  # the local list may change
chunks[0].text = "changed"  # the element may not change
```

Do not claim that `chunk_doc` returns a tuple; the tracked Module 01 reference state
returns a list. The contract is that the function creates a fresh list and does not
mutate its inputs. Callers own the returned container.

## Value transitions in FuncPipe

The types record which semantic transition has occurred:

```text
RawDoc
  | clean_doc: normalize abstract
  v
CleanDoc
  | chunk_doc: attach text offsets
  v
ChunkWithoutEmbedding
  | embed_chunk: derive deterministic vector
  v
Chunk
```

Returning a different type is not ceremony here. It prevents a reviewer from
mistaking raw text for normalized text or an unembedded slice for final output.

Inspect `clean_doc`:

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

The input is preserved. The output changes only the field named by the contract.
That makes a regression assertion precise:

```python
before = raw
after = clean_doc(raw)

assert raw == before
assert after.doc_id == raw.doc_id
assert after.title == raw.title
assert after.categories == raw.categories
```

## Configuration is also a value

`RagEnv` is frozen because chunk policy affects output:

```python
small = RagEnv(chunk_size=4)
large = RagEnv(chunk_size=8)

assert small != large
```

The configuration can be passed, compared, and captured without depending on an
ambient variable. Its constructor also prevents invalid values from entering pure
stages. Immutability without validation would only make an invalid value permanently
invalid.

## Hashing and deduplication

Hashability is useful only when equality represents the intended identity. `Chunk`
equality includes inherited fields and the embedding tuple. Module 01's
`structural_dedup_chunks` intentionally uses a narrower key:

```python
key = (chunk.doc_id, chunk.text, chunk.start, chunk.end)
```

That is a domain decision, not a consequence of `frozen=True`. Review these concepts
separately:

- dataclass equality answers whether every modeled field is equal;
- hashing supports equality-based collections;
- structural deduplication defines which fields identify a repeated RAG slice;
- canonical ordering defines how retained values are arranged.

A common mistake is to use `set(chunks)` and accidentally let implementation-level
equality define domain deduplication and output order.

## Cost and judgment

Immutable value flow can allocate more objects than an in-place algorithm. It is
usually worth the cost for control data, domain records, configuration, and pipeline
boundaries. It may be the wrong internal representation for a measured numeric hot
loop.

A defensible compromise is:

```text
immutable public input -> contained mutable implementation -> immutable public output
```

The mutation must not escape through aliases, and benchmarks—not habit—should justify
the extra complexity.

## Proof route

From the course root:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/learning/test_module_01_purity_foundations.py
```

Review `test_frozen_inputs_cannot_be_changed_in_place` and
`test_pure_core_preserves_inputs_and_canonicalizes_output`. One tests the value
boundary; the other tests that the composed transforms respect it.

The tests do not prove deep immutability for arbitrary future fields. If a list,
mapping, or mutable object is added to a frozen type, the contract must be reviewed
again.

## Learner work

Audit every field in `rag_types.py`:

1. classify it as immutable, mutable, or conditionally safe;
2. state what dataclass equality means for the containing type;
3. identify whether the type is hashable and whether it should be;
4. explain why `structural_dedup_chunks` uses its explicit key;
5. write one test that would fail if a stage mutated an input.

Acceptance evidence is the field audit, your focused test, and the unchanged Module
01 learning proof.

Continue with [Higher-Order Composition](higher-order-composition.md), which composes
these value transitions without hiding their domain order.
