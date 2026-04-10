# Macros and Quarantined Eval

Make is a language, and that means abstraction is possible. Module 03 is where that
abstraction gets a leash.

## The rule for abstraction here

Abstraction is allowed when it improves correctness without making the graph harder to
audit.

That gives you two different tools:

- small macros that enforce repeatable invariants
- optional `eval` that stays bounded, auditable, and switchable

## Macros are for invariants, not drama

The best macros in this module are small and boring. They help you avoid repeating a
correct pattern, such as:

- asserting a required value exists
- publishing through a safe helper shape
- keeping a rule contract consistent across several targets

When a macro becomes too clever to explain, it usually stops helping.

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

## The budget for eval

A healthy `eval` surface in this module should be:

- finite: the generated target set is small and predictable
- local: one include owns it
- optional: the core build does not need it
- observable: `-n`, `--trace`, and `-p` still make sense

That is what "quarantined" means here. It does not mean mysterious. It means bounded.

## A useful review question

When you see a macro or `eval` block, ask:

- what invariant is this abstraction enforcing
- what graph surface does it create
- how would I inspect the result with normal Make tools
- what breaks if I disable it

If the answers are fuzzy, the abstraction is too expensive.

## End-of-page checkpoint

Before leaving this page, you should be able to explain:

- when a macro is genuinely helping instead of hiding detail
- why `eval` must stay switchable and bounded
- how to inspect generated rules with standard Make tools
- why the core build should not depend on optional metaprogramming
