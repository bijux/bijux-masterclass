# Exercises

Use these after reading the five core lessons and the worked example. The goal is not to
memorize tool names. The goal is to make your observation choices visible and reviewable.

Each exercise asks for three things:

- the runtime question you are actually trying to answer
- the least risky tool that answers that question
- the evidence or output that would prove your choice was honest

## Exercise 1: Separate visible names from stored state

Pick one object and compare what `dir(obj)` reveals with what `vars(obj)` or `obj.__dict__`
reveals.

What to hand in:

- one object with ordinary dictionary-backed state
- one attribute name that appears in `dir(obj)` but not in stored state
- one sentence explaining why name discovery and storage inspection are different questions

## Exercise 2: Show that dynamic access is behavior

Build one object whose attribute access executes code.

What to hand in:

- one property, descriptor, or `__getattr__` example
- evidence that `getattr` or `hasattr` triggered behavior
- one explanation of why that makes the access unsafe as casual inspection

## Exercise 3: Choose the right type check

Write a tiny helper whose correctness depends on the difference between exact and
polymorphic checks.

What to hand in:

- one example where `isinstance` is the right default
- one example where `type(obj) is T` is the right choice
- one sentence explaining why the two checks answer different review questions

## Exercise 4: Prove what `callable()` does and does not promise

Create examples of both callable and non-callable objects.

What to hand in:

- one callable instance created through a type-level `__call__`
- one non-callable instance with an instance-level `__call__` attribute
- one explanation of why `callable(obj)` does not guarantee argument validity or safe execution

## Exercise 5: Compare static and dynamic lookup directly

Use one object with a property or descriptor and compare `inspect.getattr_static` with
`getattr`.

What to hand in:

- the object definition
- the result of the static lookup
- the result or side effect of the dynamic lookup
- one explanation of which lookup style better fits tooling and why

## Exercise 6: Review a debug or inspection helper

Take a tiny introspection helper of your own or use the worked example pattern.

What to hand in:

- where the helper discovers names
- where it reads stored state or resolves values
- one repair that makes the helper less eager to execute runtime behavior

## Mastery standard for this exercise set

Across all six answers, the module wants the same habits:

- you name the exact observation question before naming a tool
- you use the least risky tool that answers that question
- you distinguish discovery, storage inspection, classification, and execution
- you avoid treating dynamic access as harmless by default

If an answer still sounds like "I just checked the attribute," keep going.

## Continue through Module 02

- Previous: [Worked Example: Building a Safer Debug Printer](worked-example-building-a-safer-debug-printer.md)
- Next: [Exercise Answers](exercise-answers.md)
- Return: [Overview](index.md)
- Terms: [Glossary](glossary.md)
