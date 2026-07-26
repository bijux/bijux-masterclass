# Exercises


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive Snakemake"]
  section["Scaling Workflows Interface Boundaries"]
  page["Exercises"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Use these after reading the five core lessons and the worked example. The goal is to make
your scaling and interface reasoning visible, not to produce the most elaborate folder
tree.

Each answer should show three things:

- the boundary you are protecting
- the evidence route you would use
- the refactor or review decision that follows

## Exercise 1: Choose one healthy rule-family split

Take a workflow that is growing but still conceptually one graph.

Describe one split that belongs under `workflow/rules/` and explain why it improves named
ownership without hiding the orchestration story.

What to hand in:

- the workflow concern being split
- the proposed file name
- one sentence explaining what that file owns
- one sentence explaining why this is not yet a module boundary

## Exercise 2: Decide whether a boundary should become a module

Describe one sub-workflow that might be promoted into `workflow/modules/`.

Explain whether it really has a stable interface or whether it should remain an include.

What to hand in:

- the candidate boundary
- the interface questions you would ask first
- your decision and why
- one sign that would make the opposite decision safer

## Exercise 3: Write a small file contract

Choose one output family and describe it as a public contract.

What to hand in:

- the stable path or path family
- the semantics of that file family
- one internal path family that should not be treated as public
- one sentence explaining what kind of change would require explicit interface review

## Exercise 4: Choose the right scaling gate

For each of these questions, choose the smallest honest review surface:

- did the rule-family split keep the visible workflow surface legible
- did the public contract still align after the refactor
- did the workflow still plan the same high-level work

What to hand in:

- the command or surface for each question
- one sentence per route explaining why it is the right size of proof

## Exercise 5: Review one resource or executor-facing assumption

Describe one workflow rule family that is heavier than the others.

Explain how the repository should make that visible without hardwiring the design to one
executor story.

What to hand in:

- the heavier workflow concern
- the workflow-side resource distinction you would make visible
- one sentence explaining what should remain policy rather than workflow meaning

## Exercise 6: Refactor one Snakefile into rule families

Start from a working Snakefile with at least six rules. Group them into two or three
ownership-based includes while retaining a readable entrypoint.

What to hand in:

- the ownership map that justified each split
- the resulting tree and top-level Snakefile
- before/after `--list-rules` and dry-run evidence
- one split you deliberately rejected

## Exercise 7: Specify a module interface

Choose a genuinely reusable rule family and write its interface before moving code.

What to hand in:

- named inputs, outputs, parameters, and software assumptions
- the mapping from caller paths to module paths
- one hidden global dependency you removed
- a test showing the caller can consume the promised output

## Exercise 8: Break and defend a file API

Define a JSON or TSV public output with a schema. Deliberately remove or rename one
required field and observe the validation failure.

What to hand in:

- the documented path and schema
- valid and invalid fixtures
- the targeted validation command
- an explanation of why this is an interface change rather than an internal refactor

## Exercise 9: Keep resource declarations portable

Give two rule families meaningfully different CPU, memory, or runtime needs. Map those
declarations through local and cluster-oriented profiles without embedding scheduler
commands in the rules.

What to hand in:

- workflow-side resource declarations
- both policy mappings
- paired dry-runs
- the invariant that makes the workflow executor-independent

## Exercise 10: Review a complete scaling change

Review a repository change that adds includes, one module, a file schema, and CI checks.
Decide whether each boundary is justified and whether the evidence matches the claim.

What to hand in:

- findings ordered by impact
- a graph comparison and public-contract validation
- any abstraction that should be removed or postponed
- the smallest sufficient gate set for future changes

## Mastery standard for this exercise set

Across all ten answers, Module 04 wants the same habits:

- you split by named ownership rather than by file length alone
- you treat interfaces as contracts rather than folder preferences
- you choose proof routes that defend the boundary actually under review

If your answer says only "the repo should be more modular," keep going.
