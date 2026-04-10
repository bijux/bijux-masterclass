# Worked Example: Parallel-Safe Build

This file ties the module together around the `m02/` simulator.

## Layout

```text
m02/
  Makefile
  mk/
    common.mk
    objects.mk
    rules.mk
  include/
    util.h
    sub.h
  src/
    main.c
    util.c
    sub/sub.c
  repro/
    01-shared-log.mk
    02-temp-collision.mk
    03-stamp-clobber.mk
    04-generated-header.mk
    05-mkdir-race.mk
```

This example matters because it combines three things at once:

- a layered build you want to keep correct
- enough targets that parallel scheduling becomes visible
- several intentionally broken repro files that teach race diagnosis

## What to inspect first

Start with these questions:

1. which targets can become runnable together?
2. which outputs have one clear writer?
3. what would `selftest` need to prove before you trust `-j8`?

This worked example is the concrete home for the rest of the module.
