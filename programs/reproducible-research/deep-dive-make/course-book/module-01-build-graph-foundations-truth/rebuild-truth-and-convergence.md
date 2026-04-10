# Rebuild Truth and Convergence

Once you see the graph, the next question is whether the graph stays truthful over time.

The practical rule is straightforward:

> A correct build does not just succeed once. It converges. After a successful build,
> running the same build again without meaningful change should produce "nothing to do."

That sounds simple, but many real Makefiles fail here.

## What Make can see by default

Out of the box, Make mainly sees:

- whether a target file exists
- whether a prerequisite is newer than its target
- whether a target is declared phony

That is enough for many file-to-file relationships. It is not enough for every build
fact that matters.

## The hidden-input problem

Some things can change output meaning without appearing in the prerequisite list:

- compiler flags
- environment variables
- tool versions
- generated configuration fragments
- recipe-time discovery of files

If one of those facts changes but the graph does not mention it, Make keeps making a
decision from incomplete evidence.

## A small example

Suppose you write this:

```make
CFLAGS ?= -O2

build/main.o: src/main.c
	$(CC) $(CFLAGS) -c $< -o $@
```

Now you run:

```sh
make CFLAGS=-O0
```

The recipe text changed in a meaningful way, but the graph did not. On the next run,
Make still sees only `src/main.c` and `build/main.o`. It has no file-based evidence that
the object was compiled with different flags.

That is how a build can be "green" while still being untruthful.

## What convergence means

A convergent build has a stable resting state.

This command is a useful probe:

```sh
make clean && make all && make -q all; echo $?
```

After a successful build:

- `0` means Make believes everything is up to date
- `1` means something would rebuild
- `2` means an error occurred

Module 01 wants you to care about that middle case. A build that rebuilds forever without
meaningful change is telling you the graph is unstable.

## Two common ways convergence breaks

### Time-dependent values

```make
BUILD_ID := $(shell date +%s)
```

If that value influences an output, the build meaning changes on every run. The graph has
no stable resting state.

### Unstable file discovery

```make
SRCS = $(wildcard src/*.c)
```

This is not always wrong, but if the resulting list is unordered or if file discovery
changes without being modeled clearly, you can create confusing rebuild behavior.

## The basic repair pattern

Model semantic inputs as explicit, stable artifacts.

One common way is a stamp or manifest whose content changes only when the input meaning
changes. The important property is not the filename. The important property is that the
file becomes trustworthy evidence about a build fact.

## Practical questions for review

- If `CFLAGS` changes, what target proves that change matters?
- If a tool version changes output meaning, where is that fact recorded?
- If a target rebuilds every time, which input is moving even when the source files are
  not?

When you can answer those questions for a real build, you have moved from "it usually
works" to "the graph is telling the truth."
