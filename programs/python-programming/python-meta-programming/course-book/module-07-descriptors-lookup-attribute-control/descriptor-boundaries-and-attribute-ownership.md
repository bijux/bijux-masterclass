# Descriptor Boundaries and Attribute Ownership

This final core is the design page for the module.

By now the mechanics are visible. The remaining question is the one that matters in real
reviews:

when does attribute behavior truly belong to a descriptor?

## The sentence to keep

Use a descriptor when the invariant belongs to attribute access itself and needs the same
field-level behavior across multiple instances or classes; stay with lower-power tools
when the rule is narrower or more explicit there.

That is the boundary Module 07 is really teaching.

## The lower-power ladder

A useful review ladder for this module is:

```text
plain attribute or method
  -> property for one local attribute boundary
  -> reusable descriptor for repeated field semantics
  -> wider class hooks or metaclasses only when attribute-level ownership is no longer enough
```

This is not a prestige ladder. It is an ownership ladder.

## Properties are still descriptors, but they solve a narrower problem

A property is often the better choice when:

- one attribute on one class needs validation or computation
- reuse pressure is low
- the class should keep the rule close to one specific field

That means Module 07 is not replacing properties. It is showing when a more reusable
descriptor becomes the clearer owner.

## Reusable descriptors earn their complexity through repetition

A dedicated descriptor starts making sense when:

- the same field rule repeats across several attributes
- the same field rule repeats across several classes
- consistent class-level declaration improves readability

If those conditions are missing, a property may still be the simpler and more honest
design.

## Descriptors versus `__setattr__`

One common escalation mistake is solving field-specific rules by overriding
`__setattr__`.

That centralizes logic for every attribute in one place, which often makes the design:

- harder to review
- harder to test
- harder to extend without unintended interactions

Descriptors keep ownership local to each attribute boundary. That locality is one of their
biggest strengths.

## Descriptors versus wrappers

Wrappers own call boundaries.

Descriptors own attribute boundaries.

That sounds simple, but it prevents a lot of category mistakes. If the behavior is about:

- reading a value
- writing a value
- deleting a value

then a descriptor may be the right owner.

If the behavior is about:

- entering a function call
- retrying, caching, timing, or logging a call

then a wrapper is probably the clearer owner.

## Descriptors versus metaclasses

Descriptors do not control class creation.

Metaclasses do.

That means you should resist metaclass escalation when the real problem is still:

- field validation
- coercion on assignment
- reusable attribute semantics

Those are strong descriptor cases, not class-creation cases.

## A useful negative test

Before choosing a descriptor, ask:

```text
Would this still read naturally if I described it as "behavior of this attribute"?
```

If yes, a descriptor may be a good fit.

If the explanation immediately turns into:

- object-wide state coordination
- constructor orchestration
- class registration
- namespace preparation

then the ownership may already be elsewhere.

## Why the module centers the attribute engine

The old synthesis idea from the monolithic page is still important:

descriptors are the real attribute engine behind properties, bound methods, and many field
systems.

That matters because once the engine is visible:

- framework field objects stop looking magical
- precedence bugs become explainable
- storage mistakes become easier to spot
- descriptor use can be justified or rejected more honestly

The point is not to make descriptors feel more advanced. The point is to make them more
reviewable.

## What strong Module 07 decisions sound like

Strong design notes in this module usually sound like:

- "this belongs to one attribute, so a property is enough"
- "this rule repeats across several fields, so a reusable descriptor is the clearer owner"
- "this behavior is about calls, not attributes, so a wrapper is the wrong tool"
- "this does not require class-creation control, so a metaclass would be overreach"

That is the tone of ownership clarity the module wants.

## Review rules for descriptor boundaries

When reviewing a descriptor-heavy design, keep these questions close:

- does the rule truly belong to attribute access?
- is the same field behavior repeated enough to justify reuse?
- would a property be clearer because the rule is local to one attribute?
- is `__setattr__` being used where descriptors would keep ownership narrower?
- is someone proposing a metaclass for a field-level problem?

## What to practice from this page

Try these before moving on:

1. Take one field rule and place it on the ladder: plain attribute, property, descriptor, or metaclass.
2. Rewrite one over-engineered `__setattr__` idea into either properties or descriptors.
3. Write one short review note rejecting a descriptor because a single property would be clearer.

If those feel ordinary, the worked example can now combine the module's mechanics and
ownership boundaries inside one didactic quantity field.
