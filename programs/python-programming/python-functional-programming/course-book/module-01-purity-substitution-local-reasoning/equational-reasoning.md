# Equational Reasoning

Equational reasoning means replacing an expression with an equal expression under
stated assumptions. In Python, the engineering value is modest but powerful: a
reviewer can justify a refactor with a behavior-preserving equation instead of
relying on resemblance.

The permission depends on purity. Equal returned values are not enough when
evaluation also changes observable state.

## Begin with substitution

For a fixed document:

```python
cleaned = clean_doc(raw)
```

can be replaced by the corresponding `CleanDoc` value because `clean_doc` depends
only on `raw` and performs no effect.

That substitution lets you trace a pipeline:

```python
chunks = chunk_doc(clean_doc(raw), env)
```

becomes:

```python
chunks = chunk_doc(expected_clean_doc, env)
```

for that specific input. A failure now belongs either to the expected clean value or
the chunking contract; the reasoning is local.

## State the assumptions

An equation is useful only with its preconditions.

| Equation | Required assumptions |
| --- | --- |
| `clean_doc(clean_doc(doc)) == clean_doc(doc)` | `doc` is a valid `RawDoc` or `CleanDoc` |
| `fmap(identity)(xs) == xs` | finite iterable whose materialized values compare equal |
| `fmap(g∘f)(xs) == fmap(g)(fmap(f)(xs))` | finite input; pure `f` and `g`; intermediate allocation is acceptable |
| `full_rag(docs, env) == full_rag(reversed(docs), env)` | document IDs are unique; valid environment |
| `dedup(dedup(chunks)) == dedup(chunks)` | chunks are valid values for the structural key |

Without the assumptions, the expression may be ill-typed, non-terminating, or
observably different.

## Map fusion and fission

Module 01 tests the list-map composition law:

```python
fmap(lambda value: g(f(value)))(values)
    == fmap(g)(fmap(f)(values))
```

This supports two review directions.

Fuse two traversals:

```python
lengths = fmap(lambda doc: len(clean_doc(doc).abstract))(docs)
```

Split them for a named intermediate:

```python
cleaned = fmap(clean_doc)(docs)
lengths = fmap(lambda doc: len(doc.abstract))(cleaned)
```

The returned lists agree for pure functions. The second version allocates an
intermediate list; the first can be harder to inspect. Equality of results does not
make their performance identical.

### Effectful counterexample

```python
def record(value: int) -> int:
    audit.append(value)
    return value
```

Mapping `record` in two passes can change effect order or count even when final values
match. The composition law is a refactoring permission only for pure callbacks.

## Preserve the shared legacy contract

Module 01's `full_rag.py` contains both:

- `impure_chunks`, the monolithic dictionary-producing loop;
- `docs_to_embedded`, the staged immutable pipeline.

Their representations differ, so the law test projects the common behavior:

```python
legacy = sorted(
    (chunk["doc_id"], chunk["text"], chunk["start"], chunk["end"])
    for chunk in impure_chunks(docs, env)
)
pure = sorted(
    (chunk.doc_id, chunk.text, chunk.start, chunk.end)
    for chunk in docs_to_embedded(docs, env)
)

assert legacy == pure
```

This equation proves normalization and chunk structure survived the refactor over
generated inputs. It does not prove:

- equal representation;
- equal embedding fields;
- equal output ordering before projection;
- equal mutation behavior;
- equal I/O behavior.

A precise projection avoids both underclaiming and overclaiming.

## Canonicalization permits an ordering rewrite

`full_rag` ends with `structural_dedup_chunks`, which sorts by document ID and offset.
For inputs with unique document IDs:

```python
full_rag(docs, env) == full_rag(list(reversed(docs)), env)
```

The equation allows upstream input order to change without changing final canonical
output. It does not say that `docs_to_embedded` is order-independent; that intermediate
preserves traversal order.

This distinction matters when moving work across a canonicalization boundary:

```text
docs_to_embedded: order observable
full_rag:         canonical order
```

## Invalid rewrites

### Reordering non-commuting stages

```python
chunk_doc(clean_doc(raw), env)
```

cannot become "chunk raw text, then clean each chunk" without proof. Whitespace
collapse changes offsets and may move characters across chunk boundaries.

### Dropping canonicalization

If current examples happen to arrive sorted, removing
`structural_dedup_chunks` may pass them while violating order independence and
duplicate removal.

### Calling `full_rag` on its own output

`full_rag` accepts `list[RawDoc]` and returns `list[Chunk]`. Therefore:

```python
full_rag(full_rag(docs, env), env)
```

is not the Module 01 idempotence law; it is a type error. The correct completed-output
law is:

```python
structural_dedup_chunks(full_rag(docs, env)) == full_rag(docs, env)
```

### Claiming source helpers that do not exist

The reference state has no `risky_clean_doc`, `full_rag_pure_v1`, or
`full_rag_point_free`. Counterexamples may appear in a lesson, but proof commands must
target names actually present in the tracked snapshot.

## Proof route

Run:

```bash
PYTHONPATH=capstone/module-reference-states/module-01/src \
  python -m pytest -q \
  capstone/module-reference-states/module-01/tests/test_laws.py
```

Map claims to named evidence:

| Claim | Test |
| --- | --- |
| cleaning fixed point | `test_clean_doc_is_idempotent` |
| map identity | `test_fmap_identity_law` |
| map composition | `test_fmap_composition_law` |
| legacy chunk preservation | `test_refactor_preserves_chunk_structure` |
| canonical input-order independence | `test_full_rag_is_canonical` |
| completed-output fixed point | `test_full_rag_reaches_fixed_point_in_one_pass` |

Property tests explore many generated examples; they are strong regression evidence,
not mathematical proof of every Python value or hidden effect.

## Learner work

Review this proposed rewrite:

```python
embedded = fmap(embed_chunk)([
    chunk
    for doc in fmap(clean_doc)(docs)
    for chunk in chunk_doc(doc, env)
])
```

Compare it with `docs_to_embedded`. Provide:

1. an equation for returned values;
2. assumptions required by the equation;
3. evaluation and allocation differences;
4. one effectful counterexample that invalidates the permission;
5. the existing test that gives the closest evidence;
6. a decision to accept or reject the rewrite on readability grounds.

Continue with [Idempotent Transforms](idempotent-transforms.md), which focuses on the
fixed points used by cleaning and canonical deduplication.
