# Worked Example: Building a Safer Debug Printer

The five core lessons in Module 02 become much easier to trust when they all appear in
one realistic tool.

This example uses a debugging helper because it creates exactly the right pressure:

- the tool wants to inspect runtime state
- the caller expects observation, not business behavior
- ordinary attribute access would quietly execute descriptors and fallback hooks

That is the right place to make the static-versus-dynamic boundary concrete.

## The incident

Assume a team wants a helper called `debug_print()` for quick runtime inspection during an
incident review.

The original helper does what many first versions do:

- it loops through names from `dir(self)`
- it reads values with `getattr(self, name)`
- it recursively prints nested objects

The team reports four problems:

1. properties execute during debugging
2. dynamic fallback hooks run even when nobody wanted business behavior
3. slotted objects are awkward to inspect
4. recursive object graphs can loop forever

Every one of those problems is a Module 02 problem, not just a formatting problem.

## The first mistake: treating value resolution as observation

The inherited sketch looks plausible:

```python
def debug_print(self):
    for name in dir(self):
        value = getattr(self, name)
        print(name, value)
```

That helper looks observational, but it is already executing the attribute protocol.

So the first repair is conceptual:

> a debug printer should not use dynamic reads by default unless executing runtime behavior
> is the stated goal.

That is the same boundary the module has been drawing all along.

## Step 1: separate name discovery from value resolution

`dir(self)` can still be useful for candidate names, with one caveat: it may call a
custom `__dir__` implementation.

That is acceptable as a lower-risk discovery step, but it should not be confused with
stored state or resolved values.

The workflow becomes:

1. discover candidate names
2. inspect attached objects statically
3. evaluate dynamic values only when the tool is explicitly configured to do so

That one shift changes the honesty of the whole helper.

## Step 2: switch the default read path to static lookup

The most important repair is using `inspect.getattr_static` for default reads.

```python
import inspect


raw = inspect.getattr_static(obj, "name")
```

Why this is better:

- properties stay as property objects unless explicitly evaluated
- `__getattr__` is not triggered during default inspection
- class-attached descriptors remain visible as attached objects

This is the core of the worked example:

> debugging tools usually want attachment truth first, not execution truth.

## Step 3: decide what to do with descriptors

Once static lookup is the default, the tool still needs policy.

For example:

- show property objects without evaluating them
- optionally evaluate properties behind an explicit flag
- read slot descriptors carefully when you want actual slot values

That policy is clearer than pretending every attribute read is harmless.

## Step 4: make recursion explicit and bounded

Naive debug printers often recurse into everything, which creates two kinds of trouble:

- giant unreadable output
- infinite loops on cyclic graphs

A safer design makes recursion explicit:

- recurse only into known safe opt-in objects
- keep a visited set
- enforce a maximum depth

Those are not cosmetic concerns. They are part of making the tool behave like a debugging
tool instead of like an accidental object walker with side effects.

## A healthier implementation

```python
import inspect
from types import MemberDescriptorType
from typing import Any


class DebugMixin:
    def debug_print(
        self,
        *,
        max_depth: int = 3,
        _depth: int = 0,
        _visited: set[int] | None = None,
        indent: int = 0,
        eval_properties: bool = False,
        show_dunder: bool = False,
    ) -> None:
        if _visited is None:
            _visited = set()

        obj_id = id(self)
        if obj_id in _visited:
            print(" " * indent + f"<Revisited id={obj_id}>")
            return
        _visited.add(obj_id)

        t = type(self)
        print(" " * indent + f"{t.__name__}(id={obj_id}) " + "{")

        if _depth >= max_depth:
            print(" " * (indent + 2) + "[Max depth reached]")
            print(" " * indent + "}")
            return

        for name in sorted(dir(self)):
            if not show_dunder and name.startswith("__"):
                continue

            if name == "debug_print":
                try:
                    raw_dbg = inspect.getattr_static(self, name)
                    if raw_dbg is DebugMixin.debug_print:
                        continue
                except Exception:
                    pass

            try:
                raw = inspect.getattr_static(self, name)
            except AttributeError:
                print(" " * (indent + 2) + f"{name}: <missing>")
                continue

            value: Any

            if isinstance(raw, MemberDescriptorType):
                try:
                    value = raw.__get__(self, t)
                except Exception as exc:
                    value = f"<slot read error {type(exc).__name__}: {exc}>"
            elif isinstance(raw, property):
                if eval_properties:
                    try:
                        value = raw.__get__(self, t)
                    except Exception as exc:
                        value = f"<property error {type(exc).__name__}: {exc}>"
                else:
                    value = raw
            else:
                value = raw

            is_primitive = isinstance(value, (int, float, str, bool, type(None)))
            rep = repr(value)
            rep = rep if len(rep) <= 80 else rep[:77] + "..."

            prefix = "" if is_primitive else f"{type(value).__name__} "
            print(" " * (indent + 2) + f"{name}: {prefix}{rep}")

            if (
                not is_primitive
                and not callable(value)
                and isinstance(value, DebugMixin)
            ):
                value.debug_print(
                    max_depth=max_depth,
                    _depth=_depth + 1,
                    _visited=_visited,
                    indent=indent + 4,
                    eval_properties=eval_properties,
                    show_dunder=show_dunder,
                )

        print(" " * indent + "}")
```

## Why this version is better

The repaired helper is stronger because it makes its observation policy explicit:

- discovery comes from `dir`
- default reads come from `inspect.getattr_static`
- property execution is opt-in
- slot values are handled deliberately
- recursion is bounded and cycle-aware

It is still not magic. It is just honest about what it is observing and when it crosses
into execution.

## What this example teaches about Module 02

This worked example ties the module together:

- names are not the same as stored state or resolved values
- dynamic reads execute runtime behavior
- static lookup is the right default for many tools
- callability still matters because recursion and display policy should not blindly invoke values
- disciplined observation is a workflow, not one builtin

That is the real win. A safer debug printer is just one concrete place where the module's
observation rules prove their value.

## The review loop to keep

When you inherit a runtime-inspection helper, run this loop:

1. identify whether it discovers names, reads state, or resolves values
2. mark every dynamic read that may execute code
3. move default inspection paths toward static lookup where appropriate
4. make evaluation, recursion, and display policy explicit

If you can do that here, Module 02 has done its job and Module 03 can build on a much
cleaner observation discipline.
