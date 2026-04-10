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

## One writer per output path

This is the rule to remember:

> one output path, one owning recipe

If two recipes can both write `shared.log`, `tmp.out`, or `gen.h`, you have a race even
before you run the build in parallel. Concurrency only makes the race visible.

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

## Safer default

Derive the temporary path from `$@` so each target has its own workspace:

```make
tmp="$@.tmp"
```

That does not solve every problem, but it removes one common parallel hazard fast.
