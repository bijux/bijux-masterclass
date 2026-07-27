# Worked Example: Planning a Safe Workflow Migration

This file ties the whole module together around one realistic problem:

> a team wants change for real reasons, but could easily destroy trust by moving too many weak boundaries at once.

The question is not "how do we modernize the repository?" The question is how to review
current truth, move one boundary, preserve proof, and stop before a fashionable rewrite
erases evidence.

## The lab route

Work through the example in this order:

1. review current truth before proposing migration
2. write down what must not move first
3. sequence one ownership change at a time
4. narrow the external handoff request to what Snakemake should no longer own
5. finish by writing governance rules so the same drift does not return

## The starting situation

Assume a team inherits a Snakemake repository with these characteristics:

- the workflow itself still runs reliably
- downstream notebooks read some files from `results/`
- `publish/v1/summary.json` is trusted, but the file API is incomplete
- one profile includes a sample filter that does not belong to operating policy
- report generation is hard to test and lives in a large helper script
- leadership wants the system “moved onto the platform”

That last sentence creates risk immediately because it is larger than the review has
earned.

## Review current truth before proposing change

The first task is not migration. It is review.

A strong review note might say:

> The repository’s strongest stable surface is the versioned publish bundle, but the
> contract is weakened because some downstream consumers still read `results/`. The
> profile boundary is also weak because one profile changes sample-selection semantics.
> Report generation has a clear output surface but unclear implementation ownership.

That note already names three different problems:

- contract drift
- policy leakage
- hidden ownership

Without that review, every later migration sentence stays vague.

## Decide what must not move first

Before discussing platform migration, the team writes down what must remain stable:

- `publish/v1/summary.json`
- `publish/v1/summary.tsv`
- the publish verification route
- the ability to compare profiles honestly

This is the crucial shift. The migration is no longer “move onto the platform.” It is now
“keep trusted outputs and proof routes stable while improving weak boundaries.”

## Sequence the boundary moves

A reckless plan would do all of this at once:

- redesign profiles
- move report code into a package
- change downstream consumers
- integrate platform submission

Instead, the team chooses this order:

1. repair the publish contract boundary
2. repair the policy leak
3. move report implementation behind the same output contract
4. decide what the external platform should own

That order matters because it repairs truth problems before adding architectural motion.

## Repair contract drift first

The team updates the file API and downstream review so notebooks stop reading `results/`
directly.

Proof route used:

- publish verification
- file API review
- downstream comparison against the publish bundle

This is not glamorous work, but it removes one of the biggest migration traps: hidden
consumers of internal state.

## Move semantic settings out of profiles

Next, the suspicious sample filter moves into visible workflow or config surfaces, and
the profile is reduced back to operating policy.

Proof route used:

- profile audit
- dry-run comparison across profiles

At this point the repository becomes easier to reason about even before any external
handoff discussion.

## Migrate implementation without changing outputs

Now the team moves report-generation logic from a large helper script into package code.

The important restraint is that they do not change:

- published file names
- published file meanings
- verification routes

They compare old and new report outputs and keep the same public boundary. This is a real
migration step because ownership moved, but proof stayed visible.

## Revisit the platform request honestly

Only now does the team ask:

> what should the platform actually own?

The answer turns out to be narrower than the original request:

- Snakemake should keep owning sample discovery, orchestration, and publish artifacts
- the platform should own user-triggered requests, job-submission policy, and access control

This is a hybrid answer, and it is the correct one. The repository still explains
workflow truth better than the platform would. The platform explains service behavior
better than the repository would.

## Write governance rules so the problem does not return

The team records three rules:

1. downstream consumers must stay on the published contract
2. profiles may not change workflow meaning
3. migrations must preserve a comparison route until the new boundary earns trust

That is the part many teams skip. Without it, the same drift returns later.

## The repaired stewardship story

By the end of the migration plan, the repository can be described cleanly:

1. current truth is named before redesign
2. contract and policy drift are repaired before bigger movement
3. implementation ownership can change without changing trusted outputs
4. tool handoff is narrower and more honest than the original request
5. governance rules keep the repaired boundaries from decaying again

That is what it means to plan a safe workflow migration.

## Review questions for the repaired design

When you inspect a stewardship plan shaped like this, ask:

1. which current contract was written down before migration
2. which proof route survives the first ownership move
3. which boundary should move later, not now
4. what Snakemake still owns after the external handoff
5. which governance rule prevents the same drift from reappearing

If those answers are visible, the module’s stewardship story has landed.
