# Exercise Answers

Use this file after you have written your own answers. The value is in comparing your
reasoning, not in copying the wording here.

## Exercise 1: Draw the graph

The important answer is that `app`, `build/main.o`, and `build/util.o` are real artifact
targets, while `all` is a convenience target. `include/util.h` is a prerequisite for both
object files because changing the header changes the meaning of both objects.

## Exercise 2: Find a hidden input

`CFLAGS` is a hidden input because it changes the compiler invocation without changing any
file in the prerequisite list. The repair is to turn the semantic value of the flags into
evidence the graph can depend on, such as a stable stamp or manifest.

## Exercise 3: Review rule ownership

An explicit rule keeps ownership obvious because the target path is named directly. A
pattern rule is still correct when the mapping is clear, for example `build/%.o:
src/%.c`. The danger starts when multiple rules can publish the same path or when a
multi-output generator is treated as if each file were independent.

## Exercise 4: Explain evaluation timing

`:=` computes the value when Make reads the file. `=` stores the expansion for later.
For discovered source lists, `:=` is usually the safer Module 01 default because it gives
you one stable value for the whole invocation.

## Exercise 5: Prove safe publication

A safe answer writes to `$@.tmp` first and renames only on success. The proof statement is
that a failed recipe leaves either no final target or the previously known-good target,
but never a half-written new target.
