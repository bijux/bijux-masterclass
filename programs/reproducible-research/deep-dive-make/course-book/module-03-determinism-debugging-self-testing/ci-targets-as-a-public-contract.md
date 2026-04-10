# CI Targets as a Public Contract

CI does not consume your private understanding of the Makefile. It consumes a target
surface.

That means your public targets are part of an interface contract, not just local
convenience names.

## The core idea

If a target is public, you should be able to answer:

- what it builds or checks
- what exit behavior it guarantees
- which artifacts it is allowed to write
- whether changing its meaning would break downstream users

Targets such as `help`, `all`, `test`, and `selftest` are not just commands. They are the
public vocabulary of the build.

## Why this matters

Without a stable target contract, CI can go green for the wrong reasons:

- checks become non-fatal
- diagnostic outputs get mixed into correctness outputs
- a familiar target silently changes meaning

Module 03 wants the opposite: explicit public behavior and predictable failure semantics.
