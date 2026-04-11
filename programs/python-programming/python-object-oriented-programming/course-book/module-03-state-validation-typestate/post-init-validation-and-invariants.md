# Post-Init Validation and “Invalid States Unrepresentable”


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Object-Oriented Programming"]
  section["State Validation Typestate"]
  page["Post-Init Validation and “Invalid States Unrepresentable”"]
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

Read the first diagram as a placement map: this page is one concept inside its parent module, not a detached essay, and the capstone is the pressure test for whether the idea holds. Read the second diagram as the working rhythm for the page: name the problem, study the example, identify the boundary, then carry one review question forward.

## Purpose

Turn “validation” from an afterthought into a **construction-time guarantee**.

The core idea: if an object exists, it should already satisfy its invariants. That makes the rest of your code simpler, safer, and more teachable.

## Where This Fits

Running example: a monitoring service that fetches metrics, evaluates rules, and emits alerts. In earlier modules we refactored toward a layered design (domain/application/infrastructure) with explicit roles. From M03 onward, we tighten *data integrity* and *lifecycle semantics* so the system stays correct under change.

## 1. Invariants: The Small List of Truths Your Code Can Depend On

An **invariant** is a condition that must always hold for an object.

Examples in our domain:
- `Threshold` must be finite and within an allowed range.
- A `Window` must be positive.
- An `ActiveRule` must have an activation timestamp.
- A `RetiredRule` must not be evaluated.

If invariants are not enforced at construction, every method must defensively re-check them, and your code becomes a minefield.

## 2. `__post_init__` as the Invariant Gate

For dataclasses, `__post_init__` is the natural place to enforce invariants:

```python
from dataclasses import dataclass
import math

@dataclass(frozen=True, slots=True)
class Threshold:
    value: float

    def __post_init__(self):
        if not math.isfinite(self.value):
            raise ValueError("Threshold must be finite")
        if self.value < 0:
            raise ValueError("Threshold must be non-negative")
```

This yields a powerful design guarantee:
> “If you have a `Threshold`, it’s valid.”

The rest of the system can rely on that without re-validating.

## 3. “Invalid States Unrepresentable” in Practice

You rarely get perfect unrepresentability in Python, but you can get close by:

- using semantic types instead of primitives,
- separating typestates into distinct types (Draft/Active/Retired),
- limiting mutation to small, explicit methods.

Example: `ActiveRule` and `DraftRule` are different types:

```python
@dataclass(frozen=True, slots=True)
class DraftRule:
    metric: MetricName
    threshold: Threshold

@dataclass(frozen=True, slots=True)
class ActiveRule:
    rule_id: str
    metric: MetricName
    threshold: Threshold
    activated_at: float
```

Now the impossible is literally unconstructable:
- you cannot forget `activated_at` for an active rule,
- because there is no “maybe” field.

## 4. Validation Boundaries: Domain vs Input

Not all validation belongs in the domain object.

- **Domain invariants**: belong in `__post_init__` (always required).
- **Input validation**: belongs at the boundary (M03C26) — type coercion, missing fields, user-friendly error messages.

Example:
- Domain `Window(seconds: int)` requires `seconds > 0`.
- Boundary code may also accept `"5m"` and convert it to `300` — that is not domain logic; it’s parsing logic.

## 5. Testing Invariants: Small, Precise Tests

Write tests that prove invariants are enforced.

Pattern:
- one test per invariant, with a failing case and a passing case.

```python
import pytest

def test_threshold_rejects_nan():
    with pytest.raises(ValueError):
        Threshold(float("nan"))

def test_threshold_accepts_positive():
    assert Threshold(3.5).value == 3.5
```

## Practical Guidelines

- Enforce invariants at construction time; avoid “validate later” designs.
- Separate domain invariants from boundary parsing/coercion (M03C26).
- Prefer distinct types for distinct states over `Optional[...]` fields.
- Write invariant tests as tiny unit tests; they are high leverage and low maintenance.

## Exercises for Mastery

1. Identify 3 invariants in your domain and implement them in `__post_init__` on semantic types.
2. Replace one `Optional[...]` “maybe field” with a distinct typestate dataclass.
3. Add unit tests that confirm invalid inputs fail fast at construction.
