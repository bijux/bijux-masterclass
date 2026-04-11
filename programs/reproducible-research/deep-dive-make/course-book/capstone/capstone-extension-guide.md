# Capstone Extension Guide

Use this page before changing the capstone. The goal is not to freeze the repository. The
goal is to keep new work readable, provable, and clearly owned two years from now.

## What must survive every change

Unless the course itself is being redesigned, a capstone change should preserve these
properties:

- truthful dependency modeling
- atomic publication for real outputs
- serial and parallel equivalence where the build claims it
- a small public target surface
- a repository shape you can still audit end to end

If a proposed change weakens one of those, treat that as a design change, not routine
maintenance.

## Put changes in the right place

| If you are changing... | Start in... | Why |
| --- | --- | --- |
| public target names or user-facing help text | `capstone/Makefile` | the public contract belongs at the top level |
| tool, shell, or portability policy | `capstone/mk/contract.mk` | policy should stay explicit and centralized |
| reusable recipe helpers | `capstone/mk/macros.mk` or `capstone/mk/common.mk` | reuse belongs in named helpers, not copied shell |
| discovery or object selection | `capstone/mk/objects.mk` | graph membership should have one owning file |
| hidden inputs or rebuild state evidence | `capstone/mk/stamps.mk` | state tracking should stay reviewable |
| proof behavior | `capstone/tests/run.sh` | proof belongs to the harness, not to prose |
| a new failure specimen | `capstone/repro/` plus [Capstone Proof Guide](capstone-proof-guide.md) | failure specimens should stay isolated from the healthy build |

## Good capstone changes

These usually improve the repository:

- clarifying a target description or route page
- adding one more explicit dependency or boundary file
- improving a proof message without weakening the check
- adding a distinct repro that exposes a real failure class
- tightening file ownership so review requires less guessing

## Risky changes

Slow down when a change does any of these:

- adds abstraction that hides the graph more than it reduces repetition
- turns internal helper behavior into an undocumented public surface
- weakens selftest because one environment is inconvenient
- mixes proof residue into source or release identity
- adds repository bulk without adding a sharper lesson

## Review checklist before you commit

Answer these in your own words:

1. what review or maintenance question became easier after this change
2. which file now owns the behavior
3. which proof route still corroborates the claim
4. whether the filename and commit message would still make sense later
5. whether the change can be understood without oral history

If you cannot answer those, the change is probably not placed cleanly yet.

## Best rerun commands

From repository root:

```sh
make PROGRAM=reproducible-research/deep-dive-make capstone-walkthrough
make PROGRAM=reproducible-research/deep-dive-make inspect
make PROGRAM=reproducible-research/deep-dive-make test
make PROGRAM=reproducible-research/deep-dive-make proof
```

Those four routes cover entry, public contract, executable proof, and steward review.
