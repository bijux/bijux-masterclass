# Exercise Answers

Use this page after attempting the exercises yourself. The goal is not to match every
example exactly. The goal is to compare your reasoning against answers that ask a precise
runtime question and then choose a tool that fits that question honestly.

## Answer 1: Separate visible names from stored state

Example answer:

```python
class Explorer:
    def __init__(self):
        self.instance_only = "personal"

    def method(self):
        return "ok"


obj = Explorer()
```

Strong evidence:

- `vars(obj) == {"instance_only": "personal"}`
- `"method" in dir(obj)` is `True`
- `"method" in vars(obj)` is `False`

Good conclusion:

`dir(obj)` discovers candidate names from instance, class, and MRO context. `vars(obj)`
shows only dictionary-backed stored state. Those are different questions and should not be
treated as interchangeable.

## Answer 2: Show that dynamic access is behavior

Example answer:

```python
class Risky:
    @property
    def value(self):
        print("property executed")
        return 10


obj = Risky()
```

Strong evidence:

- `getattr(obj, "value")` prints `property executed`
- `hasattr(obj, "value")` also prints `property executed`

Good conclusion:

Dynamic reads participate in the attribute protocol. They are not neutral inspection
because descriptors and hooks can execute code while the caller thinks it is only
"checking" an attribute.

## Answer 3: Choose the right type check

Example answer:

```python
from collections.abc import Iterable


def ensure_iterable(value):
    if isinstance(value, str):
        raise TypeError("strings are excluded")
    if not isinstance(value, Iterable):
        raise TypeError("expected an iterable")
    return iter(value)
```

Strong evidence:

- `isinstance([1, 2], Iterable)` is `True`
- rejecting `str` is a narrow rule layered on top of that broader capability check
- `type(True) is bool` is a good exact-type example when distinguishing `bool` from `int`

Good conclusion:

`isinstance` is usually the right default when the question is role compatibility.
`type(obj) is T` is right when the requirement truly depends on exact identity and should
reject subclasses.

## Answer 4: Prove what `callable()` does and does not promise

Example answer:

```python
class CallableThing:
    def __call__(self):
        return 1


class Plain:
    pass


callable_obj = CallableThing()
plain_obj = Plain()
plain_obj.__call__ = lambda: 1
```

Strong evidence:

- `callable(callable_obj)` is `True`
- `callable(plain_obj)` is `False`

Good conclusion:

Callability depends on the object's type-level protocol, not on an instance attribute with
the same name. A true result means only that the runtime permits a call attempt. It does
not guarantee valid arguments, safe execution, or success.

## Answer 5: Compare static and dynamic lookup directly

Example answer:

```python
import inspect


class Demo:
    @property
    def value(self):
        print("property executed")
        return 10


obj = Demo()
raw = inspect.getattr_static(obj, "value")
resolved = getattr(obj, "value")
```

Strong evidence:

- `raw` is the `property` object itself
- `resolved == 10`
- the dynamic read prints `property executed`

Good conclusion:

Static lookup better fits tooling when the goal is to inspect what is attached without
triggering behavior. Dynamic lookup is the right choice only when the tool intentionally
wants normal runtime semantics.

## Answer 6: Review a debug or inspection helper

Example answer:

Suppose the helper currently does this:

- discover names with `dir(obj)`
- read each value with `getattr(obj, name)`
- recurse into everything it prints

Strong diagnosis:

- `dir(obj)` is a discovery step
- `getattr(obj, name)` is dynamic resolution and may execute code
- naive recursion can amplify accidental execution and create cycles

Good repair:

- keep `dir(obj)` only for candidate names
- move default reads to `inspect.getattr_static`
- make property evaluation and recursion explicit opt-ins

That repair matches the module's main discipline: the tool should stay observational by
default and cross into execution only on purpose.

## What strong Module 02 answers have in common

Across the whole set, strong answers share the same habits:

- they state the observation question before choosing a builtin
- they separate discovery, storage inspection, classification, and value resolution
- they treat dynamic attribute access as execution-capable behavior
- they use static lookup when tooling needs attachment truth more than runtime behavior

If an answer still depends on "I just checked the attribute," revise it until you can say
what kind of observation or execution actually happened.
