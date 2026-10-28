# Laboratory 20 — Object-Model Audit

## Product

Build a runtime auditor and a small component registry, then use the auditor to verify the registry's object-model contract without triggering hidden effects.

The laboratory integrates the course rather than adding another isolated feature. Your audit must distinguish:

- own and inherited properties;
- string and symbol keys;
- data and accessor descriptors;
- prototype and constructor identity;
- private-brand behavior through public probes;
- callable and iterable protocols;
- custom inspection;
- plain persistence snapshots;
- explicit lifecycle state.

## Contract

`auditObject(value)` returns a plain report containing prototype name, own descriptor summaries, visible protocol capabilities, extensibility/seal/freeze status, and whether selected reads would be effectful. It must not evaluate accessors.

`ComponentRegistry` stores branded components with stable IDs, deterministic iteration, custom inspection, plain snapshots, and an explicit close operation. Closing the registry prevents further mutation but leaves already produced snapshots valid.

## Required tests

- hidden symbol metadata appears in the deliberate audit but not ordinary enumeration;
- a throwing getter is reported but never run;
- a forged prototype object does not pass a legitimate public brand probe;
- iteration is repeatable and deterministic;
- custom inspection is bounded;
- snapshots are plain and detached;
- close is terminal and deterministic;
- the auditor itself has no mutation authority.

## Architecture note

Write a concise report naming each runtime identity, its state owner, its prototype behavior, its persistence representation, and its lifecycle. Identify at least three mechanisms you deliberately rejected.

## Transfer

Add one component alias with global uniqueness. Treat the change as a miniature rehearsal for the ObjectAtlas final extension: update representation, index authority, snapshot, audit, iteration, and tests.
