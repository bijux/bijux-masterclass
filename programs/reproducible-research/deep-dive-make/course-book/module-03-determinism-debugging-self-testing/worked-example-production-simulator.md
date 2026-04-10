# Worked Example: Production Simulator

This file gathers the module into one teaching build.

## Layout

```text
project/
  Makefile
  mk/
    common.mk
    objects.mk
    stamps.mk
    macros.mk
    rules_eval.mk
  src/
    main.c
    dynamic/
      dyn1.c
      dyn2.c
  include/
    util.h
  scripts/
    gen_dynamic_h.py
  tests/
    run.sh
```

This simulator matters because it combines deterministic discovery, generation,
selftesting, and an optional `eval` surface in one place you can actually inspect.

## What to inspect first

Start with these questions:

1. which lists are rooted and sorted
2. which generated artifacts are published atomically
3. which hidden inputs are modeled
4. which targets form the public build contract

This worked example is the concrete home for the rest of the module.
