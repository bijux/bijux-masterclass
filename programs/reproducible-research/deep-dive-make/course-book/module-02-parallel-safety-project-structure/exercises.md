# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
your reasoning visible, not to show off Make syntax.

## Exercise 1: Name the runnable targets

Take the `m02/` simulator and explain which targets may run concurrently during a clean
build and why.

What to hand in:

- a short graph sketch or target list
- one sentence per concurrently runnable target group
- one sentence naming which target must wait and why

## Exercise 2: Repair a shared-log race

Explain why `repro/01-shared-log.mk` is nondeterministic under `-j`, then redesign it so
one target owns the final log.

What to hand in:

- the bug explanation in plain language
- the repaired target layout
- one command you would run to prove the repaired log is stable

## Exercise 3: Repair a temporary-file collision

Explain why `repro/02-temp-collision.mk` is unsafe, then redesign it so each target uses
its own temporary path.

What to hand in:

- the shared path that causes the race
- the repaired temp-path pattern
- a short explanation of why temp files still count as output ownership

## Exercise 4: Choose the right ordering tool

Give one example that needs a real prerequisite, one that needs an order-only
prerequisite, and one that needs a stamp.

What to hand in:

- three short rule fragments
- one sentence per fragment explaining why that ordering tool is honest

## Exercise 5: Design a selftest

Describe the checks your `selftest` target must perform to prove parallel safety on the
declared artifact set.

What to hand in:

- the ordered checklist the selftest should run
- the artifact set it should compare
- the failure signal that would tell you the build still lies

## Mastery standard for this exercise set

Across all five answers, the module wants three things:

- you name the graph fact being tested
- you show which command or artifact proves it
- you explain the repair in terms of truth, ownership, or scheduling

If your answer only says "parallel builds are tricky," keep going.
