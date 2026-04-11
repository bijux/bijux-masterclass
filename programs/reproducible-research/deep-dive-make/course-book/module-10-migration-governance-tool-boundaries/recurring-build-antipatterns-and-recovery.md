# Recurring Build Antipatterns and Recovery

This page collects the patterns that keep returning even after teams say they already know
better.

The goal is not to mock bad Makefiles. The goal is to recognize familiar damage early
enough to stop it from spreading.

## Why antipatterns matter this late in the course

By Module 10, the learner already knows a lot of individual facts:

- honest prerequisites matter
- parallel safety matters
- target meaning matters
- release boundaries matter
- observability matters

The problem in real repositories is not usually missing isolated facts. The problem is that
the same bad combinations keep reappearing under new names.

That is why this page is about patterns, not trivia.

## The sentence to keep

When you spot a suspicious build habit, ask:

> what repeated form of truth loss or ownership drift am I looking at, and what is the
> smallest honest recovery path?

That question turns vague discomfort into action.

## Antipattern 1: phony ordering instead of real edges

This is one of the oldest mistakes:

```make
.PHONY: prepare compile

all: prepare compile

prepare:
	@mkdir -p build

compile:
	@cc -o build/app src/main.c
```

This looks harmless. The deeper problem is that `compile` does not actually say what it
needs.

Symptoms:

- a target works only because a phony step happened first
- `-j` exposes missing directories or missing generated inputs
- downstream targets rely on ritual order instead of real prerequisites

Recovery:

- make directory creation an order-only prerequisite where appropriate
- make generated inputs first-class graph nodes
- remove phony sequencing once real edges exist

Phony targets are not evil. Using them to hide real data or publication dependencies is.

## Antipattern 2: multi-writer outputs hidden behind convenience

This appears in many forms:

- two targets both rewrite `build/app`
- a packaging target rebuilds product outputs
- a helper script refreshes generated files during unrelated commands

The team often describes this as "convenient" because it avoids repeating commands. What it
really does is erase output ownership.

Symptoms:

- outputs change when running unrelated targets
- incremental behavior becomes hard to trust
- release incidents are hard to reproduce

Recovery:

- assign one writer to each trusted output
- split generation from packaging or publishing
- make convenience targets compose truthful targets instead of rewriting artifacts

Single-writer discipline is not a style preference. It is a survival rule.

## Antipattern 3: recursive or opaque orchestration hiding the graph

Some inherited builds are not recursive in the strict GNU Make sense, but they still act
like it:

- shell scripts call `make` in several places
- one target delegates to directory-local mini systems without visible edges
- a wrapper script chooses routes dynamically based on host state

Symptoms:

- nobody can describe the real graph from the top level
- `--trace` helps less than expected because the interesting work happens elsewhere
- CI failures depend on where the wrapper script happened to branch

Recovery:

- keep the top-level contract small and explicit
- expose subsystem boundaries deliberately
- model shared outputs and inputs at the layer where they can be reviewed
- stop hiding major orchestration decisions in shell branching

The point is not "never call another tool." The point is "do not bury the ownership model."

## Antipattern 4: stamps and manifests with no clear meaning

Stamps and manifests can be excellent tools. They can also become places teams dump
uncertainty.

Warning signs:

- a stamp exists because "Make needed it somehow"
- the stamp is touched every run
- nobody can explain what semantic boundary it proves
- consumers depend on the stamp while the real output shape remains unclear

Example of a weak stamp:

```make
build/generated.stamp:
	@./scripts/codegen.sh
	@touch $@
```

What does the stamp mean here?

- that code generation ran
- that it succeeded
- that all outputs were validated
- that downstream consumers should trust every generated file

If the answer is "sort of all of those," the stamp is under-specified.

Recovery:

- define the boundary fact in one sentence
- make the stamp or manifest represent that one fact only
- keep consumers depending on real published outputs where direct edges are clearer

## Antipattern 5: release or install routes that do too much

This pattern survives because it often "works" during demos:

```make
release:
	@./scripts/build.sh
	@./scripts/test.sh
	@./scripts/package.sh
	@./scripts/install.sh
```

The issue is not that each sub-step exists. The issue is that the target meaning is too
broad to review.

Symptoms:

- one command mutates many different boundaries
- failures are described as generic "release issues"
- reruns are risky because side effects already happened

Recovery:

- separate validation, packaging, install, and deployment meanings
- keep publication boundaries inspectable
- make dangerous side effects opt-in and explicit

When a target means everything, it usually means nothing clearly.

## Antipattern 6: performance fixes that erase truth

This one shows up late, often after the team has already suffered:

- skipping checks because they are slow
- caching outputs without modeling the cache boundary
- reducing rebuilds by ignoring semantic inputs
- removing trace or audit routes to reduce noise

Symptoms:

- the build is faster but less explainable
- stale outputs become harder to detect
- incidents take longer because evidence disappeared

Recovery:

- measure where the real cost lives first
- remove waste, not obligations
- add bounded observability routes instead of deleting evidence surfaces
- keep truth-preserving comparisons during optimization work

Speed is valuable. Truth is more valuable.

## A small recovery rubric

When you detect an antipattern, classify the recovery path:

| Antipattern smell | First recovery move |
| --- | --- |
| ritual order dependence | expose real edge or order-only prerequisite |
| multi-writer output | assign one owner and remove hidden rewrites |
| opaque orchestration | surface the actual boundary and contract |
| meaningless stamp | define the represented fact before keeping the file |
| overgrown release target | split target meanings and side effects |
| truth-erasing optimization | restore evidence and semantic inputs first |

This keeps the fix proportional to the finding.

## Do not confuse familiarity with legitimacy

Some patterns survive simply because teams have seen them for years:

- one giant `release` target
- a helper script that "just knows" what to rebuild
- top-level targets that rewrite shared files as a convenience
- cleanup routes that also reset caches or developer state

Longevity does not make those healthy. It usually makes them expensive.

Module 10 asks you to say that clearly.

## Failure signatures worth recognizing

### "We have to run these targets in the right order or it breaks"

That is usually hidden-edge debt, not a usage quirk.

### "Nobody wants to touch release because it does too much"

That is target-contract overload.

### "The build got faster, but now weird stale states appear"

That is a truth-erasing performance repair.

### "We keep adding stamps because the graph feels difficult"

That usually means the boundary facts were never clarified first.

## What this page wants you to leave with

Strong maintainers can say more than "this feels brittle."

They can say:

> this is a multi-writer output problem, or a hidden-edge problem, or a meaningless-stamp
> problem, and here is the smallest recovery move that restores honest ownership.

That is how antipattern recognition becomes useful instead of cynical.
