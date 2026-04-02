<a id="top"></a>
# Module 06: Class Customization Before Metaclasses


<!-- page-maps:start -->
## Module Position

```mermaid
flowchart TD
  family["Python Programming"] --> program["Python Metaprogramming"]
  program --> module["Module 06: Class Customization Before Metaclasses"]
  module --> lessons["Lesson pages and worked examples"]
  module --> checkpoints["Exercises and closing criteria"]
  module --> capstone["Related capstone evidence"]
```

```mermaid
flowchart TD
  purpose["Start with the module purpose and main questions"] --> lesson_map["Use the lesson map to choose reading order"]
  lesson_map --> study["Read the lessons and examples with one review question in mind"]
  study --> proof["Test the idea with exercises and capstone checkpoints"]
  proof --> close["Move on only when the closing criteria feel concrete"]
```
<!-- page-maps:end -->

Read the first diagram as a placement map: this page sits between the course promise, the lesson pages listed below, and the capstone surfaces that pressure-test the module. Read the second diagram as the study route for this page, so the diagrams point you toward the `Lesson map`, `Exercises`, and `Closing criteria` instead of acting like decoration.

<a id="toc"></a>
## Table of Contents

1. [Introduction](#introduction)
2. [Visual: Tooling Power Ladder](#visual)
3. [Core 1: Class Decorators — Transformation Post-Construction](#core26)
4. [Core 2: `@dataclass` Dissected — What It Generates (and What It Doesn’t)](#core27)
5. [Core 3: `@property` / `.setter` / `.deleter` — The Friendly Face of Descriptors](#core28)
6. [Core 4: Runtime Type Hints as a Declarative Aid for Attribute Validation](#core29)
7. [Capstone: `@frozen` — Surface Immutability + Optional Validation](#capstone)
8. [Learning outcomes](#learning-outcomes)
9. [Common failure modes](#common-failure-modes)
10. [Exercises](#exercises)
11. [Self-test](#self-test)
12. [Closing criteria](#closing-criteria)
13. [Power Ladder Checkpoint](#power-checkpoint)
14. [Glossary (Module 6)](#glossary)

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="introduction"></a>
## Introduction

This module is the bridge between function-level wrappers and the deeper attribute
machinery that follows. The through-line is simple: before you reach for descriptors or
metaclasses, you need to know how much control a fully created class already gives you.
Class decorators, `@dataclass`, `@property`, and shallow type-hint-driven validation cover
more ground than many meta-heavy designs admit.

That makes this module a discipline check as much as a mechanics lesson. The aim is not
to collect class tricks. The aim is to learn where class customization can stay explicit,
local, and reversible before the course moves into descriptor-level control.

Keep one question in view while reading:

> Can this class-level behavior stay honest after class creation, or am I already pushing toward descriptor or metaclass territory?

The answer matters because the capstone uses all three boundaries in different places:
wrappers on actions, descriptors on configuration fields, and a metaclass on plugin
registration. This module is where those ownership lines start becoming visible.

Design stance:

> Prefer class decorators, properties, descriptors, or explicit helpers over custom `__setattr__`.
> Reach for higher-power hooks only when the lower one cannot own the invariant cleanly.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="visual"></a>
## Visual: Tooling Power Ladder

```mermaid
graph TD
  four["4. Metaclasses<br/>class creation pipeline"]
  three["3. Class decorators<br/>post-construction rewrite"]
  two["2. Descriptors or `@property`<br/>per-attribute semantics"]
  one["1. Plain code<br/>prefer when possible"]
  four --> three --> two --> one
```

Caption: Choose the lowest-power tool that solves the problem.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="core26"></a>
## Core 1: Class Decorators — Transformation Post-Construction

### Definition

A **class decorator** is any callable that takes a class object and returns a replacement:

```python
def identity_decorator(cls):
    """Placeholder decorator that returns the class unchanged (for demonstration)."""
    return cls

@identity_decorator
class C:
    ...
```

is exactly:

```python
def identity_decorator(cls):
    """Placeholder decorator that returns the class unchanged (for demonstration)."""
    return cls

class C:
    ...
C = identity_decorator(C)
```

It runs **after** the metaclass has created the class: bases, MRO, and class namespace are already fixed.

### Visual: Class Definition Pipeline (simplified)

```mermaid
graph LR
  plain["Plain class statement<br/>`class C: ...`"]
  metaPlain["Metaclass creates class"]
  bound["Class object bound to `C`"]
  decorated["Decorated class statement<br/>`@decorator` then `class C: ...`"]
  metaDecorated["Metaclass creates class"]
  rewrite["`C = decorator(C)`"]
  returned["Finished class returned"]
  plain --> metaPlain --> bound
  decorated --> metaDecorated --> rewrite --> returned
```

Caption: Class decorators run after the metaclass; they see a fully formed class.

### Example 1: Method injection

```python
def add_method(cls):
    def extra(self):
        return f"Extra from {cls.__name__}"
    cls.extra = extra  # function becomes a descriptor on the class
    return cls

@add_method
class Basic:
    def __init__(self, value):
        self.value = value

b = Basic(42)
print(b.extra())  # Extra from Basic
```

### Example 2: Registration

```python
registry = []

def register(cls):
    registry.append(cls)
    return cls

@register
class Registered:
    pass

print([c.__name__ for c in registry])  # ['Registered']
```

### Example 3: Replacing the binding (legal, usually a bad idea)

```python
def replace_with_callable(cls):
    def proxy(*args, **kwargs):
        return f"Replaced {cls.__name__}; args={args}, kwargs={kwargs}"
    return proxy

@replace_with_callable
class Replaced:
    pass

print(Replaced(1, 2))  # Replaced Replaced; args=(1, 2), kwargs={}
```

Rule of thumb: returning a non-class breaks `isinstance` expectations and tooling. Avoid unless you *want* the name to stop being a class.

### Visual: Decorator stacking order

```mermaid
graph TD
  d2["`@d2`"]
  d1["`@d1`"]
  klass["`class C: ...`"]
  applied["`C = d2(d1(C))`"]
  d2 --> d1 --> klass --> applied
```

Caption: Decorators are applied bottom-up: inner first, outer last.

### Exercise

Implement `@log_attributes` that wraps `__setattr__`:

* logs only public assignments (skip names starting with `_`)
* affects only that decorated class (no global patching)

<span style="font-size: 1em;">[Back to top](#top)</span>

---

## Core 2: `@dataclass` Dissected — What It Generates (and What It Doesn’t) { #core27 }

### What `@dataclass` does

`dataclasses.dataclass` inspects annotations and generates (depending on options):

* `__init__`
* `__repr__`
* `__eq__` (and optionally ordering)
* `__hash__` under certain rules
* calls `__post_init__` if present

Crucially: **it does not enforce types at runtime**.

### Visual: What `@dataclass` synthesizes

```mermaid
graph TD
  annotations["Annotations and defaults"]
  fields["Field discovery"]
  init["`__init__`"]
  repr["`__repr__`"]
  eq["`__eq__` and optional ordering"]
  hash["`__hash__` depending on `frozen`, `eq`, and `unsafe_hash`"]
  post["Optional `__post_init__` hook"]
  annotations --> fields
  fields --> init
  fields --> repr
  fields --> eq
  fields --> hash
  fields --> post
```

Caption: `@dataclass` generates boilerplate from declarative hints.

### Example: Defaults and `default_factory`

```python
from dataclasses import dataclass, field

@dataclass(kw_only=True)
class Employee:
    name: str
    id: int = field(default=0, repr=False)
    dept: str = field(default_factory=lambda: "Unknown")

e = Employee(name="Alice", dept="HR")
print(e)  # Employee(name='Alice', dept='HR')
```

### Example: Frozen + slots

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
print(p)  # Point(x=1.0, y=2.0)

try:
    p.x = 3.0
except Exception as e:
    print("Expected:", type(e).__name__, e)
```

### Minimal emulation (for understanding only)

```python
import inspect
from typing import get_type_hints

def manual_dataclass(cls):
    hints = get_type_hints(cls)
    fields = [n for n in hints if not n.startswith("_")]
    defaults = {n: cls.__dict__[n] for n in fields if n in cls.__dict__}

    # required-before-optional rule
    seen_optional = False
    for n in fields:
        if n in defaults:
            seen_optional = True
        elif seen_optional:
            raise TypeError(f"Required field '{n}' cannot follow optional fields")

    params = []
    for n in fields:
        default = defaults[n] if n in defaults else inspect.Parameter.empty
        params.append(
            inspect.Parameter(
                n,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                annotation=hints[n],
                default=default,
            )
        )
    user_sig = inspect.Signature(params)

    def __init__(self, *args, **kwargs):
        bound = user_sig.bind(*args, **kwargs)
        bound.apply_defaults()
        for name, value in bound.arguments.items():
            setattr(self, name, value)

    __init__.__signature__ = inspect.Signature(
        [inspect.Parameter("self", inspect.Parameter.POSITIONAL_OR_KEYWORD)] + params
    )
    cls.__init__ = __init__

    def __repr__(self):
        body = ", ".join(f"{n}={getattr(self, n)!r}" for n in fields)
        return f"{cls.__name__}({body})"
    cls.__repr__ = __repr__

    return cls

@manual_dataclass
class ManualPoint:
    x: int
    y: int = 0

mp = ManualPoint(5)
print(mp)  # ManualPoint(x=5, y=0)
print(inspect.signature(ManualPoint.__init__))  # (self, x: int, y: int = 0)
```

### Exercise

Write `@small_dataclass` that:

* generates only `__init__` + `__repr__`
* no inheritance support
* rejects >10 fields

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="core28"></a>
## Core 3: `@property` / `.setter` / `.deleter` — The Friendly Face of Descriptors

### Correct semantics (precise)

A `property` is a **descriptor stored on the class**.

* `instance.attr` triggers `__get__`
* `instance.attr = v` triggers `__set__`
* `del instance.attr` triggers `__delete__`

#### Critical correction: `property` is a **data descriptor**

Even without a user-defined setter, `property` defines `__set__` (it raises), so it **wins over** `instance.__dict__` during lookup and **cannot be shadowed**.

### Visual: Attribute lookup precedence (obj.x)

```text
Attribute Lookup Precedence (obj.x)

1. Data descriptor on type(obj)? (defines __set__ or __delete__)
   → descriptor.__get__(obj, type(obj))                WINNER

2. "x" in obj.__dict__?
   → return instance value

3. Non-data descriptor on type(obj)? (only __get__)
   → descriptor.__get__(obj, type(obj))

4. Plain class attribute?
   → return that value

5. __getattr__ fallback or AttributeError

Caption: @property is a data descriptor even without a setter → cannot be shadowed by obj.x = value.
```

### Example 1: Standard property with validation

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius must be non-negative")
        self._radius = value

c = Circle(5)
print(c.radius)  # 5
c.radius = 10
print(c.radius)  # 10

try:
    c.radius = -1
except ValueError as e:
    print("Expected:", e)
```

### Example 2: Subclass extending a base property (correct pattern)

```python
class Base:
    @property
    def value(self):
        return 42

class Sub(Base):
    @Base.value.getter
    def value(self):
        return getattr(self, "_value", super().value)

    @Base.value.setter
    def value(self, v):
        self._value = v

s = Sub()
print(s.value)  # 42
s.value = 100
print(s.value)  # 100
```

### Example 3: Read-only property is NOT shadowable

```python
class ReadOnly:
    @property
    def x(self):
        return 123

r = ReadOnly()
print(r.x)  # 123

try:
    r.x = "shadow?"
except AttributeError as e:
    print("Expected:", e)

r.__dict__["x"] = "forced"
print(r.__dict__["x"])  # forced
print(r.x)              # 123 (property wins)
```

### Example 4: A true non-data descriptor (shadowable)

```python
class NonData:
    def __init__(self, func):
        self.func = func
        self.__doc__ = getattr(func, "__doc__", None)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.func(obj)

class Shadowable:
    @NonData
    def computed(self):
        return "computed"

sh = Shadowable()
print(sh.computed)  # computed
sh.computed = "shadow"
print(sh.computed)  # shadow
print(sh.__dict__["computed"])  # shadow
```

### Visual: `@property` is descriptor sugar

```text
@property is Descriptor Sugar

@property
def x(self): ...

is conceptually:

x = property(fget=x)

Then:

@x.setter
def x(self, v): ...
      ↓
x = x.setter(new_fset)

Each decorator returns a new property object.
Chaining builds the full descriptor.
```

Caption: Property chaining reuses and extends the original property instance.

### Exercise

Implement a minimal cached-property-like descriptor:

* computes once
* stores into `obj.__dict__[name]`
* subsequent access returns cached value
* include a `reset(obj)` method on the descriptor

<span style="font-size: 1em;">[Back to top](#top)</span>

---

## Core 4: Runtime Type Hints as a Declarative Aid for Attribute Validation { #core29 }

### Key point

`get_type_hints(MyClass)` returns resolved annotations. They do nothing unless you enforce them.

We implement:

* minimal `_is_instance` (Any, Union/Optional, plain runtime classes)
* a `TypedDescriptor` that validates on assignment
* per-class hint caching

### Visual: Typing bridge data flow

```mermaid
graph TD
  classDef["Class definition"]
  annotations["Annotations"]
  hints["`get_type_hints(Class)`"]
  cache["Hints cached on class"]
  validate["Descriptor `__set__` validates incoming value"]
  store["Store into private slot or key"]
  classDef --> annotations --> hints --> cache --> validate --> store
```

Caption: Hints are resolved once; descriptors enforce shallow runtime checks.

### Minimal `_is_instance` (deliberately limited)

```python
from typing import Any, Union, get_args, get_origin

def _is_instance(value, hint) -> bool:
    if hint is Any:
        return True

    origin = get_origin(hint)

    if origin is Union:
        return any(_is_instance(value, h) for h in get_args(hint))

    if origin is not None:
        raise NotImplementedError(f"Generic validation not supported: {hint!r}")

    try:
        return isinstance(value, hint)
    except TypeError as e:
        raise NotImplementedError(f"Unsupported hint: {hint!r}") from e
```

### Typed descriptor with per-class cached hints

```python
import sys
from typing import get_type_hints

class TypedDescriptor:
    def __set_name__(self, owner, name):
        self.public_name = name
        self.storage_name = f"_{name}"

        if not hasattr(owner, "_field_hints_cache"):
            owner._field_hints_cache = get_type_hints(
                owner,
                globalns=vars(sys.modules[owner.__module__]),
                localns=dict(owner.__dict__),
            )

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage_name)

    def __set__(self, obj, value):
        hints = obj.__class__._field_hints_cache
        expected = hints.get(self.public_name)

        if expected is not None and not _is_instance(value, expected):
            raise TypeError(f"{self.public_name}={value!r} expected {expected!r}")

        setattr(obj, self.storage_name, value)

class TypedClass:
    x: int = TypedDescriptor()
    y: str = TypedDescriptor()

tc = TypedClass()
tc.x = 42
tc.y = "ok"
print(tc.x, tc.y)  # 42 ok

try:
    tc.x = "oops"
except TypeError as e:
    print("Expected:", e)
```

### Exercise

Extend `TypedDescriptor` to support `Annotated[T, validator1, ...]`:

* validate base `T`
* then apply validators sequentially

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="capstone"></a>
## Capstone: `@frozen` — Surface Immutability + Optional Validation

A minimal frozen-class decorator that:

* reads fields from annotations
* generates `__init__`, `__repr__`
* optionally `__eq__` and `__hash__`
* enforces surface immutability via `__setattr__`/`__delattr__`
* optionally validates constructor args

### Visual: `@frozen` synthesizes

```mermaid
graph TD
  frozen["`@frozen(validate=?, eq=?)`"]
  hints["1. `get_type_hints(cls)`"]
  fields["2. collect fields and defaults"]
  signature["3. build user signature"]
  init["Generate `__init__` with optional validation and storage"]
  repr["Generate `__repr__`"]
  equality["Generate optional `__eq__` and `__hash__`"]
  immutability["Generate frozen `__setattr__` and `__delattr__` that raise"]
  frozen --> hints --> fields --> signature
  signature --> init
  signature --> repr
  signature --> equality
  signature --> immutability
```

Caption: Minimal frozen dataclass-like behavior via a class decorator.

### Implementation

```python
import inspect
from typing import Callable, get_type_hints

def frozen(*, eq: bool = True, validate: bool = False) -> Callable[[type], type]:
    def decorator(cls: type) -> type:
        hints = get_type_hints(cls)
        fields = [n for n in hints if not n.startswith("_")]
        defaults = {n: cls.__dict__[n] for n in fields if n in cls.__dict__}

        seen_optional = False
        for n in fields:
            if n in defaults:
                seen_optional = True
            elif seen_optional:
                raise TypeError(f"Required field '{n}' cannot follow optional fields")

        user_params = []
        for n in fields:
            default = defaults[n] if n in defaults else inspect.Parameter.empty
            user_params.append(
                inspect.Parameter(
                    n,
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=hints[n],
                    default=default,
                )
            )

        user_sig = inspect.Signature(user_params)

        def __init__(self, *args, **kwargs):
            bound = user_sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for name, value in bound.arguments.items():
                if validate:
                    expected = hints.get(name)
                    if expected is not None and not _is_instance(value, expected):
                        raise TypeError(f"{name}={value!r} expected {expected!r}")
                object.__setattr__(self, name, value)

        __init__.__signature__ = inspect.Signature(
            [inspect.Parameter("self", inspect.Parameter.POSITIONAL_OR_KEYWORD)] + list(user_params)
        )
        cls.__init__ = __init__
        cls.__signature__ = user_sig

        def __repr__(self):
            body = ", ".join(f"{n}={getattr(self, n)!r}" for n in fields)
            return f"{cls.__name__}({body})"
        cls.__repr__ = __repr__

        if eq:
            def __eq__(self, other):
                if type(self) is not type(other):
                    return NotImplemented
                return all(getattr(self, n) == getattr(other, n) for n in fields)

            def __hash__(self):
                return hash(tuple(getattr(self, n) for n in fields))

            cls.__eq__ = __eq__
            cls.__hash__ = __hash__

        def __setattr__(self, name, value):
            raise TypeError(f"{cls.__name__} is frozen; cannot set {name!r}")

        def __delattr__(self, name):
            raise TypeError(f"{cls.__name__} is frozen; cannot delete {name!r}")

        cls.__setattr__ = __setattr__
        cls.__delattr__ = __delattr__

        return cls
    return decorator


@frozen(validate=True)
class FrozenPoint:
    x: float
    y: float = 0.0

p = FrozenPoint(1.5)
print(p)  # FrozenPoint(x=1.5, y=0.0)

print(inspect.signature(FrozenPoint))          # (x: float, y: float = 0.0)
print(inspect.signature(FrozenPoint.__init__)) # (self, x: float, y: float = 0.0)

try:
    p.x = 2.0
except TypeError as e:
    print("Expected:", e)

try:
    FrozenPoint("x")
except TypeError as e:
    print("Expected:", e)
```

<a id="learning-outcomes"></a>
## Learning outcomes

By the end of this module, you should be able to:

- Explain when a class decorator is enough and when the invariant really belongs to a descriptor or metaclass.
- Predict what `@dataclass` generates, what it leaves alone, and where `frozen=True` or `slots=True` change the surface area.
- Describe why `property` is still a descriptor and why read-only properties still win over instance dictionaries.
- Use type hints as an opt-in runtime aid without overstating them as full runtime type enforcement.
- Build a small class-level abstraction that stays reversible, explicit, and inspectable.

<a id="common-failure-modes"></a>
## Common failure modes

- Using a class decorator to smuggle in behavior that really depends on per-attribute lookup rules; that is usually descriptor territory.
- Treating `@dataclass` as "automatic validation" when it only generates methods and honors the rules you configure.
- Forgetting that `property` is a data descriptor even without a user-defined setter, which leads to wrong shadowing assumptions.
- Recomputing `typing.get_type_hints` on every assignment instead of caching the resolved hints per class.
- Calling a class "frozen" while still exposing nested mutable state that can be mutated through existing references.

<a id="exercises"></a>
## Exercises

- Write a `@registered(kind)` class decorator that records classes in a resettable registry without changing construction semantics.
- Compare a plain class, a `@dataclass`, and the module's `@frozen` capstone for the same model type; document what each version generates and forbids.
- Replace a hand-written validating `__setattr__` with one `property` and one descriptor-based field, then explain which boundary became clearer.
- Add an `Annotated[...]` metadata parser to the runtime hint example, but keep the failure message explicit about which cases remain unsupported.

<a id="self-test"></a>
## Self-test

- Can you explain why a class decorator cannot participate in declaration-time namespace control?
- Can you point to one invariant in your own codebase that belongs on an attribute boundary instead of inside `__setattr__`?
- Can you explain the difference between surface immutability and deep immutability without hand-waving?
- Can you show which parts of a dataclass are generated code and which parts still come from the class body you wrote?

<a id="closing-criteria"></a>
## Closing criteria

You are ready for Module 7 when you can take a class customization requirement and place it honestly on the power ladder:

- Stay with plain class code when explicit methods already make the rule clear.
- Use a class decorator when the change happens after class creation and remains opt-in.
- Use `property` or a descriptor when the invariant belongs to a field boundary and must participate in attribute lookup.
- Escalate beyond this module only when you can explain why post-construction customization is no longer enough.

<a id="power-checkpoint"></a>
## Power Ladder Checkpoint

- Stay with plain classes when explicit methods and constructors already make the rule obvious.
- Use a class decorator when the change happens after class creation and does not need to infect subclasses automatically.
- Use `property` or a light descriptor when the invariant belongs to one attribute boundary rather than the whole class-creation pipeline.
- Do not escalate to metaclasses when post-construction transformation, registration, or validation already works with class decorators and descriptors.
- Re-check the [Runtime Power Ladder](../reference/runtime-power-ladder.md) before treating class customization as a reason to reach for a metaclass.

<span style="font-size: 1em;">[Back to top](#top)</span>

---

<a id="glossary"></a>
## Glossary (Module 6)

| Term                                      | Definition                                                                                                                                                                   |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Class decorator**                       | Callable that takes a fully-created class and returns a replacement; `@d class C: ...` desugars to `C = d(C)`.                                                               |
| **Post-construction transformation**      | Modification stage after metaclass/class creation; bases, MRO, and initial namespace already exist.                                                                          |
| **Binding replacement**                   | Class decorator returns a non-class (e.g., proxy function) under the original name; legal but breaks `isinstance` expectations and tooling assumptions.                      |
| **Method injection**                      | Adding functions/attributes onto the class inside a class decorator; injected functions become descriptors (bind as methods when accessed from instances).                   |
| **Registration decorator**                | Class decorator that records class objects into a registry for discovery, typically deterministic and resettable for tests.                                                  |
| **Decorator stacking order**              | Multiple class decorators apply bottom-up: `@d2 @d1 class C` becomes `C = d2(d1(C))`.                                                                                        |
| **`dataclasses.dataclass`**               | Standard-library class decorator that generates boilerplate (`__init__`, `__repr__`, `__eq__`, ordering, hashing rules, `__post_init__` hook) from annotations and defaults. |
| **Dataclass field discovery**             | Process of reading class annotations + defaults (including `field(default_factory=...)`) to define generated init parameters and repr/eq behavior.                           |
| **`default_factory`**                     | Dataclass field option producing a fresh default value per instance (avoids shared mutable defaults).                                                                        |
| **Frozen dataclass**                      | Dataclass mode (`frozen=True`) that blocks attribute rebinding after initialization (surface immutability).                                                                  |
| **Slots dataclass**                       | Dataclass mode (`slots=True`) that generates a slotted class (no per-instance `__dict__` unless requested), reducing memory and limiting dynamic attrs.                      |
| **`__post_init__`**                       | Dataclass hook called after the generated `__init__` assigns fields; used for derived fields or validation.                                                                  |
| **Descriptor**                            | Object defining `__get__` and optionally `__set__` / `__delete__`, participating in attribute access semantics when stored on a class.                                       |
| **Descriptor protocol**                   | The rules by which attribute access on instances/types calls descriptor methods (`__get__`, `__set__`, `__delete__`) instead of returning raw objects.                       |
| **`property`**                            | Built-in descriptor wrapping fget/fset/fdel; created by `property(fget, fset, fdel, doc)` and typically via `@property` / `.setter` / `.deleter`.                            |
| **Data descriptor**                       | Descriptor that defines `__set__` or `__delete__` (or both); wins over `obj.__dict__` during lookup.                                                                         |
| **Non-data descriptor**                   | Descriptor that defines only `__get__`; can be shadowed by an instance attribute of the same name.                                                                           |
| **Read-only property semantics**          | Even without a user setter, `property` is still a data descriptor (its `__set__` raises), so it cannot be shadowed by `obj.__dict__`.                                        |
| **Subclass property extension**           | Pattern of reusing a base property via `@Base.prop.getter` / `.setter` to extend behavior while keeping descriptor identity coherent.                                        |
| **`__set_name__`**                        | Descriptor hook called at class creation time with `(owner, name)`; used to capture the public name and compute storage keys.                                                |
| **Typed descriptor**                      | Descriptor that validates values in `__set__` using type hints (or validators) and stores validated data under a private name/slot.                                          |
| **Typing bridge**                         | Use of `typing.get_type_hints(cls)` as a declarative schema for shallow runtime checks (opt-in enforcement, not automatic).                                                  |
| **`typing.get_type_hints`**               | Resolves annotations (including forward refs) into runtime objects using provided globals/locals; may evaluate strings.                                                      |
| **Per-class hint cache**                  | Storing resolved hints on the class (e.g., `_field_hints_cache`) so enforcement doesn’t recompute hints per assignment/call.                                                 |
| **Shallow runtime validation**            | Limited runtime checking typically supporting plain classes, `Union`/`Optional`, and `Any`; refuses generics like `list[int]` unless implemented explicitly.                 |
| **`Annotated` (typing)**                  | Hint wrapper carrying metadata (`Annotated[T, ...]`); enforcement requires explicitly parsing metadata and applying validators.                                              |
| **Surface immutability**                  | Blocking attribute rebinding/deletion via `__setattr__`/`__delattr__`; does not freeze nested mutable objects.                                                               |
| **Frozen class decorator (`@frozen`)**    | Class decorator that synthesizes `__init__`/`__repr__` (and optionally `__eq__`/`__hash__`) and prevents further attribute mutation at the surface.                          |
| **`object.__setattr__`**                  | Bypasses custom `__setattr__` in controlled contexts (e.g., inside `__init__` of a frozen class) to perform assignments reliably.                                            |
| **Prefer descriptors over `__setattr__`** | Policy stance: use properties/descriptors/class decorators for localized semantics; override `__setattr__` only as a last resort due to global, hard-to-debug side effects.  |

Proceed to **Module 7: The Descriptor Protocol — The True Engine (Part 1)**.

<span style="font-size: 1em;">[Back to top](#top)</span>
