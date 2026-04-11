# Exercise Answers

Use this page after you have written your own answers. The value is in comparing reasoning,
not in copying wording.

The answers below are model answers. Your filenames and rule names may differ. What should
stay stable is the shape of the explanation:

- start from the target and file contract
- use one piece of workflow evidence
- explain the repair in terms of truth, ownership, or publication

## Answer 1: Explain why one rule does not run

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

## Answer 2: Prove convergence and then break it

A strong answer shows both states clearly.

Example answer shape:

- converging state:
  - run `snakemake`
  - then run `snakemake -n`
  - expected evidence: "Nothing to be done."
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

- it proves both behaviors with the same evidence route
- it explains non-convergence as unstable tracked meaning rather than as random behavior

## Answer 3: Diagnose one wildcard ownership problem

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

## Answer 4: Separate workflow meaning from execution policy

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

## Answer 5: Repair a poison output

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

## What all five answers should have in common

The best Module 01 answers usually do five things:

1. they explain behavior from the target surface backward
2. they point to a concrete evidence route such as `-n`, `--summary`, `--rulegraph`, or a
   per-job log
3. they distinguish tracked meaning from hidden or unstable state
4. they treat wildcard problems as ownership problems
5. they treat final outputs as published artifacts that must be trustworthy

If your answers do those five things, you are learning the module in the right direction.
