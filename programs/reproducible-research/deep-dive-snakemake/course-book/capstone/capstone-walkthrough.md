# Capstone Walkthrough

Use this page when you need one bounded workflow story from file contract to repository
proof. This page gives the capstone a teaching route, not just a repository map.

Choose one walkthrough depth, follow only the matching surfaces, and stop when one honest
workflow story is visible.

## How to use this walkthrough

Work in this order:

1. choose the depth that matches your question
2. follow the route exactly once without widening it
3. write down what became clearer before you open a second route
4. escalate only if the question truly changed

That discipline matters because the capstone can quickly become too large for the concept
you are trying to test.

## What this walkthrough should help you do

By the end of a good walkthrough, you should be able to:

- explain what the repository claims before you run anything heavy
- choose between a bounded first pass and a deeper executed pass
- inspect public contracts before drowning in internal detail
- record what became clearer and what still needs stronger proof

## Start by choosing the smallest walkthrough depth honestly

The first pass, executed pass, and stewardship pass are not just longer and shorter
versions of the same activity.

They answer different kinds of questions:

- first pass: what does this repository claim to do
- executed pass: how does one workflow story become saved evidence
- stewardship pass: what ownership or drift judgment would a maintainer make

Choosing the wrong depth usually makes the repository feel noisy rather than
enlightening.

## The 30-minute first pass

Use this pass when the question is still about entry and basic workflow shape.

1. read [Capstone Guide](index.md)
2. run `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-walkthrough`
3. read the copied `Snakefile`, rule files, `list-rules.txt`, and `dryrun.txt` in that
   order
4. read [Capstone File Guide](capstone-file-guide.md)
5. use [Capstone Review Worksheet](capstone-review-worksheet.md) to record what is
   visible before execution

Goal:

leave with a clear picture of:

- what the workflow claims to build
- where dynamic discovery is declared
- which files are public contracts
- which question would justify a deeper route

## One honest walkthrough decision

Suppose you are finishing Module 01 and only need to know whether the capstone still
behaves like a file-contract system rather than like command folklore.

The right walkthrough is the 30-minute first pass.

The executed pass would already be broader than the question, and the stewardship pass
would be much broader.

## Executed workflow pass

Use this only after the first pass is already clear.

1. run `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour`
2. read the executed proof bundle
3. compare the publish artifacts against `FILE_API.md`
4. follow one rule family back into `workflow/rules/`

Goal:

see how the planned workflow becomes executed evidence without losing contract clarity.

## Stewardship pass

Use this only after the workflow and publish surfaces are already legible.

1. run `make PROGRAM=reproducible-research/deep-dive-snakemake capstone-profile-audit`
2. read the publish-review and profile-audit surfaces together
3. record one current-truth statement and one drift risk in the review worksheet

Goal:

connect the repository to Modules 08 through 10 without turning every walkthrough into a
governance meeting.

## Good walkthrough habits

- keep one question in view the whole time
- prefer the smallest route that still answers it
- read the evidence bundle in the order the route intended
- stop once one honest workflow story is visible

## Bad walkthrough habits

- widening into a second route before the first one is explained
- reading random directories during the first pass
- treating the walkthrough as a substitute for the module
- escalating to stewardship review just because the repository feels impressive

## Good stopping point

Stop when you can explain one complete workflow story:

- the public contract or boundary you started from
- the rule or artifact that makes it visible
- the next command that would strengthen the claim only if needed

If you cannot tell that story yet, do not widen the walkthrough. Repeat the smaller pass.
