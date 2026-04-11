# Worked Example: Reviewing a Plugin Runtime for Observability and Control

The five core lessons in Module 10 only become trustworthy when they meet one concrete
runtime that could have become much more magical than it did.

The course capstone is that runtime.

It combines:

- metaclass-driven registration
- descriptor-backed field validation
- decorator-based action metadata
- a public CLI that exposes runtime facts without forcing plugin work

That makes it the right worked example for this module.

## The review question

The question here is not "does the capstone use metaprogramming?"

It obviously does.

The real question is:

does it keep that metaprogramming observable, bounded, reversible enough for tests, and
honest enough for code review?

That is a Module 10 question.

## Step 1: start with observational surfaces, not invocation

Good governance begins by checking whether the system exposes useful runtime facts without
performing business behavior.

In this capstone, the strongest first surfaces are:

- `manifest`
- `registry`
- `signatures`
- saved verification outputs from the proof route

Those surfaces matter because they let reviewers inspect:

- registered plugins
- generated constructor signatures
- declared actions and fields
- public runtime shape

before invoking plugin actions.

That is already a sign of discipline.

## Step 2: identify which powers were chosen, and which were rejected

The capstone uses a metaclass for one narrow ownership reason:

- concrete subclasses should register themselves deterministically at class-definition time

That is a legitimate escalation because registration belongs to the class-creation moment.

The capstone does not escalate further into:

- import-hook-based plugin discovery
- runtime code generation through `exec`
- hidden business behavior during manifest export

Those rejections matter as much as the chosen mechanism.

## Step 3: inspect whether the metaclass case stays narrow

Inside the framework, `PluginMeta` owns a few visible jobs:

- collect declared fields
- collect declared actions
- generate a constructor signature
- assign stable plugin identity
- register concrete plugins while rejecting duplicates

That is a lot, but it still stays inside one coherent timing boundary: class creation.

It helps that the design also keeps review facts public:

- `PluginMeta.registry(...)`
- `PluginMeta.clear_registry(...)`
- `build_manifest(...)`

Those explicit surfaces keep the metaclass from becoming folklore.

## Step 4: check the reversibility story

A global registry is always a governance risk unless tests can restore baseline behavior.

The capstone addresses that by exposing a reset path:

```python
@classmethod
def clear_registry(cls, group: str | None = None) -> None:
    if group is None:
        _REGISTRY.clear()
        return
    _REGISTRY.pop(group, None)
```

That method is simple, but it earns trust:

- tests can isolate groups
- duplicate-registration checks stay deterministic
- incidents have a clear control surface for registry state

Without that reset hook, the metaclass choice would be much harder to defend.

## Step 5: confirm the public CLI is a review surface, not hidden magic

The CLI intentionally separates observation from invocation.

Observational commands:

- `manifest`
- `plugin`
- `field`
- `action`
- `registry`
- `signatures`

Operational commands:

- `invoke`
- `trace`

That split is excellent Module 10 discipline because reviewers can learn a great deal
before they cross into behavior execution.

In other words, the public interface respects the same rule the course teaches: inspect
first, run later.

## Step 6: pressure-test traceability

The capstone's action wrappers preserve callable metadata and action history instead of
hiding what happened.

That matters because observability is the difference between:

- "the runtime adds policy"

and

- "the runtime adds policy, and we can still explain what happened afterward"

The strongest evidence here is not just the wrapper code. It is the paired proof surface:

- runtime tests for signature and metadata preservation
- trace output that exposes recorded action history

That is exactly the kind of double evidence Module 10 wants.

## Step 7: name the strongest rejections

The capstone becomes a stronger teaching example because it visibly refuses several higher
power temptations.

Strong refusals include:

- no import hooks for plugin discovery
- no `eval` or `exec` for plugin loading or action dispatch
- no hidden plugin invocation during manifest rendering
- no unresettable global state

Those refusals are not omissions. They are architectural choices that protect review cost.

## A small approval summary

If you were writing the review note for this capstone, it could say something like this:

- metaclass use is justified because registration and generated signatures belong to class creation
- the registry remains deterministic and resettable
- public commands expose runtime facts without requiring plugin execution
- wrappers preserve inspectable call surfaces
- the design correctly rejects import-hook and dynamic-execution escalation

That is the kind of approval language Module 10 is trying to teach.

## What would make this example worse

The same runtime would become harder to defend if it changed in any of these directions:

- manifest generation started invoking plugin actions
- plugin discovery moved to import hooks instead of explicit module ownership
- registry state lost its clear reset path
- action wrappers stopped preserving signature visibility
- review commands became side-effecting commands

These are exactly the changes you should reject in Module 10 review.

## What this worked example is really teaching

The lesson is not "the capstone is perfect."

The lesson is:

- powerful runtime mechanisms can still be reviewable
- their reviewability depends on explicit proof surfaces and narrow ownership
- the strongest designs are usually the ones that refuse extra power they could technically take

That is why this example belongs at the end of the course.

## What to practice from this example

Try these before moving on:

1. Use the [Capstone Proof Guide](../capstone/capstone-proof-guide.md) to verify one observational claim and one operational claim.
2. Name one reason the capstone metaclass is justified and one higher-power escalation it correctly refuses.
3. Write one design change you would reject as making the runtime less observable.

If those feel ordinary, the module is ready for exercises that turn these review habits
into explicit answers.

## Continue through Module 10

- Previous: [Mechanism Selection, Review Gates, and Escalation Boundaries](mechanism-selection-review-gates-and-escalation-boundaries.md)
- Next: [Exercises](exercises.md)
- Return: [Overview](index.md)
- Terms: [Glossary](glossary.md)
