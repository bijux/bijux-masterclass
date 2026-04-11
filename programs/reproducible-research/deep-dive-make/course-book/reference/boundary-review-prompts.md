# Boundary Review Prompts

Use this page when a Make review needs sharper boundary questions rather than more shell
output.

## Build truth boundaries

- Is this rule expressing a real dependency or only forcing order?
- Does this helper make the graph clearer, or does it hide it behind convenience?
- Would changing the schedule alter artifact meaning?

## Public and proof boundaries

- Is this target part of the supported command surface?
- Does this artifact belong to the build, the proof bundle, or the teaching material?
- Has review evidence leaked into artifact identity or vice versa?

## Layer boundaries

- Should this behavior live in the top-level `Makefile`, a `mk/*.mk` layer, the proof harness, or a repro?
- Is a helper layer clarifying the graph or hiding it?
- Would moving this logic make the build easier to reason about one file at a time?

## Stewardship boundaries

- Which layer should own this change: top-level `Makefile`, `mk/*.mk`, tests, or repros?
- Would a new reader know where to look without oral history?
- What would make you reject this change as too clever for the trust it earns?
