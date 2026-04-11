# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
your operational reasoning visible, not to show off a pile of flags.

Each answer should show three things:

- the boundary you are defending
- the evidence route you would use
- the repair or decision that follows

## Exercise 1: Separate policy from workflow meaning

Take a small workflow and propose four settings:

- two that belong in a profile
- two that do not belong in a profile

What to hand in:

- the four settings
- one sentence per setting explaining why it belongs where you placed it
- one short explanation of what would go wrong if a semantic setting were moved into a profile

## Exercise 2: Write a small failure policy

Choose one workflow step and describe:

- one transient failure that may be retried
- one failure that must fail fast
- one incomplete-output situation that must rerun instead of being trusted

What to hand in:

- the three situations
- the response for each one
- one sentence explaining how logs help the reviewer tell them apart

## Exercise 3: Review one staging or locality assumption

Describe a workflow that runs locally and on shared infrastructure.

Explain one operational difference that should remain policy and one path or artifact fact
that must stay semantically stable.

What to hand in:

- the operational difference
- the semantically stable path or boundary
- one sentence explaining why confusing the two would create review problems

## Exercise 4: Choose the smallest honest proof route

For each of these questions, choose the smallest honest route:

- how does the workflow plan differ between local and CI contexts
- does the repository still prove itself under its strongest built-in check
- which profile differences are visible to a reviewer

What to hand in:

- the command or route for each question
- one sentence per route explaining why a stronger or weaker route would be less appropriate

## Exercise 5: Review one operational diff like a maintainer

Imagine a pull request that changes a CI profile and a confirmation target.

Describe the order you would review it in and what questions you would ask first.

What to hand in:

- the first file or surface you would inspect
- the second proof route or artifact you would check
- two review questions you would ask before approving the change

## Mastery standard for this exercise set

Across all five answers, Module 03 wants the same habits:

- you name the policy boundary directly
- you distinguish context changes from meaning changes
- you choose proof routes proportionately instead of ritualistically

If your answer says only "production is complicated," keep going.
