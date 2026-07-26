# Worked Example: Auditing Local, CI, and Slurm Without Semantic Drift

This file ties the whole module together around one realistic problem:

> a repository claims that local, CI, and scheduler contexts only change operating policy, but nobody has recently proved that claim.

The question is not "do these profiles all run?" The question is whether they preserve one
semantic workflow while changing context honestly.

## The lab route

Work through the example in this order:

1. read the profile files directly and classify what they own
2. compare the same target across all contexts
3. inspect retries and latency through a failure model
4. confirm where scratch ends and trusted output begins
5. finish by injecting one semantic leak and catching it

## The starting situation

Assume you inherit a workflow with three operating contexts:

- local development
- CI
- Slurm

The repository claims these contexts change execution policy, not workflow meaning. That
claim is only trustworthy if the review route can prove it.

## Read the profile surfaces directly

Start with the profile files themselves:

- `profiles/local/config.yaml`
- `profiles/ci/config.yaml`
- `profiles/slurm/config.yaml`

These should be small enough to compare line by line. A healthy first impression is that
they mostly differ in:

- jobs or cores
- latency patience
- failed-log visibility
- executor mapping
- rerun and recovery policy

That already tells you something useful: the profiles are adjusting context rather than
trying to smuggle the whole workflow through flags.

## Compare the plans, not only the flags

Now request the same final target through all three contexts:

```sh
snakemake --profile profiles/local --dry-run
snakemake --profile profiles/ci --dry-run
snakemake --profile profiles/slurm --dry-run
```

This matters because dry-runs reveal whether policy differences preserve the same
workflow story. The right question is not only “did the profile file change?” It is:

> does the planned workflow still mean the same thing?

Normalize only volatile executor noise. Keep target names, rule names, wildcard bindings,
and declared inputs and outputs. Those are the semantic facts the audit exists to defend.

## Judge retries and latency honestly

Next, inspect any context-specific retry or latency settings.

These are not automatically good or bad. They only make sense when paired with a failure
model:

- visibility delay may justify more `latency-wait`
- transient infrastructure trouble may justify limited retries
- semantic defects or broken publication boundaries should fail fast instead

This is where operating policy becomes honest review rather than cargo-culted resilience.

## Mark where trust begins in storage

Now inspect staging and storage assumptions.

The workflow may use scratch or executor-local storage during execution, but a maintainer
must still be able to say:

- where temporary work lives
- what must happen before promotion
- when a final output becomes trusted

If a reviewer starts treating scratch output as equivalent to published output, the
repository has lost one of its most important operating boundaries.

## Inject and catch one semantic leak

Now imagine three possible profile edits:

1. the Slurm profile raises `latency-wait`
2. the CI profile changes a publish path to make artifacts easier to collect
3. the local profile raises retries after unexplained intermittent failures

These do not mean the same thing:

- the first may be a legitimate policy response
- the second is a semantic leak because trusted paths changed by context
- the third may be safe or unsafe depending on the failure class

The review route should catch the second case through dry-run or governed-profile audit
evidence instead of through memory.

## The repaired operating-context story

By the end of the audit, the repository can be described cleanly:

1. profiles own operating policy rather than workflow meaning
2. local, CI, and Slurm contexts plan the same semantic work
3. retries and latency settings are justified by named failure classes
4. scratch and promotion boundaries remain explicit
5. drift review fails when policy leaks into semantics

That is what it means to audit local, CI, and Slurm without semantic drift.

## Review questions for the repaired design

When you inspect a repository shaped like this, ask:

1. which profile differences are clearly policy and which are suspicious
2. whether the same final target means the same thing in each context
3. which retry or latency setting still lacks a failure model
4. where bytes exist before trust begins
5. which audit surface would fail first if a profile started changing semantics

If those answers are visible, the module’s context story has landed.
