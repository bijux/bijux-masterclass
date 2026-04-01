# Workflow Tour

This tour is the learner-facing entrypoint for the Snakemake capstone. It creates a proof
bundle under `artifacts/workflow-tour/` so you can inspect the workflow the same way the
course asks you to reason about it: through declared rules, planned jobs, published outputs,
and summary evidence.

## What the tour produces

- `list-rules.txt`: the public rule surface exposed by the workflow
- `dryrun.txt`: the planned jobs and commands without executing them
- `run.txt`: the execution log from the real workflow run
- `summary.txt`: Snakemake’s summary view after the run
- `manifest.json`: the stable publish boundary inventory
- `provenance.json`: the reproducibility record for the run
- `FILE_API.md`: the documented publish contract copied into the bundle

## How to use it

From the capstone directory:

```bash
make tour
```

From the repository root:

```bash
make PROGRAM=reproducible-research/deep-dive-snakemake capstone-tour
```

## What to inspect first

1. `list-rules.txt`
2. `dryrun.txt`
3. `summary.txt`
4. `manifest.json`
5. `provenance.json`

That order mirrors the course: rule surface, planned DAG, resulting evidence, published interface, and reproducibility metadata.
