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

## A quick chooser

| Situation | Best starting choice | Why |
| --- | --- | --- |
| One binary, one archive, one generated report | explicit rule | the target deserves a named contract |
| Many object files built the same way | pattern rule or static pattern rule | avoids noisy duplication while keeping ownership clear |
| A known list of targets with one shared build shape | static pattern rule | keeps the target set visible |
| One command creates several coupled outputs | slow down and model the coupling deliberately | this is where casual rules turn confusing |

## Why ownership matters

The cleanest way to reason about a build is this:

> one output path, one owning recipe

If two recipes can publish the same file, review gets harder fast:

- which recipe is the real source of truth?
- which prerequisites actually matter?
- which recipe ran last?

Those questions are not academic. They show up as flaky builds, surprising rebuilds, and
artifacts that differ by execution path.

Ownership also changes how easy review is. You should be able to answer:

- where does this file come from
- what evidence controls its rebuild
- what recipe has permission to overwrite it

If those answers are spread across multiple rules, you are paying a readability tax every
time someone debugs the build.

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

## A better way to think about multi-output work

Ask two questions before you write the rule:

1. Which file is the outward contract other targets should trust?
2. Are the sibling outputs merely side effects, or are they equally important contracts?

Often the clean answer is to choose one outward artifact and let the other files stay
behind it as implementation detail. That keeps the graph simpler and makes ownership
reviewable.

When that is not possible, say so explicitly in the rule design instead of pretending the
outputs are independent.

## Pattern rules still need human-friendly names

A pattern rule reduces duplication, but the surrounding variables and target names still
decide whether the rule reads clearly.

This is easier to teach and review:

```make
SRC_DIR := src
BLD_DIR := build

$(BLD_DIR)/%.o: $(SRC_DIR)/%.c include/util.h
	$(CC) -Iinclude -c $< -o $@
```

than this:

```make
%.o: %.c
	$(CC) $(X) $(Y) -c $< -o $@
```

The second version is shorter, but it hides the shape of the project. Module 01 should
push you toward clarity before cleverness.

## Rule selection should be explainable

If you choose a pattern or static pattern rule, you should be able to explain:

- why this form is clearer than repeating explicit rules
- what concrete targets it matches
- which output path each invocation owns

If you cannot explain those three points, the abstraction is probably premature.

## A review checklist for this page

- Does each output path have one obvious owner?
- Is the chosen rule form simpler than repeating explicit rules?
- If a pattern is used, can you name the matched files without guessing?
- If a generator produces several files, is the coupling part of the design, not an
  accident?

## A good Module 01 default

For small and medium builds, this is a healthy default:

- explicit rules for the top-level artifacts
- pattern or static pattern rules for repeated compile steps
- no casual multi-writer outputs

That is enough structure to keep the graph readable without turning it into ceremony.
