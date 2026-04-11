# Convergence, Rerun Causes, and Hidden Inputs

This page explains why a workflow settles down after a clean run, why some workflows rerun
forever, and why others silently miss necessary reruns.

## The sentence to keep

When a workflow reruns unexpectedly, ask:

> what tracked fact changed, or what untracked fact should have changed but the workflow
> never admitted it?

That question covers both major failure classes:

- too many reruns
- not enough reruns

## What convergence means

A small truthful workflow should settle down after it has built its requested outputs.

In practice, the simplest convergence check is:

```bash
snakemake
snakemake -n
```

After a clean successful run, the dry-run should effectively say:

```text
Nothing to be done.
```

That does not mean a workflow will never rerun again. It means:

- the current outputs match the current tracked workflow state
- Snakemake has no reason to schedule more jobs right now

Convergence is one of the most useful signs that a beginner workflow is telling the truth.

## Reruns are not automatically bad

Learners often treat reruns as evidence that Snakemake is being difficult.

That is backwards.

Reruns are good when something meaningful changed:

- an input file changed
- a tracked parameter changed
- rule code changed
- an output is incomplete or missing

What feels bad is unexplained reruns or missing reruns.

Those point to a contract problem.

## The two big failure modes

Most Module 01 rerun problems fall into two groups:

| Failure mode | What it looks like |
| --- | --- |
| non-convergence | the workflow plans jobs again even though you expected it to be settled |
| silent staleness | the workflow claims everything is up to date even though a real influence changed |

The first is noisy. The second is more dangerous because it looks calm while being wrong.

## Why non-convergence happens

The most common beginner causes are:

- unstable parameters
- code that changes meaning every run
- outputs left incomplete or poisoned by failure
- environment-dependent behavior hidden from workflow logic

The shared theme is simple:

the workflow does not present a stable story about what makes an output valid.

## A minimal non-converging example

Consider this rule:

```python
import time

rule all:
    input:
        "results/nondet.txt"

rule nondet:
    output:
        "results/nondet.txt"
    params:
        salt=lambda: time.time()
    shell:
        r"""
        mkdir -p results
        echo "{params.salt}" > {output}
        """
```

The command is not the deep problem here. The problem is that the rule meaning changes
every time the Snakefile is evaluated.

If you run:

```bash
snakemake
snakemake -n
```

you should expect the second command to plan `nondet` again instead of reporting
convergence.

That is not mysterious. The rule's tracked state is unstable.

## Why silent staleness happens

Now consider the opposite defect:

```python
MODE = os.environ.get("MODE", "default")

rule render:
    input:
        "data/input.txt"
    output:
        "results/rendered.txt"
    shell:
        r"""
        ./scripts/render.sh --mode "{MODE}" {input} > {output}
        """
```

If `MODE` changes the meaning of the output but the workflow treats it as casual hidden
state, you get a different problem:

- the output meaning changed
- the workflow may not explain the change clearly
- another person can get different results without understanding why

Whether the exact rerun behavior changes with the version and setup is less important than
the design lesson:

if something meaningfully affects the output, it should be represented in an intentional,
inspectable way.

## Hidden inputs are still inputs

Learners often think of inputs as only the paths listed under `input:`.

That is too narrow.

A hidden input can be:

- an environment variable
- a threshold embedded in Python code
- a sidecar file a shell script reads without declaring
- a catalog or manifest discovered implicitly
- a tool behavior change that the workflow never surfaces

If that thing changes output meaning, the workflow has to decide how it will be represented
and audited.

Module 01 does not require solving every advanced provenance problem. It does require
honesty.

## A better beginner habit

When an output depends on a value, choose one of these honest approaches:

- move the value into `config.yaml`
- generate a manifest file and declare it as an input
- pin the behavior in explicit rule code and accept that code changes are part of workflow
  meaning

What you should not do is let important meaning float in ambient state that nobody reviews.

## A simple example with config

Instead of this:

```python
rule summarize:
    output:
        "results/summary.txt"
    shell:
        r"""
        ./scripts/summarize.sh --threshold "$THRESHOLD" > {output}
        """
```

prefer something like this:

```python
configfile: "config/config.yaml"

THRESHOLD = config["threshold"]

rule summarize:
    output:
        "results/summary.txt"
    shell:
        r"""
        ./scripts/summarize.sh --threshold "{THRESHOLD}" > {output}
        """
```

Now the learner can point to one visible semantic source of truth.

The improvement is not just technical. It is pedagogical:

- a reader can find the meaning
- a reviewer can reason about it
- a rerun can be explained

## Incomplete outputs break trust

Another common non-convergence cause is partial or incomplete outputs after failure.

Suppose a rule writes a final output path and then crashes:

```python
rule poison:
    output:
        "results/poison.txt"
    shell:
        r"""
        mkdir -p results
        echo "partial" > {output}
        exit 1
        """
```

Now the workflow has a dangerous artifact:

- the final path exists
- the contents are not trustworthy
- later runs have to recover from a state that looks partly complete

This is one reason atomic publication matters so much. We return to it in Core 5, but it is
already part of rerun truth.

## The evidence loop for rerun questions

When rerun behavior feels wrong, use an evidence loop instead of guessing:

```bash
snakemake -n
snakemake --summary
snakemake --detailed-summary
```

The first tells you whether jobs would run.

The summary views help answer:

- which outputs exist
- which rules own them
- which outputs are missing or incomplete

If your explanation for a rerun cannot be connected back to one of those views, it is
probably still hand-wavy.

## A practical review table

| Symptom | Likely class | First review question |
| --- | --- | --- |
| reruns every dry-run | unstable tracked meaning | which param, code path, or output state changes every run |
| no rerun after a meaningful change | hidden input | what influenced the output but is not represented clearly |
| reruns after failure | incomplete or poisoned output | did a final path get published before the work was truly done |
| different behavior on different machines | ambient environment drift | which semantic choice is leaking in from host state |

This table keeps the diagnosis grounded.

## A strong explanation sounds like this

Weak explanation:

> Snakemake keeps rerunning and I do not know why.

Stronger explanation:

> The workflow does not converge because the rule's `params` value changes at parse time on
> every run, so Snakemake keeps seeing a new tracked state for `results/nondet.txt`.

Or:

> The workflow falsely appears up to date because the threshold comes from an undeclared
> environment variable, so a meaningful output influence is not represented as config or as
> another tracked input.

Those explanations teach much more than rerunning the command again.

## Failure signatures worth recognizing

### "The workflow is successful, but `snakemake -n` still wants to run jobs"

That usually means the workflow meaning is unstable or the outputs are not truly complete.

### "Changing an important option did not trigger any meaningful rebuild"

That usually means the option was a hidden semantic input.

### "The result differs between machines, but the Snakefile looks the same"

That often means ambient environment or undeclared external state is leaking into the
workflow.

### "A failed run leaves behind files that make the next run confusing"

That is a publication-truth problem as much as a failure-handling problem.

## What this page wants you to remember

Convergence is not a cosmetic check. It is evidence that the workflow currently tells a
stable truth.

If a workflow reruns forever, ask which tracked meaning keeps changing.

If it never reruns when it should, ask which real influence the workflow never admitted.

That habit will save you from a lot of mystery later in the course.
