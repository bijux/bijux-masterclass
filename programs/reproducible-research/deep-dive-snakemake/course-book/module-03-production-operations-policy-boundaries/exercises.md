# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
your operational reasoning visible through concrete runs, failure evidence, and policy
reviews, not through a pile of flags.

Do them in order. The set is one day-long progression:

- Exercises 1-3 establish the policy boundary.
- Exercises 4-6 compare contexts and proof routes.
- Exercises 7-8 classify and repair failures.
- Exercises 9-10 treat production policy as a review surface.

For every answer, keep three things:

- the setting, artifact, or failure class you are naming
- the evidence route you actually used
- one short sentence explaining why the decision belongs to policy or to workflow meaning

## Exercise 1: Separate policy from workflow meaning

Take a small workflow and propose four settings:

- two that belong in a profile
- two that do not belong in a profile

What to hand in:

- the four settings
- one sentence per setting explaining why it belongs where you placed it
- one short explanation of what would go wrong if a semantic setting were moved into a profile

## Exercise 2: Compare the same target across two profiles

Create minimal local and CI profiles for the same small workflow. Vary only operational
settings such as cores, failed-log display, and latency handling.

What to hand in:

- both profile files
- paired dry-runs against the same target
- a table classifying every differing setting
- evidence that the target graph is semantically unchanged

## Exercise 3: Choose the smallest honest proof route

For each of these questions, choose the smallest honest route:

- how does the workflow plan differ between local and CI contexts
- does the repository still prove itself under its strongest built-in check
- which profile differences are visible to a reviewer

What to hand in:

- the command or route for each question
- one sentence per route explaining why a stronger or weaker route would be less appropriate

## Exercise 4: Write a small failure policy

Choose one workflow step and describe:

- one transient failure that may be retried
- one failure that must fail fast
- one incomplete-output situation that must rerun instead of being trusted

What to hand in:

- the three situations
- the response for each one
- one sentence explaining how logs help the reviewer tell them apart

## Exercise 5: Review one staging or locality assumption

Describe a workflow that runs locally and on shared infrastructure.

Explain one operational difference that should remain policy and one path or artifact fact
that must stay semantically stable.

What to hand in:

- the operational difference
- the semantically stable path or boundary
- one sentence explaining why confusing the two would create review problems

## Exercise 6: Review one operational diff like a maintainer

Imagine a pull request that changes a CI profile and a confirmation target.

Describe the order you would review it in and what questions you would ask first.

What to hand in:

- the first file or surface you would inspect
- the second proof route or artifact you would check
- two review questions you would ask before approving the change

## Exercise 7: Inject and classify failures

Cause three controlled failures: one transient simulation, one invalid configuration, and
one interrupted write to a temporary output.

What to hand in:

- the trigger and observed evidence for each failure
- the retry, fail-fast, or rerun decision
- the log location for each case
- an explanation of why indiscriminate retries would be harmful

## Exercise 8: Design a staging route

Design data movement for a rule that reads shared storage, computes on node-local scratch,
and publishes a declared final output back to shared storage.

What to hand in:

- a diagram of source, scratch, execution, and publication
- cleanup behavior after success and failure
- the profile-owned settings or environment assumptions
- the invariant that must remain identical across local and cluster contexts

## Exercise 9: Prove a clean-room run

Run a small workflow from a fresh work directory or isolated checkout without reusing its
previous outputs, caches, or shell history.

What to hand in:

- the exact bounded command route
- environment and input prerequisites
- expected output inventory and checksum evidence
- one hidden dependency the clean-room run exposed or ruled out

## Exercise 10: Review a production policy change

Write a review for a proposed profile change that raises resources, enables retries, and
changes a staging location. Treat each line independently.

What to hand in:

- acceptance or rejection for each change
- the failure class the retry policy is intended to cover
- evidence that final outputs and publish boundaries remain stable
- the narrowest verification route that supports your conclusion

## Mastery standard for this exercise set

Across all ten answers, Module 03 wants the same habits:

- you name the policy boundary directly
- you distinguish context changes from meaning changes
- you choose proof routes proportionately instead of ritualistically

If your answer says only "production is complicated," keep going.
