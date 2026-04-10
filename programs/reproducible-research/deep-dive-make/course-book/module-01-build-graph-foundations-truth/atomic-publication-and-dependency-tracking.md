# Atomic Publication and Dependency Tracking

Even a truthful graph can be damaged by bad publication hygiene.

This page covers the final piece of Module 01:

> a target should appear only when it is complete, and its dependency edges should be real
> enough that incremental rebuilds keep telling the truth.

## Why publication hygiene matters

Imagine a compile rule that writes directly to `build/main.o` and fails halfway through.
You now have a file at the target path, but it may be incomplete or stale. On the next
run, Make sees a file and may treat it as evidence.

That is how a build becomes poisoned.

## The safe publication pattern

Write to a temporary file first, then rename it into place only after the command
succeeds.

```make
app: $(OBJS)
	tmp=$@.tmp; \
	$(CC) $^ -o $$tmp && mv -f $$tmp $@ || { rm -f $$tmp; exit 1; }
```

This gives you a strong property:

- before success, the final path is untouched
- after success, the final path is fully published

That property becomes more important, not less, as the build grows.

## `.DELETE_ON_ERROR`

Add this near the top of serious Makefiles:

```make
.DELETE_ON_ERROR:
```

It tells Make not to keep a target that failed while being built. It is not enough by
itself, but it is a good baseline.

## Header dependencies are real dependencies

In C builds, source files are not the whole story. Headers change object meaning too.

If your rule says only this:

```make
build/%.o: src/%.c
```

then a header edit may not trigger the rebuild you need.

That is why depfiles matter. They let the compiler publish the discovered header edges
into `.d` files, which Make can include on the next run.

## The core depfile shape

```make
DEPFLAGS := -MMD -MP
DEPS := $(OBJS:.o=.d)

$(BLD_DIR)/%.o: $(SRC_DIR)/%.c | $(BLD_DIR)/
	tmp=$@.tmp; dtmp=$(@:.o=.d).tmp; \
	$(CC) $(CPPFLAGS) $(CFLAGS) $(DEPFLAGS) -MF $$dtmp -MT $@ -c $< -o $$tmp && \
	mv -f $$tmp $@ && mv -f $$dtmp $(@:.o=.d)

-include $(DEPS)
```

The details matter less than the intent:

- headers become explicit evidence for future rebuilds
- the `.o` and `.d` files are published together
- a failed compile does not leave a half-truth behind

## What to prove on this page

Two checks matter:

1. force a failure and confirm the final target is absent or unchanged
2. touch a header and confirm the right object rebuilds

If you can do both, your build is starting to earn trust.
