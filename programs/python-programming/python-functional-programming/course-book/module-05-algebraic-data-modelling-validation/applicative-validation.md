# Applicative Validation


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Functional Programming"]
  section["Algebraic Data Modelling Validation"]
  page["Applicative Validation"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Stop conflating “validation” with “first error wins.” The key question is whether the checks depend on each other. If they do not, then forcing users to fix one field at a time is usually a design failure, not a necessity.

## Start With the Feedback Problem

The pain of fail-fast validation usually appears before the name “applicative.” Begin from that user-facing problem.

- If all the checks are independent, reporting only the first failure is usually unnecessary friction.
- If one validation step depends on the output of another, then applicative accumulation is no longer the right default.
- If you cannot explain how errors are combined, the validation policy is still too magical to trust.

**Core question**  
How do you replace short-circuiting validation that reports only the first error with lawful applicative combinators that run every check independently and return **all** errors at once — giving perfect diagnostics in one pass?

This lesson introduces applicative validation as the right tool for independent checks:

- run each independent check without waiting for earlier checks to succeed
- accumulate all errors using an explicit combination rule
- keep constructor assembly separate from the error-reporting policy

The motivating registration example matters because it captures the end-user impact clearly: repeated resubmission is often the direct result of the wrong validation shape.

The naïve pattern (monadic / short-circuiting):

```python
# BEFORE – fail-fast, terrible UX
def validate_user(raw: RawUser) -> Result[User, ErrInfo]:
    name = validate_name(raw.name)
    if isinstance(name, Err): return name
    email = validate_email(raw.email)
    if isinstance(email, Err): return email
    age = validate_age(raw.age)
    if isinstance(age, Err): return age
    return Ok(User(name.value, email.value, age.value))
```

This is the poor feedback loop to spot immediately.

The production pattern uses a dedicated validation container that treats error accumulation as a first-class rule rather than an ad hoc side effect of control flow.

```python
# AFTER – one lawful, composable line
validate_user = v_liftA3(
    User,
    validate_name   >> to_validation,
    validate_email  >> to_validation,
    validate_age    >> to_validation,
    combine=dedup_stable,
)

validated: Validation[User, ErrInfo] = validate_user(raw_user)
# → VFailure(errors=("name too short", "invalid email", "age negative"))
```

Now the diagnostic behavior is part of the design, and it scales better both for users and for code review.

Use this when you are tired of “fix one field, resubmit, repeat” and want complete, principled validation feedback.

**Outcome**
1. Every short-circuit validator replaced with `Validation`.
2. All validations proven to satisfy full applicative laws.
3. Complete error reports with zero boilerplate.

## Tiny Non-Domain Example – User Registration

```python
def validate_name(s: str) -> Result[str, str]:
    return Ok(s) if len(s) >= 3 else Err("name too short")

def validate_email(s: str) -> Result[str, str]:
    return Ok(s) if "@" in s else Err("missing @")

def validate_age(n: int) -> Result[int, str]:
    return Ok(n) if n >= 0 else Err("age negative")

validate_user = v_liftA3(
    lambda name, email, age: User(name, email, age),
    validate_name   >> to_validation,
    validate_email  >> to_validation,
    validate_age    >> to_validation,
    combine=dedup_stable,
)

validated = validate_user(RawUser("a", "no-at", -9))
# VFailure(errors=("name too short", "missing @", "age negative"))
```

All three errors collected — no short-circuit.

## Why Applicative Validation? (Three bullets every engineer should internalise)

- **Independent execution**: Every check runs fully — perfect diagnostics.
- **Lawful composition**: `pure(f) <*> pure(x) == pure(f(x))`, `u <*> pure(y) == pure(lambda f: f(y)) <*> u`, etc. — refactoring is safe.
- **Configurable error combination**: Errors combine via any semigroup (concat, dedup, priority, etc.).

Validation is **applicative only** — we deliberately **do not** provide monadic `bind` that would re-introduce short-circuiting.

## 1. Laws & Invariants (machine-checked)

| Law               | Formal Statement                                                            | Enforcement                              |
|-------------------|-----------------------------------------------------------------------------|------------------------------------------|
| Identity          | `pure(id) <*> v == v`                                                       | Hypothesis                               |
| Composition       | `pure(compose) <*> u <*> v <*> w == u <*> (v <*> w)`                        | Hypothesis                               |
| Homomorphism      | `pure(f) <*> pure(x) == pure(f(x))`                                         | Hypothesis                               |
| Interchange       | `u <*> pure(y) == pure(lambda f: f(y)) <*> u`                               | Hypothesis                               |
| Error Combination | When both sides fail → errors = combine(left.errors, right.errors)         | Property tests                           |
| Non-empty Failure | `VFailure.errors` never empty                                               | Constructor invariant + tests             |

## 2. Decision Table – Validation vs Result

| Scenario                     | Want short-circuit? | Want all errors? | Recommended                     |
|------------------------------|---------------------|------------------|---------------------------------|
| API / DB call                | Yes                 | No               | `Result` + monadic bind         |
| Form / config / chunk validation | No              | Yes              | `Validation` + applicative      |
| Optional independent checks  | No                  | Yes              | `Option` + applicative          |

## 3. Public API (fp/applicative.py – mypy --strict clean)

```python
\"\"\"Backward-compatible name for Module 05 Validation.

The module-05 cores introduce Validation as an applicative; later cores refer to
it as `fp.validation`. This module keeps the earlier import path working.
\"\"\"

from .validation import *  # noqa: F403
```

## 4. Reference Implementations (continued)

### 4.1 Before vs After – Multi-field Validation

```python
# BEFORE – short-circuit hell
def validate_config(cfg: RawConfig) -> Result[Config, ErrInfo]:
    port = validate_port(cfg.port)
    if isinstance(port, Err): return port
    host = validate_host(cfg.host)
    if isinstance(host, Err): return host
    timeout = validate_timeout(cfg.timeout)
    if isinstance(timeout, Err): return timeout
    return Ok(Config(port.value, host.value, timeout.value))

# AFTER – all errors, one line
validate_config = v_liftA3(
    Config,
    validate_port   >> to_validation,
    validate_host   >> to_validation,
    validate_timeout >> to_validation,
    combine=dedup_stable,
)
```

### 4.2 RAG Integration – Validate Chunk Before Embedding

```python
def validate_chunk_for_embedding(chunk: Chunk) -> Validation[Chunk, ErrInfo]:
    return v_liftA2(
        lambda _text_ok, _meta_ok: chunk,
        validate_text_length(chunk.text),
        validate_metadata_keys(chunk.metadata),
        combine=dedup_stable,
    )

validated_chunks = v_traverse(raw_chunks, validate_chunk_for_embedding)

match validated_chunks:
    case VSuccess(chunks):
        return Ok(chunks)
    case VFailure(errors):
        return Err(make_errinfo(
            code="VALIDATION",
            msg="pre-embedding validation failed",
            meta={"errors": list(errors)},
        ))
```

## 5. Property-Based Proofs (capstone/tests/test_applicative_laws.py)

```python
from hypothesis import given, strategies as st
from typing import cast
import pytest
from funcpipe_rag.fp.applicative import *

@given(x=st.integers())
def test_identity(x):
    v = v_success(x)
    assert v_ap(v_success(lambda x: x), v) == v

@given(x=st.integers())
def test_homomorphism(x):
    f = lambda n: n + 10
    assert v_ap(v_success(f), v_success(x)) == v_success(f(x))

@given(x=st.integers())
def test_interchange(x):
    u = v_success(lambda n: n * 3)
    assert v_ap(u, v_success(x)) == v_ap(v_success(lambda f: f(x)), u)

@given(x=st.integers())
def test_composition(x):
    f = lambda n: n + 1
    g = lambda n: n * 2
    u = v_success(f)
    v = v_success(g)
    w = v_success(x)
    left = v_ap(v_ap(v_ap(v_success(compose), u), v), w)
    right = v_ap(u, v_ap(v, w))
    assert left == right

@given(errs1=st.lists(st.text(), min_size=1),
       errs2=st.lists(st.text(), min_size=1))
def test_collects_all_errors_concat(errs1, errs2):
    # Cast to silence mypy on phantom types (only in tests)
    bad_f: Validation[Callable[[int], int], str] = cast(
        Validation[Callable[[int], int], str],
        v_failure(errs1),
    )
    bad_x: Validation[int, str] = cast(
        Validation[int, str],
        v_failure(errs2),
    )
    result = v_ap(bad_f, bad_x)
    assert result.errors == tuple(errs1 + errs2)

@given(errs1=st.lists(st.text(), min_size=1),
       errs2=st.lists(st.text(), min_size=1))
def test_dedup_stable(errs1, errs2):
    combined = dedup_stable(tuple(errs1), tuple(errs2))
    seen = set()
    expected = []
    for e in errs1 + errs2:
        if e not in seen:
            seen.add(e)
            expected.append(e)
    assert combined == tuple(expected)

def test_v_failure_rejects_empty():
    with pytest.raises(ValueError):
        v_failure([])
```

## 6. Big-O & Allocation Guarantees

| Operation     | Time                  | Heap                     | Notes                                  |
|---------------|-----------------------|--------------------------|----------------------------------------|
| v_ap          | O(#errors)            | O(total errors)          | Due to tuple concatenation             |
| v_liftA2/3    | O(#errors)            | O(total errors)          | Same                                   |
| v_sequence    | O(N + #errors)        | O(total errors)          | One final tuple                        |

## 7. Anti-Patterns & Immediate Fixes

| Anti-Pattern                  | Symptom                            | Fix                                      |
|-------------------------------|------------------------------------|------------------------------------------|
| Short-circuit validation      | One error at a time                | `Validation` + `v_liftA*`                |
| Manual error list building    | Duplicated code, missed errors     | `v_ap` with custom `combine`             |
| Empty VFailure                | Silent success on error            | Enforced non-empty invariant             |
| Using Result for multi-error  | Poor UX                            | `to_validation` / `from_validation`     |
| Duplicate error messages      | Noisy output                       | `combine=dedup_stable`                   |

## 8. Pre-Core Quiz

1. Applicative = functor + what? → **pure + ap**  
2. Validation short-circuits? → **Never**  
3. Homomorphism → **pure(f) <*> pure(x) == pure(f(x))**  
4. Interchange → **u <*> pure(y) == pure($y) <*> u**  
5. Default error combination → **tuple concatenation**

## 9. Post-Core Exercise

1. Refactor one short-circuit validator to `Validation` → prove it returns all errors.  
2. Add `dedup_stable` to an existing validation → verify no duplicates.  
3. Implement `v_liftA4`..`v_liftA8` via currying.  
4. Use `v_traverse` to validate an entire batch of chunks before embedding.

**Continue with:** [Monoids](../module-05-algebraic-data-modelling-validation/monoids.md)

You now validate independently and collect every error in one pass — no more “fix one, resubmit” cycles. The rest of Module 5 introduces Monoids (for error combination, logs, metrics) and Monads (for dependent sequencing when you really do want short-circuiting).
