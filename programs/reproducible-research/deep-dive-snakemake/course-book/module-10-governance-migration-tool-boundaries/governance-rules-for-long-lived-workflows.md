# Governance Rules for Long-Lived Workflows

Good governance is not bureaucracy layered on top of a workflow.

Good governance is the small set of review rules that stop a repository from drifting into
private knowledge and accidental contracts.

## How to use this page

Read this lesson with one real workflow team in mind, even if you have to invent the team
for practice.

Work through it in this order:

1. identify what governance must protect
2. decide which review rules are worth enforcing every time
3. test whether each rule would reject a realistic bad change
4. keep only the rules that are short, sharp, and durable

The target is not governance theater. The target is review discipline that survives busy
weeks and staff turnover.

## What governance should protect

In a long-lived Snakemake repository, governance should protect at least four things:

- the public file contract
- the boundary between workflow meaning and operating policy
- the proof route maintainers use under pressure
- ownership clarity around helper code, modules, and downstream interfaces

If governance does not protect those, it usually protects the wrong things.

## Start by deciding what the team must stop forgetting

Governance exists because some mistakes are too expensive to relearn repeatedly.

In a long-lived workflow, those mistakes usually sound like this:

- nobody noticed a new published file became a contract
- a profile started carrying semantic settings
- proof commands decayed because review pressure was high
- helper ownership moved, but nobody recorded what became harder to inspect

Good governance turns those recurring failures into explicit review rules.

## A simple governance model

```mermaid
flowchart TD
  contract["public contract rules"] --> policy["policy review rules"]
  policy --> proof["proof-surface rules"]
  proof --> ownership["ownership and boundary rules"]
  ownership --> review["pull-request review habit"]
```

This is enough for most workflow teams. Governance only becomes heavy when the repository
itself is already unclear.

## Rule 1: Every public file needs a contract story

If a new file appears under a published boundary, review should ask:

- who is meant to trust this file
- whether it is stable enough for downstream use
- where its meaning is documented
- whether verification and manifests know it exists

This keeps "we happened to publish it" from turning into "we now support it forever."

## Rule 2: Profiles may change policy, not workflow meaning

Profile review should treat these as ordinary:

- core count
- executor selection
- queue or resource policy
- latency and retry settings, when justified

Profile review should treat these as escalation triggers:

- sample selection
- publish path meaning
- analytical thresholds that change results
- anything that alters the planned workflow semantics

This one rule prevents a lot of quiet drift.

## Rule 3: Proof surfaces must survive change

Every significant workflow change should preserve or improve at least one visible proof
route:

- dry-run meaning
- rerun-cause visibility
- publish verification
- profile comparison
- execution evidence

If a change removes one of these with the promise to restore it later, governance should
push back.

## Rule 4: Ownership boundaries should stay visible

A repository becomes fragile when nobody can answer which layer owns:

- orchestration
- step-local implementation
- reusable package code
- public path contracts
- operating policy

Governance should force that question into review whenever a helper boundary or module
boundary moves.

## Rule 5: Downstream trust should be reviewed explicitly

Teams often notice downstream consumers only after a migration breaks them.

Good governance asks earlier:

- which published files are machine-facing
- which are human-facing
- whether any downstream consumer still depends on internal results
- whether a path change is compatible, repair-only, or version-worthy

This is why publish review belongs inside governance, not only release engineering.

## A small example

Suppose a pull request:

- changes `profiles/slurm/config.yaml`
- adds a field to `publish/v1/summary.json`
- moves one helper from `workflow/scripts/` into `src/`

A weak governance process might review that as one generic refactor.

A stronger process applies three separate rules:

- profile review checks policy versus semantics
- publish review checks downstream compatibility
- ownership review checks whether the new package boundary is clearer or more hidden

That is the difference between generic code review and workflow governance.

## One concrete governance exercise

Suppose a pull request:

- adds a new `publish/v1/metrics.tsv`
- moves analytical thresholds into a cluster profile
- extracts discovery logic into a helper package

A weak team review might approve the change because each edit looks reasonable in
isolation.

A governance-aware review asks three separate questions:

1. does the new published file have a contract and verification story
2. did workflow meaning leak into operating policy
3. did helper ownership become clearer or more hidden

That is the level of separation this lesson is trying to teach.

## Keep governance lightweight but sharp

A good governance checklist can be short:

1. did the public contract change
2. did workflow meaning move into policy
3. did we preserve proof routes
4. did ownership get clearer or blurrier
5. did downstream trust get weaker

Short is good. Vague is not.

## Governance failure patterns

Watch for these signals:

- every review becomes style discussion because boundary questions are never asked
- profiles accumulate semantic settings because they are convenient to change
- publish paths grow, but nobody owns compatibility review
- helper code expands, but no one records what moved out of visible workflow logic
- important commands still exist, but nobody can say which are canonical under pressure

These are governance problems even when the repository still "works."

## The beginner mistake to catch early

The most common beginner mistake is writing governance rules that sound wise but cannot be
enforced.

Examples of weak rules:

- keep the workflow understandable
- avoid messy profiles
- document important changes

Those are sentiments, not rules.

Good governance language names a boundary and a review consequence. For example:

- every published file must appear in the file API and verification route
- profiles may change execution policy but not sample selection or analytical thresholds
- major helper moves must preserve a visible proof or inspection route

## Keep this standard

By the end of Module 10, a team should be able to say:

- which workflow changes always need contract review
- which profile changes need semantic skepticism
- which proof routes are non-negotiable
- which ownership boundaries must stay explicit

If that cannot be said plainly, governance is still implicit, and implicit governance is
where long-lived drift starts.
