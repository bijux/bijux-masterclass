# Exercises

Use these after reading the five core lessons and the worked example. The goal is not to
repeat vocabulary from memory. The goal is to make the runtime object model visible from
evidence.

Each exercise asks for three things:

- the runtime object or relationship you are trying to explain
- the evidence that proves your claim
- the boundary or design judgment that follows from that evidence

## Exercise 1: Tell the truth about one function object

Choose one Python-defined function and explain what it carries at runtime.

What to hand in:

- the function's `__name__`, `__qualname__`, and `__module__`
- one example of live environment state through `__globals__` or closure state
- one sentence explaining why "callable" is too broad to describe this object fully

## Exercise 2: Explain one class without saying "class magic"

Choose one small class and trace how it becomes a runtime object.

What to hand in:

- the class object's metaclass, bases, and one useful entry from `cls.__dict__`
- one explanation of a method as a function stored on the class
- one lookup example showing whether a descriptor or instance storage won

## Exercise 3: Prove module identity and stale imported values

Build or inspect one module example that shows how module caching works.

What to hand in:

- evidence that two imports or lookups refer to the same module object
- one demonstration that a copied-out value can stay stale after module state changes
- one sentence explaining why module-qualified access is safer in reload-heavy workflows

## Exercise 4: Compare instance storage models honestly

Create one dictionary-backed class and one slotted class, then compare them as runtime
objects.

What to hand in:

- one proof that the dictionary-backed instance stores state in `__dict__`
- one proof that the slotted instance rejects or reshapes dynamic attributes
- one judgment about when `__slots__` is justified and when it is only adding constraint

## Exercise 5: Trace one runtime object chain from module to call

Start with a bound method in a tiny example program and trace the whole path backward.

What to hand in:

- the module object, class object, instance, bound method, and function involved
- one sentence for each runtime moment: import time, class-definition time,
  instance-creation time, and call time
- one explanation of which object-model misunderstanding this trace would prevent

## Exercise 6: Review a brittle introspection helper

Use the worked example as a model and evaluate one introspection helper or design idea
that feels clever but risky.

What to hand in:

- the exact runtime surfaces the helper depends on
- which of those surfaces are supported and which are diagnostic-only
- one rewrite or rule that makes the helper more honest

## Mastery standard for this exercise set

Across all six answers, the module wants the same habits:

- you name the runtime object before describing the behavior
- you separate supported introspection from brittle implementation detail
- you explain behavior in terms of object relationships and runtime moments
- you avoid "Python magic" as a substitute for a real object-model explanation

If an answer still sounds like folklore, keep going.
