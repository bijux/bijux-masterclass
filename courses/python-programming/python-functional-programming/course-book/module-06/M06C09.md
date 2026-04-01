# M06C09: Refactoring `try/except` Spaghetti into Pure Monadic Pipelines

## Progression Note
Module 6 shifts from pure data modelling to **effect-aware composition**.  
We now treat failure and absence as first-class effects that propagate automatically through pipelines — eliminating nested conditionals forever.

| Module | Focus                                   | Key Outcomes                                                                 |
|--------|-----------------------------------------|-------------------------------------------------------------------------------|
| 5      | Algebraic Data Modelling                | ADTs, exhaustive pattern matching, total functions, refined types            |
| 6      | Monadic Flows as Composable Pipelines   | bind/and_then, Reader/State-like patterns, error-typed flows                 |
| 7      | Effect Boundaries & Resource Safety     | Dependency injection, boundaries, testing, evolution                          |

**Core question**  
How do you systematically refactor the inevitable `try/except` + `if None` spaghetti that accumulates in every real codebase into clean, linear, composable monadic pipelines — without changing public return behaviour and while gaining testability and refactor safety?

This is the core where you finally pay off the promise of the entire module: you take real, ugly, production-grade imperative error handling and turn it into pure, lawful, beautiful FP — with mechanical proof that the public contract is identical.

**Audience**: Engineers who know the theory but still have a codebase full of nested try/except and want a repeatable, safe refactoring process.

**Outcome**
1. You will have a mechanical 6-step process for turning any try/except mess into a monadic pipeline.
2. You will prove (with Hypothesis) that the refactored version has identical public return behaviour for all inputs.
3. You will never again fear “what if I break something?” when cleaning up error handling.

## The 6-Step Refactoring Process (memorise this)

1. Identify every error path (exceptions, None checks, invalid states).
2. Define typed domain errors (`ParseErr`, `ValidationErr`, `NetworkErr`, etc.).
3. Extract pure functions for each step.
4. Bridge impurities at the boundary with `try_result` / `option_from_nullable`.
5. Chain with `.and_then` / `.map` / applicative combinators (`.ap`, `v_liftA2`).
6. Add Hypothesis equivalence tests and delete the old code.

Do this once per function and you’ll never go back.

## 1. Laws & Invariants (machine-checked in CI)

| Invariant                       | Description                                                                                  | Enforcement          |
|---------------------------------|----------------------------------------------------------------------------------------------|----------------------|
| Behavioural Equivalence         | Refactored pipeline produces identical public return values for all inputs                  | Hypothesis properties|
| Totality (expected errors)      | Expected errors always return container (never raise)                                        | Hypothesis + runtime |
| Unexpected failures still raise | Programming bugs remain exceptions (never silently become domain Err)                       | Runtime contract     |
| No New Side Effects             | Refactored boundary preserves or reduces side effects (never introduces new kinds of effects) | Code review          |
| Propagation                     | Errors short-circuit exactly where original would have returned/raised                      | Hypothesis           |

All equivalence properties run in CI. A single divergence fails the build.

## 2. Decision Table – What to Refactor Into What

| Original Pattern              | Refactor To                                                  | Why                                      |
|-------------------------------|--------------------------------------------------------------|------------------------------------------|
| try/except ValueError         | `try_result(..., map_exc, exc_type=ValueError)` + `.and_then` | Typed domain error                       |
| if value is None              | `option_from_nullable(value).and_then(...)`                  | Explicit absence                         |
| Nested try/except             | Chained `.and_then`                                          | Linear happy path                        |
| Multiple independent checks   | Validation + `v_ap` / `v_liftA2`                             | Accumulate all errors                    |

## 3. Public API – No new helpers (use everything from previous cores)

You already have everything you need:

- `.map`, `.and_then`, `.ap` on `Result`
- `.map`, `.and_then` on `Option`
- `v_ap`, `v_liftA2` (Validation applicative helpers; Validation is a sum type, not a methodful class)
- `try_result` (with `exc_type` below), `result_map_try`
- `Some` / `NoneVal` / `option_from_nullable`

### Updated try_result (matches the repository implementation)

```python
def try_result(
    thunk: Callable[[], T],
    map_exc: Callable[[Exception], E],
    exc_type: type[Exception] | tuple[type[Exception], ...] = Exception,
) -> Result[T, E]:
    """Bridge an impure thunk into Result. Use ONLY at effect boundaries.
    
    exc_type restricts which exceptions are treated as expected domain errors.
    All others propagate as bugs (never become Err).
    """
    try:
        return Ok(thunk())
    except exc_type as ex:
        return Err(map_exc(ex))
```

## 4. The Full Refactoring Cookbook – Three Real Examples

### 4.1 JSON Parsing + Processing (classic nested try/except)

```python
# BEFORE – the spaghetti everyone has
def load_and_process(path: str) -> dict | None:
    try:
        raw = open(path).read()
    except IOError as e:
        log.error(f"IO error: {e}")
        return None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        log.error(f"JSON error: {e}")
        return None
    try:
        return process(data)
    except ValueError as e:
        log.error(f"Processing error: {e}")
        return None
```

```python
# AFTER – pure, linear, testable
@dataclass(frozen=True)
class IOErrorErr: msg: str
@dataclass(frozen=True)
class JSONErr: msg: str
@dataclass(frozen=True)
class ProcessErr: msg: str
Err = IOErrorErr | JSONErr | ProcessErr

def load_and_process(path: str) -> Result[dict, Err]:
    return (
        try_result(lambda: open(path).read(), lambda e: IOErrorErr(str(e)), exc_type=OSError)
        .and_then(
            lambda raw: try_result(
                lambda: json.loads(raw),
                lambda e: JSONErr(str(e)),
                exc_type=json.JSONDecodeError,
            )
        )
        .and_then(
            lambda data: try_result(
                lambda: process(data),
                lambda e: ProcessErr(str(e)),
                exc_type=ValueError,
            )
        )
    )

# Boundary (if you need to match original None return)
def load_and_process_legacy(path: str) -> dict | None:
    match load_and_process(path):
        case Ok(data): return data
        case Err(e): log.error(e.msg); return None
```

Zero nesting. Happy path is three lines. Every error is typed and testable.

### 4.2 Multi-field Validation (independent errors)

```python
# BEFORE – early returns, only first error visible
def validate_user(name: str | None, age: int | None, email: str | None) -> dict | str:
    errors = []
    if not name:
        errors.append("name missing")
    if not age or age < 0:
        errors.append("invalid age")
    if not email or "@" not in email:
        errors.append("invalid email")
    if errors:
        return "; ".join(errors)
    return {"name": name, "age": age, "email": email}
```

```python
# AFTER – Validation accumulates all errors
def validate_user(name: str | None, age: int | None, email: str | None) -> Validation[User, str]:
    v_name = validate_name(name)
    v_age = validate_age(age)
    v_email = validate_email(email)

    partial_user: Validation[Callable[[str], User], str] = v_liftA2(
        lambda n, a: lambda e: User(n, a, e),
        v_name,
        v_age,
    )

    from funcpipe_rag.fp.validation import v_ap

    return v_ap(partial_user, v_email)

# Boundary – preserve original dict | str contract
def validate_user_legacy(name: str | None, age: int | None, email: str | None) -> dict | str:
    match validate_user(name, age, email):
        case VSuccess(user): return {"name": user.name, "age": user.age, "email": user.email}
        case VFailure(errors): return "; ".join(errors)
```

All errors always reported. Zero manual error collection.

### 4.3 Optional Chaining (absence checks)

```python
# BEFORE – pyramid of doom
def get_user_email(id: int) -> str | None:
    user = db.get_user(id)
    if user is None:
        return None
    profile = user.get("profile")
    if profile is None:
        return None
    return profile.get("email")

# AFTER – Option chain
def get_user_email(id: int) -> Option[str]:
    return (
        option_from_nullable(db.get_user(id))
        .and_then(lambda user: option_from_nullable(user.get("profile")))
        .and_then(lambda profile: option_from_nullable(profile.get("email")))
    )

# Boundary – preserve original str | None contract
def get_user_email_legacy(id: int) -> str | None:
    return get_user_email(id).unwrap_or(None)
```

Zero pyramid. Absence propagates automatically.

## 5. Proving Equivalence – The Safety Net

```python
@given(st.text())
def test_json_refactor_equivalence(raw: str):
    @dataclass(frozen=True)
    class ParseErr:
        msg: str

    # Imperative version
    def imp() -> dict | None:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None

    # FP version
    def fp() -> Result[dict, ParseErr]:
        return try_result(
            lambda: json.loads(raw),
            lambda e: ParseErr(str(e)),
            exc_type=json.JSONDecodeError,
        )

    # Boundary to match original
    def fp_boundary() -> dict | None:
        return fp().unwrap_or(None)

    assert imp() == fp_boundary()
```

Run this in CI. If it ever fails, you broke the refactor.

## 6. Anti-Patterns & Immediate Fixes

| Anti-Pattern                    | Symptom                              | Fix                                      |
|---------------------------------|--------------------------------------|------------------------------------------|
| Nested try/except               | Unreadable indentation              | Chain with `.and_then`                   |
| Early returns with error strings| Only first error visible             | Use Validation + `.ap` / `v_liftA2`      |
| if value is None pyramid        | Deep nesting                         | Chain with `.and_then` on Option         |
| No equivalence tests            | "It works on my machine"             | Add Hypothesis equivalence properties    |

## 7. Pre-Core Quiz

1. First step in refactoring? → **Identify every error path**  
2. Bridge exceptions with? → **try_result at boundary**  
3. Chain dependent steps with? → **.and_then**  
4. Accumulate independent errors with? → **Validation + .ap / v_liftA2**  
5. Prove safety with? → **Hypothesis equivalence tests**

## 8. Post-Core Exercise

1. Take the ugliest try/except function in your codebase and apply the 6-step process.
2. Add Hypothesis equivalence tests and delete the old imperative version.
3. Celebrate — you now have one less piece of spaghetti forever.

**Next:** M06C10 – Configurable Pipelines – Toggle Validation, Logging, Metrics at Runtime

You have now refactored imperative error handling into pure, composable, mathematically proven pipelines. Your codebase is dramatically cleaner, safer, and ready for the final architectural patterns.
