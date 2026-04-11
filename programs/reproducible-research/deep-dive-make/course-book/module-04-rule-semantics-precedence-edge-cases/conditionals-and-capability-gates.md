# Conditionals and Capability Gates

Conditionals in Make are easy to write and surprisingly hard to keep honest.

At first they look harmless:

- one `ifeq` for Linux
- one `ifneq` for macOS
- one `$(shell which tool)` to see what exists
- one more branch for a special CI runner

Six months later the build "works" mostly by coincidence, and nobody can say which
conditions actually control correctness.

This page teaches a healthier pattern:

> detect one capability once, give it a stable name, and reuse that name everywhere.

That sounds simple because it is. The difficulty is resisting the urge to keep adding
small local branches instead.

## The real problem conditionals are solving

Good build conditionals answer questions such as:

- do we have a tool with the feature we need
- does this version of Make support a rule form we want to use
- is an optional subsystem intentionally enabled

Bad build conditionals answer questions such as:

- what machine did I happen to test on
- which random shell command can I scatter here to guess the platform
- how can I quietly change behavior instead of failing clearly

The difference is that the first group defines capabilities. The second group produces
folklore.

## Capability thinking beats platform thinking

Suppose you want grouped targets `&:` for a generator rule. The question you need answered
is not "am I on Linux?" The question is:

> does this Make support grouped targets?

That is a capability question.

The healthy pattern looks like this:

```make
HAVE_GROUPED_TARGETS := $(filter 4.3% 4.4% 4.5% 5.%,$(MAKE_VERSION))
```

Now you can branch on one named idea instead of encoding a pile of operating-system
assumptions that only indirectly relate to the feature you need.

## Centralize the decision

One capability check should live in one place.

For example:

```make
# mk/capabilities.mk
HAVE_GROUPED_TARGETS := $(filter 4.3% 4.4% 4.5% 5.%,$(MAKE_VERSION))
HAVE_POSIX_SHELL := yes
HAVE_PYTHON3 := $(if $(shell command -v python3 >/dev/null 2>&1 && printf yes),yes,)
```

Then other files use those names:

```make
include mk/capabilities.mk

ifeq ($(HAVE_GROUPED_TARGETS),yes)
  # grouped-target implementation
else
  # stamp-based fallback
endif
```

The point is not only readability. It is auditability. When the question "why did this
branch execute?" comes up, there is one place to inspect.

## Why scattered `$(shell ...)` calls rot quickly

Scattered shell probes create three problems at once:

1. they duplicate logic
2. they create hidden inputs from the machine environment
3. they become hard to test because the condition is not named

For example, this shape is brittle:

```make
ifeq ($(shell uname),Darwin)
  TAR := gtar
else
  TAR := tar
endif
```

It looks compact, but it hides the real question. Are you choosing a tool based on an
operating system label, or based on a capability such as support for a required flag?

If the real need is a capability, detect the capability.

## Fail fast when the capability is required

One of the worst build experiences is a soft fallback that quietly changes correctness.

For example:

- skipping a rule feature and generating only one of two outputs
- dropping a validation step because a tool is missing
- changing line-ending behavior or archive options without telling the user

If the build really requires a capability, say so early:

```make
ifeq ($(HAVE_PYTHON3),)
$(error python3 is required to generate the API manifest)
endif
```

This is kinder to you than letting the build wander into a broken state later.

## A small example with Make version gates

Use this scratch Makefile:

```make
HAVE_GROUPED_TARGETS := $(if $(filter 4.3% 4.4% 4.5% 5.%,$(MAKE_VERSION)),yes,)

ifeq ($(HAVE_GROUPED_TARGETS),yes)
MODE := grouped
else
MODE := fallback
endif

.PHONY: show
show:
	@printf 'MAKE_VERSION=%s\n' '$(MAKE_VERSION)'
	@printf 'HAVE_GROUPED_TARGETS=%s\n' '$(HAVE_GROUPED_TARGETS)'
	@printf 'MODE=%s\n' '$(MODE)'
```

Run:

```sh
make show
make -p | rg 'MAKE_VERSION|HAVE_GROUPED_TARGETS|MODE'
```

The important learning outcome is not the exact version filter. It is the idea that the
branch is driven by one named capability variable that can be inspected and discussed.

## Optional features need the same discipline

Conditionals are not only for platform or tool checks. They also define optional features
such as:

- enabling verbose logging
- turning on a local developer convenience target
- enabling a bounded `eval`-based rule generator for demos

Those still deserve one source of truth:

```make
ENABLE_VERBOSE_LOGS ?= no

ifeq ($(ENABLE_VERBOSE_LOGS),yes)
  LOG_FLAGS += --verbose
endif
```

This is much easier to teach and review than hidden conditionals inside several recipes.

## Conditionals can hide real inputs

A conditional becomes dangerous when it changes artifact meaning without leaving evidence.

Example:

```make
ifeq ($(shell hostname),ci-runner-01)
  CPPFLAGS += -DENABLE_EXPERIMENTAL_PATH
endif
```

That conditional changes outputs, but the input is not a repository file and is not named
as part of the build contract. This is the kind of thing that produces "works on one
runner only" incidents.

If an environmental fact changes outputs, you must either:

- pin it explicitly
- name it as a capability and attest it
- or stop claiming the outputs are reproducible across environments

## Include fragments are often better than giant nested branches

When conditional logic grows, split by concern instead of making one file into a maze.

For example:

```make
include mk/capabilities.mk
include mk/toolchain.mk
include mk/rules.mk
```

Then each file can use the same centralized capability variables.

This is cleaner than embedding a large operating-system matrix into every rule section.

## Failure signatures worth recognizing

### "The build changes across machines, but we did not change the repo"

That usually means a capability check is actually a hidden environmental input, or the
same capability is being computed differently in multiple places.

### "We have three different platform checks for the same tool"

That is duplicated policy. Collapse it into one named capability.

### "The fallback works, but the outputs are not really equivalent"

That is not a harmless fallback. That is a correctness fork that needs to be made
explicit.

### "I cannot tell why this branch was taken"

That means the condition is not inspectable enough. You should be able to print the
deciding variable and discuss it in plain language.

## A review question that improves conditionals fast

Take any conditional branch in your build and ask:

> Is this checking a capability, or is it checking an incidental property that only
> happens to correlate with the capability?

That question catches a lot of weak design.

## What to practice from this page

Choose one conditional in the capstone or your own build and rewrite it so that:

1. the capability is computed once
2. the capability has a stable name
3. the decision can be printed with `make -p`
4. the build fails early if a required capability is missing

If you can do that cleanly, your conditionals are becoming architecture instead of trivia.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why capability checks age better than platform-label checks
- why one capability decision should live in one place
- why scattered `$(shell ...)` probes create hidden inputs and duplicated policy
- why required capabilities should fail fast instead of drifting into soft fallback
- why conditionals that change outputs need the same modeling discipline as any other input
