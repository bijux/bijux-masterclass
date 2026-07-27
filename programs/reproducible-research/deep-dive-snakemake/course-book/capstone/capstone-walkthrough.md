# Capstone Walkthrough

This page gives the capstone a teaching route, not just a repository map.

Use it when you need one bounded workflow story from file contract to repository proof.
Choose one walkthrough depth, follow only the matching surfaces, and stop when one honest
workflow story is visible.

## What this walkthrough must help you do

By the end of a good capstone walkthrough, you should be able to:

- explain what the repository claims before you run anything heavy
- choose between a bounded first pass and a deeper executed pass
- inspect public contracts before drowning in internal detail
- record what became clearer and what still needs stronger proof

## First pass versus deeper pass

- First pass: use the bounded route when you need one clear workflow story from file contract to planned proof.
- Deeper pass: use the longer routes only when the question changes from entry to policy, publish, execution, or stewardship review.

## 30-minute first pass

1. Read [Capstone Guide](index.md).
2. Run `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough`.
3. Read the copied `Snakefile`, rule files, `list-rules.txt`, and `dryrun.txt` in that order.
4. Read [Capstone File Guide](capstone-file-guide.md).
5. Use [Capstone Review Worksheet](capstone-review-worksheet.md) to record what is visible before execution.

Goal:
leave with a clear picture of what the workflow claims to build, where dynamic discovery
is declared, which files are public contracts, and which question would justify a deeper
route.

## Executed workflow pass

Use this only after the first pass is already clear.

1. Run `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour`.
2. Read the executed proof bundle.
3. Compare the publish artifacts against `FILE_API.md`.
4. Follow one rule family back into `workflow/rules/`.

Goal:
see how the planned workflow becomes executed evidence without losing contract clarity.

## Stewardship pass

Use this only after the workflow and publish surfaces are already legible.

1. Run `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-profile-audit`.
2. Read the publish-review and profile-audit surfaces together.
3. Record one current-truth statement and one drift risk in the review worksheet.

Goal:
connect the repository to Modules 08-10 without turning every walkthrough into a
governance meeting.

## Good stopping point

Stop when you can explain one complete workflow story:

- the public contract or boundary you started from
- the rule or artifact that makes it visible
- the next command that would strengthen the claim only if needed

If you cannot tell that story yet, do not widen the walkthrough. Repeat the smaller pass.
