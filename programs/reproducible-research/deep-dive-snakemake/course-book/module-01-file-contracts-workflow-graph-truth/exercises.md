# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
your file-contract reasoning visible, not to show off syntax.

Each exercise asks for three things:

- the contract or workflow question you are answering
- the evidence command or artifact you would rely on
- the repair or design choice that follows

## Exercise 1: Explain why one rule does not run

Write a tiny Snakefile with three rules:

- one `rule all`
- one rule whose output is required
- one rule whose output is never requested

Then explain, in plain language, why the extra rule is absent from the current plan.

What to hand in:

- the target requested
- the rule that matches it
- the rule that is absent
- one command, such as `snakemake -n`, that proves your explanation

## Exercise 2: Prove convergence and then break it

Start from a tiny workflow that converges after a clean run.

Then introduce one unstable influence such as a time-based parameter or another changing
tracked value so the workflow stops converging.

What to hand in:

- the converging version and the non-converging version
- the dry-run evidence that shows the difference
- one sentence explaining what made the rule meaning unstable
- the repair that restores convergence

## Exercise 3: Diagnose one wildcard ownership problem

Create either:

- an ambiguous pair of rules that can both claim one output
- or a wildcard pattern that is too loose for the filenames it should own

Then explain the ownership problem and redesign the path shape.

What to hand in:

- the problematic output pattern
- the file that demonstrates the ambiguity or looseness
- the redesigned output pattern
- one command, such as `snakemake -n` or `--rulegraph`, that supports the diagnosis

## Exercise 4: Separate workflow meaning from execution policy

Take one setting that affects output meaning and one setting that affects execution policy.
Place each one where it belongs.

What to hand in:

- one config value and why it belongs in config
- one profile value and why it belongs in a profile
- one example of a failure that early config validation would catch
- one sentence explaining why the split makes the workflow easier to review

## Exercise 5: Repair a poison output

Write a rule that fails after writing to its final output path. Then repair it so the final
output is either complete or absent.

What to hand in:

- the broken rule shape
- the repaired atomic-publication shape
- the log path or evidence route you would keep for diagnosis
- one sentence explaining why the repaired version is safer for downstream rules

## Mastery standard for this exercise set

Across all five answers, the module wants the same habits:

- you explain behavior in terms of targets, files, and ownership
- you use dry-run, summary, DAG, or logs as evidence
- you distinguish stable workflow meaning from ambient or accidental state
- you prefer clearer path contracts over clever but vague patterns
- you treat final outputs as publishable artifacts, not scratch files

If an answer says only "Snakemake was weird," keep going.
