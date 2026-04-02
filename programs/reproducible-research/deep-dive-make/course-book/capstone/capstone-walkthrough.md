# Capstone Walkthrough

<!-- page-maps:start -->
## Guide Fit

```mermaid
flowchart TD
  family["Reproducible Research"] --> program["Deep Dive Make"]
  program --> pressure["A concrete learner or reviewer question"]
  pressure --> guide["Capstone Walkthrough"]
  guide --> next["Modules, capstone, and reference surfaces"]
```

```mermaid
flowchart TD
  question["Do you need a first pass or a deeper review?"] --> route["Choose one walkthrough depth"]
  route --> inspect["Read the matching guide and artifact"]
  inspect --> next_move["Stop when one honest repository story is visible"]
```
<!-- page-maps:end -->

Read the first diagram as a timing map: this page gives the capstone a teaching route,
not just a repository map. Read the second diagram as the rule: choose one walkthrough
depth, read the matching guide and artifact, then stop when one honest repository story
is visible.

## First pass versus deeper pass

- First pass: use the 30-minute route when you need one bounded learner story from public targets to proof.
- Deeper pass: use the longer routes only when the question changes from entry to architecture or stewardship.

## 30-minute first pass

1. Run `make PROGRAM=reproducible-research/deep-dive-make capstone-walkthrough`.
2. Read the capstone's local [WALKTHROUGH_GUIDE.md](../../capstone/docs/WALKTHROUGH_GUIDE.md).
3. Run `make PROGRAM=reproducible-research/deep-dive-make inspect`.
4. Read the capstone's local [TARGET_GUIDE.md](../../capstone/docs/TARGET_GUIDE.md).
5. Read `capstone/Makefile` and `capstone/tests/run.sh`.
6. Run `make PROGRAM=reproducible-research/deep-dive-make test`.

Goal: leave with a clear picture of what the capstone promises, which targets are public,
and how the build proves more than compilation.

## Architecture pass

Use this only after Modules 06-08.

1. Read the capstone's local [ARCHITECTURE.md](../../capstone/docs/ARCHITECTURE.md).
2. Follow discovery in `capstone/mk/objects.mk`.
3. Follow modeled hidden inputs in `capstone/mk/stamps.mk`.
4. Trace generated-header production from `capstone/scripts/gen_dynamic_h.py`.
5. Run `gmake -C capstone --trace dyn`.

Goal: see how truthful graph modeling survives a repository with layers, generation, and
publication boundaries.

## Stewardship pass

Use this only after Modules 09-10.

1. Read the capstone's local [TARGET_GUIDE.md](../../capstone/docs/TARGET_GUIDE.md).
2. Read the capstone's local [ARCHITECTURE.md](../../capstone/docs/ARCHITECTURE.md).
3. Review `capstone/mk/*.mk`, `capstone/tests/`, and `capstone/repro/`.
4. Run `make PROGRAM=reproducible-research/deep-dive-make capstone-confirm`.

Goal: judge whether another maintainer could extend, review, or migrate the build
without losing its teaching honesty.

## Good stopping point

Stop when you can explain one complete repository story:

- the public target you started from
- the build behavior it is supposed to prove
- the file or proof surface that makes that claim inspectable

If you cannot tell that story yet, do not widen the tour. Repeat the smaller pass.
