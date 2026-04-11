# Performance Tuning Without Truth Loss

Once a team can measure cost and triage incidents, the next temptation is obvious:

optimize quickly.

That is where a lot of build systems get into trouble, because "faster" changes are often
proposed in forms like:

- skip a rebuild by dropping a prerequisite
- serialize a flaky route to make the symptom disappear
- cache something without modeling the cache boundary
- reduce logs by removing the evidence that showed the bug

Those changes can make the build look faster. They do not make it healthier.

This page is about a stricter rule:

> a performance change only counts if it reduces waste while preserving the build's truth.

## The sentence to keep

Before calling something a performance improvement, ask:

> what cost did this remove, and what part of the build's evidence or semantic model did it
> preserve?

If the second half of that question has no answer, the change is probably risky.

## Good tuning removes waste, not responsibility

Healthy performance work often removes one of these:

- repeated parse-time shell calls
- unnecessary recomputation of stable derived state
- redundant rule generation
- oversized evidence surfaces that answer no useful question

What it should not remove is:

- a real semantic input
- a necessary rebuild
- a useful diagnostic route
- a safety boundary around publication

The distinction matters because builds are easiest to "speed up" by making them less honest.

## Truth-preserving caching is allowed

One good performance move is to cache expensive derived state behind a truthful boundary.

For example, if discovery or tool probing is expensive, it may be better to generate a
stable manifest from explicit inputs than to rerun the same shell logic on every invocation.

That can look like:

```make
build/discovery.manifest: scripts/list_sources.py src/ | build/
	@python3 scripts/list_sources.py src > $@.tmp
	@cmp -s $@.tmp $@ 2>/dev/null || mv $@.tmp $@
	@rm -f $@.tmp
```

This is healthy if:

- the manifest depends on the right inputs
- the manifest converges
- consumers depend on it honestly

The performance win comes from removing repeated work, not from hiding a dependency.

## Moving shell work into a script can be healthy

Another useful tuning move is consolidating repeated shell logic into one dedicated script
with explicit inputs.

That may improve:

- readability
- maintainability
- parse-time cost

But the script should not become a black box that secretly widens or narrows the build
contract.

The script must still be:

- declared as an input where relevant
- inspectable
- stable enough that its output can be trusted

This is the same architectural discipline from earlier modules, applied to performance work.

## Reducing evidence noise is allowed

A build can also become operationally faster by reducing low-value evidence noise.

Examples:

- replacing scattered debug prints with one bounded diagnostic target
- moving unstable verbose output out of the default route
- creating a named `trace-count` or audit surface instead of flooding every run

This is a legitimate optimization because it reduces the cost of using the build, not only
the wall-clock time of running it.

The important condition is that the build still has a path to the evidence when an incident
occurs.

## Common anti-pattern: tuning by hiding prerequisites

One of the most dangerous fake optimizations is simply hiding an input so fewer rebuilds
happen.

That may feel like a performance win because the build does less work. It is still a defect
because the build is now lying about when work is needed.

This includes moves like:

- dropping a header prerequisite
- ignoring a generator input
- quietly freezing a variable that still changes artifact meaning

Fast wrong builds are still wrong. This course has been saying that since Module 01, and it
still applies here.

## Common anti-pattern: tuning by removing evidence

Another false win is removing the very evidence that helped reveal a real problem:

- deleting diagnostic routes because they produce too much output
- suppressing useful trace instead of making it bounded
- removing selftests because they cost time

Sometimes the evidence surface does need redesign. It should not simply disappear because
its presence is inconvenient.

The right question is:

> how do we make the evidence cheaper or more targeted without losing the ability to explain
> the build?

That is a much better tuning posture.

## Common anti-pattern: tuning by serialization

When a parallel route is flaky, teams often force serial behavior and call the problem
solved.

That can reduce operational pain temporarily. It is not automatically a legitimate
performance or correctness fix.

If the route was flaky because of:

- a shared output path
- a missing edge
- non-atomic publication

then serialization is hiding a truth problem, not solving it.

This is why the module keeps tying tuning back to incident classification.

## A good tuning note should sound like this

A strong performance change summary sounds like:

> We moved repeated discovery shell-outs into a stable manifest generated from explicit
> inputs. `make -n all` dropped from `2.4s` to `0.7s`. The manifest remains convergent and
> the consumer edges still point at the same resolved source set.

That is much stronger than:

> We optimized the Makefiles and now they feel faster.

The difference is not style. It is evidence and semantic accountability.

## Failure signatures worth recognizing

### "The build got faster, but now the wrong things stay stale"

That means the tuning change removed truth, not waste.

### "The default route is quieter, but we lost our best incident signal"

That means observability was removed instead of redesigned.

### "`-j1` fixed the issue, so we kept it"

That usually means a real correctness problem is still hiding under the performance choice.

### "We cached something expensive, but no one can explain the cache boundary"

That means the optimization is not yet trustworthy.

## A review question that improves tuning discipline

Take one proposed performance change and ask:

1. which cost layer it is reducing
2. what measurement shows the cost exists
3. what semantic inputs or evidence surfaces the change depends on
4. how the truth boundary remains preserved
5. what command would verify that the build is still honest afterward

If those answers are weak, the tuning change is probably weak too.

## What to practice from this page

Choose one expensive build habit and write down:

1. the layer where the cost lives
2. the current measurement
3. the proposed truth-preserving change
4. the evidence you would compare after the change
5. one reason the change is safer than a shortcut that simply hides work

If you can do that clearly, you are doing real build tuning rather than just chasing
"faster" feelings.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- what makes a performance change truth-preserving
- why truthful caching is different from hiding dependencies
- why reducing evidence noise can be legitimate if the evidence remains available
- why serialization is not automatically a healthy optimization
- how to describe a performance change with both measurement and semantic accountability
