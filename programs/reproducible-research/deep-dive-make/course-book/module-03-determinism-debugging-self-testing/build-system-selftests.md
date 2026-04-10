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

## Why the negative test matters

A good negative test proves the harness can catch a real build-system regression. Without
that, a passing selftest can still be weak theater.

Module 03 prefers negative tests that introduce hidden variability rather than simply
breaking compilation. The point is to expose nondeterminism or non-convergence, not to
show that syntax errors fail.
