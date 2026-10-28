# Checkpoint 04 — Topology, Scheduling, Capacity, Expansion, and Storage QoS

## Required evidence

- completed exercise responses and corrections;
- the lab evidence named in `lab.md`;
- one machine-readable Atlas capstone artifact;
- one failure trace that identifies the earliest missing transition;
- one explicit `not-executed` entry for evidence outside the current environment, if applicable.

## Decision defense

Defend this statement in no more than 500 words:

> The scheduler, capacity catalogue, expansion controller, and attributes-class policy explain every placement or mutation decision and preserve unresolved states.

Your defense must name the authoritative state, the writer or controller allowed to mutate it, the rollback or recovery boundary, and the proof that would falsify the design.

## Progression gate

Do not advance until the evidence supports the governing question: **How can compute placement and storage placement converge without deadlock, false capacity, or unsafe in-place mutation?**
