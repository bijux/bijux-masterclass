# Exercise Answers

Use this page after you have written your own answers. The point is comparison, not
copying.

## How to use the answer page well

Do not read a model answer first and then rebuild your exercise to match it.

A better rhythm is:

1. complete the exercise with your own repository tree and evidence
2. write one plain-language explanation of the boundary you are protecting
3. compare that explanation with the model answer
4. revise where the model answer exposes hidden ownership or a missing review surface

The goal is not identical wording. The goal is explicit repository reasoning about growth.

The strongest Module 04 answers usually do four things:

- they name the owning boundary directly
- they explain why the proposed split or contract is strong or weak
- they choose one proportionate review surface
- they describe the repair in terms of repository clarity, not architecture fashion

## Exercise 1: Name the current ownership problem

A strong answer starts by mapping the existing concerns before changing any files.

Example:

> The current `Snakefile` mixes preprocessing, summarization, publication, and report
> assembly in one flat surface. That hides ownership because a reviewer cannot tell which
> rules belong together or which concern should absorb the next change. The workflow is
> still one graph because all of those concerns contribute to one top-level target story,
> but the file arrangement no longer teaches that story clearly.

Why this is strong:

- it explains the existing ownership problem before refactoring
- it distinguishes one graph from one file

## Exercise 2: Choose one healthy include split

A strong answer sounds like this:

> The workflow should split its publish logic into `workflow/rules/publish.smk` because
> that file can own one clear concern: promotion of reviewed internal results into the
> public boundary. This improves named ownership while keeping the top-level orchestration
> visible. It is not yet a module because the repository still owns one visible graph and
> the split is about internal organization rather than reusable external interface.

Why this is strong:

- it names one real concern
- it distinguishes an include-level split from a module-level split

## Exercise 3: Prove the graph stayed visible

A strong answer compares graph visibility before and after the split rather than treating
the refactor as successful by default.

Example:

> The before and after rule graphs preserve the same high-level dependency story, but the
> after version makes it easier to see where publication begins and where preprocessing
> ends. A warning sign would be needing to open several files before understanding the
> top-level target route that the original graph showed immediately.

Why this is strong:

- it uses the graph as a review surface, not decoration
- it names one criterion for "too much hiding"

## Exercise 4: Decide whether a boundary is a module

A strong answer asks interface questions first.

Example answer shape:

- candidate boundary:
  - a reusable QC bundle
- interface questions:
  - what inputs does it consume
  - what outputs does it promise
  - can the top-level workflow still explain the graph after the split
- decision:
  - promote it to a module only if those answers are explicit
- opposite sign:
  - if the call site still depends on hidden globals or private path conventions, keep it
    as an include for now

Why this is strong:

- it makes interface clarity the criterion
- it avoids promoting a split just because the folder looks cleaner

## Exercise 5: Write a public file contract

A strong answer sounds like this:

> `publish/v1/summary.json` is a stable public output describing the run-level summary,
> while `results/sampleA/qc_raw.tsv` remains internal workflow state. A change to the
> published summary keys or semantics would require explicit interface review because it
> affects downstream trust, not just internal orchestration.

Why this is strong:

- it distinguishes public from internal paths clearly
- it explains what kind of change becomes an interface event

## Exercise 6: Review one abstraction you should reject

A strong answer rejects abstraction by naming the ownership loss it would cause.

Example:

> A catch-all `utils.smk` file is tempting because it feels tidy, but it would blur rule
> logic, path helpers, and interface code into one bucket. That weakens ownership because
> the next maintainer would still not know where a new publish concern should land. A
> smaller include split by concern is stronger because it keeps the graph visible and the
> boundaries explainable.

Why this is strong:

- it explains why the abstraction is tempting
- it rejects it for a structural reason, not taste

## Exercise 7: Break and defend a schema boundary

The valid fixture passes a schema that describes required fields, types, and allowed
values. Renaming a required field fails the targeted contract check even when the file is
valid JSON or TSV. That failure is correct: parseability is weaker than compatibility,
and a consumer-visible field change requires deliberate versioning or migration.

## Exercise 8: Keep resources portable while scaling

Rules declare abstract needs such as threads, memory, and runtime. A local profile maps
them to bounded workstation execution; a cluster profile maps the same needs to scheduler
resources. Neither rule contains a queue name or submission command. The invariant is that
resource policy can change without changing target paths, algorithms, or output semantics.

## Exercise 9: Review a full structural pull request

A strong review checks ownership before accepting new files, explicit interfaces before
accepting a module, and consumer semantics before accepting a schema change. It compares
the rule graph and validates public fixtures. Redundant wrappers or modules with hidden
globals should be removed. Future gates should separately defend syntax/lint, planned
graph shape, and the public file contract rather than rerunning unrelated heavy suites.

## Exercise 10: Rehearse the next month of growth

A strong answer predicts future landing places from the current structure rather than
inventing a new structure on the spot. If a new assay, report, or publish artifact already
has an obvious owning boundary, the current design is working. If every imagined change
requires reopening the whole directory strategy, the repository is not scaled yet even if
the current diff looks neat.

## What all ten answers should have in common

The best Module 04 answers usually:

1. split by named ownership rather than by file length
2. promote boundaries into modules only when the interface is explicit
3. distinguish internal workflow state from public file contracts
4. choose proof routes that defend the actual scaling boundary under review

If your answers do those four things, the module is landing in the right direction.
