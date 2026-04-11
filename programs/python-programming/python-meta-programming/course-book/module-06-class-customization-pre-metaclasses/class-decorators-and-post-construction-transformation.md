# Class Decorators and Post-Construction Transformation

Module 06 starts with the lowest-power class-wide customization tool in this part of the
course:

> a class decorator sees a fully created class object and returns the class or a
> replacement.

That timing matters because it tells you what a class decorator can still change and what
it cannot retroactively control.

## The sentence to keep

When reviewing a class decorator, ask:

> what is being changed after class creation, and is post-construction transformation still
> enough for this requirement?

That question is the gateway to the whole module.

## Class decorators run after the class exists

At the simplest level:

```python
def decorator(cls):
    ...
    return cls


@decorator
class C:
    ...
```

means:

```python
class C:
    ...


C = decorator(C)
```

The metaclass has already done its work. The class object already exists. The decorator is
now rewriting or extending that finished object.

## One picture of the timing

```mermaid
graph LR
  classStmt["class statement"]
  classObj["metaclass creates class object"]
  decorate["decorator(cls)"]
  rebound["name rebound to returned value"]
  classStmt --> classObj --> decorate --> rebound
```

Caption: class decorators see a completed class object; they do not participate in class-body namespace construction.

This timing is the most important boundary on the page.

## Method injection is a straightforward use

```python
def add_method(cls):
    def extra(self):
        return f"Extra from {cls.__name__}"

    cls.extra = extra
    return cls


@add_method
class Basic:
    def __init__(self, value):
        self.value = value
```

This is a good early example because it stays honest:

- the decorator changes the finished class
- the injected function becomes a descriptor when attached to the class
- nothing about class creation timing is being hidden

## Registration is another honest post-construction use

```python
registry = []


def register(cls):
    registry.append(cls)
    return cls


@register
class Registered:
    pass
```

This is often a reasonable use of a class decorator when:

- the registry is explicit
- reset behavior is testable
- the decorator does not pretend to be more than opt-in post-construction registration

That last point matters because registry behavior can drift upward quickly if it stops
being explicit.

## Returning a non-class is legal but usually costly

A class decorator can technically return something that is not a class at all:

```python
def replace_with_callable(cls):
    def proxy(*args, **kwargs):
        return f"Replaced {cls.__name__}; args={args}, kwargs={kwargs}"
    return proxy
```

This is legal. It also usually creates a bad surprise around:

- `isinstance` expectations
- tooling
- names that no longer clearly refer to classes

That does not make it impossible. It does make it something the design should justify
very strongly if used at all.

## Stacked class decorators still compose bottom-up

Like function decorators, stacked class decorators apply from the bottom up:

```python
@d2
@d1
class C:
    ...
```

means:

```python
class C:
    ...


C = d1(C)
C = d2(C)
```

That matters because each decorator receives the result of the previous one, not the raw
original class.

## What class decorators cannot do well

Because they run after class creation, class decorators are not the right tool when the
requirement depends on:

- controlling the class namespace while the body executes
- participating in metaclass resolution
- changing how descriptors receive `__set_name__`
- owning class-creation-time invariants that must run before the class exists

That is exactly why this module comes before the metaclass module. This boundary should
feel obvious, not mysterious.

## Review rules for class decorators

When reviewing a class decorator, keep these questions close:

- what post-construction transformation is it performing?
- does it return a class, or does it replace the binding with something more surprising?
- is registration or method injection explicit and resettable?
- is the decorator trying to solve a class-creation problem too late?
- would an explicit helper call be clearer than hiding the change in decorator syntax?

## What to practice from this page

Try these before moving on:

1. Implement a class decorator that injects one method and explain why the method still binds normally.
2. Implement a resettable registration decorator and explain why reset behavior matters.
3. Write down one class requirement that class decorators can solve honestly and one that already sounds like metaclass territory.

If those feel ordinary, the next step is dataclasses, where method generation and field
discovery automate class code without turning into metaclass control.

## Continue through Module 06

- Previous: [Overview](index.md)
- Next: [Dataclass Generation Boundaries](dataclass-generation-boundaries.md)
- Practice: [Exercises](exercises.md)
- Terms: [Glossary](glossary.md)
