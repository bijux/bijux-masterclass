# Project Structure with One DAG

As builds grow, the temptation is to split the repository into little private worlds and
let each subdirectory run its own Makefile. Module 02 argues for a different default:

> keep one top-level DAG and layer the build so the graph stays visible.

## A simple layering pattern

For this module, the healthy shape is:

```text
m02/
  Makefile
  mk/
    common.mk
    objects.mk
    rules.mk
```

Each layer has one job:

- `Makefile` owns the public targets
- `common.mk` holds stable policy knobs
- `objects.mk` maps sources to outputs
- `rules.mk` publishes artifacts

That is enough structure to scale without turning the build into a maze.

## Why recursive make is not the default

If each directory runs its own private make process, you often lose global visibility:

- hidden cross-directory dependencies
- weaker scheduling decisions
- harder debugging because each sub-make sees only part of the truth

There are legitimate boundaries, but they should be treated as explicit tool invocations
with named inputs and outputs, not as a casual way to avoid maintaining one graph.

## Optional local overrides need discipline

Local overrides such as `config.mk` can be useful for ergonomics. They should not decide
whether the build is fundamentally correct.

If an override changes artifact meaning, that fact must still be modeled in the graph.
