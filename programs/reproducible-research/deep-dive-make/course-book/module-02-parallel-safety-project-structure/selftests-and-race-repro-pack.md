# Selftests and Race Repro Pack

Module 02 is where the build has to start proving itself.

Two checks matter most:

1. convergence after a successful build
2. serial/parallel equivalence on the declared artifact set

If those fail, the build still has unresolved truth problems.

## What a selftest should prove

A useful selftest should answer:

- does `make -q all` return success after a clean successful build?
- do `-j1` and `-jN` produce the same declared artifacts?
- does the runtime check still pass after the parallel build?

That makes selftest a build-system test, not just a program test.

## Why the repro pack matters

The repro pack exists so you can practice prediction, not just repair.

Each broken Makefile should teach you to say:

- what the race is
- which path or edge makes it possible
- what repair matches the truth of the situation

That is the real skill this module is building.
