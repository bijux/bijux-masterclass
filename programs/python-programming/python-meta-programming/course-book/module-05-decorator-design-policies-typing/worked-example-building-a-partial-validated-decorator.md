# Worked Example: Building a Partial `@validated` Decorator

The five core lessons in Module 05 become much easier to trust when they all appear in
one wrapper that is useful, tempting, and easy to overclaim.

A partial runtime validator is exactly that kind of wrapper.

It combines:

- factory configuration
- signature-aware call binding
- annotation-aware runtime checks
- policy decisions about strictness and failure handling

That makes it the right worked example for the module.

## The incident

Assume a team wants a `@validated` decorator for selected callable boundaries.

They want it to:

- read type hints once
- validate supported argument types at call time
- optionally validate returns
- offer strict and warning-based modes

Those are reasonable goals. The danger is pretending this now amounts to full typing or a
general validation framework.

## The first design rule: keep it partial on purpose

This wrapper should be explicit about what it supports and what it refuses.

Supported cases might include:

- plain runtime classes
- `Union` and `Optional`
- `Any`

Unsupported cases might include:

- parameterized generics
- deep `Annotated` enforcement
- broader typing constructs that really belong to a separate validation framework

That refusal is a design strength, not a lack of ambition.

## Step 1: capture configuration and reusable evidence once

The factory shape makes the timing explicit:

```python
@validated(raise_on_error=True)
def func(...):
    ...
```

This means the wrapper can cache:

- the resolved type hints
- the signature

once at definition time, rather than rebuilding them on every call.

That is a good example of factory configuration and evidence caching working together
honestly.

## Step 2: bind the call before validating

One of the most important design choices is to validate after `sig.bind(...)`, not by
guessing from raw `args` and `kwargs`.

That makes the validation path:

1. bind arguments using Python's own call rules
2. apply defaults if needed
3. validate the resulting parameter/value mapping

This is stronger and easier to review than ad hoc argument parsing.

## Step 3: keep the type checker small and explicit

A compact helper such as `_is_instance` should stay honest about its scope:

- `Any` passes
- `Union` is checked recursively
- unsupported generic hints raise `NotImplementedError`

That clarity keeps the wrapper from drifting into fake comprehensiveness.

## A didactic implementation

```python
import functools
import inspect
import types
import warnings
from typing import Any, Callable, Union, get_args, get_origin, get_type_hints


def _is_instance(value: Any, hint: Any) -> bool:
    if hint is Any:
        return True
    origin = get_origin(hint)
    if origin in (Union, types.UnionType):
        return any(_is_instance(value, arg) for arg in get_args(hint))
    if origin is not None:
        raise NotImplementedError(
            f"runtime type checking for generic types like {hint!r} is not supported here"
        )
    return isinstance(value, hint)


def validated(raise_on_error: bool = True) -> Callable:
    def decorator(func: Callable) -> Callable:
        hints = get_type_hints(func)
        sig = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            for name, value in bound.arguments.items():
                if name in hints and not _is_instance(value, hints[name]):
                    msg = (
                        f"Argument '{name}={value!r}' is "
                        f"{type(value).__name__}, expected {hints[name]!r}"
                    )
                    if raise_on_error:
                        raise TypeError(msg)
                    warnings.warn(msg, UserWarning)

            result = func(*args, **kwargs)
            if "return" in hints and not _is_instance(result, hints["return"]):
                msg = (
                    f"Return '{result!r}' is "
                    f"{type(result).__name__}, expected {hints['return']!r}"
                )
                if raise_on_error:
                    raise TypeError(msg)
                warnings.warn(msg, UserWarning)
            return result

        return wrapper

    return decorator
```

## Why this version is a good teaching artifact

This wrapper is useful because it keeps all the important choices visible:

- configuration is explicit
- signature and hint resolution happen once
- supported hint handling is narrow and readable
- unsupported surfaces are refused clearly
- strict and warning modes are plainly separate

That is the kind of honesty a policy-heavy decorator needs.

## Warning mode is not safety mode

One especially important design boundary is:

- warning on mismatch does not make the function safe

The wrapped function can still fail internally after the warning. That is exactly why the
module frames this as a partial runtime contract rather than as a complete safety system.

## What this example teaches about Module 05

This worked example ties the module together:

- factories capture policy once
- binding keeps call matching honest
- annotation-aware checks stay partial
- metadata preservation still matters
- the wrapper is useful only because it refuses to overclaim

That is the real lesson. The validator is not here as a universal recipe. It is here as a
clear case study in policy ownership and boundary honesty.

## The review loop to keep

When you inherit or design an annotation-aware decorator, run this loop:

1. name the exact hint subset it supports
2. verify it binds calls before validating
3. check whether strict and warning modes are explicit
4. ask whether the policy still belongs in a decorator or should move to a more explicit validator component

If you can do that here, Module 05 has done its job and the course can move into
class-level customization with a stronger sense of wrapper limits.

## Continue through Module 05

- Previous: [Wrapper Policy Boundaries](wrapper-policy-boundaries.md)
- Next: [Exercises](exercises.md)
- Reference: [Exercise Answers](exercise-answers.md)
- Terms: [Glossary](glossary.md)
