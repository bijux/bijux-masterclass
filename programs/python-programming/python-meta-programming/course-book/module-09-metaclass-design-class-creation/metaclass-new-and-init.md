# Metaclass `__new__` and `__init__`

After resolution comes the next design question:

once the metaclass is in control, where should its work actually happen?

This core separates the two most commonly blurred hooks:

- metaclass `__new__`
- metaclass `__init__`

## The sentence to keep

Use metaclass `__new__` for structural decisions that must happen while the class is being
created, and use metaclass `__init__` for final bookkeeping or registration on the class
object after it already exists.

That split prevents a lot of vague metaclass code.

## What metaclass `__new__` owns

`__new__` receives the raw ingredients for class creation:

- the metaclass
- the class name
- the base classes
- the namespace mapping

That makes it the right place for work such as:

- namespace-driven validation
- injecting or rewriting attributes before the class object exists
- structural edits that depend on the class body itself

This is still the mutability window where the construction inputs are most direct.

## What metaclass `__init__` owns

`__init__` runs after the class object has been created.

That makes it a better fit for:

- registration
- final bookkeeping
- post-creation checks that need the finished class object

It is usually the wrong place for heavy structural surgery, because the class has already
been constructed.

## A compact split to keep in mind

```text
metaclass __new__
  -> shape the class

metaclass __init__
  -> record, register, or finalize the class
```

That is the practical rule most review discussions need.

## A small example

```python
class ValidatingMeta(type):
    registry = []

    def __new__(mcs, name, bases, namespace):
        has_run_here = "run" in namespace
        has_run_in_bases = any(hasattr(base, "run") for base in bases)
        if not has_run_here and not has_run_in_bases:
            raise TypeError(f"{name} must define run()")

        namespace["from_meta"] = lambda self: "ok"
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        ValidatingMeta.registry.append(cls)


class Task(metaclass=ValidatingMeta):
    def run(self):
        return "running"
```

This example keeps the split honest:

- `__new__` enforces a structural rule and injects behavior
- `__init__` records the finished class in a registry

That is exactly the division of labor the module wants.

## Why structural edits belong earlier

If a decision depends on the namespace before class creation finishes, `__new__` is the
honest owner.

Examples include:

- rejecting missing required methods
- rewriting definitions based on class-body declarations
- injecting class-level helpers before the resulting class is finalized

Trying to perform that kind of work later often makes the design harder to reason about.

## Why registration belongs later

Registration and bookkeeping usually need:

- the fully created class object
- its final bases and MRO
- a stable identity that other code can reference

That makes `__init__` the more natural place for:

- appending to registries
- recording metadata
- attaching class-family bookkeeping

The rule is not absolute, but it is a very strong default.

## What this split is trying to prevent

Without a clear split, metaclass code often turns into:

- structural mutation in `__init__`
- registration side effects mixed into `__new__`
- hard-to-review code that works mostly by accident

The point of this core is not stylistic purity. It is keeping class-creation behavior
explainable.

## A warning about overusing either hook

Both hooks are high-power surfaces.

That means both still need the same questions asked first:

- does this truly belong at class-creation time?
- could a class decorator still own it honestly?
- could plain explicit code be clearer?

Choosing between `__new__` and `__init__` is not the first question. It is the second.

## Review rules for `__new__` versus `__init__`

When reviewing metaclass hooks, keep these questions close:

- is this work structural or post-creation?
- does it depend on the raw namespace or the finished class object?
- is registration being kept separate from namespace mutation?
- is the metaclass doing work here that a lower-power tool could still own?
- would a reviewer be able to explain the class-creation effects in one pass?

## What to practice from this page

Try these before moving on:

1. Put one interface or namespace validation rule in `__new__` and explain why it belongs there.
2. Add one registry append in `__init__` and explain why it belongs after class creation.
3. Write one short review note rejecting a metaclass that mutates structure in `__init__` for no clear reason.

If those feel ordinary, the next step is `__prepare__`, the one hook that can observe and
control assignments during class body execution itself.
