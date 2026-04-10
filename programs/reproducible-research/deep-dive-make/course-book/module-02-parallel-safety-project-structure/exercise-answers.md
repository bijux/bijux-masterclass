# Exercise Answers

Use this after you have written your own answers. The point is comparison, not copying.

## Exercise 1: Name the runnable targets

Independent object-file targets may run concurrently once their prerequisites are ready.
The final link target cannot run until those object files are complete. A good answer
names the exact edges that justify the scheduling.

## Exercise 2: Repair a shared-log race

The bug is that two recipes append to the same output path. A good repair gives each
target its own log and then introduces one aggregation target that deterministically
creates the shared log.

## Exercise 3: Repair a temporary-file collision

The bug is that `tmp.out` is a shared output path. A safe repair derives the temporary
path from `$@`, so each target publishes through its own temp file.

## Exercise 4: Choose the right ordering tool

A real prerequisite is correct when content changes should trigger rebuilds. An order-only
prerequisite is correct for setup such as directory existence. A stamp is correct when a
semantic input matters but has no natural file edge.

## Exercise 5: Design a selftest

A strong answer includes convergence, serial/parallel equivalence, and a runtime check on
the declared artifacts. The selftest should fail on the first observed divergence rather
than printing vague reassurance.
