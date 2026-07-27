# Exercise Answers

Use this page after you have written your own answers. The value is in comparing reasoning,
not in copying wording.

## How to use the answer page well

Do not read an answer first and then reverse-engineer your exercise around it.

A better sequence is:

1. complete the exercise with your own files and commands
2. write one plain-language explanation
3. compare your reasoning with the model answer
4. revise the explanation if the model answer exposes a gap

The goal is not identical wording. The goal is honest workflow reasoning.

The answers below are model answers. Your filenames and rule names may differ. What should
stay stable is the shape of the explanation:

- start from the target and file contract
- use one piece of workflow evidence
- explain the repair in terms of truth, ownership, or publication

The strongest self-study packets also leave behind six concrete artifacts:

- one prediction note
- one DAG or rulegraph snapshot
- one convergence check
- one wildcard-ownership note
- one publication-safety note
- one meaning-versus-policy review note

If your answers contain only commands and outcomes, the reasoning is still too thin.

## Exercise 1: Explain why one rule does not run

A strong answer sounds like this:

> The requested target is `results/final.txt`. That file is produced by `producer`, so
> Snakemake schedules `producer` and `all`. The extra rule `never_called` publishes
> `results/ghost.txt`, but no requested target depends on that file, so it has no place in
> the current DAG. A dry-run proves this because `never_called` does not appear in the job
> list.

Why this is strong:

- it starts from the requested target
- it names the matching output contract
- it treats the missing rule as irrelevant to the target graph, not as a mystery

Weak answers usually say only "Snakemake skipped the rule."

## Exercise 2: Prove convergence on purpose

A strong answer proves that a successful run settles down.

Example answer shape:

- run `snakemake`
- then run `snakemake -n`
- expected evidence: "Nothing to be done."
- explanation:
  - "the workflow converges because the declared inputs, outputs, and tracked rule meaning
    have not changed since the successful run"

Why this is strong:

- it uses the dry-run as evidence instead of treating convergence as a feeling
- it explains why no additional work is justified

The missing but important sentence is usually this one:

> The second dry-run is quiet because the declared inputs, outputs, and tracked rule
> meaning are the same facts the successful run already satisfied.

## Exercise 3: Trigger one selective rebuild

A strong answer keeps the explanation tied to dependency edges.

Example:

> After editing `data/B.txt`, the dry-run schedules only the job that publishes
> `results/B.upper.txt` plus any downstream target that depends on it. `results/A.upper.txt`
> stays untouched because the changed file is not one of its ancestors in the DAG.

Why this is strong:

- it explains the rebuild from the changed input backward
- it avoids the false idea that rule order controls rebuilds

## Exercise 4: Break convergence and repair it

A strong answer shows both the defect and the repair.

Example answer shape:

- broken state:
  - add a changing tracked value such as `time.time()` in `params`
  - rerun `snakemake -n`
  - expected evidence: the rule is planned again
- explanation:
  - "the tracked rule meaning changes each parse because the parameter is not stable"
- repair:
  - "remove the unstable value from the rule meaning or move a stable version of it into
    config"

Why this is strong:

- it identifies unstable meaning as the cause
- it proves the repair by restoring convergence

## Exercise 5: Diagnose one wildcard ownership problem

A strong answer names the ownership defect directly.

Example:

> The output pattern `results/{x}.txt` is too broad because both `r1` and `r2` can claim
> `results/test.txt`. The issue is not merely a brace problem; it is ambiguous file
> ownership. I would redesign the paths so the rules publish different artifact families,
> such as `results/report/{x}.txt` and `results/qc/{x}.txt`. A dry-run or rule graph then
> shows one clear owner per output family.

Why this is strong:

- it identifies ambiguity as a file-ownership problem
- it fixes the path design instead of hiding the issue with precedence tricks

## Exercise 6: Repair a poison output

A strong answer contrasts the broken and repaired publication contracts.

Example:

- broken shape:
  - the rule writes directly to `results/report.txt` and then exits with failure
- repaired shape:
  - write to `results/report.txt.tmp`
  - rename to `results/report.txt` only after success
- evidence route:
  - keep a per-job log such as `logs/report.log`
- explanation:
  - "the repaired version is safer because downstream users either see a complete final
    output or no final output at all"

Why this is strong:

- it explains publication trust, not just shell mechanics
- it leaves behind evidence for the next investigation

The key explanatory sentence is:

> The final path becomes trustworthy only after the temporary output is fully written and
> atomically promoted into its declared location.

## Exercise 7: Separate workflow meaning from execution policy

A strong answer shows one value on each side of the boundary.

Example:

- config value:
  - `samples: [A, B]`
  - reason: changing it changes which outputs the workflow is supposed to build
- profile value:
  - `cores: 4`
  - reason: changing it alters execution behavior, not the meaning of results
- validation example:
  - "a schema would catch a misspelled required key like `samplez` before any job runs"
- review explanation:
  - "the split makes it easier to review whether a change alters workflow meaning or only
    the operating context"

Why this is strong:

- it makes the semantic-versus-policy split explicit
- it shows why early validation is humane, not just formal

## Exercise 8: Compare a plan with execution

After deleting `results/A.upper.txt`, a dry-run should plan only the `uppercase` job for
sample `A` plus the target aggregation. It says what Snakemake *would* do from the current
filesystem state. After execution, `--summary` should report the known outputs as current.
That summary describes file ownership and status; it is not a record that every planned
shell command succeeded in some earlier run.

## Exercise 9: Investigate a missing input

If the requested target is `results/C.upper.txt`, Snakemake can infer `sample=C` and then
requires `data/C.txt`. The error is useful evidence: the output pattern matched, but its
source contract could not be satisfied. Add the source if `C` is a legitimate sample,
remove `C` from semantic configuration if it is not, or correct the path contract if the
source lives elsewhere. Creating an empty file merely to silence the error would hide the
real defect.

## Exercise 10: Complete a trustworthy tiny project

A strong project has three explicit source records, one wildcard transformation family,
and one summary rule. `rule all` requests the summary and any intermediate files that are
intended deliverables. The summary writes to a sibling temporary path and renames only
after every row is complete. Logs are separate from published data.

Verification should show:

- the first dry-run plans three transformations and one summary
- the first execution creates all expected files
- the next dry-run converges
- changing one source rebuilds its transformation and the dependent summary
- an injected summary failure leaves no final partial file

The final review should classify sample membership and transformation parameters as
workflow meaning, while cores and shell-printing behavior remain execution policy.

The strongest answers also say explicitly why that split matters:

> A reviewer can decide whether a change alters intended outputs or only operating context
> without reverse-engineering the whole workflow.

## What all ten answers should have in common

The best Module 01 answers usually do five things:

1. they explain behavior from the target surface backward
2. they point to a concrete evidence route such as `-n`, `--summary`, `--rulegraph`, or a
   per-job log
3. they distinguish tracked meaning from hidden or unstable state
4. they treat wildcard problems as ownership problems
5. they treat final outputs as published artifacts that must be trustworthy

If your answers do those five things, you are learning the module in the right direction.

Weak answer pattern:

- "I ran the commands, the files appeared, so the workflow is probably fine"

That sentence skips convergence, ownership, and publication trust all at once. If your
answers still sound like that, keep revising.
