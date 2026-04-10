# Parallel Safety Contract

Parallel safety is simpler than it first sounds. The contract is small and strict:

1. one writer per output path
2. publish real outputs atomically
3. do not let consumers observe partial artifacts
4. clean up failure paths
5. avoid shared appends and shared temporary files

If one of those is broken, `-j` eventually exposes it.

## The main idea

Parallel builds are safe when every output path has one clear owner and each owner
publishes its result in a way other targets can trust.

That means parallel safety is not mainly about threads or locks. It is about artifact
contracts.

## The contract in plain language

If another target is going to trust a path, then that path needs three things:

- one clear owner
- a complete value when it appears
- cleanup discipline when the publish fails

If any of those are missing, concurrency becomes dangerous because two truths are now in
conflict: the path exists, but the contract behind the path is unstable.

## One writer per output path

This is the rule to remember:

> one output path, one owning recipe

If two recipes can both write `shared.log`, `tmp.out`, or `gen.h`, you have a race even
before you run the build in parallel. Concurrency only makes the race visible.

This also means that "temporary" paths count. Learners often think of `tmp.out` as an
implementation detail that does not matter. It matters the moment more than one recipe can
touch it.

## Shared appends are nondeterministic

This is a bad shape:

```make
a:
	printf 'A\n' >> shared.log

b:
	printf 'B\n' >> shared.log
```

Even if both writes succeed, the final content or ordering may vary. That is not a small
stylistic issue. That is an output contract failure.

The repair is usually not "append more carefully." The repair is to stop pretending the
shared file has two owners. Give each target its own output and then introduce a single
aggregation step if the combined file is still needed.

## Shared temporary files are also multi-writer outputs

This is another bad shape:

```make
x:
	printf 'X\n' > tmp.out
	mv -f tmp.out x.out

y:
	printf 'Y\n' > tmp.out
	mv -f tmp.out y.out
```

`tmp.out` is an output path too. If two recipes can write it, they are already breaking
the contract.

## Publication and failure belong together

Atomic publish is only half the story. Failure hygiene matters too:

- remove temps when the recipe fails
- avoid leaving plausible final outputs behind
- use `.DELETE_ON_ERROR` as baseline protection

Parallel safety is weaker than it looks if failure paths are sloppy. A race that fails
cleanly is still a bug, but a race that leaves poison artifacts behind is much harder to
diagnose.

## Safer default

Derive the temporary path from `$@` so each target has its own workspace:

```make
tmp="$@.tmp"
```

That does not solve every problem, but it removes one common parallel hazard fast.

## A review checklist for this page

- Does every output path have one obvious owner?
- Does every real artifact appear only after success?
- Could any consumer observe a partial file?
- Are there any shared appends, shared temps, or shared stamp outputs?
- Would a failed run leave behind something another target might trust?

## End-of-page checkpoint

Before leaving this page, you should be able to explain:

- why shared append is an output-ownership bug
- why temp files count as outputs too
- why atomic publication and failure cleanup belong in the same discussion
- how you would review a rule for parallel safety without running it yet
