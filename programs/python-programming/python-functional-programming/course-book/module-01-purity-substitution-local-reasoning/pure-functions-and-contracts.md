# Pure Functions and Contracts

Purity becomes useful in engineering when it is stated as a contract another person
can review:

```text
valid explicit input -> deterministic returned value, no observable effect
```

That sentence is stronger than "this function looks functional." It identifies a
domain, an output promise, and an effect promise.

## Three layers of contract

Review each pure function at three layers.

| Layer | Question | FuncPipe example |
| --- | --- | --- |
| shape | What values may cross the boundary? | `chunk_doc` accepts `CleanDoc` and `RagEnv` |
| behavior | How is the output related to the input? | chunk texts concatenate to the cleaned abstract |
| effects | What external state may be observed or changed? | `chunk_doc` performs no I/O or mutation |

Type annotations help with shape, but Python does not enforce them at runtime.
`RagEnv` therefore validates its own invariant:

```python
@dataclass(frozen=True)
class RagEnv:
    chunk_size: int

    def __post_init__(self) -> None:
        if type(self.chunk_size) is not int:
            raise ValueError("RagEnv.chunk_size must be an int")
        if self.chunk_size <= 0:
            raise ValueError("RagEnv.chunk_size must be a positive integer")
```

The exact-type check is deliberate. `True` participates in integer arithmetic in
Python, but it is not a defensible chunk-size value.

## Valid input matters

The Module 01 stages are total over their stated domain: for valid domain values they
return a value instead of selecting an effectful failure route. That does not mean
every arbitrary Python object is accepted.

```python
RagEnv(chunk_size=4)     # valid
RagEnv(chunk_size=0)     # ValueError: violates the positive-size invariant
RagEnv(chunk_size=True)  # ValueError: bool is not an exact int here
```

Separating construction from transformation simplifies every downstream function.
`chunk_doc` may rely on a positive exact integer because invalid `RagEnv` values
cannot be constructed normally.

Do not overstate this guarantee as "pure functions never raise." A pure function can
raise deterministically. The better design question is whether failure belongs in
domain construction, in an explicit result value, or at an effectful boundary. Later
modules introduce richer failure values.

## Read the actual stage contracts

The completed Module 01 stages live in:

```text
capstone/module-reference-states/module-01/src/funcpipe_rag/pipeline_stages.py
```

Their important contracts are:

### `clean_doc`

```python
def clean_doc(doc: RawDoc | CleanDoc) -> CleanDoc:
    ...
```

- preserves `doc_id`, `title`, and `categories`;
- strips, lower-cases, and collapses whitespace in `abstract`;
- returns a new frozen `CleanDoc`;
- accepts a `CleanDoc` so its fixed-point law is also true in the type contract.

```python
once = clean_doc(raw)
twice = clean_doc(once)
assert twice == once
```

This is idempotence, not merely determinism.

### `chunk_doc`

```python
def chunk_doc(
    doc: CleanDoc,
    env: RagEnv,
) -> list[ChunkWithoutEmbedding]:
    ...
```

- preserves the document ID;
- emits non-overlapping slices in increasing offset order;
- records inclusive `start` and exclusive `end`;
- covers the whole abstract, with a possibly shorter final slice;
- returns an empty list for an empty abstract.

For Module 01's non-overlapping policy:

```python
cleaned = clean_doc(raw)
chunks = chunk_doc(cleaned, RagEnv(chunk_size=5))

assert "".join(chunk.text for chunk in chunks) == cleaned.abstract
assert all(chunk.text == cleaned.abstract[chunk.start:chunk.end] for chunk in chunks)
```

### `embed_chunk`

```python
def embed_chunk(chunk: ChunkWithoutEmbedding) -> Chunk:
    ...
```

- copies identity, text, and offsets unchanged;
- derives a 16-element tuple from `chunk.text`;
- produces the same embedding for equal text regardless of document ID or position.

The embedding is a teaching double. It gives deterministic local behavior; it does
not claim semantic similarity.

### `structural_dedup_chunks`

```python
def structural_dedup_chunks(chunks: list[Chunk]) -> list[Chunk]:
    ...
```

- sorts by `(doc_id, start)`;
- removes repeated structural positions;
- reaches a fixed point after one call.

Its duplicate key is `(doc_id, text, start, end)`. Read that key before claiming what
"duplicate" means. Arbitrary `Chunk` values with the same structure but conflicting
embeddings are outside normal production output; the first canonical-order value is
retained.

## Contract violations that look plausible

### Hidden policy

```python
CHUNK_SIZE = 512


def hidden_chunk_doc(doc: CleanDoc) -> list[ChunkWithoutEmbedding]:
    ...
```

The shape annotation omits an input that determines output. Two identical-looking
calls can mean different things after a global assignment.

### Mutation before return

```python
def destructive_clean(doc: dict[str, str]) -> dict[str, str]:
    doc["abstract"] = " ".join(doc["abstract"].split())
    return doc
```

Even if the returned mapping has the right content, callers holding the original
reference observe an effect.

### Logging inside a transform

```python
def noisy_embed(chunk: ChunkWithoutEmbedding) -> Chunk:
    print(f"embedding {chunk.doc_id}")
    return embed_chunk(chunk)
```

The returned value remains deterministic, but replacing the call with its value
removes output. The function is not referentially transparent.

### A test that proves too little

```python
def test_chunk_count() -> None:
    assert len(chunk_doc(cleaned, env)) == 4
```

This could pass while offsets overlap, characters disappear, or slices are reordered.
A reconstruction assertion tests the behavioral relationship that matters.

## Proof strategy

Examples and properties answer different questions:

- a named example explains a specific contract to a learner;
- a property test explores that contract over many generated values;
- a boundary example demonstrates how invalid values fail.

Module 01 uses both:

```text
tests/learning/test_module_01_purity_foundations.py
tests/test_laws.py
```

Run the short proof:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/learning/test_module_01_purity_foundations.py
```

Then inspect these named properties in `tests/test_laws.py`:

- `test_clean_doc_is_idempotent`
- `test_chunk_doc_preserves_text`
- `test_embed_chunk_depends_only_on_text`
- `test_full_rag_is_canonical`

The tests establish observed behavior for the explored domain. They do not prove that
the implementation can never perform an effect; that claim also requires source and
dependency review.

## Review exercise

For one Module 01 stage, write a contract with:

1. valid input domain;
2. output shape;
3. preserved fields;
4. changed fields;
5. effect promise;
6. one invalid input route;
7. one example assertion;
8. one property that would catch a realistic regression.

Compare your contract with the source and both test surfaces. If the prose promises
more than the code or the test proves less than the prose, record the mismatch rather
than rationalizing it.

Continue with [Immutability and Value Semantics](immutability-and-value-semantics.md)
to see why these contracts are easier to preserve when values cannot be changed
behind another reference.
