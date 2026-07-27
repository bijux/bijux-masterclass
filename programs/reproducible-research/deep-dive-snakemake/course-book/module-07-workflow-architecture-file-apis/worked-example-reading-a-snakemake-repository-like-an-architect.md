# Worked Example: Reading a Snakemake Repository Like an Architect

This file ties the whole module together around one realistic problem:

> a workflow repository still works, but new contributors cannot explain its shape without an oral tour.

The question is not "how do we inspect every file?" The question is how to read the
repository in an order that reveals ownership, path contracts, and drift risk quickly.

## How to use this worked example

Work through this page with the five core lessons nearby.

Do not treat it as a summary you skim after the module. Treat it as a guided architecture
walkthrough:

- where to start reading
- what to postpone
- how to trace one public artifact
- how to decide whether drift is real or only a vague discomfort

## The one-day teaching goal

By the end of this example, you should be able to explain one Snakemake repository
without falling back on phrases like "the important parts are spread around."

You should be able to say:

- which surface a new maintainer reads first
- which rule family or layer owns which concern
- where path promises become explicit
- which structural problem deserves refactoring now

## The lab route

Work through the example in this order:

1. start at the entrypoint and identify visible assembly
2. inspect named rule families before any helper code
3. separate reusable workflow modules from local assembly boundaries
4. confirm the public file contract and path promises
5. finish by deciding which architectural drift matters now

## The starting situation

Assume you inherit the capstone and need to answer three questions quickly:

1. where is the workflow assembled
2. where do the main rule families live
3. where are public promises documented

If you cannot answer those questions in a stable order, the repository architecture is
already too opaque.

## What the learner should notice first

The repository may still run perfectly.

The problem is that maintainers are depending on oral guidance instead of structure. That
is exactly the kind of architecture weakness that becomes expensive later even when the
workflow still executes correctly today.

## Start at the entrypoint

The top-level `Snakefile` is the right first file because it visibly:

- loads or validates config
- includes rule families or modules
- sets directory defaults when needed
- defines the main target

That is exactly what a good entrypoint should do.

The entrypoint should tell a reviewer, early, which visible workflow story they are about
to inspect. That is why the first architectural read should begin there rather than in
`src/` or a helper directory.

## Read rule families before helpers

Once the entrypoint is clear, inspect the named rule families.

This gives a workflow story such as:

- preprocessing creates internal working surfaces
- summarization promotes selected artifacts toward publication
- publishing assembles and verifies the public contract

That sequence teaches repository architecture and workflow meaning at the same time. If
you jump into helper code first, you lose the visible graph and start from implementation
detail instead of ownership.

## A short checkpoint before you continue

Pause here and ask:

- could a new maintainer explain the workflow shape without opening package code yet?
- do the rule-family names already signal concern boundaries?
- is the top-level assembly revealing more than it hides?

If the answer to any of these is no, the architectural story is already weaker than it
should be.

## Separate local assembly from reusable workflow modules

Now inspect `workflow/modules/` only after rule-family ownership is already visible.

That distinction matters:

- rule families group one repository's visible graph
- workflow modules expose reusable workflow bundles with their own boundary

Seeing both in the same pass helps a reviewer ask a better question: is this file here
because the repository needs local readability, or because the workflow boundary is
genuinely reusable?

## Why this reading order matters educationally

This is the moment where repository inspection stops being a scavenger hunt.

The learner is no longer just finding files. They are using sequence to decide which
surfaces deserve trust first and which should be read only after the workflow story is
already visible.

## Confirm the file API explicitly

Architecture review is incomplete until the path contracts are visible.

The capstone keeps those in surfaces such as:

- `workflow/CONTRACT.md`
- `workflow/contracts/FILE_API.md`
- publish-facing contract notes

Those docs answer questions the tree alone cannot:

- which workflow paths are public
- which published paths are stable
- which changes count as contract changes instead of internal refactors

This is where architecture stops being intuitive and becomes reviewable.

## Trace one artifact through its owners

Take one concrete public output such as `publish/v1/summary.json` and record the route:

```mermaid
flowchart LR
  entry["Snakefile requests publish target"]
  family["workflow/rules/... owns promotion"]
  script["workflow/scripts/... adapts execution"]
  package["src/... owns reusable logic"]
  api["FILE_API.md defines consumer promise"]

  entry --> family --> script --> package --> api
```

Not every artifact passes through every layer. That is useful information. A missing layer
is not a defect. An unexplained jump across layers often is.

## What the learner should notice now

The artifact trace is doing two jobs at once:

- it shows which surface owns each step
- it exposes where the visible repository story breaks and hidden assumptions begin

That is why this kind of trace is more educational than a generic folder tour.

## Catch architecture drift before it hardens

Now compare the documented repository shape with the actual one.

Typical drift signals include:

- a crowded entrypoint accumulating hidden logic again
- helper code becoming the first place reviewers must look
- public paths being used without contract updates
- modules or directories whose names no longer reveal ownership

At this stage, the review should not ask only "does it run?" It should ask "does the
repository still teach its own shape?"

## The repaired architecture story

By the end of the walkthrough, the repository can be described cleanly:

1. the entrypoint reveals visible assembly
2. rule families carry named ownership
3. reusable modules are distinct from local structure
4. file APIs define public path promises
5. helper and package code support the workflow instead of replacing its story

That is what it means to read a Snakemake repository like an architect.

## Review questions for the repaired design

When you inspect a repository shaped like this, ask:

1. which surface should a new maintainer read first and why
2. which layer owns one public artifact at each step
3. where the path contract becomes explicit
4. which helper or package boundary is supporting the workflow and which one is swallowing it
5. which drift signal would justify the next structural refactor

If those answers are visible, the module's architecture story has landed.
