# Error-Typed Flows: Classify Failures at Their Boundary

`Result` makes an expected failure visible in a function signature. It should
not become a container for every exception the program can raise.

Module 06 draws a practical boundary:

- an expected, recoverable case becomes a typed value;
- an unexpected defect or broken invariant remains an exception; and
- conversion happens where throwing behavior enters the application.

This is a design decision about ownership. It is not a claim that exceptions
are bad or that all domain errors are recoverable.

## Start with one configuration boundary

Python’s `int` raises `ValueError` for non-numeric text:

```python
int("eight")
```

For a text-based configuration adapter, that is an expected input failure. The
caller can correct the value, so the adapter converts it into `ErrInfo`:

```python
def parse_chunk_size(raw: str) -> Result[int, ErrInfo]:
    return try_result(
        lambda: int(raw),
        lambda error: ErrInfo(
            code="CONFIG_PARSE",
            msg=str(error),
        ),
        exc_type=ValueError,
    )
```

The exception class is part of the contract. A `RuntimeError` raised by a
broken parser is not classified as invalid user text and must remain visible.

Run both cases:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k exception_bridge_types_expected_config_failure_only
```

The test expects:

```python
parse_chunk_size("8") == Ok(8)
parse_chunk_size("eight") == Err(
    ErrInfo(
        code="CONFIG_PARSE",
        msg="invalid literal for int() with base 10: 'eight'",
    )
)
```

It also uses `pytest.raises` to prove an unrelated `RuntimeError` is not
swallowed.

## Separate parsing from domain validation

Parsing answers:

> Can this text be interpreted as an integer?

Domain validation answers:

> Is this integer an allowed chunk size?

Keep those decisions separate:

```python
def require_positive(
    value: int,
) -> Result[int, ErrInfo]:
    if value <= 0:
        return Err(
            ErrInfo(
                code="CHUNK_SIZE",
                msg="must be positive",
            )
        )
    return Ok(value)


chunk_size = parse_chunk_size(raw).and_then(
    require_positive
)
```

Now the failure codes retain provenance:

```text
"eight" -> CONFIG_PARSE
"-2"    -> CHUNK_SIZE
"8"     -> Ok(8)
```

Do not catch the constructor exception and label every failure
`CONFIG_PARSE`; the caller loses whether the text was malformed or the value
was outside the domain.

## A classification test

Before converting an exception, ask:

1. Which exact operation can raise it?
2. Which exact exception classes are expected?
3. Can the caller take a meaningful recovery action?
4. Is the case stable enough to be part of the public contract?
5. Would catching it hide a programming defect or broken invariant?

If the answers are vague, do not widen the catch.

Examples:

| Situation | Representation | Reason |
| --- | --- | --- |
| `int(raw)` rejects user-supplied text | `Err(CONFIG_PARSE)` | expected input problem |
| validated overlap is not smaller than chunk size | `Err(OVERLAP_RANGE)` | domain rule, no exception needed |
| a required dictionary key is absent because an internal invariant broke | `KeyError` remains visible | likely defect, not caller recovery |
| a valid query finds no document | `Ok(NoneVal())` | successful absence |
| retrieval storage is unavailable | `Err(RETRIEVAL)` | operation failed |

The final two rows prepare the container-layering lesson.

## Read the exception bridge

The Module 06 adapter is deliberately small:

```python
def try_result(
    thunk: Callable[[], T],
    map_exc: Callable[[Exception], E],
    exc_type: ExcTypes = Exception,
) -> Result[T, E]:
    try:
        return Ok(thunk())
    except exc_type as error:
        return Err(map_exc(error))
```

At a call site, always inspect `exc_type`. The default is broad enough for a
general helper, but application adapters should normally pass the narrow,
expected class explicitly as the learning proof does.

`result_map_try` applies the same boundary conversion to the successful value
inside an existing Result. `v_try` and `v_map_try` return one `VFailure` for one
throwing operation. Accumulation occurs only when multiple Validation values
are later combined applicatively.

## The bridge must stay narrow in space and time

Catch around the smallest throwing expression:

```python
try_result(
    lambda: int(raw),
    to_parse_error,
    exc_type=ValueError,
)
```

Avoid:

```python
try_result(
    lambda: parse_validate_build_and_store(raw),
    to_parse_error,
    exc_type=ValueError,
)
```

The larger thunk gives every `ValueError` in parsing, validation, construction,
and storage the same meaning. A bug from a distant operation can be
misclassified as user input.

After the throwing boundary returns a typed value, continue with pure
`map`/`and_then` operations.

## Typed errors require consumption

Returning `ErrInfo` is only useful if an outer boundary handles the variants:

```python
match parse_chunk_size(raw):
    case Ok(value):
        use_chunk_size(value)
    case Err(error):
        render_config_error(error)
```

The boundary may print a message, choose an exit status, or return an HTTP
response. Those effects do not belong inside the pure parser.

Typed errors can still be poorly designed. Review:

- stable, specific codes;
- messages appropriate for the boundary;
- retained source or field context;
- whether callers can distinguish recovery actions; and
- whether sensitive implementation details leak.

## `Result` does not make a function total

This annotation:

```python
def f(raw: str) -> Result[int, ErrInfo]:
    ...
```

does not prevent `f` from raising `RuntimeError`, exhausting memory, or calling
an impure dependency. It documents the expected modeled outcomes. Tests should
cover both the typed failure and important exceptions that must propagate.

The Module 06 proof is honest about this boundary: it proves total behavior
only for the named `ValueError` route.

## Common wrong turns

- **Catching `Exception` at every layer.** This converts unrelated defects into
  misleading domain failures.
- **Using one error code for all failures.** The caller cannot choose a
  recovery action.
- **Raising for routine domain invalidity after parsing.** A pure check can
  return `Err` directly.
- **Putting try wrappers in the domain core.** Conversion belongs at the
  throwing adapter.
- **Assuming Validation automatically accumulates exceptions.** Each bridge
  creates one value; applicative combination performs accumulation.
- **Ignoring successful absence.** “No match” is not the same as failed
  retrieval.

## What the focused proof establishes

The learning test establishes that the configuration adapter:

- parses valid numeric text;
- maps `ValueError` to the declared `ErrInfo`;
- preserves the exact error code and message; and
- lets an unexpected `RuntimeError` propagate.

It does not prove that all `ValueError` instances in FuncPipe are expected, or
that every boundary should use the same error mapping.

Continue with [Layered Containers](layered-containers.md) to make absence and
failure coexist without collapsing their meanings.
