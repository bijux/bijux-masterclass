# Idempotent Transforms

A function is idempotent when applying it again does not change the result:

```text
f(f(x)) == f(x)
```

Idempotence is useful when work may be repeated after a retry, during a rebuild, or
by a defensive caller. It does not mean the first call does nothing. It means the
first call reaches a fixed point.

Module 01 has two distinct fixed-point claims:

- cleaning a cleaned document does not change it;
- structurally deduplicating canonical output does not change it.

The whole `full_rag` function is not called on its own output because its input and
output types differ.

## Cleaning reaches a fixed point

`clean_doc` normalizes an abstract with:

```python
" ".join(doc.abstract.strip().lower().split())
```

After one application:

- leading and trailing whitespace is gone;
- each internal whitespace run is one ordinary space;
- letters are lower-case.

Repeating those operations produces the same string.

```python
once = clean_doc(raw_doc)
twice = clean_doc(once)

assert twice == once
```

The signature accepts `RawDoc | CleanDoc`, so the law is valid in both runtime and
static contracts.

### A deterministic transform that is not idempotent

```python
def append_marker(text: str) -> str:
    return text + "!"


assert append_marker("pure") == "pure!"
assert append_marker(append_marker("pure")) == "pure!!"
```

Determinism gives the same output for the same input. Idempotence adds a fixed-point
relationship between output and repeated input.

## Structural deduplication reaches a fixed point

`structural_dedup_chunks`:

1. sorts chunks by `(doc_id, start)`;
2. tracks `(doc_id, text, start, end)` keys;
3. retains the first unseen structural key.

After one call, output is ordered and has no duplicate structural keys. A second call
has nothing left to change:

```python
once = structural_dedup_chunks(chunks)
twice = structural_dedup_chunks(once)

assert twice == once
```

The property suite tests this over generated chunk lists.

## Canonicalization is stronger than duplicate removal

This function removes duplicates while preserving encounter order:

```python
def preserve_first(values: list[int]) -> list[int]:
    return list(dict.fromkeys(values))
```

It is idempotent, but two permutations can produce different results:

```python
preserve_first([2, 1]) != preserve_first([1, 2])
```

Module 01's structural deduplication also sorts, so output depends on the retained
structural values rather than their input order. That canonical form supports:

```python
full_rag(docs, env) == full_rag(list(reversed(docs)), env)
```

when document IDs are unique.

Do not collapse these concepts:

| Property | Question |
| --- | --- |
| deterministic | does the same input give the same output? |
| idempotent | does repeated application stop changing output? |
| deduplicating | are repeated domain keys removed? |
| canonical | do equivalent inputs choose one stable representation? |

## The completed-output law

`full_rag` has this type:

```text
list[RawDoc] × RagEnv -> list[Chunk]
```

Therefore this expression is invalid:

```python
full_rag(full_rag(docs, env), env)
```

The output is `list[Chunk]`, not `list[RawDoc]`.

The actual law is:

```python
completed = full_rag(docs, env)
assert structural_dedup_chunks(completed) == completed
```

This states that `full_rag` returns output already at the deduplication fixed point.
Precise types prevent an attractive but meaningless algebraic slogan.

## Failure routes

### Unstable ordering

```python
def flip_order(values: list[int]) -> list[int]:
    return list(reversed(values))
```

Repeated application oscillates unless the input is symmetric. A retry can alternate
output instead of settling.

### Normalization that keeps adding information

Appending timestamps, counters, or provenance inside a normalizer prevents a fixed
point and introduces effects.

### A key that omits meaningful identity

Structural deduplication intentionally ignores embedding in its key because
production embeddings are deterministic from text. If embeddings later become
model-dependent, the key decision must be revisited; idempotence alone cannot say
which value is correct.

### Equality without resource equivalence

Calling an idempotent effectful API twice may return the same value while doubling
logs, requests, cost, or latency. Value idempotence does not automatically make
effects safe to repeat.

## Proof route

Run:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/learning/test_module_01_purity_foundations.py \
  capstone/module-reference-states/module-01/tests/test_laws.py
```

Inspect:

- `test_clean_doc_is_idempotent`;
- `test_structural_dedup_is_idempotent`;
- `test_structural_dedup_produces_canonical_order`;
- `test_structural_dedup_no_duplicates`;
- `test_full_rag_reaches_fixed_point_in_one_pass`.

Each name should describe the operation to which the law actually applies.

## Learner work

Construct three `Chunk` values:

- two with the same structural key;
- one with a different offset.

Predict the exact canonical output before running the code. Then:

1. assert the duplicate is removed;
2. assert output order;
3. assert a second deduplication is equal;
4. reverse the input and assert the same canonical output;
5. explain why this does not establish semantic embedding quality;
6. explain what would change if embedding became part of domain identity.

Use the existing deterministic `embed_chunk` to create valid chunks. Preserve the
Module 01 learning proof.

Continue with [Module 01 Refactoring Guide](refactoring-guide.md) to review the full
application state before the cumulative exercises.
