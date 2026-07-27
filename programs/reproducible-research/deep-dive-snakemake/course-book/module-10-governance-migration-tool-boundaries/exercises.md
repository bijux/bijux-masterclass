# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
stewardship judgment visible through inventories, migration sequences, governance rules,
and ownership contracts, not through vague redesign language.

## How to use this exercise set

Do the ten exercises in order.

The set is a one-day progression:

- Exercises 1-3 establish current truth and governance language.
- Exercises 4-6 classify anti-patterns and build a current-truth inventory.
- Exercises 7-8 preserve proof through one ownership move.
- Exercises 9-10 enforce governance and design an honest handoff.

For every answer, keep three things:

- the boundary you are naming
- the evidence route you actually used
- one short sentence explaining why the change preserves trust instead of only improving taste

If you want the full value of the set, write every answer as if another maintainer must
review it without oral context from you.

## Exercise 1: Review the current repository honestly

Choose a workflow repository with a mix of trusted outputs and awkward drift.

What to hand in:

- the top three risks in boundary language
- which risk you would address first
- the existing evidence route you inspect before proposing migration
- one awkward behavior you must describe honestly before changing it

## Exercise 2: Sequence a migration

Choose three desired changes such as moving report logic, changing discovery, or shifting
submission responsibility.

What to hand in:

- the safer order for the three changes
- which boundary moves first
- what proof must survive each step
- which change should wait until later and why

## Exercise 3: Write governance rules the team can keep using

Draft three short governance rules for a workflow team that keeps repeating preventable
mistakes.

What to hand in:

- the three rules
- the repository surface each rule protects
- one example of a change each rule would reject
- one reason the wording is short enough to survive real review

## Exercise 4: Name the anti-pattern family

Review a change that mixes evidence removal, undocumented publish drift, and semantic
settings hidden inside operating policy.

What to hand in:

- the anti-pattern family for each change
- which change is most dangerous and why
- the recovery step you would require first
- the proof route you would consult before approving anything else

## Exercise 5: Decide the tool boundary

Choose a request where another system wants user-triggered requests, access control,
tenancy-aware scheduling, or service behavior layered around a Snakemake repository.

What to hand in:

- what Snakemake should keep owning
- what another system should own
- the handoff artifact or schema that makes the split trustworthy
- one ownership line you refuse to blur

## Exercise 6: Build a current-truth inventory

Audit a workflow repository and record declared targets, actual consumers, semantic
configuration, profile policy, software boundaries, publish contracts, and proof routes.

What to hand in:

- the inventory with evidence links or commands
- mismatches between documentation and behavior
- risks ordered by trust impact
- facts that must be preserved before any migration

## Exercise 7: Write characterization checks

Choose one awkward but relied-upon behavior and encode focused checks for target
membership, file schema, and representative output semantics.

What to hand in:

- the behavior and known consumers
- checks that pass against the current implementation
- a deliberately incompatible candidate that fails
- an explanation of what the checks intentionally do not freeze

## Exercise 8: Migrate one ownership boundary

Move one report, helper, or discovery concern to a better owner while retaining the same
public outputs.

What to hand in:

- the old and candidate ownership diagrams
- byte-level or semantic comparison appropriate to each output
- focused proof before and after the move
- rollback criteria

## Exercise 9: Enforce one governance rule

Automate one recurring rule such as:

- published files require file-API coverage
- profiles cannot own semantic keys
- important helpers require direct tests and declared inputs

What to hand in:

- the durable policy statement
- the focused implementation
- passing and failing fixtures
- a failure message that tells a maintainer how to repair the boundary

## Exercise 10: Design and review a tool handoff

Keep Snakemake responsible for file-based execution while an external service owns user
requests, identity, access, or tenancy-aware scheduling.

What to hand in:

- request, status, cancellation, and result schemas
- ownership and failure table
- idempotency and provenance strategy
- an end-to-end proof that the returned publish bundle remains independently verifiable

## Mastery standard for this exercise set

Across all ten answers, Module 10 wants the same habits:

- review comes before redesign
- migrations move one boundary at a time
- governance protects contracts, policy boundaries, proof, and ownership clarity
- tool-boundary decisions are about responsibility and evidence, not trend-following

If your answer says only "the workflow should be modernized," keep going.
