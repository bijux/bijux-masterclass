# Variable Precedence and Expansion

Many Make variable bugs sound like shell bugs at first:

- "Why did `CFLAGS` change in CI?"
- "Why is this list duplicated now?"
- "Why did the sub-make ignore the value I just set?"
- "Why does the exact same line expand differently later?"

Those are not random surprises. They come from three separate semantic questions:

1. where did the value come from
2. when does the value get computed
3. who is allowed to see it

This page keeps those questions separate so that variable behavior becomes explainable
instead of mystical.

## The sentence to keep

When a variable surprises you, do not ask only "what is its value?"

Ask all three:

> what is the origin, what is the flavor, and when is the value observed?

That one sentence will save you a lot of time.

## Origin answers "who won?"

The `origin` function tells you where Make believes a variable came from:

```make
$(origin CFLAGS)
```

In real investigations, the practical precedence ladder is usually:

1. command-line assignment such as `make CFLAGS=-O0`
2. `override` inside the makefile
3. regular makefile assignment
4. environment assignment
5. built-in default

There is one important exception: `-e` lets the environment outrank ordinary makefile
assignments. That is why `-e` belongs in the "be suspicious" bucket. It changes the
precedence rules you are trying to reason about.

## Flavor answers "how is this stored?"

The `flavor` function tells you whether a variable is recursive or simple:

```make
$(flavor CFLAGS)
```

For day-to-day engineering, the distinction that matters most is this:

- `:=` stores the expanded result immediately
- `=` stores the expression and expands it later

That means `:=` is stable by default, while `=` stays connected to whatever the referenced
variables become later.

## Why `:=` is the healthy default

Suppose you write this:

```make
ROOT := $(CURDIR)
SRC_DIR := $(ROOT)/src
SRCS := $(wildcard $(SRC_DIR)/*.c)
```

That is easy to reason about because each variable is computed once and then held steady.

Now compare it with this:

```make
ROOT = $(CURDIR)
SRC_DIR = $(ROOT)/src
SRCS = $(wildcard $(SRC_DIR)/*.c)
```

That version is not automatically wrong. It is simply more dynamic. Every later expansion
can observe a different world if one of the referenced values changes.

If you do not need that dynamism, you are paying for complexity without getting value.

## The operators you keep meeting

| Operator | Meaning | Healthy use | Common failure |
| --- | --- | --- | --- |
| `:=` | immediate assignment | fixed paths, sorted source lists, computed defaults | rarely the problem |
| `=` | deferred assignment | true laziness, advanced indirection | value changes later in ways nobody expected |
| `?=` | assign only if unset | configurable defaults | you forget something already set the variable |
| `+=` | append | extending a stable list | duplicates or recursive growth when combined with `=` |
| `!=` | shell assignment | rare integration edge cases | hidden inputs and parse-time side effects |

You do not need to ban the last three. You do need to stop treating them as harmless.

## A tiny proof harness

Use this Makefile:

```make
CFLAGS := FILE
OPTFLAGS = $(CFLAGS) -Wall

.PHONY: show show-env show-cli show-expand

show:
	@printf 'origin=%s flavor=%s value=%s\n' \
	  '$(origin CFLAGS)' '$(flavor CFLAGS)' '$(value CFLAGS)'

show-env:
	@$(MAKE) --no-print-directory -e show

show-cli:
	@$(MAKE) --no-print-directory CFLAGS=CLI show

show-expand:
	@printf 'OPTFLAGS flavor=%s value=%s expanded=%s\n' \
	  '$(flavor OPTFLAGS)' '$(value OPTFLAGS)' '$(OPTFLAGS)'
```

Now run:

```sh
export CFLAGS=ENV
make show
make show-env
make show-cli
make show-expand
```

What to notice:

- plain `make show` should report `CFLAGS` from the file
- `make show-env` should let the environment win because of `-e`
- `make show-cli` should make the command line win
- `show-expand` reveals that `OPTFLAGS` is recursive and expands later

This is the simplest reliable way to teach precedence without hand-waving.

## The duplication trap

One of the most common beginner mistakes is mixing recursive variables with appends and
expecting the result to stay small.

For example:

```make
CFLAGS = -Wall
CFLAGS += $(EXTRA_WARNINGS)
EXTRA_WARNINGS = -Wextra
```

That may still work, but it is harder to reason about than it needs to be because the
final value depends on later expansion.

A calmer version is:

```make
CFLAGS := -Wall
EXTRA_WARNINGS := -Wextra
CFLAGS += $(EXTRA_WARNINGS)
```

Now the values are concrete and stable.

## Target-specific variables are about scope, not magic

Make also lets you write target-specific variables:

```make
debug: CFLAGS += -O0 -g
debug: app
```

This is useful, but it often gets misread. A target-specific variable means "when Make is
building this target and its prerequisites, use this value in that scope."

It does not automatically mean:

- export this to every shell process forever
- propagate it to unrelated targets
- make every recursive `$(MAKE)` invocation inherit it as environment state

That last point matters. A target-specific variable changes Make's internal evaluation
scope. It is not a universal replacement for `export`.

## Export means "make this part of the environment"

If a sub-process or sub-make truly depends on a variable, you have to decide whether to
export it:

```make
export LC_ALL := C
```

Use export with discipline because environment state can become a hidden build input. If a
variable changes outputs, then either:

- pin it as part of the build contract
- surface it in a manifest or stamp
- or stop pretending the build is reproducible across environments

The wrong lesson is "never export." The right lesson is "know when export changes the
artifact meaning."

## A small sub-make example

Parent Makefile:

```make
SUBDIR := child

.PHONY: child plain exported

plain:
	@$(MAKE) --no-print-directory -C $(SUBDIR) show

exported: export MODE := release
exported:
	@$(MAKE) --no-print-directory -C $(SUBDIR) show
```

Child Makefile:

```make
.PHONY: show

show:
	@printf 'MODE origin=%s value=%s\n' '$(origin MODE)' '$(MODE)'
```

This makes the difference between unexported Make state and exported environment state
visible immediately.

## Failure signatures worth recognizing

### "The value is different in CI"

Usually one of these is true:

- the environment is winning because of `-e`
- a CI environment variable is overriding a default
- a recursive variable is expanding against a different later state

### "The flags keep growing"

That often means recursive assignment plus repeated `+=` or self-reference.

### "The child Makefile ignored my setting"

That usually means you changed Make scope but never exported the value the child process
actually depends on.

### "I changed the variable, but the recipe still uses the old value"

That points you back to expansion timing. The recipe or a simply-expanded variable may
have captured the value earlier than you thought.

## A review habit that pays off

When you inspect a variable-related bug, collect these three lines first:

```make
$(info origin=$(origin VAR))
$(info flavor=$(flavor VAR))
$(info raw=$(value VAR))
```

Those lines tell you more than a vague dump of the final expanded text because they keep
origin, flavor, and raw expression separate.

## What to practice from this page

Take one real build variable from the capstone or your own repository and answer:

1. Where should its default live: environment, makefile, or command line?
2. Should it be simple (`:=`) or recursive (`=`)?
3. Does it affect outputs enough that exporting it changes reproducibility?
4. How would you prove the answer with `origin`, `flavor`, and `value`?

If you can answer those clearly, you are no longer guessing about variables.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why `origin` and `flavor` answer different questions
- why `:=` is usually the calmer default
- how `-e` changes precedence and why that matters
- why target-specific variables are not the same thing as exported environment state
- why `value` is often more useful than printing only the final expanded text
