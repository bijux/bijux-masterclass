# Pattern Matching


<!-- page-maps:start -->
## Lesson Map

```mermaid
flowchart LR
  chain["Start with long if/isinstance chains"] --> match["Match on ADT variants declaratively"]
  match --> narrow["Let each branch narrow to the right payload"]
  narrow --> exhaust["Use the final branch to prove exhaustiveness"]
```
<!-- page-maps:end -->

This lesson should make pattern matching feel like a safer way to read domain variants, not like syntactic novelty. Students need to see that `match` is valuable because it lines up naturally with tagged sums and makes missing cases harder to hide.

## Start With the Branching Boilerplate

Once a codebase has explicit variants, the next problem is how to handle them cleanly. Long `if isinstance` chains often preserve the information, but they bury the model under branching boilerplate.

- If every handler repeats the same variant tests and attribute extraction, the branch structure is harder to review than it needs to be.
- If adding a new variant can slip past existing handlers, the dispatch style is still too fragile.
- If you cannot tell what each branch assumes about the payload, the case analysis is not yet readable enough.

**Core question**  
How do you replace verbose, fragile `if isinstance` chains with Python 3.10+ `match` statements that destructuringly pattern-match on ADTs — guaranteeing exhaustive handling, automatic type narrowing, and refactor-safety in every FuncPipe pipeline stage?

This lesson introduces `match` as the natural case-analysis syntax for ADTs:

- destructure variants directly where they are handled
- keep guards and payload extraction close to the matching branch
- use the final `assert_never` pattern to keep the closed-union promise honest

The motivating `Result` example matters because it is exactly the kind of branch-heavy code that appears everywhere once variants are available.

The naïve pattern everyone writes first:

```python
# BEFORE – verbose, fragile, non-exhaustive
def handle_result(res: Result[T, ErrInfo]) -> T:
    if isinstance(res, Ok):
        return res.value
    elif isinstance(res, Err):
        if res.error.code == ErrorCode.RETRYABLE:
            return retry(res.error)
        else:
            raise RuntimeError(res.error.msg)
    # oops, someone added Pending and forgot to handle it → silent crash or wrong path
```

This is the branching boilerplate to replace.

The production pattern makes the variant structure visible in the code shape itself and gives tooling a better chance to help.

```python
# AFTER – one lawful, exhaustive block
def handle_result(res: Result[T, ErrInfo]) -> T:
    match res:
        case Ok(value=v):
            return v
        case Err(error=e) if e.code is ErrorCode.RETRYABLE:
            return retry(e)
        case Err(error=e):
            raise RuntimeError(e.msg)
        case other:
            assert_never(other)   # mypy errors if you add Pending and forget to handle
```

That is the real promise to care about: changes to the model become visible pressure on the handling sites instead of silent drift.

**Audience**: Engineers tired of `isinstance` spaghetti who want clearer and more trustworthy case analysis over ADTs.

**Outcome**
1. Every `if isinstance` chain replaced with `match`.
2. All matches statically checked for exhaustiveness via `case other: assert_never(other)` on closed unions.
3. Readable, safe, refactor-proof ADT handling.

## Tiny Non-Domain Example – Shape Area

```python
match shape:
    case Circle(radius=r):
        return 3.14159 * r * r
    case Rectangle(width=w, height=h):
        return w * h
    case other:
        assert_never(other)   # mypy errors if you add Triangle and forget
```

Adding `Triangle` breaks every site until handled — no silent wrong-path.

## Why Pattern Matching for ADTs? (Three bullets every engineer should internalise)

- **Exhaustiveness**: `case other: assert_never(other)` + closed union types → adding a variant forces every match to update.
- **Type narrowing**: Branches know exact variant → no more `cast` or `isinstance`.
- **Readability + safety**: Declarative patterns + guards replace nested if-elif chains forever.

Use `match` **only** on core frozen dataclasses. Pydantic models are converted at the edge (C06).

## Setup – Imports & Core ADT Recap

```python
from typing_extensions import assert_never  # critical for exhaustiveness

# In this repo, use the production ADTs:
from funcpipe_rag.fp.core import Some, NoneVal
from funcpipe_rag.fp.error import ErrorCode
from funcpipe_rag.result.types import Ok, Err, Result, ErrInfo
```

## 1. Laws & Invariants (machine-checked)

| Invariant             | Description                                          | Enforcement                              |
|-----------------------|------------------------------------------------------|------------------------------------------|
| Exhaustiveness        | All variants handled (`case other: assert_never`)    | mypy (with closed unions) + runtime      |
| Type Narrowing        | Each case narrows to exact variant                   | mypy strict mode                         |
| Guard Purity          | Guards are pure expressions                          | Code review + tests                      |
| No Side Effects       | Patterns/guards do no I/O or mutation                | Reproducibility tests                    |

With `Result = Ok[T] | Err[E]` defined as a closed union and a `case other: assert_never(other)` branch, mypy will error when you add a new variant and forget to handle it.

## 2. Decision Table – `match` vs `if isinstance`

| Scenario                     | Need guards? | Need destructuring? | Use `match`? |
|------------------------------|--------------|---------------------|--------------|
| Simple binary (Ok/Err)       | No           | Yes                 | Yes          |
| With retry logic             | Yes          | Yes                 | Yes          |
| Deeply nested product        | No           | Yes                 | Yes          |
| Performance-critical path    | No           | No                  | Optional     |
| Python <3.10                 | –            | –                   | No           |

## Gotchas (every engineer must internalise)

- **Capture vs constant**: Bare name captures → use `Literal["kind"]` or qualified `ErrorCode.RETRYABLE`.
- **Positional matching**: Dataclasses expose fields via `__match_args__`; reordering fields silently breaks positional patterns → **always use keyword patterns** (`case Ok(value=v)`).
- **Guards**: Must be pure and fast — do work after the match.
- **Exhaustiveness**: Always end with `case other: assert_never(other)`.

## 3. Reference Implementations

### 3.1 Matching Option

```python
def unwrap_or(opt: Option[T], default: T) -> T:
    match opt:
        case Some(value=v):
            return v
        case NoneVal():
            return default
        case other:
            assert_never(other)
```

### 3.2 Matching Result with Guards

```python
def handle_result(res: Result[T, ErrInfo]) -> T:
    match res:
        case Ok(value=v):
            return v
        case Err(error=e) if e.code is ErrorCode.RETRYABLE:
            return retry(e)
        case Err(error=e):
            raise RuntimeError(e.msg)
        case other:
            assert_never(other)
```

### 3.3 Matching Validation (or-patterns)

```python
def handle_validation(val: Validation[T, ErrInfo]) -> T:
    match val:
        case VSuccess(value=v):
            return v
        case VFailure(errors=(e,)) if e.code is ErrorCode.RETRYABLE:
            return retry_single(e)
        case VFailure(errors=es):
            raise MultipleErrors(es)
        case other:
            assert_never(other)
```

### 3.4 RAG Integration – Embedding Result Handling

```python
def embed_with_fallback(res: Result[Embedding, ErrInfo]) -> Embedding:
    match res:
        case Ok(value=emb):
            return emb
        case Err(error=e) if e.code in {ErrorCode.TRANSIENT, ErrorCode.RATE_LIMIT}:
            return fallback_embedding(e)
        case Err(error=e):
            log_and_raise(e)
        case other:
            assert_never(other)
```

## 4. Property-Based Proofs (capstone/tests/test_pattern_matching.py)

```python
from hypothesis import given, strategies as st

@given(v=st.integers())
def test_option_unwrap_or_some(v):
    assert unwrap_or(Some(value=v), default=-1) == v

@given(default=st.integers())
def test_option_unwrap_or_none(default):
    assert unwrap_or(NoneVal(), default) == default

@given(res=st.one_of(st.builds(Ok, value=st.integers()),
                    st.builds(Err, error=st.builds(ErrInfo, code=st.sampled_from(ErrorCode), msg=st.text()))))
def test_result_match_exhaustive(res):
    # This test verifies no runtime crash; exhaustiveness is enforced by mypy
    # via assert_never on closed unions.
    def dummy(r: Result[int, ErrInfo]) -> int:
        match r:
            case Ok(value=v):
                return v
            case Err(error=_):
                return -1
            case other:
                assert_never(other)
        # unreachable
    dummy(res)
```

## 5. Big-O & Allocation Guarantees

| Operation            | Time   | Heap   | Notes                              |
|----------------------|--------|--------|------------------------------------|
| match on ADT         | O(1)   | O(1)   | Constant time dispatch             |

## 6. Anti-Patterns & Immediate Fixes

| Anti-Pattern                  | Symptom                            | Fix                                      |
|-------------------------------|------------------------------------|------------------------------------------|
| Long if-isinstance chains     | Verbose, easy to miss cases        | Replace with `match` + `case other: assert_never` |
| Missing case other            | Silent bugs on new variants        | Always end match with `case other: assert_never(other)` |
| Side effects in guards        | Non-deterministic behaviour        | Keep guards pure                         |
| Positional matching           | Brittle on field reorder           | Prefer keyword patterns (`value=v`)      |
| Bare name capture             | Unexpected rebinding               | Use literals or qualified names          |

## 7. Pre-Core Quiz

1. `match` replaces what? → **`if isinstance` chains**  
2. Exhaustiveness via…? → **`case other: assert_never(other)`**  
3. Guards for…? → **Conditional branches**  
4. Type narrowing? → **Branch knows exact variant**  
5. Always end match with…? → **`case other: assert_never(other)`**

## 8. Post-Core Exercise

1. Refactor one `if isinstance` chain to `match` → add `case other: assert_never(other)`.  
2. Add a new variant to an existing sum type → verify mypy errors in all match sites.  
3. Use guards to handle retryable errors in a Result match.  
4. Replace a nested if-elif with or-patterns (`case Ok() | Some():`).

**Continue with:** [Serialization Beyond Pydantic](../module-05-algebraic-data-modelling-validation/serialization-beyond-pydantic.md)

You now destructure and handle every ADT with concise, exhaustive, type-narrowing `match` statements — no more `isinstance` boilerplate, no more silent missing cases. The rest of Module 5 adds stable serialization, compositional domain models, and performance guidance for heavy ADTs.
