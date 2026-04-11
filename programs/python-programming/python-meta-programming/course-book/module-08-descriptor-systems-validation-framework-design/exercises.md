# Exercises

Use these after reading the five core lessons and the worked example. The goal is not to
memorize framework vocabulary. The goal is to make cache policy, backend ownership,
composition, hint support, and architecture boundaries explicit.

Each exercise asks for three things:

- the field behavior or framework pressure you are analyzing
- the descriptor or broader owner you chose
- the reason that choice is the clearest one

## Exercise 1: Design one cached field honestly

Create or inspect one descriptor that caches a computed value.

What to hand in:

- when the value is computed
- where the cached value is stored
- one explicit invalidation rule

## Exercise 2: Review one external-storage field

Build or inspect one descriptor whose source of truth lives outside the instance.

What to hand in:

- the backend key shape
- one read-through or write-through behavior
- one explanation of what cost or I/O the attribute access hides

## Exercise 3: Compose one wrapper field

Take one field descriptor and add one extra concern through composition.

What to hand in:

- the inner field's responsibility
- the wrapper layer's added concern
- one explanation of how `__set_name__` or delegation is preserved

## Exercise 4: Validate one narrow hint subset

Build or inspect one hint-aware field descriptor.

What to hand in:

- the exact hint forms it supports
- one coercion it allows or refuses
- one explanation of how `Annotated[...]` metadata is used, if present

## Exercise 5: Reject one descriptor that became architecture

Choose one field-system idea that is starting to exceed one attribute contract.

What to hand in:

- the extra responsibility it is trying to absorb
- the explicit framework or service owner it should move to
- one sentence explaining why the descriptor layer is no longer enough

## Exercise 6: Review the educational mini relational model

Use the worked example as a case study.

What to hand in:

- one thing the field layer owns honestly
- one thing the model layer or framework layer must own instead
- one explanation of why this example is educational rather than production-grade

## Mastery standard for this exercise set

Across all six answers, the module wants the same habits:

- you treat invalidation as part of cache design
- you make the source of truth explicit
- you keep composed fields inspectable
- you keep hint-driven validation narrow and honest
- you name the point where field logic turns into framework architecture

If an answer still sounds like "the smart descriptor handles it," keep going.

## Continue through Module 08

- Previous: [Worked Example: Building an Educational Mini Relational Model](worked-example-building-an-educational-mini-relational-model.md)
- Next: [Exercise Answers](exercise-answers.md)
- Return: [Overview](index.md)
- Terms: [Glossary](glossary.md)
