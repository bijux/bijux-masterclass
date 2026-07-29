# Module 01 Exercise Answers

Use these answers to review reasoning and evidence, not only final syntax. Several
implementations are defensible when they preserve the same contracts.

## Answer 1: Trace one value through the pure core

The cleaned value is:

```python
CleanDoc(
    doc_id="paper-7",
    title="Substitution",
    abstract="pure values compose",
    categories="cs.PL",
)
```

With chunk size six, the slices are:

| Text | Start | End |
| --- | ---: | ---: |
| `"pure v"` | 0 | 6 |
| `"alues "` | 6 | 12 |
| `"compos"` | 12 | 18 |
| `"e"` | 18 | 19 |

A focused test:

```python
def test_trace_one_document() -> None:
    raw = RawDoc(
        doc_id="paper-7",
        title="Substitution",
        abstract="  Pure   values compose  ",
        categories="cs.PL",
    )
    env = RagEnv(chunk_size=6)

    cleaned = clean_doc(raw)
    chunks = chunk_doc(cleaned, env)
    embedded = [embed_chunk(chunk) for chunk in chunks]
    completed = structural_dedup_chunks(embedded)

    assert cleaned.abstract == "pure values compose"
    assert [(chunk.text, chunk.start, chunk.end) for chunk in chunks] == [
        ("pure v", 0, 6),
        ("alues ", 6, 12),
        ("compos", 12, 18),
        ("e", 18, 19),
    ]
    assert "".join(chunk.text for chunk in chunks) == cleaned.abstract
    assert all(len(chunk.embedding) == 16 for chunk in embedded)
    assert all(
        0.0 <= value <= 1.0
        for chunk in embedded
        for value in chunk.embedding
    )
    assert structural_dedup_chunks(completed) == completed
```

Every transition after constructing `raw` and `env` is pure value work. Equal text
gets equal embeddings because `embed_chunk` hashes only `chunk.text`; it copies
identity and offsets into the returned `Chunk` but does not use them to derive the
vector.

Common wrong turns:

- predicting chunks from the unnormalized abstract;
- treating `end` as inclusive;
- claiming the vector is semantically meaningful;
- calling `full_rag` on completed chunks.

The test proves this concrete trace and fixed-point output. It does not prove the laws
for all documents; the property suite supplies broader evidence.

## Answer 2: Repair a mixed transformation

Separate the pure batch transform:

```python
def clean_batch(docs: list[RawDoc]) -> list[CleanDoc]:
    return [clean_doc(doc) for doc in docs]
```

from the effectful owner:

```python
def clean_and_record_batch(
    docs: list[RawDoc],
    seen_ids: list[str],
) -> list[CleanDoc]:
    cleaned = clean_batch(docs)
    seen_ids.extend(doc.doc_id for doc in docs)
    return cleaned
```

The list parameter makes the effect target visible, but
`clean_and_record_batch` is still impure because it mutates that list. The name and
signature expose rather than erase the effect.

```python
def test_clean_batch_is_independent_of_audit_state() -> None:
    docs = [
        RawDoc("a", "A", "  PURE ", "cs.PL"),
        RawDoc("b", "B", "Values", "cs.PL"),
    ]
    before = list(docs)
    seen_ids: list[str] = []

    first = clean_batch(docs)
    second = clean_batch(docs)

    assert first == second
    assert docs == before
    assert seen_ids == []

    recorded = clean_and_record_batch(docs, seen_ids)

    assert recorded == first
    assert seen_ids == ["a", "b"]
```

The original fails substitution because replacing `normalize_batch(docs)` with its
returned list removes appends to the global `seen_ids`.

A common wrong turn is moving `seen_ids` into a closure or default parameter. That
changes where the hidden state lives, not whether it exists.

These tests demonstrate returned values, input preservation, and one explicit effect
target. They do not prove the source has no other hidden reads; source and dependency
review remain necessary.

## Answer 3: Earn a typed composition

One defensible local adapter is:

```python
from collections.abc import Callable


def chunk_count(env: RagEnv) -> Callable[[CleanDoc], int]:
    def count(doc: CleanDoc) -> int:
        return len(chunk_doc(doc, env))

    return count
```

Use it:

```python
count_chunks = RagPipe(clean_doc).then(
    chunk_count(RagEnv(chunk_size=5))
)
```

Focused evidence:

```python
def raw(abstract: str) -> RawDoc:
    return RawDoc("doc", "title", abstract, "cs.PL")


assert count_chunks(raw("")) == 0
assert count_chunks(raw("12345")) == 1
assert count_chunks(raw("123456")) == 2
```

`RagPipe(clean_doc).then(embed_chunk)` is incompatible because `.then` needs a
`Callable[[CleanDoc], C]`, while `embed_chunk` accepts
`ChunkWithoutEmbedding`.

The closure captures an immutable policy value, not input documents or mutable run
state. It is still a preview of Module 02's configurator pattern. The adapter is
useful for the exercise, but Module 01's production `docs_to_embedded` remains more
direct because the actual application needs chunks, not only their count.

The examples prove count behavior at three boundaries. They do not prove the
full-text reconstruction law; keep the existing chunk property for that.

## Answer 4: Test the effect boundary

A focused test can serialize real CSV and compare parsed output with the pure core:

```python
from dataclasses import asdict
import json

import pytest

from funcpipe_rag import RagEnv, RawDoc, full_rag, rag_shell


def json_value(value: object) -> object:
    return json.loads(json.dumps(value))


def test_rag_shell_matches_pure_core(tmp_path) -> None:
    source = tmp_path / "docs.csv"
    output = tmp_path / "chunks.jsonl"
    source.write_text(
        "doc_id,title,abstract,categories\n"
        "b,B,Local reasoning,cs.PL\n"
        "a,A,Pure values,cs.PL\n",
        encoding="utf-8",
    )
    docs = [
        RawDoc("b", "B", "Local reasoning", "cs.PL"),
        RawDoc("a", "A", "Pure values", "cs.PL"),
    ]
    env = RagEnv(chunk_size=5)

    rag_shell(env, str(source), str(output))

    actual = [
        json.loads(line)
        for line in output.read_text(encoding="utf-8").splitlines()
    ]
    expected = [json_value(asdict(chunk)) for chunk in full_rag(docs, env)]
    assert actual == expected


def test_rag_shell_writes_empty_output_for_header_only_csv(tmp_path) -> None:
    source = tmp_path / "empty.csv"
    output = tmp_path / "chunks.jsonl"
    source.write_text(
        "doc_id,title,abstract,categories\n",
        encoding="utf-8",
    )

    rag_shell(RagEnv(chunk_size=5), str(source), str(output))

    assert output.read_text(encoding="utf-8") == ""


def test_rag_shell_translates_invalid_row_shape(tmp_path) -> None:
    source = tmp_path / "invalid.csv"
    output = tmp_path / "chunks.jsonl"
    source.write_text(
        "doc_id,title,abstract\n"
        "a,A,Pure values\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=str(source)):
        rag_shell(RagEnv(chunk_size=5), str(source), str(output))


def test_rag_shell_propagates_missing_path(tmp_path) -> None:
    source = tmp_path / "missing.csv"
    output = tmp_path / "chunks.jsonl"

    with pytest.raises(FileNotFoundError):
        rag_shell(RagEnv(chunk_size=5), str(source), str(output))
```

Operation classification:

| Operation | Classification |
| --- | --- |
| `open` and `csv.DictReader` consumption | read effect |
| `RawDoc` construction | value construction at boundary |
| `full_rag` | pure transformation |
| `open`, `json.dump`, and `write` | write effect |

Common wrong turns:

- comparing JSON text formatting instead of parsed values;
- hard-coding expected embeddings rather than calling the pure core;
- expecting missing paths to be translated when the source lets
  `FileNotFoundError` propagate;
- claiming the tests prove atomic output.

The valid test proves adapter content agrees with `full_rag`. It does not prove that a
write failure leaves no partial file; direct writes provide no such guarantee.

## Answer 5: Review a false fixed-point claim

The proposal is ill-typed:

```text
full_rag: list[RawDoc] × RagEnv -> list[Chunk]
```

The inner call returns `list[Chunk]`, which the outer call cannot accept.

The correct completed-output law is:

```python
completed = full_rag(docs, env)
assert structural_dedup_chunks(completed) == completed
```

The idempotent function is `structural_dedup_chunks`:

```python
once = structural_dedup_chunks(chunks)
assert structural_dedup_chunks(once) == once
```

Canonical order independence, under unique document IDs:

```python
assert full_rag(docs, env) == full_rag(list(reversed(docs)), env)
```

A deterministic non-idempotent counterexample:

```python
def append_marker(text: str) -> str:
    return text + "!"
```

It always returns the same result for the same input, but repeated application keeps
adding markers.

Common wrong turns:

- using "idempotent" as a synonym for deterministic;
- omitting the unique-ID assumption from the reversal property;
- claiming canonicalization proves semantic embedding quality;
- proving only that one already-sorted example remains sorted.

The fixed-point assertion proves completed output needs no further structural
deduplication. The reversal assertion proves one ordering property for the given
inputs. Neither proves effect safety, resource bounds, retrieval relevance, or
correctness for every possible domain value.

## Final self-review

Your answers should preserve these earlier contracts:

- exact positive integer configuration;
- immutable domain inputs;
- deterministic normalization and embedding;
- full text coverage;
- canonical structural output;
- one explicit file-effect owner.

Run both Module 01 proof surfaces again before moving to Module 02.
