# Exercise Answers

Use this after you have written your own answers. The point is comparison, not copying.

Strong Module 07 answers do not just propose a prettier file layout. They explain:

- what interface or responsibility boundary is being protected
- what evidence made the problem visible
- why the refactor would make the build easier to evolve or review

## Exercise 1: Define a public target surface

A strong answer keeps the public surface small and stable. It usually includes targets such
as:

- `all`
- `test`
- `selftest`
- `clean`
- `help`

The strongest answers also explain what each name promises. For example:

> `selftest` is for build-system invariants, not ordinary product tests.

A good demotion candidate is often a helper such as `build-objects` or `verify-contract`
when that target exists only to support internal orchestration rather than to serve users or
CI directly.

## Exercise 2: Split one Makefile into layers

A strong answer usually separates at least:

- shared policy and tools
- discovery and mapping
- core graph targets
- optional release or local overrides

For example:

```make
include mk/common.mk
include mk/objects.mk
include mk/targets.mk
-include mk/local.mk
```

The important part is not the filenames themselves. The important part is that the learner
can say what each layer owns and why that ownership makes later mutation easier to review.

## Exercise 3: Decide whether a macro is justified

A strong answer says a macro is justified when it protects one repeated invariant, such as
atomic publication or a repeated compile shape, and remains easy to audit with `make -p`.

A strong reason to keep explicit rules instead is:

> the repeated rules are still few, and the macro would make the call sites less readable
> than the duplication it replaces.

That is a very healthy answer. Module 07 does not reward abstraction for its own sake.

## Exercise 4: Prepare the repository for growth

A strong answer redesigns both discovery and output naming.

For example:

```make
APP_SRCS := $(sort $(wildcard src/app/*.c))
LIB_SRCS := $(sort $(wildcard src/lib/*.c))

APP_OBJS := $(patsubst src/app/%.c,build/app/%.o,$(APP_SRCS))
LIB_OBJS := $(patsubst src/lib/%.c,build/lib/%.o,$(LIB_SRCS))
```

This is strong because it prevents the future ambiguity that a flat `src/*.c` plus
`build/%.o` model would create once more than one subsystem exists.

## Exercise 5: Review a build architecture before it rots

A strong answer names concrete risks, such as:

- public API risk: CI relies on an undocumented helper target
- layer-boundary risk: `mk/release.mk` mutates core compile flags
- reuse risk: one macro owns too much behavior to review comfortably
- naming risk: output paths will collide when a new component lands

The strongest answers also recommend one preventive change now rather than waiting for a
later breakage.

## What mastery-level answers sound like

A mastery-level answer set in this module does three things well:

- it treats the Makefile as an interface, not just a script
- it treats include files as responsibility boundaries, not just text fragments
- it treats reuse and naming decisions as architecture choices with long-term costs

That is the standard Module 07 is trying to build.
