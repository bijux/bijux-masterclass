# Worked Example: Repairing a Lying First Workflow
This example is the lab version of Module 01. Do not read it like a post-mortem. Rebuild
it as you go and predict each change before you run it.

The goal is to take one small workflow from misleading first draft to a version that tells
the truth about files, reruns, wildcard ownership, and published outputs.

## How to use this worked example

Treat this page like a bench exercise, not like a story you admire from a distance.

For each repair step:

1. predict what Snakemake should do next
2. run the smallest command that tests that prediction
3. write one sentence about what changed in the workflow truth

If you skip the prediction step, the example becomes reading practice instead of workflow
reasoning practice.

## The one-day teaching goal

By the end of this example, a missed class session should still feel recoverable. The
reader should be able to rebuild a tiny workflow from scratch and explain:

- why one rule is irrelevant to the requested target
- why one unstable value prevents convergence
- why one output pattern teaches ownership badly
- why one final output is unsafe to publish directly

That is the real point of the example. The code is only the vehicle.

## Build an honest baseline first

Before repairing a larger workflow, make the smallest multi-job graph concrete. Continue
in the orientation directory and replace its `Snakefile` with:

```python
SAMPLES = ["A", "B"]


rule all:
    input:
        expand("results/{sample}.upper.txt", sample=SAMPLES)


rule uppercase:
    input:
        "data/{sample}.txt"
    output:
        "results/{sample}.upper.txt"
    shell:
        """
        mkdir -p results
        tr '[:lower:]' '[:upper:]' < {input} > {output}.building
        mv {output}.building {output}
        """
```

Create the inputs and inspect the plan:

```sh
mkdir -p data
printf 'alpha\n' > data/A.txt
printf 'beta\n' > data/B.txt
snakemake --dry-run --printshellcmds
```

One rule definition becomes two jobs because the concrete targets bind `{sample}` to
`A` and `B`. Execute with `snakemake --cores 1`, then edit only `data/A.txt` and dry-run
again. Predict that only the `A` job will run. This small observation is the foundation
for the repair below.

## What to keep beside you while you work

Keep four evidence routes open all the way through the page:

- `snakemake -n`
- `snakemake --summary`
- the current `Snakefile`
- the actual output paths on disk

Those four surfaces are enough to teach the lesson if you read them carefully.

## The lab route

Use the worked example in this order:

1. build the honest baseline and prove selective rebuilds
2. read the broken first draft and predict where it lies
3. repair one defect at a time
4. dry-run after every repair instead of waiting until the end
5. finish with one output you would trust another rule to consume

## The situation

Assume you are building a tiny workflow over two text files:

- `data/A.txt`
- `data/B.txt`

The intended goal is simple:

1. uppercase each file
2. summarize the line counts
3. treat the summary as the main finished result

This sounds like an easy first Snakemake exercise. It is also exactly the kind of exercise
where beginners accidentally build a workflow that looks fine while teaching bad habits.

## The first draft

You write this:

```python
import time

SAMPLES = ["A", "B"]

rule all:
    input:
        "results/summary.txt"

rule prepare:
    output:
        "results/ready.flag"
    shell:
        r"""
        mkdir -p results staged
        echo ready > {output}
        """

rule upper:
    input:
        "data/{sample}.txt"
    output:
        "staged/{sample}.txt"
    shell:
        r"""
        tr '[:lower:]' '[:upper:]' < {input} > {output}
        """

rule summarize:
    input:
        expand("staged/{sample}.txt", sample=SAMPLES)
    output:
        "results/summary.txt"
    params:
        stamp=lambda: time.time()
    shell:
        r"""
        echo "built_at={params.stamp}" > {output}
        wc -l {input} >> {output}
        """
```

At first glance this looks reasonable. It has a default target, a helper rule, a wildcard
rule, and a summary.

It is still lying in several ways.

## What is wrong with it

The first draft has at least five issues:

1. `prepare` never runs because nothing depends on `results/ready.flag`.
2. `staged/{sample}.txt` is a vague output family with no artifact-specific naming.
3. `summarize` embeds a time-based parameter, so the workflow will not converge.
4. `summary.txt` is written directly in place, so failure could leave poison.
5. there are no per-job logs, so failures are harder to inspect.

That is a good Module 01 example because none of these problems are exotic.

## Repair order matters

Do not fix the shell first just because it looks concrete. Repair the workflow in this
order:

1. remove rules that are outside the target story
2. restore convergence
3. make output ownership easier to read
4. add logs and atomic publication

That order keeps the lesson tied to workflow truth instead of drifting straight into
implementation details.

## Why this order matters educationally

Beginners often grab the shell block first because it looks concrete. That produces a bad
habit: polishing commands before deciding whether the workflow graph says anything true.

This repair order forces a stronger instinct:

- first make the target story honest
- then make reruns explainable
- then tighten path ownership
- only then improve publication safety and diagnostics

## Review the target story

The first question is not "how do I fix the shell?"

The first question is:

> what outputs are supposed to count as finished results?

Right now `rule all` says the finished result is `results/summary.txt`.

That means `prepare` is outside the real target story unless its output becomes part of an
explicit input chain.

This is Core 1 in action. You realize:

- `prepare` is not "forgotten by Snakemake"
- it is irrelevant to the requested target

The honest repair is either:

- remove `prepare` entirely
- or make a real downstream edge depend on it

In this example, the right answer is removal. The flag is not real workflow truth.

## Remove the unstable rerun cause

You then run:

```bash
snakemake
snakemake -n
```

and notice that the dry-run still wants to execute `summarize`.

The reason is not mysterious:

- `params.stamp` changes every parse
- the rule meaning is unstable
- the workflow cannot converge

This is Core 2.

The repair is to remove the unstable time value from the rule's meaning. If you
actually need a run identifier, it should be an explicit stable config value or sidecar
audit artifact, not part of the summary's semantic content.

## A short checkpoint before moving on

Pause here and verify that you can say the problem in one sentence without mentioning
"Snakemake weirdness."

Strong sentence:

> The summary rule reruns because its tracked meaning changes every parse.

Weak sentence:

> It keeps running again for some reason.

## Make the wildcard output teach the reader

The next issue is the staging path:

```python
"staged/{sample}.txt"
```

This path is not wrong, but it is weak:

- it does not say this is an uppercased artifact
- it is easy to collide with other staged text outputs later
- it does not teach the reader enough about ownership

A stronger path is:

```python
"results/staged/{sample}.upper.txt"
```

This is Core 3:

- the directory says the artifact family
- the suffix says the artifact kind
- the wildcard has one clear role

The fix is not about pretty naming only. It is about path precision and future ambiguity
avoidance.

## Separate meaning from policy

Suppose you now want to make the sample list configurable.

A weak move would be putting samples into a profile.

A stronger move is:

**`config/config.yaml`**

```yaml
samples:
  - A
  - B
```

**`profiles/default/config.yaml`**

```yaml
cores: 2
printshellcmds: true
rerun-incomplete: true
```

Then the Snakefile can read:

```python
from snakemake.utils import validate

configfile: "config/config.yaml"
validate(config, "config/schema.yaml")

SAMPLES = config["samples"]
```

This is Core 4. You now have a clean story:

- config changes workflow meaning
- profile changes execution behavior

If this still feels abstract, change `samples` and `cores` one at a time and predict which
change should alter the target surface. That comparison usually makes the boundary click.

## Repair publication and failure evidence

You also notice that the summary rule writes directly to the final output.

That means a failure could leave a half-written `results/summary/counts.tsv`.

The repair is the Module 01 publication pattern:

- write to a temp sibling
- rename only when complete
- add per-job logs

So the repaired summary rule becomes closer to:

```python
rule summarize_counts:
    input:
        expand("results/staged/{sample}.upper.txt", sample=SAMPLES)
    output:
        "results/summary/counts.tsv"
    log:
        "logs/summarize.log"
    shell:
        r"""
        set -euo pipefail
        mkdir -p results/summary logs
        tmp="{output}.tmp"
        printf "sample\tlines\n" > "$tmp"
        for f in {input}; do
          s="$(basename "$f" .upper.txt)"
          n="$(wc -l < "$f" | tr -d ' ')"
          printf "%s\t%s\n" "$s" "$n" >> "$tmp"
        done 2> {log}
        mv -f "$tmp" {output}
        """
```

This is Core 5:

- final output is complete or absent
- failure has a log
- the publication point is explicit

## The repaired workflow

After the fixes, you have something much healthier:

```python
from snakemake.utils import validate

configfile: "config/config.yaml"
validate(config, "config/schema.yaml")

SAMPLES = config["samples"]

rule all:
    input:
        "results/summary/counts.tsv",
        expand("results/staged/{sample}.upper.txt", sample=SAMPLES)

rule stage_upper:
    input:
        "data/{sample}.txt"
    output:
        "results/staged/{sample}.upper.txt"
    log:
        "logs/stage/{sample}.log"
    shell:
        r"""
        set -euo pipefail
        mkdir -p results/staged logs/stage
        tmp="{output}.tmp"
        tr '[:lower:]' '[:upper:]' < {input} > "$tmp" 2> {log}
        mv -f "$tmp" {output}
        """

rule summarize_counts:
    input:
        expand("results/staged/{sample}.upper.txt", sample=SAMPLES)
    output:
        "results/summary/counts.tsv"
    log:
        "logs/summarize.log"
    shell:
        r"""
        set -euo pipefail
        mkdir -p results/summary logs
        tmp="{output}.tmp"
        printf "sample\tlines\n" > "$tmp"
        for f in {input}; do
          s="$(basename "$f" .upper.txt)"
          n="$(wc -l < "$f" | tr -d ' ')"
          printf "%s\t%s\n" "$s" "$n" >> "$tmp"
        done 2> {log}
        mv -f "$tmp" {output}
        """
```

This version is not advanced. It is honest.

## The evidence after repair

You can now ask much better questions and get clear answers.

Dry-run:

```bash
snakemake -n
```

After a successful clean run, the expected answer is:

```text
Nothing to be done.
```

Summary:

```bash
snakemake --summary
```

The important facts should be obvious:

- staged upper files are owned by `stage_upper`
- `results/summary/counts.tsv` is owned by `summarize_counts`
- the workflow has one clear summary output contract

DAG:

```bash
mkdir -p artifacts
snakemake --dag | dot -Tpdf > artifacts/dag.pdf
```

You should now see:

- two `stage_upper` jobs
- one `summarize_counts` job
- one `all` target

That is a workflow you can explain, not just run.

## What the learner should notice now

The repaired workflow is still tiny. That is a feature.

At this size, every improvement is visible:

- the target story is short enough to redraw
- the rerun logic is small enough to test deliberately
- the naming is specific enough to explain aloud
- the publication boundary is explicit enough to inspect after a forced failure

If a learner cannot explain the repaired version at this size, moving to a larger project
will only hide the confusion.

## What changed conceptually

```mermaid
flowchart TD
  start["Plausible first draft"] --> c1["Core 1: remove fake helper target"]
  c1 --> c2["Core 2: remove unstable rerun cause"]
  c2 --> c3["Core 3: tighten output naming and wildcard ownership"]
  c3 --> c4["Core 4: move workflow meaning into config"]
  c4 --> c5["Core 5: publish atomically and log failures"]
  c5 --> outcome["Small workflow with honest file contracts"]
```

That diagram is the real lesson of the example. Each repair made the workflow easier to
predict.

## What a strong summary sounds like

A strong summary sounds like this:

> The first draft looked acceptable, but it lied about what mattered. One helper rule was
> not part of the target graph, the summary rule changed meaning every run, staged outputs
> were named too loosely, semantic workflow data was not clearly separated from policy, and
> final outputs were written in place without reliable failure evidence. The repaired
> workflow tightened the target contract, converged after clean runs, used clearer wildcard
> ownership, validated config early, and published final outputs atomically with logs.

That summary is much better than:

> We cleaned up the Snakefile.

## What to practice after this example

Take one tiny workflow of your own and ask:

- which rule feels present but is actually irrelevant to the target graph
- which value might prevent convergence
- which path pattern is too vague
- which setting belongs in config rather than policy
- which final output is still published too early

If you can answer those five questions, Module 01 is becoming practical instead of only
theoretical.
