# Exercises
Use these after reading the five core lessons and the worked example. The goal is not to
show off syntax. The goal is to make your semantic reasoning visible.

## How to work this exercise set

These exercises are easiest when you treat them as incident practice rather than as a
syntax test.

Work in this order:

- Exercises 1-3: choose evidence and explain variable or include behavior
- Exercises 4-6: make precedence and capability choices visible
- Exercises 7-9: reproduce, observe, and repair advanced rule behavior
- Exercise 10: combine several semantic failures in one calm investigation

Each exercise asks for three things:

- the build fact you are trying to prove
- the evidence you would use to prove it
- the repair or design decision you would make after reading that evidence

Also label the semantic stage where the problem lives: read time, expansion, rule
selection, or recipe execution. If more than one stage contributes, show the causal
order rather than calling the whole build “complex.”

## Minimum evidence for every answer

Try to include:

- one exact command
- one exact semantic stage
- one repair that becomes obvious once that stage is named

## Exercise 1: Choose the right CLI probe

Suppose you say:

> "`app` rebuilt, and I do not know whether the reason was a stale input, a phony target,
> or a generated include."

Explain which Make command you would run first, which one you would run second, and what
you expect each to tell you.

What to hand in:

- the first command
- the second command
- one sentence explaining why those two commands come before `clean`, `-B`, or `-j1`

## Exercise 2: Prove where a variable value came from

You inherit a Makefile where `MODE`, `CFLAGS`, and `LDFLAGS` can all be influenced by the
environment, the command line, and the file itself. A teammate says:

> "CI is using different optimization flags, but the Makefile looks the same."

Describe how you would prove the winning origin and flavor of `CFLAGS`, and explain one
repair that would make the variable behavior easier to reason about.

What to hand in:

- the introspection lines or target you would add
- the exact facts you want to capture about `CFLAGS`
- one repair using clearer precedence or expansion rules

## Exercise 3: Repair a generated-include loop

A build generates `mk/generated-config.mk`, includes it, and rewrites it on every run with
a fresh timestamp. You report that the build never seems to settle.

Explain why that happens and redesign the rule so the included file converges.

What to hand in:

- a plain-language explanation of the restart problem
- the repaired rule shape
- one sentence explaining why atomic publication matters here

## Exercise 4: Replace a platform branch with a capability gate

You find this in a repository:

```make
ifeq ($(shell uname),Darwin)
  ARCHIVE := gtar
else
  ARCHIVE := tar
endif
```

Rewrite the idea as a capability gate instead of a platform guess. You do not need to use
this exact tool example if another capability makes the lesson clearer.

What to hand in:

- the named capability you would compute
- the single place you would compute it
- one sentence explaining why the new branch is easier to audit

## Exercise 5: Repair a multi-output generator honestly

One generator produces both `api.h` and `api.json`, but the Makefile currently uses a
naive multi-target rule and occasionally runs the generator twice under `-j`.

Describe two valid repairs and explain when you would choose each one.

What to hand in:

- a grouped-target repair
- a stamp-based repair
- one sentence on the capability or portability tradeoff between them

## Exercise 6: Compare assignment flavors

Create variables with `=`, `:=`, `?=`, and `+=`. Change a referenced variable between
assignments and print:

```make
$(origin NAME)
$(flavor NAME)
$(value NAME)
$(NAME)
```

Predict every line before running Make.

What to hand in:

- the Makefile and prediction
- the observed output
- one practical use and one risk for recursive expansion

## Exercise 7: Build a precedence matrix

Define `MODE ?= release` and print its origin. Invoke the target with:

1. no override
2. `MODE=debug make show`
3. `make MODE=debug show`
4. `MODE=debug make -e show`
5. `override MODE := hardened` in the Makefile

What to hand in:

- a table of value and origin for every invocation
- a recommended project contract for configuring `MODE`
- one reason to avoid routine use of `-e`

## Exercise 8: Observe a generated include restart

Generate `build/config.mk` from `config.txt`, include it, and print `$(MAKE_RESTARTS)`.
Publish the include only when its content changes.

Then deliberately add a timestamp so it changes every run and observe the behavior.

What to hand in:

- the stable and unstable generator rules
- restart counts or trace evidence
- the repair that restores convergence

## Exercise 9: Remove pattern-rule ambiguity

Create two pattern rules that could both produce `build/sample.o`. Use `make -d` or
`make -p` to determine which rule Make selects.

Replace the ambiguity with an explicit path boundary, a static pattern rule, or one
unambiguous pattern.

What to hand in:

- the competing rules
- the evidence showing rule selection
- the repaired rule and why a future maintainer can predict it

## Exercise 10: Diagnose a compound semantic incident

Construct or select a build with at least three symptoms:

- a surprising variable value
- a generated include that changes the graph
- a rule selected differently than expected

Investigate without beginning with `clean`, `-B`, or `.NOTPARALLEL`.

What to hand in:

- a short symptom list
- the evidence command chosen for each symptom
- the semantic cause and repair for each
- a final `make -q` or equivalent convergence result

## Before you read the answers

Do not open `exercise-answers.md` until you can already point to:

- one variable whose origin you proved
- one restart behavior you can explain
- one ambiguous rule you made predictable
- one incident where naming the semantic stage reduced the debugging scope

## Mastery standard for this exercise set

Across all ten answers, the module wants the same habit:

- you name the semantic rule involved
- you choose evidence before you choose a repair
- you explain the repair in terms of truth, convergence, precedence, or ownership

If an answer says only "Make is tricky," keep going.
