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

## A common source of drift

This shape looks harmless:

```make
SRCS = $(wildcard src/dynamic/*.c)
```

But the important question is not whether the command is short. The important question is
whether the resulting list has a canonical order and membership policy.

If discovery order moves, link order may move. If discovery membership is sloppy, editor
backups or temp files may leak into the graph.

## The healthy default

Module 03 prefers:

- rooted discovery
- sorted lists
- explicit filtering when needed
- modeled hidden state through stamps or manifests

That is not ceremony. It is how you keep the graph stable while the repository changes.
