# Exercises

Use these after reading the five core lessons and the worked example. The goal is not to
show off syntax. The goal is to make your semantic reasoning visible.

Each exercise asks for three things:

- the build fact you are trying to prove
- the evidence you would use to prove it
- the repair or design decision you would make after reading that evidence

## Exercise 1: Choose the right CLI probe

A learner says:

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
a fresh timestamp. The learner reports that the build never seems to settle.

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

## Mastery standard for this exercise set

Across all five answers, the module wants the same habit:

- you name the semantic rule involved
- you choose evidence before you choose a repair
- you explain the repair in terms of truth, convergence, precedence, or ownership

If an answer says only "Make is tricky," keep going.
