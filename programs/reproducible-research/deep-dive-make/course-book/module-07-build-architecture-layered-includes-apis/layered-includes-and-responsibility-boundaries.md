# Layered Includes and Responsibility Boundaries

Once a Makefile grows past a certain size, splitting it into `mk/*.mk` files becomes
almost unavoidable.

The split itself is not the hard part. The hard part is avoiding a new kind of mess:

- one file defines tools, then another quietly mutates them
- one include adds source discovery, then a later one appends hidden overrides
- nobody knows whether a file is allowed to define policy, graph shape, or optional user
  surfaces

That is how "modularization" can actually make a build harder to understand.

This page is about a healthier alternative:

> each include layer should have one explainable job, and include order should reinforce
> that job instead of hiding mutation.

## The sentence to keep

When you split a build into layers, ask:

> what responsibility does this file own that the neighboring layers should not quietly
> override or duplicate?

That question is more useful than "should we have more files?"

## Why layers exist at all

Healthy layer splits usually solve one of these problems:

- top-level entrypoints are getting buried under low-level rule details
- tool and shell policy is mixed with graph construction
- source discovery and naming logic is scattered
- optional release or audit surfaces are obscuring the core build

If the split does not improve one of those, it is probably just moving text around.

## Layers are about responsibility, not file count

A common beginner move is to split one Makefile into many files simply because it feels
more professional.

That often creates a different problem:

- `common.mk`
- `helpers.mk`
- `shared.mk`
- `defaults.mk`
- `misc.mk`

All of which still mutate one another in unclear ways.

The issue is not whether there are many files. The issue is whether each file has a role a
reader can describe in one sentence.

## A healthy layering shape

One practical architecture looks like this:

```text
Makefile
mk/
  common.mk
  objects.mk
  targets.mk
  release.mk
```

With responsibilities such as:

- `Makefile`: public targets and top-level includes
- `common.mk`: tools, shell discipline, shared flags, common directories
- `objects.mk`: rooted discovery and object-path mapping
- `targets.mk`: real artifact rules and the core graph
- `release.mk`: optional packaging or publication surfaces

This is not the only valid split. It is a useful example because each file has a clear
center of gravity.

## Include order is part of the architecture

Include order is not a formatting choice. It affects:

- which variables win
- which rules exist when later files are parsed
- which optional layers are allowed to override earlier values

For example:

```make
include mk/common.mk
include mk/objects.mk
include mk/targets.mk
-include mk/local.mk
```

This tells a story:

- shared policy first
- graph-supporting discovery next
- real targets after the supporting data exists
- local overrides last, and optional

That is very different from a random include list.

## Hidden mutation is the real enemy

The most dangerous include-layer bug is not duplication. It is mutation that only becomes
visible if you inspect the final evaluated world very carefully.

For example:

```make
# mk/common.mk
CFLAGS := -Wall

# mk/release.mk
CFLAGS += -O3
```

This may be acceptable if `release.mk` clearly owns release-specific policy and that
override is intentional.

It becomes unhealthy when the mutation is surprising, spread across files, or applied in a
place that does not obviously own that decision.

This is why responsibility boundaries matter. They make mutation reviewable.

## Policy and graph shape should not blur together

One very useful discipline is to distinguish:

- policy
- graph shape

Policy examples:

- tool selection
- shell flags
- global warning flags
- feature toggles

Graph-shape examples:

- source discovery
- object path mapping
- final artifact rules
- stamp or manifest boundaries

When one file mixes both without a clear reason, the build gets harder to review because
changes to one concern are buried inside the other.

## Optional layers should stay obviously optional

Some build layers really are optional:

- local developer overrides
- extra release surfaces
- experimental audit routes

That usually means they should appear as optional in the include structure too:

```make
-include mk/local.mk
```

The important architectural point is that correctness should not depend on that file
silently existing.

If the build is broken without an optional layer, the layer is not actually optional.

## A small layering example

Top-level `Makefile`:

```make
include mk/common.mk
include mk/objects.mk
include mk/targets.mk

.PHONY: all test clean help
```

`mk/common.mk`:

```make
SHELL := /bin/sh
.SHELLFLAGS := -eu -c
CC ?= cc
BUILD_DIR := build
```

`mk/objects.mk`:

```make
SRCS := $(sort $(wildcard src/*.c))
OBJS := $(patsubst src/%.c,$(BUILD_DIR)/%.o,$(SRCS))
```

`mk/targets.mk`:

```make
app: $(OBJS)
	$(CC) $^ -o $@
```

This example is small, but it already shows a healthier flow:

- shared policy first
- deterministic discovery second
- graph assembly third

That order is easy to explain.

## What layers should not do casually

Be suspicious when an include file:

- redefines variables another layer was supposed to own
- appends to source lists from far away without making that ownership clear
- creates public targets from a low-level helper file
- relies on mysterious include order to "work"

These are the kinds of details that make maintainers say "do not touch the Makefiles unless
you already know the trick."

That is exactly the culture this module is trying to prevent.

## Why `make -p` matters here

Layered includes can feel understandable until you need to know the final evaluated state.

`make -p` is useful because it answers:

- what did the variable finally become
- which rule ended up in effect
- how did the include ordering resolve

You should not need `make -p` to understand ordinary intent. You should still use it to
confirm that the layered design matches the intended ownership model.

## Failure signatures worth recognizing

### "No one knows which file is allowed to change this variable"

That usually means responsibilities are not separated cleanly.

### "The build only works because this include comes before that one"

That may be true, but if the reason is unclear, the architecture is brittle.

### "A low-level file added a public target"

That often means the build API and the internal layers are bleeding into each other.

### "We split the Makefile, but edits are harder now"

That usually means the split improved file count, not responsibility clarity.

## A review question that improves layer design

Take any `mk/*.mk` file and ask:

1. what single responsibility does this file own
2. which earlier layers it depends on
3. which later layers may depend on it
4. what variables or rules it is allowed to define or mutate
5. whether a new engineer could tell that from the filename and surrounding include order

If those answers are weak, the layer is weak too.

## What to practice from this page

Take one medium-sized Makefile and sketch a layer split:

1. the top-level public API file
2. the policy layer
3. the discovery or graph-support layer
4. the core target layer
5. any optional layer that should stay separate

Then write one sentence for each layer explaining its responsibility.

If you can do that without overlap or hand-waving, you are much closer to a usable
architecture.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why layer count matters less than responsibility clarity
- why include order is part of the architecture
- how policy and graph shape differ
- why optional layers should stay visibly optional
- how to spot hidden mutation across include files
