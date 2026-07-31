# Module 06 Exercise Answers

Use these answers to review decisions, not to copy one required implementation.
An alternative is defensible when it preserves the stated FuncPipe behavior,
makes context ownership clear, and supplies equivalent evidence.

## 1. Classify and compose the document flow

The dependency order is:

```python
result = (
    source
    .and_then(require_title)
    .and_then(require_abstract)
    .map(clean_doc)
    .map(lambda doc: doc.abstract)
)
```

The prerequisites use `and_then` because each returns Result. `clean_doc` and
the abstract projection use `map` because they return plain values.

A useful call table is:

| Input | Calls | Result |
| --- | --- | --- |
| missing title | `["title"]` | `Err(TITLE_REQUIRED)` |
| missing abstract | `["title", "abstract"]` | `Err(EMPTY_ABSTRACT)` |
| valid | `["title", "abstract", "clean"]` | `Ok(normalized_abstract)` |

Common wrong turns:

- `map(require_title)` creates a nested Result;
- running both prerequisites eagerly loses the declared fail-fast order;
- wrapping `clean_doc` in `Ok` makes an infallible step appear fallible;
- checking only the final error cannot prove later work was skipped.

The evidence proves ordered short-circuiting and correct operation selection
for these cases. It does not prove fail-fast behavior is the desired field
validation experience. If both missing fields must be reported,
`Validation` is the better context because the checks are independent.

Architecture connection: Result owns propagation; the prerequisite functions
own domain rules; `clean_doc` remains unchanged.

## 2. Prove one legal regrouping

A plain helper keeps the composition readable:

```python
def word_count(text: str) -> int:
    return len(text.split())
```

Compare:

```python
separate = (
    source
    .map(clean_doc)
    .map(lambda doc: doc.abstract)
    .map(word_count)
)

composed = source.map(
    lambda raw: word_count(
        clean_doc(raw).abstract
    )
)
```

Functor composition supports the rewrite because function order and the
surrounding Result are unchanged.

Common wrong turns:

- composing as `clean_doc(word_count(...))` reverses types and behavior;
- adding a call trace inside `word_count` changes the observations relevant to
  substitution;
- comparing only successful inner integers ignores the Err branch;
- using tidy examples only weakens the input domain.

The property proves equality for the generated strings and these functions. It
does not prove that whitespace normalization is the right product policy,
cover all Unicode text, or establish any speed advantage.

Architecture connection: the container law supports structural refactoring;
the RAG learning property supports the concrete cleaning projection.

## 3. Make read-only policy and changing progress explicit

Construct one Reader:

```python
program = asks(
    lambda env: list(
        iter_chunk_doc(doc, env)
    )
)
```

For abstract `"abcdefghij"` and size `4`:

```text
overlap 0 -> "abcd", "efgh", "ij"
overlap 2 -> "abcd", "cdef", "efgh", "ghij", "ij"
```

Account for the returned sequence by chaining an `account(chunk)` State
operation or by folding it. Each State run must receive the caller’s original
`Progress()` independently.

Common wrong turns:

- rebuilding the Reader for each environment does not prove one unchanged
  description accepts both policies;
- counting distinct characters instead of emitted characters changes the
  metric under overlap;
- reusing the final state from the first run as the second initial state makes
  the comparisons dependent;
- mutating a Progress object breaks the immutable-state claim.

The proof establishes explicit environment supply, deterministic chunk order,
and local progress transitions for the selected policies. It does not prove
Reader or State is necessary.

A simpler solution is:

```python
chunks = list(iter_chunk_doc(doc, env))
progress = reduce(account, chunks, Progress())
```

For one local traversal, that version is likely clearer. Reader and State earn
their cost only if the same context-bearing operations must compose elsewhere.

Architecture connection: chunk policy remains in immutable `RagEnv`; progress
is a local observation, not global application state.

## 4. Preserve parse failure, invalid value, absence, and retrieval failure

Keep parsing and validation separate:

```python
parsed = try_result(
    lambda: int(raw),
    to_parse_error,
    exc_type=ValueError,
)

valid = parsed.and_then(require_positive)
```

A defensible empty-query contract is:

```python
Err(
    ErrInfo(
        code="EMPTY_QUERY",
        msg="query must not be empty",
    )
)
```

This differs from a valid query with no match:

```python
Ok(NoneVal())
```

and failed retrieval:

```python
Err(
    ErrInfo(
        code="RETRIEVAL",
        msg="index unavailable",
    )
)
```

Common wrong turns:

- catching `Exception` converts defects into input errors;
- calling negative input a parse failure loses domain provenance;
- mapping retrieval failure to `NoneVal` hides an unavailable index;
- choosing a nested type before stating the four public meanings makes the
  container accidental;
- transposing only one direction cannot prove round-trip preservation.

The tests prove the declared cases remain distinct and the transpose helpers
preserve them. They do not prove every product should classify empty queries
as errors.

A named retrieval sum type may be clearer when these are the only legal cases
or when nested generic pattern matching obscures the workflow.

Architecture connection: adapters own exception conversion; pure validation
owns range rules; the retrieval model owns absence versus failure.

## 5. Add trace and policy without replacing the payload

Build the base callable once, then select validation:

```python
selected = toggle_validation(
    strict,
    require_abstract,
    normalize,
)
```

Wrap that selected callable with one Writer-returning function. A valid policy
is “trace every attempt,” so the policy entry is created before the selected
callable runs and the status entry follows its Result:

```text
document:config
policy:strict
status:error
```

Another defensible policy is “trace only completed normalization.” That order
would produce no entries for strict rejection. The exercise requires you to
choose and assert one, not assume wrappers commute.

Common wrong turns:

- duplicating strict and permissive normalizers creates two behavior owners;
- placing the strict flag inside `normalize` spreads policy into the domain
  function;
- evaluating `selected(doc)` once for the payload and again for the status
  duplicates normalization;
- returning the trace string as Writer’s payload discards the Result;
- printing entries destroys the pure returned-data contract.

The evidence proves call count, selected policy behavior, payload preservation,
and entry order for the tested cases. It does not prove delivery to an
operational logging system or that runtime flags are the best deployment
model.

Architecture connection: the builder owns policy selection, normalization owns
one transformation, and Writer carries review data without emitting it.

## 6. Defend the complete refactor

Add `" 8"`, `"+8"`, and `"-1"` to both parser implementations before changing
range policy. Python’s `int` accepts all three, so characterization should
preserve `Ok(8)`, `Ok(8)`, and `Ok(-1)` respectively.

For the equivalence strategy, generate valid environments dependently:

```python
@st.composite
def environments(draw):
    chunk_size = draw(
        st.integers(min_value=1, max_value=12)
    )
    overlap = draw(
        st.integers(
            min_value=0,
            max_value=chunk_size - 1,
        )
    )
    return RagEnv(
        chunk_size=chunk_size,
        overlap=overlap,
    )
```

Use the same generated environment and document on both routes. Compare the
complete embedded chunk sequence.

A defensible ledger may conclude:

| Context | Decision |
| --- | --- |
| Result | keep where a typed prerequisite already exists |
| Reader | reject for one local `RagEnv` argument; ordinary parameter is clearer |
| State | reject for a final-only aggregate; use a fold |
| Writer | keep only if several steps compose ordered trace data |
| policy wrapper | keep because strict/permissive modes share one normalizer and call-count evidence |

Common wrong turns:

- generating invalid overlap tests constructor rejection rather than route
  equivalence;
- comparing only chunk counts misses offsets, order, text, and embeddings;
- changing parser range behavior during the structural rewrite mixes two
  intents;
- keeping every context because it exists in the module turns teaching APIs
  into application requirements;
- claiming equal outputs prove the new route is clearer.

The property supports preservation over the generated valid environment and
text domain. The ledger supplies the separate design argument. Neither proves
boundary I/O or resource behavior, which Module 07 addresses.

Architecture connection: the refactor changes control structure while
preserving the cumulative FuncPipe application, and it rejects abstractions
that do not improve ownership.
