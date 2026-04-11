# Exercises

Use these exercises to practice architectural judgment, not only folder vocabulary.

The strongest answers will name ownership, contract surfaces, and review consequences
clearly.

## Exercise 1: Read the repository entrypoint

You open a Snakemake repository and find that the top-level `Snakefile`:

- validates config
- includes three rule files
- contains a 150-line `run:` block
- sets the default target

Write a short review note that explains:

- which parts belong in the entrypoint
- which part should probably move elsewhere
- why this is an architecture issue rather than only a style issue

## Exercise 2: Judge a rule split

A teammate split one long rule file into six smaller files named:

- `part1.smk`
- `part2.smk`
- `part3.smk`
- `helpers.smk`
- `shared.smk`
- `misc.smk`

Explain:

- why this split is weak even if each file is shorter
- what kind of boundary would make the split stronger
- what a reviewer should be able to infer from the file names

## Exercise 3: Review a file-API gap

A repository publishes `publish/v1/summary.json`, but there is no file API or contract
document. Several notebooks also read directly from `results/`.

Explain:

- what architecture problem this creates
- what risks it introduces for refactors and downstream trust
- what documentation or contract surface you would add first

## Exercise 4: Diagnose hidden coupling

A helper module under `src/`:

- reads extra files the rules never declare
- assumes a config key that is not validated anywhere
- changes behavior during import

Write a short review comment that explains why this is not only a code smell, but an
architecture problem.

## Exercise 5: Decide whether to refactor

A workflow still runs, but new contributors keep asking:

- where do the main rules live?
- which files are public versus internal?
- whether `workflow/scripts/` or `src/` should own a new feature

Describe:

- which architecture signals you see
- what boundary you would inspect first
- what kind of refactor would be justified before the repository grows further

## Mastery check

You have a strong grasp of this module if your answers consistently keep four ideas visible:

- repository layers need named responsibilities
- workflow splits should reflect ownership
- file APIs are part of architecture
- hidden coupling and doc drift are real architectural risks
