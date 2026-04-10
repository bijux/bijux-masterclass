# Determinism and Stable Discovery

The first lesson in Module 03 is simple to say and surprisingly easy to break:

> same semantic inputs should produce the same graph, the same rebuild decisions, and the
> same declared artifacts.

That is determinism in the context of Make.

## What usually breaks determinism

Four things do most of the damage:

- unstable file discovery
- parse-time shelling out to moving system state
- non-atomic generation of shared artifacts
- hidden inputs that are real but not modeled

If any one of those drifts, the build may still appear "mostly correct" while producing
different rebuild decisions on different runs or machines.

## The sentence to keep

When you review a deterministic build, the question is not "did it work on my machine?"
The question is:

> would the same semantic repository state produce the same graph and the same declared
> outputs somewhere else?

That is the standard Module 03 cares about.

## A common source of drift

This shape looks harmless:

```make
SRCS = $(wildcard src/dynamic/*.c)
```

But the important question is not whether the command is short. The important question is
whether the resulting list has a canonical order and membership policy.

If discovery order moves, link order may move. If discovery membership is sloppy, editor
backups or temp files may leak into the graph.

## Rooted discovery beats global discovery

Good discovery starts from explicit roots such as `src/` or `src/dynamic/`. That matters
because it keeps the build from accidentally depending on whatever happens to exist
elsewhere in the repository or workspace.

This is the healthy instinct:

- pick the directory boundary on purpose
- choose the filename pattern on purpose
- sort the result on purpose

That is more durable than "let the shell find whatever looks close enough."

## Parse-time shelling out needs a fence

If you must use the shell for discovery or signatures, the shell command needs to be
stable too. Locale and environment can move output in ways that are easy to miss.

For example:

```make
SRCS := $(shell LC_ALL=C find src/dynamic -name '*.c' -print | sort)
```

The point is not to worship shell commands. The point is to avoid pretending shell output
is automatically stable.

## Generated files have a determinism contract too

Generation does not become safe just because the output is "temporary." A generated file
that is consumed by multiple targets has to meet three standards:

- one clear writer
- atomic publication
- explicit consumer edges

If generation breaks any one of those, parallel flakes and cross-run drift become much
more likely.

## A useful review checklist

- Is discovery rooted?
- Is discovery order canonical?
- Could temp or editor files leak into the membership set?
- Does code generation publish one complete artifact or a partially visible one?
- Are semantic inputs modeled or only implied?

## End-of-page checkpoint

Before leaving this page, you should be able to explain:

- why unstable discovery can change both the graph and the final artifact set
- why rooted plus sorted discovery is the healthy default
- why shell-based discovery needs locale or ordering fences
- why generated artifacts need deterministic publication as well as deterministic content

## The healthy default

Module 03 prefers:

- rooted discovery
- sorted lists
- explicit filtering when needed
- modeled hidden state through stamps or manifests

That is not ceremony. It is how you keep the graph stable while the repository changes.
