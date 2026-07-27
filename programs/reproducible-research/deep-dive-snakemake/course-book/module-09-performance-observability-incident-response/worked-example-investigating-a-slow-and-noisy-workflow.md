# Worked Example: Investigating a Slow and Noisy Workflow

This file ties the whole module together around one realistic problem:

> a workflow still runs, but maintainers now describe it as slow, noisy, and unpredictable under review pressure.

The question is not "how do we make it feel faster?" The question is how to move from
symptom to explanation without losing workflow truth.

## The lab route

Work through the example in this order:

1. write down the symptom precisely
2. separate likely cost classes before touching configuration
3. inspect the narrowest evidence surfaces in order
4. repair the boundary that actually moved
5. prove the repair with the same route and turn it into a runbook

## The starting situation

Assume a maintainer reports:

> CI is much slower than last week, `make tour` feels noisy, and the publish summary was rebuilt for every sample even though only one helper changed.

That report already contains three concerns:

- slower execution
- noisier evidence
- surprising rebuild scope

A weak response would jump straight to more threads, more retries, or job grouping. The
stronger response begins by classifying what kind of problem this might be.

## Name the symptom precisely

Rewrite the incident note into something reviewable:

> `make tour` now takes roughly twice as long in CI. Summary-oriented publish artifacts
> were rebuilt for all samples. Execution logs are much noisier than the last reviewed
> run.

That is already better than “the workflow got weird.”

## Separate the likely cost classes

Now inspect:

```bash
snakemake -n -p
snakemake --summary
snakemake --list-changes input code params
```

Suppose you learn:

- dry-run now plans far more per-sample jobs than expected
- `--summary` shows many summary outputs as stale because more upstream sample surfaces changed
- `--list-changes` points mostly to input and code movement rather than parameter drift

That suggests the dominant cost class is not yet tool runtime. The stronger lead is that
the workflow is planning more work than before, which may also amplify scheduler or launch
overhead.

## Open the narrowest evidence surfaces

Now inspect:

- one benchmark file from the previously suspicious rule family
- one log file from a sample that should not have changed
- the discovery artifact listing which samples were found

Suppose the benchmarks show per-sample runtime is almost unchanged, while the discovery
artifact and logs reveal unexpected sample identities such as checksum sidecars.

That is the second big clue. The workflow did not mostly get slower because the tools
changed. It got slower because the repository widened discovery and created false work and
false noise.

## Repair the boundary that actually moved

The honest repair is not:

- add more cores
- raise retries
- hide the logs
- group the jobs until the problem looks smaller

The honest repair is:

- restore a reviewed discovery boundary
- keep the discovered sample list easy to inspect
- ensure logs and benchmarks correspond only to valid sample identities

Only after that repair should you ask whether any remaining speed issue is still worth
tuning.

## Prove the repair honestly

Use the same route again:

```bash
snakemake -n -p
snakemake --summary
make -C capstone evidence-summary
make -C capstone tour
```

What you want to see:

- dry-run target count falls back to the expected range
- summary evidence stops showing unnecessary rebuild scope
- logs become quieter because they now reflect real sample identities
- runtime improves because false work disappeared, not because truth was skipped

## Turn the route into a reusable incident note

Now record the route so another maintainer can follow it later:

1. capture the symptom in concrete terms
2. separate planning, execution, and rebuild evidence
3. inspect benchmarks and logs only after the planning surface is clear
4. repair the semantic boundary first
5. rerun the same proof route after the change

That turns one incident from private intuition into reusable repository knowledge.

## The repaired incident story

By the end of the investigation, the workflow can be described cleanly:

1. the slowdown started with widened discovery, not slower tools
2. extra jobs created extra scheduler overhead and extra log noise
3. the repair restored a reviewed discovery boundary
4. the proof route showed improvement without semantic shortcuts
5. the incident note became a usable runbook entry

That is what it means to investigate a slow and noisy workflow honestly.

## Review questions for the repaired design

When you inspect an incident route shaped like this, ask:

1. which cost class was named first and why
2. which evidence surface ruled out a tool-level slowdown
3. which workflow boundary actually moved
4. how the repair preserved workflow meaning
5. whether another maintainer could follow the route without extra oral guidance

If those answers are visible, the module’s incident story has landed.
