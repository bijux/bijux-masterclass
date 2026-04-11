# Includes, Remake Semantics, and Search Paths

Includes are where many Makefiles stop feeling like one file and start becoming a build
system.

That is a good thing. Layered include files make large builds readable. They let you keep
policy separate from rules, toolchain setup separate from public targets, and optional
developer overrides separate from shared behavior.

But includes also introduce one of Make's least-understood semantics:

> if Make remakes an included makefile, it restarts evaluation.

That is not Make being dramatic. That is Make being honest. If the input files that define
the build changed, the build logic has to be read again.

This page makes that behavior legible and then adds one more caution: search paths such as
`VPATH` can quietly hide where a dependency really came from.

## Why includes exist at all

Healthy include layering usually serves one or more of these goals:

- keep toolchain defaults in one place
- separate public targets from low-level rules
- let local developer overrides stay optional
- share a small rules library across related parts of the tree

The point is architectural clarity, not cleverness.

A simple layered shape might look like this:

```make
include mk/common.mk
include mk/contract.mk
include mk/rules.mk
-include mk/local.mk
```

Read that as:

- load shared defaults
- load the public contract
- load the rule definitions
- then, if present, load local private overrides

That is already much easier to review than one giant file with everything mixed together.

## `include` and `-include` are not interchangeable

There are two common include forms:

```make
include mk/rules.mk
-include mk/local.mk
```

The first says the file is required. If it is missing, the build definition is incomplete.

The second says the file is optional. If it is missing, keep going.

That distinction matters because optional files should only be optional when correctness
does not depend on them. A local reader-specific configuration file is a good candidate for
`-include`. A required public rules file is not.

## The restart model in plain language

If Make reads an included file and also knows how to build that file, it may decide the
included file is out of date. When that happens, Make does this:

1. build the included file
2. restart
3. read the makefiles again from the top

This makes sense once you say it out loud. If the build definition changed, continuing with
the old parsed state would be wrong.

The confusion starts when people forget that generated makefiles are still inputs to the
build system. They are not magic side files.

## A tiny generated-include example

Start with this Makefile:

```make
include generated.mk

generated.mk:
	@printf 'MESSAGE := hello\n' > $@

.PHONY: show clean

show:
	@printf 'MESSAGE=%s\n' '$(MESSAGE)'

clean:
	rm -f generated.mk
```

Now run:

```sh
make clean
make show
make show
```

What happens:

- first run: Make notices `generated.mk` is needed, builds it, restarts, then reads it
- second run: the file is already there, so the build settles immediately

That restart is healthy. It means the included file has become part of the evaluated world.

## How generated includes become a problem

Generated includes become dangerous when they are not deterministic.

For example, if the generator writes a timestamp every time:

```make
generated.mk:
	@printf 'BUILD_TIME := %s\n' "$$(date +%s)" > $@
```

Now the included file changes every run, so Make keeps finding a reason to restart or keep
the state unstable.

This is not an "include bug." It is a determinism bug in a file that happens to control
evaluation.

That is why generated includes need the same discipline as any other artifact:

- one clear writer
- deterministic content when semantics have not changed
- safe publication
- convergence tests

## `MAKEFILE_LIST` is your include stack

When you need to answer "where did this setting come from?", start with:

```make
$(info STACK=$(MAKEFILE_LIST))
```

`MAKEFILE_LIST` records the makefiles read so far. That makes it a simple but powerful
forensics tool:

- it shows include order
- it helps explain why one assignment overrode another
- it makes local override leaks easier to spot

If a local file is accidentally influencing CI, the include stack often shows it quickly.

## Include order is policy

Include order is not a formatting detail. It changes which assignment wins and which rule
definition is seen last.

For example:

```make
include mk/defaults.mk
-include mk/local.mk
```

This lets the local file override defaults.

If you reverse the order:

```make
-include mk/local.mk
include mk/defaults.mk
```

then the defaults overwrite the local settings.

Neither ordering is universally correct. The point is that the order is part of the build
policy and should be chosen on purpose.

## Search paths can hide truth

Make also offers file search features such as `VPATH` and `vpath`.

They sound convenient because they let Make find prerequisites in alternate directories.
They can also make dependency truth harder to see.

Example:

```make
VPATH := src generated

app.o: app.c config.h
	$(CC) -c $< -o $@
```

If `config.h` exists in more than one place, or if the search order changes, the build may
still "work" while you lose track of which file actually supplied the input.

That is why this course prefers explicit paths:

```make
build/app.o: src/app.c include/config.h
```

Explicit paths are easier to review, debug, and explain.

## When search paths are defensible

This page is not saying `VPATH` is forbidden forever. It is saying you should know the
cost.

Search paths are most defensible when:

- the search roots are small and well-defined
- the found files are easy to explain
- the project has tests or audits that prove the resolution is stable

If you cannot say where a prerequisite came from without running several experiments, the
search policy is too opaque.

## A small `VPATH` exercise

Create this layout:

```text
src/config.h
generated/config.h
Makefile
```

Then use:

```make
VPATH := generated src

.PHONY: show

show: config.h
	@printf 'resolved config.h from VPATH\n'
```

Now switch the order to `src generated` and watch how the resolution policy changes even
though the rule text stayed the same.

That is the teaching value of the example: search policy can change meaning without
changing the visible dependency line.

## Failure signatures worth recognizing

### "Make keeps re-reading the makefiles"

That often means an included file is being regenerated non-deterministically or the build
never converges on a stable version of it.

### "The local override worked for me, but CI ignored it"

That usually points to `-include` on a file that does not exist in CI, or to include order
that was assumed rather than reviewed.

### "The wrong prerequisite was used, but the rule looked right"

That often points to `VPATH` or `vpath` resolving the path from a different directory than
the reader expected.

### "A variable value changed after we split the build into more files"

That usually means include order changed which file's assignment wins.

## A durable review checklist

When you inspect include-related behavior, ask:

1. which files are required and which are optional
2. in what order are they read
3. can any included file be rebuilt during the run
4. if so, is that generated content deterministic
5. are any search-path features making prerequisite origins hard to explain

Those five questions catch most of the real issues.

## What to practice from this page

Take one included file in the capstone or your own repository and explain:

1. why it is included
2. whether it should be `include` or `-include`
3. whether Make could ever remake it
4. what would have to be true for that remake to stay safe
5. whether explicit prerequisite paths would be clearer than the current search policy

If you can answer those cleanly, include layering has become architecture rather than
ambient magic.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why Make restarts after remaking an included makefile
- why generated includes must be deterministic to converge
- why `MAKEFILE_LIST` is a practical forensic tool
- why include order changes semantics rather than merely style
- why `VPATH` can hide dependency truth even when the build succeeds
