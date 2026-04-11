# Architecture Review and Maintenance Discipline

Most build architectures do not fail in one dramatic moment. They drift.

A new helper target appears.
A macro grows one more parameter.
An include layer starts mutating a variable it was never meant to own.
CI quietly begins calling a private target because it was convenient once.

Six months later the repository still builds, but nobody can explain why the structure is
the way it is.

This page is about preventing that drift from becoming the normal state of the build.

## The sentence to keep

When reviewing a build architecture, ask:

> if this design keeps evolving under ordinary team pressure, what will become ambiguous or
> unsafe first?

That question makes reviews much sharper than "does it work today?"

## Build architecture needs maintenance discipline

Teams often review code architecture more seriously than build architecture.

That is a mistake because build systems accumulate the same kinds of debt:

- unclear interfaces
- hidden mutation
- poorly bounded reuse
- fragile naming
- accidental contracts

If you do not review those explicitly, the build may remain operational while becoming
harder and harder to change safely.

## A stable review rubric helps

One useful review rubric is:

1. public API clarity
2. layer responsibility clarity
3. reuse opacity risk
4. naming and discovery stability
5. override and mutation safety

This rubric matters because it keeps the review focused on architecture instead of on
whoever most recently touched the Makefile.

## Review question 1: is the public surface obvious

Ask:

- which targets are public
- where they are documented
- whether CI and scripts call only those targets
- whether any internal helper has leaked into the public contract

If the answers are fuzzy, refactoring the build will remain more dangerous than it needs to
be.

This is often the fastest architecture improvement available.

## Review question 2: does each layer have one explainable job

For each included file, ask:

- what it owns
- what it may define or mutate
- what later files may assume about it

If a file cannot be described in one sentence, it probably owns too much or too little.

Layer review is not about whether the filenames look neat. It is about whether the
responsibility boundaries stay legible.

## Review question 3: is reuse protecting invariants or hiding behavior

Macros should be reviewed the same way functions are reviewed in code:

- what rule or invariant do they encode
- how hard is it to understand one call site
- can the final expanded graph still be audited

A macro that saves twenty lines but makes one target impossible to explain is usually a bad
trade.

This is why reuse belongs in architectural review, not only in code-style discussion.

## Review question 4: will naming still work after growth

Architecture should be reviewed against likely future pressure:

- another subsystem
- more generated outputs
- another package variant
- another test surface

If the current naming scheme will collide or confuse ownership as soon as the repository
grows, the architecture already has a visible weakness.

This is much cheaper to address early than after scripts and conventions have grown around
the ambiguity.

## Review question 5: are overrides and mutations safe

Builds often become risky because changes can occur from too many places:

- a later include appends to a core list
- a local optional file changes semantic flags
- a macro changes global state as a side effect

The review question is not "can variables be overridden?" Of course they can. The real
question is:

> do we know which overrides are legitimate architecture points and which ones are silent
> mutation hazards?

That distinction is crucial.

## A small review worksheet

Take a layered build and write down:

| Review area | Question | What a strong answer sounds like |
| --- | --- | --- |
| API | which targets are public | "all, test, selftest, clean, release-check" |
| layering | what `mk/objects.mk` owns | "rooted discovery and object mapping" |
| macros | why a publication macro exists | "it enforces temporary-write then move" |
| naming | how component outputs stay distinct | "`build/app/*` and `build/lib/*` namespaces" |
| overrides | which local file may change policy | "`mk/local.mk` may override convenience-only settings, not artifact semantics" |

This kind of worksheet helps because it turns architectural intuition into reviewable text.

## Maintenance discipline is mostly about saying no early

A lot of architecture rot could be prevented by rejecting small, plausible shortcuts:

- "just expose this helper target for CI"
- "just append to this list from another include"
- "just add one more macro argument"
- "just let this local override change the release flags"

Each one may be understandable in isolation. Together they slowly dissolve the structure.

Good maintenance discipline is often the ability to say:

> if we do that, we should first clarify the contract or boundary it would be changing.

That is not bureaucracy. It is how stable architecture survives normal team pressure.

## Architecture review should happen before bugs force it

Many teams wait until:

- a refactor breaks CI
- a release target means two different things
- a new contributor adds files in the wrong place
- a macro bug becomes impossible to localize

Then they say "we need an architecture review."

The healthier move is to review the architecture while it is still calm, because the
questions are easier to answer before the system is already under stress.

## Failure signatures worth recognizing

### "Nobody wants to touch the build architecture"

That often means the structure has become brittle or socially opaque.

### "We only find architecture problems after release or CI breakage"

That usually means the review loop is too reactive.

### "The build still works, but every explanation starts with history lessons"

That is a strong sign the architecture has become folklore-driven.

### "One engineer understands the macros, another understands the release targets, and no one understands the whole system"

That is an architectural ownership smell, not just a staffing issue.

## A practical maintenance cadence

For a serious Make-based system, it is reasonable to review architecture when:

- a new public target is proposed
- a new layer is added
- a macro starts generating a new family of rules
- a subsystem grows enough to change discovery or naming policy
- CI begins calling a different target than humans do

This keeps the review connected to real pressure points instead of making it a ceremonial
exercise.

## What to practice from this page

Choose one Make architecture and perform a short review:

1. list the public targets
2. name the include layers and their responsibilities
3. point to one macro and judge whether it improves or harms clarity
4. identify one likely future naming or discovery risk
5. identify one override or mutation point that deserves tighter control

If you can do that concisely and concretely, you are reviewing architecture instead of only
observing it.

## End-of-page checkpoint

Before leaving this lesson, make sure you can explain:

- why build architecture needs periodic review even when the build still works
- what a stable architecture review rubric includes
- how to spot hidden mutation and accidental contract growth
- why future growth pressure belongs in current architecture review
- how maintenance discipline often means refusing ambiguous shortcuts before they become normal
