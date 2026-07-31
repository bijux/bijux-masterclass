# Module 05 Exercises

These exercises are the practical half of the module. They use the cumulative
FuncPipe reference state; they do not ask you to build another RAG application.

Work from `programs/python-programming/python-functional-programming`. Keep
this file and
`capstone/module-reference-states/module-05/tests/learning/test_module_05_data_modelling.py`
open together.

Use this focused command, replacing `SELECTOR` with the name shown in each
exercise:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=capstone/module-reference-states/module-05/src \
../../../artifacts/venv/python-programming/python-functional-programming/capstone/bin/pytest \
  -q capstone/module-reference-states/module-05/tests/learning/test_module_05_data_modelling.py \
  -k SELECTOR
```

For every exercise, first predict the result, then run the check, then explain
any difference. A passing test without a written explanation is incomplete.

## 1. Trace the real stage types

**Starting context:** read `core/rag_types.py` and `rag/stages.py`. Run:

```text
rag_product_types or rag_stage_types or result_sum_type
```

**Objective:** trace one document through:

```text
RawDoc -> CleanDoc -> ChunkWithoutEmbedding -> Chunk
```

Write down, for each arrow:

- the function responsible;
- the guarantee added;
- the fields that must remain equal;
- the constructor that can reject an invalid value.

Then implement a small `describe` function for `Result[Chunk, ErrInfo]`. It
must return the chunk span for `Ok` and the failure stage for `Err`.

**Constraints:**

- use the existing products and `Ok | Err`;
- do not add a status flag, nullable error field, `ChunkState`, or job
  lifecycle;
- match variants with keyword patterns;
- attempt one top-level metadata mutation and explain its failure.

**Acceptance evidence:**

- one successful span and one failure description;
- identity, text, offsets, and metadata preserved by embedding;
- a malformed embedding rejected;
- an explanation of why `Result` already owns the success/failure distinction.

**Earlier contract to preserve:** Module 4's cleaning, chunk order, and
structured failure values.

## 2. Transform and consume a result

**Starting context:** read `fp/functor.py` and your `describe` function. Run:

```text
result_functor
```

**Objective:** map two pure projections over `Result[CleanDoc, ErrInfo]`:
normalize the abstract for display, then count its words. Compare:

```python
result_map(count_words)(result_map(display_text)(input_result))
```

with one mapping of their explicit composition.

Use a `calls` list to observe which functions run for `Ok` and `Err`. Consume
the final result with `match`.

**Constraints:**

- do not inspect `.value` before mapping;
- the original `Err` object must pass through;
- do not use `result_try_map`; neither projection is intended to raise;
- spell composition as a function or lambda, not an invented `>>` operator.

**Acceptance evidence:**

- sequential and composed mappings compare equal;
- both projections run for `Ok`;
- neither projection runs for `Err`;
- your match handles `Ok` and `Err`, then ends in `assert_never`.

**Earlier contract to preserve:** failure provenance must not be replaced or
rewritten by a successful-value transformation.

## 3. Accumulate only independent errors

**Starting context:** read `fp/validation.py`, then inspect `rag/domain/chunk.py`.
Run:

```text
applicative_validation or domain_assembly
```

**Objective:** add a third independent check to the title and abstract example:
the category string must be non-empty. Combine the three values with
`v_liftA3` to construct `RawDoc`.

Next, draw the dependency graph for `rag.domain.assemble`: model agreement and
dimension agreement can both be reported, but construction requires their
successful evidence.

**Constraints:**

- preserve error order as title, abstract, category;
- `VFailure` must never be empty;
- do not use `Result` merely to make the checks fail fast;
- do not claim that a range check can run before its input is parsed.

**Acceptance evidence:**

- one input producing all three messages in order;
- one `VSuccess(RawDoc(...))`;
- both embedding mismatch codes from `assemble`;
- one sentence identifying a genuinely dependent validation pair.

**Earlier contract to preserve:** `Result` remains the type for dependent
pipeline work; `Validation` does not replace it.

## 4. Audit a metric monoid

**Starting context:** read `fp/monoid.py`. Run:

```text
monoid_fold
```

**Objective:** extend a local copy of the `Metrics` idea with a `rejected`
count. Define its empty value and combine function, then check:

```text
combine(empty, x) == x
combine(x, empty) == x
combine(combine(a, b), c) == combine(a, combine(b, c))
```

Use at least three chosen values. Keep summed latency and maximum latency as
different fields.

**Constraints:**

- `rejected` combines by addition;
- maximum latency combines with `max`;
- inputs use non-negative finite latency;
- do not claim arbitrary floating-point regrouping is bit-identical;
- do not claim `tree_reduce` starts parallel workers.

**Acceptance evidence:**

- an empty fold;
- left and right identity checks;
- both regroupings;
- a short explanation of associativity versus commutativity;
- the domain assumption that makes `0.0` a maximum-latency identity.

**Earlier contract to preserve:** aggregation must not reorder chunks or
reinterpret what an existing metric means.

## 5. Cross the validation and persistence boundaries

**Starting context:** read `boundaries/adapters/pydantic_edges.py` and
`boundaries/adapters/serde.py`. Run:

```text
pydantic_adapter or serialization
```

**Objective:** follow two separate boundary paths:

```text
untrusted chunk mapping -> ChunkModel -> core Chunk
Err(ErrInfo) -> result envelope -> JSON -> result envelope -> Err(ErrInfo)
```

For the chunk, account for document ID, text, offsets, metadata, and all 16
embedding values. For the failure, use non-empty `stage` and `path`, inspect
the encoded payload, and compare the decoded value.

Then change only the envelope version and predict the decoder error before
running it.

**Constraints:**

- Pydantic remains in the adapter;
- use the shipped encoder and decoder instead of `repr` or `__dict__`;
- do not claim the default `ErrInfo` codec preserves `cause` or `ctx`;
- reject wrong dimensions, non-finite values, and unknown versions.

**Acceptance evidence:**

- one complete accepted chunk conversion;
- one boundary rejection;
- the exact result envelope payload;
- successful provenance round trip;
- unknown-version rejection;
- an explanation of why validation and persistence are different boundaries.

**Earlier contract to preserve:** accepted core values do not depend on
Pydantic and failures retain their operational code, stage, and path.

## 6. Review the focused domain lab before changing it

**Starting context:** compare `core/rag_types.py` with `rag/domain/`. Run:

```text
domain_assembly or hybrid_embedding or boundary_refactor
```

**Objective:** write a review note answering:

1. Which type family is the cumulative pipeline?
2. Which type family is the focused cross-field assembly lab?
3. What does `assemble` teach that the stage products do not?
4. Which observables must the optimized batch representation preserve?
5. Why does `AssembledChunk` not replace the pipeline's indexed `Chunk`?

Do not begin with a refactor. First identify ownership and evidence. If you
propose a change, name the invalid state it removes and the exact tests that
would protect accepted behavior.

**Constraints:**

- do not introduce a third chunk model;
- do not benchmark inside the equivalence test;
- compare identity, order, text, metadata, embedding model, and vector values;
- declare numeric tolerance;
- separate correctness evidence from performance evidence.

**Acceptance evidence:** a concise review note with a keep/change decision,
the evidence supporting it, and one limit of that evidence.

**Earlier contract to preserve:** the main RAG pipeline remains understandable
as an application; the focused lab supports a concept rather than replacing
the application.

## Before reading the answers

For each exercise, you should have:

- a prediction;
- executable evidence;
- a design explanation;
- one common wrong turn you avoided;
- one statement about what your evidence does **not** prove.

Use [Exercise Answers](exercise-answers.md) as a review guide, not a source to
copy before attempting the work.
