# Exercises

Use these after reading the five core lessons and the worked example. The goal is to make
your scaling decisions visible through ownership maps, interface notes, and review
evidence, not through a bigger folder tree.

## How to work through this set

Treat the ten exercises as one long repository-growth lab.

Before each answer:

1. name the boundary you are protecting
2. choose the smallest review surface that proves the claim
3. keep the concrete evidence next to the structural decision

If you skip the ownership question, the work turns into file-shuffling instead of
educational scaling practice.

Do them in order. The set is one day-long progression:

- Exercises 1-3 establish ownership and graph visibility.
- Exercises 4-6 decide interfaces and public contracts.
- Exercises 7-8 defend schemas and resources.
- Exercises 9-10 review the whole structural change like a maintainer.

For every answer, keep three things:

- the boundary you are protecting
- the evidence route you actually used
- one short sentence explaining why the split improves understanding instead of only moving files

## Recommended working layout

If you want one repository shape that can support the whole day, use a small lab like
this:

```text
module04-lab/
├── Snakefile
├── workflow/
│   ├── rules/
│   └── modules/
├── config/
├── publish/
├── results/
├── tests/
└── artifacts/
```

That layout makes it easier to compare ownership, interfaces, public contracts, and gates
without rebuilding the example from scratch for every prompt.

## Exercise 1: Name the current ownership problem

Take a working workflow with at least six rules and no existing structure plan. Classify
every rule into one owned concern such as preprocessing, summarization, publication, or
quality control.

What to hand in:

- the rule list
- one sentence of ownership for each group
- one place where the current file arrangement hides that ownership
- one reason the workflow is still one graph despite several concerns

Study note:
This is not a file-count exercise. It is an ownership-clarity exercise.

## Exercise 2: Choose one healthy include split

Move one coherent rule family into `workflow/rules/` while keeping the entrypoint short
and readable.

What to hand in:

- the before and after tree
- the top-level `Snakefile`
- before and after `--list-rules` output
- one split you deliberately did not make yet and why

Study note:
If the entrypoint becomes harder to explain after the split, the split is not healthy yet.

## Exercise 3: Prove the graph stayed visible

Render the rule graph before and after the include split. Compare what a reviewer can
learn from both versions.

What to hand in:

- both graph artifacts
- one paragraph explaining what remained stable
- one paragraph explaining what became easier to review
- one signal that would tell you the split hid too much

Study note:
The point is not only that the graph still exists. The point is that a reviewer can still
learn from it quickly.

## Exercise 4: Decide whether a boundary is a module

Choose one candidate sub-workflow and decide whether it should stay an include or become
a real module boundary.

What to hand in:

- the candidate boundary
- named inputs, outputs, parameters, and assumptions
- your decision and why
- one missing interface detail that would block promotion to a module

Study note:
Promote a module only when the interface is real enough to explain without hand-waving.

## Exercise 5: Write a public file contract

Choose one output family and document it as a consumer-facing contract while marking
related internal paths as internal.

What to hand in:

- the public path or path family
- the meaning of that path
- one internal path family that should never be consumed directly
- one change that would require explicit interface review

Study note:
This is where many scaling refactors fail. Paths look tidy, but nobody can say which ones
are safe for consumers.

## Exercise 6: Review one abstraction you should reject

Find a structural change that would make the repository look more abstract but would not
actually improve understanding.

Examples might include:

- a module with no stable interface
- helper files split by size instead of ownership
- a catch-all `utils.smk` file

What to hand in:

- the rejected abstraction
- why it is tempting
- why it would weaken ownership or review
- the smaller change you chose instead

Study note:
Abstraction is not automatically progress. The right test is whether another human can
explain the repository more easily afterward.

## Exercise 7: Break and defend a schema boundary

Define a public JSON or TSV contract with a schema, then introduce one incompatible change
and make the validation fail.

What to hand in:

- the documented contract path
- the schema or validation rule
- valid and invalid examples
- an explanation of why the failure protects a public boundary rather than an internal preference

Study note:
This exercise should make interface drift feel concrete rather than theoretical.

## Exercise 8: Keep resources portable while scaling

Pick two rule families with meaningfully different CPU, memory, or runtime needs. Declare
those needs without embedding scheduler-specific commands in the rules.

What to hand in:

- the workflow-side resource declarations
- two policy mappings such as local and cluster-oriented contexts
- paired dry-runs or review evidence
- the invariant that makes the workflow executor-independent

Study note:
If the rule contains scheduler folklore, the scaling cleanup has introduced a new problem.

## Exercise 9: Review a full structural pull request

Review a change that adds includes, promotes one module, introduces a file contract, and
adds a validation gate.

What to hand in:

- findings ordered by trust impact
- one graph comparison
- one contract validation result
- any boundary that should be simplified, postponed, or removed

Study note:
This is a review exercise first. Treat structural changes as trust changes, not as style
preferences.

## Exercise 10: Rehearse the next month of growth

Imagine the repository will gain one more assay, one more report, or one more publish
artifact next month. Decide where each change would land if your current structure is
healthy.

What to hand in:

- the predicted landing place for each new concern
- the boundary that absorbs it
- the proof route you would rerun afterward
- one sign that your current structure would need another redesign

## Exit standard for the exercise day

Do not count the day complete unless you can do all of this without leaning on the answer
page as a restructuring script:

- explain one split in terms of named ownership
- reject one abstraction that only adds indirection
- defend one public file contract and one internal path family clearly
- choose one gate that protects one specific structural claim
- predict where the next month of growth should land

## Mastery standard for this exercise set

Across all ten answers, Module 04 wants the same habits:

- you split by named ownership rather than by file length
- you promote modules only when the interface is real
- you treat public paths and schemas as contracts
- you choose proof routes that defend the exact structural claim under review

If your answer says only "the repo should be more modular," keep going.
