# Exercises

Use these after reading the five core lessons and the worked example. The goal is not to
collect more decorator tricks. The goal is to make wrapper mechanics, transparency, and
stateful policy visible.

Each exercise asks for three things:

- the wrapper behavior you are trying to describe or justify
- the runtime timing or state boundary that matters
- the evidence that proves the wrapper is transparent enough or not

## Exercise 1: Build one wrapper skeleton by hand

Write a decorator without `@` syntax first and apply it manually.

What to hand in:

- the decorator definition
- the manual rebinding step `wrapped = decorator(original)`
- one explanation of what the wrapper closes over

## Exercise 2: Desugar one stacked decorator example

Take a function with at least two decorators and rewrite it in step-by-step rebinding form.

What to hand in:

- the original `@decorator` version
- the explicit `f = d2(d1(f))` form
- one explanation of definition-time order versus call-time order

## Exercise 3: Implement one thin practical wrapper

Write one narrow wrapper such as timing or deprecation.

What to hand in:

- the decorator implementation
- one proof that result and exception behavior remain transparent
- one sentence explaining why the wrapper is still thin

## Exercise 4: Show semantic drift in a stateful wrapper

Implement a small stateful decorator such as `@once`.

What to hand in:

- the state storage location
- one example showing how later calls behave differently because of prior calls
- one explanation of why this is now a policy surface and not just a thin wrapper

## Exercise 5: Preserve wrapped identity honestly

Compare one bare wrapper with one `functools.wraps`-based wrapper.

What to hand in:

- the visible `__name__`, `__doc__`, or `inspect.signature` difference
- one proof that `__wrapped__` exists on the preserved version
- one explanation of why metadata preservation matters to review and tooling

## Exercise 6: Review a small cache or retry decorator

Use the worked example pattern on a stateful decorator.

What to hand in:

- the state it owns
- one reset or inspection surface it should expose
- one limitation that must be documented instead of hidden

## Mastery standard for this exercise set

Across all six answers, the module wants the same habits:

- you separate definition-time rebinding from call-time behavior
- you distinguish thin wrappers from stateful policy-carrying wrappers
- you preserve callable identity when the wrapper claims transparency
- you name when a decorator has grown beyond a simple function transformation

If an answer still sounds like "it just decorates the function," keep going.
