# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
your publish decisions visible through bundle design, verification evidence, and consumer
tests, not through vague claims that the output “looks ready.”

Do them in order. The set is one day-long progression:

- Exercises 1-3 separate internal outputs from public promises.
- Exercises 4-6 build the versioned bundle and define artifact roles.
- Exercises 7-8 defend integrity and consumer use.
- Exercises 9-10 classify change and review downstream risk.

For every answer, keep three things:

- the boundary you are protecting
- the evidence route you actually used
- one short sentence explaining why the chosen publish surface helps a downstream user

## Exercise 1: Classify the current outputs

Take a workflow that produces internal results, logs, reports, and one or more structured
summaries. Classify every output as one of these:

- internal workflow state
- diagnostic artifact
- human-facing publish artifact
- machine-facing publish artifact

What to hand in:

- the artifact-role table
- one file that must remain internal
- one file that should become part of the public contract
- one missing artifact that keeps the current publish story weak

## Exercise 2: Draw the first publish boundary

Promote the smallest honest set of downstream-facing artifacts into `publish/v1/`.

What to hand in:

- the internal tree and public tree
- the rules that own publication
- one sentence for each included file explaining its job
- one sentence for each excluded file explaining why it stays internal

## Exercise 3: Separate machine and human surfaces

Choose one machine-readable summary and one human-readable report from the same workflow.
Explain why they are related but not interchangeable.

What to hand in:

- the authoritative machine-facing artifact
- the human-facing artifact
- the data relationship between them
- one reason scraping the report would weaken the contract

## Exercise 4: Write a manifest for the bundle

Create a manifest that inventories the public files with stable relative paths and SHA-256
checksums.

What to hand in:

- the manifest format
- the ordering rule for entries
- one successful verification transcript
- one reason absolute paths do not belong in the contract

## Exercise 5: Add provenance without confusing its role

Generate a provenance artifact for the published bundle that records enough software
context to explain the run later.

What to hand in:

- the provenance file
- the software details it records
- one trust question provenance answers well
- one trust question provenance does not answer without the contract itself

## Exercise 6: Write a consumer test

Create a small program that receives only the bundle path and uses one documented
machine-facing artifact. It must not read `results/`, repository configuration, or
producer-only paths.

What to hand in:

- the consumer
- the schema or validation route it relies on
- a successful run against the bundle
- one producer detail the consumer intentionally does not know

## Exercise 7: Corrupt the bundle and detect it

Alter one published file after the manifest is generated and run the verifier again.

What to hand in:

- the corrupted path
- the failed verification output
- an explanation of what checksum verification proves
- an explanation of what checksum verification does not prove

## Exercise 8: Simulate a downstream compatibility check

Change one bundle field, path, or artifact role and test the consumer from Exercise 6
against the new bundle.

What to hand in:

- the specific change
- the consumer outcome
- your compatibility classification
- whether the fix belongs in the current version or in a new public version

## Exercise 9: Design a deliberate version migration

Create a `publish/v2/` contract for one breaking change while preserving a clear route for
existing `v1` consumers.

What to hand in:

- both public trees
- the migration note
- supported-consumer tests
- the reason internal workflow layout still does not belong to either API

## Exercise 10: Review a full publish change like a downstream maintainer

Review a change that touches publication rules, bundle contents, manifest logic,
provenance, and a consumer-facing schema.

What to hand in:

- findings ordered by downstream trust impact
- one corrected artifact-role table
- the narrow verification route for each correction
- one change that should be versioned, postponed, or removed

## Mastery standard for this exercise set

Across all ten answers, Module 06 wants the same habits:

- you treat internal workflow state and public contracts as different promises
- you keep machine and human surfaces distinct
- you use manifests, checksums, and provenance for different jobs
- you review publish drift from the consumer’s point of view

If your answer says only "the files are in publish now," keep going.
