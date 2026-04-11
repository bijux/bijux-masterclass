# Portability Contract and Version Gates

Portability is one of the most abused words in build engineering.

Teams say things like:

- "it should be portable"
- "it mostly works on macOS"
- "CI has a newer Make, but that is probably fine"
- "if Bash is missing, people can install it"

None of that is a contract. It is hope with a few anecdotes attached.

This page is about replacing that habit with a clearer one:

> say exactly which tools, versions, and shell behaviors the build requires, and fail
> early when those conditions are not met.

That is not less portable. It is more honest. Honest boundaries are what let you add safe
fallbacks without turning the build into folklore.

## The sentence to keep

When someone asks whether the build is portable, the right answer is not "yes."

The right answer sounds more like this:

> this build requires GNU Make 4.3 or later, a POSIX shell, and `python3`; grouped targets
> are optional because we provide a stamp fallback.

That sentence is useful because another engineer can test it.

## What a portability contract actually contains

A real portability contract usually needs four parts:

1. the minimum supported Make behavior
2. the shell model the recipes assume
3. the required external tools
4. the optional features and their fallbacks

If any one of those is left implied, the build starts leaning on workstation luck.

## Required is different from optional

One of the biggest mistakes learners make is treating every tool or feature as if it were
equally negotiable.

They are not.

Use this split:

| Kind | Meaning | Build behavior |
| --- | --- | --- |
| required | without it, correctness is undefined | fail fast |
| optional | nice to have, but not essential to core correctness | warn or use a safe fallback |
| unsupported | explicitly outside the contract | fail clearly and say why |

This is important because "best effort" builds often hide correctness drift behind soft
fallbacks that were never reviewed.

## Version gates are capability gates in disguise

Suppose the build wants grouped targets `&:`. The important question is not "which machine
am I on?" The important question is:

> does this Make provide the semantics required for grouped targets?

That is why version gates should be tied to capabilities, not to tribal knowledge.

For example:

```make
ifeq ($(origin MAKE_VERSION),undefined)
$(error this repository requires GNU Make)
endif

HAVE_GROUPED_TARGETS := $(if $(filter 4.3% 4.4% 4.5% 5.%,$(MAKE_VERSION)),yes,)

ifeq ($(HAVE_GROUPED_TARGETS),)
  USE_GROUPED_TARGETS := no
else
  USE_GROUPED_TARGETS := yes
endif
```

Now the build can branch on a named capability rather than on an undocumented assumption.

## The shell is part of the contract too

Recipes run inside a shell. That means the shell is not an implementation detail. It is a
semantic dependency.

If your recipes assume:

- Bash arrays
- `pipefail`
- `[[ ... ]]`
- brace expansion
- process substitution

then you do not have a plain POSIX shell contract anymore. You have a Bash contract.

That can still be a valid decision. The mistake is hiding it.

For this course, the healthy default is:

- write recipes for POSIX `/bin/sh`
- keep shell behavior simple and explicit
- choose a stricter shell contract only when the benefit is worth stating aloud

## A simple shell mistake

This recipe is not POSIX `/bin/sh`:

```make
check:
	@if [[ -f config.env ]]; then echo ok; fi
```

It may work on one machine where `/bin/sh` is really Bash-compatible, then fail on another
machine where `/bin/sh` is stricter.

If you only need POSIX behavior, write:

```make
check:
	@if [ -f config.env ]; then echo ok; fi
```

This is not glamorous advice. It is the kind of choice that prevents avoidable portability
incidents.

## Tool requirements should be declared once

Many inherited Makefiles discover tools in a scattered, repetitive way:

```make
PYTHON := $(shell command -v python3 || command -v python)
TAR := $(shell command -v gtar || command -v tar)
AWK := $(shell command -v gawk || command -v awk)
```

This creates three problems:

1. the policy is spread out
2. the fallback order is hard to review
3. the build may silently switch tools with different semantics

A calmer pattern is to centralize tool requirements:

```make
PYTHON ?= python3
TAR ?= tar

.PHONY: contract-check
contract-check:
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "missing $(PYTHON)" >&2; exit 1; }
	@command -v $(TAR) >/dev/null 2>&1 || { echo "missing $(TAR)" >&2; exit 1; }
```

Now the contract is:

- these are the tool names we expect
- callers may override them intentionally
- the build checks them in one place

That is much easier to teach and audit.

## Fallbacks must preserve correctness

Not all fallbacks are healthy.

Healthy fallback:

- grouped targets unavailable, so use a stamp-governed generation rule

Unhealthy fallback:

- grouped targets unavailable, so only generate one of the two outputs and hope the other
  one is close enough

The first fallback preserves the logical event. The second one changes the meaning of the
build.

Whenever you add a fallback, ask:

> does this fallback preserve the same correctness contract, or does it silently lower the
> standard?

That question is more important than whether the fallback feels convenient.

## A tiny contract file

A practical contract file might look like this:

```make
ifeq ($(origin MAKE_VERSION),undefined)
$(error GNU Make is required)
endif

MIN_GNU_MAKE_OK := $(if $(filter 4.3% 4.4% 4.5% 5.%,$(MAKE_VERSION)),yes,)
ifeq ($(MIN_GNU_MAKE_OK),)
$(error GNU Make 4.3 or newer required; found $(MAKE_VERSION))
endif

SHELL := /bin/sh
.SHELLFLAGS := -eu -c

PYTHON ?= python3
HAVE_GROUPED_TARGETS := $(if $(filter 4.3% 4.4% 4.5% 5.%,$(MAKE_VERSION)),yes,)
```

This is not the only good shape, but it demonstrates the habit:

- declare the boundary
- name the capability
- make the shell contract explicit
- keep the conditions visible near the top of the build

## Failure signatures worth recognizing

### "It works locally, but CI says the syntax is invalid"

That often means the local Make or shell supports a feature the contract never declared.

### "The fallback path worked, but outputs changed subtly"

That means the fallback was not actually safe. It preserved execution, not semantics.

### "Nobody knows which tool was used on that machine"

That usually means tool discovery is happening implicitly or in too many places.

### "We support everything" but the build has machine-specific branches everywhere

That is not broad support. It is an undocumented compatibility maze.

## A good review question

When someone claims the build is portable, ask them to write a four-line summary:

1. required Make version
2. required shell behavior
3. required tools
4. optional features and fallbacks

If they cannot do that, the portability boundary is not clear enough yet.

## What to practice from this page

Take one real build in the repository and write its portability contract in plain
language:

1. which Make is required
2. which shell semantics are assumed
3. which tools are mandatory
4. which features are optional
5. which fallback preserves correctness when the optional feature is missing

If you can do that in one short section, the build has started to become explainable.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why portability needs a declared boundary instead of optimistic language
- why required, optional, and unsupported are different categories
- why version gates should be tied to capabilities
- why the shell belongs in the contract
- why a fallback is only good if it preserves correctness rather than merely keeping the build alive
