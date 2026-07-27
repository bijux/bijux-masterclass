# Exercise Answers

These answers are model explanations, not the only acceptable wording.

What matters is whether the reasoning makes repository ownership and review surfaces
clearer.

## How to use the answer page well

Do not read a model answer before you have drawn the repository map or review note
yourself.

A stronger rhythm is:

1. inspect the repository and write your own ownership explanation
2. state one boundary you believe the repository is telling well or badly
3. compare that explanation with the model answer
4. revise where the model answer reveals a hidden dependency, weak file split, or unclear
   contract surface you missed

The target is not identical wording. The target is clearer architectural judgment.

The strongest self-study packets also leave behind six concrete artifacts:

- one reading-order note
- one responsibility table
- one public-artifact trace
- one file-API note
- one failing architecture check
- one bounded review note

If your answers rely only on tree shape and naming taste, the architectural reasoning is
still too implicit.

## Exercise 1: Read the repository in the right order

A strong answer starts at the top-level `Snakefile`, identifies the visible assembly and
targets, then moves into named rule families before scripts or package code. A postponed
surface might be a generic helper or deep package module, because it only becomes useful
after the workflow shape is already visible. The key success signal is that the first
surface answers "how is this workflow assembled?" quickly.

Weak answers start in helpers or packages and only later discover what public artifact or
target surface they were supposed to be reading.

## Exercise 2: Repair a weak entrypoint

What belongs in the entrypoint:

- config loading and validation
- visible workflow assembly
- stable defaults
- the default target or public target surface

What should probably move elsewhere:

- a large inline `run:` block
- step-local logic that belongs in scripts
- reusable logic that belongs in packages

Why this is an architecture issue:

The entrypoint should announce the workflow shape. Once it starts hiding large
implementation logic, the repository entry surface becomes less useful for review and
onboarding.

Weak answers praise a shorter `Snakefile` even when the new split hides ownership rather
than clarifying it.

The missing but important sentence is usually this one:

> After the repair, the entrypoint still teaches configuration, assembly, and final
> targets before the reader needs any deeper file.

## Exercise 3: Write a repository responsibility table

A strong table gives each layer one durable job and one clear prohibition. For example:

- the entrypoint owns visible assembly, not hidden implementation
- rule-family files own coherent workflow concerns, not generic overflow
- scripts own step-local implementation, not undeclared repository scans
- packages own reusable logic, not hidden workflow state
- file APIs own path promises, not producer-only internal details

The least disruptive correction is usually the one that restores the lying boundary
directly instead of inventing a new abstraction.

Example table headings:

- layer
- durable responsibility
- forbidden responsibility
- current violating file
- least disruptive repair

Why this is strong:

- it forces each layer to own one stable job
- it makes misplaced files reviewable instead of merely annoying

## Exercise 4: Review a weak structural split

Why the split is weak:

- the filenames do not communicate ownership or workflow concern
- the split may reduce line count without improving architectural meaning

What kind of boundary would be stronger:

- rule families grouped by coherent workflow concern, such as preprocessing,
  summarization, publishing, or another clearly named domain

What a reviewer should infer from names:

- what the file owns
- which rules belong there
- how it relates to the visible workflow story

The key problem is not the number of files. It is the lack of an ownership signal.

Weak answers rename `misc` to another vague bucket without making the workflow concern any
clearer.

A useful contrast sentence is:

> I rejected the extra abstraction because it would have moved the ambiguity into a deeper
> directory instead of naming a clearer owned concern.

## Exercise 5: Trace one public artifact end to end

A strong trace begins with the documented public path and finds the publication rule, its
declared source result, any step-local script, reusable package call, semantic
configuration, and final target. It marks absent layers honestly rather than inventing
them. An undeclared style file or directory scan is a finding because the visible chain
does not explain the produced bytes.

Example trace elements:

- public path and contract sentence
- owning publication rule
- immediate input artifacts
- script or package call
- semantic config keys
- hidden dependencies or undocumented scans

Why this is strong:

- it lets another maintainer replay the reasoning from the contract backward
- it turns "where does this file come from?" into a bounded review route

## Exercise 6: Repair a file-API gap

What architecture problem this creates:

- path promises are real, but they are undocumented
- workflow-facing and downstream-facing boundaries blur together

Risks:

- refactors break notebooks and tests invisibly
- maintainers cannot tell whether a path rename is a contract change
- consumers depend on internal layout by accident

What to add first:

- a file API or contract document that distinguishes workflow-facing paths from public
  publish-facing paths

The goal is to make path promises reviewable instead of implied.

Weak answers document every internal path equally and therefore blur workflow-facing
coordination with consumer-facing stability.

The strongest answers also say explicitly which path must stay outside the contract and
why, so the file API does not quietly expand into a dump of every useful directory.

## Exercise 7: Diagnose hidden coupling

A strong review comment would say:

> This is not only a local code-quality problem. The helper changes repository behavior
> through undeclared files, unvalidated config, or import-time side effects, which means
> the visible rule and config surfaces no longer tell the full truth. That weakens the
> architecture because reviewers must inspect hidden layers to understand workflow meaning.

Why:

- architecture depends on visible boundaries staying trustworthy
- hidden dependencies move meaning away from the declared repository surfaces

Weak answers call this only a code smell and therefore miss the repository-level damage to
review and onboarding.

## Exercise 8: Detect architecture drift automatically

A useful check encodes one narrow repository claim and names the violating path. For
example, enumerate publish outputs, compare them with `FILE_API.md`, and fail on missing
or stale entries. The failing fixture demonstrates that the check protects an actual
boundary. A generic "architecture invalid" message is too vague to guide repair.

Example good failure message:

> `publish/v1/summary.tsv` is produced by the workflow but has no file-API entry. Document
> the path as public or remove it from the publish boundary.

The key explanatory sentence is:

> This is an architecture check, not generic lint, because it protects the truthfulness
> of one repository boundary that a maintainer depends on.

## Exercise 9: Compare two refactor designs

The ownership-based split is usually safer first because it improves navigation without
creating a new interface. A module or package becomes worthwhile when reuse, independent
testing, or a stable caller contract already exists. Choose the simplest structure that
makes current ownership truthful, and record measurable triggers rather than promising a
future abstraction by instinct.

Weak answers choose the more abstract tree only because it looks more advanced.

## Exercise 10: Conduct a bounded architecture review

Begin with the entrypoint and documented file API, compare the actual rule graph, then
inspect scripts and packages only where the trace leads. Findings about undeclared inputs,
unstable public paths, or hidden semantic config outrank naming preferences. Focused
dry-runs, contract tests, and direct package tests support findings without spending time
on unrelated full-suite execution.

Weak reviews spend most of their time on style and naming while leaving undeclared public
paths or hidden semantic dependencies unranked.

A useful review order often looks like this:

1. inspect the entrypoint and documented public paths first
2. trace one affected artifact through its declared owners
3. check helpers or packages only where the trace reveals hidden coupling
4. choose the narrowest verification route that proves each major finding

## Self-check

If your answers consistently explain:

- who owns orchestration
- where path promises live
- where reusable code belongs
- what makes a refactor honest rather than cosmetic

then you are using the module correctly.

Weak answer pattern:

- "the repository is cleaner now because the folders look more organized"

That sentence skips visible assembly, file APIs, and ownership boundaries all at once. If
your answers still sound like that, keep revising.
