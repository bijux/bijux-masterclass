# Build-System Selftests

This lesson is where the build stops asking for trust and starts earning it.

## What selftests should prove

A useful selftest for this module should prove at least these:

- convergence after a successful build
- serial/parallel equivalence on the declared artifact set
- one meaningful negative case where hidden variability breaks the contract
- isolation from helpful local state

That makes selftest different from `test`. Runtime tests ask whether the program behaves
correctly. Selftests ask whether the build system behaves correctly.

## A useful selftest sequence

For this module, a healthy selftest usually runs work in this order:

1. create a clean sandbox
2. build serially
3. confirm convergence with `make -q all`
4. rebuild from clean in parallel
5. compare the declared artifact set
6. run the runtime assertion
7. inject one negative case and prove the harness detects it

That order matters because it separates different claims. When the harness fails, you want
to know whether convergence broke, equivalence broke, runtime broke, or the negative test
did not actually exercise the right weakness.

## Why the negative test matters

A good negative test proves the harness can catch a real build-system regression. Without
that, a passing selftest can still be weak theater.

Module 03 prefers negative tests that introduce hidden variability rather than simply
breaking compilation. The point is to expose nondeterminism or non-convergence, not to
show that syntax errors fail.

## Choosing the artifact set

Your equivalence set should contain the declared outputs whose stability you actually care
about. In this module that often means:

- the final binary
- generated headers
- object and depfile outputs when the toolchain is fixed

It usually should not include:

- timestamps
- logs
- attestations
- caches

The lesson here is not "hash everything." The lesson is "hash the right things."

## Why sandboxing matters

Selftests that run in the live workspace often pass for the wrong reason because old state
helps the build. A sandbox removes that crutch. It makes the harness prove the contract
from a cold start instead of inheriting luck.

## End-of-page checkpoint

Before leaving this page, you should be able to explain:

- why selftest is a build-system proof, not a runtime proof
- why the negative test should introduce hidden variability rather than random breakage
- how to choose the equivalence set deliberately
- why sandboxing is part of the contract, not optional cleanup
