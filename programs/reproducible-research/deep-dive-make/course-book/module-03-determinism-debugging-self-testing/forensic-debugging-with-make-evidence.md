# Forensic Debugging with Make Evidence

Make debugging gets calmer when you stop asking the build system to reveal its soul and
start asking it for concrete evidence.

## The debugging ladder

Use these in order:

1. `make -n <target>`
2. `make --trace <target>`
3. `make -p`
4. only then add temporary probes such as `$(info ...)` or `$(warning ...)`

That order matters because it keeps the explanation grounded in the evaluated graph.

## What each command is for

- `-n` answers what would run
- `--trace` answers why Make thinks it must run
- `-p` answers what rules and variables Make actually evaluated

The most important one is usually `--trace`. If you cannot quote the line that forced the
rebuild, you usually have not located the cause yet.

## What this lesson is protecting you from

Common bad debugging habits include:

- saying "it rebuilt for no reason"
- editing recipes before confirming the triggering edge
- assuming a variable has one value because the source file "looks like" it should

This lesson trains you to use the build’s own evidence first.
