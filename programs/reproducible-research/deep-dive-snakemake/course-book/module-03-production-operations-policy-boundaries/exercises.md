# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
your operational reasoning visible through concrete runs, failure evidence, and policy
reviews, not through a pile of flags.

## How to work through this set

Treat the ten exercises as one long repository-hardening lab.

Before each answer:

1. name the boundary you are reviewing
2. choose the smallest honest proof route for that boundary
3. keep the concrete evidence next to your explanation

If you skip the boundary question, the work turns into command collection instead of
production reasoning.

Do them in order. The set is one day-long progression:

- Exercises 1-3 establish the policy boundary.
- Exercises 4-6 compare contexts and proof routes.
- Exercises 7-8 classify and repair failures.
- Exercises 9-10 treat production policy as a review surface.

For every answer, keep three things:

- the setting, artifact, or failure class you are naming
- the evidence route you actually used
- one short sentence explaining why the decision belongs to policy or to workflow meaning

## Recommended working layout

If you want one small repository to support the whole day, use a lab tree like this:

```text
module03-lab/
├── Snakefile
├── config/
├── profiles/
├── data/
├── results/
├── publish/
├── logs/
└── artifacts/
```

That layout makes it easier to compare policy surfaces, failure evidence, and proof routes
without rebuilding the project from scratch for every prompt.

Build one small production review packet as you go:

- one table comparing local, CI, and scheduler-facing profile intent
- one paired dry-run comparison for the same semantic target
- one failure-class note that distinguishes retry, fail-fast, and rerun-incomplete cases
- one storage lifecycle sketch that marks where trust begins
- one short proof ladder showing which route answers which operational question
- one maintainer-style review note for a policy diff

If those six artifacts are scattered or missing, the day usually turns into command
memory instead of production reasoning.

```mermaid
flowchart LR
  profiles["name the policy boundary"]
  compare["compare the same semantic target"]
  failures["classify failures before response"]
  storage["mark where trust begins"]
  proof["choose a proof route"]
  review["review policy like a maintainer"]

  profiles --> compare --> failures --> storage --> proof --> review
```

Use that sequence on purpose. It keeps the day anchored in boundary judgment instead of
letting isolated commands impersonate understanding.

## Exercise 1: Separate policy from workflow meaning

Take a small workflow and propose four settings:

- two that belong in a profile
- two that do not belong in a profile

What to hand in:

- the four settings
- one sentence per setting explaining why it belongs where you placed it
- one short explanation of what would go wrong if a semantic setting were moved into a profile

Study note:
This is not a placement quiz. It is a reviewability quiz.

## Exercise 2: Compare the same target across two profiles

Create minimal local and CI profiles for the same small workflow. Vary only operational
settings such as cores, failed-log display, and latency handling.

What to hand in:

- both profile files
- paired dry-runs against the same target
- a table classifying every differing setting
- evidence that the target graph is semantically unchanged
- one plain-language invariant sentence such as "the requested target, sample set, and
  publish meaning did not change"

Study note:
If the job graph changes for the same semantic inputs, treat that as a boundary defect
until you can explain it honestly.

## Exercise 3: Choose the smallest honest proof route

For each of these questions, choose the smallest honest route:

- how does the workflow plan differ between local and CI contexts
- does the repository still prove itself under its strongest built-in check
- which profile differences are visible to a reviewer

What to hand in:

- the command or route for each question
- one sentence per route explaining why a stronger or weaker route would be less appropriate

Study note:
The best answer is not always the strongest route. It is the narrowest route that proves
the claim cleanly.

## Exercise 4: Write a small failure policy

Choose one workflow step and describe:

- one transient failure that may be retried
- one failure that must fail fast
- one incomplete-output situation that must rerun instead of being trusted

What to hand in:

- the three situations
- the response for each one
- one small classification table with columns for failure class, evidence surface, and
  justified response
- one sentence explaining how logs help the reviewer tell them apart

Study note:
If two failure classes get the same response for no stated reason, the policy is probably
too vague.

## Exercise 5: Review one staging or locality assumption

Describe a workflow that runs locally and on shared infrastructure.

Explain one operational difference that should remain policy and one path or artifact fact
that must stay semantically stable.

What to hand in:

- the operational difference
- the semantically stable path or boundary
- one sentence explaining why confusing the two would create review problems

Study note:
This exercise is about holding the final contract still while the execution context moves.

## Exercise 6: Review one operational diff like a maintainer

Imagine a pull request that changes a CI profile and a confirmation target.

Describe the order you would review it in and what questions you would ask first.

What to hand in:

- the first file or surface you would inspect
- the second proof route or artifact you would check
- two review questions you would ask before approving the change

Study note:
Review order matters. Good maintainers do not start from intuition when a named boundary
already exists.

## Midday self-check

Before you move into failure injection and clean-room proof, make sure your packet can
already answer all of these:

- which settings are operational policy and which are semantic leaks
- which comparison route proves that local and CI still mean the same workflow
- which proof route is smaller than `make confirm` but still honest for a bounded claim
- which path or output is trusted and which path is only staging or scratch

If you cannot answer those four questions cleanly, do not rush into later exercises.
Return to the earlier comparisons and make the packet more explicit.

## Exercise 7: Inject and classify failures

Cause three controlled failures: one transient simulation, one invalid configuration, and
one interrupted write to a temporary output.

What to hand in:

- the trigger and observed evidence for each failure
- the retry, fail-fast, or rerun decision
- the log location for each case
- an explanation of why indiscriminate retries would be harmful

Study note:
This is where policy stops being theoretical. If the failure classes blur together here,
the repository will blur them later under pressure too.

## Exercise 8: Design a staging route

Design data movement for a rule that reads shared storage, computes on node-local scratch,
and publishes a declared final output back to shared storage.

What to hand in:

- a diagram of source, scratch, execution, and publication
- cleanup behavior after success and failure
- the profile-owned settings or environment assumptions
- the invariant that must remain identical across local and cluster contexts
- a visible mark on the diagram showing the exact point where downstream trust begins

Study note:
If scratch placement changes what a downstream consumer trusts, the route is wrong.

## Exercise 9: Prove a clean-room run

Run a small workflow from a fresh work directory or isolated checkout without reusing its
previous outputs, caches, or shell history.

What to hand in:

- the exact bounded command route
- environment and input prerequisites
- expected output inventory and checksum evidence
- one hidden dependency the clean-room run exposed or ruled out

Study note:
Clean-room proof is valuable because it punishes undeclared habits. That is the point of
the exercise, not an annoyance.

## Exercise 10: Review a production policy change

Write a review for a proposed profile change that raises resources, enables retries, and
changes a staging location. Treat each line independently.

What to hand in:

- acceptance or rejection for each change
- the failure class the retry policy is intended to cover
- evidence that final outputs and publish boundaries remain stable
- the narrowest verification route that supports your conclusion
- the order in which you reviewed profile policy, failure policy, and storage assumptions

Study note:
Treat this like a maintainer handoff, not like a personal preference memo. If the review
order is invisible, the next maintainer cannot repeat your reasoning under pressure.

## What weak completion looks like

Do not call the day complete if your answers do any of these:

- treat "works locally" as proof that policy is honest
- discuss retries without naming a failure class first
- trust scratch or interrupted outputs because bytes were visible
- jump straight to the strongest route when a smaller one would prove the claim more clearly
- approve a production diff without showing a stable review order

## Exit standard for the exercise day

Do not count the day complete unless you can do all of this without leaning on the answer
page as a command script:

- separate profile policy from workflow meaning confidently
- match a failure class to a recovery decision with evidence
- explain one staging design without confusing scratch and final trust surfaces
- choose one proportionate proof route for one bounded claim
- review one production diff in a stable order

## Mastery standard for this exercise set

Across all ten answers, Module 03 wants the same habits:

- you name the policy boundary directly
- you distinguish context changes from meaning changes
- you choose proof routes proportionately instead of ritualistically

If your answer says only "production is complicated," keep going.
