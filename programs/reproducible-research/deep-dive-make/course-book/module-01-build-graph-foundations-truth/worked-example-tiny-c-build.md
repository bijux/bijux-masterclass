# Worked Example: Tiny C Build

This file ties the five core lessons together in one small project.

## Project layout

```text
project/
  Makefile
  include/
    util.h
  src/
    main.c
    util.c
```

Use this example because it is just large enough to expose the real issues:

- object files depend on both source files and headers
- compiler flags can become hidden inputs
- the link step publishes a real artifact
- a broken compile can leave poison behind if publication is careless

## Minimal source files

`include/util.h`

```c
#pragma once
int util_add(int a, int b);
```

`src/util.c`

```c
#include "util.h"

int util_add(int a, int b) {
    return a + b;
}
```

`src/main.c`

```c
#include <stdio.h>
#include "util.h"

int main(void) {
    printf("%d\n", util_add(2, 3));
    return 0;
}
```

## What you should inspect while reading

Start with three questions:

1. what are the real file targets?
2. which inputs change object meaning?
3. what proves the build has converged?

As you work through the rest of the module, keep returning here and answer those
questions again with better precision.

## Evidence loop

Run these commands in `project/`:

```sh
make -n all
make --trace all
make -p
make clean && make all
make -q all; echo $?
```

This file is not the whole lesson. It is the place where the lessons meet one build you
can reason about line by line.
