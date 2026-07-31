# Refactoring `try`/`except` Without Changing the Contract

Replacing a local `try` block with `try_result` is a control-flow refactor. It
should not silently change which inputs succeed, which exception classes are
caught, or which error value the caller receives.

The safe order is:

1. characterize the existing boundary;
2. name the expected exception;
3. introduce the typed bridge;
4. compare complete public results;
5. prove unexpected exceptions still escape; and
6. remove the duplicate implementation.

The order matters. If you change validation policy and control flow together,
a failing comparison cannot tell you which decision caused the difference.

## Characterize the existing parser

The Module 06 learning proof begins with:

```python
def legacy_parse(
    raw: str,
) -> Result[int, ErrInfo]:
    try:
        return Ok(int(raw))
    except ValueError as error:
        return Err(
            ErrInfo(
                code="CONFIG_PARSE",
                msg=str(error),
            )
        )
```

Before rewriting, record representative public cases:

```python
[
    ("8", Ok(8)),
    (
        "eight",
        Err(
            ErrInfo(
                code="CONFIG_PARSE",
                msg=(
                    "invalid literal for int() "
                    "with base 10: 'eight'"
                ),
            )
        ),
    ),
]
```

Characterization is not approval. The error message may later need a
product-level redesign. For this refactor, it defines the behavior being
preserved.

## Introduce the narrow bridge

The replacement is:

```python
def refactored_parse(
    raw: str,
) -> Result[int, ErrInfo]:
    return try_result(
        lambda: int(raw),
        lambda error: ErrInfo(
            code="CONFIG_PARSE",
            msg=str(error),
        ),
        exc_type=ValueError,
    )
```

The important decisions are visible:

- the throwing expression is only `int(raw)`;
- only `ValueError` is expected;
- the same error code is produced; and
- the exception message mapping is unchanged.

Run the comparison:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k refactored_config_boundary_matches_characterized_behavior
```

The test compares each implementation with the same complete expected Result.

## Expand the input table before deleting the old path

Python’s integer parser accepts more than digit-only strings:

```text
" 8" -> 8
"+8" -> 8
"-1" -> -1
```

Add those cases while both implementations exist. If both return `Ok`, the
control-flow refactor preserves the old parsing contract.

Whether negative chunk sizes should later become `Err(CHUNK_SIZE)` is a
separate domain-validation change. Add it after the parser equivalence commit,
with its own tests and explanation.

## Compare the observation the caller actually sees

Weak comparison:

```python
assert legacy_parse(raw).is_ok() == (
    refactored_parse(raw).is_ok()
)
```

This can pass while values, error codes, or messages differ.

Strong comparison:

```python
assert legacy_parse(raw) == refactored_parse(raw)
```

For a larger RAG route, compare complete domain values:

- document identifiers;
- normalized text;
- chunk text and offsets;
- output order;
- embeddings; and
- typed error provenance.

Choose the public observation first. Internal line-by-line similarity is not
the preservation goal.

## Prove the catch did not widen

The earlier [Error-Typed Flows](error-typed-flows.md) proof supplies a function
that raises `RuntimeError`:

```python
def broken_parser() -> int:
    raise RuntimeError("parser invariant broken")
```

The bridge must not convert that exception:

```python
with pytest.raises(
    RuntimeError,
    match="parser invariant broken",
):
    try_result(
        broken_parser,
        to_config_error,
        exc_type=ValueError,
    )
```

Without this negative proof, a future edit could widen `exc_type` and hide a
defect behind `CONFIG_PARSE`.

## When a property test is warranted

A finite table is enough when the public input space is deliberately small.
For a parser accepting arbitrary text, a property can compare old and new
boundary observations:

```python
@given(raw=st.text(max_size=40))
def test_parser_equivalence(raw: str) -> None:
    assert legacy_parse(raw) == refactored_parse(raw)
```

Bound the strategy to the contract under review and be honest about what it
omits. If the old implementation depends on platform encoding, locale, or
external state, value generation alone is not sufficient.

Property-based equivalence supports a larger input domain. It does not prove
the old behavior is desirable.

## Refactor a dependent route in small boundaries

For a longer function:

```python
try:
    size = int(raw_size)
    env = RagEnv(chunk_size=size)
    return run_pipeline(env)
except ValueError as error:
    return Err(to_config_error(error))
```

Do not wrap the entire body in one `try_result`. Separate owners:

```python
parsed = try_result(
    lambda: int(raw_size),
    to_config_error,
    exc_type=ValueError,
)

validated = parsed.and_then(require_positive)
environment = validated.map(
    lambda size: RagEnv(chunk_size=size)
)
```

Now:

- the adapter owns text parsing;
- a pure function owns the positivity rule;
- a plain constructor owns the valid environment shape; and
- the outer shell owns actual pipeline execution.

Each failure points to the layer that can explain it.

## Do not refactor every `try` block into Result

Keep ordinary exceptions when:

- the caller cannot recover meaningfully;
- the failure represents a violated invariant or programming error;
- the surrounding Python API is idiomatically exception-based;
- converting the failure would erase traceback context without adding a
  useful contract; or
- the code is already at the outermost process boundary that will terminate.

Result is valuable for expected outcomes that callers should compose. It is
not a requirement to turn Python into a language without exceptions.

## Review the change in three passes

### Contract pass

- Which inputs and outputs are public?
- Are complete success and error values unchanged?
- Is ordering or evaluation count observable?

### Classification pass

- Which exception class is expected?
- Is the catching expression narrow?
- Do unexpected exceptions still propagate?

### Composition pass

- Are dependent checks under `and_then`?
- Are plain transforms under `map`?
- Are independent validation errors still accumulated where required?
- Is the new flow easier to review than the direct `try` block?

If the final answer is no, keep the direct implementation. A combinator is not
an improvement by definition.

## Common wrong turns

- changing range policy during the control-flow refactor;
- comparing only `is_ok`;
- retaining old and new implementations indefinitely;
- catching a broad expression rather than one throwing call;
- mapping unrelated exceptions to one error code;
- assuming property equivalence proves the original policy is correct; and
- replacing a clear local `try` with a less readable abstraction.

## What the focused proof establishes

The learning test proves that the direct and bridged parsers return the same
complete Results for the characterized valid and invalid inputs. The companion
exception test proves `RuntimeError` remains an exception.

It does not prove equivalence for all strings until the exercise expands the
input domain, and it does not prove the parsing policy is the best product
contract.

Continue with [Configurable Pipelines](configurable-pipelines.md), where one
stable normalization function is wrapped with policy chosen at assembly time.
