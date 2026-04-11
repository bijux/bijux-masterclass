# Measuring Parse, Recipe, and Evidence Cost

One of the most common mistakes in build-performance work is using the word "slow" as if it
meant one thing.

It rarely does.

A build can feel slow because:

- Make spends too much time parsing or expanding
- recipes do expensive real work
- diagnostics and trace volume are operationally heavy
- humans cannot tell which of those is happening, so they make the wrong changes

This page is about separating those costs before tuning begins.

## The sentence to keep

When someone says "the build is slow," ask:

> slow in which layer: parse and evaluation, recipe execution, or evidence and diagnostics?

That question prevents a lot of wasted work.

## Not all build time lives in the same place

A Make-based system has at least three performance surfaces worth naming:

1. parse and evaluation cost
2. recipe execution cost
3. evidence-surface cost

Each one creates a different kind of problem and needs a different kind of fix.

Treating them as one undifferentiated "performance problem" is how teams end up rewriting
the wrong layer.

## Parse and evaluation cost

This is the time Make spends:

- reading included files
- expanding variables
- running parse-time shell expressions
- constructing its internal view of the graph

Typical warning signs:

- `make -n all` already feels heavy
- the build has many `$(shell ...)` calls
- include files do expensive work at parse time
- rule generation or repeated expansions dominate before any real tool runs

This cost is architectural. It has more to do with how the build is described than with how
expensive the compiler or tests are.

## Recipe execution cost

This is the time spent in the actual external work:

- compilation
- linking
- testing
- packaging
- code generation

Typical warning signs:

- `make -n all` is cheap, but `make all` is expensive
- one tool invocation dominates the wall clock
- adding cores or changing tool flags matters more than changing Make structure

This is often where teams incorrectly blame Make for costs that belong to the underlying
tools.

## Evidence-surface cost

This is the cost of making the build understandable:

- trace volume
- dump size
- amount of output humans must sift through during incidents

This cost matters because a build can be semantically correct and still be operationally
painful if its evidence is too noisy to use under pressure.

Examples:

- `--trace` output is enormous
- one incident requires scrolling through thousands of low-value lines
- diagnostic targets dump unstable or redundant information no one can use

This is not purely cosmetic. Observability quality affects how quickly the team can debug
the build.

## A simple measurement loop

Start with a minimal loop:

```sh
/usr/bin/time -p make -n all >/dev/null
/usr/bin/time -p make all >/dev/null
make --trace all > build/trace.log
wc -l build/trace.log
```

This gives you:

- a dry-run timing signal for parse and decision work
- a full-build timing signal that includes real recipe cost
- a rough trace-volume signal

That is not a full profiler. It is enough to stop guessing blindly.

## Why `make -n` is such a useful lens

`make -n` does not execute recipes, but it still performs parse and graph work.

That means:

- if `make -n all` is already expensive, your first suspect is not the compiler
- if `make -n all` is cheap and `make all` is expensive, your first suspect is probably not Make itself

This is one of the simplest and most useful distinctions in the module.

It lets you say:

> this complaint is about build description overhead

or:

> this complaint is about recipe work

Those are very different diagnoses.

## Trace volume is a real operational metric

Some engineers treat trace volume as secondary because it does not always change wall-clock
time much. That misses the point.

A build whose evidence is too large or too noisy can still be expensive in practice because:

- incidents take longer to diagnose
- maintainers avoid using the evidence surfaces
- real signals get buried under routine noise

That is why a simple metric like trace line count can still be useful:

```sh
make --trace all > build/trace.log
wc -l build/trace.log
```

The goal is not "fewest lines wins." The goal is to notice whether the build is producing
an evidence surface that another engineer can actually work with.

## A small comparison example

Imagine two measurements.

### Case A

```text
make -n all   -> 2.9s
make all      -> 3.2s
trace lines   -> 240
```

This suggests the build description and decision process are consuming most of the cost.

### Case B

```text
make -n all   -> 0.2s
make all      -> 18.0s
trace lines   -> 180
```

This suggests the performance problem mostly lives in recipes, not in Make's own structure.

This is why measurement separation matters so much. It changes what a rational next move
looks like.

## Parse cost often comes from habits, not obvious bugs

A build may have parse overhead because of design habits like:

- repeated `$(shell find ...)`
- overuse of `eval`
- broad, unsorted discovery
- too many layers doing similar work at parse time

These are not dramatic failures. They are accumulations.

That is why Module 09 frames performance work as architecture plus operations, not just
micro-optimizations.

## Recipe cost often needs tool-level thinking

When recipe time dominates, the right next question is often not:

> how do we optimize the Makefiles?

It is often:

> which tool invocation is doing the expensive work, and is that work justified?

This might point to:

- compilation flags
- test scope
- packaging compression level
- repeated code generation

Make still matters because it orchestrates those steps, but the cost may not belong to its
own layer.

## Evidence cost should stay proportional to the incident value

A build should expose enough evidence to make incidents explainable. It should not emit so
much routine noise that the team stops using its own observability surfaces.

That means observability design is part of performance design:

- bounded diagnostic targets
- clear trace usage
- no unstable debug prints inside semantic outputs

This is the part of performance work many teams ignore until an incident forces them to
care.

## Failure signatures worth recognizing

### "`make -n all` is already slow"

That usually points to parse, expansion, or discovery cost.

### "`make all` is slow, but dry-run is cheap"

That usually points to real tool or recipe cost rather than Make structure.

### "We technically have trace output, but nobody can use it under pressure"

That means evidence-surface cost is too high.

### "We optimized something and saw no measurable difference"

That usually means the change targeted the wrong layer.

## A review question that improves measurement work

Before anyone proposes a build-performance change, ask:

1. which layer appears expensive
2. what measurement supports that claim
3. what command was used
4. what a contrasting measurement would have looked like
5. whether the proposed change actually targets that layer

If those answers are weak, the tuning proposal is probably weak too.

## What to practice from this page

Choose one build route and produce a short measurement note:

1. dry-run time
2. full-build time
3. trace line count
4. your best guess about which layer dominates
5. one next experiment to validate that guess

If you can do that clearly, you have already improved the quality of performance
discussion a lot.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why "slow build" is not a sufficient diagnosis
- what parse and evaluation cost means
- what recipe cost means
- why evidence-surface cost is operationally real
- how a small measurement loop can change the next engineering decision
