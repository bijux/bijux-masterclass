# Class Customization Boundaries

Module 06 is not only a collection of class-level tools. It is also a decision module.

By this point, the course has introduced several ways to change class behavior without
reaching for metaclasses:

- plain methods and constructors
- class decorators
- dataclasses
- properties
- descriptor-backed validation

The last core exists to ask the real design question:

> which of these is the smallest honest owner for the current invariant?

## The sentence to keep

When class-level behavior feels like it is escalating, ask:

> can this still stay explicit after class creation, or does the invariant truly require a
> lower-level attribute owner or class-creation control?

That question is the whole point of the module.

## Plain class code is still the first option

One of the easiest mistakes in metaprogramming work is skipping over the obvious option:

- a plain constructor
- a plain method
- a plain helper function

If explicit class code already makes the rule easy to see, that is often the best answer.

Metaprogramming does not win by default just because it is available.

## Class decorators are good for opt-in post-construction changes

Class decorators are strongest when:

- the class already exists
- the change is opt-in
- the transformation stays inspectable and reversible

They are weaker when the requirement depends on class-body-time control or deeper
attribute semantics.

## Dataclasses are excellent for generated boilerplate, not for broad policy

Dataclasses are a great answer when the real need is:

- generated constructors
- generated reprs
- generated equality behavior

They are a weak answer when people start assuming:

- runtime validation appears automatically
- deep immutability appears automatically
- every field policy belongs in dataclass flags

That is a good example of a tool being strong within one boundary and misleading outside
it.

## Properties are strongest at one attribute boundary

Properties are a good fit when:

- one field needs validation or computation
- one attribute should expose a controlled surface

They are a weaker fit when:

- many fields want the same rule
- the same invariant repeats across many classes

At that point a reusable descriptor may be the clearer owner.

## Descriptors are the next step, not the first reflex

This module introduces descriptor-backed validation carefully because descriptors are
stronger than properties in one important way:

- they can be reused across many attributes and classes

That is powerful. It is also why the course does not jump to them immediately.

If one property solves the problem honestly, stay there.

## Metaclasses should still be treated as a later escalation

A metaclass becomes worth considering only when the requirement truly depends on
class-creation-time control:

- namespace preparation
- creation-time registration rules
- logic that must run before or during class construction itself

If the behavior can still be expressed after class creation with the tools in this module,
that is usually the clearer design.

## One picture of the lower-power ladder

```text
Plain class code
  -> class decorator
  -> property or focused descriptor
  -> metaclass only when class-creation control is truly required
```

This is not a prestige ladder. It is a blast-radius ladder.

## Surface immutability is a good example of boundary pressure

Take "make this class frozen" as an example:

- plain code might already be enough for explicit APIs
- a class decorator can enforce surface immutability after creation
- deeper immutability is a much broader policy question

That is why the worked example stays carefully at surface immutability instead of
pretending to solve every mutability problem.

## Review rules for class customization boundaries

When reviewing a class-level design, keep these questions close:

- is plain explicit class code already enough?
- if not, is the change really post-construction, or does it need attribute-boundary or class-creation control?
- is one property enough, or is there now a repeated field rule that deserves a descriptor?
- are dataclass features being used for generation, or are they carrying broader policy than they should?
- has the design crossed the threshold where a metaclass is being proposed for prestige instead of necessity?

## What to practice from this page

Try these before moving on:

1. Take one class invariant and place it on the ladder: plain code, class decorator, property, descriptor, or metaclass.
2. Rewrite one over-engineered class rule downward to a lower-power tool.
3. Write one review note rejecting a metaclass because post-construction customization is still enough.

If those feel ordinary, the worked example can pressure-test this whole decision model
inside a minimal frozen class decorator.

## Continue through Module 06

- Previous: [Type Hints and Descriptor-Backed Validation](type-hints-and-descriptor-backed-validation.md)
- Next: [Worked Example: Building a Minimal `@frozen` Class Decorator](worked-example-building-a-minimal-frozen-class-decorator.md)
- Return: [Overview](index.md)
- Terms: [Glossary](glossary.md)
