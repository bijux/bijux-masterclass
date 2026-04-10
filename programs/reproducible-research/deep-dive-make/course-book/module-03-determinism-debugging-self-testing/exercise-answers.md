# Exercise Answers

Use this after writing your own answers. The point is to compare reasoning, not copy it.

## Exercise 1: Stabilize discovery

A strong answer uses rooted discovery, canonical ordering, and explicit filtering when
needed. The key idea is that discovery should produce the same semantic file set in the
same order given the same repository state.

## Exercise 2: Trace a rebuild properly

A strong answer quotes the actual `--trace` line that names the prerequisite reason rather
than paraphrasing from memory. The point is to let Make supply the explanation.

## Exercise 3: Define the CI contract

Good public targets usually include `help`, `all`, `test`, and `selftest`. The strong
answer explains what each guarantees and why silently changing that meaning would be a
contract break.

## Exercise 4: Design the selftest

A strong answer includes convergence, serial/parallel equivalence, a meaningful negative
test, and isolation from helpful local state. It also names which artifact set should be
compared and why.

## Exercise 5: Quarantine eval

The acceptable conditions are that `eval` stays bounded, auditable, switchable, and
non-essential to the core build. A strong answer explains how to prove that disabling it
still leaves `selftest` meaningful.
