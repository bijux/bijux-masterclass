# Exercises

Use these exercises to practice stewardship judgment, not only migration vocabulary.

The strongest answers will make the current contract, the preserved proof route, and the
future boundary move explicit.

## Exercise 1: Review the current repository honestly

A repository has:

- `publish/v1/summary.json`
- several downstream notebooks that still read `results/`
- one profile with a different sample filter
- a helper package that owns discovery logic no reviewer can explain quickly

Write a short review note that explains:

- the top three risks in boundary language
- which risk you would address first
- which existing evidence route you would inspect before proposing migration

## Exercise 2: Sequence a migration

A team wants to:

- move report generation into package code
- change how samples are discovered
- migrate job submission onto an external platform

Describe a safer order for these changes.

Your answer should name:

- which boundary moves first
- what proof must survive that step
- which change should wait until later and why

## Exercise 3: Write governance rules

Draft three short governance rules for a workflow team that keeps repeating these mistakes:

- published files appear without documentation updates
- profile changes alter workflow meaning
- helper scripts become important but remain hard to review

Each rule should be short enough that a team could realistically keep using it in review.

## Exercise 4: Name the anti-pattern

A pull request does all of the following:

- removes benchmark files because they "make the repository noisy"
- adds a new published TSV without updating verification
- moves analytical thresholds into `profiles/slurm/config.yaml`

Explain:

- which anti-pattern family each change belongs to
- which change is the most dangerous and why
- what recovery step you would require first

## Exercise 5: Decide the tool boundary

A team now wants user-triggered analysis requests, access control, and tenancy-aware job
scheduling, but the current Snakemake repository still does a strong job of producing
trusted publish bundles.

Write a short recommendation that explains:

- what Snakemake should keep owning
- what another system should own
- what handoff artifact or review surface should make the split trustworthy

## Mastery check

You have a strong grasp of this module if your answers consistently keep four ideas
visible:

- review comes before redesign
- migration moves one boundary at a time
- governance protects contracts, policy boundaries, proof, and ownership clarity
- tool-boundary decisions are about responsibility and evidence, not trend-following
