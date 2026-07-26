# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
your discovery reasoning visible through runnable artifacts, not through checkpoint
folklore.

Do them in order. The set is one day-long progression:

- Exercises 1-3 establish the discovery ladder.
- Exercises 4-6 turn discovery into durable artifacts.
- Exercises 7-8 justify or reject checkpoints.
- Exercises 9-10 test whether dynamic behavior survives review and publication.

For every answer, keep three things:

- the workflow files or command sequence you actually used
- the artifact that proves what the workflow discovered
- one short sentence explaining why the design is honest

## Exercise 1: Compare two discovery surfaces

Model the same three-sample workflow in two ways:

- one with a versioned sample sheet
- one with a deterministic directory scan

What to hand in:

- both discovery shapes
- one reason to prefer each in a real project
- one command that proves they generate the same target list
- one sentence naming the declared source of truth in each design

## Exercise 2: Turn ambient discovery into a declared contract

Start from a tiny workflow that scans `data/raw/` directly at parse time and relies on
whatever filenames happen to be present.

Repair it so the workflow has one named discovery surface and one normalization point.

What to hand in:

- the original discovery shape and why it was weak
- the repaired discovery rule or helper
- the normalized sample list it produces
- one sentence explaining why another reviewer could trust the new design more

## Exercise 3: Prevent one accidental fanout explosion

Design a small example where `expand()` creates more targets than the real domain calls
for.

Then repair it so the target list comes from one validated record structure instead of two
independent lists.

What to hand in:

- the buggy expansion
- the unintended targets it creates
- the repaired target-list design
- one command, such as `snakemake -n`, that would make the difference obvious

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

## Exercise 6: Build a validated candidate registry

Create a tabular manifest with at least three sample identifiers and source paths. Load it
once, reject duplicate identifiers and missing files, sort it, and use it to build
concrete QC targets without a checkpoint.

What to hand in:

- the manifest and validation code
- the deterministic target list
- one deliberately invalid record and its early error
- an explanation of why static planning is sufficient

## Exercise 7: Justify one checkpoint and reject one fake one

Write two short design sketches:

- one workflow shape where a checkpoint is justified
- one workflow shape where a checkpoint would only hide weak modeling

What to hand in:

- the discovery question each sketch is trying to answer
- the output artifact of the justified checkpoint
- the cleaner alternative for the unjustified checkpoint
- one sentence explaining the difference between the two cases

## Exercise 8: Implement a justified checkpoint

Start from a declared candidate set, then make a validation checkpoint publish a registry
containing only usable candidates. Fan out one downstream job per accepted identifier.

What to hand in:

- the checkpoint output contract
- the input function that reads it through `checkpoints.<name>.get()`
- evidence from before and after checkpoint completion
- an explanation of the runtime fact that could not be known during initial planning

## Exercise 9: Test discovery integrity under change

Run the checkpoint workflow, then add one candidate, remove one candidate, and corrupt one
candidate in separate trials. Predict the registry and downstream target changes before
each run.

What to hand in:

- the three predictions
- registry diffs for each trial
- dry-run evidence for affected downstream jobs
- the rejection evidence retained for the corrupt candidate

## Exercise 10: Publish a reviewable dynamic result

Publish a versioned bundle for the checkpoint workflow. Include the accepted registry,
rejection record, results, resolved configuration, provenance, and a manifest with
checksums.

What to hand in:

- the public directory tree
- a machine-readable inventory and checksum verification command
- a short consumer procedure that does not depend on internal working paths
- an explanation of which artifacts are public contracts and which remain internal state

## Mastery standard for this exercise set

Across all ten answers, Module 02 wants the same habits:

- you name the artifact or boundary that carries the truth
- you explain dynamic behavior without using mystical language
- you show which command or file would let another person verify the claim

If your answer says only "Snakemake will handle it," keep going.
