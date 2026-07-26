# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
operating-context judgment visible through profile comparisons, failure models, and
storage-boundary evidence, not through a pile of flags.

Do them in order. The set is one day-long progression:

- Exercises 1-3 establish profile and semantic boundaries.
- Exercises 4-6 compare contexts and classify settings.
- Exercises 7-8 test resource and storage policy honestly.
- Exercises 9-10 audit drift like a maintainer.

For every answer, keep three things:

- the boundary you are protecting
- the evidence route you actually used
- one short sentence explaining why the decision belongs to operating policy or to workflow meaning

## Exercise 1: Decide whether a profile change is safe

Review a small set of proposed profile edits and decide which are operating policy and
which are semantic leaks.

What to hand in:

- the proposed changes
- one sentence per change explaining your classification
- one change you reject immediately
- one reason the distinction matters to downstream trust

## Exercise 2: Review retries honestly

Choose a recurring failure and decide whether raising retries is justified.

What to hand in:

- the failure symptom
- the failure class you suspect first
- the evidence you inspect before approving retries
- one case where retries would hide a real defect

## Exercise 3: Diagnose a storage-boundary problem

Choose or simulate a workflow that stages outputs through scratch or intermediate storage.

What to hand in:

- the storage route
- the point where an output becomes trusted
- one trust problem created by checking scratch directly
- the policy or documentation boundary that repairs it

## Exercise 4: Compare three contexts

Run the same target through local, CI, and scheduler-oriented profiles and compare the
planned work.

What to hand in:

- the capture commands
- the normalized comparison
- one harmless policy difference
- one semantic difference the comparison would catch

## Exercise 5: Escalate a semantic profile leak

Create or study a profile change that alters config, sample filtering, publish paths, or
some other semantic surface.

What to hand in:

- the leak
- why it is not just a profile choice
- which repository surface should own that decision instead
- what must happen before approval

## Exercise 6: Build a governed policy matrix

Inventory local, CI, and scheduler profile keys and classify each as capacity,
observability, recovery, filesystem, executor mapping, or semantic leak.

What to hand in:

- the full matrix
- disagreements that are justified by context
- duplicate defaults that should be centralized or documented
- every key that should be removed from profile policy

## Exercise 7: Map resources to two executors

Declare threads, memory, runtime, and temporary disk for a heavy rule family, then map
those abstract needs into two operating contexts.

What to hand in:

- the workflow-side resource declarations
- both policy mappings
- an explanation of units and defaults
- evidence that changing the mapping does not change output meaning

## Exercise 8: Verify scratch promotion

Execute or simulate a job through scratch, validation, atomic promotion, and cleanup.
Interrupt it before promotion and inspect every location.

What to hand in:

- the storage lifecycle diagram
- success and interruption inventories
- the point where the output becomes trusted
- recovery behavior that cannot mistake scratch for publication

## Exercise 9: Write an operating-context drift gate

Implement a focused audit that compares governed profile keys and semantic dry-run
surfaces.

What to hand in:

- the governed invariants
- passing and failing evidence
- a precise failure message
- an explanation of what remains intentionally context-specific

## Exercise 10: Review a policy change like a maintainer

Review a change that touches local, CI, and scheduler profiles together with an audit
route.

What to hand in:

- findings ordered by semantic risk
- one accepted policy difference
- one rejected leak
- the narrow verification route supporting each decision

## Mastery standard for this exercise set

Across all ten answers, Module 08 wants the same habits:

- profiles own policy, not workflow meaning
- context comparisons protect trusted outputs
- retries and latency changes require a failure model
- storage and visibility assumptions are part of review, not folklore

If your answer says only "the profiles are different," keep going.
