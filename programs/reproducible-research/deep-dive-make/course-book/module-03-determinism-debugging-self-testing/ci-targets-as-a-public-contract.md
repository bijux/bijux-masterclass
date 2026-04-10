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

## A practical contract table

| Target | Minimum promise |
| --- | --- |
| `help` | lists the supported public surface without making the reader guess |
| `all` | builds the declared correctness artifacts |
| `test` | runs runtime assertions and fails non-zero on regression |
| `selftest` | checks build-system invariants, not just executable behavior |

That table is simple on purpose. If the team cannot agree on those meanings, CI is
already consuming an unstable interface.

## Why this matters

Without a stable target contract, CI can go green for the wrong reasons:

- checks become non-fatal
- diagnostic outputs get mixed into correctness outputs
- a familiar target silently changes meaning

Module 03 wants the opposite: explicit public behavior and predictable failure semantics.

## Diagnostics are not correctness by default

One common mistake is wiring an attestation, report, or timestamped diagnostic artifact
into `all` as if it were part of core correctness. That usually creates one of two bad
outcomes:

- the build stops converging because the diagnostic changes every run
- the correctness artifact set gets polluted with files that are allowed to vary

Diagnostics can be useful. They just should not quietly redefine the correctness contract.

## A good public-target review question

For each public target, ask:

- what would a CI job owner believe this target guarantees
- what file outputs are part of that guarantee
- what exit behavior proves failure cleanly

If the answer is vague, the target is not ready to be a public contract.

## End-of-page checkpoint

Before leaving this page, you should be able to explain:

- why public targets are an interface rather than an implementation detail
- why silently changing target meaning is a contract break
- why diagnostics and attestations should not casually become correctness prerequisites
- how `help`, `all`, `test`, and `selftest` differ in responsibility
