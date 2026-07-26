# Worked Example: Making Checkpoint Discovery Reviewable

This file pulls the whole module together around one realistic question:

> how do you let a workflow discover samples from `data/raw/` without turning the DAG into a moving target?

The example stays small on purpose. The point is to make the design visible and to show
why a checkpoint is usually the fourth move, not the first.

## The lab route

Work through the example in this order:

1. inspect the weak draft and name the hidden discovery assumptions
2. repair the workflow with a declared candidate set first
3. narrow the output family before you add more dynamism
4. introduce a checkpoint only when runtime validation really changes the usable set
5. carry the accepted set into the publish boundary

## The scenario

Assume a workflow that should:

1. inspect `data/raw/` for FASTQ files
2. discover which samples exist
3. run one QC job per sample
4. publish a reviewed boundary that keeps the discovered set visible

That sounds ordinary. It still creates most of the mistakes people make with dynamic
Snakemake workflows.

## The weak first draft

```python
from pathlib import Path

SAMPLES = [path.stem for path in Path("data/raw").glob("*.fastq.gz")]

rule all:
    input:
        expand("results/{sample}.json", sample=SAMPLES)

rule qc:
    input:
        "data/raw/{sample}.fastq.gz"
    output:
        "results/{sample}.json"
    shell:
        "python scripts/qc.py --input {input} --output {output}"
```

This draft is small, but it already teaches four bad lessons:

- discovery is an implicit parse-time scan with weak normalization
- output naming is too broad to carry more artifact families safely
- nothing records the discovered sample set for review
- the publish boundary has not been separated from internal execution state

The code works only if you avoid asking serious questions.

## Prefer a declared candidate set

The first repair is not a checkpoint. The first repair is to replace ambient directory
state with a declared candidate set. A small `config/samples.tsv` can say:

```text
sample	path
A	data/raw/A.fastq.gz
B	data/raw/B.fastq.gz
```

Load, validate, and sort those records once near the top of the Snakefile. The concrete
input paths can then drive ordinary static expansion:

```python
import csv

with open("config/samples.tsv", encoding="utf-8", newline="") as handle:
    RECORDS = sorted(csv.DictReader(handle, delimiter="\t"), key=lambda row: row["sample"])

SAMPLES = [record["sample"] for record in RECORDS]
SOURCE_BY_SAMPLE = {record["sample"]: record["path"] for record in RECORDS}
```

This changes the conversation immediately.

Now the workflow can answer:

- which samples were candidates
- which path belongs to each sample
- which version-controlled record defines the target set

If that is all the workflow needs, stop here. Adding a checkpoint would make a known
target set harder to reason about.

That pause matters. More dynamic is not automatically more advanced.

## Narrow the artifact family

The original output shape was:

```python
"results/{sample}.json"
```

That path does not teach enough. It will become confusing the moment you add another JSON
artifact family.

A better shape is:

```python
"results/{sample}/qc.json"
```

Now the workflow has:

- one place for sample identity
- one place for artifact identity
- room to grow into `kmer.json`, `screen.json`, or `summary.json` later

That is Core 2 in action: the wildcard owns a narrow, reviewable domain.

## Introduce a checkpoint only when execution reveals a new fact

Suppose a validation tool must read each candidate file and only non-empty, structurally
valid samples may continue. The usable subset cannot be known until that tool executes.
Now a checkpoint earns its place because runtime work reveals a new target domain.

```python
checkpoint validate_candidates:
    input:
        lambda wildcards: [SOURCE_BY_SAMPLE[sample] for sample in SAMPLES]
    output:
        directory("results/discovery")
    run:
        import json
        from pathlib import Path

        outdir = Path(output[0])
        outdir.mkdir(parents=True, exist_ok=True)
        samples = sorted(
            sample
            for sample, source in SOURCE_BY_SAMPLE.items()
            if Path(source).stat().st_size > 0
        )
        (outdir / "samples.json").write_text(
            json.dumps({"samples": samples}, indent=2) + "\n",
            encoding="utf-8",
        )


def qc_targets(_wildcards):
    import json
    from pathlib import Path

    checkpoint_job = checkpoints.validate_candidates.get()
    registry = Path(checkpoint_job.output[0]) / "samples.json"
    samples = json.loads(registry.read_text(encoding="utf-8"))["samples"]
    return expand("results/{sample}/qc.json", sample=samples)


rule all:
    input:
        qc_targets
```

The checkpoint is justified here because the downstream target set genuinely depends on
the validation result. In a real workflow, replace the non-empty-file demonstration with
a domain validator and record rejection reasons as well as accepted samples.

The important part is not the keyword `checkpoint`. The important part is that the
discovered set is written once and reused.

## What to check before moving on

After the checkpoint version works, confirm all of these:

- the declared candidate set is still visible
- the accepted registry is a deterministic function of declared inputs
- downstream fanout reads the registry instead of the raw directory
- a rejected candidate leaves reviewable evidence instead of disappearing silently

## Keep discovery visible at the publish boundary

Now imagine the workflow publishes a versioned result bundle.

Weak shape:

- publish only the per-sample QC outputs
- drop the discovery registry entirely

That leaves a downstream reviewer asking:

- why do these exact sample outputs exist
- which sample set drove the DAG
- whether the run discovered something different from yesterday

Stronger shape:

```text
publish/v1/
  discovered_samples.json
  summary.json
  provenance.json
  manifest.json
```

This is Core 4: discovery should remain legible when the workflow crosses into public
contract space.

## Avoid accidental operational drag

Even a correct design can become awkward if it creates too much setup cost.

Two easy repairs help here:

- keep one shared environment for the QC and summary rules if they truly use the same toolchain
- process one sample per job instead of splitting into many trivial fragment jobs without a real need

That is Core 5: improve speed by repairing boundaries and granularity, not by hiding
truth.

## The repaired module story

By the end of the repairs, the workflow can be described cleanly:

1. raw files in `data/raw/` are the declared discovery surface
2. discovery writes one durable registry
3. downstream fanout reads that registry
4. per-sample outputs live under narrow, predictable paths
5. the publish boundary carries forward the discovery and provenance needed for review

That is what Module 02 means by a dynamic DAG you can trust.

## Review questions for the repaired design

When you inspect a workflow shaped like this, ask:

1. where is the discovered set recorded
2. which downstream rule reads that exact record
3. which paths belong to the public boundary
4. what part of the workflow proves the sample set was deterministic
5. what environment or job-shape choices keep the workflow practical to run

If those answers are visible, the workflow is no longer relying on magic.
