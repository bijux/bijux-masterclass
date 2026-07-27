# Entrypoints, Repository Layers, and Visible Assembly

The first architecture question in a Snakemake repository is simple:

> where should a reviewer look first to understand the workflow?

If that question does not have a clear answer, the repository is already asking too much
from memory and too little from structure.

This page is about making the entrypoint and layer responsibilities visible.

## How to use this page

Read this page while keeping one real repository open in front of you.

Your job is not to admire the folder tree. Your job is to answer one practical question:

> if a new maintainer opens this repository for the first time, what should they read first, and what should that first surface teach them immediately?

By the end of the page, you should be able to explain the repository in discovery order,
not only in storage order.

## The top-level entrypoint should announce the workflow shape

In the capstone, the top-level `Snakefile` does several important things:

- loads and validates config
- sets stable defaults
- assembles the workflow from named rule files
- defines the entrypoint target

That is a strong job for the entrypoint.

It tells a reviewer:

- where workflow assembly starts
- which files contribute rules
- which boundaries are visible at the top level

The `Snakefile` should feel like a routing and assembly surface, not a hiding place.

## Start with visible assembly before hidden implementation

The beginner mistake is to dive into helpers, packages, or folder depth too early.

A stronger reading order is:

1. open the top-level `Snakefile`
2. identify the included rule families and visible targets
3. inspect the repository layers those rule families point into
4. descend into scripts or packages only after the workflow shape is already visible

If the repository only makes sense in the reverse order, the architecture is already
teaching the story badly.

## A repository becomes clearer when layers have jobs

The capstone architecture already points toward a healthy split:

- `Snakefile` for visible assembly
- `workflow/rules/` for rule families and declared file contracts
- `workflow/modules/` for reusable workflow bundles
- `workflow/scripts/` for workflow-adjacent implementation
- `src/capstone/` for reusable package code
- `profiles/` for execution policy
- `config/` for input configuration and schema boundaries

These folders are useful only when their ownership stays legible.

## Layering is not about folder aesthetics

A repository layer matters when it answers a review question quickly.

For example:

- “where is the workflow assembled?” points to `Snakefile`
- “where does this rule family live?” points to `workflow/rules/`
- “where is reusable implementation code?” points to `src/capstone/`
- “where are path promises documented?” points to the file API and contract docs

If a folder exists but does not answer any boundary question, it may be decorative rather
than architectural.

## One useful architecture map

```mermaid
flowchart TD
  snakefile["Snakefile"] --> rules["workflow/rules/"]
  snakefile --> modules["workflow/modules/"]
  rules --> scripts["workflow/scripts/"]
  rules --> contracts["workflow/contracts/FILE_API.md"]
  scripts --> package["src/capstone/"]
  snakefile --> config["config/ and schema"]
  snakefile --> profiles["profiles/ as policy"]
```

This diagram matters because it shows the repository as a set of named boundaries rather
than a pile of adjacent directories.

## One concrete repository-reading exercise

Take one public target such as a published bundle or report and trace it backward.

A strong repository lets you answer these in order:

- where is the target declared or surfaced?
- which rule family owns it?
- which scripts or package code implement it?
- which config or policy surfaces influence it?

If you have to discover those answers by wandering through helpers first, visible
assembly has already been lost.

## A weak entrypoint

Weak shape:

- the `Snakefile` contains large implementation blocks
- rule inclusion happens with no clear naming or ownership reason
- important defaults are scattered across helper files most reviewers never read

This makes the repository harder to enter and easier to misunderstand.

## A stronger entrypoint

Stronger shape:

- keep the top-level file focused on assembly, defaults, and visible targets
- use named includes or modules that match coherent rule families
- keep implementation code and helper logic in their own owned layers

Now a reviewer can explain the repository in the same order they discover it.

## The beginner mistake to catch early

Beginners often think a short `Snakefile` is automatically good.

That is false.

A short entrypoint that hides critical defaults, routing, or ownership behind indirection
can be worse than a slightly longer one that teaches the workflow honestly. Brevity helps
only when the visible story stays intact.

## A practical test

Ask these questions:

1. Can a new reviewer locate the workflow assembly point quickly?
2. Can they tell which folders are for orchestration, implementation, policy, and contracts?
3. Does the entrypoint reveal more than it hides?

If those answers depend on prior oral explanation, the architecture is already weaker than
it should be.

## Common failure modes

| Failure mode | What goes wrong | Better repair |
| --- | --- | --- |
| `Snakefile` becomes a giant monolith | assembly and implementation blur together | keep orchestration visible and move owned logic outward |
| folders exist with no clear responsibility | readers browse without a mental map | assign each layer one reviewable job |
| config, policy, and workflow logic mix together | architecture questions become semantic questions | separate meaning, policy, and configuration surfaces clearly |
| helper code becomes easier to find than rules | the visible DAG stops being the first story | keep rule assembly easier to inspect than helper internals |
| entrypoint only works for insiders | onboarding depends on oral tradition | make the top-level file teach the repository layout directly |

## What a reviewer should hear

A strong explanation sounds like this:

> The top-level `Snakefile` shows assembly, target shape, and major boundaries first. I
> only need to go deeper after I understand which rule families, policy surfaces, and
> contracts are being assembled.

That is a more useful explanation than "the repo is split into many folders," because it
teaches discovery order rather than mere geography.

## The explanation a reviewer trusts

Strong explanation:

> the `Snakefile` assembles the workflow and points to the owned rule families, while the
> repository layers separate orchestration, implementation, contracts, configuration, and
> policy so a reviewer can inspect one boundary at a time.

Weak explanation:

> the repository is organized into folders, and the important parts are spread around.

The strong explanation describes ownership. The weak one describes geography.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain what the top-level `Snakefile` should own
- describe why repository layers need named responsibilities
- explain how visible assembly helps code review and onboarding
- identify one sign that a repository entrypoint is hiding too much

If you still describe the entrypoint mainly as a startup file, pause and reframe. In this
module, it is the first architectural teaching surface.
