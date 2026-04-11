# Exercise Answers

Use this page after attempting the exercises yourself. The point is not to match every
example literally. The point is to compare your reasoning against answers that name the
runtime claim first and then judge the strength of the evidence honestly.

## Answer 1: Describe one callable contract precisely

Example answer:

```python
import inspect


def demo(a: int, /, b, *, c: bool = False, **kw):
    pass


sig = inspect.signature(demo)
```

Strong evidence:

- `str(sig)` is `(a: int, /, b, *, c: bool = False, **kw)`
- `a` is `POSITIONAL_ONLY`
- `b` is `POSITIONAL_OR_KEYWORD`
- `c` is `KEYWORD_ONLY`
- `kw` is `VAR_KEYWORD`

Good conclusion:

The signature is stronger than a hand-written summary because it exposes interpreter-level
parameter rules, not just a human description of "roughly what the function takes."

## Answer 2: Bind one call honestly

Example answer:

```python
import inspect


def demo(a, /, b, *, c=False):
    pass


sig = inspect.signature(demo)
ba = sig.bind(10, 20)
ba.apply_defaults()
```

Strong evidence:

- `ba.arguments == {"a": 10, "b": 20, "c": False}`
- `sig.bind(a=10, b=20)` raises `TypeError` because `a` is positional-only

Good conclusion:

Binding is better than manual matching because it reuses Python's own call rules, including
positional-only and keyword-only behavior, instead of relying on incomplete custom logic.

## Answer 3: Recover provenance without overclaiming

Example answer:

```python
import inspect


def demo():
    return 42


module = inspect.getmodule(demo)
```

Strong evidence:

- `module` often points at the defining module
- `getfile(demo)` may return a file path
- `getsource(demo)` may succeed in a normal file-backed context

Good limitation statement:

Those helpers are best-effort because interactive sessions, generated code, packaged
environments, or transformed source can break or weaken the recovery path.

## Answer 4: Compare dynamic members with static structure

Example answer:

```python
import inspect


class Example:
    @property
    def expensive(self):
        print("SIDE EFFECT")
        return 123
```

Strong evidence:

- `inspect.getmembers(Example())` can trigger `SIDE EFFECT`
- `inspect.getattr_static(Example, "expensive")` returns the `property` object itself

Good conclusion:

Dynamic member enumeration is a value-oriented tool and may execute behavior. Static lookup
is the stronger fit for framework inspection when the goal is to inspect structure safely.

## Answer 5: Use frames only as diagnostics

Example answer:

```python
import inspect


def top_callers(limit=2):
    frame = inspect.currentframe()
    if frame is None:
        return []
    try:
        out = []
        current = frame.f_back
        while current is not None and len(out) < limit:
            out.append(current.f_code.co_name)
            current = current.f_back
        return out
    finally:
        del frame
```

Strong evidence:

- the helper returns a small slice of caller names
- it releases the starting frame explicitly

Good conclusion:

This belongs to diagnostics because it inspects execution context rather than explicit
program state. It should not become ordinary application control flow.

## Answer 6: Review a runtime-description helper

Example answer:

Suppose a `__repr__` helper:

- uses `inspect.signature(cls.__init__)` for ordering
- reads `__dict__` and slots for values
- avoids `getattr` on arbitrary names

Strong assessment:

- signature ordering is strong evidence when available
- stored state is the right value source for a safe representation
- avoiding broad dynamic lookup keeps properties from being evaluated accidentally

Good repair if the helper is weaker:

If the helper currently uses `getattr` over arbitrary names, replace that with direct
storage reads and deliberate slot handling so representation stays observational.

## What strong Module 03 answers have in common

Across the whole set, strong answers share the same habits:

- they state the runtime claim before naming a helper
- they separate strong callable evidence from best-effort provenance
- they distinguish dynamic value inspection from static structure
- they keep frame inspection in the diagnostics bucket

If an answer still sounds like "inspect told me so," revise it until you can say what
kind of evidence `inspect` actually gave you.
