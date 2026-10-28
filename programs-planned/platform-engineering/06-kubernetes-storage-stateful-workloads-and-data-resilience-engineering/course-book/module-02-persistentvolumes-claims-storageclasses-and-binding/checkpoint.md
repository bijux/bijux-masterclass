# Checkpoint 02 — PersistentVolumes, Claims, StorageClasses, and Binding

## Required evidence

- completed exercise responses and corrections;
- the lab evidence named in `lab.md`;
- one machine-readable Atlas capstone artifact;
- one failure trace that identifies the earliest missing transition;
- one explicit `not-executed` entry for evidence outside the current environment, if applicable.

## Decision defense

Defend this statement in no more than 500 words:

> A deterministic binder creates topology-compatible PVs, preserves one-to-one claim identity, and refuses unsafe rebinding or destructive reclaim.

Your defense must name the authoritative state, the writer or controller allowed to mutate it, the rollback or recovery boundary, and the proof that would falsify the design.

## Progression gate

Do not advance until the evidence supports the governing question: **How does a storage request become one specific volume without creating an unschedulable or destructively managed workload?**
