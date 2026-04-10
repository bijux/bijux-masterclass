# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
your reasoning visible, not to show off Make syntax.

## Exercise 1: Name the runnable targets

Take the `m02/` simulator and explain which targets may run concurrently during a clean
build and why.

## Exercise 2: Repair a shared-log race

Explain why `repro/01-shared-log.mk` is nondeterministic under `-j`, then redesign it so
one target owns the final log.

## Exercise 3: Repair a temporary-file collision

Explain why `repro/02-temp-collision.mk` is unsafe, then redesign it so each target uses
its own temporary path.

## Exercise 4: Choose the right ordering tool

Give one example that needs a real prerequisite, one that needs an order-only
prerequisite, and one that needs a stamp.

## Exercise 5: Design a selftest

Describe the checks your `selftest` target must perform to prove parallel safety on the
declared artifact set.
