# Worked Example: Investigating a Slow and Noisy Workflow

This example shows how Module 09 fits together when a workflow starts feeling wrong under
real pressure.

The point is not to memorize this exact story. The point is to see a calm route from
symptom to explanation.

## The situation

A maintainer reports:

> CI is much slower than last week, `make tour` feels noisy, and the publish summary was
> rebuilt for every sample even though we only changed one helper script.

That report contains three different concerns:

- slower execution
- noisier evidence
- surprising rebuild scope

A weak response would jump straight to retries, threads, or job grouping.

Instead, start with the Module 09 ladder.

## Step 1: Name the symptom

The incident note becomes:

> `make tour` now takes roughly twice as long in CI. The publish summary and report were
> rebuilt for all samples. The maintainer also reports much noisier execution logs than the
> last reviewed run.

That is already better than "the workflow got weird."

## Step 2: Check planned work before real execution

Run:

```bash
snakemake -n -p
snakemake --summary
snakemake --list-changes input code params
```

What you learn:

- dry-run plans far more per-sample jobs than expected
- `--summary` confirms that summary-oriented outputs are stale because many upstream sample
  outputs are now considered missing or changed
- `--list-changes` points mostly to input and code changes rather than parameter drift

That is the first big clue.

The workflow is not only slow. It is planning more work.

## Step 3: Separate cost classes

At this point, do not say "the tools got slower."

Nothing yet suggests that.

The likely dominant cost class is now:

- planning and discovery, because the workflow scope widened
- scheduler overhead, because the widened scope creates many more short jobs

Tool runtime is still only a possibility, not the current lead explanation.

## Step 4: Open the narrowest evidence surfaces

Now inspect:

- one benchmark file from the previously suspicious rule family
- one log file from a sample that should not have changed
- the discovery artifact that lists which samples were found

The benchmarks show that rule runtime per sample is almost unchanged.

The logs show many jobs running on sample names that look wrong:

- expected names such as `sampleA`
- unexpected names such as `sampleA.fastq.gz.md5`

That is the second big clue.

The workflow did not mostly get slower because the tools changed. It got slower because
discovery widened and created extra tiny jobs.

## Step 5: Find the boundary that moved

A recent helper edit changed sample discovery from a tight file pattern to a broader glob.

The repository now treats checksum sidecars as if they were real samples.

That causes three visible effects:

1. dry-run plans many extra jobs
2. scheduler overhead rises because most of those jobs are tiny
3. logs become noisy because rule-local messages now mention invalid sample identities

This is a strong example of why performance and observability are connected.

The performance symptom came from a workflow-semantics mistake, and the noisy evidence came
from the same mistake.

## Step 6: Repair the right thing

The honest repair is not:

- add more cores
- raise retries
- delete noisy logs
- group the jobs and hope the problem becomes less visible

The honest repair is:

- restore a reviewed sample-discovery rule
- make the discovered sample list easy to inspect
- keep the log and benchmark surfaces tied to valid sample identities

Only after that repair should you reconsider whether any remaining speed issue is still
worth tuning.

## Step 7: Prove the repair honestly

Use the same route again:

```bash
snakemake -n -p
snakemake --summary
make -C capstone evidence-summary
make -C capstone tour
```

What you want to see:

- dry-run target count falls back to the expected range
- `--summary` stops showing unnecessary rebuild scope
- evidence becomes quieter because it now reflects real sample identities
- the run time improves without any semantic shortcuts

## What this example teaches

This incident matters because it is easy to misread.

A rushed maintainer could easily conclude:

- CI needs more resources
- Snakemake scheduling is inefficient
- the logs are too verbose

Those claims all point away from the root problem.

The real issue was a widened discovery boundary that created false work and false noise.

## The review note you would want in the pull request

> The slowdown was not primarily tool runtime. Dry-run and summary evidence showed that the
> workflow had started planning extra jobs after sample discovery widened to include
> checksum sidecars. Benchmarks for valid samples stayed close to their previous timings,
> which argues against a tool-level regression. The repair restores a reviewed discovery
> pattern and keeps the discovered sample list inspectable. Speed improved because the
> extra work disappeared, not because the workflow was taught to skip truth.

That is the standard this module is aiming for.

## Why this is a mastery example

This one story exercises all five cores:

- Core 1: cost classes were separated before tuning
- Core 2: the right evidence surfaces were chosen in order
- Core 3: the incident ladder prevented random edits
- Core 4: the repair preserved workflow semantics
- Core 5: the route is short enough to become a runbook entry
