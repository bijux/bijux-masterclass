# Module 05 Exercise Answers

Use these answers to review your reasoning after attempting the exercises. The
code is one defensible route, not a required transcription. A good alternative
must preserve the same application contract and produce equivalent evidence.

## 1. Trace the real stage types

The four products describe information available at successive points:

| Value | Guarantee added by its producer |
| --- | --- |
| `RawDoc` | source fields have been ingested |
| `CleanDoc` | title and abstract are normalized |
| `ChunkWithoutEmbedding` | a concrete text span is ready to embed |
| `Chunk` | the span has a 16-value embedding |

`clean_doc`, `chunk_doc`, and `embed_chunk` own the arrows. Embedding must
preserve `doc_id`, text, offsets, and metadata. The `Chunk` constructor rejects
an embedding with the wrong dimension.

A result consumer can reuse the existing sum:

```python
def describe(result: Result[Chunk, ErrInfo]) -> str:
    match result:
        case Ok(value=Chunk(doc_id=doc_id, start=start, end=end)):
            return f"ready:{doc_id}:{start}-{end}"
        case Err(error=ErrInfo(stage=stage)):
            return f"failed:{stage}"
        case other:
            assert_never(other)
```

The important modeling decision is the absence of another outcome hierarchy.
`Result` already says success or failure; `ChunkWithoutEmbedding` and `Chunk`
already say before or after embedding.

**Common wrong turn:** adding `embedding: tuple[...] | None`, `error: str |
None`, and a status Boolean to one loose record. That permits contradictory
combinations.

**What the evidence proves:** the tested stage path preserves named fields,
top-level metadata mutation is blocked, and both result alternatives are
observable.

**What it does not prove:** metadata is deeply immutable, arbitrary mappings
are valid boundary input, or every real embedding provider succeeds.

## 2. Transform and consume a result

Use plain functions because neither operation introduces failure:

```python
calls: list[str] = []

def display_text(doc: CleanDoc) -> str:
    calls.append("display")
    return " ".join(doc.abstract.split())

def count_words(text: str) -> int:
    calls.append("count")
    return len(text.split())

sequential = result_map(count_words)(result_map(display_text)(input_result))
```

The comparable composition is explicit:

```python
def display_word_count(doc: CleanDoc) -> int:
    return count_words(display_text(doc))

composed = result_map(display_word_count)(input_result)
assert sequential == composed
```

Use a fresh `calls` list for each evaluation. With `Ok`, the trace is
`["display", "count"]`. With `Err`, it is empty and the returned object should
be the original error result.

**Common wrong turn:** passing a function returning `Result` to `result_map`.
That creates a nested `Result[Result[...], ...]`; sequencing is the required
operation.

**What the evidence proves:** identity of the failure path and composition for
these pure projections.

**What it does not prove:** arbitrary callables are pure or that
floating-point/side-effecting functions remain observationally equivalent when
regrouped.

## 3. Accumulate only independent errors

The third check has the same shape as the first two:

```python
def category(raw: str) -> Validation[str, str]:
    return v_success(raw) if raw.strip() else v_failure(("category required",))

def build(title: str, abstract: str, category: str) -> RawDoc:
    return RawDoc("validation-1", title, abstract, category)

checked = v_liftA3(
    build,
    validate_title(raw_title),
    validate_abstract(raw_abstract),
    category(raw_category),
)
```

For three invalid inputs, the expected order is:

```python
VFailure(("title required", "abstract too short", "category required"))
```

That order follows the `v_liftA3` argument order and tuple concatenation. A
valid input calls `build` only after all three values exist.

In `assemble`, model agreement and dimension agreement are independent, so one
embedding can report both `EMB_MODEL_MISMATCH` and `EMB_DIM_MISMATCH`.
Construction depends on the checks and therefore happens only on success.

A genuinely dependent pair is “parse `expected_dim` as an integer, then check
that it is positive.” The positivity check cannot run on an unparsed string.

**Common wrong turn:** calling all validation “applicative” even when later
checks require earlier outputs.

**What the evidence proves:** deterministic accumulation for the declared
independent checks and construction only from successful values.

**What it does not prove:** every domain invariant is independent or already
known.

## 4. Audit a metric monoid

One defensible local extension is:

```python
@dataclass(frozen=True)
class ReviewMetrics:
    processed: int = 0
    succeeded: int = 0
    rejected: int = 0
    latency_sum_ms: float = 0.0
    latency_max_ms: float = 0.0

def combine(left: ReviewMetrics, right: ReviewMetrics) -> ReviewMetrics:
    return ReviewMetrics(
        processed=left.processed + right.processed,
        succeeded=left.succeeded + right.succeeded,
        rejected=left.rejected + right.rejected,
        latency_sum_ms=left.latency_sum_ms + right.latency_sum_ms,
        latency_max_ms=max(left.latency_max_ms, right.latency_max_ms),
    )
```

`ReviewMetrics()` is an identity only under the stated non-negative-latency
domain. If negative latency were legal, `max(0.0, negative)` would change the
value.

Associativity permits:

```python
combine(combine(a, b), c) == combine(a, combine(b, c))
```

It does not permit swapping `a` and `b` for an order-sensitive operation.
Associative list concatenation is the usual counterexample to “associative
means commutative.”

**Common wrong turn:** combine averages directly. An average cannot be
recombined correctly without carrying at least a sum and count.

**What the evidence proves:** the chosen examples satisfy the declared
identities and regrouping.

**What it does not prove:** IEEE-754 addition is exactly associative for all
floats, the input constructor rejects every invalid metric, or `tree_reduce`
executes in parallel.

## 5. Cross the validation and persistence boundaries

A complete accepted boundary value includes every field:

```python
edge = ChunkModel.model_validate(
    {
        "doc_id": "boundary-1",
        "text": "validated boundary",
        "start": 0,
        "end": 18,
        "metadata": {"source": "exercise"},
        "embedding": (0.0,) * 16,
    }
)
core = to_core_chunk(edge)

assert core.doc_id == edge.doc_id
assert core.text == edge.text
assert (core.start, core.end) == (edge.start, edge.end)
assert dict(core.metadata) == edge.metadata
assert core.embedding == edge.embedding
```

Changing `end` to `17`, using 15 embedding values, or including `NaN` must fail
before conversion.

The persistence route is separate:

```python
failure = Err(
    ErrInfo(
        code="EMBED_FAIL",
        msg="model offline",
        stage="embed",
        path=(2, 4),
    )
)
encoded = to_json(failure, enc_result())
decoded = from_json(encoded, dec_result())
assert decoded == failure
```

The payload should retain `kind`, `code`, `msg`, `stage`, and `path`. Change
the envelope's `ver` from `1` to `2`; `dec_result` should raise
`ValueError("unknown version 2")`.

**Common wrong turn:** treat successful `json.dumps(model.__dict__)` as a
versioned persistence design. It has no sum discriminator, governed schema, or
migration route.

**What the evidence proves:** the chosen accepted chunk crosses without field
loss, invalid examples are rejected, and a failure with `cause=None` and
`ctx=None` preserves its public provenance.

**What it does not prove:** the default codec preserves non-`None` `cause` or
`ctx`, unknown versions can migrate without a registered migration, or parsing
untrusted input has resource limits.

## 6. Review the focused domain lab before changing it

The two families have different jobs:

- `core.rag_types.Chunk` is the cumulative pipeline's indexed text span. It
  carries document identity, offsets, metadata, and the required 16-value
  embedding.
- `rag.domain.AssembledChunk` is the focused Module 5 assembly model. It joins
  `ChunkText`, `ChunkMetadata`, and optional `Embedding`, checks model and
  dimension agreement, normalizes tags, and supports the pure-versus-NumPy
  representation exercise.

`AssembledChunk` therefore does not replace the pipeline type. Its name makes
that scope visible and removes the earlier collision where two unrelated
classes were both imported as `Chunk`.

A defensible review decision is to keep the focused lab while keeping its
boundary explicit. It earns its place by teaching cross-field ownership and
representation equivalence. It should be removed or merged only if those
claims move into the cumulative application with a clear module delta—not
merely because two values both concern chunks.

The equivalence review must compare:

- list length and order;
- stable IDs;
- text;
- metadata;
- embedding model and dimension;
- vector values within the declared tolerance;
- corresponding failure errors.

**Common wrong turn:** measure only throughput or output length and call the
optimized representation equivalent.

**What the evidence proves:** the chosen/generated batches preserve the tested
public observables between pure and hybrid modes.

**What it does not prove:** the hybrid path is faster on production data,
every possible batch is covered, or the focused model should become the main
pipeline API.

Return to [Module 05 Exercises](exercises.md) and revise any answer that lacks
a preserved earlier contract or a limit on its evidence.
