# Determinism Is a Spectrum, Not a Switch


<!-- page-maps:start -->
## Page Maps

```mermaid
graph LR
  family["Reproducible Research"]
  program["Deep Dive DVC"]
  section["Execution Environments Reproducible Inputs"]
  page["Determinism Is a Spectrum, Not a Switch"]
  capstone["Capstone evidence"]

  family --> program --> section --> page
  page -.applies in.-> capstone
```

```mermaid
flowchart LR
  orient["Orient on the page map"] --> read["Read the main claim and examples"]
  read --> inspect["Inspect the related code, proof, or capstone surface"]
  inspect --> verify["Run or review the verification path"]
  verify --> apply["Apply the idea back to the module and capstone"]
```
<!-- page-maps:end -->

Teams often talk as if workflows are either deterministic or not.

That is usually too blunt to be useful.

Module 03 gets more accurate by treating determinism as a spectrum of control and
sensitivity.

## Why this matters

If you imagine determinism as an all-or-nothing property, you make bad diagnoses:

- small numeric drift looks like chaos
- any mismatch looks like user error
- environment strategy becomes moralized instead of engineered

A spectrum model is calmer and more honest.

## Three broad zones

| Zone | Typical situation | What it means for review |
| --- | --- | --- |
| strongly deterministic | simple sequential logic with tightly controlled inputs | divergence is usually a strong signal of a real change |
| conditionally deterministic | many ML and numerical workflows | divergence may reflect environment or execution differences rather than human error |
| inherently variable | asynchronous, hardware-sensitive, or stochastic behavior | the workflow may need declared tolerance or comparison policy rather than exact sameness |

Most real DVC workflows live in the middle zone more often than teams admit.

## A small example

Suppose two honest runs differ by a tiny metric change.

Weak interpretation:

> someone must have changed the code or the data.

Stronger interpretation:

> the workflow may be conditionally deterministic, and the environment or execution context
> may have shifted enough to change the result slightly.

That second explanation is not hand-waving. It is often the correct starting point.

## Where conditional determinism comes from

Examples include:

- floating-point reductions
- threaded numerical libraries
- GPU kernels
- ordering-sensitive file enumeration
- stochastic algorithms whose seeds or runtime behavior are only partly controlled

These do not mean the workflow is hopeless.

They mean the team needs to know what exact sameness is realistic and what evidence is
needed when results differ.

## A practical picture

```mermaid
flowchart LR
  strict["strict sameness"] --> conditional["small controlled divergence"]
  conditional --> variable["declared variability or tolerance"]
```

The point of the picture is not classification for its own sake. It is to help you choose
the right response.

## What strong response looks like

When divergence appears, ask:

1. is the workflow expected to be strongly deterministic here
2. what environment or runtime conditions could move it into conditional behavior
3. what level of difference is meaningful for this workflow

Those questions produce better engineering choices than reflexively pinning everything or
blaming the user.

## Do not call hidden drift a tolerance

The runtime audit produces an exact, deterministic difference:

```text
dot runtime:   8.00
comma runtime: 8,00
```

No randomness is involved. The hidden case stays at `8.00` after ordinary repro because
DVC cannot see the changed process variable.

This is **under-rebuild**, not conditional determinism. A tolerance would answer whether
two freshly executed results are acceptably close. It cannot justify reusing a result
produced under old runtime meaning.

Use this order:

1. prove the stage executed under each intended environment
2. compare the resulting values
3. apply a declared tolerance only if exact sameness is not required

Skipping the first step turns stale output into apparently stable output.

## Classify divergence with evidence

| Observation | Classification | Required evidence |
| --- | --- | --- |
| identical outputs under matching fingerprints | repeatable in tested context | both result and fingerprint receipts |
| different outputs under one isolated runtime change | deterministic environment influence | controlled contrast |
| bounded differences across fully executed contexts | conditional determinism candidate | repeated runs and declared tolerance |
| old output reused after hidden context change | stale semantic result | planner receipt plus current fingerprint |

The final row belongs to contract repair, not statistical tolerance design.

## Use force only as a diagnostic probe

In the hidden case, forced repro changes output from `8.00` to `8,00`. That establishes
that runtime state is causal.

It does not establish a durable execution contract:

- `dvc.yaml` remains unchanged
- the next environment change remains invisible
- the lock records what happened only after force

Force is useful here because it answers “would current runtime state change the result?”
It is not the answer to “will future stale decisions be correct?”

## Write a conditional determinism contract

When variability is real rather than stale reuse, record:

| Contract element | Example |
| --- | --- |
| governed context | Python lock hash and container digest |
| controlled runtime values | seed, thread count, locale |
| repeated-run method | three clean executions per context |
| comparison measure | absolute metric delta |
| acceptance boundary | delta no greater than `0.002` |
| escalation route | reject release and inspect runtime evidence |

The word “conditional” should point to inspectable conditions, not provide cover for an
unexplained difference.

## Why this matters for DVC specifically

DVC helps keep data, stages, and recorded state explicit.

That makes divergence easier to interpret, but it does not force the runtime world into
perfect sameness.

So you need two ideas at once:

- DVC makes important parts of the workflow more inspectable
- inspectable is not the same as mathematically identical under every runtime condition

## A helpful discipline

If a workflow is only conditionally deterministic, the team should be able to say:

- which sources of variance are expected
- which ones are unacceptable
- which environment evidence matters most when reviewing drift

That is much stronger than saying only "sometimes CI is weird."

## Keep this standard

Do not force every divergence into one of two simplistic stories:

- perfect sameness should always happen
- nothing can ever be trusted

Most real workflows need a better sentence:

> this pipeline is deterministic only under certain declared conditions, and we need to
> review those conditions honestly.
