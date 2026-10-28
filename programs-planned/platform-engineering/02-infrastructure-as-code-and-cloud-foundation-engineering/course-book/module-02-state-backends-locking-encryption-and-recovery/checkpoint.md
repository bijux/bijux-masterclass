# Checkpoint — State Authority and Recovery

## Required evidence

Retain:

- backend bootstrap and ownership diagram;
- state-boundary decision;
- encryption, key administration, and recovery-role model;
- lock acquisition and contention evidence;
- stale-lock decision criteria;
- lineage and serial comparison;
- isolated restore rehearsal;
- remote/state reconciliation table;
- partial-apply orphan disposition;
- cleanup of rehearsal keys and locks.

## Decision defense

Explain why backend versioning is a source of candidate recovery snapshots, not automatic rollback correctness. Describe the sequence for a remote object created before state commit failed, including how you decide between import, deletion, and leaving the object unmanaged temporarily.

## Progression gate

You pass only when recovery preserves authoritative evidence and never overwrites shared state during diagnosis. You must be able to state why `force-unlock` and `tofu state push` are incident-grade actions and what evidence is required before either can be considered.
