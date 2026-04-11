# Deciding When Make Should Stop Owning the Problem

This page is about tool boundaries.

Make is excellent within its natural territory, but many inherited systems become painful
because the team never decides which concerns still belong in Make and which ones do not.

## The false choice to avoid

Boundary conversations often collapse into one of two slogans:

- "Make can do anything if you are clever enough"
- "Make is old, so we should replace it"

Both are weak positions.

The first ignores modeling limits. The second ignores the places where Make remains a
strong, honest tool.

Module 10 asks for a better question.

## The sentence to keep

When you are unsure about a boundary, ask:

> is Make still the most honest owner of this responsibility, or are we forcing it to
> imitate a different kind of system?

That wording matters because ownership is the real issue.

## What Make is naturally good at

Make is especially strong when the problem has these properties:

- work can be explained as dependencies between named outputs
- the build benefits from incremental rebuild behavior
- correctness depends on explicit inputs and outputs
- local file or manifest publication is central
- humans need to inspect why a route ran and what it produced

Typical good fits include:

- compilation and local build graph orchestration
- generated-file pipelines with explicit outputs
- deterministic packaging steps
- audit and selftest routes tied to repository-local evidence

These are not accidental successes. They align with what Make models well.

## What Make is often forced to fake

Make becomes uncomfortable when the responsibility is dominated by things it cannot model
cleanly:

- long-lived remote state
- dynamic workflow scheduling over distributed systems
- approval processes with external authorities
- deployment coordination with rollback and live service state
- provenance graphs whose truth lives outside repository-local files and manifests

Make can still invoke the tools that own those concerns. That is different from Make being
the owner.

## A simple boundary rubric

Use these questions:

1. can the responsibility be expressed truthfully as local inputs, outputs, and publication
   events
2. can failures be diagnosed with repository-local evidence
3. does incremental rebuild behavior make sense here
4. does the concern rely on external state Make cannot observe honestly
5. would Make be orchestrating, or pretending to be a scheduler, deployment controller, or
   policy engine

The more often questions 4 and 5 dominate, the more likely another tool should own the
concern.

## Keep orchestration distinct from ownership

A boundary mistake many teams make is confusing "Make calls it" with "Make owns it."

For example:

```make
deploy:
	@./scripts/deploy-prod.sh
```

This target tells us almost nothing about ownership.

Possible interpretations:

- Make owns deployment semantics
- Make merely offers a convenience wrapper
- the real deployment controller lives elsewhere
- the script is managing state Make cannot see

Those are not equivalent.

A healthier pattern is to state the ownership plainly:

- Make owns build, package, and local verification
- deployment is owned by a separate system with its own state and approval model
- Make may expose a convenience entrypoint for initiating that system, but not pretend to
  define deployment truth

This sounds subtle. In practice it removes a lot of confusion.

## A good boundary handoff is explicit

Suppose a team decides release metadata generation belongs in a dedicated tool rather than
custom Make macros.

An explicit handoff looks like this:

- Make still defines when metadata generation is needed
- the dedicated tool produces a declared manifest or metadata file
- downstream Make targets depend on that published result
- errors surface as failed production of a known artifact

An implicit handoff looks like this:

- a shell wrapper calls several tools
- the final files appear somewhere in `dist/`
- nobody can say where metadata truth actually lives

The first is a boundary. The second is an excuse.

## Make should not remain owner out of habit

Many long-lived builds keep concerns inside Make for reasons that are no longer technical:

- "it is already there"
- "the maintainer knows how it works"
- "rewriting would be annoying"
- "CI already calls the target"

Those may be real constraints. They are not ownership arguments.

A real ownership argument sounds like this:

- the concern is still file-oriented and local
- Make still exposes the meaningful edges clearly
- observability remains sufficient
- another tool would add indirection without solving a modeling problem

That is a much higher standard.

## Another tool should not become owner out of fashion

The opposite error is also common:

- a team adopts a workflow system because it feels modern
- Make is removed from places where it was already doing honest graph work
- repository-local truth becomes harder to inspect
- the new system takes on more responsibility than anyone can explain

Migration to another tool is justified when it solves a real ownership mismatch, not when
it merely changes aesthetics.

If a new tool cannot answer "what exactly is it better at modeling," the handoff is
probably premature.

## Small examples of honest boundaries

### Keep it in Make

Case:

- generating headers from schema files
- compiling binaries
- packaging a tarball with a manifest and checksum

Why Keep it:

- inputs and outputs are explicit
- local publication matters
- incremental rebuild behavior is valuable

### Hand it off

Case:

- coordinating staged production deployment with approvals and rollback state

Why hand it off:

- the truth lives in remote state and operational policy
- the concern needs a controller, not just local dependency evaluation
- Make can start or validate the process, but it should not own it

### Hybrid boundary

Case:

- Make builds and packages an artifact
- a release service signs and publishes it

Why hybrid:

- Make remains the owner of artifact production
- the release service owns signing authority and publication policy
- the handoff is the produced artifact plus declared metadata

Hybrid boundaries are often the clearest ones.

## A warning sign: Make is becoming a policy engine

Be careful when Make starts encoding:

- environment approval rules
- user roles
- deployment windows
- multi-stage remote workflows
- long-lived mutable state machines

Those are usually signs that Make is being stretched into a policy or orchestration system
rather than used as a build graph engine.

At that point the question is no longer "can we script it?" The question is "should this
responsibility have a different owner?"

## Failure signatures worth recognizing

### "Our Makefile now mostly calls APIs and waits for remote systems"

That usually means Make is no longer the real owner of the workflow.

### "We moved packaging out of Make and lost clear artifact evidence"

That often means the handoff was done for fashion rather than for a real modeling reason.

### "Nobody can tell whether deployment failed because of build truth or remote state"

That is usually a boundary problem: too many kinds of truth were hidden behind one target.

### "The new system is powerful, but local review got harder"

That can mean the team handed off responsibility too eagerly and lost repository-local
legibility.

## What this page wants you to say

A strong Module 10 boundary answer sounds like this:

> Make should keep owning the local build graph, generated outputs, and package production,
> but it should stop pretending to own remote deployment state and approval policy. The
> handoff boundary is the published artifact and its evidence.

That is a much better answer than either "keep Make for everything" or "replace Make."
