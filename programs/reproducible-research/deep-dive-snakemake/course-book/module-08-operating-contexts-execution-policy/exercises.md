# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
operating-context judgment visible through profile comparisons, failure models, and
storage-boundary evidence, not through a pile of flags.

## How to work through this set

Treat this set as one full operating-context audit day.

For each exercise, keep three things together:

- the boundary you are protecting
- the evidence route you actually used
- one plain-language note about why the decision belongs to operating policy or to
  workflow meaning

If your answer cannot say what stayed semantically invariant and what changed only in
operations, the exercise is not finished yet.

Do them in order. The set is one day-long progression:

- Exercises 1-3 establish profile and semantic boundaries.
- Exercises 4-6 compare contexts and classify settings.
- Exercises 7-8 test resource and storage policy honestly.
- Exercises 9-10 audit drift like a maintainer.

For every answer, keep three things:

- the boundary you are protecting
- the evidence route you actually used
- one short sentence explaining why the decision belongs to operating policy or to
  workflow meaning

## Recommended working layout

Build one small policy-review packet as you go:

- a profile comparison sheet
- one dry-run comparison
- one failure-class note
- one storage lifecycle diagram
- one focused drift gate with a deliberate failing example

## Exercise 1: Decide whether a profile change is safe

Review a small set of proposed profile edits and decide which are operating policy and
which are semantic leaks.

What to hand in:

- the proposed changes
- one sentence per change explaining your classification
- one change you reject immediately
- one reason the distinction matters to downstream trust

Study note:
If you cannot classify a profile key cleanly, the profile boundary is already under
defined.

## Exercise 2: Review retries honestly

Choose a recurring failure and decide whether raising retries is justified.

What to hand in:

- the failure symptom
- the failure class you suspect first
- the evidence you inspect before approving retries
- one case where retries would hide a real defect

Study note:
Do not start with “how many retries?” Start with “what kind of failure is this?”

## Exercise 3: Diagnose a storage-boundary problem

Choose or simulate a workflow that stages outputs through scratch or intermediate storage.

What to hand in:

- the storage route
- the point where an output becomes trusted
- one trust problem created by checking scratch directly
- the policy or documentation boundary that repairs it

Study note:
This exercise is about when trust starts, not when bytes first appear.

## Exercise 4: Compare three contexts

Run the same target through local, CI, and scheduler-oriented profiles and compare the
planned work.

What to hand in:

- the capture commands
- the normalized comparison
- one harmless policy difference
- one semantic difference the comparison would catch

Study note:
Do not normalize away the very things that prove semantic drift.

## Exercise 5: Escalate a semantic profile leak

Create or study a profile change that alters config, sample filtering, publish paths, or
some other semantic surface.

What to hand in:

- the leak
- why it is not just a profile choice
- which repository surface should own that decision instead
- what must happen before approval

Study note:
If the change affects trusted outputs or path contracts, it has already escaped pure
policy.

## Exercise 6: Build a governed policy matrix

Inventory local, CI, and scheduler profile keys and classify each as capacity,
observability, recovery, filesystem, executor mapping, or semantic leak.

What to hand in:

- the full matrix
- disagreements that are justified by context
- duplicate defaults that should be centralized or documented
- every key that should be removed from profile policy

Study note:
This is where policy review stops being anecdotal and becomes auditable.

## Exercise 7: Map resources to two executors

Declare threads, memory, runtime, and temporary disk for a heavy rule family, then map
those abstract needs into two operating contexts.

What to hand in:

- the workflow-side resource declarations
- both policy mappings
- an explanation of units and defaults
- evidence that changing the mapping does not change output meaning

Study note:
The mapping may vary. The trusted contract may not.

## Exercise 8: Verify scratch promotion

Execute or simulate a job through scratch, validation, atomic promotion, and cleanup.
Interrupt it before promotion and inspect every location.

What to hand in:

- the storage lifecycle diagram
- success and interruption inventories
- the point where the output becomes trusted
- recovery behavior that cannot mistake scratch for publication

Study note:
If reviewers could trust the wrong location after interruption, the storage boundary is
too weak.

## Exercise 9: Write an operating-context drift gate

Implement a focused audit that compares governed profile keys and semantic dry-run
surfaces.

What to hand in:

- the governed invariants
- passing and failing evidence
- a precise failure message
- an explanation of what remains intentionally context-specific

Study note:
A good gate tells the maintainer exactly which invariant leaked and where.

## Exercise 10: Review a policy change like a maintainer

Review a change that touches local, CI, and scheduler profiles together with an audit
route.

What to hand in:

- findings ordered by semantic risk
- one accepted policy difference
- one rejected leak
- the narrow verification route supporting each decision

Study note:
This is a maintainership exercise, not a “profiles differ by environment” exercise.

## Mastery standard for this exercise set

Across all ten answers, Module 08 wants the same habits:

- profiles own policy, not workflow meaning
- context comparisons protect trusted outputs
- retries and latency changes require a failure model
- storage and visibility assumptions are part of review, not folklore

If your answer says only "the profiles are different," keep going.

## Exit standard for the exercise day

You are done only when you can defend all of these clearly:

- which settings belong in profiles and which do not
- which outputs and paths stay semantically invariant across contexts
- which failure class justifies one retry or latency change
- where temporary storage ends and trusted output begins
- which drift difference is harmless policy and which is a leak
