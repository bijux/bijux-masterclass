# Manual Class Creation with `type(...)`

Module 09 starts by stripping away the `class` statement and looking at the class creation
primitive directly.

That matters because metaclasses are not a separate magical system. They are an extension
of the same class-construction story.

## The sentence to keep

`type(name, bases, namespace)` is the default class-construction primitive, and
understanding it makes metaclasses feel like control over class creation rather than like
mystical syntax.

That is the foundation for the rest of the module.

## What the three arguments mean

The shape is:

```python
type(name, bases, namespace)
```

and each part has a clear job:

- `name` becomes the class name
- `bases` defines inheritance and contributes to the MRO
- `namespace` provides the class attributes, methods, and metadata

That is enough to build a class object directly.

## A compact example

```python
def make_greeter_class(class_name, greeting):
    def greet(self):
        return f"{greeting} from {self.__class__.__name__}"

    namespace = {
        "__doc__": f"{class_name} created with type()",
        "greet": greet,
        "kind": "generated",
    }
    return type(class_name, (object,), namespace)


Hello = make_greeter_class("Hello", "Hi")
instance = Hello()

print(instance.greet())  # Hi from Hello
print(Hello.kind)        # generated
```

This example is small, but it already shows the main point:

class creation is something Python can perform from data.

## Why this matters before metaclasses

Metaclasses only make sense once you see that class creation is already a runtime action.

If a class can be created from:

- a name
- base classes
- a namespace mapping

then a metaclass is a way to intercept or customize that process.

That is much easier to reason about than “metaclasses are the class of a class” by itself.

## The namespace is not just a bag of attributes

The `namespace` argument is where the future class body lands conceptually:

- methods
- constants
- descriptors
- documentation
- special names such as `__module__`

This matters because later hooks such as metaclass `__new__` and `__prepare__` are really
about controlling or observing that namespace at the right time.

## A note about `__module__`

A `class` statement fills in `__module__` automatically.

When calling `type(...)` directly, you should set it yourself if you care about:

- debugging and reprs
- pickling
- documentation surfaces

For example:

```python
def make_class_in_module(name, module):
    namespace = {
        "__module__": module,
        "value": 1,
    }
    return type(name, (object,), namespace)
```

This is a small detail, but it keeps dynamic classes from feeling half-formed.

## Why `type(...)` is still lower-power than a custom metaclass

Manual `type(...)` creation is dynamic, but it is still explicit and local:

- one class is being created
- the caller owns the whole construction site
- there is no automatic effect on future subclasses

That makes it a lower-power tool than a metaclass, even though both participate in class
creation.

## What this page is really teaching

The lesson is not “build classes dynamically all the time.”

The lesson is:

- class creation is a runtime event
- class objects can be built explicitly
- metaclasses only make sense as control over that event

Once that is clear, the rest of Module 09 becomes much less mystical.

## Review rules for manual class creation

When reviewing code that uses `type(...)`, keep these questions close:

- why is the class being built dynamically at all?
- are the bases and namespace explicit enough to inspect?
- does the class need `__module__` or other metadata set manually?
- would a plain `class` statement still be clearer if no true dynamic construction is needed?
- is this dynamic class creation staying local, or is it drifting toward a metaclass-level concern?

## What to practice from this page

Try these before moving on:

1. Build one tiny class with `type(...)` and explain which part of the tuple or namespace produced each visible behavior.
2. Add `__module__` manually and explain why it matters for dynamic classes.
3. Write one sentence explaining why `type(...)` is still lower-power than a custom metaclass.

If those feel ordinary, the next step is metaclass resolution: how Python chooses a
metaclass, when the work runs, and why conflicts appear.

## Continue through Module 09

- Previous: [Overview](index.md)
- Next: [Metaclass Resolution, Timing, and Conflicts](metaclass-resolution-timing-and-conflicts.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
