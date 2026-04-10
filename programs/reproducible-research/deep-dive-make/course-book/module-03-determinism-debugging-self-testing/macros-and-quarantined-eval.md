# Macros and Quarantined Eval

Make is a language, and that means abstraction is possible. Module 03 is where that
abstraction gets a leash.

## The rule for abstraction here

Abstraction is allowed when it improves correctness without making the graph harder to
audit.

That gives you two different tools:

- small macros that enforce repeatable invariants
- optional `eval` that stays bounded, auditable, and switchable

## Why quarantine matters

`eval` is not forbidden. It is dangerous when it becomes the hidden source of the real
build graph.

The healthy pattern is:

- put it in one obvious include
- guard it behind an explicit switch
- keep the core build working without it
- make sure `-n`, `--trace`, and `-p` still tell the truth

That way the abstraction remains inspectable instead of turning the Makefile into a black
box generator.
