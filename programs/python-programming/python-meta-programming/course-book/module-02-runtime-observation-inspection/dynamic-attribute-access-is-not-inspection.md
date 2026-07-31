# Dynamic Attribute Access Is Not Inspection


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Python Programming"]
  program["Python Meta-Programming"]
  section["Runtime Observation Inspection"]
  page["Dynamic Attribute Access Is Not Inspection"]
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

Module 02 becomes useful the moment one sentence lands:

> reading an attribute in Python is not automatically passive.

That is why this page matters. `getattr`, `setattr`, `delattr`, and `hasattr` are not
simple dictionary helpers. They participate in the full attribute protocol and can invoke
user-defined behavior.

If you have ever said "I was only checking whether the attribute exists," this is the page
that should interrupt that habit.

## The sentence to keep

When code uses dynamic attribute access, ask:

> is this trying to inspect structure, or is it intentionally participating in runtime
> behavior?

If the answer is "inspect structure," these tools are often too eager.

This page is deliberately repetitive about that boundary because the mistaken mental model
is strong:

- learners see a string attribute name and assume a simple dictionary lookup
- Python sees a protocol entry point and may run descriptors, hooks, or policy code

## These builtins are programmable dot syntax

The core builtins are close relatives of normal attribute syntax:

- `getattr(obj, name[, default])` corresponds to `obj.name`
- `setattr(obj, name, value)` corresponds to `obj.name = value`
- `delattr(obj, name)` corresponds to `del obj.name`
- `hasattr(obj, name)` effectively attempts a read and treats `AttributeError` as missing

That family resemblance is exactly why they are risky for observation. Dot syntax is not a
storage read; it is a protocol entry point.

That means dynamic attribute helpers are good when you actually want normal runtime
semantics. They are bad when your question is narrower than "please perform lookup as the
object defines it."

## The attribute protocol is the real story

When you do `getattr(obj, "x")`, Python may:

- invoke `obj.__getattribute__`
- consult descriptors on the class
- consult instance storage
- fall back to class attributes
- invoke `obj.__getattr__`

Any of those steps can run user code.

So a better review question is not "does `getattr` work?" but:

> do we really want normal runtime lookup here, or do we only want to inspect attachment
> structure without executing the object's behavior?

The same warning applies to writes and deletes:

- `setattr` may trigger `__setattr__` or descriptor `__set__`
- `delattr` may trigger `__delattr__` or descriptor `__delete__`

## One picture of the risk

```text
getattr(obj, "x")
  -> attribute protocol
     -> __getattribute__
     -> descriptor logic
     -> __getattr__
     -> proxy or wrapper code

setattr / delattr
  -> __setattr__ / __delattr__
  -> descriptor __set__ / __delete__
```

This is why Module 02 insists that dynamic access is behavior, not neutral inspection.

Keep this decision rule close:

| If you need to know... | Prefer... | Why |
| --- | --- | --- |
| whether a name is a candidate for lookup | `dir(obj)` | discovery stays lower-risk than resolution |
| whether state is locally stored | `vars(obj)` or storage inspection | asks the storage question directly |
| what object is attached before descriptors run | `inspect.getattr_static` | attachment truth without normal protocol execution |
| what runtime lookup actually produces | `getattr` | this is the honest moment to execute behavior |

## `getattr(..., default)` can hide two different situations

The optional default parameter looks convenient:

```python
value = getattr(obj, "name", None)
```

But the convenience hides an ambiguity.

The default is returned when `AttributeError` is raised, and that can mean:

- the attribute is truly missing
- the attribute exists, but its getter raised `AttributeError` internally

That ambiguity matters in real systems because it can turn internal failures into fake
"missing attribute" results.

```python
class AmbiguityDemo:
    @property
    def value(self):
        raise AttributeError("internal error")


obj = AmbiguityDemo()

try:
    getattr(obj, "value")
except AttributeError:
    print("Could be missing, or could be an internal getter failure.")
```

When the distinction matters, prefer explicit `try`/`except` around `getattr` without a
default and document what you mean by "missing."

Beginners often like the default form because it looks concise. The teaching problem is
that it also makes failures easier to misclassify. In reviewable tooling, honesty matters
more than brevity.

## `hasattr` is not safe probing

`hasattr(obj, "x")` is often treated like a harmless existence check. It is not.

It attempts attribute access and only converts `AttributeError` into `False`.

That means:

- it can execute descriptors and lookup hooks
- it can hide bugs where a getter mistakenly raises `AttributeError`
- it can still let non-`AttributeError` exceptions escape

```python
class Risky:
    @property
    def x(self):
        print("property executed")
        return 1


assert hasattr(Risky(), "x") is True
```

The printed line is the lesson. The existence check already executed runtime behavior.

That is why `hasattr` is often the wrong first tool for debugging helpers, serializers,
admin panels, or safety checks. It answers a broader question than those tools usually
intend to ask.

## `hasattr` does not swallow every failure

```python
class Explodes:
    @property
    def x(self):
        raise ValueError("boom")


# hasattr(Explodes(), "x") raises ValueError
```

This is another good reminder that `hasattr` is not separate from attribute lookup. It is
just a narrow wrapper around it.

The practical review rule is simple:

- if a failure should stay visible, `hasattr` is often too blunt
- if execution should be avoided, `hasattr` is already too eager
- if absence versus internal failure matters, `hasattr` is too lossy

## Dynamic mutation is still subject to object policy

Because `setattr` and `delattr` go through object policy, they are constrained by the
same runtime model as ordinary attribute syntax.

```python
class Slotted:
    __slots__ = ("x",)

    def __init__(self):
        self.x = 1


s = Slotted()
setattr(s, "x", 2)

try:
    setattr(s, "y", 3)
except AttributeError as exc:
    print("Expected:", exc)
```

The dynamic API did not bypass slots. It respected the storage and descriptor rules of
the object.

This is a healthy correction for another beginner myth: spelling the operation
dynamically does not make it lower-level or more powerful than the object model.

## A better helper keeps exceptions informative

When you need a helper around dynamic access, do not collapse every failure into "missing"
or "False."

For example:

```python
def try_get(obj, name):
    try:
        value = getattr(obj, name)
    except AttributeError as exc:
        return (False, exc)
    else:
        return (True, value)
```

That keeps the "attribute missing" path separate from other exceptions, which should
usually continue to surface as real failures rather than as inspection results.

## A realistic beginner lab

Before you move on, build one object that combines at least two of these:

- a property
- a custom `__getattr__`
- slot-backed storage
- a deliberate internal exception in a getter

Then answer four questions separately:

1. which names are discoverable?
2. which state is locally stored?
3. which lookup route executes behavior?
4. which helper form would most easily blur "missing" with "failed"?

If you cannot answer all four on one object, reread the page with that object open in a
scratch file. The module becomes much more durable when one concrete object carries the
whole boundary.

## Guided lab: make repeated execution countable

Run:

```console
$ python3 -m labs.runtime_observation |
  python3 -c 'import json, sys; print(json.load(sys.stdin)["dynamic_access"])'
{'hasattr_result': True, 'property_reads_after_dynamic_lookup': 1, 'property_reads_after_hasattr': 2, 'property_reads_after_static_lookup': 0, 'resolved_score': 7, 'static_lookup_returns_property': True}
```

`IncidentObservationTarget.risk_score` increments `_property_reads` every time the
property executes. Read the packet as an event sequence:

| Operation | Counter afterward | Boundary crossed |
| --- | ---: | --- |
| `inspect.getattr_static(target, "risk_score")` | 0 | attachment inspection only |
| `getattr(target, "risk_score")` | 1 | descriptor execution |
| `hasattr(target, "risk_score")` | 2 | descriptor execution again |

The counter turns "may execute" into observable evidence. `hasattr` did not protect the
later read; it performed another read of its own.

### Failure route

Change `risk_score` so it raises `RuntimeError`. `hasattr` will not convert that failure
to `False`; the exception escapes. Then change it to raise `AttributeError` and observe
the different result. Record why neither outcome means the property was safely inspected,
restore the baseline, and run `make observation-lab-test`.

### Transfer to the incident-plugin runtime

The capstone `invoke()` function uses:

```python
method = getattr(plugin, action_name)
return method(**kwargs)
```

That is an intentional behavioral route: it resolves a named action and calls it. A
debugger copying the same line merely to "see whether an action exists" would be using
the right mechanism for the wrong question. Module 02 asks you to identify the purpose
of the lookup before judging the builtin.

## Review mistakes this page should eliminate

These are the most common weak review comments this lesson should prevent:

| Weak comment | What it misses | Stronger comment |
| --- | --- | --- |
| "We only used `hasattr`, so this is safe." | `hasattr` already executes dynamic lookup. | "This helper is still executing lookup while probing for existence." |
| "`getattr(..., default)` handles missing values cleanly." | missing and internal `AttributeError` may be blurred together. | "The helper still needs to distinguish real absence from a failing getter." |
| "Dynamic access is fine because we are not mutating anything." | reads can still execute behavior. | "Even read-only dynamic access can trigger descriptors and fallback hooks." |
| "`setattr` is lower-level, so it bypasses the class policy." | dynamic mutation still respects slots and descriptor rules. | "`setattr` is still participating in the object's runtime policy." |

## Review rules for dynamic access

When reviewing code that uses these builtins, keep these questions close:

- is the code intentionally executing the attribute protocol, or does it only need observation?
- is `hasattr` hiding a more precise question that should be asked another way?
- does `getattr(..., default)` blur together true absence and internal getter failure?
- is the code assuming `setattr` or `delattr` bypass descriptor or slot policy when they do not?
- would static lookup or direct stored-state inspection answer the real question more honestly?

One final self-test:

> If a debug helper uses `hasattr(obj, name)` before `getattr(obj, name)`, has it really
> reduced risk, or has it simply executed lookup twice?

## What to practice from this page

Try these before moving on:

1. Write `try_get(obj, name)` so it separates missing attributes from successful reads.
2. Build one property that raises `AttributeError` internally and explain why
   `getattr(..., default)` becomes ambiguous.
3. Show one example where `hasattr` executes code and one where it lets a non-`AttributeError`
   exception escape.

If those feel ordinary, the next step is classification: when you inspect a value, what
kind of object is it really, and how exact does your type check need to be?

## Continue through Module 02

- Previous: [Visible Names and Stored State](visible-names-and-stored-state.md)
- Next: [Exactness and Polymorphism in Runtime Type Checks](exactness-and-polymorphism-in-runtime-type-checks.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
