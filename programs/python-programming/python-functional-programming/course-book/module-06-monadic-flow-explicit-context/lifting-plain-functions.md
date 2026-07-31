# Lifting Plain Functions into a Context

Most useful FuncPipe functions are ordinary Python functions. `clean_doc`
accepts a `RawDoc`; the `RagEnv` constructor accepts integers; a projection
accepts a domain value. You should not rewrite those functions merely because
their inputs happen to be inside `Result`.

*Lifting* means applying an ordinary function while preserving a surrounding
context. The important skill is not memorizing combinator names. It is reading
the dependency shape before choosing an operation.

## Four questions before choosing an operation

Given `current: Result[T, E]` and a next function, ask:

| Question | Function shape | Operation |
| --- | --- | --- |
| Does it transform one successful value without adding failure? | `T -> U` | `current.map(f)` |
| Does it transform the error while leaving success alone? | `E -> F` | `current.map_err(f)` |
| Does it perform the next dependent fallible step? | `T -> Result[U, E]` | `current.and_then(f)` |
| Does it combine independent contextual inputs? | `(T, U) -> V` over `Result[T, E]` and `Result[U, E]` | `liftA2(f, left, right)` |

The table is a reading aid, not a mandate to keep every value inside a
container. If no contextual rule is needed, call the plain function directly.

## Run the FuncPipe configuration example

`RagEnv` needs `chunk_size` and `overlap`. Once each field has been parsed,
neither value depends on the other:

```python
def make_env(chunk_size: int, overlap: int) -> RagEnv:
    return RagEnv(chunk_size=chunk_size, overlap=overlap)

chunk_size: Result[int, ErrInfo] = Ok(8)
overlap: Result[int, ErrInfo] = Ok(2)

combined = liftA2(make_env, chunk_size, overlap)

assert combined == Ok(RagEnv(chunk_size=8, overlap=2))
```

Run the success and failure cases:

```bash
cd capstone/module-reference-states/module-06
PYTHONPATH=src pytest -q tests/learning/test_module_06_explicit_context.py \
  -k liftA2_combines_independent_rag_config_fields
```

The constructor remains an ordinary function. `liftA2` is responsible for
opening successful inputs, applying the constructor, and restoring the Result
context.

## Independence does not imply accumulation

The two configuration fields are independent, but the Module 06 `Result`
applicative is still fail-fast. If both inputs are `Err`, the left error is
returned:

```python
failed = liftA2(
    make_env,
    Err(ErrInfo(code="CHUNK_SIZE", msg="must be positive")),
    Err(ErrInfo(code="OVERLAP", msg="must be non-negative")),
)

assert failed == Err(
    ErrInfo(code="CHUNK_SIZE", msg="must be positive")
)
```

This behavior is deterministic, but it does not report every invalid field.
If the learner or caller must see all independent field errors, use the
Module 05 `Validation` applicative instead.

The decision has two dimensions:

```text
dependency:  independent inputs or a later step needing an earlier success?
failure UX:  first error or every independent error?
```

Do not infer the second answer from the first.

## Cross-field constraints have a different owner

`chunk_size=4` and `overlap=6` may each be locally valid integers, but the pair
violates `overlap < chunk_size`. That rule cannot be checked by either field
parser alone.

A clear sequence is:

1. parse or validate each field independently;
2. combine the successful values;
3. validate the relationship at the join;
4. construct `RagEnv` only from a valid pair.

For a fail-fast Result route:

```python
@dataclass(frozen=True)
class ChunkPolicy:
    chunk_size: int
    overlap: int


def require_valid_overlap(
    policy: ChunkPolicy,
) -> Result[ChunkPolicy, ErrInfo]:
    if policy.overlap >= policy.chunk_size:
        return Err(
            ErrInfo(
                code="OVERLAP_RANGE",
                msg="overlap must be smaller than chunk size",
            )
        )
    return Ok(policy)


policy = liftA2(ChunkPolicy, chunk_size, overlap)
env = policy.and_then(require_valid_overlap).map(
    lambda valid: RagEnv(
        chunk_size=valid.chunk_size,
        overlap=valid.overlap,
    )
)
```

Notice the change in operation:

- `liftA2` combines independent inputs;
- `and_then` runs a dependent cross-field check;
- `map` constructs the final value from an already valid policy.

## Lifting does not catch constructor exceptions

This is unsafe if `RagEnv` can reject the pair:

```python
liftA2(RagEnv, Ok(4), Ok(6))
```

`liftA2` does not convert a constructor’s `ValueError` into `ErrInfo`. Either
validate before construction or use a narrow exception bridge at the boundary
where throwing input enters the application. Do not assume that “inside
Result” means arbitrary Python exceptions are captured.

## `map_err` changes the public error vocabulary

Sometimes an adapter error is too specific for the caller:

```python
parsed: Result[int, ParseError] = parse_integer(raw)
public: Result[int, ErrInfo] = parsed.map_err(
    lambda error: ErrInfo(
        code="CONFIG_PARSE",
        msg=error.message,
    )
)
```

This is a semantic conversion. The mapping function should preserve enough
provenance for the caller to act. Replacing every error with
`ErrInfo(code="FAILED", msg="failed")` technically changes the type but damages
the application contract.

## Derive the operation from the shapes

Trace this small RAG route:

```python
source: Result[RawDoc, ErrInfo]
```

Then classify:

```python
source.map(clean_doc)
```

`clean_doc: RawDoc -> CleanDoc`, so the result is
`Result[CleanDoc, ErrInfo]`.

```python
source.and_then(require_abstract)
```

`require_abstract: RawDoc -> Result[RawDoc, ErrInfo]`, so the result remains
one `Result[RawDoc, ErrInfo]`.

```python
liftA2(make_env, parsed_size, parsed_overlap)
```

`make_env` needs both independent successful integers, so the result is
`Result[RagEnv, ErrInfo]`.

When the operation is hard to choose, write the function signatures on paper.
The correct structure is usually visible before any implementation code.

## Common wrong turns

- **Using `and_then` for independent fields.** This invents a dependency and
  can make error order look like business logic.
- **Expecting `Result.liftA2` to accumulate.** The shipped Result contract
  preserves the left failure; Module 05 Validation accumulates.
- **Placing all validation inside a constructor.** A throwing constructor
  bypasses typed error values unless the boundary is handled explicitly.
- **Lifting an impure function and calling the flow pure.** The container does
  not remove filesystem, clock, network, or mutation effects.
- **Wrapping a plain local calculation for style.** Lifting earns its place
  when a real context must be preserved.

## What the focused proof establishes

The learning test proves that:

- two successful values construct the expected `RagEnv`;
- the declared left error wins when both Results fail; and
- the plain constructor can be reused without container-aware parameters.

It does not prove that all `RagEnv` pairs are valid, that errors accumulate, or
that constructor exceptions are caught.

Continue with [Law-Guided Design](law-guided-design.md) to learn which
structural rewrites these operations permit.
