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

## Why the order matters

It is common to jump straight to adding `echo` lines or rewriting a recipe. That tends to
mix symptoms with causes. The ladder above forces a cleaner sequence:

- inspect the intended work
- inspect the reason for the work
- inspect the evaluated world
- only then add temporary probes if something is still hidden

That keeps debugging factual instead of theatrical.

## What each command is for

- `-n` answers what would run
- `--trace` answers why Make thinks it must run
- `-p` answers what rules and variables Make actually evaluated

The most important one is usually `--trace`. If you cannot quote the line that forced the
rebuild, you usually have not located the cause yet.

## A small example of the right question

Wrong question:

- "Why is Make acting strangely?"

Better question:

- "Which prerequisite or target state made `build/main.o` out of date according to
  `--trace`?"

That sounds smaller, but it is much more actionable. The smaller question leads you back
to a specific edge or artifact instead of an opinion about the whole build.

## What `make -p` is for in this module

`make -p` is where you go when the source file and the evaluated build no longer seem to
match. It helps answer questions like:

- what did this variable expand to
- which rules actually exist after includes and conditionals
- whether the build used the value you think it used

That is especially important in Module 03 because hidden variability and optional
abstraction can move behavior away from what a quick read suggests.

## What this lesson is protecting you from

Common bad debugging habits include:

- saying "it rebuilt for no reason"
- editing recipes before confirming the triggering edge
- assuming a variable has one value because the source file "looks like" it should

This lesson trains you to use the build’s own evidence first.

## A good debugging sentence

Try to make yourself say the issue this way:

"`build/include/dynamic.h` rebuilt because `scripts/gen_dynamic_h.py` was newer than the
target according to `--trace`."

That is a debug statement. It names the target, the cause, and the evidence.

## End-of-page checkpoint

Before leaving this page, you should be able to explain:

- why `--trace` is usually the first real explanation tool
- when `make -p` becomes more useful than rereading the source
- why temporary probes come last, not first
- how to phrase a rebuild explanation as evidence instead of opinion
