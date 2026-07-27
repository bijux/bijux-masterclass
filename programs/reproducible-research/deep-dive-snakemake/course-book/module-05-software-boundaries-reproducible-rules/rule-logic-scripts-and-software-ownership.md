# Rule Logic, Scripts, and Software Ownership

The first software-boundary decision is usually the most common one:

> should this logic stay in the rule, or should it move into software?

If that question is answered badly, the repository often gets worse in two ways at once:

- rules become hard to review
- helper code becomes hard to trust

This page is about drawing that line well.

## How to use this page

Read this page with one long rule from your own repository or from the capstone open
beside you.

Do not read it as advice to "make rules shorter." Read it as training for one specific
judgment:

> which parts of this step are the public workflow contract, and which parts are merely the implementation behind that contract?

By the end of the page you should be able to mark a rule in three colors:

- what must stay visible in the rule
- what can move into `workflow/scripts/`
- what deserves promotion into reusable package code

## Start with the rule as a public contract

A Snakemake rule is strongest when it makes these things explicit:

- declared inputs and outputs
- parameters that affect file meaning
- resource claims
- the execution boundary for one step

That is orchestration.

Once a rule starts containing large parsing logic, data transformation logic, or report
generation logic, it is often becoming the least testable program in the repository.

That is the warning sign: the repository now contains software, but it is trying to hide
that fact inside orchestration.

## What usually belongs in each home

Use this table before you move anything:

| Keep it here | When it belongs here | What the learner should be able to say |
| --- | --- | --- |
| rule body | the file contract, resource claim, parameter surface, and small obvious glue still read clearly | this step reads these declared files, writes these outputs, and reruns when these declared conditions change |
| `workflow/scripts/` | one step needs non-trivial implementation that is still tightly coupled to that step | the workflow still owns the contract, but this step now has a real program behind it |
| `src/` package code | logic is reusable, importable, and worth direct tests outside Snakemake | this is part of the repository's software layer, not only workflow glue |

If you cannot explain the ownership in one sentence, do not move the code yet.

## What belongs comfortably in a rule

Rules are a good home for:

- short shell commands whose meaning is still obvious
- small glue logic that keeps the file contract readable
- explicit parameter passing into an external command or script

The important part is that a reviewer can still explain:

- what files this rule reads
- what files it writes
- what change would make it rerun

If that explanation becomes cloudy, the boundary is already weakening.

## What usually belongs in a script or package

Move logic out of the rule when it becomes:

- non-trivial data transformation
- reusable domain logic
- logic that deserves direct tests outside Snakemake
- code whose readability would improve if treated like a normal program

That is why the capstone keeps reusable processing code under `src/capstone/` and leaves
workflow-adjacent metadata generation in `workflow/scripts/`.

The rule should still own the file contract even when the implementation moves.

## One useful split

```mermaid
flowchart LR
  rule["Snakemake rule"] --> contract["declared files, params, logs, resources"]
  contract --> script["workflow/scripts step implementation"]
  contract --> package["src package reusable logic"]
  script --> output["produced artifact"]
  package --> output
```

This picture matters because the rule is not replaced. It remains the place where the
file contract stays visible.

The script or package owns implementation, not workflow meaning by itself.

## A concrete decomposition exercise

Imagine a long `run:` block that does all of this:

- opens the declared input file
- validates required columns
- normalizes field names
- computes summary statistics
- writes the final report
- imports a helper that another rule also wants to use

Do not ask only, "Can I move this to a script?"

Ask these better questions:

1. Which lines express the visible file contract and therefore must remain obvious from the rule?
2. Which lines are step-local implementation and can safely live in `workflow/scripts/`?
3. Which lines are no longer really about this one step and should become reusable package code?

That sequence prevents two common mistakes:

- leaving real software trapped in a rule forever
- moving everything out of the rule until the rule stops explaining the workflow

## A weak first draft

Weak shape:

```python
rule summarize:
    input:
        "results/raw.json"
    output:
        "publish/v1/summary.json"
    run:
        import json
        data = json.load(open(input[0]))
        # many lines of transformation and formatting logic here
        ...
```

This may work. It creates two problems:

- the rule body becomes the hidden implementation layer
- the logic is harder to test outside a workflow run

The repository now has software; it is just pretending it does not.

## A stronger rewrite

Stronger shape:

```python
rule summarize:
    input:
        "results/raw.json"
    output:
        "publish/v1/summary.json"
    script:
        "workflow/scripts/summarize.py"
```

Or, when the logic is reusable:

```python
rule summarize:
    input:
        "results/raw.json"
    output:
        "publish/v1/summary.json"
    shell:
        "python -m capstone.summarize --input {input} --output {output}"
```

This improves the repository only if the rule still tells the file story clearly and the
software boundary is explicit.

## `script:` and package code solve different problems

`script:` is a good fit when:

- the code is workflow-adjacent
- the logic is meaningful but still closely tied to one orchestration step

Package code under `src/` is a better fit when:

- the logic is reusable across steps
- it deserves direct tests and imports
- it is real implementation code, not only glue

The difference is not prestige. It is ownership.

## A review conversation you should be able to have

The goal is not only to move code. The goal is to defend the movement in review.

Here is the kind of explanation a strong learner should be able to give:

> The rule still owns the declared files, parameters, log path, and runtime choice. I moved the transformation loop into `workflow/scripts/` because it became step-local program logic that deserves normal code structure. I moved the shared parser into `src/` because two rules need it and it should be tested directly without a Snakemake context.

That explanation is better than "the rule looked messy" because it teaches another reader
how the repository is organized.

## Common failure modes

| Failure mode | What it looks like | Better repair |
| --- | --- | --- |
| giant `run:` block | rule files become the least reviewed programs in the repo | move non-trivial logic into script or package code |
| script hides undeclared file reads | the rule contract looks smaller than the real behavior | keep all meaningful file dependencies visible in the rule |
| package code changes workflow meaning silently | helpers become a second hidden workflow | keep the rule as the visible contract boundary |
| shell fragments turn into mini applications | debugging and testing stay trapped inside Snakemake runs | promote real program logic into software surfaces |
| everything is moved to helper code reflexively | rules stop explaining the workflow | leave simple orchestration in the rule where it belongs |

## The beginner mistake to catch early

Many beginners hear "separate concerns" and immediately move almost everything out of the
rule.

That is not mature structure. That is often just invisible structure.

If a rule no longer makes it easy to answer:

- what enters this step
- what leaves this step
- what parameter changes matter
- what runtime this step assumes

then the workflow boundary has been over-compressed.

## The explanation a reviewer trusts

Strong explanation:

> this rule still owns the file contract, but the transformation logic moved into
> `workflow/scripts/` because it became real program logic; the repository now keeps the
> workflow story visible in the rule and the implementation testable in code.

Weak explanation:

> we moved it to a script because the rule looked messy.

The first explanation gives an ownership reason. The second gives only a cleanliness
reaction.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain one case where logic should stay in a rule
- explain one case where logic should move into a script
- explain one case where logic belongs in package code under `src/`
- describe why moving code out of a rule does not remove the rule’s ownership of the file contract

If you still describe the decision mainly as "shorter versus longer," read the page once
more. The real distinction is public contract versus owned implementation.
