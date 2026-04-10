# Evaluation and Expansion

Many Make bugs come from one quiet misunderstanding:

> some things happen while Make is reading the file, and other things happen later when a
> recipe runs in the shell.

If you blur those moments together, builds feel nondeterministic even when the syntax is
valid.

## Two different moments

### Read time

When Make parses the Makefile, it expands some variables, chooses rules, and builds its
internal model of the graph.

### Recipe time

Later, when a target needs rebuilding, Make launches a shell and executes the recipe.

That distinction matters because a value computed at read time can affect the graph before
any recipe runs.

## The assignment operators you need first

### `:=` immediate assignment

```make
SRCS := $(sort $(wildcard src/*.c))
```

Make computes the value once when reading the file. This is a good default for lists you
want to stay stable.

### `=` recursive assignment

```make
SRCS = $(wildcard src/*.c)
```

Make stores the recipe for computing the value and expands it later when the variable is
used. This is useful, but it is easier to misuse.

### `?=` and `+=`

Use `?=` for defaults and `+=` for simple extension. They are helpful, but they do not
replace the need to understand when evaluation happens.

## Why `$(shell ...)` deserves caution

`$(shell ...)` runs while Make is expanding the variable.

That means a line like this can change the graph before any recipe executes:

```make
BUILD_ID := $(shell date +%s)
```

If that value is part of target naming, prerequisites, or command selection, your build
definition itself changes every time Make reads the file.

That is how "we did not change the source" turns into "the build still changed."

## A safer Module 01 posture

- prefer `:=` for computed lists and flags
- sort discovered file lists so they stay stable
- treat `$(shell ...)` as a design choice, not harmless convenience
- inspect `make -p` when variable origin or value seems surprising

## Useful introspection tools

When a variable behaves oddly, these are worth knowing:

```make
$(origin VAR)
$(flavor VAR)
$(value VAR)
```

They tell you where a variable came from, how it expands, and what raw value it holds.

Those are not "advanced tricks." They are often the shortest path out of confusion.

## Review questions

- Is this value supposed to be fixed when Make starts, or recomputed later?
- Could this expansion depend on time, environment, or filesystem order?
- If the value changes build meaning, where is that change made visible to the graph?

When you ask those questions early, Make stops feeling moody and starts feeling legible.
