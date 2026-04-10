# Rule Shapes and Target Ownership

Make gives you several ways to describe work. The best choice is the one that keeps
ownership of outputs obvious.

This page is about two ideas:

- choosing a rule form that matches the shape of the build
- keeping exactly one recipe responsible for publishing each output path

## The main rule forms

### Explicit rule

Use an explicit rule when one target deserves one clearly named recipe.

```make
app: build/main.o build/util.o
	$(CC) $^ -o $@
```

This is the easiest form to read and review.

### Pattern rule

Use a pattern rule when many targets follow the same shape.

```make
build/%.o: src/%.c include/util.h
	$(CC) -Iinclude -c $< -o $@
```

Pattern rules remove duplication, but they also make matching behavior less obvious. When
in doubt, confirm with `make --trace`.

### Static pattern rule

Use a static pattern rule when you know the exact target list but want one shared shape.

```make
$(OBJS): build/%.o: src/%.c include/util.h
	$(CC) -Iinclude -c $< -o $@
```

This is often a good compromise between repetition and clarity.

## Why ownership matters

The cleanest way to reason about a build is this:

> one output path, one owning recipe

If two recipes can publish the same file, review gets harder fast:

- which recipe is the real source of truth?
- which prerequisites actually matter?
- which recipe ran last?

Those questions are not academic. They show up as flaky builds, surprising rebuilds, and
artifacts that differ by execution path.

## A generator-shaped hazard

Suppose one command creates two files:

```make
schema.json client.py:
	python scripts/gen_client.py
```

This looks neat. It is also easy to misunderstand. Multi-target rules have semantics that
become subtle when one recipe produces several outputs and one output is missing or newer
than another.

Module 01 does not require mastery of every edge case yet. It does require one healthy
instinct:

If one command produces a coupled set of files, treat that coupling deliberately. Do not
casually let Make imply ownership rules you have not reasoned through.

## Rule selection should be explainable

If you choose a pattern or static pattern rule, you should be able to explain:

- why this form is clearer than repeating explicit rules
- what concrete targets it matches
- which output path each invocation owns

If you cannot explain those three points, the abstraction is probably premature.

## A good Module 01 default

For small and medium builds, this is a healthy default:

- explicit rules for the top-level artifacts
- pattern or static pattern rules for repeated compile steps
- no casual multi-writer outputs

That is enough structure to keep the graph readable without turning it into ceremony.
