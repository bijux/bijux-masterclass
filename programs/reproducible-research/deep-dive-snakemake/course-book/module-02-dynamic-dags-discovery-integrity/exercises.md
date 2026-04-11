# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
your reasoning visible, not to prove that you can write the cleverest Snakefile.

Each answer should show three things:

- the workflow fact you are defending
- the evidence route you would use
- the repair or design choice that follows

## Exercise 1: Turn ambient discovery into a declared contract

Start from a tiny workflow that scans `data/raw/` directly at parse time.

Repair it so the workflow has one named discovery surface and one durable discovered-set
artifact.

What to hand in:

- the original discovery shape and why it was weak
- the repaired discovery rule or helper
- the path of the discovered-set artifact
- one sentence explaining why another reviewer could trust the new design more

## Exercise 2: Prevent one accidental fanout explosion

Design a small example where `expand()` creates more targets than the real domain calls
for.

Then repair it so the target list comes from one validated record structure instead of two
independent lists.

What to hand in:

- the buggy expansion
- the unintended targets it creates
- the repaired target-list design
- one command, such as `snakemake -n`, that would make the difference obvious

## Exercise 3: Justify one checkpoint and reject one fake one

Write two short design sketches:

- one workflow shape where a checkpoint is justified
- one workflow shape where a checkpoint would only hide weak modeling

What to hand in:

- the discovery question each sketch is trying to answer
- the output artifact of the justified checkpoint
- the cleaner alternative for the unjustified checkpoint
- one sentence explaining the difference between the two cases

## Exercise 4: Design the integrity trail for a dynamic run

Assume a workflow discovers samples and publishes a versioned bundle.

Describe the minimum artifact set that would let a downstream reviewer answer:

- which samples were discovered
- which files are part of the public boundary
- what run identity produced that boundary

What to hand in:

- one discovery artifact path
- one provenance artifact path
- one manifest or inventory artifact path
- one short explanation of what each artifact proves

## Exercise 5: Improve performance without weakening truth

Start from a workflow shape that is operationally clumsy, for example:

- too many tiny per-fragment jobs
- too many almost-identical environment files

Repair it without hiding required artifacts or changing the meaning of the publish
boundary.

What to hand in:

- the original smell
- the repaired environment or job-boundary design
- one sentence explaining why the repair lowers overhead
- one sentence explaining why workflow truth stayed intact

## Mastery standard for this exercise set

Across all five answers, Module 02 wants the same habits:

- you name the artifact or boundary that carries the truth
- you explain dynamic behavior without using mystical language
- you show which command or file would let another person verify the claim

If your answer says only "Snakemake will handle it," keep going.
