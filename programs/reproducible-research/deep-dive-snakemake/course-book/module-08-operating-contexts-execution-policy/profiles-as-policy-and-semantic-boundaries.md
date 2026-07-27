# Profiles as Policy and Semantic Boundaries

The first operating-context question is the most important one:

> what is allowed to change when the profile changes?

If that answer is vague, profiles become one of the easiest places to hide semantic drift.

This page is about keeping that boundary honest.

## How to use this page

Read this page with one real profile file open beside you.

Your job is not only to list settings. Your job is to classify each one:

- policy that changes how the workflow is run
- semantics that changes what the workflow means

If you cannot make that distinction line by line, the profile boundary is already too
weak for safe review.

## Profiles should change operations, not workflow meaning

A profile is a good home for operating policy such as:

- executor choice
- parallelism defaults
- printed command policy
- latency waits
- retry counts
- log visibility and operational convenience flags

Those settings affect how the workflow is run.

They should not silently change:

- the set of inputs the workflow trusts
- the meaning of the outputs it promises
- the path contract of the repository
- the scientific or analytical interpretation of the run

That distinction is the foundation of this module.

## Start by separating policy knobs from semantic knobs

The most useful beginner habit in this module is to stop calling all config-like values
"settings."

That word is too vague.

A stronger reading practice is:

1. identify executor and observability settings
2. identify retry and latency settings
3. ask whether any setting changes trusted inputs, outputs, paths, sample membership, or
   published meaning

The first two groups usually belong in profiles. The third usually does not.

## The capstone profiles are small on purpose

The capstone's `profiles/local/config.yaml`, `profiles/ci/config.yaml`, and
`profiles/slurm/config.yaml` are useful because they stay narrow.

They express operating differences such as:

- job counts
- latency waits
- shell command visibility
- failed-log visibility

That makes them easier to review as policy rather than as hidden workflow definition.

## Why this boundary matters

If switching from `profiles/local` to `profiles/ci` changes what the workflow is supposed
to produce, then the repository is no longer separating policy from semantics.

At that point:

- reviews become harder
- reproducibility claims weaken
- environment-specific behavior starts to masquerade as workflow truth

This is how “works locally” becomes a structural problem instead of a temporary annoyance.

## One useful contrast

```mermaid
flowchart LR
  profile["profile config"] --> policy["how the workflow runs"]
  snakefile["workflow contract"] --> meaning["what the workflow means"]
  policy --> execution["execution behavior"]
  meaning --> outputs["declared outputs and contracts"]
```

The point of this diagram is that policy and meaning are connected, but they are not the
same boundary.

## One concrete classification exercise

Imagine three profile changes:

1. raise `jobs` from 4 to 32
2. increase `latency-wait` for a slower shared filesystem
3. switch the published output path or sample-selection config inside the profile

The first two are often operating-policy changes.

The third is usually a semantic leak because the profile is no longer only describing how
the workflow runs. It is starting to redefine what the repository claims to produce.

That kind of comparison is how you stop profile review from becoming hand-wavy.

## A weak profile posture

Weak shape:

- a profile injects alternate paths that change workflow meaning
- a profile changes config values that alter the analytical contract
- maintainers rely on profile switching to “fix” correctness differences

This creates hidden forks of workflow behavior.

## A stronger profile posture

Stronger shape:

- keep profile settings focused on executor and operational behavior
- keep workflow meaning in visible workflow and config-contract surfaces
- review profile changes as policy changes unless they explicitly cross into semantics

Now profiles help the workflow move across contexts without pretending to redefine it.

## The beginner mistake to catch early

Beginners often think every environment-specific difference belongs in the environment's
profile.

That is false.

Some differences should trigger a harder question instead:

- why does this context need different semantic config?
- why is this path stable in one context and different in another?
- why is this output trusted only under one executor?

When a profile starts answering those questions, it is probably carrying too much meaning.

## A practical test

Ask these questions about a profile change:

1. Does this setting change only execution policy?
2. Would the trusted outputs mean the same thing after the change?
3. If this changed the workflow contract, would that fact be visible anywhere besides the profile?

If the answer to the second question is no, the profile boundary is leaking.

## Common failure modes

| Failure mode | What goes wrong | Better repair |
| --- | --- | --- |
| profile changes output or input paths | operating policy starts altering workflow meaning | keep path contracts in workflow or config surfaces, not in profiles |
| CI profile carries “special-case” semantic knobs | one context becomes a hidden alternate workflow | move semantic settings into explicit config and review them there |
| retries and waits are used to hide unstable rules | policy masks correctness issues | repair the rule or runtime instead of normalizing the symptom |
| profile files accumulate unrelated decisions | policy review becomes muddy | keep profile settings focused on execution context |
| maintainers cannot explain whether a setting is semantic | drift goes unchallenged | document the policy-versus-semantics boundary and review against it |

## What a reviewer should hear

A strong explanation sounds like this:

> These profile settings change how jobs are launched, observed, or retried, but they do
> not change trusted inputs, output meaning, or contract paths.

That is much stronger than "each environment needs its own setup," because it names the
boundary that must remain stable.

## The explanation a reviewer trusts

Strong explanation:

> these profile differences affect execution policy only: job concurrency, logging, and
> latency expectations change, but the workflow contract, inputs, and published outputs do
> not.

Weak explanation:

> the profiles are different because each environment needs its own setup.

The strong explanation names the boundary. The weak explanation leaves the boundary
unexamined.

## End-of-page checkpoint

Before leaving this page, you should be able to:

- explain what profiles should own
- explain what profiles should not silently change
- describe why profile drift can become semantic drift
- give one example of a policy change that is safe and one that is not

If you still describe profiles mainly as convenience files, pause and reframe. In this
module they are policy surfaces that must not become hidden workflow definitions.
