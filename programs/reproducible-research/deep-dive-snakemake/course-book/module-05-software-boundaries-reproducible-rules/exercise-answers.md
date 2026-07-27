# Exercise Answers

These answers are written as model explanations, not as the only acceptable wording.

## How to use the answer page well

Do not read a model answer first and then bend your exercise to match it.

A better rhythm is:

1. complete the exercise with your own rule, script, package, or runtime evidence
2. write one plain-language explanation of the software boundary you are defending
3. compare that explanation with the model answer
4. revise where the model answer exposes hidden ownership or missing rebuild evidence

The standard to aim for is clear ownership reasoning.

The strongest self-study packets also leave behind six concrete artifacts:

- one ownership map
- one before-and-after rule view
- one script-versus-package decision note
- one runtime-layer note
- one rebuild explanation tied to code or runtime drift
- one maintainer-style review note

If your answers contain only code movement and verdicts, the reasoning is still too
implicit.

## Exercise 1: Map one long rule by ownership

A strong answer separates the visible contract from the software hiding behind it.

Example:

> The rule should keep declared inputs, outputs, params, logs, and resources because that
> is the visible file contract. The data transformation loop belongs in step-local
> implementation because it is owned by this one step. A parsing helper used elsewhere is
> reusable logic and belongs in package code. The ambient Python assumption is a runtime
> issue and needs an explicit environment boundary.

Why this is strong:

- it distinguishes four ownership categories clearly
- it starts from the visible rule boundary rather than code style

## Exercise 2: Extract step-local logic into a script

The resulting rule should still reveal every meaningful input, output, parameter, runtime,
and log path. The script may transform those declared values but must not discover extra
files behind the rule. A focused run proves integration, while reviewing file access or
testing with an absent undeclared file helps establish that extraction did not hide a
dependency.

The missing but important sentence is usually this one:

> After extraction, the rule still teaches the step contract at a glance, while the
> script owns only how the declared work is carried out.

## Exercise 3: Diagnose a hidden dependency

Why it is a software-boundary problem:

- the visible rule contract is smaller than the real behavior
- a reviewer cannot trust the declared execution story

Risks:

- the file graph is misleading
- rebuild behavior may ignore a meaningful input
- publication review becomes weaker because software behavior is partially hidden

Repair:

- declare `config/report-style.yaml` in the rule if it materially affects the output
- keep the script as implementation, not as a place to invent undeclared dependencies

The core principle is simple: meaningful inputs should stay visible at the rule boundary.

## Exercise 4: Decide whether code belongs in `workflow/scripts/` or `src/`

A strong answer keeps the workflow adapter thin and promotes only the reusable part.

Example:

> The script should keep Snakemake-specific path wiring because that is workflow-adjacent.
> The shared parser used by two report steps belongs in `src/` because it can be imported
> and tested directly without a Snakemake context. I would not move publication-path
> decisions into `src/` because those still belong to workflow ownership.

Why this is strong:

- it separates workflow-adjacent and reusable responsibilities cleanly
- it resists moving too much into package code

A useful warning sentence is:

> If moving the code into `src/` makes it harder to see which path assumptions or publish
> choices still belong to the workflow, the promotion happened too early.

## Exercise 5: Write a runtime contract

Rule-scoped environment:

- declares the software needed by one step or a small cluster of closely related steps
- keeps the runtime boundary close to the rule that depends on it

Repository-level `environment.yaml`:

- gives contributors and workflow runners a shared baseline for working with the project
- supports authoring and whole-repository execution setup

Container definition:

- provides a stronger machine-level boundary when host differences are risky
- helps when OS tools, compiled dependencies, or infrastructure portability matter

Why they are not interchangeable:

They all describe software, but they protect different scopes. A repository environment is
too broad to explain every step. A rule-scoped environment is too narrow to replace a full
machine boundary. A container solves portability problems an environment file alone cannot.

A compact layer note might look like this:

| Layer | What it owns |
| --- | --- |
| rule-scoped environment | software needed for one step to execute honestly |
| repository-level environment | contributor tooling and whole-repository working setup |
| container boundary | stronger machine portability when host differences matter |

## Exercise 6: Test reusable code directly

The package API should accept ordinary values or paths and return ordinary values rather
than depending on the injected `snakemake` object. Both workflow scripts remain thin
adapters. Tests cover a valid record, an empty or boundary case, and malformed input.
Path wiring and publication remain workflow-owned; reusable parsing or calculation moves
to the package.

## Exercise 7: Observe code and runtime drift

The implementation change should mark outputs owned by that script as candidates for
rebuilding while unrelated branches remain current. Runtime declaration changes require the
same trust review even when source data is unchanged. After rebuilding, a dry-run
converges and provenance records the repository revision, resolved environment, semantic
configuration, and execution identity.

The key explanatory sentence is:

> Unchanged input data does not preserve trust when the code or runtime that interprets
> that data has changed.

## Exercise 8: Review one wrapper or abstraction adoption

A strong review comment would delay adoption for now:

> I would not merge this wrapper change yet. The shorter rule is not enough benefit unless
> we can explain the wrapper's tool version assumptions, runtime requirements, and visible
> file contract. Right now the wrapper reduces local readability but also reduces review
> confidence. If we can document what it runs and why that contract is acceptable, then the
> wrapper may become a net improvement.

Why this is the right reasoning:

- the question is whether the wrapper increases clarity
- if it hides behavior the team cannot review, it weakens the software boundary

## Exercise 9: Rebuild a published artifact honestly

Why outputs may no longer be trustworthy:

- helper code under `src/capstone/` can change output meaning even with unchanged inputs
- a runtime change in `workflow/envs/python.yaml` can alter execution behavior

Evidence to request before approval:

- confirmation that affected outputs were rebuilt
- provenance showing the new repository revision and runtime context
- a review explanation connecting the software change to the rebuilt artifacts

What provenance should accompany the rebuilt outputs:

- repository revision or release identifier
- relevant runtime declaration or software versions
- execution timestamp
- any workflow configuration that materially affects meaning

The main lesson is that unchanged input datasets do not cancel software drift.

## Exercise 10: Review a complete software boundary

Prioritize undeclared meaningful inputs and unrecorded runtime drift over cosmetic file
placement. Remove duplicate implementation between scripts and packages, keep the file
contract in the rule, and test reusable code directly. A container is justified when OS or
compiled-runtime portability is part of the claim; if a rule-scoped environment already
satisfies the supported contexts, another image may add maintenance without additional
trust.

A strong review usually orders itself like this:

1. check whether the visible rule contract still tells the truth
2. inspect whether scripts or package code introduced hidden dependencies
3. review whether runtime drift is recorded at the right layer
4. choose the narrowest verification route that proves each corrected boundary

## Self-check

If your answers consistently explain:

- who owns the file contract
- where the implementation belongs
- which runtime boundary matters
- what evidence supports rebuilt trust

then you are using the module correctly.

Weak answer pattern:

- "the code is more organized now, so the workflow must be more reproducible"

That sentence skips the visible contract, the runtime contract, and the rebuild story all
at once. If your answers still sound like that, keep revising.
